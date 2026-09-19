# 07 — Fundamentos técnicos exercitados

Este capítulo existe para tornar explícito o conhecimento de base que o
protótipo exige e demonstra. Nada aqui é genérico: cada conceito está ancorado
em código, disassembly ou medição deste repositório.

---

## 1. Linguagem C e Assembly

### 1.1 Ponteiros e aritmética de endereços

O parser de telecomando trabalha o quadro recebido como um bloco de bytes cru e
navega por ele com aritmética de ponteiro (`firmware/src/tc.c`):

```c
uint8_t  apid = frame[2];
uint32_t len  = frame[3];
tc_copy(ctx.buf, &frame[TC_HDR_LEN], len);
```

O `&frame[TC_HDR_LEN]` é o ponto onde os dados do atacante entram no sistema. A
`tc_copy()` é um laço de cópia byte a byte deliberadamente escrito à mão, em vez
de `memcpy`, para que a falha fique visível no código-fonte e não escondida
atrás de uma função de biblioteca.

### 1.2 Layout de memória e o quadro de pilha

O ponto central do trabalho é que **o layout que o compilador escolhe é o que
determina o que o atacante alcança**. O quadro de `tc_handle_frame()` foi lido
diretamente do binário:

```
0000061c <tc_handle_frame>:
     61c:  b580        push  {r7, lr}      <- salva o endereço de retorno na pilha
     61e:  b096        sub   sp, #88       <- abre 88 bytes de locais
     620:  af00        add   r7, sp, #0    <- r7 vira o frame pointer
     ...
     656:  653b        str   r3, [r7, #80] <- len (o campo LEN do telecomando)
     664:  64fb        str   r3, [r7, #76] <- ctx.handler
     66a:  f107 030c   add.w r3, r7, #12   <- &ctx.buf
```

Traduzido para deslocamentos a partir do início de `ctx.buf` (`r7+12`), que é
onde a cópia começa:

```
   r7+12   ...   r7+75    ctx.buf[64]        offsets 0..63
   r7+76                  ctx.handler        offset 64   <- alvo do ATK-2
   r7+80                  len
   r7+87                  apid
   r7+88                  r7 salvo           offset 76
   r7+92                  LR salvo           offset 80   <- alvo do ATK-1
   r7+96                  (topo do quadro)   offset 84   <- estágio 2 do ROP
   r7+100                                    offset 88
```

Os offsets em `attacks/attacks.py` não são chutes: saíram desta leitura.

### 1.3 Registradores e a ABI do ARM

O que torna os ataques possíveis é a convenção de chamada do Cortex-M:

| Registrador | Papel | Relevância para o ataque |
|---|---|---|
| `r0`–`r3` | argumentos e retorno | carregam o payload para o handler |
| `r7` | frame pointer em `-O0` | base de todos os offsets acima |
| `sp` (`r13`) | stack pointer | define onde a cópia transborda |
| `lr` (`r14`) | endereço de retorno | **salvo na pilha** em função não-folha — por isso é sobrescrevível |
| `pc` (`r15`) | program counter | destino final de `pop {r7, pc}` |

O detalhe decisivo: em ARM o endereço de retorno vive em `lr`, um registrador —
não na pilha. Uma função folha, portanto, **não é vulnerável a este ataque**.
`tc_handle_frame()` chama outras funções, então precisa preservar `lr` na pilha
(`push {r7, lr}`), e é exatamente essa preservação que o overflow alcança.

### 1.4 O bit Thumb

Todo endereço de destino nos ataques leva `| 1`:

```python
def thumb(self, name: str) -> int:
    return self._syms[name] | 1
```

O Cortex-M executa apenas o conjunto Thumb, e o bit 0 do endereço carregado no
`PC` seleciona o estado de instrução. Um endereço com bit 0 zerado provoca
UsageFault em vez de executar o alvo — errar isso é a diferença entre um exploit
funcional e um `HARD FAULT`.

### 1.5 Gadgets: instruções como matéria-prima

O ATK-3 não injeta código; reutiliza o que já está na imagem. O gadget é
localizado por padrão de encoding:

```python
if "bd80" in line and "pop" in line and "{r7, pc}" in line:
```

`0xbd80` é o encoding Thumb de `pop {r7, pc}`. Todo epílogo de função não-folha
compilada com `-O0` termina assim — o binário oferece 148 desses. Isso ilustra
por que W^X e "não injetar código" não bastam: o código legítimo já contém as
peças.

---

## 2. Sistemas Operacionais e Arquitetura

### 2.1 Como a CPU executa: blocos básicos e o trace

O monitor não vê instruções uma a uma; vê **blocos**. Reconstruir a execução
exige saber onde cada bloco termina, o que é feito caminhando o disassembly até
a primeira instrução de transferência de controle:

```python
while True:
    insn = self.insns.get(pc)
    if is_transfer(insn):
        return pc, steps
    pc += insn["size"]
```

`pc += insn["size"]` é literalmente o modelo de execução da CPU: Thumb mistura
instruções de 2 e 4 bytes, e assumir largura fixa desalinha todo o resto.

### 2.2 Gerenciamento de pilha em um RTOS

Cada uma das cinco tarefas tem sua própria pilha, dimensionada na criação:

```c
xTaskCreate(task_tc_rx,   "tc_rx",   256, NULL, 4, NULL);
xTaskCreate(task_adcs,    "adcs",    192, NULL, 3, NULL);
```

O número é em **palavras**, não bytes: 256 palavras = 1 KB. O overflow do ATK-1
acontece dentro da pilha da `tc_rx`, o que significa que a corrupção é local à
tarefa — e é justamente por isso que ela não é detectada por nenhum mecanismo do
kernel: do ponto de vista do FreeRTOS, a tarefa está usando a própria memória.

