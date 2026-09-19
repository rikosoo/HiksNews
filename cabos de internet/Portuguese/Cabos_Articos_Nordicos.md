# Cabos Submarinos no Ártico Nórdico: Clima, Geopolítica e a Resiliência da Infraestrutura Digital Crítica

## Resumo

Os cabos submarinos de fibra óptica transportam a quase totalidade do tráfego de dados intercontinental — a cifra de 99%, amplamente repetida, tem origem documental frágil e é examinada criticamente na Seção 1 —, o que torna essa camada física um ativo de infraestrutura crítica tão essencial quanto as redes de energia ou de transporte. Na região nórdica e ártica, essa infraestrutura opera sob uma condição singular: o mesmo aquecimento regional que viabiliza novas rotas transárticas, ao reduzir a cobertura de gelo marinho e alongar as janelas de lançamento, é o que degrada as condições de instalação, ancoragem e reparo desses sistemas, por meio da perda de permafrost, da erosão costeira e da intensificação do tráfego marítimo.

Este artigo analisa essa tensão em quatro movimentos. Mapeia o cenário de cabos nórdicos e árticos, incluindo os projetos transárticos em desenvolvimento. Examina o clima ártico como vetor de risco físico, decomposto em cinco mecanismos, dos quais a restrição sazonal da capacidade de reparo é o mais determinante. Integra esses mecanismos a um modelo de ameaça único, que trata origem natural, acidental e adversarial como incidentes sobre os mesmos pontos de falha — modelo cuja premissa central, a indistinguibilidade entre acidente e agressão no plano físico, foi confirmada por via judicial no caso *Eagle S*, em que o Tribunal de Apelação de Helsinque firmou, em agosto de 2026, que a distinção repousa não no mecanismo, mas na avaliação da conduta subsequente. Por fim, discute o arcabouço regulatório aplicável (NIS2, Diretiva CER, UNCLOS) e propõe eixos de resiliência hierarquizados por vetor de risco atendido e por custo.

Argumenta-se que risco climático e risco adversarial não constituem agendas separadas na região, mas manifestações de um mesmo problema de resiliência, e que a lentidão da dissuasão por via jurídica desloca o peso da resposta para a detecção precoce e para o projeto resiliente.

---

## Palavras-chave

Cabos Submarinos, Infraestrutura Ártica, Proteção de Infraestrutura Crítica, Resiliência Climática, Região Nórdica, Ameaças Híbridas, Permafrost, Direito do Mar, UNCLOS, Segurança Cibernética

---

## 1. Introdução

A percepção pública da internet é dominada por metáforas imateriais — nuvem, éter, sem fio. A realidade operacional é oposta: a conectividade intercontinental depende de um conjunto finito de cabos de fibra óptica assentados no leito oceânico, cada um com poucos centímetros de diâmetro, cuja destruição física interrompe serviços digitais em escala nacional.

Convém tratar com cuidado a cifra mais repetida nesse debate. A afirmação de que "99% do tráfego intercontinental trafega por cabos submarinos" circula amplamente na imprensa e em documentos de política pública, quase sempre sem fonte. A própria TeleGeography, à qual a cifra é com frequência atribuída, registra que não dispõe de medição direta do tráfego global e que o dado rastreável é outro: estatísticas da Comissão Federal de Comunicações dos Estados Unidos indicam que os satélites respondem por cerca de 0,37% da capacidade internacional norte-americana [8, 9]. A conclusão qualitativa permanece robusta — a dependência da camada submarina é quase total e os enlaces por satélite funcionam como redundância de capacidade limitada, não como substituto —, mas a precisão numérica frequentemente atribuída a ela não se sustenta. Este artigo adota a formulação qualitativa.

A região nórdica concentra três características que tornam esse tema particularmente relevante. Primeiro, há uma dependência estrutural elevada: Islândia, Ilhas Faroe, Groenlândia e Svalbard são territórios cuja conectividade total repousa sobre um número muito pequeno de cabos — em alguns casos, dois. Segundo, a região abriga uma densidade incomum de infraestrutura digital sensível, incluindo data centers de grande porte atraídos pelo clima frio e pela energia renovável barata, além de estações terrestres de satélite de importância científica e militar. Terceiro, o recuo do gelo marinho ártico transformou a região em objeto de projetos de rotas transárticas — notadamente Far North Fiber e Polar Connect — que prometem reduzir substancialmente a latência entre Ásia e Europa em relação às rotas via Suez.

Paralelamente, a sequência de incidentes ocorridos entre 2022 e 2024 no Ártico norueguês e no mar Báltico deslocou os cabos submarinos da categoria de ativo técnico para a de objeto de política de segurança. Este artigo parte dessa convergência e formula três perguntas de pesquisa:

1. De que modo as mudanças climáticas no Ártico alteram o perfil de risco físico da infraestrutura de cabos nórdica?
2. Como os riscos climáticos e os riscos adversariais interagem, em vez de se somarem de forma independente?
3. Quais estratégias de resiliência são aplicáveis a um ambiente em que a capacidade de reparo é geograficamente e sazonalmente restrita?

### 1.1 Metodologia e escopo

O estudo se estrutura como uma revisão documental e analítica. As fontes primárias são de quatro tipos: literatura acadêmica revisada por pares sobre degradação de permafrost e impactos climáticos em infraestrutura ártica; documentos regulatórios da União Europeia e instrumentos de direito internacional; relatórios técnicos de entidades setoriais de cabos submarinos; e relatos públicos e comunicados oficiais referentes aos incidentes de 2022 a 2024. Não foram utilizados dados operacionais proprietários de operadores de cabo.

O escopo geográfico compreende os cinco países nórdicos e seus territórios associados — Islândia, Ilhas Faroe, Groenlândia e Svalbard —, com extensão ao mar Báltico onde os incidentes recentes e a malha de interconexão o exigem. O escopo temporal dos incidentes analisados vai de 2022 ao final de 2024; os desdobramentos judiciais e institucionais deles decorrentes são acompanhados até agosto de 2026, uma vez que a jurisprudência produzida no caso Eagle S é diretamente pertinente à análise da Seção 6.2. As limitações decorrentes dessas escolhas estão explicitadas na Seção 9.

