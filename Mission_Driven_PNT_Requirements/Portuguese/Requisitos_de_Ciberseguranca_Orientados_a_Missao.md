# Requisitos de Cibersegurança Orientados à Missão para Satélites LEO Dependentes de GNSS

**Um framework para derivar requisitos cibernéticos mínimos de bordo a partir de cadeias de ameaça PNT**

> Versão em português de `Mission-Driven Cybersecurity Requirements for GNSS-Dependent LEO Spacecraft`. A numeração de seções, tabelas e figuras é idêntica à da versão em inglês, para permitir referência cruzada entre as duas.

---

## Resumo

Satélites em Órbita Terrestre Baixa (LEO) tornaram-se estruturalmente dependentes dos Sistemas Globais de Navegação por Satélite (GNSS) para determinação de órbita, sincronização de tempo, apoio à determinação de atitude, geolocalização de carga útil e manobras autônomas. A literatura de segurança trata essa dependência quase exclusivamente como um problema de *sinal* — como detectar spoofing, como rejeitar jamming — enquanto a literatura de cibersegurança espacial a trata quase exclusivamente como um problema de *princípio* — defesa em profundidade, secure-by-design, defesa informada por ameaças. Os dois corpos de trabalho raramente se encontram, e a consequência prática é que equipes de missão ouvem que "GNSS pode sofrer spoofing" sem jamais ouvir o que a sua espaçonave precisa, portanto, ser capaz de fazer.

Este artigo propõe o **GNSS-CRF**, um framework de ciber-resiliência que estreita essa lacuna ao tratar Posicionamento, Navegação e Tempo (PNT) não como uma entrada de sensor, mas como um *serviço portador de confiança* com um contrato de serviço derivado da missão. Ele se apoia diretamente em trabalho recente de Falco e colegas sobre derivação de requisitos cibernéticos espaciais mínimos a partir de prioridades de missão, e é melhor compreendido como uma especialização profunda e quantificada daquela abordagem para uma única dependência (Seção 2.5). O GNSS-CRF define uma cadeia de derivação de sete estágios — **Objetivo de Missão → Dependência de GNSS → Ameaça → Efeito → Detecção → Mitigação → Requisito Cibernético** — e um conjunto de regras que torna cada transição rastreável, de modo que um cenário de ataque PNT seja transformado deterministicamente em um requisito verificável de espaçonave, e não em uma recomendação.

Três argumentos distinguem o framework de uma checklist. Primeiro, sustentamos que em espaçonaves o perigo dominante não é a perda da solução de navegação, mas o **envenenamento do estimador**: PNT falso é absorvido pelo filtro de navegação e pela efeméride propagada, de modo que seu efeito *persiste depois de terminado o ataque* e a detecção precisa, portanto, ser consciente do estado, não apenas do sinal. Segundo, mostramos que a dinâmica orbital em LEO constitui uma **assimetria explorável a favor do defensor** — a trajetória de uma espaçonave é restringida por uma física que um spoofer baseado em solo precisa reproduzir com alta fidelidade através de uma janela curta e geometricamente desfavorável — e convertemos essa assimetria em primitivas concretas de detecção que não exigem qualquer suporte criptográfico. Terceiro, argumentamos que a unidade correta de mitigação não é um filtro, mas um **portão de autoridade**: o estado de confiança em PNT deve governar quais ações autônomas a espaçonave está autorizada a executar, e nenhuma atuação irreversível deveria ser executável sob PNT não confiável.

A aplicação da cadeia a oito objetivos representativos de missão LEO, e em seguida em profundidade a uma constelação hipotética de smallsats de vigilância marítima, produz uma **Baseline Mínima de Controles (MCB)** em camadas, com dezesseis controles mapeados para táticas do SPARTA, famílias de controle do NIST SP 800-53 Rev. 5 e o NIST IR 8323. Propomos também uma metodologia de avaliação e cinco métricas de resiliência (tempo até detecção, erro de estado induzido por spoofing no instante da detecção, crescimento do erro em holdover, correção do portão de autoridade e disponibilidade da missão sob ataque), junto com um plano de validação em hardware-in-the-loop. O estudo de caso produz um resultado que o framework não pressupôs: sob gating de viabilidade orbital, um único spoofer baseado em solo fica limitado a cerca de um quilômetro de erro de posição induzido pela própria capacidade de empuxo da espaçonave e pela geometria da passagem, e esse limite escala com a classe de propulsão ao longo de três ordens de grandeza — tornando o dimensionamento da propulsão um determinante da superfície de ataque PNT. O framework é analítico e não foi validado em voo; a Seção 10 declara essa limitação explicitamente e a Seção 11 define o programa experimental necessário para fechá-la.

**Palavras-chave:** satélites LEO, spoofing de GNSS, jamming, resiliência PNT, secure-by-design, cibersegurança espacial, SPARTA, engenharia de requisitos, modelagem de ameaças.

---

## 1. Introdução

### 1.1 Motivação

Uma espaçonave LEO moderna é, em sentido bastante literal, um receptor GNSS com uma carga útil acoplada. Receptores GPS/Galileo de bordo fornecem determinação de órbita em tempo real com acurácia da ordem do metro, disciplinam o relógio de bordo ao UTC, carimbam o tempo dos dados de carga útil, orientam o apontamento de antenas e instrumentos, agendam contatos com solo e — cada vez mais — fecham a malha de desvio autônomo de colisão e de voo em formação. Remover o GNSS não apenas degrada uma missão; para muitas arquiteturas de smallsat, remove a capacidade da espaçonave de saber onde e quando ela está.

Essa dependência cresceu ao mesmo tempo em que o ambiente de ameaças a PNT se deteriorou. Jamming e spoofing de GNSS migraram de demonstrações de laboratório para características rotineiras de regiões contestadas, e o incidente Viasat KA-SAT de 2022 demonstrou que adversários dispostos a atacar infraestrutura habilitada por espaço o farão com capacidade e intenção. Enquanto isso, a economia da indústria de smallsats empurrou operadores na direção de receptores comerciais de prateleira, sinais civis não autenticados e pilhas de software que jamais foram projetadas sob a hipótese de entradas adversariais.

A resposta de segurança foi bifurcada. De um lado, a comunidade de navegação — com destaque para Humphreys e colegas — produziu um corpo maduro de trabalho sobre a mecânica do spoofing, sua detectabilidade e o projeto de esquemas de autenticação. De outro, a comunidade de cibersegurança espacial — Falco, o projeto SPARTA da Aerospace Corporation, a SPD-5, os NIST IR 8270/8323 e o esforço IEEE P3349 — produziu princípios, matrizes de ameaça e catálogos de controle para sistemas espaciais como um todo. O que falta entre elas é um *método*: um procedimento repetível que tome uma missão específica, uma dependência de PNT específica e um ataque específico, e produza um requisito específico e testável que um engenheiro possa inserir numa especificação de espaçonave e que um revisor possa verificar.

### 1.2 Pergunta central de pesquisa

> **Qual é o conjunto mínimo de controles de cibersegurança de bordo que um satélite LEO dependente de GNSS precisa possuir para continuar operando — com segurança e dentro da tolerância da missão — durante spoofing e jamming de GNSS?**

Duas palavras nessa pergunta carregam o peso analítico. *Mínimo* significa que o framework precisa produzir um piso defensável em vez de um máximo aspiracional: espaçonaves são restringidas em massa, potência, processamento e cronograma, e uma baseline que ignore isso será, por sua vez, ignorada. *Continuar operando* significa que o objetivo é resiliência, não prevenção: o framework assume que o ataque tem sucesso na camada de sinal e pergunta o que precisa ser verdadeiro sobre a espaçonave para que a missão sobreviva a ele.

### 1.3 Contribuições

A ideia geral de derivar requisitos cibernéticos espaciais mínimos a partir de prioridades de missão **não** é reivindicada aqui como inédita: ela se deve a Falco e colegas (Seção 2.5), e este artigo é melhor lido como uma especialização profunda daquela ideia para uma única dependência.

1. **Uma cadeia formal de derivação (GNSS-CRF)** especializada em PNT, convertendo ataques a GNSS em requisitos de cibersegurança de espaçonave através de sete estágios rastreáveis, com regras de transição explícitas e condições quantitativas de adequação em cada estágio (Seção 4).
2. **O Contrato de Serviço PNT**, uma especificação por objetivo de limites de acurácia, integridade, holdover e autenticidade, que torna a "dependência de GNSS" uma grandeza mensurável em vez de uma afirmação qualitativa (Seção 4.2).
3. **O argumento do envenenamento do estimador**: uma caracterização de por que ataques de decepção contra espaçonaves diferem fundamentalmente de ataques de decepção contra receptores terrestres, e os requisitos de recuperação que isso implica (Seções 3.4 e 4.3).
4. **A dinâmica LEO como primitiva de detecção**: quatro testes de detecção derivados da mecânica orbital e da geometria de sinal em LEO, indisponíveis a usuários terrestres e sem necessidade de suporte criptográfico (Seção 4.3, estágio 5).
5. **A Máquina de Estados de Confiança PNT e o gating de autoridade**, um mecanismo que vincula a autoridade autônoma da espaçonave ao nível de confiança em PNT, com a regra de que nenhuma atuação irreversível é permitida sob PNT não confiável (Seção 4.5).
6. **Uma Baseline Mínima de Controles em camadas**, com dezesseis controles que respondem à pergunta central, mapeados para SPARTA, NIST SP 800-53 Rev. 5 e NIST IR 8323 (Seção 7).
7. **Um estudo de caso hipotético** levado até os números, que produz um limite quantitativo para o erro induzido por spoofing alcançável, identifica um acoplamento até então não declarado entre arquitetura de propulsão e superfície de ataque PNT, e demonstra a capacidade do framework de *eliminar* requisitos além de gerá-los (Seção 6).
8. **Uma metodologia de avaliação** com cinco métricas, três predições falsificáveis e um plano de validação em hardware-in-the-loop (Seção 8).

### 1.4 Escopo e estrutura

O framework trata do **segmento espacial** de uma missão LEO: a espaçonave, seu receptor GNSS, seu filtro de navegação, seu relógio e sua autonomia. Segurança de segmento de solo e de camada de enlace (autenticação de comandos, criptografia de TT&C, endurecimento de estações terrenas) é tratada como pré-condição assumida como presente — não por ser pouco importante (o incidente Viasat mostra o contrário), mas porque está bem coberta em outros lugares e porque a contribuição aqui é especificamente sobre dependência de PNT. A Seção 2 revisa as duas literaturas de origem e enuncia a lacuna. A Seção 3 apresenta o modelo de ameaças. A Seção 4 define o framework. A Seção 5 o aplica a oito objetivos de missão, e a Seção 6 o aplica em profundidade a uma missão hipotética. A Seção 7 apresenta a baseline. As Seções 8–11 cobrem avaliação, discussão, limitações e conclusões.

---

## 2. Fundamentação e Trabalhos Relacionados

### 2.1 A natureza da dependência de GNSS em LEO

A recepção de GNSS em LEO é geometricamente diferente da recepção em solo, e a diferença importa tanto para o ataque quanto para a defesa.

Constelações GNSS ocupam a Órbita Terrestre Média a cerca de 20.200 km de altitude, com antenas de transmissão apontadas para a Terra. Uma espaçonave a 400–800 km de altitude fica *abaixo* dessa constelação e, portanto, não enxerga os satélites diretamente acima como faz um usuário em solo. Em vez disso, ela adquire sinais de satélites GNSS do lado oposto da Terra, cujas emissões de lóbulo principal passam sobre o limbo terrestre, complementados por energia de lóbulos laterais. As consequências práticas são: menos satélites utilizáveis, potência recebida mais fraca do que a especificação ao nível do solo, geometria pior e que muda mais rapidamente, e desvios Doppler uma ordem de grandeza maiores do que os de um usuário terrestre estático — da ordem de dezenas de quilohertz em L1, causados pela própria velocidade orbital de ~7,5 km/s da espaçonave.

A bordo, o receptor raramente alimenta soluções brutas diretamente nas funções de missão. Ele alimenta um filtro de navegação — tipicamente um filtro de Kalman estendido ou unscented — que funde medições GNSS com um modelo dinâmico da órbita e, em plataformas mais capazes, com sensores inerciais e de atitude. Determinação de órbita de bordo em tempo real na classe do metro é rotineira com essa arquitetura; o pós-processamento em solo alcança nível centimétrico. O filtro é o que torna o GNSS útil em LEO e, como argumenta a Seção 3.4, é também o que torna a decepção de GNSS perigosa em LEO.

A dependência não se restringe à posição. A solução de tempo do GNSS disciplina o relógio de bordo, e esse relógio sustenta janelas de validade criptográfica, proteção contra replay, ordenação de logs, carimbo temporal de carga útil, agendamento de enlaces intersatélites e janelas de contato com solo. O tempo é frequentemente a dependência mais profunda e menos documentada de uma espaçonave, e é aquela cuja corrupção produz o maior dano interdomínio.

### 2.2 Ameaças a PNT e detecção de spoofing (a linha de trabalho de Humphreys)

A literatura de segurança em navegação, desenvolvida substancialmente por Humphreys e pelo Radionavigation Laboratory da Universidade do Texas, e por colegas nas comunidades ION e IEEE, estabelece diversos resultados que este framework toma como dados.

**Ataques são baratos e já não são exóticos.** Spoofers civis portáteis de GPS construídos com componentes de rádio definido por software foram demonstrados há mais de quinze anos, e as demonstrações públicas subsequentes contra um VANT e contra uma embarcação de superfície mostraram que um spoofer bem construído consegue capturar as malhas de rastreamento de um receptor e afastar a solução reportada da verdade de forma suficientemente suave para que a própria instrumentação da vítima reporte operação nominal o tempo todo.

