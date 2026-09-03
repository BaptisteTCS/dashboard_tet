"""Smoke test jetable : suggestion d'indicateurs a partir de titres d'actions."""
import pathlib
import time

source = pathlib.Path("pages/43_indicateur_reference.py").read_text(encoding="utf-8")
logique = source.split("# ==========================\n# Interface")[0]

espace: dict = {}
exec(compile(logique, "page43_logique", "exec"), espace)

df = espace["load_indicateur_reference"]()
catalogue, themes, libelles = espace["build_catalogue"](df)
resoudre = espace["resoudre_suggestion"]

actions = [
    "Amenager des pistes cyclables",
    "Renover l'eclairage public de la commune",
    "Installer des panneaux photovoltaiques sur les toitures des ecoles",
    "Mettre en place une collecte separee des biodechets",
    "Organiser la fete de la musique",
    "Accompagner les menages en situation de precarite energetique",
]

for action in actions:
    debut = time.perf_counter()
    res = resoudre(action, catalogue, themes, libelles)
    duree = time.perf_counter() - debut
    print(f"\n[{duree:.2f}s] {action}")
    print(f"  theme : {res['theme']}")
    for item in res["libelles"]:
        print(f"   - {item['libelle']} ({item['nb_ct']} ct)")
    if not res["libelles"]:
        print("   (aucun indicateur retenu)")
