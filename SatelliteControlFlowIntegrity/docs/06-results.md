# Resultados / Results

Gerado por `eval/run_matrix.py` | firmware: `flight.elf` | CPU: Cortex-M3 @ 25 MHz (QEMU mps2-an385)


## Por cenário / Per scenario

| Cenário | Descrição | Comprometido | Violações | Detectado | Latência (instr) | Latência (ms) |
|---|---|---|---|---|---|---|
| S0 | Nominal telecommands | não | 0 | n/a | — | — |
| S1 | Malformed telecommands (rejected) | não | 0 | n/a | — | — |
| S4 | Sustained nominal load | não | 0 | n/a | — | — |
| ATK-1 | Buffer overflow | sim | 1 | SIM | 1230 | 0.0492 |
| ATK-2 | Function pointer corruption | sim | 1 | SIM | 26 | 0.0010 |
| ATK-3 | ROP / control-flow hijacking | sim | 2 | SIM | 1303 | 0.0521 |
| ATK-4 | Malicious task scheduling | sim | 1 | SIM | 1230 | 0.0492 |
| ATK-5 | Unauthorized privileged function | sim | 2 | SIM | 1230 | 0.0492 |
| S5 | Data-only attack (no CF deviation) | sim | 0 | NÃO | — | — |

## Métricas agregadas / Summary metrics

| Métrica | Valor |
|---|---|
| Attack detection | 5/5 (100%) |
| False positives (S0, S1, S4) | 0 |
| S5 — Data-only attack (no CF deviation) | comprometido=sim, violações=0 → **fora do alcance da técnica** |
| Detection latency | 26–1303 instr (0.0010–0.0521 ms @ 25 MHz) |
| CPU overhead (on board) | 0% — o firmware não é instrumentado |
| Flash overhead (on board) | 0 KB — nenhum código adicionado à imagem |
| Memory overhead (on board) | 0 KB — nenhuma estrutura em RAM de voo |
| Modelo de CFG (lado do monitor) | 939.7 KB |
| Extração do modelo (build time) | 0.3 s |
| Volume de trace analisado | 2588 MB |
| Tempo de análise | 83 s |

## Leitura dos números

O overhead de bordo é **zero por construção**: o detector não instrumenta o
firmware, ele consome o trace que o hardware já produz. O custo não desaparece —
migra para a banda do canal de trace e para os recursos do monitor. Essa é a
troca central da abordagem, e é o que a torna plausível sob orçamento de energia
e prazo de tempo real de um satélite.

A latência de detecção é medida entre a escrita que corrompe a pilha (retorno de
`tc_copy`) e o primeiro desvio ilegal observado. Ela é menor que o intervalo do
laço de ADCS (10 ms), o que significa que há margem para uma resposta antes do
próximo ciclo de controle.
