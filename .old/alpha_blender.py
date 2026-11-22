"""ALPHA v1.3.0: configurable RGB underglow added to the lower base perimeter.
Run: blender -b --python alpha_blender.py [-- --preview]
All helper arguments are millimetres; actual Blender geometry is in metres.
"""
import bpy, math, sys, json
from pathlib import Path
from mathutils import Vector, Matrix

ROOT=Path(__file__).resolve().parent
if ROOT.name=='alpha_blender': ROOT=ROOT.parent
OUT=ROOT/'alpha_blender'
VERSION='1.3.0'
PREFIX=f'Alpha_v{VERSION}'
PREVIEW='--preview' in sys.argv
DEST=Path('/tmp/alpha_v130_preview') if PREVIEW else OUT
DEST.mkdir(exist_ok=True)
BLEND=DEST/f'{PREFIX}.blend'
if not PREVIEW and BLEND.exists(): raise FileExistsError(f'Preservar versao existente: {BLEND}')
U=.001
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene
scene.unit_settings.system='METRIC'; scene.unit_settings.scale_length=1; scene.unit_settings.length_unit='MILLIMETERS'
COLS={}
for name in ['01_Carcaça','02_Teclas_3x3','03_Potenciômetro','04_Chave_microfone','05_Biometria','06_Conectores','07_Estúdio','08_Seleção_camadas','09_Gravador_ambiente','10_Faixa_RGB_base']:
    c=bpy.data.collections.new(name); scene.collection.children.link(c); COLS[name]=c
CURRENT=COLS['01_Carcaça']

def link(o):
    for c in list(o.users_collection): c.objects.unlink(o)
    CURRENT.objects.link(o); return o

def material(name,color,metal=0,rough=.4,grain=0,coat=0):
    m=bpy.data.materials.new(name); m.diffuse_color=(*color,1); m.use_nodes=True
    nodes=m.node_tree.nodes; p=nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value=(*color,1); p.inputs['Metallic'].default_value=metal
    p.inputs['Roughness'].default_value=rough; p.inputs['Coat Weight'].default_value=coat
    if grain:
        tc=nodes.new('ShaderNodeTexCoord'); noise=nodes.new('ShaderNodeTexNoise'); noise.inputs['Scale'].default_value=18000
        noise.inputs['Detail'].default_value=2
        m.node_tree.links.new(tc.outputs['Object'],noise.inputs['Vector'])
        bump=nodes.new('ShaderNodeBump'); bump.inputs['Strength'].default_value=.16; bump.inputs['Distance'].default_value=grain*U
        m.node_tree.links.new(noise.outputs['Fac'],bump.inputs['Height']); m.node_tree.links.new(bump.outputs['Normal'],p.inputs['Normal'])
        ramp=nodes.new('ShaderNodeMapRange'); ramp.inputs['To Min'].default_value=rough-.055; ramp.inputs['To Max'].default_value=rough+.055
        m.node_tree.links.new(noise.outputs['Fac'],ramp.inputs['Value']); m.node_tree.links.new(ramp.outputs['Result'],p.inputs['Roughness'])
    return m
bodymat=material('Alumínio preto acetinado · microtextura',(.018,.020,.022),.55,.4,.015)
keymat=material('Teclas PBT grafite · textura fina',(.035,.038,.042),0,.43,.011)
black=material('Polímero preto fosco',(.006,.007,.009),0,.48,.006)
steel=material('Níquel acetinado',(.47,.49,.52),1,.26,.003)
polish=material('Aço polido nas arestas',(.55,.57,.6),1,.18)
darksteel=material('Aço escovado escuro',(.09,.10,.12),.9,.34,.002)
glass=material('Vidro preto do sensor',(.009,.014,.019),.05,.17,0,.38)
gold=material('Contatos dourados',(.63,.37,.095),.85,.25)
green=material('Filete verde #00FF00 · inserto sólido',(.001,.8,.0005),0,.28,0,.2)
rubber=material('Borracha da base',(.009,.010,.011),0,.78,.01)
groundmat=material('Fundo de estúdio',(.028,.031,.035),0,.63,.006)

