# 05 — Avaliação

## Métricas
| Métrica | Definição | Por que importa no espaço |
|---|---|---|
| Taxa de detecção | % dos cenários de hijacking detectados | Eficácia bruta |
| Falsos positivos | Alertas em operação nominal (S0, S4) | Um FP pode disparar *safe mode* e custar dias de missão |
| Latência de detecção | Instruções entre o desvio e o alerta | Define se dá para bloquear antes da ação crítica |
| Overhead de CPU | % de tempo adicionado ao ciclo do RTOS | Compete com o laço de controle do ADCS |
| Memória adicional | Flash + RAM do modelo de CFG | Recurso escasso e fixo pós-lançamento |
| Custo energético estimado | mJ por hora de monitoramento | Orçamento de energia é restrição dura |
| Impacto no determinismo | Jitter introduzido nos prazos das tarefas | Perda de prazo no ADCS é falha de missão |

## Formato de resultado (a preencher)
| Cenário | Detectado | Latência (instr.) | FP |
|---|---|---|---|
| S0 | — | — | |
| S1 | — | — | |
| S2 | — | — | |
| S3 | — | — | |
| S4 | — | — | |
| S5 | — | — | |

## Limitações previstas
- **Ataques apenas de dados** (S5) não alteram o fluxo e escapam por construção.
- Chamadas indiretas exigem CFG conservador — reduz precisão.
- Buffers de trace pequenos (MTB) podem perder eventos sob carga alta.
- Avaliação de energia em QEMU é estimativa, não medição.
- Radiação e SEU podem produzir desvios de fluxo **não adversariais**: o detector
  não distingue ataque de falha de hardware — e isso é uma discussão relevante,
  não um defeito escondido.
