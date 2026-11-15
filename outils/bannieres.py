# Bannières sobres pour les réseaux (sans logo de projet), assorties à la photo de profil.
# Lancer : python outils/bannieres.py   puis les PNG par Chrome sans fenêtre (voir FORMATS ci-dessous).
import importlib.util
import random
from pathlib import Path

_spec = importlib.util.spec_from_file_location("fabriquer", Path(__file__).with_name("fabriquer.py"))
fab = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(fab)

SORTIE = Path(__file__).resolve().parent.parent / "bannieres"
SORTIE.mkdir(exist_ok=True)

# nom : (largeur, hauteur, part de la hauteur pour le mot)
FORMATS = {
    "x-twitter-1500x500": (1500, 500, 0.27),
    "linkedin-1584x396": (1584, 396, 0.30),
    "discord-680x240": (680, 240, 0.28),
    "youtube-2560x1440": (2560, 1440, 0.11),  # seule la zone centrale 1546x423 est sûre partout
}
RAPPORT_LARGEUR = 4.02  # largeur de « Luandre » en Tektur ≈ 4,02 × corps (mesuré sur la bannière du README)


def banniere(l, h, part):
    random.seed(l * h)
    etoiles = "".join(
        f'<circle cx="{random.uniform(0, l):.0f}" cy="{random.uniform(0, h):.0f}" '
        f'r="{random.choice([0.8, 1, 1.3, 1.7]) * max(1, h / 800):.1f}" fill="#cfe0ff" opacity="{random.uniform(.15, .75):.2f}"/>'
        for _ in range(min(140, int(l * h / 9000)))  # plafonné : un grand format ne doit pas devenir une neige
    )
    corps = h * part
    larg = corps * RAPPORT_LARGEUR
    cx, cy = l / 2, h / 2 + corps * 0.30
    ligne_y = cy + corps * 0.22
    ep = max(4, corps * 0.06)
    arrets = "".join(f'<stop offset="{i/5:.2f}" stop-color="{c}"/>' for i, c in enumerate(fab.SPECTRE))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{l}" height="{h}" viewBox="0 0 {l} {h}">
{fab.police_tektur()}
<defs>
<linearGradient id="fond" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{fab.FOND}"/><stop offset="1" stop-color="{fab.FOND2}"/></linearGradient>
<radialGradient id="halo" cx=".5" cy=".5" r=".5" gradientTransform="translate(0 0)"><stop offset="0" stop-color="{fab.TURQUOISE}" stop-opacity=".13"/><stop offset=".6" stop-color="{fab.OR}" stop-opacity=".04"/><stop offset="1" stop-color="{fab.FOND}" stop-opacity="0"/></radialGradient>
<linearGradient id="spectre" x1="0" y1="0" x2="1" y2="0">{arrets}</linearGradient>
<filter id="flou" x="-10%" y="-400%" width="120%" height="900%"><feGaussianBlur stdDeviation="{ep * 1.6:.1f}"/></filter>
</defs>
<rect width="{l}" height="{h}" fill="url(#fond)"/>
<ellipse cx="{cx}" cy="{h/2}" rx="{l*0.45:.0f}" ry="{h*0.75:.0f}" fill="url(#halo)"/>
{etoiles}
<text x="{cx}" y="{cy:.0f}" text-anchor="middle" font-family="Tektur" font-size="{corps:.0f}" fill="{fab.TEXTE}">Luandre</text>
<rect x="{cx - larg/2:.0f}" y="{ligne_y:.0f}" width="{larg:.0f}" height="{ep:.1f}" rx="{ep/2:.1f}" fill="url(#spectre)" filter="url(#flou)" opacity=".9"/>
<rect x="{cx - larg/2:.0f}" y="{ligne_y:.0f}" width="{larg:.0f}" height="{ep:.1f}" rx="{ep/2:.1f}" fill="url(#spectre)"/>
<text x="{cx}" y="{ligne_y + ep + corps*0.42:.0f}" text-anchor="middle" font-family="{fab.MONO}" font-size="{corps*0.15:.0f}" letter-spacing="{corps*0.04:.1f}" fill="{fab.TEXTE3}">DÉVELOPPEUR SOLO · FRANCE</text>
</svg>
'''


if __name__ == "__main__":
    for nom, (l, h, part) in FORMATS.items():
        (SORTIE / f"{nom}.svg").write_text(banniere(l, h, part), encoding="utf-8")
        print("écrit", nom)
