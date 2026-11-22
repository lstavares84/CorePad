"""Alpha 0.1.0: cálculo e posicionamento preliminar. NÃO gera placa fabricável."""
from pathlib import Path
import csv, json, os
os.environ.setdefault('MPLCONFIGDIR','/tmp/alpha-mpl')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle
import pcbnew as p

ROOT=Path(__file__).resolve().parent

def csvfile(name, headers, rows):
    with (ROOT/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f,delimiter=';');w.writerow(headers);w.writerows(rows)

bom=[
('U1',1,'Controle','STM32U5A5ZJT6Q','ST','LQFP144 20x20','Candidato principal','Pinagem e SMPS interno a validar','S03'),
('U2',1,'Conversor áudio','TAC5112IRGER','TI','VQFN24 RGE0024R','Candidato principal','Desenho de soldagem específico ainda não implementado','S04'),
('U3',1,'Amplificador P2','TPA6132A2RTER','TI','WQFN16','Candidato principal','Ganho; acoplamento de entrada; carga real','S06'),
('MIC1 MIC2',2,'Captação','IM73A135V01XTSA1','Infineon','MEMS 4x3x1.2','Candidato principal','Dutos acústicos e alimentação <=3.0 V','S05'),
('U4 U5',2,'Mudo analógico','TS5A23157DGS(R)','TI','VSSOP10','Família/embalagem a fechar','Comutação em hardware; referência e transitórios','S14'),
('U6',1,'Segurança','SE050C2HQ1/Z01SD','NXP','HX2QFN20','Candidato principal','Provisionamento e canal autenticado; não é FIDO2 pronto','S08'),
('BIO1',1,'Biometria bancada','4750','Adafruit','Módulo redondo 20.8 mm','Somente desenvolvimento','Sem comprovação de canal autenticado; estoque pendente','S09'),
('U7',1,'Carregador','BQ25622','TI','WQFN-HR18 2.5x3','Família; sufixo a fechar','CE bloqueado até configuração; termistor na célula','S10'),
('U8',1,'Regulador principal 3V3','TPS63070RNMR','TI','VQFN-HR15','Candidato principal','Indutor e estabilidade; consumo real; capacidade de pico SD','S23'),
('U9',1,'Regulador microfones','TPS7A20 2.8 V','TI','Sufixo/encapsulamento a fechar','Família','Somente cápsulas; codec AVDD 3.3V separado e filtrado','S24'),
('U10',1,'Medidor bateria','MAX17048','Analog Devices','Sufixo/encapsulamento a fechar','Família','Caracterizar célula e estimativa de carga','S16'),
('U11 U12',2,'Chaves alimentação','TPS22918DBVR','TI','SOT23-6','Candidatos','Biometria e cartão; impedir alimentação parasita por sinais','S25'),
('U13',1,'USB-C corrente','TUSB320','TI','X2QFN12','Família','Somente consumidor; partida com bateria esgotada; CC protegido','S15'),
('DUSB1',1,'Proteção USB dados','TPD2EUSB30','TI','Sufixo a fechar','Família','Proteção próxima ao conector; avaliar clamping para MCU','S26'),
('J1',1,'USB-C traseiro','USB4105-GF-A','GCT','16 contatos topo','Candidato mecânico','Comprimento de ancoragem e altura de centro a fechar','S20'),
('J2',1,'Slot microSD','DM3AT-SF-PEJM5','Hirose','SMT','Candidato mecânico','Esquerda; acesso e altura a resolver','S21'),
('J3',1,'P2 estéreo','SJ-3523-SMT-TR','Same Sky','SMT angular TRS','Candidato mecânico','Esquerda; somente saída; sem detecção de plugue nesta peça','S22'),
('SW1-SW9',9,'Teclas rasas','CPG135301D01 Choc V2 Red','Kailh','Perfil baixo THT','Candidato mecânico','Sem clique; tecla e curso precisam caber; padrão próprio a conferir','S19'),
('RV1',1,'Deslizante vertical','PTA1543, 10 kohm linear','Bourns','THT curso 15 mm','Família','Comprimento da haste e código completo após empilhamento','S18'),
('SW12',1,'Chave mudo','7201, DPDT ON-ON','C&K / Littelfuse','Alavanca painel','Família','Selecionar contatos para baixa corrente e haste curta','S13'),
('SW10 SW11',2,'Camada / gravador','A definir','A definir','Tátil baixo perfil','Pendente','Reserva 6x3 e diâmetro4 refere-se à tampa, não ao corpo da peça','Projeto'),
('LED1-LED3',3,'Camadas','Verde de alta eficiência','A definir','0402 ou 0603','Pendente','0.1 a 0.3 mA inicial; guia óptico; brilho a ensaiar','Projeto'),
('LED4',1,'Estado gravador','Verde de alta eficiência','A definir','0402 ou 0603','Proposta nova','Ponto discreto no botão; preservar 3 LEDs só para camadas','Projeto'),
('BAT1',1,'Bateria referência','2011; 3.7 V 2000 mAh','Adafruit','60x36x7 mm','Referência de bancada','Pacote protegido; validar ficha real e termistor externo','S02'),
('TH1',1,'Temperatura bateria','NTC 10 kohm; curva a fechar','A definir','Em contato com célula','Pendente','Rede TS calculada para curva real; não simular temperatura por resistor fixo','Projeto'),
('J4',1,'Conector bateria','Polarizado com trava; a definir','A definir','PCB/cabo','Pendente','Polaridade e corrente conferidas com pacote real','Projeto'),
('J5 J6',2,'Interligação interface','A definir','A definir','FFC ou placa a placa','Pendente','Número de vias; altura; retenção; aterramento','Projeto'),
('Y1',1,'Relógio principal','A definir conforme ST','A definir','SMD','Pendente','Tolerância USB e áudio; não fixar carga capacitiva sem peça','S03'),
('Y2',1,'Relógio calendário','32768 Hz; a definir','A definir','SMD','Pendente','Carga e partida; sincronizar calendário por USB','S03'),
('L*','A definir','Indutores','Conforme U1 U7 U8','A definir','Blindados','Pendente','Valor corrente saturação perdas e corrente eficaz pelo cálculo','Projeto'),
('R*','A definir','Resistores','1% ou melhor conforme função','A definir','0402/0603','Pendente','Pull-ups; feedback; LEDs; limitação e termistor','Projeto'),
('C*','A definir','Capacitores','Conforme circuitos','A definir','MLCC/baixa distorção','Pendente','Valor efetivo com tensão DC; desacoplamento e áudio','Projeto'),
('ESD*','A definir','Proteções adicionais','CC VBUS P2 microSD controles','A definir','A definir','Pendente','Tensão clamping; capacitância; sobrevoltagem; descarga','Projeto'),
('TP*','A definir','Pontos de ensaio','SWD reset energia áudio','Projeto','Pads de teste','Pendente','Acesso bancada; isolamento de correntes por domínio','Projeto'),
('CARD1',1,'Cartão','microSDXC até256GB; homologar','A definir','Removível','Pendente','Consumo médio/pico; latência; resistência a perda de energia','Projeto'),
('PCB1',1,'Placa principal','98x78 mm; 4 camadas referência','Projeto','Espessura a fechar','Estudo','Sem esquema nem trilhas; NÃO FABRICAR','Projeto'),
('PCB2',1,'Placa de interface','98x78 mm; 2 camadas referência','Projeto','Espessura a fechar','Estudo','Reservas sem terminais; NÃO FABRICAR','Projeto'),
('MEC*','A definir','Peças mecânicas','Teclas; dutos; isolação; fixação','Projeto/catálogo','A definir','Pendente','Célula sem compressão; acústica e força das teclas','Projeto'),
]
csvfile('BOM_Alpha_v0.1.0.csv',['Referencias','Quantidade','Funcao','Codigo_ou_familia','Fabricante','Formato','Situacao','Pendencia','Fonte_no_relatorio'],bom)

