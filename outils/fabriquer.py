# Fabrique les images SVG du profil GitHub (dossier ../assets).
# Lancer : python outils/fabriquer.py   (depuis la racine du dépôt du profil)
import base64
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
LOGOS = RACINE / "outils" / "logos"
SORTIE = RACINE / "assets"
SORTIE.mkdir(exist_ok=True)

# Palette : la nuit de Kemet pour le fond, une couleur par projet.
FOND, FOND2, CARTE = "#0b1426", "#070d1a", "#0f1a31"
TEXTE, TEXTE2, TEXTE3 = "#eef2f8", "#b4c0d4", "#7d8ba4"
TURQUOISE, OR, ARDOISE, ROUGE = "#2ee6d6", "#d9ab4f", "#e7ebf1", "#ff6b4a"
SPECTRE = ["#3ba3ff", "#2fbf71", "#f2c14e", "#ff8a3d", "#ff5c8a", "#b07cff"]

SANS = "'Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif"
MONO = "'JetBrains Mono','Cascadia Code',Consolas,'SFMono-Regular',Menlo,monospace"


def png(nom):
    return "data:image/png;base64," + base64.b64encode((LOGOS / f"{nom}.png").read_bytes()).decode()


def logo_lumenkod(x, y, taille):
    # Le logo de LumenKod (version sombre) posé sur une tuile.
    interieur = (LOGOS / "lumenkod.svg").read_text(encoding="utf-8")
    interieur = interieur.split(">", 1)[1].rsplit("</svg>", 1)[0]
    interieur = interieur.replace("<title>LumenKod</title>", "")
    return (
        f'<rect x="{x}" y="{y}" width="{taille}" height="{taille}" rx="{taille*0.22:.1f}" fill="#151c2b" stroke="#2a3550"/>'
        f'<svg x="{x + taille*0.12:.1f}" y="{y + taille*0.08:.1f}" width="{taille*0.76:.1f}" height="{taille*0.76:.1f}" viewBox="0 0 64 64">{interieur}</svg>'
    )


def tuile(nom, x, y, taille):
    if nom == "lumenkod":
        return logo_lumenkod(x, y, taille)
    return f'<image href="{png(nom)}" x="{x}" y="{y}" width="{taille}" height="{taille}"/>'


