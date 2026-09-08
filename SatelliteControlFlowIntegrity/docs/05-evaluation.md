# 05 — Avaliação

Resultados medidos na bancada descrita em `04-methodology.md`.
A tabela bruta gerada pelo harness fica em `06-results.md`
(`prototype/eval/run_matrix.py --out out/results.md`).

## Métricas

| Métrica | Valor medido | Como foi obtida |
|---|---|---|
| **Attack detection** | **5/5 (100%)** | ATK-1..5, uma execução completa cada |
| **False positives** | **0** | S0, S1 e S4 — 1,4 M de blocos executados sem alerta |
| **Detection latency** | **26 – 1379 instruções (0,001 – 0,055 ms @ 25 MHz)** | da escrita que corrompe a pilha até a primeira aresta ilegal |
| **CPU overhead (bordo)** | **0%** | o firmware não é instrumentado |
| **Flash overhead (bordo)** | **0 KB** | nenhum código adicionado à imagem |
| **Memory overhead (bordo)** | **0 KB** | nenhuma estrutura em RAM de voo |
| Modelo de CFG (lado do monitor) | 929 KB | JSON não comprimido, 9.716 instruções |
| Extração do modelo (build time) | 0,2 s | uma vez por build |
| Throughput do monitor | ~34 MB de trace/s | 2,4 GB analisados em 69 s |

## Por cenário

| Cenário | Comprometido | Violações | Detectado | Latência (instr) | Latência (ms) |
|---|---|---|---|---|---|
| S0 — telecomandos nominais | não | 0 | n/a | — | — |
| S1 — malformados, rejeitados | não | 0 | n/a | — | — |
| S4 — carga sustentada | não | 0 | n/a | — | — |
| ATK-1 — buffer overflow | sim | 1 | **SIM** | 1301 | 0,0520 |
| ATK-2 — function pointer | sim | 1 | **SIM** | 26 | 0,0010 |
| ATK-3 — ROP | sim | 2 | **SIM** | 1379 | 0,0552 |
| ATK-4 — task scheduling | sim | 1 | **SIM** | 1303 | 0,0521 |
| ATK-5 — função privilegiada | sim | 2 | **SIM** | 1303 | 0,0521 |

ATK-3 e ATK-5 produzem duas violações porque o desvio tem dois estágios (o
gadget e o alvo final; a entrada no corpo privilegiado e o seu retorno). São
arestas do mesmo ataque, não alertas independentes.

## Leitura dos resultados

**O overhead de bordo é zero por construção — e esse é o resultado central.**
O detector não instrumenta o firmware; ele consome o trace que o hardware já
produz. Num satélite, onde flash e RAM são fixados antes do lançamento e cada
ciclo de CPU tem custo energético e térmico, um esquema de CFI que cobra 0 KB e
0% de CPU na placa é qualitativamente diferente de um que cobra 5–15%.

O custo não desaparece: migra para a **banda do canal de trace** e para os
recursos do monitor. Um segundo de voo emulado gerou ~200 MB de trace bruto do
QEMU. É a limitação prática mais séria da abordagem e está discutida abaixo.

**A latência cabe no orçamento de tempo real.** O pior caso medido (0,055 ms) é
cerca de 180× menor que o período do laço de ADCS (10 ms). Existe folga para
disparar uma resposta antes do próximo ciclo de controle de atitude — que é o
que separa "detectar" de "conter".

**ATK-2 é detectado 50× mais rápido** que os demais (26 instruções contra ~1300):
a corrupção do ponteiro de função é usada imediatamente na chamada indireta,
enquanto os ataques de retorno só disparam quando a função retorna, depois do
handler legítimo ter rodado.

**Zero falso positivo em 1,4 M de blocos** é encorajador, mas o firmware é
pequeno e a carga é sintética. Não se deve extrapolar para um flight software
real sem repetir a medição.

## Limitações

- **Ataques apenas de dados (S5) escapam por construção.** Corromper um valor de
  telemetria ou um setpoint do ADCS sem desviar o fluxo é invisível para o
  detector. Isso não é um defeito de implementação: é a fronteira da técnica.
- **Volume de trace.** ~200 MB/s de trace do QEMU é inviável para downlink. Em
  hardware real o ETM comprime agressivamente e o MTB só guarda uma janela
  circular, mas a questão de quanto trace cabe no orçamento de banda continua
  aberta e é o próximo item experimental.
- **Chamadas indiretas exigem CFG conservador.** O conjunto de alvos permitidos
  é aproximado pelas funções cujo endereço aparece na imagem — mais permissivo
  que o conjunto real.
- **Artefatos do emulador.** O QEMU reinicia um bloco quando chega uma
  interrupção, o que o monitor precisa tratar explicitamente; e o encadeamento
  de blocos (`nochain` desligado) omite execuções. Nenhum dos dois existe no ETM
  real, mas ambos afetam a comparabilidade dos números.
- **Energia não foi medida, foi argumentada.** Sem instrumentação de bordo o
  consumo adicional na placa é zero; o consumo do canal de trace precisa de
  medição em hardware.
- **Radiação.** Um SEU pode desviar o fluxo de controle sem qualquer adversário.
  O detector sinaliza os dois casos de forma idêntica. Distinguir ataque de
  falha de hardware exige correlação com outra fonte (contadores de ECC,
  histórico de órbita) e está fora do escopo deste protótipo.

## Ameaças à validade

- Firmware pequeno (23 KB de texto) e escrito por nós: o CFG é mais simples e
  mais preciso do que o de um flight software real.
- Cortex-M3 emulado a 25 MHz; a conversão de instruções para milissegundos
  assume 1 instrução por ciclo, o que subestima o tempo real no Cortex-M3.
- Uma execução por cenário. Números de latência devem ser lidos como ordem de
  grandeza, não como média de uma distribuição.