links=[
('USB_D_P/N','USB-C J1','ESD e USB_HS U1','USB2 HS','3.3V PHY','90 ohms diferencial; não roteado'),
('USB_CC1/2','USB-C J1','TUSB320 U13','Controle USB-C','Conforme CC','Limitação fonte; proteção e dead-battery a fechar'),
('VBUS_5V','USB-C J1','BQ25622 U7','Energia','5V','Limite de entrada e proteção'),
('BAT','Bateria BAT1','BQ25622 U7 + MAX17048 U10','Energia','1S Li-ion','Termistor na célula; proteção independente'),
('SYS','BQ25622 U7','TPS63070 U8','Energia','Variável','Regulação 3V3 e teste de retirada USB'),
('3V3','TPS63070 U8','MCU cartão I/O biometria amplificador','Energia','3.3V','Domínios desligáveis e picos SD'),
('2V8_MIC','TPS7A20 U9','Polo A SW12','Energia','2.8V','Microfone nunca recebe 3.3 V'),
('3V3_AUDIO','3V3 filtrado','AVDD e IOVDD do TAC5112','Energia','3.3V','AVDD do codec não aceita2.8V; filtragem a calcular'),
('MIC_VDD','Polo A SW12','MIC1 MIC2','Energia interrompida fisicamente','2.8V/aberto','Mudo independente do programa'),
('MIC_L_P/N','MIC1','U4 e capacitores -> U2','Analógico diferencial','Conforme mic','Dutos acústicos selados e trilhas silenciosas'),
('MIC_R_P/N','MIC2','U5 e capacitores -> U2','Analógico diferencial','Conforme mic','Sem alimentação parasita'),
('MIC_ALLOW','Polo B SW12','U4 U5 + leitura protegida MCU','Comando físico','0/3.3V','MCU só observa; padrão mudo'),
('SAI_AUDIO','U1','U2','I2S/TDM MCLK BCLK FS TX RX','3.3V I/O','Relógio comum e retorno USB; pinos a definir'),
('LINE_L/R','U2','TPA6132A2 U3','Áudio de reprodução','Conforme datasheets','Acoplamento de entrada e ganho a calcular'),
('HP_L/R/GND','U3','J3 P2','Saída fone','Referenciada a GND','Nunca mutar junto aos microfones'),
('SDMMC','U1','J2 cartão','CLK CMD D0 D1 D2 D3 + CD','3.3V','Sem UHS de1.8V nesta revisão; série/pull-ups a calcular'),
('I2C_AUDIO','U1','U2','SCL SDA','3.3V','Pull-ups e endereços a confirmar'),
('I2C_POWER','U1','U7 U10 U13','SCL SDA + alertas','3.3V','Habilitação carga permanece segura durante reset'),
('I2C_SEC','Área segura U1','SE050 U6','SCL SDA EN','Conforme SE050','Barramento dedicado; canal autenticado'),
('BIO_UART','U1','BIO1','TX RX IRQ','3.3V','Somente bancada até segurança resolvida'),
('KEY1..9','SW1..9','U1','9 GPIO independentes','3.3V','Sem diodos de matriz; filtragem temporal'),
('AUX_INPUTS','SW10 SW11','U1','GPIO interrupção','3.3V','Início seguro e função de despertar'),
('LAYER_LED1..3','U1','LED1..3','GPIO + resistores','3.3V','Somente um aceso por camada'),
('REC_LED','U1','LED4','GPIO + resistor','3.3V','Indicador adicional proposto'),
('VOLUME','RV1','U1 ADC','Cursor filtrado','0..3.3V','Volume de reprodução; gravação independente'),
('SWD','Conector/pads de teste','U1','Programação','3.3V','Protegido em produção; recuperação assinada'),
]
csvfile('Interligacoes_funcionais_v0.1.0.csv',['Rede_grupo','Origem','Destino','Interface','Nivel','Observacao'],links)

