"""Compare exported schematic connectivity against every PCB pad and pin manifest."""
from pathlib import Path
import json
import xml.etree.ElementTree as ET
import pcbnew
root=Path(__file__).resolve().parent
expected=json.loads((root/'interface_pins.json').read_text())
schematic={}
for net in ET.parse(root/'reports/interface.net').getroot().find('nets'):
    for node in net.findall('node'):
        schematic[(node.attrib['ref'],node.attrib['pin'])]=net.attrib['name'].lstrip('/')
board=pcbnew.LoadBoard(str(root/'CorePad_Interface_Bancada_v0.2.0.kicad_pcb'))
actual={(fp.GetReference(),pad.GetNumber()):pad.GetNetname() for fp in board.GetFootprints() for pad in fp.Pads()}
wanted={(ref,pin):name for ref,mapping in expected.items() for pin,name in mapping.items()}
assert schematic==wanted,(schematic,wanted)
assert actual==wanted,(actual,wanted)
print(f'PASS: {len(wanted)} pads and schematic pins match the interface contract')
