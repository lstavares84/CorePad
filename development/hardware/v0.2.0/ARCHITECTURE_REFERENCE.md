# Alpha • eletrônica 0.1.0

> Referência técnica herdada para o desenvolvimento Beta. Este relatório foi preservado do estudo inicial por conter justificativas, cálculos e fontes ainda úteis. Não representa o estado atual dos arquivos: consultar `README.md`, `BOM.md` e os projetos 0.2.0 desta pasta. O design Alpha e seus demais artefatos foram arquivados em `.old/`.

22/11/2026 | Projeto autoral a partir da Alpha Blender 1.2.0 aprovada pelo usuário e da documentação dos fabricantes indicada ao final.

**A referência visual está firmada. A proposta eletrônica é um aparelho USB-C com bateria interna, controlador de baixo consumo, dois microfones, áudio dedicado, microSD e proteção separada das credenciais.** A autonomia de projeto é de pelo menos 30 horas de gravação ambiente. A espessura de 14,3 mm do modelo visual não é uma restrição de engenharia: a carcaça será ajustada ao conjunto real.

Esta revisão inicia a engenharia e não autoriza fabricação ou compra integral. Entrega arquitetura proposta, componentes candidatos, cálculo energético, interligações funcionais e dois estudos editáveis de posicionamento em KiCad. **Ainda não há esquema elétrico pino a pino, circuito simulado, trilhas roteadas ou protótipo testado.** Os desenhos de posicionamento usam reservas de espaço e um padrão de soldagem da biblioteca KiCad; nenhum deles está aprovado para produção.

## 1. O que fica definido

Os requisitos aprovados são nove teclas rasas sem inscrições, em matriz 3 × 3; três camadas e três micro LEDs; seletor de camadas independente; botão dedicado ao gravador; biometria; controle deslizante vertical e chave mecânica à direita; P2 à esquerda; microSD à esquerda, atrás do P2; USB-C exclusivamente atrás; visual preto com filete verde e sem iluminação de teclas. A faixa verde será um inserto de cor sólida, sem consumo elétrico. As aberturas laterais alimentam dois microfones, não oito.

O usuário autorizou que a eletrônica determine as mudanças necessárias na construção. A intenção de alinhar os centros de P2, microSD e USB-C na metade da espessura permanece, mas não será apresentada como resolvida ao colocar conectores de alturas diferentes sobre a mesma placa. Pequenas placas auxiliares, rebaixos ou outra seleção de conectores podem ser necessários. A referência de área é 104 × 84 mm; nenhum aumento está aprovado como dimensão definitiva.

A alimentação deverá funcionar por USB-C e por bateria interna. A referência solicitada é o Plaud Note original, cujo fabricante anuncia até 30 horas de gravação com 400 mAh [S01]. Adotar o mesmo tempo não significa adotar a mesma capacidade. Propõe-se começar com 2.000 mAh para acomodar o consumo e a variabilidade do microSD removível. A bateria de catálogo usada como referência mede 60 × 36 × 7 mm [S02].

## 2. Arquitetura escolhida para o estudo

| Bloco | Candidato principal | Motivo e limite da escolha |
|---|---|---|
| Controle central | STM32U5A5ZJT6Q | Processador de baixo consumo, USB de alta velocidade com interface física integrada, áudio digital e cartão SD. A variante Q permite usar o regulador interno eficiente. Pinagem simultânea ainda precisa ser fechada. [S03] |
| Conversão de áudio | TAC5112IRGER | Dois canais analógicos de entrada e saída; permite separar o áudio recebido do computador da captação local. É candidato moderno e compacto. [S04] |
| Microfones | 2 × IM73A135V01XTSA1 | Captação omnidirecional e saída diferencial, uma cápsula por lateral. Dutos e membranas serão projetados e ensaiados. [S05] |
| Saída para fone | TPA6132A2RTER | Amplificador de saída referenciada ao terra, adequado a um P2 estéreo convencional; evita grandes capacitores de saída. Entradas e ganho dependem do circuito final. [S06] |
| Armazenamento | microSD por SDMMC de 4 bits | Cartões até 256 GB, sistema de arquivos exFAT; leitura pelo computador exclusivamente no estado Arquivos. [S03, S07] |
| Proteção das credenciais | SE050C2HQ1/Z01SD | Componente criptográfico dedicado, acessado pela área protegida do controlador. Não transforma sozinho o aparelho em autenticador FIDO2. [S08] |
| Biometria de bancada | Adafruit 4750 | Referência redonda de 20,8 mm, comunicação serial e alimentação de 3,3 V. Usar inicialmente para interface e ergonomia; não aprovar como raiz de confiança. [S09] |
| Carga e alimentação | BQ25622 + reguladores separados | Permite alimentar o sistema e carregar a bateria com gestão de corrente. A corrente de carga será configurada para a célula escolhida. [S10] |