Este artigo dialoga com outros trabalhos deste repositório, em particular [*Security Challenges in Cloud-Based Critical Infrastructure Systems*](../../academics/Security_Challenges.md), que trata da camada lógica e de nuvem da mesma classe de ativos, e [*IT and OT as a Bridge of Friendship*](../../academics/ItAndOT.md), que examina a convergência entre tecnologia de informação e tecnologia operacional referida na Seção 4.

---

## 2. O Cenário de Cabos Nórdicos e Árticos

### 2.1 Configuração atual

A infraestrutura de cabos da região pode ser organizada em quatro camadas.

**Enlaces do Atlântico Norte.** A Islândia é servida por um conjunto reduzido de sistemas: FARICE-1, em operação desde 2004, conectando o país às Ilhas Faroe e à Escócia; DANICE, desde 2009, com aterragem na Dinamarca; e IRIS, que entrou em serviço em 2023, estabelecendo uma rota direta para a Irlanda. A adição do IRIS foi motivada explicitamente por argumentos de redundância nacional, o que ilustra o reconhecimento estatal do problema.

**Enlaces árticos e insulares.** O Svalbard Undersea Cable System, composto por dois pares de fibras entre Longyearbyen e o continente norueguês, sustenta não apenas a população civil do arquipélago, mas também a transmissão de dados da estação de satélites SvalSat, que atende a operadores científicos e comerciais internacionais. A Groenlândia depende do Greenland Connect, em operação desde 2009, com uma configuração igualmente concentrada.

**Enlaces intranórdicos e bálticos.** O mar Báltico é atravessado por uma malha densa de cabos de telecomunicações e de energia que interconecta Finlândia, Suécia, Estônia, Lituânia, Polônia e Alemanha. Entre eles, o C-Lion1 (Helsinque–Rostock) e o BCS East-West Interlink (Lituânia–Suécia) ganharam notoriedade pelos danos sofridos em 2024. A característica geográfica determinante aqui é a profundidade: o Báltico é um mar raso, o que coloca os cabos ao alcance de âncoras de navios comerciais em grande parte de seu traçado.

**Rotas transárticas em desenvolvimento.** O projeto Far North Fiber, empreendimento conjunto entre a finlandesa Cinia, a norte-americana Far North Digital e a japonesa Arteria Networks, propõe conectar Japão e Europa atravessando a Passagem Noroeste ao longo de aproximadamente 14 mil quilômetros, com aterragens previstas no Alasca, no Canadá ártico, na Groenlândia, na Islândia, na Noruega, na Finlândia e na Irlanda. O Polar Connect, conduzido no âmbito da NORDUnet e de redes acadêmicas nórdicas, estuda uma rota a partir da Noruega, via Svalbard, através do Oceano Ártico [10]. Ambos derivam sua viabilidade das condições de gelo alteradas pelo aquecimento regional.

**Tabela 1 — Sistemas de referência na região nórdica e ártica**

| Sistema | Rota | Em serviço | Observação |
|---|---|---|---|
| FARICE-1 | Islândia – Ilhas Faroe – Escócia | 2004 | Primeiro enlace moderno da Islândia |
| DANICE | Islândia – Dinamarca | 2009 | Segunda rota islandesa |
| IRIS | Islândia – Irlanda | 2023 | Adicionado por argumento explícito de redundância nacional |
| Greenland Connect | Groenlândia – Islândia / Canadá | 2009 | Dependência concentrada |
| Svalbard Undersea Cable System | Longyearbyen – Noruega continental | 2004 | Dois pares de fibras; sustenta a estação SvalSat |
| C-Lion1 | Helsinque – Rostock | 2016 | Danificado em novembro de 2024 |
| BCS East-West Interlink | Lituânia – Suécia | 2009 | Danificado em novembro de 2024 |
| Far North Fiber | Japão – Europa, via Passagem Noroeste (~14.000 km) | Em implantação | Consórcio Cinia / Far North Digital / Arteria; viabilidade decorrente do recuo do gelo |
| Polar Connect | Noruega – Svalbard – Ártico – Ásia / América do Norte | Em estudo | Conduzido por redes acadêmicas nórdicas, com cofinanciamento europeu |

### 2.2 Concentração e pontos de estrangulamento

Do ponto de vista de proteção de infraestrutura crítica, o traço mais relevante desse cenário não é o número de cabos, mas a distribuição da dependência. Um território servido por dois cabos possui, na prática, tolerância a uma única falha. Quando ambos compartilham corredor geográfico, estação de aterragem ou backhaul terrestre, mesmo essa tolerância é nominal: um evento único pode comprometer os dois caminhos.

As estações de aterragem merecem atenção específica. São instalações terrestres, fixas, publicamente localizáveis e frequentemente situadas em áreas costeiras remotas com vigilância limitada. Concentram, em um ponto único, o equipamento de terminação óptica, a alimentação elétrica dos repetidores submarinos e a interconexão com a rede terrestre. No contexto ártico, acumulam ainda uma vulnerabilidade adicional, tratada na seção seguinte: muitas estão assentadas sobre terreno cuja estabilidade geotécnica está mudando.

---

## 3. O Clima Ártico como Vetor de Risco Físico

O Ártico aquece a uma taxa várias vezes superior à média global, fenômeno documentado na literatura climatológica como amplificação ártica. Rantanen et al. (2022) estimam que, no período de 1979 a 2021, a região aqueceu aproximadamente 3,8 vezes mais rápido que a média planetária, com razão ainda maior no mar de Barents [2]. As consequências para a infraestrutura de cabos se distribuem em cinco mecanismos distintos.

### 3.1 Recuo do gelo marinho: habilitação e exposição

