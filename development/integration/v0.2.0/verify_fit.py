"""Reproducible nominal clearance checks against the mechanical v0.1.0 case."""
from pathlib import Path
import json
import cadquery as cq

ROOT=Path(__file__).resolve().parent
OLD=ROOT.parent/'v0.1.0'/'parts'
def step(path): return cq.importers.importStep(str(path)).val()
def box(x,y,z,dx,dy,dz): return cq.Workplane('XY').box(dx,dy,dz).translate((x,y,z)).val()
base,lid,battery=(step(OLD/(name+'.step')) for name in ('base_plastica','tampa_carbono','bateria_reserva'))
main=step(ROOT/'pcb_main_v0.3.0.step').translate((0,0,12.6))
ui=step(ROOT/'pcb_ui_v0.3.0.step').translate((0,0,20.4))
main_top=main.BoundingBox().zmax
ui_top=ui.BoundingBox().zmax
components={
 'microSD_DM3AT':box(-43,14,main_top+.84,15.95,13.85,1.68),
 'P2_SJ3523':box(-44.5,-18,main_top+2.5,9,11,5),
 'USB_C_USB4105':box(0,38.2,main_top+1.6,9,6,3.2),
 'FFC24_main':box(-30,33.5,main_top+1,20.35,6.75,2),
 'FFC24_ui':box(-30,33.5,19.4,20.35,6.75,2),
 'MCU_LQFP144':box(0,0,main_top+.7,20,20,1.4),
}
report={
 'units':'mm',
 'board_to_case_intersection_mm3':{name:{'base':round(board.intersect(base).Volume(),3),'lid':round(board.intersect(lid).Volume(),3),'battery':round(board.intersect(battery).Volume(),3)} for name,board in [('main',main),('ui',ui)]},
 'component_to_case_intersection_mm3':{name:{'base':round(body.intersect(base).Volume(),3),'lid':round(body.intersect(lid).Volume(),3)} for name,body in components.items()},
 'z_stack_mm':{'battery_top':10,'main_bottom':12.6,'main_top':round(main_top,2),'ui_bottom':20.4,'ui_top':round(ui_top,2),'lid_bottom':26,'lid_top':28.4,'main_to_ui_clearance':round(20.4-main_top,2),'FFC_body_to_body_gap':round(18.4-(main_top+2),2),'switch_body_top':round(ui_top+6.4,2),'switch_body_top_below_lid_top':round(28.4-(ui_top+6.4),2)},
 'port_alignment_mm':{'P2_jack_center_z':round(main_top+2.5,2),'P2_case_aperture_center_z':14.2,'P2_offset_up':round(main_top+2.5-14.2,2),'microSD_body_top':round(main_top+1.68,2),'microSD_aperture_top':15.7},
 'critical_non_geometric':[
  'Both PCBs lack mounting holes/standoffs at their nominal Z planes; base corner bosses stop at Z=7.',
  'FFC bend and insertion orientation have no manufacturer cable model or bend-radius verification.',
  'Keycap/actuator dimensions and biometric module are not supplier controlled.',
  'P2 aperture center differs from actual candidate jack center; body-box no-overlap alone does not validate plug access.',
  'USB and microSD candidate body boxes intersect the previous base and require case/placement revision.'
 ]}
(ROOT/'fit_report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(report['component_to_case_intersection_mm3'],indent=2))