A alternativa com computador Linux embarcado aumentaria consumo, tempo de inicialização e complexidade. Controladores USB limitados à velocidade básica dificultariam a transferência de gravações grandes. A escolha do STM32U5A5 oferece folga de memória e interfaces sem acrescentar rádio: Wi-Fi e Bluetooth não fazem parte desta revisão. A combinação de periféricos deve ser validada antes do esquema, inclusive canais de transferência automática, pinos e recursos USB disponíveis.

## 3. Como o áudio deverá funcionar

Os microfones entram em dois canais do conversor de áudio. O controlador recebe essas amostras, envia a voz ao computador quando conectado e grava no cartão. O áudio que o computador envia ao Alpha segue para o fone e também pode ser registrado antes do ajuste de volume. Assim, baixar o volume do fone não reduz o nível da gravação dos participantes remotos.

O computador deverá selecionar o Alpha como saída e entrada de áudio da chamada. **O aparelho não recebe automaticamente o som enviado a outro dispositivo**, como o alto-falante do monitor ou um fone Bluetooth. Esse cenário exigiria encaminhamento pelo sistema operacional ou aplicativo auxiliar, como a captura de saída descrita pela Microsoft [S11]. A primeira implementação deve provar o caminho direto, sem depender de um aplicativo para chamadas normais.

O P2 é inicialmente saída estéreo de três contatos, sem entrada para microfone de headset. A referência elétrica de entrada do amplificador deve respeitar as tensões do conversor; não ligar saídas em ponte diretamente ao terra do P2. O TAC5112 dispõe de configurações de saída distintas [S04], razão para registrar explicitamente o uso de saídas de linha e do amplificador separado nesta proposta.

Para o protótipo, propor gravação ambiente em PCM de 48 kHz e 16 bits, dois canais, um por microfone. No modo híbrido, quatro canais no mesmo arquivo: microfone esquerdo, microfone direito, computador esquerdo e computador direito. Essa separação permite tratamento posterior; não identifica pessoas automaticamente. Não enviar de volta à chamada o áudio remoto que foi recebido, evitando realimentação. O tratamento de eco quando houver alto-falantes externos continua sendo uma validação específica.

Uma gravação ambiente de 30 horas ocupa aproximadamente 20,736 GB, sem cabeçalhos; a híbrida nas mesmas condições ocupa 41,472 GB. São cálculos de 48.000 amostras/s × 2 bytes × número de canais × duração. Um WAV RIFF convencional atinge seu limite de tamanho antes disso. A proposta é RF64 para manter um arquivo por reunião e exFAT no cartão [S07, S12]. O programa de exportação poderá converter o arquivo para um formato aceito pelo serviço de transcrição escolhido; não pressupor envio direto de um arquivo de dezenas de gigabytes.

Usar um relógio comum para conversor e gravação, com retorno de sincronização da interface USB de áudio. Validar deriva, contagem de amostras e continuidade. Reservar memória para escrita em blocos e medir as pausas máximas dos cartões. Dois megabytes de memória de áudio, se disponíveis após o restante do programa, cobrem cerca de 10,4 segundos no modo ambiente ou 5,2 segundos no híbrido. Esses números não garantem que qualquer microSD funcionará.

## 4. Mudo físico independente do fone

