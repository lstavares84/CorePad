"""Editable Blender concept for the selected ALPHA 3x3 macropad.

Run with: blender --background --python alpha_blender.py
Units are millimetres. This is an appearance and packaging study, not a
manufacturing-ready mechanical or electronic design.
"""

import bpy
import math
from pathlib import Path
from mathutils import Vector

OUT = Path(__file__).resolve().parent / "alpha_blender"
OUT.mkdir(exist_ok=True)
VERSION = "1.0.0"
PREFIX = f"Alpha_v{VERSION}"
RENDERS = (
    "frente_esquerda",
    "traseira_USB-C",
    "vista_superior",
    "lateral_microSD_P2",
)
DELIVERABLES = [OUT / f"{PREFIX}.blend"] + [OUT / f"{PREFIX}_{name}.png" for name in RENDERS]
existing = [path for path in DELIVERABLES if path.exists()]
if existing:
    raise FileExistsError(
        "Esta versao ja existe. Aumente VERSION antes de gerar outro refinamento: "
        + ", ".join(str(path) for path in existing)
    )

bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
bpy.context.scene.unit_settings.system = "METRIC"
bpy.context.scene.unit_settings.scale_length = 0.001
bpy.context.scene.unit_settings.length_unit = "MILLIMETERS"

W, D, H = 104.0, 84.0, 15.0
TOP = H


def mat(name, color, metallic=0, roughness=.5, emission=0):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.use_nodes = True
    p = m.node_tree.nodes.get("Principled BSDF")
    p.inputs["Base Color"].default_value = (*color, 1)
    p.inputs["Metallic"].default_value = metallic
    p.inputs["Roughness"].default_value = roughness
    if emission:
        p.inputs["Emission Color"].default_value = (*color, 1)
        p.inputs["Emission Strength"].default_value = emission
    return m


body = mat("01 · carbon black enclosure", (.031, .034, .036), .33, .58)
top = mat("02 · finely textured matte top", (.043, .045, .047), .12, .74)
keymat = mat("03 · unmarked shallow matte keycaps", (.065, .067, .068), .04, .67)
metal = mat("04 · brushed dark nickel", (.38, .40, .40), .78, .33)
steel = mat("05 · polished switch metal", (.64, .66, .64), .83, .25)
black = mat("06 · genuine recessed openings", (.005, .006, .006), 0, .92)
glass = mat("07 · fingerprint contact surface", (.025, .031, .034), .18, .22)
green = mat("08 · continuous green frame #00FF00", (0, 1, 0), .1, .48, .08)
background = mat("09 · studio background", (.032, .034, .036), 0, .88)


def box(name, xyz, dims, material, bevel=0, segments=5):
    bpy.ops.mesh.primitive_cube_add(size=1, location=xyz)
    ob = bpy.context.object
    ob.name = name
    ob.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    ob.data.materials.append(material)
    if bevel:
        mod = ob.modifiers.new("Manufactured edge radius", "BEVEL")
        mod.width = bevel
        mod.segments = segments
        ob.modifiers.new("Weighted corner normals", "WEIGHTED_NORMAL")
    return ob


def cyl(name, xyz, radius, height, material, vertices=64, rotation=None):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=height, location=xyz)
    ob = bpy.context.object
    ob.name = name
    if rotation:
        ob.rotation_euler = rotation
    ob.data.materials.append(material)
    bevel = ob.modifiers.new("Soft circular rim", "BEVEL")
    bevel.width = min(.15, height / 4)
    bevel.segments = 3
    ob.modifiers.new("Weighted circular normals", "WEIGHTED_NORMAL")
    return ob


def rounded_loop(name, width, depth, corner, z, material, thickness):
    points = []
    for cx, cy, start in ((width/2-corner, depth/2-corner, 0),
                          (-width/2+corner, depth/2-corner, 90),
                          (-width/2+corner, -depth/2+corner, 180),
                          (width/2-corner, -depth/2+corner, 270)):
        for i in range(17):
            a = math.radians(start + 90*i/16)
            points.append((cx+corner*math.cos(a), cy+corner*math.sin(a), z))
    curve = bpy.data.curves.new(name, "CURVE")
    curve.dimensions = "3D"
    curve.resolution_u = 16
    curve.bevel_depth = thickness
    curve.bevel_resolution = 3
    spline = curve.splines.new("POLY")
    spline.points.add(len(points)-1)
    for p, coords in zip(spline.points, points):
        p.co = (*coords, 1)
    spline.use_cyclic_u = True
    ob = bpy.data.objects.new(name, curve)
    bpy.context.collection.objects.link(ob)
    ob.data.materials.append(material)
    return ob