# Configurable product underglow. These scene properties document the controls
# expected from the future configuration software and also drive this visual study.
scene['Faixa_RGB_cor']=[0.0,1.0,0.0]
scene.id_properties_ui('Faixa_RGB_cor').update(min=0.0,max=1.0,subtype='COLOR')
scene['Faixa_RGB_brilho']=0.65
scene.id_properties_ui('Faixa_RGB_brilho').update(min=0.0,max=1.0,description='Brilho ilustrativo da faixa inferior; não representa consumo validado.')
scene['Faixa_RGB_ligada']=True
scene.id_properties_ui('Faixa_RGB_ligada').update(description='Liga/desliga a faixa RGB no estudo visual.')
rgb=material('Faixa RGB · difusor translúcido configurável',(.001,.8,.0005),0,.24,0,.32)
rgb_bs=rgb.node_tree.nodes.get('Principled BSDF')
for input_name in ('Base Color','Emission Color'):
    inp=rgb_bs.inputs[input_name]
    for component in range(3):
        drv=inp.driver_add('default_value',component).driver
        var=drv.variables.new();var.name='c';var.type='SINGLE_PROP'
        var.targets[0].id_type='SCENE';var.targets[0].id=scene
        var.targets[0].data_path=f'["Faixa_RGB_cor"][{component}]'
        drv.expression='max(0.0,min(1.0,c))'
rgb_strength=rgb_bs.inputs['Emission Strength']
rgb_strength.default_value=2.925
drv=rgb_strength.driver_add('default_value').driver
for name,path in [('on','["Faixa_RGB_ligada"]'),('level','["Faixa_RGB_brilho"]')]:
    var=drv.variables.new();var.name=name;var.type='SINGLE_PROP'
    var.targets[0].id_type='SCENE';var.targets[0].id=scene;var.targets[0].data_path=path
drv.expression='4.5 * on * max(0.0,min(1.0,level))'

# Explicit XY radii are independent of piece thickness.
def outline(w,d,r,n=12):
    pts=[]
    for cx,cy,start in [(w/2-r,d/2-r,0),(-w/2+r,d/2-r,90),(-w/2+r,-d/2+r,180),(w/2-r,-d/2+r,270)]:
        for i in range(n):
            a=math.radians(start+90*i/(n-1)); pts.append((cx+r*math.cos(a),cy+r*math.sin(a)))
    return pts

def mesh(name,verts,faces,mat,smooth=False):
    me=bpy.data.meshes.new(name); me.from_pydata([tuple(t*U for t in v) for v in verts],[],faces); me.update()
    o=bpy.data.objects.new(name,me); CURRENT.objects.link(o); o.data.materials.append(mat)
    if smooth:
        for p in me.polygons:p.use_smooth=True
    return o

def normals(o):
    m=o.modifiers.new('Normais de acabamento','WEIGHTED_NORMAL'); m.keep_sharp=True; m.weight=50
    return o

def rr(name,xyz,w,d,h,r,mat,edge=.1):
    edge=min(edge,h*.45,r*.4)
    profiles=[(w-2*edge,d-2*edge,r-edge,-h/2),(w,d,r,-h/2+edge),(w,d,r,h/2-edge),(w-2*edge,d-2*edge,r-edge,h/2)] if edge else [(w,d,r,-h/2),(w,d,r,h/2)]
    verts=[]; n=len(outline(w,d,r)); faces=[]
    for wi,di,ri,z in profiles: verts.extend([(x,y,z) for x,y in outline(wi,di,ri)])
    for j in range(len(profiles)-1):
        for i in range(n):faces.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i))
    faces.extend([tuple(reversed(range(n))),tuple(range((len(profiles)-1)*n,len(profiles)*n))])
    o=mesh(name,verts,faces,mat,True); o.location=Vector(xyz)*U; return normals(o)