A chave proposta é uma alavanca de dois polos e duas posições estáveis, família C&K 7201 [S13]. Um polo interrompe fisicamente a alimentação exclusiva das duas cápsulas. O outro comanda, diretamente por circuito, dois comutadores TS5A23157 que afastam os quatro sinais analógicos dos microfones e ligam as entradas, antes dos capacitores de acoplamento, a uma referência silenciosa. As entradas do conversor mantêm a polarização indicada pelo fabricante, sem curto de sua tensão interna de referência. Essa topologia ainda requer esquema detalhado e ensaio de transitórios [S14].

O programa apenas lê o estado da chave; não deve ter caminho capaz de forçar a alimentação das cápsulas ou vencer o comando de mudo. Resistores mantêm o estado seguro durante inicialização ou cabo desconectado. Evitar alimentação parasita pelas saídas analógicas. O conversor, sua parte de reprodução e o amplificador do fone continuam alimentados. Mudo não desliga a reunião nem o áudio remoto. A captação local deverá ser bloqueada mesmo com o programa travado; o teste precisa medir o áudio residual, não apenas verificar uma variável no programa.

## 5. Energia e a meta de 30 horas

A bateria de referência é uma célula protegida de 3,7 V e 2.000 mAh, energia nominal de 7,4 Wh. Para dimensionamento, adotam-se 80% de energia utilizável e 90% de eficiência média de conversão. Esses fatores são hipóteses de engenharia para margem, não características medidas do Alpha. Energia disponível às cargas: 7,4 × 0,80 × 0,90 = 5,328 Wh. Para 30 horas, o limite médio das cargas é **177,6 mW**. O orçamento inicial foi fixado em **150 mW**, que produziria 35,5 horas sob essas hipóteses.

| Bloco no modo ambiente | Orçamento médio às cargas | Natureza do valor |
|---|---:|---|
| Controlador, memória e relógios | 35 mW | Alocação a validar com programa real |
| Conversor, somente entrada | 15 mW | Alocação incluindo operação e alimentação propostas; não copiar o mínimo de catálogo |
| Dois microfones | 2 mW | Alocação a validar no modo e tensão escolhidos |
| microSD, incluindo intervalos entre escritas | 70 mW | Principal incerteza, exige homologação de modelos de cartão |
| Indicador de gravação e controles | 2 mW | LEDs em baixa corrente, sem faixa iluminada |
| Supervisão, medição e perdas não cobertas pela conversão global | 6 mW | Alocação de consumo auxiliar |
| Margem de implementação | 20 mW | Reserva |
| **Total** | **150 mW** | **Estimativa, não resultado de teste** |

Com 200 mW, a mesma conta cai para 26,6 horas. Portanto, a bateria de 2.000 mAh é um ponto de partida, não uma promessa. A aceitação exige pelo menos 30 horas contínuas, sem perda de amostras, com cartão homologado, indicação de gravação ativa e bateria em condições declaradas. O teste de envelhecimento deve ser separado do teste com bateria nova. Fone tocando, biometria continuamente ativa e transferência de arquivos exigem outro orçamento; não fazem parte da comparação com gravação ambiente autônoma.

No modo de gravação sem computador, desligar USB, reprodução, amplificador do fone e alimentação principal do leitor biométrico quando não necessários. Não cortar energia do microSD entre blocos sem protocolo seguro; otimizar escrita em rajadas, tempos ociosos e escolha do cartão. A segurança não pode perder chaves por ser desligada; sua política de retomada deve ser definida.

As cápsulas usam alimentação exclusiva de 2,8 V. O TAC5112 usa AVDD e IOVDD de 3,3 V, com filtragem própria: não ligar seu AVDD à linha de 2,8 V, pois essa tensão está fora das faixas de operação recomendadas [S04].

O BQ25622 alimenta o sistema por USB e/ou bateria. O padrão de carga do componente não deve ser aceito automaticamente: manter sua entrada de habilitação em carga desativada até configurar os limites validados [S10]. Propor inicialmente 0,5 A para a referência de bancada, sujeito à confirmação da ficha da célula e do aquecimento. Carga completa será da ordem de várias horas; não foi assumido o tempo de carga do Plaud. Medir temperatura na célula com termistor, além da proteção interna do pacote. Proteção da célula, carregador, termistor e limitação da entrada cumprem funções diferentes.

