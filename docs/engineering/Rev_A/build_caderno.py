"""Generate the source-bound CorePad A3 engineering notebook (Rev. A).

Run from repository root with: python3 docs/engineering/Rev_A/build_caderno.py
Only approved project data and inspected repository artifacts appear as facts. The
notebook is deliberately blocked for manufacture wherever evidence is missing.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from collections import defaultdict
from html import escape
import hashlib, json, math, re
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
FONT = OUT / 'fonts'
MM = 72 / 25.4
W, H = 420*MM, 297*MM
M = 16*MM
CONTENT_TOP = H-64*MM
CONTENT_BOTTOM = 43*MM
CONTENT_WIDTH = W-2*M
DATE = '22/11/2026'
REV = 'A'
INK='#1B1E21'; SECOND='#5A5F64'; PALE='#A9A79F'; LINE='#D6D2C8'; GRID='#E2DED5'; PAPER='#EEEAE2'
DARK='#090C11'; PANEL='#161B22'; BORDER='#2A313B'; LIGHT='#C9CDD3'; DARKGRID='#151A21'
GREEN='#55D86A'
for name, file in [('JuraLight','Jura-Light.ttf'),('JuraMedium','Jura-Medium.ttf'),('WorkRegular','WorkSans-Regular.ttf'),('WorkMedium','WorkSans-Medium.ttf'),('GeistRegular','GeistMono-Regular.ttf'),('GeistMedium','GeistMono-Medium.ttf'),('InstrumentItalic','InstrumentSerif-Italic.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(FONT/file)))

FONT_SIZES={'cover':70.9,'cover_sub':20.4,'divider_num':79.4,'divider_title':51.0,'divider_body':23.0,'title':32.6,'title_long':28.3,'title_two':28.9,'right_label':19.6,'subtitle':19.8,'body':19.8,'note':30.6,'table_head':16.6,'table_cell':18.3,'kv':18.4,'diagram':17.4,'diagram_head':16.2,'code':18.1,'caption':16.7,'footer':19.6,'source':16.4,'ruler':16.2}

SOURCES={
'S01': 'Especificacao_Produto_Macropad_Biometrico_Gravador_2026-11-21.md',
'S02': 'README.md',
'S03': 'development/hardware/v0.3.0/README.md',
'S04': 'development/hardware/v0.3.0/BOM_DELTA.md',
'S05': 'development/hardware/v0.3.0/interconnect_24.json',
'S06': 'development/hardware/v0.3.0/ui_drc.txt',
'S07': 'development/hardware/v0.3.0/main_drc.txt',
'S08': 'development/integration/v0.2.0/fit_report.json',
'S09': 'development/integration/v0.2.0/assembly_manifest.json',
'S10': 'development/firmware/corepad.h',
'S11': 'development/firmware/corepad.c',
'S12': 'development/software/PROTOCOL.md',
'S13': 'development/software/wire_protocol.py',
'S14': 'development/software/configurator.py',
'S15': 'development/VALIDATION.md',
'S16': 'docs/ROADMAP.md',
'S17': 'development/hardware/v0.2.0/BOM.md',
'S18': 'development/integration/v0.1.0/LIBERACAO_MANUFATURA.md',
'S19': 'development/integration/v0.2.0/README.md',
'S20': 'CLAUDE.md',
'S21': 'docs/engineering/Rev_A/prompt_origem.txt',
}
FIGURES={
'cover':'beta_blender/Beta_v1.0.1_RGB_verde.png',
'colors_orange':'beta_blender/Beta_v1.0.1_RGB_laranja.png',
'colors_blue':'beta_blender/Beta_v1.0.1_RGB_azul.png',
'ui':'development/hardware/v0.3.0/CorePad_UI_trilhas.png',
'main':'development/hardware/v0.3.0/CorePad_Main_componentes.png',
'assembly':'development/integration/v0.2.0/montagem_PCB_match_v0.2.0.png',
'base':'docs/images/base_interior.png',
'lid':'docs/images/tampa_tecnica.png',
'exploded':'docs/images/pecas_explodidas.png',
'product_top':'beta_blender/Beta_v1.0.0_vista_superior.png',
'product_side':'beta_blender/Beta_v1.0.0_lateral_microSD_P2.png',
'product_rear':'beta_blender/Beta_v1.0.0_traseira_USB-C.png',
}

@dataclass
class Block:
    kind: str
    data: object
    height: float

@dataclass
class Page:
    section: str
    title: str
    dark: bool=False
    blocks: list[Block]=field(default_factory=list)
    used: float=0
    sources: set[str]=field(default_factory=set)
    figure_ids: list[int]=field(default_factory=list)

pages: list[Page]=[]
current: Page|None=None
figure_counter=1  # Cover render is Fig. 1.
pending=[]
sections=[]

def style(font='WorkRegular',size=19.8,leading=None,color=INK,align=TA_LEFT):
    return ParagraphStyle('p',fontName=font,fontSize=size,leading=leading or size*1.42,textColor=HexColor(color),alignment=align,allowWidows=0,allowOrphans=0)

def para(text,width,font='WorkRegular',size=19.8,leading=None,color=INK,align=TA_LEFT):
    p=Paragraph(escape(text).replace('\n','<br/>'),style(font,size,leading,color,align))
    _,h=p.wrap(width,10000)
    return p,h

def new_page(section,title,dark=False):
    global current
    current=Page(section,title,dark)
    pages.append(current)
    return current

def ensure(height):
    global current
    if current is None: raise RuntimeError('no page')
    if current.used+height > CONTENT_TOP-CONTENT_BOTTOM:
        current=new_page(current.section,current.title.removesuffix(' (cont.)')+' (cont.)')
    return current

def add_block(kind,data,height,sources=()):
    pg=ensure(height)
    pg.blocks.append(Block(kind,data,height));pg.used+=height;pg.sources.update(sources)
    return pg

def body(text,sources=()):
    p,h=para(text,CONTENT_WIDTH,size=FONT_SIZES['body'])
    if h>CONTENT_TOP-CONTENT_BOTTOM: raise ValueError('paragraph too long')
    add_block('paragraph',p,h+8,sources)

def subtitle(text,sources=()):
    add_block('subtitle',text,58,sources)

def note(text,sources=()):
    p,h=para(text,CONTENT_WIDTH,font='InstrumentItalic',size=FONT_SIZES['note'],leading=38,color=SECOND)
    add_block('note',p,h+20,sources)

def code(lines,sources=()):
    lines=lines if isinstance(lines,list) else [lines]
    for line in lines:
        p,h=para(line,CONTENT_WIDTH-24,font='GeistRegular',size=FONT_SIZES['code'],leading=27)
        add_block('code',p,h+8,sources)

def placeholder(label,need,sources=()):
    add_block('placeholder',(label,need),100,sources)

def table(headers,rows,widths=None,sources=()):
    if widths is None: widths=[CONTENT_WIDTH/len(headers)]*len(headers)
    else:
        total=sum(widths);widths=[CONTENT_WIDTH*w/total for w in widths]
    def row_height(row,header=False):
        hs=[]
        for i,cell in enumerate(row):
            font='JuraMedium' if header else ('GeistRegular' if i==0 and str(cell).startswith(('REQ-','P-','T-','D-','R-','S')) else 'WorkRegular')
            size=FONT_SIZES['table_head'] if header else FONT_SIZES['table_cell']
            _,h=para(str(cell),widths[i]-16,font,size,leading=size*1.28)
            hs.append(h)
        return max(max(hs)+14, 32.6)
    header_h=row_height(headers,True)
    queue=list(rows)
    first=True
    while queue:
        if current.used+header_h+row_height(queue[0])>CONTENT_TOP-CONTENT_BOTTOM:
            new_page(current.section,current.title.removesuffix(' (cont.)')+' (cont.)')
        chunk=[];height=header_h
        while queue and current.used+height+row_height(queue[0])<=CONTENT_TOP-CONTENT_BOTTOM:
            row=queue.pop(0);chunk.append((row,row_height(row)));height+=chunk[-1][1]
        if not chunk:
            raise ValueError('table row too tall: '+str(queue[0])[:90])
        add_block('table',(headers,chunk,widths,header_h),height+12,sources)
        first=False

def figure(key,caption,sources=(),max_height=380):
    global figure_counter
    path=ROOT/FIGURES[key]
    if not path.exists(): raise FileNotFoundError(path)
    iw,ih=Image.open(path).size
    width=min(CONTENT_WIDTH, max_height*iw/ih)
    height=width*ih/iw
    figure_counter+=1
    num=figure_counter
    cap=f'Fig. {num} - {caption}'
    cp,ch=para(cap,CONTENT_WIDTH,'GeistRegular',FONT_SIZES['caption'],FONT_SIZES['caption']*1.36,SECOND)
    total=height+ch+26
    if total>CONTENT_TOP-CONTENT_BOTTOM:
        raise ValueError('figure too tall '+key)
    pg=add_block('figure',(path,width,height,cp,ch),total,sources)
    pg.figure_ids.append(num)
    return num

def gap(code,topic,owner,next_step):
    pending.append({'id':code,'item':topic,'responsavel':owner,'proximo_passo':next_step})

def section(number,name,opening,source='S01'):
    sections.append((number,name))
    new_page(str(number),name,True)
    add_block('divider',(number,name,opening),CONTENT_TOP-CONTENT_BOTTOM-1,(source,))
    new_page(str(number),name)

# Content begins here. Each paragraph/table row is deliberately bounded for
# high legibility at the mandatory A3 type sizes.
new_page('0','CAPA',True)
add_block('cover',None,CONTENT_TOP-CONTENT_BOTTOM-1,('S01','S02','S21'))
new_page('0','CONTROLE DE REVISÕES')
table(['REVISÃO','DATA','ESCOPO','SITUAÇÃO'],[
['A',DATE,'Primeira consolidação técnica das evidências do repositório.','ESTUDO - fabricação bloqueada.'],
['A DEFINIR','A DEFINIR','Assinaturas de engenharia, qualidade e proprietário.','Pendente de aprovação formal.']],widths=[1,1.3,5,3],sources=('S02','S15'))
body('Este caderno separa VALIDADO (teste ou medição), PROJETADO (CAD e simulação) e HIPÓTESE. “A DEFINIR” não é autorização para suprir dados por interpretação.',('S15','S19'))
body('A marca “CorePad” é nome de projeto. Situação de registro no INPI: A DEFINIR. O produto desenhado é a versão Premium Beta Carbon.',('S01',))
gap('D-001','Situação da marca CorePad no INPI','Gestão de produto','Consultar processo de marca e registrar número, classe e parecer.')
new_page('0','MAPA DO DOCUMENTO')
add_block('toc',None,CONTENT_TOP-CONTENT_BOTTOM-1)
new_page('0','LEGENDA E GLOSSÁRIO')
table(['TERMO','SIGNIFICADO'],[
['VALIDADO','Evidência de teste ou medição registrada; escopo limitado ao ensaio.'],
['PROJETADO','Dimensão ou comportamento derivado de arquivo CAD, desenho ou simulação.'],
['HIPÓTESE','Proposta técnica sem prova experimental ou especificação fechada.'],
['A DEFINIR','Informação ausente; há responsável e próximo passo no registro final.'],
['PCB / PCBA','Placa de circuito impresso / placa com componentes montados.'],
['FFC','Cabo flexível plano entre placas; orientação e dobra ainda não validadas.'],
['ERC / DRC','Checagem de regras elétricas / de regras de desenho de PCB.'],
['EVT / DVT / PVT / MP','Validação de engenharia / desenho / produção / fabricação em série.']],widths=[2.2,7.8],sources=('S03','S15','S16'))

section(1,'VISÃO GERAL DO SISTEMA','O conceito Beta Carbon aprovado orienta o produto; a eletrônica e a mecânica ainda estão em estudo.')
body('CorePad Premium é um macropad USB-C com nove teclas em matriz física 3 × 3, seletor de camadas, biometria, áudio P2 e gravação em microSD. A faixa RGB configurável fica somente na base; a tampa segue o estilo de fibra de carbono, sem filete superior. [S01]',('S01',))
body('Os modos Arquivos e Gravação são exclusivos. A camada protegida depende de autenticação biométrica. A meta de autonomia é de pelo menos 30 h de gravação ambiente, ainda sem prova em hardware. [S01]',('S01',))
figure('product_top','Vista superior Beta: organização visual das teclas e controles; arquivo Blender do projeto. [S02]',('S02',),max_height=390)
new_page('1','ARQUITETURA EM BLOCOS')
figure_counter+=1
add_block('diagram',figure_counter,420,('S01','S03','S10','S12'))
body('O aplicativo desktop atual usa um simulador; não há transporte USB físico. Também não há serviço de nuvem implementado. Transcrição por ferramentas externas é fluxo pretendido, sem integração pronta. [S01, S12]',('S01','S12'))
new_page('1','MODOS E PRIORIDADES')
table(['ESTADO','PRIORIDADE','COMPORTAMENTO','COR / TEMPO'],[
['Falha / bateria baixa','A DEFINIR','Núcleo C pode solicitar finalização de gravação; retorno a estado seguro.','A DEFINIR'],
['Gravação','Exclusivo de Arquivos','Cartão sob controle do aparelho; captura local/remota é requisito.','A DEFINIR'],
['Arquivos','Exclusivo de Gravação','Cartão sob controle do computador; gravação bloqueada.','A DEFINIR'],
['Pronto','A DEFINIR','Teclas comuns e volume disponíveis; camada protegida bloqueada.','A DEFINIR'],
['RGB base','Independente dos LEDs funcionais','Cor configurável pelo software; desligável.','HEX escolhido pelo usuário; tempo A DEFINIR']],widths=[1.7,2.0,4.3,2.0],sources=('S01','S10','S11'))
body('Cores, brilho, animações e temporizações de cada estado funcional ainda não constam em requisito testável. A galeria de cinco cores ilustra a faixa decorativa, não sinalização de estado. [S01, S02]',('S01','S02'))
gap('D-002','Prioridades, HEX, brilho e temporização dos estados','Produto + firmware','Aprovar tabela de estados e verificar no protótipo.')

section(2,'REQUISITOS E ESPECIFICAÇÕES','Toda característica de produção precisa chegar a um teste e a um critério de aceitação.')
table(['ID','REQUISITO','EVIDÊNCIA ATUAL','TESTE DE ACEITAÇÃO'],[
['REQ-001','Nove teclas macro, matriz 3 × 3; contagem exata.','PROJETADO: CAD/PCB UI.','T-001: inspeção dimensional e elétrica.'],
['REQ-002','Três camadas; terceira protegida.','PROJETADO: núcleo C.','T-002: autenticação e bloqueio.'],
['REQ-003','Texto de pelo menos 256 caracteres por tecla.','VALIDADO apenas no simulador.','T-003: entrada HID com acentos.'],
['REQ-004','Faixa RGB inferior configurável por software.','PROJETADO no visual; simulador.','T-004: cor, consumo e persistência.'],
['REQ-005','Mudo físico bloqueia microfone e preserva P2.','HIPÓTESE de circuito.','T-005: medir com firmware travado.'],
['REQ-006','Estados exclusivos Arquivos/Gravação.','VALIDADO no núcleo C em host.','T-006: troca segura com microSD real.'],
['REQ-007','Áudio local/remoto em arquivo por reunião.','HIPÓTESE.','T-007: gravação longa e recuperação.'],
['REQ-008','Autonomia >= 30 h ambiente por carga.','Meta sem medição.','T-008: ensaio de descarga declarado.'],
['REQ-009','Biometria protege credenciais; FIDO2.','HIPÓTESE de arquitetura.','T-009: ameaça e interoperabilidade.'],
['REQ-010','USB-C traseiro; P2 e SD à esquerda.','PROJETADO com choques de caixa.','T-010: montagem e acesso com plug.']],widths=[1.2,4.2,2.4,2.2],sources=('S01','S08','S10','S12','S15'))
new_page('2','ESPECIFICAÇÕES MENSURÁVEIS')
table(['ATRIBUTO','VALOR / UNIDADE','TOLERÂNCIA','ORIGEM / STATUS'],[
['Corpo CAD','104 × 84 × 28,4 mm','A DEFINIR','CAD mecânico 0.1.0; PROJETADO'],
['PCB principal e UI','98 × 78 mm cada','A DEFINIR','KiCad 0.3.0; PROJETADO'],
['Espessura nominal PCB','1,6 mm','A DEFINIR','Projeto KiCad; exportação STEP 1,51 mm'],
['Entre PCBs','6,29 mm','A DEFINIR','STEP/fit report 0.2.0; PROJETADO'],
['Capacidade microSD','até 256 GB','A DEFINIR','Especificação 0.7; requisito'],
['Autonomia','>= 30 h','A DEFINIR','Especificação 0.7; meta, não medida'],
['RGB','cor selecionada no software','A DEFINIR','Especificação 0.7; simulação visual'],
['Temperatura / IP / vibração','A DEFINIR','A DEFINIR','Sem requisito ou teste no projeto']],widths=[2.4,2.5,1.7,3.4],sources=('S01','S03','S08','S19'))
gap('D-003','Tolerâncias dimensionais e ambientais','Mecânica + qualidade','Definir critérios a partir de processo, fornecedores e ensaios.')
new_page('2','ACESSIBILIDADE E LUZ')
body('A faixa RGB usa cores livres no configurador; os três LEDs de camada e o indicador de gravação são sinais funcionais separados. Nenhum arquivo atual define frequência de animação, intensidade luminosa, contraste ou alternativa não cromática. [S01, S03]',('S01','S03'))
body('Fotossensibilidade, brilho máximo, efeitos, desligamento por bateria e interface acessível entram como requisitos de projeto. Limites normativos aplicáveis e protocolo de ensaio: A DEFINIR. Não há certificação obtida. [S01, S16]',('S01','S16'))
figure('colors_orange','Exemplo de cor decorativa laranja no render Beta; não representa estado funcional. [S02]',('S02',),max_height=360)
gap('D-004','Critérios de acessibilidade e efeitos RGB','Produto + qualidade','Definir limites de animação, contraste e ensaio com usuários.')

section(3,'ELETRÔNICA','A revisão KiCad mostra posicionamento e trilhas piloto, não um circuito de produto completo.')
body('A arquitetura candidata usa STM32U5A5ZJT6Q, codec TAC5112IRGER e amplificador TPA6132A2RTER; microSD, USB-C e P2 estão posicionados. Os footprints principais não possuem pinagem de MCU, passivos, proteção ou circuito de carga. [S03, S04]',('S03','S04'))
body('Esquemático completo da principal: A DEFINIR. O único esquema disponível é da interface de bancada 0.2.0, que não substitui a PCB UI do produto. ERC de produção: A DEFINIR. [S15, S18]',('S15','S18'))
figure('main','Footprints candidatos na placa principal; ausência de trilhas funcionais é o estado real. [S03]',('S03',),max_height=400)
new_page('3','INTERLIGAÇÃO ENTRE PLACAS')
table(['PINOS FFC','SINAL / FUNÇÃO','ESTADO'],[
['1–9','KEY1 a KEY9','Seis sinais roteados na UI; KEY4, KEY7, KEY8 abertos.'],
['10–11','LAYER; RECORD','Componentes UI a selecionar.'],
['12–13','MUTE_SENSE; FADER_ADC','Circuitos a selecionar.'],
['14–16','3V3_UI; GND; GND','Corrente e retorno a dimensionar.'],
['17','MUTE_HW_EN','Ação física independente do firmware a provar.'],
['18–20','BIO_UART_TX; BIO_UART_RX; BIO_RESET','Sensor seguro a selecionar.'],
['21–24','LED_LAYER_1/2/3; LED_RECORD','LEDs, resistores e guias a selecionar.']],widths=[1.8,3.7,4.5],sources=('S03','S05'))
body('O conector proposto é Amphenol F32R-1A7H1-11024, 24 vias em passo de 0,5 mm. Orientação, cabo, corrente e raio de dobra não foram validados. RGB da base permanece fora desse FFC. [S03, S05]',('S03','S05'))
gap('D-005','Cabo FFC, orientação e corrente admissível','Hardware + mecânica','Escolher MPN de cabo e validar amostra na montagem real.')
new_page('3','PINAGEM DO CONTROLADOR')
table(['BLOCO','PINO MCU','REDE','OBSERVAÇÃO'],[
['USB composto','A DEFINIR','A DEFINIR','HID, áudio, configuração, arquivos e FIDO2 precisam coexistir.'],
['SDMMC','A DEFINIR','SD_CLK/CMD/D0–D3 candidatos','Provar DMA e simultaneidade.'],
['Áudio digital','A DEFINIR','A DEFINIR','Codec, clock e buffers a fechar.'],
['Biometria','A DEFINIR','BIO_UART_TX/RX/RESET','Segurança de canal não definida.'],
['Mudo físico','A DEFINIR','MUTE_HW_EN','Não depender do programa para cortar captação.'],
['RGB e LEDs','A DEFINIR','A DEFINIR','Corrente, PWM e driver a selecionar.']],widths=[2,2,2.8,3.2],sources=('S03','S16'))
gap('D-006','Pinmap completo do STM32U5A5','Hardware + firmware','Fechar tabela de funções alternativas e revisar colisões de periféricos.')
new_page('3','ALIMENTAÇÃO E CONSUMO')
table(['BLOCO','CANDIDATO','CORRENTE POR ESTADO','STATUS'],[
['Bateria','Li-ion 1S protegida, 2.000 mAh como referência','A DEFINIR','Capacidade não selecionada.'],
['Carga / power path','TI BQ25622, encapsulamento WQFN-HR 18 pinos','A DEFINIR','Footprint e passivos ausentes.'],
['3V3 digital','TI TPS63070RNMR','A DEFINIR','Circuito ausente.'],
['Microfones','TI TPS7A20 2,8 V candidato','A DEFINIR','Circuito ausente.'],
['RGB base','LEDs/driver A DEFINIR','A DEFINIR','Medir em cor/brilho por bateria.'],
['MCU, SD, áudio','MPNs candidatos na BOM 0.2.0','A DEFINIR','Sem orçamento medido.']],widths=[2.4,3.4,2.3,1.9],sources=('S01','S03','S17'))
body('Árvore elétrica, correntes de pico, margens térmicas, autonomia por estado e proteção da célula: A DEFINIR. A meta de 30 h não pode ser inferida da bateria de referência. [S01, S16, S17]',('S01','S16','S17'))
gap('D-007','Orçamento medido de energia e bateria final','Hardware + teste','Medir placa de bancada por estado e dimensionar célula/reguladores.')
new_page('3','SINAIS CRÍTICOS E PROTEÇÕES')
table(['INTERFACE','REGRA ATUAL','FALTA'],[
['USB-C','Par diferencial e referência contínua propostos.','Stack-up do fabricante; impedância, ESD, CC/VBUS.'],
['microSD','Roteamento SDMMC de 4 bits proposto.','Clock, integridade, proteção ESD, consumo.'],
['Áudio','Codec e amplificador candidatos próximos ao P2.','Bias, filtros, retorno, isolamento do mudo.'],
['Biometria','UART e reset reservados no FFC.','Sensor seguro, protocolo autenticado, proteção.'],
['RGB','Controle pela principal/base.','Topologia, corrente, EMC/acústica, temporização.']],widths=[2.2,3.3,4.5],sources=('S03','S16','S17'))
body('Largura de trilha, separação, vias, pontos de teste e temporização só podem ser liberados após esquema, stack-up e ensaios. Valores de 0,15 mm/0,20 mm na UI são do roteador piloto, não regra de compra. [S03]',('S03',))
new_page('3','PCB DE INTERFACE E DRC')
figure('ui','Cobre F.Cu e B.Cu da UI; seis teclas roteadas e três abertas. [S03, S06]',('S03','S06'),max_height=370)
body('DRC UI: 0 violações geométricas, 13 conexões abertas. Switch Choc V2 tem footprint piloto, dependente de amostra física. Não há componentes para seletor, fader, mudo, biometria ou LEDs. [S03, S06]',('S03','S06'))
new_page('3','PCB PRINCIPAL E SAÍDAS')
table(['ENTREGÁVEL','ESTADO','BLOQUEIO'],[
['DRC principal','8 violações; 8 conexões abertas entre pads nomeados.','4 furo/pad USB; 4 serigrafia/borda.'],
['ERC produto','A DEFINIR','Sem esquema completo.'],
['Gerber / furação','A DEFINIR','Sem roteamento/DRC final.'],
['BOM de compra / CPL','A DEFINIR','Faltam passivos, MPNs e componentes UI.'],
['Stack-up / impedância','A DEFINIR','Fornecedor de PCB não selecionado.'],
['Painelização / separação','A DEFINIR','Furos, bordas e fixação não fechados.']],widths=[2.6,3.3,4.1],sources=('S03','S06','S07','S18'))
body('Nenhum arquivo de fabricação deve ser interpretado como liberado. A saída de manufatura virá somente após revisão independente de esquema, layout, montagem e ensaios. [S18]',('S18',))
new_page('3','COMPONENTES CRÍTICOS')
table(['REF.','MPN CANDIDATO','ALTERNATIVA / PREÇO'],[
['SW1–9','Kailh CPG135301D01','Second source e preço datado: A DEFINIR.'],
['J_UI × 2','Amphenol F32R-1A7H1-11024','Cabo compatível e preço: A DEFINIR.'],
['U1','ST STM32U5A5ZJT6Q','Pin-compatible second source: A DEFINIR.'],
['U2','TI TAC5112IRGER','Land pattern e equivalente: A DEFINIR.'],
['U3','TI TPA6132A2RTER','Equivalente: A DEFINIR.'],
['J_USB','GCT USB4105-GF-A','Footprint/altura e choque: corrigir.'],
['J_SD','Hirose DM3AT-SF-PEJM5','Acesso e choque: corrigir.'],
['J_P2','Same Sky SJ-3523-SMT-TR','Centro do plug: corrigir.']],widths=[1.7,4.0,4.3],sources=('S04','S17'))
gap('D-008','BOM completa, second source, estoque e preços datados','Compras + hardware','Cotação por lote após esquemas e MPNs aprovados.')

section(4,'MECÂNICA','O envelope Beta está desenhado, porém os componentes candidatos não encaixam integralmente.')
figure('assembly','Montagem integrada: placas KiCad, caixa, bateria, teclas e envelopes. [S09, S19]',('S09','S19'),max_height=410)
body('O STEP reúne 32 grupos de projeto. Corpos eletrônicos e FFC são reservas, sem STEP certificado de fornecedor. O acabamento “carbono” é visual, não especificação de material. [S01, S09, S19]',('S01','S09','S19'))
new_page('4','LISTA MECÂNICA')
table(['PEÇA','MATERIAL / PROCESSO','COR / ACABAMENTO','MASSA'],[
['P-01 Base','Plástico isolante; PA12/PC+ABS candidatos.','Grafite; faixa RGB na base.','A DEFINIR'],
['P-02 Tampa','Plástico; processo A DEFINIR.','Aparência de fibra de carbono.','A DEFINIR'],
['P-03 Difusor','Translúcido; resina/processo A DEFINIR.','A DEFINIR','A DEFINIR'],
['P-04 Botão camada','Polímero/processo A DEFINIR.','A DEFINIR','A DEFINIR'],
['P-05 Botão gravação','Polímero/processo A DEFINIR.','A DEFINIR','A DEFINIR'],
['P-06 Pés/fixadores','MPN/material A DEFINIR.','A DEFINIR','A DEFINIR']],widths=[1.9,3.6,3.1,1.4],sources=('S01','S18','S19'))
body('Desenhos individuais cotados, GD&T, rugosidade, contração, ensaio de acabamento e fornecedor-alvo: A DEFINIR. Os STL atuais validam apenas volume/topologia de estudo. [S15, S18]',('S15','S18'))
placeholder('FIGURA A DEFINIR · DESENHOS P-01 A P-05','Faltam cotas e tolerâncias por peça, datums, material e processo final para cada desenho de fabricação.',('S18',))
gap('D-009','Material, processo e desenhos liberados de todas as peças','Mecânica + manufatura','Projetar peças com componentes finais e gerar desenhos por peça.')
new_page('4','FOLGAS E INTERFERÊNCIAS')
table(['PAR','NOMINAL / UNIDADE','PIOR CASO','ORIGEM'],[
['PCB nuas × caixa/bateria','0 mm³ de interseção','A DEFINIR','CAD 0.2.0; PROJETADO'],
['USB-C × base','9,828 mm³ de choque','A DEFINIR','CAD 0.2.0; PROJETADO'],
['microSD × base','2,533 mm³ de choque','A DEFINIR','CAD 0.2.0; PROJETADO'],
['P2 centro × abertura','+2,41 mm vertical','A DEFINIR','CAD 0.2.0; PROJETADO'],
['FFC corpos','2,29 mm livres','A DEFINIR','CAD 0.2.0; dobra desconhecida'],
['Bateria topo × PCB principal','2,60 mm livres','A DEFINIR','CAD 0.2.0; célula de reserva'],
['Corpo switch × abertura','2,30 mm por lado','A DEFINIR','CAD 0.2.0; sem keycap final']],widths=[2.7,2.8,1.8,2.7],sources=('S08','S19'))
body('Nenhuma interferência de encaixe foi aprovada como intencional. A passagem do switch pela janela da tampa é funcional, mas a tolerância de curso/retenção não foi verificada. [S19]',('S19',))
new_page('4','BASE E TAMPA')
figure('base','Interior da base de estudo com canais e aberturas; fixação das PCBs não resolvida. [S02]',('S02',),max_height=370)
body('Os bosses existentes terminam em Z=7 mm e não sustentam a placa principal em Z=12,6 mm. Furos de fixação das duas PCBs ainda não foram projetados. [S08, S19]',('S08','S19'))
new_page('4','MONTAGEM EXPLODIDA')
figure('exploded','Explosão das peças plásticas de estudo, sem tolerâncias ou processo final. [S02]',('S02',),max_height=395)
body('Cabos, parafusos, trava da bateria, adesivos, membranas acústicas e vedação: MPN e limites dimensionais A DEFINIR. A configuração de produção requer nova vista explodida com peças fechadas. [S18, S19]',('S18','S19'))

section(5,'INSTRUÇÕES DE MONTAGEM','A sequência é um plano de processo; nenhum torque ou força está aprovado.')
table(['ETAPA','AÇÃO PREVISTA','INSPEÇÃO / FERRAMENTA'],[
['M-01','Conferir peças, lotes e PCBA.','Critérios e gabaritos: A DEFINIR.'],
['M-02','Instalar difusor RGB na base.','Retenção, uniformidade e adesivo: A DEFINIR.'],
['M-03','Fixar bateria protegida e chicote.','Força, alívio de tração, polaridade: A DEFINIR.'],
['M-04','Fixar PCB principal.','Bosses/furos/parafusos inexistentes: BLOQUEADO.'],
['M-05','Inserir FFC e PCB UI.','Orientação e raio de dobra: BLOQUEADO.'],
['M-06','Montar switches, caps, controles e tampa.','Alturas, torque, curso: A DEFINIR.'],
['M-07','Executar teste final e etiquetar.','Fixture/limites/número de série: A DEFINIR.']],widths=[1.3,4.5,4.2],sources=('S08','S18','S19'))
body('Não executar montagem de linha com estes passos. Faltam desenho de cada operação, figura de gabarito, ferramenta, torque, força de prensa e prevenção de montagem invertida. [S18]',('S18',))
for stage,need in [
 ('M-01','Foto e critério visual do recebimento de peças e PCBA.'),
 ('M-02','Vista cotada do difusor, orientação e retenção na base.'),
 ('M-03','Posição da célula, polaridade e alívio de tração do chicote.'),
 ('M-04','Desenho dos bosses, furos e ferramenta de fixação da principal.'),
 ('M-05','Orientação A/B do FFC, dobra admissível e fixação da UI.'),
 ('M-06','Vista de inserção de switches, caps, controles e tampa.'),
 ('M-07','Fixture, conexões, etiqueta e resultado de teste final.')]:
    placeholder('FIGURA A DEFINIR · ETAPA '+stage,need,('S18',))
gap('D-010','Instruções ilustradas, ferramentas, torque e poka-yoke','Manufatura + mecânica','Fechar peças/PCBA e executar piloto de montagem com medições.')

section(6,'FIRMWARE','O código atual é um núcleo portátil de estados, não uma imagem de dispositivo.')
body('O cabeçalho C define estados CP_IDLE, CP_RECORDING, CP_FILES e CP_FAULT, seleção de camada, autenticação declarada por serviço confiável, controle RGB e bateria baixa. Testes em host e compilação de objeto Cortex-M33 foram executados; não há startup, HAL, USB ou imagem gravável. [S10, S11, S15]',('S10','S11','S15'))
table(['FUNÇÃO','ESTADO ATUAL','PENDÊNCIA'],[
['Teclado USB','Não implementado no MCU.','Descritores, HID e layouts.'],
['Áudio / cartão','Estados apenas; sem drivers.','Codec, SDMMC, exFAT, recuperação.'],
['Segurança','Interface de autenticação abstrata.','Sensor, SE, provisionamento, CTAP.'],
['Atualização','A DEFINIR','Bootloader, assinatura, rollback, option bytes.'],
['Memória não volátil','A DEFINIR','Mapa, desgaste, transação, proteção.']],widths=[2.3,3.4,4.3],sources=('S10','S11','S15'))
new_page('6','PROTOCOLO PÚBLICO CPD1')
table(['OFFSET','CAMPO','TAMANHO','ORIGEM / REGRA'],[
['0','Magic “CPD1”','4 bytes','Constante do código.'],
['4','Versão','1 byte','Valor atual 1; simulador.'],
['5','Opcode','1 byte','GET=1, SET=2, CONFIG=0x81, ACK=0x82.'],
['6','ID de requisição','2 bytes','Little-endian; faixa 0–65535.'],
['8','Comprimento payload','2 bytes','Little-endian; até 32768 bytes.'],
['10','JSON UTF-8','N bytes','Configuração pública.'],
['10+N','CRC32','4 bytes','Sobre cabeçalho+payload.']],widths=[1.6,2.3,1.7,4.4],sources=('S12','S13'))
body('Quadros inválidos não alteram o simulador. CRC32 detecta corrupção acidental, sem autenticar host nem cifrar dados. Transporte USB, timeout, retry, erros e persistência no aparelho: A DEFINIR. [S12, S13]',('S12','S13'))
new_page('6','BUILD, GRAVAÇÃO E TESTES')
code(['make -C development/firmware test arm','python3 -m unittest discover -s development/tests -v'],('S15',))
body('O primeiro comando testa o núcleo C em host e compila apenas um objeto ARM Cortex-M33. O segundo executa testes Python de configuração, RF64 e enquadramento. Versões exatas de toolchain, gravador, firmware assinado, procedimento de flash e hardware-in-the-loop: A DEFINIR. [S15]',('S15',))
gap('D-011','Firmware inicializável e procedimento de gravação','Firmware + segurança','Criar projeto de placa, bootloader, imagem e ensaio em protótipo.')

section(7,'SOFTWARE E APP','O configurador existe para desenvolvimento local, sem conexão física com CorePad.')
body('O aplicativo Python/Tkinter edita 18 macros comuns em duas camadas, escolhe HEX RGB e brilho, salva/carrega JSON UTF-8 e aplica a configuração a um simulador em memória. A camada secreta não é exportada por este editor. [S12, S14]',('S12','S14'))
table(['INTEGRAÇÃO','SITUAÇÃO','PRÓXIMO PASSO'],[
['USB físico','A DEFINIR','Escolher interface e implementar transporte.'],
['Autenticação app/dispositivo','A DEFINIR','Modelo de ameaça e comandos permitidos.'],
['Logs/diagnóstico','A DEFINIR','Definir dados, retenção e consentimento.'],
['Atualização do app','A DEFINIR','Empacotar, assinar e testar sistemas.'],
['Nuvem / transcrição','Sem serviço implementado.','Definir fluxo externo e privacidade.']],widths=[2.4,3.2,4.4],sources=('S01','S12','S14'))
gap('D-012','Distribuição, diagnóstico e privacidade do app','Software + produto','Definir sistemas-alvo, política de dados e instaladores.')

section(8,'MANUAL DE OPERAÇÃO','Uso final só pode ser publicado após validação de hardware e segurança.')
body('Uso pretendido: ligar por USB-C; selecionar camada no botão separado; acionar uma das nove teclas; configurar macros comuns e cor da faixa RGB no aplicativo; operar o cartão por estados exclusivos Arquivos e Gravação. Esses fluxos são requisitos e protótipos de software, não instruções testadas no produto. [S01, S12, S14]',('S01','S12','S14'))
table(['SINTOMA','CAUSA POSSÍVEL','AÇÃO ATUAL'],[
['Configuração não chega ao aparelho','USB físico não implementado.','Usar apenas simulador de desenvolvimento.'],
['MicroSD não aparece','Estado de propriedade desconhecido.','Procedimento de produto A DEFINIR.'],
['Sem som no P2','Circuito não fabricado.','Diagnóstico de produto A DEFINIR.'],
['Biometria não libera','Cadeia segura não selecionada.','Não inserir credenciais reais.'],
['RGB não altera no aparelho','Driver físico não implementado.','Testar somente a simulação.']],widths=[2.6,3.5,3.9],sources=('S01','S12','S15'))
body('Primeiro uso, limpeza, manutenção, troca de bateria/cartão e solução de falhas do produto real: A DEFINIR após EVT. [S16]',('S16',))
gap('D-013','Manual final de usuário e manutenção','Produto + suporte','Validar protótipo e redigir instruções ensaiadas com usuários.')

section(9,'TESTE DE PRODUÇÃO E QUALIDADE','Sem PCBA liberada não existe fixture de linha nem limite de passa/falha.')
table(['TESTE','ESTADO','CRITÉRIO / REGISTRO'],[
['T-001 Teclas','Planejado.','Todas as 9 entradas; limite elétrico A DEFINIR.'],
['T-004 RGB','Planejado.','HEX, corrente, brilho e uniformidade A DEFINIR.'],
['T-005 Mudo','Planejado.','Corte local com firmware travado; P2 preservado.'],
['T-006 Cartão','Planejado.','Exclusividade, retirada segura, arquivo recuperável.'],
['T-008 Autonomia','Planejado.','Meta >= 30 h; condições e amostra A DEFINIR.'],
['T-009 Segurança','Planejado.','Ataque de sensor falso e interoperabilidade.']],widths=[2.3,2.0,5.7],sources=('S01','S16','S18'))
body('Recebimento, AQL, serial, lote, calibração, registro de teste e rastreio: A DEFINIR. Nenhum produto foi inspecionado em linha. [S15, S18]',('S15','S18'))
placeholder('FIGURA A DEFINIR · FIXTURE DE TESTE','Faltam posição dos pontos de teste, conectores, gabarito e disposição da etiqueta/serial.',('S18',))
gap('D-014','Fixture, AQL, limites de teste e rastreabilidade','Qualidade + manufatura','Criar plano de controle após EVT e executar piloto PVT.')
new_page('9','PLANO DVT E PVT')
table(['ENSAIO','CONDIÇÃO / LIMITE','EVIDÊNCIA'],[
['Térmico / carga','A DEFINIR','Sem protótipo.'],
['Queda / vibração','A DEFINIR','Sem protótipo.'],
['Tração USB e FFC','A DEFINIR','Sem conjunto fechado.'],
['ESD / EMC','A DEFINIR','Sem circuito final.'],
['Vida útil das teclas/controles','A DEFINIR','Amostra e ciclo a definir.'],
['Áudio e microfones','A DEFINIR','Ruído, fala e mudo a medir.'],
['Bateria e armazenamento','30 h como meta; método A DEFINIR','Sem ensaio.']],widths=[3,4,3],sources=('S01','S16','S18'))

section(10,'CONFORMIDADE E SEGURANÇA','Considerações e plano: nenhuma certificação foi obtida.')
table(['TEMA','PLANO','STATUS'],[
['EMC / ESD','Definir mercados e normas; pré-conformidade com PCB final.','A DEFINIR'],
['Segurança elétrica / bateria','Analisar carregador, célula, proteção e transporte.','A DEFINIR'],
['RoHS / REACH','Obter declarações da cadeia de fornecimento.','A DEFINIR'],
['USB-IF','Revisar descritores, conector, energia e testes aplicáveis.','A DEFINIR'],
['Acessibilidade','Definir luz, contraste, fotossensibilidade e operação tátil.','A DEFINIR'],
['Marcação / etiquetas','Mercados, símbolos e conteúdo legal a definir.','A DEFINIR']],widths=[2.6,5.2,2.2],sources=('S01','S16','S18'))
gap('D-015','Mercados e plano normativo aplicável','Produto + qualidade','Selecionar regiões de venda e contratar avaliação normativa.')

section(11,'GESTÃO DE PRODUTO','A linha Beta é a direção visual escolhida; o desenho de produção permanece em aberto.')
table(['DISCIPLINA','FASE ATUAL','CRITÉRIO PARA EVOLUIR'],[
['Eletrônica','Pré-EVT','Esquema, pinmap, DRC, protótipo.'],
['Mecânica','Pré-EVT','Eliminar choques, fixações, tolerâncias.'],
['Firmware','Pré-EVT','Imagem executável no hardware.'],
['Software','Simulador','Transporte USB e instalação.'],
['Qualidade','Plano inicial','DVT/PVT com limites e registros.'],
['MP','Não iniciada','Liberação formal após PVT.']],widths=[2.3,2.5,5.2],sources=('S15','S16','S18'))
new_page('11','CUSTO E SUPRIMENTOS')
table(['ITEM','LOTE / CUSTO','FONTE'],[
['BOM eletrônica','A DEFINIR','MPNs ainda candidatos.'],
['BOM mecânica','A DEFINIR','Material/processo não liberados.'],
['Montagem e teste','A DEFINIR','Fixture e tempo de linha ausentes.'],
['Embalagem/frete/impostos','A DEFINIR','Mercados e embalagem ausentes.'],
['Preço-alvo e margem','A DEFINIR','Entrada de negócio em branco.'],
['MOQ / lead time / alternativos','A DEFINIR','Sem cotações datadas.']],widths=[3.2,2.8,4.0],sources=('S04','S17','S18'))
gap('D-016','Preço, custo por lote e cadeia de suprimentos','Gestão de produto + compras','Solicitar cotações datadas após BOM/mercados fechados.')
new_page('11','RISCOS E DECISÕES')
table(['RISCO / DECISÃO','PROB. × IMPACTO','MITIGAÇÃO / DONO'],[
['R-01 Pinos MCU concorrentes','A DEFINIR','Matriz de pinagem; hardware.'],
['R-02 USB/SD colidem com caixa','A DEFINIR','Redesenhar portas; mecânica.'],
['R-03 P2 acima da abertura','A DEFINIR','Jack baixo/placa auxiliar; hardware+mecânica.'],
['R-04 FFC e suportes ausentes','A DEFINIR','Protótipo de montagem; mecânica.'],
['R-05 Biometria simulável','A DEFINIR','Sensor autenticado; segurança.'],
['R-06 Mudo não independente','A DEFINIR','Circuito fail-safe; hardware.'],
['R-07 30 h não atingidas','A DEFINIR','Medição por estado; hardware.']],widths=[3.5,2.1,4.4],sources=('S03','S08','S16'))
new_page('11','REGISTRO DE DECISÕES')
table(['DATA','DECISÃO','ORIGEM / IMPACTO'],[
['21/11/2026','Nove teclas em 3 × 3 e biometria visível.','Especificação 0.7; layout físico.'],
['22/11/2026','Beta em estilo carbono; sem linha verde superior.','Especificação 0.7; visual.'],
['22/11/2026','Faixa RGB difusa somente na base, cor por software.','Especificação 0.7; óptica/energia.'],
['22/11/2026','Revisão PCB 0.3.0 com FFC 24 vias proposto.','Engenharia; não aprovado para compra.']],widths=[1.8,4.7,3.5],sources=('S01','S03'))
body('Marcos com datas, prazos das decisões abertas e responsável nominal: A DEFINIR. Próxima revisão: corrigir portas/suportes, fechar esquema e evidência de bancada antes de rotear a principal. [S16]',('S16',))

section(12,'EMBALAGEM E LOGÍSTICA','O produto ainda não tem configuração de fornecimento nem desenho de embalagem.')
table(['ITEM','SITUAÇÃO','AÇÃO'],[
['Conteúdo da caixa','A DEFINIR','Escolher cabo, cartão, guia e acessórios.'],
['Material / dimensões','A DEFINIR','Desenhar embalagem após dimensão final.'],
['Etiqueta / códigos','A DEFINIR','Definir serial, lote e mercados.'],
['Proteção de transporte','A DEFINIR','Ensaio de queda e vibração.'],
['Bateria em transporte','A DEFINIR','Revisar normas do mercado selecionado.']],widths=[3.0,2.0,5.0],sources=('S18',))
gap('D-017','Embalagem, etiqueta e logística','Produto + manufatura','Definir conteúdo e mercados após desenho fechado.')
gap('D-018','VID:PID, descritores USB e classes efetivas','Firmware + produto','Definir identidade USB e provar composição em hardware.')
gap('D-019','Mapa de memória não volátil e option bytes','Firmware + segurança','Projetar armazenamento, boot e provisionamento; ensaiar recuperação.')
gap('D-020','Timeouts, retries e códigos de erro do CPD1 físico','Firmware + software','Implementar transporte USB e testar falhas de comunicação.')
gap('D-021','Formato final do arquivo de gravação e temporização SD/áudio','Firmware + áudio','Ensaiar codec e cartão com gravação longa recuperável.')
gap('D-022','Brilho, efeitos e consumo da faixa RGB','Hardware + produto','Selecionar LEDs/driver e medir cor, corrente e uniformidade.')
gap('D-023','Temperatura, vibração, grau de proteção e vida útil','Qualidade + mecânica','Definir ambiente de uso e ensaios DVT com limites.')
gap('D-024','Stack-up PCB, impedâncias, Gerber/furação e painelização','Hardware + fabricante PCB','Fechar esquema/layout e revisar pacote com fornecedor.')
gap('D-025','Pontos de teste e circuito de programação','Hardware + manufatura','Adicionar acesso de fixture após pinmap e revisar DFT.')
gap('D-026','Alternativas qualificadas e disponibilidade dos críticos','Compras + hardware','Cotação datada, amostras e revalidação elétrica/mecânica.')
gap('D-027','Geometria e segurança do módulo biométrico final','Segurança + mecânica','Escolher sensor autenticado e validar encaixe e ameaça.')

section(13,'ANEXOS E RASTREABILIDADE','Os arquivos de origem acompanham o PDF e permitem reconstruir cada conclusão.')
table(['FAMÍLIA','FONTE NO REPOSITÓRIO','USO'],[
['Requisito','S01: especificação 0.7','Decisões do proprietário.'],
['Hardware','S03–S07, S17','PCB, pinos, BOM e DRC.'],
['Mecânica','S08–S09, S18–S19','STEP, choque, manufatura.'],
['Firmware','S10–S11, S15','Estados, validação.'],
['Software','S12–S14','Protocolo e configurador.'],
['Gestão','S16, S20','Roteiro e continuidade.']],widths=[2,5,3],sources=('S01','S03','S08','S15'))
body('Relatórios completos ERC/DRC, CPL, Gerbers, folhas de esquemático, logs físicos, datasheets congelados, prompt de origem e caderno de conceito em PDF não compõem este pacote de produção. Os itens existentes são listados no mapa de fontes ao fim. [S18]',('S18',))
new_page('13','MAPA DE FONTES')
source_rows=[]
for sid,path in SOURCES.items():
 source_rows.append([sid,path,'SHA-256 no manifesto digital'])
table(['ID','CAMINHO','CONTROLE'],source_rows,widths=[1.0,7.0,2.0])
new_page('13','PENDÊNCIAS A DEFINIR')
table(['ID','ITEM','RESPONSÁVEL / PRÓXIMO PASSO'],[[x['id'],x['item'],x['responsavel']+' - '+x['proximo_passo']] for x in pending],widths=[1.0,3.6,5.4])
new_page('13','CRITÉRIO DE LIBERAÇÃO')
note('A fabricação permanece bloqueada. Este caderno é uma linha de base de engenharia, não um pacote de produção.',('S15','S18'))
body('Para liberar o produto, o terceiro ainda precisa receber esquema pino a pino, PCB sem violações não justificadas, Gerbers/furação/BOM/CPL, modelos e desenhos mecânicos finais, firmware gravável, fixture/limites de teste, instruções de montagem ensaiadas e conformidade aplicável. [S16, S18]',('S16','S18'))
body('Os valores “A DEFINIR” são decisões ou medições pendentes. O registro final associa cada uma a um responsável funcional e ao próximo passo. Revisão formal requer assinatura de responsáveis e atualização do histórico. [S18]',('S18',))

# Source manifest is part of the reproducibility package.
manifest={sid:{'path':path,'sha256':hashlib.sha256((ROOT/path).read_bytes()).hexdigest()} for sid,path in SOURCES.items()}
(OUT/'source_manifest.json').write_text(json.dumps({'revision':REV,'date':DATE,'sources':manifest,'figures':FIGURES},indent=2,ensure_ascii=False)+'\n')

# Page lookup for the two-pass TOC and total footer.
section_pages={}
for i,pg in enumerate(pages,1):
    if pg.dark and pg.section not in ('0',) and pg.section not in section_pages:
        section_pages[pg.section]=i

c=canvas.Canvas(str(OUT/'CorePad_Caderno_de_Engenharia_Rev_A.pdf'),pagesize=(W,H),pageCompression=1)
c.setTitle('CorePad - Caderno de Engenharia - Revisão A')
c.setAuthor('Projeto CorePad')

def text_with_tracking(x,y,text,font,size,tracking,color,align='left'):
    c.saveState()
    c.setFillColor(HexColor(color));t=c.beginText();t.setFont(font,size);t.setCharSpace(tracking)
    tw=pdfmetrics.stringWidth(text,font,size)+max(0,len(text)-1)*tracking
    if align=='right':x-=tw
    if align=='center':x-=tw/2
    t.setTextOrigin(x,y);t.textOut(text);c.drawText(t)
    c.restoreState()
    return tw

def form_background(dark):
    name='DARK_BG' if dark else 'LIGHT_BG'
    c.beginForm(name,0,0,W,H)
    c.setFillColor(HexColor(DARK if dark else PAPER));c.rect(0,0,W,H,fill=1,stroke=0)
    c.setFillColor(HexColor(DARKGRID if dark else GRID))
    radius=.07*MM
    for ix in range(0,85):
        x=ix*5*MM
        for iy in range(0,60):
            c.circle(x,iy*5*MM,radius,fill=1,stroke=0)
    c.setStrokeColor(HexColor(BORDER if dark else PALE));c.setLineWidth(.35)
    for x,dx in ((M,-1),(W-M,1)):
        for y,dy in ((M,-1),(H-M,1)):
            c.line(x,y,x+dx*5*MM,y);c.line(x,y,x,y+dy*5*MM)
    c.endForm()
    return name
light_bg=form_background(False);dark_bg=form_background(True)

def page_frame(pg,index,total):
    c.doForm(dark_bg if pg.dark else light_bg)
    fg=LIGHT if pg.dark else INK;sec=LIGHT if pg.dark else SECOND;rule=BORDER if pg.dark else LINE
    # Millimetre ruler, exact tick spacings from the requested system.
    y=H-16*MM
    c.setStrokeColor(HexColor(BORDER if pg.dark else SECOND));c.setLineWidth(.38)
    for i in range(0,389):
        x=M+i*MM
        l=(2.6 if i%10==0 else 1.6 if i%5==0 else .8)*MM
        c.line(x,y,x,y-l)
    for mm_pos in range(0,389,50):
        text_with_tracking(M+mm_pos*MM,y-7.1*MM,str(mm_pos),'GeistRegular',FONT_SIZES['ruler'],0,PALE)
    if not pg.dark:
        title=pg.title.upper();label='METROLOGIA LUMINOSA'
        tw=pdfmetrics.stringWidth(title,'JuraLight',FONT_SIZES['title'])+max(0,len(title)-1)*(.9*MM)
        if tw<750:
            text_with_tracking(M,H-38.5*MM,title,'JuraLight',FONT_SIZES['title'],.9*MM,INK)
        else:
            size=FONT_SIZES['title_long'];track=.4*MM
            words=title.split();lines=['']
            for w in words:
                test=(lines[-1]+' '+w).strip()
                width=pdfmetrics.stringWidth(test,'JuraLight',size)+max(0,len(test)-1)*track
                if width>750 and lines[-1]:lines.append(w)
                else:lines[-1]=test
            for n,line in enumerate(lines[:2]):text_with_tracking(M,H-(38.5+n*13)*MM,line,'JuraLight',size,track,INK)
        text_with_tracking(W-M,H-38.5*MM,label,'JuraMedium',FONT_SIZES['right_label'],.6*MM,SECOND,'right')
        c.setStrokeColor(HexColor(SECOND));c.setLineWidth(1);c.line(M,H-47*MM,M+23*MM,H-47*MM)
    # Source note stays above the footer divider.
    if pg.sources and not pg.dark:
        txt='Fonte: '+', '.join(sorted(pg.sources))+'; detalhes no mapa de fontes.'
        sp,sh=para(txt,CONTENT_WIDTH,'GeistRegular',FONT_SIZES['source'],FONT_SIZES['source']*1.34,SECOND)
        if sh>38: raise ValueError('source note too long on '+pg.title)
        sp.drawOn(c,M,89)
    c.setStrokeColor(HexColor(rule));c.setLineWidth(.14*MM);c.line(M,M+9*MM,W-M,M+9*MM)
    left=f'{index:02d} / {total}'
    center='COREPAD · CADERNO DE ENGENHARIA · REV. A'
    right=pg.title.upper()
    leftw=text_with_tracking(M,M+1.8*MM,left,'GeistRegular',FONT_SIZES['footer'],0,fg)
    centerw=pdfmetrics.stringWidth(center,'JuraMedium',FONT_SIZES['footer'])+(len(center)-1)*(.45*MM)
    cx=W/2;center_left=cx-centerw/2;center_right=cx+centerw/2
    if M+leftw+18>center_left: raise ValueError('footer left collision')
    max_right=W-M-center_right-18
    while right and pdfmetrics.stringWidth(right,'JuraMedium',FONT_SIZES['footer'])+(len(right)-1)*(.35*MM)>max_right:
        right=right[:-2].rstrip(' .')+'…'
    text_with_tracking(cx,M+1.8*MM,center,'JuraMedium',FONT_SIZES['footer'],.45*MM,sec,'center')
    text_with_tracking(W-M,M+1.8*MM,right,'JuraMedium',FONT_SIZES['footer'],.35*MM,fg,'right')

def draw_table(block,y):
    headers,chunk,widths,hh=block.data
    x=M
    c.setStrokeColor(HexColor(SECOND));c.setLineWidth(1.2)
    for i,head in enumerate(headers):
        p,_=para(str(head).upper(),widths[i]-16,'JuraMedium',FONT_SIZES['table_head'],FONT_SIZES['table_head']*1.25,SECOND)
        p.drawOn(c,x+8,y-hh+8)
        x+=widths[i]
    y-=hh;c.line(M,y,W-M,y)
    c.setStrokeColor(HexColor(LINE));c.setLineWidth(.5)
    for row,rh in chunk:
        x=M
        for i,cell in enumerate(row):
            font='GeistRegular' if i==0 and str(cell).startswith(('REQ-','P-','T-','D-','R-','S')) else ('WorkMedium' if str(cell).startswith('ESTUDO - fabricação bloqueada.') else 'WorkRegular')
            p,_=para(str(cell),widths[i]-16,font,FONT_SIZES['table_cell'],FONT_SIZES['table_cell']*1.28)
            p.drawOn(c,x+8,y-rh+8)
            x+=widths[i]
        y-=rh;c.line(M,y,W-M,y)
    return y-12

def draw_diagram(y,num):
    # All links and modules come from S01/S03/S10/S12.
    boxes=[(M+10,y-120,280,92,'INTERFACE UI','9 teclas · FFC 24 vias'),
           (M+390,y-120,300,92,'PLACA PRINCIPAL','MCU · áudio · microSD'),
           (M+790,y-120,280,92,'COMPUTADOR','USB · configurador local'),
           (M+120,y-310,320,92,'BASE','Bateria · faixa RGB'),
           (M+610,y-310,350,92,'SERVIÇOS EXTERNOS','Transcrição: fluxo pretendido')]
    c.setStrokeColor(HexColor(SECOND));c.setLineWidth(1.1)
    for x,by,bw,bh,head,detail in boxes:
        c.setFillColor(HexColor(PAPER));c.roundRect(x,by,bw,bh,8,fill=1,stroke=1)
        text_with_tracking(x+bw/2,by+bh-29,head,'JuraMedium',FONT_SIZES['diagram_head'],.35*MM,SECOND,'center')
        p,ph=para(detail,bw-24,'WorkRegular',FONT_SIZES['diagram'],FONT_SIZES['diagram']*1.35,INK,TA_CENTER)
        p.drawOn(c,x+12,by+12)
    for a,b in [((M+290,y-74),(M+390,y-74)),((M+690,y-74),(M+790,y-74)),((M+440,y-264),(M+540,y-200)),((M+740,y-264),(M+690,y-200))]:
        c.line(*a,*b)
    p,ph=para(f'Fig. {num} - Diagrama funcional derivado da especificação e do código existente. Nuvem não implementada. [S01, S03, S10, S12]',CONTENT_WIDTH,'GeistRegular',FONT_SIZES['caption'],FONT_SIZES['caption']*1.36,SECOND)
    p.drawOn(c,M,y-390)

def draw_cover():
    img=ROOT/FIGURES['cover']
    iw,ih=Image.open(img).size
    x=W*0.52;y=H*.18;mw=W*.43;mh=H*.64
    scale=min(mw/iw,mh/ih)
    dw,dh=iw*scale,ih*scale
    c.setFillColor(HexColor(PANEL));c.roundRect(x-20,y-20,mw+40,mh+40,10,fill=1,stroke=0)
    c.drawImage(ImageReader(str(img)),x+(mw-dw)/2,y+(mh-dh)/2,width=dw,height=dh)
    text_with_tracking(M+10,H-87*MM,'COREPAD','JuraLight',FONT_SIZES['cover'],4.5*MM,LIGHT)
    text_with_tracking(M+10,H-112*MM,'CADERNO DE ENGENHARIA','JuraMedium',FONT_SIZES['cover_sub'],0,LIGHT)
    text_with_tracking(M+10,H-123*MM,'METROLOGIA LUMINOSA','JuraMedium',FONT_SIZES['cover_sub'],0,LIGHT)
    text_with_tracking(M+10,H-150*MM,'BETA CARBON · VERSÃO PREMIUM','GeistRegular',FONT_SIZES['footer'],0,LIGHT)
    text_with_tracking(M+10,H-165*MM,'REV. A · '+DATE,'GeistMedium',FONT_SIZES['footer'],0,LIGHT)
    text_with_tracking(M+10,H-205*MM,'ESTUDO DE ENGENHARIA','JuraMedium',23,.4*MM,LIGHT)
    text_with_tracking(M+10,H-217*MM,'FABRICAÇÃO BLOQUEADA','JuraMedium',23,.4*MM,LIGHT)
    text_with_tracking(M+10,H-230*MM,'Fig. 1 - Render Beta 1.0.1. [S02]','GeistRegular',FONT_SIZES['caption'],0,LIGHT)

def draw_divider(data):
    num,name,opening=data
    roman={1:'I',2:'II',3:'III',4:'IV',5:'V',6:'VI',7:'VII',8:'VIII',9:'IX',10:'X',11:'XI',12:'XII',13:'XIII'}[int(num)]
    text_with_tracking(M+10,H-90*MM,roman,'JuraLight',FONT_SIZES['divider_num'],5*MM,LIGHT)
    title=name.upper()
    tw=pdfmetrics.stringWidth(title,'JuraLight',FONT_SIZES['divider_title'])+(len(title)-1)*1.4*MM
    if tw>W-2*M-40:
        # Split across two exact-size lines rather than shrinking.
        words=title.split();mid=len(words)//2;lines=[' '.join(words[:mid]),' '.join(words[mid:])]
    else:lines=[title]
    for i,line in enumerate(lines):text_with_tracking(M+10,H-(128+i*23)*MM,line,'JuraLight',FONT_SIZES['divider_title'],1.4*MM,LIGHT)
    line_y=H-(137+(len(lines)-1)*23)*MM
    c.setStrokeColor(HexColor(GREEN));c.setLineWidth(1*MM);c.line(M+10,line_y,M+70*MM,line_y)
    p,ph=para(opening,700,'WorkRegular',FONT_SIZES['divider_body'],FONT_SIZES['divider_body']*1.42,LIGHT)
    p.drawOn(c,M+10,line_y-45-ph)
    text_with_tracking(M+10,31.5*MM,f'COREPAD · REV. A · {DATE}','JuraMedium',FONT_SIZES['footer'],.6*MM,LIGHT)

for index,pg in enumerate(pages,1):
    page_frame(pg,index,len(pages))
    y=CONTENT_TOP
    for block in pg.blocks:
        if block.kind=='cover':draw_cover()
        elif block.kind=='divider':draw_divider(block.data)
        elif block.kind=='toc':
            items=[('0','CAPA / CONTROLE / GLOSSÁRIO',1)]+[(str(n),name,section_pages[str(n)]) for n,name in sections]
            half=math.ceil(len(items)/2)
            for col,group in enumerate((items[:half],items[half:])):
                x=M+col*(CONTENT_WIDTH/2+10)
                yy=CONTENT_TOP-15
                for number,name,page_no in group:
                    text_with_tracking(x,yy,number.zfill(2),'GeistRegular',FONT_SIZES['table_cell'],0,SECOND)
                    p,ph=para(name,CONTENT_WIDTH/2-140,'WorkRegular',FONT_SIZES['table_cell'],FONT_SIZES['table_cell']*1.26)
                    p.drawOn(c,x+50,yy-ph+17)
                    text_with_tracking(x+CONTENT_WIDTH/2-30,yy,str(page_no).zfill(2),'GeistRegular',FONT_SIZES['table_cell'],0,INK,'right')
                    yy-=max(55,ph+14)
        elif block.kind=='paragraph':
            h=block.height-8;block.data.drawOn(c,M,y-h);y-=block.height
        elif block.kind=='subtitle':
            text_with_tracking(M,y-28,block.data.upper(),'JuraMedium',FONT_SIZES['subtitle'],.45*MM,INK);y-=block.height
        elif block.kind=='note':
            h=block.height-20;block.data.drawOn(c,M,y-h);y-=block.height
        elif block.kind=='code':
            h=block.height-8;block.data.drawOn(c,M+24,y-h);y-=block.height
        elif block.kind=='placeholder':
            label,need=block.data
            c.setStrokeColor(HexColor(SECOND));c.setLineWidth(.6)
            c.roundRect(M,y-86,CONTENT_WIDTH,82,6,fill=0,stroke=1)
            text_with_tracking(M+3*MM,y-30,label,'JuraMedium',17.9,.45*MM,INK)
            p,ph=para(need,CONTENT_WIDTH-6*MM,'WorkRegular',17.4,17.4*1.35,SECOND)
            p.drawOn(c,M+3*MM,y-40-ph)
            y-=block.height
        elif block.kind=='table':y=draw_table(block,y)
        elif block.kind=='figure':
            path,bw,bh,cp,ch=block.data
            x=M+(CONTENT_WIDTH-bw)/2
            c.drawImage(ImageReader(str(path)),x,y-bh,width=bw,height=bh,mask='auto')
            cp.drawOn(c,M,y-bh-ch-10)
            y-=block.height
        elif block.kind=='diagram':draw_diagram(y,block.data);y-=block.height
        else:raise ValueError(block.kind)
    if y<CONTENT_BOTTOM-1 and pg.blocks[0].kind not in ('cover','divider','toc'):
        raise ValueError(f'content overflow page {index}: {pg.title}: {y}')
    c.showPage()
c.save()

report={
 'document':'CorePad - Caderno de Engenharia - Rev. A',
 'date':DATE,'pages':len(pages),
 'page_size_mm':[420,297],
 'pdf_bytes':(OUT/'CorePad_Caderno_de_Engenharia_Rev_A.pdf').stat().st_size,
 'sections':{name:{'start':section_pages[str(n)],'end':(section_pages.get(str(n+1),len(pages)+1)-1)} for n,name in sections},
 'font_sizes_pt':FONT_SIZES,
 'figures':figure_counter,
 'a_definir':pending,
 'release':'BLOQUEADA: estudo de engenharia sem esquemas e saídas de fabricação completos.'}
(OUT/'relatorio_geracao.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
lines=[
    '# Relatório de geração - CorePad Rev. A','',
    f"- Páginas: {report['pages']}",
    '- Formato: A3 paisagem, 420 × 297 mm',
    f"- Tamanho do PDF: {report['pdf_bytes']/1024/1024:.2f} MiB",
    f"- Figuras numeradas: {report['figures']}",
    f"- Grupos de pendências A DEFINIR: {len(pending)}",'',
    '## Seções e páginas','',
]
for name,span in report['sections'].items():
    lines.append(f"- {name}: {span['start']}–{span['end']}")
lines.extend(['','## Tamanhos de fonte (pt)',''])
for name,size in FONT_SIZES.items():lines.append(f'- {name}: {size}')
lines.extend(['','## Pendências A DEFINIR',''])
for item in pending:
    lines.append(f"- **{item['id']} {item['item']}** — {item['responsavel']}. Próximo passo: {item['proximo_passo']}")
lines.extend(['','**Liberação de fabricação: BLOQUEADA.**',''])
(OUT/'relatorio_final.md').write_text('\n'.join(lines))
print(json.dumps({'pages':len(pages),'bytes':report['pdf_bytes'],'figures':report['figures'],'pending':len(pending)},ensure_ascii=False))