def ring(name,xyz,outer,inner,height,mat):
    # Rounded rectangular annulus, open through the middle.
    a=outline(*outer); b=outline(*inner); n=len(a); vs=[]
    for pts,z in [(a,-height/2),(a,height/2),(b,height/2),(b,-height/2)]:vs.extend([(x,y,z) for x,y in pts])
    fs=[]
    for j in range(4):
        for i in range(n):fs.append((j*n+i,j*n+(i+1)%n,((j+1)%4)*n+(i+1)%n,((j+1)%4)*n+i))
    o=mesh(name,vs,fs,mat,True);o.location=Vector(xyz)*U;return normals(o)

def lathe(name,xyz,profile,mat,n=96):
    vs=[];fs=[]
    for rad,z in profile:
        for i in range(n):
            a=2*math.pi*i/n;vs.append((rad*math.cos(a),rad*math.sin(a),z))
    for j in range(len(profile)-1):
        for i in range(n):fs.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i))
    o=mesh(name,vs,fs,mat,True);o.location=Vector(xyz)*U;return normals(o)

def disc(name,xyz,r,h,mat):
    return lathe(name,xyz,[(0,-h/2),(r-.06,-h/2),(r,-h/2+.06),(r,h/2-.06),(r-.06,h/2),(0,h/2)],mat)

def tube(name,xyz,ro,ri,h,mat,n=96):
    e=min(.05,h*.15,(ro-ri)*.25)
    p=[(ri,-h/2),(ro-e,-h/2),(ro,-h/2+e),(ro,h/2-e),(ro-e,h/2),(ri+e,h/2),(ri,h/2-e),(ri,-h/2)]
    return lathe(name,xyz,p,mat,n)

def apply_mods(o):
    bpy.context.view_layer.objects.active=o
    for m in list(o.modifiers):bpy.ops.object.modifier_apply(modifier=m.name)

def cut(target,cutter):
    apply_mods(cutter)
    bpy.context.view_layer.objects.active=target
    m=target.modifiers.new('Abertura real','BOOLEAN');m.object=cutter;m.operation='DIFFERENCE';m.solver='EXACT'
    # Boolean before normal modifier, to avoid layering normals over topology edits.
    bpy.ops.object.modifier_move_up(modifier=m.name)
    bpy.ops.object.modifier_apply(modifier=m.name);bpy.data.objects.remove(cutter,do_unlink=True)

def orient(o,origin,side):
    # local XY is the connector face; local Z points outwards.
    axes={'left':((0,-1,0),(0,0,1),(-1,0,0)),'rear':((-1,0,0),(0,0,1),(0,1,0)), 'right':((0,1,0),(0,0,1),(1,0,0))}
    o.rotation_euler=Matrix(axes[side]).transposed().to_euler();o.location=Vector(origin)*U;return o

def sphere(name,xyz,r,mat):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48,ring_count=24,radius=r*U,location=Vector(xyz)*U)
    o=link(bpy.context.object);o.name=name;o.data.materials.append(mat)
    for p in o.data.polygons:p.use_smooth=True
    return o

def curve(name,pts,r,mat):
    c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.bevel_depth=r*U;c.bevel_resolution=3
    s=c.splines.new('POLY');s.points.add(len(pts)-1)
    for p,v in zip(s.points,pts):p.co=(*(t*U for t in v),1)
    o=bpy.data.objects.new(name,c);CURRENT.objects.link(o);o.data.materials.append(mat);return o

