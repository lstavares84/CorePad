"""Three editable Blender concept models for the biometric recording macropad.

Run: blender --background --python blender_macropad_concepts.py
Dimensions are exploratory millimetres, not a manufacturing specification.
"""

import bpy
import math
from mathutils import Vector
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "blender_concepts"
ROOT.mkdir(exist_ok=True)


def material(name, rgb, metallic=0, roughness=0.45, emission=0):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*rgb, 1)
    m.use_nodes = True
    p = m.node_tree.nodes.get("Principled BSDF")
    p.inputs["Base Color"].default_value = (*rgb, 1)
    p.inputs["Metallic"].default_value = metallic
    p.inputs["Roughness"].default_value = roughness
    if emission:
        p.inputs["Emission Color"].default_value = (*rgb, 1)
        p.inputs["Emission Strength"].default_value = emission
    return m


def cube(name, location, scale, mat, bevel=0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    o = bpy.context.object
    o.name = name
    o.dimensions = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(mat)
    if bevel:
        b = o.modifiers.new("Rounded edges", "BEVEL")
        b.width = bevel
        b.segments = 4
        b.affect = "EDGES"
        o.modifiers.new("Weighted normals", "WEIGHTED_NORMAL")
    return o


def cylinder(name, location, radius, depth, mat, vertices=48, rot=None):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=location)
    o = bpy.context.object
    o.name = name
    if rot:
        o.rotation_euler = rot
    o.data.materials.append(mat)
    o.modifiers.new("Weighted normals", "WEIGHTED_NORMAL")
    return o


def curve_line(name, points, mat, radius=0.35):
    c = bpy.data.curves.new(name, "CURVE")
    c.dimensions = "3D"
    c.resolution_u = 16
    c.bevel_depth = radius
    c.bevel_resolution = 3
    s = c.splines.new("POLY")
    s.points.add(len(points)-1)
    for i, xyz in enumerate(points):
        s.points[i].co = (*xyz, 1)
    o = bpy.data.objects.new(name, c)
    bpy.context.collection.objects.link(o)
    o.data.materials.append(mat)
    return o


def perimeter(w, d, z, r, green):
    pts = []
    for cx, cy, start in [(w/2-r,d/2-r,0),(-w/2+r,d/2-r,90),(-w/2+r,-d/2+r,180),(w/2-r,-d/2+r,270)]:
        for j in range(9):
            a = math.radians(start + j*90/8)
            pts.append((cx+r*math.cos(a),cy+r*math.sin(a),z))
    pts.append(pts[0])
    curve_line("Continuous green frame inlay", pts, green, .45)


def ports(w,d,base_z,mat_black,mat_metal):
    # Both openings are on the left side, with microSD physically above P2.
    x=-w/2-.15
    cylinder("P2 headphone socket dark opening LEFT",(x,-d*.13,4.45),1.8,.35,mat_black,rot=(0,math.pi/2,0))
    cylinder("P2 headphone socket metal rim LEFT",(x+.03,-d*.13,4.45),2.55,.12,mat_metal,rot=(0,math.pi/2,0))
    cylinder("P2 headphone socket visible centre",(x-.07,-d*.13,4.45),1.75,.18,mat_black,rot=(0,math.pi/2,0))
    cube("microSD narrow slot ABOVE P2 LEFT",(x,-d*.13,10.0),(.18,11.0,1.65),mat_black,.35)
    cube("microSD slot metallic edge ABOVE P2 LEFT",(x+.07,-d*.13,11.0),(.16,11.0,.35),mat_metal,.12)
    # A single USB-C on the rear face.
    cube("USB-C socket metal shell REAR",(0,d/2+.10,6.7),(8.6,.25,3.25),mat_metal,1.0)
    cube("USB-C dark cavity REAR",(0,d/2+.27,6.7),(6.9,.12,2.1),mat_black,.75)


def key(name,x,y,z,w,h,mats,style):
    if style == "soft":
        cube(name,(x,y,z+.48),(w,h,.95),mats["key"],1.25)
    elif style == "tile":
        cube(name,(x,y,z+.40),(w,h,.80),mats["key"],.45)
    else:
        cube(name,(x,y,z+.50),(w,h,1.0),mats["key"],2.2)