**Decepção é mais perigosa que negação.** O jamming se anuncia: o receptor perde o travamento, sinaliza perda de solução, e os consumidores a jusante podem reagir a uma falha explícita. Um spoof bem executado produz uma solução *plausível, internamente consistente, porém falsa*, e o sistema segue operando confiantemente sobre dados errados. A dificuldade de detecção é, portanto, inversamente relacionada à sofisticação do ataque, e o modo de falha é silencioso.

**A detecção é em camadas, e nenhuma camada isolada é suficiente.** A literatura organiza as contramedidas em famílias que este framework adota e estende: monitoramento em nível de sinal (anomalias de controle automático de ganho e de C/N0, distorção da função de correlação, tetos de potência recebida), consistência em nível de medição (monitoramento autônomo de integridade no receptor e suas variantes avançadas, testes de resíduo e de inovação, consistência entre Doppler e taxa de pseudodistância), discriminação espacial (estimação de ângulo de chegada com múltiplos elementos de antena, sob o princípio de que sinais autênticos chegam de muitas direções e um spoof tipicamente chega de uma só), monitoramento do comportamento do relógio, e verificação cruzada contra sensores independentes não-GNSS.

**A autenticação criptográfica ajuda, mas não fecha o problema.** A autenticação da mensagem de navegação — o OSNMA do Galileo e o conceito Chimera para o GPS — permite a um receptor verificar que os dados de navegação decodificados se originaram no operador da constelação. Isso derrota a falsificação em nível de dados. Não derrota por si só o meaconing (sinais autênticos gravados e retransmitidos com atraso), porque os bits retransmitidos são genuínos; derrotar replay exige restrições temporais adicionais. Além disso, esquemas baseados em divulgação retardada de chave impõem uma latência de autenticação que precisa ser conciliada com o orçamento de holdover da missão — um trade-off que este framework torna explícito na Seção 4.2.

Os números publicados tornam esse trade-off concreto em vez de abstrato. O OSNMA do Galileo entrou em sua fase de observação pública em 15 de novembro de 2021 e foi declarado operacionalmente disponível em 24 de julho de 2025. O aprimoramento de sinal Chimera da AFRL para o GPS L1C, embarcado como experimento no satélite NTS-3 lançado em 12 de agosto de 2025, autentica um receptor autônomo — aquele que dispõe apenas do sinal GNSS — aproximadamente **uma vez a cada três minutos**, com intervalos mais curtos (da ordem de segundos) disponíveis apenas a usuários capazes de receber a chave por um canal fora de banda. Um intervalo de autenticação de três minutos cabe confortavelmente dentro de um orçamento de holdover de seis horas para determinação de órbita, e fica confortavelmente fora do tempo de reação disponível para uma decisão autônoma de desvio de colisão. Se a autenticação criptográfica é um controle utilizável para um dado objetivo não é, portanto, uma questão geral sobre o esquema; é uma questão sobre o `η` daquele objetivo — que é exatamente o que a condição de adequação (i) do framework obriga o analista a calcular.

**A interferência é observável a partir da órbita.** O grupo de Humphreys também publicou resultados plurianuais de monitoramento de interferência GNSS conduzido *a partir* da órbita terrestre baixa, geolocalizando fontes terrestres de jamming desde uma plataforma LEO. Isso importa a este artigo de duas maneiras: é evidência empírica direta de que o ponto de vista LEO carrega informação explorável sobre interferência de RF terrestre, e sustenta o argumento de atribuibilidade feito para a camada de detecção D4 na Seção 4.3.

**PNT em LEO é uma alternativa emergente.** Trabalhos recentes, incluindo as investigações de Humphreys sobre PNT oportunista a partir de downlinks de banda larga em LEO, apontam para a diversificação das fontes de PNT. Este framework trata tais fontes como candidatas a entradas alternativas de navegação (Seção 4.3, estágio 6), observando que ainda não estão maduras o bastante para serem assumidas como presentes numa baseline mínima.

### 2.3 Princípios de cibersegurança de sistemas espaciais (a linha de trabalho de Falco)

A segunda literatura de origem aborda espaçonaves como sistemas ciberfísicos, e não como rádios. O trabalho de Falco — incluindo o argumento de que sistemas espaciais foram tratados como um vácuo de segurança, a articulação de princípios de cibersegurança para sistemas espaciais, e a liderança de esforços de padronização como o IEEE P3349 — estabeleceu diversas posições sobre as quais este framework se constrói.

**Segurança precisa ser projetada, não acrescentada.** Uma espaçonave não pode receber patches como um servidor. As janelas de uplink são curtas, a banda é escassa, uma atualização malsucedida é potencialmente fatal para a missão, e a plataforma voará por anos com a arquitetura com que foi lançada. Propriedades de segurança que não estejam presentes no congelamento do projeto estão, na prática, permanentemente ausentes. Este é o argumento mais forte disponível para derivar requisitos cibernéticos *antes* de o projeto ser fixado — que é precisamente para o que serve o GNSS-CRF.

**Prioridades de missão precisam guiar decisões de segurança.** Nem todas as funções de uma espaçonave merecem proteção igual, e um catálogo de controles aplicado uniformemente desperdiça justamente os recursos escassos de que sistemas espaciais menos dispõem. O investimento em segurança deve decorrer daquilo que a missão não pode perder. O GNSS-CRF operacionaliza isso iniciando toda cadeia de derivação em um objetivo de missão e escalando a prioridade do requisito resultante à criticidade do objetivo.

**Requisitos mínimos viáveis são a saída útil.** Para o setor de smallsats e comercial, um conjunto máximo de controles é aspiracional; um piso defensável é acionável. A Baseline Mínima de Controles da Seção 7 é escrita nesse espírito.

**Defesa informada por ameaças precisa de um modelo específico do domínio espacial.** Modelos genéricos de ameaça de TI não capturam ataques em camada de RF, dinâmica orbital, acoplamento com o segmento de solo, nem a irreversibilidade das ações em órbita.

### 2.4 SPARTA como substrato de modelagem de ameaças

O SPARTA (Space Attack Research and Tactic Analysis), desenvolvido e publicado pela **The Aerospace Corporation**, fornece uma matriz no estilo ATT&CK adaptada a sistemas espaciais, abrangendo os segmentos espacial, de enlace, de solo e de usuário. Suas nove táticas são Reconnaissance (ST0001), Resource Development (ST0002), Initial Access (ST0003), Execution, Persistence, Defense Evasion, Lateral Movement, Exfiltration e Impact, cada uma povoada por técnicas, subtécnicas e contramedidas específicas do domínio espacial.

O GNSS-CRF usa o SPARTA em dois pontos da cadeia. No estágio 3 (Ameaça), o SPARTA fornece o vocabulário e a verificação de completude: uma enumeração de ameaças só é defensável se tiver sido percorrida contra uma matriz publicada, em vez de montada a partir da imaginação do analista. No estágio 7 (Requisito Cibernético), os identificadores de técnica do SPARTA tornam-se a âncora de rastreabilidade que liga um requisito específico da missão de volta a um comportamento adversarial documentado — o que é o que torna o requisito auditável por um terceiro.

*Nota sobre higiene de citação:* identificadores de técnica do SPARTA são versionados e mudam entre releases. Ao longo deste artigo nomeamos **táticas** do SPARTA, que são estáveis, e marcamos identificadores de técnica como campos a serem preenchidos contra a matriz vigente no momento do uso. Analistas que apliquem o framework devem fixar (pin) a versão da matriz em seu registro de rastreabilidade.

### 2.5 O trabalho anterior mais próximo

Uma publicação está consideravelmente mais próxima deste artigo do que o restante de qualquer das duas literaturas, e a honestidade quanto à reivindicação de ineditismo exige dizê-lo claramente. Falco, Boschetti, Vecellio Segate, Maple e colegas, em *Minimum Requirements for Space System Cybersecurity — Ensuring Cyber Access to Space* (IEEE SMC-IT, 2024), propõem um método escalável e extensível para derivar princípios mínimos de projeto cibernético, e requisitos subsequentes, para um sistema espacial **a partir de uma prioridade de missão declarada**. Eles o testam sobre a prioridade de missão de preservar o acesso ao espaço impedindo a perda permanente de controle de um satélite, e expressam a saída como declarações "shall" de requisito mínimo.

Esse é o mesmo movimento fundamental que este artigo faz — prioridade de missão primeiro, requisitos como artefato de saída, declarações "shall" como formato — e a reivindicação geral de ter inventado a derivação de requisitos cibernéticos espaciais mínimos orientada à missão pertence, portanto, àquele trabalho, e não a este. O que este artigo acrescenta é profundidade em uma dimensão que um método geral necessariamente deixa em aberto:

- **Uma dependência específica e quantificada.** O método deles toma uma prioridade de missão; o GNSS-CRF toma um objetivo de missão *e um Contrato de Serviço PNT* com limites numéricos de acurácia, integridade, holdover e autenticidade (Seção 4.2), que é o que permite às condições de adequação da Seção 4.3 e à aritmética da Seção 6 existirem.
- **Uma física de ameaça específica.** O GNSS-CRF é construído em torno da superfície de ataque PNT — spoofing, meaconing, jamming, exploração do receptor e arrasto temporal — e não em torno da perda de controle em geral.
- **Persistência do efeito em estimadores.** A análise de envenenamento do estimador da Seção 3.4 não tem contrapartida em um método de nível de princípio.
- **Detecção como estágio de primeira classe.** A cadeia deles vai de prioridade a princípio a requisito; o GNSS-CRF insere detecção e mitigação como estágios separados, com suas próprias regras de seleção, porque para PNT o requisito é largamente determinado pelo que se consegue detectar e com que rapidez.
- **Gating de autoridade.** Vincular autoridade autônoma a um estado de confiança PNT (Seção 4.5) não está presente, pela nossa leitura, no método anterior.

*Ressalva, declarada para proteção do leitor:* o texto completo do artigo do SMC-IT não pôde ser obtido durante a preparação deste rascunho, e a caracterização acima baseia-se em seu resumo e em metadados publicados. **Ele precisa ser lido integralmente e esta subseção revisada de acordo antes da submissão.** Se o método deles já abranger qualquer um dos cinco pontos acima, a reivindicação de contribuição correspondente na Seção 1.3 precisa ser retirada ou restringida.

### 2.6 A lacuna

A Tabela 1 enuncia a lacuna diretamente.

| | Literatura de segurança em navegação | Literatura de cibersegurança espacial | Falco et al. 2024 (trabalho anterior mais próximo) | GNSS-CRF |
|---|---|---|---|---|
| Objeto primário | O sinal e o receptor | A espaçonave e a organização | A prioridade de missão | O objetivo de missão e seu contrato PNT |
| Tratamento da ameaça | Profundo, quantitativo, específico de RF | Amplo, em nível de tática, guiado por matriz | Perda de controle, genericamente | Específico de PNT (T1–T9), via vocabulário SPARTA |
| Saída | Algoritmos de detecção, esquemas de autenticação | Princípios, catálogos de controle, matrizes de ameaça | Declarações "shall" de requisito mínimo | Declarações "shall" com limites e métodos de V&V |
| Dependência quantificada | N/A | Não | Não, pela nossa leitura | Sim — `⟨D, α, ι, η, A⟩` (Seção 4.2) |
| Trata persistência no estimador | Raramente (receptores terrestres costumam ser sem memória) | Não | Não | Explicitamente (Seção 3.4) |
| Detecção como estágio de derivação | É o assunto inteiro | Não | Não | Sim, com condições de adequação (Seção 4.3) |
| Trata autoridade da autonomia | Não | Parcialmente (via controle de acesso genérico) | Não, pela nossa leitura | Explicitamente (Seção 4.5) |
| Rastreabilidade à missão | Ausente | Afirmada como princípio | Mecanizada | Mecanizada, com limites numéricos |

**Tabela 1.** Posicionamento do GNSS-CRF em relação às duas literaturas de origem e ao trabalho anterior mais próximo. As entradas na coluna Falco et al. estão marcadas como "pela nossa leitura" porque se apoiam no resumo e nos metadados daquele artigo, e não em seu texto completo — ver a ressalva na Seção 2.5.

A lacuna não é que qualquer das literaturas esteja errada, nem que ninguém tenha tentado uni-las — a Seção 2.5 mostra que a ponte já foi iniciada. É que a ponte geral, por ser geral, não consegue carregar as grandezas das quais a resiliência PNT depende: uma tolerância de acurácia, um orçamento de holdover, uma latência de detecção, e as condições de adequação que os relacionam. Um método que para na declaração "shall" deixa a pergunta mais difícil — *este requisito é suficiente?* — sem resposta. O que um programa de espaçonave precisa no congelamento do projeto é um requisito com um limite, um método de verificação e uma demonstração de que a detecção é rápida o bastante para importar, rastreável tanto a um objetivo de missão quanto a uma ameaça documentada.

---

## 3. Modelo de Ameaças

### 3.1 Adversário

Assumimos um adversário com as seguintes capacidades:

- **Capacidade de RF.** Consegue transmitir nas bandas GNSS a partir de plataformas terrestres ou aéreas com alta potência efetiva irradiada, e consegue gerar sinais com rádios definidos por software usando especificações civis publicadas. Consegue gravar e retransmitir sinais autênticos.
- **Conhecimento.** Conhece a órbita aproximada do alvo — hipótese razoável, já que órbitas LEO são catalogadas publicamente — e consegue prever a geometria e o instante das passagens.
- **Persistência.** Consegue atacar repetidamente ao longo de passagens sobre território que controla, e coordenar ataques a partir de múltiplos sítios em solo.
- **Capacidade cibernética.** Consegue forjar dados de navegação malformados ou semanticamente hostis destinados a explorar o firmware do receptor, e pode ter tentado influência de cadeia de suprimentos sobre o firmware do receptor ou sobre dados de auxílio.

