# Eletrônica CorePad Beta 0.2.0

## Arquivos e limites

`CorePad_Interface_Bancada_v0.2.0.kicad_sch` contém esquema elétrico de conectores para testar nove teclas e controles externos. `CorePad_Interface_Bancada_v0.2.0.kicad_pcb` contém footprints e redes correspondentes. Os conectores J1–J9 recebem fios dos switches reais; **não são footprints dos Kailh Choc V2**. O PCB não foi roteado. Esta interface é um apoio de bancada e não substitui a placa superior do produto.

`CorePad_Principal_v0.2.0.kicad_pcb` contém contorno e footprint do STM32U5A5. O esquema pino a pino, passivos e redes da principal ainda precisam ser desenvolvidos. O estudo Alpha 0.1.0 permanece como origem da arquitetura, com os riscos registrados.

A [PCB UI de posicionamento mecânico](../ui_mechanical/v0.1.0/README.md) agora compartilha com o conjunto 3D o contorno e os centros dos controles. Ela **não** substitui esta interface elétrica de bancada, nem é ainda uma PCB de produto: não tem pads, footprints reais ou roteamento.

Todos os sinais da interface são referidos a GND e trabalham no domínio 3,3 V. Teclas usam pull-up no controlador e fecham contra GND. `MUTE_SENSE` é somente leitura da posição: o corte físico dos microfones permanece na placa principal. `FADER` recebe o cursor de um potenciômetro de 10 kohm entre 3V3 e GND, sujeito a filtro/proteção na principal. J14 alimenta a referência de bancada; conferir o manifesto antes de ligar.

## Recursos a reservar na principal

| Bloco | Interface necessária | Fechamento pendente |
|---|---|---|
| USB | OTG HS, D+/D−, VBUS sense, proteção | USB composto e orçamento de endpoints; CC integrado versus controlador externo |
| Cartão | SDMMC CLK/CMD/D0–D3 + detecção | Pinos/AF, resistores série, pull-ups e ESD |
| Codec | SAI RX/TX/BCLK/FS/MCLK + I2C | Relógio simultâneo, DMA, alimentação e filtragem |
| Segurança | I2C autenticado + enable | Provisionamento, TrustZone e política de depuração |
| Biometria | A definir com sensor seguro | Não aceitar resultado UART como autenticação de produção |
| Teclas | 9 GPIO | Sem matriz elétrica; 3 × 3 é disposição física |
| Auxiliares | 3 GPIO + ADC + detecção SD | Fader, camada, gravação e leitura de mudo |
| LEDs | 3 GPIO + indicador REC | Correntes e ótica |
| RGB | PWM/driver a selecionar + chave de carga | Ripple/ruído acústico, consumo e brilho |
| Alimentação | I2C, alertas, NTC, SWD/RESET | Corrente USB, célula, carga e partida com bateria esgotada |

Não atribuir números de pinos antes de conferir todas as funções alternativas na ficha da variante exata. As interfaces acima não constituem validação de coexistência.

## Fontes consultadas em 22/11/2026

- ST: https://www.st.com/en/microcontrollers-microprocessors/stm32u5a5zj.html
- ST, ficha da família/variante: https://www.st.com/resource/en/datasheet/stm32u5a5zj.pdf
- TI, codec: https://www.ti.com/product/TAC5112
- Kailh, switches: https://www.kailh.net/products/kailh-choc-v2-low-profile-switch-set
- Demais candidatos: fontes primárias no relatório Alpha 0.1.0, ainda exigindo reconferência por componente antes do esquema.

DRC e netlist ficam em `reports/`. Violações de conexão aberta são esperadas nesta revisão não roteada. Não gerar compra integral ou fabricação a partir dela.
