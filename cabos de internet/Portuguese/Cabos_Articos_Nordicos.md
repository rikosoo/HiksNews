# Cabos Submarinos no Ártico Nórdico: Clima, Geopolítica e a Resiliência da Infraestrutura Digital Crítica

## Resumo

Aproximadamente 99% do tráfego de dados intercontinental trafega por cabos submarinos de fibra óptica, o que torna essa camada física um ativo de infraestrutura crítica tão essencial quanto as redes de energia ou de transporte. Na região nórdica e ártica, essa infraestrutura opera sob uma condição singular: o mesmo aquecimento regional que viabiliza novas rotas transárticas — reduzindo a cobertura de gelo marinho e abrindo janelas de lançamento antes impraticáveis — é o que degrada as condições de instalação, ancoragem e reparo desses sistemas, por meio da perda de permafrost, da erosão costeira e da intensificação do tráfego marítimo. Este artigo analisa essa tensão. Primeiro, mapeia o cenário de cabos nórdicos e árticos, incluindo os projetos transárticos em desenvolvimento. Em seguida, examina o clima ártico como vetor de risco físico e o articula com o modelo de ameaça híbrida evidenciado pelos incidentes de Svalbard (2022) e do mar Báltico (2023–2024). Por fim, discute o arcabouço regulatório aplicável (NIS2, Diretiva CER, UNCLOS) e propõe eixos de resiliência: diversidade de rotas e de pontos de aterragem, monitoramento acústico distribuído, capacidade regional de reparo com classe de gelo e planejamento de infraestrutura informado por projeções climáticas. Argumenta-se que risco climático e risco adversarial não são agendas separadas na região, mas manifestações de um mesmo problema de resiliência.

---

## Palavras-chave

Cabos Submarinos, Infraestrutura Ártica, Proteção de Infraestrutura Crítica, Resiliência Climática, Região Nórdica, Ameaças Híbridas, Permafrost, Segurança Cibernética

---

## 1. Introdução

A percepção pública da internet é dominada por metáforas imateriais — nuvem, éter, sem fio. A realidade operacional é oposta: a conectividade intercontinental depende de um conjunto finito de cabos de fibra óptica assentados no leito oceânico, cada um com poucos centímetros de diâmetro, cuja destruição física interrompe serviços digitais em escala nacional. Estimativas amplamente citadas na literatura de telecomunicações indicam que cerca de 99% do tráfego internacional de dados percorre esses sistemas, com os enlaces por satélite funcionando como redundância de capacidade limitada, e não como substituto.

A região nórdica concentra três características que tornam esse tema particularmente relevante. Primeiro, há uma dependência estrutural elevada: Islândia, Ilhas Faroe, Groenlândia e Svalbard são territórios cuja conectividade total repousa sobre um número muito pequeno de cabos — em alguns casos, dois. Segundo, a região abriga uma densidade incomum de infraestrutura digital sensível, incluindo data centers de grande porte atraídos pelo clima frio e pela energia renovável barata, além de estações terrestres de satélite de importância científica e militar. Terceiro, o recuo do gelo marinho ártico transformou a região em objeto de projetos de rotas transárticas — notadamente Far North Fiber e Polar Connect — que prometem reduzir substancialmente a latência entre Ásia e Europa em relação às rotas via Suez.

Paralelamente, a sequência de incidentes ocorridos entre 2022 e 2024 no Ártico norueguês e no mar Báltico deslocou os cabos submarinos da categoria de ativo técnico para a de objeto de política de segurança. Este artigo parte dessa convergência e formula três perguntas de pesquisa:

1. De que modo as mudanças climáticas no Ártico alteram o perfil de risco físico da infraestrutura de cabos nórdica?
2. Como os riscos climáticos e os riscos adversariais interagem, em vez de se somarem de forma independente?
3. Quais estratégias de resiliência são aplicáveis a um ambiente em que a capacidade de reparo é geograficamente e sazonalmente restrita?

O estudo se estrutura como uma revisão documental e analítica, cujas limitações estão explicitadas na Seção 9.

---

## 2. O Cenário de Cabos Nórdicos e Árticos

### 2.1 Configuração atual

A infraestrutura de cabos da região pode ser organizada em quatro camadas.

