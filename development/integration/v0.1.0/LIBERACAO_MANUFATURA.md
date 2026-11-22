# Dossiê de manufatura — índice e critérios de liberação

**Situação em 22/11/2026: estudo de integração, sem liberação de fabricação.** A montagem STEP e os SVG são início do dossiê, não um conjunto completo para ferramental ou PCBA.

| Entregável | Estado atual | Fechamento necessário |
|---|---|---|
| Requisitos e controle de versão | Especificação, decisões Beta e revisão dos artefatos | Matriz requisito → verificação e assinatura de revisão |
| CAD 3D de conjunto | STEP com 21 grupos, incluídos PCB principal e cabos de reserva | Substituir volumes por STEP de fornecedor; fixações, suportes, retenção, raios de cabo; auditoria de colisão completa |
| Desenhos técnicos | Planta e seção preliminares em SVG | Desenho individual de cada peça com material, acabamento, datum, tolerâncias, GD&T, rugosidade e cotas críticas |
| Materiais e processo | PA12/PC+ABS e difusor como candidatos | Testes de acabamento carbono, óptica RGB, resistência, temperatura, inflamabilidade e dielétrico |
| Esquema principal | Somente PCB com footprint MCU | Arquitetura elétrica pino a pino, áudio, segurança, carga, biometria, RGB e proteção; ERC limpo |
| PCB principal | Contorno 4 camadas, sem trilhas | Stack-up, impedâncias USB/áudio, roteamento, DRC, Gerber/ODB++, furação, pick-and-place, assembly drawing |
| PCB UI | KiCad mecânico com contorno/centros, sem pads; bancada 0.2.0 é distinta | Footprints reais de Choc V2 e controles, interligação, furos/fixação, esquema, ERC/DRC e fabricação |
| Cabos | FFC 16 vias e bateria 2 vias em posição indicativa | Especificação por conector, pinagem, comprimentos, raio mínimo, acabamento e teste de continuidade |
| BOM total/AVL | Candidatos eletrônicos e mecânicos separados | MPN completo, fabricante, quantidade, vida útil, alternativos qualificados e aprovação de compras |
| Firmware/software | Núcleo de estados, simulador, RF64 e enquadramento de mensagens | USB real, drivers, armazenamento, áudio, segurança/CTAP, atualização, produção e testes de sistema |
| Qualificação | Testes de software e geometria nominal | Protótipos, inspeção dimensional, áudio, bateria 30 h, ESD/EMC, segurança elétrica e repetibilidade de montagem |

## Pendente que governa o próximo desenho

1. Medir os modelos reais de switches Choc V2/keycaps, portas USB-C/P2/SD, fader, DPDT, bateria protegida e sensor biométrico seguro.
2. Definir a placa UI de produto e o conector para 16 sinais; J20 de bancada tem passo 2,54 mm e **não é** o FFC mostrado no 3D.
3. Fechar furos, bosses e fixadores antes de dimensionar plástico para molde. A folga de 1 mm entre borda das placas e a parede interna é apenas nominal.
4. Rever o empilhamento após componentes reais: existem 2,6 mm entre topo da bateria e PCB principal, 6,2 mm entre PCBs e 4 mm entre PCB UI e tampa; alturas de componentes e dilatação da bateria não foram consideradas.
5. Construir protótipo de bancada que prove USB Audio + gravação microSD, mudo físico, segurança biométrica, RGB sem interferência acústica e autonomia.

Não emitir pedido de ferramenta, montagem eletrônica ou compra integral com esta revisão.
