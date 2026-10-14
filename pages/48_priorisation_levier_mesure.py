import streamlit as st

st.set_page_config(
    page_title="Classification levier × mesure",
    page_icon="📌",
    layout="wide",
)

import hashlib
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from typing import Any

import anthropic
import pandas as pd
from sqlalchemy import text

from utils.db import get_engine, get_engine_prod

# Haiku 4.5 ignore cache_control sous 4096 tokens. Le prompt système est
# dimensionné au-dessus de ce seuil ; ce plancher en caractères laisse une marge
# si le tokenizer est particulièrement efficace.
_MIN_CHARS_PROMPT = 22_000
_MODELE_HAIKU = "claude-haiku-4-5"
_WORKERS = 12
_MAX_TENTATIVES = 3
_MAX_TOKENS = 800

_USAGE_LOCK = Lock()
_USAGES: list[dict[str, int]] = []
# Déposé juste avant l'appel à classification_en_cache, pour n'y écrire qu'un succès.
_A_MEMORISER: dict[tuple[str, str], tuple[tuple[str, int], ...]] = {}

LEVIERS = """
Changement chaudières fioul + rénovation (résidentiel)
Changement chaudières gaz + rénovation (résidentiel)
Sobriété des bâtiments (résidentiel)
Changement de chaudière à fioul (tertiaire)
Changement de chaudière à gaz (tertiaire)
Sobriété et isolation des bâtiments (tertiaire)
Réduction des déplacements
Covoiturage
Vélo et transport en commun
Véhicules électriques
Efficacité et carburants décarbonés des véhicules privés
Bus et cars décarbonés
Fret décarboné et multimodalité
Efficacité et sobriété logistique
Bâtiments & Machines agricoles
Elevage durable
Changements de pratiques de fertilisation azotée
Production Industrielle
Captage de méthane dans les ISDND
Prévention des déchets
Valorisation matière des déchets
Gestion des forêts et produits bois
Pratiques stockantes
Gestion des haies
Gestion des prairies
Sobriété foncière
Electricité renouvelable
Biogaz
Réseaux de chaleur décarbonés
"""

LEVIERS_LIST = [ligne.strip() for ligne in LEVIERS.strip().split("\n") if ligne.strip()]
LEVIERS_SET = set(LEVIERS_LIST)
VALID_CATEGORIES = {1, 2, 3, 4, 5, 6}

REQUETE_MESURES = r"""
SELECT
    a4.action_id,
    concat(a1.nom, ' - ', a2.nom, ' - ', a3.nom, ' : ', a4.nom) AS nom
FROM action_definition a4
LEFT JOIN action_definition a3
       ON a3.referentiel = a4.referentiel
      AND a3.action_id = regexp_replace(a4.action_id, '\.[^.]+$', '')
LEFT JOIN action_definition a2
       ON a2.referentiel = a4.referentiel
      AND a2.action_id = regexp_replace(a4.action_id, '(\.[^.]+){2}$', '')
LEFT JOIN action_definition a1
       ON a1.referentiel = a4.referentiel
      AND a1.action_id = regexp_replace(a4.action_id, '(\.[^.]+){3}$', '')
WHERE a4.action_id ~ '^[^.]+(\.[^.]+){3}$'
and a4.referentiel in ('cae', 'eci', 'te')
ORDER BY a4.action_id
"""