# Single hollow lower enclosure and independent top cover.
case=rr('Corpo | parede 1,7 mm, cavidade interna', (0,0,6.75),104,84,12.1,8,bodymat,.6)
cut(case,rr('Cavidade interna',(0,0,10.0),100.6,80.6,16.0,6.3,black,.1))
lid=rr('Tampa | contorno arredondado e furos reais',(0,0,13.975),104,84,2.05,8,bodymat,.23)
ring('Junta periférica da carcaça',(0,0,12.87),(103.5,83.5,7.75),(100.4,80.4,6.2),.10,black)
# An inset flat ring, seated in a matching routed groove.
groove=ring('Canal do inserto',(0,0,15.0),(101.1,81.1,6.7),(99.4,79.4,5.85),.5,black)
cut(lid,groove)
ring('Moldura verde | inserto plano contínuo',(0,0,14.97),(100.95,80.95,6.625),(99.55,79.55,5.925),.18,green)
# Real mounting apertures.
positions=[(row+1,col+1,x,y) for row,y in enumerate((20.5,0,-20.5)) for col,x in enumerate((-33,-13,7))]
for row,col,x,y in positions:cut(lid,rr('Furo tecla',(x,y,14),19.5,19.5,5,2.5,black,0))
cut(lid,disc('Furo biometria',(35.5,-26.5,14),10.58,6,black))
cut(lid,disc('Furo chave',(35.5,29,14),3.18,6,black))
cut(lid,rr('Furo potenciômetro',(35.5,2,14),7.3,26,6,1.8,black,0))
# Ambient sound enters through the side ports added below.
# Center all connectors on the actual case + lid thickness, excluding feet.
bpy.context.view_layer.update()
case_bounds=[(o.matrix_world @ Vector(v)).z / U for o in (case,lid) for v in o.bound_box]
CASE_BOTTOM,CASE_TOP=min(case_bounds),max(case_bounds)
PORT_Z=(CASE_BOTTOM+CASE_TOP)/2
p2=(-52,-18,PORT_Z);sd=(-52,14,PORT_Z);usb=(0,42,PORT_Z)
cut(case,orient(disc('Furo P2',(0,0,0),2.85,7,black),p2,'left'))
cut(case,orient(rr('Furo microSD',(0,0,0),12.1,2.1,7,.65,black,0),sd,'left'))
cut(case,orient(rr('Furo USB-C',(0,0,0),9.5,3.75,7,1.75,black,0),usb,'rear'))
for x in (-40,40):
    for y in (-30,30):disc('Pé de borracha',(x,y,.25),3.4,.9,rubber)

# Continuous RGB diffuser set into the lower base, just above the feet. The
# recessed channel leaves a dark reveal above and below the luminous strip.
CURRENT=COLS['10_Faixa_RGB_base']
RGB_Z=1.66
RGB_HEIGHT=1.10
rgb_channel=ring('Canal contínuo da faixa RGB',(0,0,RGB_Z),(105.0,85.0,8.5),(100.15,80.15,6.15),1.48,black)
cut(case,rgb_channel)
rgb_band=ring('Faixa RGB | difusor perimetral inferior',(0,0,RGB_Z),(103.75,83.75,7.88),(100.35,80.35,6.18),RGB_HEIGHT,rgb)
rgb_band['Posição']='Perímetro inferior da base, acima dos pés e abaixo dos conectores.'
rgb_band['Controle']='Cor, brilho e liga/desliga ilustrados por propriedades da cena.'
rgb_band['Independência']='Não substitui LEDs de camada nem indicador de gravação.'
# A narrow downward-facing lip makes the table wash legible from low angles.
ring('Faixa RGB | emissão inferior para a mesa',(0,0,1.08),(101.6,81.6,6.8),(98.7,78.7,5.55),.16,rgb)

# Discreet separate layer selector, above the nine macro keys.
CURRENT=COLS['08_Seleção_camadas']
lx,ly=-13.0,34.4
cut(lid,rr('Abertura do seletor de camadas',(lx,ly,14),6.5,3.5,5,1.6,black,0))
ring('Camadas | guia rebaixada',(lx,ly,14.65),(6.4,3.4,1.55),(6.12,3.12,1.40),.5,black)
layer_button=rr('Camadas | botão discreto sem inscrição',(lx,ly,14.90),6.0,3.0,.7,1.36,keymat,.13)
layer_button['Função']='Selecionar camadas; camada secreta continua dependente da autenticação biométrica.'
layer_button['Tipo']='Botão auxiliar, separado das nove teclas macro.'
rr('Camadas | haste interna',(lx,ly,14.0),1.8,1.2,1.2,.4,black,.08)

