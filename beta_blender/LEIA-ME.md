# Beta | versão atual 1.0.1

Abra `Beta_v1.0.1.blend` no Blender 4.3 ou posterior. A revisão refina materiais e iluminação da Beta carbon: trama twill 2 × 2 com feixes de 0,85 mm, filamentos finos, relevo sutil, resina e reflexos anisotrópicos. O novo anteparo interno confina o RGB à base. A 1.0.0 permanece como referência geométrica das vistas técnicas já entregues.

A única faixa decorativa iluminada fica no perímetro inferior da base, acima dos pés e abaixo dos conectores. Ela projeta luz sobre a mesa. As propriedades de cena `Faixa_RGB_cor`, `Faixa_RGB_brilho` e `Faixa_RGB_ligada` controlam o material ilustrativo; o arquivo abre em verde e inclui uma vista adicional em azul.

O material `Fibra de carbono preta · trama diagonal` é procedural e serve para avaliar a linguagem visual. Não comprova material real, processo de fabricação, espessura, resistência, acabamento ou custo. A Beta não altera os requisitos funcionais: nove teclas, biometria, fader, mudo, seletor, indicadores, gravador, P2, microSD, USB-C e aberturas acústicas permanecem.

O arquivo `Beta_v1.0.1.py` é o gerador ativo. Execute `blender -b --python beta_blender/Beta_v1.0.1.py`; use `-- --preview` para uma prévia em pasta temporária. Cada refinamento deve criar uma nova versão `Beta_vMAJOR.MINOR.PATCH`, sem sobrescrever a anterior. A antiga cópia da raiz foi arquivada em `.old/beta_blender_duplicate.py`.

Na 1.0.1, a galeria traz laranja, amarelo, verde, vermelho e azul na mesma perspectiva, mais detalhe dos controles e vista baixa da faixa. São renders Cycles de 256 amostras em 2000 × 1700 pixels. `Beta_v1.0.1_validacao.json` registra a paleta e as configurações. As cores hexadecimais sRGB são convertidas para valores lineares na cena. Circuito, firmware, consumo, difusor físico e fabricação continuam pendentes.

Para repetir um render a partir do `.blend` entregue, sem reconstruí-lo, use `blender -b --python beta_blender/Beta_v1.0.1.py -- --render-one laranja`. Os demais alvos são `amarelo`, `verde`, `vermelho`, `azul`, `detalhe_controles` e `faixa_RGB_base`.
