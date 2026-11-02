# Stabilité Mistral Large 4 — classification volet GES

Modèle `claude-haiku-5-5`, raisonnement `aucun`, température par défaut de l'API. Prompt v2 (`prompts/classification_volet_ges_v2.md`), une fiche par appel, codes de leviers et JSON contraint, 3 runs indépendants. Lecture seule sur la prod.

Mis à jour le 2026-11-02 13:35.

## Synthèse

| Collectivité | Fiches | Stables | Instables | % stable | Paires 3/3 | Majorité = prod |
|---|---:|---:|---:|---:|---:|---:|
| Hélette (13693) | 41 | 38 | 3 | 93% | 31/36 | non classée en prod |
| Saint-Jean-de-Braye (1609) | 36 | 34 | 2 | 94% | 32/36 | non classée en prod |
| CA Privas Centre Ardèche (3893) | 100 | 93 | 7 | 93% | 70/81 | 11/51 |
| CC Ardennes Thiérache (3914) | 104 | 97 | 7 | 93% | 97/107 | 10/56 |
| CA Rochefort Océan (4026) | 75 | 71 | 4 | 95% | 59/65 | 24/53 |
| CA Guingamp-Paimpol Agglomération de l'Armor à l'Argoat (4097) | 102 | 86 | 16 | 84% | 107/141 | 10/54 |
| CC Creuse Sud Ouest (4111) | 80 | 77 | 3 | 96% | 27/32 | 3/25 |
| Bordeaux Métropole (4322) | 55 | 37 | 18 | 67% | 82/116 | 2/38 |
| CC de la Forêt (4576) | 94 | 86 | 8 | 91% | 83/96 | 12/63 |
| CC Baugeois Vallée (4637) | 91 | 72 | 19 | 79% | 103/131 | 8/70 |
| CC du Pays de Colombey et du Sud Toulois (4707) | 83 | 77 | 6 | 93% | 71/85 | 14/66 |
| CC du Pays de Barr (4939) | 41 | 37 | 4 | 90% | 43/47 | 17/39 |
| CC Sundgau (4973) | 37 | 30 | 7 | 81% | 33/46 | non classée en prod |
| CC du Pays de l'Arbresle (CCPA) (4994) | 96 | 87 | 9 | 91% | 85/99 | 15/66 |
| Métropole de Lyon (4999) | 81 | 76 | 5 | 94% | 65/70 | 7/41 |
| CC Val de Gray (5005) | 42 | 40 | 2 | 95% | 43/47 | non classée en prod |
| CC Brionnais Sud Bourgogne (5033) | 111 | 107 | 4 | 96% | 78/86 | 22/70 |
| Le Havre Seine Métropole (5119) | 88 | 73 | 15 | 83% | 86/112 | 11/50 |
| CC du Pays des Achards (5300) | 103 | 95 | 8 | 92% | 75/89 | 12/50 |
| Paris Est Marne & Bois (5390) | 141 | 133 | 8 | 94% | 69/82 | 19/68 |
| SM du SCoT Sambre Avesnois (6030) | 73 | 62 | 11 | 85% | 70/89 | 11/53 |
| **Total** | **1674** | **1508** | **166** | **90%** | | |

« Paires 3/3 » : paires levier × catégorie données par les 3 runs, sur toutes les paires proposées au moins une fois.

## Hélette (13693)

- Fiches : **41** — stables sur les 3 runs : **38** (93%), instables : **3**
- Paires levier × catégorie distinctes proposées : 36 — 3/3 runs : 31, 2/3 runs : 1, 1/3 runs : 4
- Aucune classification en prod pour cette collectivité
- Réponses JSON invalides rejouées : 0
- Appels : 123 — tokens d'entrée 1 186 569 (dont 1 120 653 en cache, 94%), sortie 6 967 — coût estimé 0.02 $ pour les 3 runs
- Date : 2026-11-02 13:35

### Classée dans certains runs, aucun levier dans d'autres (2)

#### Fiche 143326 — 3.1.3 - Animer des ateliers d'éducation à l'alimentation bio et durable dans les cantines des écoles

- **Run 1 :** Elevage durable [6]
- **Run 2 :** (aucun levier)
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Elevage durable (1/3)

#### Fiche 143378 — 6.3.1 - Limiter la consommation d'eau potable de la commune et systématiser la collecte et l’utilisation des eaux de pluies

- **Run 1 :** Sobriété des bâtiments (résidentiel) [6]
- **Run 2 :** (aucun levier)
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété des bâtiments (résidentiel) (1/3)

> La mise en oeuvre de cette action peut consister par exemple à : Mettre en place un suivi des consommations d'eau Encourager l’expérimentation de toilettes sèches séparatives Installer des équipements hydro-économes Optimiser l'arrosage (Ex : Paillage laine broyat, amélioration des pratiques d'entretien de la voirie,…) Réutiliser les eaux de pluies pour les sanitaires, l'entretien des espaces verts, le nettoyage des véhicules communaux, etc

### Levier présent dans certains runs seulement (1)

#### Fiche 143350 — 5.1.2 - Sanctuariser un budget d’investissement annuel pour la rénovation et mobiliser des aides

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [3] | Changement chaudières gaz + rénovation (résidentiel) [3]
- **Run 2 :** Sobriété des bâtiments (résidentiel) [3]
- **Run 3 :** Sobriété des bâtiments (résidentiel) [3]
- **Prod :** (aucun levier)
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (1/3), Changement chaudières gaz + rénovation (résidentiel) (1/3), Sobriété des bâtiments (résidentiel) (2/3)

## Saint-Jean-de-Braye (1609)

- Fiches : **36** — stables sur les 3 runs : **34** (94%), instables : **2**
- Paires levier × catégorie distinctes proposées : 36 — 3/3 runs : 32, 2/3 runs : 2, 1/3 runs : 2
- Aucune classification en prod pour cette collectivité
- Réponses JSON invalides rejouées : 0
- Appels : 108 — tokens d'entrée 1 028 304 (dont 983 988 en cache, 96%), sortie 6 224 — coût estimé 0.02 $ pour les 3 runs
- Date : 2026-11-02 13:35

### Levier présent dans certains runs seulement (1)

#### Fiche 16449 — Élaborer une politique de stationnement volontariste

- **Run 1 :** Réduction des déplacements [2] | Vélo et transport en commun [2]
- **Run 2 :** Réduction des déplacements [2]
- **Run 3 :** Réduction des déplacements [2] | Vélo et transport en commun [2]
- **Prod :** (aucun levier)
- Leviers intermittents : Vélo et transport en commun (2/3)

> Mettre en place une politique de stationnement dans le centre-ville et/ ou les zones de forte pression (commerces de quartier, etc.) Mettre en place une tarification différenciée si besoin Pour les communes en zones rurale, mettre l'accent sur la sensibilisation et l’information auprès des habitants sur le besoin de gérer l’usage de la voiture et de marquer les places réservées au stationnement et le développement de zones bleues le cas échéant autour des zones de trafic. Faire respecter la rég…

### Levier intermittent et catégories instables (1)

#### Fiche 16431 — Prévenir et lutter contre la précarité énergétique

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6] | Sobriété des bâtiments (résidentiel) [6]
- **Run 2 :** Sobriété des bâtiments (résidentiel) [4, 6]
- **Run 3 :** Sobriété des bâtiments (résidentiel) [4, 6]
- **Prod :** (aucun levier)
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (1/3), Changement chaudières gaz + rénovation (résidentiel) (1/3)
- Catégories instables sur : Sobriété des bâtiments (résidentiel)

> Engager une politique de prévention et de lutte contre la précarité énergétique (liée au logement et à la mobilité) et l'inscrire dans ses documents stratégiques. Réaliser un travail d’inventaire des acteurs de la précarité énergétique et des actions existantes, sur lesquelles construire le dispositif. Utiliser au mieux les moyens humains à disposition pour identifier des situations de précarité énergétique du logement et orienter les familles directement vers les dispositifs existants ou indir…

## CA Privas Centre Ardèche (3893)

- Fiches : **100** — stables sur les 3 runs : **93** (93%), instables : **7**
- Paires levier × catégorie distinctes proposées : 81 — 3/3 runs : 70, 2/3 runs : 8, 1/3 runs : 3
- Vote majoritaire = prod : 11/51 fiches classées d'un côté ou de l'autre
- Réponses JSON invalides rejouées : 0
- Appels : 300 — tokens d'entrée 2 865 396 (dont 2 733 300 en cache, 95%), sortie 16 149 — coût estimé 0.05 $ pour les 3 runs
- Date : 2026-11-02 13:35

### Levier présent dans certains runs seulement (3)

#### Fiche 78907 — Fiche action 1.5 - Réaliser une campagne d’isolation par l’extérieur des bâtiments privés

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6] | Sobriété et isolation des bâtiments (tertiaire) [6]
- **Run 2 :** Sobriété et isolation des bâtiments (tertiaire) [6]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6] | Sobriété et isolation des bâtiments (tertiaire) [6]
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [6]
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (2/3), Changement chaudières gaz + rénovation (résidentiel) (2/3)

> Nouvelle, en lien avec existant (Plateforme Rénofuté, ALEC 07) - Réduire les consommations d’énergie (hiver comme été) - Améliorer le confort - Anticiper le changement climatique et adapter le bâti à l’avenir - Faciliter la compréhension autour de cette technique - Faire aboutir des projets ambitieux - Encourager et aider les particuliers qui sont démunis techniquement - Faire monter en compétence les professionnels du territoire Éléments de calendrier : En année 1 A renouveler en année 3 et 5 …

#### Fiche 78941 — Fiche action 4.8 - Valoriser et récupérer les déchets verts compostables

- **Run 1 :** Prévention des déchets [1] | Valorisation matière des déchets [1]
- **Run 2 :** Valorisation matière des déchets [1]
- **Run 3 :** Prévention des déchets [1] | Valorisation matière des déchets [1]
- **Prod :** Valorisation matière des déchets [1, 4]
- Leviers intermittents : Prévention des déchets (2/3)

> Nouvelle action Réduire les transports de déchets verts (broyat moins volumineux) Diminuer les tonnages en déchetterie Favoriser la valorisation locale des déchets verts : usagers, communes et agriculteurs Moyen de soutenir l’activité agricole indirectement (enjeu économique) Limiter l’achat de produits phytosanitaires et en réduire l’usage grâce à l’utilisation du broyat produit (et faire attention aux risques sanitaires lié à la diffusion de broyat non compostés) Réduire l’arrosage des espace…

#### Fiche 78945 — Fiche action 4.12 - Diminuer la consommation d’intrants (produits phytosanitaires, eau, engrais minéraux, aliments concentrés, énergie directe) dans les exploitations agricoles

- **Run 1 :** Changements de pratiques de fertilisation azotée [6] | Elevage durable [6]
- **Run 2 :** Changements de pratiques de fertilisation azotée [6] | Elevage durable [6]
- **Run 3 :** Bâtiments & Machines agricoles [6] | Changements de pratiques de fertilisation azotée [6]
- **Prod :** Bâtiments & Machines agricoles [6] | Changements de pratiques de fertilisation azotée [6]
- Leviers intermittents : Bâtiments & Machines agricoles (1/3), Elevage durable (2/3)

> Action en cours • Diminution de la pollution des nappes phréatiques et de l’usure des sols • Amélioration de la qualité nutritive des produits consommés • Incitation à l’exemplarité • Economie de la ressource en eau • Adaptation aux futures contraintes de ressources et d’utilisation d’engrais • Amélioration de la qualité de l’air • Améliorer l’efficacité des systèmes de production sans réduire le niveau de production agricole • Renforcer l’autonomie des exploitations

### Levier intermittent et catégories instables (1)

#### Fiche 78915 — Fiche action 2.2 - Développer les énergies renouvelables pour le chauffage et l’eau-chaude des bâtiments publics et privés

- **Run 1 :** Electricité renouvelable [1] | Gestion des forêts et produits bois [1] | Réseaux de chaleur décarbonés [6]
- **Run 2 :** Electricité renouvelable [1] | Gestion des forêts et produits bois [1] | Réseaux de chaleur décarbonés [6]
- **Run 3 :** Electricité renouvelable [1] | Réseaux de chaleur décarbonés [1, 6]
- **Prod :** (aucun levier)
- Leviers intermittents : Gestion des forêts et produits bois (2/3)
- Catégories instables sur : Réseaux de chaleur décarbonés

> Action nouvelle • Réduire la facture énergétique • Tendre vers plus d’autonomie énergétique • Développer la géothermie - Production de chaud et de froid (climatisation) - Amélioration des connaissances et sensibilisation sur cette technologie - Promouvoir les artisans locaux • Améliorer l’utilisation du chauffage au bois - Réduire la contribution du bois-énergie à la pollution de l’air - Réduire la consommation de combustible - Regrouper la filière autour d’une plateforme intercommunale pour st…

### Mêmes leviers, catégories différentes (3)

#### Fiche 78910 — Fiche action 1.8 - Soutenir l’amélioration de l’habitat privé via une OPAH et Rénofuté

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [3, 6] | Changement chaudières gaz + rénovation (résidentiel) [3, 6]
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [3] | Changement chaudières gaz + rénovation (résidentiel) [3]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [3, 6] | Changement chaudières gaz + rénovation (résidentiel) [3, 6]
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [3, 6]
- Catégories instables sur : Changement chaudières fioul + rénovation (résidentiel), Changement chaudières gaz + rénovation (résidentiel)

> Lancée depuis 2016 avec Rénofuté, de nouvelles actions venant s’ajouter • Réalisation d’une OPAH : - Lutte contre l’insalubrité, le logement indigne et la précarité énergétique, - Adaptation des logements au maintien à domicile des personnes âgées et handicapées, - Accompagnement des copropriétés fragiles, - Développement du parc à vocation sociale, - Mobilisation du parc vacant pour les primo accédants • Soutien à la plateforme Rénofuté pour réaliser des rénovations énergétiques performantes -…

#### Fiche 78917 — Fiche action 2.4 - Promouvoir l’autoconsommation PVT via les sociétés citoyennes

- **Run 1 :** Electricité renouvelable [6]
- **Run 2 :** Electricité renouvelable [3, 6]
- **Run 3 :** Electricité renouvelable [3, 6]
- **Prod :** Electricité renouvelable [3, 6]
- Catégories instables sur : Electricité renouvelable

> Action nouvelle • Développer de petites installations de production dans les maisons individuelles • Accompagner les structures citoyennes locales pour permettre leur professionnalisation et garantir des projets exemplaires à coûts maitrisés • Favoriser l’autoconsommation • Etre complémentaire avec la subvention publique et l’expertise des sociétés locales • Permettre la réduction des factures et la lutte contre la précarité énergétique Éléments de calendrier : Année 1 et 2 : définition contrat…

#### Fiche 78918 — Fiche action 2.5 - Développer un cadastre éolien foncier public (+AMI) et un cadastre solaire au sol pour anciens sites industriels & carrières

- **Run 1 :** Electricité renouvelable [2, 4]
- **Run 2 :** Electricité renouvelable [2]
- **Run 3 :** Electricité renouvelable [2]
- **Prod :** Electricité renouvelable [2, 4]
- Catégories instables sur : Electricité renouvelable

> Action nouvelle • Identifier les potentiels éolien et solaire du territoire • Gérer le développement des EnR de façon coordonnée sur la CAPCA • Apporter un cadre et un accompagnement aux communes démunies et démarchées par les développeurs • Accompagner le co-développement citoyens/collectivités d’un parc éolien Éléments de calendrier : Année 1 et 2 : identification des sites et des porteurs de projet, lancement AMI et communiquer Années suivantes : lancement opérationnel des projets, suivi et …

## CC Ardennes Thiérache (3914)

- Fiches : **104** — stables sur les 3 runs : **97** (93%), instables : **7**
- Paires levier × catégorie distinctes proposées : 107 — 3/3 runs : 97, 2/3 runs : 3, 1/3 runs : 7
- Vote majoritaire = prod : 10/56 fiches classées d'un côté ou de l'autre
- Réponses JSON invalides rejouées : 0
- Appels : 312 — tokens d'entrée 2 968 515 (dont 2 842 632 en cache, 96%), sortie 18 193 — coût estimé 0.05 $ pour les 3 runs
- Date : 2026-11-02 13:16

### Classée dans certains runs, aucun levier dans d'autres (4)

#### Fiche 76393 — Minimiser l'impact environnemental lié aux travaux de la collectivité

- **Run 1 :** Production Industrielle [5]
- **Run 2 :** (aucun levier)
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Production Industrielle (1/3)

