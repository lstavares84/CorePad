# Estado do projeto

Atualizado em 22/11/2026.

## Resumo executivo

O CorePad concluiu a fase de definição visual conceitual e iniciou a exploração eletrônica. A Alpha 1.2.0 é a referência visual aprovada. A revisão eletrônica 0.1.0 organiza arquitetura, candidatos de componentes, orçamento de energia, estudos de posicionamento e plano de validação, mas ainda não existe uma placa funcional ou fabricável.

## Baselines vigentes

| Área | Baseline | Situação |
|---|---|---|
| Produto | Especificação 0.5 | Vigente; contém decisões e pendências explícitas |
| Visual/mecânica | Alpha 1.2.0 | Aparência aprovada; encaixe e fabricação não validados |
| Eletrônica | 0.1.0 | Estudo preliminar; sem esquema completo ou trilhas |
| Firmware | — | Não iniciado |
| Aplicativo/configuração | — | Não iniciado |
| Protótipo físico | — | Não iniciado |

## O que já existe

- nove teclas 3 × 3, seletor de camadas, três LEDs, botão de gravação, biometria e controles representados no Blender;
- vistas de revisão, geradores Python e validações JSON;
- proposta de arquitetura com STM32U5A5, áudio dedicado, microSD, elemento seguro, bateria e carga;
- BOM preliminar, estimativa de autonomia, interligações funcionais e reservas de posicionamento KiCad;
- critérios de teste para autonomia, cartão, áudio, mudo, USB, segurança e mecânica.

## O que ainda não existe

- esquema pino a pino e seleção completa de passivos/proteções;
- pinagem simultânea comprovada para todos os periféricos;
- placa roteada, ERC/DRC de produção ou Gerbers;
- firmware de teclado, áudio, armazenamento, segurança ou atualização;
- prova de autonomia, integridade de gravação longa ou transição segura Arquivos/Gravação;
- cadeia biométrica autenticada e implementação CTAP/FIDO2;
- empilhamento 3D com modelos certificados e tolerâncias de montagem;
- protótipo, ensaios acústicos, térmicos, EMC/ESD ou de segurança.

## Riscos prioritários

| Prioridade | Risco | Evidência necessária para reduzir |
|---:|---|---|
| 1 | Interfaces/pinos do MCU não acomodarem o USB composto, áudio e SDMMC simultâneos | Matriz de pinagem revisada e prova em kit de desenvolvimento |
| 2 | microSD exceder consumo ou pausar escritas, quebrando 30 h e gravação contínua | Medições com modelos de cartão e arquivo longo recuperável |
| 3 | sensor biométrico de bancada ser simulável e liberar credenciais | Sensor/cadeia autenticada e modelo de ameaça revisado |
| 4 | mudo não interromper fisicamente toda a captação | Esquema fail-safe e medição com firmware travado |
| 5 | peças reais não caberem no volume visual | Empilhamento 3D com modelos dimensionais e tolerâncias |
| 6 | arquivo híbrido longo ser impraticável para transcrição | Teste RF64/exportação e fluxo de processamento definido |

## Próxima decisão de avanço

A revisão 0.2.0 só deve começar depois de fechar a matriz de recursos/pinos e de obter evidência inicial para os três maiores riscos de bancada: gravação contínua no microSD, áudio USB simultâneo e consumo. Consulte `docs/ROADMAP.md`.