A extensão mínima anual do gelo marinho ártico, medida em setembro, apresenta tendência de declínio consistente ao longo das últimas quatro décadas, conforme as séries do National Snow and Ice Data Center [4] e as sínteses do Arctic Monitoring and Assessment Programme [5]. Para a indústria de cabos, o efeito primário é habilitador: janelas de navegação mais longas permitem operações de lançamento em rotas antes inacessíveis, o que é precondição para projetos como o Far North Fiber.

O efeito secundário, porém, é de exposição. Águas navegáveis atraem tráfego marítimo comercial, pesqueiro e turístico — e a causa dominante de falhas em cabos submarinos em escala global não é sabotagem nem desastre natural, mas exatamente essa atividade humana rotineira. Dados setoriais compilados pelo International Cable Protection Committee situam âncoras arrastadas e redes de pesca de fundo entre 70% e 80% do total de falhas, em um universo da ordem de duzentas falhas anuais no conjunto dos sistemas globais [6, 7]. Segue-se que um Ártico navegável é, por construção, um Ártico onde essa causa dominante passa a operar.

Cabe registrar que a redução do gelo não elimina o risco associado ao gelo. Icebergs à deriva e o sulcamento do leito marinho por quilhas de gelo (*ice keel scouring*) continuam representando ameaças em águas rasas costeiras, e a mobilidade aumentada do gelo pode tornar esses eventos menos previsíveis.

### 3.2 Degradação do permafrost sob instalações terrestres

Este é o mecanismo de maior relevância para as estações de aterragem e para o backhaul terrestre. O degelo do permafrost reduz a capacidade de suporte do solo, provoca recalques diferenciais e compromete fundações dimensionadas sob a premissa de terreno permanentemente congelado. Hjort et al. (2018), em estudo publicado na *Nature Communications*, estimaram que cerca de 70% da infraestrutura construída no domínio do permafrost situa-se em áreas com alto potencial de degelo do permafrost próximo à superfície, e que aproximadamente um terço da infraestrutura pan-ártica se encontra em regiões onde a instabilidade do solo associada ao degelo pode causar dano severo ao ambiente construído até meados do século — proporções que, segundo os autores, não se reduzem substancialmente mesmo no cenário de cumprimento das metas do Acordo de Paris [1].

A implicação para cabos é direta e frequentemente subestimada: a resiliência de um sistema submarino é avaliada, em geral, pelo trecho submerso, mas o ponto de falha pode estar em terra firme, sob um edifício de aterragem cuja fundação está se deslocando.

### 3.3 Erosão costeira e instabilidade do leito

A combinação de permafrost costeiro degradado, menor proteção por gelo marinho e maior energia de ondas acelera a erosão de costas árticas, com taxas de recuo que, em alguns trechos, atingem vários metros por ano. Cabos com aterragem nessas costas podem ter seu trecho de praia exposto, deslocado ou submetido a esforços mecânicos não previstos em projeto. Em ambiente submarino, o aumento do aporte sedimentar fluvial e a instabilidade de taludes elevam a probabilidade de correntes de turbidez — fluxos de sedimento em massa capazes de romper múltiplos cabos simultaneamente ao longo de um mesmo cânion submarino, com precedentes documentados em outras regiões do mundo.

### 3.4 Efeitos térmicos sobre o sistema óptico

Variações de temperatura afetam parâmetros ópticos e eletrônicos de sistemas de longa distância. No trecho submarino profundo, a temperatura é estável e o efeito é marginal. A sensibilidade concentra-se nos trechos rasos, no segmento terrestre e nos equipamentos das estações de aterragem, onde alterações no regime térmico e na estabilidade do solo influenciam tanto o desempenho quanto o ciclo de manutenção. Trata-se de um fator secundário quando comparado aos mecanismos geotécnicos, mas relevante para o dimensionamento de margens de projeto em sistemas com vida útil projetada de 25 anos — horizonte em que as condições ambientais de referência já não podem ser tratadas como estacionárias.

### 3.5 Restrição sazonal da capacidade de reparo

O tempo de reparo é a variável que converte uma falha em crise. Globalmente, o reparo de um cabo submarino depende de uma frota especializada de navios-cabo, numericamente reduzida, com idade média elevada e distribuída de forma desigual. No Ártico, três fatores agravam o quadro: a distância até as bases de navios disponíveis, a necessidade de casco com classe de gelo para operar em parte do ano e as janelas meteorológicas restritas. Uma falha ocorrida no início do inverno pode permanecer sem reparo por meses.

Este ponto merece destaque analítico: em regiões temperadas, a resiliência é discutida majoritariamente em termos de redundância de caminho. No Ártico, a redundância de caminho é necessária mas insuficiente, porque a janela de indisponibilidade de qualquer caminho é estruturalmente mais longa.

---

## 4. Cabos como Infraestrutura Crítica: Dependências e Efeitos em Cascata

A classificação de cabos submarinos como infraestrutura crítica decorre menos do serviço que prestam diretamente e mais das dependências que outros setores estabeleceram sobre eles.

**Energia.** Sistemas modernos de geração e transmissão dependem de telemetria, supervisão remota e coordenação entre operadores. Onde a convergência entre TI e TO (Tecnologia Operacional) foi implementada com dependência de conectividade externa — para monitoramento em nuvem, manutenção preditiva ou acesso remoto de fornecedores —, a perda de conectividade internacional degrada a capacidade de operação supervisionada. Cabos de energia e de telecomunicações frequentemente compartilham corredores no Báltico, o que cria correlação de falha entre os dois setores.

**Serviços financeiros e públicos.** A digitalização avançada dos Estados nórdicos, com identidade digital, pagamentos eletrônicos e serviços públicos majoritariamente on-line, converte uma interrupção de conectividade em interrupção de serviço essencial ao cidadão.

**Saúde e operações remotas.** Em territórios árticos de baixa densidade populacional, a telemedicina e o suporte remoto a operações de busca e salvamento não são conveniências, mas componentes do sistema de atendimento.

