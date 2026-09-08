# Detecção de Violação de Fluxo de Controle em Software de Voo Embarcado de Satélites

**Palavras-chave:** segurança espacial, sistemas embarcados, integridade de fluxo
de controle, ARM Cortex-M, FreeRTOS, trace de hardware, CubeSat

---

## Resumo

Satélites pequenos executam software de voo em microcontroladores sem MMU, com
memória na casa de dezenas de kilobytes e orçamento de energia rígido — um
ambiente onde as defesas convencionais contra sequestro de fluxo de controle são
caras demais para serem embarcadas. Este trabalho investiga se técnicas de
detecção baseadas em trace de hardware, na linha do SHERLOC, podem ser
transpostas para o domínio espacial.

Construímos um computador de bordo funcional — ARM Cortex-M3 rodando FreeRTOS e
cinco tarefas de voo (recepção de telecomando, controle de atitude, energia,
telemetria e carga útil) — e injetamos nele uma vulnerabilidade controlada de
parsing. Sobre essa única falha implementamos cinco ataques distintos: estouro de
buffer, corrupção de ponteiro de função, cadeia ROP, escalonamento malicioso de
tarefa e execução de função privilegiada sem autorização. Um monitor externo
extrai o grafo de fluxo de controle do binário em tempo de compilação e verifica
o trace de execução contra ele.

O monitor detectou **5 dos 5 ataques**, com **zero falsos positivos** em 1,4
milhão de blocos de execução legítima, e latência de detecção entre 0,001 e
0,052 ms — cerca de duas ordens de grandeza abaixo do período do laço de controle
de atitude. Por não instrumentar o firmware, o custo a bordo é de **0% de CPU,
0 KB de flash e 0 KB de RAM**; o custo migra integralmente para a banda do canal
de trace, que identificamos como a limitação prática dominante.

Implementamos também, deliberadamente, um sexto cenário fora do alcance da
técnica: um ataque exclusivamente de dados que compromete a missão sem desviar o
fluxo de controle. O monitor não o detecta, e não poderia. Essa fronteira é parte
do resultado.

---

## 1. Introdução

A infraestrutura orbital deixou de ser um domínio isolado. Constelações em órbita
baixa sustentam comunicação, navegação e observação da Terra, e o ataque à rede
KA-SAT da Viasat em fevereiro de 2022 demonstrou que o setor é alvo real, com
efeito operacional em escala — inclusive transbordo para infraestrutura civil,
com 5.800 turbinas eólicas na Alemanha perdendo monitoramento remoto [12].

Vale a precisão: aquele ataque inutilizou **modems em solo**, por meio de um
appliance VPN mal configurado no segmento de gerenciamento; não foi um
comprometimento do firmware de bordo. Ele motiva este trabalho por demonstrar
adversários capazes e interessados no domínio espacial, não por ser uma
instância da ameaça que atacamos aqui.

O que torna o domínio espacial distinto não é a natureza das vulnerabilidades —
estouros de buffer em parsers de protocolo são os mesmos de qualquer sistema
embarcado — mas as **restrições sob as quais a defesa precisa operar**:

| Restrição | Consequência para a defesa |
|---|---|
| Microcontrolador sem MMU | Não há isolamento forte entre tarefas do RTOS |
| Dezenas a centenas de KB de RAM | Shadow stacks e instrumentação pesada são inviáveis |
| Orçamento de energia rígido | Overhead de CPU tem custo térmico e elétrico real |
| Janela de contato curta | Resposta humana a incidente é lenta ou impossível |
| Atualização de firmware cara e arriscada | Correção pós-incidente leva meses |
| Ações irreversíveis | Desligar o barramento de energia encerra a missão |

O último item reorganiza as prioridades. Em um servidor, detectar tarde ainda
permite remediar. Em um satélite, uma função crítica executada uma vez pode
encerrar a missão. **Detectar no instante do desvio vale mais do que remediar
depois** — e é essa a lacuna que motiva este trabalho.