O USB-C opera inicialmente a 5 V, como consumidor de energia; não se prevê fornecer energia de volta ao cabo. O controlador de porta TUSB320 informa a corrente anunciada pela fonte [S15]. Respeitar também os limites de uma porta USB comum antes/depois da enumeração. Se a fonte não suportar sistema e carga, reduzir a carga. Acrescentar proteção contra descarga eletrostática e sobretensão nos pontos externos. O MAX17048 é candidato a estimar a carga restante, com calibração para a célula [S16]. A retirada do USB deve continuar a gravação pela bateria; bateria baixa deve encerrar e fechar o arquivo antes da proteção cortar energia.

## 6. Credenciais, biometria e configuração

Reservar uma região protegida do controlador para autenticação, acesso ao SE050, atualização assinada e políticas de bloqueio. Configurações comuns e textos ficam na memória interna com atualização transacional e proteção contra desgaste. Credenciais tradicionais ficam cifradas fora do microSD; chaves de proteção ficam vinculadas ao componente criptográfico e à política do controlador. O canal para o componente seguro precisa ser autenticado e provisionado na montagem. O acesso de depuração deve ser controlado em produção, mantendo recuperação de desenvolvimento separada.

O módulo biométrico serial de bancada responde a comandos; a documentação consultada não comprova uma resposta criptograficamente autenticada que impeça a substituição do sensor por um simulador. **Não liberar senhas reais apenas por uma resposta serial desse módulo.** Ele serve para validar interação e encaixe. A seleção final depende de sensor com comunicação autenticada ou de uma arquitetura adicional de autenticação. O leitor 4750 estava sem estoque na página consultada; abastecimento também é pendência [S09]. Não retirar a biometria do produto para contornar essa pendência.

FIDO2 será uma função separada do teclado que digita textos. Exige implementação do protocolo CTAP, proteção de chaves, confirmação física, política de PIN/biometria, recuperação e testes entre sistemas [S17]. O SE050 ajuda na proteção criptográfica, mas não entrega esse programa pronto nem certifica o produto. Até a cadeia biométrica ser validada, os ensaios usam credenciais fictícias e autenticação de desenvolvimento. A terceira camada permanece protegida como requisito, ainda não implementada.

O controle terá nove entradas independentes, uma por tecla, sem necessidade de matriz elétrica ou diodos para evitar teclas fantasmas. A matriz 3 × 3 é a disposição física. Reservar entradas para seletor, gravador, estado de mudo e detecção do cartão, além de saída para cada LED. Textos devem armazenar pelo menos 256 caracteres por posição, distinguindo caracteres de bytes UTF-8. Teclado USB envia códigos de teclas; acentuação consistente depende do idioma configurado no computador. Perfis de teclado por sistema e eventual aplicativo de inserção de texto precisam ser definidos; não prometer Unicode universal apenas por usar USB.

## 7. Estados e uso

| Estado | Dono do cartão | Comportamento proposto |
|---|---|---|
| Pronto | Aparelho, sem gravação | Teclas disponíveis por USB; gravador pronto; camada protegida bloqueada por padrão |
| Gravando | Aparelho | MicroSD não é unidade disponível ao computador; início/fim pelo botão dedicado |
| Arquivos | Computador | Sem gravação; copiar e organizar arquivos; teclas podem continuar disponíveis |
| Transição | Nenhum acesso concorrente | Fechar e sincronizar arquivo, desmontar, transferir propriedade e só então habilitar o próximo uso |
| Bateria baixa/falha | Aparelho | Finalização controlada, sinalização e bloqueio de novo início |

A retirada da unidade lógica não equivale, sozinha, à expulsão segura pelo computador. Para sair de Arquivos, exigir liberação pelo sistema/aplicativo; se não houver confirmação, manter o cartão indisponível para gravação e indicar a pendência. Não interromper gravações do computador silenciosamente. Propor um botão de gravação com ponto luminoso próprio, discreto, para indicar gravação/erro sem confundir os três LEDs de camada. Esse quarto indicador é uma proposta técnica nova, não uma alteração já aprovada no Blender.

