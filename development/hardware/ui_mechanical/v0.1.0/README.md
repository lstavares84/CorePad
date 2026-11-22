# PCB UI — posicionamento mecânico 0.1.0

Arquivo KiCad com contorno 98 × 78 mm, espessura nominal 1,6 mm, centros e janelas de nove teclas e centros de biometria, fader, mudo, camada e gravação. O gerador `build_ui.py` e `placement.json` mantêm as coordenadas ligadas ao datum da montagem 3D.

**Não há pads, footprints de switches, trilhas, redes ou esquema.** Os retângulos de 19,6 mm são as aberturas nominais da tampa, não o desenho de soldagem do Kailh Choc V2. Esta revisão é apenas um suporte de posicionamento para o conjunto STEP. A interface elétrica de bancada 0.2.0, em `../../v0.2.0/`, é outra placa e não deve ser confundida com esta.

O `drc.txt` registra zero violações e zero itens desconectados para este contorno mecânico vazio. Esse resultado **não é** um DRC de PCB elétrica pronta.

Próximo fechamento: conferir datasheet/STEP dos switches, curso e keycap; decidir conectores entre placas, furos e suportes; construir esquema da UI, footprints, redes, roteamento e DRC com os modelos reais.
