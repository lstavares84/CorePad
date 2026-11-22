"""KiCad 9 PCB placement revision: supplier land patterns, nets and fixed datums.

Main board is a component placement/partition study, not a completed circuit.
UI switch footprint follows the Kailh drawing as a *pilot* until sample checked.
"""
from pathlib import Path
import json
import pcbnew as p

ROOT = Path(__file__).resolve().parent
LIB = Path("/usr/share/kicad/footprints")
CASE_DATUM = (99, 89)  # KiCad mm; world X=x-99, world Y=89-y.
SIGNALS = [f"KEY{i}" for i in range(1, 10)] + [
    "LAYER", "RECORD", "MUTE_SENSE", "FADER_ADC", "3V3_UI", "GND", "GND",
    "MUTE_HW_EN", "BIO_UART_TX", "BIO_UART_RX", "BIO_RESET",
    "LED_LAYER_1", "LED_LAYER_2", "LED_LAYER_3", "LED_RECORD"]
FFC_PINS = {str(i + 1): signal for i, signal in enumerate(SIGNALS)}


def pos(x, y):
    return p.VECTOR2I(p.FromMM(x + CASE_DATUM[0]), p.FromMM(CASE_DATUM[1] - y))


def segment(board, a, b, layer=p.Dwgs_User, width=.12):
    item = p.PCB_SHAPE()
    item.SetShape(p.SHAPE_T_SEGMENT)
    item.SetStart(pos(*a)); item.SetEnd(pos(*b))
    item.SetLayer(layer); item.SetWidth(p.FromMM(width))
    board.Add(item)


def rectangle(board, x, y, w, h, layer=p.Dwgs_User):
    corners = [(x-w/2,y-h/2),(x+w/2,y-h/2),(x+w/2,y+h/2),(x-w/2,y+h/2)]
    for first, second in zip(corners, corners[1:] + corners[:1]):
        segment(board, first, second, layer)


def label(board, x, y, value, size=1):
    item = p.PCB_TEXT(board)
    item.SetText(value)
    item.SetPosition(pos(x, y))
    item.SetTextSize(p.VECTOR2I(p.FromMM(size), p.FromMM(size)))
    item.SetLayer(p.Dwgs_User)
    board.Add(item)


def new_board(layers):
    board = p.BOARD()
    board.SetCopperLayerCount(layers)
    board.GetDesignSettings().SetBoardThickness(p.FromMM(1.6))
    rectangle(board, 0, 0, 98, 78, p.Edge_Cuts)
    return board


def net(board, name):
    item = p.NETINFO_ITEM(board, name)
    board.Add(item)
    return item


def fp(board, library, name, ref, value, x, y, angle=0, underside=False):
    folder = ROOT / "CorePad.pretty" if library == "CorePad" else LIB / (library + ".pretty")
    item = p.FootprintLoad(str(folder), name)
    if item is None:
        raise RuntimeError(f"Footprint missing: {library}:{name}")
    item.SetReference(ref); item.SetValue(value)
    item.SetPosition(pos(x, y))
    item.SetOrientationDegrees(angle)
    board.Add(item)
    if underside:
        item.Flip(item.GetPosition(), False)
    return item


def assign(item, mapping, nets):
    for pad in item.Pads():
        name = mapping.get(pad.GetNumber())
        if name and name in nets:
            pad.SetNet(nets[name])


# UI product board: a real FFC land pattern and nine pilot Choc V2 patterns.
ui = new_board(2)
ui_nets = {name: net(ui, name) for name in sorted(set(SIGNALS))}
keys = []
for number, (x, y) in enumerate(((x,y) for y in (20.5,0,-20.5) for x in (-33,-13,7)), 1):
    item = fp(ui, "CorePad", "SW_Kailh_Choc_V2_CPG135301D01_Pilot", f"SW{number}",
              "CPG135301D01 PILOT", x, y)
    assign(item, {"1": f"KEY{number}", "2": "GND"}, ui_nets)
    keys.append({"ref": f"SW{number}", "center_mm": [x, y],
                 "terminal1_mm": [x+3.8,y+5], "terminal2_mm": [x+5.9,y],
                 "body_mm": [15,15], "body_above_pcb_mm": 6.4,
                 "terminal_below_pcb_mm": 2.2})
ffc_name = "Amphenol_F32R-1A7x1-11024_1x24-1MP_P0.5mm_Horizontal"
ui_conn = fp(ui, "Connector_FFC-FPC", ffc_name, "J_UI", "F32R-1A7H1-11024 CANDIDATE",
             -30, 33.5, angle=180, underside=True)