**Ciência e observação da Terra.** O caso de Svalbard é ilustrativo: a estação SvalSat realiza downlink de dados de satélites de observação polar para operadores internacionais, e o escoamento desses dados depende do cabo submarino. Um dano ao enlace afeta usuários muito além da Noruega.

**Data centers.** A atratividade da região para computação em larga escala repousa sobre energia renovável barata e resfriamento natural, mas o valor econômico dessa carga de trabalho só se realiza por meio da conectividade internacional. Concentrar capacidade computacional em um local com poucos caminhos de saída transfere o risco de concentração do cabo para os serviços nele hospedados.

### 4.1 Incidentes de referência

**Svalbard, janeiro de 2022.** Em 7 de janeiro de 2022, um dos dois cabos do sistema de Svalbard — enlace de cerca de 1.300 km operado pela Space Norway — perdeu comunicação após dano em trecho de águas profundas. O enlace remanescente manteve a conectividade do arquipélago, o que demonstrou o valor da redundância existente e, simultaneamente, expôs o fato de que o sistema operou durante todo o período de reparo sem qualquer margem adicional. As marcas no cabo recuperado eram compatíveis com raspagem por objeto rebocado ao longo do leito, tipicamente uma porta de arrasto de rede de pesca. A polícia norueguesa considerou provável a origem em atividade humana, não estabeleceu intencionalidade e encerrou a investigação por insuficiência de provas, sem indiciamento [14]. O episódio é objeto de análise detalhada de Schia, Gjesvik e Rødningen [3], que examinam a cadeia de consequências e a gestão da crise. A ausência de atribuição conclusiva é, em si, um achado analiticamente relevante, retomado na Seção 5.

**Balticconnector e cabos associados, outubro de 2023.** O gasoduto Balticconnector, entre Finlândia e Estônia, e cabos de telecomunicações próximos sofreram danos simultâneos. A investigação finlandesa concentrou-se no arrasto de âncora por um navio comercial.

**Mar Báltico, novembro de 2024.** Os cabos BCS East-West Interlink (Lituânia–Suécia) e C-Lion1 (Finlândia–Alemanha) foram danificados em intervalo de aproximadamente 24 horas, em um padrão consistente com arrasto de âncora ao longo de uma mesma rota de navegação. A operadora Cinia registrou a falha no C-Lion1 às 4h04 (horário da Europa Oriental) de 18 de novembro de 2024, atribuiu-a a força física externa e encaminhou pedido de investigação ao Serviço Nacional de Investigação finlandês no dia seguinte [16]; o serviço foi restabelecido em 28 de novembro, após dez dias de indisponibilidade e do deslocamento de um navio-cabo desde Calais [17]. O intervalo é ilustrativo do argumento da Seção 3.5, ainda que se trate de um mar de acesso comparativamente fácil.

**Estlink 2 e cabos adjacentes, dezembro de 2024.** Em 25 de dezembro de 2024, o cabo de energia Estlink 2, entre Finlândia e Estônia, e quatro cabos de telecomunicações foram danificados. As autoridades finlandesas conduziram o navio-tanque *Eagle S*, registrado nas Ilhas Cook, às águas territoriais finlandesas e abriram investigação; segundo o Serviço Nacional de Investigação, a embarcação arrastou sua âncora pelo leito por distância da ordem de noventa a cem quilômetros [15]. O episódio marcou uma inflexão na postura de aplicação da lei na região e gerou o desdobramento judicial tratado na Seção 6.2, cuja relevância excede a do incidente isolado.

O padrão comum a esses casos é significativo para a análise de risco: o mecanismo físico do dano — uma âncora arrastada no leito — é idêntico ao de um acidente marítimo corriqueiro. Essa equivalência é precisamente o que torna a atribuição difícil e o que, na literatura de segurança, caracteriza a ação abaixo do limiar do conflito armado.

---

## 5. Modelo de Ameaça: Natural, Acidental e Adversarial

A prática convencional separa a análise de risco natural da análise de risco de segurança. Para cabos árticos nórdicos, essa separação produz avaliações incompletas, porque os três tipos de origem convergem sobre o mesmo pequeno conjunto de pontos de falha e, em parte, sobre o mesmo mecanismo físico.

**Tabela 2 — Modelo de ameaça consolidado**

| Origem | Mecanismo típico | Frequência relativa | Tempo de reparo | Atribuição |
|---|---|---|---|---|
| Natural — geotécnica | Degelo de permafrost, erosão costeira, deslizamento submarino | Baixa por evento, crescente na tendência | Longo (obra civil) | Não aplicável |
| Natural — gelo | Sulcamento por quilha de gelo, iceberg à deriva | Baixa a moderada, sazonal | Longo (restrição de acesso) | Não aplicável |
| Acidental — humana | Âncora, rede de pesca de fundo | Alta (causa dominante global) | Médio, restrito por janela | Geralmente possível |
| Adversarial — híbrida | Arrasto deliberado de âncora, intervenção subaquática | Baixa, concentrada geograficamente | Médio a longo | Difícil e frequentemente inconclusiva |
| Adversarial — cibernética | Comprometimento de sistemas de gerenciamento da rede e da estação de aterragem | Sem dados públicos consolidados | Variável | Difícil |

Três observações decorrem dessa estrutura.

Primeiro, **a ambiguidade é uma propriedade do domínio, não uma falha da investigação.** Quando o mesmo ato físico pode ser acidente ou agressão, a resposta institucional é estruturalmente lenta, e um adversário racional obtém efeito com risco de atribuição reduzido.

Segundo, **o clima altera a linha de base contra a qual a anomalia é medida.** Um mar mais navegável produz mais incidentes acidentais genuínos. Isso eleva o ruído de fundo, tornando mais difícil distinguir o evento deliberado — o que constitui uma interação entre o vetor climático e o vetor adversarial, e não uma mera coincidência temporal.