O deslizante deve controlar inicialmente o volume local do P2, lido pelo conversor analógico do controlador e aplicado ao ganho digital de reprodução. Isso preserva o nível do arquivo e evita diferenças entre sistemas. Controle do volume geral do computador pode ser um modo configurável futuro. Essa atribuição é proposta técnica, pois a especificação ainda não havia fechado a origem do volume.

## 8. Placas e posicionamento

O estudo entregue usa **placa principal de quatro camadas e placa superior de interface de duas camadas**, ambas com contorno de referência 98 × 78 mm. A placa superior concentra teclas e controles; a principal concentra processamento, áudio, armazenamento e energia. O conjunto com duas placas facilita o primeiro protótipo e desacopla altura das teclas de circuitos sensíveis. Não é ainda uma decisão de produção: depois do ensaio, comparar com placa única para reduzir conectores e espessura.

Na placa principal, a região de energia fica atrás, afastada do circuito de microfones. O áudio fica à esquerda, próximo ao P2. O controlador fica no centro/direita, com segurança próxima. As cápsulas ficam nas duas bordas, usando dutos selados para que os furos laterais captem o exterior em vez do ruído interno da caixa. A bateria tem uma reserva de montagem na face inferior; componentes podem existir na face oposta, mas terminais atravessando a placa não podem perfurar ou pressionar a célula. Reservar proteção rígida e espaço definido pelo fabricante para tolerâncias/expansão.

Camadas propostas da principal: sinais/componentes, plano contínuo de terra, alimentação e sinais lentos, sinais/componentes. O plano de referência não será dividido entre áudio e digital; separação por posicionamento e caminhos de retorno evita cruzar fendas sob sinais rápidos. USB exige par diferencial de 90 ohms, calculado com a composição real da placa escolhida com o fabricante. Não fixar largura e espaçamento antes dessa definição. Áudio analógico fica afastado de indutores, relógios, cartão e caminhos de carga. Reservar pontos de medição de corrente por bloco.

O desenho de posicionamento preserva as projeções dos controles da Alpha. Nenhum arquivo presume que microSD, P2 e USB-C tenham centros alinhados em altura. Resolver isso no modelo tridimensional de peças reais antes de fechar a mecânica. Para planejamento, trabalhar com uma faixa exploratória de espessura de aproximadamente 22 a 28 mm para duas placas e a bateria escolhida; **isso não é cota validada nem dimensão final**. A chave de alavanca pode ser o componente limitante. Encaixe, curso das teclas, altura do deslizante e raio dos cabos exigem medição ou modelos dimensionais certificados.

A BOM é preliminar: componentes principais têm código ou família e fonte; passivos, conectores entre placas, relógios e proteção final têm pendências explícitas. Não há custo total calculado porque isso sugeriria uma lista completa inexistente. Estoque, preço, lote e equivalências precisam ser cotados na revisão de compra. Não substituir encapsulamentos só por terem o mesmo número de terminais.

## 9. O que precisa ser provado antes da primeira fabricação

Primeiro, validar em bancada o controlador com áudio simultâneo USB, gravação em microSD e escrita de arquivo longo. Medir consumo com os cartões candidatos. Segundo, validar mudo independente e áudio no P2 durante a atuação da chave. Terceiro, fechar seleção da biometria e política de segurança. Esses ensaios orientam a revisão 0.2.0 de esquema elétrico e pinagem, evitando fabricar uma placa em torno de suposições que mudam a arquitetura.

| Ensaio | Critério de avanço |
|---|---|
| Autonomia | Pelo menos 30 h no perfil ambiente declarado; registrar capacidade, temperatura, cartão e estado dos indicadores |
| Cartão | Gravar continuamente e recuperar após retirada do USB; medir pausas, consumo e comportamento próximo da lotação |
| Mudo | Captação local interrompida por hardware, inclusive com programa travado; reprodução no P2 permanece normal |
| Áudio | Sem perda de amostras; avaliar ruído, fala distante, toque nas teclas, carregamento e eco |
| Arquivos | Exclusividade demonstrada, sem montagem simultânea; transição segura e recuperação após falta de energia |
| USB | Teclado, áudio, configuração, arquivos e futura autenticação cabem nos recursos do controlador e funcionam nos sistemas-alvo |
| Segurança | Sensor falso/desconectado não libera credenciais; proteção de depuração, atualização e chaves revisada |
| Mecânica | Peças reais sem colisão, bateria protegida, conectores acessíveis e centros de altura resolvidos |

