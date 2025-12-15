import streamlit as st
from google import genai
from google.genai import types
from pypdf import PdfReader
import asyncio
import os
import io
import time
from datetime import datetime
import json
import pandas as pd
import re
import nest_asyncio
import pandas as pd
from openpyxl import load_workbook
nest_asyncio.apply()

st.set_page_config(layout="wide")
st.title("✨ Import Tool :blue-badge[:material/experiment: Beta]")

# Configuration des APIs
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialisation des clients async
gemini_client = genai.Client(api_key=GOOGLE_API_KEY)

# Prompt personnalisé
custom_prompt = """
Vous êtes un agent d’extraction documentaire spécialisé dans les plans d’actions de transition écologique des collectivités, y compris les PCAET.

Contexte du fichier en entrée
Le texte fourni est un document de plan d’actions d’une collectivité. Un plan est structuré en axes, sous axes, actions et parfois sous actions. Le contenu peut être issu d’un PDF converti avec des artefacts de mise en page. Certaines rubriques comme budget, service pilote ou statut ne sont pas toujours explicites.

Objectif
Analyser le texte ci dessous et extraire toutes les actions, en reconstruisant la hiérarchie axe puis sous axe puis action, et en ajoutant des sous actions si nécessaire. Axes, sous axes et actions sont obligatoires. Les sous actions sont optionnels.

Sortie attendue
1 Répondre uniquement avec un tableau JSON valide
2 Ne rien ajouter avant ni après le JSON
3 Ne pas utiliser de balises Markdown

Schéma des objets du tableau
Chaque entrée du tableau est un objet avec exactement ces champs
[
 "axe",
 "sous-axe",
 "titre",
 "description",
 "sous-actions",
 "direction ou service pilote",
 "personne pilote",
 "budget",
 "statut"
]

Types et formats attendus
• "axe" est une chaîne
• "sous-axe" est une chaîne
• "titre" est une chaîne
• "description" est une chaîne
• "sous-actions" est une liste de chaînes. Si aucune sous action ne s’impose, mettre une liste vide []
• "direction ou service pilote" est une chaîne
• "personne pilote" est une chaîne
• "budget" est soit la valeur vide "", soit un entier sans séparateur d’espace
• "statut" est une chaîne

Définitions opérationnelles
• Plan. Ensemble structuré d’orientations et de mesures d’une collectivité
• Axe. Grande orientation stratégique du plan. Exemple "Vers une mobilité vertueuse et réfléchie"
• Sous axe. Déclinaison thématique d’un axe. Exemple "Mettre en œuvre les conditions favorables à des déplacements plus sobres"
• Action. Mesure opérationnelle unique qui peut être mise en œuvre et suivie. Elle a un titre court et une description synthétique
• Sous action. Etape ou brique concrète qui détaille la mise en œuvre d’une action. Les sous actions sont listées dans "sous-actions"

Hiérarchie et numérotation
1 Conserver strictement les libellés exacts du texte source lorsque la numérotation et les titres existent
2 Lorsque le texte ne fournit pas de numérotation explicite, construire une numérotation stable et cohérente selon la règle suivante
   On note les axes "n".
   On note les sous axes "n.X".
   On note les actions "n.X.Y"
3 "axe" doit être formaté exactement "Axe n : Titre de l’axe"
4 "sous-axe" doit être formaté exactement "n.X  Titre du sous-axe"
6 "titre" doit être formaté "n.X.Y Titre de l’action"
7 Un sous axe doit avoir un nom complet. Il ne peut pas être uniquement un nombre
8 Pour un même identifiant hiérarchique le libellé doit être identique partout

Tâches obligatoires et ordre d’exécution
1 Normalisation du texte source
   • Retirer uniquement les artefacts manifestes de conversion comme "Unnamed" ou des mots isolés insérés au milieu d’une phrase
   • Conserver l’orthographe et les majuscules des noms propres et sigles
2 Relevé de structure
   • Repérer les axes puis les sous axes
3 Extraction des actions
   • Lister chaque action avec un titre court et une description synthétique fidèle au texte
   • Lorsque le texte présente des puces, des sous parties ou des verbes d’exécution multiples rattachés à une même action, créer des sous actions dans "sous-actions" comme une liste de chaînes
4 Rattachement hiérarchique
   • Associer chaque action à son sous axe et à son axe
5 Complétude des champs
   • Remplir "direction ou service pilote", "personne pilote", "budget" et "statut" uniquement si l’information est explicite et non ambiguë
6 Validation du format
   • Produire un JSON valide
   • Vérifier que chaque objet contient exactement les champs définis
   • Si une information manque, la laisser à "" sauf "sous-actions" qui doit être une liste vide et "budget" qui doit être "" ou un entier
7 Dé duplication
   • Si deux entrées décrivent la même action, conserver une seule entrée avec la description la plus complète
8 Couverture
   • Parcourir tout le texte fourni et extraire l’ensemble des actions identifiables

Règles générales
1 Ne jamais inventer des informations ou des chiffres
2 Ne pas réécrire le sens de la "description". La nettoyer uniquement pour supprimer des artefacts évidents
3 "statut" ne peut prendre que l’une des valeurs suivantes sinon ""
   ["À venir", "À discuter", "En cours", "Réalisé", "En retard", "En pause", "Bloqué"]
4 "direction ou service pilote" contient uniquement des organismes ou services. "personne pilote" contient uniquement des noms de personnes
5 Majuscules. Mettre une majuscule au premier mot de chaque champ texte. Conserver les majuscules des noms propres et des sigles. Supprimer les espaces superflus au début et à la fin
6 Respect strict des libellés existants pour axes et sous axes lorsque fournis. En l’absence de libellé explicite, créer un libellé concis et fidèle au contenu
7 Ordre de tri. Le tableau doit être trié selon la hiérarchie axe puis sous axe puis ordre des actions

Exemples de bonne structure de plan
Exemple de titres hiérarchiques attendus quand le texte les fournit
Axe 1 : Une transition construite de manière transversale
1.1 S’appuyer sur un pilotage et des coopérations stables
1.1.1 Définir un portage politique fort
1.2 Impliquer tous les publics dans les transitions
Axe 2 : Vers un territoire rural affirmé aux multiples atouts en faveur du climat
2.1 Soutenir une agriculture paysanne
Axe 3 : Vers des équipements de qualité thermique et écologique
3.1 Concevoir des bâtiments publics de qualité une normalité
Axe 4 : Vers une mobilité vertueuse et réfléchie
4.2 Mettre en œuvre les conditions favorables à des déplacements plus sobres

Exemple de bonne extraction avec sous actions
Texte source
"Réduire l’autosolisme. Développer la pratique du covoiturage en s’appuyant tout d’abord sur des services existants mais aussi en mettant en place des infrastructures permettant de diversifier les offres
• S’appuyer sur l’offre existante proposée par Blablacar Daily pour le covoiturage domicile travail
• Déployer des lignes de covoiturage à haut niveau de service et les aménagements associés
• Réfléchir à des solutions d’autopartage en boucle"

Extraction attendue pour une action située dans le sous axe "4.2 Mettre en œuvre les conditions favorables à des déplacements plus sobres"
{
 "axe": "Axe 4  Vers une mobilité vertueuse et réfléchie",
 "sous-axe": "4.2  Mettre en œuvre les conditions favorables à des déplacements plus sobres",
 "titre": "4.2.1 Réduire l’autosolisme",
 "description": "Développer la pratique du covoiturage en s’appuyant sur des services existants et en mettant en place des infrastructures qui diversifient l’offre",
 "sous-actions": [
   "S’appuyer sur l’offre existante proposée par Blablacar Daily pour le covoiturage domicile travail",
   "Déployer des lignes de covoiturage à haut niveau de service et les aménagements associés",
   "Réfléchir à des solutions d’autopartage en boucle"
 ],
 "direction ou service pilote": "",
 "personne pilote": "",
 "budget": "",
 "statut": ""
}

Précisions sur le nettoyage minimal
• Retirer les mentions "Unnamed"
• Corriger les espaces multiples
• Conserver la ponctuation et les capitales des noms propres et sigles
• Ne pas corriger l’orthographe sauf artefacts de conversion manifestes

Consignes de saisie de champs
1 "direction ou service pilote" et "personne pilote" doivent contenir uniquement le nom de l’entité ou de la personne sans préposition. Exemple "SNCF" et non "Avec la SNCF"
2 **En cas de pluralité d’entités pour "direction ou service pilote" et/ou "personne pilote", les lister séparées par une virgule et un espace**
3 "budget" ne doit contenir que des chiffres sans séparateur ou la valeur vide
4 Si "statut" n’est pas exactement dans la liste autorisée, laisser ""

Rappel de robustesse
• Si le document fournit des numérotations et des titres, les réutiliser strictement
• Si des titres existent sans numéro, générer des numéros cohérents et stables
• Si la position d’une action parmi plusieurs sous axes demeure ambiguë, laisser vides les champs d’appartenance incertains plutôt que de forcer un rattachement

Jusqu’à présent, le prompt décrivait les règles générales d’extraction. Si le champ suivant n’est pas vide, vous devez impérativement tenir compte des précisions spécifiques ci-dessous.  
Elles peuvent modifier ou affiner l’interprétation de la structure du plan. Elles prévalent sur les règles générales lorsqu’il existe une contradiction ou une ambiguïté.
--- Précisions spécifiques (à appliquer strictement si présentes) ---
{precisions}
--- Fin des précisions spécifiques ---


Voici le texte à analyser :
{texte_pdf_a_analyser}  
"""