> <p><strong>Garantir que les bâtiments neufs soient performants énergétiquement</strong></p><p>-Réglementation RE2020</p><p>-Intégrer des critères sur la conception bioclimatique (en réflexion pour la construction de l'école à Maubert ?)</p><p><strong>Inclure dans les marchés publics des critères sur l'empreinte carbone des travaux</strong></p><p>-Privilégier des matériaux bio-sourcés (bois, chanvre, liège, paille, …)</p><p>-Faire appel à des artisans certifiés RGE</p><p><strong>A minima, demand…

#### Fiche 76561 — Création d'une restauration scolaire à Signy-le-Petit

- **Run 1 :** (aucun levier)
- **Run 2 :** (aucun levier)
- **Run 3 :** Sobriété et isolation des bâtiments (tertiaire) [1]
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété et isolation des bâtiments (tertiaire) (1/3)

#### Fiche 76565 — Réaménagement des Broises Basses en Brasserie

- **Run 1 :** (aucun levier)
- **Run 2 :** (aucun levier)
- **Run 3 :** Sobriété foncière [1]
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété foncière (1/3)

#### Fiche 76625 — Création d'aire de camping car

- **Run 1 :** Sobriété foncière [1]
- **Run 2 :** (aucun levier)
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété foncière (1/3)

### Levier présent dans certains runs seulement (2)

#### Fiche 76382 — Soutenir le développement des filières de l’économie circulaire

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [2, 3] | Réduction des déplacements [1] | Sobriété foncière [1]
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [3] | Réduction des déplacements [1] | Sobriété foncière [1]
- **Run 3 :** Changement chaudières gaz + rénovation (résidentiel) [3] | Réduction des déplacements [1] | Sobriété foncière [1]
- **Prod :** Covoiturage [1] | Prévention des déchets [2, 4] | Réduction des déplacements [1, 2, 4] | Véhicules électriques [1] | Vélo et transport en commun [1]
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (2/3), Changement chaudières gaz + rénovation (résidentiel) (1/3)

> <p><strong>Mettre en place des projets de revitalisation dans le cadre des ORT (5 communes) et du dispositif Petites Villes de Demain (Signy-le-Petit)</strong></p><p>Exemples d'actions</p><p>-Fédérer les commerçants</p><p>-Développer des cafés multiservices</p><p>-Mettre en place des IRVE, des stationnements vélos, des aires de covoiturage,</p><p>-Maintenir le commerce existant</p><p>-Vitrophanie</p><p>-Lutter contre le logement vacant</p><p>-OPAH</p><p>-THLV</p><p>-Rénovation du bâti ancien</p…

#### Fiche 76383 — Revitaliser les centres de villages et développer des services de proximité

- **Run 1 :** Réduction des déplacements [1] | Sobriété foncière [1] | Vélo et transport en commun [1]
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [3] | Réduction des déplacements [1] | Sobriété foncière [1]
- **Run 3 :** Réduction des déplacements [1] | Sobriété foncière [1] | Vélo et transport en commun [1]
- **Prod :** Réduction des déplacements [1, 2]
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (1/3), Vélo et transport en commun (2/3)

> <p><strong>Mettre en place des projets de revitalisation dans le cadre des ORT (5 communes) et du dispositif Petites Villes de Demain (Signy-le-Petit)</strong></p><p>Exemples d'actions</p><p>-Fédérer les commerçants</p><p>-Développer des cafés multiservices</p><p>-Mettre en place des IRVE, des stationnements vélos, des aires de covoiturage,</p><p>-Maintenir le commerce existant</p><p>-Vitrophanie</p><p>-Lutter contre le logement vacant</p><p>-OPAH</p><p>-THLV</p><p>-Rénovation du bâti ancien</p…

### Mêmes leviers, catégories différentes (1)

#### Fiche 76387 — Soutenir les démarches vers l'agroécologie

- **Run 1 :** Changements de pratiques de fertilisation azotée [6] | Elevage durable [3, 6] | Pratiques stockantes [6]
- **Run 2 :** Changements de pratiques de fertilisation azotée [6] | Elevage durable [3, 6] | Pratiques stockantes [6]
- **Run 3 :** Changements de pratiques de fertilisation azotée [6] | Elevage durable [6] | Pratiques stockantes [6]
- **Prod :** Changements de pratiques de fertilisation azotée [3, 6] | Elevage durable [3, 4, 6] | Pratiques stockantes [6]
- Catégories instables sur : Elevage durable

> <p><strong>Action PNR </strong>:</p><p>•Réaliser des évènements (ciné débat/séminaire/visite...) incitant à réfléchir ensemble à travailler autrement, vers des pratiques agro-environnementales, élevage à l'herbe, autonomie alimentaire sur la ferme, adaptation au changement climatique, soin des animaux allopathiques...</p><p><strong>Actions CCAT</strong></p><p>•Apporter des conseils et des aides aux éleveurs qui s'engagent dans des démarches de réduction des émissions de GES de leur cheptel</p><…

## CA Rochefort Océan (4026)

- Fiches : **75** — stables sur les 3 runs : **71** (95%), instables : **4**
- Paires levier × catégorie distinctes proposées : 65 — 3/3 runs : 59, 2/3 runs : 3, 1/3 runs : 3
- Vote majoritaire = prod : 24/53 fiches classées d'un côté ou de l'autre
- Réponses JSON invalides rejouées : 0
- Appels : 225 — tokens d'entrée 2 137 965 (dont 2 049 975 en cache, 96%), sortie 12 159 — coût estimé 0.04 $ pour les 3 runs
- Date : 2026-11-02 13:35

### Mêmes leviers, catégories différentes (4)

#### Fiche 87222 — Action 8 - Accompagner la mise en œuvre de matériauthèques thématiques (culture, pro…)

- **Run 1 :** Prévention des déchets [6]
- **Run 2 :** Prévention des déchets [1]
- **Run 3 :** Prévention des déchets [6]
- **Prod :** Prévention des déchets [1]
- Catégories instables sur : Prévention des déchets

> Détourner plus d’objets des bennes de déchèteries. Faire changer les modes de consommation. Mettre en avant la seconde vie des objets et matières par la réutilisation et la réparation. Développer une recyclerie vitrine du réemploi sur le territoire, qui soit complémentaire des solutions déjà existantes. Innover en impulsant la création de recycleries-matériauthèques spécialisées (culturelles, sportives, etc.). L’objectif est de détourner 400 tonnes de déchets par an à terme

#### Fiche 87239 — Action 25 - Accompagner les restaurateurs et les commerçants à réduire leurs déchets

- **Run 1 :** Prévention des déchets [6]
- **Run 2 :** Prévention des déchets [4, 6]
- **Run 3 :** Prévention des déchets [4, 6]
- **Prod :** Prévention des déchets [6]
- Catégories instables sur : Prévention des déchets

> Cette action a pour objectif de développer l’accompagnement des professionnels par le biais d’une prestation afin de réaliser un diagnostic de la situation, définir les besoins et accompagner à la mise en place de solutions alternatives pour réduire les déchets des professionnels. Les contributions reçues lors de la mise en consultation du PLPDMA montrent que les habitants sont attentifs à ce que l’effort de réduction soit porté aussi par les entreprises, qui ont-elles aussi une part de respons…

#### Fiche 87241 — Action 27 - Accompagner les artisans hors BTP à réduire leurs déchets

- **Run 1 :** Prévention des déchets [6]
- **Run 2 :** Prévention des déchets [4, 6]
- **Run 3 :** Prévention des déchets [6]
- **Prod :** Prévention des déchets [6]
- Catégories instables sur : Prévention des déchets

> Cette action a pour objectif de développer l’accompagnement des professionnels par le biais d’une prestation afin de réaliser un diagnostic de la situation, définir les besoins et accompagner à la mise en place de solutions alternatives pour réduire les déchets des professionnels. Les contributions reçues lors de la mise en consultation du PLPDMA montrent que les habitants sont attentifs à ce que l’effort de réduction soit porté aussi par les entreprises, qui ont-elles aussi une part de respons…

#### Fiche 87278 — Action 27 - Accentuer la démarche d’EIT

- **Run 1 :** Valorisation matière des déchets [4]
- **Run 2 :** Valorisation matière des déchets [6]
- **Run 3 :** Valorisation matière des déchets [6]
- **Prod :** (aucun levier)
- Catégories instables sur : Valorisation matière des déchets

> Action visant à développer les actions en direction des entreprises, en complément du travail réalisé par l'association Circule'R.

## CA Guingamp-Paimpol Agglomération de l'Armor à l'Argoat (4097)

- Fiches : **102** — stables sur les 3 runs : **86** (84%), instables : **16**
- Paires levier × catégorie distinctes proposées : 141 — 3/3 runs : 107, 2/3 runs : 18, 1/3 runs : 16
- Vote majoritaire = prod : 10/54 fiches classées d'un côté ou de l'autre
- Réponses JSON invalides rejouées : 0
- Appels : 306 — tokens d'entrée 3 104 262 (dont 2 787 966 en cache, 90%), sortie 19 378 — coût estimé 0.07 $ pour les 3 runs
- Date : 2026-11-02 13:35

### Classée dans certains runs, aucun levier dans d'autres (2)

#### Fiche 31882 — CAE 12. Favoriser les activités économiques durables sur le territoire

- **Run 1 :** (aucun levier)
- **Run 2 :** (aucun levier)
- **Run 3 :** Valorisation matière des déchets [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Valorisation matière des déchets (1/3)

> La collectivité initie, soutient ou participe à des projets de coopération avec les acteurs de l'économie locale ou régionale sur le climat, l'air et l'énergie, afin d'encourager la mutation des activités économiques vers un modèle bas-carbon. Elle participe notamment au développement des projets d’écologie industrielle et plus généralement d'économie circulaire sur le territoire. Elle contribue à l'amélioration de la qualité environnementale des zones d’activités .

#### Fiche 31891 — ECI 6. Connaître les coûts de la gestion des déchets pour maîtriser les dépenses publiques

- **Run 1 :** Prévention des déchets [2]
- **Run 2 :** (aucun levier)
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Prévention des déchets (1/3)

> La maîtrise des dépenses publiques se caractérise par la capacité de la collectivité à identifier les marges de manœuvre économiques des services dont elle a la maîtrise d'ouvrage tout en maintenant la qualité du service. Concernant l'économie circulaire, il s'agit principalement de la collecte et du traitement des déchets mais aussi d'autres actions en faveur de l'économie circulaire. Cela nécessite un suivi précis et détaillé des coûts et permet, in fine, de mettre en place des actions optimi…

### Levier présent dans certains runs seulement (7)

#### Fiche 2239 — 2.1 Finaliser un PLUi intégrateur des enjeux transversaux de sobriété

- **Run 1 :** Electricité renouvelable [2] | Réduction des déplacements [2] | Sobriété foncière [2]
- **Run 2 :** Electricité renouvelable [2] | Réduction des déplacements [2] | Sobriété foncière [2]
- **Run 3 :** Changement chaudières gaz + rénovation (résidentiel) [2] | Réduction des déplacements [2] | Sobriété foncière [2]
- **Prod :** Electricité renouvelable [2] | Réduction des déplacements [2] | Sobriété foncière [2]
- Leviers intermittents : Changement chaudières gaz + rénovation (résidentiel) (1/3), Electricité renouvelable (2/3)

> Le PLUi est en cours d'élaboration. Toutefois, le PADD, qui fixe les grands enjeux et objectifs du PLUi, est voté. Il est organisé autour de trois axes décliné du projet de territoire et fixe les objectifs suivants en lien direct avec le PCAET : I. L'excellence environnementale, un atout majeur de valorisation et d'amélioration du cadre de vie 1 - L'eau, un milieu à protéger, une ressource à préserver : en assurant un développement cohérent avec les ressources disponibles et tenant compte des m…

#### Fiche 2243 — 2.5 Préserver et garantir un accès équitable à une ressource en eau de qualité 

- **Run 1 :** Prévention des déchets [6] | Sobriété des bâtiments (résidentiel) [6]
- **Run 2 :** Prévention des déchets [6]
- **Run 3 :** Prévention des déchets [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété des bâtiments (résidentiel) (1/3)

> L'Agglomération est concernée par 4 périmètres de SAGE : Argoat-Trégor-Goëlo (bassins versants du Leff, Trieux, Jaudy-Guindy-Bizien, ruisseaux côtiers de Plouézec à PLourivo), Baie de Lannion (bassin versant du Léguer), SAGE Aulne (bassins versants de l'Aulne et de l'Hyères), SAGE du Blavet (bassin versant du Haut Blavet). Depuis le 1er janvier 2019, Guingamp-Paimpol Agglomération porte les actions de bassins versants sur son territoire et deux nouveaux Contrats Territoriaux ont débuté au 1er j…

#### Fiche 2336 — 3.4 Mettre en œuvre le Programme Local de l’Habitat 2020-2025

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [2, 3] | Changement chaudières gaz + rénovation (résidentiel) [2, 3] | Sobriété des bâtiments (résidentiel) [6]
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [2, 3] | Changement chaudières gaz + rénovation (résidentiel) [2, 3] | Sobriété des bâtiments (résidentiel) [6]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [2, 3] | Changement chaudières gaz + rénovation (résidentiel) [2, 3]
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [2, 3, 6] | Changement chaudières gaz + rénovation (résidentiel) [2, 3, 6] | Sobriété des bâtiments (résidentiel) [2, 3, 6]
- Leviers intermittents : Sobriété des bâtiments (résidentiel) (2/3)

> Historiquement, seuls les deux secteurs urbains disposaient d’un PLH (Guingamp et Paimpol). Lors de la création de l’agglomération, le PLH a été étendu à l’ensemble du territoire. Le diagnostic a mise en évidence des problèmes forts de confort, d’indignité, de besoins d’adaptation et de précarité énergétique. 60 à 65% des foyers de l’agglomération sont éligibles au logement social. Sur le secteur guingampais, cette proportion monte à près de 80% des foyers. Une filière artisanale encore fragile…

#### Fiche 2345 — 4.5 Accompagner la transition et mobiliser la capacité de résilience du secteur agricole

- **Run 1 :** Bâtiments & Machines agricoles [6] | Gestion des haies [6] | Pratiques stockantes [6]
- **Run 2 :** Bâtiments & Machines agricoles [6] | Changements de pratiques de fertilisation azotée [6] | Pratiques stockantes [6]
- **Run 3 :** Bâtiments & Machines agricoles [6] | Changements de pratiques de fertilisation azotée [6] | Pratiques stockantes [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Changements de pratiques de fertilisation azotée (2/3), Gestion des haies (1/3)

> La Bretagne est un territoire d’exportation agricole essentiel à l’échelle française et internationale. Elle regroupe des exploitations variées avec des fonctionnements et des modèles économiques très différents. Les crises récentes (sanitaires, de consommation, événements climatiques…) ont mis en évidence des vulnérabilités de certains modèles agricoles, notamment les moins autonomes. Dès 2019, l’agglomération a fait le choix du renforcement des filières locales par l’engagement de la restaura…

#### Fiche 21888 — Dispositif d’aides au conseil pour des projets d’investissement liés à la transformation et la commercialisation des productions locales

- **Run 1 :** Bâtiments & Machines agricoles [3]
- **Run 2 :** Production Industrielle [3]
- **Run 3 :** Bâtiments & Machines agricoles [3]
- **Prod :** (aucun levier)
- Leviers intermittents : Bâtiments & Machines agricoles (2/3), Production Industrielle (1/3)

> Aide pouvant aller jusqu’à 2 000 € apportée à des entreprises agricoles ou des groupements d’agriculteurs qui souhaitent recourir à des prestations externes ayant trait à du conseil, de l’accompagnement, des études de faisabilité, des études d’opportunité ou des expérimentations en vue de réaliser des investissements visant un ou plusieurs des objectifs suivants : * la diversification par la transformation de produits de l’exploitation, * l’élargissement des gammes de produits finis, * la reche…

#### Fiche 21920 — Suivre et animer un Opération Programmée d’Amélioration de l’Habitat et Renouvellement Urbain (OPAH-RU) sur les 4 communes « Petites Villes de Demain (PVD)

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [3] | Changement chaudières gaz + rénovation (résidentiel) [3] | Sobriété foncière [6]
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [3] | Changement chaudières gaz + rénovation (résidentiel) [3] | Sobriété foncière [6]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [3] | Changement chaudières gaz + rénovation (résidentiel) [3]
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [3, 6] | Changement chaudières gaz + rénovation (résidentiel) [3, 6] | Sobriété foncière [3, 6]
- Leviers intermittents : Sobriété foncière (2/3)

> Les 4 communes PVD et l’agglomération sont signataires d’une convention d’Opération de Revitalisation Territoriale (ORT), dont le volet habitat se traduit de manière opérationnelle par la mise en œuvre d’un outil d’amélioration du parc privé de logement : l’OPAH-RU. Ce dispositif contractuel avec l’Anah vise à concentrer de l’ingénierie et des moyens financiers en vue de redonner de l’attractivité résidentielle aux centralités de ces 4 villes prioritaires. L’OPAH-RU s’adresse aux propriétaires …

#### Fiche 31816 — CAE 11. Accompagner et coopérer avec les acteurs professionnels et les particulier pour la rénovation et la construction durable de leur logement

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [3, 6] | Changement chaudières gaz + rénovation (résidentiel) [3, 6] | Sobriété des bâtiments (résidentiel) [6]
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [3, 6] | Changement chaudières gaz + rénovation (résidentiel) [3, 6] | Sobriété et isolation des bâtiments (tertiaire) [6]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [3, 6] | Changement chaudières gaz + rénovation (résidentiel) [3, 6] | Sobriété et isolation des bâtiments (tertiaire) [6]
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [3, 6] | Changement chaudières gaz + rénovation (résidentiel) [3, 6] | Changement de chaudière à fioul (tertiaire) [6] | Changement de chaudière à gaz (tertiaire) [6] | Sobriété et isolation des bâtiments (tertiaire) [6]
- Leviers intermittents : Sobriété des bâtiments (résidentiel) (1/3), Sobriété et isolation des bâtiments (tertiaire) (2/3)

> La collectivité joue un rôle d’animateur territorial pour impulser une dynamique sur le territoire en matière de climat, air et énergie. Elle informe et incite les acteurs professionnels du bâtiment (bailleurs sociaux, promoteurs, investisseurs, artisans, bureaux d'études, administrateurs de biens, notaires, agents immobiliers, etc.) à intégrer ces enjeux dans leurs activités. Ces actions sont réalisées via des espaces conseils France Rénov ou des conventions volontaires, qui incluent des stand…

### Levier intermittent et catégories instables (4)

#### Fiche 2248 — 3.1 (Re-)dynamiser des centres villes pour un mode de vie sobre en énergie

- **Run 1 :** Réduction des déplacements [1] | Sobriété des bâtiments (résidentiel) [2] | Sobriété foncière [2]
- **Run 2 :** Réduction des déplacements [2] | Sobriété des bâtiments (résidentiel) [2] | Sobriété foncière [2]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [2] | Réduction des déplacements [1] | Sobriété foncière [2]
- **Prod :** Réduction des déplacements [1, 2] | Sobriété foncière [1, 2]
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (1/3), Sobriété des bâtiments (résidentiel) (2/3)
- Catégories instables sur : Réduction des déplacements

> La ville de Guingamp et Guingamp-Paimpol Agglomération sont signataires depuis 2016 d'une convention de revitalisation du centre-ville et de développement du territoire (CRCDT). Cette convention 2017-2022 les engage sur 5 volets d'action en faveur de la centralité de Guingamp mais aussi, par capitalisation, de l'ensemble des centralités du territoire. Depuis, l'Agglomération est partenaire de 2 protocoles régionaux (Guingamp, Paimpol) dans le cadre des appels à projets "centres-bourgs" régionau…

#### Fiche 2343 — 4.3 Réduire l’empreinte environnementale de la pêche en mer artisanale

- **Run 1 :** Efficacité et carburants décarbonés des véhicules privés [1] | Valorisation matière des déchets [1]
- **Run 2 :** Efficacité et carburants décarbonés des véhicules privés [1, 6]
- **Run 3 :** Efficacité et carburants décarbonés des véhicules privés [1] | Valorisation matière des déchets [1]
- **Prod :** (aucun levier)
- Leviers intermittents : Valorisation matière des déchets (2/3)
- Catégories instables sur : Efficacité et carburants décarbonés des véhicules privés

> Les ports de Loguivy-de-la-Mer et Pors Even à Ploubazlanec et le port de Paimpol appartiennent au Quartier maritime de Paimpol, qui compte 115 bateaux. La pratique de la pêche locale amène de nombreux bâtiments à changer de localisation sur le quartier maritime dans le courant de l’année. Par conséquent, afin de prendre en compte cette spécificité, les données de la pêche du Quartier maritime seront comptabilisées à l’échelle des deux EPCI Lannion Trégor Communauté (50%) et Guingamp-Paimpol Agg…

#### Fiche 4080 — 5.6 Renforcer l'autonomie des exploitations agricoles par le développement des énergies renouvelables et de récupération

- **Run 1 :** Biogaz [2, 6] | Electricité renouvelable [3, 6]
- **Run 2 :** Biogaz [3, 6] | Electricité renouvelable [3, 6] | Réseaux de chaleur décarbonés [3, 6]
- **Run 3 :** Biogaz [1, 3, 6] | Electricité renouvelable [3, 6] | Réseaux de chaleur décarbonés [3, 6]
- **Prod :** Biogaz [3] | Bâtiments & Machines agricoles [3] | Electricité renouvelable [3]
- Leviers intermittents : Réseaux de chaleur décarbonés (2/3)
- Catégories instables sur : Biogaz

> 5.6.1 Développer les projets d'EnR agricoles en autoconsommation Energie solaire : Pour soutenir les agriculteurs dans l’acquisition d’installations solaires photovoltaïques (bâti ou trackers) en autoconsommation individuelle ou collective, la Région Bretagne propose une aide financière, de l’étude de faisabilité au dispositif de suivi des performance (plafond à 30% de 25 000 € HT). L’ADEME peut apporter une aide financière aux études de montage juridique, technique et financier pour les projet…

#### Fiche 21899 — Stratégie d’optimisation foncière et immobilière

- **Run 1 :** Sobriété foncière [1, 2]
- **Run 2 :** Sobriété et isolation des bâtiments (tertiaire) [1] | Sobriété foncière [2]
- **Run 3 :** Sobriété et isolation des bâtiments (tertiaire) [1] | Sobriété foncière [1, 2]
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété et isolation des bâtiments (tertiaire) (2/3)
- Catégories instables sur : Sobriété foncière

> Sur le volet foncier : 1. Inventaire des ZAE 2. Etude des gisements fonciers 3. Commercialisation via le bail à construction sur les zones des pôles urbains 4. Plan d’action pour acquisition/densification/commercialisation Sur le volet immobilier 1. Créer une offre de location tertiaire en centralité de Guingamp 2. Faciliter la mutualisation des locaux d’activité privés (en partenariat avec l’Adit) 3. Travailler avec les promoteurs et agences immobilières pour constituer une bourse de l’immobil…

### Mêmes leviers, catégories différentes (3)

#### Fiche 2219 — 1.6 Organiser la transition énergétique du patrimoine immobilier public

- **Run 1 :** Changement de chaudière à fioul (tertiaire) [3] | Changement de chaudière à gaz (tertiaire) [3] | Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 2 :** Changement de chaudière à fioul (tertiaire) [3] | Changement de chaudière à gaz (tertiaire) [3] | Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 3 :** Changement de chaudière à fioul (tertiaire) [5] | Changement de chaudière à gaz (tertiaire) [5] | Sobriété et isolation des bâtiments (tertiaire) [5]
- **Prod :** Changement de chaudière à fioul (tertiaire) [3, 4, 5, 6] | Changement de chaudière à gaz (tertiaire) [3, 4, 5, 6] | Sobriété et isolation des bâtiments (tertiaire) [3, 4, 5, 6]
- Catégories instables sur : Changement de chaudière à fioul (tertiaire), Changement de chaudière à gaz (tertiaire)

> Le diagnostic du Plan Climat a mis en évidence un bâti public plutôt ancien et énergivore mais parfois à forte valeur patrimoniale. Ceci rend complexe leur rénovation thermique, notamment pour les plus petites communes rurales. Le décret n°2019-771 du 23 juillet 2019 dit "décret tertiaire" fixe une obligation de réduction de la consommation d'énergie pour les bâtiments d'activité tertiaire de plus de 1000m2 de 40% pour 2030, 50% pour 2040 et 60% pour 2050 par rapport à 2010. 1.6.1 Développer le…

#### Fiche 4079 — 5.5 Développer la filière bois énergie, notamment issue du bocage

- **Run 1 :** Gestion des haies [1, 4] | Réseaux de chaleur décarbonés [1, 6]
- **Run 2 :** Gestion des haies [1, 4] | Réseaux de chaleur décarbonés [1, 4]
- **Run 3 :** Gestion des haies [1, 4] | Réseaux de chaleur décarbonés [1, 4]
- **Prod :** Gestion des haies [4] | Réseaux de chaleur décarbonés [4]
- Catégories instables sur : Réseaux de chaleur décarbonés

> Guingamp-Paimpol Agglomération est le territoire de Bretagne ayant la plus importante ressource forestière (données OEB 2020). Sur le territoire, le développement de la filière bois énergie se construit prioritairement sur la mobilisation d’une importante ressource bocagère, dont les enjeux sont multiples : milieu, biodiversité, qualité de l’eau, infiltration des eaux pluviales, maintien des sols et production de bois. Son exploitation est limitée d’une part par le manque d’exutoire en valorisa…

#### Fiche 21892 — Actions en faveur du bocage

- **Run 1 :** Gestion des forêts et produits bois [1] | Gestion des haies [1, 2]
- **Run 2 :** Gestion des forêts et produits bois [1] | Gestion des haies [1, 4]
- **Run 3 :** Gestion des forêts et produits bois [1] | Gestion des haies [1, 2]
- **Prod :** Gestion des forêts et produits bois [1, 4] | Gestion des haies [1, 2, 4]
- Catégories instables sur : Gestion des haies

> *Réalisation de chantiers de plantations et de gestion de haies chez les agriculteurs *Mise en place de travaux de gestion du bois bord de route avec les communes *Instruction des déclarations préalables et des dossiers BCAE8 pour le déplacement de haies *Assurer une gestion durable des boisements de l’Agglomération *Mise en place de Plan de Gestion Durable des Haies (PGDH) pour les agriculteurs producteurs de la SCIC Bocagénèse Éléments de calendrier : 2023/2027 : mise en œuvre de la stratégie…

## CC Creuse Sud Ouest (4111)

- Fiches : **80** — stables sur les 3 runs : **77** (96%), instables : **3**
- Paires levier × catégorie distinctes proposées : 32 — 3/3 runs : 27, 2/3 runs : 4, 1/3 runs : 1
- Vote majoritaire = prod : 3/25 fiches classées d'un côté ou de l'autre
- Réponses JSON invalides rejouées : 0
- Appels : 240 — tokens d'entrée 2 311 827 (dont 2 186 640 en cache, 95%), sortie 10 615 — coût estimé 0.04 $ pour les 3 runs
- Date : 2026-11-02 13:35

### Classée dans certains runs, aucun levier dans d'autres (1)

#### Fiche 64545 — 1.4.6 Mettre en place un fond vitrine pour redynamiser les centres bourgs

- **Run 1 :** Sobriété foncière [3]
- **Run 2 :** Sobriété foncière [3]
- **Run 3 :** (aucun levier)
- **Prod :** Sobriété et isolation des bâtiments (tertiaire) [3]
- Leviers intermittents : Sobriété foncière (2/3)

> Le diagnostic ACP sur le Sud Creusois, par une enquête en ligne auprès des commerçants, a identifié des besoins de travaux sur les vitrines. Aucun dispositif de soutien ne cible à ce jour les vitrines, CSO préférant agir sur un programme de rénovation d’énergétique d’ensemble du local commercial. Cette démarche nécessitera d’impliquer également les propriétaires bailleurs de locaux commerciaux, car les exploitants sont locataires. Éléments de calendrier : Calendrier Action annuelle et récurrent…

### Levier présent dans certains runs seulement (1)

#### Fiche 63967 — 2.2.3 Déployer une déchèterie mobile

- **Run 1 :** Valorisation matière des déchets [1]
- **Run 2 :** Prévention des déchets [1]
- **Run 3 :** Valorisation matière des déchets [1]
- **Prod :** Valorisation matière des déchets [1, 3]
- Leviers intermittents : Prévention des déchets (1/3), Valorisation matière des déchets (2/3)

> Contexte : Le territoire couvert par la régie Creuse Sud-ouest couvre 27 communes et plus de 630 Km2. La collectivité ne dispose que d'une déchèterie dont la position n'est pas centrale. Une proportion importante des habitants est située à plus 20 minutes en voiture de ce service. Éléments de calendrier : 2025 : travail préliminaire sur besoin du territoire et matériel 2026 : acquisition de l'équipement et déploiement Années suivantes : suivi et ajustements

### Mêmes leviers, catégories différentes (1)

#### Fiche 63973 — 2.3.4 Réduire les déplacements, la consommation des flux : énergie, eau, déchets

- **Run 1 :** Réduction des déplacements [2, 6] | Sobriété des bâtiments (résidentiel) [2, 6]
- **Run 2 :** Réduction des déplacements [2, 6] | Sobriété des bâtiments (résidentiel) [2, 6]
- **Run 3 :** Réduction des déplacements [2] | Sobriété des bâtiments (résidentiel) [2]
- **Prod :** Prévention des déchets [4, 6] | Réduction des déplacements [4, 6]
- Catégories instables sur : Réduction des déplacements, Sobriété des bâtiments (résidentiel)

> Contexte : Cette action en complète d’autres déjà engagées sur la rénovation énergétique ou l’optimisation des équipements en mettant l’accent sur le facteur humain : la sobriété repose en grande partie sur les usages, les arbitrages du quotidien et les comportements individuels et collectifs. Éléments de calendrier : 2026 : Réalisation du diagnostic par service et type d'usagers 2027 : Préconisations et sensibilisations 2028 - 2045 : Déploiement et révision

## Bordeaux Métropole (4322)

- Fiches : **55** — stables sur les 3 runs : **37** (67%), instables : **18**
- Paires levier × catégorie distinctes proposées : 116 — 3/3 runs : 82, 2/3 runs : 10, 1/3 runs : 24
- Vote majoritaire = prod : 2/38 fiches classées d'un côté ou de l'autre
- Réponses JSON invalides rejouées : 0
- Appels : 165 — tokens d'entrée 1 630 605 (dont 1 503 315 en cache, 92%), sortie 11 356 — coût estimé 0.03 $ pour les 3 runs
- Date : 2026-11-02 13:35

### Classée dans certains runs, aucun levier dans d'autres (2)

#### Fiche 34935 — Action 9. Créer une coopérative carbone territoriale en lien avec les territoires voisins

- **Run 1 :** Sobriété foncière [4]
- **Run 2 :** (aucun levier)
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété foncière (1/3)

> 1. Mettre en place un groupe de travail réunissant les directions métropolitaines actrices de la transition, le conseil des partenaires et les territoires girondins 2. Définir une stratégie territorialisée de réduction des émissions et de compensation carbone : analyse quantitative du potentiel permettant d’évaluer le périmètre de la coopérative carbone, analyse qualitative avec identification des acteurs locaux, analyse de la demande de compensation et des besoins de réduction des émissions, é…

#### Fiche 34975 — Action 49. Inciter à une consommation sobre, utile et durable

- **Run 1 :** Prévention des déchets [6]
- **Run 2 :** Prévention des déchets [6]
- **Run 3 :** (aucun levier)
- **Prod :** Prévention des déchets [5, 6]
- Leviers intermittents : Prévention des déchets (2/3)

> 1. Intégrer l'empreinte carbone dans les marchés à chaque fois que pertinent et une évaluation des gaz à effet de serre lors de l’exécution du marché 2. Intégrer des clauses incitatives ou des critères de sélection dédiés dans ses marchés pour contribuer à la lutte contre l’obsolescence programmée et à l’allongement de la durée d’usage notamment dans le secteur du numérique 3.Etudier la faisabilité de promouvoir les achats responsables dans les politiques d'achat communales 4. Dans le cadre du …

### Levier présent dans certains runs seulement (6)

#### Fiche 34933 — Action 7. Renforcer la transition énergétique et écologique dans les partenariats avec les communes,  les territoires voisins et à l’international

- **Run 1 :** Electricité renouvelable [3, 6] | Réduction des déplacements [6]
- **Run 2 :** Electricité renouvelable [3, 6] | Sobriété foncière [2]
- **Run 3 :** Electricité renouvelable [3, 6] | Vélo et transport en commun [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Réduction des déplacements (1/3), Sobriété foncière (1/3), Vélo et transport en commun (1/3)

> 1. Renforcer le soutien apporté à la transition énergétique et écologique des communes métropolitaines au travers les contrats de CODEV et des règlements d’intervention en mesurant l’impact carbone des projets soutenus et leur contribution au bilan carbone de la Métropole 2. Approfondir ce soutien aux communes en leur offrant la possibilité de participer pleinement à la co construction des stratégies et outils nécessaires à l'atteinte de leurs objectifs de décarbonation. Afin de concrétiser ce …

#### Fiche 34946 — Action 20. Développer la production locale de gaz renouvelable

- **Run 1 :** Biogaz [1] | Valorisation matière des déchets [1]
- **Run 2 :** Biogaz [1]
- **Run 3 :** Biogaz [1]
- **Prod :** Biogaz [1, 4]
- Leviers intermittents : Valorisation matière des déchets (1/3)

> 1. Développer des projets de méthanisation sur les stations d'épuration de Bordeaux Métropole pour injecter a minima 50 GWh de biogaz d’ici 2026 2. Valoriser 50% a minima de la collecte des biodéchets en production de biogaz à 2028 3. Développer un méthaniseur industriel de 30 GWh d’ici 2026 : projet Cap vert énergie sur le port avec du biogaz injecté dans le réseau 4. Etudier et engager le développement de deux projets de méthaniseurs de 30GWh à l’horizon 2032 et 2038 avec les territoires vois…

#### Fiche 34952 — Action 26. Anticiper les emplois de demain et accompagner les filières économiques émergeantes nécessaires à l’atteinte des objectifs du plan climat

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [6] | Efficacité et sobriété logistique [3] | Vélo et transport en commun [3]
- **Run 2 :** Efficacité et sobriété logistique [3] | Prévention des déchets [3] | Réduction des déplacements [3]
- **Run 3 :** Efficacité et sobriété logistique [3] | Fret décarboné et multimodalité [3]
- **Prod :** (aucun levier)
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (1/3), Fret décarboné et multimodalité (1/3), Prévention des déchets (1/3), Réduction des déplacements (1/3), Vélo et transport en commun (1/3)

> 1. Lancer une étude « état des lieux et perspectives de développement des emplois verts » dans le cadre de la convention entre Bordeaux Métropole et l’A’urba pour anticiper la création des emplois de demain et la formation initiale et continue en lien avec la transition écologique du tissu économique. Coordonner avec la Région Nouvelle-Aquitaine, les ambitions métropolitaine de développement économique et de formation. 2. Massifier les clauses d’insertion dans la commande publique métropolitain…

#### Fiche 34955 — Action 29. Accompagner les acteurs économiques dans l’adoption de process sobres en énergie et en carbone

- **Run 1 :** Changement de chaudière à gaz (tertiaire) [6] | Production Industrielle [6] | Sobriété et isolation des bâtiments (tertiaire) [6]
- **Run 2 :** Production Industrielle [6] | Sobriété et isolation des bâtiments (tertiaire) [6]
- **Run 3 :** Production Industrielle [6] | Sobriété et isolation des bâtiments (tertiaire) [6]
- **Prod :** Production Industrielle [3, 4, 6]
- Leviers intermittents : Changement de chaudière à gaz (tertiaire) (1/3)

> 1. Co-construire et diffuser un kit d'accompagnement à la transition écologique des acteurs économiques visant à˚: (1)présenter l'offre de service globale de la Métropole sur les thématiques mobilités, 1M d’arbres, rénovation énergétique, étudier techniquement et économiquement l’installation de panneaux photovoltaïques, numérique responsable, déchets, … (2)accélérer et amplifier le passage à l'acte des entreprises (3)optimiser la prospection et la promotion des dispositifs d'accompagnement de …

#### Fiche 34966 — Action 40. Définir une zone à Faibles Emissions mobilité

- **Run 1 :** Covoiturage [2] | Efficacité et carburants décarbonés des véhicules privés [2, 3]
- **Run 2 :** Efficacité et carburants décarbonés des véhicules privés [2, 3] | Véhicules électriques [2]
- **Run 3 :** Efficacité et carburants décarbonés des véhicules privés [2, 3] | Véhicules électriques [2]
- **Prod :** Efficacité et carburants décarbonés des véhicules privés [2, 3] | Véhicules électriques [2, 3] | Vélo et transport en commun [1, 2]
- Leviers intermittents : Covoiturage (1/3), Véhicules électriques (2/3)

> 1. Déploiement d’une concertation ciblée (acteurs économiques, associatifs, acteurs de la santé, institutionnels) au premier semestre 2022 2. Mise en place d’une signalétique adaptée aux abords de la rocade notamment en 2023 3. Déploiement du dispositif de contrôle à partir de fin 2023 (travail avec l’Etat sur le contrôle semi-automatisé 4. Mettre en place un dispositif de suivi avec une gouvernance associée pour apporter les ajustements nécessaires dans le déploiement de la ZFE-m 5. Mettre en …

#### Fiche 34978 — Action 52. Promouvoir un urbanisme durable et favorable à la santé

- **Run 1 :** Réduction des déplacements [2] | Sobriété foncière [2]
- **Run 2 :** Sobriété et isolation des bâtiments (tertiaire) [2] | Sobriété foncière [2]
- **Run 3 :** Sobriété et isolation des bâtiments (tertiaire) [2] | Sobriété foncière [2]
- **Prod :** (aucun levier)
- Leviers intermittents : Réduction des déplacements (1/3), Sobriété et isolation des bâtiments (tertiaire) (2/3)

> 1. Imposer un référentiel d’aménagement inspiré du label bâtiment frugal bordelais, regroupant l'ensemble des critères à respecter pour les projets d'aménagements permettant de faciliter l'appropriation des enjeux environnementaux par l’ensemble des acteurs concernés (bilan carbone, biodiversité, mobilité, énergies renouvelables, air, …) 2. Systématiser la réalisation de bilan carbone des opérations d’aménagement 3. Multiplier les évaluations d'impact en santé dans les projets d'aménagement pou…

### Mêmes leviers, catégories différentes (10)

#### Fiche 34944 — Action 18. Développer la production d'électricité renouvelable et locale

- **Run 1 :** Electricité renouvelable [1, 2]
- **Run 2 :** Electricité renouvelable [1]
- **Run 3 :** Electricité renouvelable [1, 2]
- **Prod :** Electricité renouvelable [1, 5, 6]
- Catégories instables sur : Electricité renouvelable

> 1. "Développer les installations photovoltaïques sur ombrières : (1) Objectif de 100 MWc installés à l’horizon 2028 (production de 105 GWh) puis 160 MWc à long terme (2) Privilégier les installations de grande taille (plus de 5 000m²) et a minima sur des parkings de plus de 1 500m² (projets de plus de 100 kWc). (3)Equilibrer les objectifs énergétiques et les objectifs écologiques : équiper à terme environ 60% des parkings d’ombrières photovoltaïques (et 85% des parkings de plus de 5 000 m²), et…

#### Fiche 34947 — Action 21. Importer des énergies renouvelables

- **Run 1 :** Electricité renouvelable [4, 6]
- **Run 2 :** Electricité renouvelable [2, 4]
- **Run 3 :** Electricité renouvelable [4, 6]
- **Prod :** Electricité renouvelable [3, 4, 6]
- Catégories instables sur : Electricité renouvelable

> 1. Soutenir le développement de projets EnR régionaux grâce à Bordeaux Métropole Energies et à la coopérative carbone 2. Structurer et mettre en place un suivi de l’achat d’énergie renouvelable en partenariat avec les observatoires existants (ALEC, AREC, …), pour collecter et traiter des données sur l’approvisionnement en gaz et électricité vertes des acteurs publics, entreprises et ménages, dans le but de développer les mécanismes d’achat direct 3. Soutenir la création, d’une structure et/ou d…

#### Fiche 34957 — Action 31. Réduire la production des déchets

- **Run 1 :** Prévention des déchets [2, 4, 6]
- **Run 2 :** Prévention des déchets [2, 6]
- **Run 3 :** Prévention des déchets [2, 4, 6]
- **Prod :** Prévention des déchets [2, 3, 6] | Valorisation matière des déchets [6]
- Catégories instables sur : Prévention des déchets

> 1. Développer les actions de sensibilisation et d'animation à destination de tous les publics sur l'ensemble des thématiques zéro déchet zéro gaspillage (évènements zéro déchets, communications de proximité, Juniors du développement durable, etc.) 2. Réduire les déchets des entreprises : information sur leurs obligations réglementaires, mise à disposition d'outils et mise en place d'un réseau d'entreprise 3. Accompagner les communes vers des actions de réduction des déchets auprès de leurs habi…

#### Fiche 34961 — Action 35. Amplifier l'usage du vélo

- **Run 1 :** Vélo et transport en commun [1, 3, 4, 5, 6]
- **Run 2 :** Vélo et transport en commun [1, 3, 6]
- **Run 3 :** Vélo et transport en commun [1, 3, 6]
- **Prod :** Vélo et transport en commun [1, 3, 5, 6]
- Catégories instables sur : Vélo et transport en commun

> 1. Développer un réseau cyclable performant grâce au réseau vélo express (ReVE), à l’entretien et au développement des aménagements cyclables, à une mise à jour du guide des aménagements cyclables, à un jalonnement d’itinéraires cyclables 2. Permettre de stationner son vélo en toute sécurité par le déploiement d’arceaux vélos, le développement d’offre de stationnement vélo sécurisé et l’amélioration des locaux à vélos dans les constructions neuves 3. Développer les services autour du vélo notam…

#### Fiche 34962 — Action 36. Favoriser la pratique de la marche

- **Run 1 :** Réduction des déplacements [1, 2, 6]
- **Run 2 :** Réduction des déplacements [1, 6]
- **Run 3 :** Réduction des déplacements [1, 2, 6]
- **Prod :** Vélo et transport en commun [1, 2, 6]
- Catégories instables sur : Réduction des déplacements

> 1. Concevoir un espace public plus marchable par la mise en œuvre de zones marchables, le désencombrement des trottoirs, l’intégration dans les documents de planification, l’élaboration de plan d’accessibilité de la voirie et des espaces publics, la mise en conformité des passages piétons 2. Favoriser des déplacements scolaires piétons autonomes par l’expérimentation de fermeture de rues d’écoles, d’incitation à l’écomobilité scolaire (pédibus, vélobus) 3. Articuler la marche et les transports …

#### Fiche 34963 — Action 37. Développer les usages partagés de l'automobile

- **Run 1 :** Covoiturage [1, 4]
- **Run 2 :** Covoiturage [1, 4]
- **Run 3 :** Covoiturage [1, 6]
- **Prod :** Covoiturage [1, 4, 6]
- Catégories instables sur : Covoiturage

> 1. Développer le covoiturage pour les déplacements de moyenne et longue distance grâce à un plan coordonné multipartenarial de covoiturage afin de développer les voies réservées au covoiturage, les aires de covoiturage 2. Développer l’autopartage en incitant les communes à dédier des voiries, en proposant aux gestionnaires de parkings ouverts de créer des places réservées, en expérimentant un service d’autopartage dans des opérations immobilières mixtes et en sensibilisant les salariés des entr…

#### Fiche 34964 — Action 38. Décarboner les véhicules motorisés

- **Run 1 :** Bus et cars décarbonés [1] | Efficacité et carburants décarbonés des véhicules privés [1] | Véhicules électriques [1]
- **Run 2 :** Bus et cars décarbonés [1, 2] | Efficacité et carburants décarbonés des véhicules privés [1, 6] | Véhicules électriques [1, 2]
- **Run 3 :** Bus et cars décarbonés [1] | Efficacité et carburants décarbonés des véhicules privés [1] | Véhicules électriques [1]
- **Prod :** Bus et cars décarbonés [1] | Efficacité et carburants décarbonés des véhicules privés [5] | Véhicules électriques [1] | Vélo et transport en commun [2]
- Catégories instables sur : Bus et cars décarbonés, Efficacité et carburants décarbonés des véhicules privés, Véhicules électriques

> 1. Etablir un schéma directeur des installations de recharge des véhicule électrique (SDIRVE), planifiant notamment la mise à disposition au public d’un vaste parc de bornes de recharge pour véhicules électriques en exploitant de nouveau les 170 bornes de l’ancien serMettre progressivement en place une flotte de bus TBM décarbonée pour remplacer d’ici 2028 les bus diesel et hybrides par des bus électriques et bioGNVvice Bluecub et en incitant au déploiement d’offres privées 2. Mettre progressiv…

#### Fiche 34967 — Action 41. Accompagner le développement du télétravail

- **Run 1 :** Réduction des déplacements [1, 4]
- **Run 2 :** Réduction des déplacements [1, 2, 3]
- **Run 3 :** Réduction des déplacements [1, 2]
- **Prod :** Réduction des déplacements [1, 4, 6]
- Catégories instables sur : Réduction des déplacements

> 1. Réaliser une étude pour mesurer l’adhésion des entreprises de la métropole et de leurs salariés à la mise en place de lieux de travail à distance partagés (analyse des pratiques et appétence des entreprises pour réduire leur empreinte immobilière et carbone, évaluation de la valeur potentielle du service, recensement des besoins d’accompagnement ; étude des conditions d’adhésion des salariés résidant dans la métropole et dans les EPCI voisins, analyse de la localisation potentielle des sites…

#### Fiche 34969 — Action 43. Rénover et décarboner le secteur tertiaire public et privé

- **Run 1 :** Changement de chaudière à fioul (tertiaire) [5] | Changement de chaudière à gaz (tertiaire) [5] | Sobriété et isolation des bâtiments (tertiaire) [2, 5]
- **Run 2 :** Changement de chaudière à fioul (tertiaire) [1, 5] | Changement de chaudière à gaz (tertiaire) [1, 5] | Sobriété et isolation des bâtiments (tertiaire) [2, 5]
- **Run 3 :** Changement de chaudière à fioul (tertiaire) [5] | Changement de chaudière à gaz (tertiaire) [5] | Sobriété et isolation des bâtiments (tertiaire) [2, 5]
- **Prod :** Changement de chaudière à fioul (tertiaire) [5] | Sobriété et isolation des bâtiments (tertiaire) [3, 5, 6]
- Catégories instables sur : Changement de chaudière à fioul (tertiaire), Changement de chaudière à gaz (tertiaire)

> 1. Sur le patrimoine public, réaliser un diagnostic énergétique de l’ensemble des bâtiments, un schéma directeur immobilier pour prioriser les rénovations et proposer un conseiller en énergie partagé pour tous les bâtiments communaux, y compris ceux inférieurs à 1000 m2. 2. Accélérer la conversion des équipements de chauffage carbonés (et en priorité ceux au fioul) des bâtiments publics vers de la chaleur renouvelable en accompagnement de la loi Climat et résilience 3. Accompagner les maitres d…

#### Fiche 34976 — Action 50. Privilégier le réemploi pour donner une 2ème vie aux objets

- **Run 1 :** Prévention des déchets [1, 3, 6]
- **Run 2 :** Prévention des déchets [1, 3, 4, 6]
- **Run 3 :** Prévention des déchets [1, 3, 4, 6]
- **Prod :** Prévention des déchets [1, 3, 5, 6]
- Catégories instables sur : Prévention des déchets

> 1. Etudier la mise en place d'un « Allo 2nde vie » en partenariat avec des associations 2. Accompagner techniquement la structuration du réseau des ressourceries à l'échelle métropolitaine 3. Participer à la réalisation du projet Ikos (village du réemploi) en apportant un soutien technique et financier aux porteurs du projet 4. Développer les boites à dons dans les lieux ouverts au public D’ici à 2028, mettre en place six aires de réemploi éphémères installées temporairement à fréquence réguliè…

## CC de la Forêt (4576)

- Fiches : **94** — stables sur les 3 runs : **86** (91%), instables : **8**
- Paires levier × catégorie distinctes proposées : 96 — 3/3 runs : 83, 2/3 runs : 6, 1/3 runs : 7
- Vote majoritaire = prod : 12/63 fiches classées d'un côté ou de l'autre
- Réponses JSON invalides rejouées : 0
- Appels : 282 — tokens d'entrée 2 674 929 (dont 2 569 302 en cache, 96%), sortie 16 306 — coût estimé 0.04 $ pour les 3 runs
- Date : 2026-11-02 13:35

### Levier présent dans certains runs seulement (2)

#### Fiche 40466 — 3.16 Faciliter l'adaptation au changement climatique en soutenant les expérimentations et les nouvelles initiatives

- **Run 1 :** Changements de pratiques de fertilisation azotée [6] | Elevage durable [6] | Pratiques stockantes [6]
- **Run 2 :** Changements de pratiques de fertilisation azotée [6] | Elevage durable [6]
- **Run 3 :** Changements de pratiques de fertilisation azotée [6] | Elevage durable [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Pratiques stockantes (1/3)

> <p>Accompagner les agriculteurs désireux de réaliser un diagnostic permettant d’identifier les vulnérabilités et atouts de leur exploitation</p><p>Dégager des pistes pour modifier les pratiques, réduire les consommations, notamment à travers l’outil CAP’2ER pour les éleveurs</p><p>Informer les agriculteurs sur les études réalisées sur les conduites de culture et sur le changement d’espèces permettant une meilleure adaptation au changement climatique</p><p>Soutenir les expérimentations agricoles…

#### Fiche 40585 — 4. Soutenir le développement des filières d'éco-matériaux (paille, bois, chanvre…)

- **Run 1 :** Gestion des forêts et produits bois [5]
- **Run 2 :** Production Industrielle [5]
- **Run 3 :** Gestion des forêts et produits bois [5]
- **Prod :** Gestion des forêts et produits bois [5]
- Leviers intermittents : Gestion des forêts et produits bois (2/3), Production Industrielle (1/3)

> Les filières d'éco-matériaux (paille, bois, chanvre…) sont developées via la commande publique de la CCF. Des clauses sont intégrées dans les marchés pour intégrer des éco-matéiraux dans les constructions des collectivités.

### Levier intermittent et catégories instables (1)

#### Fiche 40487 — 7.37 Rendre exemplaires les bâtiments et l'éclairage public

- **Run 1 :** Sobriété et isolation des bâtiments (tertiaire) [2, 6]
- **Run 2 :** Changement de chaudière à fioul (tertiaire) [6] | Changement de chaudière à gaz (tertiaire) [6] | Sobriété et isolation des bâtiments (tertiaire) [6]
- **Run 3 :** Sobriété et isolation des bâtiments (tertiaire) [2, 6]
- **Prod :** Changement de chaudière à fioul (tertiaire) [5] | Changement de chaudière à gaz (tertiaire) [5] | Sobriété et isolation des bâtiments (tertiaire) [5]
- Leviers intermittents : Changement de chaudière à fioul (tertiaire) (1/3), Changement de chaudière à gaz (tertiaire) (1/3)
- Catégories instables sur : Sobriété et isolation des bâtiments (tertiaire)

> <p>Informer les communes sur les subventions possibles pour leurs projets de rénovation de bâtiments et de modernisation de l’éclairage public et communiquer sur les guides réalisés par l’ADEME sur ces sujets</p><p>Réaliser un diagnostic de l’ensemble des bâtiments publics du territoire et proposer à chaque commune d’engager un plan de rénovation énergétique</p><p>Favoriser les matériaux locaux et biosourcés dans les futures constructions publiques</p><p>Travailler sur la diminution de l’intens…

### Mêmes leviers, catégories différentes (5)

#### Fiche 40452 — 1.2 Développer les OPAH et accompagner les ménages les plus précaires

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [2, 6] | Changement chaudières gaz + rénovation (résidentiel) [2, 6]
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [2] | Changement chaudières gaz + rénovation (résidentiel) [2]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [2, 6] | Changement chaudières gaz + rénovation (résidentiel) [2, 6]
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6]
- Catégories instables sur : Changement chaudières fioul + rénovation (résidentiel), Changement chaudières gaz + rénovation (résidentiel)

> Mener une étude pré-opérationnelle puis mettre en place d'une OPAH avec des permanences sur le territoire.

#### Fiche 40482 — 5.32 Initier et soutenir des projets "nouvelles énergies" appuyés sur une participation citoyenne

- **Run 1 :** Electricité renouvelable [6]
- **Run 2 :** Electricité renouvelable [3, 6]
- **Run 3 :** Electricité renouvelable [6]
- **Prod :** Electricité renouvelable [4, 6]
- Catégories instables sur : Electricité renouvelable

> <p>Accompagner l’émergence et le déploiement de collectifs citoyens porteurs de projets d’énergies renouvelables en travaillant sur le sujet avec Energie partagée</p><p>Communiquer sur la possibilité pour les citoyens de porter des projets de production d’énergie renouvelable</p><p>Informer les citoyens sur les possibilités de financement de ces projets et soutenir ces projets via les contrats du PETR</p><p>Impulser des dynamiques entre élus et citoyens pour développer des projets d’énergie cit…

#### Fiche 40483 — 5.33 Développer des projets de méthanisation sans concurrencer la production alimentaire

- **Run 1 :** Biogaz [6]
- **Run 2 :** Biogaz [2, 6]
- **Run 3 :** Biogaz [2, 6]
- **Prod :** Biogaz [1, 4, 6]
- Catégories instables sur : Biogaz

> <p>Etudier les réseaux à mettre en place autour de la méthanisation</p><p>Sensibiliser les agriculteurs et le grand public aux avantages de la méthanisation</p><p>Accompagner l’insertion paysagère des projets de méthanisation lorsque les sites ont été identifiés</p>

#### Fiche 40488 — 7.38 Rendre exemplaires les déplacements des administrations

- **Run 1 :** Covoiturage [6] | Réduction des déplacements [5] | Véhicules électriques [5]
- **Run 2 :** Covoiturage [6] | Réduction des déplacements [5] | Véhicules électriques [5]
- **Run 3 :** Covoiturage [5, 6] | Réduction des déplacements [5] | Véhicules électriques [5]
- **Prod :** (aucun levier)
- Catégories instables sur : Covoiturage

> <p>Rendre les flottes autombiles communales et intercommunales moins émettrices lors du renouvellement du parc</p><p>Poursuivre et étendre la politique d’achats de véhicules groupés, entre les structures</p><p>Rendre possibles les échanges de bonnes pratiques entre collectivités en matière de déplacements professionnels</p><p>Limiter, quand cela est possible, les besoins de se déplacer, favoriser le covoiturage</p><p>Communiquer sur Rezo Pouce auprès des agents des collectivités</p>

#### Fiche 40575 — 4.1.5 Mener des réflexions sur le covoiturage (Mobicoop, incitation financière, bassin de mobilité en lien avec OM)

- **Run 1 :** Covoiturage [2]
- **Run 2 :** Covoiturage [6]
- **Run 3 :** Covoiturage [2]
- **Prod :** (aucun levier)
- Catégories instables sur : Covoiturage

> Accueillir des animations sur le territoire de la CCF Relai de communication des actions menées par le PETR Réflexions communes sur la pratique du covoiturage

## CC Baugeois Vallée (4637)

- Fiches : **91** — stables sur les 3 runs : **72** (79%), instables : **19**
- Paires levier × catégorie distinctes proposées : 131 — 3/3 runs : 103, 2/3 runs : 11, 1/3 runs : 17
- Vote majoritaire = prod : 8/70 fiches classées d'un côté ou de l'autre
- Réponses JSON invalides rejouées : 0
- Appels : 273 — tokens d'entrée 2 760 837 (dont 2 487 303 en cache, 90%), sortie 16 505 — coût estimé 0.06 $ pour les 3 runs
- Date : 2026-11-02 13:35

### Classée dans certains runs, aucun levier dans d'autres (3)

#### Fiche 32286 — COT 4. Réaliser une évaluation "climat" du budget

- **Run 1 :** (aucun levier)
- **Run 2 :** (aucun levier)
- **Run 3 :** Sobriété et isolation des bâtiments (tertiaire) [4]
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété et isolation des bâtiments (tertiaire) (1/3)

> 2024 Juillet : Nommer une équipe transversale sur le budget vert : Guillaume, Nicolas et Anaïs (+ Maxime - achats durables ?) Août : Définir en interne, à partir des ressources et doctrines existantes, une grille d’analyse des dépenses d’investissement (pour savoir ce qui favorable/indéterminé/défavorable) qui sera diffusé aux services en amont de la préparation budgétaire Août : Ajouter une colonne dans la matrice budgétaire pour renseigner cette approche « budget vert » Août : Intégration dan…

#### Fiche 144000 — Action 1 : Constitution de la CCES et structuration des données du territoire

- **Run 1 :** Sobriété des bâtiments (résidentiel) [4]
- **Run 2 :** (aucun levier)
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété des bâtiments (résidentiel) (1/3)

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="ac4c461a-ac09-4a23-8a50-4ed073022c71"><div class="bn-block" data-node-type="blockContainer" data-id="ac4c461a-ac09-4a23-8a50-4ed073022c71"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]">Recenser les acteurs représentatifs : élus, chambres consulaires, représentants sociétés civiles, citoye…

#### Fiche 144002 — Action 3 : Réduire l’impact climatique des déchets sur le territoire

- **Run 1 :** Valorisation matière des déchets [1]
- **Run 2 :** Valorisation matière des déchets [1]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Valorisation matière des déchets (2/3)

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="d3be00f1-0f74-4de1-a0fc-bff01dfde2a9"><div class="bn-block" data-node-type="blockContainer" data-id="d3be00f1-0f74-4de1-a0fc-bff01dfde2a9"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]">Le service gestion et valorisation des déchets, en transversalité avec les autres services de la collect…

### Levier présent dans certains runs seulement (3)

#### Fiche 32302 — COT 21. Accompagner le développement d'une offre de tourisme et de loisirs "sans ma voiture"

- **Run 1 :** Vélo et transport en commun [6]
- **Run 2 :** Vélo et transport en commun [6]
- **Run 3 :** Covoiturage [6] | Vélo et transport en commun [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Covoiturage (1/3)

> - Recenser l’ensemble des offres de transports : Vers Baugeois- Vallée Vers les métropoles (gares) Pointer les Forces, Faiblesses, Opportunités et Menaces. Recensement des offres touristiques et de loisirs sur Baugeois-vallée Rechercher ce qui se fait ailleurs et comment Recouper les données et construire les offres Impliquer les prestataires / habitants (Greeters) / élus dans la démarche Tester Promouvoir/Communiquer

#### Fiche 72498 — 16. Accompagner les employeurs publics/privés et leurs salariés vers l’écomobilité

- **Run 1 :** Covoiturage [4] | Efficacité et carburants décarbonés des véhicules privés [6] | Vélo et transport en commun [6]
- **Run 2 :** Covoiturage [4] | Efficacité et carburants décarbonés des véhicules privés [6] | Vélo et transport en commun [6]
- **Run 3 :** Covoiturage [4] | Réduction des déplacements [6] | Vélo et transport en commun [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Efficacité et carburants décarbonés des véhicules privés (2/3), Réduction des déplacements (1/3)

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="d3253af6-2b45-4542-baca-d39f29364681"><div class="bn-block" data-node-type="blockContainer" data-id="d3253af6-2b45-4542-baca-d39f29364681"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]">84% des trajets domicile-travail sur le territoire de Baugeois-Vallée sont effectués en voiture en 2017.…

#### Fiche 72512 — 29. Optimiser l’irrigation agricole

- **Run 1 :** Bâtiments & Machines agricoles [6] | Gestion des haies [6]
- **Run 2 :** Bâtiments & Machines agricoles [6] | Gestion des haies [6]
- **Run 3 :** Bâtiments & Machines agricoles [6] | Pratiques stockantes [6]
- **Prod :** Bâtiments & Machines agricoles [6] | Gestion des haies [6] | Pratiques stockantes [6]
- Leviers intermittents : Gestion des haies (2/3), Pratiques stockantes (1/3)

> <p>Le territoire de la CCBV est fortement concerné par les effets du changement climatique sur la ressource en eau. L’agriculture, très présente localement, représente un poste majeur de consommation, et sa résilience dépend d’une gestion plus économe et partagée de cette ressource. Cette action s’inscrit dans les objectifs du PCAET, renforcés par les dynamiques régionales portées par la Chambre d’agriculture et les SAGE Loir et Authion.</p><p>&nbsp;</p><p>·&nbsp;&nbsp;&nbsp;&nbsp; <strong>Prom…

### Levier intermittent et catégories instables (1)

#### Fiche 32289 — COT 7. Suivre les consommations énergétiques par service

- **Run 1 :** Efficacité et carburants décarbonés des véhicules privés [2] | Sobriété et isolation des bâtiments (tertiaire) [2, 4, 5]
- **Run 2 :** Efficacité et carburants décarbonés des véhicules privés [2, 5] | Sobriété et isolation des bâtiments (tertiaire) [2, 5]
- **Run 3 :** Covoiturage [5] | Sobriété et isolation des bâtiments (tertiaire) [2, 5]
- **Prod :** Sobriété et isolation des bâtiments (tertiaire) [5]
- Leviers intermittents : Covoiturage (1/3), Efficacité et carburants décarbonés des véhicules privés (2/3)
- Catégories instables sur : Sobriété et isolation des bâtiments (tertiaire)

> Consommation des bâtiments - Renseigner le tableau de suivi avec les surfaces de chaque bâtiment - Renseigner le tableau de suivi avec les consommations énergétiques par bâtiment et par an - Produire des indicateurs de suivi : consommation globale des bâtiments, rapportés à la surface totale et à la population totale - Communiquer sur ces indicateurs (rapport d’activités) - Relancer le partenariat avec le SIEML (conseil en énergie partagé) pour établir un diagnostic énergétique de nos bâtiments…

### Mêmes leviers, catégories différentes (12)

#### Fiche 32304 — COT 23. Soutenir les énergies citoyennes

- **Run 1 :** Electricité renouvelable [4]
- **Run 2 :** Electricité renouvelable [4, 6]
- **Run 3 :** Electricité renouvelable [4, 6]
- **Prod :** (aucun levier)
- Catégories instables sur : Electricité renouvelable

> Avec la signature de la charte citoyenne , la CCBV s’engage à faire intervenir plus de citoyens dans les projets L'intérêt est de faire valoir l'apport de l'intégration des citoyens dans les projets au niveau politique avec les élus de la CCBV. La CCBV à adhéré au partenaire RECIT cela permet d'être intégré dans le réseau et d'avoir accès à des webinaires et des formations L'objectif est de sensibiliser les élus mais également de parler aux habitants en montrant qu’ils peuvent s’inscrire dans l…

#### Fiche 32306 — COT 24. Mettre en œuvre le plan de prévention des déchets, avec le suivi des objectifs et indicateurs

- **Run 1 :** Prévention des déchets [2]
- **Run 2 :** Prévention des déchets [2, 4]
- **Run 3 :** Prévention des déchets [2]
- **Prod :** (aucun levier)
- Catégories instables sur : Prévention des déchets

> La communauté de communes Baugeois-Vallée, en charge de la compétence « collecte, gestion et valorisation des déchets », doit mettre en place son propre programme, comme prévu par le décret n°2015- 662 du 14 juin 2015. Ce PLPDMA est un document de planification territorial obligatoire depuis le 1er janvier 2012, règlementé par le décret n°2015-662 du 10 juin 2015. Ce plan a été élaboré en 2022 puis validé en 2023. L’objectif du PLPDMA vise la réduction des déchets ménagers et assimilés et d’une…

#### Fiche 32311 — COT 29. Préserver l'aire de captage de Beaufort

- **Run 1 :** Changements de pratiques de fertilisation azotée [6] | Gestion des haies [2] | Pratiques stockantes [6]
- **Run 2 :** Changements de pratiques de fertilisation azotée [6] | Gestion des haies [6] | Pratiques stockantes [6]
- **Run 3 :** Changements de pratiques de fertilisation azotée [6] | Gestion des haies [2] | Pratiques stockantes [6]
- **Prod :** (aucun levier)
- Catégories instables sur : Gestion des haies

> Fiabiliser la délimitation de l’aire d’alimentation de captage Mettre en place un comité de suivi Déployer le programme agro environnemental et climatique : - Diagnostic agricole - Dossier de demande auprès de la DRAFF - Communication sur le dispositif - Sollicitation d’agriculteurs volontaires - Accompagnement des agriculteurs Sensibiliser à des pratiques vertueuses (changement de pratique, rotation des cultures…) Réfléchir à une politique foncière autour des captages, maîtrise foncière avec b…

#### Fiche 72496 — 14. Encourager le covoiturage

- **Run 1 :** Covoiturage [6]
- **Run 2 :** Covoiturage [6]
- **Run 3 :** Covoiturage [1, 6]
- **Prod :** (aucun levier)
- Catégories instables sur : Covoiturage

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="82e0b1f7-1039-4444-b418-21e37dce8746"><div class="bn-block" data-node-type="blockContainer" data-id="82e0b1f7-1039-4444-b418-21e37dce8746"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]">Le secteur des transports routiers constitue le premier poste consommateur d’énergie sur le territoire d…

#### Fiche 72497 — 15. Promouvoir le transport à la demande

- **Run 1 :** Vélo et transport en commun [3, 4, 6]
- **Run 2 :** Vélo et transport en commun [3, 6]
- **Run 3 :** Vélo et transport en commun [3, 4, 6]
- **Prod :** (aucun levier)
- Catégories instables sur : Vélo et transport en commun

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="a44767a0-7378-48be-aa35-c3350b53dafc"><div class="bn-block" data-node-type="blockContainer" data-id="a44767a0-7378-48be-aa35-c3350b53dafc"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]">Dans un territoire rural comme Baugeois-Vallée, l’accès aux services et à la mobilité reste inégal, nota…

#### Fiche 72501 — 19. Développer la méthanisation

- **Run 1 :** Biogaz [2, 6]
- **Run 2 :** Biogaz [2, 6]
- **Run 3 :** Biogaz [2, 4, 6]
- **Prod :** Biogaz [2, 4]
- Catégories instables sur : Biogaz

> <p>Le territoire de la CCBV présente un fort potentiel agricole et des enjeux d’autonomie énergétique, mais le développement de la filière de méthanisation nécessite une structuration cohérente, une bonne acceptabilité sociale, et une coordination étroite entre acteurs publics, agriculteurs et habitants.</p><p>&nbsp;</p><p><strong>Définir une stratégie territoriale de développement de la méthanisation</strong></p><ul><li><p><strong>Identifier les potentiels et acteurs concernés</strong> : carto…

#### Fiche 72502 — 20. Développer l’éolien

- **Run 1 :** Electricité renouvelable [1, 2]
- **Run 2 :** Electricité renouvelable [1, 2]
- **Run 3 :** Electricité renouvelable [1, 2, 4, 6]
- **Prod :** Electricité renouvelable [2, 6]
- Catégories instables sur : Electricité renouvelable

> <p>Le territoire de la CCBV bénéficie d’un gisement de vent favorable, identifié dans le diagnostic du PCAET. Toutefois, les projets éoliens restent sensibles : les enjeux de paysage, biodiversité et acceptabilité sociale nécessitent un travail de concertation renforcé et une stratégie intercommunale partagée.</p><p>&nbsp;</p><p>·&nbsp;&nbsp;&nbsp;&nbsp; <strong>Définir une stratégie de développement de la filière éolienne&nbsp;:</strong></p><p>o&nbsp;&nbsp; <strong>Identifier et cartographier …

#### Fiche 72504 — 22. Développer le solaire au sol

- **Run 1 :** Electricité renouvelable [1, 2, 6]
- **Run 2 :** Electricité renouvelable [2, 6]
- **Run 3 :** Electricité renouvelable [1, 2, 6]
- **Prod :** Electricité renouvelable [2, 6]
- Catégories instables sur : Electricité renouvelable

> <p>Le territoire bénéficie d’un bon ensoleillement et de nombreuses surfaces disponibles (zones d’activités, friches, anciennes carrières, foncier agricole). L’atlas des sites favorables au solaire et les travaux sur les ZAEnR permettent d’identifier les parcelles à fort potentiel. La CCBV souhaite structurer le développement du solaire au sol en conciliant production d’énergie, respect des sols et de la biodiversité.</p><p>&nbsp;</p><p>·&nbsp;&nbsp;&nbsp;&nbsp; <strong>Identifier les opportuni…

#### Fiche 72506 — 23. Favoriser une gouvernance partagée et les projets citoyens pour les projets d’ENR

- **Run 1 :** Electricité renouvelable [6]
- **Run 2 :** Electricité renouvelable [6]
- **Run 3 :** Electricité renouvelable [2, 6]
- **Prod :** (aucun levier)
- Catégories instables sur : Electricité renouvelable

> <p>Le développement des énergies renouvelables (ENR) suscite des interrogations et nécessite une meilleure acceptabilité. Les projets citoyens ou à gouvernance partagée permettent d’impliquer les habitants et collectivités dans la transition énergétique, en leur offrant une participation directe aux décisions et aux bénéfices. Avec la signature en 2023 de la charte pour des projets d’énergies renouvelables à gouvernance locale en Maine-et-Loire, la CCBV s’engage à faire intervenir plus de citoy…

#### Fiche 72507 — 24. Encourager la plantation de haies et d’arbres

- **Run 1 :** Gestion des forêts et produits bois [6] | Gestion des haies [3, 6]
- **Run 2 :** Gestion des forêts et produits bois [6] | Gestion des haies [3, 6]
- **Run 3 :** Gestion des forêts et produits bois [2] | Gestion des haies [3, 6]
- **Prod :** Gestion des haies [2, 3, 6] | Pratiques stockantes [3, 6]
- Catégories instables sur : Gestion des forêts et produits bois

> <p>La préservation des zones humides et des arbres en place, en particulier les arbres isolés, les haies et les boisements fait partie des grands enjeux du territoire sous l’effet des activités humaines. La CCBV s’inscrit dans une dynamique de reconquête de son paysage et écosystème, appuyée par la charte forestière de territoire, la politique agricole locale et les dispositifs de replantation de haies.</p><p>&nbsp;</p><p>·&nbsp;&nbsp;&nbsp;&nbsp; <strong>Renforcer les plantations de haies et l…

#### Fiche 144017 — Action 18 : Accompagner les établissements scolaires au tri à la source des biodéchets

- **Run 1 :** Prévention des déchets [5, 6]
- **Run 2 :** Prévention des déchets [5, 6]
- **Run 3 :** Prévention des déchets [1, 6]
- **Prod :** Valorisation matière des déchets [1, 5, 6]
- Catégories instables sur : Prévention des déchets

> Accompagner techniquement les demandes des établissements scolaires pour l’installation d’un composteur partagé. Fournir le matériel. Former les référents adultes et les utilisateurs (élèves, enseignantes, autre personnel).

#### Fiche 144025 — Action 26 : Promotion textiles lavables

- **Run 1 :** Prévention des déchets [1, 3]
- **Run 2 :** Prévention des déchets [1, 3, 6]
- **Run 3 :** Prévention des déchets [1, 3, 6]
- **Prod :** Prévention des déchets [3, 6]
- Catégories instables sur : Prévention des déchets

> Maintenir les aides à l’achat aux couches lavables. Proposer une nouvelle possibilité : celle d’essayer des kits de prêt pendant 1-2 mois avec un partenaire professionnel de couches lavables. Ateliers d’informations aux couches lavables pour les parents. Ateliers de formation aux couches lavables pour les professionnels de la petite enfance. Communication générale sur les textiles lavables dont les couches lavables.

## CC du Pays de Colombey et du Sud Toulois (4707)

- Fiches : **83** — stables sur les 3 runs : **77** (93%), instables : **6**
- Paires levier × catégorie distinctes proposées : 85 — 3/3 runs : 71, 2/3 runs : 7, 1/3 runs : 7
- Vote majoritaire = prod : 14/66 fiches classées d'un côté ou de l'autre
- Réponses JSON invalides rejouées : 0
- Appels : 249 — tokens d'entrée 2 355 804 (dont 2 268 639 en cache, 96%), sortie 14 862 — coût estimé 0.04 $ pour les 3 runs
- Date : 2026-11-02 13:35

### Classée dans certains runs, aucun levier dans d'autres (2)

#### Fiche 51807 — Promouvoir les matériaux biosourcés (laine de bois, laine de mouton …) garantissant à la fois un confort d’été

- **Run 1 :** (aucun levier)
- **Run 2 :** Sobriété foncière [6]
- **Run 3 :** Sobriété foncière [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété foncière (2/3)

#### Fiche 51862 — lavage de laine, re localisation et mutualisation d'un outil de lavage

- **Run 1 :** (aucun levier)
- **Run 2 :** Efficacité et sobriété logistique [1]
- **Run 3 :** Efficacité et sobriété logistique [4]
- **Prod :** (aucun levier)
- Leviers intermittents : Efficacité et sobriété logistique (2/3)

### Levier présent dans certains runs seulement (2)

#### Fiche 51805 — Communiquer sur les moyens d'isolation

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6]
- **Run 2 :** Sobriété des bâtiments (résidentiel) [6]
- **Run 3 :** Sobriété des bâtiments (résidentiel) [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (1/3), Changement chaudières gaz + rénovation (résidentiel) (1/3), Sobriété des bâtiments (résidentiel) (2/3)

#### Fiche 51849 — Recenser le foncier agricole communal disponible

- **Run 1 :** Sobriété foncière [2]
- **Run 2 :** Changements de pratiques de fertilisation azotée [3] | Pratiques stockantes [3] | Sobriété foncière [2]
- **Run 3 :** Changements de pratiques de fertilisation azotée [3] | Pratiques stockantes [3] | Sobriété foncière [2]
- **Prod :** (aucun levier)
- Leviers intermittents : Changements de pratiques de fertilisation azotée (2/3), Pratiques stockantes (2/3)

> Aider à l'implantation de producteurs locaux « cultures végétales » (mobilisation du foncier disponible, subvention à l’installation …) dont les productions sont destinées au marché local

### Mêmes leviers, catégories différentes (2)

#### Fiche 51809 — Donner la priorité à la rénovation énergétique chez les particuliers

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [2] | Changement chaudières gaz + rénovation (résidentiel) [2]
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [2] | Changement chaudières gaz + rénovation (résidentiel) [2]
- **Prod :** (aucun levier)
- Catégories instables sur : Changement chaudières fioul + rénovation (résidentiel), Changement chaudières gaz + rénovation (résidentiel)

#### Fiche 51848 — Les surplus de broyage des plates-formes sont proposés en apport carbone pour épandage.

- **Run 1 :** Gestion des forêts et produits bois [6]
- **Run 2 :** Gestion des forêts et produits bois [1]
- **Run 3 :** Gestion des forêts et produits bois [6]
- **Prod :** Pratiques stockantes [6]
- Catégories instables sur : Gestion des forêts et produits bois

## CC du Pays de Barr (4939)

- Fiches : **41** — stables sur les 3 runs : **37** (90%), instables : **4**
- Paires levier × catégorie distinctes proposées : 47 — 3/3 runs : 43, 2/3 runs : 3, 1/3 runs : 1
- Vote majoritaire = prod : 17/39 fiches classées d'un côté ou de l'autre
- Réponses JSON invalides rejouées : 0
- Appels : 123 — tokens d'entrée 1 519 698 (dont 1 120 653 en cache, 74%), sortie 7 399 — coût estimé 0.05 $ pour les 3 runs
- Date : 2026-11-02 13:35

### Classée dans certains runs, aucun levier dans d'autres (1)

#### Fiche 88641 — 3.1.2.2. Participer au contrat opérationnel de mobilité : être force de proposition auprès de la Région Grand Est

- **Run 1 :** Vélo et transport en commun [4]
- **Run 2 :** Vélo et transport en commun [4]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Vélo et transport en commun (2/3)

> <p class="!text-base !text-grey-8 font-[Marianne]">La Communauté de communes du Pays de Barr est associée aux EPCI limitrophes dans un même bassin de mobilité.</p><p>&nbsp;</p><p class="!text-base !text-grey-8 font-[Marianne]">Cette échelle de bassin doit permettre de coordonner, en lien avec la Région, les liaisons interurbaines, d’expérimenter des actions entre les territoires et de réfléchir à une offre de mobilité au plus près des besoins des habitants et des enjeux locaux, en lien avec les…

### Levier présent dans certains runs seulement (3)

#### Fiche 88637 — 1.1. Créer et diffuser un guide grand public de la mobilité

- **Run 1 :** Vélo et transport en commun [6]
- **Run 2 :** Covoiturage [6] | Vélo et transport en commun [6]
- **Run 3 :** Covoiturage [6] | Vélo et transport en commun [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Covoiturage (2/3)

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="1738d8a0-e710-4306-9aed-dccf8f928555"><div class="bn-block" data-node-type="blockContainer" data-id="1738d8a0-e710-4306-9aed-dccf8f928555"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]"></p></div></div></div><div class="bn-block-outer" data-node-type="blockOuter" data-id="737ec3f4-9022-449…

#### Fiche 130281 — 1.3. Accompagner les entreprises à réaliser leur plan de mobilités

- **Run 1 :** Réduction des déplacements [6] | Vélo et transport en commun [6]
- **Run 2 :** Réduction des déplacements [6]
- **Run 3 :** Réduction des déplacements [6] | Vélo et transport en commun [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Vélo et transport en commun (2/3)

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="454f05cc-f6a8-42c9-b5e8-afe523b4da04"><div class="bn-block" data-node-type="blockContainer" data-id="454f05cc-f6a8-42c9-b5e8-afe523b4da04"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]"></p></div></div></div><div class="bn-block-outer" data-node-type="blockOuter" data-id="cc84fa66-4286-4db…

#### Fiche 130869 — 6.3. Former les agents pour accompagner les citoyens dans leur mobilité

- **Run 1 :** Vélo et transport en commun [5]
- **Run 2 :** Covoiturage [6] | Vélo et transport en commun [5]
- **Run 3 :** Vélo et transport en commun [5]
- **Prod :** Vélo et transport en commun [6]
- Leviers intermittents : Covoiturage (1/3)

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="96bd6404-258c-4f99-b999-8d417e3f0ba2"><div class="bn-block" data-node-type="blockContainer" data-id="96bd6404-258c-4f99-b999-8d417e3f0ba2"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]"></p></div></div></div><div class="bn-block-outer" data-node-type="blockOuter" data-id="786a2034-973b-49d…

## CC Sundgau (4973)

- Fiches : **37** — stables sur les 3 runs : **30** (81%), instables : **7**
- Paires levier × catégorie distinctes proposées : 46 — 3/3 runs : 33, 2/3 runs : 5, 1/3 runs : 8
- Aucune classification en prod pour cette collectivité
- Réponses JSON invalides rejouées : 0
- Appels : 111 — tokens d'entrée 1 053 330 (dont 1 011 321 en cache, 96%), sortie 6 380 — coût estimé 0.02 $ pour les 3 runs
- Date : 2026-11-02 13:16

### Classée dans certains runs, aucun levier dans d'autres (3)

#### Fiche 53163 — organiser des visites de jardins et prise de parole de jardiniers

- **Run 1 :** (aucun levier)
- **Run 2 :** Prévention des déchets [6]
- **Run 3 :** Prévention des déchets [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Prévention des déchets (2/3)

#### Fiche 61677 — Créer un document d'aide à l'organisation d'une éco-manifestation

- **Run 1 :** (aucun levier)
- **Run 2 :** (aucun levier)
- **Run 3 :** Prévention des déchets [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Prévention des déchets (1/3)

#### Fiche 61681 — Parcours d'animation sur l'alimentation locale et antigaspi

- **Run 1 :** Prévention des déchets [6]
- **Run 2 :** (aucun levier)
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Prévention des déchets (1/3)

### Levier présent dans certains runs seulement (2)

#### Fiche 42051 — Sensibiliser aux enjeux des mobilités alternatives à la voiture individuelle

- **Run 1 :** Covoiturage [6] | Vélo et transport en commun [6]
- **Run 2 :** Covoiturage [6] | Réduction des déplacements [6] | Vélo et transport en commun [6]
- **Run 3 :** Covoiturage [6] | Vélo et transport en commun [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Réduction des déplacements (1/3)

> Sensibiliser aux enjeux des mobilités alternatives à la voiture individuelle/autosolisme, en prenant en compte les publics précaires. \n- Recenser les actions déjà menées en faveur des mobilités alternatives à la voiture individuelle/autosolisme - Valoriser ces actions - Définir les publics ciblés par les démarches de sensibilisation - Initier et/ou poursuivre les actions de sensibilisation, information et communication en identifiant les formats adaptés en fonction des publics ciblés (exemples…

#### Fiche 42053 — Réaliser des achats durables via la commande publique

- **Run 1 :** Electricité renouvelable [5] | Production Industrielle [5] | Prévention des déchets [5]
- **Run 2 :** Efficacité et sobriété logistique [5] | Prévention des déchets [5]
- **Run 3 :** Electricité renouvelable [5] | Production Industrielle [5] | Prévention des déchets [5]
- **Prod :** (aucun levier)
- Leviers intermittents : Efficacité et sobriété logistique (1/3), Electricité renouvelable (2/3), Production Industrielle (2/3)

> Mobiliser la commande publique pour réaliser des achats durables sur l'ensemble des produits, bien et services gérés par la collectivité. Contenu à aborder : favoriser les achats de proximité / réduire les déchets d'emballage via la commande publique / Inclure le critère de consommation énergétique dans les choix de matériels informatiques / stopper les achats non équitables ou non éthiques, intégrer dans les marchés publics des critères d'efficacité énergétique, de réduction de l'impact enviro…

### Levier intermittent et catégories instables (1)

#### Fiche 42050 — Mettre en place une politique de mobilité alternative des agents et des élu.e.s

- **Run 1 :** Covoiturage [6] | Réduction des déplacements [5, 6] | Vélo et transport en commun [5, 6]
- **Run 2 :** Réduction des déplacements [5, 6] | Véhicules électriques [5] | Vélo et transport en commun [5, 6]
- **Run 3 :** Covoiturage [6] | Réduction des déplacements [5, 6] | Vélo et transport en commun [3, 4, 6]
- **Prod :** (aucun levier)
- Leviers intermittents : Covoiturage (2/3), Véhicules électriques (1/3)
- Catégories instables sur : Vélo et transport en commun

> Mettre en place une politique de mobilité alternative des agents et des élu.e.s, visant le changement de comportement, en adoptant une approche diversifiée pour couvrir tant les déplacements professionnels que ceux domicile-travail. Cette politique devrait inclure l'optimisation et le renouvellement de la flotte de véhicules, une gestion optimisée des déplacements, le développement de l'usage du vélo, des campagnes de communication et de sensibilisation, ainsi que la promotion des transports co…

### Mêmes leviers, catégories différentes (1)

#### Fiche 61676 — Créer un "appartement du futur et du réemploi" à visée pédagogique

- **Run 1 :** Prévention des déchets [6]
- **Run 2 :** Prévention des déchets [6]
- **Run 3 :** Prévention des déchets [1, 6]
- **Prod :** (aucun levier)
- Catégories instables sur : Prévention des déchets

## CC du Pays de l'Arbresle (CCPA) (4994)

- Fiches : **96** — stables sur les 3 runs : **87** (91%), instables : **9**
- Paires levier × catégorie distinctes proposées : 99 — 3/3 runs : 85, 2/3 runs : 5, 1/3 runs : 9
- Vote majoritaire = prod : 15/66 fiches classées d'un côté ou de l'autre
- Réponses JSON invalides rejouées : 0
- Appels : 288 — tokens d'entrée 2 754 387 (dont 2 623 968 en cache, 95%), sortie 16 758 — coût estimé 0.05 $ pour les 3 runs
- Date : 2026-11-02 13:35

### Classée dans certains runs, aucun levier dans d'autres (2)

#### Fiche 62330 — Mise en place du Projet Alimentaire territorial PAT

- **Run 1 :** Elevage durable [4]
- **Run 2 :** Production Industrielle [2]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Elevage durable (1/3), Production Industrielle (1/3)

> Déploiement de la stratégie alimentaire de la CCPA: favoriser l'émergence d'une dynamique locale sur la thematique alimentaire en rassemblant l'ensemble des acteurs impliqués dans le domaine. Réaliser une étude d'oportunité de création d'une cuisine centrale s'appuyant sur des produits locaux

#### Fiche 90936 — 1.8 Suivre, évaluer, améliorer le déploiement de la politique Economie Circulaire

- **Run 1 :** (aucun levier)
- **Run 2 :** Prévention des déchets [4]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Prévention des déchets (1/3)

### Levier présent dans certains runs seulement (3)

#### Fiche 62264 — Programme de rencontres pour les entreprises en lien avec leurs démarches RSE

- **Run 1 :** Réduction des déplacements [6] | Sobriété des bâtiments (résidentiel) [6] | Sobriété et isolation des bâtiments (tertiaire) [6]
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [6] | Réduction des déplacements [6] | Sobriété et isolation des bâtiments (tertiaire) [6]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [6] | Réduction des déplacements [6] | Sobriété et isolation des bâtiments (tertiaire) [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (2/3), Sobriété des bâtiments (résidentiel) (1/3)

> <p class="!text-base !text-grey-8 font-[Marianne]">Energie : travail de sensibilisation de l'ALTE et liens avec CCI et CMA (renovation) + AURA entreprises pour aide à la recherche de financement pour les industriels</p><p class="!text-base !text-grey-8 font-[Marianne]">&gt; Sensibiliser les entreprises à la rénovation et aux éco-gestes lors de rencontres des clubs d'entreprises <br>&gt; Rappeler l'intérêt des CEE et de leur valorisation<br>&gt; Informations sur le decret tertiaire</p><p>&nbsp;<…

#### Fiche 62288 — Favoriser l'intermodalité

- **Run 1 :** Vélo et transport en commun [1]
- **Run 2 :** Vélo et transport en commun [1]
- **Run 3 :** Réduction des déplacements [6] | Vélo et transport en commun [1]
- **Prod :** Vélo et transport en commun [1, 2]
- Leviers intermittents : Réduction des déplacements (1/3)

> Renforcer les services et installations existants en facilitant l'intermodalité et particulièrement le rabbatement en modes actifs vers les arrêts de transports en commun. Continuer l'étude des évolutions de part modales pour accéder aux gares et aux arrêts de bus du territoire. Éléments de calendrier : 2025-2027

#### Fiche 62356 — Lancer une reflexion sur une prime pour les rénovations énergétiques des particuliers  performantes en particulier pour l'utilisation de matériaux bio-sourcés

- **Run 1 :** Sobriété des bâtiments (résidentiel) [2]
- **Run 2 :** Sobriété des bâtiments (résidentiel) [2]
- **Run 3 :** Sobriété et isolation des bâtiments (tertiaire) [2]
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété des bâtiments (résidentiel) (2/3), Sobriété et isolation des bâtiments (tertiaire) (1/3)

### Mêmes leviers, catégories différentes (4)

#### Fiche 62307 — Accompagner et suivre les communes pour la définition de Zones d'accélération des ENR et leurs modifications éventuelles

- **Run 1 :** Electricité renouvelable [2]
- **Run 2 :** Electricité renouvelable [6]
- **Run 3 :** Electricité renouvelable [2]
- **Prod :** Electricité renouvelable [2, 6]
- Catégories instables sur : Electricité renouvelable

> Poursuivre l'accompagnement par la CCPA des communes dans la déclaration de leurs ZAER en lien avec la DDT

#### Fiche 62312 — Encadrer l'agri-voltaisme

- **Run 1 :** Electricité renouvelable [2]
- **Run 2 :** Electricité renouvelable [2]
- **Run 3 :** Electricité renouvelable [6]
- **Prod :** (aucun levier)
- Catégories instables sur : Electricité renouvelable

> Poursuivre la formation des élus et techniciens sur le sujet afin d'aboutir sur un positionnement commun pour la CCPA et réfléchir à accompagner des éventuels projets expérimentaux

#### Fiche 62313 — Grappe de projets PV avec le SYDER

- **Run 1 :** Electricité renouvelable [1]
- **Run 2 :** Electricité renouvelable [1, 4]
- **Run 3 :** Electricité renouvelable [1]
- **Prod :** Electricité renouvelable [3]
- Catégories instables sur : Electricité renouvelable

> suivre les installations sur les toitures des bâtiments publics sur les communes de la CCPA suite aux études strucures financées par la CCPA pour les bâtiments de la phase 2

#### Fiche 62317 — Encourager l'autoconsommation collective sur les ZAE

- **Run 1 :** Electricité renouvelable [1, 2]
- **Run 2 :** Electricité renouvelable [1, 2]
- **Run 3 :** Electricité renouvelable [1]
- **Prod :** Electricité renouvelable [3, 6]
- Catégories instables sur : Electricité renouvelable

> Encourager l'autoconsommation collective sur les zones d'activité : poursuivre le financement d'une étude d'oportunité et l' accompagnement des entreprises concernées par le projet expérimentale sur la ZAE des Garelles, étudier la possibilité d'une dérogation afin d'étendre la boucle à d'autres ZAE

## Métropole de Lyon (4999)

- Fiches : **81** — stables sur les 3 runs : **76** (94%), instables : **5**
- Paires levier × catégorie distinctes proposées : 70 — 3/3 runs : 65, 2/3 runs : 1, 1/3 runs : 4
- Vote majoritaire = prod : 7/41 fiches classées d'un côté ou de l'autre
- Réponses JSON invalides rejouées : 0
- Appels : 243 — tokens d'entrée 2 431 941 (dont 2 213 973 en cache, 91%), sortie 13 392 — coût estimé 0.05 $ pour les 3 runs
- Date : 2026-11-02 13:35

### Classée dans certains runs, aucun levier dans d'autres (1)

#### Fiche 90526 — D9 - Conforter la prise en compte de la stratégie territoriale du PCAET dans les chantiers collectifs conduits au titre du Livre Blanc de l’Habitat

- **Run 1 :** Sobriété foncière [4]
- **Run 2 :** (aucun levier)
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété foncière (1/3)

### Levier présent dans certains runs seulement (2)

#### Fiche 65613 — Action n°24 - Structurer une stratégie territoriale de valorisation de la biomasse pour la production d’énergie

- **Run 1 :** Biogaz [2] | Gestion des forêts et produits bois [2] | Réseaux de chaleur décarbonés [2]
- **Run 2 :** Biogaz [2] | Gestion des forêts et produits bois [2] | Réseaux de chaleur décarbonés [2]
- **Run 3 :** Biogaz [2] | Réseaux de chaleur décarbonés [2]
- **Prod :** Biogaz [2] | Réseaux de chaleur décarbonés [2]
- Leviers intermittents : Gestion des forêts et produits bois (2/3)

> <p class="!text-sm !text-primary-9 font-[Marianne]">La biomasse représente un gisement important valorisable en énergies renouvelables. Cette valorisation peut se réaliser soit par combustion, soit par un processus de transformation de la ressource (méthanisation, pyrolyse, etc.) – pour produire du gaz vert issu de la décomposition de la matière organique.</p><p>&nbsp;</p><p class="!text-sm !text-primary-9 font-[Marianne]">Le bois énergie représente 35% de la production locale d’EnR&amp;R, soit…

#### Fiche 65631 — Action n°41 - Moderniser les Usines de Traitement et de Valorisation énergétiques des déchets (UTVE)

- **Run 1 :** Réseaux de chaleur décarbonés [1]
- **Run 2 :** Réseaux de chaleur décarbonés [1]
- **Run 3 :** Réseaux de chaleur décarbonés [1] | Valorisation matière des déchets [1]
- **Prod :** Réseaux de chaleur décarbonés [5] | Valorisation matière des déchets [5]
- Leviers intermittents : Valorisation matière des déchets (1/3)

> <p class="!text-sm !text-primary-9 font-[Marianne]">La Métropole de Lyon dispose de 2 unités de traitement et valorisation énergétique (UTVE) des déchets sur son territoire (Lyon-Nord à Rillieux-la-Pape et Lyon-Sud à Lyon 7ème-Gerland) pour une capacité globale annuelle de 400 000 tonnes de déchets. Ces installations alimentent en chaleur les réseaux de chauffage urbain en développement. </p><p>&nbsp;</p><p class="!text-sm !text-primary-9 font-[Marianne]">Après plus de 35 ans de fonctionnement,…

### Mêmes leviers, catégories différentes (2)

#### Fiche 65596 — Action n°7 - Lutter contre la précarité énergétique

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [3] | Changement chaudières gaz + rénovation (résidentiel) [3] | Sobriété des bâtiments (résidentiel) [3, 6]
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [3] | Changement chaudières gaz + rénovation (résidentiel) [3] | Sobriété des bâtiments (résidentiel) [6]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [3] | Changement chaudières gaz + rénovation (résidentiel) [3] | Sobriété des bâtiments (résidentiel) [6]
- **Prod :** Sobriété des bâtiments (résidentiel) [6]
- Catégories instables sur : Sobriété des bâtiments (résidentiel)

> <p class="!text-sm !text-primary-9 font-[Marianne]">Selon la loi du 12 juillet 2010 relative à «&nbsp;l’engagement national pour l’environnement&nbsp;», une personne est considérée en situation de précarité énergétique lorsqu’elle «&nbsp; éprouve dans son logement des difficultés particulières à disposer de la fourniture d’énergie nécessaire à la satisfaction de ses besoins élémentaires en raison de l’inadaptation de ses ressources ou de ses conditions d’habitat ».</p><p>&nbsp;</p><p class="!te…

#### Fiche 65608 — Action n°19 - Maintenir et développer une activité industrielle en la circularisant

- **Run 1 :** Production Industrielle [6]
- **Run 2 :** Production Industrielle [4, 6]
- **Run 3 :** Production Industrielle [6]
- **Prod :** Production Industrielle [4, 6]
- Catégories instables sur : Production Industrielle

> <p class="!text-sm !text-primary-9 font-[Marianne]">L’industrie est prépondérante et fragile sur le territoire de la Métropole de Lyon :</p><ul><li><p class="!text-sm !text-primary-9 font-[Marianne]">Prépondérante car elle représente près de 80 500 emplois (13,4 % des emplois du territoire), 60 % de la richesse créée, et fournit certains produits nécessaires aux habitants du territoire,</p></li><li><p class="!text-sm !text-primary-9 font-[Marianne]">Fragile car elle est fortement dépendante d’i…

## CC Val de Gray (5005)

- Fiches : **42** — stables sur les 3 runs : **40** (95%), instables : **2**
- Paires levier × catégorie distinctes proposées : 47 — 3/3 runs : 43, 2/3 runs : 0, 1/3 runs : 4
- Aucune classification en prod pour cette collectivité
- Réponses JSON invalides rejouées : 0
- Appels : 126 — tokens d'entrée 1 198 728 (dont 1 147 986 en cache, 96%), sortie 7 619 — coût estimé 0.02 $ pour les 3 runs
- Date : 2026-11-02 13:35

### Levier présent dans certains runs seulement (1)

#### Fiche 12591 — Élaborer une politique de stationnement volontariste

- **Run 1 :** Réduction des déplacements [2]
- **Run 2 :** Covoiturage [2] | Réduction des déplacements [2]
- **Run 3 :** Réduction des déplacements [2]
- **Prod :** (aucun levier)
- Leviers intermittents : Covoiturage (1/3)

> Mettre en place une politique de stationnement dans le centre-ville et/ ou les zones de forte pression (commerces de quartier, etc.) Mettre en place une tarification différenciée si besoin Pour les communes en zones rurale, mettre l'accent sur la sensibilisation et l’information auprès des habitants sur le besoin de gérer l’usage de la voiture et de marquer les places réservées au stationnement et le développement de zones bleues le cas échéant autour des zones de trafic. Faire respecter la rég…

### Levier intermittent et catégories instables (1)

#### Fiche 12610 — Prévenir et lutter contre la précarité énergétique

- **Run 1 :** Sobriété des bâtiments (résidentiel) [4]
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6] | Sobriété des bâtiments (résidentiel) [4]
- **Run 3 :** Sobriété des bâtiments (résidentiel) [4, 6]
- **Prod :** (aucun levier)
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (1/3), Changement chaudières gaz + rénovation (résidentiel) (1/3)
- Catégories instables sur : Sobriété des bâtiments (résidentiel)

> Engager une politique de prévention et de lutte contre la précarité énergétique (liée au logement et à la mobilité) et l'inscrire dans ses documents stratégiques. Réaliser un travail d’inventaire des acteurs de la précarité énergétique et des actions existantes, sur lesquelles construire le dispositif. Utiliser au mieux les moyens humains à disposition pour identifier des situations de précarité énergétique du logement et orienter les familles directement vers les dispositifs existants ou indir…

## CC Brionnais Sud Bourgogne (5033)

- Fiches : **111** — stables sur les 3 runs : **107** (96%), instables : **4**
- Paires levier × catégorie distinctes proposées : 86 — 3/3 runs : 78, 2/3 runs : 4, 1/3 runs : 4
- Vote majoritaire = prod : 22/70 fiches classées d'un côté ou de l'autre
- Réponses JSON invalides rejouées : 0
- Appels : 333 — tokens d'entrée 3 138 813 (dont 3 033 963 en cache, 97%), sortie 18 028 — coût estimé 0.05 $ pour les 3 runs
- Date : 2026-11-02 13:16

### Classée dans certains runs, aucun levier dans d'autres (2)

#### Fiche 57625 — 6.5.2 Organiser des ramassages annuels des déchets sauvages

- **Run 1 :** Valorisation matière des déchets [6]
- **Run 2 :** Prévention des déchets [6]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Prévention des déchets (1/3), Valorisation matière des déchets (1/3)

#### Fiche 57631 — 7.1.2 Créer des vergers conservatoires

- **Run 1 :** (aucun levier)
- **Run 2 :** Gestion des haies [1]
- **Run 3 :** Gestion des haies [1]
- **Prod :** Gestion des forêts et produits bois [1]
- Leviers intermittents : Gestion des haies (2/3)

### Levier présent dans certains runs seulement (1)

#### Fiche 57577 — 3.3.7 Organiser un Salon de l'Habitat

- **Run 1 :** Sobriété des bâtiments (résidentiel) [6]
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (2/3), Changement chaudières gaz + rénovation (résidentiel) (2/3), Sobriété des bâtiments (résidentiel) (1/3)

### Mêmes leviers, catégories différentes (1)

#### Fiche 57621 — 6.3.2 Généraliser des actions permettant de réduire les tonnages produits (réduction des bacs de regroupement, fermeture des bacs d'ordures ménagères, fréquence de collecte…)

- **Run 1 :** Prévention des déchets [1]
- **Run 2 :** Prévention des déchets [3]
- **Run 3 :** Prévention des déchets [3]
- **Prod :** Prévention des déchets [2]
- Catégories instables sur : Prévention des déchets

## Le Havre Seine Métropole (5119)

- Fiches : **88** — stables sur les 3 runs : **73** (83%), instables : **15**
- Paires levier × catégorie distinctes proposées : 112 — 3/3 runs : 86, 2/3 runs : 11, 1/3 runs : 15
- Vote majoritaire = prod : 11/50 fiches classées d'un côté ou de l'autre
- Réponses JSON invalides rejouées : 0
- Appels : 264 — tokens d'entrée 2 570 163 (dont 2 332 416 en cache, 91%), sortie 16 194 — coût estimé 0.06 $ pour les 3 runs
- Date : 2026-11-02 13:35

### Classée dans certains runs, aucun levier dans d'autres (2)

#### Fiche 26729 — 3.3.4 Structurer les réseaux de transport et de distribution d'énergie pour participer à la résilience du territoire

- **Run 1 :** Electricité renouvelable [2]
- **Run 2 :** (aucun levier)
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Electricité renouvelable (1/3)

> L'ambition de la Communauté urbaine de quadrupler la production locale d'ENR&R sur le territoire entre 2019 et 2040 suppose une hausse de la quantité d’énergie injectée dans les réseaux de transport et de distribution de gaz et d’électricité du territoire. L’électrification des usages est également à prendre en compte pour le déploiement futur des réseaux. Cette action vise à anticiper les besoins en matière de transport et de distribution de l'énergie, en tenant compte des évolutions des usage…

#### Fiche 27353 — 4.4.1 Prévenir les risques et développer la culture du risque

- **Run 1 :** (aucun levier)
- **Run 2 :** (aucun levier)
- **Run 3 :** Sobriété foncière [2]
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété foncière (1/3)

> La Communauté urbaine déploie depuis de nombreuses années une politique sur un territoire « multirisques ». Elle s’appuie pour cela sur différents dispositifs, notamment la stratégie locale de gestion du risque inondation - SLGRI), 4 plans de prévention des risques naturels (inondation-érosion, submersion marine et falaises), 2 plans de prévention des risques technologiques (pour 17 SEVESO seuils hauts) et 2 plans particuliers d’intervention (PPI). Aujourd’hui, un constat récurrent montre le dé…

### Levier présent dans certains runs seulement (3)

#### Fiche 26108 — 2.1.4 Mettre en place une Zone à faibles émissions mobilité (ZFE-m)

- **Run 1 :** Efficacité et carburants décarbonés des véhicules privés [2] | Vélo et transport en commun [2]
- **Run 2 :** Véhicules électriques [2]
- **Run 3 :** Vélo et transport en commun [2]
- **Prod :** Véhicules électriques [2] | Vélo et transport en commun [2]
- Leviers intermittents : Efficacité et carburants décarbonés des véhicules privés (1/3), Véhicules électriques (1/3), Vélo et transport en commun (2/3)

> La ZFE-m est un secteur défini dans lequel la circulation et le stationnement de véhicules sont réglementés en fonction de leurs émissions de polluants atmosphériques (certificat de qualité de l’air appelé aussi vignette CRIT’AIR). Ainsi, la ZFE-m a pour objectif de réduire les concentrations de particules fines et de NOx dans les zones urbaines les plus impactées, en limitant la circulation des véhicules les plus polluants. La loi Climat et Résilience impose aux collectivités de plus de 150 00…

#### Fiche 26125 — 2.2.4 Accompagner l'électrification des quais pour contribuer à la réduction de l'impact carbone du transport maritime

- **Run 1 :** Efficacité et carburants décarbonés des véhicules privés [1]
- **Run 2 :** Electricité renouvelable [1]
- **Run 3 :** Electricité renouvelable [1]
- **Prod :** (aucun levier)
- Leviers intermittents : Efficacité et carburants décarbonés des véhicules privés (1/3), Electricité renouvelable (2/3)

> L’électrification des quais croisière, qui permet aux navires de se raccorder à l’électricité lors de leurs escales, est un enjeu majeur de réduction des émissions de gaz à effet de serre et plus largement de polluants atmosphériques. Préalablement au lancement des travaux, le raccordement au réseau de distribution public d’électricité réalisé par Enedis a nécessité la création de 3 km de réseau souterrain composé de 3 câbles 20 000 volts et l’ajout d’un transformateur HTB/HTA 40MVA au poste so…

#### Fiche 27279 — 4.2.1 Améliorer la gestion globale de la protection de la ressource en eau

- **Run 1 :** Changements de pratiques de fertilisation azotée [2, 3] | Pratiques stockantes [2, 3] | Production Industrielle [2]
- **Run 2 :** Changements de pratiques de fertilisation azotée [2, 3] | Pratiques stockantes [2, 3] | Réseaux de chaleur décarbonés [2]
- **Run 3 :** Changements de pratiques de fertilisation azotée [2, 3] | Pratiques stockantes [2, 3] | Production Industrielle [2]
- **Prod :** (aucun levier)
- Leviers intermittents : Production Industrielle (2/3), Réseaux de chaleur décarbonés (1/3)

> L'action vise à assurer le bon état qualitatif et quantitatif des ressources en eau pour l’approvisionnement en eau potable (et en eau industrielle), en améliorant la connaissance et le suivi. Elle se compose de 5 sous-actions, dont 3 fondamentales déjà en cours, qui seront complétées par les actions 4 et 5. Elles se dérouleront en parallèle. 1. Mise en œuvre et révision des Déclarations d’Utilité Publique liées aux captages d’eau a. Mise en œuvre des DUP b. Protection des périmètres de captage…

### Levier intermittent et catégories instables (1)

#### Fiche 27318 — 4.3.1 Gérer durablement les réservoirs de biodiversité

- **Run 1 :** Gestion des haies [1, 6] | Réseaux de chaleur décarbonés [1] | Sobriété foncière [4]
- **Run 2 :** Gestion des haies [1, 6] | Réseaux de chaleur décarbonés [1] | Sobriété foncière [4]
- **Run 3 :** Gestion des haies [6] | Sobriété foncière [2]
- **Prod :** Gestion des forêts et produits bois [3, 4] | Gestion des haies [3, 4] | Sobriété foncière [2, 4]
- Leviers intermittents : Réseaux de chaleur décarbonés (2/3)
- Catégories instables sur : Gestion des haies, Sobriété foncière

> Cette action vise à renforcer la préservation et la séquestration du carbone par les puits naturels sur le territoire. Cela passe par les mesures suivantes : 1. Développer la plantation de haies sur le territoire a. Programme d’action « Opération Normandie Haie » b. Agir avec les partenaires sur la filière aval notamment en créant/accompagnant la filière de valorisation de l’entretien de la haie via le bois énergie. 2. Déployer Carbolocal, startup de territoire pour accélérer la transition écol…

### Mêmes leviers, catégories différentes (9)

#### Fiche 26067 — 1.2.2 Accompagner la rénovation énergétique des locaux tertiaires privés

- **Run 1 :** Changement de chaudière à fioul (tertiaire) [6] | Changement de chaudière à gaz (tertiaire) [6] | Sobriété et isolation des bâtiments (tertiaire) [2]
- **Run 2 :** Changement de chaudière à fioul (tertiaire) [6] | Changement de chaudière à gaz (tertiaire) [6] | Sobriété et isolation des bâtiments (tertiaire) [6]
- **Run 3 :** Changement de chaudière à fioul (tertiaire) [6] | Changement de chaudière à gaz (tertiaire) [6] | Sobriété et isolation des bâtiments (tertiaire) [6]
- **Prod :** Sobriété et isolation des bâtiments (tertiaire) [6]
- Catégories instables sur : Sobriété et isolation des bâtiments (tertiaire)

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="4b669fc0-19da-4da0-9c4c-2a5abcd0e244"><div class="bn-block" data-node-type="blockContainer" data-id="4b669fc0-19da-4da0-9c4c-2a5abcd0e244"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]">L'action vise à accélérer la rénovation énergétique des locaux tertiaires privés par un accompagnement d…

#### Fiche 26106 — 2.1.2 Promouvoir et faciliter l'usage du vélo et des modes actifs

- **Run 1 :** Vélo et transport en commun [1, 3]
- **Run 2 :** Vélo et transport en commun [1]
- **Run 3 :** Vélo et transport en commun [1, 3]
- **Prod :** Vélo et transport en commun [1]
- Catégories instables sur : Vélo et transport en commun

> L'action vise à développer la part des transports doux, part relativement faible dans l'enquête ménages déplacements menée en 2018 (2%). L'action se décompose en plusieurs sous-actions : - développer les aménagements cyclables du territoire - développer l'offre de trottinettes et de vélos à assistance en électrique en libre service - développer la location longue durée de vélos et vélos à assistance électrique

#### Fiche 26115 — 2.2.2 Accélérer le déploiement des infrastructures de recharge pour véhicules électriques

- **Run 1 :** Véhicules électriques [1]
- **Run 2 :** Véhicules électriques [1]
- **Run 3 :** Véhicules électriques [1, 6]
- **Prod :** Véhicules électriques [1, 3]
- Catégories instables sur : Véhicules électriques

> L'action vise à mettre en œuvre le schéma directeur des infrastructures de recharge pour véhicules électriques sur le territoire de la Communauté urbaine : - déploiement de bornes de recharge sur la voie publique - incitation des copropriétés à s'équiper d'infrastructures de recharge.

#### Fiche 26121 — 2.2.3 Encourager une logistique urbaine durable

- **Run 1 :** Efficacité et sobriété logistique [6] | Fret décarboné et multimodalité [6]
- **Run 2 :** Efficacité et sobriété logistique [4, 6] | Fret décarboné et multimodalité [6]
- **Run 3 :** Efficacité et sobriété logistique [6] | Fret décarboné et multimodalité [6]
- **Prod :** Efficacité et sobriété logistique [2, 6] | Fret décarboné et multimodalité [2, 6]
- Catégories instables sur : Efficacité et sobriété logistique

> La Communauté urbaine a lancé en 2023 l’étude Interlud (Innovations Territoriales et Logistique Urbaine Durable) dont les objectifs sont les suivants : • informer, sensibiliser et accompagner les collectivités et les opérateurs économiques à l’échelle territoriale sur les enjeux de la logistique urbaine ; • structurer les filières économiques et leurs représentations ; • favoriser la participation des acteurs privés dans le cadre des chartes logistiques urbaines et les faire dialoguer avec les …

#### Fiche 26704 — 3.2.1 Développer la production de biogaz à partir des sources industrielles et agricoles

- **Run 1 :** Biogaz [2, 6]
- **Run 2 :** Biogaz [6]
- **Run 3 :** Biogaz [6]
- **Prod :** Biogaz [3, 4, 6]
- Catégories instables sur : Biogaz

> La loi de Transition Énergétique pour la Croissance Verte (LTECV) fixe un objectif de 10 % de gaz renouvelable dans les réseaux d’ici 2030, 30% d’ici 2050. La Communauté urbaine s'est fixé l'objectif de production de 204 GWh/an de biogaz sur son territoire d'ici 2040. L'action vise à développer la production de biogaz sur le territoire et à développer les circuits courts entre industriels. Pour cela, elle mène une action de sensibilisation sur le thème de la méthanisation, identifie les ressour…

#### Fiche 26727 — 3.3.2 Accélérer le développement de l'énergie photovoltaïque

- **Run 1 :** Electricité renouvelable [1, 2, 4, 6]
- **Run 2 :** Electricité renouvelable [1, 2, 3, 4, 6]
- **Run 3 :** Electricité renouvelable [1, 2, 4, 6]
- **Prod :** Electricité renouvelable [1, 2, 4, 6]
- Catégories instables sur : Electricité renouvelable

> Cette action vise à traduire de manière concrète l'objectif fixé dans le PCAET de production de 808 GWh via le photovoltaïque en 2040. Cela passe par : - la mise en oeuvre d'EUCF - le développement de projets avec la SEM ASER - l'accompagnement des communes dans leurs projets photovoltaïques - l'accompagnement des acteurs privés et publics - le développement d'un cadastre solaire - la numérisation des données et la mise en place d'un outil de comptabilisation des projets développés et de la pui…

#### Fiche 27356 — 5.2.1 Accompagner l’essor d’une démarche d’écologie industrielle et territoriale  (EIT) vers la transformation bas-carbone de l'industrie

- **Run 1 :** Production Industrielle [4, 6] | Valorisation matière des déchets [6]
- **Run 2 :** Production Industrielle [6] | Valorisation matière des déchets [4]
- **Run 3 :** Production Industrielle [6] | Valorisation matière des déchets [4, 6]
- **Prod :** Production Industrielle [4, 6]
- Catégories instables sur : Production Industrielle, Valorisation matière des déchets

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="39deab80-929b-4e62-b362-e22588c0268b"><div class="bn-block" data-node-type="blockContainer" data-id="39deab80-929b-4e62-b362-e22588c0268b"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]">L’économie circulaire nous invite à interroger la notion de besoin, à transformer nos déchets en ressour…

#### Fiche 27360 — 5.3.2 Renforcer la collecte des objets et favoriser les pratiques de réparation, de réemploi et de lutte contre le gaspillage alimentaire

- **Run 1 :** Prévention des déchets [3, 6]
- **Run 2 :** Prévention des déchets [1, 3, 6]
- **Run 3 :** Prévention des déchets [3, 6]
- **Prod :** Prévention des déchets [3, 4, 6]
- Catégories instables sur : Prévention des déchets

> Chaque habitant du territoire produit en moyenne près de 600 kilos de déchets par an. Malgré le nombre croissant de filières de recyclage, ne pas produire de déchets reste de loin la meilleure des solutions pour éviter tout gaspillage. La loi anti-gaspillage pour une économie circulaire (Agec) dont l’orientation vise à favoriser le réemploi de matériaux et objets. Elle prévoit notamment de « sortir du plastique jetable, mieux informer les consommateurs, lutter contre le gaspillage et pour le ré…

#### Fiche 37499 — Rénovation énergétique du bâtiment Curie et intégration d'ENR en toiture

- **Run 1 :** Electricité renouvelable [5] | Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 2 :** Electricité renouvelable [1] | Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 3 :** Electricité renouvelable [5] | Sobriété et isolation des bâtiments (tertiaire) [5]
- **Prod :** Electricité renouvelable [5] | Sobriété et isolation des bâtiments (tertiaire) [5]
- Catégories instables sur : Electricité renouvelable

> Ce bâtiment à usage de bureaux pour la Direction du Cycle de l'Eau et le Service Marché a été construit en 2012. Il est énergétiquement performant mais les usagers ressente un inconfort thermique contant (trop froid en hiver, trop chaud en été). Un dispositif hybride de production d'électricité renouvelable en autoconsommation ou ACC (couplé panneaux photovoltaïques et petites éoliennes à axe horizontal) est envisagé en toiture. Instance de gouvernance : Présentation au Directeur DEMB.

## CC du Pays des Achards (5300)

- Fiches : **103** — stables sur les 3 runs : **95** (92%), instables : **8**
- Paires levier × catégorie distinctes proposées : 89 — 3/3 runs : 75, 2/3 runs : 7, 1/3 runs : 7
- Vote majoritaire = prod : 12/50 fiches classées d'un côté ou de l'autre
- Réponses JSON invalides rejouées : 0
- Appels : 309 — tokens d'entrée 2 976 759 (dont 2 815 299 en cache, 95%), sortie 16 002 — coût estimé 0.05 $ pour les 3 runs
- Date : 2026-11-02 13:35

### Levier présent dans certains runs seulement (4)

#### Fiche 23026 — 1.3 Encourager la sobriété énergétique sur le bâti

- **Run 1 :** Changement de chaudière à fioul (tertiaire) [6] | Changement de chaudière à gaz (tertiaire) [6] | Sobriété des bâtiments (résidentiel) [6]
- **Run 2 :** Changement de chaudière à fioul (tertiaire) [6] | Réseaux de chaleur décarbonés [6] | Sobriété des bâtiments (résidentiel) [6]
- **Run 3 :** Changement de chaudière à fioul (tertiaire) [6] | Réseaux de chaleur décarbonés [6] | Sobriété des bâtiments (résidentiel) [6]
- **Prod :** Changement de chaudière à fioul (tertiaire) [5] | Sobriété des bâtiments (résidentiel) [6]
- Leviers intermittents : Changement de chaudière à gaz (tertiaire) (1/3), Réseaux de chaleur décarbonés (2/3)

> Les consommations d’énergie pour le chauffage des bâtiments à usage d’habitation et les bâtiments publics représentent une part prépondérante des consommations du territoire. La CC Pays des Achards souhaite développer un volet spécifique sur la performance des systèmes de chauffage. Pour les logements, cela passe par une incitation au remplacement des équipements de chauffage biomasse vétustes (foyers ouverts) par des installations plus efficaces en termes de consommation de bois et de combusti…

#### Fiche 23035 — 4.3 Accompagner les entreprises et les acteurs du territoire vers une gestion optimisée de leurs déplacements

- **Run 1 :** Covoiturage [4] | Réduction des déplacements [6]
- **Run 2 :** Réduction des déplacements [6]
- **Run 3 :** Covoiturage [4] | Réduction des déplacements [6]
- **Prod :** Covoiturage [4, 6] | Réduction des déplacements [1, 4, 6]
- Leviers intermittents : Covoiturage (2/3)

> Afin de renforcer l’offre d’accompagnement aux entreprises en matière de mobilité, il est proposé de soutenir les démarches collectives entre entreprises en faveur de la mutualisation des déplacements, et de les accompagner dans la mise en place de Plans de Déplacement Inter-Entreprises (PDIE). Encourager la mise en place d’espaces de coworking et du télétravail permet également de réduire les déplacements et l’empreinte carbone des entreprises et de leurs salariés. DETAILS DE L'ACTION Développ…

#### Fiche 23040 — 5.5 Adapter l’agriculture aux changements climatiques

- **Run 1 :** Biogaz [6] | Changements de pratiques de fertilisation azotée [6] | Pratiques stockantes [6]
- **Run 2 :** Changements de pratiques de fertilisation azotée [6] | Elevage durable [6] | Pratiques stockantes [6]
- **Run 3 :** Changements de pratiques de fertilisation azotée [6] | Elevage durable [6] | Pratiques stockantes [6]
- **Prod :** Bâtiments & Machines agricoles [6] | Pratiques stockantes [6]
- Leviers intermittents : Biogaz (1/3), Elevage durable (2/3)

> L’identification des opportunités de développement économique du territoire conciliant réalités économiques et anticipation des impacts du changement climatique est indispensable pour le territoire de la CCPA, notamment pour le secteur agricole. La volonté de la CCPA est de faire évoluer les pratiques pour favoriser une agriculture locale et durable, tant d’un point de vue de la production que de la consommation. DETAILS DE L'ACTION Assurer le maintien d’une agriculture économe en eau : > Etabl…

#### Fiche 85996 — FA 14 : Construire un Plan d'Actions commun en faveur des Mobilités Solidaires

- **Run 1 :** Vélo et transport en commun [2]
- **Run 2 :** Vélo et transport en commun [2]
- **Run 3 :** Covoiturage [2] | Vélo et transport en commun [2]
- **Prod :** (aucun levier)
- Leviers intermittents : Covoiturage (1/3)

### Levier intermittent et catégories instables (1)

#### Fiche 23037 — 5.2 Maintenir et développer la séquestration carbone

- **Run 1 :** Gestion des forêts et produits bois [4] | Gestion des haies [6] | Sobriété foncière [6]
- **Run 2 :** Gestion des forêts et produits bois [4] | Gestion des haies [6]
- **Run 3 :** Gestion des forêts et produits bois [6] | Gestion des haies [6]
- **Prod :** Gestion des forêts et produits bois [3, 4] | Gestion des haies [4, 6] | Gestion des prairies [4, 6]
- Leviers intermittents : Sobriété foncière (1/3)
- Catégories instables sur : Gestion des forêts et produits bois

> En France, entre 3 à 4 milliards de tonnes de carbone sont stockés tout juste sous nos pieds. La capacité de stockage du sol dépend de l’affectation qui lui a été donnée. Plus le sol se retrouve « artificialisé », plus sa capacité de stockage est réduite. La CCPA possède 95% de surface non artificialisée/imperméabilisée. De manière un peu contre-intuitive, pour que le bocage se maintienne, il faut le « couper » régulièrement : une haie qui n'est pas entretenue dépérit à terme. En dehors des enj…

### Mêmes leviers, catégories différentes (3)

#### Fiche 23029 — 3.1 Maîtriser les consommations d’énergie sur le patrimoine et les transports

- **Run 1 :** Changement de chaudière à fioul (tertiaire) [5] | Changement de chaudière à gaz (tertiaire) [5] | Sobriété et isolation des bâtiments (tertiaire) [4, 5]
- **Run 2 :** Changement de chaudière à fioul (tertiaire) [5] | Changement de chaudière à gaz (tertiaire) [5] | Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 3 :** Changement de chaudière à fioul (tertiaire) [5] | Changement de chaudière à gaz (tertiaire) [5] | Sobriété et isolation des bâtiments (tertiaire) [4, 5]
- **Prod :** Changement de chaudière à fioul (tertiaire) [5] | Changement de chaudière à gaz (tertiaire) [5] | Efficacité et carburants décarbonés des véhicules privés [5] | Sobriété et isolation des bâtiments (tertiaire) [5]
- Catégories instables sur : Sobriété et isolation des bâtiments (tertiaire)

> Selon le Programme des Nations Unies pour l’Environnement (PNUE), 15% des émissions de GES sont directement issues des décisions prises par les collectivités territoriales, concernant leur patrimoine (bâtiment, éclairage public, flotte de véhicules) et leurs compétences (transports, déchets, etc). La collectivité a donc un rôle d’exemplarité. Pour les petites et moyennes communes, la dépense consacrée à l’énergie représente en moyenne 6% du budget de fonctionnement. La Communauté de communes so…

#### Fiche 85999 — FA 16 : Renforcer l'usage du vélo vers les pôles générateurs de déplacements

- **Run 1 :** Vélo et transport en commun [1]
- **Run 2 :** Vélo et transport en commun [6]
- **Run 3 :** Vélo et transport en commun [6]
- **Prod :** Vélo et transport en commun [1, 6]
- Catégories instables sur : Vélo et transport en commun

#### Fiche 87965 — 3.1.3. Impulser une réflexion autour de la coordination entre les EHPAD et les SSIAD du territoire pour organiser ponctuellement le transport de seniors à domicile vers les EHPAD

- **Run 1 :** Vélo et transport en commun [4]
- **Run 2 :** Vélo et transport en commun [2]
- **Run 3 :** Vélo et transport en commun [2]
- **Prod :** (aucun levier)
- Catégories instables sur : Vélo et transport en commun

> <p class="!text-base !text-grey-8 font-[Marianne]">Amorcer une réflexion autour de la coordination entre les SSIAD et les trois EHPAD du territoire afin d’organiser ponctuellement le transport de seniors vivant à domicile, à mobilité réduite pour leur permettre de participer aux activités proposées dans les EHPAD.</p>

## Paris Est Marne & Bois (5390)

- Fiches : **141** — stables sur les 3 runs : **133** (94%), instables : **8**
- Paires levier × catégorie distinctes proposées : 82 — 3/3 runs : 69, 2/3 runs : 7, 1/3 runs : 6
- Vote majoritaire = prod : 19/68 fiches classées d'un côté ou de l'autre
- Réponses JSON invalides rejouées : 0
- Appels : 423 — tokens d'entrée 4 011 609 (dont 3 853 953 en cache, 96%), sortie 20 721 — coût estimé 0.06 $ pour les 3 runs
- Date : 2026-11-02 13:16

### Classée dans certains runs, aucun levier dans d'autres (1)

#### Fiche 84970 — Fixer des objectifs Energie - Climat dans le PLUi

- **Run 1 :** Sobriété foncière [2]
- **Run 2 :** Sobriété foncière [2]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété foncière (2/3)

### Levier présent dans certains runs seulement (1)

#### Fiche 85370 — Mettre en œuvre le plan sur 5 années

- **Run 1 :** Covoiturage [2] | Réduction des déplacements [2] | Vélo et transport en commun [2]
- **Run 2 :** Covoiturage [2] | Vélo et transport en commun [2]
- **Run 3 :** Covoiturage [2] | Réduction des déplacements [2] | Vélo et transport en commun [2]
- **Prod :** Bus et cars décarbonés [2] | Covoiturage [2] | Réduction des déplacements [2] | Vélo et transport en commun [2]
- Leviers intermittents : Réduction des déplacements (2/3)

### Mêmes leviers, catégories différentes (6)

#### Fiche 85374 — Adhérer à l'Agence Locale de l'Energie et du Climat - MVE pour permettre aux habitants d'accéder au service public de la performance énergétique de l'habitat

- **Run 1 :** Sobriété des bâtiments (résidentiel) [4]
- **Run 2 :** Sobriété des bâtiments (résidentiel) [4]
- **Run 3 :** Sobriété des bâtiments (résidentiel) [6]
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [4, 6] | Changement chaudières gaz + rénovation (résidentiel) [4, 6] | Sobriété des bâtiments (résidentiel) [4, 6]
- Catégories instables sur : Sobriété des bâtiments (résidentiel)

#### Fiche 85377 — Impliquer davantage les professionnels du cadre bâti dans la rénovation énergétique

- **Run 1 :** Sobriété et isolation des bâtiments (tertiaire) [4]
- **Run 2 :** Sobriété et isolation des bâtiments (tertiaire) [6]
- **Run 3 :** Sobriété et isolation des bâtiments (tertiaire) [4]
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6] | Sobriété des bâtiments (résidentiel) [6]
- Catégories instables sur : Sobriété et isolation des bâtiments (tertiaire)

#### Fiche 85379 — Renforcer l'efficacité énergétique des bâtiments dans le parc social

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [1] | Changement chaudières gaz + rénovation (résidentiel) [1] | Sobriété des bâtiments (résidentiel) [6]
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [1] | Changement chaudières gaz + rénovation (résidentiel) [1] | Sobriété des bâtiments (résidentiel) [6]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [1] | Changement chaudières gaz + rénovation (résidentiel) [1] | Sobriété des bâtiments (résidentiel) [1]
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [3]
- Catégories instables sur : Sobriété des bâtiments (résidentiel)

#### Fiche 85671 — Concevoir une plate-forme territoriale pour repérer et accompagner les ménages en situation de précarité énergétique

- **Run 1 :** Sobriété des bâtiments (résidentiel) [1, 6]
- **Run 2 :** Sobriété des bâtiments (résidentiel) [1]
- **Run 3 :** Sobriété des bâtiments (résidentiel) [1]
- **Prod :** (aucun levier)
- Catégories instables sur : Sobriété des bâtiments (résidentiel)

#### Fiche 85692 — Optimiser les parcours de collecte

- **Run 1 :** Efficacité et sobriété logistique [2]
- **Run 2 :** Efficacité et sobriété logistique [1]
- **Run 3 :** Efficacité et sobriété logistique [1]
- **Prod :** Efficacité et sobriété logistique [4]
- Catégories instables sur : Efficacité et sobriété logistique

#### Fiche 85722 — Dispositif territoire roule propre

- **Run 1 :** Efficacité et carburants décarbonés des véhicules privés [5]
- **Run 2 :** Efficacité et carburants décarbonés des véhicules privés [5]
- **Run 3 :** Efficacité et carburants décarbonés des véhicules privés [6]
- **Prod :** (aucun levier)
- Catégories instables sur : Efficacité et carburants décarbonés des véhicules privés

## SM du SCoT Sambre Avesnois (6030)

- Fiches : **73** — stables sur les 3 runs : **62** (85%), instables : **11**
- Paires levier × catégorie distinctes proposées : 89 — 3/3 runs : 70, 2/3 runs : 8, 1/3 runs : 11
- Vote majoritaire = prod : 11/53 fiches classées d'un côté ou de l'autre
- Réponses JSON invalides rejouées : 0
- Appels : 219 — tokens d'entrée 2 123 598 (dont 1 995 309 en cache, 94%), sortie 13 672 — coût estimé 0.04 $ pour les 3 runs
- Date : 2026-11-02 13:35

### Classée dans certains runs, aucun levier dans d'autres (3)

#### Fiche 126676 — 3.1.2. Accompagner la mise en œuvre de plans de mobilité intercommunaux

- **Run 1 :** (aucun levier)
- **Run 2 :** Covoiturage [2] | Vélo et transport en commun [2]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Covoiturage (1/3), Vélo et transport en commun (1/3)

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="efe16c93-87da-41ad-bd77-d3ed165004f8"><div class="bn-block" data-node-type="blockContainer" data-id="efe16c93-87da-41ad-bd77-d3ed165004f8"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]">Le Plan de Déplacements Urbains (PDU) est un outil de planification qui a été créé par la Loi d’Orientat…

#### Fiche 126711 — 6.4.2. MR2 - Qualité de l’air et chauffage au bois

- **Run 1 :** Sobriété des bâtiments (résidentiel) [6]
- **Run 2 :** Sobriété des bâtiments (résidentiel) [6]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété des bâtiments (résidentiel) (2/3)

> Le territoire de la Sambre Avesnois porte plusieurs objectifs de développement de la filière bois énergie. Cette filière présente de très nombreux avantages : Production d’énergie renouvelable Production d’énergie locale / autonomie énergétique Source de revenus non délocalisable, économie circulaire Mais comme toute combustion, le chauffage au bois est à l'origine d'émissions : de polluants de l'air, c'est-à-dire de substances contribuant à dégrader directement la qualité de l'air. On parle de…

#### Fiche 126715 — 7.2.1. Encourager et soutenir les changements de pratiques agricoles

- **Run 1 :** Changements de pratiques de fertilisation azotée [6] | Pratiques stockantes [6]
- **Run 2 :** Changements de pratiques de fertilisation azotée [6] | Pratiques stockantes [6]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Changements de pratiques de fertilisation azotée (2/3), Pratiques stockantes (2/3)

> L’agriculture, comme de nombreux secteurs d’activité, doit évoluer afin de réduire son impact environnemental et d’adapter au changement climatique. Les territoires, en proposant des formations, des moments d’échange et de sensibilisations, peuvent accompagner le changement des pratiques agricoles vers des méthodes plus respectueuses de l’environnement et apte à supporter les changements climatiques à venir.

### Levier présent dans certains runs seulement (6)

#### Fiche 126656 — 1.1.1. Mettre en œuvre le Programme Local de l'Habitat 2025-2030

- **Run 1 :** Sobriété foncière [2]
- **Run 2 :** Sobriété foncière [2]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [2] | Changement chaudières gaz + rénovation (résidentiel) [2]
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [2] | Changement chaudières gaz + rénovation (résidentiel) [2]
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (1/3), Changement chaudières gaz + rénovation (résidentiel) (1/3), Sobriété foncière (2/3)

> Elaboré pour 6 ans, le PLH est un document réglementaire définissant la stratégie et les actions à mener dans le cadre de la politique de l’habitat. Le PLH porte des objectifs ambitieux sur les thématiques de rénovation et de lutte contre la précarité énergétique.

#### Fiche 126657 — 1.1.2. Mise en œuvre du POA Habitat (PLUi-H), incluant la lutte contre la précarité énergétique, l'adaptation de l'offre, … (2023-2029)

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [2, 3] | Changement chaudières gaz + rénovation (résidentiel) [2, 3]
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [2, 3] | Changement chaudières gaz + rénovation (résidentiel) [2, 3]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [2, 3] | Changement chaudières gaz + rénovation (résidentiel) [2, 3] | Sobriété foncière [2]
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [2] | Changement chaudières gaz + rénovation (résidentiel) [2]
- Leviers intermittents : Sobriété foncière (1/3)

> La CC Cœur de l'Avesnois a souhaité intégrer des dispositions habitat au sein de son PLUi tenant lieu de Programme Local pour l’Habitat (PLH) à travers la rédaction d’un Programme d’Orientations et d’Actions Habitat. Elaboré pour 6 ans, le PLH est un document réglementaire définissant la stratégie et les actions à mener dans le cadre de la politique de l’habitat. Le POA Habitat de la CC Cœur de l'Avesnois porte des objectifs ambitieux sur les questions de lutte contre la vacance, contre l’insal…

#### Fiche 126671 — 2.3.2. Développer des bâtiments publics « producteurs » et « sobres » en énergies

- **Run 1 :** Electricité renouvelable [1] | Sobriété et isolation des bâtiments (tertiaire) [2]
- **Run 2 :** Electricité renouvelable [1]
- **Run 3 :** Electricité renouvelable [1] | Sobriété et isolation des bâtiments (tertiaire) [2]
- **Prod :** Electricité renouvelable [5]
- Leviers intermittents : Sobriété et isolation des bâtiments (tertiaire) (2/3)

> Les bâtiments publics représentent un potentiel important de toiture non exploité pour la production d'énergie ou la récupération des eaux pluviales. Une réflexion est à porter sur le développement des énergies renouvelables au sein des bâtiments publics existants et futurs et les possibilités de stockage.

#### Fiche 126677 — 3.1.3. Inciter le monde économique à déployer des actions de mobilité décarbonée

- **Run 1 :** Réduction des déplacements [2, 6]
- **Run 2 :** Covoiturage [6] | Vélo et transport en commun [6]
- **Run 3 :** Réduction des déplacements [6]
- **Prod :** Réduction des déplacements [4, 5, 6]
- Leviers intermittents : Covoiturage (1/3), Réduction des déplacements (2/3), Vélo et transport en commun (1/3)

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="75f0f0bb-2464-4b5d-b34e-9d8923721dd3"><div class="bn-block" data-node-type="blockContainer" data-id="75f0f0bb-2464-4b5d-b34e-9d8923721dd3"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]">La voiture est prépondérante dans les trajets domicile - travail sur le territoire. La mise en place de …

#### Fiche 126694 — 4.4.3. Valoriser énergétiquement les déchets produits sur le territoire

- **Run 1 :** Biogaz [1]
- **Run 2 :** Biogaz [1] | Valorisation matière des déchets [1]
- **Run 3 :** Biogaz [1]
- **Prod :** Biogaz [1] | Valorisation matière des déchets [1]
- Leviers intermittents : Valorisation matière des déchets (1/3)

> Les déchets produits sur le territoire sont une ressource qu'il est possible d'exploiter. Les déchets agro-alimentaires en particulier, peuvent être utilisés en compost, ou encore dans une unité de méthanisation, permettant de produire du gaz renouvelable localement.

#### Fiche 126717 — 7.2.3. Accompagner la diversification des activités

- **Run 1 :** Biogaz [6] | Electricité renouvelable [6]
- **Run 2 :** Biogaz [6] | Electricité renouvelable [6] | Gestion des haies [6]
- **Run 3 :** Biogaz [6] | Electricité renouvelable [6]
- **Prod :** Biogaz [6] | Electricité renouvelable [6]
- Leviers intermittents : Gestion des haies (1/3)

> Les agriculteurs peuvent mettre en place des activités annexes de productions et de valorisations énergétiques sur leur terrain. De la méthanisation à la production de bois déchiqueté de bocage pour les chaufferies, ces activités participent à la valorisation des ressources du territoire et apportent aux agriculteurs un complément de revenu non négligeable. Porter une attention particulière au développement de toutes les énergies renouvelables et en particulier à l’éolien et à l’agrivoltaïsme, …

### Mêmes leviers, catégories différentes (2)

#### Fiche 126658 — 1.2.1. Améliorer l’efficacité énergétique et thermique des habitations

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [1, 6] | Changement chaudières gaz + rénovation (résidentiel) [1, 6]
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [1, 6] | Changement chaudières gaz + rénovation (résidentiel) [1, 6]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [1] | Changement chaudières gaz + rénovation (résidentiel) [1]
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [6]
- Catégories instables sur : Changement chaudières fioul + rénovation (résidentiel), Changement chaudières gaz + rénovation (résidentiel)

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="4568bd70-7978-4e5b-b4bb-ff8a3a2324c8"><div class="bn-block" data-node-type="blockContainer" data-id="4568bd70-7978-4e5b-b4bb-ff8a3a2324c8"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]">Un nombre important d'habitations sont considérées comme des passoires thermiques, avec une étiquettes é…

#### Fiche 126709 — 6.3.4. Mettre en œuvre des projets de méthanisation

- **Run 1 :** Biogaz [1]
- **Run 2 :** Biogaz [1]
- **Run 3 :** Biogaz [1, 6]
- **Prod :** Biogaz [1] | Valorisation matière des déchets [1]
- Catégories instables sur : Biogaz

> La Sambre-Avesnois compte 9 unités de méthanisation, dont une seule unité réalisant de l'injection de gaz dans le réseau. Le potentiel sur le territoire est important du fait d'une activité agricole et agroalimentaire importante. L'intéret de la méthanisation est multiple : valorisation des déchets, limitations de la pollution agricole, production de digestat pouvant se substituer aux engrais minéraux, production de biogaz renforçant l'indépendance énergétique de la Sambre-Avesnois, apporter un…