**Enlaces do Atlântico Norte.** A Islândia é servida por um conjunto reduzido de sistemas: FARICE-1, em operação desde 2004, conectando o país às Ilhas Faroe e à Escócia; DANICE, desde 2009, com aterragem na Dinamarca; e IRIS, que entrou em serviço em 2023, estabelecendo uma rota direta para a Irlanda. A adição do IRIS foi motivada explicitamente por argumentos de redundância nacional, o que ilustra o reconhecimento estatal do problema.

**Enlaces árticos e insulares.** O Svalbard Undersea Cable System, composto por dois pares de fibras entre Longyearbyen e o continente norueguês, sustenta não apenas a população civil do arquipélago, mas também a transmissão de dados da estação de satélites SvalSat, que atende a operadores científicos e comerciais internacionais. A Groenlândia depende do Greenland Connect, em operação desde 2009, com uma configuração igualmente concentrada.

**Enlaces intranórdicos e bálticos.** O mar Báltico é atravessado por uma malha densa de cabos de telecomunicações e de energia que interconecta Finlândia, Suécia, Estônia, Lituânia, Polônia e Alemanha. Entre eles, o C-Lion1 (Helsinque–Rostock) e o BCS East-West Interlink (Lituânia–Suécia) ganharam notoriedade pelos danos sofridos em 2024. A característica geográfica determinante aqui é a profundidade: o Báltico é um mar raso, o que coloca os cabos ao alcance de âncoras de navios comerciais em grande parte de seu traçado.

**Rotas transárticas em desenvolvimento.** O projeto Far North Fiber propõe conectar Japão e Europa atravessando a Passagem Noroeste, com aterragens previstas no Alasca, no Canadá ártico, na Groenlândia, na Islândia, na Noruega, na Finlândia e na Irlanda. O Polar Connect, conduzido no âmbito da NORDUnet e de redes acadêmicas nórdicas, estuda uma rota através do Oceano Ártico central. Ambos derivam sua viabilidade das condições de gelo alteradas pelo aquecimento regional.

### 2.2 Concentração e pontos de estrangulamento

Do ponto de vista de proteção de infraestrutura crítica, o traço mais relevante desse cenário não é o número de cabos, mas a distribuição da dependência. Um território servido por dois cabos possui, na prática, tolerância a uma única falha. Quando ambos compartilham corredor geográfico, estação de aterragem ou backhaul terrestre, mesmo essa tolerância é nominal: um evento único pode comprometer os dois caminhos.

As estações de aterragem merecem atenção específica. São instalações terrestres, fixas, publicamente localizáveis e frequentemente situadas em áreas costeiras remotas com vigilância limitada. Concentram, em um ponto único, o equipamento de terminação óptica, a alimentação elétrica dos repetidores submarinos e a interconexão com a rede terrestre. No contexto ártico, acumulam ainda uma vulnerabilidade adicional, tratada na seção seguinte: muitas estão assentadas sobre terreno cuja estabilidade geotécnica está mudando.

---

## 3. O Clima Ártico como Vetor de Risco Físico

O Ártico aquece a uma taxa várias vezes superior à média global, fenômeno documentado na literatura climatológica como amplificação ártica. As consequências para a infraestrutura de cabos se distribuem em cinco mecanismos distintos.

### 3.1 Recuo do gelo marinho: habilitação e exposição

A extensão mínima anual do gelo marinho ártico, medida em setembro, apresenta tendência de declínio consistente ao longo das últimas quatro décadas. Para a indústria de cabos, o efeito primário é habilitador: janelas de navegação mais longas permitem operações de lançamento em rotas antes inacessíveis, o que é precondição para projetos como o Far North Fiber.

O efeito secundário, porém, é de exposição. Águas navegáveis atraem tráfego marítimo comercial, pesqueiro e turístico. A causa dominante de falhas em cabos submarinos em escala global não é sabotagem nem desastre natural, mas atividade humana rotineira — âncoras arrastadas e redes de pesca de fundo. Um Ártico navegável é, por construção, um Ártico onde essa causa dominante passa a operar. A redução do gelo não elimina o risco de gelo: icebergs à deriva e o sulcamento do leito marinho por quilhas de gelo (*ice keel scouring*) continuam representando ameaças em águas rasas costeiras, e a mobilidade aumentada do gelo pode tornar esses eventos menos previsíveis.