# Prompt de vérification 1 : vérifie la qualité de l'extraction
prompt_verif_1 = """
Tu es un agent de validation d’extractions documentaires extrêmement strict.

Contexte
Le document source accessible plus bas est un plan d’action.
Une première IA a déjà extrait une série d’actions. 

Structure attendue des actions
Les actions sont repérables car elles commencent par un identifiant numérique du type :
1.1.1 Titre de l’action; Description; Sous actions; Direction ou service pilote; Statut; Budget; Personne pilote; etc.
Tout ce qui suit une action appartient à cette action jusqu’au prochain identifiant du même type ou la fin du texte.

Objectif
1 Tu dois identifier chaque action dans le texte fourn
2 Pour chaque action, parcourir le document source via le file search.
3 Retrouver le passage correspondant à cette action dans le plan d’action.
4 Vérifier la fidélité de l’extraction pour cette action.
5 Attribuer un score de confiance entre 0 et 100 pour chaque identifiant d’action.

Critères de jugement
Tu dois juger uniquement sur
• omissions de texte significatives
• reformulations textuelles (changement de vocabulaire ou de structure de phrase)
Les ajouts de vocabulaire non présents dans le texte source sont considérés comme des reformulations.

Règles de notation
Tu dois attribuer pour chaque action un score entier entre 0 et 100, noté score, qui reflète la fidélité au texte source.

Guides de notation
• 100  texte quasi identique au texte source, aucune information manquante ni reformulation significative
• 90 à 99  quelques reformulations légères, aucun changement de sens, pas d’omission d’information importante
• 70 à 89  plusieurs reformulations ou petites omissions, mais le sens global reste correct
• 30 à 69  omissions importantes et ou nombreuses reformulations qui altèrent le texte
• 1 à 29  action très éloignée du contenu du document source
• 0  action hors sujet ou ne correspondant pas au document source

Changement de sens
• Si tu détectes un changement de sens, même partiel, le score doit chuter fortement en dessous de 70.
• Si le sens est largement incorrect ou trompeur, le score doit être inférieur ou égal à 30.

Contraintes pour le score
• Le score doit être un entier compris entre 0 et 100.
• Si le calcul te conduirait en dehors de ces bornes, ramène systématiquement le score dans l’intervalle.
• La notation doit suivre l’esprit du barème ci dessus et être stricte.

Format de sortie
Tu dois répondre uniquement avec un objet JSON strict représentant un dictionnaire :
• Les clés sont les identifiants des actions, sous forme d'un int qui se trouve entre les | au début du titre (exemple : 12)
• Les valeurs sont des objets contenant :
    - un entier entre 0 et 100 représentant le score de confiance
    - une explication très courte (quelques mots maximum) uniquement si le score est strictement inférieur à 90
    - si le score est supérieur ou égal à 90, l’explication doit être une chaîne vide ""

Exemples d’explications acceptables :
"omissions partielles"
"reformulation légère"
"altération mineure du sens"
"omissions + reformulation"

Exemple de format attendu :
{{
  "1": {{ "score": 95, "explication": "" }},
  "2": {{ "score": 82, "explication": "omissions partielles" }}
}}

Contraintes supplémentaires
• Ne pas recopier de longs extraits du document source.
• Ne pas citer le texte du plan.
• Ne pas ajouter de commentaires, d’explications ou de texte en dehors du JSON.
• Ne pas ajouter d’autres clés que les identifiants des actions.

Voici le texte extrait par l'IA : 
{reponse_ia}

Voici le texte original : 
{texte_pdf_a_analyser}
"""

