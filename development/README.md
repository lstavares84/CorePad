# CorePad Beta — desenvolvimento integrado 0.2.0

22/11/2026. A Beta em estilo fibra de carbono foi escolhida para seguir o desenvolvimento.

Esta entrega implementa a base de software e modelos de prototipagem. A placa principal permanece em engenharia: não existe ainda um produto completo que possa ser comprado, fabricado e usado com todas as funções.

| Entrega | Arquivo | Situação |
|---|---|---|
| Firmware portátil C11 | `firmware/corepad.c` | Estados de cartão, bloqueio de camada, RGB; testado em host e compilado para Cortex-M33 |
| Configurador desktop | `software/configurator.py` | Editor de 18 macros comuns e RGB; exportação JSON e simulador local |
| Protocolo | `software/device.py` | Contrato e validação de configuração; transporte USB físico pendente |
| Gravação RF64 | `software/rf64.py` | Escritor PCM de referência, testado com arquivo pequeno; não executa no MCU |
| Eletrônica KiCad | `hardware/v0.2.0/` | Esquema de bancada da interface e PCB com redes; principal com footprint MCU, sem esquema completo/roteamento |
| Peças plásticas | `mechanical/v0.1.0/` | Base, tampa, difusor e botões editáveis; STL para estudo de encaixe |
| BOM | `hardware/v0.2.0/BOM.md` | Lista por bloco com códigos candidatos e pendências; sem preço total fictício |
| Montagem 3D integrada | `integration/v0.1.0/` | STEP conjunto e peças, placa principal KiCad, volumes de reserva, cabos propostos, dois desenhos SVG e relatório de encaixe |
| PCB UI mecânica | `hardware/ui_mechanical/v0.1.0/` | Contorno KiCad e centros dos controles, sem pads ou trilhas |
| Enquadramento de mensagens | `software/wire_protocol.py` | Quadro com ID, limite de tamanho e CRC32 testado no simulador; ainda sem USB físico |

## Executar

Na raiz do repositório:

```sh
make -C development/firmware test arm
python3 -m unittest discover -s development/tests -v
python3 development/software/configurator.py
```

O configurador usa Python 3 e Tkinter. O simulador e os testes usam apenas a biblioteca padrão. O alvo ARM gera um objeto compilado; startup, linker, HAL, USB Audio/HID/MSC, FatFs, codec e CTAP ainda precisam ser integrados.

## Sequência de engenharia pendente

1. Fechar a tabela de funções alternativas/pinos do STM32U5A5ZJT6Q com SDMMC, SAI e USB simultâneos.
2. Ensaiar USB Audio + gravação contínua em microSD com kit de desenvolvimento; medir consumo e latência.
3. Selecionar o sensor biométrico seguro. O módulo serial 4750 continua limitado a ergonomia/bancada.
4. Fechar esquemas da principal, desacoplamentos, carga, áudio, proteção e pinagem das interligações.
5. Validar os footprints de catálogo, empilhamento, curso das teclas, conectores e bateria com peças/modelos reais.
6. Rotear, revisar ERC/DRC, montar protótipo e medir os requisitos de áudio e 30 horas.

O [dossiê de manufatura](integration/v0.1.0/LIBERACAO_MANUFATURA.md) identifica desenhos, BOM, modelos e testes ainda necessários. O [STEP integrado](integration/v0.1.0/CorePad_Beta_integrado_v0.1.0.step) é estudo dimensional, sem liberação de ferramental.

Não foi realizado ensaio de hardware nesta entrega. O relatório KiCad registra conexões ainda abertas. Não há Gerbers liberados.