Assumimos que o adversário **não consegue** quebrar a criptografia de sinais autenticados onde tais sinais sejam usados, não consegue posicionar transmissores em órbita acima do alvo, e não possui autoridade válida de comando sobre a espaçonave. Esta última hipótese importa: um adversário com autoridade de comando não precisa fazer spoofing de GNSS, e defender-se desse caso é problema do segmento de solo, não deste framework.

### 3.2 Superfície de ataque

A superfície de ataque PNT de uma espaçonave LEO compreende cinco pontos de entrada:

1. **O front end de RF** — a antena e a cadeia receptora, expostas a jamming, meaconing e spoofing.
2. **O conteúdo dos dados de navegação** — efemérides, almanaque e correções de relógio decodificados do sinal, expostos a falsificação onde não há autenticação, e à exploração da lógica de parsing do receptor por entradas malformadas.
3. **O filtro de navegação** — exposto à injeção de medições individualmente plausíveis, porém coletivamente enganosas.
4. **Dados de auxílio enviados por uplink** — atualizações de órbita, TLEs, correções diferenciais e referências de tempo fornecidas do solo, expostas a comprometimento do segmento de solo ou a corrupção na cadeia de suprimentos.
5. **A malha de disciplinamento do relógio de bordo** — exposta a ataques lentos de arrasto temporal que deslocam o tempo da espaçonave sem jamais produzir um salto obviamente anômalo.

### 3.3 Taxonomia de ameaças

| ID | Ameaça | Mecanismo | Classe de efeito primária |
|---|---|---|---|
| **T1** | Jamming de banda larga | Ruído de alta potência ao longo da banda | Negação |
| **T2** | Jamming de banda estreita / chirp / pulsado | Interferência dirigida, possivelmente intermitente para evadir monitoramento | Negação, degradação intermitente |
| **T3** | Meaconing (replay) | Sinais autênticos gravados e retransmitidos com atraso | Decepção (deslocamento de posição e tempo) |
| **T4** | Spoofing por sobreposição (tomada suave) | Sinais falsos alinhados aos autênticos, potência elevada gradualmente, solução afastada da verdade | Decepção (silenciosa, pior caso) |
| **T5** | Spoofing assíncrono | Constelação falsa transmitida sem alinhamento; força reaquisição sobre sinais falsos | Decepção, precedida de breve negação |
| **T6** | Falsificação de dados de navegação | Parâmetros falsos de efeméride/relógio injetados onde o sinal não é autenticado | Decepção com longa persistência |
| **T7** | Exploração do receptor | Quadros de navegação malformados usados para disparar falhas de segurança de memória ou de lógica no firmware do receptor | Comprometimento do próprio receptor |
| **T8** | Corrupção de dados de auxílio | Dados de órbita/tempo/correção enviados por uplink, maliciosos ou corrompidos | Decepção, contornando todas as defesas de RF |
| **T9** | Ataque de arrasto temporal | Manipulação lenta e sublimiar da solução de tempo | Cascata interdomínio (cripto, logs, agendamento) |

**Tabela 2.** Taxonomia de ameaças PNT usada ao longo do framework. T1–T6 mapeiam para a literatura de segurança em navegação; T7–T9 são as ameaças de cruzamento cibernético que motivam tratar PNT como um problema de segurança e não de processamento de sinais.

### 3.4 O perigo central: envenenamento do estimador

A afirmação mais importante desta seção é que espaçonaves respondem à decepção de modo diferente de receptores terrestres, e que a diferença é arquitetural, não incidental.

Um receptor de mão é quase sem memória. Quando um spoof termina, a solução seguinte é computada a partir do próximo conjunto de medições, e a decepção termina com ele. Um filtro de navegação de espaçonave não é sem memória. Ele mantém uma estimativa de estado e uma covariância, e funde medições conforme o quanto confia naquele estado. Isso produz três consequências específicas de espaçonaves:

**Persistência.** Medições falsas aceitas pelo filtro alteram a estimativa de estado. Quando o ataque cessa, a estimativa não volta sozinha — ela precisa ser trazida de volta por medições autênticas subsequentes, e quanto mais confiante o filtro tiver ficado no estado envenenado, mais lentamente isso acontece.

**Inversão de confiança.** Um spoof habilmente executado produz medições *mais* mutuamente consistentes que as autênticas, porque o atacante controla todas elas e o mundo real contém ruído. A covariância do filtro, portanto, encolhe: o estimador torna-se maximamente confiante exatamente quando está maximamente errado. Qualquer esquema de detecção que trate resíduos baixos como evidência de saúde será invertido por isso.

**Propagação.** O estado envenenado não fica confinado ao filtro. Ele é escrito na efeméride propagada, nas soluções de órbita armazenadas, nos metadados de carga útil já transmitidos ao solo, e nas tabelas de agendamento. Um ataque que dure uma passagem pode corromper produtos por dias.

As consequências de projeto são diretas, e são a razão pela qual o framework não para na detecção:

- A detecção precisa incluir testes **conscientes do estado** (a trajetória estimada permanece fisicamente viável?) e não apenas testes conscientes do sinal, porque testes de sinal podem ser derrotados por um atacante com fidelidade suficiente, enquanto a física não pode.
- O sistema precisa ser capaz de **colocar em quarentena e reverter** o estado do filtro, o que significa que precisa manter checkpoints de estado confiável e reter a capacidade de reinicializar a partir de uma âncora não-GNSS.
- Produtos gerados sob confiança PNT degradada precisam ser **rotulados** com esse nível de confiança, de modo que a corrupção seja delimitada e identificável a posteriori em vez de silenciosamente misturada ao acervo.

### 3.5 Classes de efeito

Classificamos os efeitos em cinco classes, usadas no estágio 4 da cadeia:

| Classe | Definição | Detectabilidade | Persistência após o fim do ataque |
|---|---|---|---|
| **E1 Negação** | Perda da solução PNT | Alta (explícita) | Nenhuma |
| **E2 Degradação** | Solução disponível, porém fora da tolerância de acurácia | Média | Baixa |
| **E3 Decepção** | Solução plausível, porém falsa | Baixa | **Alta** (envenenamento do estimador) |
| **E4 Temporal** | Deslocamento ou deriva de relógio induzidos | Baixa | **Alta** (propaga para cripto, logs, agendamento) |
| **E5 Comprometimento** | Estado do receptor ou do software alterado por entrada hostil | Muito baixa | **Permanente até remediação** |

**Tabela 3.** Classes de efeito. Note a relação inversa entre detectabilidade e persistência: os efeitos mais difíceis de enxergar são os que duram mais. Essa relação é a justificativa central da ênfase do framework em recuperação e gating de autoridade, e não em detecção isoladamente.

---

## 4. O Framework GNSS-CRF

### 4.1 Visão geral

O GNSS-CRF é uma cadeia de derivação de sete estágios. Cada estágio consome a saída do anterior e aplica uma regra de transição declarada, de modo que o requisito final possa ser rastreado para trás até o objetivo de missão que o justifica, e para frente até o método de verificação que o confirma.

```
   [1]              [2]               [3]          [4]         [5]           [6]            [7]
Objetivo   →    Dependência  →    Ameaça    →   Efeito   →  Detecção   →  Mitigação   →  Requisito
de Missão       de GNSS                                                                  Cibernético
   |                |                 |            |            |             |              |
 o que a         quais serviços    qual        o que faz    como          o que          o que a
 missão não      PNT, com que      ataque      com o        percebemos    fazemos        espaçonave
 pode perder     tolerância        a alcança   objetivo                   a respeito     DEVE fazer,
                                                                                         com um limite
```

**Figura 1.** A cadeia de derivação do GNSS-CRF.

A cadeia é aplicada uma vez por par (objetivo, ameaça). Uma missão com oito objetivos e nove ameaças não exige setenta e duas análises, porque a maioria dos pares é eliminada no estágio 2: uma ameaça que não consegue alcançar uma dependência que o objetivo não possui está fora de escopo, e a própria eliminação é registrada — o que é o que torna a análise auditável quanto à completude.

### 4.2 Definições formais

**Objetivos de missão.** Seja `O = {o₁, …, oₙ}` o conjunto de objetivos de missão, cada um com uma criticidade `κ(oᵢ) ∈ {catastrófico, crítico, maior, menor}` atribuída pela própria análise de perigos da missão. A criticidade é herdada da prática de segurança (safety) e de garantia de missão, em vez de inventada aqui, o que mantém o framework compatível com a documentação de programa existente.

**Serviços PNT.** Seja `S = {P, V, T}` os serviços de posição, velocidade e tempo.

**O Contrato de Serviço PNT.** Para cada objetivo, a dependência é expressa não como um booleano, mas como um contrato:

```
C(oᵢ) = ⟨ D, α, ι, η, A ⟩

  D  ⊆ S              quais serviços PNT o objetivo consome
  α                   limite de acurácia: erro máximo tolerável com o objetivo ainda atendido
  ι                   limite de integridade: probabilidade máxima de erro fora de limite não detectado
  η                   orçamento de holdover: por quanto tempo o objetivo sobrevive sem atualização PNT válida
  A  ∈ {nenhuma, dados, fonte, plena}   nível de autenticidade exigido da entrada PNT
```

O orçamento de holdover `η` é o número mais útil que o framework produz, e a maioria das missões nunca o calculou. É a resposta a "por quanto tempo esta função consegue operar de memória?", e determina diretamente se um esquema de autenticação com divulgação retardada de chave é utilizável, se um relógio atômico em escala de chip é necessário ou se um oscilador compensado em temperatura basta, e se uma latência de detecção de trinta segundos é tolerável ou fatal.

**Ameaças e efeitos.** Seja `T = {T1, …, T9}` o conjunto de ameaças da Tabela 2 e `E = {E1, …, E5}` as classes de efeito da Tabela 3. O mapeamento de efeito é

```
ε : O × T → E × ℝ⁺ × ℝ⁺
```

produzindo uma classe de efeito, uma magnitude (o erro induzido, nas unidades de `α`) e um tempo de persistência (por quanto tempo o efeito sobrevive ao ataque).

**Violação de contrato.** Um par (objetivo, ameaça) está **em escopo** se e somente se o efeito viola o contrato:

```
viola(oᵢ, tⱼ)  ⇔  magnitude(ε(oᵢ,tⱼ)) > α(oᵢ)
               ∨  persistência(ε(oᵢ,tⱼ)) > η(oᵢ)
               ∨  A(oᵢ) não é satisfeito pelo sinal disponível
```

Este predicado é a regra de eliminação que mantém a análise tratável, e é também o mecanismo de honestidade mais importante do framework: um analista que não consegue enunciar `α` e `η` não consegue avaliá-lo e, portanto, não pode alegar ter analisado a dependência.

**Detecção e mitigação.** Seja `Δ` o conjunto de mecanismos de detecção, com, para cada `d ∈ Δ`, uma latência de detecção `λ(d)`, uma probabilidade de detecção `P_d(d, tⱼ)` contra a ameaça `tⱼ`, e uma taxa de alarme falso `P_fa(d)`. Seja `M` o conjunto de mitigações, cada uma com uma função de risco residual e um custo de recursos em massa, potência, processamento e esforço de engenharia não recorrente.

**A regra de derivação de requisitos.** Para cada par em escopo, o requisito derivado precisa satisfazer três condições simultaneamente:

```
R(oᵢ, tⱼ) é adequado  ⇔
      (i)   λ(d) + t_resposta  <  η(oᵢ)               [tempestividade]
      (ii)  P_d(d, tⱼ) ≥ 1 − ι(oᵢ)                     [integridade]
      (iii) erro_residual após mitigação ≤ α(oᵢ)       [tolerância]
```

A condição (i) é a mais frequentemente violada na prática: um esquema de detecção que funciona mas reporta depois de expirado o orçamento de holdover fornece perícia, não resiliência. Enunciá-la como condição formal de adequação força o trade-off entre confiança de detecção e velocidade de detecção a ser feito explicitamente e defendido, em vez de descoberto durante uma revisão de anomalia.

**Prioridade do requisito.** O nível de prioridade do requisito derivado é função da criticidade do objetivo, da persistência do efeito e da recuperabilidade:

```
prioridade(R) = f( κ(oᵢ), persistência(ε), recuperabilidade )
```

com a regra de que qualquer requisito que trate de um efeito **irreversível em órbita** — uma manobra propulsiva executada sobre posição falsa, um comando de deorbit, uma entrada irrecuperável em modo seguro — é promovido ao nível mais alto independentemente da probabilidade atribuída à ameaça. Irreversibilidade, e não verossimilhança, é o termo dominante em sistemas espaciais, porque não existe desfazer em órbita.

### 4.3 Os estágios

**Estágio 1 — Objetivo de Missão.** Enumere o que a missão não pode perder, em linguagem de missão e não em linguagem de engenharia: *manter conhecimento de órbita suficiente para avaliação de conjunção*, *entregar imageamento geolocalizado dentro da especificação*, *manter rastreabilidade temporal para a carga útil*, *executar desvio autônomo de colisão*. Atribua `κ`. A disciplina aqui é resistir a começar pelo receptor; começar pelo receptor produz requisitos de receptor, que é justamente a falha que este framework existe para corrigir.

**Estágio 2 — Dependência de GNSS.** Para cada objetivo, complete o contrato `C(oᵢ)`. Três perguntas costumam ser reveladoras: qual de P, V, T este objetivo *de fato* consome, por oposição ao que ele por acaso recebe; que erro faria o objetivo falhar, e não apenas degradar; e por quanto tempo este objetivo conseguiria operar se o GNSS desaparecesse agora. Dependências ocultas de tempo emergem neste estágio mais do que qualquer outra coisa, porque tempo é consumido por funções cujos projetistas nunca se consideraram usuários de GNSS.

