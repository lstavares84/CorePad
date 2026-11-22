# BOM de posicionamento — mudanças na revisão 0.3.0

A [BOM por bloco 0.2.0](../v0.2.0/BOM.md) permanece o inventário funcional. Esta tabela identifica somente o que entrou ou mudou nos footprints e no encaixe 0.3.0. **Não é BOM de compra**: faltam passivos, proteção, alimentação, componentes UI, modelos mecânicos e circuito completo.

| Ref. | Qtd. por unidade | Candidato | Estado e decisão pendente |
|---|---:|---|---|
| SW1–SW9 | 9 | Kailh CPG135301D01 Choc V2 Red | Footprint piloto colocado; testar solda, orientação de terminais e keycap em amostra |
| J_UI (principal + UI) | 2 | Amphenol F32R-1A7H1-11024 | 24 vias, passo 0,5 mm, altura 2 mm; travas, face de contato e montagem a conferir |
| FFC24 | 1 | Cabo flexível 24 vias / 0,5 mm, MPN aberto | Comprimento, orientação A/B, espessura 0,3 mm e raio de dobra a definir |
| U1 | 1 | ST STM32U5A5ZJT6Q | Footprint LQFP-144 20 × 20 mm; pinagem ainda sem prova |
| U2 | 1 | TI TAC5112IRGER | Footprint genérico VQFN-24 4 × 4 mm; EP/pads a comparar com desenho TI |
| U3 | 1 | TI TPA6132A2RTER | Footprint WQFN-16 3 × 3 mm; EP/pads a conferir |
| J_USB | 1 | GCT USB4105-GF-A | Footprint com 4 violações de isolamento de furo; caixa colide |
| J_SD | 1 | Hirose DM3AT-SF-PEJM5 | Footprint colocado; colide com base e serigrafia passa borda |
| J_P2 | 1 | Same Sky SJ-3523-SMT-TR | Footprint colocado; centro do plug +2,41 mm frente à abertura |
| U7 (futuro) | 1 | TI BQ25622, sufixo aberto | Encapsulamento real WQFN-HR **18 pinos**, não 24; footprint não colocado |
| SW_MUTE (futuro) | 1 | Código aberto | C&K 7201SYZQE da BOM antiga não foi aceito mecanicamente; escolher chave compacta após ensaio |
| RV1 (futuro) | 1 | Bourns PTA1543, variante aberta | Corpo de 30 mm sob fenda de 26,5 mm; curso/haste a comprovar |
| LED1–4 (futuro) | 4 | MPN aberto | Três LEDs de camada + gravação na UI; saídas reservadas nos pinos FFC 21–24 |
| BIO1 (futuro) | 1 | Sensor seguro a selecionar | UART TX/RX e reset reservados; protocolo autenticado e volume real pendentes |
| RGB da base (futuro) | A definir | LEDs/driver a selecionar | Alimentação e controle permanecem na placa principal/base, fora do FFC |

Quantidades de componentes não colocados são necessidades funcionais, não ordens de montagem. Conferir folhas de dados e disponibilidade novamente antes de selecionar fornecedores.