# Libellé exact du levier, puis lecture opérationnelle pour un intitulé sans description.
_GLOSSAIRE: tuple[tuple[str, str], ...] = (
    (
        "Changement chaudières fioul + rénovation (résidentiel)",
        "Sortie du fioul dans les logements des habitants, presque toujours couplée à des "
        "travaux sur le bâti résidentiel privé. Retenir si l'intitulé vise le fioul, la cuve "
        "ou la conversion du parc de maisons et d'immeubles chauffés au fioul. Une aide "
        "financière aux ménages est la catégorie 3, des travaux chez l'habitant la catégorie 1, "
        "un conseil sans flux d'argent la catégorie 6, une prescription d'urbanisme la catégorie 2, "
        "un dispositif de pilotage la catégorie 4. Le patrimoine communal, le gaz, le réseau de "
        "chaleur et la simple baisse du chauffage relèvent d'autres leviers.",
    ),
    (
        "Changement chaudières gaz + rénovation (résidentiel)",
        "Remplacement des chaudières gaz des logements privés, avec rénovation du logement. "
        "Retenir pour le gaz naturel, le propane ou la chaudière gaz des particuliers, pas pour "
        "le fioul ni pour une pompe à chaleur décrite sans énergie d'origine. Les aides aux "
        "ménages sont la catégorie 3, les travaux sur le parc privé la catégorie 1, l'information "
        "la catégorie 6. Une chaudière d'une école ou d'une mairie est tertiaire, pas résidentielle. "
        "Un raccordement à un réseau de chaleur se classe sur le levier réseau, pas ici.",
    ),
    (
        "Sobriété des bâtiments (résidentiel)",
        "Baisse des consommations du parc résidentiel sans substitution d'énergie : consignes "
        "de chauffage, suivi des consommations, extinction, petits gestes, accompagnement des "
        "occupants. Retenir pour l'habitat privé ou social quand le levier est le comportement "
        "ou le pilotage léger, pas l'isolation lourde ni le changement de chaudière. Une campagne "
        "auprès des habitants est souvent la catégorie 6. Une aide financière pour des thermostat "
        "ou des kits est la catégorie 3. Le tertiaire et le patrimoine propre de la collectivité "
        "vont sur le levier de sobriété tertiaire, en catégorie 5 si c'est le fonctionnement interne.",
    ),
    (
        "Changement de chaudière à fioul (tertiaire)",
        "Sortie du fioul des bâtiments tertiaires : bureaux, commerces, écoles, gymnases, mairie, "
        "patrimoine public. Retenir quand le fioul est nommé dans un bâtiment qui n'est pas un "
        "logement. Si le bâtiment appartient à la collectivité, la catégorie est 5. S'il s'agit "
        "d'un équipement ou d'une aide destinés aux acteurs économiques du territoire, catégories "
        "1 ou 3. Ne pas confondre avec le résidentiel, le gaz tertiaire, ni avec un réseau de chaleur "
        "qui remplace la chaudière : dans ce dernier cas le levier principal est le réseau.",
    ),
    (
        "Changement de chaudière à gaz (tertiaire)",
        "Remplacement des chaudières gaz du tertiaire privé ou public. Même frontière que le fioul "
        "tertiaire : patrimoine de la collectivité en catégorie 5, acteurs du territoire en 1 ou 3, "
        "règle d'urbanisme en 2, simple information en 6. Ne pas l'utiliser pour les logements, "
        "ni pour une isolation sans changement de chaudière, ni pour le biogaz injecté ou un réseau "
        "de chaleur. Le libellé exact porte « chaudière » au singulier et « gaz », à ne pas reformuler.",
    ),
    (
        "Sobriété et isolation des bâtiments (tertiaire)",
        "Isolation, rénovation de l'enveloppe et sobriété d'usage des bâtiments tertiaires, sans "
        "que le cœur de l'intitulé soit le changement de chaudière. Écoles, bureaux, commerces, "
        "équipements. Le patrimoine communal se classe en catégorie 5. Une aide aux entreprises "
        "ou commerçants pour isoler est la catégorie 3, des travaux sur un équipement ouvert au "
        "public qui n'est pas le fonctionnement interne peuvent être la catégorie 1. L'habitat "
        "reste sur les leviers résidentiels.",
    ),
    (
        "Réduction des déplacements",
        "Moins de kilomètres parcourus : télétravail, rapprochement des services, urbanisme des "
        "courtes distances, plans de mobilité qui suppriment des trajets, livraison mutualisée "
        "vue comme moins de déplacements. Retenir quand l'intitulé réduit le besoin de se déplacer, "
        "pas quand il reporte le trajet vers le vélo, le bus ou le covoiturage. Une zone à faibles "
        "émissions ou un document d'urbanisme est la catégorie 2. Un service interne de la "
        "collectivité qui limite les déplacements des agents est la catégorie 5.",
    ),
    (
        "Covoiturage",
        "Partage d'une voiture particulière : aires, voies, application, incitation, animation. "
        "Retenir seulement si le covoiturage est nommé ou nettement décrit. Une aire de covoiturage "
        "est la catégorie 1, une subvention aux conducteurs la catégorie 3, une campagne la "
        "catégorie 6. Ne pas y mettre l'autopartage de véhicules municipaux (souvent exemplarité "
        "ou véhicules électriques), ni le vélo, ni les transports en commun.",
    ),
    (
        "Vélo et transport en commun",
        "Report modal vers le vélo, la marche outillée comme alternative à la voiture, le bus, "
        "le car, le train du quotidien : pistes, stationnement vélo, pôles d'échanges, fréquence, "
        "tarification des réseaux. Une piste cyclable est la catégorie 1. Une aide à l'achat de "
        "vélos est la catégorie 3. Le plan de circulation opposable est la catégorie 2. La flotte "
        "de bus décarbonée se classe plutôt sur « Bus et cars décarbonés ». Les vélos des agents "
        "municipaux seuls sont la catégorie 5.",
    ),
    (
        "Véhicules électriques",
        "Électrification des voitures : bornes, aides à l'achat de véhicules électriques pour les "
        "ménages et les entreprises, conversion d'une flotte. Bornes ouvertes au public : catégorie "
        "1. Prime aux habitants : catégorie 3. Flotte municipale : catégorie 5, et ce levier plutôt "
        "que la simple exemplarité abstraite, parce que le mécanisme CO2 est bien l'électrification. "
        "Un bus électrique va sur « Bus et cars décarbonés ». Un vélo à assistance électrique va "
        "sur le levier vélo, sauf si l'intitulé est clairement une voiture.",
    ),
    (
        "Efficacité et carburants décarbonés des véhicules privés",
        "Voitures particulières qui restent thermiques mais consomment moins, ou passent à un "
        "carburant moins carboné (hors électrification, qui a son levier). Éco-conduite des "
        "particuliers, renouvellement vers des véhicules plus sobres, critique des SUV, biocarburant "
        "pour les voitures. Ne pas y mettre les bus, le fret, ni les bornes électriques. Une "
        "formation des habitants est la catégorie 6. Une prime à la conversion hors électrique "
        "est la catégorie 3.",
    ),
    (
        "Bus et cars décarbonés",
        "Motorisation des bus et cars : électrique, hydrogène, biogaz, renouvellement de la flotte "
        "de transport public. Retenir pour le matériel roulant de transport collectif, pas pour une "
        "piste cyclable ni pour la seule hausse de fréquence (cette hausse, si elle reporte la "
        "voiture, va vers « Vélo et transport en commun »). Un bus municipal scolaire peut être "
        "catégorie 5 s'il s'agit de la flotte propre, ou 1 si l'investissement est un service aux "
        "habitants. Le dépôt et les ouvrages restent cohérents avec ce levier s'ils servent ces bus.",
    ),
    (
        "Fret décarboné et multimodalité",
        "Marchandises : ferroutage, fleuve, mutualisation des livraisons, dernier kilomètre en "
        "vélo-cargo professionnel, zones de livraison. Retenir quand l'objet est le transport de "
        "biens, pas le déplacement des personnes. Une aire de livraison est la catégorie 1, un "
        "règlement d'accès poids lourds la catégorie 2, une aide aux entreprises la catégorie 3. "
        "L'optimisation d'un entrepôt sans report modal va plutôt vers la sobriété logistique.",
    ),
    (
        "Efficacité et sobriété logistique",
        "Moins de tonnes-kilomètres ou moins d'énergie à trafic de marchandises donné : taux de "
        "chargement, emballages, orga des tournées, sobriété des entrepôts. Distinct du report "
        "modal. Une charte avec les entreprises sans argent est souvent la catégorie 6 ou 4. "
        "Une subvention au matériel sobre est la catégorie 3. Ne pas y classer un plan vélo des "
        "habitants ni la prévention des déchets ménagers, même si les deux réduisent des flux.",
    ),
    (
        "Bâtiments & Machines agricoles",
        "Serres, hangars, blocs de traite, tracteurs, irrigation énergétique, séchoirs. Le levier "
        "porte sur l'énergie des bâtiments et engins de l'exploitation, pas sur le troupeau ni "
        "l'engrais. Une aide aux agriculteurs pour un tracteur ou une isolation de hangar est la "
        "catégorie 3. Le patrimoine non agricole de la commune n'y entre pas. Le libellé exact "
        "contient le signe &.",
    ),
    (
        "Elevage durable",
        "Cheptel, alimentation animale, gestion des effluents d'élevage, réduction du méthane "
        "entérique, pâturage vu comme pratique d'élevage. Le libellé officiel est « Elevage » "
        "sans accent. Ne pas y mettre la fertilisation des cultures (levier azote), les haies, "
        "ni les prairies si l'intitulé porte sur le couvert plutôt que sur l'animal. Un "
        "accompagnement des éleveurs sans subvention est la catégorie 6, une aide à l'investissement "
        "la catégorie 3.",
    ),
    (
        "Changements de pratiques de fertilisation azotée",
        "Moins d'azote minéral, meilleure date d'apport, légumineuses, couverture qui vise l'azote, "
        "matériel d'épandage de précision. Retenir si l'engrais ou l'azote est le sujet. Une MAEC "
        "ou une aide est la catégorie 3, une règle la catégorie 2, un conseil agricole la catégorie 6. "
        "Le stockage de carbone dans le sol sans enjeu azote va sur « Pratiques stockantes ». "
        "L'élevage et les machines ont leurs leviers.",
    ),
    (
        "Production Industrielle",
        "Procédés des sites industriels : chaleur de process, efficacité des usines, substitution "
        "d'énergie en industrie. Le P et le I sont en capitales dans le libellé exact. Retenir pour "
        "les entreprises industrielles, pas pour un commerce, un logement ou une ferme. Une aide "
        "à l'investissement usine est la catégorie 3, un club des industriels la catégorie 4 ou 6, "
        "une prescription la catégorie 2. Ne pas confondre avec le fret qui quitte l'usine.",
    ),
    (
        "Captage de méthane dans les ISDND",
        "Installations de stockage de déchets non dangereux : captage, torchère, valorisation du "
        "biogaz de décharge. Très étroit. Ne pas y mettre une collecte des biodéchets, un compostage "
        "ou une prévention. Un équipement de captage est la catégorie 1, son exploitation par la "
        "collectivité peut être la catégorie 5 si c'est son installation. Le biogaz agricole ou "
        "d'un méthaniseur territorial va sur le levier « Biogaz ».",
    ),
    (
        "Prévention des déchets",
        "Produire moins de déchets : réemploi, consigne, lutte contre le gaspillage, compostage "
        "domestique qui évite la collecte, stop pub. Distinct de la valorisation matière, qui traite "
        "un déchet déjà produit. Une recyclerie peut relever des deux si elle évite et si elle "
        "réemploie ; n'attribuer la prévention que si l'évitement est concret. Une ressourcerie "
        "municipale ouverte aux habitants est souvent la catégorie 1 ou 6. Le tri en déchetterie "
        "sans baisse à la source va vers la valorisation matière.",
    ),
    (
        "Valorisation matière des déchets",
        "Tri, recyclage, déchetterie, filières de matières, valorisation des biodéchets déjà "
        "collectés quand ils deviennent une matière. Retenir quand un déchet existe et est orienté "
        "vers une filière. Un centre de tri est la catégorie 1. Une redevance incitative est la "
        "catégorie 3. Ne pas y mettre le captage en ISDND ni une simple campagne « produire moins » "
        "sans filière.",
    ),
    (
        "Gestion des forêts et produits bois",
        "Forêt, sylviculture, bois d'œuvre, bois énergie vu comme produit forestier, renouvellement "
        "de peuplements. Retenir pour la forêt et le matériau bois. Une charte forestière est souvent "
        "la catégorie 2 ou 4. Le boisement de haies agricoles va sur « Gestion des haies » si l'objet "
        "est la haie, pas la forêt. Le chauffage au bois d'un logement, sans gestion forestière, "
        "n'est pas automatiquement ce levier.",
    ),
    (
        "Pratiques stockantes",
        "Pratiques agricoles qui stockent du carbone dans les sols : couverture, moins de labour, "
        "restitutions, agroforesterie intraparcellaire quand le sujet est le stock de carbone du sol. "
        "Ne pas y mettre l'azote si l'intitulé ne parle que d'engrais, ni une haie (levier haies), "
        "ni une prairie permanente (levier prairies) quand c'est le couvert herbacé qui est nommé. "
        "L'accompagnement des agriculteurs est la catégorie 6, l'aide la catégorie 3.",
    ),
    (
        "Gestion des haies",
        "Plantation, restauration et entretien de haies, souvent bocagères. Retenir si la haie est "
        "nommée. Une plantation chez des agriculteurs avec subvention est la catégorie 3, un "
        "chantier communal ouvert au territoire la catégorie 1, le plan de gestion la catégorie 2 "
        "ou 4. Ne pas basculer vers la forêt ni vers les prairies. Une haie dans la cour d'une école, "
        "sans enjeu bocager, est souvent trop faible pour ce levier.",
    ),
    (
        "Gestion des prairies",
        "Maintien ou restauration de prairies permanentes, retournement évité, pâturage vu comme "
        "gestion du couvert prairial. Distinct de l'élevage (l'animal et le méthane entérique) et "
        "des pratiques stockantes génériques. Une MAEC prairie est la catégorie 3. Un document "
        "d'urbanisme qui protège des prairies peut être la catégorie 2, et parfois aussi la sobriété "
        "foncière si l'enjeu principal est de ne pas artificialiser.",
    ),
    (
        "Sobriété foncière",
        "Moins d'artificialisation : densification, friches, zéro artificialisation, renaturation "
        "qui évite l'étalement, désimperméabilisation quand elle rend du sol. Un PLU qui réduit "
        "les droits à construire est la catégorie 2. Une opération d'aménagement est la catégorie 1. "
        "Ne pas y mettre une piste cyclable, ni une forêt gérée pour le bois. La renaturation d'une "
        "cour d'école du patrimoine communal peut être la catégorie 5 si elle ne porte que sur le "
        "foncier propre, mais le mécanisme CO2 de ce levier est bien la sobriété foncière.",
    ),
    (
        "Electricité renouvelable",
        "Solaire photovoltaïque, éolien, hydroélectricité. Le libellé exact commence par « Electricité » "
        "sans accent sur le E. Retenir pour la production d'électricité renouvelable. Ombrières et "
        "toitures ouvertes au territoire : catégorie 1. Prime aux particuliers : catégorie 3. Toiture "
        "de la mairie : catégorie 5. Le solaire thermique d'un réseau de chaleur va sur le levier "
        "réseau. Le biogaz qui fait de l'électricité se classe d'abord sur « Biogaz » si l'installation "
        "est un méthaniseur.",
    ),
    (
        "Biogaz",
        "Méthanisation agricole ou territoriale, injection, bioGNV produit localement. Distinct du "
        "captage de décharge et du réseau de chaleur, même si le biogaz peut alimenter l'un ou l'autre. "
        "Si l'intitulé est le méthaniseur, retenir ce levier. Une unité sur une exploitation aidée "
        "est la catégorie 3, un équipement public la catégorie 1 ou 5 selon qu'il sert le territoire "
        "ou le seul patrimoine. Ne pas y mettre un composteur de jardin.",
    ),
    (
        "Réseaux de chaleur décarbonés",
        "Réseau de chaleur, extension, densification, substitution de la chaleur fossile du réseau. "
        "Retenir quand le réseau ou la chaleur urbaine est le sujet. Les travaux de réseau sont la "
        "catégorie 1, un classement en réseau la catégorie 2, un raccordement subventionné la "
        "catégorie 3. Une chaudière fioul isolée, sans réseau, reste sur le levier chaudière. La "
        "géothermie ou la biomasse ne sont ce levier que si elles alimentent un réseau ou en sont "
        "explicitement la source.",
    ),
)


