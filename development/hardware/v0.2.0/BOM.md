# BOM CorePad Beta 0.2.0

Quantidades por aparelho; candidatos herdados do estudo 0.1.0, acrescidos do RGB e das peças mecânicas. Sem cotação, sem custo total e sem liberação de compra. A BOM de produção depende dos esquemas completos. A placa de bancada usa seus próprios conectores ao final.

| Ref. | Qtd. | Função / candidato | Situação e pendência |
|---|---:|---|---|
| U1 | 1 | ST STM32U5A5ZJT6Q | Principal candidato; pinagem/USB/DMA simultâneos pendentes |
| U2 | 1 | TI TAC5112IRGER | Codec candidato; circuito analógico e relógios pendentes |
| U3 | 1 | TI TPA6132A2RTER | Amplificador P2 candidato; ganho/acoplamento pendentes |
| MIC1–2 | 2 | Infineon IM73A135V01XTSA1 | Cápsulas candidatas; dutos, membranas e ruído pendentes |
| U4–5 | 2 | TI TS5A23157, sufixo a fechar | Mudo por hardware; transitórios e polarização pendentes |
| U6 | 1 | NXP SE050C2HQ1/Z01SD | Proteção criptográfica candidata; provisionamento pendente |
| BIO1 | 1 | Sensor seguro a selecionar | Adafruit 4750 serve somente para bancada/ergonomia |
| U7 | 1 | TI BQ25622, sufixo a fechar | Carga/power-path; passivos, NTC e corrente pendentes |
| U8 | 1 | TI TPS63070RNMR | 3V3 candidato; indutor e pico SD pendentes |
| U9 | 1 | TI TPS7A20 2,8 V, sufixo a fechar | Alimentação exclusiva dos microfones |
| U10 | 1 | ADI MAX17048, sufixo a fechar | Medição de bateria; célula/calibração pendentes |
| U11–12 | 2 | TI TPS22918DBVR | Domínios desligáveis; alimentação parasita a revisar |
| U13 | 0 ou 1 | TUSB320 | Comparar uso de CC integrado no STM32; não comprar duplicado |
| ESD USB | 1 | TI TPD2EUSB30, sufixo a fechar | Clamping/capacitância e VBUS/CC ainda a revisar |
| J_USB | 1 | GCT USB4105-GF-A | Candidato; altura/ancoragem pendentes |
| J_SD | 1 | Hirose DM3AT-SF-PEJM5 | Candidato; alinhamento e tolerâncias pendentes |
| J_P2 | 1 | Same Sky SJ-3523-SMT-TR | Saída estéreo; sem microfone de headset |
| SW1–9 | 9 | Kailh CPG135301D01 Choc V2 Red | Confirmar desenho de soldagem e keycaps próprios |
| SW_CAM/REC | 2 | Tátil baixo perfil, a selecionar | Superfície visual não define corpo de catálogo |
| SW_MUTE | 1 | C&K 7201 DPDT ON-ON, código completo a fechar | Haste, contatos e altura pendentes |
| RV1 | 1 | Bourns PTA1543, 10 kohm linear | Código completo/haste conforme empilhamento |
| LED_CAM | 3 | Verde 0603 de alta eficiência, a selecionar | Corrente, resistor e guia óptico pendentes |
| LED_REC | 1 | Indicador dedicado, a selecionar | Aprovação de integração visual e circuito pendentes |
| RGB1 | A definir | LEDs RGB + driver ou módulo RGB | Topologia, quantidade, corrente e PWM pendentes |
| RGB_SW | 1 | Chave de alimentação RGB, a selecionar | Corte total na gravação autônoma como proposta inicial |
| BAT1 | 1 | Li-ion 1S protegida, referência 2.000 mAh | Dimensão 60 × 36 × 7 mm de estudo; célula final pendente |
| NTC1 | 1 | NTC conforme célula e carregador | Curva e rede TS pendentes |
| CARD1 | 1 | microSDXC até 256 GB | Homologar consumo e latência; não incluso na memória secreta |
| R/C/L/XTAL | A definir | Passivos, indutores e relógios | Lista incompleta até fechar esquema pino a pino |
| PCB_MAIN | 1 | FR4 4 camadas | Stack-up, esquema e roteamento pendentes |
| PCB_UI | 1 | FR4 2 camadas | Contorno/centros no KiCad mecânico 0.1.0; placa elétrica final distinta da interface de bancada |
| CASE_BASE | 1 | Base plástica isolante | STL de estudo; proposta PA12/ABS para protótipo |
| CASE_TOP | 1 | Tampa plástica com acabamento carbono | Revestimento proposto; processo final em aberto |
| DIFFUSER | 1 | Difusor translúcido da base | STL de estudo; testar uniformidade óptica |
| BTN_LAYER/REC | 2 | Botões plásticos | STL; interface com tátil real pendente |
| FEET | 4 | Pés de borracha | Espessura/adesivo a selecionar |
| FIX/DUCT | A definir | Fixações, insertos, dutos e membranas | Medição e tolerâncias pendentes |

## Componentes adicionais da interface de bancada

| Ref. | Qtd. | Componente | Observação |
|---|---:|---|---|
| J1–J14 | 14 | Pin header 1 × 2, passo 2,54 mm | Footprint KiCad; fabricante/código a escolher |
| J20 | 1 | Pin header 2 × 8, passo 2,54 mm | Saída do chicote; conferir orientação em `interface_pins.json` |

Fontes: códigos e links em `ARCHITECTURE_REFERENCE.md`, preservado nesta pasta a partir do estudo inicial; ST, TI TAC5112 e Kailh reconferidos em 22/11/2026. Estoque, preço, equivalentes e demais fichas ainda não foram revalidados nesta revisão.