### 3.2 Degradação do permafrost sob instalações terrestres

Este é o mecanismo de maior relevância para as estações de aterragem e para o backhaul terrestre. O degelo do permafrost reduz a capacidade de suporte do solo, provoca recalques diferenciais e compromete fundações dimensionadas sob a premissa de terreno permanentemente congelado. Hjort et al. (2018), em estudo publicado na *Nature Communications*, estimaram que uma fração majoritária da infraestrutura construída no domínio do permafrost ártico — da ordem de 70% — situa-se em áreas com risco elevado de dano associado ao degelo até meados do século.

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

### 4.1 Incidentes de referência

**Svalbard, janeiro de 2022.** Um dos dois cabos do sistema de Svalbard sofreu dano em trecho de águas profundas. O enlace remanescente manteve a conectividade do arquipélago, o que demonstrou o valor da redundância existente — e, simultaneamente, o fato de que o sistema operou, durante o período de reparo, sem qualquer margem adicional. A investigação conduzida pelas autoridades norueguesas apontou atividade humana como causa provável, sem que se chegasse a uma atribuição conclusiva. A ausência de atribuição é, em si, um achado analítico relevante.

**Balticconnector e cabos associados, outubro de 2023.** O gasoduto Balticconnector, entre Finlândia e Estônia, e cabos de telecomunicações próximos sofreram danos simultâneos. A investigação finlandesa concentrou-se no arrasto de âncora por um navio comercial.

**Mar Báltico, novembro de 2024.** Os cabos BCS East-West Interlink (Lituânia–Suécia) e C-Lion1 (Finlândia–Alemanha) foram danificados em intervalo de aproximadamente 24 horas, em um padrão consistente com arrasto de âncora ao longo de uma mesma rota de navegação.

**Estlink 2 e cabos adjacentes, dezembro de 2024.** O cabo de energia Estlink 2, entre Finlândia e Estônia, e diversos cabos de telecomunicações foram danificados. As autoridades finlandesas detiveram e investigaram um navio-tanque suspeito de arrasto de âncora, marcando uma inflexão na postura de aplicação da lei na região.

O padrão comum a esses casos é significativo para a análise de risco: o mecanismo físico do dano — uma âncora arrastada no leito — é idêntico ao de um acidente marítimo corriqueiro. Essa equivalência é precisamente o que torna a atribuição difícil e o que, na literatura de segurança, caracteriza a ação abaixo do limiar do conflito armado.

---

## 5. Modelo de Ameaça: Natural, Acidental e Adversarial

A prática convencional separa a análise de risco natural da análise de risco de segurança. Para cabos árticos nórdicos, essa separação produz avaliações incompletas, porque os três tipos de origem convergem sobre o mesmo pequeno conjunto de pontos de falha e, em parte, sobre o mesmo mecanismo físico.

| Origem | Mecanismo típico | Frequência relativa | Tempo de reparo | Atribuição |
|---|---|---|---|---|
| Natural — geotécnica | Degelo de permafrost, erosão costeira, deslizamento submarino | Baixa por evento, crescente na tendência | Longo (obra civil) | Não aplicável |
| Natural — gelo | Sulcamento por quilha de gelo, iceberg à deriva | Baixa a moderada, sazonal | Longo (restrição de acesso) | Não aplicável |
| Acidental — humana | Âncora, rede de pesca de fundo | Alta (causa dominante global) | Médio, restrito por janela | Geralmente possível |
| Adversarial — híbrida | Arrasto deliberado de âncora, intervenção subaquática | Baixa, concentrada geograficamente | Médio a longo | Difícil e frequentemente inconclusiva |
| Adversarial — cibernética | Comprometimento de sistemas de gerenciamento da rede e da estação de aterragem | Não pública | Variável | Difícil |

Três observações decorrem dessa estrutura.

Primeiro, **a ambiguidade é uma propriedade do domínio, não uma falha da investigação.** Quando o mesmo ato físico pode ser acidente ou agressão, a resposta institucional é estruturalmente lenta, e um adversário racional obtém efeito com risco de atribuição reduzido.

