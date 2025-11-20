import streamlit as st
import anthropic
import openai
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

st.set_page_config(layout="wide")
st.title("✨ Import des plans :blue-badge[:material/experiment: Beta]")

# Configuration des APIs
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialisation des clients async
claude_client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)
openai_client = openai.AsyncOpenAI(api_key=OPENAI_API_KEY)
gemini_client = genai.Client(api_key=GOOGLE_API_KEY)

# Prompt personnalisé
custom_prompt = """
Vous êtes un agent d’extraction documentaire spécialisé dans les plans d’actions de transition écologique des collectivités, y compris les PCAET.

Contexte du fichier en entrée
Le texte fourni est un document de plan d’actions d’une collectivité. Un plan est structuré en axes, sous axes, actions et parfois sous actions. Il peut aussi contenir des sous sous axes si cela améliore la clarté du regroupement des actions. Le contenu peut être issu d’un PDF converti avec des artefacts de mise en page. Certaines rubriques comme budget, service pilote ou statut ne sont pas toujours explicites.

Objectif
Analyser le texte ci dessous et extraire toutes les actions, en reconstruisant la hiérarchie axe puis sous axe puis action, et en ajoutant des sous actions si nécessaire. L’agent décide librement d’introduire des sous sous axes lorsque cela correspond clairement à la structure du texte source. Axes, sous axes et actions sont obligatoires. Les sous actions et les sous sous axes sont optionnels.

Sortie attendue
1 Répondre uniquement avec un tableau JSON valide
2 Ne rien ajouter avant ni après le JSON
3 Ne pas utiliser de balises Markdown

Schéma des objets du tableau
Chaque entrée du tableau est un objet avec exactement ces champs
[
 "axe",
 "sous-axe",
 "sous-sous-axe",
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
• "sous-sous-axe" est une chaîne ou la valeur vide
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
• Sous sous axe. Regroupement fin optionnel à l’intérieur d’un sous axe si le texte source présente un niveau intermédiaire stable. Exemple "Développer les mobilités actives"
• Action. Mesure opérationnelle unique qui peut être mise en œuvre et suivie. Elle a un titre court et une description synthétique
• Sous action. Etape ou brique concrète qui détaille la mise en œuvre d’une action. Les sous actions sont listées dans "sous-actions"

Hiérarchie et numérotation
1 Conserver strictement les libellés exacts du texte source lorsque la numérotation et les titres existent
2 Lorsque le texte ne fournit pas de numérotation explicite, construire une numérotation stable et cohérente selon la règle suivante
   On note les axes "n".
   On note les sous axes "n.X".
   On note les sous sous axes "n.X.Y"
   On note les actions "n.X.Y.Z" ou "n.X.Z" si le sous sous axe n'existe pas
3 "axe" doit être formaté exactement "Axe n : Titre de l’axe"
4 "sous-axe" doit être formaté exactement "n.X  Titre du sous-axe"
5 "sous-sous-axe" si présent doit être formaté exactement "n.X.Y  Titre du sous-sous-axe". Sinon mettre ""
6 "titre" doit être formaté "n.X.Y.Z Titre de l’action" ou "n.X.Z Titre de l’action" si le sous sous axe n'existe pas
7 Un sous axe ou un sous sous axe doit avoir un nom complet. Il ne peut pas être uniquement un nombre
8 Pour un même identifiant hiérarchique le libellé doit être identique partout

Tâches obligatoires et ordre d’exécution
1 Normalisation du texte source
   • Retirer uniquement les artefacts manifestes de conversion comme "Unnamed" ou des mots isolés insérés au milieu d’une phrase
   • Conserver l’orthographe et les majuscules des noms propres et sigles
2 Relevé de structure
   • Repérer les axes puis les sous axes
   • Identifier un éventuel niveau sous sous axe lorsque le texte le justifie clairement
3 Extraction des actions
   • Lister chaque action avec un titre court et une description synthétique fidèle au texte
   • Lorsque le texte présente des puces, des sous parties ou des verbes d’exécution multiples rattachés à une même action, créer des sous actions dans "sous-actions" comme une liste de chaînes
4 Rattachement hiérarchique
   • Associer chaque action à son sous axe et à son axe. Associer aussi à un sous sous axe si pertinent, sinon laisser ""
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
7 Ordre de tri. Le tableau doit être trié selon la hiérarchie axe puis sous axe puis sous sous axe puis ordre des actions

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
 "sous-sous-axe": "",
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

Quelques précisions
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
    """Extrait le texte d'un fichier CSV"""
    try:
        df = pd.read_csv(csv_file, sep=';')
        
        # Informations générales
        text = f"# Fichier CSV\n\n"
        text += f"**Dimensions :** {len(df)} lignes × {len(df.columns)} colonnes\n\n"
        text += f"**Colonnes :** {', '.join(df.columns)}\n\n"
        
        # Types de données
        text += "**Types de données :**\n"
        for col, dtype in df.dtypes.items():
            text += f"  - {col}: {dtype}\n"
        text += "\n"

        text += "**Contenu complet :**\n\n"
        text += df.to_string(index=False)
        
        return text
    except Exception as e:
        return f"Erreur lors de la lecture du CSV : {str(e)}"