Terceiro, **a dimensão cibernética não deve ser omitida.** A discussão pública concentra-se no dano físico, mas os sistemas de gerenciamento de elementos de rede, os sistemas de alimentação (*power feed equipment*) e os controles de acesso das estações de aterragem constituem superfície de ataque lógica. Aplicam-se aqui os mesmos princípios de defesa em profundidade, segmentação e gestão de identidade discutidos para ambientes de infraestrutura crítica em nuvem e para convergência TI/TO.

---

## 6. Governança e Arcabouço Regulatório

### 6.1 Nível europeu

A Diretiva NIS2 (Diretiva (UE) 2022/2555) [11] amplia o escopo de entidades sujeitas a requisitos de gestão de risco cibernético e de notificação de incidentes, incluindo explicitamente a infraestrutura digital. A Diretiva CER (Diretiva (UE) 2022/2557) [12], sobre a resiliência de entidades críticas, trata da dimensão física e exige que os Estados-membros identifiquem entidades críticas e conduzam avaliações de risco que contemplem, entre outros fatores, riscos naturais e mudanças climáticas. A leitura conjunta das duas diretivas é o instrumento mais direto para tratar a convergência analisada neste artigo.

A aplicabilidade na região não é uniforme. Dinamarca, Suécia e Finlândia são Estados-membros da União Europeia. Noruega e Islândia integram o Espaço Econômico Europeu, com incorporação por mecanismo próprio e cronograma distinto. A Groenlândia e as Ilhas Faroe possuem estatutos específicos. O resultado é um mosaico regulatório sobre uma infraestrutura que, por natureza, é transfronteiriça.

### 6.2 Direito internacional do mar

A Convenção das Nações Unidas sobre o Direito do Mar (UNCLOS) [13] trata da proteção de cabos submarinos em seus artigos 113 a 115, obrigando os Estados a tipificar como infração o dano doloso ou por negligência culposa a cabo submarino causado por navio de sua bandeira. O regime apresenta três fragilidades operacionais reconhecidas na literatura: depende da jurisdição do Estado de bandeira, cuja cooperação é incerta; foi concebido para o acidente e não para a ação estatal deliberada; e oferece instrumentos limitados de interdição em alto-mar.

O caso *Eagle S* converteu essa discussão doutrinária em jurisprudência. Em outubro de 2025, o Tribunal Distrital de Helsinque extinguiu o processo criminal contra o comandante e dois oficiais da embarcação por entender que a Finlândia carecia de jurisdição: os atos imputados teriam ocorrido na zona econômica exclusiva finlandesa, fora, portanto, do mar territorial, e a lei penal finlandesa não lhes alcançaria. A decisão repercutiu como demonstração concreta da lacuna apontada pela literatura — navios sob bandeira de conveniência poderiam danificar infraestrutura submarina em águas não territoriais sem consequência penal efetiva.

Em 27 de agosto de 2026, o Tribunal de Apelação de Helsinque reformou, por unanimidade, aquela decisão, reconhecendo a jurisdição finlandesa e determinando a reabertura do processo em primeira instância [18, 19]. O fundamento é analiticamente relevante para este artigo: embora o tribunal tenha admitido que o lançamento inicial da âncora pudesse ser tratado como acidental, entendeu que o que se seguiu — o arrasto prolongado pelo leito — não se enquadra na categoria de acidente marítimo para os fins da UNCLOS. A decisão ainda não é definitiva e admite recurso à Suprema Corte, cujo prazo se encerra em outubro de 2026.

O episódio confirma a tese central da Seção 5 por via judicial: a linha que separa acidente de agressão não é dada pelo mecanismo físico, que é idêntico nos dois casos, mas por uma avaliação da conduta subsequente. Enquanto essa avaliação depender de litígio prolongado e de resultado incerto, a dissuasão por consequência jurídica permanece fraca — o que reforça o peso relativo das medidas de detecção e de projeto resiliente discutidas na Seção 7.

### 6.3 Dimensão de defesa e cooperação regional

A resposta institucional recente inclui iniciativas de vigilância marítima dedicadas à proteção de infraestrutura submarina, entre elas a operação Nordic Warden, conduzida no âmbito da Joint Expeditionary Force, e a atividade Baltic Sentry, iniciada pela OTAN em 14 de janeiro de 2025 após a série de incidentes, conduzida pelo Comando de Força Conjunta Aliada de Brunssum em articulação com o Comando Marítimo Aliado [20]. A adesão de Finlândia e Suécia à OTAN alterou de forma substantiva a arquitetura de segurança regional no período analisado.

---

## 7. Estratégias de Resiliência

As medidas a seguir são organizadas por horizonte de implementação e tratam conjuntamente as origens de risco identificadas na Seção 5.

### 7.1 Diversidade estrutural

**Diversidade de rota e de aterragem.** A redundância só é efetiva quando os caminhos alternativos não compartilham corredor submarino, estação de aterragem, backhaul terrestre nem fornecedor de energia. A avaliação deve ser conduzida como análise de modo de falha comum, e não como contagem de cabos. O caso islandês, com a adição do IRIS em rota distinta, exemplifica a aplicação desse princípio.

**Heterogeneidade tecnológica.** Constelações de satélites em órbita baixa não substituem a capacidade de um cabo, mas podem sustentar serviços essenciais mínimos — comunicação de emergência, telemetria crítica, coordenação de resposta — durante o período de reparo. O dimensionamento deve ser explícito quanto a essa limitação, e a própria camada satelital possui seu conjunto distinto de vulnerabilidades.

### 7.2 Detecção e monitoramento

**Sensoriamento acústico distribuído (DAS).** Técnicas que utilizam a própria fibra óptica como sensor distribuído permitem detectar eventos mecânicos ao longo do cabo — incluindo atividade de âncora nas proximidades — antes que o dano se concretize ou imediatamente após, com localização precisa. O valor é duplo: reduz o tempo de localização da falha, que é componente relevante do tempo total de reparo, e fornece evidência técnica para investigação e atribuição.