# Three physical diffusers, one for each layer. Only the selected one glows.
scene['Camada_ativa']=1
scene.id_properties_ui('Camada_ativa').update(min=1,max=3,description='Estado ilustrativo dos três indicadores; não implementa firmware.')
for i,x in enumerate((-7.2,-4.7,-2.2),1):
    cut(lid,disc('Furo indicador de camada',(x,34.4,14),.64,5,black))
    tube(f'LED {i} | aro isolante',(x,34.4,14.86),.61,.49,.3,black,48)
    lm=material(f'LED camada {i} · verde',(.004,.014,.006),0,.26,0,.3)
    bs=lm.node_tree.nodes.get('Principled BSDF')
    bs.inputs['Emission Color'].default_value=(.001,1,.001,1)
    inp=bs.inputs['Emission Strength'];inp.default_value=2.5 if i==1 else 0
    drv=inp.driver_add('default_value').driver
    var=drv.variables.new();var.name='layer';var.type='SINGLE_PROP'
    var.targets[0].id_type='SCENE';var.targets[0].id=scene;var.targets[0].data_path='["Camada_ativa"]'
    drv.expression=f'2.5 if layer == {i} else 0.0'
    led=disc(f'LED {i} | difusor da camada',(x,34.4,15.0),.46,.16,lm)
    led['Camada']=i

CURRENT=COLS['09_Gravador_ambiente']
rx,ry=8.5,34.4
cut(lid,disc('Furo botão do gravador',(rx,ry,14),2.24,5,black))
tube('Gravador | guia rebaixada',(rx,ry,14.65),2.18,2.05,.5,black)
record=disc('Gravador | botão circular sem inscrição',(rx,ry,14.9),2.0,.7,keymat)
record['Função']='Ativar modo de gravação de som ambiente; implementação eletrônica pendente.'
rr('Gravador | haste interna',(rx,ry,14),1.4,1.4,1.2,.4,black,.08)
# Real through-holes on both sides, set clear of the ports and corner radius.
for side,sign in [('left',-1),('right',1)]:
    for i,y in enumerate((25.5,27.5,29.5,31.5),1):
        cut(case,orient(disc('Corte acústico lateral',(0,0,0),.50,6,black),(sign*52,y,PORT_Z),side))
        acoustic=orient(disc(f'Microfone {side} {i} | membrana acústica',(0,0,0),.61,.12,rubber),(sign*49.95,y,PORT_Z),side)
        acoustic['Abertura_mm']=1.0
        acoustic['Nota']='Membrana ilustrativa atrás de furo passante, sem escolha de cápsula de microfone.'

CURRENT=COLS['02_Teclas_3x3']
for row,col,x,y in positions:
    ring(f'KEY {row}{col} · guia e folga',(x,y,14.2),(19.42,19.42,2.46),(19.1,19.1,2.3),1.1,black)
    # Rounded key with a very shallow fingertip dish; profiled independently in XY/Z.
    n=len(outline(19,19,2.25)); vs=[];fs=[]
    profiles=[(18.35,18.35,2.0,14.65),(18.95,18.95,2.25,15.05),(19,19,2.28,15.65),(18.88,18.88,2.26,15.96),(18.45,18.45,2.15,16.18),(17.9,17.9,2.0,16.25),(15.4,15.4,2.7,16.21),(10,10,3.5,16.13),(3,3,1.3,16.07)]
    for w,d,r,z in profiles:vs.extend([(a+x,b+y,z) for a,b in outline(w,d,r)])
    for j in range(len(profiles)-1):
        for i in range(n):fs.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i))
    fs.append(tuple(reversed(range(n))));fs.append(tuple(range((len(profiles)-1)*n,len(profiles)*n)))
    normals(mesh(f'KEY {row}{col} · tecla rasa sem grafia',vs,fs,keymat,True))

CURRENT=COLS['03_Potenciômetro']
fx,fy=35.5,2
plate=rr('Fader | chapa acetinada',(fx,fy,15.18),9.4,30, .32,1.55,darksteel,.06)
cut(plate,rr('Rasgo real do fader',(fx,fy,15.2),1.85,20,3,.9,black,0))
rr('Fader | fundo interno do alojamento',(fx,fy,13.1),6.8,24,1.0,1.3,black,.15)
rr('Fader | haste móvel',(fx,fy-1.3,15.6),1.1,1.8,3,.2,steel,.06)
knob=rr('Fader | botão pequeno com ranhuras',(fx,fy-1.3,16.75),7.4,4.7,1.55,.75,black,.25)
for dy in (-1.35,-.68,0,.68,1.35):
    cut(knob,rr('Ranhura de aderência',(fx,fy-1.3+dy,17.52),6.2,.23,.34,.105,black,.04))