def display_result(result_text, mode_json):
    """Affiche le résultat en mode JSON (dataframe) ou texte normal"""
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
            
            # Afficher en dataframe si c'est une liste
            if isinstance(data, list):
                df = pd.DataFrame(data)
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

async def query_chatgpt(user_prompt):
    """Interroge ChatGPT avec streaming asynchrone"""
    start_time = time.time()
    print(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] 💬 ChatGPT START")
    if False:
        # Utiliser le streaming pour la réponse -> SKIP POUR L'INSTANT CAR IL FAUT UNE VERIFICATION SUR OPEN AI DE L'ORG
        stream = await openai_client.responses.create(
            model="gpt-5",
            input=user_prompt,
            max_output_tokens=128000,
            stream=True
        )
        
        parts = []
        tokens = 0
        async for chunk in stream:
            if hasattr(chunk, 'output_text') and chunk.output_text:
                parts.append(chunk.output_text)
            elif hasattr(chunk, 'delta') and hasattr(chunk.delta, 'content') and chunk.delta.content:
                parts.append(chunk.delta.content)
            # Récupérer les tokens si disponible dans le dernier chunk
            if hasattr(chunk, 'usage') and hasattr(chunk.usage, 'output_tokens'):
                tokens = chunk.usage.output_tokens
        
        reponse = "".join(parts)
        elapsed = time.time() - start_time
        print(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] ✅ ChatGPT END ({elapsed:.1f}s, {tokens} tokens)")
        return reponse, elapsed, tokens
    else:
        #print(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] ❌ ChatGPT ERROR: {str(e)}")
        # Si le streaming ne fonctionne pas, fallback sur l'API standard
        try:
            response = await openai_client.responses.create(
                model="gpt-5",
                input=user_prompt,
                max_output_tokens=128000
            )
            elapsed = time.time() - start_time
            tokens = response.usage.output_tokens if hasattr(response, 'usage') and hasattr(response.usage, 'output_tokens') else 0
            print(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] ✅ ChatGPT END ({elapsed:.1f}s, {tokens} tokens)")
            return str(response.output_text), elapsed, tokens
        except Exception as e2:
            elapsed = time.time() - start_time
            return f"Erreur ChatGPT: {str(e2)}", elapsed, 0

