# Fabrique les variantes de la photo de profil (dossier ../avatar), dans le style du README.
# Lancer : python outils/avatar.py   (depuis la racine du dépôt du profil)
# PNG 1024 px ensuite, par Chrome sans fenêtre, pour chaque variante :
#   chrome --headless=new --window-size=1024,1024 --default-background-color=0b1426ff --screenshot=avatar/<nom>.png file:///…/avatar/<nom>.svg
import importlib.util
import math
import random
from pathlib import Path

# Palette, police et logos repris du générateur du README.
_spec = importlib.util.spec_from_file_location("fabriquer", Path(__file__).with_name("fabriquer.py"))
fab = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(fab)
FOND, FOND2, OR, TURQUOISE, SPECTRE, SANS, tuile = fab.FOND, fab.FOND2, fab.OR, fab.TURQUOISE, fab.SPECTRE, fab.SANS, fab.tuile

SORTIE = Path(__file__).resolve().parent.parent / "avatar"
SORTIE.mkdir(exist_ok=True)
T = 1024
C = T / 2


def ciel(graine, nombre=60):
    random.seed(graine)
    points = []
    for _ in range(nombre):
        x, y = random.randint(40, T - 40), random.randint(40, T - 40)
        # les étoiles restent dans le rond que GitHub découpe
        if (x - C) ** 2 + (y - C) ** 2 < (C - 50) ** 2:
            points.append(f'<circle cx="{x}" cy="{y}" r="{random.choice([1.6, 2, 2.6, 3.2])}" fill="#cfe0ff" opacity="{random.uniform(.2, .8):.2f}"/>')
    return "".join(points)


def fond(halo):
    return f'''<defs>
<linearGradient id="fond" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{FOND}"/><stop offset="1" stop-color="{FOND2}"/></linearGradient>
<radialGradient id="halo" cx=".5" cy=".45" r=".55">{halo}</radialGradient>
<linearGradient id="spectre" x1="0" y1="0" x2="1" y2="0">{"".join(f'<stop offset="{i/5:.2f}" stop-color="{c}"/>' for i, c in enumerate(SPECTRE))}</linearGradient>
<filter id="flou" x="-20%" y="-300%" width="140%" height="700%"><feGaussianBlur stdDeviation="16"/></filter>
<filter id="flou-anneau" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="14"/></filter>
</defs>
<rect width="{T}" height="{T}" fill="url(#fond)"/>
<rect width="{T}" height="{T}" fill="url(#halo)"/>'''


def svg(contenu):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{T}" height="{T}" viewBox="0 0 {T} {T}">{contenu}</svg>\n'


ONEST = Path.home() / "Desktop" / "LumenKod" / "LumenKit" / "packages" / "pdf" / "fonts" / "onest-400.woff"


def police_onest():
    # Police de LumenKod, embarquée pour que le rendu ne dépende pas du poste.
    import base64
    donnees = base64.b64encode(ONEST.read_bytes()).decode()
    return f'<style>@font-face{{font-family:Onest;src:url(data:font/woff;base64,{donnees})}}</style>'


def texte(famille, poids=400, taille=560, y=640, extra=""):
    return f'<text x="{C}" y="{y}" text-anchor="middle" font-family="{famille}" font-size="{taille}" font-weight="{poids}" fill="#eef2f8" {extra}>L</text>'


# Les « L » essayés pour le monogramme ; la clé choisie va dans LETTRE.
LETTRES = {
    "d-origine": lambda: texte(SANS, 800),
    "segoe-fin": lambda: texte("'Segoe UI'", 300),
    "segoe-demi-fin": lambda: texte("'Segoe UI'", 350),
    "segoe-demi-gras": lambda: texte("'Segoe UI'", 600),
    "bahnschrift": lambda: texte("Bahnschrift", 400, 600, 650),
    "bahnschrift-fin": lambda: texte("Bahnschrift", 300, 600, 650),
    "onest": lambda: police_onest() + texte("Onest", 400),
    "georgia": lambda: texte("Georgia", 400, 580, 640),
    "tektur": lambda: fab.police_tektur() + texte("Tektur", 500, 560, 640),
    "trace": lambda: '<path d="M418 268V632H624" fill="none" stroke="#eef2f8" stroke-width="46" stroke-linecap="round" stroke-linejoin="round"/>',
}
LETTRE = "tektur"  # choix de Luandre le 2026-11-15, comme « Luandre » sur la bannière


