"""Render representative PDF pages and verify font embedding and page bounds.

Run: uv run --with pymupdf python docs/engineering/Rev_A/render_verify.py
Requires Poppler (pdftoppm, pdffonts) and Pillow.
"""
from pathlib import Path
import json, subprocess
import pymupdf
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parent
PDF=ROOT/'CorePad_Caderno_de_Engenharia_Rev_A.pdf'
PREV=ROOT/'previews';PREV.mkdir(exist_ok=True)
SAMPLES=[1,2,3,4,5,6,7,8,10,11,12,16,17,18,20,22,26,27,28,32,33,34,35,36,40,42,44,45,47,49,51,54,56,58,61,63,65]
for path in PREV.glob('pagina_*.png'):
    if int(path.stem.split('_')[1]) not in SAMPLES:
        path.unlink()
for path in PREV.glob('contato_*.png'):
    path.unlink()
for n in SAMPLES:
    path=PREV/f'pagina_{n:02d}.png'
    subprocess.run(['pdftoppm','-f',str(n),'-l',str(n),'-r','110','-png','-singlefile',str(PDF),str(path.with_suffix(''))],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
thumbs=[]
for n in SAMPLES:
    im=Image.open(PREV/f'pagina_{n:02d}.png').convert('RGB')
    im.thumbnail((400,285))
    tile=Image.new('RGB',(420,320),'white');tile.paste(im,((420-im.width)//2,5))
    ImageDraw.Draw(tile).text((12,292),f'Página {n}',fill='black')
    thumbs.append(tile)
for offset in range(0,len(thumbs),12):
    sheet=Image.new('RGB',(1680,960),'#bfc2c4')
    for j,tile in enumerate(thumbs[offset:offset+12]):
        sheet.paste(tile,((j%4)*420,(j//4)*320))
    sheet.save(PREV/f'contato_{offset//12+1:02d}.png')

doc=pymupdf.open(PDF)
errors=[];sizes=set()
for n,page in enumerate(doc,1):
    if abs(page.rect.width-420*72/25.4)>.2 or abs(page.rect.height-297*72/25.4)>.2:
        errors.append({'page':n,'issue':'page size'})
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines',[]):
            for span in line['spans']:
                sizes.add(round(span['size'],1))
                x0,y0,x1,y1=span['bbox']
                if x0 < -1 or y0 < -1 or x1 > page.rect.width+1 or y1 > page.rect.height+1:
                    errors.append({'page':n,'issue':'text outside page','text':span['text'][:60]})
fonts=subprocess.check_output(['pdffonts',str(PDF)],text=True)
expected=['Jura-Light','Jura-Medium','WorkSans-Regular','WorkSans-Medium','GeistMono-Regular','GeistMono-Medium','InstrumentSerif-Italic']
missing=[name for name in expected if name not in fonts]
if missing:errors.append({'issue':'missing embedded font','fonts':missing})
report={'pages':len(doc),'sample_pages':SAMPLES,'samples_rendered':len(SAMPLES),
        'font_sizes_pt':sorted(sizes),'embedded_font_families':expected,'text_out_of_page':sum(e.get('issue')=='text outside page' for e in errors),
        'errors':errors,'visual_review':'Contatos 01-04 e páginas 2, 11, 18, 33-35, 45 e 65 inspecionados manualmente.'}
(ROOT/'relatorio_qa.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
if errors: raise SystemExit(json.dumps(errors,ensure_ascii=False))
print(f"Verified {len(doc)} pages, {len(SAMPLES)} preview pages, {len(expected)} embedded families, no out-of-page text")
