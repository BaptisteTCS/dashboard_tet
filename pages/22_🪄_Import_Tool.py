import streamlit as st
from google import genai
from google.genai import types
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from pypdf import PdfReader
import asyncio
import hashlib
import os
import io
import time
import traceback
from datetime import datetime
from pathlib import Path
import json
import pandas as pd
import re
import nest_asyncio
import pandas as pd
from openpyxl import load_workbook
from openai import AsyncOpenAI
nest_asyncio.apply()

# ID du dossier Google Drive de destination pour les fichiers d'import générés
DRIVE_FOLDER_ID = "1wu0jAgxrkPRUm3uDjcgZvCSVwgUVkbCG"

st.set_page_config(layout="wide")
st.title("✨ Import Tool :blue-badge[:material/experiment: Beta]")

# Colonnes optionnelles dont on peut activer/désactiver le remplissage par l'IA.
# Format : (label affiché, nom de colonne dans le DataFrame, clé JSON utilisée
# dans le prompt d'enrichissement des sous-actions)
TOGGLABLE_COLUMNS = [
    ("Description", "description", "description"),
    ("Objectifs", "objectifs", None),
    ("Structure pilote", "structure pilote", None),
    ("Direction ou service pilote", "direction ou service pilote", None),
    ("Personne pilote", "personne pilote", "personne_pilote"),
    ("Budget", "budget", None),
    ("Statut", "statut", "statut"),
    ("Date de début", "date de début", "date_debut"),
    ("Date de fin", "date de fin", "date_fin"),
]

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
 "objectifs",
 "structure pilote",
 "direction ou service pilote",
 "personne pilote",
 "budget",
 "statut"
]

Types et formats attendus
• "axe" est une chaîne
• "sous-axe" est une chaîne
• "titre" est une chaîne courte (300 caractères maximum). Si le titre issu du texte source dépasse 300 caractères, conserver uniquement les 300 premiers caractères significatifs dans "titre" et reporter le reste dans "description"
• "description" est une chaîne
• "sous-actions" est une liste de chaînes. Si aucune sous action ne s’impose, mettre une liste vide []
• "objectifs" est une chaîne. Reprendre fidèlement le contenu du champ "Objectifs" du document source si présent (par exemple "Préserver la qualité et la diversité des productions agricoles"). Si l'information n'est pas explicitement présente, laisser ""
• "structure pilote" est une chaîne. Une ou plusieurs structures (organisme englobant : la collectivité elle-même, ou par exemple "Chambre d'agriculture", "DDT", etc.) séparées par ", ". Distinct de "direction ou service pilote" qui est interne à la structure. Si l'information n'est pas explicitement présente, laisser ""
• "direction ou service pilote" est une chaîne
• "personne pilote" est une chaîne
• "budget" est soit la valeur vide "", soit un entier sans séparateur d’espace
• "statut" est une chaîne

Définitions opérationnelles
• Plan. Ensemble structuré d’orientations et de mesures d’une collectivité
• Axe. Grande orientation stratégique du plan. Exemple "Vers une mobilité vertueuse et réfléchie"
• Sous axe. Déclinaison thématique d’un axe. Exemple "Mettre en œuvre les conditions favorables à des déplacements plus sobres"
• Action. Mesure opérationnelle unique qui peut être mise en œuvre et suivie. Elle a un titre court et, uniquement si nécessaire, une description synthétique apportant des informations complémentaires au titre
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
   • Remplir "objectifs", "structure pilote", "direction ou service pilote", "personne pilote", "budget" et "statut" uniquement si l’information est explicite et non ambiguë. "objectifs" et "structure pilote" sont des champs facultatifs : ne pas inventer, laisser "" en l'absence d'information explicite
   • Lorsque le texte présente pour une action des dates ou un calendrier (sans libellé de statut explicite pour cette action), vous pouvez déduire « statut » uniquement parmi « À venir » et « En cours » en vous appuyant sur ces dates et la date du jour ({date_du_jour}). Si seule une année est mentionnée sans mois précis (par exemple "2026"), considérer le statut comme « En cours » si cette année correspond à l'année actuelle, et « À venir » si elle est dans le futur
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
4 bis Distinction entre "structure pilote" et "direction ou service pilote" :
   • "structure pilote" est l'organisme global englobant (ex. la collectivité, "Chambre d'agriculture", "DDT", "Communauté de communes X").
   • "direction ou service pilote" est l'entité interne à cette structure (ex. "Service urbanisme", "Service économique", "Direction de la transition écologique").
   • Exemple : si le document indique "Service urbanisme de la Collectivité X", alors "structure pilote" = "Collectivité X" et "direction ou service pilote" = "Service urbanisme".
   • Si une seule des deux informations est présente, ne remplir que ce champ et laisser l'autre à "".
5 Majuscules. Mettre une majuscule au premier mot de chaque champ texte. Conserver les majuscules des noms propres et des sigles. Supprimer les espaces superflus au début et à la fin
6 Respect strict des libellés existants pour axes et sous axes lorsque fournis. En l’absence de libellé explicite, créer un libellé concis et fidèle au contenu
7 Ordre de tri. Le tableau doit être trié selon la hiérarchie axe puis sous axe puis ordre des actions
8 "titre" et "description" ne doivent jamais contenir les mêmes informations. La description apporte un complément au titre. Si le titre suffit à décrire l’action et qu’il n’y a rien de pertinent à ajouter, laisser "description" à ""
9 Ne recopie pas les objectifs dans les descriptions. S'il n'y a pas de description et seulement des objectifs, les mettre dans le champ "objectifs"
10 Ne jamais nommer un axe avec "plan d'action", si tu detected qu'un axe qui est a priori le titre du plan, alors tu passes les sous-axes comme axe.
11 Ne pas remplir les sous-axes et les fiches actions avec le même titre. Et de meme ne pas remplir les axes et sous-axes avec le meme titre. Soit il y a un titre différent, soit il y a une hiérarchie à changer. Si vraiment on doit passer d'axe directement à action, il est préférable d'inventer des sous-axes cohérents, proche de la réalité, pour ne pas reprendre le titre de l'axe dans le sous-axe.
12 Toujours numéroter dans l'ordre, même si le document original dévie.
13 Les titres des sous-action (et actions) sont en général court, tous le reste va dans la description. Par exemple on ne liste pas les objectifs et la gouvernance dans le titre.
14 Mettre les objectifs dans le champ "objectifs" et non dans la description. Si la description est vide, mettre "A compléter".
15 Si le plan a sa propre numérotation et qu'elle est cohérente, utiliser cette numérotation pour les axes, sous-axes et actions.

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
• Réfléchir à des solutions d’autopartage en boucle. 
Budget de 24000€ pour cette action en cours menée par Jean Dupoint du Service mobilité, piloté par la DDT, qui a pour but de rendre la pratique du covoiturage plus courante."

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
 "objectifs": "Rendre la pratique du covoiturage plus courante",
 "structure pilote": "DDT",
 "direction ou service pilote": "Service mobilité",
 "personne pilote": "Jean Dupoint",
 "budget": "24000",
 "statut": "En cours"
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

--- Consignes spécifiques IMPORTANTES (à appliquer strictement si présentes) qui prennent le dessus sur les règles générales ---
{precisions}
--- Fin des consignes spécifiques IMPORTANTES ---


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
1 Tu dois identifier chaque action dans le texte fourni
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
Ces actions sont données sous forme de titres d'actions :

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
• "titre" est une chaîne de la forme "n.X.Y Titre de l'action" qui doit correspondre à l’une des actions listées. Le titre ne doit pas dépasser 300 caractères. Si le titre issu du texte source dépasse 300 caractères, conserver uniquement les 300 premiers caractères significatifs dans "titre" et reporter le reste dans "description"
• "description" est une chaîne
• "sous-actions" est une liste de chaînes. Si aucune sous action ne s’impose, mettre []

Règles d’extraction spécifiques
1) Si l’information n’est pas explicitement présente dans le texte source, laisser ces champs à [] pour "sous-actions"
2) **SOYEZ COMPLETEMENT EXHAUSTIF SUR L'EXTRACTION NOTAMMENT DES DESCRIPTIONS ET SOUS-ACTIONS** 
3) Ne vous répétez pas entre les descriptions et les sous-actions, si certaines phrases s'apparentent à des sous-actions. Mettez les dans les sous-actions et non dans la description.
4) Le titre et la description ne doivent JAMAIS contenir les mêmes informations. La description ne doit apporter que des informations complémentaires au titre. Si le titre est suffisant, laisser "description" à "".

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
"axe", "sous-axe", "titre", "titre de la sous-action", "description", "objectifs", "structure pilote", "direction ou service pilote", "personne pilote", "budget", "statut", "date de début", "date de fin" s'ils sont disponibles.
Les actions classiques ont "titre" rempli. Les sous-actions apparaissent comme des lignes séparées marquées [SA], avec "titre" vide et "titre de la sous-action" rempli.

Voici la sortie à évaluer
{reponse_ia}

Objectif
Votre travail n’est pas de corriger la sortie ni de la réécrire, mais de porter un jugement qualitatif sur sa qualité globale et de signaler les erreurs manifestes.

Axes d’évaluation
• Artefacts  vérifier qu’il ne subsiste pas d’artefacts évidents de conversion ou de mise en page comme "Unnamed", bouts de tableau, listes cassées, balises, répétitions absurdes, numérotations sans contenu.
• Cohérence sémantique  vérifier que chaque "description" a du sens, est compréhensible, et correspond à une action ou sous-action concrète de plan d’actions.
• Qualité des sous-actions  vérifier que les lignes marquées [SA] sont bien des sous-actions opérationnelles ou des étapes de mise en œuvre
• Cohérence hiérarchique  vérifier que "axe", "sous-axe" et "titre" sont cohérents entre eux, que la numérotation est plausible et stable, et que le contenu de l’action correspond bien à son axe et sous-axe.
• Champs pilotage, budget, statut  vérifier que "objectifs", "structure pilote", "direction ou service pilote", "personne pilote", "budget" et "statut" ne semblent pas inventés, sont utilisés seulement lorsque l’information est explicitement plausible, et restent vides sinon. Pour "structure pilote" et "direction ou service pilote", vérifier que la distinction est respectée (structure = organisme englobant, direction/service = entité interne).
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
• Les sous-actions apparaissent comme des lignes à part entière, avec "titre" vide et "titre de la sous-action" rempli.
• Les actions classiques ont "titre" rempli et "titre de la sous-action" vide.
"""

prompt_enrich_sous_actions = """
Vous êtes un agent d'enrichissement documentaire spécialisé dans les plans d'actions de transition écologique des collectivités, y compris les PCAET.

Contexte
On vous fournit :
1) Une liste numérotée de sous-actions, chacune rattachée à son action parente (indiquée entre crochets pour le contexte).
2) Le texte source complet du plan d'actions (issu d'un PDF parfois bruité).

