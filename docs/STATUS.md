# Estado do projeto

Atualizado em 22/11/2026.

O `docs/engineering/Rev_A/` contém um Caderno de Engenharia A3 com fontes verificadas, 65 páginas, prévias renderizadas e registro de pendências. Seu estado é **estudo de engenharia**; não há pacote liberado de fabricação, montagem ou teste de produção.

Repositório organizado em torno da Beta carbon. A linha Alpha, conceitos descartados e geradores duplicados foram movidos para `.old/`. O relatório de arquitetura ainda útil foi preservado no pacote eletrônico ativo. O README contém vistas do produto, renders KiCad e vistas das peças plásticas, com suas fontes e limitações de estágio.

A revisão visual 1.0.1 refina a trama de carbono, resina, texturas e luz de estúdio. A galeria compara RGB laranja, amarelo, verde, vermelho e azul na mesma câmera, em 2000 × 1700 pixels. A 1.0.0 permanece como fonte das vistas geométricas anteriores.

## Resumo executivo

O CorePad concluiu a fase de definição visual conceitual e iniciou a integração eletromecânica. A Beta 1.0.1 é a proposta visual atual: carcaça e tampa em estilo fibra de carbono, nenhuma linha verde superior e faixa RGB configurável somente na base. A linha Alpha permanece preservada como histórico. Existe um conjunto STEP preliminar com peças, placas, bateria e cabos propostos; ainda não existe uma placa funcional ou fabricável.

## Baselines vigentes

| Área | Baseline | Situação |
|---|---|---|
| Produto | Especificação 0.7 | Vigente; contém decisões e pendências explícitas |
| Visual/mecânica | Beta 1.0.1 | Carbono refinado e RGB em cinco cores; material, difusor e fabricação não validados |
| Eletrônica | 0.3.0 em development/hardware/ | UI com nove switches, FFC 24 vias e seis teclas roteadas; principal com footprints candidatos, sem esquema completo/roteamento |
| Firmware | Núcleo C11 inicial | Estados testados; drivers, USB, áudio e segurança pendentes |
| Aplicativo/configuração | Configurador desktop inicial | Editor JSON e simulador; transporte USB pendente |
| Conjunto eletromecânico | Integração 0.2.0 | STEP com as duas placas KiCad 0.3.0; choque de USB-C/microSD, P2 desalinhado e suportes ausentes |
| Protótipo físico | — | Não iniciado |

## Desenvolvimento integrado após escolha da Beta

O proprietário escolheu seguir com a Beta em fibra de carbono em 22/11/2026. A entrega em `development/` acrescenta um núcleo C11 com estados do cartão/camadas/RGB, compilado para Cortex-M33 e testado em host; um configurador desktop Python com importação/exportação JSON e simulador; um escritor RF64 de referência; um esquema KiCad de interface de bancada com 44 pinos conferidos contra a PCB; e cinco peças plásticas volumétricas em STL/Blender. A BOM por bloco está em `development/hardware/v0.2.0/BOM.md`.

A interface de bancada tem ERC limpo e 29 conexões ainda não roteadas. Ela usa chicotes para switches externos e não substitui a placa final. A principal ainda precisa de esquema completo. O firmware de dispositivo, transporte USB, drivers de áudio/cartão e segurança ainda não foram integrados. As peças mecânicas precisam de suportes, fixações, retenções e validação de componentes reais. Protótipo físico continua não iniciado.

A montagem `development/integration/v0.2.0/` atualiza o STEP com duas placas KiCad reais e 32 grupos. O choque nominal de volumes candidatos com a base é 9,828 mm³ no USB-C e 2,533 mm³ no microSD; o centro do jack P2 está 2,41 mm acima da abertura. As placas nuas não colidem, mas faltam suportes e furos. O cabo FFC 24 vias é uma reserva espacial, sem dobra validada. A UI tem seis trilhas de tecla, zero violações geométricas e 13 conexões abertas; a principal tem oito violações e oito conexões abertas entre pads já nomeados. O protocolo público tem quadro com ID/CRC32 validado somente no simulador.

Evidências e limites: `development/VALIDATION.md`. Próximo avanço: pinagem simultânea, seleção da biometria segura e bancada MCU + áudio + SD antes da liberação das placas finais.

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
- placas totalmente roteadas, ERC/DRC de produção ou Gerbers; somente seis sinais de tecla da UI têm trilhas piloto;
- firmware de teclado, áudio, armazenamento, segurança ou atualização;
- material e processo reais da carcaça, difusor físico validado, circuito e controle de software da faixa RGB;
- prova de autonomia, integridade de gravação longa ou transição segura Arquivos/Gravação;
- cadeia biométrica autenticada e implementação CTAP/FIDO2;
- empilhamento 3D com modelos certificados, fixações e tolerâncias de montagem; o conjunto preliminar usa volumes de reserva;
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

Para avançar além do estudo 3D, fechar modelos de fornecedor, pinagem simultânea e evidência de bancada para gravação microSD, áudio USB e consumo. Consulte `docs/ROADMAP.md` e o índice de liberação em `development/integration/v0.1.0/`.
