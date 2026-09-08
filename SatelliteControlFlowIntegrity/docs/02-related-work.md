# 02 — Trabalhos relacionados

Referências verificadas nas fontes primárias. As entradas sem número de página
são as que não consegui confirmar em fonte acessível; estão marcadas.

---

## 1. Control-Flow Integrity clássica

**[1]** M. Abadi, M. Budiu, Ú. Erlingsson, J. Ligatti. *Control-Flow Integrity.*
Em *Proceedings of the 12th ACM Conference on Computer and Communications
Security (CCS '05)*, Alexandria, VA, EUA, nov. 2005, pp. 340–353.
DOI: [10.1145/1102120.1102165](https://doi.org/10.1145/1102120.1102165)

**[2]** M. Abadi, M. Budiu, Ú. Erlingsson, J. Ligatti. *Control-Flow Integrity
Principles, Implementations, and Applications.* ACM Transactions on Information
and System Security (TISSEC), v. 13, n. 1, out. 2009.
DOI: [10.1145/1609956.1609960](https://doi.org/10.1145/1609956.1609960)
— versão estendida de [1].

Formulação original da CFI e o vocabulário (arestas forward/backward, CFG como
política) que este trabalho usa. A limitação relevante para nós é que a CFI
clássica depende de **instrumentação do binário**, o que num alvo de voo cobra
flash, RAM e ciclos que não temos.

---

## 2. CFI baseada em trace de hardware — a base direta

**[3]** X. Tan, Z. Zhao. *SHERLOC: Secure and Holistic Control-Flow Violation
Detection on Embedded Systems.* Em *Proceedings of the 2023 ACM SIGSAC
Conference on Computer and Communications Security (CCS '23)*, Copenhague,
Dinamarca, nov. 2023.
DOI: [10.1145/3576915.3623077](https://doi.org/10.1145/3576915.3623077)
Código: https://github.com/CactiLab/Sherloc-Cortex-M-CFVD

Trabalho de referência deste projeto. Detecção de violação de fluxo de controle
(CFVD) baseada em trace, **sem instrumentar o software protegido e sem alterar
seu layout de memória** — exatamente a propriedade que torna a abordagem viável
sob orçamento de voo. Implementado para ARMv8-M e avaliado em Cortex-M33
(placa ARM V2M-MPS2+).

> **Ponto em que o SHERLOC está à frente deste protótipo.** O SHERLOC resolve o
> problema de distinguir interrupções assíncronas legítimas e trocas de contexto
> em tempo de execução, por meio de um algoritmo de detecção *interrupt- and
> scheduling-aware*. O nosso monitor **não faz isso**: aceita entrada e retorno
> de exceção incondicionalmente (`docs/05-evaluation.md`, Seção 6.3 do artigo).
> Essa é uma lacuna nossa em relação ao estado da arte, não uma diferença de
> escopo, e está declarada como tal.

**[4]** X. Tan, Z. Ma, S. Pinto, L. Guan, N. Zhang, J. Xu, Z. Lin, H. Hu,
Z. Zhao. *SoK: Where's the "up"?! A Comprehensive (bottom-up) Study on the
Security of Arm Cortex-M Systems.* Em *18th USENIX WOOT Conference on Offensive
Technologies (WOOT '24)*, 2024, pp. 149–169.
https://www.usenix.org/conference/woot24/presentation/tan

Sistematização da superfície de ataque em Cortex-M; posiciona CFVD entre as
demais defesas e serve de mapa do espaço de projeto.

---

## 3. Proteção de fluxo de controle em RTOS

**[5]** Y. Du, Z. Shen, K. Dharsee, J. Zhou, R. J. Walls, J. Criswell.
*Holistic Control-Flow Protection on Real-Time Embedded Systems with Kage.*
Em *31st USENIX Security Symposium (USENIX Security '22)*, Boston, MA, EUA,
ago. 2022, pp. 2281–2298.
https://www.usenix.org/conference/usenixsecurity22/presentation/du

Contraponto metodológico direto: o Kage protege dados de controle de aplicação
**e** do kernel em FreeRTOS, mas o faz por **transformação de compilador e
separação de regiões de memória** — isto é, paga o custo a bordo que a
abordagem por trace evita. A comparação entre as duas famílias é o eixo da
Seção 8.3 do artigo.

---

## 4. Trace de hardware em ARM

**[6]** Arm Ltd. *Embedded Trace Macrocell Architecture Specification,
ETMv4.0 to ETMv4.6.* Documento ARM IHI 0064.
https://developer.arm.com/documentation/ihi0064/hb/

**[7]** Arm Ltd. *CoreSight Architecture Specification.*
https://developer.arm.com/documentation/ihi0029/latest/

Fonte de evidência da abordagem. O ponto que fundamenta o modelo de confiança:
ETM e MTB operam **fora do domínio de execução do firmware**, de modo que um
firmware comprometido não consegue falsificar o próprio trace.

---

## 5. Segurança de sistemas espaciais

**[8]** The Aerospace Corporation. *SPARTA — Space Attack Research & Tactic
Analysis.* https://sparta.aerospace.org/

> **Correção:** o SPARTA é mantido pela **The Aerospace Corporation**, não pela
> MITRE. Versões anteriores deste repositório o atribuíam incorretamente à
> MITRE. O framework é o equivalente espacial do ATT&CK, e o mapeamento das
> técnicas cobertas pelo nosso detector continua como trabalho futuro.

**[9]** M. Scholl, T. Suloway. *Introduction to Cybersecurity for Commercial
Satellite Operations.* NIST Internal Report NIST IR 8270, jul. 2023.
https://nvlpubs.nist.gov/nistpubs/ir/2023/NIST.IR.8270.pdf

**[10]** CCSDS. *Space Data Link Security Protocol.* Recommended Standard,
CCSDS 355.0-B-2 (Blue Book), jul. 2022.
https://ccsds.org/Pubs/355x0b2.pdf

**[11]** CCSDS. *TC Space Data Link Protocol.* Recommended Standard,
CCSDS 232.0-B (Blue Book). https://ccsds.org/Pubs/232x0b3s.pdf
— base do formato de telecomando que o protótipo simplifica.

---

## 6. Incidentes públicos

**[12]** J. A. Guerrero-Saade, M. Hegel. *AcidRain — A Modem Wiper Rains Down on
Europe.* SentinelLabs, 31 mar. 2022.
https://www.sentinelone.com/labs/acidrain-a-modem-wiper-rains-down-on-europe/

> **Precisão necessária.** O ataque de 24 de fevereiro de 2022 inutilizou
> **modems KA-SAT em solo**, por meio de um appliance VPN mal configurado no
> segmento de gerenciamento — não foi um ataque ao firmware de bordo do
> satélite. Citá-lo como evidência de que "o firmware de satélite é atacado" é
> incorreto. O que ele demonstra, e é o que o artigo afirma, é que o setor
> espacial é alvo real, com efeito operacional em escala e transbordo para
> infraestrutura civil (5.800 turbinas eólicas na Alemanha perderam
> monitoramento remoto).

---

## 7. Ferramentas

**[13]** F. Bellard. *QEMU, a Fast and Portable Dynamic Translator.* Em
*USENIX Annual Technical Conference, FREENIX Track*, 2005, pp. 41–46.

**[14]** FreeRTOS Kernel V11.1.0. https://github.com/FreeRTOS/FreeRTOS-Kernel

---

## Lacuna identificada

CFVD baseada em trace está estabelecida para firmware embarcado genérico [3] e
CFI instrumentada está estabelecida para RTOS [5]. **Nenhuma das duas foi
avaliada sob as restrições específicas de voo** — orçamento de energia, janela
de contato, irreversibilidade da ação e ambiguidade entre ataque e evento de
radiação. É essa lacuna que este trabalho ocupa, e a contribuição é a
transposição e a avaliação, não uma técnica de detecção nova.

## Pendências de verificação

- Páginas exatas do SHERLOC [3] nos anais do CCS '23 — não confirmadas em fonte
  acessível (o portal da ACM está bloqueado neste ambiente). O DOI está correto.
- Revisão exata do CCSDS 232.0-B [11] a confirmar antes da submissão.