_EXEMPLES = """
Les lectures ci-dessous expliquent le classement. Elles ne font pas partie du format de réponse. Face à un intitulé, la réponse reste un JSON seul.

Exemple A — aménagement destiné aux habitants, un seul mécanisme.
Intitulé : Mobilités - Vélo - Infrastructures : Créer des pistes cyclables sécurisées entre les bourgs
Sortie : {"Vélo et transport en commun": [1]}
Lecture : l'objet est un ouvrage cyclable pour les habitants. Aucune subvention, aucun document d'urbanisme, aucune flotte municipale n'est nommé. La catégorie 3 serait une aide à l'achat, la 5 serait des vélos d'agents.

Exemple B — le même thème, mais le moyen est l'argent.
Intitulé : Mobilités - Vélo - Aides : Subventionner l'achat de vélos à assistance électrique pour les habitants
Sortie : {"Vélo et transport en commun": [3]}
Lecture : il y a un flux financier vers les habitants. Ce n'est pas une piste (catégorie 1) ni une simple campagne (catégorie 6). Le vélo à assistance reste sur le levier vélo, pas sur les véhicules électriques.

Exemple C — patrimoine propre, donc exemplarité, levier tertiaire.
Intitulé : Patrimoine - Bâtiments publics - Chauffage : Remplacer la chaudière fioul de l'hôtel de ville
Sortie : {"Changement de chaudière à fioul (tertiaire)": [5]}
Lecture : le bâtiment appartient à la collectivité. Le levier résidentiel serait faux. La catégorie 1 serait fausse parce que l'ouvrage n'est pas destiné aux usagers comme infrastructure ouverte : c'est le fonctionnement interne.

Exemple D — même énergie, mais chez l'habitant, avec deux mécanismes réellement écrits.
Intitulé : Habitat - Parc privé - Fioul : Aider les propriétaires à remplacer leur chaudière fioul et rénover le logement
Sortie : {"Changement chaudières fioul + rénovation (résidentiel)": [1, 3]}
Lecture : le texte dit à la fois des travaux chez l'habitant et une aide. Les deux catégories sont concrètes. Le levier tertiaire ne s'applique pas.

Exemple E — information trop générique pour retenir un levier.
Intitulé : Habitat - Rénovation - Conseil : Tenir une permanence pour orienter les ménages vers les aides à la rénovation
Sortie : {}
Lecture : informer sur des aides existantes n'est pas verser la subvention, donc ce n'est pas la catégorie 3. Le fioul, le gaz, le tertiaire ou l'isolation ne sont pas nommés. Sans levier sûr, l'objet reste vide. Une liste de catégories vide pour un levier nommé serait de toute façon interdite.

Exemple F — conseil ciblé, levier sûr, catégorie 6.
Intitulé : Habitat - Gaz - Accompagnement : Conseiller les ménages au remplacement de leur chaudière gaz
Sortie : {"Changement chaudières gaz + rénovation (résidentiel)": [6]}
Lecture : le gaz résidentiel est nommé. Le moyen est le conseil, pas un chèque et pas un chantier porté par la collectivité.

Exemple G — acte juridique, pas la gouvernance.
Intitulé : Urbanisme - Planification - PLU : Interdire les chaudières fioul dans le règlement du PLU
Sortie : {"Changement chaudières fioul + rénovation (résidentiel)": [2]}
Lecture : l'objet est le document opposable. Créer ensuite un comité de suivi du PLU serait la catégorie 4, sur un intitulé distinct.

Exemple H — gouvernance sans acte.
Intitulé : Climat - Pilotage - Instance : Installer un comité de suivi de la rénovation énergétique
Sortie : {}
Lecture : l'instance pilote, mais aucun levier CO2 n'est identifiable sans savoir si l'on parle de logements, de tertiaire, de fioul ou de gaz. La catégorie 4 supposerait d'abord un levier sûr. Ici le lien est trop indirect.

Exemple I — comité rattaché à un levier nommé.
Intitulé : Mobilités - Vélo - Gouvernance : Créer un comité vélo associant communes et associations
Sortie : {"Vélo et transport en commun": [4]}
Lecture : le levier vélo est clair et le moyen est le pilotage partenarial, pas un ouvrage.

Exemple J — deux leviers, parce que deux mécanismes CO2 sont écrits.
Intitulé : Mobilités - Alternatives à la voiture - Dispositifs : Ouvrir une aire de covoiturage et un abri vélos sécurisé au pôle d'échange
Sortie : {"Covoiturage": [1], "Vélo et transport en commun": [1]}
Lecture : les deux équipements sont concrets. On ne choisit pas un seul levier pour « faire simple ».

Exemple K — réduction des déplacements, pas le vélo.
Intitulé : Mobilités - Organisation - Services : Développer le télétravail et rapprocher les services publics des bourgs
Sortie : {"Réduction des déplacements": [1]}
Lecture : le trajet est évité. Aucun mode de report n'est décrit. Si l'intitulé ne portait que sur une charte interne des agents, la catégorie serait 5.

Exemple L — bus, pas le levier vélo ni les voitures électriques.
Intitulé : Transports - Réseau urbain - Matériel : Remplacer les bus diesel par des bus électriques
Sortie : {"Bus et cars décarbonés": [1]}
Lecture : le matériel de transport collectif est le mécanisme. La hausse de fréquence sans changement de motorisation irait vers « Vélo et transport en commun ».

Exemple M — flotte municipale électrique.
Intitulé : Administration - Moyens internes - Véhicules : Électrifier la flotte de véhicules de service
Sortie : {"Véhicules électriques": [5]}
Lecture : voitures de la collectivité. Catégorie 5. Le levier « efficacité des véhicules privés » serait faux : ce ne sont pas des véhicules privés, et le mécanisme est l'électricité.

Exemple N — fret, pas la logistique d'entrepôt.
Intitulé : Économie - Marchandises - Report modal : Aider les entreprises à basculer des camions vers le fret ferroviaire
Sortie : {"Fret décarboné et multimodalité": [3]}
Lecture : l'aide financière et le report modal sont écrits. L'optimisation du taux de chargement, elle, irait vers « Efficacité et sobriété logistique ».

Exemple O — prévention, pas la valorisation.
Intitulé : Déchets - Réduction à la source - Gaspillage : Former les cantines et les habitants à réduire le gaspillage alimentaire
Sortie : {"Prévention des déchets": [6]}
Lecture : le déchet est évité. Une déchetterie ou une consigne de tri irait vers la valorisation matière. La catégorie 6 convient à la formation. Si l'intitulé portait seulement sur la cantine municipale comme fonctionnement interne, la catégorie 5 serait envisageable ; ici les habitants sont inclus, donc 6.

Exemple P — captage ISDND, levier étroit.
Intitulé : Déchets - Installation de stockage - Gaz : Capter et brûler le biogaz de l'installation de stockage de déchets
Sortie : {"Captage de méthane dans les ISDND": [1]}
Lecture : le site est une ISDND. Un méthaniseur agricole aurait été « Biogaz ». Ne pas ajouter la valorisation matière.

Exemple Q — agriculture, trois leviers qu'il ne faut pas fusionner.
Intitulé : Agriculture - Pratiques - Azote : Conseiller les exploitants sur la réduction des engrais azotés minéraux
Sortie : {"Changements de pratiques de fertilisation azotée": [6]}
Lecture : l'azote est nommé. Ce n'est pas l'élevage, ni les machines, ni les pratiques stockantes, tant que le carbone du sol n'est pas le sujet.

Exemple R — haie nommée.
Intitulé : Bocage - Haies - Plantation : Subventionner la plantation de haies chez les agriculteurs
Sortie : {"Gestion des haies": [3]}
Lecture : la haie est l'objet et le moyen est la subvention. Ne pas déplacer vers la forêt ni vers les prairies.

Exemple S — solaire sur toit communal.
Intitulé : Énergie - Patrimoine - Électricité : Poser des panneaux photovoltaïques sur les toitures des écoles et de la mairie
Sortie : {"Electricité renouvelable": [5]}
Lecture : production d'électricité sur le patrimoine propre. Libellé exact du levier, avec E majuscule sans accent. Un réseau de chaleur solaire serait l'autre levier.

Exemple T — réseau de chaleur.
Intitulé : Énergie - Chaleur urbaine - Travaux : Étendre le réseau de chaleur et raccorder des copropriétés
Sortie : {"Réseaux de chaleur décarbonés": [1]}
Lecture : l'ouvrage de réseau est décrit. Le raccordement des copropriétés fait partie du même aménagement. On n'ajoute le levier gaz résidentiel que si le remplacement des chaudières gaz est lui-même décrit.

Exemple U — industrie.
Intitulé : Économie - Industrie - Procédés : Subventionner la récupération de chaleur fatale dans les usines
Sortie : {"Production Industrielle": [3]}
Lecture : le site est industriel et le moyen est l'aide. Le libellé du levier garde les deux capitales.

Exemple V — sobriété foncière dans le document d'urbanisme.
Intitulé : Urbanisme - Foncier - Règles : Réduire les zones à urbaniser dans le PLU pour limiter l'artificialisation
Sortie : {"Sobriété foncière": [2]}
Lecture : l'acte est le PLU. Le mécanisme CO2 est le foncier, pas un levier bâtiment.

Exemple W — intitulé trop large.
Intitulé : Transversal - Climat - Animation : Sensibiliser le grand public à la transition écologique
Sortie : {}
Lecture : aucun mécanisme CO2 direct n'est nommé. La catégorie 6 ne se pose qu'une fois un levier retenu. En cas de doute, objet vide.

Exemple X — deux catégories internes au même levier, toutes deux concrètes.
Intitulé : Mobilité - Covoiturage - Dispositif : Aménager des aires de covoiturage et verser une indemnité aux conducteurs
Sortie : {"Covoiturage": [1, 3]}
Lecture : l'ouvrage et le flux financier sont tous les deux dans la phrase. On n'ajoute pas la catégorie 6, qui n'est pas décrite.
"""


