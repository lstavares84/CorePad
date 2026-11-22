# Três estudos 3D do macropad biométrico Premium

Criados em Blender 4.3.2 em 21/11/2026 a partir de `Especificacao_Produto_Macropad_Biometrico_Gravador_2026-11-21.md`. As dimensões abaixo são apenas parâmetros de estudo e não medidas para produção. Cada arquivo `.blend` contém objetos nomeados, materiais, iluminação e duas câmeras. A câmera frontal mostra P2 e microSD na lateral esquerda; a traseira mostra o USB-C.

| Alternativa | Distribuição das 12 teclas | Corpo exploratório | Biometria | Característica |
|---|---|---|---|---|
| 01 Grade panorâmica | 4 colunas × 3 linhas | 121 × 82 × 13 mm | Circular no canto inferior direito | Menor área de mesa entre as três |
| 02 Quadrado compacto | 3 colunas × 4 linhas | 104 × 106 × 13 mm | Quadrada no canto inferior direito | Corpo menos largo, com acesso direto à grade |
| 03 Biometria superior | 4 colunas × 3 linhas | 120 × 96 × 14 mm | Circular na faixa superior | Separa o leitor da faixa de controles |

Todas têm 12 teclas rasas sem inscrições e sem iluminação, moldura verde contínua, controle deslizante vertical com botão pequeno e chave mecânica à direita, P2 na lateral esquerda, slot microSD acima do P2 e USB-C atrás. Os três pequenos pontos no tampo representam aberturas de captação ambiente. A independência elétrica da saída P2 em relação ao mudo do microfone, a gravação, a biometria e FIDO2 não são demonstradas por um modelo visual.

O arquivo `blender_macropad_concepts.py` recria as três cenas e seus renders em uma instalação do Blender 4.3.2. Os renderizadores e materiais podem ser editados livremente. Os arquivos PNG `*_frente` e `*_traseira` são as vistas de comparação.