def echapper(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def largeur(texte, corps, mono=False):
    return len(texte) * corps * (0.6 if mono else 0.56)


def pastille(x, y, texte, couleur, corps=14, plein=False):
    l = largeur(texte, corps, mono=True) + 24
    fond = couleur if plein else "none"
    encre = FOND if plein else couleur
    return (
        f'<rect x="{x}" y="{y}" width="{l:.0f}" height="{corps+14}" rx="{(corps+14)/2:.0f}" fill="{fond}" '
        f'stroke="{couleur}" stroke-opacity="{1 if plein else .55}"/>'
        f'<text x="{x + l/2:.0f}" y="{y + corps + 3.5:.0f}" text-anchor="middle" font-family="{MONO}" '
        f'font-size="{corps}" font-weight="600" fill="{encre}">{echapper(texte)}</text>'
    ), l


MOINS_DE_MOUVEMENT = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"


def ecrire(nom, contenu):
    (SORTIE / nom).write_text(contenu, encoding="utf-8")
    print("écrit", nom, len(contenu) // 1024, "Ko")


# ---------------------------------------------------------------- bannière
def banniere():
    L, H = 1280, 360
    import random
    random.seed(7)
    etoiles = "".join(
        f'<circle cx="{random.randint(0, L)}" cy="{random.randint(0, H)}" r="{random.choice([0.8, 1, 1.2, 1.6])}" '
        f'class="e" style="animation-delay:{random.uniform(0, 6):.1f}s"/>'
        for _ in range(70)
    )
    arrets = "".join(
        f'<stop offset="{i/(len(SPECTRE)*2-1):.3f}" stop-color="{c}"/>'
        for i, c in enumerate(SPECTRE + SPECTRE)
    )
    # Les quatre projets en losange, reliés par un fil de lumière.
    pos = {"neofrag": (1010, 46), "kemet": (1142, 140), "fsr": (878, 140), "lumenkod": (1010, 234)}
    T = 92
    centre = {k: (x + T / 2, y + T / 2) for k, (x, y) in pos.items()}
    ordre = ["neofrag", "kemet", "lumenkod", "fsr", "neofrag"]
    fil = " ".join(f"{'M' if i == 0 else 'L'}{centre[k][0]:.0f},{centre[k][1]:.0f}" for i, k in enumerate(ordre))
    tuiles = "".join(
        f'<g class="f" style="animation-delay:{i*0.8:.1f}s">{tuile(k, x, y, T)}</g>'
        for i, (k, (x, y)) in enumerate(pos.items())
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{L}" height="{H}" viewBox="0 0 {L} {H}" role="img" aria-label="Luandre, développeur solo">
<style>
.e{{fill:#cfe0ff;animation:sc 6s ease-in-out infinite}}
@keyframes sc{{0%,100%{{opacity:.15}}50%{{opacity:.8}}}}
.f{{animation:fl 7s ease-in-out infinite}}
@keyframes fl{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-6px)}}}}
.fil{{stroke-dasharray:6 10;animation:fi 4s linear infinite}}
@keyframes fi{{to{{stroke-dashoffset:-64}}}}
{MOINS_DE_MOUVEMENT}
</style>
<defs>
<linearGradient id="fond" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{FOND}"/><stop offset="1" stop-color="{FOND2}"/></linearGradient>
<radialGradient id="halo" cx=".78" cy=".5" r=".45"><stop offset="0" stop-color="#2ee6d6" stop-opacity=".16"/><stop offset=".55" stop-color="#d9ab4f" stop-opacity=".06"/><stop offset="1" stop-color="{FOND}" stop-opacity="0"/></radialGradient>
<linearGradient id="spectre" x1="0" y1="0" x2="1" y2="0" spreadMethod="repeat">{arrets}
<animateTransform attributeName="gradientTransform" type="translate" from="0 0" to="-1 0" dur="9s" repeatCount="indefinite"/></linearGradient>
<filter id="flou" x="-10%" y="-400%" width="120%" height="900%"><feGaussianBlur stdDeviation="7"/></filter>
</defs>
<rect width="{L}" height="{H}" rx="22" fill="url(#fond)"/>
<rect width="{L}" height="{H}" rx="22" fill="url(#halo)"/>
{etoiles}
<text x="80" y="92" font-family="{MONO}" font-size="17" letter-spacing="3" fill="{TEXTE3}">DÉVELOPPEUR SOLO · FRANCE</text>
<text x="74" y="190" font-family="{SANS}" font-size="112" font-weight="800" letter-spacing="-2" fill="{TEXTE}">Luandre</text>
<rect x="82" y="216" width="478" height="7" rx="3.5" fill="url(#spectre)" filter="url(#flou)" opacity=".9"/>
<rect x="82" y="216" width="478" height="7" rx="3.5" fill="url(#spectre)"/>
<text x="80" y="266" font-family="{SANS}" font-size="25" fill="{TEXTE2}">Jeux, CMS libre et outils maison.</text>
<text x="80" y="302" font-family="{SANS}" font-size="19" font-style="italic" fill="{TEXTE3}">Je fais renaître ce qui en vaut la peine.</text>
<path d="{fil}" fill="none" stroke="#9fb3d6" stroke-opacity=".35" stroke-width="1.5" class="fil"/>
{tuiles}
</svg>
'''


# ---------------------------------------------------------------- fiche
def fiche():
    L = 1280
    lignes = [
        ("Classe", "Développeur solo, touche-à-tout du web au jeu vidéo"),
        ("Langages", "PHP · TypeScript · C# · Go"),
        ("Outils", "Godot 4 .NET · Next.js · PostgreSQL · MariaDB · Docker"),
        ("Terrain", "mon propre serveur Linux, des bots Discord, Cloudflare"),
        ("Quêtes", "NeoFrag Reborn · Kemet · Friendly Strike Reborn · LumenKod"),
        ("Signe", "tout en français, de l'interface aux commentaires du code"),
        ("Premiers pas", "NeoFrag, le CMS que je fais renaître aujourd'hui"),
    ]
    y0, pas = 140, 48
    H = y0 + pas * len(lignes) + 18
    corps = ""
    for i, (cle, val) in enumerate(lignes):
        y = y0 + i * pas
        corps += (
            f'<text x="72" y="{y}" font-family="{MONO}" font-size="20" fill="{OR}">{echapper(cle)}</text>'
            f'<line x1="{72 + largeur(cle, 20, True) + 12:.0f}" y1="{y-6}" x2="316" y2="{y-5}" stroke="{TEXTE3}" stroke-opacity=".45" stroke-dasharray="2 6"/>'
            f'<text x="332" y="{y}" font-family="{SANS}" font-size="23" fill="{TEXTE}">{echapper(val)}</text>'
        )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{L}" height="{H}" viewBox="0 0 {L} {H}" role="img" aria-label="Fiche du personnage">
<defs><linearGradient id="b" x1="0" y1="0" x2="1" y2="0">{"".join(f'<stop offset="{i/5:.2f}" stop-color="{c}"/>' for i, c in enumerate(SPECTRE))}</linearGradient></defs>
<rect x="1" y="1" width="{L-2}" height="{H-2}" rx="20" fill="{CARTE}" stroke="#22304d"/>
<rect x="1" y="1" width="{L-2}" height="5" rx="2.5" fill="url(#b)" opacity=".85"/>
<text x="72" y="72" font-family="{SANS}" font-size="30" font-weight="700" fill="{TEXTE}">Fiche du personnage</text>
<text x="{L-72}" y="72" text-anchor="end" font-family="{MONO}" font-size="17" fill="{TEXTE3}">niveau : toujours en train d'apprendre</text>
<line x1="72" y1="94" x2="{L-72}" y2="94" stroke="#22304d"/>
{corps}
</svg>
'''


# ---------------------------------------------------------------- cartes
def carte(cle, titre, couleur, statut, statut_couleur, description, etiquettes, logo):
    L, H = 620, 360
    desc = "".join(
        f'<text x="36" y="{172 + i*32}" font-family="{SANS}" font-size="21" fill="{TEXTE2}">{echapper(l)}</text>'
        for i, l in enumerate(description)
    )
    x, tags = 36, ""
    for i, e in enumerate(etiquettes):
        # LumenKod : chaque étiquette prend une couleur du spectre.
        teinte = SPECTRE[(i * 2) % 6] if couleur == "spectre" else couleur
        p, l = pastille(x, 292, e, teinte, corps=15)
        tags += p
        x += l + 10
    chip, _ = pastille(136, 86, statut, statut_couleur, corps=14, plein=True)
    accent = (
        f'<linearGradient id="a{cle}" x1="0" y1="0" x2="1" y2="0">'
        + "".join(f'<stop offset="{i/5:.2f}" stop-color="{c}"/>' for i, c in enumerate(SPECTRE))
        + "</linearGradient>"
        if couleur == "spectre"
        else f'<linearGradient id="a{cle}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{couleur}"/><stop offset="1" stop-color="{couleur}" stop-opacity=".15"/></linearGradient>'
    )
    halo = SPECTRE[0] if couleur == "spectre" else couleur
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{L}" height="{H}" viewBox="0 0 {L} {H}" role="img" aria-label="{echapper(titre)}">
<defs>{accent}
<radialGradient id="h{cle}" cx=".1" cy=".05" r=".8"><stop offset="0" stop-color="{halo}" stop-opacity=".2"/><stop offset="1" stop-color="{halo}" stop-opacity="0"/></radialGradient></defs>
<rect x="1" y="1" width="{L-2}" height="{H-2}" rx="20" fill="{CARTE}" stroke="#22304d"/>
<rect x="1" y="1" width="{L-2}" height="{H-2}" rx="20" fill="url(#h{cle})"/>
{logo}
<text x="136" y="70" font-family="{SANS}" font-size="31" font-weight="700" fill="{TEXTE}">{echapper(titre)}</text>
{chip}
{desc}
{tags}
<rect x="1" y="{H-7}" width="{L-2}" height="6" rx="3" fill="url(#a{cle})"/>
</svg>
'''


def cartes():
    ecrire("carte-neofrag.svg", carte(
        "nf", "NeoFrag Reborn", TURQUOISE, "PUBLIÉ · LIBRE", "#3ddc84",
        ["Le CMS PHP libre des communautés : forum,",
         "actualités, événements, membres, équipes et",
         "matchs. La suite de NeoFrag, reprise et modernisée."],
        ["PHP 8.2+", "MariaDB", "marketplace", "bot Discord"],
        tuile("neofrag", 36, 36, 84)))
    ecrire("carte-kemet.svg", carte(
        "km", "Kemet", OR, "EN DÉVELOPPEMENT", OR,
        ["Jeu de gestion social par navigateur dans",
         "l'Égypte de Ramsès : une économie faite par",
         "les joueurs, une histoire sourcée."],
        ["TypeScript", "Next.js", "PostgreSQL"],
        tuile("kemet", 36, 36, 84)))
    ecrire("carte-fsr.svg", carte(
        "fs", "Friendly Strike Reborn", ROUGE, "EN DÉVELOPPEMENT", ROUGE,
        ["Friendly Strike recréé de zéro en technos",
         "modernes : shooter 2D en arène, manches et",
         "phase d'achat, à 4 sur un PC, en ligne en cours."],
        ["C#", "Godot 4 .NET", ".NET 10"],
        tuile("fsr", 36, 36, 84)))
    ecrire("carte-lumenkod.svg", carte(
        "lk", "LumenKod", "spectre", "EN CONSTRUCTION", SPECTRE[2],
        ["Mon entreprise : sites web, logiciels Windows",
         "sur devis, bots Discord, reprise de projets",
         "existants — et une gamme d'outils maison."],
        ["TypeScript", "Next.js", "PostgreSQL"],
        tuile("lumenkod", 36, 36, 84)))


# ---------------------------------------------------------------- établi
def etabli():
    L = 1280
    groupes = [
        ("Langages", ["PHP", "TypeScript", "C#", "Go"], TURQUOISE),
        ("Moteurs et cadres", ["Godot 4 .NET", "Next.js", "WPF", "Hono"], OR),
        ("Données", ["PostgreSQL", "MariaDB", "Redis"], SPECTRE[5]),
        ("Terrain", ["Linux", "Docker", "Cloudflare", "Discord"], ROUGE),
    ]
    corps, y = "", 34
    for titre, items, c in groupes:
        corps += f'<text x="56" y="{y + 25}" font-family="{MONO}" font-size="19" fill="{TEXTE3}">{echapper(titre)}</text>'
        x = 330
        for it in items:
            p, l = pastille(x, y, it, c, corps=19)
            corps += p
            x += l + 14
        y += 62
    H = y + 4
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{L}" height="{H}" viewBox="0 0 {L} {H}" role="img" aria-label="L'établi">
<rect x="1" y="1" width="{L-2}" height="{H-2}" rx="20" fill="{CARTE}" stroke="#22304d"/>
{corps}
</svg>
'''


# ---------------------------------------------------------------- pied
def pied():
    # Répond à la bannière : même nuit étoilée, même ligne de lumière, les quatre projets en signature.
    L, H = 1280, 210
    import random
    random.seed(11)
    etoiles = "".join(
        f'<circle cx="{random.randint(0, L)}" cy="{random.randint(0, H-30)}" r="{random.choice([0.8, 1, 1.2, 1.5])}" '
        f'class="e" style="animation-delay:{random.uniform(0, 6):.1f}s"/>'
        for _ in range(45)
    )
    arrets = "".join(
        f'<stop offset="{i/(len(SPECTRE)*2-1):.3f}" stop-color="{c}"/>'
        for i, c in enumerate(SPECTRE + SPECTRE)
    )
    T, x0 = 64, 870
    tuiles = "".join(
        f'<g class="f" style="animation-delay:{i*0.7:.1f}s">'
        f'<rect x="{x0 + i*(T+22) - 1}" y="57" width="{T+2}" height="{T+2}" rx="15" fill="#151c2b" stroke="#2a3550"/>'
        f'{tuile(k, x0 + i*(T+22), 58, T)}</g>'
        for i, k in enumerate(["neofrag", "kemet", "fsr", "lumenkod"])
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{L}" height="{H}" viewBox="0 0 {L} {H}" role="img" aria-label="Merci de la visite, à bientôt sur l'un des projets">
<style>
.e{{fill:#cfe0ff;animation:sc 6s ease-in-out infinite}}
@keyframes sc{{0%,100%{{opacity:.15}}50%{{opacity:.8}}}}
.f{{animation:fl 7s ease-in-out infinite}}
@keyframes fl{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-5px)}}}}
{MOINS_DE_MOUVEMENT}
</style>
<defs>
<linearGradient id="fond" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{FOND2}"/><stop offset="1" stop-color="{FOND}"/></linearGradient>
<radialGradient id="halo" cx=".18" cy=".45" r=".5"><stop offset="0" stop-color="{OR}" stop-opacity=".12"/><stop offset="1" stop-color="{FOND}" stop-opacity="0"/></radialGradient>
<linearGradient id="spectre" x1="0" y1="0" x2="1" y2="0" spreadMethod="repeat">{arrets}
<animateTransform attributeName="gradientTransform" type="translate" from="0 0" to="-1 0" dur="9s" repeatCount="indefinite"/></linearGradient>
<filter id="flou" x="-10%" y="-400%" width="120%" height="900%"><feGaussianBlur stdDeviation="7"/></filter>
<clipPath id="k"><rect width="{L}" height="{H}" rx="22"/></clipPath>
</defs>
<g clip-path="url(#k)">
<rect width="{L}" height="{H}" fill="url(#fond)"/>
<rect width="{L}" height="{H}" fill="url(#halo)"/>
{etoiles}
<text x="80" y="92" font-family="{SANS}" font-size="46" font-weight="800" letter-spacing="-1" fill="{TEXTE}">Merci de la visite.</text>
<text x="82" y="134" font-family="{SANS}" font-size="21" fill="{TEXTE2}">À bientôt sur l'un des projets.</text>
<text x="{x0 + (4*T + 3*22)/2:.0f}" y="156" text-anchor="middle" font-family="{MONO}" font-size="13" letter-spacing="2" fill="{TEXTE3}">FAIT EN FRANCE · EN FRANÇAIS</text>
{tuiles}
<rect x="0" y="{H-8}" width="{L}" height="8" fill="url(#spectre)" filter="url(#flou)" opacity=".9"/>
<rect x="0" y="{H-6}" width="{L}" height="6" fill="url(#spectre)"/>
</g>
</svg>
'''


ecrire("banniere.svg", banniere())
ecrire("fiche.svg", fiche())
cartes()
ecrire("etabli.svg", etabli())
ecrire("pied.svg", pied())
