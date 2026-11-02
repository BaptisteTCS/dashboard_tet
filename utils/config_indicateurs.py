"""Lecture, validation et agrégation des indicateurs décrits dans utils/config.yaml.

Une entrée du YAML = une déclinaison d'une mesure de cube (api_nom_cube, ID) ventilée selon
UN axe (api_nom_axe). Plusieurs entrées peuvent donc pointer vers la même mesure.

L'API renvoie toujours tous les axes du cube, même ceux qui ne sont pas demandés : les lignes
qui ne diffèrent que par les autres axes sont fusionnées selon le champ `agregation` :
- unique (défaut) : au plus une ligne non nulle attendue, sinon erreur ;
- somme : somme des lignes (mesures additives : nombres, volumes, puissances...) ;
- part : somme, puis part en % du total de toutes les valeurs de l'axe.
"""
import pandas as pd
import yaml

CHEMIN_CONFIG = "utils/config.yaml"
AGREGATIONS = ("unique", "somme", "part")


def charger_indicateurs(path_yaml: str = CHEMIN_CONFIG) -> list:
    with open(path_yaml, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)["indicateurs"]


def agregation(indic: dict) -> str:
    return indic.get("agregation") or "unique"


def a_un_axe(indic: dict) -> bool:
    return isinstance(indic["correspondance_indicateurs"], dict)


def identifiants_referentiel(indic: dict) -> list:
    corr = indic["correspondance_indicateurs"]
    return list(corr) if isinstance(corr, dict) else [corr]


def libelle_indicateur(indic: dict) -> str:
    details = [f"ID: {indic['ID']}"]
    if a_un_axe(indic):
        details.append(f"axe: {indic.get('api_nom_axe')}")
    if agregation(indic) != "unique":
        details.append(agregation(indic))
    return f"{indic['metadata']['nom_donnees']} ({', '.join(details)})"


def index_par_identifiant(indicateurs: list) -> dict:
    """identifiant_referentiel -> entrée YAML (unicité garantie par valider_indicateurs)."""
    return {ident: indic for indic in indicateurs for ident in identifiants_referentiel(indic)}


def valider_indicateurs(indicateurs: list) -> list:
    """Retourne la liste des incohérences du YAML (liste vide si tout est correct)."""
    erreurs = []
    libelles = set()
    libelles_par_identifiant = {}
    metadata_par_cle = {}

    for indic in indicateurs:
        lib = libelle_indicateur(indic)
        if lib in libelles:
            erreurs.append(f"Deux entrées ont le même libellé : « {lib} »")
        libelles.add(lib)

        if agregation(indic) not in AGREGATIONS:
            erreurs.append(
                f"{lib} : agregation « {indic['agregation']} » inconnue "
                f"(valeurs possibles : {', '.join(AGREGATIONS)})"
            )
        if a_un_axe(indic) and not indic.get("api_nom_axe"):
            erreurs.append(f"{lib} : api_nom_axe requis quand correspondance_indicateurs est un dictionnaire")
        if agregation(indic) == "part" and not a_un_axe(indic):
            erreurs.append(f"{lib} : l'agrégation « part » nécessite un axe et un dictionnaire de correspondance")

        for ident in identifiants_referentiel(indic):
            libelles_par_identifiant.setdefault(ident, []).append(lib)

        # Les métadonnées sont upsertées par (source_id, nom_donnees) : deux entrées qui partagent
        # cette clé doivent avoir exactement les mêmes métadonnées.
        cle_meta = (indic["metadata"]["source_id"], indic["metadata"]["nom_donnees"])
        if cle_meta in metadata_par_cle and metadata_par_cle[cle_meta] != indic["metadata"]:
            erreurs.append(f"{lib} : métadonnées différentes d'une autre entrée ayant le même nom_donnees")
        metadata_par_cle.setdefault(cle_meta, indic["metadata"])

    for ident, libs in libelles_par_identifiant.items():
        if len(libs) > 1:
            erreurs.append(f"identifiant_referentiel « {ident} » présent dans plusieurs entrées : {' / '.join(libs)}")

    return erreurs


def agreger_autres_axes(df: pd.DataFrame, indic: dict) -> tuple:
    """Fusionne les lignes API qui ne diffèrent que par les axes du cube non utilisés par l'entrée.

    Args:
        df: données API jointes aux collectivités (colonnes brutes de l'API + collectivite_id)
        indic: entrée YAML

    Returns:
        tuple (df_agrege, df_conflits) : df_conflits n'est non vide qu'en agrégation « unique »,
        quand plusieurs lignes non nulles existent pour la même clé.
    """
    cube = indic["api_nom_cube"]
    col_mesure = f"{cube}.id_{indic['ID']}"
    cles = ["collectivite_id", "type_collectivite", f"{cube}.date_mesure.year"]
    if a_un_axe(indic):
        cles.append(f"{cube}.{indic['api_nom_axe']}")

    df = df.copy()
    df[col_mesure] = pd.to_numeric(df[col_mesure], errors="coerce")
    df = df.dropna(subset=[col_mesure])

    mode = agregation(indic)
    if mode == "unique":
        doublons = df.duplicated(subset=cles, keep=False)
        return df.loc[~doublons, cles + [col_mesure]].copy(), df.loc[doublons].sort_values(cles)

    df_agrege = df.groupby(cles, as_index=False)[col_mesure].sum()
    if mode == "part":
        total = df_agrege.groupby(cles[:-1])[col_mesure].transform("sum")
        df_agrege[col_mesure] = (df_agrege[col_mesure] / total * 100).where(total != 0)
        df_agrege = df_agrege.dropna(subset=[col_mesure])
    return df_agrege, df.iloc[0:0]