def subtract(target, cutter, name):
    bpy.context.view_layer.objects.active = target
    mod = target.modifiers.new(name, "BOOLEAN")
    mod.operation = "DIFFERENCE"
    mod.solver = "EXACT"
    mod.object = cutter
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(cutter, do_unlink=True)


# The exterior has real port openings, not dark decals on solid walls.
enclosure = box("Enclosure | 104 × 84 × 15 mm concept envelope", (0, 0, H/2), (W, D, H), body, 3.3)
bpy.context.view_layer.objects.active = enclosure
bpy.ops.object.modifier_apply(modifier=enclosure.modifiers[0].name)

# The P2 and microSD occupy different stations along the left edge. The card
# opening is also higher on that edge, as requested and as seen in ALPHA.
p2_y, p2_z = -18.0, 5.3
sd_y, sd_z = 14.0, 10.7
cutter = cyl("CUT · left P2 opening", (-W/2, p2_y, p2_z), 2.05, 5.0, black, rotation=(0, math.pi/2, 0))
subtract(enclosure, cutter, "True P2 cylindrical cut")
cutter = box("CUT · microSD opening", (-W/2, sd_y, sd_z), (5, 11.5, 1.45), black, .35)
bpy.context.view_layer.objects.active = cutter
bpy.ops.object.modifier_apply(modifier=cutter.modifiers[0].name)
subtract(enclosure, cutter, "True microSD slot cut")
cutter = box("CUT · rear USB-C opening", (0, D/2, 7.3), (9.1, 5, 3.35), black, 1.55)
bpy.context.view_layer.objects.active = cutter
bpy.ops.object.modifier_apply(modifier=cutter.modifiers[0].name)
subtract(enclosure, cutter, "True rear USB-C cut")

# A subtly different top surface reinforces the floating key grid. The strip
# remains a single continuous part, with no LEDs below or within the keys.
box("Top panel · charcoal fine grain", (0, 0, H-.48), (W-1.0, D-1.0, .75), top, 3.0)
rounded_loop("APPROVED · uninterrupted green perimeter", W-7.6, D-7.6, 6.4, TOP+.04, green, .38)

# Nine identical, unprinted low keycaps, precisely aligned as 3 × 3.
for row, y in enumerate((20.0, 0.0, -20.0), 1):
    for col, x in enumerate((-33.0, -13.5, 6.0), 1):
        box(f"KEY {row}{col} | blank low cap", (x, y, TOP+.55), (18.0, 18.0, 1.10), keymat, 1.15)

# Right-hand controls. Short vertical 15 mm slider travel uses a 30 mm class
# component envelope, with a deliberately small movable thumb piece.
fx = 36.0
box("Volume | 15 mm VERTICAL fader base", (fx, .5, TOP+.10), (7.5, 32.0, .22), metal, 1.25)
box("Volume | dark vertical travel channel", (fx, .5, TOP+.23), (2.0, 26.0, .12), black, .45)
box("Volume | small sliding thumb", (fx, -1.0, TOP+.84), (7.2, 4.7, 1.20), metal, .52)
for dy in (-1.15, -.45, .25, .95):
    box("Thumb grip rib", (fx, -1.0+dy, TOP+1.48), (6.0, .19, .07), black, .07)

tx, ty = 36.0, 30.0
cyl("Microphone-only mute | switch washer", (tx, ty, TOP+.25), 4.4, .45, steel)
cyl("Microphone-only mute | black isolating collar", (tx, ty, TOP+.58), 2.85, .30, black)
lever = cyl("Microphone-only mute | mechanical toggle", (tx, ty, TOP+3.5), 1.22, 5.5, steel, 32)
lever.rotation_euler[1] = math.radians(12)
cyl("Microphone-only mute | rounded tip", (tx+.54, ty, TOP+6.55), 1.45, .8, steel, 32)

