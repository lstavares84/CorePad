"""Parametric CorePad Beta fit study. Units: mm, origin: case centre at bottom.

Run with CadQuery 2.8 after exporting the real KiCad board outline to STEP.
The UI PCB, connector bodies, battery and cables are *envelopes*, not released parts.
"""
from pathlib import Path
import json
import cadquery as cq

ROOT = Path(__file__).resolve().parent
PARTS = ROOT / "parts"
PARTS.mkdir(exist_ok=True)


def rounded_box(x, y, z, dx, dy, dz, radius=0):
    solid = cq.Workplane("XY").box(dx, dy, dz)
    if radius:
        solid = solid.edges("|Z").fillet(radius)
    return solid.translate((x, y, z))


def aperture_cylinder(x, y, radius):
    return cq.Workplane("XY").center(x, y).circle(radius).extrude(40)


# Case: 104 x 84 x 28.4. The lower illuminated band is the only RGB band.
base = rounded_box(0, 0, 13, 104, 84, 26, 2)
base = base.cut(rounded_box(0, 0, 15, 100, 80, 26, 1.5))
ring_cut = rounded_box(0, 0, 2, 106, 86, 1.4, .4).cut(
    rounded_box(0, 0, 2, 99, 79, 3, .4))
base = base.cut(ring_cut)
for x in (-48, 48):
    for y in (-38, 38):
        base = base.union(rounded_box(x, y, 3.5, 5, 5, 7, .5))
base = base.cut(rounded_box(0, 42, 14.2, 10.2, 8, 4.4, .7))
base = base.cut(rounded_box(-52, 14, 14.2, 8, 13, 3, .5))
base = base.cut(cq.Workplane("YZ").center(-18, 14.2).circle(3.2).extrude(8).translate((-56, 0, 0)))
for side in (-1, 1):
    for y in (25.5, 27.5, 29.5, 31.5):
        mic = cq.Workplane("YZ").center(y, 14.2).circle(.6).extrude(8)
        base = base.cut(mic.translate(((48 if side == 1 else -56), 0, 0)))

lid = rounded_box(0, 0, 27.2, 104, 84, 2.4, 1)
for y in (20.5, 0, -20.5):
    for x in (-33, -13, 7):
        lid = lid.cut(rounded_box(x, y, 27.2, 19.6, 19.6, 8, 1))
for x, y, radius in ((35.5, -26.5, 10.65), (35.5, 29, 3.3), (8.5, 34.4, 2.3)):
    lid = lid.cut(aperture_cylinder(x, y, radius))
lid = lid.cut(rounded_box(35.5, 2, 27.2, 7.5, 26.5, 8, 1))
lid = lid.cut(rounded_box(-13, 34.4, 27.2, 6.6, 3.6, 8, .8))
for x in (-7.2, -4.7, -2.2):
    lid = lid.cut(aperture_cylinder(x, 34.4, .7))

diffuser = rounded_box(0, 0, 2, 103.8, 83.8, 1.1, .35).cut(
    rounded_box(0, 0, 2, 99.3, 79.3, 3, .4))
for x in (-48, 48):
    for y in (-38, 38):
        diffuser = diffuser.cut(rounded_box(x, y, 2, 5.3, 5.3, 3, .5))

# The imported main PCB is native KiCad board geometry, including its outline.
main = cq.importers.importStep(str(ROOT / "pcb_principal_kicad.step")).translate((0, 0, 12.6))
ui = cq.importers.importStep(str(ROOT / "pcb_ui_kicad.step")).translate((0, 0, 20.4))
battery = rounded_box(-18, -8, 6.5, 60, 36, 7, 2)
# Component/connector volumes have no manufacturer model in the current design.
usb = rounded_box(0, 39.5, 14.2, 9, 6, 3.2, .6)
audio = rounded_box(-45.5, -18, 14.2, 5, 6, 6, .5).union(
    cq.Workplane("YZ").center(-18, 14.2).circle(3).extrude(4).translate((-52, 0, 0)))
sd = rounded_box(-47, 14, 14.2, 8, 13, 2, .4)
ffc = rounded_box(25, 27, 17.35, 8, .3, 6.1, .1)
ffc_main_socket = rounded_box(25, 27, 14.8, 10, 2, 1.2, .2)
ffc_ui_socket = rounded_box(25, 27, 19.8, 10, 2, 1.2, .2)


def cable(points, radius):
    pieces = []
    for first, last in zip(points, points[1:]):
        a, b = cq.Vector(*first), cq.Vector(*last)
        v = b.sub(a)
        pieces.append(cq.Solid.makeCylinder(radius, v.Length, a, v.normalized()))
    for p in points[1:-1]:
        pieces.append(cq.Solid.makeSphere(radius, cq.Vector(*p)))
    return cq.Compound.makeCompound(pieces)