def _bloc_glossaire() -> str:
    blocs = []
    for levier, lecture in _GLOSSAIRE:
        blocs.append(f"### {levier}\n{lecture}")
    return "\n\n".join(blocs)


_REGLES = f"""Tu es un expert en analyse d'impact carbone des politiques publiques et en modélisation par leviers CO2.

# Tâche
On te donne UN intitulé de mesure issu d'un référentiel (CAE, ECI ou TE). L'intitulé a la forme « niveau 1 - niveau 2 - niveau 3 : mesure ». Il n'y a PAS de description. Tu classes cette mesure :
- sur zéro, un ou plusieurs leviers CO2 de la liste fermée ;
- pour chaque levier retenu, sur une ou plusieurs catégories de type d'action, entiers de 1 à 6.

Le message utilisateur contient seulement cet intitulé. Tu ne dois rien demander de plus.

# Les 6 catégories
La catégorie ne décrit pas l'impact carbone mais le MOYEN par lequel la collectivité agit.
1. Aménagement & infrastructures — Actions physiques sur le territoire à destination des habitants et des acteurs économiques : urbanisme, mobilités douces, espaces verts, réseaux (eau, chaleur, assainissement), renaturation, équipements publics ouverts au public.
2. Réglementation & planification — Documents cadres et actes juridiques qui orientent l'action du territoire : PLU/PLUi, PCAET, SCoT, règlements locaux, zones à faibles émissions, arrêtés municipaux.
3. Financement & fiscalité — Orientation des flux économiques : subventions aux particuliers et entreprises, tarification incitative, budgets participatifs écologiques, fiscalité locale verte.
4. Gouvernance & partenariats — Pilotage de la politique de transition : élu référent, service dédié, stratégie et feuille de route, coopération intercommunale, partenariats privés/associatifs, concertation citoyenne, suivi-évaluation.
5. Exemplarité interne — Transition écologique appliquée au fonctionnement PROPRE de la collectivité : rénovation du patrimoine bâti public, flotte de véhicules, restauration collective, achats et commande publique responsables, numérique responsable, formation des agents.
6. Sensibilisation & accompagnement — Information, éducation et conseil aux habitants, entreprises et associations : guichet unique rénovation, animations scolaires, ateliers, communication, accompagnement de projets citoyens.

# Distinctions à respecter
- Catégorie 1 vs 5 : une action sur un bâtiment ou un véhicule relève de la 5 si elle porte sur le patrimoine ou les moyens PROPRES de la collectivité, et de la 1 seulement si l'équipement est destiné aux habitants ou aux acteurs du territoire.
- Catégorie 2 vs 4 : la 2 est l'acte juridique ou le document opposable ; la 4 est la manière de piloter, décider et coopérer. Adopter un PLU = 2. Créer un comité de suivi = 4.
- Catégorie 3 vs 6 : verser une subvention = 3 ; informer, orienter ou accompagner sans flux financier = 6.
- Plusieurs catégories dans un même levier seulement si l'intitulé décrit concrètement plusieurs mécanismes. Ne pas ajouter une catégorie seulement parce qu'elle est plausible.
- Plusieurs leviers seulement si plusieurs mécanismes CO2 sont clairs dans l'intitulé.

# Règles
- N'associe un levier que si le lien avec un mécanisme d'impact CO2 est clair, direct ou très fortement plausible à la seule lecture de l'intitulé.
- Si le lien est indirect, spéculatif, ou dépend d'une description absente, n'associe pas le levier.
- En cas de doute sur un levier, s'abstenir. La précision prime sur l'exhaustivité.
- Un levier retenu a AU MOINS une catégorie. Une liste vide est interdite.
- N'invente aucun levier. Recopie le libellé exactement, accents, majuscules et signe & compris.
- Les catégories sont des entiers 1, 2, 3, 4, 5 ou 6. Pas de libellé de catégorie dans le JSON.
- L'absence de levier sûr se traduit par un objet vide {{}}.

# Format de réponse
Réponds UNIQUEMENT avec un JSON valide, sans texte, sans markdown, sans commentaire.
Les clés sont les leviers retenus. Les valeurs sont des listes d'entiers.
N'utilise pas l'intitulé comme clé. Ne reproduis pas les lignes « Lecture » des exemples.

Forme :
{{"Vélo et transport en commun": [1, 3]}}
ou, à défaut de levier sûr :
{{}}

# Liste fermée des leviers
{LEVIERS.strip()}
"""

