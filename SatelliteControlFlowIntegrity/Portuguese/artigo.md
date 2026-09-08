# Detecção de Violação de Fluxo de Controle em Software de Voo Embarcado de Satélites

> **Status:** rascunho / esqueleto. Cada seção lista o que precisa ser escrito e
> de onde vem a evidência.

---

## Resumo
*(a escrever — 200 palavras: problema, lacuna, abordagem, resultado principal)*

**Pergunta de pesquisa:** é possível adaptar técnicas semelhantes ao SHERLOC para
detectar ataques contra firmware de sistemas espaciais embarcados?

---

## 1. Introdução
- Dependência crescente de infraestrutura orbital (comunicação, navegação, observação).
- CubeSats e constelações LEO: hardware barato, firmware complexo, superfície ampla.
- O que torna o domínio espacial diferente: irreversibilidade, janela de contato, energia, radiação.
- Contribuições deste trabalho (lista de 3 a 4 itens).

## 2. Contexto
### 2.1 Arquitetura típica de um computador de bordo
*(diagrama: ground station → módulo de comunicação → Cortex-M → FreeRTOS → subsistemas)*
### 2.2 Control-Flow Hijacking em alvos embarcados
### 2.3 Trace de hardware em Cortex-M (ETM / MTB)

## 3. Trabalhos relacionados
→ ver `docs/02-related-work.md`. Fechar com a lacuna: trace-based CFI não foi
avaliada sob restrições de voo.

## 4. Modelo de ameaças
→ ver `docs/01-threat-model.md`. Capacidades A1–A4, ativos, fora de escopo.

## 5. Sistema alvo: protótipo de computador de bordo
- 5 tarefas FreeRTOS: `tc_rx`, `adcs`, `eps`, `tm_tx`, `payload`.
- Formato do telecomando e caminho de parsing.
- Vulnerabilidade controlada e sua justificativa (é representativa? por quê?).

## 6. Cadeia de ataque
```
pacote da estacao -> parsing vulneravel -> buffer overflow
 -> return address alterado -> control-flow hijacking -> funcao critica
```
- Descrição do exploit e da função crítica alvo (`eps_kill_switch`).
- Por que a consequência é irreversível num satélite real.

## 7. Defesa: monitor de fluxo de controle
- Extração estática de CFG na build.
- Verificação online sobre o trace de hardware.
- Política de resposta em níveis L0–L3 e por que a decisão é da missão, não do detector.

## 8. Avaliação
→ ver `docs/05-evaluation.md`. Cenários S0–S5, métricas, tabela de resultados.

## 9. Discussão
- O que a técnica cobre e o que não cobre (ataques só de dados).
- Ataque vs. falha induzida por radiação: mesma assinatura, respostas diferentes.
- Custo de um falso positivo em operação real de missão.

## 10. Conclusão e trabalhos futuros
- Resposta direta à pergunta de pesquisa.
- Próximos passos: hardware real, atestação remota via telemetria, CFG sensível a contexto.

## Referências
*(a fechar)*