energy=[]
for power in [100,120,150,177.6,200,250]:
    energy.append([2000,3.7,.8,.9,power,round(2*3.7*.8*.9/(power/1000),2),'Estimativa sem medição'])
csvfile('Autonomia_cenarios_v0.1.0.csv',['Capacidade_mAh','Tensao_V','Fracao_util','Eficiencia','Potencia_cargas_mW','Horas_estimadas','Situacao'],energy)

# Coordenadas mm: origem no canto traseiro esquerdo, vista superior, y cresce para frente.
# Retângulos são ENVELOPES, não padrões de soldagem.
main=[
('J1','USB-C',49,3,12,6,'io'),('PWR','Carga + 3V3',72,12,24,14,'power'),
('J2','microSD',9,27,16,16,'io'),('AUDIO','Codec + mudo',28,29,18,20,'audio'),
('U1','STM32U5A5',72,40,28,28,'logic'),('SEC','SE050',54,65,12,12,'security'),
('HP','Amplificador',24,56,12,12,'audio'),('J3','P2',5,56,10,18,'io'),
('MIC1','Mic E',4,9,6,6,'audio'),('MIC2','Mic D',94,9,6,6,'audio'),
('LINK','Interface',77,71,22,7,'logic'),('BAT1','Bateria abaixo',42,44,64,40,'battery'),
]
ui=[]
for row,y in enumerate([18.5,39,59.5]):
    for col,x in enumerate([16,36,56]):
        ui.append((f'SW{row*3+col+1}',str(row*3+col+1),x,y,19,19,'key'))