**Estágio 3 — Ameaça.** Percorra a taxonomia de ameaças da Tabela 2 contra a dependência, com verificação cruzada contra a matriz SPARTA para completude. Registre as eliminações com justificativa. A saída é o conjunto de ameaças que consegue fisicamente alcançar essa dependência.

**Estágio 4 — Efeito.** Para cada ameaça sobrevivente, determine a classe de efeito, a magnitude nas unidades de `α` e a persistência. É aqui que a análise de envenenamento do estimador da Seção 3.4 é aplicada: a pergunta não é o que o receptor reporta durante o ataque, mas como fica o *estado da missão* depois dele. Avalie `viola()`. Pares que não violam o contrato são documentados e encerrados.

**Estágio 5 — Detecção.** Selecione mecanismos de detecção sujeitos às condições de adequação (i) e (ii). Organizamos os mecanismos disponíveis em cinco camadas, das quais a quarta é específica de espaçonaves e, argumentamos, subexplorada.

*Camada D1 — Nível de sinal.* Monitoramento de controle automático de ganho e de C/N0; testes de teto de potência recebida; monitoramento de distorção da função de correlação; monitoramento espectral em busca de assinaturas de jamming. Rápida, barata, derrotada por um atacante cuidadoso.

*Camada D2 — Nível de medição.* RAIM e suas variantes avançadas; teste de resíduos de pseudodistância; consistência entre a taxa de distância derivada do Doppler e a diferenciação de pseudodistância; continuidade de fase de portadora. Eficaz contra spoofs inconsistentes, derrotada por um spoof plenamente autoconsistente.

*Camada D3 — Criptográfica.* Autenticação da mensagem de navegação (OSNMA, Chimera) onde disponível. Derrota a falsificação de dados (T6) por completo. Não derrota meaconing sem restrições temporais adicionais, e impõe uma latência de autenticação que precisa ser confrontada com `η` sob a condição de adequação (i).

*Camada D4 — Dinâmica orbital e geometria LEO.* Esta é a camada que argumentamos ser distintiva, porque o movimento de uma espaçonave é restringido por uma física que o atacante precisa reproduzir exatamente e cuja verificação nada custa ao defensor:

  - **Viabilidade kepleriana.** Uma trajetória reportada precisa ser consistente com movimento de dois corpos mais perturbações conhecidas (J2, arrasto, pressão de radiação solar) e com a capacidade propulsiva conhecida da espaçonave. Uma sequência de posições que implique aceleração não modelada superior à que os propulsores conseguem produzir não é uma trajetória possível, e nenhuma dose de autoconsistência interna nas medições falsas consegue esconder isso.
  - **Geometria da vista do céu.** A partir da LEO, o conjunto esperado de satélites GNSS visíveis, suas elevações aproximadas e sua distribuição de intensidade de sinal são previsíveis a partir do almanaque e da órbita. Um spoofer em solo que produza uma constelação cuja geometria implícita corresponda à vista do céu de um usuário terrestre — ou cujos sinais cheguem todos de um único setor angular estreito próximo ao limbo — é inconsistente com a física da recepção em altitude.
  - **Consistência do perfil Doppler.** A assinatura Doppler de um receptor movendo-se a ~7,5 km/s é grande e altamente estruturada, evoluindo de modo previsível ao longo de uma passagem. Reproduzi-la exige que o atacante modele a dinâmica do alvo de forma precisa e contínua.
  - **Plausibilidade do balanço de enlace.** Sobrepujar sinais GNSS autênticos na altitude LEO a partir do solo exige potência efetiva irradiada muito alta, dirigida a um alvo em movimento rápido através de uma janela de duração limitada. O ataque é, portanto, geometricamente restringido e, em princípio, detectável como um evento anômalo de potência correlacionado a uma região específica do solo — o que também o torna *atribuível* ao longo de passagens repetidas.

  A camada D4 não exige hardware adicional, apenas computação e um modelo que a espaçonave já carrega. Para smallsats com restrição de recursos, esta é a camada de detecção de maior valor disponível, e é a menos tratada na literatura existente.

*Camada D5 — Interdomínio.* Comparação contra star tracker, sensor solar, magnetômetro e medições inerciais; contra soluções de órbita fornecidas do solo recebidas por enlace autenticado; contra telemetria de distância entre satélites; e contra efeméride propagada de forma independente. Lenta, mas independente do canal atacado — o que é o que a torna a âncora da recuperação.

A regra do framework neste estágio é que **pelo menos duas camadas de bases físicas distintas precisam estar presentes** para qualquer objetivo cujo contrato especifique `A ≥ fonte`, já que a detecção de camada única tem uma única condição de derrota.

**Estágio 6 — Mitigação.** As mitigações são selecionadas ao longo de cinco funções:

  - *Prevenir:* antenas de padrão de recepção controlado ou anulação de feixe onde massa e custo permitam; filtragem de front end; endurecimento do firmware do receptor e validação de entrada contra T7; habilitação de sinais autenticados onde disponíveis.
  - *Detectar e isolar:* a Máquina de Estados de Confiança PNT da Seção 4.5; gating de inovação no filtro de navegação, com a ressalva explícita da Seção 3.4 de que o gating não pode tratar resíduos baixos como prova de saúde.
  - *Degradar graciosamente:* holdover sobre efeméride propagada e oscilador disciplinado; atitude a partir de star tracker, independente do GNSS; tempo a partir de um relógio local com modelo de deriva caracterizado, dimensionado para que a deriva ao longo de `η` permaneça dentro de `α`.
  - *Recuperar:* estado confiável com checkpoint; quarentena e rollback do filtro; reinicialização a partir de uma âncora não-GNSS (upload autenticado do solo, determinação de órbita baseada em star tracker, ou telemetria de distância entre satélites).
  - *Responder:* autonomia condicionada ao estado de confiança, alerta por telemetria e rotulagem de produtos com o nível de confiança PNT.

**Estágio 7 — Requisito Cibernético.** Expresse o resultado em um gabarito fixo, para que seja testável e não aspiracional:

> **[Subsistema] DEVE [capacidade] de modo que [limite mensurável] sob [condição de ameaça], verificado por [método de V&V].**

Um requisito que não pode ser escrito nesta forma não foi derivado; foi desejado. O gabarito força um limite e um método de verificação, que são as duas coisas que separam um requisito de uma recomendação.

### 4.4 Exemplo completo de transição

Aplicando a cadeia a um único par, integralmente:

| Estágio | Conteúdo |
|---|---|
| **1. Objetivo** | Manter conhecimento de órbita suficiente para desvio autônomo de conjunção. `κ = catastrófico` (colisão cria detritos e é irreversível). |
| **2. Dependência** | `D = {P, V}`; `α` = erro de posição pequeno em relação ao volume de triagem de conjunção; `η` = o intervalo ao longo do qual a efeméride propagada permanece dentro de `α`, da ordem de horas a um dia para uma órbita LEO bem modelada; `ι` muito baixo; `A = fonte`. |
| **3. Ameaça** | T4 (spoofing por sobreposição) — alcança a dependência diretamente; o adversário conhece a órbita e consegue prever a passagem. |
| **4. Efeito** | E3 Decepção. Magnitude: arbitrária, escolhida pelo atacante. Persistência: alta — o estado falso entra no filtro de navegação e na efeméride propagada, sobrevivendo ao ataque por dias. `viola() = verdadeiro` nas três cláusulas. |
| **5. Detecção** | D4 viabilidade kepleriana (a trajetória falsa implica aceleração inconsistente com a capacidade propulsiva do veículo) + D5 verificação cruzada contra órbita autenticada fornecida do solo e atitude/órbita derivada de star tracker. Duas camadas, bases físicas distintas, satisfazendo a regra do estágio 5. A latência precisa ser demonstrada menor que `η` menos o tempo de resposta. |
| **6. Mitigação** | Transição ao estado de confiança DEGRADED/UNTRUSTED; quarentena das atualizações do filtro; manutenção sobre efeméride propagada; **inibição de manobras propulsivas** até que a confiança seja restaurada a partir de uma âncora não-GNSS; alerta ao operador. |
| **7. Requisito** | *O subsistema de navegação DEVE detectar soluções de posição inconsistentes com dinâmica orbital viável e transitar ao estado PNT UNTRUSTED dentro de uma latência demonstravelmente menor que o orçamento de holdover da efeméride propagada, e DEVE inibir todos os comandos propulsivos enquanto estiver nesse estado, verificado por ensaio em hardware-in-the-loop contra um perfil de spoofing de tomada suave a taxas de walk-off definidas.* |

**Tabela 4.** Travessia completa da cadeia para um par (objetivo, ameaça).

Note o que a cadeia produziu e que um tratamento em nível de princípio não produziria: uma condição de inibição sobre a propulsão. Esse requisito não decorre de "GNSS pode sofrer spoofing". Decorre de rastrear o efeito específico de uma ameaça específica sobre um objetivo específico até a autoridade específica que precisa ser retirada.

### 4.5 A Máquina de Estados de Confiança PNT e o gating de autoridade

A construção central de mitigação do framework é que a confiança em PNT é um **estado de sistema explícito e de primeira classe** que governa a autoridade da espaçonave. A maioria das espaçonaves trata a validade do PNT como um flag por medição, consumido localmente pelo filtro de navegação. Argumentamos que ele deveria ser, em vez disso, um estado em nível de veículo que outros subsistemas leem e obedecem, pela mesma razão que o modo seguro é um estado em nível de veículo: a resposta correta a uma navegação não confiável é uma mudança no que o veículo *está autorizado a fazer*, e não meramente uma mudança no que o filtro acredita.

| Estado | Critérios de entrada | Autonomia permitida | Produtos |
|---|---|---|---|
| **NOMINAL** | Todas as camadas de detecção nominais; autenticação válida onde disponível; resíduos e dinâmica consistentes | Autonomia plena, incluindo manobras propulsivas | Sem rótulo (nominal) |
| **SUSPECT** | Anomalia em camada única, ou autenticação indisponível, ou geometria degradada | Autonomia não propulsiva; manobras exigem confirmação do solo | Rotulado `PNT=SUSPECT` |
| **DEGRADED** | Jamming confirmado (E1/E2); PNT indisponível, porém não enganoso | Somente operações em holdover; sem manobras autônomas | Rotulado `PNT=HOLDOVER`, com tempo decorrido de holdover |
| **UNTRUSTED** | Inconsistência multicamada, inviabilidade dinâmica, ou decepção confirmada (E3/E4) | **Nenhuma ação irreversível.** Entrada GNSS em quarentena; filtro congelado ou revertido ao checkpoint | Rotulado `PNT=UNTRUSTED`; consumidores a jusante devem tratar como inválido |

**Tabela 5.** Máquina de Estados de Confiança PNT. Transições ascendentes de confiança exigem um evento positivo e independente de reancoragem; nunca devem ocorrer apenas porque a anomalia deixou de ser observada.

Três regras de projeto decorrem daí, e as enunciamos como o núcleo normativo do framework:

**Regra 1 — A autoridade segue a confiança.** Toda capacidade autônoma é anotada com o estado mínimo de confiança PNT sob o qual pode executar. A anotação é imposta pelo caminho de comando do software de voo, não por convenção.

**Regra 2 — Nenhuma atuação irreversível sob PNT não confiável.** Propulsão, acionamento de mecanismos, deorbit e qualquer comando cujo efeito não possa ser desfeito em órbita exigem confiança NOMINAL ou autorização explícita do solo. Este é o requisito de maior valor que o framework produz, porque converte uma falha de integridade da informação em uma perda limitada de função, e não em perda permanente do veículo.

**Regra 3 — Restauração de confiança exige uma âncora independente.** A saída de UNTRUSTED exige reancoragem contra uma fonte que não seja o canal atacado — um upload autenticado do solo, determinação de órbita baseada em star tracker, ou telemetria de distância entre satélites. A ausência da anomalia não é evidência de sua inexistência, e um atacante que observe o estado de confiança na telemetria pode, de outro modo, simplesmente pausar para reiniciá-lo.

---

## 5. Aplicação: Oito Objetivos de Missão

A Tabela 6 aplica a cadeia a oito objetivos típicos de uma missão LEO. Ela é intencionalmente compacta; cada linha é o resumo de uma travessia do tipo mostrado integralmente na Tabela 4.

