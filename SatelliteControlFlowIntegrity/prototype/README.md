# Protótipo

Ambiente experimental do artigo. Nada aqui é executado contra sistema real:
firmware escrito por nós, rodando em QEMU.

## Bancada

```
Laptop -> Ground Station Simulator -> UART/radio sim (socket TCP)
       -> ARM Cortex-M3 (QEMU mps2-an385) -> FreeRTOS V11.1.0
       -> CubeSat-like flight software -> CFI monitor (fora da placa)
```

## Requisitos

| Ferramenta | Versão usada nas medições |
|---|---|
| `arm-none-eabi-gcc` | 13.2.1 |
| `qemu-system-arm` | 8.2.2 |
| FreeRTOS Kernel | V11.1.0 (pinado em `tools/fetch_deps.sh`) |
| Python | 3.11+, sem dependências externas |

## Uso

```bash
./tools/fetch_deps.sh          # baixa o kernel do FreeRTOS
make -C firmware               # compila flight.elf
make -C firmware run           # boot interativo no terminal

python3 eval/run_scenario.py S0        # voo nominal
python3 eval/run_scenario.py ATK-3     # ROP chain
python3 eval/run_matrix.py --out out/results.md   # matriz completa
```

`run_matrix.py` apaga cada trace assim que o consome: um segundo de voo emulado
gera ~200 MB de trace bruto.

## Diretórios

| Pasta | Conteúdo |
|---|---|
| `firmware/` | Flight software: 5 tarefas FreeRTOS + parser de telecomando vulnerável |
| `ground_station/` | `gs.py` — protocolo de telecomando e link simulado |
| `attacks/` | `attacks.py` — ATK-1..ATK-5 sobre a mesma vulnerabilidade |
| `monitor/` | `cfg_extract.py` (build time) e `cfi_monitor.py` (runtime) |
| `eval/` | `run_scenario.py` e `run_matrix.py` |
| `tools/` | `fetch_deps.sh` |

## Alvos críticos no firmware

Funções inalcançáveis por qualquer caminho legítimo de telecomando. Existem só
para servir de alvo mensurável:

| Função | Consequência simulada |
|---|---|
| `eps_kill_switch()` | desliga o barramento de energia |
| `payload_wipe()` | apaga a memória da carga útil |
| `debug_spawn_rogue_task()` | cria task acima da prioridade do ADCS |
| `priv_raw_write_body()` | escrita privilegiada sem autenticação |

## A vulnerabilidade

Uma só, em `firmware/src/tc.c`, marcada no código como
`CONTROLLED VULNERABILITY`: o campo `LEN` do telecomando é usado sem validação
como comprimento de cópia para `ctx.buf[64]` na pilha.

O firmware é compilado com `-O0 -fno-stack-protector` de propósito: o layout de
pilha precisa ser estável e a falha precisa continuar alcançável para que as
medições sejam reproduzíveis.