def monogramme(lettre=None):
    # A : le « L » et la ligne de lumière, comme le pseudo de la bannière.
    halo = f'<stop offset="0" stop-color="{TURQUOISE}" stop-opacity=".16"/><stop offset=".6" stop-color="{OR}" stop-opacity=".05"/><stop offset="1" stop-color="{FOND}" stop-opacity="0"/>'
    return svg(fond(halo) + ciel(3) + f'''
{LETTRES[lettre or LETTRE]()}
<rect x="282" y="700" width="460" height="26" rx="13" fill="url(#spectre)" filter="url(#flou)" opacity=".9"/>
<rect x="282" y="700" width="460" height="26" rx="13" fill="url(#spectre)"/>''')


def anneau():
    # B : le « L » au centre d'un anneau de lumière aux six couleurs.
    halo = f'<stop offset="0" stop-color="{SPECTRE[5]}" stop-opacity=".14"/><stop offset="1" stop-color="{FOND}" stop-opacity="0"/>'
    arcs = ""
    r = 330
    for i, c in enumerate(SPECTRE):
        a0, a1 = math.radians(-90 + i * 60 + 4), math.radians(-90 + (i + 1) * 60 - 4)
        x0, y0, x1, y1 = C + r * math.cos(a0), C + r * math.sin(a0), C + r * math.cos(a1), C + r * math.sin(a1)
        d = f"M{x0:.1f} {y0:.1f} A{r} {r} 0 0 1 {x1:.1f} {y1:.1f}"
        arcs += f'<path d="{d}" stroke="{c}" stroke-width="30" fill="none" stroke-linecap="round" filter="url(#flou-anneau)" opacity=".8"/>'
        arcs += f'<path d="{d}" stroke="{c}" stroke-width="22" fill="none" stroke-linecap="round"/>'
    return svg(fond(halo) + ciel(5) + arcs + f'''
<text x="{C}" y="{C + 165}" text-anchor="middle" font-family="{SANS}" font-size="470" font-weight="800" fill="#eef2f8">L</text>''')


def constellation():
    # C : le « L » relié aux quatre projets, comme le losange de la bannière.
    halo = f'<stop offset="0" stop-color="{TURQUOISE}" stop-opacity=".14"/><stop offset=".6" stop-color="{OR}" stop-opacity=".06"/><stop offset="1" stop-color="{FOND}" stop-opacity="0"/>'
    t = 150
    pos = {"neofrag": (C - t / 2, 120), "kemet": (T - 120 - t, C - t / 2), "lumenkod": (C - t / 2, T - 120 - t), "fsr": (120, C - t / 2)}
    centres = {k: (x + t / 2, y + t / 2) for k, (x, y) in pos.items()}
    ordre = ["neofrag", "kemet", "lumenkod", "fsr", "neofrag"]
    fil = " ".join(f"{'M' if i == 0 else 'L'}{centres[k][0]:.0f} {centres[k][1]:.0f}" for i, k in enumerate(ordre))
    tuiles = "".join(
        f'<rect x="{x - 2}" y="{y - 2}" width="{t + 4}" height="{t + 4}" rx="{t * 0.24:.0f}" fill="#151c2b" stroke="#2a3550" stroke-width="3"/>'
        + tuile(k, x, y, t)
        for k, (x, y) in pos.items()
    )
    return svg(fond(halo) + ciel(9) + f'''
<path d="{fil}" fill="none" stroke="#9fb3d6" stroke-opacity=".35" stroke-width="4" stroke-dasharray="14 18"/>
{tuiles}
<text x="{C}" y="{C + 105}" text-anchor="middle" font-family="{SANS}" font-size="300" font-weight="800" fill="#eef2f8">L</text>
<rect x="{C - 120}" y="{C + 140}" width="240" height="16" rx="8" fill="url(#spectre)"/>''')


if __name__ == "__main__":
    for nom, f in [("a-monogramme", monogramme), ("b-anneau", anneau), ("c-constellation", constellation)]:
        (SORTIE / f"{nom}.svg").write_text(f(), encoding="utf-8")
        print("écrit", nom)
