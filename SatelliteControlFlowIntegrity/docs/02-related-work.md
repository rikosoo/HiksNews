# 02 — Trabalhos relacionados

## Eixos de literatura a cobrir

### 1. Control-Flow Integrity clássica
- Abadi et al. (2005) — formulação original de CFI.
- CFI de granularidade fina vs. grossa; custo de instrumentação.
- Limitações em alvos sem MMU.

### 2. CFI e detecção baseada em trace de hardware
- **SHERLOC** — detecção de violação de fluxo de controle em firmware embarcado usando trace de hardware; base metodológica deste trabalho.
- ARM CoreSight **ETM** / **MTB**: o que cada um expõe, custo em pinos e memória.
- Trabalhos correlatos que usam trace para atestação de execução.

### 3. Segurança de RTOS embarcado
- Isolamento por MPU no FreeRTOS; o que ele cobre e o que não cobre.
- Ataques entre tarefas e corrupção de fila/heap.

### 4. Segurança de sistemas espaciais
- MITRE **SPARTA** — táticas e técnicas específicas do domínio espacial; mapeamento das técnicas cobertas pelo nosso detector.
- CCSDS — telecomando/telemetria e camada de segurança (SDLS).
- NIST IR 8270 e SP 800-53 aplicados a operações espaciais.
- Incidentes públicos (Viasat 2022 e correlatos) como evidência de relevância.

### 5. Lacuna identificada
Trace-based CFI é estudada em IoT genérica; **não há avaliação sob as restrições
específicas de voo** — orçamento de energia, tolerância a radiação, janela de
contato e irreversibilidade da resposta. É essa lacuna que o trabalho ocupa.

> TODO: fechar cada item com citação completa (autor, veículo, ano, DOI).