**Fusão com dados de tráfego marítimo.** A correlação entre eventos detectados na fibra e dados de AIS permite identificar padrões anômalos, incluindo desligamento de transponder e velocidade incompatível com navegação normal sobre traçados de cabo conhecidos.

**Monitoramento geotécnico das aterragens.** Instrumentação de temperatura de solo e de recalque em estações situadas em domínio de permafrost, integrada ao ciclo de manutenção preventiva.

### 7.3 Capacidade de resposta

**Capacidade regional de reparo.** A disponibilidade de navio-cabo com classe de gelo posicionado na região, seja por contrato de prontidão compartilhado entre operadores nórdicos, seja por arranjo público-privado, ataca diretamente a variável de tempo de reparo identificada na Seção 3.5. Esta é, entre as medidas listadas, a de maior custo e a de maior efeito sobre o risco agregado.

**Planejamento de contingência intersetorial.** Exercícios que envolvam operadores de telecomunicações, de energia, autoridades marítimas e órgãos de proteção civil, com cenários que incluam indisponibilidade prolongada e não apenas interrupção breve.

### 7.4 Projeto informado por clima

Sistemas com vida útil de 25 anos instalados hoje operarão sob condições ambientais significativamente distintas das atuais. Recomenda-se que a seleção de rota, o dimensionamento de enterramento, a escolha do sítio de aterragem e o projeto de fundação utilizem projeções climáticas regionais como parâmetro de entrada, em vez de séries históricas tratadas como estacionárias. Para novas rotas transárticas, esse princípio é especialmente pertinente, dado que a própria viabilidade do projeto decorre de uma mudança ambiental ainda em curso.

### 7.5 Síntese

A Tabela 3 relaciona cada medida aos vetores de risco da Seção 5, evidenciando quais delas atuam sobre mais de uma origem de risco simultaneamente — critério útil de priorização quando o orçamento é limitado.

**Tabela 3 — Medidas de resiliência e vetores de risco atendidos**

| Medida | Geotécnico | Gelo | Acidental | Adversarial | Horizonte | Custo relativo |
|---|:---:|:---:|:---:|:---:|---|---|
| Diversidade de rota e aterragem | ✔ | ✔ | ✔ | ✔ | Longo | Alto |
| Heterogeneidade tecnológica (satélite) | ✔ | ✔ | ✔ | ✔ | Curto | Médio |
| Sensoriamento acústico distribuído (DAS) | — | ✔ | ✔ | ✔ | Curto | Baixo a médio |
| Fusão com dados AIS | — | — | ✔ | ✔ | Curto | Baixo |
| Monitoramento geotécnico das aterragens | ✔ | — | — | — | Médio | Baixo |
| Navio-cabo com classe de gelo na região | ✔ | ✔ | ✔ | ✔ | Médio | Muito alto |
| Contingência intersetorial | ✔ | ✔ | ✔ | ✔ | Curto | Baixo |
| Projeto informado por clima | ✔ | ✔ | — | — | Longo | Baixo no projeto novo |

Duas leituras se destacam. O sensoriamento distribuído e a fusão com dados AIS oferecem a melhor relação entre custo e cobertura de vetores, por atuarem sobre o tempo de localização da falha e sobre a capacidade de atribuição. A capacidade regional de reparo é a medida mais cara e a única que reduz diretamente a duração da indisponibilidade, que é a variável determinante identificada na Seção 3.5.

---

## 8. Discussão

A tensão central identificada neste artigo pode ser formulada de maneira direta: **o degelo ártico é simultaneamente a condição de possibilidade e a principal fonte de risco físico das novas rotas de cabo na região.** As mesmas condições que tornam economicamente atrativa uma rota transártica — menos gelo, janelas de navegação mais longas — produzem terreno de aterragem instável, costas em erosão e tráfego marítimo mais denso sobre traçados de cabo. Tratar oportunidade e risco como agendas separadas, conduzidas por equipes distintas, é o erro analítico que este artigo procura evidenciar.

Uma segunda conclusão diz respeito à relação entre clima e ameaça híbrida. Não se sustenta aqui qualquer relação causal entre mudança climática e ação adversarial. O que se argumenta é mais específico e, do ponto de vista de defesa, mais consequente: o aumento do tráfego marítimo legítimo eleva a taxa de incidentes acidentais genuínos, o que amplia o ruído de fundo contra o qual um evento deliberado precisaria ser distinguido. Em um domínio onde o mecanismo físico do acidente e o da agressão são indistinguíveis, elevar o ruído de fundo é, funcionalmente, degradar a capacidade de atribuição.

Uma terceira observação refere-se à assimetria entre custo de ataque e custo de defesa. Danificar um cabo exige meios modestos e amplamente disponíveis. Protegê-lo exige vigilância marítima contínua sobre áreas extensas, capacidade naval de reparo e redundância cara. Essa assimetria não é eliminável por meios técnicos; ela desloca o peso da resposta para o projeto resiliente, para a detecção precoce e para a dissuasão por meio de atribuição e consequência jurídica crível — o que confere à discussão regulatória da Seção 6 um peso operacional, e não meramente formal. A trajetória judicial do caso *Eagle S*, que consumiu quase dois anos apenas para firmar a competência do foro, dimensiona a distância entre a dissuasão pretendida e a efetivamente disponível.

---

## 9. Limitações

Este trabalho constitui uma revisão documental e analítica, baseada em literatura acadêmica, documentos regulatórios públicos e relatos de incidentes de domínio público. Não incorpora dados operacionais proprietários de operadores de cabo, cuja divulgação é restrita por razões comerciais e de segurança. As investigações referentes aos incidentes de 2022 a 2024 encontram-se, em parte, sem conclusão pública definitiva, de modo que as caracterizações apresentadas na Seção 4 devem ser lidas como descrição do que é conhecido publicamente, e não como atribuição. As estimativas quantitativas citadas — participação dos cabos no tráfego intercontinental, proporção de infraestrutura ártica em risco de degelo — provêm das fontes indicadas e carregam as incertezas metodológicas próprias a elas. Por fim, a situação regulatória e de segurança regional descrita reflete o estado dos fatos até setembro de 2026 e é objeto de evolução rápida; em particular, o desfecho do caso *Eagle S* permanece pendente de eventual recurso à Suprema Corte finlandesa, de modo que as conclusões da Seção 6.2 devem ser lidas como análise de um precedente ainda não consolidado.