A verificação feita nesta entrega cobre abertura dos arquivos KiCad, contornos, quantidades de reservas e cálculos. Não há aprovação elétrica ou de fabricação. A próxima revisão deverá acrescentar esquema elétrico pino a pino e BOM completa; depois, roteamento e verificações de projeto; por último, fabricação de protótipos, montagem, testes e revisão do Blender com as medidas reais.

## Fontes primárias e origem

Fontes consultadas em 22/11/2026. Os cálculos, orçamento energético, organização das placas, estados e decisões de arquitetura são propostas autorais desta revisão. As características dos componentes vêm dos documentos abaixo. Aprovação de conceito e autorização para adequar a mecânica: mensagens do usuário deste chat.

- [S01] Plaud, autonomia por modelo: https://support.plaud.ai/hc/en-us/articles/61748135468825-How-long-does-the-battery-last-on-my-Plaud-device
- [S02] Adafruit 2011, bateria de referência: https://www.adafruit.com/product/2011
- [S03] ST, STM32U5A5ZJ: https://www.st.com/en/microcontrollers-microprocessors/stm32u5a5zj.html ; ficha: https://www.st.com/resource/en/datasheet/stm32u5a5zj.pdf
- [S04] TI, TAC5112: https://www.ti.com/product/TAC5112 ; ficha: https://www.ti.com/lit/ds/symlink/tac5112.pdf
- [S05] Infineon, IM73A135: https://www.infineon.com/assets/row/public/documents/30/49/infineon-im73a135-datasheet-en.pdf
- [S06] TI, TPA6132A2: https://www.ti.com/product/TPA6132A2
- [S07] FatFs, configuração exFAT: https://elm-chan.org/fsw/ff/doc/config.html
- [S08] NXP, SE050: https://www.nxp.com/docs/en/data-sheet/SE050-DATASHEET.pdf
- [S09] Adafruit 4750, sensor biométrico: https://www.adafruit.com/product/4750
- [S10] TI, BQ25622: https://www.ti.com/product/BQ25622 ; ficha: https://www.ti.com/lit/ds/symlink/bq25622.pdf
- [S11] Microsoft, captura de saída: https://learn.microsoft.com/en-us/windows/win32/coreaudio/loopback-recording
- [S12] EBU, RF64: https://tech.ebu.ch/docs/tech/tech3306.pdf
- [S13] Littelfuse/C&K, série 7000: https://www.littelfuse.com/assetdocs/littelfuse-ck-toggle-7000-series-datasheet?assetguid=fed01bc6-88d0-4bda-b896-13c98cf9e90e
- [S14] TI, TS5A23157: https://www.ti.com/product/TS5A23157
- [S15] TI, TUSB320: https://www.ti.com/product/TUSB320
- [S16] Analog Devices, MAX17048: https://www.analog.com/en/products/max17048.html
- [S17] FIDO Alliance, CTAP: https://fidoalliance.org/specs/fido-v2.3-ps-20260226/fido-client-to-authenticator-protocol-v2.3-ps-20260226.html
- [S18] Bourns, potenciômetros PTA: https://www.bourns.com/docs/Product-Datasheets/PTA.pdf
- [S19] Kailh, Choc V2: https://www.kailh.net/products/kailh-choc-v2-low-profile-switch-set
- [S20] GCT, USB4105: https://gct.co/connector/usb4105
- [S21] Hirose, microSD: https://www.hirose.com/en/product/p/CL0609-0031-0-00
- [S22] Same Sky, P2: https://www.sameskydevices.com/product/resource/sj-352x-smt.pdf
- [S23] TI, TPS63070: https://www.ti.com/product/TPS63070
- [S24] TI, TPS7A20: https://www.ti.com/product/TPS7A20
- [S25] TI, TPS22918: https://www.ti.com/product/TPS22918
- [S26] TI, TPD2EUSB30: https://www.ti.com/product/TPD2EUSB30
