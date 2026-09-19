# 01 — Modelo de ameaças

## Ativos protegidos
| Ativo | Por que importa |
|---|---|
| Integridade do fluxo de controle do flight software | Um desvio já é execução de código do atacante |
| ADCS (controle de atitude) | Perda de apontamento = perda de link e de energia |
| EPS (energia) | Desligamento indevido pode ser terminal |
| Telemetria | É o único canal de observabilidade da missão |
| Payload | Objetivo científico/comercial da missão |

## Atacante — capacidades assumidas
- **A1. Uplink hostil:** consegue injetar telecomandos malformados (estação de solo comprometida, spoofing de RF, ou operador legítimo abusado).
- **A2. Conhecimento do firmware:** conhece o binário (COTS, código aberto, ou vazamento da cadeia de suprimentos).
- **A3. Sem acesso físico em órbita:** não pode reprogramar via JTAG após o lançamento.
- **A4. Sem quebra de cripto:** assume-se que a autenticação de telecomando, quando existe, é a fronteira — o ataque acontece *depois* do parsing.

## Fora de escopo
- Ataques físicos (laser, jamming puro, SEU induzido por radiação sem intenção adversarial).
- Comprometimento da estação de solo em si (é premissa, não alvo).
- Canais laterais e extração de chave.

## Superfície de ataque priorizada
1. Parser de telecomando (deserialização de pacote de tamanho variável) — **alvo do protótipo**.
2. Handlers de subsistema chamados por ponteiro de função (tabela de comandos).
3. Filas e buffers compartilhados entre tarefas do FreeRTOS.

## Objetivo do atacante no PoC
Desviar o fluxo para uma função crítica que **não é alcançável** a partir do
caminho legítimo do parser — tornando a violação detectável no nível do CFG.

## Modelo de detecção
O defensor observa apenas o **trace de hardware** (sequência de transições de
fluxo). Não confia em nada que rode no mesmo domínio do firmware comprometido.
