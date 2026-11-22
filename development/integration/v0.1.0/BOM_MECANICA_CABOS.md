# BOM mecânica e chicotes — estudo 0.1.0

Quantidades por CorePad. Complementa a [BOM eletrônica](../../hardware/v0.2.0/BOM.md). `RESERVA` significa que código de compra, material final, dimensão e/ou fornecedor ainda não estão fechados. O STEP não autoriza compra.

| Item | Qtd. | Descrição | Material/processo candidato | Estado |
|---|---:|---|---|---|
| ME-01 | 1 | Base isolante, 104 × 84 × 26 mm nominal | PA12 MJF para prova; PC+ABS injetado a avaliar para série | Geometria 3D preliminar; sem nervuras/fixações finais |
| ME-02 | 1 | Tampa 104 × 84 × 2,4 mm nominal | PC+ABS ou PA12 com aparência de fibra de carbono | Aparência aprovada; revestimento/processo não selecionado |
| ME-03 | 1 | Difusor inferior RGB | PC translúcido ou resina óptica a ensaiar | Continuidade geométrica; retenção e uniformidade não medidas |
| ME-04 | 9 | Keycap sem inscrição, 18,4 × 18,4 mm envelope | PBT/ABS a selecionar, acabamento carbono coerente | Reserva de volume; encaixe com Choc V2 não projetado |
| ME-05 | 1 | Botão camada | Plástico isolante a selecionar | Encaixe no tátil não definido |
| ME-06 | 1 | Botão gravação | Plástico isolante a selecionar | Encaixe no tátil não definido |
| ME-07 | 1 | Cursor fader | Plástico isolante a selecionar | Haste e curso do PTA1543 não medidos |
| ME-08 | 1 | Alavanca mudo | Plástico isolante a selecionar | Haste do DPDT não medida |
| ME-09 | 4 | Pés antiderrapantes | Silicone/EPDM + adesivo a selecionar | Posição, espessura, dureza e código pendentes |
| ME-10 | A definir | Parafusos, insertos, suportes das duas placas e retenção da tampa | Metais/insertos conforme amostra | **Não modelados**; furos de placa também faltam |
| ME-11 | A definir | Membranas/dutos de microfone e vedação de porta | Acústica a medir | **Não modelados**; necessários para gravação ambiental |
| CA-01 | 1 | Ligação UI–principal de 16 sinais | FFC ou flex, pitch/conectores a selecionar | Apenas envelope 8 × 0,3 mm e rota visual; pinagem lógica vem de J20 de bancada |
| CA-02 | 1 | Chicote da célula 1S: 2 vias de potência; NTC/conexão térmica a definir | Fio e terminal conforme célula protegida/charger | Só duas rotas visuais; bitola, comprimento, polaridade física e strain relief não fechados |
| CA-03 | A definir | Chicotes/flat adicionais para sensor biométrico e controles caso fora das PCBs | A selecionar após alocação de componentes | **Não modelados**; não assumir integração sem roteamento |
| PCB-01 | 1 | Principal FR4, 4 camadas, 98 × 78 × 1,6 mm | Stack-up/fabricante a definir | Contorno real KiCad, sem esquema/roteamento |
| PCB-02 | 1 | Interface final FR4, 2 camadas, 98 × 78 × 1,6 mm envelope | Stack-up/fabricante a definir | KiCad mecânico contém contorno/centros, **sem pads/trilhas**; bancada é distinta |

Para BOM de fabricação faltam códigos completos (MPN), alternativas aprovadas, desenhos de cada peça, arquivos de cobre, montagem, cotação e teste de primeiro artigo. A fibra de carbono é a **aparência** definida; um compósito estrutural condutivo não foi escolhido como material da tampa.