# Prompt d'amélioration : améliore les actions à faible score
prompt_upgrade_1 = """
Vous êtes un agent d’extraction documentaire spécialisé dans les plans d’actions de transition écologique des collectivités, y compris les PCAET.

Contexte
On vous fournit :
1) Une liste d’actions ciblées que l’on souhaite extraire ou corriger.
2) Le texte source complet du plan d’actions (issu d’un PDF parfois bruité).

Vous NE devez travailler QUE sur les actions explicitement listées ci dessous.

Actions ciblées à traiter
Ces actions sont données sous forme de titres d’actions :

-------- DEBUT LISTE --------
{actions_a_ameliorer}
--------- FIN LISTE ---------

Texte source du plan d’actions. Il peut y avoir des artefacts de mise en page.

--------- TEXTE SOURCE ---------
{texte_pdf_a_analyser}
--------- FIN TEXTE SOURCE ---------

Objectif
Pour chaque action présente dans la liste "Actions ciblées à traiter" :
1) Parcourir le texte source.
2) Retrouver l’action correspondante à partir de son titre.
3) Extraire tous ses attributs en respectant strictement le schéma JSON décrit ci dessous.

Schéma des objets du tableau
La sortie doit être un tableau JSON. Chaque élément du tableau est un objet contenant exactement les champs suivants pour chaque index :

"titre"
"description"
"sous-actions"

Exemple :

{
  "12": {
    "titre": "1.4.1 Animer et suivre le COT et la démarche de transition écologique",
    "description": "Assurer le suivi des actions pilotées par les collègues ou d'autres acteurs, animer le Comité de pilotage, et assurer la mobilisation des élus.",
    "sous-actions": [
      "sous_action_1",
      "sous_action_2",
      "sous_action_3"
    ]
  }
}

L'index est donnée entre les | dans la liste en entrée


Types et formats attendus
• "titre" est une chaîne de la forme "n.X.Y Titre de l’action" qui doit correspondre à l’une des actions listées
• "description" est une chaîne
• "sous-actions" est une liste de chaînes. Si aucune sous action ne s’impose, mettre []

Règles d’extraction spécifiques
1) Si l’information n’est pas explicitement présente dans le texte source, laisser ces champs à [] pour "sous-actions"
2) **SOYEZ COMPLETEMENT EXHAUSTIF SUR L'EXTRACTION NOTAMMENT DES DESCRIPTIONS ET SOUS-ACTIONS** 
3) Ne vous répétez pas entre les descriptions et les sous-actions, si certaines phrases s'apparentent à des sous-actions. Mettez les dans les sous-actions et non dans la description.

Nettoyage minimal
• Corriger les espaces multiples
• Retirer les artefacts manifestes ("Unnamed", numéros isolés sans sens, etc.)
• Ne pas réécrire le sens de la description, uniquement nettoyer les artefacts

Sortie attendue
1) Répondre uniquement avec un tableau JSON valide
2) Ne rien ajouter avant ni après le JSON
3) Ne pas utiliser de balises Markdown
4) Le tableau ne doit contenir QUE les actions demandées qui ont pu être retrouvées dans le texte source
"""


