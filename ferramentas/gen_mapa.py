# -*- coding: utf-8 -*-
# Gera mapas/europa.svg: pega no mapa base (Wikimedia, CC BY-SA 3.0), pinta os
# países do livro e acrescenta a camada de rótulos (nomes + linhas-guia).
# Correr a partir desta pasta:  python3 gen_mapa.py
# Ajustar países: lista BOOK.  Ajustar rótulos: dicionário L (coordenadas no
# sistema do SVG base, 0..680 x 0..520).
import re

SRC = "europa-base.svg"
DST = "../mapas/europa.svg"

BOOK = "pt es ad fr mc it sm va mt gb ie be nl lu de ch li at dk no se is fi ee lv lt pl cz sk hu si hr ba rs me xk al mk gr bg ro md tr cy ua by ru ge am az".split()

# Membros da UE (recebem o azul da bandeira; os restantes países do livro ficam azulejo)
BOOK_EU = "pt es fr it mt ie be nl lu de at dk se fi ee lv lt pl cz sk hu si hr gr bg ro cy".split()

COR_EU     = "#003399"   # azul da bandeira europeia
COR_LIVRO  = "#2C5F7C"   # azulejo — países do livro fora da UE
COR_OUTROS = "#E7E1D3"   # restantes territórios

VIEWBOX = "100 50 600 470"

# iso: (text, x, y, size, cls, leader_to (x,y) or None, extra)
#   cls: 'on' (light text on country) | 'off' (dark text on sea/margin)
#   extra dict keys: a=text-anchor(middle/start/end), ls=letter-spacing, rot=deg
L = {
 "ru": ("RÚSSIA",         505,150, 12,"on", None, {"ls":3}),
 "ua": ("UCRÂNIA",        479,322,  9,"on", None, {"ls":1}),
 "tr": ("TURQUIA",        512,452,  8,"on", None, {"ls":1}),
 "fr": ("FRANÇA",         243,381,  9,"on", None, {"ls":1}),
 "es": ("ESPANHA",        198,452,  9,"on", None, {"ls":1}),
 "pt": ("Portugal",       118,472,  6,"off", (136,450), {"a":"middle"}),
 "de": ("ALEMANHA",       312,320,  8,"on", None, {}),
 "pl": ("POLÓNIA",        380,306,  8,"on", None, {}),
 "it": ("ITÁLIA",         322,412,  7,"on", None, {"rot":26}),
 "se": ("SUÉCIA",         357,182,  8,"on", None, {"rot":-62}),
 "no": ("NORUEGA",        320,150,  8,"on", None, {"rot":-57}),
 "fi": ("FINLÂNDIA",      399,156,  7,"on", None, {"rot":-57}),
 "gb": ("REINO|UNIDO",    232,233,  5.8,"on", None, {}),
 "is": ("ISLÂNDIA",       161,119,  7,"on", None, {}),
 "ie": ("IRLANDA",        170,281,  5.0,"on", None, {}),
 "ro": ("ROMÉNIA",        438,373,  8,"on", None, {}),
 "by": ("BIELORRÚSSIA",   440,276,  6,"on", None, {"ls":0.3}),
 "bg": ("BULGÁRIA",       449,414,  6.4,"on", None, {}),
 "gr": ("GRÉCIA",         432,452,  6.4,"on", None, {}),
 "dk": ("DINAMARCA",      314,254,  5.2,"on", None, {}),
 "at": ("ÁUSTRIA",        340,364,  6.2,"on", None, {}),
 "cz": ("CHÉQUIA",        352,337,  6.2,"on", None, {}),
 "hu": ("HUNGRIA",        389,367,  6.2,"on", None, {}),
 "rs": ("SÉRVIA",         405,401,  5.8,"on", None, {}),
 "hr": ("CROÁCIA",        349,393,  5.6,"on", None, {}),
 "ba": ("BÓSNIA",         379,413,  5.2,"on", None, {}),
 "ch": ("SUÍÇA",          293,377,  5.6,"on", None, {}),
 "ee": ("ESTÓNIA",        405,220,  5.8,"on", None, {}),
 "lv": ("LETÓNIA",        408,243,  5.8,"on", None, {}),
 "lt": ("LITUÂNIA",       404,266,  5.8,"on", None, {}),
 "sk": ("ESLOVÁQUIA",     390,347,  4.8,"on", None, {}),

 # leader-line labels (small / crowded)
 "ad": ("Andorra",        236,464, 5.6,"off", (231,427), {"a":"middle"}),
 "mc": ("Mónaco",         302,452, 5.6,"off", (286,417), {"a":"start"}),
 "sm": ("San Marino",     366,417, 5.2,"off", (331,413), {"a":"start"}),
 "va": ("Vaticano",       302,458, 5.4,"off", (331,439), {"a":"end"}),
 "li": ("Listenstaine",   318,392, 4.8,"off", (305,374), {"a":"end"}),
 "lu": ("Luxemburgo",     245,344, 5.2,"off", (277,340), {"a":"end"}),
 "be": ("Bélgica",        241,328, 5.2,"off", (265,332), {"a":"end"}),
 "nl": ("Países Baixos",  246,306, 5.2,"off", (272,313), {"a":"end"}),
 "si": ("Eslovénia",      321,379, 5.2,"off", (351,385), {"a":"end"}),
 "me": ("Montenegro",     350,442, 5.4,"off", (392,424), {"a":"end"}),
 "al": ("Albânia",        389,466, 5.4,"off", (404,443), {"a":"middle"}),
 "xk": ("Kosovo",         449,423, 5.2,"off", (409,424), {"a":"start"}),
 "mk": ("Mac. do Norte",  452,440, 5.0,"off", (419,435), {"a":"start"}),
 "md": ("Moldávia",       472,349, 5.4,"off", (462,357), {"a":"start"}),
 "cy": ("Chipre",         560,487, 5.8,"off", (545,483), {"a":"start"}),
 "mt": ("Malta",          366,507, 5.6,"off", (353,511), {"a":"start"}),
 "ge": ("Geórgia",        650,350, 5.8,"off", (605,366), {"a":"start"}),
 "am": ("Arménia",        654,372, 5.8,"off", (631,381), {"a":"start"}),
 "az": ("Azerbaijão",     652,392, 5.8,"off", (649,369), {"a":"start"}),
}