### Pergunta de pesquisa

> É possível adaptar técnicas semelhantes ao SHERLOC para detectar ataques contra
> firmware de sistemas espaciais embarcados?

### Contribuições

1. Um computador de bordo funcional, do bring-up bare-metal ao software de voo
   sobre FreeRTOS, construído especificamente como alvo de medição de segurança.
2. Cinco ataques de fluxo de controle reproduzíveis, todos sobre a mesma
   vulnerabilidade injetada, isolando o tipo de desvio como única variável.
3. Um detector baseado em trace, sem instrumentação do firmware, com extração
   estática de CFG e verificação externa.
4. Avaliação quantitativa sob métricas relevantes para voo: detecção, falsos
   positivos, latência e overhead de CPU, flash e memória.
5. A demonstração explícita da fronteira da técnica, por meio de um ataque
   exclusivamente de dados que compromete a missão sem ser detectado.

---

## 2. Contexto

### 2.1 Arquitetura típica de um computador de bordo

```
Estação de solo
      |  telecomando (TC)
      v
Módulo de comunicação
      v
ARM Cortex-M
      v
FreeRTOS
      v
Software de voo
      v
+---------------------------------+
| ADCS | Telemetria | EPS | Payload|
+---------------------------------+
```

Telecomandos chegam por RF, são desempacotados por um módulo de comunicação e
entregues ao software de voo, que os interpreta e aciona os subsistemas. O parser
de telecomando é, portanto, a fronteira onde dados controlados pelo atacante
encontram código privilegiado.

### 2.2 Sequestro de fluxo de controle em alvos embarcados

Em ARM, o endereço de retorno reside no registrador `lr`. Uma função folha o
mantém em registrador e é imune ao ataque clássico de pilha; uma função que chama
outras precisa preservá-lo na pilha (`push {r7, lr}`), e é essa cópia que um
estouro alcança. O Cortex-M executa apenas o conjunto Thumb, e o bit 0 do
endereço carregado no `PC` seleciona o estado de instrução — um endereço com esse
bit zerado provoca falha em vez de executar o alvo.

Ausência de MMU significa que não há separação de espaços de endereçamento entre
tarefas: o isolamento depende inteiramente da MPU, opcional e frequentemente não
utilizada.

### 2.3 Trace de hardware em Cortex-M

Núcleos Cortex-M oferecem, via CoreSight [6, 7], o **ETM** (Embedded Trace Macrocell),
que emite um fluxo comprimido de desvios tomados, e o **MTB** (Micro Trace
Buffer), um buffer circular em RAM. Ambos operam **fora do domínio de execução do
firmware**: um firmware comprometido não consegue falsificar o próprio trace.
Essa propriedade é o que fundamenta a abordagem — o detector não confia em nada
que rode no mesmo domínio que ele observa.

---

## 3. Modelo de ameaças

**Capacidades assumidas do atacante:**

- **A1 — Uplink hostil.** Consegue injetar telecomandos malformados, seja por
  comprometimento da estação de solo, spoofing de RF ou abuso de operador
  legítimo.
- **A2 — Conhecimento do firmware.** Conhece o binário, por ser COTS, código
  aberto ou vazamento na cadeia de suprimentos.
- **A3 — Sem acesso físico.** Não pode reprogramar via JTAG após o lançamento.
- **A4 — Sem quebra de criptografia.** A autenticação de telecomando, quando
  existe, é a fronteira; o ataque ocorre **depois** do parsing.

**Fora de escopo:** jamming, ataques físicos, comprometimento da estação de solo
em si (premissa, não alvo) e canais laterais.

**Objetivo do atacante:** desviar a execução para uma função crítica inalcançável
pelo caminho legítimo do parser.

**Postura do defensor:** o monitor observa apenas o trace de execução. Não confia
em nenhum estado reportado pelo firmware.

---

## 4. Sistema alvo

Implementamos um software de voo do tipo CubeSat sobre QEMU `mps2-an385`
(Cortex-M3 a 25 MHz), FreeRTOS Kernel V11.1.0, imagem de 23 KB de texto.

