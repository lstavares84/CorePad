# Alpha | versão atual 1.2.0

Abra `Alpha_v1.2.0.blend` no Blender 4.3 ou posterior. As versões 1.0.0 e 1.0.1 foram preservadas. Cada refinamento recebe um novo arquivo no formato `Alpha_vMAJOR.MINOR.PATCH.blend`: MAJOR para mudança estrutural de definição; MINOR para inclusão de função ou mudança perceptível da organização; PATCH para correção e acabamento. O gerador recusa sobrescrever um arquivo Blender existente.

A versão 1.1.0 conserva nove teclas macro em matriz 3 × 3 e acrescenta um botão auxiliar de 6 × 3 mm acima da matriz, sem inscrição, com topo apenas 0,25 mm acima da tampa. A camada secreta continua dependendo da biometria. O acionamento e a indicação de estado serão definidos no projeto funcional.

Os centros de P2, microSD e USB-C estão no mesmo plano horizontal, calculado pela metade da altura do conjunto corpo e tampa. Os pés e os comandos não entram nessa medida. Na geometria atual, o fundo do corpo está em Z = 0,70 mm e a tampa chega a Z = 15,00 mm; o centro comum dos conectores é Z = 7,85 mm. P2 e microSD ficam à esquerda; USB-C atrás. O microSD permanece mais próximo da traseira que o P2.

O corpo mede 104 × 84 mm em planta. As teclas rasas têm superfície máxima de 19 × 19 mm, com bordas arredondadas, concavidade discreta e altura de 1,25 mm acima da tampa. A versão mantém o filete verde, o controle vertical com botão ranhurado, a chave mecânica detalhada e a biometria circular. A referência visual aprovada está em `Referencia_Alpha.png`.

O arquivo `Alpha_v1.2.0.py` conserva o gerador desta versão. O `alpha_blender.py` na pasta principal representa o gerador atual. As câmeras de frente, detalhe, traseira, topo e lateral estão no arquivo Blender. Materiais e detalhes visuais são propostas de acabamento, sem seleção final de componentes ou validação de fabricação e eletrônica.

A especificação funcional vigente está em `Especificacao_Produto_Macropad_Biometrico_Gravador_2026-11-21.md`, versão 0.6, na pasta principal. Sua numeração é independente da versão do modelo Blender.

A versão 1.1.1 corrige o sombreamento das superfícies planas da tampa e do corpo, identificado na vista superior da 1.1.0. O seletor e as cotas dos conectores da 1.1.0 foram conservados. A 1.1.0 também permanece disponível.

A versão 1.2.0 inclui três micro LEDs de 0,92 mm junto ao seletor de camadas e um botão circular de 4 mm para ativar a gravação ambiente. A propriedade de cena `Camada_ativa`, de 1 a 3, permite visualizar cada LED ativo, um por vez. O botão circular também tem saliência de 0,25 mm. Foram removidos os antigos furos da face superior e feitos quatro furos passantes de 1 mm em cada lateral, com membranas ilustrativas recuadas. Nenhuma dessas representações valida a captação acústica ou implementa firmware.

Depois da aprovação da 1.2.0, o usuário definiu uma faixa RGB difusa no perímetro inferior da base, inspirada na iluminação inferior de um mouse, com cor escolhida pelo software. Essa decisão não altera retroativamente a 1.2.0. Por ser uma função visual perceptível, deve ser modelada em uma nova Alpha 1.3.0, preservando o filete e a ausência de iluminação sob as teclas até nova decisão expressa.