Objectif
Pour chaque sous-action de la liste ci-dessous, parcourir le texte source et extraire les informations suivantes si elles sont explicitement présentes dans le document :
• "description" : une description synthétique et fidèle au texte source de la sous-action
• "personne_pilote" : le nom de la personne pilote ou référente de la sous-action.
• "statut" : le statut de la sous-action
• "date_debut" : la date de début
• "date_fin" : la date de fin ou échéance

Valeurs autorisées pour "statut"
["À venir", "À discuter", "En cours", "Réalisé", "En retard", "En pause", "Bloqué"]
Si le statut trouvé ne correspond à aucune de ces valeurs exactes, laisser "".

Règles strictes
1 Aucun champ n'est obligatoire. Si l'information n'est pas explicitement présente dans le texte source, laisser une chaîne vide "".
2 Ne jamais inventer d'informations, de dates ou de statuts.
3 Les dates doivent être au format JJ/MM/AAAA. Si seule l'année est disponible, utiliser 01/01/AAAA. Si seuls le mois et l'année sont disponibles, utiliser 01/MM/AAAA.
4 La description doit être fidèle au texte source. Ne pas réécrire le sens, uniquement nettoyer les artefacts de conversion.
5 Le titre de l'action parente entre crochets sert uniquement de contexte pour localiser la sous-action dans le document. Ne pas le reproduire dans la description.
6 Si une sous-action est trop générique ou introuvable dans le texte source, laisser tous les champs à "".
7 Une personne pilote doit forcément être une personne physique et NE PEUT PAS être une direction ou service
8 La description de la sous-action ne doit pas répéter le titre de la sous-action. Elle doit apporter des informations complémentaires. Si le titre est suffisant, laisser "description" à "".

Liste des sous-actions à enrichir

-------- DEBUT LISTE --------
{sous_actions_list}
--------- FIN LISTE ---------

Texte source du plan d'actions

--------- TEXTE SOURCE ---------
{texte_pdf_a_analyser}
--------- FIN TEXTE SOURCE ---------

Format de sortie
1 Répondre uniquement avec un objet JSON valide
2 Ne rien ajouter avant ni après le JSON
3 Ne pas utiliser de balises Markdown
4 Les clés sont les index numériques des sous-actions tels que fournis dans la liste

Exemple de format attendu
{{
  "0": {{"description": "Description trouvée dans le texte", "personne_pilote": "Jean Dupont", "statut": "En cours", "date_debut": "01/01/2025", "date_fin": "31/12/2025"}},
  "1": {{"description": "", "personne_pilote": "", "statut": "", "date_debut": "", "date_fin": ""}}
}}
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
        raw = re.sub(r'\s+', ' ', raw)

        text += raw
        
        return text

    except Exception as e:
        return f"Erreur lors de la lecture du CSV : {str(e)}"

def extract_text_from_excel(excel_file):
    try:
        sheets = pd.read_excel(excel_file, sheet_name=None, engine='openpyxl')

        parts = []
        total_rows = 0
        for sheet_name, df in sheets.items():
            df = df.fillna('')
            total_rows += len(df)

            part = f"## Onglet : {sheet_name}\n\n"
            part += f"**Dimensions :** {len(df)} lignes × {len(df.columns)} colonnes\n\n"
            part += f"**Colonnes :** {', '.join(str(c) for c in df.columns)}\n\n"
            part += "**Contenu :**\n\n"

            raw = df.to_string(index=False)
            raw = re.sub(r'\s+', ' ', raw)
            part += raw

            parts.append(part)

        header = f"# Fichier Excel — {len(sheets)} onglet(s), {total_rows} lignes au total\n\n"
        return header + "\n\n---\n\n".join(parts)

    except Exception as e:
        return f"Erreur lors de la lecture du fichier Excel : {str(e)}"

def df_to_compact_text(df: pd.DataFrame, show_index: bool = True) -> str:
    """Convertit un dataframe en texte compact pour l'envoyer à Gemini.
    Gère deux formats : ancien (sous-actions en liste) et nouveau (titre de la sous-action en colonne)."""
    cols_expected = ["axe", "sous-axe"]
    for col in cols_expected:
        if col not in df.columns:
            raise ValueError(f"Colonne manquante dans le DataFrame : {col}")

    has_sous_actions_list = "sous-actions" in df.columns
    has_sous_action_col = "titre de la sous-action" in df.columns

    df_sorted = df.copy()
    df_sorted = df_sorted.sort_values(by=["axe", "sous-axe"]).reset_index(drop=True)

    parts = []

    def add_segment(segment: str):
        if not segment:
            return
        parts.append(segment.strip())

    for axe in df_sorted["axe"].dropna().unique():
        df_axe = df_sorted[df_sorted["axe"] == axe]
        add_segment(f"{axe} :")

        for sous_axe in df_axe["sous-axe"].dropna().unique():
            df_sous_axe = df_axe[df_axe["sous-axe"] == sous_axe]
            add_segment(f"Sous axe {sous_axe} :")

            for index_row, row in df_sous_axe.iterrows():
                champs_action = []

                titre = str(row.get("titre", "")).strip()
                titre_sa = str(row.get("titre de la sous-action", "")).strip() if has_sous_action_col else ""
                is_sous_action_row = has_sous_action_col and not titre and titre_sa

                if is_sous_action_row:
                    if show_index:
                        champs_action.append(f"| {index_row} | [SA] {titre_sa}")
                    else:
                        champs_action.append(f"[SA] {titre_sa}")
                elif titre:
                    if show_index:
                        champs_action.append(f"| {index_row} | {titre}")
                    else:
                        champs_action.append(f"{titre}")

                desc = str(row.get("description", "")).strip()
                if desc:
                    champs_action.append(f"{desc}")

                if has_sous_actions_list and not has_sous_action_col:
                    sous_actions = row.get("sous-actions", None)
                    if isinstance(sous_actions, (list, tuple)):
                        sa_clean = [str(sa).strip() for sa in sous_actions if str(sa).strip()]
                        if sa_clean:
                            champs_action.append("" + "; ".join(sa_clean))
                    elif isinstance(sous_actions, str) and sous_actions.strip():
                        champs_action.append(f"{sous_actions.strip()}")

                champs_optionnels = [
                    ("objectifs", "Objectifs"),
                    ("structure pilote", "Structure pilote"),
                    ("direction ou service pilote", "Direction ou service pilote"),
                    ("personne pilote", "Personne pilote"),
                    ("budget", "Budget"),
                    ("statut", "Statut"),
                    ("date de début", "Date de début"),
                    ("date de fin", "Date de fin"),
                ]

                for col, label in champs_optionnels:
                    if col in df_sous_axe.columns:
                        val = row.get(col, None)
                        if pd.notna(val):
                            val_str = str(val).strip()
                            if val_str:
                                champs_action.append(f"{label} {val_str}")

                if champs_action:
                    texte_action = "" + "; ".join(champs_action) + "."
                    add_segment(texte_action)

    return "\n".join(parts).strip()

def build_ignore_directive(disabled_fields: list[str]) -> str:
    """Construit un bloc d'instruction prioritaire à préfixer aux prompts Gemini
    pour ignorer le remplissage de certains champs/colonnes.

    Retourne une chaîne vide si aucun champ n'est désactivé.
    """
    if not disabled_fields:
        return ""

    lines = "\n".join(f'- "{f}"' for f in disabled_fields)
    return (
        "================================================================\n"
        "INSTRUCTION PRIORITAIRE — COLONNES / CHAMPS À IGNORER\n"
        "Les colonnes/champs suivants NE doivent PAS être remplis :\n"
        f"{lines}\n"
        "Pour chacun de ces champs, retournez systématiquement la valeur "
        "vide (\"\" pour les chaînes, [] pour les listes, \"\" pour les nombres).\n"
        "Si les règles, exemples ou précisions ci-dessous décrivent comment "
        "remplir ces champs, IGNOREZ ces instructions : ne remplissez que "
        "les autres champs. Cette consigne est PRIORITAIRE sur tout le reste.\n"
        "================================================================\n\n"
    )


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


def normalize_sous_actions_value(val):
    """Retourne une liste de chaînes non vides pour la colonne « sous-actions ».

    Si le modèle renvoie une chaîne au lieu d'une liste, pandas/itération la parcourt
    caractère par caractère et déclenche à tort l'enrichissement des sous-actions.
    """
    if val is None:
        return []
    if isinstance(val, float) and pd.isna(val):
        return []
    if hasattr(val, "tolist") and not isinstance(val, (str, bytes, list, tuple, dict)):
        try:
            val = val.tolist()
        except Exception:
            return []
    if isinstance(val, (list, tuple)):
        return [str(x).strip() for x in val if str(x).strip()]
    if isinstance(val, str):
        s = val.strip()
        if not s or s.lower() in ("[]", "null", "none", "nan"):
            return []
        if s.startswith("["):
            try:
                parsed = json.loads(s)
                if isinstance(parsed, list):
                    return [str(x).strip() for x in parsed if str(x).strip()]
            except json.JSONDecodeError:
                pass
        return []
    return []


def split_long_titles(df: pd.DataFrame, max_len: int = 300, description_enabled: bool = True) -> pd.DataFrame:
    """Scinde les titres trop longs : conserve max_len chars dans le titre, reporte le reste dans description.

    Si `description_enabled` est False, le titre est simplement tronqué (l'overflow est ignoré)
    pour éviter de remplir une colonne désactivée par l'utilisateur.
    """
    for col in ["titre", "titre de la sous-action"]:
        if col not in df.columns:
            continue
        for idx in df.index:
            val = df.at[idx, col]
            if not isinstance(val, str) or len(val) <= max_len:
                continue
            cut = val.rfind(" ", 0, max_len)
            if cut == -1:
                cut = max_len
            overflow = val[cut:].strip()
            df.at[idx, col] = val[:cut].strip()
            if not description_enabled or "description" not in df.columns:
                continue
            existing_desc = str(df.at[idx, "description"]).strip() if pd.notna(df.at[idx, "description"]) else ""
            if existing_desc:
                df.at[idx, "description"] = overflow + " - " + existing_desc
            else:
                df.at[idx, "description"] = overflow
    return df

def strip_action_numbering(value):
    """Retire la numérotation d'une action (ex. 1.1.2) en tête de libellé."""
    if not isinstance(value, str) or not value.strip():
        return value
    return re.sub(r"^\d+(\.\d+)+\.?\s+", "", value.strip()).strip()


def strip_numbering_from_df(df: pd.DataFrame) -> pd.DataFrame:
    """Retourne une copie du dataframe sans numérotation dans les titres d'actions."""
    df_copy = df.copy()
    for col in ("titre", "titre de la sous-action"):
        if col in df_copy.columns:
            df_copy[col] = df_copy[col].apply(strip_action_numbering)
    return df_copy