Segundo, **o clima altera a linha de base contra a qual a anomalia é medida.** Um mar mais navegável produz mais incidentes acidentais genuínos. Isso eleva o ruído de fundo, tornando mais difícil distinguir o evento deliberado — o que constitui uma interação entre o vetor climático e o vetor adversarial, e não uma mera coincidência temporal.

Terceiro, **a dimensão cibernética não deve ser omitida.** A discussão pública concentra-se no dano físico, mas os sistemas de gerenciamento de elementos de rede, os sistemas de alimentação (*power feed equipment*) e os controles de acesso das estações de aterragem constituem superfície de ataque lógica. Aplicam-se aqui os mesmos princípios de defesa em profundidade, segmentação e gestão de identidade discutidos para ambientes de infraestrutura crítica em nuvem e para convergência TI/TO.

---

## 6. Governança e Arcabouço Regulatório

### 6.1 Nível europeu

A Diretiva NIS2 (Diretiva (UE) 2022/2555) amplia o escopo de entidades sujeitas a requisitos de gestão de risco cibernético e de notificação de incidentes, incluindo explicitamente a infraestrutura digital. A Diretiva CER (Diretiva (UE) 2022/2557), sobre a resiliência de entidades críticas, trata da dimensão física e exige que os Estados-membros identifiquem entidades críticas e conduzam avaliações de risco que contemplem, entre outros fatores, riscos naturais e mudanças climáticas. A leitura conjunta das duas diretivas é o instrumento mais direto para tratar a convergência analisada neste artigo.

A aplicabilidade na região não é uniforme. Dinamarca, Suécia e Finlândia são Estados-membros da União Europeia. Noruega e Islândia integram o Espaço Econômico Europeu, com incorporação por mecanismo próprio e cronograma distinto. A Groenlândia e as Ilhas Faroe possuem estatutos específicos. O resultado é um mosaico regulatório sobre uma infraestrutura que, por natureza, é transfronteiriça.

### 6.2 Direito internacional do mar

A Convenção das Nações Unidas sobre o Direito do Mar (UNCLOS) trata da proteção de cabos submarinos em seus artigos 113 a 115, obrigando os Estados a tipificar como infração o dano doloso ou por negligência culposa a cabo submarino causado por navio de sua bandeira. O regime apresenta três fragilidades operacionais reconhecidas na literatura: depende da jurisdição do Estado de bandeira, cuja cooperação é incerta; foi concebido para o acidente e não para a ação estatal deliberada; e oferece instrumentos limitados de interdição em alto-mar. Os eventos bálticos de 2024, em que autoridades costeiras adotaram medidas mais assertivas sobre navios suspeitos, indicam um teste prático dos limites desse regime.

### 6.3 Dimensão de defesa e cooperação regional

A resposta institucional recente inclui iniciativas de vigilância marítima dedicadas à proteção de infraestrutura submarina, entre elas a operação Nordic Warden, conduzida no âmbito da Joint Expeditionary Force, e a atividade Baltic Sentry, iniciada pela OTAN em janeiro de 2025 após a série de incidentes. A adesão de Finlândia e Suécia à OTAN alterou de forma substantiva a arquitetura de segurança regional no período analisado.

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

---

## 8. Discussão

A tensão central identificada neste artigo pode ser formulada de maneira direta: **o degelo ártico é simultaneamente a condição de possibilidade e a principal fonte de risco físico das novas rotas de cabo na região.** As mesmas condições que tornam economicamente atrativa uma rota transártica — menos gelo, janelas de navegação mais longas — produzem terreno de aterragem instável, costas em erosão e tráfego marítimo mais denso sobre traçados de cabo. Tratar oportunidade e risco como agendas separadas, conduzidas por equipes distintas, é o erro analítico que este artigo procura evidenciar.

Uma segunda conclusão diz respeito à relação entre clima e ameaça híbrida. Não se sustenta aqui qualquer relação causal entre mudança climática e ação adversarial. O que se argumenta é mais específico e, do ponto de vista de defesa, mais consequente: o aumento do tráfego marítimo legítimo eleva a taxa de incidentes acidentais genuínos, o que amplia o ruído de fundo contra o qual um evento deliberado precisaria ser distinguido. Em um domínio onde o mecanismo físico do acidente e o da agressão são indistinguíveis, elevar o ruído de fundo é, funcionalmente, degradar a capacidade de atribuição.