---

## 10. Conclusão

A infraestrutura de cabos submarinos do Ártico nórdico ocupa uma posição incomum na análise de infraestrutura crítica: é o ponto em que risco climático, risco acidental e ameaça geopolítica incidem sobre o mesmo ativo físico, com os mesmos modos de falha e o mesmo conjunto restrito de opções de reparo. A resposta adequada não é conduzir três análises de risco paralelas, mas uma única análise de resiliência que reconheça a interação entre esses vetores.

Retomando as perguntas formuladas na Seção 1:

**Quanto ao perfil de risco físico (pergunta 1),** o aquecimento regional não desloca esse perfil em uma única direção. Ele o reconfigura: habilita rotas ao recuar o gelo, e simultaneamente degrada a fundação das estações de aterragem pelo degelo do permafrost, expõe trechos costeiros pela erosão, eleva a probabilidade de eventos de instabilidade no leito e amplia a exposição a âncoras e artes de pesca ao tornar o mar navegável. O mecanismo de maior consequência prática, contudo, não é o dano em si, mas a restrição sazonal da capacidade de reparo, que alonga estruturalmente a janela de indisponibilidade.

**Quanto à interação entre os vetores (pergunta 2),** não se sustenta relação causal entre mudança climática e ação adversarial. Sustenta-se algo mais específico: ao elevar o volume de tráfego marítimo legítimo, o degelo aumenta a taxa de incidentes acidentais genuínos e, com ela, o ruído de fundo contra o qual um evento deliberado precisaria ser distinguido. Em um domínio onde o mecanismo físico do acidente e o da agressão são idênticos, elevar esse ruído equivale a degradar a capacidade de atribuição. O caso *Eagle S* deu a essa proposição confirmação judicial e mediu seu custo: quase dois anos de litígio apenas para firmar a competência do foro.

**Quanto às estratégias aplicáveis (pergunta 3),** quatro prioridades emergem, hierarquizadas na Tabela 3. Diversidade estrutural avaliada por modo de falha comum, e não por contagem de cabos. Detecção precoce por sensoriamento na própria fibra, integrada a dados de tráfego marítimo — a medida de melhor relação entre custo e cobertura de vetores. Capacidade regional de reparo com classe de gelo, a mais onerosa e a única que reduz diretamente o tempo de indisponibilidade. E projeto de infraestrutura que adote projeções climáticas como parâmetro de entrada, dada a incompatibilidade entre uma vida útil de 25 anos e um ambiente não estacionário.

A camada física da internet foi, por muito tempo, tratada como um problema resolvido de engenharia. No Ártico nórdico, ela voltou a ser uma questão aberta de política pública, de direito internacional e de segurança.

---

## Referências

Vinte referências formatadas segundo a ABNT NBR 6023. Todas as fontes em linha foram verificadas em **19 de setembro de 2026**, data de acesso indicada em cada entrada. As entradas [14], [18] e [19] são fontes jornalísticas ou de blog acadêmico, empregadas nas condições descritas na nota ao final.

### Literatura acadêmica

[1] HJORT, Jan et al. Degrading permafrost puts Arctic infrastructure at risk by mid-century. **Nature Communications**, v. 9, art. 5147, 11 dez. 2018. DOI: 10.1038/s41467-018-07557-4. Disponível em: https://www.nature.com/articles/s41467-018-07557-4. Acesso em: 19 set. 2026.

[2] RANTANEN, Mika et al. The Arctic has warmed nearly four times faster than the globe since 1979. **Communications Earth & Environment**, v. 3, art. 168, 11 ago. 2022. DOI: 10.1038/s43247-022-00498-3. Disponível em: https://www.nature.com/articles/s43247-022-00498-3. Acesso em: 19 set. 2026.

### Dados climáticos e ambientais

[3] SCHIA, Niels Nagelhus; GJESVIK, Lars; RØDNINGEN, Ida. **The subsea cable cut at Svalbard January 2022: What happened, what were the consequences, and how were they managed?** NUPI Policy Brief 1/2023. Oslo: Norwegian Institute of International Affairs, 2023. Disponível em: https://www.nupi.no/content/pdf_preview/26372/file/NUPI_Policy_Brief_1_23_Schia_Gjesvik_R%C3%B8dningen-FERDIG.pdf. Acesso em: 19 set. 2026.

### Dados climáticos e ambientais

[4] FETTERER, Florence; KNOWLES, Kenneth; MEIER, Walter N.; SAVOIE, Matthew; WINDNAGEL, Ann K.; STAFFORD, Timothy. **Sea Ice Index**, Version 4. Boulder, Colorado: National Snow and Ice Data Center, 2025. Conjunto de dados G02135. DOI: 10.7265/a98x-0f50. Disponível em: https://nsidc.org/data/g02135/versions/4. Acesso em: 19 set. 2026.

[5] ARCTIC MONITORING AND ASSESSMENT PROGRAMME. **Arctic Climate Change Update 2021: Key Trends and Impacts**. Tromsø: AMAP, 2021. viii + 148 p. Disponível em: https://www.amap.no/documents/doc/amap-arctic-climate-change-update-2021-key-trends-and-impacts/3594. Acesso em: 19 set. 2026.

### Infraestrutura de cabos submarinos

[6] EUROPEAN UNION AGENCY FOR CYBERSECURITY. **Subsea Cables — What is at Stake?** Atenas: ENISA, jul. 2023. Disponível em: https://www.enisa.europa.eu/sites/default/files/publications/Undersea%20cables%20-%20What%20is%20a%20stake%20report.pdf. Acesso em: 19 set. 2026.