def remplir_fichier_import(df: pd.DataFrame) -> io.BytesIO:
    """Remplit le fichier import avec les données du dataframe et retourne un BytesIO"""
    
    # 1 Charger le fichier source directement (sans copie sur disque)
    src = "utils/template_pa.xlsx"
    wb = load_workbook(src)
    ws = wb["Fichier dimport"]

    # 2 Mapping des colonnes Excel (lettre → nom de colonne df)
    mapping = {
        "A": "axe",
        "B": "sous-axe",
        "D": "titre",
        "E": "titre de la sous-action",
        "F": "description",
        "H": "objectifs",
        "J": "structure pilote",
        "M": "direction ou service pilote",
        "N": "personne pilote",
        "X": "budget",
        "Y": "statut",
        "AA": "date de début",
        "AB": "date de fin",
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


def upload_excel_to_drive(excel_bytes: io.BytesIO, filename: str, folder_id: str = DRIVE_FOLDER_ID):
    """Upload un fichier Excel (BytesIO) sur Google Drive dans le dossier configuré.

    Renvoie l'objet file Drive (avec id, name, webViewLink).
    """
    service_account_info = st.secrets["SERVICE_ACCOUNT_INFO"]
    if isinstance(service_account_info, str):
        service_account_info = json.loads(service_account_info)
    elif not isinstance(service_account_info, dict):
        service_account_info = dict(service_account_info)

    credentials = service_account.Credentials.from_service_account_info(
        service_account_info,
        scopes=["https://www.googleapis.com/auth/drive.file"],
    )
    service = build("drive", "v3", credentials=credentials)

    excel_bytes.seek(0)

    file_metadata = {
        "name": filename,
        "parents": [folder_id],
    }
    media = MediaIoBaseUpload(
        excel_bytes,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        resumable=False,
    )

    file = (
        service.files()
        .create(
            body=file_metadata,
            media_body=media,
            fields="id, name, webViewLink",
            supportsAllDrives=True,
        )
        .execute()
    )
    return file


def build_drive_filename(source_filename: str) -> str:
    """Construit le nom de fichier au format YYYY-MM-DD_HH-MM-SS_[nom de base].xlsx."""
    base_name = os.path.splitext(source_filename or "import")[0].strip() or "import"
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return f"{timestamp}_{base_name}.xlsx"


def display_df_markdown(df: pd.DataFrame):
    """Affiche un dataframe en mode structuré (axes > sous-axes > actions et sous-actions)"""
    has_sous_action_col = "titre de la sous-action" in df.columns

    axes = df["axe"].unique()

    for axe in axes:
        st.markdown(f"### {axe}")

        df_axe = df[df["axe"] == axe]
        sous_axes = df_axe["sous-axe"].unique()

        for sous_axe in sous_axes:
            with st.expander(f"{sous_axe}", expanded=False):
                df_sous_axe = df_axe[df_axe["sous-axe"] == sous_axe]

                for _, row in df_sous_axe.iterrows():
                    titre = str(row.get("titre", "")).strip() if pd.notna(row.get("titre")) else ""
                    titre_sa = ""
                    if has_sous_action_col:
                        titre_sa = str(row.get("titre de la sous-action", "")).strip() if pd.notna(row.get("titre de la sous-action")) else ""

                    is_sous_action = has_sous_action_col and not titre and titre_sa

                    if is_sous_action:
                        sa_md = ""
                        sa_md += f"> **Sous-action :** {titre_sa}\n>\n"

                        if row.get("description") and str(row["description"]).strip():
                            sa_md += f"> **Description :** {row['description']}\n>\n"

                        if row.get("personne pilote") and str(row["personne pilote"]).strip():
                            sa_md += f"> **Personne pilote :** {row['personne pilote']}\n>\n"

                        if row.get("statut") and str(row["statut"]).strip():
                            sa_md += f"> **Statut :** {row['statut']}\n>\n"

                        if row.get("date de début") and str(row["date de début"]).strip():
                            sa_md += f"> **Date de début :** {row['date de début']}\n>\n"

                        if row.get("date de fin") and str(row["date de fin"]).strip():
                            sa_md += f"> **Date de fin :** {row['date de fin']}\n>\n"

                        st.markdown(sa_md)
                    else:
                        action_md = ""

                        if titre:
                            action_md += f"**Titre :** {titre}\n\n"

                        if row.get("description") and str(row["description"]).strip():
                            action_md += f"**Description :** {row['description']}\n\n"

                        if not has_sous_action_col:
                            sous_actions = row.get("sous-actions", [])
                            if sous_actions and len(sous_actions) > 0:
                                action_md += "**Sous-actions :**\n"
                                for sa in sous_actions:
                                    if sa and str(sa).strip():
                                        action_md += f"- {sa}\n"
                                action_md += "\n"

                        if row.get("objectifs") and str(row["objectifs"]).strip():
                            action_md += f"**Objectifs :** {row['objectifs']}\n\n"

                        if row.get("structure pilote") and str(row["structure pilote"]).strip():
                            action_md += f"**Structure pilote :** {row['structure pilote']}\n\n"

                        if row.get("direction ou service pilote") and str(row["direction ou service pilote"]).strip():
                            action_md += f"**Direction ou service pilote :** {row['direction ou service pilote']}\n\n"

                        if row.get("personne pilote") and str(row["personne pilote"]).strip():
                            action_md += f"**Personne pilote :** {row['personne pilote']}\n\n"

                        if row.get("budget") and str(row["budget"]).strip():
                            action_md += f"**Budget :** {row['budget']}\n\n"

                        if row.get("statut") and str(row["statut"]).strip():
                            action_md += f"**Statut :** {row['statut']}\n\n"

                        st.markdown(action_md)

                        if "score" in df.columns and row.get("score") is not None:
                            score = row["score"]
                            if row.get("amelioree", False):
                                st.info(f"FA consolidée. (confiance précédente: **{score}**)")
                            else:
                                explication = row.get("explication", "")
                                if explication and str(explication).strip():
                                    st.info(f"Confiance: **{score}** - {explication}")
                                else:
                                    st.info(f"Confiance: **{score}**")

                    st.markdown("---")

    st.markdown("#### ✅ Vue tableau")
    cols_to_drop = [c for c in ['score', 'explication', 'amelioree'] if c in df.columns]
    df_a_afficher = df.drop(columns=cols_to_drop).copy()
    st.dataframe(df_a_afficher, use_container_width=True, height=600)


MISTRAL_MODEL = "mistral-large-4"
MISTRAL_BASE_URL = "https://api.mistral.ai/v1"
# Plafond déjà utilisé avec ce modèle dans les scripts du projet.
# "none" est refusé par l'API ; le raisonnement compte dans max_tokens.
MISTRAL_MAX_OUTPUT_TOKENS = 40000
MISTRAL_REASONING_EFFORT = "low"
# USD / million de tokens, tarif promo (utils/test_run_impact.py).
MISTRAL_PRICE_PER_M = {"input": 0.68, "output": 2.09}

_mistral_client: AsyncOpenAI | None = None


def max_output_tokens_for(model: str) -> int:
    """Plafond de sortie par modèle.

    gemini-2.5-pro, gemini-3-pro-preview et gemini-3.8-flash sont limités à
    65 536 tokens par l'API. gemini-4-argon accepte des sorties bien plus longues.
    mistral-large-4 est plafonné plus bas : le raisonnement consomme ce budget.
    """
    if model == MISTRAL_MODEL:
        return MISTRAL_MAX_OUTPUT_TOKENS
    if model == "gemini-4-argon":
        return 262144
    return 65536


def format_run_cost(model: str | None, tokens) -> str:
    """Coût indicatif. Gemini reste en euros (grille historique de l'outil), Mistral en dollars."""
    out_tok = int((tokens or [0, 0])[0] or 0)
    in_tok = int((tokens or [0, 0])[1] or 0)
    if model == MISTRAL_MODEL:
        amount = (MISTRAL_PRICE_PER_M["output"] * out_tok + MISTRAL_PRICE_PER_M["input"] * in_tok) / 1_000_000
        return f"✅ Import prêt pour un coût d'environ {amount:.2f} $ (tarif Mistral Large 4)"
    amount = (10 * out_tok + 2 * in_tok) / 1_000_000
    return f"✅ Import prêt pour un coût d'environ {amount:.2f} €"


def _mistral_api_key() -> str:
    key = os.environ.get("MISTRAL_API_KEY") or os.environ.get("mistral_api_key") or ""
    if key:
        return key
    try:
        return str(st.secrets.get("mistral_api_key") or "")
    except Exception:
        return ""


def get_mistral_client() -> AsyncOpenAI:
    global _mistral_client
    if _mistral_client is None:
        key = _mistral_api_key()
        if not key:
            raise RuntimeError("mistral_api_key absente (env ou .streamlit/secrets.toml).")
        _mistral_client = AsyncOpenAI(base_url=MISTRAL_BASE_URL, api_key=key, timeout=900.0)
    return _mistral_client


def _mistral_message_text(response) -> str:
    content = response.choices[0].message.content
    if isinstance(content, list):
        parts = []
        for part in content:
            get = part.get if isinstance(part, dict) else (lambda k, p=part: getattr(p, k, None))
            if get("type") == "text":
                parts.append(str(get("text") or ""))
        return "".join(parts)
    return str(content or "")


async def query_mistral(user_prompt, model=MISTRAL_MODEL):
    """Interroge Mistral. Le raisonnement est fixé à « low » : « none » est refusé sur Large 4."""
    start_time = time.time()
    output_token_limit = max_output_tokens_for(model)
    print(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] ✨ Mistral START ({model}, max {output_token_limit} tokens)")
    try:
        response = await get_mistral_client().chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": user_prompt}],
            max_tokens=output_token_limit,
            extra_body={"reasoning_effort": MISTRAL_REASONING_EFFORT},
        )
        usage = getattr(response, "usage", None)
        tokens = [
            int(getattr(usage, "completion_tokens", 0) or 0),
            int(getattr(usage, "prompt_tokens", 0) or 0),
        ]
        elapsed = time.time() - start_time
        print(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] ✅ Mistral END ({elapsed:.1f}s, {tokens} tokens)")
        return _mistral_message_text(response), elapsed, tokens
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] ❌ Mistral ERROR: {e}")
        return f"Erreur Mistral: {e}", elapsed, [0, 0]