s = open(SRC, encoding="utf-8").read()

def sel(codes):
    return ",".join(f"#{c},#{c} *" for c in codes)

sel_livro = sel([c for c in BOOK if c not in BOOK_EU])
sel_eu    = sel([c for c in BOOK_EU])
xk_eu = "xk" in BOOK_EU
style = ('<style id="style1">'
  f'.c{{fill:{COR_OUTROS};stroke:#FFFFFF;stroke-width:0.4}}'
  '.d{stroke-dasharray:0.4 0.4;fill:#0000}'
  '.k{paint-order:stroke fill;stroke-width:0.8}'
  f'{sel_livro}{{fill:{COR_LIVRO}}}'
  f'{sel_eu}{{fill:{COR_EU}}}'
  f'#xk,#xk *{{fill:{COR_EU if xk_eu else COR_LIVRO};stroke-dasharray:none;stroke:#FFFFFF}}'
  '.maplbl{font-family:"Work Sans","Helvetica Neue",Arial,sans-serif;font-weight:600;'
    'paint-order:stroke;stroke-linejoin:round;stroke-linecap:round;}'
  '.maplbl.on{fill:#FAF7F0;stroke:#1c4258;stroke-width:1.1;}'
  '.maplbl.off{fill:#2b3a42;stroke:#FAF7F0;stroke-width:1.4;}'
  '.leader{stroke:#8a7a5c;stroke-width:0.35;fill:none;}'
  '.leaderdot{fill:#6B1E2B;}'
  '</style>')
s = re.sub(r'<style\b[^>]*>.*?</style>', style, s, count=1, flags=re.S)

# viewBox
s = s.replace('<svg\n   width="680"\n   height="520"',
              f'<svg\n   width="680"\n   height="520"\n   viewBox="{VIEWBOX}"', 1)

def esc(t):
    return t.replace("&","&amp;").replace("<","&lt;")

leaders = []
labels = []
for iso,(t,x,y,sz,cls,to,ex) in L.items():
    a = ex.get("a","middle")
    ls = ex.get("ls")
    rot = ex.get("rot")
    if to:
        lx,ly = to
        leaders.append(f'<line class="leader" x1="{x}" y1="{y-1.3}" x2="{lx}" y2="{ly}"/>')
        leaders.append(f'<circle class="leaderdot" cx="{lx}" cy="{ly}" r="1.1"/>')
    attrs = f'class="maplbl {cls}" x="{x}" y="{y}" font-size="{sz}" text-anchor="{a}"'
    if ls is not None: attrs += f' letter-spacing="{ls}"'
    if rot is not None: attrs += f' transform="rotate({rot} {x} {y})"'
    if "|" in t:
        a1,a2 = t.split("|",1)
        inner = (f'<tspan x="{x}" dy="-0.35em">{esc(a1)}</tspan>'
                 f'<tspan x="{x}" dy="1.05em">{esc(a2)}</tspan>')
        labels.append(f'<text {attrs}>{inner}</text>')
    else:
        labels.append(f'<text {attrs}>{esc(t)}</text>')

overlay = '<g id="rotulos">' + "".join(leaders) + "".join(labels) + '</g>'
s = s.replace("</svg>", overlay + "</svg>", 1)

open(DST,"w",encoding="utf-8").write(s)
print("wrote", DST, len(s), "bytes;", len(L), "labels")
