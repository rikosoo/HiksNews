# 04 — Metodologia

## Bancada de laboratório

```
Laptop
   |
   |  Ground Station Simulator          prototype/ground_station/gs.py
   v
UART / radio simulation                 socket TCP exposto pela serial do QEMU
   |
   v
ARM Cortex-M board                      QEMU mps2-an385 (Cortex-M3 @ 25 MHz)
   |
   v
FreeRTOS                                kernel V11.1.0
   |
   v
CubeSat-like flight software            5 tarefas: tc_rx, adcs, eps, tm_tx, payload
   |
   v
SHERLOC / CFI monitor                   prototype/monitor/
```

O monitor **não roda no mesmo domínio do firmware**: ele consome o trace de
execução produzido pelo hardware. Na fase 1 o trace vem do QEMU (`-d exec,nochain`),
que faz o papel do stream do ARM CoreSight ETM/MTB. Um firmware comprometido não
tem como silenciar o detector.

## Fases
1. **Construir o alvo** — flight software mínimo mas realista.
2. **Injetar uma vulnerabilidade controlada** — uma só, documentada.
3. **Construir os cinco ataques** sobre essa mesma falha.
4. **Extrair o CFG** estaticamente a partir do ELF, na build.
5. **Verificar o trace** contra o modelo, fora da placa.
6. **Medir** detecção, latência, overhead e falsos positivos.

## A vulnerabilidade controlada

Uma única falha, em `tc_handle_frame()` (`prototype/firmware/src/tc.c`): o campo
`LEN` do telecomando é usado como comprimento de cópia para um buffer de pilha de
64 bytes, sem validação. O quadro de pilha, medido no binário compilado:

```
offset  0..63   ctx.buf[64]
offset 64       ctx.handler        <- alvo da chamada indireta
offset 76       r7 salvo
offset 80       LR salvo           <- vai para o PC no retorno
offset 84       (r7 do gadget)
offset 88       (PC do gadget)     <- segundo estágio do ROP
```

Todos os cinco ataques atravessam essa mesma falha — o que isola a variável: o
que muda entre eles é **o tipo de desvio de fluxo**, não o bug de entrada.

## Os cinco ataques controlados

| ID | Ataque | Mecanismo | Alvo alcançado |
|---|---|---|---|
| **ATK-1** | Buffer overflow | sobrescreve o LR salvo (offset 80) | `eps_kill_switch()` |
| **ATK-2** | Function pointer corruption | sobrescreve `ctx.handler` (offset 64) | `payload_wipe()` |
| **ATK-3** | ROP / control-flow hijacking | cadeia de 2 estágios via gadget `pop {r7, pc}` | `payload_wipe()` |
| **ATK-4** | Malicious task scheduling | desvia para hook de debug esquecido na imagem | task rogue acima do ADCS |
| **ATK-5** | Unauthorized privileged function | entra no corpo de `priv_raw_write()` pulando a checagem de auth | escrita privilegiada sem autenticação |

Notas sobre a escolha dos alvos:

- **ATK-4** usa `debug_spawn_rogue_task()`, uma rotina de fábrica/teste que ficou
  na imagem e nunca é chamada em voo. Isso não é artificial: código de bringup
  esquecido no binário é um achado comum em firmware embarcado. A task criada
  roda acima da prioridade do ADCS e **mata o laço de controle de atitude** — o
  efeito é perda de apontamento, não apenas execução de código.
- **ATK-5** não chama `priv_raw_write()`: entra direto em
  `priv_raw_write_body()`, pulando a checagem `g_tc_authenticated`. É um bypass
  de autenticação que aparece no trace como uma aresta que o CFG não permite.

## Cenários

| ID | Cenário | Resultado esperado |
|---|---|---|
| S0 | Telecomandos válidos | Nenhum alerta |
| S1 | Telecomandos malformados, rejeitados pelo parser | Nenhum alerta |
| S4 | Carga sustentada (100 telecomandos) | Nenhum alerta |
| ATK-1..5 | Os cinco ataques acima | Detecção |
| S5 | Corrupção de dados sem desvio de fluxo | **Não detectado** — limitação declarada |

S5 é deliberado: delimita honestamente o que a técnica não cobre.

## Reprodutibilidade

```bash
cd prototype
./tools/fetch_deps.sh          # FreeRTOS V11.1.0 (pinado)
make -C firmware               # arm-none-eabi-gcc 13.2
python3 eval/run_scenario.py ATK-1
python3 eval/run_matrix.py --out out/results.md
```

Toolchain usada nas medições publicadas: `arm-none-eabi-gcc 13.2.1`,
QEMU 8.2.2, FreeRTOS Kernel V11.1.0, Python 3 (sem dependências externas —
a desmontagem sai do `objdump`).
