# Renders técnicos do README

As imagens correspondem aos modelos versionados. Nenhum componente eletrônico adicional foi inventado para completar a aparência dos renders.

## Produto Beta

Fonte: `beta_blender/Beta_v1.0.0.blend`. Os sete renders já entregues são reutilizados diretamente pelo README. O gerador está em `beta_blender/Beta_v1.0.0.py` e recusa sobrescrever uma revisão entregue; para mudar o design, criar a próxima versão.

## Placas

KiCad CLI 9.0.2:

```sh
kicad-cli pcb render development/hardware/v0.2.0/CorePad_Interface_Bancada_v0.2.0.kicad_pcb -o docs/images/pcb_interface_3d.png --width 1500 --height 1000 --rotate '325,0,25' --background opaque --quality high
kicad-cli pcb render development/hardware/v0.2.0/CorePad_Principal_v0.2.0.kicad_pcb -o docs/images/pcb_main_3d.png --width 1500 --height 1000 --rotate '325,0,25' --background opaque --quality high
```

Os modelos 3D de catálogo usados pelo KiCad dependem da instalação da biblioteca 3D correspondente. Os renders preservam a ausência atual de trilhas e a implantação parcial da principal.

## Peças plásticas

Blender 4.3.2:

```sh
blender -b --python docs/render/render_mechanical.py
```

O script abre `development/mechanical/v0.1.0/Beta_Pecas_v0.1.0.blend`, converte a escala de mm para metros na cena temporária e renderiza a vista explodida, interior da base e topo da tampa. A montagem-fonte e os STL não são alterados. O verde do difusor é uma cor de identificação do render.