# Actual cross-recessed heads, each seated in a countersink.
def screw(x,y,z,label):
    head=lathe(label,(x,y,z),[(0,-.34),(.52,-.34),(.9,-.06),(.97,.02),(.91,.14),(0,.18)],steel,64)
    for angle in (0,math.pi/2):
        c=rr('Rebaixo Phillips',(x,y,z+.14),1.25,.25,.33,.08,black,.03);c.rotation_euler[2]=angle;cut(head,c)
    return head
for sy in (fy-12.2,fy+12.2):
    cut(plate,disc('Assento do parafuso',(fx,sy,15.25),1.02,1,black))
    screw(fx,sy,15.23,'Fader | parafuso Phillips M1,6')

CURRENT=COLS['04_Chave_microfone']
tx,ty=35.5,29
# Separate washer, nut, threaded sleeve and pivot, with visible contact surfaces.
tube('Chave | arruela',(tx,ty,15.12),4.65,3.12,.2,steel)
tube('Chave | porca sextavada',(tx,ty,15.78),4.15,3.10,1.04,steel,6)
tube('Chave | corpo roscado M6',(tx,ty,16.32),2.84,1.71,2.15,darksteel)
pts=[]
for i in range(241):
    t=i/240*2*math.pi*4.4;pts.append((tx+2.93*math.cos(t),ty+2.93*math.sin(t),15.4+.45*t/(2*math.pi)))
curve('Chave | rosca helicoidal contínua',pts,.095,steel)
sphere('Chave | articulação esférica',(tx,ty,17.35),1.68,black)
pivot=Vector((tx,ty,17.35))*U; rot=Matrix.Rotation(math.radians(-12),3,'X')
shaft=lathe('Chave | alavanca cromada',(tx,ty,17.35),[(0,-.55),(.91,-.55),(1.04,.2),(1.02,3.15),(0,3.15)],polish)
shaft.rotation_euler=rot.to_euler()
grip=lathe('Chave | ponta arredondada acetinada',(tx,ty,17.35),[(0,2.7),(1.15,2.7),(1.38,2.95),(1.42,5.1),(1.36,5.48),(1.1,5.78),(.65,5.98),(0,6.06)],darksteel)
grip.rotation_euler=rot.to_euler()

CURRENT=COLS['05_Biometria']
bx,by=35.5,-26.5
tube('Biometria | vedação externa',(bx,by,14.65),10.50,10.35,.55,black)
tube('Biometria | moldura metálica chanfrada',(bx,by,15.08),10.35,9.35,.6,steel)
tube('Biometria | junta do vidro',(bx,by,15.03),9.34,9.18,.32,black)
disc('Biometria | superfície de contato',(bx,by,15.07),9.17,.24,glass)

CURRENT=COLS['06_Conectores']
orient(tube('P2 | anel metálico aberto',(0,0,0),2.72,1.82,1.2,steel),(-51.68,-18,PORT_Z),'left')
orient(tube('P2 | isolamento interno',(0,0,0),2.4,1.77,4.5,black),(-49.7,-18,PORT_Z),'left')
orient(tube('P2 | contato interno',(0,0,0),1.76,1.70,.6,gold),(-49.4,-18,PORT_Z),'left')
orient(disc('P2 | fundo do conector',(0,0,0),1.76,.2,black),(-47.5,-18,PORT_Z),'left')
orient(ring('microSD | boca metálica',(0,0,0),(11.9,1.95,.6),(11.05,1.17,.3),1.4,darksteel),(-51.35,14,PORT_Z),'left')
orient(rr('microSD | fundo interno',(0,0,0),11.1,1.2,.2,.3,black,.03),(-49.2,14,PORT_Z),'left')
orient(ring('USB-C | blindagem com abertura oval',(0,0,0),(9.15,3.45,1.7),(8.0,2.28,1.12),2.1,steel),(0,41.0,PORT_Z),'rear')
orient(rr('USB-C | fundo interno',(0,0,0),8.1,2.4,.2,1.1,black,.03),(0,39.8,PORT_Z),'rear')
orient(rr('USB-C | lingueta central',(0,0,0),6.5,.68,1.6,.2,black,.05),(0,40.6,PORT_Z),'rear')
for i in range(12):
    x=(i-5.5)*.44
    for z in (PORT_Z-.36,PORT_Z+.36):rr('USB-C | contato dourado',(x,40.85,z),.19,1.05,.055,.06,gold,.01)

