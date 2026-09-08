# 🛰️ Control-Flow Violation Detection for Embedded Satellite Flight Software

> **Pergunta de pesquisa**
> É possível adaptar técnicas semelhantes ao **SHERLOC** para detectar ataques de
> *control-flow hijacking* contra firmware de sistemas espaciais embarcados?

Este diretório reúne o artigo, o modelo de ameaças e o protótipo de um
**monitor de integridade de fluxo de controle (CFI)** para software de voo de
satélites baseados em **ARM Cortex-M + FreeRTOS**, usando **trace de hardware**
(ETM / MTB / Micro Trace Buffer) como fonte de evidência.

---

## 📌 Motivação

Satélites pequenos (CubeSats, constelações LEO) rodam firmware em
microcontroladores com recursos severamente limitados:

| Restrição | Impacto na defesa |
|---|---|
| RAM na casa de dezenas/centenas de KB | Inviabiliza shadow stacks grandes e instrumentação pesada |
| Sem MMU (apenas MPU, quando existe) | Isolamento fraco entre tarefas do RTOS |
| Orçamento de energia rígido | Overhead de CPU tem custo térmico e elétrico real |
| Janela de contato curta com a estação | Resposta a incidente é lenta ou impossível em tempo real |
| Atualização de firmware cara e arriscada | Correção pós-incidente pode levar meses |

Nesse contexto, **detectar** o desvio de fluxo de controle no momento em que ele
acontece vale mais do que remediar depois. É exatamente a lacuna que o SHERLOC
ataca em IoT — e que este trabalho leva para o domínio espacial.

---

## 🧩 Arquitetura do protótipo

### 1. Bancada de laboratório

```
Laptop
   |
   |  Ground Station Simulator
   v
UART / radio simulation
   |
   v
ARM Cortex-M board
   |
   v
FreeRTOS
   |
   v
CubeSat-like Flight Software
   |
   v
SHERLOC / CFI monitor
```

Concretamente, hoje: `gs.py` no laptop conversa por socket TCP com a serial do
QEMU (`mps2-an385`, Cortex-M3 @ 25 MHz), que roda FreeRTOS V11.1.0 e cinco
tarefas de voo — `tc_rx`, `adcs`, `eps`, `tm_tx`, `payload`. O monitor consome o
trace de execução **fora** do domínio do firmware.

```
+--------------+
| ADCS         |  controle de atitude
| Telemetry    |  telemetria (TM)
| Power        |  gerenciamento de energia / EPS
| Payload      |  carga útil
+--------------+
```

### 2. Cadeia de ataque (vulnerabilidade controlada)

```
Ground station envia pacote
            |
            v
    parsing vulneravel
            |
            v
     buffer overflow
            |
            v
  return address alterado
            |
            v
  control-flow hijacking
            |
            v
  funcao critica executada
```

Exemplo de "função crítica" abusada: acionamento de *thrusters*, desligamento do
subsistema de energia, apagamento de memória de payload ou desativação da
telemetria — ações que, num satélite real, são irreversíveis.

### 3. Defesa proposta

```
        Firmware
            |
            v
      hardware trace  (ETM / MTB)
            |
            v
  Control-flow monitor  (modelo de CFG + politica)
            |
            v
   comportamento esperado?
       /            \
     SIM             NAO
      |               |
   continua      alerta / bloqueia
                 (+ telemetria de seguranca)
```

O monitor **não instrumenta o firmware**: ele consome o trace produzido pelo
hardware e compara transições observadas contra um **grafo de fluxo de controle
(CFG)** extraído estaticamente na fase de build. Isso preserva o timing
determinístico exigido pelo RTOS.

---

## 💥 Os cinco ataques controlados

Todos atravessam **a mesma vulnerabilidade injetada** — o campo `LEN` do
telecomando usado sem validação como comprimento de cópia para um buffer de
pilha de 64 bytes em `tc_handle_frame()`. O que muda entre eles é o tipo de
desvio de fluxo, não o bug de entrada.

| ID | Ataque | Mecanismo | Efeito a bordo |
|---|---|---|---|
| ATK-1 | Buffer overflow | sobrescreve o LR salvo | `eps_kill_switch()` — barramento desligado |
| ATK-2 | Function pointer corruption | sobrescreve o ponteiro de dispatch | `payload_wipe()` |
| ATK-3 | ROP / control-flow hijacking | cadeia de 2 estágios via `pop {r7, pc}` | `payload_wipe()` |
| ATK-4 | Malicious task scheduling | hook de debug esquecido na imagem | task rogue acima do ADCS — apontamento perdido |
| ATK-5 | Unauthorized privileged function | entra no corpo pulando a checagem de auth | escrita privilegiada sem autenticação |

## 📊 Resultados medidos

| Métrica | Valor |
|---|---|
| **Attack detection** | **5/5 — 100%** |
| **False positives** | **0** (1,4 M de blocos em S0, S1 e S4) |
| **Detection latency** | **0,001 – 0,055 ms** (26 – 1379 instruções @ 25 MHz) |
| **CPU overhead (bordo)** | **0%** |
| **Flash overhead (bordo)** | **0 KB** |
| **Memory overhead (bordo)** | **0 KB** |
| Modelo de CFG (monitor) | 929 KB |
| Throughput do monitor | ~34 MB de trace/s |