[7] INTERNATIONAL CABLE PROTECTION COMMITTEE. **Government Best Practices for Protecting and Promoting Resilience of Submarine Telecommunications Cables**, versão 1.2. ICPC, [s.d.]. Disponível em: https://www.iscpc.org/documents/?id=3733. Acesso em: 19 set. 2026.

[8] TELEGEOGRAPHY. **Do Submarine Cables Account For Over 99% of Intercontinental Data Traffic?** Série Mythbusting, parte 3, 2023. Disponível em: https://resources.telegeography.com/2023-mythbusting-part-3. Acesso em: 19 set. 2026.

[9] TELEGEOGRAPHY. **Submarine Cable FAQs**. [s.d.]. Disponível em: https://www2.telegeography.com/submarine-cable-faqs-frequently-asked-questions. Acesso em: 19 set. 2026.

[10] NORDUNET. **Polar Connect**. Descrição do projeto de enlace transártico. Disponível em: https://nordu.net/polar-connect/. Acesso em: 19 set. 2026.

### Instrumentos normativos

[11] UNIÃO EUROPEIA. **Diretiva (UE) 2022/2555** do Parlamento Europeu e do Conselho, de 14 de dezembro de 2022, relativa a medidas destinadas a garantir um elevado nível comum de cibersegurança na União (Diretiva NIS 2). *Jornal Oficial da União Europeia*, L 333, p. 80–152, 27 dez. 2022. CELEX 32022L2555. Disponível em: http://data.europa.eu/eli/dir/2022/2555/oj. Acesso em: 19 set. 2026.

[12] UNIÃO EUROPEIA. **Diretiva (UE) 2022/2557** do Parlamento Europeu e do Conselho, de 14 de dezembro de 2022, relativa à resiliência das entidades críticas e que revoga a Diretiva 2008/114/CE do Conselho (Diretiva CER). *Jornal Oficial da União Europeia*, L 333, p. 164–198, 27 dez. 2022. CELEX 32022L2557. Em vigor desde 16 jan. 2023. Disponível em: http://data.europa.eu/eli/dir/2022/2557/oj. Acesso em: 19 set. 2026.

[13] ORGANIZAÇÃO DAS NAÇÕES UNIDAS. **Convenção das Nações Unidas sobre o Direito do Mar**. Montego Bay, 10 dez. 1982. *United Nations Treaty Series*, v. 1833, p. 3. Em vigor desde 16 nov. 1994. Artigos 113 a 115. Disponível em: https://www.un.org/depts/los/convention_agreements/texts/unclos/unclos_e.pdf. Acesso em: 19 set. 2026.

### Fontes primárias sobre incidentes

[14] THE BARENTS OBSERVER. **'Human activity' behind Svalbard cable disruption**. Kirkenes, fev. 2022. Disponível em: https://thebarentsobserver.com/en/security/2022/02/unknown-human-activity-behind-svalbard-cable-disruption. Acesso em: 19 set. 2026.

[15] POLIISI — FINNISH POLICE. **Police investigating incidents in the Gulf of Finland in cooperation with other authorities**. Comunicado oficial, 26 dez. 2024. Disponível em: https://poliisi.fi/en/-/police-investigating-incidents-in-the-gulf-of-finland-in-cooperation-with-other-authorities. Acesso em: 19 set. 2026.

[16] CINIA OY. **A fault in the Cinia C-Lion1 submarine cable between Finland and Germany**. Comunicado oficial, 18 nov. 2024. Disponível em: https://www.cinia.fi/en/news/a-fault-in-the-cinia-c-lion1-submarine-cable-between-finland-and-germany. Acesso em: 19 set. 2026.

[17] CINIA OY. **Cinia's C-Lion1 Submarine Cable Has Fully Restored**. Comunicado oficial, 28 nov. 2024. Disponível em: https://www.cinia.fi/en/news/cinias-c-lion1-submarine-cable-has-fully-restored. Acesso em: 19 set. 2026.

[18] YLE NEWS. **Court u-turn: Finland does have jurisdiction in Eagle S cable damage case**. Helsinque, 27 ago. 2026. Disponível em: https://yle.fi/a/74-20243196. Acesso em: 19 set. 2026.

[19] PAPANICOLOPULU, Irini et al. **Anchoring Criminal Jurisdiction at Sea: The Helsinki District Court's Eagle S Judgement and its impact for the protection of submarine cables and pipelines**. EJIL: Talk! — Blog of the European Journal of International Law, 2025. Disponível em: https://www.ejiltalk.org/anchoring-criminal-jurisdiction-at-sea-the-helsinki-district-courts-eagle-s-judgement-and-its-impact-for-the-protection-of-submarine-cables-and-pipelines/. Acesso em: 19 set. 2026.

### Defesa e cooperação regional

[20] NATO ALLIED MARITIME COMMAND. **NATO's Baltic Sentry steps up patrols in the Baltic Sea to safeguard Critical Undersea Infrastructure**. Northwood, 2025. Disponível em: https://mc.nato.int/media-centre/news/2025/nato-baltic-sentry-steps-up-patrols-in-the-baltic-sea-to-safeguard-critical-undersea-infrastructure. Acesso em: 19 set. 2026.

### Nota sobre as fontes

As referências [18] e [19] são, respectivamente, cobertura jornalística de veículo público e análise doutrinária em blog acadêmico especializado. Foram empregadas por ausência, até a data de acesso, de texto integral publicado das decisões do Tribunal Distrital e do Tribunal de Apelação de Helsinque em repositório de acesso aberto. Recomenda-se, para uso acadêmico formal, a substituição pelas decisões originais quando disponíveis. A autoria da entrada [19] deve ser conferida na fonte antes de citação formal.

---

*Artigo de natureza acadêmica e analítica, elaborado a partir de fontes públicas. Uma versão em inglês está disponível em [`English/Nordic_Arctic_Cables.md`](../English/Nordic_Arctic_Cables.md). Contribuições, correções e discussões são bem-vindas por meio de issues ou pull requests.*