SYSTEM_PROMPT = (
    _REGLES
    + "\n# Glossaire opérationnel\n"
    + "Chaque bloc précise ce que le levier couvre quand on ne dispose que de l'intitulé.\n\n"
    + _bloc_glossaire()
    + "\n\n# Exemples annotés\n"
    + _EXEMPLES
)

PROMPT_VERSION = hashlib.sha256(SYSTEM_PROMPT.encode("utf-8")).hexdigest()[:16]

if set(levier for levier, _ in _GLOSSAIRE) != LEVIERS_SET:
    raise RuntimeError("Le glossaire des leviers ne couvre pas exactement la liste fermée.")

if len(SYSTEM_PROMPT) < _MIN_CHARS_PROMPT:
    raise RuntimeError(
        f"Prompt système trop court pour le cache Haiku 4.5 "
        f"({len(SYSTEM_PROMPT)} caractères, minimum {_MIN_CHARS_PROMPT})."
    )


def _cle_anthropic() -> str:
    try:
        depuis_secrets = st.secrets.get("ANTHROPIC_API_KEY", "")
    except Exception:
        depuis_secrets = ""
    return str(depuis_secrets or os.getenv("ANTHROPIC_API_KEY") or "")


@st.cache_resource(show_spinner=False)
def get_anthropic_client() -> anthropic.Anthropic | None:
    cle = _cle_anthropic()
    if not cle:
        return None
    return anthropic.Anthropic(api_key=cle)