Sem MMU, não há isolamento entre tarefas — só a MPU, opcional e não usada aqui.
Essa é a diferença de fundo entre um alvo embarcado e um servidor.

### 2.3 Interrupções, exceções e a tabela de vetores

A tabela de vetores é escrita à mão em `firmware/src/startup.c`, e é ela que
liga o hardware ao RTOS:

```c
void (* const g_vectors[])(void) = {
    (void (*)(void)) &_estack,   /* valor inicial do SP */
    Reset_Handler,
    ...
    vPortSVCHandler,             /* SVCall  */
    xPortPendSVHandler,          /* PendSV  - troca de contexto */
    xPortSysTickHandler,         /* SysTick - tick do escalonador */
};
```

A primeira entrada não é uma função: é o valor inicial do stack pointer, que o
hardware carrega antes de executar qualquer instrução.

Interrupções são o principal problema prático do detector. Quando uma exceção
ocorre, o hardware empilha o contexto e desvia o `PC` para o handler — um desvio
que **nenhum CFG contém**, porque não vem de nenhuma instrução do programa. O
monitor precisa tratá-lo explicitamente:

```python
if dest in self.handlers:
    return True, "exception-entry", steps
if func in self.handler_funcs:
    return True, "exception-return", steps
```

Isso é aceitar duas classes de transição sem verificação — um buraco real de
cobertura, declarado em `05-evaluation.md` em vez de escondido.

O `xPortPendSVHandler` é o caso mais agudo: ele **troca a tarefa em execução**,
então o `PC` depois dele pertence a outro fluxo. Sem tratar o retorno de exceção
como irrestrito, cada troca de contexto viraria um falso positivo — e o
escalonador roda a 1 kHz.

### 2.4 Memória-mapeada e `volatile`

O driver de UART conversa com o periférico por endereços fixos:

```c
#define UART_STATE  (*(volatile uint32_t *)(UART0_BASE + 0x04))
while (UART_STATE & STATE_TX_FULL) { }
```

Sem `volatile`, o compilador percebe que `UART_STATE` não muda dentro do laço,
iça a leitura para fora e produz um laço infinito. É o caso didático de por que
`volatile` existe — e a mesma razão pela qual `g_state.authenticated` é
`volatile` no bloco de configuração.

### 2.5 O escalonador como superfície de ataque

O ATK-4 não corrompe dados nem executa shellcode: ele **usa o escalonador como
arma**. Criando uma tarefa em prioridade 5, acima da prioridade 3 do ADCS, o
laço de controle de atitude simplesmente para de ser escalonado.

O efeito num satélite real não é "código executado": é perda de apontamento,
depois perda de link e de geração de energia. A consequência é de missão, e
nenhum antivírus de arquivo a veria.

---

## 3. Projeto prático / Prova de conceito

O que foi construído, e o que cada peça demonstra:

| Componente | Arquivo | Demonstra |
|---|---|---|
| Bring-up bare-metal | `firmware/src/startup.c`, `mps2_an385.ld` | tabela de vetores, seções, cópia de `.data`, zeragem de `.bss` |
| Driver de periférico | `firmware/src/uart.c` | I/O memória-mapeada, `volatile`, polling |
| Integração de RTOS | `firmware/src/main.c`, `FreeRTOSConfig.h` | tarefas, prioridades, escalonamento preemptivo |
| Parser de protocolo | `firmware/src/tc.c` | máquina de recepção, tabela de dispatch por ponteiro de função |
| Vulnerabilidades controladas | `tc.c`, `privileged.c` | overflow de pilha e escrita fora de limites em array |
| Exploits | `attacks/attacks.py` | 5 técnicas distintas sobre a mesma falha |
| Análise estática de binário | `monitor/cfg_extract.py` | desmontagem, extração de CFG, resolução de alvos |
| Análise dinâmica de trace | `monitor/cfi_monitor.py` | reconstrução de fluxo, verificação de política |
| Harness de medição | `eval/run_matrix.py` | automação de experimento e coleta de métricas |

### O que o exercício ensinou que não estava no plano

**1. O trace mentiu primeiro.** A primeira execução do monitor produziu 382.668
violações — todas falsas. A causa não era o modelo de CFG: o QEMU encadeia
blocos de tradução e **deixa de registrar execuções** quando eles estão
encadeados. Sem `-d exec,nochain`, o trace tem buracos, e cada buraco vira uma
aresta impossível. Depois da correção: 9 violações. Depois de tratar retorno de
chamada indireta e reentrada de bloco: **1**, que era o ataque.

A lição é sobre instrumentação, não sobre segurança: **antes de acreditar num
detector, é preciso validar a fonte de evidência.** Um detector alimentado por
trace incompleto produz alarme constante, e alarme constante em operação de
satélite é indistinguível de detector desligado.

**2. A prioridade importava mais que o exploit.** O ATK-4 chegava perfeitamente
ao alvo — `debug_spawn_rogue_task()` executava — e mesmo assim nada acontecia. A
tarefa maliciosa era criada na mesma prioridade da `tc_rx` e nunca preemptava. O
exploit estava certo; o modelo de escalonamento é que decidia o resultado.

**3. Detectar cedo depende de quando o valor corrompido é *usado*.** O ATK-2 é
detectado em 26 instruções e os ataques de retorno em ~1230. Todos corrompem a
pilha no mesmo instante. A diferença é que o ponteiro de função é consumido
imediatamente, enquanto o endereço de retorno só é consumido no epílogo — depois
do handler legítimo ter rodado inteiro.
