# 03 — Arquitetura

## Sistema alvo (implementado)
- **MCU:** ARM Cortex-M3 @ 25 MHz, emulado em QEMU (`mps2-an385`) na fase 1; placa real na fase 2.
- **RTOS:** FreeRTOS Kernel V11.1.0, `configMAX_PRIORITIES = 6`, tick de 1 kHz.
- **Imagem:** 23 KB de texto, 33 KB de BSS.
- **Tarefas:**
  | Tarefa | Prioridade | Período | Papel |
  |---|---|---|---|
  | `tc_rx` | 4 | polling 2 ms | recebe e faz parsing de telecomandos |
  | `adcs` | 3 | 10 ms | laço de controle de atitude |
  | `eps` | 2 | 5 s | monitoramento de energia |
  | `tm_tx` | 1 | 2 s | monta e envia telemetria (beacon) |
  | `payload` | 1 | 50 ms | tarefa de carga útil |

  A prioridade 5 fica livre em voo — é justamente o degrau que o ATK-4 ocupa
  para starvar o ADCS.

## Formato de telecomando (simplificado)
```
+--------+--------+--------+-------------------+
| SYNC   | APID   | LEN    | PAYLOAD (LEN B)   |
| 2 B    | 1 B    | 1 B    | 0..255 B          |
| EB 90  |        |        |                   |
+--------+--------+--------+-------------------+
```

APIDs válidos: `0x10` ADCS mode, `0x20` TM beacon, `0x30` EPS report,
`0x40` payload capture. Não há CRC nem autenticação: o modelo de ameaças
(`01-threat-model.md`, capacidade A4) assume que o atacante já passou dessa
fronteira, então adicioná-la não mudaria nada no experimento — só esconderia o
que está sendo medido.

A vulnerabilidade controlada mora na cópia do `PAYLOAD` para um buffer de pilha
de 64 bytes, sem validar `LEN`. Uma só falha, documentada em
`04-methodology.md`, que serve de porta para os cinco ataques.

## Monitor de fluxo de controle

### Fase offline (build time)
1. Compila o firmware com informação de símbolos.
2. Extrai o **CFG** do ELF (desmontagem + resolução de alvos diretos).
3. Resolve chamadas indiretas por tabela de comandos (conjunto permitido explícito).
4. Emite um **modelo de política**: conjunto de arestas `(origem, destino)` válidas.

### Fase online (runtime)
0. Fonte de trace: hoje o log de blocos do QEMU (`-d exec,nochain`), que faz o
   papel do stream do ETM/MTB. O `nochain` é obrigatório: com encadeamento de
   blocos ligado o QEMU deixa de registrar execuções e o trace fica incompleto.
1. Consome o trace — sequência de blocos executados.
2. Reconstrói as transições executadas.
3. Verifica cada aresta contra o modelo.
4. Em violação: gera evento com contexto (função de origem, PC de origem,
   destino ilegal, instante estimado).

Duas classes de transição são aceitas incondicionalmente, e é importante
declará-las porque são um buraco real na cobertura, não um detalhe de
implementação:

- **entrada de exceção** — o destino é uma entrada da tabela de vetores;
- **retorno de exceção** — o PC restaurado pelo hardware não está no modelo.

Uma terceira, **reentrada de bloco**, é artefato do emulador: o QEMU abandona um
bloco quando chega uma interrupção e o reexecuta do início. O ETM real emite um
pacote de exceção explícito e o caso não existe.

### Resposta a incidente (específica do domínio)
| Nível | Ação |
|---|---|
| L0 | Registra evento em telemetria de segurança |
| L1 | Quarentena do subsistema afetado |
| L2 | Entrada em *safe mode* (atitude estável, rádio ativo, payload desligado) |
| L3 | Reinício controlado a partir de imagem confiável |

A escolha do nível é **política de missão**, não do detector — princípio
importante porque um falso positivo que dispara L3 tem custo operacional real.