| Tarefa | Prioridade | Período | Papel |
|---|---|---|---|
| `tc_rx` | 4 | polling 2 ms | recepção e parsing de telecomandos |
| `adcs` | 3 | 10 ms | laço de controle de atitude |
| `eps` | 2 | 5 s | monitoramento de energia |
| `tm_tx` | 1 | 2 s | telemetria (beacon) |
| `payload` | 1 | 50 ms | carga útil |

A prioridade 5 permanece livre em operação nominal — detalhe que se torna
relevante na Seção 5.

**Formato de telecomando:**

```
+--------+--------+--------+-------------------+
| SYNC   | APID   | LEN    | PAYLOAD (LEN B)   |
| EB 90  | 1 B    | 1 B    | 0..255 B          |
+--------+--------+--------+-------------------+
```

**Funções críticas**, inalcançáveis por qualquer caminho legítimo e presentes
apenas como alvo mensurável: `eps_kill_switch()` (desliga o barramento de
energia), `payload_wipe()` (apaga a memória da carga útil),
`debug_spawn_rogue_task()` (hook de fábrica esquecido na imagem) e
`priv_raw_write_body()` (escrita privilegiada).

### 4.1 A vulnerabilidade controlada

Uma única falha, em `tc_handle_frame()`: o campo `LEN` do telecomando é usado sem
validação como comprimento de cópia para um buffer de pilha de 64 bytes. O quadro
de pilha, lido do binário compilado:

```
offset  0..63   ctx.buf[64]
offset 64       ctx.handler        <- alvo da chamada indireta
offset 76       r7 salvo
offset 80       LR salvo           <- vai para o PC no retorno
offset 84/88    quadro do gadget   <- segundo estágio do ROP
```

Concentrar todos os ataques em uma única falha é uma escolha metodológica: isola
o **tipo de desvio de fluxo** como variável experimental, eliminando diferenças
de bug de entrada como fator de confusão.

---

## 5. Os cinco ataques

| ID | Ataque | Mecanismo | Efeito de missão |
|---|---|---|---|
| ATK-1 | Estouro de buffer | sobrescreve o LR salvo | barramento de energia desligado |
| ATK-2 | Corrupção de ponteiro de função | sobrescreve o ponteiro de dispatch | memória da carga útil apagada |
| ATK-3 | Cadeia ROP | dois estágios via gadget `pop {r7, pc}` | memória da carga útil apagada |
| ATK-4 | Escalonamento malicioso | desvia para hook de debug residual | apontamento perdido |
| ATK-5 | Função privilegiada não autorizada | entra no corpo pulando a checagem | escrita privilegiada sem auth |

Dois merecem comentário.

**ATK-3** não injeta código: reutiliza o que já está na imagem. O gadget
`pop {r7, pc}` (encoding Thumb `0xbd80`) é o epílogo padrão de toda função
não-folha compilada sem otimização — o binário oferece 148 ocorrências. Isso
ilustra por que impedir injeção de código não basta.

**ATK-4** não executa shellcode nem corrompe dados de missão: usa o **escalonador
como arma**. A tarefa criada em prioridade 5 fica acima do ADCS em prioridade 3, e
o laço de controle de atitude simplesmente deixa de ser escalonado. A consequência
não é "código executado", é perda de apontamento — seguida de perda de link e de
geração de energia.

---

## 6. O detector

### 6.1 Fase estática (tempo de compilação)

`cfg_extract.py` desmonta o ELF e emite a política de arestas permitidas:

- **Arestas diretas** (`b`, `bl`, condicionais): alvo exato codificado na
  instrução.
- **Chamadas indiretas** (`blx rN`): aproximadas pelo conjunto de funções cujo
  endereço aparece materializado na imagem — a aproximação conservadora que toda
  implementação prática de CFI precisa fazer.
