# Peças mecânicas Beta 0.1.0

Cinco modelos STL e uma montagem Blender editável: base, tampa, difusor RGB, botão de camada e botão de gravação. Todas as medidas de exportação são em mm. O gerador `build_parts.py` reproduz as peças.

Volume exploratório: 104 × 84 × 28,4 mm, excluindo comandos. A espessura foi aumentada para explorar montagem com bateria e duas placas; não é fechamento dimensional. Os recortes de P2, microSD e USB-C têm centro em Z=14,2 mm, metade do conjunto base e tampa. A montagem de conectores reais nesse plano continua pendente. Esta revisão não substitui a apresentação visual Beta 1.0.0.

As peças têm paredes e recortes volumétricos. Quatro pontes internas mantêm o fundo unido às paredes através do canal luminoso, com folgas correspondentes no difusor. Cada STL é um volume conexo fechado, conforme `validation.json`. Não incluem encaixes de catálogo para switches, fixações da tampa, suportes de PCB ou retenção definitiva do difusor. Teclas e knob do fader dependem das hastes reais. Imprimir apenas para avaliar volume, acesso e ergonomia. Não montar bateria energizada ou circuito solto nessa revisão.

Proposta de processo: plástico isolante PA12/ABS na base e tampa, com revestimento decorativo em aparência de carbono; difusor translúcido em resina/PETG a ensaiar. A escolha do proprietário é o estilo carbono. Compósito estrutural, película ou hidroimpressão ainda não foram escolhidos. A proposta de revestimento deve ser validada por amostra física.

Na próxima revisão, fechar o empilhamento com os componentes de catálogo, recalcular o plano médio dos conectores, incluir suportes e fixações, folgas de montagem, espaço para expansão da bateria, dutos de microfone, curso das teclas e retenção do difusor. O canal luminoso não pode comprometer a rigidez ou a fixação da base.