def fingerprint(x,y,z,mats,shape):
    if shape == "square":
        cube("Biometric sensor recessed bezel",(x,y,z+.12),(13,13,.35),mats["metal"],1.9)
        cube("Biometric touch surface",(x,y,z+.34),(11.5,11.5,.25),mats["glass"],1.5)
    else:
        cylinder("Biometric sensor recessed bezel",(x,y,z+.18),7.0,.36,mats["metal"])
        cylinder("Biometric touch surface",(x,y,z+.40),6.1,.19,mats["glass"])
    # Concentric rim is a material detail, not a marking on any key.


def controls(fx, f_y, travel, tx, ty, bx, by, z, mats, switch_style):
    cube("Vertical slider track RIGHT",(fx,f_y,z+.08),(4.9,travel,.2),mats["recess"],2.1)
    cube("Small volume slider cap RIGHT",(fx,f_y-travel*.12,z+.91),(5.8,6.0,1.45),mats["metal"],1.0)
    cube("Slider cap green detail",(fx,f_y-travel*.12-2.75,z+1.67),(5.1,.55,.18),mats["green"],.18)
    cylinder("Mic mute switch base RIGHT",(tx,ty,z+.27),3.45,.52,mats["metal"])
    if switch_style == "flip":
        o=cube("Mechanical mic mute lever RIGHT",(tx,ty+.2,z+2.9),(2.2,4.5,5.0),mats["metal"],.55)
        o.rotation_euler[0]=math.radians(18)
    elif switch_style == "low":
        cube("Mechanical mic mute lever RIGHT",(tx,ty,z+1.1),(4.7,3.0,1.8),mats["metal"],.6)
    else:
        cylinder("Mechanical mic mute lever RIGHT",(tx,ty,z+2.05),1.25,3.9,mats["metal"],16,rot=(math.radians(12),0,0))
    fingerprint(bx,by,z,mats,"square" if switch_style=="low" else "round")


def studio(w,d,mats):
    cube("Studio ground",(0,0,-.5),(360,360,1),mats["ground"],0)
    world=bpy.context.scene.world
    world.color=(.3,.3,.3)
    world.use_nodes=True
    world.node_tree.nodes["Background"].inputs["Color"].default_value=(.32,.35,.37,1)
    world.node_tree.nodes["Background"].inputs["Strength"].default_value=.5
    def area(name,loc,power,size):
        bpy.ops.object.light_add(type="AREA", location=loc)
        a=bpy.context.object
        a.name=name
        a.data.energy=power
        a.data.shape="DISK"
        a.data.size=size
        a.rotation_euler=(Vector((0,0,0))-a.location).to_track_quat("-Z","Y").to_euler()
    area("Softbox left",(-120,-150,180),45000,120)
    area("Softbox right",(120,100,170),52000,110)
    area("Edge light",(-35,120,110),28000,90)
    bpy.ops.object.camera_add(location=(-w*1.45,-d*1.65,max(w,d)*1.2))
    camera=bpy.context.object
    camera.name="Hero camera - front and left ports"
    camera.rotation_euler=(Vector((0,0,4))-camera.location).to_track_quat("-Z","Y").to_euler()
    camera.data.type="ORTHO"
    camera.data.ortho_scale=max(w*1.54,d*1.8)
    bpy.context.scene.camera=camera
    return camera


def camera_rear(w,d):
    bpy.ops.object.camera_add(location=(w*.9,d*1.55,w*.72))
    c=bpy.context.object
    c.name="Rear camera - USB-C"
    c.rotation_euler=(Vector((0,0,5))-c.location).to_track_quat("-Z","Y").to_euler()
    c.data.type="ORTHO"
    c.data.ortho_scale=max(w*1.55,d*1.75)
    return c