# Prompt de vérification qualitative finale
prompt_verif_quali = """
Vous êtes un auditeur qualité spécialisé dans les plans d’actions de transition écologique.

Contexte
On vous fournit une extraction déjà structurée avec les éléments suivants :
"axe", "sous-axe", "titre", "description", "sous-actions" et "direction ou service pilote", "personne pilote", "budget", "statut" s'ils sont disponibles.

Voici la sortie à évaluer
{reponse_ia}

Objectif
Votre travail n’est pas de corriger la sortie ni de la réécrire, mais de porter un jugement qualitatif sur sa qualité globale et de signaler les erreurs manifestes.

Axes d’évaluation
• Artefacts  vérifier qu’il ne subsiste pas d’artefacts évidents de conversion ou de mise en page comme "Unnamed", bouts de tableau, listes cassées, balises, répétitions absurdes, numérotations sans contenu.
• Cohérence sémantique  vérifier que chaque "description" et chaque "sous-action" a du sens, est compréhensible, et correspond à une action concrète de plan d’actions.
• Qualité des sous-actions  vérifier que les éléments de "sous-actions" sont bien des sous-actions opérationnelles ou des étapes de mise en œuvre
• Cohérence hiérarchique  vérifier que "axe", "sous-axe" et "titre" sont cohérents entre eux, que la numérotation est plausible et stable, et que le contenu de l’action correspond bien à son axe et sous-axe.
• Champs pilotage, budget, statut  vérifier que "direction ou service pilote", "personne pilote", "budget" et "statut" ne semblent pas inventés, sont utilisés seulement lorsque l’information est explicitement plausible, et restent vides sinon.
• Doublons et éclatement inutile  vérifier qu’il n’y a pas de doublons évidents d’actions et que les actions ne sont pas artificiellement éclatées en plusieurs entrées identiques.
• Vérifier que les directions ou service pilote et personnes pilotes, si pluriel, sont des listes séparées par une virgule et un espace. S'il y a des tirets qui semble séparer deux entités **distinctes**, le relever.

Format de réponse attendu
• Répondre en français, sous forme de quelques lignes de texte libre.
• Commencer par un court avis global sur la qualité de l’extraction, par exemple "Extraction globalement cohérente avec quelques points à surveiller".
• Si tout est satisfaisant, le préciser explicitement, par exemple "Aucun problème majeur détecté".
• S’il existe des problèmes manifestes, les mentionner de manière ciblée en citant systématiquement la numérotation de l’action concernée, c’est à dire la partie "n.x.y" du champ "titre".
  Exemple  "1.2.4  description trop générale et peu opérationnelle" ou "4.1.3  présence probable d’artefacts de mise en page".
• Ne pas réécrire les actions et ne pas proposer de nouvelle version en JSON.
• Ne pas dépasser une dizaine de lignes.

Précision
• C'est normal que les sous-actions soient mises l'une à la suite des autres par des ;
"""

def extract_text_from_pdf(pdf_file):
    """Extrait le texte d'un fichier PDF"""
    try:
        pdf_reader = PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Erreur lors de l'extraction du PDF : {str(e)}"

def extract_text_from_csv(csv_file):
    try:
        df = pd.read_csv(csv_file, sep=';').fillna('')

        text = "# Fichier CSV\n\n"
        text += f"**Dimensions :** {len(df)} lignes × {len(df.columns)} colonnes\n\n"
        text += f"**Colonnes :** {', '.join(df.columns)}\n\n"
        text += "**Contenu complet :**\n\n"

        raw = df.to_string(index=False)
        raw = re.sub(r'\s+', ' ', raw)  # compresse

        text += raw
        
        return text

    except Exception as e:
        return f"Erreur lors de la lecture du CSV : {str(e)}"

def df_to_compact_text(df: pd.DataFrame, show_index: bool = True) -> str:
    """Convertit un dataframe en texte compact pour l'envoyer à Gemini"""
    # Sécurité : on travaille sur une copie triée
    cols_expected = ["axe", "sous-axe"]
    for col in cols_expected:
        if col not in df.columns:
            raise ValueError(f"Colonne manquante dans le DataFrame : {col}")

    df_sorted = df.copy()
    df_sorted = df_sorted.sort_values(by=["axe", "sous-axe"]).reset_index(drop=True)

    parts = []

    # Petite fonction utilitaire pour gérer le séparateur
    def add_segment(segment: str):
        if not segment:
            return
        parts.append(segment.strip())

    for axe in df_sorted["axe"].dropna().unique():
        df_axe = df_sorted[df_sorted["axe"] == axe]

        # Présentation de l'axe (une seule fois)
        add_segment(f"{axe} :")

        for sous_axe in df_axe["sous-axe"].dropna().unique():
            df_sous_axe = df_axe[df_axe["sous-axe"] == sous_axe]

            # Présentation du sous axe (une seule fois)
            add_segment(f"Sous axe {sous_axe} :")

            for index_row, row in df_sous_axe.iterrows():
                champs_action = []

                # Titre
                titre = str(row.get("titre", "")).strip()
                if titre:
                    if show_index:
                        champs_action.append(f"| {index_row} | {titre}")
                    else:
                        champs_action.append(f"{titre}")

                # Description
                desc = str(row.get("description", "")).strip()
                if desc:
                    champs_action.append(f"{desc}")

                # Sous actions (liste ou chaîne)
                sous_actions = row.get("sous-actions", None)
                if isinstance(sous_actions, (list, tuple)):
                    sa_clean = [str(sa).strip() for sa in sous_actions if str(sa).strip()]
                    if sa_clean:
                        champs_action.append("" + "; ".join(sa_clean))
                elif isinstance(sous_actions, str) and sous_actions.strip():
                    champs_action.append(f"{sous_actions.strip()}")

                # Champs optionnels
                champs_optionnels = [
                    ("direction ou service pilote", "Direction ou service pilote"),
                    ("personne pilote", "Personne pilote"),
                    ("budget", "Budget"),
                    ("statut", "Statut"),
                ]

                for col, label in champs_optionnels:
                    if col in df_sous_axe.columns:
                        val = row.get(col, None)
                        if pd.notna(val):
                            val_str = str(val).strip()
                            if val_str:
                                champs_action.append(f"{label} {val_str}")

                # On ne garde l'action que si on a au moins un champ
                if champs_action:
                    # Une seule phrase par action, pour limiter les tokens
                    texte_action = "" + "; ".join(champs_action) + "."
                    add_segment(texte_action)

    # Construction finale du texte
    return "\n".join(parts).strip()

