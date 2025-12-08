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
2 En cas de pluralité d’entités, les lister séparées par une virgule et un espace
3 "budget" ne doit contenir que des chiffres sans séparateur ou la valeur vide
4 Si "statut" n’est pas exactement dans la liste autorisée, laisser ""

Rappel de robustesse
• Si le document fournit des numérotations et des titres, les réutiliser strictement
• Si des titres existent sans numéro, générer des numéros cohérents et stables
• Si la position d’une action parmi plusieurs sous axes demeure ambiguë, laisser vides les champs d’appartenance incertains plutôt que de forcer un rattachement

Quelques précisions qui peuvent notamment s'avérer très importantes si elles contiennent des informations sur la structure du plan :
{precisions}

Voici le texte à analyser :
{texte_pdf_a_analyser}  
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

def display_result(result_text, mode_json):
    """Affiche le résultat en mode structuré (axes > sous-axes > actions)"""
    if mode_json:
        try:
            # Tenter de parser le JSON
            # D'abord, nettoyer le texte (enlever les balises markdown si présentes)
            cleaned_text = result_text.strip()
            if cleaned_text.startswith("```json"):
                cleaned_text = cleaned_text[7:]
            if cleaned_text.startswith("```"):
                cleaned_text = cleaned_text[3:]
            if cleaned_text.endswith("```"):
                cleaned_text = cleaned_text[:-3]
            cleaned_text = cleaned_text.strip()
            
            # Parser le JSON
            data = json.loads(cleaned_text)
            
            # Créer le dataframe pour garder les données
            if isinstance(data, list):
                df = pd.DataFrame(data)
                
                # Affichage structuré par axes et sous-axes
                axes = df["axe"].unique()
                
                for axe in axes:
                    st.markdown(f"## {axe}")
                    
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
                                st.markdown("---")
                
                # Afficher aussi le dataframe en dessous pour référence
                with st.expander("📊 Voir le tableau complet", expanded=False):
                    st.dataframe(df, use_container_width=True, height=600)
            else:
                st.json(data)
        except json.JSONDecodeError as e:
            st.error(f"❌ Erreur de parsing JSON : {str(e)}")
            st.markdown("**Texte brut reçu :**")
            st.text(result_text)
        except Exception as e:
            st.error(f"❌ Erreur lors de l'affichage : {str(e)}")
            st.markdown("**Texte brut reçu :**")
            st.text(result_text)
    else:
        # Mode normal : afficher le texte tel quel
        st.markdown(result_text)

async def query_claude(user_prompt):
    """Interroge Claude avec streaming asynchrone"""
    start_time = time.time()
    print(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] 🤖 Claude START")
    try:
        async with claude_client.messages.stream(
            model="claude-sonnet-4-5-20250929",
            max_tokens=64000,
            temperature=0.2,
            messages=[{"role": "user", "content": user_prompt}]
        ) as stream:
            parts = []
            async for text in stream.text_stream:
                parts.append(text)  # Récupération des chunks au fur et à mesure
            reponse = "".join(parts)  # Assemblage de la réponse complète
            
            # Récupérer les tokens utilisés
            final_message = await stream.get_final_message()
            tokens = final_message.usage.output_tokens if hasattr(final_message, 'usage') else 0
            
        elapsed = time.time() - start_time
        print(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] ✅ Claude END ({elapsed:.1f}s, {tokens} tokens)")
        return reponse, elapsed, tokens
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] ❌ Claude ERROR")
        return f"Erreur Claude: {str(e)}", elapsed, 0

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
        tokens = 0
        last_chunk = None
        async for chunk in stream:
            if hasattr(chunk, 'text') and chunk.text:
                parts.append(chunk.text)
            last_chunk = chunk
        
        # Récupérer les tokens du dernier chunk
        if last_chunk and hasattr(last_chunk, 'usage_metadata'):
            tokens = last_chunk.usage_metadata.candidates_token_count if hasattr(last_chunk.usage_metadata, 'candidates_token_count') else 0
        
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
            tokens = response.usage_metadata.candidates_token_count if hasattr(response, 'usage_metadata') and hasattr(response.usage_metadata, 'candidates_token_count') else 0
            print(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] ✅ Gemini END (fallback) ({elapsed:.1f}s, {tokens} tokens)")
            return str(response.text), elapsed, tokens
        except Exception as e2:
            elapsed = time.time() - start_time
            return f"Erreur Gemini: {str(e2)}", elapsed, 0


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
gemini_model = st.segmented_control(
    "Modèle Gemini",
    options=["gemini-3-pro-preview", "gemini-2.5-pro"],
    default="gemini-2.5-pro"
)

# Mode test (tronque le texte à 10 000 caractères)
mode_test = st.toggle("🧪 Mode test (30 000 caractères max)", value=False)

mode_json = True # Avant on pouvait choisir, maintenant on force à True. On pourra revenir dessus si besoin

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

            selected_prompt = custom_prompt
            
            user_prompt = selected_prompt.replace("{precisions}", precisions).replace("{texte_pdf_a_analyser}", extracted_text)

            with st.spinner("🌀 Interrogation de Gemini. Cela peut prendre quelques minutes..."):
                gemini_result, elapsed_time, tokens_count = asyncio.run(query_gemini(user_prompt, gemini_model))
                st.info(f"✨ Gemini : {elapsed_time:.1f}s | {tokens_count:,} tokens")
            
            # Afficher les résultats
            if gemini_result and not gemini_result.startswith("Erreur"):
                st.success("✅ Analyse terminée !")
                
                st.markdown("---")
                st.markdown("## ✨ Résultats")
                
                st.markdown(f"### Gemini ({gemini_model})")
                display_result(gemini_result, mode_json)
            else:
                st.error(f"❌ Erreur lors de l'analyse : {gemini_result}")
                
        
        else:
            st.error(f"❌ Erreur lors de l'extraction du texte du {file_type}")
            st.error(extracted_text)
else:
    st.info(f"👆 Veuillez charger un fichier {file_type} pour commencer")

