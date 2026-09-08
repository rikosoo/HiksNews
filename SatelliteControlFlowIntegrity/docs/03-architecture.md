# 03 — Arquitetura

## Sistema alvo
- **MCU:** ARM Cortex-M (M3/M4), emulado em QEMU (`mps2-an385` ou similar) na fase 1; placa real na fase 2.
- **RTOS:** FreeRTOS.
- **Tarefas:**
  | Tarefa | Prioridade | Papel |
  |---|---|---|
  | `tc_rx` | alta | recebe e faz parsing de telecomandos |
  | `adcs` | alta | laço de controle de atitude |
  | `eps` | média | monitoramento de energia |
  | `tm_tx` | baixa | monta e envia telemetria |
  | `payload` | baixa | tarefa de carga útil |

## Formato de telecomando (simplificado)
```
+--------+--------+---------+-------------------+--------+
| SYNC   | APID   | LEN     | PAYLOAD (LEN B)   | CRC16  |
| 2 B    | 2 B    | 2 B     | variavel          | 2 B    |
+--------+--------+---------+-------------------+--------+
```
A vulnerabilidade controlada mora na cópia do `PAYLOAD` para um buffer de pilha
de tamanho fixo, sem validar `LEN` contra o tamanho do buffer.

## Monitor de fluxo de controle

### Fase offline (build time)
1. Compila o firmware com informação de símbolos.
2. Extrai o **CFG** do ELF (desmontagem + resolução de alvos diretos).
3. Resolve chamadas indiretas por tabela de comandos (conjunto permitido explícito).
4. Emite um **modelo de política**: conjunto de arestas `(origem, destino)` válidas.

### Fase online (runtime)
1. Consome o trace de hardware (ETM/MTB) — sequência de branches tomados.
2. Reconstrói as transições executadas.
3. Verifica cada aresta contra o modelo.
4. Em violação: gera evento com contexto (tarefa, PC de origem, destino ilegal).

### Resposta a incidente (específica do domínio)
| Nível | Ação |
|---|---|
| L0 | Registra evento em telemetria de segurança |
| L1 | Quarentena do subsistema afetado |
| L2 | Entrada em *safe mode* (atitude estável, rádio ativo, payload desligado) |
| L3 | Reinício controlado a partir de imagem confiável |

A escolha do nível é **política de missão**, não do detector — princípio
importante porque um falso positivo que dispara L3 tem custo operacional real.