def parse_json_response(result_text: str):
    """Parse une réponse JSON de Gemini en nettoyant les balises markdown"""
    cleaned_text = result_text.strip()
    if cleaned_text.startswith("```json"):
        cleaned_text = cleaned_text[7:]
    if cleaned_text.startswith("```"):
        cleaned_text = cleaned_text[3:]
    if cleaned_text.endswith("```"):
        cleaned_text = cleaned_text[:-3]
    cleaned_text = cleaned_text.strip()
    return json.loads(cleaned_text)

def remplir_fichier_import(df: pd.DataFrame) -> io.BytesIO:
    """Remplit le fichier import avec les données du dataframe et retourne un BytesIO"""
    
    # 1 Charger le fichier source directement (sans copie sur disque)
    src = "utils/modele-import-pa.xlsx"
    wb = load_workbook(src)
    ws = wb["Fichier dimport"]

    # 2 Mapping des colonnes Excel (lettre → nom de colonne df)
    mapping = {
        "A": "axe",
        "B": "sous-axe",
        "D": "titre",
        "E": "description",
        "L": "direction ou service pilote",
        "M": "personne pilote",
        "W": "budget",
        "X": "statut"
    }

    # 3 Écrire les données à partir de la ligne 5
    start_row = 5

    for i, (_, row) in enumerate(df.iterrows(), start=start_row):
        for col_letter, df_col in mapping.items():
            value = row.get(df_col, "")
            ws[f"{col_letter}{i}"] = "" if pd.isna(value) else value

    # 4 Sauvegarder dans un BytesIO (en mémoire, pas sur disque)
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)

    return output

def display_df_markdown(df: pd.DataFrame):
    """Affiche un dataframe en mode structuré (axes > sous-axes > actions)"""
    # Affichage structuré par axes et sous-axes
    axes = df["axe"].unique()
    
    for axe in axes:
        st.markdown(f"### {axe}")
        
        df_axe = df[df["axe"] == axe]
        sous_axes = df_axe["sous-axe"].unique()
        
        for sous_axe in sous_axes:
            with st.expander(f"{sous_axe}", expanded=False):
                df_sous_axe = df_axe[df_axe["sous-axe"] == sous_axe]
                
                for _, action in df_sous_axe.iterrows():
                    # Afficher chaque action
                    action_md = ""
                    
                    # Titre
                    if action.get("titre") and str(action["titre"]).strip():
                        action_md += f"**Titre :** {action['titre']}\n\n"
                    
                    # Description
                    if action.get("description") and str(action["description"]).strip():
                        action_md += f"**Description :** {action['description']}\n\n"
                    
                    # Sous-actions (liste)
                    sous_actions = action.get("sous-actions", [])
                    if sous_actions and len(sous_actions) > 0:
                        action_md += "**Sous-actions :**\n"
                        for sa in sous_actions:
                            if sa and str(sa).strip():
                                action_md += f"- {sa}\n"
                        action_md += "\n"
                    
                    # Direction ou service pilote
                    if action.get("direction ou service pilote") and str(action["direction ou service pilote"]).strip():
                        action_md += f"**Direction ou service pilote :** {action['direction ou service pilote']}\n\n"
                    
                    # Personne pilote
                    if action.get("personne pilote") and str(action["personne pilote"]).strip():
                        action_md += f"**Personne pilote :** {action['personne pilote']}\n\n"
                    
                    # Budget
                    if action.get("budget") and str(action["budget"]).strip():
                        action_md += f"**Budget :** {action['budget']}\n\n"
                    
                    # Statut
                    if action.get("statut") and str(action["statut"]).strip():
                        action_md += f"**Statut :** {action['statut']}\n\n"
                    
                    st.markdown(action_md)
                    
                    # Affichage de la confiance dans un st.info
                    if "score" in action and action.get("score") is not None:
                        score = action["score"]
                        if action.get("amelioree", False):
                            # Action améliorée à l'étape 3
                            st.info(f"FA consolidée. (confiance précédente: **{score}**)")
                        else:
                            # Action non améliorée
                            explication = action.get("explication", "")
                            if explication and str(explication).strip():
                                st.info(f"Confiance: **{score}** - {explication}")
                            else:
                                st.info(f"Confiance: **{score}**")
                    
                    st.markdown("---")
    
    # Afficher aussi le dataframe en dessous pour référence
    st.markdown("#### ✅ Vue tableau")
    df_a_afficher = df.drop(columns=['score', 'explication', 'amelioree']).copy()
    st.dataframe(df_a_afficher, use_container_width=True, height=600)