bx, by = 36.0, -26.0
cyl("Biometric | 20.8 mm sensor outer ring", (bx, by, TOP+.20), 10.4, .40, metal)
cyl("Biometric | black optical contact", (bx, by, TOP+.46), 9.3, .18, glass)
cyl("Biometric | slim inner ring", (bx, by, TOP+.52), 8.9, .10, black)
cyl("Biometric | exposed contact surface", (bx, by, TOP+.59), 8.55, .09, glass)

# Port hardware fits behind the actual openings. There is exactly one USB-C.
cyl("LEFT P2 | nickel socket surround", (-W/2-.08, p2_y, p2_z), 2.72, .20, metal,
    rotation=(0, math.pi/2, 0))
cyl("LEFT P2 | black jack bore", (-W/2-.21, p2_y, p2_z), 1.89, .16, black,
    rotation=(0, math.pi/2, 0))
box("LEFT microSD | recessed black slot", (-W/2-.12, sd_y, sd_z), (.16, 10.7, 1.18), black, .22)
box("LEFT microSD | thin visible metal lip", (-W/2-.16, sd_y, sd_z+1.0), (.12, 11.0, .20), metal, .08)
box("REAR USB-C | socket metal shell", (0, D/2+.07, 7.3), (8.7, .17, 3.10), metal, 1.48)
box("REAR USB-C | true dark inner cavity", (0, D/2+.19, 7.3), (6.9, .12, 1.90), black, .9)
box("REAR USB-C | internal tongue", (0, D/2+.27, 7.3), (4.9, .16, .42), metal, .18)

# Small unobtrusive acoustic apertures on the rear-facing upper strip.
for i in range(3):
    cyl("Rear acoustic inlet | microphone", (-5.0+i*2.5, 36.0, TOP+.04), .34, .11, black, 20)

for x in (-40, 40):
    for y in (-31, 31):
        cyl("Underside elastomer foot", (x, y, -.35), 3.2, .7, black, 32)


def camera(name, location, target, ortho):
    bpy.ops.object.camera_add(location=location)
    ob = bpy.context.object
    ob.name = name
    ob.rotation_euler = (Vector(target)-ob.location).to_track_quat("-Z", "Y").to_euler()
    ob.data.type = "ORTHO"
    ob.data.ortho_scale = ortho
    return ob


box("Studio floor", (0, 0, -1.25), (340, 340, 1.0), background)
world = bpy.context.scene.world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs["Color"].default_value = (.13, .14, .15, 1)
world.node_tree.nodes["Background"].inputs["Strength"].default_value = .45

for name, loc, power, size in (
    ("Large left softbox", (-70, -100, 135), 48000, 100),
    ("Right reflection softbox", (90, 35, 140), 38000, 75),
    ("Rear separation softbox", (-20, 90, 95), 27000, 65),
):
    bpy.ops.object.light_add(type="AREA", location=loc)
    lamp = bpy.context.object
    lamp.name = name
    lamp.data.energy = power
    lamp.data.shape = "DISK"
    lamp.data.size = size
    lamp.rotation_euler = (Vector((0, 0, 2))-lamp.location).to_track_quat("-Z", "Y").to_euler()

hero = camera("01 · ALPHA front-left hero | left ports visible", (-137, -133, 113), (0, 0, 8), 148)
rear = camera("02 · rear | USB-C visible", (87, 116, 73), (0, 0, 7), 143)
topcam = camera("03 · top | exactly nine blank keys", (0, 0, 185), (0, 0, 7), 120)
leftcam = camera("04 · left side | microSD above P2", (-150, 0, 30), (-52, 0, 7), 105)

scene = bpy.context.scene
scene.render.engine = "CYCLES"
scene.cycles.samples = 40
scene.cycles.use_denoising = False
bpy.context.view_layer.cycles.use_denoising = False
scene.render.resolution_x = 1400
scene.render.resolution_y = 1050
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.film_transparent = False
scene.view_settings.view_transform = "AgX"
scene.view_settings.look = "AgX - Medium High Contrast"
scene.view_settings.exposure = .7
scene.camera = hero
bpy.ops.wm.save_as_mainfile(filepath=str(OUT / f"{PREFIX}.blend"))

for cam, name in zip((hero, rear, topcam, leftcam), RENDERS):
    filename = f"{PREFIX}_{name}.png"
    scene.camera = cam
    scene.render.filepath = str(OUT / filename)
    bpy.ops.render.render(write_still=True)
    print("RENDERED", filename, flush=True)

print("FINISHED Alpha 3x3", flush=True)
