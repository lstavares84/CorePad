"""CorePad placement-level integrated STEP, using the revised KiCad board solids.

All component bodies and cables here are bounding envelopes, not vendor STEP models.
"""
from pathlib import Path
import json
import cadquery as cq

ROOT = Path(__file__).resolve().parent
OLD = ROOT.parent / 'v0.1.0' / 'parts'
OUT = ROOT / 'CorePad_Beta_PCB_match_v0.2.0.step'
PARTS = ROOT / 'render_meshes'
PARTS.mkdir(exist_ok=True)


def part(name):
    return cq.importers.importStep(str(OLD / (name+'.step'))).val()


def box(x,y,z,dx,dy,dz):
    return cq.Workplane('XY').box(dx,dy,dz).translate((x,y,z)).val()


def cable(points, radius):
    pieces=[]
    for a,b in zip(points,points[1:]):
        start,end=cq.Vector(*a),cq.Vector(*b)
        d=end.sub(start)
        pieces.append(cq.Solid.makeCylinder(radius,d.Length,start,d.normalized()))
    return cq.Compound.makeCompound(pieces)


assembly=cq.Assembly(name='CorePad_Beta_PCB_match_v0.2.0')
manifest=[]

def add(name, solid, color, status):
    assembly.add(solid,name=name,color=cq.Color(*color))
    cq.exporters.export(solid,str(PARTS/(name+'.stl')),tolerance=.06,angularTolerance=.1)
    b=solid.BoundingBox()
    manifest.append({'name':name,'bounds_mm':[round(v,3) for v in (b.xmin,b.ymin,b.zmin,b.xmax,b.ymax,b.zmax)],'status':status})


add('base_plastica',part('base_plastica'),(.08,.09,.1),'from mechanical v0.1.0; ports not recut')
add('tampa_carbono',part('tampa_carbono'),(.13,.14,.15),'from mechanical v0.1.0; openings not recut')
add('difusor_rgb_base',part('difusor_rgb_base'),(.2,.85,.25),'previous envelope')
add('pcb_main_v0_3',cq.importers.importStep(str(ROOT/'pcb_main_v0.3.0.step')).val().translate((0,0,12.6)),(.08,.31,.22),'KiCad board solid; placement-only circuit')
add('pcb_ui_v0_3',cq.importers.importStep(str(ROOT/'pcb_ui_v0.3.0.step')).val().translate((0,0,20.4)),(.1,.34,.27),'KiCad board solid; six key nets routed')
add('battery',part('bateria_reserva'),(.35,.36,.39),'60x36x7 mm reserved cell')
add('battery_positive',part('bateria_cabo_positivo'),(.8,.1,.05),'old wire envelope; connector unspecified')
add('battery_negative',part('bateria_cabo_negativo'),(.1,.1,.1),'old wire envelope; connector unspecified')
main_top=12.6+1.51
ui_top=20.4+1.51
for n,(x,y) in enumerate(((x,y) for y in (20.5,0,-20.5) for x in (-33,-13,7)),1):
    add(f'SW{n}_Kailh_body',box(x,y,ui_top+3.2,15,15,6.4),(.26,.27,.29),'Kailh Choc V2 package envelope; no cap/actuator STEP')
for name,color in [('keycaps_9_reserva',(.13,.14,.16)),
                   ('biometria_reserva',(.12,.16,.19)),
                   ('fader_comando_reserva',(.25,.27,.28)),
                   ('mute_comando_reserva',(.3,.32,.34)),
                   ('botao_camada',(.2,.22,.24)),
                   ('botao_gravacao',(.7,.08,.06))]:
    add(name,part(name),color,'mechanical v0.1.0 reserve; catalog fit unvalidated')
# Selected candidate outer bodies, roughly located from their PCB footprints.
add('MCU_LQFP144',box(0,0,main_top+.7,20,20,1.4),(.14,.14,.16),'package 20x20x1.4; pins unassigned')
add('audio_codec_VQFN24',box(-22,-18,main_top+.5,4,4,1),(.15,.15,.17),'package envelope; pad pattern to verify')
add('headphone_amp_WQFN16',box(-30,-29,main_top+.4,3,3,.8),(.15,.15,.17),'package envelope; pad pattern to verify')
add('microSD_DM3AT',box(-43,14,main_top+.84,15.95,13.85,1.68),(.62,.62,.64),'supplier dimensions; orientation/nose must be reviewed')
add('P2_SJ3523',box(-44.5,-18,main_top+2.5,9,11,5),(.6,.6,.63),'supplier body envelope; centre is 2.41 mm high vs case opening')
add('USB_C_USB4105',box(0,38.2,main_top+1.6,9,6,3.2),(.58,.58,.61),'candidate body envelope; vendor 3D not checked')
add('FFC24_main_socket',box(-30,33.5,main_top+1,20.35,6.75,2),(.7,.6,.45),'Amphenol F32R 24way candidate courtyard envelope')
add('FFC24_ui_socket',box(-30,33.5,19.4,20.35,6.75,2),(.7,.6,.45),'same candidate, underside; orientation under review')
# This is a cable *space claim*, not an electrically validated bend path.
add('FFC24_cable_envelope',box(-30,33.5,17.25,12.5,5.8,2.3),(.9,.65,.2),'24-conductor 0.5mm-pitch cable bend reservation only')
assembly.export(str(OUT))
(ROOT/'assembly_manifest.json').write_text(json.dumps({'units':'mm','origin':'case centre at bottom','main_board_z':[12.6,main_top], 'ui_board_z':[20.4,ui_top],'items':manifest},indent=2)+'\n')
print('Exported',len(manifest),'groups:',OUT)
