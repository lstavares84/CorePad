"""Render the actual plastic-part study for the README without modifying its source.
Run: blender -b --python docs/render/render_mechanical.py
"""
from pathlib import Path
import bpy
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/images'
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'development/mechanical/v0.1.0/Beta_Pecas_v0.1.0.blend'))
scene=bpy.context.scene
parts={o.name:o for o in bpy.data.objects if o.type=='MESH'}
for o in parts.values():
    o.location*=.001;o.scale*=.001
scene.unit_settings.scale_length=1
def material(name,color,rough=.4):
    m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
    bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*color,1);bs.inputs['Roughness'].default_value=rough
    return m
body=material('Plastico isolante para prototipo',(.075,.09,.105))
lid=material('Tampa sem revestimento',(.36,.40,.44))
diff=material('Difusor translúcido - visualizacao verde',(.08,.65,.13),.3)
button=material('Botoes',(.015,.021,.027))
for name,o in parts.items():
    o.data.materials.clear();o.data.materials.append(diff if 'Difusor' in name else lid if 'Tampa' in name else button if 'Botao' in name else body)
    normal=o.modifiers.new('Normais para render','WEIGHTED_NORMAL');normal.keep_sharp=True
world=bpy.data.worlds.new('Estudio');world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.65,.69,.75,1);world.node_tree.nodes['Background'].inputs[1].default_value=.35;scene.world=world
def point(obj,target):obj.rotation_euler=(Vector(target)-obj.location).to_track_quat('-Z','Y').to_euler()
for xyz,power,size in [((-.10,-.12,.25),12,.16),((.13,-.01,.18),8,.12),((0,.16,.22),14,.14)]:
    bpy.ops.object.light_add(type='AREA',location=xyz);light=bpy.context.object;light.data.energy=power*.12;light.data.shape='DISK';light.data.size=size;point(light,(0,0,.04))
bpy.ops.object.camera_add(location=(-.18,-.23,.18));camera=bpy.context.object;camera.data.type='ORTHO';camera.data.ortho_scale=.175;camera.data.clip_start=.001;point(camera,(0,0,.04));scene.camera=camera
scene.render.engine='CYCLES';scene.cycles.samples=64;scene.cycles.use_denoising=False
bpy.context.view_layer.cycles.use_denoising=False
scene.render.resolution_x=1500;scene.render.resolution_y=1200;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.render.film_transparent=False
scene.view_settings.view_transform='AgX'
original={name:o.location.copy() for name,o in parts.items()}
def render(name):
    scene.render.filepath=str(OUT/(name+'.png'));bpy.ops.render.render(write_still=True)
# Exploded geometry: separate the ring and lid vertically to reveal real openings.
parts['Difusor_RGB'].location.z+=.038
parts['Tampa_carbono'].location.z+=.036
for name in ('Botao_camada','Botao_gravacao'):parts[name].location.z+=.051
render('pecas_explodidas')
for name,o in parts.items():o.location=original[name];o.hide_render=name!='Base_plastica'
camera.location=(-.13,-.16,.19);point(camera,(0,0,.009));camera.data.ortho_scale=.147
render('base_interior')
for name,o in parts.items():o.hide_render=name!='Tampa_carbono'
camera.location=(0,0,.24);point(camera,(0,0,.027));camera.data.ortho_scale=.132
render('tampa_tecnica')
print('README mechanical views rendered from the editable source')