- **Retornos**: restritos aos sítios de retorno dos chamadores reais da função.
- **Entrada e retorno de exceção**: aceitos incondicionalmente (ver 6.3).

Na imagem avaliada: 9.716 instruções, 1.156 sítios de desvio direto, 3 sítios
indiretos, 148 sítios de retorno. Extração em 0,3 s.

### 6.2 Fase dinâmica (execução)

`cfi_monitor.py` consome o trace de execução — aqui o log de blocos do QEMU, no
papel do fluxo do ETM — reconstrói cada transição e a compara com a política. O
monitor **não roda no espaço de endereçamento do firmware**: um software de voo
comprometido não tem como silenciá-lo.

### 6.3 O que é aceito sem verificação

Duas classes de transição são aceitas incondicionalmente, e declará-las é parte
do resultado — inclusive porque é aqui que o SHERLOC [3] está à frente deste
protótipo: ele resolve o problema com um algoritmo de detecção *interrupt- and
scheduling-aware*, enquanto o nosso monitor simplesmente isenta os dois casos.
Trata-se de uma lacuna nossa em relação ao estado da arte, não de uma diferença
de escopo.

- **Entrada de exceção**: o desvio é executado pelo hardware e não parte de
  nenhuma instrução do programa; nenhum CFG o contém.
- **Retorno de exceção**: o `PC` restaurado não está no modelo. O caso mais agudo
  é o `PendSV`, que troca a tarefa em execução — sem essa isenção, cada troca de
  contexto seria um falso positivo, a 1 kHz.

São buracos reais de cobertura, não simplificações de implementação.

### 6.4 Resposta a incidente

A política de resposta é decisão de missão, não do detector:

| Nível | Ação |
|---|---|
| L0 | Registro em telemetria de segurança |
| L1 | Quarentena do subsistema afetado |
| L2 | Entrada em modo seguro (atitude estável, rádio ativo, payload desligado) |
| L3 | Reinício a partir de imagem confiável |

A separação importa: um falso positivo que dispare L3 tem custo operacional real,
medido em dias de missão.

---

## 7. Avaliação

### 7.1 Resultados por cenário

| Cenário | Comprometido | Violações | Detectado | Latência (instr) | Latência (ms) |
|---|---|---|---|---|---|
| S0 — telecomandos nominais | não | 0 | n/a | — | — |
| S1 — malformados, rejeitados | não | 0 | n/a | — | — |
| S4 — carga sustentada | não | 0 | n/a | — | — |
| ATK-1 — estouro de buffer | sim | 1 | **SIM** | 1230 | 0,0492 |
| ATK-2 — ponteiro de função | sim | 1 | **SIM** | 26 | 0,0010 |
| ATK-3 — ROP | sim | 2 | **SIM** | 1303 | 0,0521 |
| ATK-4 — escalonamento | sim | 1 | **SIM** | 1230 | 0,0492 |
| ATK-5 — função privilegiada | sim | 2 | **SIM** | 1230 | 0,0492 |
| **S5 — ataque só de dados** | **sim** | **0** | **NÃO** | — | — |

ATK-3 e ATK-5 produzem duas violações porque o desvio tem dois estágios; são
arestas do mesmo ataque, não alertas independentes.

### 7.2 Métricas agregadas

| Métrica | Valor |
|---|---|
| Detecção de ataques | **5/5 (100%)** |
| Falsos positivos | **0** em 1,4 M de blocos (S0, S1, S4) |
| Latência de detecção | 26–1303 instruções (0,001–0,052 ms a 25 MHz) |
| Overhead de CPU a bordo | **0%** |
| Overhead de flash a bordo | **0 KB** |
| Overhead de memória a bordo | **0 KB** |
| Modelo de CFG (lado do monitor) | 940 KB |
| Throughput do monitor | ~31 MB de trace/s |

### 7.3 Leitura dos resultados