Uma terceira observação refere-se à assimetria entre custo de ataque e custo de defesa. Danificar um cabo exige meios modestos e amplamente disponíveis. Protegê-lo exige vigilância marítima contínua sobre áreas extensas, capacidade naval de reparo e redundância cara. Essa assimetria não é eliminável por meios técnicos; ela desloca o peso da resposta para o projeto resiliente, para a detecção precoce e para a dissuasão por meio de atribuição e consequência jurídica crível — o que confere à discussão regulatória da Seção 6 um peso operacional, e não meramente formal.

---

## 9. Limitações

Este trabalho constitui uma revisão documental e analítica, baseada em literatura acadêmica, documentos regulatórios públicos e relatos de incidentes de domínio público. Não incorpora dados operacionais proprietários de operadores de cabo, cuja divulgação é restrita por razões comerciais e de segurança. As investigações referentes aos incidentes de 2022 a 2024 encontram-se, em parte, sem conclusão pública definitiva, de modo que as caracterizações apresentadas na Seção 4 devem ser lidas como descrição do que é conhecido publicamente, e não como atribuição. As estimativas quantitativas citadas — participação dos cabos no tráfego intercontinental, proporção de infraestrutura ártica em risco de degelo — provêm das fontes indicadas e carregam as incertezas metodológicas próprias a elas. Por fim, a situação regulatória e de segurança regional descrita reflete o estado dos fatos até a data de redação e é objeto de evolução rápida.

---

## 10. Conclusão

A infraestrutura de cabos submarinos do Ártico nórdico ocupa uma posição incomum na análise de infraestrutura crítica: é o ponto em que risco climático, risco acidental e ameaça geopolítica incidem sobre o mesmo ativo físico, com os mesmos modos de falha e o mesmo conjunto restrito de opções de reparo. A resposta adequada não é conduzir três análises de risco paralelas, mas uma única análise de resiliência que reconheça a interação entre esses vetores.

As prioridades que emergem da análise são quatro: diversidade estrutural avaliada por modo de falha comum e não por contagem de cabos; detecção precoce por sensoriamento na própria fibra, integrada a dados de tráfego marítimo; capacidade regional de reparo com classe de gelo, por ser o tempo de indisponibilidade a variável que converte falha em crise; e projeto de infraestrutura que adote projeções climáticas como parâmetro de entrada, dada a incompatibilidade entre uma vida útil de 25 anos e um ambiente não estacionário.

A camada física da internet foi, por muito tempo, tratada como um problema resolvido de engenharia. No Ártico nórdico, ela voltou a ser uma questão aberta de política pública, de direito internacional e de segurança.

---

## Referências

As referências abaixo indicam as fontes e categorias de material que fundamentam a análise. Recomenda-se a consulta às versões mais recentes, dada a rápida evolução do tema.

1. Hjort, J. et al. *Degrading permafrost puts Arctic infrastructure at risk by mid-century.* Nature Communications, v. 9, 2018.
2. TeleGeography. *Submarine Cable Map* e relatórios associados sobre tráfego internacional e frota de navios-cabo.
3. International Cable Protection Committee (ICPC). Publicações sobre causas de falha em cabos submarinos e boas práticas de proteção.
4. União Europeia. Diretiva (UE) 2022/2555 (NIS2), relativa a medidas para um elevado nível comum de cibersegurança na União.
5. União Europeia. Diretiva (UE) 2022/2557 (CER), relativa à resiliência das entidades críticas.
6. Organização das Nações Unidas. Convenção das Nações Unidas sobre o Direito do Mar (UNCLOS), artigos 113 a 115.
7. National Snow and Ice Data Center (NSIDC). Séries de extensão de gelo marinho ártico.
8. Arctic Monitoring and Assessment Programme (AMAP). Relatórios sobre amplificação ártica e impactos em infraestrutura.
9. Relatos públicos e comunicados oficiais referentes aos incidentes de Svalbard (2022), Balticconnector (2023) e mar Báltico (2024).
10. Documentação pública dos projetos Far North Fiber e Polar Connect (NORDUnet).

---

*Artigo de natureza acadêmica e analítica, elaborado a partir de fontes públicas. Contribuições, correções e discussões são bem-vindas por meio de issues ou pull requests.*