async def query_gemini(user_prompt, model='gemini-3-pro-preview'):
    """Interroge Gemini avec streaming asynchrone"""
    start_time = time.time()
    print(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] ✨ Gemini START ({model})")
    try:
        # Utiliser le streaming pour la réponse
        stream = await gemini_client.aio.models.generate_content_stream(
            model=model,
            contents=user_prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,
                max_output_tokens=64000
            )
        )
        
        parts = []
        tokens = [0,0]
        last_chunk = None

        async for chunk in stream:
            if hasattr(chunk, 'text') and chunk.text:
                parts.append(chunk.text)
            last_chunk = chunk
        
        # Récupérer les tokens du dernier chunk
        if hasattr(last_chunk, 'usage_metadata') and hasattr(last_chunk.usage_metadata, 'candidates_token_count') and hasattr(last_chunk.usage_metadata, 'prompt_token_count'):
            tokens = [last_chunk.usage_metadata.candidates_token_count, last_chunk.usage_metadata.prompt_token_count]
        else:
            tokens = [0, 0]
        
        reponse = "".join(parts)
        elapsed = time.time() - start_time
        print(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] ✅ Gemini END ({elapsed:.1f}s, {tokens} tokens)")
        return reponse, elapsed, tokens

    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] ❌ Gemini ERROR: {str(e)}")
        # Si le streaming ne fonctionne pas, fallback sur l'API standard
        try:
            response = await gemini_client.aio.models.generate_content(
                model=model,
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    temperature=0.2,
                    max_output_tokens=64000
                )
            )
            elapsed = time.time() - start_time
            #Calcul des tokens
            if hasattr(response, 'usage_metadata') and hasattr(response.usage_metadata, 'candidates_token_count') and hasattr(response.usage_metadata, 'prompt_token_count'):
                tokens = [response.usage_metadata.candidates_token_count, response.usage_metadata.prompt_token_count]
            else:
                tokens = [0, 0]
            print(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] ✅ Gemini END (fallback) ({elapsed:.1f}s, {tokens[0]} tokens, {tokens[1]} tokens)")
            return str(response.text), elapsed, tokens
        
        except Exception as e2:
            elapsed = time.time() - start_time
            return f"Erreur Gemini: {str(e2)}", elapsed, [0, 0]


# ==========================
# Interface utilisateur
# ==========================

# Toggle pour le type de fichier
file_type = st.segmented_control(
    "Type de fichier à importer",
    options=["PDF", "CSV"],
    default="PDF"
)

# Titre dynamique
if file_type == "PDF":
    uploaded_file = st.file_uploader(
        "Glissez-déposez votre fichier PDF ici",
        type=['pdf'],
        help="Sélectionnez un fichier PDF à analyser",
        key="pdf_uploader"
    )
else:
    uploaded_file = st.file_uploader(
        "Glissez-déposez votre fichier CSV ici",
        type=['csv'],
        key="csv_uploader"
    )

precisions = st.text_area(
    "Précisions",
    height=300,
    placeholder="Ajoutez des précisions supplémentaires si nécessaire. Vous pouvez ici définir une strucutre spécifique, certaines règles à respecter, donner du contexte, etc. Cliquez sur Ctrl+Enter pour valider."
)

# Choix du modèle Gemini
# gemini_model = st.segmented_control(
# "Modèle Gemini",
# options=["gemini-3-pro-preview", "gemini-2.5-pro"],
# default="gemini-2.5-pro"
# )
gemini_model = "gemini-2.5-pro"

# Mode test (tronque le texte à 10 000 caractères)
# mode_test = st.toggle("🧪 Mode test (30 000 caractères max)", value=False)
mode_test = False

total_tokens_consumed = [0, 0]