**O overhead zero a bordo é o resultado central, e é uma propriedade estrutural,
não uma otimização.** O firmware não é instrumentado; o detector consome o trace
que o hardware já produz. Em um satélite, onde flash e RAM são fixados antes do
lançamento e cada ciclo de CPU tem custo energético e térmico, um esquema que
cobra 0 KB e 0% na placa é qualitativamente diferente de um que cobra 5–15%.

O custo não desaparece: **migra integralmente para a banda do canal de trace.**
Um segundo de voo emulado gerou cerca de 200 MB de trace bruto do QEMU. É a
limitação prática dominante e o próximo item experimental.

**A latência cabe no orçamento de tempo real.** O pior caso medido, 0,052 ms, é
cerca de 190 vezes menor que o período do laço de ADCS (10 ms). Existe folga para
disparar contenção antes do próximo ciclo de controle — o que separa "detectar"
de "conter".

**ATK-2 é detectado 47 vezes mais rápido** que os ataques de retorno (26 contra
~1230 instruções). Todos corrompem a pilha no mesmo instante; a diferença é
*quando o valor corrompido é consumido*. O ponteiro de função é usado
imediatamente na chamada indireta; o endereço de retorno só é consumido no
epílogo, depois de o handler legítimo ter executado por inteiro. **Latência de
detecção é propriedade do ataque, não apenas do detector.**

### 7.4 A fronteira: o cenário S5

O S5 foi construído para falhar. Uma segunda vulnerabilidade controlada — escrita
fora de limites em uma tabela de parâmetros de missão — permite que dois
telecomandos **perfeitamente bem formados** comprometam o satélite:

1. `param_set(index=8)` escreve além do fim da tabela e atinge o campo
   `authenticated` do bloco de configuração, adjacente na memória.
2. Um telecomando privilegiado legítimo então passa na checagem de autenticação
   que deveria ter falhado.

Nenhuma aresta ilegal é executada, porque **todas as arestas são legais**. O
monitor reporta zero violações. O satélite continua transmitindo telemetria
normalmente — nem sequer há falha visível. A missão está comprometida.

Este é o limite da abordagem, e é estrutural: um detector de fluxo de controle
não pode ver um ataque que não desvia o fluxo de controle. Reportá-lo como
resultado, e não omiti-lo, é o que separa uma avaliação de uma demonstração.

---

## 8. Discussão

### 8.1 Ataque ou radiação?

Um Single Event Upset induzido por radiação pode corromper um endereço de retorno
sem qualquer adversário envolvido. Para o detector, as duas situações produzem a
**mesma assinatura**: uma aresta que o CFG não permite.

Isso não é apenas ruído. Tem consequência operacional direta: a resposta correta
a um ataque (entrar em modo seguro, isolar o canal de uplink) é diferente da
resposta correta a um SEU (corrigir e continuar). Distinguir os dois exige
correlação com outras fontes — contadores de ECC, posição orbital em relação à
Anomalia do Atlântico Sul, taxa histórica de eventos — e está fora do escopo
deste protótipo. É, na nossa avaliação, a questão de pesquisa mais interessante
que o trabalho abre.

### 8.2 O custo de um falso positivo

Zero falsos positivos em 1,4 milhão de blocos é encorajador, mas o firmware é
pequeno e a carga é sintética. A extrapolação para software de voo real não é
válida sem repetir a medição.

O ponto merece ênfase porque a assimetria de custo é severa: em um satélite, um
falso positivo que dispare modo seguro custa dias de missão e uma janela de
contato para recuperação. Um detector com taxa de falso positivo mesmo baixa, mas
não nula, precisa de uma política de resposta escalonada — e é por isso que a
Seção 6.4 separa detecção de reação.

### 8.3 Posicionamento

Duas famílias de defesa disputam este espaço, e a diferença entre elas é onde o
custo é pago.

O **Kage** [5] protege dados de controle de aplicação e de kernel em FreeRTOS por
transformação de compilador e separação de regiões de memória — ou seja, paga o
custo **a bordo**, em flash, RAM e ciclos. O **SHERLOC** [3] usa trace de
hardware e não instrumenta o software protegido nem altera seu layout de
memória, movendo o custo para fora da placa. Este trabalho segue a segunda
família, e é o que explica o overhead nulo da Seção 7.