async def query_gemini(user_prompt, model='gemini-3.1-pro-preview'):
    """Interroge Gemini avec streaming asynchrone, ou Mistral si ce modèle est choisi."""
    if model == MISTRAL_MODEL:
        return await query_mistral(user_prompt, model)
    start_time = time.time()
    output_token_limit = max_output_tokens_for(model)
    print(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] ✨ Gemini START ({model}, max {output_token_limit} tokens)")
    try:
        # Utiliser le streaming pour la réponse
        stream = await gemini_client.aio.models.generate_content_stream(
            model=model,
            contents=user_prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,
                max_output_tokens=output_token_limit
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
                    max_output_tokens=output_token_limit
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
# Découpage PDF, cache et fusion
# ==========================

IMPORT_CACHE_DIR = Path(__file__).resolve().parents[1] / "data" / "import_tool_cache"

_STEP_LABELS = {
    0: "texte extrait",
    1: "fiches extraites",
    2: "vérification faite",
    3: "consolidation faite",
    4: "sous-actions enrichies",
    5: "analyse terminée",
}


def _atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


def cache_file_id(file_hash: str, split: bool) -> str:
    mode = "split" if split else "full"
    return f"{file_hash[:16]}_{mode}"


def _first_half_page_count(n_pages: int) -> int:
    """Nombre de pages de la première moitié. La seconde reçoit le reste."""
    return max(1, (n_pages + 1) // 2)


def _split_text_halfway(text: str) -> tuple[str, str]:
    """Coupe un texte près du milieu, de préférence entre deux paragraphes."""
    if not text:
        return "", ""
    mid = len(text) // 2
    search_from = max(0, mid // 2)
    search_to = min(len(text), mid + 2000)
    cut = text.rfind("\n\n", search_from, search_to)
    if cut == -1:
        cut = text.rfind("\n", search_from, search_to)
    if cut == -1:
        cut = mid
    left, right = text[:cut].strip(), text[cut:].strip()
    if not left or not right:
        left, right = text[:mid].strip(), text[mid:].strip()
    return left, right


def _split_note(which: str, detail: str) -> str:
    return (
        "NOTE IMPORTANTE SUR LE DÉCOUPAGE\n"
        f"Le texte fourni est la {which} d’un document plus long ({detail}).\n"
        "Extrais uniquement les actions présentes dans ce texte. "
        "N’invente pas d’actions situées dans les pages absentes.\n"
        "Si le document source porte déjà une numérotation, conserve-la exactement.\n\n"
    )


def build_text_parts(file_bytes: bytes, filename: str, file_type: str, split: bool) -> tuple[list[dict], str | None]:
    """Découpe le fichier en une ou deux parties de texte.

    Pour un PDF, la coupe se fait au milieu du nombre de pages.
    Un PDF d'une seule page est coupé dans le texte.
    """
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if file_type == "PDF":
        try:
            reader = PdfReader(io.BytesIO(file_bytes))
            pages = [(i, page.extract_text() or "") for i, page in enumerate(reader.pages, start=1)]
        except Exception as e:
            return [], f"Erreur lors de l'extraction du PDF : {e}"
        if not pages:
            return [], "Erreur lors de l'extraction du PDF : aucune page"

        if not split:
            text = "\n".join(t for _, t in pages)
            label_pages = f"{len(pages)} page" + ("s" if len(pages) > 1 else "")
            return [{"label": "Document", "detail": label_pages, "text": text, "split_note": ""}], None

        if len(pages) == 1:
            left, right = _split_text_halfway(pages[0][1])
            raw_parts = [
                ("Moitié 1", "page 1, début du texte", left, "PREMIÈRE MOITIÉ"),
                ("Moitié 2", "page 1, suite du texte", right, "SECONDE MOITIÉ"),
            ]
        else:
            mid = _first_half_page_count(len(pages))
            slices = [pages[:mid], pages[mid:]]
            raw_parts = []
            for idx, sl in enumerate(slices):
                which = "PREMIÈRE MOITIÉ" if idx == 0 else "SECONDE MOITIÉ"
                label = "Moitié 1" if idx == 0 else "Moitié 2"
                detail = f"pages {sl[0][0]}–{sl[-1][0]}"
                text = "\n".join(t for _, t in sl)
                raw_parts.append((label, detail, text, which))

        parts = []
        for label, detail, text, which in raw_parts:
            parts.append({
                "label": label,
                "detail": detail,
                "text": text,
                "split_note": _split_note(which, detail),
            })
        return parts, None

    bio = io.BytesIO(file_bytes)
    if ext in ("xlsx", "xls"):
        text = extract_text_from_excel(bio)
    else:
        text = extract_text_from_csv(bio)
    if isinstance(text, str) and text.startswith("Erreur"):
        return [], text
    return [{"label": "Document", "detail": ext or "fichier", "text": text or "", "split_note": ""}], None


def describe_pdf_split(file_bytes: bytes) -> str | None:
    """Résumé de la coupe prévue, avant de lancer l'analyse."""
    try:
        reader = PdfReader(io.BytesIO(file_bytes))
        n = len(reader.pages)
    except Exception as e:
        return f"Impossible de lire le nombre de pages ({e})."
    if n <= 1:
        return "Ce PDF n'a qu'une page : le texte sera coupé en deux au milieu. Les deux analyses partiront en parallèle."
    mid = _first_half_page_count(n)
    return (
        f"Découpe prévue : pages 1–{mid} et pages {mid + 1}–{n} ({n} pages). "
        "Les deux analyses partiront en parallèle, puis les fiches seront fusionnées."
    )


def df_to_payload(df: pd.DataFrame | None) -> dict | None:
    if df is None:
        return None
    records = json.loads(df.to_json(orient="records", force_ascii=False))
    return {"columns": list(df.columns), "records": records}


def df_from_payload(payload) -> pd.DataFrame | None:
    if not payload:
        return None
    columns = payload.get("columns") or []
    records = payload.get("records") or []
    if not records:
        return pd.DataFrame(columns=columns)
    df = pd.DataFrame(records)
    for col in columns:
        if col not in df.columns:
            df[col] = None
    return df[columns]


def compute_step(state: dict) -> int:
    if state.get("final_done"):
        return 5
    parts = state.get("parts") or []
    if parts and all(p.get("enrich_done") for p in parts):
        return 4
    if parts and all(p.get("upgrade_done") for p in parts):
        return 3
    if parts and all(p.get("verify_done") for p in parts):
        return 2
    if parts and all(p.get("extract_done") for p in parts):
        return 1
    return 0


def _rows_of_saved(full: dict) -> int:
    if full.get("final_done") and full.get("merged_df"):
        return len(full["merged_df"].get("records") or [])
    total = 0
    for part in full.get("parts") or []:
        payload = part.get("df")
        if payload:
            total += len(payload.get("records") or [])
    return total


def dehydrate_state(state: dict) -> dict:
    parts_out = []
    for part in state["parts"]:
        parts_out.append({
            "label": part.get("label"),
            "detail": part.get("detail"),
            "text": part.get("text") or "",
            "split_note": part.get("split_note") or "",
            "extract_done": bool(part.get("extract_done")),
            "verify_done": bool(part.get("verify_done")),
            "upgrade_done": bool(part.get("upgrade_done")),
            "enrich_done": bool(part.get("enrich_done")),
            "errors": list(part.get("errors") or [])[-8:],
            "df": df_to_payload(part.get("df_obj")),
        })
    return {
        "id": state["id"],
        "filename": state.get("filename") or "import",
        "file_hash": state.get("file_hash"),
        "split": bool(state.get("split")),
        "created_at": state.get("created_at"),
        "updated_at": datetime.now().isoformat(timespec="seconds"),
        "settings": state.get("settings") or {},
        "parts": parts_out,
        "tokens": [int((state.get("tokens") or [0, 0])[0]), int((state.get("tokens") or [0, 0])[1])],
        "merged_df": df_to_payload(state.get("merged_obj")),
        "quali_result": state.get("quali_result"),
        "quali_done": bool(state.get("quali_done")),
        "final_done": bool(state.get("final_done")),
        "drive_link": state.get("drive_link"),
        "drive_name": state.get("drive_name"),
        "drive_error": state.get("drive_error"),
        "export_filename": state.get("export_filename"),
        "renumbered": bool(state.get("renumbered")),
        "deduped_rows": int(state.get("deduped_rows") or 0),
        "step_completed": compute_step(state),
    }


def cache_meta(full: dict) -> dict:
    settings = full.get("settings") or {}
    return {
        "id": full.get("id"),
        "filename": full.get("filename"),
        "file_hash": full.get("file_hash"),
        "split": bool(full.get("split")),
        "created_at": full.get("created_at"),
        "updated_at": full.get("updated_at"),
        "model": settings.get("model"),
        "final_done": bool(full.get("final_done")),
        "step_completed": int(full.get("step_completed") or 0),
        "rows": _rows_of_saved(full),
        "part_details": [f"{p.get('label')} ({p.get('detail')})" for p in full.get("parts") or []],
        "tokens": full.get("tokens") or [0, 0],
        "errors": [
            f"{p.get('label')}: {str(err)[:240]}"
            for p in full.get("parts") or []
            for err in (p.get("errors") or [])[:2]
        ][:6],
    }


def save_import_cache(state: dict) -> None:
    full = dehydrate_state(state)
    cache_id = full["id"]
    payload = json.dumps(full, ensure_ascii=False)
    _atomic_write_text(IMPORT_CACHE_DIR / f"{cache_id}.json", payload)
    _atomic_write_text(
        IMPORT_CACHE_DIR / f"{cache_id}.meta.json",
        json.dumps(cache_meta(full), ensure_ascii=False),
    )
    print(f"[cache] étape {full['step_completed']}/5 enregistrée ({cache_id})")


def load_import_cache(cache_id: str) -> dict | None:
    path = IMPORT_CACHE_DIR / f"{cache_id}.json"
    if not path.exists():
        return None
    try:
        full = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[cache] lecture impossible {cache_id}: {e}")
        return None
    for part in full.get("parts") or []:
        part["df_obj"] = df_from_payload(part.get("df"))
        part.setdefault("errors", [])
        part.setdefault("split_note", "")
        part.setdefault("text", "")
    full["merged_obj"] = df_from_payload(full.get("merged_df"))
    tokens = full.get("tokens") or [0, 0]
    full["tokens"] = [int(tokens[0] or 0), int(tokens[1] or 0)]
    full.setdefault("settings", {})
    return full


def list_import_caches() -> list[dict]:
    if not IMPORT_CACHE_DIR.exists():
        return []
    items = []
    for meta_path in IMPORT_CACHE_DIR.glob("*.meta.json"):
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not meta.get("id") or not meta.get("file_hash"):
            continue
        items.append(meta)
    items.sort(key=lambda m: m.get("updated_at") or "", reverse=True)
    return items


def delete_import_cache(cache_id: str) -> None:
    for suffix in (".json", ".meta.json", ".json.tmp", ".meta.json.tmp"):
        path = IMPORT_CACHE_DIR / f"{cache_id}{suffix}"
        if path.exists():
            path.unlink()


def format_cache_time(value: str | None) -> str:
    if not value:
        return ""
    try:
        return datetime.fromisoformat(value).strftime("%d/%m/%Y %H:%M")
    except ValueError:
        return value


def ensure_score_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "score" not in df.columns:
        df["score"] = None
    if "explication" not in df.columns:
        df["explication"] = ""
    if "amelioree" not in df.columns:
        df["amelioree"] = False
    return df


def finalize_extracted_df(data, avec_sous_actions: bool, disabled_columns: list[str]) -> pd.DataFrame:
    if not isinstance(data, list):
        raise ValueError("La réponse n'est pas un tableau JSON")
    if len(data) == 0:
        df = pd.DataFrame(columns=[
            "axe", "sous-axe", "titre", "description", "sous-actions",
            "objectifs", "structure pilote", "direction ou service pilote",
            "personne pilote", "budget", "statut",
        ])
    else:
        df = pd.DataFrame(data)
    if not avec_sous_actions:
        df["sous-actions"] = [[] for _ in range(len(df))]
    elif "sous-actions" not in df.columns:
        df["sous-actions"] = [[] for _ in range(len(df))]
    else:
        df["sous-actions"] = df["sous-actions"].apply(normalize_sous_actions_value)
    for col in ("objectifs", "structure pilote"):
        if col not in df.columns:
            df[col] = ""
        else:
            df[col] = df[col].fillna("")
    for col in disabled_columns:
        if col in df.columns:
            df[col] = ""
    return df.reset_index(drop=True)


def _add_tokens(state: dict, tokens) -> None:
    state["tokens"][0] += int((tokens or [0, 0])[0] or 0)
    state["tokens"][1] += int((tokens or [0, 0])[1] or 0)


def _prompt_with_note(part: dict, body: str) -> str:
    return (part.get("split_note") or "") + body


async def extract_one(part: dict, state: dict) -> dict:
    settings = state["settings"]
    try:
        ignore = build_ignore_directive(settings.get("disabled_columns") or [])
        prompt = _prompt_with_note(
            part,
            ignore + custom_prompt
            .replace("{precisions}", settings.get("precisions") or "")
            .replace("{texte_pdf_a_analyser}", part.get("text") or "")
            .replace("{date_du_jour}", datetime.now().strftime("%d/%m/%Y")),
        )
        result, elapsed, tokens = await query_gemini(prompt, settings.get("model"))
        _add_tokens(state, tokens)
        if not result or str(result).startswith("Erreur"):
            part["errors"].append(str(result or "Réponse vide"))
            save_import_cache(state)
            return {"ok": False, "elapsed": elapsed, "tokens": tokens, "error": result, "raw": result}
        data = parse_json_response(result)
        df = finalize_extracted_df(
            data,
            bool(settings.get("avec_sous_actions", True)),
            settings.get("disabled_columns") or [],
        )
        part["df_obj"] = df
        part["extract_done"] = True
        part["errors"] = []
        if len(df) == 0:
            part["df_obj"] = ensure_score_columns(df)
            part["verify_done"] = True
            part["upgrade_done"] = True
            part["enrich_done"] = True
        save_import_cache(state)
        return {"ok": True, "elapsed": elapsed, "tokens": tokens, "n": len(df), "detail_line": f"{len(df)} actions"}
    except Exception as e:
        traceback.print_exc()
        part["errors"].append(f"Extraction : {e}")
        save_import_cache(state)
        raw = locals().get("result")
        return {"ok": False, "elapsed": 0, "tokens": [0, 0], "error": str(e), "raw": raw if isinstance(raw, str) else None}


async def verify_one(part: dict, state: dict) -> dict:
    settings = state["settings"]
    try:
        df = part["df_obj"]
        reponse_ia = df_to_compact_text(df)
        prompt = _prompt_with_note(
            part,
            prompt_verif_1.replace("{texte_pdf_a_analyser}", part.get("text") or "").replace("{reponse_ia}", reponse_ia or ""),
        )
        result, elapsed, tokens = await query_gemini(prompt, settings.get("model"))
        _add_tokens(state, tokens)
        if not result or str(result).startswith("Erreur"):
            part["errors"].append(str(result or "Réponse vide"))
            save_import_cache(state)
            return {"ok": False, "elapsed": elapsed, "tokens": tokens, "error": result, "raw": result}
        scores = parse_json_response(result)
        if not isinstance(scores, dict):
            raise ValueError("La vérification n'a pas renvoyé un objet JSON indexé")
        df = ensure_score_columns(df)
        applied = 0
        for idx_str, score_info in scores.items():
            idx = int(idx_str)
            if idx in df.index:
                info = score_info if isinstance(score_info, dict) else {}
                df.at[idx, "score"] = info.get("score")
                df.at[idx, "explication"] = info.get("explication", "")
                applied += 1
        part["df_obj"] = df
        part["verify_done"] = True
        part["errors"] = []
        save_import_cache(state)
        return {"ok": True, "elapsed": elapsed, "tokens": tokens, "applied": applied, "detail_line": f"{applied} scores"}
    except Exception as e:
        traceback.print_exc()
        part["errors"].append(f"Vérification : {e}")
        save_import_cache(state)
        raw = locals().get("result")
        return {"ok": False, "elapsed": 0, "tokens": [0, 0], "error": str(e), "raw": raw if isinstance(raw, str) else None}


async def upgrade_one(part: dict, state: dict) -> dict:
    settings = state["settings"]
    disabled_columns = settings.get("disabled_columns") or []
    try:
        df = part["df_obj"].copy()
        if "score" not in df.columns:
            part["df_obj"] = ensure_score_columns(df)
            part["upgrade_done"] = True
            save_import_cache(state)
            return {"ok": True, "elapsed": 0, "tokens": [0, 0], "upgraded": 0, "low": 0, "skipped": True}
        scores_num = pd.to_numeric(df["score"], errors="coerce")
        low_indices = list(df.index[scores_num < 90])
        if not low_indices:
            part["df_obj"] = df
            part["upgrade_done"] = True
            save_import_cache(state)
            return {"ok": True, "elapsed": 0, "tokens": [0, 0], "upgraded": 0, "low": 0, "skipped": True, "detail_line": "rien à consolider"}

        batch_size = 5
        batches = [low_indices[i:i + batch_size] for i in range(0, len(low_indices), batch_size)]
        ignore = build_ignore_directive(disabled_columns)
        prompts = []
        for batch_indices in batches:
            actions = ""
            for idx in batch_indices:
                row = df.loc[idx]
                actions += f"|{idx}| {row['titre']}\n"
            prompts.append(_prompt_with_note(
                part,
                ignore + prompt_upgrade_1.replace("{texte_pdf_a_analyser}", part.get("text") or "").replace("{actions_a_ameliorer}", actions),
            ))

        results = await asyncio.gather(
            *[query_gemini(prompt, settings.get("model")) for prompt in prompts],
            return_exceptions=True,
        )
        upgraded = 0
        errors = []
        max_time = 0.0
        total_tokens = [0, 0]
        for batch_idx, result in enumerate(results):
            if isinstance(result, Exception):
                errors.append(f"Batch {batch_idx + 1}: {result}")
                continue
            upgrade_result, elapsed, tokens = result
            max_time = max(max_time, elapsed)
            total_tokens[0] += int(tokens[0] or 0)
            total_tokens[1] += int(tokens[1] or 0)
            if upgrade_result and not str(upgrade_result).startswith("Erreur"):
                try:
                    upgrade_data = parse_json_response(upgrade_result)
                    if not isinstance(upgrade_data, dict):
                        raise ValueError("réponse non indexée")
                    for idx_str, item in upgrade_data.items():
                        idx = int(idx_str)
                        if idx not in df.index or not isinstance(item, dict):
                            continue
                        if "titre" in item:
                            df.at[idx, "titre"] = item["titre"]
                        if "description" in item and "description" not in disabled_columns:
                            df.at[idx, "description"] = item["description"]
                        if "sous-actions" in item and settings.get("avec_sous_actions", True):
                            df.at[idx, "sous-actions"] = normalize_sous_actions_value(item["sous-actions"])
                        df.at[idx, "amelioree"] = True
                        upgraded += 1
                except Exception as e:
                    errors.append(f"Batch {batch_idx + 1}: parsing {e}")
            else:
                errors.append(f"Batch {batch_idx + 1}: {upgrade_result}")

        _add_tokens(state, total_tokens)
        part["df_obj"] = df
        part["upgrade_done"] = True
        part["errors"] = errors
        save_import_cache(state)
        return {
            "ok": True,
            "elapsed": max_time,
            "tokens": total_tokens,
            "upgraded": upgraded,
            "low": len(low_indices),
            "batches": len(batches),
            "errors": errors,
            "detail_line": f"{upgraded} consolidées sur {len(low_indices)}",
        }
    except Exception as e:
        traceback.print_exc()
        part["errors"].append(f"Consolidation : {e}")
        save_import_cache(state)
        return {"ok": False, "elapsed": 0, "tokens": [0, 0], "error": str(e)}


async def enrich_one(part: dict, state: dict) -> dict:
    settings = state["settings"]
    disabled_columns = settings.get("disabled_columns") or []
    disabled_json_keys = settings.get("disabled_json_keys") or []
    try:
        df = part["df_obj"].copy()
        if not settings.get("avec_sous_actions", True):
            df["sous-actions"] = [[] for _ in range(len(df))]

        all_sous_actions = []
        sa_parent_map = {}
        global_idx = 0
        if "sous-actions" in df.columns:
            for df_idx, row in df.iterrows():
                sous_actions = normalize_sous_actions_value(row.get("sous-actions", None))
                df.at[df_idx, "sous-actions"] = sous_actions
                for sa_pos, sa_str in enumerate(sous_actions):
                    if sa_str:
                        all_sous_actions.append({
                            "global_idx": global_idx,
                            "parent_idx": df_idx,
                            "parent_titre": row.get("titre", ""),
                            "sa_titre": sa_str,
                            "sa_pos": sa_pos,
                        })
                        sa_parent_map[(df_idx, sa_pos)] = global_idx
                        global_idx += 1

        enrichment_data = {}
        max_time = 0.0
        total_tokens = [0, 0]
        errors = []
        n_batches = 0

        if all_sous_actions:
            batch_size = 30
            sa_batches = [all_sous_actions[i:i + batch_size] for i in range(0, len(all_sous_actions), batch_size)]
            n_batches = len(sa_batches)
            enrich_ignore = build_ignore_directive(disabled_json_keys)
            prompts = []
            for batch in sa_batches:
                sous_actions_list = ""
                for sa_info in batch:
                    sous_actions_list += f"{sa_info['global_idx']} | [Action parente : {sa_info['parent_titre']}] {sa_info['sa_titre']}\n"
                prompts.append(_prompt_with_note(
                    part,
                    enrich_ignore + prompt_enrich_sous_actions
                    .replace("{sous_actions_list}", sous_actions_list)
                    .replace("{texte_pdf_a_analyser}", part.get("text") or ""),
                ))
            results = await asyncio.gather(
                *[query_gemini(prompt, settings.get("model")) for prompt in prompts],
                return_exceptions=True,
            )
            for batch_idx, result in enumerate(results):
                if isinstance(result, Exception):
                    errors.append(f"Batch {batch_idx + 1}: {result}")
                    continue
                enrich_result, elapsed, tokens = result
                max_time = max(max_time, elapsed)
                total_tokens[0] += int(tokens[0] or 0)
                total_tokens[1] += int(tokens[1] or 0)
                if enrich_result and not str(enrich_result).startswith("Erreur"):
                    try:
                        parsed = parse_json_response(enrich_result)
                        if not isinstance(parsed, dict):
                            raise ValueError("réponse non indexée")
                        for idx_str, fields in parsed.items():
                            enrichment_data[int(idx_str)] = fields if isinstance(fields, dict) else {}
                    except Exception as e:
                        errors.append(f"Batch {batch_idx + 1}: parsing {e}")
                else:
                    errors.append(f"Batch {batch_idx + 1}: {enrich_result}")
            _add_tokens(state, total_tokens)

            def _sa_field(col_name: str, value: str) -> str:
                return "" if col_name in disabled_columns else value

            new_rows = []
            for df_idx, row in df.iterrows():
                action_row = row.to_dict()
                action_row["titre de la sous-action"] = ""
                action_row["date de début"] = ""
                action_row["date de fin"] = ""
                action_row.pop("sous-actions", None)
                new_rows.append(action_row)

                sous_actions_list_raw = row.get("sous-actions", [])
                if isinstance(sous_actions_list_raw, (list, tuple)):
                    for sa_pos, sa in enumerate(sous_actions_list_raw):
                        sa_str = str(sa).strip()
                        if not sa_str:
                            continue
                        gidx = sa_parent_map.get((df_idx, sa_pos))
                        sa_enrichment = enrichment_data.get(gidx, {}) if gidx is not None else {}
                        new_rows.append({
                            "axe": row.get("axe", ""),
                            "sous-axe": row.get("sous-axe", ""),
                            "titre": row.get("titre", ""),
                            "titre de la sous-action": sa_str,
                            "description": _sa_field("description", sa_enrichment.get("description", "")),
                            "objectifs": "",
                            "structure pilote": "",
                            "direction ou service pilote": "",
                            "personne pilote": _sa_field("personne pilote", sa_enrichment.get("personne_pilote", "")),
                            "budget": "",
                            "statut": _sa_field("statut", sa_enrichment.get("statut", "")),
                            "date de début": _sa_field("date de début", sa_enrichment.get("date_debut", "")),
                            "date de fin": _sa_field("date de fin", sa_enrichment.get("date_fin", "")),
                            "score": None,
                            "explication": "",
                            "amelioree": False,
                        })
            df = pd.DataFrame(new_rows).reset_index(drop=True)
        else:
            df["titre de la sous-action"] = ""
            df["date de début"] = ""
            df["date de fin"] = ""
            if "sous-actions" in df.columns:
                df = df.drop(columns=["sous-actions"])

        for col in disabled_columns:
            if col in df.columns:
                df[col] = ""

        enriched_count = sum(
            1 for v in enrichment_data.values()
            if any(v.get(k) for k in ("description", "personne_pilote", "statut", "date_debut", "date_fin"))
        )
        part["df_obj"] = df
        part["enrich_done"] = True
        part["errors"] = errors
        save_import_cache(state)
        return {
            "ok": True,
            "elapsed": max_time,
            "tokens": total_tokens,
            "sous_actions": len(all_sous_actions),
            "enriched": enriched_count,
            "batches": n_batches,
            "rows": len(df),
            "errors": errors,
            "skipped_sous_actions": not settings.get("avec_sous_actions", True),
            "detail_line": f"{enriched_count} sous-actions enrichies sur {len(all_sous_actions)}",
        }
    except Exception as e:
        traceback.print_exc()
        part["errors"].append(f"Enrichissement : {e}")
        save_import_cache(state)
        return {"ok": False, "elapsed": 0, "tokens": [0, 0], "error": str(e)}


def _parse_axe(label: str) -> tuple[int | None, str]:
    if not isinstance(label, str):
        return None, ""
    match = re.match(r"^\s*Axe\s+(\d+)\s*:\s*(.*)$", label, flags=re.IGNORECASE)
    if not match:
        return None, label.strip()
    return int(match.group(1)), match.group(2).strip()


def _axis_entries(df: pd.DataFrame) -> list[tuple[int | None, str]]:
    if df is None or "axe" not in getattr(df, "columns", []):
        return []
    seen = set()
    entries = []
    for raw in df["axe"].tolist():
        if not isinstance(raw, str) or raw in seen:
            continue
        seen.add(raw)
        entries.append(_parse_axe(raw))
    return entries


def build_axis_map(df_first: pd.DataFrame, df_next: pd.DataFrame) -> dict[int, int]:
    """Recolle la numérotation de la moitié suivante sur la première.

    Un axe dont le titre existe déjà garde le numéro de la première moitié.
    Un numéro déjà pris, ou qui redémarre au milieu de la plage déjà vue, est décalé à la suite.
    """
    title_to_num: dict[str, int] = {}
    claimed: set[int] = set()
    for num, title in _axis_entries(df_first):
        if num is None:
            continue
        claimed.add(num)
        key = title.lower()
        if key and key not in title_to_num:
            title_to_num[key] = num

    next_title_by_num: dict[int, str] = {}
    next_nums: list[int] = []
    for num, title in _axis_entries(df_next):
        if num is None or num in next_title_by_num:
            continue
        next_title_by_num[num] = title
        next_nums.append(num)

    mapping: dict[int, int] = {}
    unmatched: list[int] = []
    for num in next_nums:
        key = (next_title_by_num.get(num) or "").lower()
        if key and key in title_to_num:
            mapping[num] = title_to_num[key]
            claimed.add(mapping[num])
        else:
            unmatched.append(num)

    for num in unmatched:
        ceiling = max(claimed) if claimed else 0
        if num not in claimed and num > ceiling:
            mapping[num] = num
            claimed.add(num)
            continue
        nxt = ceiling + 1
        while nxt in claimed:
            nxt += 1
        mapping[num] = nxt
        claimed.add(nxt)
    return mapping


def _rewrite_leading_number(value, mapping: dict[int, int]):
    if not isinstance(value, str) or not mapping:
        return value
    match = re.match(r"^(\s*Axe\s+)(\d+)(\b.*)$", value, flags=re.IGNORECASE)
    if match:
        old = int(match.group(2))
        if old in mapping and mapping[old] != old:
            return f"{match.group(1)}{mapping[old]}{match.group(3)}"
        return value
    match = re.match(r"^(\s*)(\d+)(\.\d+.*)$", value)
    if match:
        old = int(match.group(2))
        if old in mapping and mapping[old] != old:
            return f"{match.group(1)}{mapping[old]}{match.group(3)}"
    return value


def apply_axis_map(df: pd.DataFrame, mapping: dict[int, int]) -> pd.DataFrame:
    if not mapping or all(src == dst for src, dst in mapping.items()):
        return df
    df = df.copy()
    for col in ("axe", "sous-axe", "titre", "titre de la sous-action"):
        if col in df.columns:
            df[col] = df[col].apply(lambda v, m=mapping: _rewrite_leading_number(v, m))
    return df


def merge_part_dataframes(frames: list[pd.DataFrame], split: bool) -> tuple[pd.DataFrame, dict]:
    info = {"renumbered": False, "deduped": 0}
    usable = [df for df in frames if df is not None]
    if not usable:
        return pd.DataFrame(), info
    if len(usable) == 1:
        return usable[0].reset_index(drop=True), info

    ordered = [usable[0].copy()]
    accumulated = usable[0]
    for nxt in usable[1:]:
        mapping = build_axis_map(accumulated, nxt)
        if any(src != dst for src, dst in mapping.items()):
            nxt = apply_axis_map(nxt, mapping)
            info["renumbered"] = True
        ordered.append(nxt)
        accumulated = pd.concat([accumulated, nxt], ignore_index=True)

    columns: list[str] = []
    for df in ordered:
        for col in df.columns:
            if col not in columns:
                columns.append(col)
    aligned = []
    for df in ordered:
        copied = df.copy()
        for col in columns:
            if col not in copied.columns:
                copied[col] = None
        aligned.append(copied[columns])
    merged = pd.concat(aligned, ignore_index=True)
    if split:
        keys = [c for c in ("axe", "sous-axe", "titre", "titre de la sous-action") if c in merged.columns]
        if keys:
            before = len(merged)
            merged = merged.drop_duplicates(subset=keys, keep="first").reset_index(drop=True)
            info["deduped"] = before - len(merged)
    return merged, info


def cleanup_final_df(df: pd.DataFrame, disabled_columns: list[str]) -> pd.DataFrame:
    df = df.copy()
    for col in disabled_columns:
        if col in df.columns:
            df[col] = ""
    df = split_long_titles(df, description_enabled="description" not in disabled_columns)
    for col in ("direction ou service pilote", "personne pilote"):
        if col in df.columns:
            df[col] = df[col].apply(lambda x: x.replace("/", ", ") if isinstance(x, str) else x)
    for col in df.columns:
        df[col] = df[col].apply(lambda x: re.sub(r" +", " ", x).strip() if isinstance(x, str) else x)
    return df


def _show_part_metrics(label: str, step_name: str, result: dict) -> None:
    if not result or not result.get("ok"):
        err = (result or {}).get("error") or "erreur"
        st.error(f"❌ {label} — {step_name} : {err}")
        raw = (result or {}).get("raw")
        if isinstance(raw, str) and raw.strip():
            st.text(raw[:8000])
        return
    tokens = result.get("tokens") or [0, 0]
    extra = result.get("detail_line") or ""
    suffix = f" | {extra}" if extra else ""
    st.info(
        f"✨ {label} — {step_name} : {float(result.get('elapsed') or 0):.1f}s | "
        f"Entrée : {int(tokens[1]):,} tokens | Sortie : {int(tokens[0]):,} tokens{suffix}"
    )


def _run_parallel(parts: list[dict], factory) -> list:
    async def _go():
        return await asyncio.gather(*[factory(part) for part in parts], return_exceptions=True)

    started = time.time()
    raw_results = asyncio.run(_go())
    wall = time.time() - started
    results = []
    for part, result in zip(parts, raw_results):
        if isinstance(result, Exception):
            traceback.print_exception(type(result), result, result.__traceback__)
            part.setdefault("errors", []).append(str(result))
            results.append({"ok": False, "elapsed": 0, "tokens": [0, 0], "error": str(result)})
        else:
            results.append(result)
    return results, wall


def _step_intro(title: str, state: dict) -> None:
    st.markdown("---")
    st.markdown(title)
    if state.get("split") and len(state.get("parts") or []) > 1:
        details = ", ".join(f"{p['label']} ({p['detail']})" for p in state["parts"])
        st.caption(f"Traitement en parallèle — {details}")


def run_import_pipeline(state: dict, resuming: bool = False) -> dict:
    """Enchaîne les 5 étapes. Chaque partie est traitée en parallèle, puis fusionnée."""
    if state.get("final_done"):
        return state

    parts = state["parts"]
    settings = state.get("settings") or {}
    if resuming:
        st.info("Reprise du cache. Les parties et les étapes déjà terminées ne sont pas relancées.")

    pending = [p for p in parts if not p.get("extract_done")]
    if pending:
        _step_intro("## 🪄 Étape 1 : Définition de la structure et créations des fiches actions", state)
        if settings.get("disabled_columns"):
            st.caption("🚫 Colonnes désactivées (ignorées par l'IA) : " + ", ".join(settings["disabled_columns"]))
        already = [p["label"] for p in parts if p.get("extract_done")]
        if already:
            st.caption("Déjà en cache : " + ", ".join(already))
        with st.spinner("🌀 Étape 1/5 : extraction des fiches actions..."):
            results, wall = _run_parallel(pending, lambda part: extract_one(part, state))
        for part, result in zip(pending, results):
            _show_part_metrics(part["label"], "extraction", result)
            if result.get("ok") and part.get("df_obj") is not None:
                st.success(f"✅ {part['label']} : {len(part['df_obj'])} actions extraites")
                st.dataframe(part["df_obj"], use_container_width=True, height=400)
        if len(pending) > 1:
            st.caption(f"Attente parallèle : {wall:.1f}s")
        if any(not p.get("extract_done") for p in parts):
            st.warning("L'extraction n'est pas complète. Le cache conserve les parties réussies : vous pouvez reprendre.")
            return state

    if not settings.get("avec_verifications", True):
        changed = False
        for part in parts:
            if part.get("extract_done") and not part.get("upgrade_done"):
                part["df_obj"] = ensure_score_columns(part["df_obj"])
                part["verify_done"] = True
                part["upgrade_done"] = True
                changed = True
        if changed:
            st.markdown("---")
            st.info("⏭️ Vérifications désactivées — étapes 2 et 3 ignorées.")
            save_import_cache(state)
    else:
        pending = [p for p in parts if not p.get("verify_done")]
        if pending:
            _step_intro("## 🔍 Étape 2 : Vérification de la qualité des fiches actions", state)
            already = [p["label"] for p in parts if p.get("verify_done")]
            if already:
                st.caption("Déjà en cache : " + ", ".join(already))
            with st.spinner("🌀 Étape 2/5 : vérification de la qualité des fiches actions..."):
                results, wall = _run_parallel(pending, lambda part: verify_one(part, state))
            for part, result in zip(pending, results):
                _show_part_metrics(part["label"], "vérification", result)
                df = part.get("df_obj")
                if result.get("ok") and df is not None and "score" in df.columns:
                    cols = [c for c in ("titre", "score", "explication") if c in df.columns]
                    st.dataframe(df[cols], use_container_width=True, height=300)
            if len(pending) > 1:
                st.caption(f"Attente parallèle : {wall:.1f}s")
            if any(not p.get("verify_done") for p in parts):
                st.warning("La vérification n'est pas complète. Le cache conserve les parties réussies : vous pouvez reprendre.")
                return state

        pending = [p for p in parts if not p.get("upgrade_done")]
        if pending:
            _step_intro("## 🔧 Étape 3/5 : Consolidation des fiches actions", state)
            already = [p["label"] for p in parts if p.get("upgrade_done")]
            if already:
                st.caption("Déjà en cache : " + ", ".join(already))
            with st.spinner("🌀 Étape 3/5 : consolidation des fiches actions..."):
                results, wall = _run_parallel(pending, lambda part: upgrade_one(part, state))
            for part, result in zip(pending, results):
                if result.get("skipped"):
                    st.success(f"✅ {part['label']} : toutes les actions ont un score suffisant")
                else:
                    _show_part_metrics(part["label"], "consolidation", result)
                    if result.get("ok") and result.get("upgraded"):
                        st.success(f"✅ {part['label']} : {result['upgraded']} actions consolidées")
                for err in result.get("errors") or []:
                    st.error(f"❌ {part['label']} — {err}")
            if len(pending) > 1:
                st.caption(f"Attente parallèle : {wall:.1f}s")
            if any(not p.get("upgrade_done") for p in parts):
                st.warning("La consolidation n'est pas complète. Vous pouvez reprendre depuis le cache.")
                return state

    pending = [p for p in parts if not p.get("enrich_done")]
    if pending:
        _step_intro("## 🔎 Étape 4/5 : Enrichissement des sous-actions", state)
        if not settings.get("avec_sous_actions", True):
            st.info("⏭️ Sous-actions désactivées par l'utilisateur.")
        already = [p["label"] for p in parts if p.get("enrich_done")]
        if already:
            st.caption("Déjà en cache : " + ", ".join(already))
        with st.spinner("🌀 Étape 4/5 : enrichissement des sous-actions..."):
            results, wall = _run_parallel(pending, lambda part: enrich_one(part, state))
        for part, result in zip(pending, results):
            _show_part_metrics(part["label"], "enrichissement", result)
            if result.get("ok"):
                st.success(f"✅ {part['label']} : {result.get('rows', 0)} lignes (actions + sous-actions)")
            for err in result.get("errors") or []:
                st.error(f"❌ {part['label']} — {err}")
        if len(pending) > 1:
            st.caption(f"Attente parallèle : {wall:.1f}s")
        if any(not p.get("enrich_done") for p in parts):
            st.warning("L'enrichissement n'est pas complet. Vous pouvez reprendre depuis le cache.")
            return state

    if state.get("merged_obj") is None:
        merged, info = merge_part_dataframes(
            [p.get("df_obj") for p in parts],
            split=bool(state.get("split")),
        )
        merged = cleanup_final_df(merged, settings.get("disabled_columns") or [])
        state["merged_obj"] = merged
        state["renumbered"] = info["renumbered"]
        state["deduped_rows"] = info["deduped"]
        save_import_cache(state)
        if state.get("split") and len(parts) > 1:
            st.success(f"✅ Moitiés fusionnées : {len(merged)} lignes")

    if not state.get("quali_done"):
        st.markdown("---")
        st.markdown("## ✅ Étape 5/5 : Vérifications finales")
        merged = state.get("merged_obj")
        if merged is None or len(merged) == 0:
            state["quali_result"] = "Aucune action extraite."
            state["quali_done"] = True
        else:
            async def _quali():
                text = df_to_compact_text(merged, show_index=False)
                return await query_gemini(
                    prompt_verif_quali.replace("{reponse_ia}", text or ""),
                    settings.get("model"),
                )

            with st.spinner("🌀 Étape 5/5 : analyse qualitative finale..."):
                try:
                    quali_result, elapsed, tokens = asyncio.run(_quali())
                except Exception as e:
                    traceback.print_exc()
                    quali_result, elapsed, tokens = f"Erreur lors de la vérification qualitative : {e}", 0, [0, 0]
            _add_tokens(state, tokens)
            state["quali_result"] = quali_result
            state["quali_done"] = True
            st.info(
                f"✨ Vérifications finales : {float(elapsed):.1f}s | "
                f"Entrée : {int(tokens[1] or 0):,} tokens | Sortie : {int(tokens[0] or 0):,} tokens"
            )

    state["final_done"] = True
    if not state.get("export_filename"):
        state["export_filename"] = build_drive_filename(state.get("filename") or "import")
    save_import_cache(state)
    return state


def render_cache_card(meta: dict, primary: bool) -> tuple[str, str] | None:
    cid = meta["id"]
    step = int(meta.get("step_completed") or 0)
    label = _STEP_LABELS.get(step, "en cours")
    mode = "PDF coupé en deux" if meta.get("split") else "document entier"
    when = format_cache_time(meta.get("updated_at"))
    rows = int(meta.get("rows") or 0)
    parts = ", ".join(meta.get("part_details") or [])
    st.markdown(f"**Cache disponible — {meta.get('filename') or 'fichier'}**")
    st.caption(
        f"{mode} · {label} ({step}/5) · {rows} lignes · {when} · modèle {meta.get('model') or '—'}"
        + (f" · {parts}" if parts else "")
    )
    if meta.get("final_done"):
        st.caption("L'analyse est terminée. Vous pouvez réafficher le résultat et retélécharger le fichier.")
    else:
        st.caption("Reprendre relance uniquement les étapes qui ne sont pas encore dans le cache.")
    for err in meta.get("errors") or []:
        st.caption(f"Dernière erreur conservée : {err}")
    left, right = st.columns(2)
    button_type = "primary" if primary else "secondary"
    action = None
    if meta.get("final_done"):
        if left.button("Afficher le résultat en cache", type=button_type, key=f"show_{cid}"):
            action = ("show", cid)
    elif left.button("Reprendre depuis le cache", type=button_type, key=f"resume_{cid}"):
        action = ("resume", cid)
    if right.button("Supprimer ce cache", key=f"del_{cid}"):
        action = ("delete", cid)
    return action


def render_final_result(state: dict, upload_drive: bool = False, from_cache_view: bool = False) -> None:
    df = state.get("merged_obj")
    if df is None:
        st.error("Le résultat en cache est vide.")
        return

    st.markdown("---")
    st.markdown("## ✨ Plan final")
    if from_cache_view:
        st.caption(f"Résultat rechargé depuis le cache local ({format_cache_time(state.get('updated_at'))}).")
    if state.get("split"):
        details = ", ".join(f"{p.get('label')} ({p.get('detail')})" for p in state.get("parts") or [])
        st.caption(f"Plan fusionné des deux moitiés — {details}")
    if state.get("renumbered"):
        st.caption("La numérotation de la seconde moitié a été recollée sur la première lorsque les axes se chevauchaient ou redémarraient à 1.")
    if state.get("deduped_rows"):
        st.caption(f"{int(state['deduped_rows'])} ligne(s) identiques à la jonction des deux moitiés ont été retirées.")
    for part in state.get("parts") or []:
        for err in (part.get("errors") or [])[:3]:
            st.caption(f"{part.get('label')} : {err}")

    st.markdown(f"**Avis de l'IA** \n\n {state.get('quali_result') or ''}")
    tokens = state.get("tokens") or [0, 0]
    model_name = (state.get("settings") or {}).get("model")
    st.success(format_run_cost(model_name, tokens))
    display_df_markdown(df)

    try:
        excel_data = remplir_fichier_import(df)
        export_name = state.get("export_filename") or build_drive_filename(state.get("filename") or "import")
        state["export_filename"] = export_name

        do_upload = upload_drive and not state.get("drive_link")
        if not state.get("drive_link") and not upload_drive:
            do_upload = st.button("☁️ Envoyer sur Google Drive", key=f"drive_{state['id']}")

        if do_upload and not state.get("drive_link"):
            try:
                with st.spinner("☁️ Sauvegarde sur Google Drive..."):
                    drive_file = upload_excel_to_drive(excel_data, export_name)
                state["drive_link"] = drive_file.get("webViewLink")
                state["drive_name"] = drive_file.get("name", export_name)
                state["drive_error"] = None
                save_import_cache(state)
            except Exception as drive_err:
                state["drive_error"] = str(drive_err)
                save_import_cache(state)

        if state.get("drive_link"):
            st.success(
                f"✅ Fichier sauvegardé sur Google Drive : "
                f"[{state.get('drive_name') or export_name}]({state['drive_link']})"
            )
        elif state.get("drive_error"):
            st.warning(f"⚠️ Sauvegarde sur Google Drive impossible : {state['drive_error']}")

        excel_data.seek(0)
        excel_data_no_num = remplir_fichier_import(strip_numbering_from_df(df))
        excel_data_no_num.seek(0)
        dl_col1, dl_col2 = st.columns(2)
        with dl_col1:
            st.download_button(
                label="📥 Télécharger le fichier d'import rempli au format Excel",
                data=excel_data,
                file_name=export_name,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                type="primary",
                key=f"dl_{state['id']}",
            )
        with dl_col2:
            st.download_button(
                label="📥 Télécharger sans la numérotation des actions",
                data=excel_data_no_num,
                file_name=export_name,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                type="secondary",
                key=f"dl_nonum_{state['id']}",
            )
    except Exception as e:
        st.error(f"❌ Erreur lors du remplissage du fichier import : {e}")


def new_analysis_state(file_bytes: bytes, filename: str, file_type: str, split: bool, settings: dict) -> tuple[dict | None, str | None]:
    parts_raw, error = build_text_parts(file_bytes, filename, file_type, split)
    if error:
        return None, error
    now = datetime.now().isoformat(timespec="seconds")
    file_hash = hashlib.sha256(file_bytes).hexdigest()
    parts = []
    for raw in parts_raw:
        parts.append({
            "label": raw["label"],
            "detail": raw["detail"],
            "text": raw["text"],
            "split_note": raw.get("split_note") or "",
            "extract_done": False,
            "verify_done": False,
            "upgrade_done": False,
            "enrich_done": False,
            "errors": [],
            "df_obj": None,
        })
    state = {
        "id": cache_file_id(file_hash, split),
        "filename": filename,
        "file_hash": file_hash,
        "split": split,
        "created_at": now,
        "updated_at": now,
        "settings": settings,
        "parts": parts,
        "tokens": [0, 0],
        "merged_obj": None,
        "quali_result": None,
        "quali_done": False,
        "final_done": False,
        "drive_link": None,
        "drive_name": None,
        "drive_error": None,
        "export_filename": None,
        "renumbered": False,
        "deduped_rows": 0,
    }
    return state, None


# ==========================
# Interface utilisateur
# ==========================

# Toggle pour le type de fichier
file_type = st.segmented_control(
    "Type de fichier à importer",
    options=["PDF", "CSV / Excel"],
    default="PDF"
)

if file_type == "PDF":
    uploaded_file = st.file_uploader(
        "Glissez-déposez votre fichier PDF ici",
        type=['pdf'],
        help="Sélectionnez un fichier PDF à analyser",
        key="pdf_uploader"
    )
else:
    uploaded_file = st.file_uploader(
        "Glissez-déposez votre fichier CSV ou Excel ici",
        type=['csv', 'xlsx', 'xls'],
        help="Fichiers acceptés : .csv, .xlsx, .xls. Les fichiers Excel multi-onglets sont supportés.",
        key="csv_excel_uploader"
    )

split_pdf = False
if file_type == "PDF":
    split_pdf = st.toggle(
        "Couper le PDF en deux",
        value=False,
        key="split_pdf_toggle",
        help=(
            "Découpe le PDF en deux moitiés (par nombre de pages), lance les deux analyses "
            "en parallèle, puis fusionne les fiches. Utile quand le fichier est trop volumineux."
        ),
    )
    if split_pdf and uploaded_file is not None:
        st.caption(describe_pdf_split(uploaded_file.getvalue()))
    elif uploaded_file is not None and getattr(uploaded_file, "size", 0) >= 3_000_000:
        st.caption("Fichier volumineux : activez « Couper le PDF en deux » si une seule analyse est trop lourde pour le modèle.")

precisions = st.text_area(
    "Précisions",
    height=300,
    placeholder="Ajoutez des précisions supplémentaires si nécessaire. Vous pouvez ici définir une strucutre spécifique, certaines règles à respecter, donner du contexte, etc. Cliquez sur Ctrl+Enter pour valider."
)

# Choix du modèle
gemini_model = st.segmented_control(
    "Modèle",
    options=["gemini-4-argon", "gemini-3.8-flash", "gemini-3-pro-preview", "gemini-2.5-pro", MISTRAL_MODEL],
    default="gemini-2.5-pro"
)

avec_sous_actions = st.toggle("Avec sous-actions", value=True, help="Si désactivé, les sous-actions ne seront pas extraites ni enrichies.")
avec_verifications = st.toggle("Vérifications", value=(file_type == "PDF"), help="Désactiver pour les fichiers simples (CSV, petits PDF). Ignore la vérification et la consolidation des fiches actions.")

with st.expander("⚙️ Colonnes à remplir", expanded=False):
    st.caption(
        "Désactivez les colonnes que vous ne souhaitez pas faire remplir par l'IA "
        "pour soulager le modèle et améliorer la qualité du reste."
    )
    _toggle_cols = st.columns(3)
    column_toggles: dict[str, bool] = {}
    for _i, (_label, _df_col, _json_key) in enumerate(TOGGLABLE_COLUMNS):
        with _toggle_cols[_i % 3]:
            column_toggles[_df_col] = st.toggle(
                _label, value=True, key=f"col_toggle_{_df_col}"
            )

disabled_columns = [c for c, on in column_toggles.items() if not on]
disabled_json_keys = [
    json_key
    for (_, df_col, json_key) in TOGGLABLE_COLUMNS
    if json_key is not None and df_col in disabled_columns
]

analysis_settings = {
    "model": gemini_model or "gemini-2.5-pro",
    "precisions": precisions or "",
    "avec_sous_actions": bool(avec_sous_actions),
    "avec_verifications": bool(avec_verifications),
    "disabled_columns": list(disabled_columns),
    "disabled_json_keys": list(disabled_json_keys),
    "file_type": file_type or "PDF",
}

file_hash = None
file_bytes = None
if uploaded_file is not None:
    file_bytes = uploaded_file.getvalue()
    file_hash = hashlib.sha256(file_bytes).hexdigest()
    st.success(f"✅ Fichier chargé : {uploaded_file.name}")

caches = list_import_caches()
target_id = cache_file_id(file_hash, bool(split_pdf)) if file_hash else None
if file_hash:
    matched = [c for c in caches if c.get("file_hash") == file_hash]
    others = [c for c in caches if c.get("file_hash") != file_hash]
    visible = matched
    hidden = others[:5]
else:
    visible = caches[:5]
    hidden = []

chosen = None
if visible:
    st.markdown("#### Analyses enregistrées")
    for index, meta in enumerate(visible):
        with st.container(border=True):
            if target_id and meta.get("id") == target_id:
                st.caption("Ce cache correspond au fichier et au mode de découpe actuellement choisis.")
            hit = render_cache_card(meta, primary=(index == 0))
            if hit:
                chosen = hit

if hidden:
    with st.expander("Autres analyses en cache"):
        for meta in hidden:
            with st.container(border=True):
                hit = render_cache_card(meta, primary=False)
                if hit:
                    chosen = hit

start_button = False
if uploaded_file is not None:
    has_matching_cache = any(c.get("id") == target_id for c in caches)
    if has_matching_cache:
        start_button = st.button(
            "Relancer depuis le début (remplace le cache)",
            type="secondary",
            key="start_analysis",
        )
    else:
        start_button = st.button("🚀 Lancer l'analyse", type="primary", key="start_analysis")
elif not visible:
    label = "PDF" if file_type == "PDF" else "CSV ou Excel"
    st.info(f"👆 Veuillez charger un fichier {label} pour commencer")

shown_result = False

if chosen and chosen[0] == "delete":
    delete_import_cache(chosen[1])
    if st.session_state.get("import_show_cache") == chosen[1]:
        st.session_state.pop("import_show_cache", None)
    st.rerun()
elif chosen and chosen[0] == "show":
    st.session_state["import_show_cache"] = chosen[1]
    loaded = load_import_cache(chosen[1])
    if loaded is None:
        st.error("Ce cache est illisible ou a déjà été supprimé.")
    else:
        render_final_result(loaded, upload_drive=False, from_cache_view=True)
        shown_result = True
elif chosen and chosen[0] == "resume":
    st.session_state.pop("import_show_cache", None)
    loaded = load_import_cache(chosen[1])
    if loaded is None:
        st.error("Ce cache est illisible ou a déjà été supprimé.")
    else:
        cached_model = (loaded.get("settings") or {}).get("model")
        if cached_model and cached_model != (gemini_model or "gemini-2.5-pro"):
            st.caption(
                f"Cette reprise utilise le modèle enregistré ({cached_model}) "
                "et les réglages stockés avec le cache."
            )
        loaded = run_import_pipeline(loaded, resuming=True)
        if loaded.get("final_done"):
            st.session_state["import_show_cache"] = loaded["id"]
            render_final_result(loaded, upload_drive=True, from_cache_view=False)
            shown_result = True
elif start_button:
    st.session_state.pop("import_show_cache", None)
    with st.spinner("📖 Lecture du fichier..."):
        state, error = new_analysis_state(
            file_bytes,
            uploaded_file.name,
            file_type or "PDF",
            bool(split_pdf) if file_type == "PDF" else False,
            analysis_settings,
        )
    if error or state is None:
        st.error("❌ Erreur lors de l'extraction du texte du fichier")
        st.error(error or "Texte vide")
    else:
        total_chars = sum(len(part.get("text") or "") for part in state["parts"])
        if total_chars < 20:
            st.error("Le texte extrait est vide ou trop court pour être analysé.")
        else:
            st.success(f"✅ Texte extrait : {total_chars:,} caractères")
            for part in state["parts"]:
                st.caption(f"{part['label']} ({part['detail']}) : {len(part.get('text') or ''):,} caractères")
            save_import_cache(state)
            state = run_import_pipeline(state, resuming=False)
            if state.get("final_done"):
                st.session_state["import_show_cache"] = state["id"]
                render_final_result(state, upload_drive=True, from_cache_view=False)
                shown_result = True

if not shown_result:
    show_id = st.session_state.get("import_show_cache")
    if show_id and file_hash:
        shown_meta = next((c for c in caches if c.get("id") == show_id), None)
        if shown_meta and shown_meta.get("file_hash") != file_hash:
            st.session_state.pop("import_show_cache", None)
            show_id = None
    if show_id and not (chosen and chosen[0] == "delete"):
        loaded = load_import_cache(show_id)
        if loaded and loaded.get("final_done"):
            render_final_result(loaded, upload_drive=False, from_cache_view=True)
        elif loaded is None:
            st.session_state.pop("import_show_cache", None)