| # | Objetivo de missão | Dependência `D` | Ameaça dominante | Efeito | Detecção | Mitigação | Requisito cibernético derivado |
|---|---|---|---|---|---|---|---|
| 1 | Determinação de órbita | P, V | T4 spoofing por sobreposição | E3 decepção, alta persistência via filtro e efeméride | D4 viabilidade kepleriana + D5 verificação cruzada solo/star tracker | Estado de confiança → UNTRUSTED; quarentena do filtro; holdover sobre efeméride propagada | Detectar soluções dinamicamente inviáveis dentro do orçamento de holdover; colocar o filtro em quarentena; reancorar a partir de fonte independente |
| 2 | Referência de tempo de bordo | T | T9 arrasto temporal, T3 meaconing | E4 temporal, cascateia para validade criptográfica, janelas de replay, ordenação de logs | D1 monitoramento de deriva do relógio contra o modelo do oscilador; D3 autenticação; D5 tempo autenticado do solo | Holdover em oscilador local com deriva caracterizada; gate de taxa de variação limitada nas correções de relógio | Rejeitar correções de tempo que excedam um limite de taxa fisicamente justificado; manter o tempo dentro de `α_T` ao longo de `η` sem GNSS |
| 3 | Desvio autônomo de colisão | P, V | T4, T8 | E3, **irreversível** se uma manobra executar sobre estado falso | D4 + D5, duas bases independentes | **Inibir propulsão** abaixo da confiança NOMINAL; exigir confirmação do solo | Nenhum comando propulsivo executa sob confiança PNT sub-NOMINAL (Regra 2) |
| 4 | Geolocalização de dados de carga útil | P, T | T4, T5 | E3 — corrompe silenciosamente o acervo científico/de imagens | D2 consistência de resíduos + D4 | Rotular produtos com o estado de confiança PNT; reter medições brutas para reprocessamento | Todos os produtos de carga útil carregam um rótulo de confiança PNT; produtos de confiança degradada são recuperáveis por reprocessamento em solo |
| 5 | Apoio à determinação de atitude | P, V, T | T1/T2 jamming | E1/E2 — degrada o apontamento onde o GNSS auxilia a atitude | D1 monitoramento de sinal | Star tracker como fonte primária de atitude, arquiteturalmente independente do GNSS | A determinação de atitude DEVE atender à especificação de apontamento com GNSS indisponível durante todo o orçamento de holdover |
| 6 | Agendamento de contatos com solo | P, T | T9, T8 | E4 — passagens perdidas, oportunidade de comando degradada, isolamento cumulativo | D5 verificação cruzada do plano contra a órbita propagada | Margem de agendamento dimensionada para a deriva em holdover; autoridade de agendamento no solo | O agendamento de contatos DEVE tolerar a incerteza de tempo e de órbita de bordo acumulada ao longo de `η` |
| 7 | Coordenação de constelação / formação | P, V, T | T4 visando um ou vários membros | E3 — o erro de estado relativo se propaga pela formação | D5 telemetria de distância entre satélites; consistência entre veículos (um spoof que afeta um membro é visível aos vizinhos) | Recuar para navegação relativa via ISL; isolar o membro afetado | A navegação relativa DEVE ser sustentável sem GNSS absoluto durante o orçamento de holdover de coordenação |
| 8 | Execução de deorbit em fim de vida | P, V, T | T4, T8 | E3, **irreversível e catastrófico** | D4 + D5 + autorização do solo | Execução somente autorizada pelo solo; confirmação de estado por múltiplas fontes | O deorbit DEVE exigir autorização autenticada do solo e confirmação de estado por múltiplas fontes; NÃO DEVE ser executável autonomamente apenas com GNSS |

**Tabela 6.** Aplicação da cadeia GNSS-CRF a oito objetivos de missão LEO.

Três observações emergem da aplicação e não eram evidentes antes dela.

**O tempo é a dependência menos analisada.** Os objetivos 2, 4, 6 e 8 consomem tempo, e na maior parte da documentação de espaçonaves nenhum deles é registrado como dependência de GNSS. A corrupção de tempo é também a classe de efeito com o maior raio de dano interdomínio, porque invalida silenciosamente janelas de validade criptográfica, proteção contra replay e a ordenação dos próprios logs que um operador usaria para investigar o incidente.

**Irreversibilidade, e não probabilidade, comanda o conjunto de requisitos.** Os objetivos 3 e 8 produzem os requisitos mais fortes da tabela, e o fazem independentemente de quão provável se julgue um ataque de spoofing, porque o custo de errar é ilimitado. Esta é uma propriedade geral de sistemas espaciais, e é por isso que a pontuação de risco convencional, que multiplica verossimilhança por impacto, sistematicamente os subprotege.

**O voo em formação inverte a economia do ataque.** O objetivo 7 mostra que uma constelação não é simplesmente uma superfície de ataque maior. Os vizinhos são observadores independentes: um spoof que captura um membro produz uma inconsistência de estado relativo visível aos demais, de modo que arquiteturas multissatélite possuem uma capacidade de detecção que uma espaçonave isolada não tem. A telemetria de distância entre satélites é, portanto, um controle de segurança tanto quanto um auxílio à navegação.

---

## 6. Estudo de Caso Hipotético: a Constelação TERRA-SENTINEL

A Seção 5 demonstrou a amplitude do framework ao longo de objetivos. Esta seção demonstra sua profundidade sobre uma única missão hipotética, levada até os números. A missão é fictícia e os valores dos parâmetros são ilustrativos — escolhidos para serem representativos da classe smallsat, e não extraídos de qualquer programa real — mas a aritmética é real, e produz um resultado que não antecipávamos ao construir o framework.

### 6.1 Definição da missão

**TERRA-SENTINEL** é uma constelação hipotética de doze satélites de consciência situacional do domínio marítimo.

| Atributo | Valor |
|---|---|
| Órbita | Heliossíncrona a 550 km, período de ~95,6 min, três planos |
| Espaçonave | Smallsat classe 180 kg, ×12 |
| Carga útil | Imageador óptico (GSD 1,5 m) + receptor AIS |
| GNSS | Receptor COTS de dupla frequência, GPS L1/L2 + Galileo E1/E5a, compatível com OSNMA |
| Atitude | Dois star trackers, sensores solares grosseiros, magnetômetro, rodas de reação |
| Propulsão | Monopropelente, empuxo de 1 N — manutenção de órbita e desvio de colisão |
| Enlace cruzado | Enlace intersatélite em banda S dentro do plano |
| Relógio | OCXO como baseline; relógio atômico em escala de chip sob análise de trade-off |
| Autonomia | Desvio autônomo de conjunção habilitado |
| Contexto operacional | Passagens rotineiras sobre regiões com interferência GNSS documentada |

**Tabela 7.** Missão de referência TERRA-SENTINEL (hipotética).

A missão é deliberadamente escolhida para situar-se no ponto de tensão máxima: é restrita o bastante em custo para que os controles de Nível 2 sejam inviáveis, autônoma o bastante para que a Regra 2 tenha consequências reais, e operacionalmente exposta o bastante para que a ameaça não seja hipotética ainda que a missão seja.

### 6.2 Contratos de Serviço PNT

A aplicação dos estágios 1 e 2 da cadeia produz os contratos a seguir. Os valores são ilustrativos; um programa real os deriva de suas próprias análises de perigos e de desempenho.

| Objetivo | `κ` | `D` | `α` | `ι` | `η` | `A` |
|---|---|---|---|---|---|---|
| **O1** Determinação de órbita para triagem de conjunção | Catastrófico | P, V | 100 m (3σ) | 10⁻⁵ por triagem | 6 h | fonte |
| **O2** Referência de tempo de bordo | Crítico | T | 10 µs | 10⁻⁶ | 24 h | fonte |
| **O3** Desvio autônomo de colisão | Catastrófico | P, V | como O1 | como O1 | intervalo entre aviso e queima | fonte |
| **O4** Geolocalização de carga útil | Maior | P, T | 15 m | 10⁻³ | uma passagem de imageamento (~10 min) | dados |
| **O5** Agendamento de contatos com solo | Menor | P, T | 1 s | 10⁻² | 72 h | nenhuma |

**Tabela 8.** Contratos de Serviço PNT da TERRA-SENTINEL (valores ilustrativos).

Duas observações surgem antes de qualquer ameaça ser considerada, o que é em si um argumento a favor do framework: o estágio 2 se paga mesmo que o estágio 3 nunca seja alcançado.

Primeiro, **o contrato de O2 já está em tensão com o hardware de baseline.** Um OCXO com desvio fracionário de frequência efetivo pós-calibração de 10⁻¹⁰ deriva 8,64 µs ao longo do orçamento de holdover de 24 horas, consumindo 86% da tolerância de 10 µs sem qualquer folga para envelhecimento ou excursão térmica. O contrato, escrito honestamente, converte a escolha do relógio de uma decisão de custo em uma decisão de resiliência: um CSAC a 10⁻¹¹ resulta em 0,86 µs no mesmo período, uma margem de dez vezes. Este é exatamente o tipo de consequência de projeto que "GNSS pode sofrer spoofing" jamais produz.

Segundo, **O5 não exige autenticidade alguma** (`A = nenhuma`, `α` = 1 s, `η` = 72 h). Seu contrato é tão frouxo que nenhum ataque PNT dentro do modelo de ameaças consegue violá-lo. O framework, portanto, elimina O5 de análise posterior e registra o porquê. Um método que gera requisitos para tudo não é um método; a capacidade de justificar *não* impor um requisito é o que torna a saída defensável perante um gerente de programa que administra orçamento de massa e de custo.

### 6.3 Cenário A — spoofing de tomada suave durante uma passagem

**Configuração.** Um adversário operando um spoofer em solo dentro da região de cobertura da constelação executa um ataque T4 por sobreposição contra uma única espaçonave. O adversário conhece a órbita pelo catálogo público e consegue prever a passagem. O ataque é habilmente executado: os sinais são casados em potência na aquisição e elevados gradualmente, de modo que o C/N0 sobe menos que o limiar de alarme de D1, e a constelação falsa é plenamente autoconsistente, de modo que o teste de resíduos de D2 nada percebe. As camadas D1 e D2 estão, por construção, derrotadas.

**O teste D4.** A camada D4 faz uma pergunta diferente: o movimento reportado é fisicamente possível para *este veículo*? Afastar a posição reportada da verdade exige que a solução falsa exiba uma aceleração aparente que a espaçonave não é capaz de produzir. A aceleração propulsiva máxima da TERRA-SENTINEL é

```
a_max = F / m = 1 N / 180 kg = 5,56 × 10⁻³ m/s²
```

Se o subsistema de navegação rejeita qualquer solução que implique aceleração sustentada não modelada acima de `a_max` (mais uma margem para erro do modelo dinâmico e ruído de medição), o adversário é forçado a manter o walk-off dentro desse limite. O deslocamento máximo de posição alcançável passa então a ser limitado pela janela de ataque:

```
deslocamento_max = ½ · a_max · T_vis²
```

onde `T_vis` é a duração pela qual o spoofer em solo consegue iluminar o alvo. Para uma órbita de 550 km, uma passagem de horizonte a horizonte sobre um único sítio em solo é da ordem de dez minutos, logo `T_vis ≈ 600 s`:

```
deslocamento_max = ½ × 5,56 × 10⁻³ × 600²  ≈  1,0 km
```

**O resultado.** Um único spoofer baseado em solo não consegue induzir mais que aproximadamente um quilômetro de erro de posição contra esta espaçonave sem tornar-se dinamicamente inviável e, portanto, detectável — *independentemente de quão sofisticado seja o spoofer na camada de sinal*. O limite vem do empuxo do próprio veículo e da geometria orbital, não da qualidade do rádio do atacante.

**O corolário, que é o achado mais interessante.** O limite escala com a capacidade propulsiva e, portanto, a superfície de ataque também:

| Propulsão | `a_max` (m/s²) | Deslocamento limitado em uma passagem de 600 s |
|---|---|---|
| Monopropelente, 1 N / 180 kg | 5,56 × 10⁻³ | ≈ 1000 m |
| Elétrica, 1 mN / 180 kg | 5,56 × 10⁻⁶ | ≈ 1 m |
| Sem manobra (apenas arrasto/SRP residual, ~10⁻⁶) | ~10⁻⁶ | ≈ 0,18 m |

**Tabela 9.** Limite de deslocamento por spoofing sob gating de viabilidade kepleriana, por classe de propulsão.

**Espaçonaves de baixo empuxo são estruturalmente muito mais difíceis de enganar, e espaçonaves sem manobra são quase imunes** — sob este gate, e supondo que o gate seja efetivamente imposto. O dimensionamento da propulsão, uma decisão tomada por razões inteiramente alheias no início do projeto de missão, acaba determinando a exposição da espaçonave à decepção PNT por três ordens de grandeza. Até onde sabemos, este acoplamento entre arquitetura de propulsão e superfície de ataque PNT não foi enunciado em nenhuma das duas literaturas de origem, e é produto direto de percorrer a cadeia, em vez de raciocinar sobre spoofing em geral.

**Qualificações honestas.** Três, e elas importam:

1. O limiar de detecção não pode ser exatamente `a_max`. Precisa ser `a_max + margem`, onde a margem cobre erro do modelo dinâmico, variabilidade não modelada de arrasto e de SRP, e ruído de medição. Uma margem frouxa enfraquece o limite proporcionalmente; os números acima são, portanto, um limite de *melhor caso*, e caracterizar a margem alcançável é precisamente a predição **P1** da Seção 8.3.
2. O gate não pode disparar em manobras legítimas. O subsistema de navegação precisa saber quando o sistema de propulsão é comandado, o que torna a consciência do estado de manobra um requisito de *segurança*, e não apenas de navegação — acoplamento registrado como REQ-CS-03 adiante.
3. O limite vale para um *único* sítio em solo. Adversários multissítio ou aerotransportados estendem `T_vis` e relaxam o limite quadraticamente, o que é o contra-ataque mais barato do adversário.

**A adaptação do adversário, e por que a Regra 2 sobrevive a ela.** Uma resposta natural do atacante é *catracar* (ratchet): permanecer dentro do gate de viabilidade em cada passagem e acumular deslocamento ao longo de muitas passagens. Isso falha contra a TERRA-SENTINEL por uma razão estrutural — a espaçonave retorna aos sinais autênticos por cerca de 85 minutos de cada órbita de 95,6 minutos, e medições autênticas puxam o filtro de volta. Catracar exige impedir a reancoragem entre passagens, o que um único sítio em solo não consegue fazer.

Logo, o movimento racional do atacante não é corromper o *estado*, mas corromper uma *decisão*: sincronizar o spoof com uma queima planejada de desvio de conjunção, e usar o erro limitado de um quilômetro para transformar uma manobra correta em uma manobra errada. Um quilômetro é pouco diante das ambições de um spoofer, mas não é pouco diante de um volume de triagem de conjunção. Este é o cenário no qual toda a defesa se reduz a um único controle — **MCB-02, nenhuma atuação irreversível sob PNT não confiável** — e é por isso que colocamos o gating de autoridade acima da detecção na baseline. A detecção limita o erro; apenas o portão de autoridade limita a *consequência*.