ui += [('SW10','Camada',33.5,4.6,6,3,'logic'),('LED1','',41.8,4.6,1,1,'led'),
('LED2','',44.3,4.6,1,1,'led'),('LED3','',46.8,4.6,1,1,'led'),
('SW11','Gravar',57.5,4.6,4,4,'logic'),('SW12','Mudo',84.5,10,16,16,'audio'),
('RV1','Volume',84.5,37,10,33,'audio'),('BIO1','Biometria',84.5,65.5,22,22,'security')]
csvfile('Posicionamento_reservas_v0.1.0.csv',['Placa','Referencia','Descricao','X_mm','Y_mm','Largura_mm','Altura_mm','Grupo'],[['Principal',*r] for r in main]+[['Interface',*r] for r in ui])

def vec(x,y):return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
def line(board,a,b,layer,width=.15):
    sh=p.PCB_SHAPE();sh.SetShape(p.SHAPE_T_SEGMENT);sh.SetStart(vec(*a));sh.SetEnd(vec(*b));sh.SetLayer(layer);sh.SetWidth(p.FromMM(width));board.Add(sh)
def text(board,s,x,y,layer=p.Dwgs_User,size=1):
    t=p.PCB_TEXT(board);t.SetText(s);t.SetPosition(vec(x,y));t.SetTextSize(vec(size,size));t.SetTextThickness(p.FromMM(.15));t.SetLayer(layer);board.Add(t)
def rect(board,cx,cy,w,h,layer):
    a=(cx-w/2,cy-h/2); b=(cx+w/2,cy-h/2); c=(cx+w/2,cy+h/2); d=(cx-w/2,cy+h/2)
    for aa,bb in [(a,b),(b,c),(c,d),(d,a)]:line(board,aa,bb,layer)
def outline(board):
    r=6;ox=50;oy=50;W=98;H=78
    for a,b in [((r,0),(W-r,0)),((W,r),(W,H-r)),((W-r,H),(r,H)),((0,H-r),(0,r))]:
        line(board,(a[0]+ox,a[1]+oy),(b[0]+ox,b[1]+oy),p.Edge_Cuts,.05)
    import math
    for cx,cy,ang in [(W-r,r,-90),(W-r,H-r,0),(r,H-r,90),(r,r,180)]:
        a=p.PCB_SHAPE();a.SetShape(p.SHAPE_T_ARC);a.SetLayer(p.Edge_Cuts);a.SetWidth(p.FromMM(.05))
        pts=[vec(ox+cx+r*math.cos(math.radians(ang+d)),oy+cy+r*math.sin(math.radians(ang+d))) for d in [0,45,90]]
        a.SetArcGeometry(*pts);board.Add(a)
def make_board(name,rows,layers):
    b=p.BOARD();b.SetCopperLayerCount(layers);b.GetDesignSettings().SetBoardThickness(p.FromMM(1.2 if layers==4 else 1.0));outline(b)
    for ref,label,x,y,w,h,g in rows:
        layer=p.Cmts_User if g=='battery' else p.Dwgs_User
        rect(b,50+x,50+y,w,h,layer)
        if label:text(b,f'{ref} {label}',50+x,50+y,layer,.85 if w>9 else .6)
    text(b,'ALPHA 0.1.0 - POSICIONAMENTO PRELIMINAR',99,44,size=1.1)
    text(b,'SEM ESQUEMA / REDES / TRILHAS - NAO FABRICAR',99,133,size=1)
    text(b,'Retangulos: reservas, nao footprints. Alturas nao validadas.',99,136,size=.8)
    if name=='Principal':
        fp=p.FootprintLoad('/usr/share/kicad/footprints/Package_QFP.pretty','LQFP-144_20x20mm_P0.5mm')
        fp.SetReference('U1');fp.SetValue('STM32U5A5ZJT6Q');fp.SetPosition(vec(122,90));b.Add(fp)
        fp.Reference().SetVisible(False);fp.Value().SetVisible(False)
    path=ROOT/f'Alpha_{name}_v0.1.0.kicad_pcb';p.SaveBoard(str(path),b)
    loaded=p.LoadBoard(str(path))
    assert loaded.GetCopperLayerCount()==layers and len(list(loaded.GetTracks()))==0
    return {'arquivo':path.name,'camadas':layers,'trilhas':0,'footprints_com_pads':len(list(loaded.GetFootprints())),'reservas':len(rows),'esquema_eletrico':False}