battery_red = cable([(-47, -8, 10.2), (-45, -8, 11.2), (-40, -14, 11.2), (-38, -14, 12.6)], .35)
battery_black = cable([(-47, -10, 10.2), (-44, -10, 11.2), (-39, -16, 11.2), (-37, -16, 12.6)], .35)
key_centres = [(x, y) for y in (20.5, 0, -20.5) for x in (-33, -13, 7)]
switches = cq.Compound.makeCompound([
    rounded_box(x, y, 24.2, 16, 16, 4.4, .5).val() for x, y in key_centres])
keycaps = cq.Compound.makeCompound([
    rounded_box(x, y, 28.2, 18.4, 18.4, 2.8, 1).val() for x, y in key_centres])
bio = cq.Workplane("XY").center(35.5, -26.5).circle(10).extrude(2).translate((0, 0, 25.5))
fader = rounded_box(35.5, 2, 28.1, 6.5, 8, 2, .5)
mute = rounded_box(35.5, 29, 27.8, 4, 4, 2, .5)
layer_button = rounded_box(-13, 34.4, 28.6, 6, 3, .8, .35)
record_button = cq.Workplane("XY").center(8.5, 34.4).circle(2).extrude(.8).translate((0, 0, 28.2))

items = [
    ("base_plastica", base, (0.055, .06, .07), "revisao parametrica"),
    ("tampa_carbono", lid, (.12, .13, .14), "acabamento carbono visual"),
    ("difusor_rgb_base", diffuser, (.25, .9, .24), "translucido a selecionar"),
    ("pcb_principal_kicad", main, (.06, .22, .18), "KiCad 0.2.0; sem roteamento"),
    ("pcb_ui_reserva", ui, (.08, .3, .2), "contorno KiCad mecanico; sem pads ou roteamento"),
    ("bateria_reserva", battery, (.35, .36, .39), "60 x 36 x 7 mm; celula nao selecionada"),
    ("usb_c_reserva", usb, (.55, .55, .58), "corpo aproximado"),
    ("p2_reserva", audio, (.52, .52, .56), "corpo aproximado"),
    ("micro_sd_reserva", sd, (.52, .52, .56), "corpo aproximado"),
    ("ffc_ui_principal", ffc, (.9, .68, .2), "rota proposta; 16 vias, pitch nao liberado"),
    ("ffc_conector_principal", ffc_main_socket, (.8, .68, .4), "reserva"),
    ("ffc_conector_ui", ffc_ui_socket, (.8, .68, .4), "reserva"),
    ("bateria_cabo_positivo", battery_red, (.8, .05, .04), "rota proposta"),
    ("bateria_cabo_negativo", battery_black, (.05, .05, .06), "rota proposta"),
    ("switches_9_reserva", switches, (.28, .28, .31), "envelopes, sem STEP do fabricante"),
    ("keycaps_9_reserva", keycaps, (.13, .14, .16), "caps customizados a dimensionar"),
    ("biometria_reserva", bio, (.12, .16, .19), "sensor seguro nao selecionado"),
    ("fader_comando_reserva", fader, (.25, .27, .28), "haste/curso a validar"),
    ("mute_comando_reserva", mute, (.3, .32, .34), "haste/DPDT a validar"),
    ("botao_camada", layer_button, (.2, .22, .24), "interface tatil a validar"),
    ("botao_gravacao", record_button, (.7, .08, .06), "interface tatil a validar"),
]
assembly = cq.Assembly(name="CorePad_Beta_integrado_v0.1.0")
manifest = []
for name, part, color, note in items:
    obj = part.val() if isinstance(part, cq.Workplane) else part
    cq.exporters.export(obj, str(PARTS / f"{name}.step"))
    cq.exporters.export(obj, str(PARTS / f"{name}.stl"), tolerance=.06, angularTolerance=.1)
    assembly.add(obj, name=name, color=cq.Color(*color))
    bb = obj.BoundingBox()
    manifest.append({"name": name, "bbox_mm": [round(v, 3) for v in
        (bb.xmin, bb.ymin, bb.zmin, bb.xmax, bb.ymax, bb.zmax)], "status": note})
assembly.export(str(ROOT / "CorePad_Beta_integrado_v0.1.0.step"))
(ROOT / "assembly_manifest.json").write_text(json.dumps({
    "units": "mm", "origin": "centro do corpo, plano inferior Z=0",
    "envelope_mm": [104, 84, 28.4], "items": manifest}, indent=2, ensure_ascii=False) + "\n")
print(f"Exported {len(items)} solids, assembly STEP and manifest")