O overhead de bordo é zero **por construção**: o firmware não é instrumentado, o
monitor consome o trace que o hardware já produz. O custo migra para a banda do
canal de trace — que é a limitação prática mais séria e está discutida em
`docs/05-evaluation.md`. Tabela completa em `docs/06-results.md`.

## ▶️ Como reproduzir

```bash
cd prototype
./tools/fetch_deps.sh              # FreeRTOS V11.1.0 (pinado)
make -C firmware                   # arm-none-eabi-gcc

python3 eval/run_scenario.py S0    # voo nominal
python3 eval/run_scenario.py ATK-1 # ataque: veja a missão ser perdida
python3 eval/run_matrix.py --out out/results.md   # matriz completa + métricas
```

Requisitos: `arm-none-eabi-gcc`, `qemu-system-arm` e Python 3. O monitor não tem
dependências externas — a desmontagem vem do `objdump`.

## 🔬 Relação com o SHERLOC — e o que há de novo

| Eixo | SHERLOC (IoT) | Este trabalho (espaço) |
|---|---|---|
| Alvo | Firmware IoT em Cortex-M | Software de voo de satélite sobre FreeRTOS |
| Fonte de evidência | Trace de hardware | Trace de hardware (mesma classe) |
| Modelo de ameaça | Atacante local/rede | Estação de solo comprometida, uplink hostil, cadeia de suprimentos |
| Resposta | Alerta / parada | Modo seguro (*safe mode*), quarentena de subsistema, telemetria de segurança |
| Restrição dominante | Custo e memória | Energia, radiação, janela de contato, irreversibilidade |

**Contribuição pretendida:** transpor a detecção de violação de fluxo de controle
para um modelo de ameaças espacial, onde a resposta a incidentes não pode
depender de intervenção humana imediata.

---

## 📂 Estrutura do diretório

```
SatelliteControlFlowIntegrity/
├── README.md
├── Portuguese/artigo.md        <- artigo completo (PT-BR)
├── English/article.md          <- full article (EN)
├── docs/
│   ├── 01-threat-model.md      <- modelo de ameaças e superfície de ataque
│   ├── 02-related-work.md      <- SHERLOC, CFI, atestação remota, SPARTA
│   ├── 03-architecture.md      <- projeto do monitor e do sistema alvo
│   ├── 04-methodology.md       <- bancada, vulnerabilidade e os 5 ataques
│   ├── 05-evaluation.md        <- métricas, resultados e limitações
│   └── 06-results.md           <- tabela bruta gerada pelo harness
└── prototype/
    ├── firmware/               <- flight software: FreeRTOS + 5 tarefas + parser
    ├── ground_station/gs.py    <- simulador da estação de solo
    ├── attacks/attacks.py      <- ATK-1..ATK-5
    ├── monitor/
    │   ├── cfg_extract.py      <- ELF -> modelo de fluxo de controle (build time)
    │   └── cfi_monitor.py      <- trace -> detecção de violação (runtime)
    ├── eval/
    │   ├── run_scenario.py     <- executa um cenário de ponta a ponta
    │   └── run_matrix.py       <- matriz completa + tabela de métricas
    └── tools/fetch_deps.sh
```

---

## 🗺️ Roadmap

- [x] Definir pergunta de pesquisa e escopo
- [x] Estrutura do repositório e esqueleto do artigo
- [x] Firmware alvo: 5 tarefas FreeRTOS + parser de telecomando em QEMU
- [x] Vulnerabilidade controlada e os 5 ataques reproduzíveis
- [x] Extração estática de CFG a partir do ELF
- [x] Monitor consumindo trace de execução
- [x] Primeira rodada de avaliação (detecção, FP, latência, overhead)
- [ ] Modelo de ameaças formalizado (docs/01)
- [ ] Revisão de literatura consolidada (docs/02)
- [ ] Cenário S5 (ataque só de dados) implementado como limite declarado
- [ ] Repetições múltiplas por cenário, com distribuição de latência
- [ ] Porte para hardware real com ETM/MTB e medição de energia
- [ ] Redação final PT-BR + EN

## ⚖️ Escopo ético

Todo o trabalho ocorre em **firmware escrito por nós**, executado em emulador
(QEMU) ou em placa de desenvolvimento própria. Não há alvo real, satélite em
órbita, operador ou estação de solo de terceiros envolvidos. As vulnerabilidades
são **introduzidas deliberadamente** para servir de alvo de medição — nenhuma
falha de produto de terceiros é explorada ou divulgada aqui.

---

## 📚 Referências iniciais

- SHERLOC — detecção de violação de fluxo de controle em firmware embarcado via trace de hardware
- Abadi et al., *Control-Flow Integrity* (CCS 2005)
- MITRE **SPARTA** — Space Attack Research & Tactic Analysis
- CCSDS — padrões de telecomando/telemetria e segurança
- NIST SP 800-53 / IR 8270 (cibersegurança para operações espaciais)
- ARM CoreSight ETM / MTB — documentação de trace em Cortex-M

> As referências serão fechadas com citação completa em `docs/02-related-work.md`.

---

## 🤝 Contribuições

Ideias, críticas ao modelo de ameaças e sugestões de referência são bem-vindas
via issues ou pull requests.
