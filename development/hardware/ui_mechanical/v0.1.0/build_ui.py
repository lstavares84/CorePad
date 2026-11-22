"""KiCad 9 mechanical placement board. No electrical footprints or nets yet."""
from pathlib import Path
import json
import pcbnew as p

ROOT = Path(__file__).resolve().parent
NAME = "CorePad_UI_Posicionamento_v0.1.0"
board = p.BOARD()
board.SetCopperLayerCount(2)
board.GetDesignSettings().SetBoardThickness(p.FromMM(1.6))


def point(x, y):
    # Same KiCad coordinates as main PCB, world X=x-99, world Y=89-y.
    return p.VECTOR2I(p.FromMM(x + 99), p.FromMM(89 - y))


def segment(a, b, layer=p.Dwgs_User, width=.12):
    shape = p.PCB_SHAPE()
    shape.SetShape(p.SHAPE_T_SEGMENT)
    shape.SetStart(point(*a))
    shape.SetEnd(point(*b))
    shape.SetLayer(layer)
    shape.SetWidth(p.FromMM(width))
    board.Add(shape)


def box(x, y, w, h, layer=p.Dwgs_User):
    corners = ((x-w/2,y-h/2),(x+w/2,y-h/2),(x+w/2,y+h/2),(x-w/2,y+h/2))
    for a,b in zip(corners,corners[1:]+corners[:1]):
        segment(a,b,layer)


def cross(x, y, size=1.5):
    segment((x-size,y),(x+size,y))
    segment((x,y-size),(x,y+size))


def label(x, y, value):
    item = p.PCB_TEXT(board)
    item.SetText(value)
    item.SetPosition(point(x,y))
    item.SetLayer(p.Dwgs_User)
    item.SetTextSize(p.VECTOR2I(p.FromMM(1),p.FromMM(1)))
    board.Add(item)


box(0,0,98,78,p.Edge_Cuts)
positions=[]
for i,(x,y) in enumerate(((x,y) for y in (20.5,0,-20.5) for x in (-33,-13,7)),1):
    box(x,y,19.6,19.6)
    cross(x,y)
    label(x+6.7,y+6.7,f"SW{i}")
    positions.append({"ref":f"SW{i}","center_mm":[x,y],"opening_mm":[19.6,19.6]})
for ref,x,y in (("BIO",35.5,-26.5),("FADER",35.5,2),("MUTE",35.5,29),
                ("LAYER",-13,34.4),("REC",8.5,34.4)):
    cross(x,y)
    label(x-2,y-4,ref)
label(-28,37,"NO PADS / NO ROUTING / MECHANICAL ONLY")
p.SaveBoard(str(ROOT/(NAME+".kicad_pcb")),board)
(ROOT/(NAME+".kicad_pro")).write_text(json.dumps({"meta":{"version":1,"filename":NAME+".kicad_pro"}},indent=2))
(ROOT/"placement.json").write_text(json.dumps({"datum":"X/Y at case centre, Y positive rear",
    "board_mm":[98,78,1.6],"switches":positions,
    "controls":{"biometric":[35.5,-26.5],"fader":[35.5,2],
                "mute":[35.5,29],"layer":[-13,34.4],"record":[8.5,34.4]}},indent=2)+"\n")
print("Generated mechanical UI KiCad board and placement manifest")