def _enregistrer_usage(usage: Any) -> None:
    if usage is None:
        return
    releve = {
        "input_tokens": int(getattr(usage, "input_tokens", 0) or 0),
        "output_tokens": int(getattr(usage, "output_tokens", 0) or 0),
        "cache_creation_input_tokens": int(
            getattr(usage, "cache_creation_input_tokens", 0) or 0
        ),
        "cache_read_input_tokens": int(getattr(usage, "cache_read_input_tokens", 0) or 0),
    }
    with _USAGE_LOCK:
        _USAGES.append(releve)


def _oter_balises(brut: str) -> str:
    texte = (brut or "").strip()
    if texte.startswith("```"):
        texte = (
            texte.replace("```json", "").replace("```JSON", "").replace("```", "").strip()
        )
    return texte


def _charger_json(brut: str) -> Any:
    texte = _oter_balises(brut)
    try:
        return json.loads(texte)
    except json.JSONDecodeError:
        debut = texte.find("{")
        fin = texte.rfind("}")
        if debut >= 0 and fin > debut:
            return json.loads(texte[debut : fin + 1])
        raise


def valider_classification(data: Any) -> list[tuple[str, int]]:
    """Normalise {levier: [catégories]} en couples. Un objet vide est valide."""
    if not isinstance(data, dict):
        raise ValueError("La classification doit être un objet JSON")
    if not data:
        return []

    paires: list[tuple[str, int]] = []
    for levier_brut, categories in data.items():
        if not isinstance(levier_brut, str):
            raise ValueError(f"Levier illisible : {levier_brut!r}")
        levier = levier_brut.strip()
        if levier not in LEVIERS_SET:
            raise ValueError(f"Levier inconnu : {levier}")
        if not isinstance(categories, list) or len(categories) == 0:
            raise ValueError(f"Catégories vides pour le levier « {levier} »")

        vues: set[int] = set()
        for cat in categories:
            if isinstance(cat, bool) or isinstance(cat, float):
                raise ValueError(f"Catégorie invalide {cat!r} pour « {levier} »")
            try:
                cat_int = int(cat)
            except (TypeError, ValueError) as exc:
                raise ValueError(f"Catégorie invalide {cat!r} pour « {levier} »") from exc
            if cat_int not in VALID_CATEGORIES:
                raise ValueError(f"Catégorie hors 1-6 ({cat_int}) pour « {levier} »")
            vues.add(cat_int)
        for cat_int in sorted(vues):
            paires.append((levier, cat_int))
    return paires


