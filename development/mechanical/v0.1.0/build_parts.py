"""Plastic fit-study parts for CorePad Beta; run Blender in background.
All dimensions in mm; STL exports use mm coordinates for slicers.
"""
import bpy, bmesh, json
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parent
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=.001
def box(name,center,size,radius=0):
    bpy.ops.mesh.primitive_cube_add(size=1,location=center);o=bpy.context.object;o.name=name;o.dimensions=size
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if radius:
        modifier=o.modifiers.new('Raio','BEVEL');modifier.width=radius;modifier.segments=8
        bpy.ops.object.modifier_apply(modifier=modifier.name)
    return o
def cut(target,tool):
    bpy.context.view_layer.objects.active=target
    modifier=target.modifiers.new('Recorte','BOOLEAN');modifier.operation='DIFFERENCE';modifier.solver='EXACT';modifier.object=tool
    bpy.ops.object.modifier_apply(modifier=modifier.name);bpy.data.objects.remove(tool,do_unlink=True)
def union(target,tool):
    bpy.context.view_layer.objects.active=target
    modifier=target.modifiers.new('Ponte interna','BOOLEAN');modifier.operation='UNION';modifier.solver='EXACT';modifier.object=tool
    bpy.ops.object.modifier_apply(modifier=modifier.name);bpy.data.objects.remove(tool,do_unlink=True)
def cylinder(name,center,radius,depth):
    bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=radius,depth=depth,location=center);o=bpy.context.object;o.name=name;return o
base=box('Base_plastica',(0,0,13),(104,84,26),2)
cut(base,box('Interior',(0,0,15),(100,80,26),1.5))
# Common center of base plus lid (0 to 28.4), excluding protruding controls.
PORT_Z=14.2
cut(base,box('USB_C',(0,42,PORT_Z),(10.2,8,4.4),.7))
p2=cylinder('P2',(-52,-18,PORT_Z),3.2,8);p2.rotation_euler[1]=1.57079632679;cut(base,p2)
cut(base,box('SD',(-52,14,PORT_Z),(8,13,3),.5))
for side in (-1,1):
    for y in (25.5,27.5,29.5,31.5):
        hole=cylinder('Microfone',(side*51,y,PORT_Z),.6,8);hole.rotation_euler[1]=1.57079632679;cut(base,hole)
# Diffuser slot: base has lower floor lip and vertical opening for a separately
# printed ring. Assembly/retention and PCB supports need a later mechanical review.
outer=box('Corte_faixa',(0,0,2),(106,86,1.4),.4)
inner=box('Miolo',(0,0,2),(99,79,5),.4);cut(outer,inner);cut(base,outer)
# Hidden inner corner bridges keep the floor connected to the upper walls across
# the light channel. The luminous path stays on the outer skin of the diffuser.
for x in (-48,48):
    for y in (-38,38):union(base,box('Ponte_estrutural',(x,y,3.5),(5,5,7),.5))
lid=box('Tampa_carbono',(0,0,27.2),(104,84,2.4),1)
for y in (20.5,0,-20.5):
    for x in (-33,-13,7):cut(lid,box('Abertura_tecla',(x,y,27),(19.6,19.6,8),1))
for x,y,r in [(35.5,-26.5,10.65),(35.5,29,3.3),(8.5,34.4,2.3)]:cut(lid,cylinder('Abertura',(x,y,27),r,8))
cut(lid,box('Fader',(35.5,2,27),(7.5,26.5,8),1))
cut(lid,box('Seletor',(-13,34.4,27),(6.6,3.6,8),.8))
for x in (-7.2,-4.7,-2.2):cut(lid,cylinder('LED',(x,34.4,27),.7,8))
diffuser=box('Difusor_RGB',(0,0,2),(103.8,83.8,1.1),.35)
cut(diffuser,box('Interior_difusor',(0,0,2),(99.3,79.3,5),.4))
for x in (-48,48):
    for y in (-38,38):cut(diffuser,box('Folga_ponte',(x,y,2),(5.3,5.3,5),.5))
layer=box('Botao_camada',(-13,34.4,28.6),(6,3,.8),.35)
record=cylinder('Botao_gravacao',(8.5,34.4,28.6),2,.8)
parts=[base,lid,diffuser,layer,record]
for o in parts:
    o['Revisao']='Beta mecanica 0.1.0 - estudo de encaixe'
    o['Limites']='Sem fixacoes, suportes PCB ou retencao do difusor validados; nao usar como carcaça final.'
scene['Dimensoes']='104 x 84 x 28.4 mm, excluindo comandos; espessura exploratoria'
scene['Acabamento']='Carbono visual sobre estrutura plastica isolante; proposta de processo'
scene['Filete_verde_superior']=False
scene['Exportacao_STL']='STL em mm; blend com scale_length 0.001'
checks=[]
for o in parts:
    bm=bmesh.new();bm.from_mesh(o.data);unseen=set(bm.verts);components=0
    while unseen:
        components+=1;stack=[unseen.pop()]
        while stack:
            vertex=stack.pop()
            for edge in vertex.link_edges:
                neighbor=edge.other_vert(vertex)
                if neighbor in unseen:unseen.remove(neighbor);stack.append(neighbor)
    check={'part':o.name,'connected_components':components,'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'volume_mm3':bm.calc_volume()}
    bm.free();checks.append(check)
    assert check['connected_components']==1 and check['nonmanifold_edges']==0 and check['volume_mm3']>0,check
(ROOT/'validation.json').write_text(json.dumps(checks,indent=2)+'\n')
for o in parts:
    bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
    # Local origin at the bottom of each part, ready for slicer import.
    original=o.location.copy();mins=min((o.matrix_world@Vector(v)).z for v in o.bound_box)
    o.location.z-=mins
    bpy.ops.wm.stl_export(filepath=str(ROOT/(o.name+'.stl')),export_selected_objects=True,apply_modifiers=True)
    o.location=original
bpy.ops.object.select_all(action='SELECT')
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'Beta_Pecas_v0.1.0.blend'))
print('Exported five fit-study parts in STL and editable Blender assembly')
