"""Preliminary dimensioned SVG views, derived from the assembly master dimensions."""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parent


def svg(body, title, width=1100, height=690):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<style>text{{font-family:DejaVu Sans,Arial,sans-serif;fill:#e8edf2}} .small{{font-size:13px}} .label{{font-size:16px}} .dim{{font-size:14px;fill:#63dcd0}} .line{{stroke:#c7d3dd;stroke-width:2;fill:none}} .guide{{stroke:#65939c;stroke-width:1;fill:none}} .reserve{{stroke:#ffa94d;stroke-width:2;stroke-dasharray:7 5;fill:none}} .body{{fill:#202a32;stroke:#d5e3ed;stroke-width:2}} .board{{fill:#126750;stroke:#55dabb;stroke-width:2}} .battery{{fill:#53606a;stroke:#ffa94d;stroke-width:2;stroke-dasharray:6 4}}</style>
<rect width="100%" height="100%" fill="#101920"/><text x="36" y="44" font-size="25" font-weight="bold" fill="white">{escape(title)}</text>
<text x="37" y="69" class="small">CorePad Beta Carbon · engenharia v0.1.0 · mm · estudo dimensional, NÃO liberado para manufatura</text>
<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto-start-reverse"><path d="M0 0 L8 4 L0 8 Z" fill="#63dcd0"/></marker></defs>
{body}<line x1="36" y1="646" x2="1064" y2="646" class="guide"/><text x="36" y="670" class="small">DATUM: X/Y no centro do corpo; Z=0 na face inferior. Medidas nominais; tolerâncias e GD&amp;T pendentes.</text></svg>'''


def text(x, y, label, cls="label"):
    return f'<text x="{x}" y="{y}" class="{cls}">{escape(label)}</text>'


def line(x1, y1, x2, y2, cls="line"):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="{cls}"/>'


def dim(x1, y1, x2, y2, label):
    mx, my = (x1+x2)/2, (y1+y2)/2
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#63dcd0" marker-start="url(#arrow)" marker-end="url(#arrow)"/>'+text(mx-25,my-8,label,"dim")


# Top view: 4 px/mm.
s = 4
cx, cy = 260, 318
px = lambda x: cx + s*x
py = lambda y: cy - s*y
top = [f'<rect x="{px(-52)}" y="{py(42)}" width="416" height="336" rx="8" class="body"/>',
       f'<rect x="{px(-49)}" y="{py(39)}" width="392" height="312" class="reserve"/>',
       f'<rect x="{px(-48)}" y="{py(10)}" width="240" height="144" class="battery"/>']
for y in (20.5,0,-20.5):
    for x in (-33,-13,7):
        top.append(f'<rect x="{px(x-9.8)}" y="{py(y+9.8)}" width="78.4" height="78.4" rx="4" class="line"/>')
for x,y,r in ((35.5,-26.5,10.65),(35.5,29,3.3),(8.5,34.4,2.3)):
    top.append(f'<circle cx="{px(x)}" cy="{py(y)}" r="{s*r}" class="line"/>')
top += [f'<rect x="{px(31.75)}" y="{py(15.25)}" width="30" height="106" rx="3" class="line"/>',
        line(px(-52),py(-42)+35,px(-52),py(-42)+58,"guide"),
        line(px(52),py(-42)+35,px(52),py(-42)+58,"guide"),
        dim(px(-52),py(-42)+47,px(52),py(-42)+47,"104"),
        line(px(52)+34,py(42),px(52)+52,py(42),"guide"),
        line(px(52)+34,py(-42),px(52)+52,py(-42),"guide"),
        dim(px(52)+43,py(42),px(52)+43,py(-42),"84"),
        line(px(-33),py(20.5),px(7),py(20.5),"guide"),
        text(548,175,"9 teclas, centros X = -33 / -13 / 7 mm"),
        text(548,203,"Centros Y = +20,5 / 0 / -20,5 mm"),
        text(548,254,"Abertura de tecla 19,6 × 19,6 mm"),
        text(548,282,"Biometria Ø21,3 em (+35,5; -26,5)"),
        text(548,328,"Placas: 98 × 78 mm, contorno laranja"),
        text(548,356,"Bateria provisória: 60 × 36 × 7 mm"),
        text(548,406,"USB-C: traseira, X=0 · microSD: esquerda Y=+14"),
        text(548,434,"P2: esquerda Y=-18 · RGB somente na base"),
        text(548,492,"Laranja tracejado = envelope a confirmar com peça real","dim")]
(ROOT/"desenho_planta.svg").write_text(svg("\n".join(top),"Planta técnica preliminar"))

# Longitudinal side section: x axis horizontal, Z vertical. 5 px/mm.
S=4; ox, floor=300, 525
X=lambda x:ox+S*x
Z=lambda z:floor-S*z
side=[f'<rect x="{X(-52)}" y="{Z(26)}" width="{S*104}" height="{S*26}" class="body"/>',
      f'<rect x="{X(-50)}" y="{Z(26)}" width="{S*100}" height="{S*24}" fill="#101920"/>',
      f'<rect x="{X(-52)}" y="{Z(2)}" width="{S*104}" height="{S*2}" fill="#202a32"/>',
      f'<rect x="{X(-52)}" y="{Z(28.4)}" width="{S*104}" height="{S*2.4}" class="body"/>',
      f'<rect x="{X(-49)}" y="{Z(14.2)}" width="{S*98}" height="{S*1.6}" class="board"/>',
      f'<rect x="{X(-49)}" y="{Z(22)}" width="{S*98}" height="{S*1.6}" class="board"/>',
      f'<rect x="{X(-48)}" y="{Z(10)}" width="{S*60}" height="{S*7}" class="battery"/>',
      f'<rect x="{X(21)}" y="{Z(20.4)}" width="{S*8}" height="{S*6.1}" fill="#d89d39"/>',
      line(X(-52)-50,Z(0),X(-52)-20,Z(0),"guide"),
      line(X(-52)-50,Z(28.4),X(-52)-20,Z(28.4),"guide"),
      dim(X(-52)-35,Z(0),X(-52)-35,Z(28.4),"28,4"),
      text(56,572,"Z0 face inferior"),text(58,278,"Z28,4 topo da tampa"),
      text(640,355,"Tampa 26,0–28,4 mm"),
      text(640,392,"PCB UI: 20,4–22,0 mm (reserva)"),
      text(640,423,"FFC: 14,3–20,4 mm (proposta)"),
      text(640,454,"PCB principal: 12,6–14,2 mm"),
      text(640,485,"Bateria: 3,0–10,0 mm (reserva)"),
      text(640,516,"Fundo: 0–2,0 mm"),
      text(640,550,"Folgas verticais nominais: 2,6 / 6,2 / 4,0 mm","dim")]
(ROOT/"desenho_empilhamento.svg").write_text(svg("\n".join(side),"Seção e empilhamento preliminar"))
print("Created two dimensioned preliminary SVG views")
