# Estado do projeto

Atualizado em 22/11/2026.

## Resumo executivo

O CorePad concluiu a fase de definição visual conceitual e iniciou a exploração eletrônica. A Beta 1.0.0 é a proposta visual atual: carcaça e tampa em estilo fibra de carbono, nenhuma linha verde superior e faixa RGB configurável somente na base. A linha Alpha permanece preservada como histórico. A revisão eletrônica 0.1.0 organiza arquitetura, candidatos de componentes, orçamento de energia, estudos de posicionamento e plano de validação, mas ainda não existe uma placa funcional ou fabricável.

## Baselines vigentes

| Área | Baseline | Situação |
|---|---|---|
| Produto | Especificação 0.7 | Vigente; contém decisões e pendências explícitas |
| Visual/mecânica | Beta 1.0.0 | Carbono e RGB modelados; material, difusor e fabricação não validados |
| Eletrônica | 0.1.0 | Estudo preliminar; sem esquema completo ou trilhas |
| Firmware | — | Não iniciado |
| Aplicativo/configuração | — | Não iniciado |
| Protótipo físico | — | Não iniciado |

## O que já existe

- nove teclas 3 × 3, seletor de camadas, três LEDs, botão de gravação, biometria e controles representados no Blender;
- Beta 1.0.0 com estilo fibra de carbono, sem filete superior, faixa RGB inferior, controles de cor/brilho/liga-desliga e vistas verde/azul;
- vistas de revisão, geradores Python e validações JSON;
- proposta de arquitetura com STM32U5A5, áudio dedicado, microSD, elemento seguro, bateria e carga;
- BOM preliminar, estimativa de autonomia, interligações funcionais e reservas de posicionamento KiCad;
- critérios de teste para autonomia, cartão, áudio, mudo, USB, segurança e mecânica.

## O que ainda não existe

- esquema pino a pino e seleção completa de passivos/proteções;
- pinagem simultânea comprovada para todos os periféricos;
- placa roteada, ERC/DRC de produção ou Gerbers;
- firmware de teclado, áudio, armazenamento, segurança ou atualização;
- material e processo reais da carcaça, difusor físico validado, circuito e controle de software da faixa RGB;
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
| 7 | faixa RGB reduzir a autonomia ou contaminar áudio/EMC | Orçamento por brilho, acionamento adequado e testes com gravação ativa |

## Próxima decisão de avanço

A revisão 0.2.0 só deve começar depois de fechar a matriz de recursos/pinos e de obter evidência inicial para os três maiores riscos de bancada: gravação contínua no microSD, áudio USB simultâneo e consumo. Consulte `docs/ROADMAP.md`.