async def query_gemini(user_prompt):
    """Interroge Gemini avec streaming asynchrone"""
    start_time = time.time()
    print(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] ✨ Gemini START")
    try:
        # Utiliser le streaming pour la réponse
        stream = await gemini_client.aio.models.generate_content_stream(
            model='gemini-3-pro-preview',
            contents=user_prompt,
            config=types.GenerateContentConfig(
                temperature=0.3,
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
                model='gemini-2.5-pro',
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

            selected_prompt = custom_prompt
            
            user_prompt = selected_prompt.replace("{precisions}", precisions).replace("{texte_pdf_a_analyser}", extracted_text)

            with st.spinner("🌀 Interrogation des modèles en parallèle. Cela peut prendre quelques minutes..."):
                # Fonction async pour exécuter les trois modèles en parallèle
                async def run_all_models():
                    # Lancer les trois requêtes en parallèle
                    print(f"\n[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] 🚀 Démarrage de l'analyse parallèle")
                    results_tuple = await asyncio.gather(
                        query_claude(user_prompt),
                        query_chatgpt(user_prompt),
                        query_gemini(user_prompt),
                        return_exceptions=True
                    )
                    print(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] 🏁 Tous les modèles ont terminé\n")
                    
                    # Décomposer les tuples (réponse, temps, tokens)
                    results = {}
                    times = {}
                    tokens = {}
                    
                    for idx, model_name in enumerate(["Claude", "ChatGPT", "Gemini"]):
                        if isinstance(results_tuple[idx], Exception):
                            results[model_name] = f"Erreur : {str(results_tuple[idx])}"
                            times[model_name] = 0
                            tokens[model_name] = 0
                        elif isinstance(results_tuple[idx], tuple) and len(results_tuple[idx]) == 3:
                            results[model_name] = results_tuple[idx][0]
                            times[model_name] = results_tuple[idx][1]
                            tokens[model_name] = results_tuple[idx][2]
                        else:
                            results[model_name] = str(results_tuple[idx])
                            times[model_name] = 0
                            tokens[model_name] = 0
                    
                    return results, times, tokens
                
                # Exécuter les requêtes async
                results, times, tokens = asyncio.run(run_all_models())
                
                # Afficher les temps et tokens individuels
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.info(f"🤖 Claude : {times['Claude']:.1f}s | {tokens['Claude']:,} tokens")
                with col2:
                    st.info(f"💬 ChatGPT : {times['ChatGPT']:.1f}s | {tokens['ChatGPT']:,} tokens")
                with col3:
                    st.info(f"✨ Gemini : {times['Gemini']:.1f}s | {tokens['Gemini']:,} tokens")
            
            # Afficher les résultats
            if results:
                st.success("✅ Analyse terminée !")
                
                # Affichage des résultats dans des onglets
                st.markdown("---")
                st.markdown("## ✨ Résultats")
                
                tab1, tab2, tab3 = st.tabs(["🌀 Claude", "💬 ChatGPT", "💫 Gemini"])
                
                with tab1:
                    st.markdown("### Claude Sonnet 4.5")    
                    claude_result = results.get("Claude", "Pas de réponse")
                    
                    # Afficher selon le mode
                    display_result(claude_result, mode_json)
                
                with tab2:
                    st.markdown("### ChatGPT (GPT-5)")
                    chatgpt_result = results.get("ChatGPT", "Pas de réponse")
                    
                    # Afficher selon le mode
                    display_result(chatgpt_result, mode_json)
                
                with tab3:
                    st.markdown("### Gemini 2.5 Pro")
                    gemini_result = results.get("Gemini", "Pas de réponse")
                    
                    # Afficher selon le mode
                    display_result(gemini_result, mode_json)
                
                # Statistiques de comparaison
                st.markdown("---")
                st.markdown("### 📈 Statistiques")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    claude_words = len(results.get("Claude", "").split())
                    st.metric("Mots (Claude)", claude_words)
                
                with col2:
                    gpt_words = len(results.get("ChatGPT", "").split())
                    st.metric("Mots (ChatGPT)", gpt_words)
                
                with col3:
                    gemini_words = len(results.get("Gemini", "").split())
                    st.metric("Mots (Gemini)", gemini_words)
        
        else:
            st.error(f"❌ Erreur lors de l'extraction du texte du {file_type}")
            st.error(extracted_text)
else:
    st.info(f"👆 Veuillez charger un fichier {file_type} pour commencer")

