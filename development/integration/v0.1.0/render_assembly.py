"""Render engineering views from the exact CAD STL exports; Blender 4.3."""
import sys
from pathlib import Path
import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parent
view = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else "exploded"
assert view in ("exploded", "open", "assembled", "routing")
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
scene = bpy.context.scene
scene.unit_settings.system = "METRIC"
scene.unit_settings.scale_length = .001
scene.render.engine = "CYCLES"
scene.cycles.samples = 64
scene.cycles.use_denoising = False
bpy.context.view_layer.cycles.use_denoising = False
scene.render.resolution_x = 1600
scene.render.resolution_y = 1200
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.film_transparent = False
scene.view_settings.view_transform = "Standard"
scene.view_settings.look = "Medium High Contrast"
scene.view_settings.exposure = 2.2
scene.world.use_nodes = True
scene.world.node_tree.nodes.get("Background").inputs["Color"].default_value = (.5, .55, .6, 1)
scene.world.node_tree.nodes.get("Background").inputs["Strength"].default_value = .55


def mat(name, color, metallic=0, rough=.38, alpha=1):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, alpha)
    m.use_nodes = True
    p = m.node_tree.nodes.get("Principled BSDF")
    p.inputs["Base Color"].default_value = (*color, 1)
    p.inputs["Metallic"].default_value = metallic
    p.inputs["Roughness"].default_value = rough
    if alpha < 1:
        p.inputs["Alpha"].default_value = alpha
        m.surface_render_method = "DITHERED"
    return m


materials = {
    "base_plastica": mat("PA12 grafite", (.065, .07, .08), rough=.46, alpha=.45 if view in ("open", "routing") else 1),
    "tampa_carbono": mat("carbono visual", (.06, .065, .07), rough=.28),
    "difusor_rgb_base": mat("difusor verde", (.08, .85, .11), rough=.19),
    "pcb_principal_kicad": mat("FR4 principal", (.025, .19, .13), rough=.31, alpha=.5 if view == "routing" else 1),
    "pcb_ui_reserva": mat("FR4 UI", (.04, .24, .16), rough=.34, alpha=.73 if view == "open" else 1),
    "bateria_reserva": mat("celula de reserva", (.27, .29, .32), metallic=.5),
    "usb_c_reserva": mat("metal USB", (.55, .57, .6), metallic=.8),
    "p2_reserva": mat("metal P2", (.52, .54, .57), metallic=.8),
    "micro_sd_reserva": mat("metal SD", (.52, .54, .57), metallic=.8),
    "ffc_ui_principal": mat("FFC ambar", (.78, .48, .11), rough=.38),
    "ffc_conector_principal": mat("conector FFC", (.8, .68, .4)),
    "ffc_conector_ui": mat("conector FFC", (.8, .68, .4)),
    "bateria_cabo_positivo": mat("fio vermelho", (.7, .035, .025)),
    "bateria_cabo_negativo": mat("fio preto", (.025, .025, .03)),
    "switches_9_reserva": mat("switches", (.22, .23, .25)),
    "keycaps_9_reserva": mat("caps carbono", (.11, .12, .14), rough=.3),
    "biometria_reserva": mat("sensor", (.11, .14, .17), rough=.2),
    "fader_comando_reserva": mat("fader", (.3, .31, .33), metallic=.25),
    "mute_comando_reserva": mat("mute", (.31, .32, .34), metallic=.25),
    "botao_camada": mat("camada", (.2, .21, .23)),
    "botao_gravacao": mat("gravacao", (.7, .035, .025)),
}
offsets = {"base_plastica": -20, "difusor_rgb_base": -20,
           "pcb_principal_kicad": 9, "usb_c_reserva": 9,
           "p2_reserva": 9, "micro_sd_reserva": 9,
           "pcb_ui_reserva": 22,
           "switches_9_reserva": 22, "keycaps_9_reserva": 37,
           "tampa_carbono": 37, "biometria_reserva": 37,
           "fader_comando_reserva": 37, "mute_comando_reserva": 37,
           "botao_camada": 37, "botao_gravacao": 37}
hide_exploded = {"ffc_ui_principal", "ffc_conector_principal", "ffc_conector_ui",
                 "bateria_cabo_positivo", "bateria_cabo_negativo"}
for name, material in materials.items():
    if view == "exploded" and name in hide_exploded:
        continue
    if view == "open" and name == "tampa_carbono":
        continue
    if view == "routing" and name in {"tampa_carbono", "pcb_ui_reserva", "switches_9_reserva",
                                       "keycaps_9_reserva", "biometria_reserva", "fader_comando_reserva",
                                       "mute_comando_reserva", "botao_camada", "botao_gravacao"}:
        continue
    bpy.ops.wm.stl_import(filepath=str(ROOT / "parts" / (name + ".stl")))
    o = bpy.context.object
    o.name = name
    o.data.materials.append(material)
    if view == "exploded":
        o.location.z += offsets.get(name, 0)


def point(obj, xyz):
    obj.rotation_euler = (Vector(xyz) - obj.location).to_track_quat("-Z", "Y").to_euler()


def area(name, xyz, power, size):
    data = bpy.data.lights.new(name, "AREA")
    data.energy = power
    data.shape = "DISK"
    data.size = size
    obj = bpy.data.objects.new(name, data)
    scene.collection.objects.link(obj)
    obj.location = xyz
    point(obj, (0, 0, 25))


area("softbox principal", (35, -55, 120), 2300, 100)
area("softbox recorte", (-70, 55, 95), 1700, 80)
area("luz frontal", (0, -110, 45), 800, 85)
bpy.ops.object.camera_add(location=(126, 130 if view == "routing" else -155,
                                    117 if view in ("open", "routing") else 152))
camera = bpy.context.object
point(camera, (0, 0, 22 if view == "exploded" else 25))
camera.data.type = "ORTHO"
camera.data.ortho_scale = 205 if view == "exploded" else 172
scene.camera = camera

ground = mat("fundo tecnico", (.075, .085, .10), rough=.8)
bpy.ops.mesh.primitive_plane_add(size=1000, location=(0, 0, -22 if view == "exploded" else -2))
bpy.context.object.name = "fundo"
bpy.context.object.data.materials.append(ground)

scene.render.filepath = str(ROOT / f"montagem_{view}.png")
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT / f"CorePad_Beta_{view}_v0.1.0.blend"))
bpy.ops.render.render(write_still=True)
print(f"Rendered {scene.render.filepath}")