### 6.4 Cenário B — jamming regional, e um requisito eliminado

**Configuração.** Um jammer T1 de banda larga nega o GNSS durante toda a duração de cada passagem sobre uma região contestada: uma passagem por órbita, cerca de 600 s de negação a cada 95,6 minutos.

**Avaliação do contrato.** Para O1, `η` = 6 h. Uma interrupção de 600 s está uma ordem de grandeza dentro do orçamento de holdover, e a efeméride propagada a cobre confortavelmente. Para O2, `η` = 24 h; o relógio corre livre por 600 s, acumulando bem menos que um microssegundo mesmo no OCXO. Para O4, `η` é uma passagem de imageamento, e a negação durante a passagem significa que as imagens daquela passagem ficam degradadas — mas o efeito é E2, limitado, não persistente e visível.

`viola()` retorna **falso** para O1 e O2, e **verdadeiro apenas para O4**, cuja consequência é perda de acurácia de geolocalização nas imagens afetadas, e não perda da missão.

**O que isso demonstra.** O jamming, a ameaça que recebe mais atenção operacional porque é a que as pessoas percebem, produz o conjunto de requisitos *mais fraco* para esta missão: rotular os produtos afetados (MCB-10) e aceitar a degradação. O framework diz isso explicitamente, com aritmética, em vez de impor um controle porque jamming soa grave. Enquanto isso, a ameaça que produz o requisito catastrófico — o spoof silencioso do Cenário A — não geraria reclamação alguma do operador enquanto estivesse acontecendo. Essa inversão entre saliência operacional e risco real é, a nosso ver, uma das coisas mais valiosas que o framework faz emergir.

### 6.5 Cenário C — arrasto temporal contra o relógio

**Configuração.** Um ataque T9 manipula a solução de tempo lentamente o bastante para permanecer abaixo de qualquer limiar de detecção de salto, com o objetivo de deslocar o tempo da espaçonave o suficiente para invalidar janelas de validade criptográfica e corromper a ordenação de logs.

**O gate de taxa.** O MCB-07 exige que as correções de relógio aceitas sejam limitadas por uma taxa fisicamente justificada. Correções legítimas não podem exceder a deriva do próprio oscilador, de modo que um gate ajustado em três vezes a deriva de 10⁻¹⁰ do OCXO permite no máximo 0,3 µs por 1000 s. Dentro de uma passagem de 600 s, o adversário consegue, portanto, injetar no máximo **0,18 µs**, e alcançar a tolerância de 10 µs de O2 exigiria cerca de **56 passagens** de manipulação cumulativa ininterrupta — com o mesmo problema de reancoragem do Cenário A derrotando a acumulação.

**O resultado estrutural.** Os cenários A e C produzem a mesma forma de resposta pelo mesmo mecanismo: *um limite de taxa fisicamente justificado, multiplicado por uma janela de ataque geometricamente limitada, limita a autoridade total do adversário sobre o estado.* Esta é a principal contribuição teórica do estudo de caso de volta ao framework, e generaliza para além desses dois cenários — onde quer que um defensor consiga limitar a taxa legítima de variação de uma grandeza e o acesso do adversário seja em janelas, a corrupção alcançável fica limitada sem criptografia alguma.

### 6.6 Conjunto de requisitos derivado

A execução do estágio 7 ao longo dos cenários produz os seguintes requisitos para a TERRA-SENTINEL.

| ID | Requisito | Origem | MCB | Verificação |
|---|---|---|---|---|
| **REQ-CS-01** | O subsistema de navegação DEVE rejeitar soluções derivadas de GNSS que impliquem aceleração sustentada não modelada superior a `a_max` mais a margem de modelo caracterizada, e DEVE transitar a UNTRUSTED em até 60 s do início. | A / O1 | MCB-03, MCB-01 | HIL contra perfis de walk-off |
| **REQ-CS-02** | A espaçonave NÃO DEVE executar qualquer comando propulsivo enquanto a confiança PNT estiver abaixo de NOMINAL, na ausência de autorização autenticada do solo. | A / O3 | MCB-02 | Ensaio do caminho de comando; métrica AGC = 1,0 |
| **REQ-CS-03** | O subsistema de navegação DEVE receber estado autoritativo de manobra do subsistema de propulsão e DEVE suprimir alarmes do gate de viabilidade apenas para manobras comandadas. | A / O3 | MCB-03 | Ensaio de integração |
| **REQ-CS-04** | O relógio de bordo DEVE manter o tempo dentro de 10 µs ao longo de 24 h sem qualquer atualização válida de tempo por GNSS. | B, C / O2 | MCB-06 | Análise + caracterização em termovácuo |
| **REQ-CS-05** | O receptor DEVE rejeitar correções de relógio que excedam três vezes a taxa de deriva caracterizada do oscilador. | C / O2 | MCB-07 | Ensaio de injeção |
| **REQ-CS-06** | Todos os produtos de carga útil DEVEM carregar o estado de confiança PNT e o tempo decorrido de holdover no instante da aquisição. | B / O4 | MCB-10 | Inspeção de produto |
| **REQ-CS-07** | O subsistema de navegação DEVE manter checkpoint do estado confiável e DEVE suportar rollback e reinicialização a partir de órbita autenticada fornecida pelo solo ou de solução derivada de star tracker. | A / O1 | MCB-09, MCB-12 | Ensaio HIL de recuperação |
| **REQ-CS-08** | Eventos PNT relevantes para segurança DEVEM ser registrados com ordenação monotônica independente da fonte de tempo GNSS. | A, C | MCB-11 | Inspeção de logs sob ataque de tempo |
| **REQ-CS-09** | A saída de UNTRUSTED DEVE exigir reancoragem positiva contra uma fonte não-GNSS; a cessação da anomalia NÃO DEVE constituir reancoragem. | A | MCB-01, MCB-12 | Ensaio da máquina de estados |

**Tabela 10.** Requisitos derivados para a TERRA-SENTINEL.

Nove requisitos, todos de Nível 0, nenhum exigindo hardware que a missão já não carregue — com a única exceção do REQ-CS-04, que pode motivar a escolha do CSAC. Essa é a forma prática da saída do framework.

### 6.7 O que o estudo de caso estabelece

O estudo de caso é hipotético e não prova nada empiricamente. O que ele estabelece é que o framework é *gerativo*: percorrido de ponta a ponta sobre uma missão concreta, produziu quatro resultados que não eram entradas dele.

1. **Um limite quantitativo de spoofing.** O gating de viabilidade kepleriana limita um spoofer de solo de sítio único a ≈1 km de erro induzido contra esta espaçonave, a partir da física do veículo e não do processamento de sinais.
2. **A arquitetura de propulsão como superfície de ataque PNT.** O limite escala com o empuxo ao longo de três ordens de grandeza, transformando um trade-off de propulsão em um trade-off de segurança.
3. **O princípio limite-de-taxa × limite-de-janela.** Os cenários A e C convergem para a mesma defesa estrutural, que parece generalizar para além do PNT.
4. **A inversão de saliência.** A ameaça mais barulhenta (jamming) gerou os requisitos mais fracos; a silenciosa (spoofing) gerou os catastróficos.

Ele também produziu um resultado negativo que merece ser declarado: o framework eliminou O5 por completo e reduziu o jamming a um requisito de rotulagem. Um framework que apenas acrescenta controles não é confiável como tendo analisado coisa alguma.

---

## 7. A Baseline Mínima de Controles

Esta seção responde à pergunta central de pesquisa. A baseline é organizada em níveis, de modo a escalar de um cubesat universitário a infraestrutura crítica, e todo controle é enunciado como uma capacidade, e não como um produto.

**Nível 0 — Obrigatório para qualquer satélite LEO dependente de GNSS.** São os controles sem os quais a espaçonave não tem defesa que sobreviva a um atacante competente, e todos são realizáveis em software sobre hardware que a espaçonave já carrega.

| ID | Controle | Função | Tática SPARTA | NIST SP 800-53 Rev. 5 |
|---|---|---|---|---|
| **MCB-01** | Máquina de Estados de Confiança PNT explícita, com os quatro estados da Tabela 5 | Detectar / responder | Impact, Defense Evasion | SI-4, SI-13 |
| **MCB-02** | Gating de autoridade: nenhuma atuação irreversível sob confiança sub-NOMINAL (Regra 2) | Responder | Impact | AC-3, CM-5, SI-13 |
| **MCB-03** | Verificação de plausibilidade por dinâmica orbital (viabilidade kepleriana, D4) | Detectar | Impact | SI-4, SI-10 |
| **MCB-04** | Monitoramento de anomalias em nível de sinal (AGC, C/N0, teto de potência) | Detectar | Initial Access, Impact | SI-4 |
| **MCB-05** | Gating de inovação no filtro de navegação, com consciência da inversão de covariância | Detectar / isolar | Impact | SI-10, SI-13 |
| **MCB-06** | Holdover de tempo com modelo de deriva caracterizado e dimensionado para `η` | Degradar | Impact | SC-45, AU-8 |
| **MCB-07** | Gate de taxa de variação limitada nas correções de relógio aceitas | Detectar / prevenir | Impact | SI-10, SC-45 |
| **MCB-08** | Validação de entrada do receptor e endurecimento de firmware contra dados de navegação malformados (T7) | Prevenir | Execution, Initial Access | SI-7, SI-10, SA-8 |
| **MCB-09** | Checkpoint de estado confiável com quarentena e rollback do filtro | Recuperar | Impact, Persistence | CP-10, CP-12 |
| **MCB-10** | Rotulagem de confiança PNT em todos os produtos e na telemetria | Responder / perícia | Exfiltration, Impact | AU-3, SC-16 |
| **MCB-11** | Registro de eventos PNT relevantes para segurança, com proteção de integridade e ordenação monotônica independente do tempo GNSS | Detectar / perícia | Defense Evasion | AU-2, AU-8, AU-9 |
| **MCB-12** | Caminho independente de reancoragem não-GNSS para restauração de confiança (Regra 3) | Recuperar | Impact | CP-10, IR-4 |

**Nível 1 — Controles adicionais para missões com manobra, de constelação e de serviço comercial.**

| ID | Controle | Função | NIST SP 800-53 Rev. 5 |
|---|---|---|---|
| **MCB-13** | Autenticação da mensagem de navegação habilitada onde o sinal suporta (OSNMA / Chimera), com latência de autenticação verificada contra `η` | Prevenir | SC-8, SC-16, SI-7 |
| **MCB-14** | Fonte secundária independente de navegação (determinação de órbita por star tracker, telemetria de distância entre satélites, ou LEO-PNT) | Degradar / recuperar | CP-10, SC-5 |

**Nível 2 — Controles adicionais para missões de infraestrutura crítica e de alta garantia.**

| ID | Controle | Função | NIST SP 800-53 Rev. 5 |
|---|---|---|---|
| **MCB-15** | Discriminação espacial: antena de padrão de recepção controlado ou detecção de ângulo de chegada com múltiplos elementos | Prevenir / detectar | SC-5, SI-4 |
| **MCB-16** | Verificação de consistência PNT entre veículos ao longo da constelação | Detectar | SI-4, SC-5 |

**Tabela 11.** A Baseline Mínima de Controles. Identificadores de técnica do SPARTA são deliberadamente omitidos e devem ser preenchidos contra a versão fixada da matriz no momento do uso, conforme a Seção 2.4.

### 7.1 Por que isto é um *mínimo*

Três propriedades justificam chamar o Nível 0 de mínimo, e não de meramente pequeno.

**É realizável dentro das restrições de smallsats.** MCB-01 a MCB-12 são controles de software mais uma decisão sobre qualidade de relógio. Nenhum exige antena de padrão de recepção controlado, cadeia de RF adicional ou módulo criptográfico. O mais exigente computacionalmente, o MCB-03, precisa de um modelo dinâmico que a espaçonave já carrega para propagação.

**Cada controle fecha um modo de falha distinto.** Remover qualquer controle de Nível 0 deixa um caminho não tratado da Tabela 2 à Tabela 3: sem o MCB-03, um spoof autoconsistente é indetectável; sem o MCB-02, a detecção não impede uma ação irreversível; sem o MCB-09, a recuperação após envenenamento do estimador é impossível; sem o MCB-11, o incidente não pode ser investigado, porque o atacante corrompeu a base de tempo dos logs.

**É completo em cobertura contra a taxonomia de ameaças.** Toda ameaça T1–T9 é endereçada por ao menos um controle de Nível 0, e toda classe de efeito E1–E5 possui ao menos um controle de detecção e um de recuperação. Completude de cobertura é uma afirmação mais fraca que eficácia, e não a exageramos: significa que nenhuma ameaça está sem tratamento, não que toda ameaça esteja derrotada.

### 7.2 Mapeamento para frameworks externos