# Curated perspective cameras, real metre dimensions and broad reflection cards.
CURRENT=COLS['07_Estúdio']
rr('Plano contínuo de estúdio',(0,0,-.8),3000,3000,1,30,groundmat,.1)
world=scene.world;world.use_nodes=True
world.node_tree.nodes['Background'].inputs['Color'].default_value=(.24,.27,.31,1)
world.node_tree.nodes['Background'].inputs['Strength'].default_value=.20

def area(name,xyz,power,size,shape='DISK',target=(0,0,8),size_y=70):
    bpy.ops.object.light_add(type='AREA',location=Vector(xyz)*U);o=link(bpy.context.object);o.name=name
    o.data.energy=power*.01;o.data.shape=shape;o.data.size=size*U
    if shape=='RECTANGLE':o.data.size_y=size_y*U
    o.rotation_euler=(Vector(target)*U-o.location).to_track_quat('-Z','Y').to_euler()
area('Luz principal difusa',(-85,-90,150),7.5,130)
area('Reflexo longo direito',(110,-20,100),5,35,'RECTANGLE',size_y=130)
area('Recorte traseiro',(-20,95,120),9,75,'RECTANGLE',size_y=110)
area('Preenchimento das portas',(-130,5,40),2,85)
area('Preenchimento superior',(15,5,180),3,150)

def cam(name,xyz,target,lens=65,scale=None):
    bpy.ops.object.camera_add(location=Vector(xyz)*U);o=link(bpy.context.object);o.name=name
    o.rotation_euler=(Vector(target)*U-o.location).to_track_quat('-Z','Y').to_euler();o.data.lens=lens
    o.data.clip_start=.001;o.data.clip_end=100
    if scale:o.data.type='ORTHO';o.data.ortho_scale=scale*U
    return o
