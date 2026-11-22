"""Technical render of the actual KiCad 0.3.0 boards in the nominal case."""
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parent
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene
scene.render.engine='CYCLES';scene.cycles.samples=48
scene.cycles.use_denoising=False
bpy.context.view_layer.cycles.use_denoising=False
scene.render.resolution_x=1700;scene.render.resolution_y=1250;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'
scene.view_settings.view_transform='Standard';scene.view_settings.look='Medium High Contrast';scene.view_settings.exposure=1.5
scene.world.use_nodes=True
scene.world.node_tree.nodes.get('Background').inputs['Color'].default_value=(.5,.52,.55,1)
scene.world.node_tree.nodes.get('Background').inputs['Strength'].default_value=.55

def material(name,color,metallic=0,alpha=1):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,alpha);m.use_nodes=True
 bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*color,1)
 bs.inputs['Metallic'].default_value=metallic;bs.inputs['Roughness'].default_value=.4
 if alpha<1:
  bs.inputs['Alpha'].default_value=alpha;m.surface_render_method='DITHERED'
 return m

def point(obj,xyz): obj.rotation_euler=(Vector(xyz)-obj.location).to_track_quat('-Z','Y').to_euler()

colors={
 'base_plastica':((.08,.09,.1),0,.26),'tampa_carbono':((.14,.15,.16),0,.35),
 'difusor_rgb_base':((.08,.8,.17),0,1),'pcb_main_v0_3':((.03,.31,.18),0,1),
 'pcb_ui_v0_3':((.04,.37,.24),0,1),'battery':((.26,.28,.3),.3,1),
 'battery_positive':((.8,.05,.04),0,1),'battery_negative':((.02,.02,.025),0,1),
 'keycaps_9_reserva':((.12,.13,.15),0,1),'biometria_reserva':((.12,.16,.19),0,1),
 'fader_comando_reserva':((.28,.29,.3),.25,1),'mute_comando_reserva':((.28,.29,.3),.25,1),
 'botao_camada':((.2,.21,.22),0,1),'botao_gravacao':((.7,.05,.04),0,1),
}
for stl in sorted((ROOT/'render_meshes').glob('*.stl')):
 name=stl.stem
 bpy.ops.wm.stl_import(filepath=str(stl))
 obj=bpy.context.object;obj.name=name
 if name in colors: color,metal,alpha=colors[name]
 elif name.startswith('SW'):color,metal,alpha=(.27,.28,.3),0,1
 elif name.startswith('FFC'):color,metal,alpha=(.8,.56,.19),0,.75
 elif name.startswith(('USB','microSD','P2')):color,metal,alpha=(.62,.65,.68),.6,1
 else:color,metal,alpha=(.15,.17,.18),.12,1
 obj.data.materials.append(material(name,color,metal,alpha))

def light(name,loc,power,size):
 d=bpy.data.lights.new(name,'AREA');d.energy=power;d.shape='DISK';d.size=size
 o=bpy.data.objects.new(name,d);scene.collection.objects.link(o);o.location=loc;point(o,(0,0,15))
light('key',(30,-65,110),2400,100);light('rim',(-70,45,95),1600,80);light('front',(0,-90,50),700,80)
bpy.ops.object.camera_add(location=(126,-145,115));cam=bpy.context.object;point(cam,(0,0,16));cam.data.type='ORTHO';cam.data.ortho_scale=174;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=1000,location=(0,0,-2));bpy.context.object.data.materials.append(material('background',(.11,.12,.14)))
scene.render.filepath=str(ROOT/'montagem_PCB_match_v0.2.0.png')
bpy.ops.render.render(write_still=True)
print(scene.render.filepath)