assign(ui_conn, FFC_PINS, ui_nets)
for name,x,y,w,h in [("BIO MODULE UNSPECIFIED",35.5,-26.5,21.3,21.3),
                      ("FADER PTA1543 BODY",35.5,2,8.5,30),
                      ("MUTE DPDT TO RESOLVE",35.5,29,8,8)]:
    rectangle(ui,x,y,w,h);label(ui,x,y,name,.7)
label(ui,0,-36,"UI 0.3.0 / SWITCH+FFC PILOT / AUX COMPONENTS UNPLACED",.85)
p.SaveBoard(str(ROOT / "CorePad_UI_v0.3.0.kicad_pcb"), ui)

# Main board: stock KiCad land patterns of selected candidate packages and ports.
main = new_board(4)
main_net_names = sorted(set(SIGNALS) | {"VBUS", "USB_D+", "USB_D-", "CC1", "CC2",
                                        "SD_VDD", "SD_CLK", "SD_CMD", "SD_D0", "SD_D1",
                                        "SD_D2", "SD_D3", "AUDIO_L", "AUDIO_R"})
main_nets = {name: net(main, name) for name in main_net_names}
main_conn = fp(main,"Connector_FFC-FPC",ffc_name,"J_UI","F32R-1A7H1-11024 CANDIDATE",-30,33.5)
assign(main_conn, FFC_PINS, main_nets)
usb = fp(main,"Connector_USB","USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal",
         "J_USB","USB4105-GF-A CANDIDATE",0,36.5,180)
usb_nets = {"A1":"GND","A12":"GND","B1":"GND","B12":"GND",
            "A4":"VBUS","A9":"VBUS","B4":"VBUS","B9":"VBUS",
            "A5":"CC1","B5":"CC2","A6":"USB_D+","B6":"USB_D+",
            "A7":"USB_D-","B7":"USB_D-"}
assign(usb,usb_nets,main_nets)
sd = fp(main,"Connector_Card","microSD_HC_Hirose_DM3AT-SF-PEJM5",
        "J_SD","DM3AT-SF-PEJM5 CANDIDATE",-43,14,90)
assign(sd,{"1":"SD_D2","2":"SD_D3","3":"SD_CMD","4":"SD_VDD",
           "5":"SD_CLK","6":"GND","7":"SD_D0","8":"SD_D1"},main_nets)
audio = fp(main,"Connector_Audio","Jack_3.5mm_CUI_SJ-3523-SMT_Horizontal",
           "J_P2","SJ-3523-SMT-TR CANDIDATE",-43,-18,90)
assign(audio,{"T":"AUDIO_L","R":"AUDIO_R","S":"GND"},main_nets)
fp(main,"Package_QFP","LQFP-144_20x20mm_P0.5mm","U1","STM32U5A5ZJT6Q",0,0)
fp(main,"Package_DFN_QFN","VQFN-24-1EP_4x4mm_P0.5mm_EP2.45x2.45mm",
   "U2","TAC5112IRGER LAND PATTERN TO CHECK",-22,-18)
fp(main,"Package_DFN_QFN","Texas_RTE_WQFN-16-1EP_3x3mm_P0.5mm_EP1.2x0.8mm",
   "U3","TPA6132A2RTER LAND PATTERN TO CHECK",-30,-29)
for name,x,y,w,h in [("CHARGER/POWER RESERVE",18,27,14,12),
                      ("SECURE ELEMENT RESERVE",22,-24,12,10),
                      ("RGB DRIVER RESERVE",-18,27,10,9),
                      ("MICROPHONES/DUCTS RESERVE",34,28,12,9)]:
    rectangle(main,x,y,w,h);label(main,x,y,name,.7)
label(main,0,-36,"MAIN 0.3.0 / PLACEMENT+PORT NETS / NO MCU PINMAP",.9)
p.SaveBoard(str(ROOT / "CorePad_Main_v0.3.0.kicad_pcb"), main)

(ROOT / "interconnect_24.json").write_text(json.dumps({
    "candidate_mpn": "F32R-1A7H1-11024", "pitch_mm": .5,
    "board_connector_centres_mm": {"main": [-30,33.5], "ui": [-30,33.5]},
    "pins": FFC_PINS,
    "note": "Electrical allocation only. Physical mute signal is a proposed direct hardware enable, not a verified circuit. RGB stays on the main/base. Cable orientation, supply current and bend unvalidated."
},indent=2)+"\n")
(ROOT / "switch_placement.json").write_text(json.dumps(keys,indent=2)+"\n")
for name in ("CorePad_Main_v0.3.0","CorePad_UI_v0.3.0"):
    (ROOT/(name+".kicad_pro")).write_text(json.dumps({"meta":{"version":1,"filename":name+".kicad_pro"}},indent=2))
print("Generated 2 boards: main candidate placement and UI Choc V2 pilot + 24-pin FFC")
