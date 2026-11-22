# Beta | versão atual 1.0.0

Abra `Beta_v1.0.0.blend` no Blender 4.3 ou posterior. Beta é uma linha visual separada da Alpha: preserva a geometria funcional da Alpha 1.3.0, mas remove a linha verde superior e aplica estilo de fibra de carbono preta à carcaça e à tampa.

A única faixa decorativa iluminada fica no perímetro inferior da base, acima dos pés e abaixo dos conectores. Ela projeta luz sobre a mesa. As propriedades de cena `Faixa_RGB_cor`, `Faixa_RGB_brilho` e `Faixa_RGB_ligada` controlam o material ilustrativo; o arquivo abre em verde e inclui uma vista adicional em azul.

O material `Fibra de carbono preta · trama diagonal` é procedural e serve para avaliar a linguagem visual. Não comprova material real, processo de fabricação, espessura, resistência, acabamento ou custo. A Beta não altera os requisitos funcionais: nove teclas, biometria, fader, mudo, seletor, indicadores, gravador, P2, microSD, USB-C e aberturas acústicas permanecem.

O arquivo `Beta_v1.0.0.py` é o gerador ativo desta revisão. Execute `blender -b --python beta_blender/Beta_v1.0.0.py`. Cada refinamento deve criar uma nova versão `Beta_vMAJOR.MINOR.PATCH`, sem sobrescrever a anterior. A antiga cópia da raiz foi arquivada em `.old/beta_blender_duplicate.py`.

As vistas entregues são frente/esquerda, controles, traseira USB-C, superior, lateral P2/microSD, faixa RGB baixa e variante azul. `Beta_v1.0.0_validacao.json` registra as verificações ilustrativas. Circuito, firmware, consumo, difusor físico e fabricação continuam pendentes.
