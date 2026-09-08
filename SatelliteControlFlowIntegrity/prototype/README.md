# Protótipo

Ambiente experimental do artigo. Nada aqui é executado contra sistema real:
firmware próprio, rodando em QEMU ou em placa de desenvolvimento.

## Diretórios
| Pasta | Conteúdo |
|---|---|
| `firmware/` | Flight software: FreeRTOS + 5 tarefas + parser de telecomando |
| `ground_station/` | Cliente que envia telecomandos válidos e malformados |
| `attacks/` | PoCs de control-flow hijacking (S2, S3) |
| `monitor/` | Extrator de CFG a partir do ELF + verificador de trace |
| `eval/` | Scripts dos cenários S0–S5 e coleta de métricas |

## Toolchain pretendida
- `arm-none-eabi-gcc` (versão a fixar)
- FreeRTOS Kernel (versão a fixar)
- QEMU `qemu-system-arm`, máquina `mps2-an385`
- Python 3 para o monitor (`capstone`/`pyelftools` para desmontagem e CFG)

> Versões exatas serão travadas quando a primeira build funcionar, para garantir
> reprodutibilidade dos resultados.

## Estado
Esqueleto. Ainda sem código — ver o roadmap no README principal.