CONCEPTS=[
    dict(n="01_Grade_Panoramica",w=121,d=82,h=13,cols=4,rows=3,x0=-43.7,y0=20.7,pitch_x=20.0,pitch_y=20.0,
         ksize=(18.5,18.0),key_style="tile",body_bevel=5.0,control=(43,-4,31,43,27,43,-29),switch="flip",
         description="4 x 3; compact horizontal keyboard; fingerprint below the right controls."),
    dict(n="02_Quadrado_Compacto",w=104,d=106,h=13,cols=3,rows=4,x0=-34,y0=31.5,pitch_x=20.5,pitch_y=20.5,
         ksize=(18.2,18.6),key_style="soft",body_bevel=7.0,control=(33,-5,43,33,38,33,-39),switch="low",
         description="3 x 4; narrow near-square footprint; square fingerprint below the right controls."),
    dict(n="03_Biometria_Superior",w=120,d=96,h=14,cols=4,rows=3,x0=-42,y0=12,pitch_x=20.1,pitch_y=20.1,
         ksize=(18.2,18.5),key_style="rounded",body_bevel=8.0,control=(43,-11,38,43,24,-10,31),switch="pin",
         description="4 x 3; biometric sensor in a narrow top band; fader plus mute at the right."),
]


def build(c):
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for m in list(bpy.data.materials):
        bpy.data.materials.remove(m)
    mats={
        "body":material("carbon black anodised enclosure",(.025,.029,.031),.53,.47),
        "top":material("fine grain top panel",(.044,.048,.050),.25,.67),
        "key":material("blank low profile keycaps",(.065,.070,.073),.14,.58),
        "metal":material("dark brushed metal controls",(.34,.38,.40),.77,.33),
        "glass":material("biometric glass sensing area",(.045,.082,.076),.19,.22),
        "green":material("approved 00FF00 frame inlay",(.02,.84,.015),.18,.35,.10),
        "recess":material("black cavities",(.005,.007,.008),.0,.91),
        "ground":material("neutral studio ground",(.37,.40,.41),.0,.88),
    }
    w,d,h=c["w"],c["d"],c["h"]
    cube("Compact enclosure",(0,0,h*.5),(w,d,h),mats["body"],c["body_bevel"])
    inset=c["body_bevel"]+.4
    perimeter(w-2*inset,d-2*inset,h+.04,max(2,c["body_bevel"]-1),mats["green"])
    for row in range(c["rows"]):
        for col in range(c["cols"]):
            x=c["x0"]+col*c["pitch_x"]
            y=c["y0"]-row*c["pitch_y"]
            key(f"Blank low key {row+1:02d}-{col+1:02d}",x,y,h,c["ksize"][0],c["ksize"][1],mats,c["key_style"])
    controls(*c["control"],h,mats,c["switch"])
    ports(w,d,h,mats["recess"],mats["metal"])
    # Discreet acoustic ports on the top edge, separate from the blank keycaps.
    for x in [-2.0,1.0,4.0]:
        cylinder("Room microphone acoustic opening",(x,d/2-c["body_bevel"]-2.2,h-.03),.55,.12,mats["recess"],16)
    hero=studio(w,d,mats)
    rear=camera_rear(w,d)
    scene=bpy.context.scene
    scene.render.engine="CYCLES"
    scene.cycles.samples=64
    scene.cycles.use_denoising=False
    bpy.context.view_layer.cycles.use_denoising=False
    scene.render.resolution_x=1500
    scene.render.resolution_y=1100
    scene.render.resolution_percentage=100
    scene.render.image_settings.file_format="PNG"
    scene.view_settings.view_transform="AgX"
    scene.view_settings.exposure=.45
    scene.render.film_transparent=False
    scene.camera=hero
    bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/(c["n"]+".blend")))
    scene.render.filepath=str(ROOT/(c["n"]+"_frente.png"))
    bpy.ops.render.render(write_still=True)
    scene.camera=rear
    scene.render.filepath=str(ROOT/(c["n"]+"_traseira.png"))
    bpy.ops.render.render(write_still=True)
    print("DONE",c["n"],c["description"],flush=True)


for concept in CONCEPTS:
    build(concept)