def _appeler_haiku(client: anthropic.Anthropic, nom: str) -> list[tuple[str, int]]:
    reponse = client.messages.create(
        model=_MODELE_HAIKU,
        max_tokens=_MAX_TOKENS,
        extra_body={"temperature": 0},
        system=[
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[{"role": "user", "content": nom}],
    )
    _enregistrer_usage(reponse.usage)
    if reponse.stop_reason == "max_tokens":
        raise ValueError("Réponse tronquée")
    brut = "".join(bloc.text for bloc in reponse.content if bloc.type == "text")
    return valider_classification(_charger_json(brut))


def classer_intitule(client: anthropic.Anthropic, nom: str) -> list[tuple[str, int]]:
    """Un appel par intitulé, avec deux nouvelles tentatives si la sortie est invalide."""
    derniere_erreur: Exception | None = None
    for tentative in range(1, _MAX_TENTATIVES + 1):
        try:
            return _appeler_haiku(client, nom)
        except Exception as exc:
            derniere_erreur = exc
            if tentative < _MAX_TENTATIVES:
                time.sleep(0.4 * tentative)
    raise RuntimeError(f"{nom} : {derniere_erreur}")


@st.cache_data(ttl="1d", show_spinner=False)
def classification_en_cache(
    nom: str, prompt_version: str
) -> tuple[tuple[str, int], ...]:
    """Sert une classification déjà réussie.

    Au premier appel d'une clé, le résultat doit avoir été déposé dans
    `_A_MEMORISER`. Streamlit ne mémorise pas l'exception d'un appel sans dépôt,
    ce qui laisse les échecs hors cache. Les succès sont ensuite relus sans
    réexécuter cette fonction.
    """
    cle = (nom, prompt_version)
    if cle not in _A_MEMORISER:
        raise KeyError(nom)
    return _A_MEMORISER.pop(cle)


def lire_classification_cachee(nom: str) -> tuple[tuple[str, int], ...] | None:
    try:
        return classification_en_cache(nom, PROMPT_VERSION)
    except KeyError:
        return None


def memoriser_classification(nom: str, paires: list[tuple[str, int]]) -> None:
    fige = tuple((levier, int(cat)) for levier, cat in paires)
    _A_MEMORISER[(nom, PROMPT_VERSION)] = fige
    classification_en_cache(nom, PROMPT_VERSION)


def charger_mesures() -> pd.DataFrame:
    """Lecture seule sur la production."""
    engine = get_engine_prod()
    with engine.connect() as conn:
        df = pd.read_sql_query(text(REQUETE_MESURES), conn)
    df["action_id"] = df["action_id"].astype(str)
    df["nom"] = df["nom"].fillna("").astype(str).str.strip()
    return df[df["nom"] != ""].reset_index(drop=True)


def construire_lignes(
    df: pd.DataFrame, resultats: dict[str, list[tuple[str, int]]]
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for action_id, nom in zip(df["action_id"], df["nom"], strict=True):
        paires = resultats.get(nom)
        if not paires:
            continue
        for levier, categorie in paires:
            rows.append(
                {"action_id": action_id, "levier": levier, "categorie": int(categorie)}
            )
    colonnes = ["action_id", "levier", "categorie"]
    if not rows:
        return pd.DataFrame(columns=colonnes)
    return pd.DataFrame(rows, columns=colonnes).drop_duplicates()


def sauver_olap(df: pd.DataFrame) -> None:
    """Remplace priorisation_levier_mesure sur OLAP. N'écrit jamais en production."""
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(text("DROP TABLE IF EXISTS priorisation_levier_mesure"))
        conn.execute(
            text(
                """
                CREATE TABLE priorisation_levier_mesure (
                    action_id text NOT NULL,
                    levier text NOT NULL,
                    categorie integer NOT NULL
                )
                """
            )
        )
        if not df.empty:
            df.to_sql(
                "priorisation_levier_mesure",
                con=conn,
                if_exists="append",
                index=False,
            )


def _afficher_echecs(df_mesures: pd.DataFrame, erreurs: dict[str, str]) -> None:
    if not erreurs:
        return
    st.subheader("Intitulés en échec")
    df_erreurs = pd.DataFrame(
        [
            {
                "nom": nom,
                "erreur": message,
                "nb_mesures": int((df_mesures["nom"] == nom).sum()),
            }
            for nom, message in sorted(erreurs.items())
        ]
    )
    st.dataframe(df_erreurs, use_container_width=True, hide_index=True)


def _somme_usage() -> dict[str, int]:
    totaux = {
        "input_tokens": 0,
        "output_tokens": 0,
        "cache_creation_input_tokens": 0,
        "cache_read_input_tokens": 0,
    }
    with _USAGE_LOCK:
        releves = list(_USAGES)
    for releve in releves:
        for cle in totaux:
            totaux[cle] += releve.get(cle, 0)
    return totaux


st.title("Classification levier × mesure")
st.markdown(
    "Calcul one-shot des mesures CAE, ECI et TE. Chaque intitulé, sans description, "
    "est envoyé seul à Claude Haiku. Les couples levier × catégorie sont écrits dans "
    "`priorisation_levier_mesure` sur OLAP. La production n'est lue qu'en lecture seule."
)
st.caption(
    f"Modèle `{_MODELE_HAIKU}`, {_WORKERS} appels en parallèle, "
    f"préfixe mis en cache ({len(SYSTEM_PROMPT)} caractères, version `{PROMPT_VERSION}`)."
)

if st.button("Lancer la classification", type="primary"):
    client = get_anthropic_client()
    if client is None:
        st.error(
            "Clé ANTHROPIC_API_KEY manquante : configurez-la dans secrets.toml "
            "ou dans les variables d'environnement."
        )
        st.stop()

    with st.status("Classification en cours…", expanded=True) as statut:
        statut.write("Lecture des mesures en production…")
        try:
            df_mesures = charger_mesures()
        except Exception as exc:
            statut.update(label="Lecture impossible", state="error")
            st.error(f"Lecture prod impossible : {exc}")
            st.stop()

        if df_mesures.empty:
            statut.update(label="Aucune mesure", state="error")
            st.warning("La requête n'a renvoyé aucune mesure.")
            st.stop()

        noms_uniques = list(dict.fromkeys(df_mesures["nom"].tolist()))
        resultats: dict[str, list[tuple[str, int]]] = {}
        a_appeler: list[str] = []
        for nom in noms_uniques:
            en_cache = lire_classification_cachee(nom)
            if en_cache is None:
                a_appeler.append(nom)
            else:
                resultats[nom] = list(en_cache)

        statut.write(
            f"{len(df_mesures)} mesures, {len(noms_uniques)} intitulés distincts, "
            f"{len(resultats)} déjà en cache, {len(a_appeler)} appels à lancer."
        )

        erreurs: dict[str, str] = {}
        if a_appeler:
            barre = st.progress(0.0, text="Appels Haiku…")
            faits = 0
            with ThreadPoolExecutor(max_workers=_WORKERS) as executor:
                futurs = {
                    executor.submit(classer_intitule, client, nom): nom for nom in a_appeler
                }
                for futur in as_completed(futurs):
                    nom = futurs[futur]
                    try:
                        paires = futur.result()
                    except Exception as exc:
                        erreurs[nom] = str(exc)
                    else:
                        memoriser_classification(nom, paires)
                        resultats[nom] = paires
                    faits += 1
                    barre.progress(faits / len(a_appeler), text=f"{faits}/{len(a_appeler)}")

        df_lignes = construire_lignes(df_mesures, resultats)
        if not resultats:
            statut.update(label="Aucune classification réussie", state="error")
        else:
            statut.write("Écriture OLAP…")
            try:
                sauver_olap(df_lignes)
            except Exception as exc:
                statut.update(label="Écriture OLAP impossible", state="error")
                st.error(f"Échec de l'écriture OLAP : {exc}")
                st.stop()
            statut.update(label="Classification enregistrée", state="complete")

    if not resultats:
        st.error(
            "Tous les appels ont échoué. La table OLAP `priorisation_levier_mesure` "
            "n'a pas été modifiée."
        )
        _afficher_echecs(df_mesures, erreurs)
        st.stop()

    noms_sans_levier = {nom for nom, paires in resultats.items() if not paires}
    n_succes_ids = int(df_mesures["nom"].isin(resultats).sum())
    n_sans_levier = int(df_mesures["nom"].isin(noms_sans_levier).sum())
    usage = _somme_usage()

    col_1, col_2, col_3, col_4 = st.columns(4)
    col_1.metric("Mesures lues", len(df_mesures))
    col_2.metric("Lignes écrites", len(df_lignes))
    col_3.metric("Mesures sans levier", n_sans_levier)
    col_4.metric("Intitulés en échec", len(erreurs))
    st.caption(
        f"{n_succes_ids} mesures classées, dont {len(noms_uniques) - len(a_appeler)} "
        f"intitulés relus depuis le cache Streamlit et {len(a_appeler) - len(erreurs)} "
        f"nouveaux appels réussis."
    )
    st.caption(
        "Tokens Anthropic — "
        f"cache créé : {usage['cache_creation_input_tokens']}, "
        f"cache lu : {usage['cache_read_input_tokens']}, "
        f"entrée hors cache : {usage['input_tokens']}, "
        f"sortie : {usage['output_tokens']}."
    )
    if a_appeler and usage["cache_creation_input_tokens"] == 0 and usage["cache_read_input_tokens"] == 0:
        st.warning(
            "Aucun token n'a été servi par le cache Anthropic. Le préfixe est probablement "
            "resté sous le seuil de 4096 tokens de Haiku 4.5."
        )

    st.subheader("Lignes enregistrées")
    st.dataframe(df_lignes, use_container_width=True, hide_index=True)
    _afficher_echecs(df_mesures, erreurs)