if uploaded_file is not None:
    st.success(f"✅ Fichier chargé : {uploaded_file.name}")
    
    start_button = st.button("🚀 Lancer l'analyse", type="primary")
    
    if start_button:
        # Extraction selon le type de fichier
        if file_type == "PDF":
            with st.spinner("📖 Extraction du texte du PDF..."):
                extracted_text = extract_text_from_pdf(uploaded_file)
        else:
            with st.spinner("🔍 Lecture du fichier CSV..."):
                extracted_text = extract_text_from_csv(uploaded_file)
        
        if extracted_text and not extracted_text.startswith("Erreur"):
            st.success(f"✅ Texte extrait : {len(extracted_text)} caractères")
            
            # Tronquer le texte en mode test
            if mode_test and len(extracted_text) > 30000:
                extracted_text = extracted_text[:30000]
                st.warning(f"🧪 Mode test activé : texte tronqué à 30 000 caractères")

            # ========================================
            # ÉTAPE 1 : Extraction initiale
            # ========================================
            st.markdown("---")
            st.markdown("## 🪄 Étape 1 : Définition de la structure et créations des fiches actions")
            
            user_prompt = custom_prompt.replace("{precisions}", precisions).replace("{texte_pdf_a_analyser}", extracted_text)

            with st.spinner("🌀 Étape 1/4 : Définition de la structure et créations des fiches actions..."):
                gemini_result, elapsed_time, tokens_count = asyncio.run(query_gemini(user_prompt, gemini_model))
                total_tokens_consumed[0] += tokens_count[0]
                total_tokens_consumed[1] += tokens_count[1]
                st.info(f"✨ Extraction : {elapsed_time:.1f}s | Entrée : {tokens_count[1]:,} tokens | Sortie : {tokens_count[0]:,} tokens")
            
            if gemini_result and not gemini_result.startswith("Erreur"):
                try:
                    # Parser le JSON et créer le dataframe
                    data = parse_json_response(gemini_result)
                    df_actions = pd.DataFrame(data)
                    st.success(f"✅ {len(df_actions)} actions extraites")
                    st.dataframe(df_actions, use_container_width=True, height=400)
                    
                    # ========================================
                    # ÉTAPE 2 : Vérification des scores
                    # ========================================
                    st.markdown("---")
                    st.markdown("## 🔍 Étape 2 : Vérification de la qualité des fiches actions")
                    
                    reponse_ia = df_to_compact_text(df_actions)
                    user_prompt_verif = prompt_verif_1.replace("{texte_pdf_a_analyser}", extracted_text).replace("{reponse_ia}", reponse_ia or "")
                    
                    with st.spinner("🌀 Étape 2/4 : Vérification de la qualité des fiches actions..."):
                        verif_result, elapsed_time, tokens_count = asyncio.run(query_gemini(user_prompt_verif, gemini_model))
                        total_tokens_consumed[0] += tokens_count[0]
                        total_tokens_consumed[1] += tokens_count[1]
                        st.info(f"✨ Vérification : {elapsed_time:.1f}s | Entrée : {tokens_count[1]:,} tokens | Sortie : {tokens_count[0]:,} tokens")
                    
                    if verif_result and not verif_result.startswith("Erreur"):
                        try:
                            # ========================================
                            # ÉTAPE 3 : Ajout des scores au dataframe
                            # ========================================
                            scores_data = parse_json_response(verif_result)
                            
                            # Ajouter les colonnes score, explication et amelioree
                            df_actions["score"] = None
                            df_actions["explication"] = ""
                            df_actions["amelioree"] = False
                            
                            for idx_str, score_info in scores_data.items():
                                idx = int(idx_str)
                                if idx < len(df_actions):
                                    df_actions.at[idx, "score"] = score_info.get("score")
                                    df_actions.at[idx, "explication"] = score_info.get("explication", "")
                            
                            st.success(f"✅ Scores ajoutés pour {len(scores_data)} actions")
                            st.dataframe(df_actions[["titre", "score", "explication"]], use_container_width=True, height=300)
                            
                            # ========================================
                            # ÉTAPE 4 : Amélioration des actions à faible score
                            # ========================================
                            st.markdown("---")
                            st.markdown("## 🔧 Étape 3/4 : Consolidation des fiches actions")
                            
                            # Sélectionner les actions avec score < 90
                            df_low_score = df_actions[df_actions["score"] < 90].copy()
                            
                            if len(df_low_score) > 0:
                                st.warning(f"⚠️ {len(df_low_score)} actions avec un score < 90 à améliorer")
                                
                                # Découper en batches de max 5 actions
                                BATCH_SIZE = 5
                                low_score_indices = list(df_low_score.index)
                                batches = [low_score_indices[i:i + BATCH_SIZE] for i in range(0, len(low_score_indices), BATCH_SIZE)]
                                
                                if len(batches) > 1:
                                    st.info(f"📦 Envoi de {len(batches)} batchs en parallèle à l'IA pour consolidation")
                                else:
                                    st.info(f"📦 Envoi de {len(batches)} batch(s) en parallèle à l'IA pour consolidation")
                                
                                # Créer les prompts pour chaque batch
                                batch_prompts = []
                                for batch_indices in batches:
                                    actions_a_ameliorer = ""
                                    for idx in batch_indices:
                                        row = df_actions.loc[idx]
                                        actions_a_ameliorer += f"|{idx}| {row['titre']}\n"
                                    
                                    batch_prompt = prompt_upgrade_1.replace("{texte_pdf_a_analyser}", extracted_text).replace("{actions_a_ameliorer}", actions_a_ameliorer)
                                    batch_prompts.append(batch_prompt)
                                
                                # Fonction async pour exécuter tous les batches en parallèle
                                async def run_upgrade_batches():
                                    tasks = [query_gemini(prompt, gemini_model) for prompt in batch_prompts]
                                    return await asyncio.gather(*tasks, return_exceptions=True)
                                
                                with st.spinner(f"🌀 Étape 3 : Consolidation des fiches actions ({len(batches)} batches en parallèle)..."):
                                    batch_results = asyncio.run(run_upgrade_batches())
                                
                                # Traiter les résultats de tous les batches
                                total_upgraded = 0
                                max_time = 0  # Renommer en max_time
                                total_tokens = [0,0]
                                all_errors = []
                                
                                for batch_idx, result in enumerate(batch_results):
                                    if isinstance(result, Exception):
                                        all_errors.append(f"Batch {batch_idx + 1}: {str(result)}")
                                        continue
                                    
                                    upgrade_result, elapsed_time, tokens_count = result
                                    max_time = max(max_time, elapsed_time)  # Prendre le max
                                    total_tokens[0] += tokens_count[0]
                                    total_tokens[1] += tokens_count[1]
                                    
                                    if upgrade_result and not upgrade_result.startswith("Erreur"):
                                        try:
                                            # ========================================
                                            # ÉTAPE 5 : Mise à jour du dataframe
                                            # ========================================
                                            upgrade_data = parse_json_response(upgrade_result)
                                            
                                            # Mettre à jour les champs titre, description, sous-actions
                                            # Format: {"12": {"titre": "...", "description": "...", "sous-actions": [...]}}
                                            for idx_str, item in upgrade_data.items():
                                                idx = int(idx_str)
                                                if idx < len(df_actions):
                                                    if "titre" in item:
                                                        df_actions.at[idx, "titre"] = item["titre"]
                                                    if "description" in item:
                                                        df_actions.at[idx, "description"] = item["description"]
                                                    if "sous-actions" in item:
                                                        df_actions.at[idx, "sous-actions"] = item["sous-actions"]
                                                    # Marquer l'action comme améliorée
                                                    df_actions.at[idx, "amelioree"] = True
                                                    total_upgraded += 1
                                        except Exception as e:
                                            all_errors.append(f"Batch {batch_idx + 1}: Parsing error - {str(e)}")
                                    else:
                                        all_errors.append(f"Batch {batch_idx + 1}: {upgrade_result}")
                                
                                # Afficher le résumé
                                total_tokens_consumed[0] += total_tokens[0]
                                total_tokens_consumed[1] += total_tokens[1]
                                st.info(f"✨ Consolidation : {max_time:.1f}s total | Entrée : {total_tokens[1]:,} tokens | Sortie : {total_tokens[0]:,} tokens")
                                
                                if total_upgraded > 0:
                                    st.success(f"✅ {total_upgraded} actions consolidées")
                                
                                if all_errors:
                                    for error in all_errors:
                                        st.error(f"❌ {error}")
                            else:
                                st.success("✅ Toutes les actions ont un score > 90, pas de consolidation nécessaire")
                            
                            # ========================================
                            # ÉTAPE 6 : Vérification qualitative finale
                            # ========================================
                            st.markdown("---")
                            st.markdown("## ✅ Étape 4 : Vérifications finales")
                            
                            # Nettoyage des colonnes : remplacer "/" par ", "
                            for col in ["direction ou service pilote", "personne pilote"]:
                                if col in df_actions.columns:
                                    df_actions[col] = df_actions[col].apply(
                                        lambda x: x.replace("/", ", ") if isinstance(x, str) else x
                                    )
                            
                            # Nettoyage des doubles espaces
                            for col in df_actions.columns:
                                df_actions[col] = df_actions[col].apply(
                                    lambda x: re.sub(r' +', ' ', x).strip() if isinstance(x, str) else x
                                )
                            
                            st.success("✅ Nettoyage effectué des colonnes pilotes")
                            
                            reponse_ia_finale = df_to_compact_text(df_actions, show_index=False)
                            user_prompt_quali = prompt_verif_quali.replace("{reponse_ia}", reponse_ia_finale or "")
                            
                            with st.spinner("🌀 Étape 4/4 : Analyse qualitative finale..."):
                                quali_result, elapsed_time, tokens_count = asyncio.run(query_gemini(user_prompt_quali, gemini_model))
                                total_tokens_consumed[0] += tokens_count[0]
                                total_tokens_consumed[1] += tokens_count[1]
                                st.info(f"✨ Vérifications finales : {elapsed_time:.1f}s | Entrée : {tokens_count[1]:,} tokens | Sortie : {tokens_count[0]:,} tokens")
                            
                            # ========================================
                            # ÉTAPE 7 : Affichage final
                            # ========================================
                            st.markdown("---")
                            st.markdown("## ✨ Plan final")
                            
                            # Afficher le résultat de la vérification qualitative
                            st.markdown(f"**Avis de l'IA** \n\n {quali_result}")

                            st.success(f"✅ Import réussi pour un cout d'environ {(10*total_tokens_consumed[0] + 2*total_tokens_consumed[1])/1000000:.2f} €")
                            
                            # Afficher le dataframe final en markdown
                            display_df_markdown(df_actions)

                            # Remplir le fichier import et proposer le téléchargement
                            try:
                                excel_data = remplir_fichier_import(df_actions)
                                
                                st.download_button(
                                    label="📥 Télécharger le fichier d'import rempli au format Excel",
                                    data=excel_data,
                                    file_name="import_plan_actions_" + pd.Timestamp.now().strftime('%Y%m%d_%H%M%S') + ".xlsx",
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                    type="primary"
                                )
                            except Exception as e:
                                st.error(f"❌ Erreur lors du remplissage du fichier import : {str(e)}")
                            
                        except Exception as e:
                            st.error(f"❌ Erreur lors du parsing des scores : {str(e)}")
                            st.text(verif_result)
                    else:
                        st.error(f"❌ Erreur lors de la vérification : {verif_result}")
                        
                except Exception as e:
                    st.error(f"❌ Erreur lors du parsing de l'extraction : {str(e)}")
                    st.text(gemini_result)
            else:
                st.error(f"❌ Erreur lors de l'extraction : {gemini_result}")
                
        
        else:
            st.error(f"❌ Erreur lors de l'extraction du texte du {file_type}")
            st.error(extracted_text)
else:
    st.info(f"👆 Veuillez charger un fichier {file_type} pour commencer")

