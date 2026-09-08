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

### 1. Sistema alvo — "computador de bordo"

```
Ground Station
       |
       | comando (TC / telecomando)
       v
Communication module (UART / RF simulado)
       |
       v
ARM Cortex-M
       |
       v
FreeRTOS
       |
       v
Satellite flight software
       |
       v
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
├── README.md                  <- este arquivo
├── Portuguese/
│   └── artigo.md              <- artigo completo (PT-BR)
├── English/
│   └── article.md             <- full article (EN)
├── docs/
│   ├── 01-threat-model.md     <- modelo de ameaças e superfície de ataque
│   ├── 02-related-work.md     <- SHERLOC, CFI, atestação remota, SPARTA
│   ├── 03-architecture.md     <- projeto do monitor e do sistema alvo
│   ├── 04-methodology.md      <- como o experimento é conduzido
│   └── 05-evaluation.md       <- métricas, resultados e limitações
├── prototype/
│   ├── firmware/              <- flight software (FreeRTOS, Cortex-M)
│   ├── ground_station/        <- envio de telecomandos e fuzzing de pacotes
│   ├── attacks/               <- PoCs de hijacking controlado
│   ├── monitor/               <- extrator de CFG + verificador de trace
│   └── eval/                  <- scripts de medição e datasets
└── assets/                    <- diagramas e figuras
```

---

## 🗺️ Roadmap

- [x] Definir pergunta de pesquisa e escopo
- [x] Estrutura do repositório e esqueleto do artigo
- [ ] Modelo de ameaças formalizado (docs/01)
- [ ] Revisão de literatura consolidada (docs/02)
- [ ] Firmware alvo mínimo: 4 tarefas FreeRTOS + parser de telecomando
- [ ] Vulnerabilidade controlada e PoC de hijacking reproduzível
- [ ] Extração estática de CFG a partir do ELF
- [ ] Monitor consumindo trace (QEMU primeiro, hardware depois)
- [ ] Avaliação: detecção, falsos positivos, overhead, custo energético
- [ ] Redação final PT-BR + EN

---

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
