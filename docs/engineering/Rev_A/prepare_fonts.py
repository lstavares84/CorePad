"""Fetch OFL Google Fonts and freeze the exact static weights for the PDF."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
import requests

ROOT=Path(__file__).resolve().parent/'fonts'
ROOT.mkdir(parents=True,exist_ok=True)
FAMILIES={
 'jura':('Jura[wght].ttf','Jura',[(300,'Light','Jura-Light.ttf'),(500,'Medium','Jura-Medium.ttf')]),
 'worksans':('WorkSans[wght].ttf','Work Sans',[(400,'Regular','WorkSans-Regular.ttf'),(500,'Medium','WorkSans-Medium.ttf')]),
 'geistmono':('GeistMono[wght].ttf','Geist Mono',[(400,'Regular','GeistMono-Regular.ttf'),(500,'Medium','GeistMono-Medium.ttf')]),
}

def fetch(family,filename):
    url=f'https://raw.githubusercontent.com/google/fonts/main/ofl/{family}/{filename}'
    response=requests.get(url,timeout=30);response.raise_for_status()
    return response.content

def set_names(font,family,style,postscript):
    names=font['name']
    for name_id,value in [(1,family),(2,style),(3,postscript+'-2026'),(4,family+' '+style),
                          (6,postscript),(16,family),(17,style)]:
        for platform,encoding,language in ((3,1,0x409),(1,0,0)):
            names.setName(value,name_id,platform,encoding,language)
    font['OS/2'].fsSelection &= ~1  # no synthetic italic

for folder,(variable,family,weights) in FAMILIES.items():
    source=ROOT/variable.replace('[wght]','-variable')
    source.write_bytes(fetch(folder,variable))
    for weight,style,out in weights:
        font=instantiateVariableFont(TTFont(source),{'wght':weight},inplace=True)
        set_names(font,family,style,out.removesuffix('.ttf'))
        font.save(ROOT/out)
    license_text=fetch(folder,'OFL.txt').decode('utf-8')
    (ROOT/(folder+'-OFL.txt')).write_text('\n'.join(line.rstrip() for line in license_text.splitlines())+'\n')
(ROOT/'InstrumentSerif-Italic.ttf').write_bytes(fetch('instrumentserif','InstrumentSerif-Italic.ttf'))
license_text=fetch('instrumentserif','OFL.txt').decode('utf-8')
(ROOT/'instrumentserif-OFL.txt').write_text('\n'.join(line.rstrip() for line in license_text.splitlines())+'\n')
print('Prepared seven named static font files and four OFL licenses')