validation=[make_board('Principal',main,4),make_board('Interface',ui,2)]

colors={'io':'#81b4df','power':'#edbe72','audio':'#8bd0c0','logic':'#b4c6e8','security':'#c3a5df','battery':'#e7ce97','key':'#333b42','led':'#73e640'}
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10})
fig,axes=plt.subplots(1,2,figsize=(15,7.6));fig.patch.set_facecolor('#f5f7f7')
for ax,rows,title in zip(axes,[ui,main],['Interface superior • 2 camadas','Placa principal • 4 camadas']):
    ax.set_aspect('equal');ax.set_xlim(-3,101);ax.set_ylim(83,-6);ax.axis('off')
    ax.add_patch(FancyBboxPatch((0,0),98,78,boxstyle='round,pad=0,rounding_size=6',facecolor='#e3ece8',edgecolor='#204637',linewidth=1.8))
    for ref,label,x,y,w,h,g in sorted(rows,key=lambda r: r[-1]!='battery'):
        if g=='battery':
            ax.add_patch(Rectangle((x-w/2,y-h/2),w,h,fill=False,edgecolor='#ac7625',linestyle='--',linewidth=1.5));ax.text(45,47,'Bateria na face inferior',fontsize=7,ha='center',color='#795015');continue
        if g=='led':ax.add_patch(Circle((x,y),.5,color=colors[g]));continue
        ax.add_patch(FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle='round,pad=0,rounding_size=1',facecolor=colors[g],edgecolor='#50616a',linewidth=.8))
        if ref in ('SW10','SW11'):continue
        fs=8 if g not in ('key',) else 13
        ax.text(x,y,label if g=='key' else label.replace(' + ','\n+ '),ha='center',va='center',fontsize=fs,color='white' if g=='key' else '#182a32')
    ax.text(49,-3,'TRASEIRA',ha='center',fontsize=9,color='#5a6e65')
    ax.text(49,82,'98 × 78 mm • referência de estudo',ha='center',fontsize=10)
    ax.set_title(title,loc='left',fontsize=16,pad=15,fontweight='bold')
for x,label in [(33.5,'Camada'),(44.3,'LEDs'),(57.5,'Gravar')]:
    axes[0].text(x,-.5,label,fontsize=7,ha='center')
fig.suptitle('ALPHA / ELETRÔNICA 0.1.0',x=.045,y=.98,ha='left',fontsize=23,fontweight='bold',color='#163e2f')
fig.text(.045,.91,'Estudo de posicionamento baseado no conceito aprovado. Alturas e conexões ainda em desenvolvimento.',fontsize=11,color='#41545c')
fig.text(.045,.025,'Reservas de espaço, sem trilhas. Não é placa liberada para fabricação.  |  Projeto autoral • 22/11/2026',fontsize=10,color='#6c4522')
fig.subplots_adjust(top=.82,bottom=.09,wspace=.12,left=.04,right=.96)
fig.savefig(ROOT/'Alpha_Posicionamento_v0.1.0.png',dpi=160)
fig.savefig(ROOT/'Alpha_Posicionamento_v0.1.0.svg')
plt.close(fig)

checks={'revisao':'0.1.0','placas':validation,'teclas_reservadas':sum(r[-1]=='key' for r in ui),'leds_camada_reservados':sum(r[-1]=='led' for r in ui),'energia_util_cargas_Wh':5.328,'limite_30h_mW':177.6,'orcamento_mW':150,'horas_estimadas':35.52,'bom_linhas':len(bom),'eletrica_validada':False,'liberado_fabricacao':False}
assert checks['teclas_reservadas']==9 and checks['leds_camada_reservados']==3
(ROOT/'Verificacao_v0.1.0.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(checks,ensure_ascii=False))
