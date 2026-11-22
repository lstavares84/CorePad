# CorePad Beta Carbon — montagem eletromecânica 0.1.0

Esta revisão inicia o **modelo integrado 3D** em milímetros. O arquivo `CorePad_Beta_integrado_v0.1.0.step` contém carcaça, difusor, placa principal exportada do KiCad, volume da futura placa de interface, bateria, volumes de conectores, nove switches/keycaps, biometria, controles e cabos internos propostos. `parts/` contém STEP e STL por item. `assembly_manifest.json` registra os limites de cada sólido. O STEP é editável como conjunto de sólidos em CAD compatível; o histórico paramétrico fica em `build_assembly.py`.

## Autoridade geométrica

| Elemento | Origem e estágio |
|---|---|
| Caixa 104 × 84 × 28,4 mm | Hipótese dimensional de engenharia; diverge da espessura do render de aparência Beta 1.0.1 |
| Base, tampa e difusor | Peças paramétricas derivadas da mecânica exploratória 0.1.0; não incluem fixação, vedação nem tolerâncias |
| PCB principal 98 × 78 × 1,6 mm | Contorno nativo do KiCad 0.2.0 exportado para STEP; circuito incompleto e não roteado |
| PCB da interface 98 × 78 × 1,6 mm | Contorno do [KiCad mecânico 0.1.0](../../hardware/ui_mechanical/v0.1.0/README.md), com centros de controles; **sem pads, esquema ou roteamento**. A placa de bancada 0.2.0 é outra |
| Bateria 60 × 36 × 7 mm | Volume de referência, não uma célula selecionada ou homologada |
| USB-C, P2, microSD, biometria, nove switches e controles | Reservas geométricas sem STEP do fabricante; não usar para corte de ferramenta |
| FFC UI–principal e dois fios da bateria | Rotas visuais propostas, sem cabo/conector comprado, raio mínimo, pinagem final ou alívio de tração |

Datum: X/Y no centro da caixa, X positivo à direita, Y positivo para trás; Z=0 na face inferior. A tampa ocupa Z=26–28,4. As portas têm centro nominal Z=14,2; os conectores reais precisam confirmar esta altura. A banda RGB fica apenas na base, em Z≈2.

Os corpos isolantes no STEP `--board-only` do KiCad medem 1,51 mm em Z, embora a espessura nominal configurada nas placas seja 1,6 mm. O desenho de empilhamento e as folgas abaixo usam **1,6 mm como reserva conservadora**; conferir a pilha de cobre/máscara e o STEP completo quando o stack-up for escolhido.

## Empilhamento nominal

| Item | Faixa Z (mm) | Folga nominal seguinte |
|---|---:|---:|
| Fundo da base | 0–2 | 1 até bateria |
| Bateria de referência | 3–10 | 2,6 até PCB principal |
| PCB principal | 12,6–14,2 | 6,2 até PCB UI |
| PCB UI reserva | 20,4–22 | 4 até face inferior da tampa |
| Tampa | 26–28,4 | — |

`fit_report.json` verifica interseção volumétrica entre os dez pares rígidos mais críticos: **0 mm³** nos dez pares. Não verifica o volume de componentes montados, curso dos switches, expansão da célula, raio de dobra do FFC, dissipação, EMC, suportes/fixações ou tolerâncias acumuladas. Os conectores e o FFC podem ocupar superfícies de montagem intencionalmente; não são validação elétrica ou mecânica.

## Arquivos para abrir e revisar

- `CorePad_Beta_integrado_v0.1.0.step`: conjunto CAD em posição montada, com cores e sólidos separados.
- `CorePad_Beta_assembled_v0.1.0.blend`: vista Blender montada; outros `.blend` separam as vistas aberta, explodida e de inspeção da passagem de cabos.
- `desenho_planta.svg` e `desenho_empilhamento.svg`: desenhos dimensionais **preliminares**, com cotas nominais e indicação de reservas. Faltam vistas por peça, tolerâncias, referências de datum de fabricação e controle de revisão para uma ordem de compra.
- `montagem_assembled.png`, `montagem_open.png`, `montagem_exploded.png`, `montagem_routing.png`: imagens de revisão, não prova de fabricabilidade.
- `BOM_MECANICA_CABOS.md` e `LIBERACAO_MANUFATURA.md`: materiais candidatos e lista de fechamento.

## Reproduzir

Ferramentas verificadas localmente: KiCad CLI 9.0.2, CadQuery 2.8.0 (Python 3.13 em ambiente virtual) e Blender 4.3.2. O ambiente virtual não é versionado.

```sh
python3 -m venv /tmp/corepad-cad-venv
/tmp/corepad-cad-venv/bin/pip install cadquery==2.8.0
kicad-cli pcb export step --board-only --user-origin 99x89mm -f -o development/integration/v0.1.0/pcb_principal_kicad.step development/hardware/v0.2.0/CorePad_Principal_v0.2.0.kicad_pcb
/usr/bin/python3 development/hardware/ui_mechanical/v0.1.0/build_ui.py
kicad-cli pcb export step --board-only --user-origin 99x89mm -f -o development/integration/v0.1.0/pcb_ui_kicad.step development/hardware/ui_mechanical/v0.1.0/CorePad_UI_Posicionamento_v0.1.0.kicad_pcb
/tmp/corepad-cad-venv/bin/python development/integration/v0.1.0/build_assembly.py
/tmp/corepad-cad-venv/bin/python development/integration/v0.1.0/verify_fit.py
python3 development/integration/v0.1.0/build_drawings.py
blender -b -t 4 --python development/integration/v0.1.0/render_assembly.py -- assembled
```

As outras vistas usam `open`, `exploded` e `routing` no último argumento. O método STEP é intercambiável com FreeCAD, Fusion 360 e SolidWorks para revisão e detalhamento, mas o arquivo paramétrico mestre desta revisão é CadQuery/Python. STL é só malha para prototipagem/renderização.