cams={
 'frente_esquerda':cam('01 · ALPHA hero',(-105,-160,205),(0,0,8),63),
 'detalhe_controles':cam('02 · detalhe dos controles',(90,-100,120),(32,1,16),80),
 'traseira_USB-C':cam('03 · USB-C traseiro',(110,175,135),(0,0,8),60),
 'vista_superior':cam('04 · topo e matriz 3 × 3',(0,0,220),(0,0,0),scale=122),
 'lateral_microSD_P2':cam('05 · lateral esquerda',(-220,-18,80),(-10,0,8),65),
 'faixa_RGB_base':cam('06 · faixa RGB na base',(-128,-175,42),(0,-2,2.2),70),
}
scene.camera=cams['frente_esquerda']
scene.render.engine='CYCLES';scene.cycles.samples=48 if PREVIEW else 96
scene.cycles.use_denoising=False;bpy.context.view_layer.cycles.use_denoising=False
scene.cycles.max_bounces=8;scene.cycles.diffuse_bounces=3;scene.cycles.glossy_bounces=4
scene.cycles.adaptive_threshold=.02 if PREVIEW else .008
scene.render.resolution_x=1000 if PREVIEW else 1600;scene.render.resolution_y=850 if PREVIEW else 1360
scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
scene.view_settings.view_transform='AgX';scene.view_settings.look='AgX - Medium High Contrast';scene.view_settings.exposure=.55
scene.render.film_transparent=False
scene['Versão']=VERSION;scene['Origem']='ALPHA v1.2.0; faixa RGB inferior configurável adicionada após aprovação do usuário.'
scene['Limitação']='Estudo visual e de encaixes aparentes; não é validação eletrônica ou de fabricação.'
scene['Mudo']='Somente microfone. Saída do fone independente, requisito para circuito posterior.'
scene['Dimensões_corpo_mm']=f'104 x 84 x {CASE_TOP-CASE_BOTTOM:.2f}'
scene['Centro_conectores_z_mm']=PORT_Z
scene['Alterações']='Faixa RGB difusa no perímetro inferior da base; cor, brilho e liga/desliga configuráveis na cena.'
# Bundle a concise record inside the editable .blend.
text=bpy.data.texts.new('LEIA-ME · versão 1.3.0')
text.write('ALPHA v1.3.0\nModelo em escala real, metros com exibição em milímetros.\nPreserva as nove teclas 3x3, biometria, controles, conectores e aberturas da 1.2.0.\nMoldura verde superior sólida, sem iluminação das teclas.\nNova faixa RGB contínua e difusa no perímetro inferior da base, acima dos pés.\nA faixa projeta luz sobre a mesa e permanece separada dos LEDs funcionais.\nAltere Faixa_RGB_cor, Faixa_RGB_brilho e Faixa_RGB_ligada nas propriedades da cena.\nA configuração ilustra o requisito de software; circuito, consumo e firmware não foram implementados.\nP2 e microSD ficam à esquerda; USB-C fica atrás, todos no centro da espessura da carcaça.\nEsta cena detalha a aparência. A compatibilidade e a eletrônica não foram validadas.\n')
# Save with useful viewport and camera, avoiding an unframed startup view.
for screen in bpy.data.screens:
    for a in screen.areas:
        if a.type=='VIEW_3D':
            a.spaces.active.region_3d.view_distance=.2;a.spaces.active.region_3d.view_location=Vector((0,0,.009))
            a.spaces.active.region_3d.view_perspective='CAMERA';a.spaces.active.clip_start=.001
            a.spaces.active.shading.color_type='MATERIAL'
for ob in (case,lid):
    for polygon in ob.data.polygons:
        if abs(polygon.normal.z)>.95 or (ob == case and max(abs(polygon.normal.x),abs(polygon.normal.y))>.999): polygon.use_smooth=False
scene.render.filepath=str(DEST/f'{PREFIX}_frente_esquerda.png')
bpy.ops.wm.save_as_mainfile(filepath=str(BLEND))
selected=['frente_esquerda','faixa_RGB_base'] if PREVIEW else list(cams)
for name in selected:
    scene.camera=cams[name];scene.render.filepath=str(DEST/f'{PREFIX}_{name}.png')
    bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
if not PREVIEW:
    # A second low-angle render proves that the same geometry/material responds
    # to a different user-selected color without changing the upper green trim.
    scene['Faixa_RGB_cor']=[0.0,0.18,1.0]
    bpy.context.view_layer.update()
    scene.camera=cams['faixa_RGB_base']
    scene.render.filepath=str(DEST/f'{PREFIX}_faixa_RGB_azul.png')
    bpy.ops.render.render(write_still=True);print('RENDERED faixa_RGB_azul',flush=True)
    scene['Faixa_RGB_cor']=[0.0,1.0,0.0]
    bpy.context.view_layer.update()
validation={
    'versao':VERSION,
    'teclas_macro':9,
    'leds_camadas':3,
    'faixa_rgb':{
        'continua':True,
        'posicao':'perimetro inferior da base, acima dos pes e abaixo dos conectores',
        'altura_centro_z_mm':RGB_Z,
        'altura_difusor_mm':RGB_HEIGHT,
        'cor_padrao_rgb':[0.0,1.0,0.0],
        'variante_renderizada_rgb':[0.0,0.18,1.0],
        'controles_cena':['Faixa_RGB_cor','Faixa_RGB_brilho','Faixa_RGB_ligada'],
        'independente_leds_funcionais':True,
    },
    'eletronica_implementada':False,
    'firmware_implementado':False,
    'consumo_validado':False,
    'resultado':'Geometria, propriedades e vistas ilustrativas conferidas; difusor, circuito, consumo e software dependem de desenvolvimento.'
}
(DEST/f'{PREFIX}_validacao.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('DONE',str(BLEND),flush=True)