A baseline é deliberadamente expressa para poder ser consumida por estruturas de conformidade existentes, em vez de competir com elas. O NIST IR 8323 (o perfil PNT fundacional que aplica o Cybersecurity Framework ao uso responsável de serviços PNT) fornece a âncora externa mais próxima, e o mapeamento é direto: sua função *Identify* corresponde aos estágios 1–2 do GNSS-CRF, *Protect* às mitigações de prevenção, *Detect* ao estágio 5, e *Respond*/*Recover* à máquina de estados de confiança e aos controles de reancoragem. O NIST IR 8270 e a SPD-5 fornecem o enquadramento setorial espacial, os padrões de segurança do CCSDS cobrem as pré-condições de camada de enlace assumidas na Seção 1.4, e o IEEE P3349 é o foro de padronização no qual requisitos deste tipo têm maior probabilidade de encontrar um lar normativo.

---

## 8. Metodologia de Avaliação

Um framework que propõe requisitos precisa também propor como saber se eles foram atendidos. Definimos cinco métricas e um ambiente de validação.

### 8.1 Métricas

| Métrica | Definição | Propriedade-alvo |
|---|---|---|
| **TTD** — tempo até detecção | Intervalo do início do ataque até a transição de estado de confiança | `TTD + t_resposta < η` (condição de adequação i) |
| **SIE** — erro de estado induzido por spoofing na detecção | Magnitude do erro de estado de navegação acumulado no instante da detecção | `SIE ≤ α` |
| **HEG** — crescimento do erro em holdover | Taxa de acumulação de erro de posição/tempo sem GNSS válido | Determina o `η` alcançável; orienta o projeto de relógio e de efeméride |
| **AGC** — correção do portão de autoridade | Fração de comandos irreversíveis corretamente inibidos sob confiança sub-NOMINAL | Precisa ser 1,0; qualquer valor menor falsifica a Regra 2 |
| **MAA** — disponibilidade da missão sob ataque | Fração de objetivos de missão que cumprem seus contratos durante e após um episódio de ataque | O número-síntese de resiliência |

**Tabela 12.** Métricas de avaliação. TTD e SIE juntas caracterizam a detecção; HEG caracteriza a degradação graciosa; AGC caracteriza a propriedade de segurança; MAA caracteriza o resultado de missão.

Uma nota sobre alarmes falsos: `P_fa` precisa ser avaliada conjuntamente com TTD, porque um detector ajustado para velocidade transitará a UNTRUSTED diante de mudanças benignas de geometria, e uma espaçonave que inibe suas próprias manobras de desvio de colisão por alarmes falsos trocou um modo de falha catastrófico por outro. O framework não resolve esse trade-off; exige que ele seja declarado, medido e defendido por objetivo.

### 8.2 Ambiente de validação proposto

Propomos uma bancada em hardware-in-the-loop com quatro elementos:

1. **Simulação de dinâmica orbital** (por exemplo, GMAT ou Basilisk) gerando trajetórias-verdade com perturbações realistas, fornecendo a referência para SIE e HEG.
2. **Simulação de sinal GNSS com dinâmica LEO**, acionando um simulador comercial de constelação ou um gerador baseado em SDR, e incluindo criticamente a geometria correta de LEO: lóbulos principais cruzando o limbo, recepção por lóbulos laterais, visibilidade reduzida de satélites e Doppler em magnitude plena. Simulação de sinal com perfil terrestre superestimará o desempenho defensivo, porque a camada D4 depende precisamente da geometria que um perfil terrestre omite.
3. **Biblioteca de perfis de ataque** cobrindo T1–T9, parametrizada por taxa de walk-off para spoofing de tomada suave, por atraso para meaconing, por ciclo de trabalho para jamming pulsado, e por taxa sublimiar para arrasto temporal.
4. **Software representativo de voo** executando o filtro de navegação, a máquina de estados de confiança e o caminho de comando reais, de modo que a AGC meça o caminho de comando de fato, e não um modelo dele.

### 8.3 Predições falsificáveis

O framework faz afirmações que a bancada pode refutar, e as enunciamos para que ele seja falsificável em vez de meramente plausível:

- **P1.** Contra um spoof de tomada suave que derrota as camadas D1 e D2, a camada D4 (viabilidade kepleriana) detecta o ataque antes que o SIE exceda `α`, para taxas de walk-off acima de alguma taxa-limiar `r*`. Se não existir tal `r*` a taxas de alarme falso utilizáveis, a afirmação sobre D4 da Seção 4.3 falha.
- **P2.** O envenenamento do estimador persiste de forma mensurável após a cessação do ataque, com o tempo de recuperação crescendo à medida que a covariância do filtro diminui durante o ataque — o efeito de inversão de confiança da Seção 3.4. Se a recuperação pós-ataque for rápida e independente da covariância, o argumento a favor do MCB-09 enfraquece.
- **P3.** O gating de autoridade (MCB-02) reduz os desfechos catastróficos a zero em toda a biblioteca de ataques, ao custo de uma penalidade mensurável de disponibilidade por alarmes falsos. O tamanho dessa penalidade é o custo real do framework, e é desconhecido até ser medido.

---

## 9. Discussão

**A assimetria do defensor é física, e está subutilizada.** O tema dominante que atravessa as Seções 4 a 6 é que uma espaçonave é um alvo difícil para um atacante de PNT de maneiras que um carro ou um telefone não são. Ela se move a 7,5 km/s ao longo de uma trajetória restringida pela mecânica celeste; observa o GNSS a partir de uma geometria que o atacante não consegue replicar facilmente; é visível ao atacante apenas em janelas curtas e previsíveis; e carrega um modelo dinâmico preciso o bastante para testar a viabilidade de seu próprio movimento reportado. A pesquisa antispoofing terrestre concentrou-se necessariamente em criptografia e em discriminação na camada de RF, porque um usuário terrestre não tem restrição física equivalente à qual recorrer. Espaçonaves têm, e a recomendação prática do framework é explorá-la primeiro, porque é de graça.

**Restrições de segurança podem vir de subsistemas que não são subsistemas de segurança.** O achado sobre propulsão do estudo de caso (Seção 6.3) é o exemplo mais claro. O nível de empuxo é escolhido por orçamento de delta-v, cadência de manutenção de órbita e custo; ninguém o escolhe por resistência a spoofing. Ainda assim, sob gating de viabilidade, ele estabelece o teto de quão longe um adversário consegue mover a posição que o veículo acredita ter, e o faz ao longo de três ordens de grandeza. A lição geral é que, em sistemas ciberfísicos, o envelope de segurança frequentemente é definido por decisões físicas de projeto tomadas em outro lugar do programa, e que um método de requisitos que comece pela missão — em vez de pelo receptor — é o tipo de método que as encontrará.

**Resiliência é mais barata que prevenção, e mais adequada ao setor.** O Nível 0 não contém hardware novo. Isso importa porque a população de espaçonaves LEO dependentes de GNSS é dominada por plataformas comerciais e acadêmicas restritas em custo, para as quais antenas de padrão de recepção controlado e módulos criptográficos estão fora de alcance. Uma baseline que elas consigam de fato implementar vale mais do que uma mais forte que elas não implementarão.

**A saída real do framework é um conjunto de números, não um conjunto de controles.** `α`, `ι`, `η` e `A` por objetivo são o que converte a análise de narrativa em engenharia. Na nossa experiência de aplicar a cadeia, calcular `η` é o passo que mais frequentemente muda decisões de projeto, porque é o momento em que uma equipe descobre por quanto tempo a missão de fato sobrevive sem GNSS — um número que é com frequência muito menor, ou muito maior, do que se supunha, e qualquer das duas descobertas realoca orçamento.

**Relação com o modo seguro.** Uma objeção que merece resposta é que espaçonaves já possuem modo seguro, e que PNT não confiável poderia simplesmente acioná-lo. Achamos que isso é errado nas duas direções. O modo seguro é grosseiro demais: ele abandona a missão, e um adversário capaz de forçar o modo seguro com um jammer obteve negação de forma barata e repetível. E é também insuficiente: algumas implementações de modo seguro dependem elas próprias do GNSS para atitude ou tempo, de modo que o recurso de contingência compartilha um modo de falha com aquilo de que está se protegendo. A autoridade condicionada à confiança é a construção de granularidade mais fina — a espaçonave continua fazendo tudo o que não depende da entrada comprometida, e para apenas o que depende.

**Aplicabilidade além da LEO.** Os estágios 1–2 e 6–7 são agnósticos à órbita. A camada D4 do estágio 5 é onde reside a especificidade LEO, e ela generaliza com modificações: qualquer veículo cujo movimento seja fortemente restringido por um modelo dinâmico conhecido pode testar a viabilidade de seu próprio estado reportado. A construção deve transferir-se para plataformas MEO e GEO, para veículos lançadores e para missões de espaço profundo, com a restrição tornando-se mais apertada à medida que a dinâmica se torna mais previsível.

---

## 10. Limitações

Enunciamos estas limitações de forma direta, porque a credibilidade do framework depende de não exagerar suas afirmações.

1. **Sem validação experimental.** O GNSS-CRF é uma construção analítica. Nenhuma das métricas da Seção 8 foi medida, e as predições P1–P3 não foram testadas. A Seção 8.2 é uma proposta, não um relato de resultados.
2. **O estudo de caso é hipotético e sua aritmética é limitante, não preditiva.** A TERRA-SENTINEL é fictícia e os valores de seus contratos são ilustrativos. O limite de ≈1 km do spoofing na Seção 6.3 é um número de melhor caso, que supõe um limiar de detecção ajustado estritamente em `a_max`; um limiar real precisa absorver erro do modelo dinâmico, variabilidade de arrasto e de pressão de radiação solar e ruído de medição, e uma margem frouxa degrada o limite proporcionalmente. O limite também supõe um único sítio em solo — adversários multissítio ou aerotransportados o relaxam quadraticamente na janela estendida. O número é uma prova de existência de que um limite computável existe, não uma afirmação de desempenho.
3. **Sem herança de voo.** O framework não foi aplicado a uma missão voada, e o custo operacional de alarmes falsos de estado de confiança em um programa real é desconhecido.
4. **O desempenho de detecção é afirmado, não caracterizado.** A afirmação de que a camada D4 detecta spoofs autoconsistentes apoia-se em raciocínio físico. Os pontos de operação `P_d`/`P_fa` alcançáveis, e sua dependência da taxa de walk-off do ataque, do regime orbital, da sintonia do filtro e da fidelidade do modelo dinâmico, são precisamente o que não foi quantificado. Este é o item aberto mais significativo do framework.
5. **Os parâmetros de contrato são específicos da missão.** O framework diz ao analista o que calcular, não qual é a resposta. Duas equipes aplicando-o a missões semelhantes podem derivar valores diferentes de `η`, e o framework não fornece procedimento de calibração para reconciliá-los.
6. **O modelo de ameaças exclui o insider e o segmento de solo comprometido.** Um adversário com autoridade de comando está fora de escopo por construção (Seção 3.1), embora a dependência do MCB-12 em uploads autenticados do solo signifique que um segmento de solo comprometido degrada o caminho de recuperação — acoplamento que o framework reconhece, mas não resolve.
7. **A revisão de literatura é estrutural e não exaustiva, e três citações permanecem incompletas.** A lista de referências foi conferida contra fontes primárias ou secundárias autoritativas, e as entradas que não puderam ser completadas estão marcadas como **[não verificado]** na Seção 12: o intervalo de páginas de Bhatti e Humphreys (2017), o intervalo de páginas de Falco (2019), e a lista exata de autores do artigo de requisitos mínimos do SMC-IT 2024. Duas correções substantivas foram feitas durante a verificação e ficam aqui registradas por transparência: o SPARTA é um produto da **The Aerospace Corporation**, e não da MITRE, como afirmava um rascunho anterior deste artigo; e o trabalho anterior mais próximo (Seção 2.5) estava inteiramente ausente daquele rascunho. A revisão permanece estrutural — caracteriza as duas literaturas de origem no nível de suas posições e resultados, em vez de examiná-las exaustivamente — e uma revisão sistemática completa continua pendente.
8. **O trabalho anterior mais próximo foi caracterizado a partir de seu resumo, não de seu texto completo.** Ver a ressalva na Seção 2.5. Esta é a tarefa de verificação pendente mais importante, porque as reivindicações de ineditismo da Seção 1.3 dependem dela.
9. **O mapeamento SPARTA está em granularidade de tática.** O mapeamento em nível de técnica exige uma versão fixada da matriz e não foi realizado.

---

## 11. Conclusão e Trabalhos Futuros

Perguntamos qual é o conjunto mínimo de controles de cibersegurança de que um satélite LEO dependente de GNSS precisa para seguir operando através de spoofing e jamming. A resposta que derivamos é a baseline de dezesseis controles da Tabela 11, dos quais doze são obrigatórios, todos os doze são implementáveis em software, e o mais importante deles não é sequer um detector, mas um portão de autoridade: **nenhuma ação irreversível sob PNT não confiável**.

O método que produz essa resposta é a contribuição que consideramos mais durável do que a própria resposta. A cadeia de sete estágios — Objetivo de Missão → Dependência de GNSS → Ameaça → Efeito → Detecção → Mitigação → Requisito Cibernético — com o Contrato de Serviço PNT no estágio 2 e as condições de adequação no estágio 7, converte ataques PNT em requisitos verificáveis de espaçonave por meio de passos que um revisor pode auditar e um segundo analista pode reproduzir. Esse é um tipo de artefato diferente de uma lista de boas práticas, e é o artefato de que um programa de espaçonave precisa antes do congelamento do projeto, quando propriedades de segurança ainda podem ser acrescentadas.

O estudo de caso da Seção 6 forneceu o resultado mais concreto do framework, e ele não era uma entrada dele: sob gating de viabilidade orbital, um único spoofer baseado em solo fica limitado a cerca de um quilômetro de erro induzido contra uma espaçonave de 180 kg e 1 N, e esse limite cai para cerca de um metro em um veículo de baixo empuxo e para centímetros em um veículo sem manobra. A arquitetura de propulsão, escolhida por razões que nada têm a ver com segurança, define portanto o envelope de decepção PNT ao longo de três ordens de grandeza. O mesmo estudo de caso mostrou por que a detecção ainda assim é insuficiente: um adversário confinado a um quilômetro de erro deixará de atacar o estado e passará a atacar a decisão, sincronizando o spoof com uma queima planejada de desvio de colisão — o que deixa o portão de autoridade como o único controle entre um erro limitado e uma consequência ilimitada.

Três achados adicionais nos surpreenderam ao longo da construção e merecem ser levados adiante. O tempo é a dependência de GNSS mais profunda e menos documentada em uma espaçonave, e sua corrupção tem o maior raio de dano. A irreversibilidade domina a verossimilhança em sistemas espaciais, o que significa que a pontuação de risco convencional os subprotege sistematicamente. E a dinâmica orbital LEO dá ao defensor uma primitiva de detecção que não custa nada e que usuários terrestres não possuem — o resultado prático mais forte do artigo, e o que mais carece de confirmação experimental.

**Trabalhos futuros**, em ordem de prioridade:

1. **Construir a bancada da Seção 8.2 e testar P1.** Caracterizar a curva de operação `P_d`/`P_fa` da verificação de plausibilidade por dinâmica orbital contra a taxa de walk-off é o próximo experimento de maior valor, porque a afirmação mais distintiva do framework se apoia nele.
2. **Quantificar o envenenamento do estimador (P2)** ao longo de arquiteturas de filtro, e derivar políticas de checkpoint e de rollback a partir da dinâmica de recuperação medida.
3. **Medir o custo de disponibilidade do gating de autoridade (P3)**, já que a aceitabilidade operacional da Regra 2 depende inteiramente de sua carga de alarmes falsos.
4. **Completar o mapeamento SPARTA em nível de técnica** contra uma versão fixada da matriz (v2.0 ou posterior), e propor entradas de contramedida específicas de PNT onde a matriz for rala.
5. **Reconciliar com o trabalho anterior mais próximo**, obtendo e analisando integralmente o método de requisitos mínimos do SMC-IT 2024, e então restringindo as afirmações deste artigo ou, preferencialmente, expressando o GNSS-CRF como uma instanciação PNT daquele método — o que fortaleceria ambos.
6. **Desenvolver um procedimento de calibração para os parâmetros de contrato**, de modo que `α`, `ι`, `η` e `A` sejam derivados consistentemente entre missões, e não por analista.
7. **Estender o framework a fontes alternativas de PNT**, incluindo LEO-PNT a partir de downlinks de banda larga, e à detecção entre veículos em escala de constelação (MCB-16), onde a economia de ataque e defesa parece mais favorável ao defensor.

---

## 12. Referências

> **Situação da verificação.** As entradas abaixo foram conferidas contra fontes primárias ou secundárias autoritativas durante a preparação deste rascunho. Itens marcados como **[não verificado]** não puderam ser confirmados nessa passagem — em todos os casos porque o site da editora estava inacessível a partir do ambiente de redação, e não porque a obra esteja em dúvida — e precisam ser completados antes da submissão. Nada nesta lista é citado apenas de memória. Os títulos das obras são mantidos no idioma original.

**Ameaças a PNT, spoofing e detecção**

1. Humphreys, T. E., Ledvina, B. M., Psiaki, M. L., O'Hanlon, B. W., e Kintner, P. M., Jr. "Assessing the Spoofing Threat: Development of a Portable GPS Civilian Spoofer." *Proceedings of the ION GNSS Conference*, Savannah, GA, 16–19 de setembro de 2008.
2. Humphreys, T. E. "Detection Strategy for Cryptographic GNSS Anti-Spoofing." *IEEE Transactions on Aerospace and Electronic Systems*, Vol. 49, No. 2, 2013, pp. 1073–1090.
3. Psiaki, M. L., e Humphreys, T. E. "GNSS Spoofing and Detection." *Proceedings of the IEEE*, Vol. 104, No. 6, junho de 2016, pp. 1258–1270.
4. Humphreys, T. E. "Interference." In Teunissen, P. J. G., e Montenbruck, O. (eds.), *Springer Handbook of Global Navigation Satellite Systems*, Springer, Cham, 2017, pp. 469–503. DOI 10.1007/978-3-319-42928-1_16.
5. Kerns, A. J., Shepard, D. P., Bhatti, J. A., e Humphreys, T. E. "Unmanned Aircraft Capture and Control Via GPS Spoofing." *Journal of Field Robotics*, Vol. 31, No. 4, 2014, pp. 617–636. DOI 10.1002/rob.21513.
6. Bhatti, J., e Humphreys, T. E. "Hostile Control of Ships via False GPS Signals: Demonstration and Detection." *NAVIGATION*, Vol. 64, No. 1, 2017. DOI 10.1002/navi.183. *(Intervalo de páginas **[não verificado]**.)* Demonstração de campo contra um iate de 65 m no Mediterrâneo.
7. Murrian, M. J., Narula, L., Iannucci, P. A., Budzien, S., O'Hanlon, B. W., Powell, S. P., e Humphreys, T. E. "First Results from Three Years of GNSS Interference Monitoring from Low Earth Orbit." *NAVIGATION*, Vol. 68, No. 4, 2021, pp. 673–685. Preprint: arXiv:2009.04093.
8. Humphreys, T. E., Iannucci, P. A., et al. "Signal Structure of the Starlink Ku-Band Downlink." UT Austin Radionavigation Laboratory. *(Veículo de publicação, volume e ano **[não verificado]**.)* Relacionado: "Timing Properties of the Starlink Ku-Band Downlink," arXiv:2501.05302.

**Cibersegurança de sistemas espaciais**

9. Falco, G. "The Vacuum of Space Cyber Security." *2018 AIAA SPACE and Astronautics Forum and Exposition*, AIAA, 17–19 de setembro de 2018. DOI 10.2514/6.2018-5275.
10. Falco, G. "Cybersecurity Principles for Space Systems." *Journal of Aerospace Information Systems*, Vol. 16, No. 2, 2019 (publicado online em dezembro de 2018). DOI 10.2514/1.I010693. *(Intervalo de páginas **[não verificado]** — o site da AIAA estava inacessível.)* Este artigo é amplamente creditado como insumo da SPD-5, que leva o mesmo título.
11. Falco, G. "Job One for Space Force: Space Asset Cybersecurity." Cyber Security Project, Belfer Center for Science and International Affairs, Harvard Kennedy School, julho de 2018.
12. Falco, G., Boschetti, N., Vecellio Segate, R., Maple, C., et al. "Minimum Requirements for Space System Cybersecurity — Ensuring Cyber Access to Space." *2024 IEEE 10th International Conference on Space Mission Challenges for Information Technology (SMC-IT)*, Mountain View, CA, 2024, pp. 78–88. DOI 10.1109/SMC-IT61443.2024.00016. *(Lista completa e ordem dos autores **[não verificado]** — os índices divergem sobre quais coautores são nomeados.)* **Trabalho anterior mais próximo; ver a Seção 2.5. O texto completo precisa ser lido antes da submissão.**
13. IEEE P3349, Space System Cybersecurity Working Group, IEEE Standards Association. G. Falco, presidente fundador. Padrão técnico internacional de cibersegurança de sistemas espaciais, desenvolvido por um grupo de trabalho que abrange mais de 20 países.

**Frameworks, padrões e política pública**

14. The Aerospace Corporation. *SPARTA: Space Attack Research and Tactic Analysis.* https://sparta.aerospace.org/ — v2.0 publicada; **fixe a versão da matriz no registro de rastreabilidade no momento do uso.** Nota: o SPARTA é um produto da Aerospace Corporation, não da MITRE.
15. Bartock, M., Brule, J., Li-Baboud, Y.-S., Lightman, S., McCarthy, J., Meldorf, K., Reczek, K., Northrip, D., Scholz, A., e Suloway, T. *NIST IR 8323r1: Foundational PNT Profile — Applying the Cybersecurity Framework for the Responsible Use of Positioning, Navigation, and Timing (PNT) Services.* NIST, janeiro de 2023.
16. *NIST IR 8270: Introduction to Cybersecurity for Commercial Satellite Operations.* NIST, julho de 2023.
17. *NIST SP 800-53 Rev. 5: Security and Privacy Controls for Information Systems and Organizations.* NIST, setembro de 2020, com atualizações posteriores (patch release 5.2.0). Os controles citados na Tabela 11 são desta revisão.
18. *Space Policy Directive-5 (SPD-5): Cybersecurity Principles for Space Systems.* Assinada em 4 de setembro de 2020; publicada no Federal Register em 10 de setembro de 2020.
19. *Executive Order 13905: Strengthening National Resilience Through Responsible Use of Positioning, Navigation, and Timing Services.* Assinada em 12 de fevereiro de 2020; Federal Register de 18 de fevereiro de 2020. O NIST IR 8323 foi produzido em cumprimento a esta ordem executiva.
20. *CCSDS 355.0-B-2: Space Data Link Security Protocol.* Recommended Standard (Blue Book), Issue 2, julho de 2022. (Issue 1: setembro de 2015.)
21. EUSPA / European GNSS Service Centre. *Galileo Open Service Navigation Message Authentication (OSNMA).* Fase de observação pública desde 15 de novembro de 2021; serviço declarado operacional em 24 de julho de 2025, com publicação do Service Definition Document do OSNMA.
22. Air Force Research Laboratory. *Chimera (Chips-Message Robust Authentication) signal enhancement for GPS L1C.* Embarcado como experimento no Navigation Technology Satellite-3 (NTS-3), lançado em 12 de agosto de 2025 a bordo de um ULA Vulcan a partir de Cabo Canaveral. Intervalo de autenticação para receptor autônomo ≈ 3 minutos; ≈ 1,5–6 s com canal de chave fora de banda. Ver também a publicação ION "Chips-Message Robust Authentication (Chimera) for GPS Civilian Signals."

**Incidentes**

23. SentinelLabs. *AcidRain: A Modem Wiper Rains Down on Europe.* 31 de março de 2022. Análise do wiper implantado contra modems Viasat KA-SAT em 24 de fevereiro de 2022 por meio do comprometimento da rede de gerenciamento do KA-SAT. Nota quanto ao escopo do presente artigo (Seção 1.4): tratou-se de um comprometimento do **segmento de solo**, não de um ataque a uma espaçonave.

---

## Apêndice A — Gabarito de Requisito

```
REQ-[ID]
  Objetivo:         [objetivo de missão, do estágio 1]
  Criticidade:      [κ]
  Contrato:         D=[...]  α=[...]  ι=[...]  η=[...]  A=[...]
  Ameaça:           [Tn]  (tática SPARTA: [...]; técnica: [fixar versão da matriz])
  Efeito:           [En], magnitude [...], persistência [...]
  Enunciado:        O [subsistema] DEVE [capacidade] de modo que [limite]
                    sob [condição de ameaça].
  Detecção:         [camadas, com λ e P_d]
  Adequação:        (i) λ + t_resposta = [...] < η = [...]    ☐
                    (ii) P_d = [...] ≥ 1 − ι = [...]           ☐
                    (iii) erro residual = [...] ≤ α = [...]    ☐
  Gating de confiança:  Estado mínimo de confiança PNT para a capacidade afetada: [...]
  Verificação:      [análise | ensaio HIL | simulação | inspeção]
  Mapeamento MCB:   [MCB-nn]
  Nível de prioridade:  [de prioridade(R); irreversível ⇒ mais alto]
```

## Apêndice B — Planilha do Analista

Para cada objetivo de missão:

1. Enuncie o objetivo em linguagem de missão, não em linguagem de engenharia. Atribua `κ`.
2. Complete o contrato. Se você não consegue enunciar `η`, pare — a dependência ainda não foi compreendida.
3. Percorra a Tabela 2 contra a dependência. Registre e justifique cada eliminação.
4. Para cada ameaça sobrevivente, determine classe de efeito, magnitude e persistência. Aplique a Seção 3.4: pergunte como fica o *estado da missão* depois do ataque, não o que o receptor reportou durante ele. Avalie `viola()`.
5. Selecione detecção em pelo menos duas camadas de bases físicas distintas. Verifique as condições de adequação (i) e (ii).
6. Selecione mitigações em prevenir / detectar / degradar / recuperar / responder. Atribua o estado mínimo de confiança para cada capacidade autônoma afetada.
7. Escreva o requisito usando o gabarito do Apêndice A. Se ele não puder ser escrito com um limite e um método de verificação, retorne ao passo 2.

---

*Rascunho para discussão. Ver a Seção 10 para limitações e a Seção 12 para a nota de verificação de citações.*

---

## Nota sobre a tradução

Esta é uma tradução da versão em inglês, mantida em `../English/Mission_Driven_Cybersecurity_Requirements.md`. Convenções adotadas:

- **A versão em inglês é a normativa.** Em caso de divergência, ela prevalece; correções devem ser aplicadas a ambas.
- **Numeração idêntica.** Seções, tabelas, figuras, ameaças (T1–T9), efeitos (E1–E5), camadas de detecção (D1–D5), controles (MCB-01–16) e requisitos (REQ-CS-01–09) mantêm os mesmos identificadores nas duas versões.
- **"SHALL" → "DEVE"** nos enunciados de requisito, seguindo a prática brasileira de engenharia de requisitos.
- **Termos técnicos mantidos em inglês** quando são de uso corrente na área e a tradução prejudicaria a busca ou a precisão: *spoofing*, *jamming*, *meaconing*, *holdover*, *walk-off*, *checkpoint*, *rollback*, *gating*, *star tracker*, *smallsat*, *baseline*, *hardware-in-the-loop*, *safe mode*, além das siglas (GNSS, PNT, LEO, OCXO, CSAC, AGC, RAIM, SRP, ISL, HIL, COTS, GSD, AIS, TLE).
- **Nomes dos estados de confiança** (NOMINAL, SUSPECT, DEGRADED, UNTRUSTED) e das táticas do SPARTA são mantidos em inglês porque são rótulos que aparecem em telemetria e em matrizes publicadas.
- **Títulos de obras citadas** permanecem no idioma original.
