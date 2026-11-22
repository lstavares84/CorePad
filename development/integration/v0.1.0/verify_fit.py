"""Check solid intersections and nominal vertical clearances of the current fit study."""
from pathlib import Path
import json
import cadquery as cq

ROOT = Path(__file__).resolve().parent


def load(name):
    return cq.importers.importStep(str(ROOT / "parts" / f"{name}.step"))


names = ("base_plastica", "tampa_carbono", "difusor_rgb_base",
         "pcb_principal_kicad", "pcb_ui_reserva", "bateria_reserva",
         "usb_c_reserva", "p2_reserva", "micro_sd_reserva")
parts = {n: load(n) for n in names}
pairs = (("base_plastica", "tampa_carbono"),
         ("base_plastica", "difusor_rgb_base"),
         ("base_plastica", "pcb_principal_kicad"),
         ("base_plastica", "pcb_ui_reserva"),
         ("base_plastica", "bateria_reserva"),
         ("pcb_principal_kicad", "pcb_ui_reserva"),
         ("pcb_principal_kicad", "bateria_reserva"),
         ("base_plastica", "usb_c_reserva"),
         ("base_plastica", "p2_reserva"),
         ("base_plastica", "micro_sd_reserva"))
overlaps = []
for first, second in pairs:
    intersection = parts[first].intersect(parts[second])
    volume = intersection.val().Volume() if intersection.val() else 0
    overlaps.append({"a": first, "b": second, "overlap_mm3": round(volume, 4)})
stack = {"battery_to_main_mm": 2.6, "main_to_ui_mm": 6.2,
         "ui_to_lid_mm": 4.0, "battery_bottom_from_floor_mm": 1.0}
data = {"basis": "CAD STEP 0.1.0; only the listed solid pairs were checked",
        "overlaps": overlaps, "nominal_clearances": stack,
        "unverified": ["component heights", "switch travel", "battery swelling",
                       "FFC bend radius", "fastener placement", "supplier tolerances"]}
(ROOT / "fit_report.json").write_text(json.dumps(data, indent=2) + "\n")
for row in overlaps:
    print(row)
print(stack)
