# Renders técnicos do README

As imagens correspondem aos modelos versionados. Nenhum componente eletrônico adicional foi inventado para completar a aparência dos renders.

## Produto Beta

Fontes: `beta_blender/Beta_v1.0.1.blend` para a galeria RGB e detalhe de materiais; `Beta_v1.0.0.blend` para as vistas técnicas de topo/lateral/traseira. A revisão 1.0.1 tem trama twill procedural em escala física, Cycles com 256 amostras e resolução 2000 × 1700. A paleta é convertida de sRGB para linear.

O gerador ativo é `beta_blender/Beta_v1.0.1.py` e recusa sobrescrever uma revisão entregue. Prévia: `blender -b --python beta_blender/Beta_v1.0.1.py -- --preview`. Para mudar o design, criar a próxima versão.

## Placas

KiCad CLI 9.0.2:

```sh
kicad-cli pcb render development/hardware/v0.2.0/CorePad_Interface_Bancada_v0.2.0.kicad_pcb -o docs/images/pcb_interface_3d.png --width 1500 --height 1000 --rotate '325,0,25' --background opaque --quality high
kicad-cli pcb render development/hardware/v0.2.0/CorePad_Principal_v0.2.0.kicad_pcb -o docs/images/pcb_main_3d.png --width 1500 --height 1000 --rotate '325,0,25' --background opaque --quality high
kicad-cli pcb export svg --layers Edge.Cuts,Dwgs.User --mode-single --fit-page-to-board --exclude-drawing-sheet -o docs/images/pcb_ui_placement.svg development/hardware/ui_mechanical/v0.1.0/CorePad_UI_Posicionamento_v0.1.0.kicad_pcb
```

Os modelos 3D de catálogo usados pelo KiCad dependem da instalação da biblioteca 3D correspondente. Os renders preservam a ausência atual de trilhas e a implantação parcial da principal.

## Peças plásticas

Blender 4.3.2:

```sh
blender -b --python docs/render/render_mechanical.py
```

O script abre `development/mechanical/v0.1.0/Beta_Pecas_v0.1.0.blend`, converte a escala de mm para metros na cena temporária e renderiza a vista explodida, interior da base e topo da tampa. A montagem-fonte e os STL não são alterados. O verde do difusor é uma cor de identificação do render.

## Conjunto integrado

`development/integration/v0.1.0/README.md` contém a sequência para gerar os STEP a partir das duas PCBs KiCad e do CAD CadQuery. As quatro vistas da montagem vêm dos STL gerados pelo CAD:

```sh
blender -b -t 4 --python development/integration/v0.1.0/render_assembly.py -- assembled
blender -b -t 4 --python development/integration/v0.1.0/render_assembly.py -- exploded
blender -b -t 4 --python development/integration/v0.1.0/render_assembly.py -- open
blender -b -t 4 --python development/integration/v0.1.0/render_assembly.py -- routing
```

O script salva PNG e `.blend` de cada vista. As versões `open` e `routing` ocultam peças e usam transparência apenas para inspecionar o interior; o STEP permanece sempre na posição montada.