Comparado ao SHERLOC especificamente:

| Eixo | SHERLOC [3] | Este trabalho |
|---|---|---|
| Alvo | Firmware embarcado, ARMv8-M / Cortex-M33 | Software de voo sobre FreeRTOS, Cortex-M3 |
| Evidência | Trace de hardware | Trace de hardware (QEMU no papel do ETM) |
| Interrupções e troca de contexto | **Tratadas** por algoritmo dedicado | **Isentas** — lacuna declarada (6.3) |
| Ameaça | Atacante local ou de rede | Estação de solo comprometida, uplink hostil |
| Resposta | Alerta / parada | Modo seguro, quarentena, telemetria de segurança |
| Restrição dominante | Custo e memória | Energia, radiação, janela de contato, irreversibilidade |
| Validação | Hardware real (V2M-MPS2+) | Emulação |

A contribuição não é uma técnica nova de detecção, e apresentá-la como tal seria
incorreto — em capacidade de detecção este protótipo está **atrás** do SHERLOC,
não à frente. A contribuição é a transposição para um modelo de ameaças em que
**a resposta a incidente não pode depender de intervenção humana imediata**, a
avaliação sob as métricas que esse contexto impõe, e a delimitação empírica da
fronteira da técnica (Seção 7.4).

---

## 9. Limitações

- **Ataques exclusivamente de dados escapam por construção** (Seção 7.4).
- **Volume de trace.** ~200 MB/s do QEMU é inviável para downlink. O ETM real
  comprime agressivamente e o MTB guarda apenas uma janela circular, mas quanto
  trace cabe no orçamento de banda permanece em aberto.
- **CFG conservador para chamadas indiretas**, mais permissivo que o conjunto
  real de alvos.
- **Isenção de exceções** (Seção 6.3) é um buraco de cobertura declarado.
- **Energia não foi medida, foi argumentada.** Sem instrumentação a bordo, o
  consumo adicional na placa é zero por construção; o consumo do canal de trace
  exige medição em hardware.
- **Artefatos de emulação.** O QEMU reinicia blocos ao receber interrupção e, com
  encadeamento ativo, omite execuções — o que exigiu `-d exec,nochain`. Nenhum
  dos dois existe no ETM real, mas ambos afetam a comparabilidade.

### Ameaças à validade

Firmware pequeno (23 KB) e escrito pelos autores: o CFG é mais simples e preciso
que o de software de voo real. A conversão de instruções para milissegundos assume
1 instrução por ciclo, o que subestima o tempo no Cortex-M3. Uma execução por
cenário: os números de latência devem ser lidos como ordem de grandeza, não como
média de distribuição.

---

## 10. Conclusão

**Sim, com uma fronteira precisa.** Detecção de violação de fluxo de controle
baseada em trace transfere-se para software de voo de satélite, e a transferência
é favorável: 100% de detecção sobre cinco classes distintas de ataque, sem falso
positivo na carga avaliada, com latência duas ordens de grandeza abaixo do laço
de controle de atitude e **custo nulo de CPU, flash e memória a bordo** — a
propriedade que torna a abordagem plausível sob orçamento de energia e prazo de
tempo real de um satélite.

A fronteira é igualmente clara. A técnica não vê ataques que não desviam o fluxo
de controle, e demonstramos isso comprometendo o satélite com dois telecomandos
bem formados sem disparar um único alerta. Ela também não distingue um ataque de
um evento de radiação — o que, no domínio espacial, não é um detalhe.

### Trabalhos futuros

1. **Porte para hardware real** com ETM/MTB, e medição do custo energético do
   canal de trace — hoje argumentado, não medido.
2. **Orçamento de banda de trace**: quanto trace um satélite consegue de fato
   processar a bordo, e o que a janela circular do MTB deixa de fora.
3. **Discriminação entre ataque e SEU**, por correlação com contadores de ECC e
   posição orbital.
