"""KiCad 9: electrical interface harness prototype and main-board layout draft.
Run with /usr/bin/python3. Footprints are connector harnesses, not Choc substitutes.
"""
from pathlib import Path
import json
from uuid import uuid5,NAMESPACE_URL
import pcbnew as p
ROOT=Path(__file__).resolve().parent
LIB=Path('/usr/share/kicad/footprints')
def xy(x,y):return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
def outline(board):
    for a,b in [((50,50),(148,50)),((148,50),(148,128)),((148,128),(50,128)),((50,128),(50,50))]:
        item=p.PCB_SHAPE();item.SetShape(p.SHAPE_T_SEGMENT);item.SetStart(xy(*a));item.SetEnd(xy(*b));item.SetLayer(p.Edge_Cuts);item.SetWidth(p.FromMM(.05));board.Add(item)
def label(board,text,x,y):
    item=p.PCB_TEXT(board);item.SetText(text);item.SetPosition(xy(x,y));item.SetTextSize(xy(1,1));item.SetLayer(p.Dwgs_User);board.Add(item)
def footprint(board,library,name,ref,value,x,y):
    item=p.FootprintLoad(str(LIB/(library+'.pretty')),name)
    if item is None:raise RuntimeError(name)
    item.SetReference(ref);item.SetValue(value);item.SetPosition(xy(x,y));board.Add(item);return item
def newnet(board,name):
    item=p.NETINFO_ITEM(board,name);board.Add(item);return item

board=p.BOARD();board.SetCopperLayerCount(2);board.GetDesignSettings().SetBoardThickness(p.FromMM(1.6));outline(board)
nets={name:newnet(board,name) for name in ['GND']+[f'KEY{i}' for i in range(1,10)]+['LAYER','RECORD','MUTE_SENSE','FADER','3V3']}
pins={}
for i in range(1,10):
    x=66+20*((i-1)%3);y=68+20*((i-1)//3)
    fp=footprint(board,'Connector_PinHeader_2.54mm','PinHeader_1x02_P2.54mm_Vertical',f'J{i}',f'External key {i}',x,y)
    for pad in fp.Pads():pad.SetNet(nets[f'KEY{i}' if pad.GetNumber()=='1' else 'GND'])
    pins[f'J{i}']={'1':f'KEY{i}','2':'GND'}
aux=['LAYER','RECORD','MUTE_SENSE','FADER','3V3']
for i,name in enumerate(aux,10):
    fp=footprint(board,'Connector_PinHeader_2.54mm','PinHeader_1x02_P2.54mm_Vertical',f'J{i}',name,132,59+(i-10)*10)
    for pad in fp.Pads():pad.SetNet(nets[name if pad.GetNumber()=='1' else 'GND'])
    pins[f'J{i}']={'1':name,'2':'GND'}
fp=footprint(board,'Connector_PinHeader_2.54mm','PinHeader_2x08_P2.54mm_Vertical','J20','Interface 3V3',115,99)
signals=[f'KEY{i}' for i in range(1,10)]+aux+['GND','GND']
for pad in fp.Pads():pad.SetNet(nets[signals[int(pad.GetNumber())-1]])
pins['J20']={str(i+1):name for i,name in enumerate(signals)}
label(board,'COREPAD BETA 0.2.0 - INTERFACE DE BANCADA',99,44)
label(board,'Conectores para controles externos / sem roteamento',99,134)
p.SaveBoard(str(ROOT/'CorePad_Interface_Bancada_v0.2.0.kicad_pcb'),board)

# Native schematic with embedded passive connector symbols and matching labels.
def uid(key):return str(uuid5(NAMESPACE_URL,'corepad-beta-interface-020/'+key))
def effects():return '(effects (font (size 1.0 1.0)))'
symbols={}
for n in (2,16):
    symbol=f'(symbol "CorePad:Header{n}" (pin_names (offset 0.5)) (in_bom yes) (on_board yes) '
    symbol+=f'(property "Reference" "J" (at 0 2.54 0) {effects()}) (property "Value" "Header{n}" (at 0 5.08 0) {effects()}) '
    symbol+=f'(symbol "Header{n}_1_1" '
    for pin in range(1,n+1):
        symbol+=f'(pin passive line (at -5.08 {-2.54*(pin-1)} 0) (length 2.54) (name "Pin_{pin}" {effects()}) (number "{pin}" {effects()})) '
    symbol+='))';symbols[n]=symbol
root_id=uid('root')
lines=[f'(kicad_sch (version 20250114) (generator "eeschema") (uuid "{root_id}") (paper "A4")',
       '(lib_symbols '+' '.join(symbols.values())+')']
for idx,(ref,mapping) in enumerate(pins.items()):
    n=len(mapping);x=35.56+(idx%4)*63.5;y=30.48+(idx//4)*38.1
    fpname='PinHeader_1x02_P2.54mm_Vertical' if n==2 else 'PinHeader_2x08_P2.54mm_Vertical'
    lines += [f'(symbol (lib_id "CorePad:Header{n}") (at {x} {y} 0) (unit 1) (in_bom yes) (on_board yes) (dnp no) (uuid "{uid(ref)}")',
              f'(property "Reference" "{ref}" (at {x} {y-5} 0) {effects()})',
              f'(property "Value" "Interface_{ref}" (at {x+3} {y-2} 0) {effects()})',
              f'(property "Footprint" "Connector_PinHeader_2.54mm:{fpname}" (at {x} {y} 0) (effects (font (size 1 1)) (hide yes)))',
              f'(instances (project "CorePad_Interface_Bancada_v0.2.0" (path "/{root_id}" (reference "{ref}") (unit 1)))))']
    for number,name in mapping.items():
        py=y+2.54*(int(number)-1)
        lines += [f'(label "{name}" (at {x-5.08} {py} 0) (effects (font (size 1 1)) (justify left bottom)) (uuid "{uid(ref+number)}"))']
lines += [')']
(ROOT/'CorePad_Interface_Bancada_v0.2.0.kicad_sch').write_text('\n'.join(lines)+'\n')
library='(kicad_symbol_lib (version 20241209) (generator "kicad_symbol_editor") '+' '.join(s.replace('CorePad:','') for s in symbols.values())+')'
(ROOT/'CorePad.kicad_sym').write_text(library)
(ROOT/'sym-lib-table').write_text('(sym_lib_table (lib (name "CorePad") (type "KiCad") (uri "${KIPRJMOD}/CorePad.kicad_sym") (options "") (descr "CorePad passive harness symbols")))')
(ROOT/'interface_pins.json').write_text(json.dumps(pins,indent=2)+'\n')

main=p.BOARD();main.SetCopperLayerCount(4);main.GetDesignSettings().SetBoardThickness(p.FromMM(1.6));outline(main)
footprint(main,'Package_QFP','LQFP-144_20x20mm_P0.5mm','U1','STM32U5A5ZJT6Q',122,90)
label(main,'COREPAD BETA - PRINCIPAL 0.2.0 - EM ENGENHARIA',99,44)
label(main,'MCU sem redes / audio, energia e seguranca pendentes',99,134)
p.SaveBoard(str(ROOT/'CorePad_Principal_v0.2.0.kicad_pcb'),main)
(ROOT/'CorePad_Interface_Bancada_v0.2.0.kicad_pro').write_text(json.dumps({'meta':{'version':1,'filename':'CorePad_Interface_Bancada_v0.2.0.kicad_pro'}},indent=2))
print('Generated KiCad boards, interface schematic and pin manifest')
