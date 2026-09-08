# 04 — Metodologia

## Fases
1. **Construir o alvo** — flight software mínimo mas realista (5 tarefas, parser de TC, laço ADCS).
2. **Injetar vulnerabilidade controlada** — overflow de pilha no parser, documentado e versionado.
3. **Construir o exploit** — sobrescrita de endereço de retorno para chamar `eps_kill_switch()` (função crítica inalcançável pelo caminho legítimo).
4. **Extrair o CFG** — a partir do ELF, na build.
5. **Instrumentar o trace** — capturar transições em QEMU; depois via MTB em hardware.
6. **Implementar o verificador** — comparar trace contra CFG.
7. **Avaliar** — ver `05-evaluation.md`.

## Cenários de teste
| ID | Cenário | Resultado esperado |
|---|---|---|
| S0 | Operação nominal, telecomandos válidos | Nenhum alerta |
| S1 | Telecomandos malformados rejeitados pelo parser | Nenhum alerta (não há desvio) |
| S2 | Overflow com retorno para função crítica | **Detecção** |
| S3 | Overflow reutilizando função legítima (ROP curto) | Detecção (aresta inválida) |
| S4 | Carga de trabalho pesada (todas as tarefas ativas) | Sem falso positivo |
| S5 | Corrupção de dados sem desvio de fluxo | **Não detectado** — limitação declarada |

S5 é deliberado: delimita honestamente o que a técnica *não* cobre.

## Reprodutibilidade
- Toolchain e versões fixadas em `prototype/README.md`.
- Cada cenário é um script executável em `prototype/eval/`.
- Traces brutos versionados para permitir reanálise independente.