4. **Integridade de fluxo de dados** para cobrir a classe do S5.
5. **Atestação remota via telemetria**, transformando o veredito do monitor em
   evidência verificável na estação de solo.
6. **Tratamento de interrupções e troca de contexto** no nível do SHERLOC [3],
   eliminando a isenção da Seção 6.3.
7. **Mapeamento das técnicas cobertas para o framework SPARTA** [8], da The
   Aerospace Corporation.

---

## Disponibilidade

Firmware, ataques, monitor e harness de medição estão em `prototype/`, com
toolchain fixada e um script por cenário. A tabela bruta de resultados é gerada
por `eval/run_matrix.py`.

## Considerações éticas

Todo o trabalho ocorre em firmware escrito pelos autores, executado em emulador.
Não há satélite em órbita, operador ou estação de solo de terceiros envolvidos.
As vulnerabilidades são introduzidas deliberadamente como alvo de medição;
nenhuma falha de produto de terceiros é explorada ou divulgada.

## Referências

[1] M. Abadi, M. Budiu, Ú. Erlingsson, J. Ligatti. *Control-Flow Integrity.*
Em *Proceedings of the 12th ACM Conference on Computer and Communications
Security (CCS '05)*, Alexandria, VA, EUA, nov. 2005, pp. 340–353.
DOI: 10.1145/1102120.1102165

[2] M. Abadi, M. Budiu, Ú. Erlingsson, J. Ligatti. *Control-Flow Integrity
Principles, Implementations, and Applications.* ACM TISSEC, v. 13, n. 1,
out. 2009. DOI: 10.1145/1609956.1609960

[3] X. Tan, Z. Zhao. *SHERLOC: Secure and Holistic Control-Flow Violation
Detection on Embedded Systems.* Em *CCS '23*, Copenhague, Dinamarca,
26–30 nov. 2023, pp. 1332–1346. DOI: 10.1145/3576915.3623077

[4] X. Tan, Z. Ma, S. Pinto, L. Guan, N. Zhang, J. Xu, Z. Lin, H. Hu, Z. Zhao.
*SoK: Where's the "up"?! A Comprehensive (bottom-up) Study on the Security of
Arm Cortex-M Systems.* Em *18th USENIX WOOT*, 2024, pp. 149–169.

[5] Y. Du, Z. Shen, K. Dharsee, J. Zhou, R. J. Walls, J. Criswell. *Holistic
Control-Flow Protection on Real-Time Embedded Systems with Kage.* Em *31st
USENIX Security Symposium*, Boston, MA, EUA, ago. 2022, pp. 2281–2298.

[6] Arm Ltd. *Embedded Trace Macrocell Architecture Specification, ETMv4.0 to
ETMv4.6.* ARM IHI 0064.

[7] Arm Ltd. *CoreSight Architecture Specification.* ARM IHI 0029.

[8] The Aerospace Corporation. *SPARTA — Space Attack Research & Tactic
Analysis.* https://sparta.aerospace.org/

[9] M. Scholl, T. Suloway. *Introduction to Cybersecurity for Commercial
Satellite Operations.* NIST IR 8270, jul. 2023.

[10] CCSDS. *Space Data Link Security Protocol.* Recommended Standard,
CCSDS 355.0-B-2 (Blue Book), jul. 2022.

[11] CCSDS. *TC Space Data Link Protocol.* Recommended Standard,
CCSDS 232.0-B-4 (Blue Book), Issue 4, out. 2021.

[12] J. A. Guerrero-Saade, M. Hegel. *AcidRain — A Modem Wiper Rains Down on
Europe.* SentinelLabs, 31 mar. 2022.

[13] F. Bellard. *QEMU, a Fast and Portable Dynamic Translator.* Em *USENIX
Annual Technical Conference, FREENIX Track*, 2005, pp. 41–46.

[14] FreeRTOS Kernel V11.1.0. https://github.com/FreeRTOS/FreeRTOS-Kernel
