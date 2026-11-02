# Stabilité Mistral Large 4 — classification volet GES

Modèle `mistral-large-4`, `reasoning_effort=low`, température par défaut de l'API. Même prompt (`pages/26_run_impact.py`), mêmes lots de 25 fiches, 3 runs indépendants. Lecture seule sur la prod.

Mis à jour le 2026-10-30 16:16.

## Synthèse

| Collectivité | Fiches | Stables | Instables | % stable | Paires 3/3 | Majorité = prod |
|---|---:|---:|---:|---:|---:|---:|
| Hélette (13693) | 41 | 25 | 16 | 61% | 18/54 | non classée en prod |
| Saint-Jean-de-Braye (1609) | 36 | 22 | 14 | 61% | 37/72 | non classée en prod |
| CA Privas Centre Ardèche (3893) | 100 | 61 | 39 | 61% | 69/152 | 15/49 |
| CC Ardennes Thiérache (3914) | 104 | 56 | 48 | 54% | 77/243 | 11/57 |
| CA Rochefort Océan (4026) | 75 | 50 | 25 | 67% | 45/103 | 24/52 |
| CA Guingamp-Paimpol Agglomération de l'Armor à l'Argoat (4097) | 102 | 52 | 50 | 51% | 103/307 | 12/53 |
| CC Creuse Sud Ouest (4111) | 80 | 54 | 26 | 68% | 19/73 | 5/30 |
| Bordeaux Métropole (4322) | 55 | 16 | 39 | 29% | 105/313 | 3/37 |
| CC de la Forêt (4576) | 94 | 39 | 55 | 41% | 63/202 | 13/63 |
| CC Baugeois Vallée (4637) | 91 | 32 | 59 | 35% | 110/282 | 11/69 |
| CC du Pays de Colombey et du Sud Toulois (4707) | 83 | 35 | 48 | 42% | 59/149 | 19/67 |
| CC du Pays de Barr (4939) | 41 | 29 | 12 | 71% | 32/51 | 23/39 |
| CC Sundgau (4973) | 37 | 22 | 15 | 59% | 34/62 | non classée en prod |
| CC du Pays de l'Arbresle (CCPA) (4994) | 96 | 41 | 55 | 43% | 59/185 | 16/65 |
| Métropole de Lyon (4999) | 81 | 41 | 40 | 51% | 82/241 | 12/47 |
| CC Val de Gray (5005) | 42 | 29 | 13 | 69% | 46/87 | non classée en prod |
| CC Brionnais Sud Bourgogne (5033) | 111 | 74 | 37 | 67% | 56/117 | 18/73 |
| Le Havre Seine Métropole (5119) | 88 | 56 | 32 | 64% | 75/157 | 16/46 |
| CC du Pays des Achards (5300) | 103 | 75 | 28 | 73% | 65/148 | 16/46 |
| Paris Est Marne & Bois (5390) | 141 | 85 | 56 | 60% | 62/160 | 22/75 |
| SM du SCoT Sambre Avesnois (6030) | 73 | 28 | 45 | 38% | 56/176 | 6/53 |
| **Total** | **1674** | **922** | **752** | **55%** | | |

« Paires 3/3 » : paires levier × catégorie données par les 3 runs, sur toutes les paires proposées au moins une fois.

## Hélette (13693)

- Fiches : **41** — stables sur les 3 runs : **25** (61%), instables : **16**
- Paires levier × catégorie distinctes proposées : 54 — 3/3 runs : 18, 2/3 runs : 17, 1/3 runs : 19
- Aucune classification en prod pour cette collectivité
- Réponses JSON invalides rejouées : 0
- Appels : 6 — tokens d'entrée 31 713 (dont 0 en cache, 0%), sortie 36 011 — coût estimé 0.10 $ pour les 3 runs
- Date : 2026-10-30 14:38

### Classée dans certains runs, aucun levier dans d'autres (10)

#### Fiche 143322 — 2.1.1 - Réorienter les demandes de rénovation de particuliers vers la MHE

- **Run 1 :** (aucun levier)
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6] | Sobriété des bâtiments (résidentiel) [6]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6] | Sobriété des bâtiments (résidentiel) [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (2/3), Changement chaudières gaz + rénovation (résidentiel) (2/3), Sobriété des bâtiments (résidentiel) (2/3)

#### Fiche 143323 — 2.1.2 - Recenser les logements vacants et inciter les propriétaires à les remettre sur le marché locatif

- **Run 1 :** Sobriété foncière [6]
- **Run 2 :** Sobriété foncière [6]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété foncière (2/3)

#### Fiche 143324 — 3.1.1 - Se mettre en conformité avec les lois Egalim en restauration collective

- **Run 1 :** (aucun levier)
- **Run 2 :** (aucun levier)
- **Run 3 :** Changements de pratiques de fertilisation azotée [5] | Elevage durable [5] | Pratiques stockantes [5]
- **Prod :** (aucun levier)
- Leviers intermittents : Changements de pratiques de fertilisation azotée (1/3), Elevage durable (1/3), Pratiques stockantes (1/3)

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="56f12250-6d60-453b-ab37-e02a5b971a11"><div class="bn-block" data-node-type="blockContainer" data-id="56f12250-6d60-453b-ab37-e02a5b971a11"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]"></p></div></div></div></div>

#### Fiche 143326 — 3.1.3 - Animer des ateliers d'éducation à l'alimentation bio et durable dans les cantines des écoles

- **Run 1 :** (aucun levier)
- **Run 2 :** (aucun levier)
- **Run 3 :** Changements de pratiques de fertilisation azotée [1, 2] | Gestion des prairies [1, 2] | Pratiques stockantes [1, 2]
- **Prod :** (aucun levier)
- Leviers intermittents : Changements de pratiques de fertilisation azotée (1/3), Gestion des prairies (1/3), Pratiques stockantes (1/3)

#### Fiche 143327 — 3.2.1 - Identifier et valoriser les terrains publics propices pour des activités agroécologiques et une production citoyenne nourricière

- **Run 1 :** Changements de pratiques de fertilisation azotée [1, 2] | Pratiques stockantes [1, 2]
- **Run 2 :** Changements de pratiques de fertilisation azotée [1, 2] | Pratiques stockantes [1, 2]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Changements de pratiques de fertilisation azotée (2/3), Pratiques stockantes (2/3)

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="f71a2696-dff3-4f81-8c8f-5369a645655c"><div class="bn-block" data-node-type="blockContainer" data-id="f71a2696-dff3-4f81-8c8f-5369a645655c"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]">A Hélette : </p></div></div></div><div class="bn-block-outer" data-node-type="blockOuter" data-id="d7fbb…

#### Fiche 143330 — 3.2.4 - Développer les circuits courts sur la commune

- **Run 1 :** (aucun levier)
- **Run 2 :** Efficacité et sobriété logistique [6]
- **Run 3 :** Efficacité et sobriété logistique [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Efficacité et sobriété logistique (2/3)

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="bb0d41ad-61c1-4a34-8083-e8cbfd117e43"><div class="bn-block" data-node-type="blockContainer" data-id="bb0d41ad-61c1-4a34-8083-e8cbfd117e43"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]"></p></div></div></div></div>

#### Fiche 143344 — 5.2.1 - Adhérer au Groupement d'Achat d'Energie Pays Basque

- **Run 1 :** (aucun levier)
- **Run 2 :** Electricité renouvelable [5]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Electricité renouvelable (1/3)

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="18d34254-751d-47f8-b1f8-7899af5a1653"><div class="bn-block" data-node-type="blockContainer" data-id="18d34254-751d-47f8-b1f8-7899af5a1653"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]"></p></div></div></div></div>

#### Fiche 143356 — 5.4.1 - Repenser les achats de la commune sous l'angle de la sobriété et de l'éco-responsabilité

- **Run 1 :** Prévention des déchets [5]
- **Run 2 :** (aucun levier)
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Prévention des déchets (1/3)

> Cette action peut par exemple consister à : Instaurer de clauses environnementales dans les marchés publics Acheter des produits recyclés ou issu du réémploi, notamment pour le mobilier et les équipements municipaux

#### Fiche 143375 — 6.2.6 - Développer et systématiser les principes de gestion différenciée des espaces verts

- **Run 1 :** (aucun levier)
- **Run 2 :** Pratiques stockantes [1]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Pratiques stockantes (1/3)

#### Fiche 143382 — 6.4.2 - Déployer des forêts pédagogiques sur des parcelles dédiées, en collaboration avec des écoles

- **Run 1 :** Gestion des forêts et produits bois [1, 6]
- **Run 2 :** Gestion des forêts et produits bois [1, 6]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Gestion des forêts et produits bois (2/3)

### Levier présent dans certains runs seulement (2)

#### Fiche 143333 — 4.1.3 - Réaménager les entrées des établissements scolaires pour limiter la voiture

- **Run 1 :** Réduction des déplacements [1]
- **Run 2 :** Réduction des déplacements [1]
- **Run 3 :** Vélo et transport en commun [1]
- **Prod :** (aucun levier)
- Leviers intermittents : Réduction des déplacements (2/3), Vélo et transport en commun (1/3)

#### Fiche 143343 — 4.3.2 - Optimiser les émissions de la flotte communale

- **Run 1 :** Véhicules électriques [5] | Vélo et transport en commun [5]
- **Run 2 :** Véhicules électriques [5]
- **Run 3 :** Efficacité et carburants décarbonés des véhicules privés [5] | Véhicules électriques [5]
- **Prod :** (aucun levier)
- Leviers intermittents : Efficacité et carburants décarbonés des véhicules privés (1/3), Vélo et transport en commun (1/3)

> Plusieurs sous -actions peuvent être mises en oeuvre : Acheter des véhicules électriques Intégrer des vélos de service dans la flotte

### Levier intermittent et catégories instables (1)

#### Fiche 143328 — 3.2.2 - Remettre en culture bio des terres en friches pour des productions végétales et ne plus consommer de terres agricoles sur la commune

- **Run 1 :** Changements de pratiques de fertilisation azotée [1, 2] | Pratiques stockantes [1, 2] | Sobriété foncière [1, 2]
- **Run 2 :** Changements de pratiques de fertilisation azotée [2] | Pratiques stockantes [2] | Sobriété foncière [2]
- **Run 3 :** Changements de pratiques de fertilisation azotée [1, 2] | Pratiques stockantes [1, 2]
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété foncière (2/3)
- Catégories instables sur : Changements de pratiques de fertilisation azotée, Pratiques stockantes

> A suivre avec PLUi

### Mêmes leviers, catégories différentes (3)

#### Fiche 143345 — 5.2.4 - Développer le recours à de la chaleur d'origine renouvelable et de récupération (EnR&R)

- **Run 1 :** Réseaux de chaleur décarbonés [5]
- **Run 2 :** Réseaux de chaleur décarbonés [1]
- **Run 3 :** Réseaux de chaleur décarbonés [1]
- **Prod :** (aucun levier)
- Catégories instables sur : Réseaux de chaleur décarbonés

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="1d957724-3a97-4579-b9d8-cab5ff82ae64"><div class="bn-block" data-node-type="blockContainer" data-id="1d957724-3a97-4579-b9d8-cab5ff82ae64"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]"></p></div></div></div><div class="bn-block-outer" data-node-type="blockOuter" data-id="3985f98f-85a9-475…

#### Fiche 143348 — 5.2.2 - Développer des projets communaux d'autoconsommation collective

- **Run 1 :** Electricité renouvelable [5]
- **Run 2 :** Electricité renouvelable [1]
- **Run 3 :** Electricité renouvelable [5]
- **Prod :** (aucun levier)
- Catégories instables sur : Electricité renouvelable

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="41f7730a-663e-40a5-bb41-599407dcb792"><div class="bn-block" data-node-type="blockContainer" data-id="41f7730a-663e-40a5-bb41-599407dcb792"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]"></p></div></div></div></div>

#### Fiche 143349 — 5.1.1 - Elaborer et mettre en œuvre une stratégie immobilière d’économie d’énergie

- **Run 1 :** Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 2 :** Sobriété et isolation des bâtiments (tertiaire) [4, 5]
- **Run 3 :** Sobriété et isolation des bâtiments (tertiaire) [5]
- **Prod :** (aucun levier)
- Catégories instables sur : Sobriété et isolation des bâtiments (tertiaire)

> Cette action structurante peut faire l'objet de plusieurs sous-actions pour être mise en oeuvre : Réaliser un audit énergétique/rénovation thermique des batiments communaux Engager des travaux de rénovation thermique des batiments communaux si les audits sont concluants Assurer le suivi avec le logiciel CITRON Si action "1.1.4 - Assurer l'exemplarité de la commune en terme de sobriété" en cours, faire le lien avec le référent sobriété identifié dans cette action

## Saint-Jean-de-Braye (1609)

- Fiches : **36** — stables sur les 3 runs : **22** (61%), instables : **14**
- Paires levier × catégorie distinctes proposées : 72 — 3/3 runs : 37, 2/3 runs : 13, 1/3 runs : 22
- Aucune classification en prod pour cette collectivité
- Réponses JSON invalides rejouées : 0
- Appels : 6 — tokens d'entrée 18 576 (dont 0 en cache, 0%), sortie 29 454 — coût estimé 0.07 $ pour les 3 runs
- Date : 2026-10-30 14:38

### Classée dans certains runs, aucun levier dans d'autres (3)

#### Fiche 16431 — Prévenir et lutter contre la précarité énergétique

- **Run 1 :** (aucun levier)
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6] | Sobriété des bâtiments (résidentiel) [6]
- **Run 3 :** Réduction des déplacements [6] | Sobriété des bâtiments (résidentiel) [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (1/3), Changement chaudières gaz + rénovation (résidentiel) (1/3), Réduction des déplacements (1/3), Sobriété des bâtiments (résidentiel) (2/3)

> Engager une politique de prévention et de lutte contre la précarité énergétique (liée au logement et à la mobilité) et l'inscrire dans ses documents stratégiques. Réaliser un travail d’inventaire des acteurs de la précarité énergétique et des actions existantes, sur lesquelles construire le dispositif. Utiliser au mieux les moyens humains à disposition pour identifier des situations de précarité énergétique du logement et orienter les familles directement vers les dispositifs existants ou indir…

#### Fiche 16436 — Optimiser l'éclairage public

- **Run 1 :** (aucun levier)
- **Run 2 :** (aucun levier)
- **Run 3 :** Sobriété et isolation des bâtiments (tertiaire) [5]
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété et isolation des bâtiments (tertiaire) (1/3)

> Limiter les points lumineux autant que nécessaire. Réduire les plages horaires de fonctionnement en adaptant l'éclairage aux usages Remplacer les équipements par des systèmes LED performants

#### Fiche 16445 — Restauration collective : développer les circuits courts, les produits de saison et issus de l'agriculture biologique

- **Run 1 :** (aucun levier)
- **Run 2 :** Changements de pratiques de fertilisation azotée [5] | Elevage durable [5]
- **Run 3 :** Efficacité et sobriété logistique [5]
- **Prod :** (aucun levier)
- Leviers intermittents : Changements de pratiques de fertilisation azotée (1/3), Efficacité et sobriété logistique (1/3), Elevage durable (1/3)

> La restauration collective atteint des taux élevée de produits locaux, de saison et biologiques Ces taux sont au-dessus des objectifs réglementaires fixés par la loi égalim.

### Levier présent dans certains runs seulement (5)

#### Fiche 16433 — Disposer d'un plan de mobilité visant la décarbonation des transports sur le territoire

- **Run 1 :** Bus et cars décarbonés [2] | Covoiturage [2] | Fret décarboné et multimodalité [2] | Réduction des déplacements [2] | Véhicules électriques [2] | Vélo et transport en commun [2]
- **Run 2 :** Bus et cars décarbonés [2] | Covoiturage [2] | Efficacité et carburants décarbonés des véhicules privés [2] | Efficacité et sobriété logistique [2] | Fret décarboné et multimodalité [2] | Réduction des déplacements [2] | Véhicules électriques [2] | Vélo et transport en commun [2]
- **Run 3 :** Bus et cars décarbonés [2] | Covoiturage [2] | Efficacité et carburants décarbonés des véhicules privés [2] | Efficacité et sobriété logistique [2] | Fret décarboné et multimodalité [2] | Réduction des déplacements [2] | Véhicules électriques [2] | Vélo et transport en commun [2]
- **Prod :** (aucun levier)
- Leviers intermittents : Efficacité et carburants décarbonés des véhicules privés (2/3), Efficacité et sobriété logistique (2/3)

> Disposer d’une planification spatialisée des déplacements sur son territoire avec des indications concrètes, des orientations stratégiques et un dispositif de suivi et de contrôle pour : - réduire le trafic motorisé individuel – l’autosolisme - promouvoir les modes actifs (marche, vélo), l'intermodalité et les mobilités partagées - Promouvoir une logistique urbaine durable - promouvoir les carburants alternatifs (électrique batterie, bioGNV, hydrogène renouvelable) et l’hippomobilité, développe…

#### Fiche 16434 — Développer le réseau piétonnier

- **Run 1 :** Réduction des déplacements [1] | Vélo et transport en commun [1]
- **Run 2 :** Réduction des déplacements [1] | Vélo et transport en commun [1]
- **Run 3 :** Réduction des déplacements [1]
- **Prod :** (aucun levier)
- Leviers intermittents : Vélo et transport en commun (2/3)

> Le réseau piétonnier et la marchabilité est priorisée dans tous les aménagements du territoire

#### Fiche 16435 — Développer le réseau et les infrastructures cyclables

- **Run 1 :** Vélo et transport en commun [1]
- **Run 2 :** Réduction des déplacements [1] | Vélo et transport en commun [1]
- **Run 3 :** Vélo et transport en commun [1]
- **Prod :** (aucun levier)
- Leviers intermittents : Réduction des déplacements (1/3)

> Le réseau cyclable et la cyclabilité sont priorisés dans tous les aménagements de voirie sur le territoire. Le stationnement à vélo est facile et privilégié pour les cyclistes par rapport aux automobilistes aux abords des lieux publics et des lieux à forte fréquentation du public.

#### Fiche 16437 — Préserver la biodiversité du territoire et développer des espaces verts

- **Run 1 :** Gestion des forêts et produits bois [1, 2]
- **Run 2 :** Pratiques stockantes [1, 2]
- **Run 3 :** Sobriété foncière [1, 2]
- **Prod :** (aucun levier)
- Leviers intermittents : Gestion des forêts et produits bois (1/3), Pratiques stockantes (1/3), Sobriété foncière (1/3)

> Protéger les espaces naturels existants et développer les trames vertes et bleues. Végétaliser en plantant des arbres et en développant les espaces verts avec une approche prenant en considération les risques d'évolution climatique sur le territoire et en choisissant des espèces permettant de supprimer (ou a minima de limiter) les besoins d'arrosage.

#### Fiche 16439 — Stopper l'artificialisation

- **Run 1 :** Sobriété foncière [2]
- **Run 2 :** Pratiques stockantes [2] | Sobriété foncière [2]
- **Run 3 :** Sobriété foncière [2]
- **Prod :** (aucun levier)
- Leviers intermittents : Pratiques stockantes (1/3)

> Utiliser les documents d'urbanisme pour lutter contre l'artificialisation des sols, assurer le maintien des espaces naturels, agricoles et forestiers et favoriser la restauration de ces espaces quand cela est possible.

### Levier intermittent et catégories instables (3)

#### Fiche 16423 — Soutenir une agriculture et une alimentation plus durable

- **Run 1 :** Bâtiments & Machines agricoles [6] | Changements de pratiques de fertilisation azotée [3, 6] | Elevage durable [3, 6] | Prévention des déchets [5, 6] | Sobriété foncière [2]
- **Run 2 :** Bâtiments & Machines agricoles [6] | Changements de pratiques de fertilisation azotée [6] | Elevage durable [6] | Prévention des déchets [6] | Sobriété foncière [2]
- **Run 3 :** Changements de pratiques de fertilisation azotée [3, 6] | Elevage durable [3, 6] | Prévention des déchets [3, 5, 6]
- **Prod :** (aucun levier)
- Leviers intermittents : Bâtiments & Machines agricoles (2/3), Sobriété foncière (2/3)
- Catégories instables sur : Changements de pratiques de fertilisation azotée, Elevage durable, Prévention des déchets

> Soutenir, promouvoir et encourager des pratiques agricoles et alimentaires durables sur son territoire et sur ses territoires d’approvisionnement : - en menant des actions visant à réduire les émissions de gaz à effet de serre, de particules et plus globalement les impacts environnementaux du secteur agricole (formation aux pratiques agro-écologiques, certification environnementale des exploitations...) - en préservant le foncier agricole au travers des documents d’urbanisme et en accompagnant …

#### Fiche 16427 — Soutenir l'utilisation durable des forêts et des espaces boisés

- **Run 1 :** Gestion des forêts et produits bois [2, 3, 6]
- **Run 2 :** Gestion des forêts et produits bois [2, 6] | Pratiques stockantes [2, 6]
- **Run 3 :** Gestion des forêts et produits bois [2, 3, 6]
- **Prod :** (aucun levier)
- Leviers intermittents : Pratiques stockantes (1/3)
- Catégories instables sur : Gestion des forêts et produits bois

> - Prendre en compte la forêt et les espaces boisés dans ses documents d’urbanisme, dans un objectif d’identification, de préservation, d’utilisation rationnelle ou de développement. - Inciter aux pratiques sylvicoles durables et au développement des pratiques de gestion raisonnée des forêts et espaces boisés, en interne et auprès des particuliers et des professionnels. - Contribuer à structurer et développer des filières bois-énergie et bois-construction.

#### Fiche 16444 — Connaitre le potentiel de développement des ENR du territoire et programmer leur développement

- **Run 1 :** Electricité renouvelable [2, 4]
- **Run 2 :** Biogaz [2] | Electricité renouvelable [2]
- **Run 3 :** Biogaz [2] | Electricité renouvelable [2] | Réseaux de chaleur décarbonés [2]
- **Prod :** (aucun levier)
- Leviers intermittents : Biogaz (2/3), Réseaux de chaleur décarbonés (1/3)
- Catégories instables sur : Electricité renouvelable

> - Prendre en compte et quantifier tous les potentiels de développement - Programmer la mise en oeuvre de l'ensemble du potentiel de production d'énergie renouvelable locale

### Mêmes leviers, catégories différentes (3)

#### Fiche 16438 — Limiter l’emprise de la publicité

- **Run 1 :** Prévention des déchets [2, 6]
- **Run 2 :** Prévention des déchets [2, 6]
- **Run 3 :** Prévention des déchets [3, 6]
- **Prod :** (aucun levier)
- Catégories instables sur : Prévention des déchets

> - Sensibiliser les habitants à travers des actions rapides et efficaces tel que la promotion et généralisation du Stop Pub pour réduire les imprimés - Faire respecter les obligations concernant les enseignes lumineuses des commerces et l'affichage sur la voie publique - Mettre en place une taxe locale sur les enseignes et publicités extérieures (TPLE) - Devenir une ville sans publicité en instaurant une Zone de Publicité Restreinte et en supprimant la publicité commerciale au profit d'une publi…

#### Fiche 16443 — Mettre en place une politique d'achat exemplaires pour avoir un impact positif sur le territoire

- **Run 1 :** Réduction des déplacements [2, 3, 6]
- **Run 2 :** Réduction des déplacements [2, 6]
- **Run 3 :** Réduction des déplacements [2, 3, 6]
- **Prod :** (aucun levier)
- Catégories instables sur : Réduction des déplacements

> Mettre en place une politique de stationnement dans le centre-ville et/ ou les zones de forte pression (commerces de quartier, etc.) Mettre en place une tarification différenciée si besoin Pour les communes en zones rurale, mettre l'accent sur la sensibilisation et l’information auprès des habitants sur le besoin de gérer l’usage de la voiture et de marquer les places réservées au stationnement et le développement de zones bleues le cas échéant autour des zones de trafic. Faire respecter la rég…

#### Fiche 16449 — Élaborer une politique de stationnement volontariste

- **Run 1 :** Réduction des déplacements [2]
- **Run 2 :** Réduction des déplacements [2]
- **Run 3 :** Réduction des déplacements [1, 2]
- **Prod :** (aucun levier)
- Catégories instables sur : Réduction des déplacements

> Mettre en place une politique de stationnement dans le centre-ville et/ ou les zones de forte pression (commerces de quartier, etc.) Mettre en place une tarification différenciée si besoin Pour les communes en zones rurale, mettre l'accent sur la sensibilisation et l’information auprès des habitants sur le besoin de gérer l’usage de la voiture et de marquer les places réservées au stationnement et le développement de zones bleues le cas échéant autour des zones de trafic. Faire respecter la rég…

## CA Privas Centre Ardèche (3893)

- Fiches : **100** — stables sur les 3 runs : **61** (61%), instables : **39**
- Paires levier × catégorie distinctes proposées : 152 — 3/3 runs : 69, 2/3 runs : 24, 1/3 runs : 59
- Vote majoritaire = prod : 15/49 fiches classées d'un côté ou de l'autre
- Réponses JSON invalides rejouées : 0
- Appels : 12 — tokens d'entrée 48 297 (dont 0 en cache, 0%), sortie 63 796 — coût estimé 0.17 $ pour les 3 runs
- Date : 2026-10-30 15:07

### Classée dans certains runs, aucun levier dans d'autres (10)

#### Fiche 78909 — Fiche action 1.7 - Former des relais pour la lutte contre la précarité énergétique

- **Run 1 :** (aucun levier)
- **Run 2 :** Sobriété des bâtiments (résidentiel) [6]
- **Run 3 :** Sobriété des bâtiments (résidentiel) [6]
- **Prod :** Sobriété des bâtiments (résidentiel) [6]
- Leviers intermittents : Sobriété des bâtiments (résidentiel) (2/3)

> Nouvelle action (en lien avec le travail des OPAH, Rénofuté et ALEC 07) • Offrir un accompagnement adapté aux ménages en précarité énergétique • Repérer les situations de précarité énergétique, notamment les personnes isolées, en restriction, et non suivies par les services sociaux • Repérer les logements insalubres, avec des pertes énergétiques etc. • Sensibiliser / faire connaitre les actions éco-citoyennes, les aides, les acteurs opérationnels, les offres de service possible et l’accès aux d…

#### Fiche 78913 — Fiche action 1.11- Adapter les villes et les bâtiments publics et privés aux chaleurs estivales

- **Run 1 :** (aucun levier)
- **Run 2 :** (aucun levier)
- **Run 3 :** Pratiques stockantes [1] | Sobriété des bâtiments (résidentiel) [3] | Sobriété et isolation des bâtiments (tertiaire) [3, 5]
- **Prod :** (aucun levier)
- Leviers intermittents : Pratiques stockantes (1/3), Sobriété des bâtiments (résidentiel) (1/3), Sobriété et isolation des bâtiments (tertiaire) (1/3)

> Nouvelle action. - Diminution des îlots de chaleur urbains - Amélioration de la qualité de l’air - Stockage carbone - Restauration des continuités écologiques - Réduction des températures des bâtiments en été - Lutter contre la prolifération des climatiseurs - Eviter la mortalité due aux périodes de canicule Éléments de calendrier : Année 1 : étude, montage du fond d’aide et du fond de concours Année 2-6 : réalisation, accompagnement

#### Fiche 78915 — Fiche action 2.2 - Développer les énergies renouvelables pour le chauffage et l’eau-chaude des bâtiments publics et privés

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6] | Changement de chaudière à fioul (tertiaire) [5] | Changement de chaudière à gaz (tertiaire) [5] | Sobriété des bâtiments (résidentiel) [6] | Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 2 :** (aucun levier)
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (1/3), Changement chaudières gaz + rénovation (résidentiel) (1/3), Changement de chaudière à fioul (tertiaire) (1/3), Changement de chaudière à gaz (tertiaire) (1/3), Sobriété des bâtiments (résidentiel) (1/3), Sobriété et isolation des bâtiments (tertiaire) (1/3)

> Action nouvelle • Réduire la facture énergétique • Tendre vers plus d’autonomie énergétique • Développer la géothermie - Production de chaud et de froid (climatisation) - Amélioration des connaissances et sensibilisation sur cette technologie - Promouvoir les artisans locaux • Améliorer l’utilisation du chauffage au bois - Réduire la contribution du bois-énergie à la pollution de l’air - Réduire la consommation de combustible - Regrouper la filière autour d’une plateforme intercommunale pour st…

#### Fiche 78940 — Fiche action 4.7 -Réaliser un guide d’achat durable pour la collectivité

- **Run 1 :** (aucun levier)
- **Run 2 :** (aucun levier)
- **Run 3 :** Prévention des déchets [5]
- **Prod :** (aucun levier)
- Leviers intermittents : Prévention des déchets (1/3)

> Nouvelle Réduction de l’impact environnemental des achats du territoire MDE Éléments de calendrier : 2020

#### Fiche 82518 — TR4 - Assurer une meilleure intégration paysagère des projets

- **Run 1 :** (aucun levier)
- **Run 2 :** Electricité renouvelable [2]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Electricité renouvelable (1/3)

#### Fiche 82525 — E1 - Encourager le renouvellement des parcs existants

- **Run 1 :** (aucun levier)
- **Run 2 :** Efficacité et carburants décarbonés des véhicules privés [6]
- **Run 3 :** Efficacité et carburants décarbonés des véhicules privés [3]
- **Prod :** (aucun levier)
- Leviers intermittents : Efficacité et carburants décarbonés des véhicules privés (2/3)

#### Fiche 117837 — 2.1.1 Restauration de milieux à Saint-Julien-en-Saint-Alban [travaux]

- **Run 1 :** (aucun levier)
- **Run 2 :** Pratiques stockantes [1]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Pratiques stockantes (1/3)

> Code action PTGE: B8. Références: Feuille de route des Assises de l'Eau 07 (2023) - 15; Défi 11.

#### Fiche 117839 — 2.1.3 Restauration de milieu Mézayon [travaux]

- **Run 1 :** (aucun levier)
- **Run 2 :** Pratiques stockantes [1]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Pratiques stockantes (1/3)

> Code action PTGE: B10. Références: Feuille de route des Assises de l'Eau 07 (2023) - 15; Défi 11.

#### Fiche 117842 — 2.1.6 Restauration des fonctionnalités du Charalon

- **Run 1 :** (aucun levier)
- **Run 2 :** Pratiques stockantes [1]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Pratiques stockantes (1/3)

> Code action PTGE: B13. Références: Feuille de route des Assises de l'Eau 07 (2023) - 15; Défi 11; SCOT - R 55.

#### Fiche 117843 — 2.1.7 Plan de Gestion Stratégique Zones Humides

- **Run 1 :** (aucun levier)
- **Run 2 :** Pratiques stockantes [2]
- **Run 3 :** Pratiques stockantes [2]
- **Prod :** (aucun levier)
- Leviers intermittents : Pratiques stockantes (2/3)

> Code action PTGE: B14. Coût: Temps agent. Références: Feuille de route des Assises de l'Eau 07 (2023) - 15; Défi 15; SCOT - P 103, R 55.

### Levier présent dans certains runs seulement (11)

#### Fiche 78903 — Fiche action 1.1 - Massifier la rénovation thermique exemplaire du bâti public (notamment en promouvant le bois local et le solaire
photovoltaïque dans les projets)

- **Run 1 :** Electricité renouvelable [5] | Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 2 :** Electricité renouvelable [5] | Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 3 :** Electricité renouvelable [5] | Gestion des forêts et produits bois [5] | Sobriété et isolation des bâtiments (tertiaire) [5]
- **Prod :** Electricité renouvelable [5] | Sobriété et isolation des bâtiments (tertiaire) [5]
- Leviers intermittents : Gestion des forêts et produits bois (1/3)

> Nouvelle sur la CAPCA mais intégrée aux missions globales des communes forestières et de Fibois Ardèche-Drôme Valoriser le matériau bois pour ses avantages dans les projets de rénovation / réhabilitation et son intérêt dans le développement de circuits courts / Production d’EnR et maîtrise de l’énergie. • Faire connaître les avantages du bois dans les rénovations : légèreté, performance thermique, facilité d’utilisation… • Utiliser du bois local pour favoriser les circuits courts (certification…

#### Fiche 78911 — Fiche action 1.9 - Renforcer et déployer les permanences info-énergie et habitat des partenaires

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6] | Sobriété des bâtiments (résidentiel) [6]
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6] | Sobriété des bâtiments (résidentiel) [6]
- **Run 3 :** Sobriété des bâtiments (résidentiel) [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (2/3), Changement chaudières gaz + rénovation (résidentiel) (2/3)

> En cours : • La Voulte sur Rhône, permanences hebdomadaires, • Les Ollières sur Eyrieux, Vernoux en Vivarais et Privas, mensuelles, • Favoriser l’accès aux services pour les bénéficiaires • Faciliter les actions des partenaires • Accompagner les particuliers de manière indépendante • Fluidifier le parcours pour les ménages Éléments de calendrier : Année 1 : signature des conventions de partenariat et lancement des permanences au bout de 3 mois

#### Fiche 78920 — Fiche action 3.1 - Redonner de l’attractivité aux centres-bourgs et villages

- **Run 1 :** Réduction des déplacements [1, 2] | Sobriété foncière [1, 2]
- **Run 2 :** Réduction des déplacements [1, 2] | Sobriété foncière [1, 2]
- **Run 3 :** Sobriété foncière [1, 2]
- **Prod :** Réduction des déplacements [1, 2] | Sobriété foncière [2]
- Leviers intermittents : Réduction des déplacements (2/3)

> Problématique relativement nouvelle, déjà engagée via des actions comme « Privas Coeur de Ville » mais à étendre aux pôles de centralité (La Voulte sur Rhône, Le Pouzin, Les Ollières sur Eyrieux, St Sauveur de Montagut et Vernoux-en-Vivarais), aux pôles intermédiaires et aux villages. • Limiter l’étalement urbain et les besoins en déplacements • Eviter les concurrences résidentielles entre centre et périphérie • S’engager vers une co-définition de l’espace urbain (via des concertations publique…

#### Fiche 78925 — Fiche action 3.6 - Sensibiliser les publics précaires aux enjeux mobilité

- **Run 1 :** Covoiturage [6] | Véhicules électriques [6] | Vélo et transport en commun [6]
- **Run 2 :** Vélo et transport en commun [6]
- **Run 3 :** Vélo et transport en commun [6]
- **Prod :** Vélo et transport en commun [3, 6]
- Leviers intermittents : Covoiturage (1/3), Véhicules électriques (1/3)

> Action nouvelle – démarrage mi 2019 • Cohésion sociale au niveau du territoire • Mobilité alternative • Lutte contre les précarités Éléments de calendrier : Fin 2019 lancement de l’opération 2020 : mise en place des ateliers et acquisition des VAE 2021 : suivi du projet et réalisation des outils de communication 2022 : poursuite du projet et recherche de financement

#### Fiche 78927 — Fiche action 3.8 - Inciter à se déplacer sur les voies douces

- **Run 1 :** Vélo et transport en commun [6]
- **Run 2 :** Vélo et transport en commun [6]
- **Run 3 :** Réduction des déplacements [6] | Vélo et transport en commun [6]
- **Prod :** Vélo et transport en commun [6]
- Leviers intermittents : Réduction des déplacements (1/3)

> Nouvelle • Inciter à la mobilité active • Densifier le trafic alternatif à la route, inciter à la pratique de mobilités actives • Réduire l’usage de la voiture sur les courtes distances • Améliorer la santé des usagers • Créer du lien social entre usagers • Découvrir des sites non visibles depuis la route Éléments de calendrier : Fin 2021 : lancement d’une campagne d’information et de communication 2021 - 2022 : Rencontres des partenaires sociaux et des établissements scolaires pour mise en pla…

#### Fiche 78932 — Fiche action 3.13 - Mettre en place le réseau de transport en commun T'CAP

- **Run 1 :** Vélo et transport en commun [1]
- **Run 2 :** Vélo et transport en commun [1]
- **Run 3 :** Réduction des déplacements [1] | Vélo et transport en commun [1]
- **Prod :** Vélo et transport en commun [1, 4]
- Leviers intermittents : Réduction des déplacements (1/3)

> Engagée en 2018 • Mise en place de transports collectifs sur l’ensemble du territoire • Adaptation de l’offre aux caractéristiques du territoire : réseau urbain en zone urbaine, lignes régulières en péri urbain et TAD en zones rurales • Réduction de l’autosolisme • Faire évoluer les comportements en faveur des transports collectifs • Réduire l’isolement de certaines catégories d’usagers : personnes âgées, personnes en inserti Éléments de calendrier : Septembre 2018 : Mise en place du réseau T’C…

#### Fiche 78935 — Fiche action 4.2 - Créer une plateforme en ligne « Bourse aux déchets » et réaliser une action « commerçants zéro déchets"

- **Run 1 :** Prévention des déchets [6] | Valorisation matière des déchets [6]
- **Run 2 :** Efficacité et sobriété logistique [6] | Prévention des déchets [6] | Valorisation matière des déchets [6]
- **Run 3 :** Efficacité et sobriété logistique [6] | Fret décarboné et multimodalité [6] | Prévention des déchets [6] | Valorisation matière des déchets [6]
- **Prod :** Prévention des déchets [4, 6] | Valorisation matière des déchets [4, 6]
- Leviers intermittents : Efficacité et sobriété logistique (2/3), Fret décarboné et multimodalité (1/3)

> Nouvelle • Sensibiliser et éduquer les acteurs économiques, les fédérer (via les unions commerciales) à questionner leurs pratiques • Réduction des transports de marchandise • Valorisation et réduction des déchets • Création de synergies entre acteurs économiques (y compris artisans et commerces) Éléments de calendrier : • 2021 : Repérage des acteurs volontaires et recrutement d’un animateur, lancement de la démarche dans le cadre de la SERD • 2022 : Restitution, synthèse et développement de la…

#### Fiche 78938 — Fiche action 4.5 - Accompagner la restauration collective vers un approvisionnement local de qualité

- **Run 1 :** Fret décarboné et multimodalité [5]
- **Run 2 :** Efficacité et sobriété logistique [3, 6]
- **Run 3 :** Fret décarboné et multimodalité [5, 6]
- **Prod :** (aucun levier)
- Leviers intermittents : Efficacité et sobriété logistique (1/3), Fret décarboné et multimodalité (2/3)

> Action partiellement engagée, à renforcer par une incitation locale • Réduire les consommations énergétiques liées aux transports et à l’approvisionnement • Limiter les intrants dans le sol • Sensibiliser à la consommation de produits locaux et de saison et une alimentation saine • Sensibiliser à la conversion des agriculteurs en bio (étapes, coûts, bénéfices…) • Création d’emploi sur le territoire • Réduire l’impact écologique du secteur tertiaire (kWh consommés et CO2 évités) Éléments de cale…

#### Fiche 78943 — Fiche action 4.10 - Installer des composteurs partagés au pied des HLM

- **Run 1 :** Valorisation matière des déchets [1, 6]
- **Run 2 :** Prévention des déchets [1, 6] | Valorisation matière des déchets [1, 6]
- **Run 3 :** Prévention des déchets [1, 6] | Valorisation matière des déchets [1, 6]
- **Prod :** Valorisation matière des déchets [1, 6]
- Leviers intermittents : Prévention des déchets (2/3)

> Nouvelle action • Permettre aux habitants n’ayant pas de jardin de valoriser leurs déchets organiques • Former les acteurs sociaux du territoire de la CAPCA au tri sélectif • Appréhender avec les habitants les enjeux du tri sélectif dans son ensemble • Développer le sentiment d’utilité sociale concrète et d’implication des habitants dans la vie du quartier • Sensibiliser le grand public via des actions de sensibilisation et une campagne de communication • Réduire le transport et le traitement d…

#### Fiche 78944 — Fiche action 4.11 - Adapter l’agriculture locale aux enjeux du changement climatique

- **Run 1 :** Pratiques stockantes [6]
- **Run 2 :** Pratiques stockantes [6]
- **Run 3 :** Bâtiments & Machines agricoles [6] | Pratiques stockantes [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Bâtiments & Machines agricoles (1/3)

> En cours • Adapter les exploitations aux aléas climatiques (sécheresse, canicules, inondations) • Préserver les ressources en eau en qualité et en quantité • Favoriser les cultures plus résistantes et moins consommatrices en eau • Diversifier les pratiques agricoles • Améliorer la séquestration carbone du territoire • Améliorer la qualité de l’air

#### Fiche 78945 — Fiche action 4.12 - Diminuer la consommation d’intrants (produits phytosanitaires, eau, engrais minéraux, aliments concentrés, énergie directe) dans les exploitations agricoles

- **Run 1 :** Bâtiments & Machines agricoles [6] | Changements de pratiques de fertilisation azotée [6]
- **Run 2 :** Bâtiments & Machines agricoles [6] | Changements de pratiques de fertilisation azotée [6] | Elevage durable [6]
- **Run 3 :** Bâtiments & Machines agricoles [6] | Changements de pratiques de fertilisation azotée [6] | Elevage durable [6]
- **Prod :** Bâtiments & Machines agricoles [6] | Changements de pratiques de fertilisation azotée [6]
- Leviers intermittents : Elevage durable (2/3)

> Action en cours • Diminution de la pollution des nappes phréatiques et de l’usure des sols • Amélioration de la qualité nutritive des produits consommés • Incitation à l’exemplarité • Economie de la ressource en eau • Adaptation aux futures contraintes de ressources et d’utilisation d’engrais • Amélioration de la qualité de l’air • Améliorer l’efficacité des systèmes de production sans réduire le niveau de production agricole • Renforcer l’autonomie des exploitations

### Levier intermittent et catégories instables (6)

#### Fiche 78914 — Fiche action 2.1 - Création d’une unité de méthanisation industrielle et d’une station bio-GNV

- **Run 1 :** Biogaz [1] | Efficacité et carburants décarbonés des véhicules privés [1]
- **Run 2 :** Biogaz [1, 3]
- **Run 3 :** Biogaz [1, 3]
- **Prod :** Biogaz [1, 3]
- Leviers intermittents : Efficacité et carburants décarbonés des véhicules privés (1/3)
- Catégories instables sur : Biogaz

> En cours. - Réalisation d’une unité de méthanisation - Création d’une filière de biogaz sur le territoire - Création de points d’avitaillement en biogaz sur le territoire Éléments de calendrier : Année 1 : diagnostic du potentiel, plan de communication (support et contenu), vote de l’aide (et rédaction du cahier des charges pour établir des critères d’éligibilité) Années suivantes : gestion des dossiers et des attributions

#### Fiche 78921 — Fiche action 3.2 - Rationnaliser les déplacements professionnels en mettant en place des plateformes de logistique

- **Run 1 :** Efficacité et sobriété logistique [1] | Fret décarboné et multimodalité [1] | Réduction des déplacements [1]
- **Run 2 :** Efficacité et sobriété logistique [1, 6] | Fret décarboné et multimodalité [1, 6]
- **Run 3 :** Efficacité et sobriété logistique [1] | Fret décarboné et multimodalité [1]
- **Prod :** Efficacité et sobriété logistique [1, 4]
- Leviers intermittents : Réduction des déplacements (1/3)
- Catégories instables sur : Efficacité et sobriété logistique, Fret décarboné et multimodalité

> En cours. Une micro-plateforme est en cours de montage à Saint-Sauveur de Montagut. Il s’agit maintenant d’en développer de nouvelles sur le reste du territoire. • Diminuer les consommations et émissions du transport de marchandises, • Diminuer les coûts de transports pour les entreprises • Réduire le trafic routier et l’insécurité routière • Améliorer les conditions de travail • Augmentation de l’utilisation des modes doux • Rationnaliser les livraisons de la vallée du Rhône à Privas (optimisa…

#### Fiche 78929 — Fiche action 3.10 - Mettre en oeuvre un plan de covoiturage en direction des administrations et des entreprises

- **Run 1 :** Covoiturage [4, 6]
- **Run 2 :** Covoiturage [4, 6]
- **Run 3 :** Covoiturage [6] | Réduction des déplacements [6]
- **Prod :** Covoiturage [6]
- Leviers intermittents : Réduction des déplacements (1/3)
- Catégories instables sur : Covoiturage

> Action nouvelle – Lancement prévu en septembre 2019 • Réduire l’autosolisme • Favoriser la pratique du covoiturage courte distance • Créer du lien social entre les salariés • Promouvoir les nouvelles mobilités • Apporter des solutions al ternatives au réseau urbain Éléments de calendrier : - Fin 2019 : Sensibilisation des administrations privadoises au covoiturage - 2020 : Expérimentation – 1er bilan - Fin 2021 : Extension de l’expérimentation aux ZAE du Pouzin et de La Voulte sur Rhône

#### Fiche 78934 — Fiche action 4.1 - Réduire et valoriser les déchets et relocaliser leur transformation

- **Run 1 :** Fret décarboné et multimodalité [1] | Prévention des déchets [6] | Valorisation matière des déchets [1, 6]
- **Run 2 :** Efficacité et sobriété logistique [4, 6] | Prévention des déchets [4, 6] | Valorisation matière des déchets [4, 6]
- **Run 3 :** Captage de méthane dans les ISDND [6] | Fret décarboné et multimodalité [6] | Prévention des déchets [6] | Valorisation matière des déchets [6]
- **Prod :** Prévention des déchets [4, 6] | Valorisation matière des déchets [4, 6]
- Leviers intermittents : Captage de méthane dans les ISDND (1/3), Efficacité et sobriété logistique (1/3), Fret décarboné et multimodalité (2/3)
- Catégories instables sur : Prévention des déchets, Valorisation matière des déchets

> Action nouvelle • Réduire le volume énergétique consommé par le territoire • Identifier l'ensemble (la chaîne) des consommations énergétiques du territoire, Identifier les gisements de déchets. • Donner corps aux politiques publiques, permettre au territoire Centre Ardèche d'atteindre voire de dépasser les objectifs internationaux, européens et nationaux et de développer des actions modélisables reproductives sur d'autres territoires. • Accompagner les acteurs au changement • Donner de la visib…

#### Fiche 78939 — Fiche action 4.6 - Inciter les entreprises et artisans à réduire leurs consommations de flux (énergie, eau, matières premières, déchets)

- **Run 1 :** Prévention des déchets [6]
- **Run 2 :** Production Industrielle [4, 6] | Prévention des déchets [4, 6]
- **Run 3 :** Production Industrielle [6] | Prévention des déchets [6]
- **Prod :** Production Industrielle [4, 6]
- Leviers intermittents : Production Industrielle (2/3)
- Catégories instables sur : Prévention des déchets

> En cours Disposer d’un état des lieux du territoire et identifier les leviers d’action auprès des acteurs économiques Mobiliser les acteurs de l’économie, écologie industrielle et territoriale, réduction des consommations énergétiques. Éléments de calendrier : 2021 : kit de communication 2021-2022 : recruter une AMO pour la réalisation des diagnostics 2022 : Accompagnement au changement de pratiques 2023 : Evaluation et valorisation du dispositif

#### Fiche 78941 — Fiche action 4.8 - Valoriser et récupérer les déchets verts compostables

- **Run 1 :** Fret décarboné et multimodalité [1] | Valorisation matière des déchets [1]
- **Run 2 :** Prévention des déchets [1, 6] | Valorisation matière des déchets [1, 6]
- **Run 3 :** Captage de méthane dans les ISDND [1] | Prévention des déchets [1] | Valorisation matière des déchets [1]
- **Prod :** Valorisation matière des déchets [1, 4]
- Leviers intermittents : Captage de méthane dans les ISDND (1/3), Fret décarboné et multimodalité (1/3), Prévention des déchets (2/3)
- Catégories instables sur : Valorisation matière des déchets

> Nouvelle action Réduire les transports de déchets verts (broyat moins volumineux) Diminuer les tonnages en déchetterie Favoriser la valorisation locale des déchets verts : usagers, communes et agriculteurs Moyen de soutenir l’activité agricole indirectement (enjeu économique) Limiter l’achat de produits phytosanitaires et en réduire l’usage grâce à l’utilisation du broyat produit (et faire attention aux risques sanitaires lié à la diffusion de broyat non compostés) Réduire l’arrosage des espace…

### Mêmes leviers, catégories différentes (12)

#### Fiche 78905 — Fiche action 1.3 - Concevoir et déployer sur la CAPCA le Service Public de la Performance Energétique de l’Habitat (SPPEH)

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6] | Sobriété des bâtiments (résidentiel) [6]
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [4, 6] | Changement chaudières gaz + rénovation (résidentiel) [4, 6] | Sobriété des bâtiments (résidentiel) [4, 6]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6] | Sobriété des bâtiments (résidentiel) [6]
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6] | Sobriété des bâtiments (résidentiel) [6]
- Catégories instables sur : Changement chaudières fioul + rénovation (résidentiel), Changement chaudières gaz + rénovation (résidentiel), Sobriété des bâtiments (résidentiel)

> Nouvelle action à déployer • Faciliter le parcours des propriétaires et l’aboutissement de projets de rénovation • Rapprocher les acteurs de l’énergie et de l’habitat • Sensibiliser les habitants à la maitrise de l’énergie • Prévenir et lutter contre la précarité énergétique • Accompagner les particuliers de manière indépendante • Faciliter la formation des professionnels du bâtiment et du secteur bancaire • Valoriser les actions et rénovations exemplaires • Faciliter l’accès aux aides et aux a…

#### Fiche 78910 — Fiche action 1.8 - Soutenir l’amélioration de l’habitat privé via une OPAH et Rénofuté

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [3, 6] | Changement chaudières gaz + rénovation (résidentiel) [3, 6] | Sobriété des bâtiments (résidentiel) [3, 6]
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [3, 4, 6] | Changement chaudières gaz + rénovation (résidentiel) [3, 4, 6] | Sobriété des bâtiments (résidentiel) [3, 4, 6]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [3, 6] | Changement chaudières gaz + rénovation (résidentiel) [3, 6] | Sobriété des bâtiments (résidentiel) [3, 6]
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [3, 6]
- Catégories instables sur : Changement chaudières fioul + rénovation (résidentiel), Changement chaudières gaz + rénovation (résidentiel), Sobriété des bâtiments (résidentiel)

> Lancée depuis 2016 avec Rénofuté, de nouvelles actions venant s’ajouter • Réalisation d’une OPAH : - Lutte contre l’insalubrité, le logement indigne et la précarité énergétique, - Adaptation des logements au maintien à domicile des personnes âgées et handicapées, - Accompagnement des copropriétés fragiles, - Développement du parc à vocation sociale, - Mobilisation du parc vacant pour les primo accédants • Soutien à la plateforme Rénofuté pour réaliser des rénovations énergétiques performantes -…

#### Fiche 78917 — Fiche action 2.4 - Promouvoir l’autoconsommation PVT via les sociétés citoyennes

- **Run 1 :** Electricité renouvelable [3, 6]
- **Run 2 :** Electricité renouvelable [3, 4, 6]
- **Run 3 :** Electricité renouvelable [3, 6]
- **Prod :** Electricité renouvelable [3, 6]
- Catégories instables sur : Electricité renouvelable

> Action nouvelle • Développer de petites installations de production dans les maisons individuelles • Accompagner les structures citoyennes locales pour permettre leur professionnalisation et garantir des projets exemplaires à coûts maitrisés • Favoriser l’autoconsommation • Etre complémentaire avec la subvention publique et l’expertise des sociétés locales • Permettre la réduction des factures et la lutte contre la précarité énergétique Éléments de calendrier : Année 1 et 2 : définition contrat…

#### Fiche 78918 — Fiche action 2.5 - Développer un cadastre éolien foncier public (+AMI) et un cadastre solaire au sol pour anciens sites industriels & carrières

- **Run 1 :** Electricité renouvelable [2, 4]
- **Run 2 :** Electricité renouvelable [1, 2]
- **Run 3 :** Electricité renouvelable [2, 4]
- **Prod :** Electricité renouvelable [2, 4]
- Catégories instables sur : Electricité renouvelable

> Action nouvelle • Identifier les potentiels éolien et solaire du territoire • Gérer le développement des EnR de façon coordonnée sur la CAPCA • Apporter un cadre et un accompagnement aux communes démunies et démarchées par les développeurs • Accompagner le co-développement citoyens/collectivités d’un parc éolien Éléments de calendrier : Année 1 et 2 : identification des sites et des porteurs de projet, lancement AMI et communiquer Années suivantes : lancement opérationnel des projets, suivi et …

#### Fiche 78919 — Fiche action 2.6 - Créer une structure juridique locale pour porter des investissements EnR

- **Run 1 :** Electricité renouvelable [3, 4]
- **Run 2 :** Electricité renouvelable [3, 4]
- **Run 3 :** Electricité renouvelable [4]
- **Prod :** Electricité renouvelable [4]
- Catégories instables sur : Electricité renouvelable

> Action nouvelle • Avoir un levier d’investissement public, intégrant des partenaires privés citoyens • Maîtriser la gouvernance de projets EnR (via les sociétés de projet) • Permettre au territoire de bénéficier des retombées du projet • Produire de l’énergie localement et réduire notre facture énergétique (autonomie énergétique) Éléments de calendrier : Année 1 : mobiliser les partenaires, connaitre les REX, définir le montage juridique Année 2 : lancer l’AMI et identifier les projets porteurs…

#### Fiche 78923 — Fiche action 3.4 - Mettre en place l’autostop organisé en milieu rural

- **Run 1 :** Covoiturage [1]
- **Run 2 :** Covoiturage [1, 6]
- **Run 3 :** Covoiturage [1, 6]
- **Prod :** Covoiturage [1, 4]
- Catégories instables sur : Covoiturage

> Nouvelle. • Sécuriser la pratique de stop en créant un réseau d'usagers • Matérialiser des arrêts pour sécuriser la prise ou de la dépose de l'autostoppeur. • Recréer du lien social en se rendant service • Apporter une réponse aux besoins de mobilité des habitants. • Appuyer sur un logiciel facilitant la mise en relation, créé en interne ou de faire appel à un opérateur privé Éléments de calendrier : Décembre 2019 : rencontre des communes et travail sur le choix des points d’arrêt 2020 : instal…

#### Fiche 78924 — Fiche action 3.5 - Mettre en place l’autopartage de véhicules électriques et de proximité

- **Run 1 :** Covoiturage [1] | Véhicules électriques [1]
- **Run 2 :** Covoiturage [1, 6] | Véhicules électriques [1, 6]
- **Run 3 :** Covoiturage [1] | Véhicules électriques [1]
- **Prod :** Véhicules électriques [4]
- Catégories instables sur : Covoiturage, Véhicules électriques

> Actions stratégie mobilités alternatives de l’Agglomération. Démarrage fin 2020 par l’audition de prestataires pour le partage de véhicules électriques • Proposer des véhicules en autopartage • Réduire l’utilisation du pétrole • Rationaliser les déplacements • Réduire la pollution (CO2) • Diminuer le nombre de véhicules en circulation • Recréer du lien social • Lutter contre l’isolement social et la précarité • Faciliter l’accès à une voiture à un coût raisonnable Éléments de calendrier : Choix…

#### Fiche 78926 — Fiche action 3.7 - Mettre en place en place un service de location de Vélos à Assistance Electrique

- **Run 1 :** Vélo et transport en commun [1, 3]
- **Run 2 :** Vélo et transport en commun [1, 3]
- **Run 3 :** Vélo et transport en commun [1]
- **Prod :** Vélo et transport en commun [1, 3]
- Catégories instables sur : Vélo et transport en commun

> Déjà engagée, renforcée par de nouvelles actions • Promouvoir les mobilités actives • Faciliter les déplacements pour les publics fragiles • Proposer une offre de mobilité complémentaire aux autres solutions : transports en commun, covoiturage Éléments de calendrier : 2017 : acquisition des premiers VAE sur Privas Depuis 2018 : renforcement progressif de la flotte de VAE et extension des possibilités de location sur l’ensemble du territoire 2021 : lancement des aides à l’acquisition de VAE

#### Fiche 78930 — Fiche action 3.11 - Développer l’accès des services intercommunaux au plus près des habitants – Point info Jeunes et MSAP itinérante

- **Run 1 :** Réduction des déplacements [6]
- **Run 2 :** Réduction des déplacements [1]
- **Run 3 :** Réduction des déplacements [6]
- **Prod :** Réduction des déplacements [4]
- Catégories instables sur : Réduction des déplacements

> Itinérance du point info jeunes de manière opérationnelle en février 2019 Mise en place d’une maison de services au public itinérante en mars 2019 • Aller à la rencontre des jeunes sur leurs lieux de vie • Réduire les freins à l’accès aux droits des jeunes : soucis de mobilité, fiabilité et actualisation des informations (formation, emploi, logement, santé, loisirs, culture, mobilité internationale, engagement…) • Rendre les jeunes acteurs de leur quotidien et de leur avenir (autonomie, engagem…

#### Fiche 78936 — Fiche action 4.3 - Développer la méthanisation agricole par injection dans le réseau

- **Run 1 :** Biogaz [1]
- **Run 2 :** Biogaz [4]
- **Run 3 :** Biogaz [1]
- **Prod :** Biogaz [1]
- Catégories instables sur : Biogaz

> Nouvelle action • Production d’énergie renouvelable et locale à partir des produits fermentescibles agricoles • Amélioration de l’autonomie financière des exploitations agricoles Éléments de calendrier : • 2021 : démarrage des études • 2022 : visite de site • Fin 2022 : montage du projet • 2023 : réunions de concertation et démarrage des travaux

#### Fiche 78949 — Fiche action 4.16 - Limiter l’artificialisation des sols

- **Run 1 :** Pratiques stockantes [2] | Sobriété foncière [2]
- **Run 2 :** Pratiques stockantes [1, 2] | Sobriété foncière [1, 2]
- **Run 3 :** Pratiques stockantes [1, 2] | Sobriété foncière [1, 2]
- **Prod :** Sobriété foncière [1, 2]
- Catégories instables sur : Pratiques stockantes, Sobriété foncière

> Nouvelle Eviter, réduire et compenser l’artificialisation des sols Désimperméabiliser les sols Augmenter le stockage carbone Réduire le risque d’inondation en favorisant l’infiltration Réduire l’effet îlot de chaleur (grâce à l’évapotranspiration du végétal, phénomène qui permet, par la perte d’eau, et par l’échange de chaleur entre l’eau et l’air, de rafraîchir l’air). Développement et intégration de la biodiversité en milieu urbain Éléments de calendrier : Etat des lieux (année 1) Ciblage des…

#### Fiche 82520 — B1 - Etudier l'opportunité de créer une aide publique pour permettre de sortir du bois en petite quantité

- **Run 1 :** Gestion des forêts et produits bois [4]
- **Run 2 :** Gestion des forêts et produits bois [4]
- **Run 3 :** Gestion des forêts et produits bois [3]
- **Prod :** (aucun levier)
- Catégories instables sur : Gestion des forêts et produits bois

## CC Ardennes Thiérache (3914)

- Fiches : **104** — stables sur les 3 runs : **56** (54%), instables : **48**
- Paires levier × catégorie distinctes proposées : 243 — 3/3 runs : 77, 2/3 runs : 59, 1/3 runs : 107
- Vote majoritaire = prod : 11/57 fiches classées d'un côté ou de l'autre
- Réponses JSON invalides rejouées : 0
- Appels : 15 — tokens d'entrée 51 441 (dont 0 en cache, 0%), sortie 84 333 — coût estimé 0.21 $ pour les 3 runs
- Date : 2026-10-30 15:07

### Classée dans certains runs, aucun levier dans d'autres (11)

#### Fiche 76378 — Renforcer le lien et la proximité des habitants à la nature et la biodiversité

- **Run 1 :** Pratiques stockantes [1, 6]
- **Run 2 :** (aucun levier)
- **Run 3 :** Pratiques stockantes [1, 6]
- **Prod :** (aucun levier)
- Leviers intermittents : Pratiques stockantes (2/3)

> <p><strong>Sensibilisation et information des publics Natura 2000</strong></p><p>•Conception, diffusion d’un bulletin d’information annuel (l’Arduinna)</p><p>•Conception, réalisation et pose de panneaux d'information</p><p>•Animations grand public (sorties nature, animations canoë, ciné-débats…) et scolaires</p><p>•Réédition de documents et outils pédagogiques (guides pédagogiques, jeu de 7 familles…)</p><p>•Outils de sensibilisation Quiétude attitude (banderoles de matérialisation des zones, a…

#### Fiche 76389 — Soutenir les projets citoyens et participatifs

- **Run 1 :** Electricité renouvelable [4, 6] | Réseaux de chaleur décarbonés [4, 6]
- **Run 2 :** (aucun levier)
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Electricité renouvelable (1/3), Réseaux de chaleur décarbonés (1/3)

> <p><em>La démarche PCAET portée nécessite d’être menée avec les différents acteurs (institutionnels, associatifs, économiques, …). Certains de ces partenaires et plusieurs citoyens se sont investis dans la phase d’élaboration du plan, en étant présents aux réunions de concertation. Néanmoins, la faible participation citoyenne constatée lors des réunions publiques montre une faible implication des habitants dans l’élaboration du PCAET. Forte de ce constat, les Communautés entendent renforcer l’a…

#### Fiche 76393 — Minimiser l'impact environnemental lié aux travaux de la collectivité

- **Run 1 :** (aucun levier)
- **Run 2 :** Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 3 :** Sobriété et isolation des bâtiments (tertiaire) [5]
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété et isolation des bâtiments (tertiaire) (2/3)

> <p><strong>Garantir que les bâtiments neufs soient performants énergétiquement</strong></p><p>-Réglementation RE2020</p><p>-Intégrer des critères sur la conception bioclimatique (en réflexion pour la construction de l'école à Maubert ?)</p><p><strong>Inclure dans les marchés publics des critères sur l'empreinte carbone des travaux</strong></p><p>-Privilégier des matériaux bio-sourcés (bois, chanvre, liège, paille, …)</p><p>-Faire appel à des artisans certifiés RGE</p><p><strong>A minima, demand…

#### Fiche 76549 — Mise en place d'une ORT

- **Run 1 :** Sobriété foncière [2]
- **Run 2 :** (aucun levier)
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété foncière (1/3)

#### Fiche 76578 — Etude pré opérationnelle OPAH

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6] | Sobriété des bâtiments (résidentiel) [6]
- **Run 2 :** (aucun levier)
- **Run 3 :** (aucun levier)
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [2] | Changement chaudières gaz + rénovation (résidentiel) [2]
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (1/3), Changement chaudières gaz + rénovation (résidentiel) (1/3), Sobriété des bâtiments (résidentiel) (1/3)

#### Fiche 76582 — Assainissement collectif Auvillers-Les-Forges / Eteignières

- **Run 1 :** (aucun levier)
- **Run 2 :** (aucun levier)
- **Run 3 :** Biogaz [1]
- **Prod :** (aucun levier)
- Leviers intermittents : Biogaz (1/3)

#### Fiche 76583 — Assainissement collectif Maubert-Fontaine

- **Run 1 :** (aucun levier)
- **Run 2 :** (aucun levier)
- **Run 3 :** Biogaz [1]
- **Prod :** (aucun levier)
- Leviers intermittents : Biogaz (1/3)

#### Fiche 76584 — Assainissement collectif Signy-le-Petit

- **Run 1 :** (aucun levier)
- **Run 2 :** (aucun levier)
- **Run 3 :** Biogaz [1]
- **Prod :** (aucun levier)
- Leviers intermittents : Biogaz (1/3)

#### Fiche 76591 — Etude en vue de la création d'une voie cyclable entre Hirson et Ham-les-Moines

- **Run 1 :** Vélo et transport en commun [6]
- **Run 2 :** (aucun levier)
- **Run 3 :** (aucun levier)
- **Prod :** Vélo et transport en commun [2]
- Leviers intermittents : Vélo et transport en commun (1/3)

#### Fiche 76592 — Création d'un schéma directeur cyclable

- **Run 1 :** Vélo et transport en commun [2]
- **Run 2 :** (aucun levier)
- **Run 3 :** Vélo et transport en commun [2]
- **Prod :** Vélo et transport en commun [2]
- Leviers intermittents : Vélo et transport en commun (2/3)

#### Fiche 76632 — Désimperméabilisation des cours d'école

- **Run 1 :** Pratiques stockantes [1]
- **Run 2 :** Pratiques stockantes [1]
- **Run 3 :** (aucun levier)
- **Prod :** Sobriété foncière [1]
- Leviers intermittents : Pratiques stockantes (2/3)

### Levier présent dans certains runs seulement (8)

#### Fiche 76362 — Mise en œuvre d'un observatoire sur le logement vacant

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [2, 4, 6] | Changement chaudières gaz + rénovation (résidentiel) [2, 4, 6] | Sobriété des bâtiments (résidentiel) [2, 4, 6]
- **Run 2 :** Sobriété foncière [2, 4, 6]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [2, 4, 6] | Changement chaudières gaz + rénovation (résidentiel) [2, 4, 6] | Sobriété des bâtiments (résidentiel) [2, 4, 6]
- **Prod :** (aucun levier)
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (2/3), Changement chaudières gaz + rénovation (résidentiel) (2/3), Sobriété des bâtiments (résidentiel) (2/3), Sobriété foncière (1/3)

> <p><strong>Diagnostic et recensement des logements vacants dans les 37 communes</strong></p><p>•Méthode : enquête auprès des propriétaires</p><p>•S'appuyer sur la connaissance du terrain par les Maires</p><p>•</p><p><strong>Réaliser un atlas de la vacance des logements</strong></p><p>•Prise de rendez-vous avec les propriétaires et orientation de ces derniers vers les dispositifs d’aides appropriés</p><p>•Mettre en place une opération programmée de l’amélioration de l’habitat avec des dispositif…

#### Fiche 76367 — Intégrer les enjeux climat-énergie-biodiversité dans les documents d’urbanisme

- **Run 1 :** Pratiques stockantes [1, 2] | Sobriété foncière [2]
- **Run 2 :** Sobriété foncière [2]
- **Run 3 :** Sobriété foncière [2]
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [2] | Changement chaudières gaz + rénovation (résidentiel) [2] | Réduction des déplacements [2] | Sobriété des bâtiments (résidentiel) [2] | Sobriété foncière [2] | Vélo et transport en commun [2]
- Leviers intermittents : Pratiques stockantes (1/3)

> <p>•<strong>Réaliser un guide de bonnes pratiques sur la façon d'intégrer les enjeux climat-énergie dans les documents d'urbanisme</strong></p><p>•Fourniture d’une note d'intégration des enjeux climat-énergie</p><p>•Etudier la conciliation entre architecture climatique et préservation du patrimoine, les solutions de végétalisation&nbsp; et de désimperméabilisation les plus vertueuses et les plus faciles à mettre en œuvre.</p><p>•<strong>Intégrer les enjeux du PCAET au Schéma de Cohérence Territ…

#### Fiche 76384 — Réduire les émissions de GES liées au centre de traitement des déchets

- **Run 1 :** Biogaz [1] | Captage de méthane dans les ISDND [1]
- **Run 2 :** Biogaz [1] | Captage de méthane dans les ISDND [1]
- **Run 3 :** Biogaz [1] | Captage de méthane dans les ISDND [1] | Electricité renouvelable [1]
- **Prod :** Biogaz [1, 3, 4] | Captage de méthane dans les ISDND [1, 3, 4]
- Leviers intermittents : Electricité renouvelable (1/3)

> <p><strong>IVEDA d'Eteignières</strong></p><p><strong>Valorisation énergétique du biogaz capté :</strong></p><p>•Production Electricité via deux moteurs de COGENERATION&nbsp;: Revente sur le marché libre</p><p>•Production de chaleur via &nbsp;deux moteurs de COGENERATION et utilisation de celle-ci ( Bassin biologique, Tour de désulfuration, Chauffage des serres)</p><p>•Améliorations techniques&nbsp;: Mise en place d’un système bioréacteur afin de maîtriser la fermentation des déchets et notamme…

#### Fiche 76387 — Soutenir les démarches vers l'agroécologie

- **Run 1 :** Changements de pratiques de fertilisation azotée [6] | Elevage durable [3, 6] | Gestion des prairies [6] | Pratiques stockantes [6]
- **Run 2 :** Elevage durable [3, 6]
- **Run 3 :** Elevage durable [3, 6]
- **Prod :** Changements de pratiques de fertilisation azotée [3, 6] | Elevage durable [3, 4, 6] | Pratiques stockantes [6]
- Leviers intermittents : Changements de pratiques de fertilisation azotée (1/3), Gestion des prairies (1/3), Pratiques stockantes (1/3)

> <p><strong>Action PNR </strong>:</p><p>•Réaliser des évènements (ciné débat/séminaire/visite...) incitant à réfléchir ensemble à travailler autrement, vers des pratiques agro-environnementales, élevage à l'herbe, autonomie alimentaire sur la ferme, adaptation au changement climatique, soin des animaux allopathiques...</p><p><strong>Actions CCAT</strong></p><p>•Apporter des conseils et des aides aux éleveurs qui s'engagent dans des démarches de réduction des émissions de GES de leur cheptel</p><…

#### Fiche 76395 — Réduire la production de déchets et optimiser leur collecte

- **Run 1 :** Prévention des déchets [5] | Valorisation matière des déchets [5]
- **Run 2 :** Prévention des déchets [5] | Valorisation matière des déchets [5]
- **Run 3 :** Covoiturage [5] | Réduction des déplacements [5] | Véhicules électriques [5] | Vélo et transport en commun [5]
- **Prod :** Covoiturage [4, 5] | Réduction des déplacements [4, 5] | Véhicules électriques [4, 5] | Vélo et transport en commun [1, 5]
- Leviers intermittents : Covoiturage (1/3), Prévention des déchets (2/3), Réduction des déplacements (1/3), Valorisation matière des déchets (2/3), Véhicules électriques (1/3), Vélo et transport en commun (1/3)

> <p>Optimiser la flotte de véhicules de la collectivité Prolonger la durée de vie des véhicules Interroger les besoins pour réduire au minimum la taille de la flotte nécessaire Lors de l'achat de véhicules, privilégier des véhicules électriques, d'occasion, de faible puissance</p><p>Mise en place d’une étude territoriale sur le verdissement de la flotte de véhicules des EPCI. Combien de véhicules électriques dans la flotte de la CCAT aujourd’hui ? 2 Quels objectifs ?</p><p>Mettre en place un Pla…

#### Fiche 76396 — Réduire l’impact environnemental lié au numérique

- **Run 1 :** Prévention des déchets [5] | Valorisation matière des déchets [5]
- **Run 2 :** Prévention des déchets [5]
- **Run 3 :** Prévention des déchets [5]
- **Prod :** (aucun levier)
- Leviers intermittents : Valorisation matière des déchets (1/3)

> <p><strong>Prolonger la durée de vie du parc informatique</strong></p><p>Charte d’utilisation / bonnes pratiques</p><p><strong>Mettre en place des critères exigeants sur la part de produits reconditionnés et/ou de seconde main dans les équipements informatiques et numériques</strong></p><p>-Définir des critères plus exigeants que la réglementation ?</p><p><strong>Donner une seconde vie au matériel et équipements informatiques obsolètes</strong></p><p>-Ordinateurs vieillissants donnés à Bell'Occ…

#### Fiche 76397 — Soutenir une alimentation locale et à faible empreinte carbone dans la restauration collective

- **Run 1 :** Prévention des déchets [5]
- **Run 2 :** Elevage durable [5] | Prévention des déchets [5]
- **Run 3 :** Elevage durable [5] | Prévention des déchets [5]
- **Prod :** Prévention des déchets [3, 5, 6]
- Leviers intermittents : Elevage durable (2/3)

> <p><strong>Mettre en place une cuisine centrale approvisionnée en circuit-court (PAT)</strong></p><p>-Projet validé, sera réalisé à Auvillers-les-Forges</p><p>-Fournir les établissements scolaires, les maisons de retraite, les personnes isolées (700 repas/jour)</p><p>-</p><p><strong>Mettre en place des critères sur l'empreinte carbone des repas servis dans la restauration collective</strong></p><p>-Compter et afficher systématique le "contenu carbone" des repas servis</p><p>-Réduire la quantité…

#### Fiche 76589 — Bornes de recharge VAE

- **Run 1 :** Vélo et transport en commun [1]
- **Run 2 :** Vélo et transport en commun [1]
- **Run 3 :** Véhicules électriques [1] | Vélo et transport en commun [1]
- **Prod :** Vélo et transport en commun [1]
- Leviers intermittents : Véhicules électriques (1/3)

### Levier intermittent et catégories instables (15)

#### Fiche 76370 — Etudier et soutenir le développement des filières locales hydrogène et bioGNV

- **Run 1 :** Biogaz [4] | Bus et cars décarbonés [4] | Fret décarboné et multimodalité [4] | Véhicules électriques [4]
- **Run 2 :** Biogaz [4] | Bus et cars décarbonés [4] | Fret décarboné et multimodalité [4]
- **Run 3 :** Biogaz [2, 4]
- **Prod :** Biogaz [2, 4] | Bus et cars décarbonés [4] | Fret décarboné et multimodalité [4]
- Leviers intermittents : Bus et cars décarbonés (2/3), Fret décarboné et multimodalité (2/3), Véhicules électriques (1/3)
- Catégories instables sur : Biogaz

> <p><strong>Hydrogène</strong></p><p>Le gisement de consommation actuel est insuffisant pour avoir une unité hydrogène sur le territoire</p><p>•Etudier les gisements de consommation possibles : demande industrielle, TER, etc.</p><p>•Etudier le potentiel de développement d’une filière hydrogène (partenaire : SEM EnR)</p><p>•Point de vigilance : veiller à un approvisionnement en hydrogène bas-carbone (hydrogène vert, jaune)</p><p>•</p><p><strong>Biogaz</strong></p><p>Une filière peut voir le jour …

#### Fiche 76371 — Soutenir le déploiement des véhicules électriques et des installations de recharge

- **Run 1 :** Véhicules électriques [1, 2]
- **Run 2 :** Véhicules électriques [1, 2, 4]
- **Run 3 :** Electricité renouvelable [1] | Véhicules électriques [1, 2, 3, 6]
- **Prod :** Véhicules électriques [2, 3, 4, 6]
- Leviers intermittents : Electricité renouvelable (1/3)
- Catégories instables sur : Véhicules électriques

> <p><em>En 2023, moins de 1% du parc automobile est électrifié sur le territoire d’Ardennes Thiérache. Le territoire ne dispose pas de bornes de recharge pour véhicules électriques</em></p><p>•Elaboration d’un Schéma Directeur IRVE à l’échelle départementale (SDIRVE)</p><p>•Evaluer les besoins en accès aux nouvelles énergies pour voitures (hydrogène, essences nouvelles, électricité etc.) ;</p><p>•Inciter les exploitants à installer et exploiter des bornes de recharge ;</p><p>•Informer les baille…

#### Fiche 76373 — Lutter contre l’autosolisme

- **Run 1 :** Covoiturage [1, 4]
- **Run 2 :** Covoiturage [1, 6]
- **Run 3 :** Covoiturage [1, 4] | Véhicules électriques [1]
- **Prod :** Covoiturage [1, 3, 4]
- Leviers intermittents : Véhicules électriques (1/3)
- Catégories instables sur : Covoiturage

> <p><strong>Mettre à disposition des véhicules électriques en autopartage</strong></p><p><strong>Création d’une aire de covoiture sur le territoire (mon Idée)</strong></p><p><strong>Créer une plateforme/un réseau de mise en relation des habitants qui souhaiteraient partager leur véhicule</strong></p><p><strong>Mettre en place une application de covoiturage à l'échelle de la CC</strong></p><p><em>Action engagée : mise en relation pour du covoiturage sur l'application de la CCAT (pas de paiement d…

#### Fiche 76374 — Mettre en place un service de transports à la demande

- **Run 1 :** Bus et cars décarbonés [1] | Véhicules électriques [1]
- **Run 2 :** Bus et cars décarbonés [1, 5] | Réduction des déplacements [1] | Véhicules électriques [1, 5]
- **Run 3 :** Bus et cars décarbonés [4]
- **Prod :** Véhicules électriques [1, 3] | Vélo et transport en commun [1, 3, 4]
- Leviers intermittents : Réduction des déplacements (1/3), Véhicules électriques (2/3)
- Catégories instables sur : Bus et cars décarbonés

> <p><strong>Mettre en place un service de Transports à la Demande</strong></p><p><strong>Action en réflexion avancée :</strong></p><p>-le service visera à apporter une solution de mobilités aux personnes en incapacité de se déplacer et/ou qui justifient d'un isolement. Les principales dessertes seront les services de santé, les marchés, les activités culturelles de proximité</p><p>-la CCAT est en train de déposer un dossier pour un minibus électrique</p><p>-réfléchir à ce qui peut être mutualisé…

#### Fiche 76375 — Renforcer l’attractivité et la qualité des services de transports en commun

- **Run 1 :** Bus et cars décarbonés [1, 4] | Vélo et transport en commun [4]
- **Run 2 :** Réduction des déplacements [4] | Vélo et transport en commun [1, 4]
- **Run 3 :** Vélo et transport en commun [1, 4]
- **Prod :** Vélo et transport en commun [1, 2, 4]
- Leviers intermittents : Bus et cars décarbonés (1/3), Réduction des déplacements (1/3)
- Catégories instables sur : Vélo et transport en commun

> <p><strong>1. Améliorer la desserte du territoire en transports en commun en ajoutant des arrêts sur les lignes traversant le territoire</strong></p><p>Un arrêt a été réalisé à Auvillers-les-Forges (hameau de Mon Idée) sur la ligne de bus Charleville - Hirson (gérée par la SNCF)</p><p><strong>2. Améliorer la flexibilité des bus qui traversent le territoire sans s'y arrêter.</strong></p><p>Un passager devrait pouvoir descendre du car/bus même en dehors des arrêts lorsque celui-ci est peu emprunt…

#### Fiche 76379 — Mettre en oeuvre une gestion durable et un plan de diversification de la ressource forestière

- **Run 1 :** Gestion des forêts et produits bois [4, 6]
- **Run 2 :** Gestion des forêts et produits bois [4] | Pratiques stockantes [4]
- **Run 3 :** Gestion des forêts et produits bois [2, 4, 6]
- **Prod :** Gestion des forêts et produits bois [4, 6]
- Leviers intermittents : Pratiques stockantes (1/3)
- Catégories instables sur : Gestion des forêts et produits bois

> <p><strong>Enjeu de diversifier les essences en parallèle du plan de gestion</strong></p><p>•Suivre et accompagner les actions de l’ONF en matière de gestion durable de la ressource forestière</p><p>•Renforcer la communication entre l’ONF et les collectivités</p><p>•Mettre en place, renforcer ou pérenniser des rencontres entre la CCAT, l’ONF, le PNR, et d’autres acteurs impliqués dans la gestion de la ressource forestière</p><p>•Travailler avec la Fédération de chasse pour réduire le déséquilib…

#### Fiche 76382 — Soutenir le développement des filières de l’économie circulaire

- **Run 1 :** Prévention des déchets [1, 4] | Valorisation matière des déchets [1, 4]
- **Run 2 :** Prévention des déchets [1, 4] | Valorisation matière des déchets [1, 4]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [2, 4, 6] | Changement chaudières gaz + rénovation (résidentiel) [2, 4, 6] | Covoiturage [1] | Prévention des déchets [4] | Réduction des déplacements [1, 4] | Sobriété des bâtiments (résidentiel) [2, 4, 6] | Valorisation matière des déchets [4] | Véhicules électriques [1] | Vélo et transport en commun [1]
- **Prod :** Covoiturage [1] | Prévention des déchets [2, 4] | Réduction des déplacements [1, 2, 4] | Véhicules électriques [1] | Vélo et transport en commun [1]
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (1/3), Changement chaudières gaz + rénovation (résidentiel) (1/3), Covoiturage (1/3), Réduction des déplacements (1/3), Sobriété des bâtiments (résidentiel) (1/3), Véhicules électriques (1/3), Vélo et transport en commun (1/3)
- Catégories instables sur : Prévention des déchets, Valorisation matière des déchets

> <p><strong>Mettre en place des projets de revitalisation dans le cadre des ORT (5 communes) et du dispositif Petites Villes de Demain (Signy-le-Petit)</strong></p><p>Exemples d'actions</p><p>-Fédérer les commerçants</p><p>-Développer des cafés multiservices</p><p>-Mettre en place des IRVE, des stationnements vélos, des aires de covoiturage,</p><p>-Maintenir le commerce existant</p><p>-Vitrophanie</p><p>-Lutter contre le logement vacant</p><p>-OPAH</p><p>-THLV</p><p>-Rénovation du bâti ancien</p…

#### Fiche 76383 — Revitaliser les centres de villages et développer des services de proximité

- **Run 1 :** Prévention des déchets [1, 4] | Valorisation matière des déchets [1, 4]
- **Run 2 :** Prévention des déchets [1, 4] | Valorisation matière des déchets [1, 4]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [2, 4, 6] | Changement chaudières gaz + rénovation (résidentiel) [2, 4, 6] | Covoiturage [1] | Prévention des déchets [4] | Réduction des déplacements [1, 4] | Sobriété des bâtiments (résidentiel) [2, 4, 6] | Valorisation matière des déchets [4] | Véhicules électriques [1] | Vélo et transport en commun [1]
- **Prod :** Réduction des déplacements [1, 2]
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (1/3), Changement chaudières gaz + rénovation (résidentiel) (1/3), Covoiturage (1/3), Réduction des déplacements (1/3), Sobriété des bâtiments (résidentiel) (1/3), Véhicules électriques (1/3), Vélo et transport en commun (1/3)
- Catégories instables sur : Prévention des déchets, Valorisation matière des déchets

> <p><strong>Mettre en place des projets de revitalisation dans le cadre des ORT (5 communes) et du dispositif Petites Villes de Demain (Signy-le-Petit)</strong></p><p>Exemples d'actions</p><p>-Fédérer les commerçants</p><p>-Développer des cafés multiservices</p><p>-Mettre en place des IRVE, des stationnements vélos, des aires de covoiturage,</p><p>-Maintenir le commerce existant</p><p>-Vitrophanie</p><p>-Lutter contre le logement vacant</p><p>-OPAH</p><p>-THLV</p><p>-Rénovation du bâti ancien</p…

#### Fiche 76385 — Relocaliser la production alimentaire et soutenir les circuits courts

- **Run 1 :** Efficacité et sobriété logistique [4, 6] | Elevage durable [4, 6] | Pratiques stockantes [4, 6]
- **Run 2 :** Efficacité et sobriété logistique [4, 6] | Elevage durable [4, 6]
- **Run 3 :** Efficacité et sobriété logistique [4] | Elevage durable [4, 6] | Réduction des déplacements [4, 6]
- **Prod :** (aucun levier)
- Leviers intermittents : Pratiques stockantes (1/3), Réduction des déplacements (1/3)
- Catégories instables sur : Efficacité et sobriété logistique

> <p><strong>Actions PNR </strong>:</p><p>•Analyse et étude de la logistique des produits locaux entre producteurs, professionnels, restauration collective, commerces/points de vente... et éventuellement structure d'aides alimentaires en vue de la création d'un outils numérique et/ou d'investissement sur le territoire</p><p>•Formation auprès des producteurs sur la détermination des prix de vente</p><p>•Outils de sensibilisation et de communication autour des produits locaux (affiches explicatives…

#### Fiche 76386 — Renforcer le lien entre les producteurs, les transformateurs, les distributeurs

- **Run 1 :** Efficacité et sobriété logistique [1, 4] | Prévention des déchets [1, 4]
- **Run 2 :** Efficacité et sobriété logistique [4, 6] | Prévention des déchets [4]
- **Run 3 :** Efficacité et sobriété logistique [1, 4] | Prévention des déchets [4] | Réduction des déplacements [4]
- **Prod :** (aucun levier)
- Leviers intermittents : Réduction des déplacements (1/3)
- Catégories instables sur : Efficacité et sobriété logistique, Prévention des déchets

> <p>•Mutualiser des installations qui pourraient bénéficier à plusieurs acteurs (exemple : Albatros 08 possèdent un autoclave qui permet de valoriser les invendus des maraîchers)</p><p>•</p><p><strong>Association L’Environnement D’Abord (LEDA)</strong></p><p>•Agrandir le réseau des producteurs impliqués, devenir la structure coordinatrice de la distribution en circuit court sur le territoire</p><p>•Chambre d’Agriculture : les accompagner et les aider à associer le plus possible de producteurs lo…

#### Fiche 76392 — Être exemplaire dans la gestion de l'énergie des bâtiments de la collectivité

- **Run 1 :** Changement de chaudière à fioul (tertiaire) [5] | Changement de chaudière à gaz (tertiaire) [5] | Réseaux de chaleur décarbonés [5] | Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 2 :** Changement de chaudière à fioul (tertiaire) [5] | Changement de chaudière à gaz (tertiaire) [5] | Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 3 :** Changement de chaudière à fioul (tertiaire) [5] | Changement de chaudière à gaz (tertiaire) [5] | Réseaux de chaleur décarbonés [5] | Sobriété et isolation des bâtiments (tertiaire) [5, 6]
- **Prod :** Changement de chaudière à fioul (tertiaire) [3, 5] | Changement de chaudière à gaz (tertiaire) [3, 5] | Sobriété et isolation des bâtiments (tertiaire) [5, 6]
- Leviers intermittents : Réseaux de chaleur décarbonés (2/3)
- Catégories instables sur : Sobriété et isolation des bâtiments (tertiaire)

> <p>Pistes de travail :</p><p>-Ne plus avoir de bâtiments ou de pièces surchauffés</p><p>-En cours dans les bâtiments scolaires et les COSEC</p><p>-Installer des robinets thermostatique (dispositif CEE, financé)</p><p>-Fournir aux agents des vestes pour permettre de baisser la température de consigne dans les bâtiments (fait)</p><p>-Remplacer les systèmes de chauffage gaz/fioul des bâtiments les plus énergivores</p><p>-Installer des chauffages mutualisés sur plusieurs équipements, alimentés par …

#### Fiche 76419 — Développer de nouvelles filières agricoles locales

- **Run 1 :** Changements de pratiques de fertilisation azotée [6] | Elevage durable [4, 6] | Gestion des prairies [6] | Pratiques stockantes [6]
- **Run 2 :** Elevage durable [4, 6] | Gestion des prairies [4, 6]
- **Run 3 :** Gestion des prairies [3, 6] | Pratiques stockantes [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Changements de pratiques de fertilisation azotée (1/3), Elevage durable (2/3), Pratiques stockantes (2/3)
- Catégories instables sur : Gestion des prairies

> <p><strong>Actions PNR </strong>:</p><p>•Initier la réflexion pour le développement de production de fruits et légumes sur le territoire (analyse des producteurs existants, étude sur le foncier (enquêtes auprès des communes/EPCI/SAFER/Terres de lien…), les outils de transformation et les points de vente)</p><p>•Identifier une/des filières prioritaires et mettre en place un programme de développement de cette/ces filières (AMI filière ? Lait de pâturage ?) - 2e session ?</p><p><strong>Actions CC…

#### Fiche 76575 — Mise en place du tri des biodéchets

- **Run 1 :** Valorisation matière des déchets [1]
- **Run 2 :** Prévention des déchets [1] | Valorisation matière des déchets [1]
- **Run 3 :** Prévention des déchets [2, 6] | Valorisation matière des déchets [2, 6]
- **Prod :** Valorisation matière des déchets [1]
- Leviers intermittents : Prévention des déchets (2/3)
- Catégories instables sur : Valorisation matière des déchets

#### Fiche 76580 — Création d'une objeterie

- **Run 1 :** Prévention des déchets [1] | Valorisation matière des déchets [1]
- **Run 2 :** Prévention des déchets [1, 6]
- **Run 3 :** Prévention des déchets [1] | Valorisation matière des déchets [1]
- **Prod :** Prévention des déchets [1]
- Leviers intermittents : Valorisation matière des déchets (2/3)
- Catégories instables sur : Prévention des déchets

#### Fiche 76629 — Travail sur les logements vacants et indignes

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6] | Sobriété des bâtiments (résidentiel) [6]
- **Run 2 :** Sobriété des bâtiments (résidentiel) [2, 6]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [3] | Changement chaudières gaz + rénovation (résidentiel) [3] | Sobriété des bâtiments (résidentiel) [3]
- **Prod :** (aucun levier)
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (2/3), Changement chaudières gaz + rénovation (résidentiel) (2/3)
- Catégories instables sur : Sobriété des bâtiments (résidentiel)

### Mêmes leviers, catégories différentes (14)

#### Fiche 76364 — Etudier la mise en place d'un Permis de louer

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [2] | Changement chaudières gaz + rénovation (résidentiel) [2] | Sobriété des bâtiments (résidentiel) [2]
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [2] | Changement chaudières gaz + rénovation (résidentiel) [2] | Sobriété des bâtiments (résidentiel) [2]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [2, 6] | Changement chaudières gaz + rénovation (résidentiel) [2, 6] | Sobriété des bâtiments (résidentiel) [2, 6]
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [2, 6] | Changement chaudières gaz + rénovation (résidentiel) [2, 6]
- Catégories instables sur : Changement chaudières fioul + rénovation (résidentiel), Changement chaudières gaz + rénovation (résidentiel), Sobriété des bâtiments (résidentiel)

> <p><strong><em>Le permis de louer visera notamment à contraindre les bailleurs privés à rénover leurs biens.</em></strong></p><p><strong>Etape 0 : Communiquer auprès des propriétaires bailleurs </strong>l'interdiction<strong> </strong>à venir de la mise en location des passoires thermiques (G en 2025, F en 2028) pour les inciter à les rénover</p><p><strong>Etape 1: mise en place d’un Label Qualité Logement à l’échelle EPCI</strong></p><p>La CCAT souhaite mettre en place un LQL dans le cadre de …

#### Fiche 76365 — Mettre en place une Opération Programmée d’Amélioration de l’Habitat (OPAH)

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [3, 6] | Changement chaudières gaz + rénovation (résidentiel) [3, 6] | Sobriété des bâtiments (résidentiel) [3, 6]
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6] | Sobriété des bâtiments (résidentiel) [6]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [2, 3, 6] | Changement chaudières gaz + rénovation (résidentiel) [2, 3, 6] | Sobriété des bâtiments (résidentiel) [2, 3, 6]
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [3, 4, 6] | Changement chaudières gaz + rénovation (résidentiel) [3, 4, 6]
- Catégories instables sur : Changement chaudières fioul + rénovation (résidentiel), Changement chaudières gaz + rénovation (résidentiel), Sobriété des bâtiments (résidentiel)

> <p><strong>Opération Programmée d’Amélioration de l’Habitat </strong>dont l’animation est confiée au PNR des Ardennes. La démarche s’inscrit dans la continuité du PIG «&nbsp;Habiter mieux en Ardennes&nbsp;» ayant pris fin en 2022</p><p>•Accompagner les ménages dans leurs projets de rénovation (énergétique, accessibilité et décence) en lien avec les aides de l’ANAH</p><p>•Les aides volontaires : les EPCI ont la possibilité de compléter leurs interventions d’aides volontaires : façade, toiture, l…

#### Fiche 76366 — Poursuivre l’accompagnement France Rénov’ auprès des particuliers / OKTAVE

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [4, 6] | Changement chaudières gaz + rénovation (résidentiel) [4, 6] | Sobriété des bâtiments (résidentiel) [4, 6]
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6] | Sobriété des bâtiments (résidentiel) [6]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [4, 6] | Changement chaudières gaz + rénovation (résidentiel) [4, 6] | Sobriété des bâtiments (résidentiel) [4, 6]
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [4, 6] | Changement chaudières gaz + rénovation (résidentiel) [4, 6] | Sobriété des bâtiments (résidentiel) [6]
- Catégories instables sur : Changement chaudières fioul + rénovation (résidentiel), Changement chaudières gaz + rénovation (résidentiel), Sobriété des bâtiments (résidentiel)

> <p><strong>Espace France Rénov’ </strong>: <em>les Communautés de communes,&nbsp;&nbsp;Ardennes Thiérache&nbsp;Ardenne Rives de Meuse et&nbsp;Vallées et plateau d’Ardenne&nbsp;ont décidé de mutualiser leur action et de simplifier le parcours de rénovation énergétique des ménages. Pour cela, elles ont confié l’animation du SARE (service d’accompagnement à la rénovation énergétique) au Parc Naturel Régional des Ardennes.</em></p><p>•Assurer des permanences sur le territoire</p><p>•Accompagner les…

#### Fiche 76372 — Soutenir le développement des mobilités actives

- **Run 1 :** Vélo et transport en commun [1, 3, 6]
- **Run 2 :** Vélo et transport en commun [1, 3, 6]
- **Run 3 :** Vélo et transport en commun [1, 2, 6]
- **Prod :** Véhicules électriques [1, 6] | Vélo et transport en commun [1, 2, 6]
- Catégories instables sur : Vélo et transport en commun

> <p><strong>Mettre en place un Schéma Directeur Cyclable à l'échelle de la CCAT</strong></p><p><em>Action engagée dans le cadre de l'Appel à Projet AVELO2 : la CCAT est lauréate</em></p><p>Travailler en particulier :</p><p>-au raccordement à la voie verte départementale (Eurovéloroute 19) à Hirson (Eurovéloroute 3) (doit constituer l'axe dorsal du réseau cyclable du territoire)</p><p>-à la desserte des écoles, services publics, médecins, commerces, pharmacies, etc.</p><p>-à la reconversion de la…

#### Fiche 76376 — Réduire les besoins de déplacements en développant des services de proximité

- **Run 1 :** Réduction des déplacements [1, 4, 6]
- **Run 2 :** Réduction des déplacements [1, 6]
- **Run 3 :** Réduction des déplacements [1, 4]
- **Prod :** Réduction des déplacements [1, 4]
- Catégories instables sur : Réduction des déplacements

> <p><em>Avoir accès à plus de services de proximité permet de réduire les déplacements des habitants du territoire et ainsi de réduire la consommation d’énergie et les émissions de gaz à effet de serre associées.</em></p><p><strong>Mesures initiées et perspectives :</strong></p><p>•Développer des services en ligne pour les habitants liés aux compétences (urbanisme, eau-assainissement, etc.…)</p><p>•Aménager une nouvelle Maison France Service en lien avec les services de la Communauté de Communes…

#### Fiche 76388 — Structurer une filière de valorisation du bois

- **Run 1 :** Gestion des forêts et produits bois [1, 3, 4]
- **Run 2 :** Gestion des forêts et produits bois [1, 3, 4]
- **Run 3 :** Gestion des forêts et produits bois [3, 4]
- **Prod :** Gestion des forêts et produits bois [1, 3, 4]
- Catégories instables sur : Gestion des forêts et produits bois

> <p><em>Dans les 6 prochaines années, des volumes très importants seront à traiter sachant que la forêt ne pourra produire davantage notamment avec le changement climatique au-delà de 10 - 20 ans.</em></p><p>•Relocaliser la filière via contrats d’approvisionnement avec l’ONF</p><p>•Soutenir l’installation d’ETF (Entreprises de Travaux Forestiers) sur le territoire pour répondre au besoin de main d’œuvre de l’ONF (si ces entreprises sont prêtes à s’installer, l’ONF peut leur garantir de l’activit…

#### Fiche 76390 — Développer une centrale photovoltaïque

- **Run 1 :** Electricité renouvelable [1, 4]
- **Run 2 :** Electricité renouvelable [1]
- **Run 3 :** Electricité renouvelable [1, 4]
- **Prod :** Electricité renouvelable [1, 4]
- Catégories instables sur : Electricité renouvelable

> <p><em>Le Département des Ardennes équipe le site de l‘ancienne base de OTAN à Regniowez avec une centrale photovoltaïque au sol (28,6 MWc, 23 ha de pistes).</em></p><p><em>L'entreprise CVE Groupe a été retenue suite à un appel à projets en 2020 pour une durée de 40 ans.</em></p><p><strong>Intégration de critères environnementaux et sociaux :</strong></p><p>•Pas de changement de nature de sol (uniquement sur les pistes),</p><p>•Gestion des zones naturelle sera confiée au Conservatoire d'espaces…

#### Fiche 76391 — Accompagner les communes et la CCAT sur le développement des EnR (évaluation d’opportunités sur leur patrimoine et évaluation des projets photovoltaïques portés par des développeurs privés )

- **Run 1 :** Electricité renouvelable [4, 6] | Réseaux de chaleur décarbonés [4, 6]
- **Run 2 :** Electricité renouvelable [6] | Réseaux de chaleur décarbonés [6]
- **Run 3 :** Electricité renouvelable [4, 6] | Réseaux de chaleur décarbonés [4, 6]
- **Prod :** Electricité renouvelable [4, 6]
- Catégories instables sur : Electricité renouvelable, Réseaux de chaleur décarbonés

> <p><strong>Hypothèse 1 : Création d’une structure intercommunale participative pour la mise en œuvre d’un réseau de chaleur sur la commune de Maubert Fontaine</strong></p><p><strong>Hypothèse 2 : Travailler avec l’ALE 08 à travers le dispositif Générateurs (solaire photovoltaïque) :</strong></p><p>L'ALE 08 fait partie du dispositif Les GÉnÉRATEURS :</p><p>Ce dispositif co-finance des acteurs qui peuvent intervenir auprès des communes dès l’émergence d’un projet photovoltaïque, que la commune so…

#### Fiche 76564 — Réaménagement des Broises Basses en gîte de groupe

- **Run 1 :** Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 2 :** Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 3 :** Sobriété et isolation des bâtiments (tertiaire) [1]
- **Prod :** (aucun levier)
- Catégories instables sur : Sobriété et isolation des bâtiments (tertiaire)

#### Fiche 76565 — Réaménagement des Broises Basses en Brasserie

- **Run 1 :** Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 2 :** Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 3 :** Sobriété et isolation des bâtiments (tertiaire) [1]
- **Prod :** (aucun levier)
- Catégories instables sur : Sobriété et isolation des bâtiments (tertiaire)

#### Fiche 76566 — Réaménagement des Broises-Basses en salle de spectacle

- **Run 1 :** Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 2 :** Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 3 :** Sobriété et isolation des bâtiments (tertiaire) [1]
- **Prod :** (aucun levier)
- Catégories instables sur : Sobriété et isolation des bâtiments (tertiaire)

#### Fiche 76576 — Création d'un cadastre solaire

- **Run 1 :** Electricité renouvelable [6]
- **Run 2 :** Electricité renouvelable [2, 6]
- **Run 3 :** Electricité renouvelable [6]
- **Prod :** Electricité renouvelable [2]
- Catégories instables sur : Electricité renouvelable

#### Fiche 76577 — PIG

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6] | Sobriété des bâtiments (résidentiel) [6]
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [3, 6] | Changement chaudières gaz + rénovation (résidentiel) [3, 6] | Sobriété des bâtiments (résidentiel) [3, 6]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [3] | Changement chaudières gaz + rénovation (résidentiel) [3] | Sobriété des bâtiments (résidentiel) [3]
- **Prod :** (aucun levier)
- Catégories instables sur : Changement chaudières fioul + rénovation (résidentiel), Changement chaudières gaz + rénovation (résidentiel), Sobriété des bâtiments (résidentiel)

#### Fiche 76594 — Création et mise en place de l'application de co-voiturage

- **Run 1 :** Covoiturage [6]
- **Run 2 :** Covoiturage [1, 6]
- **Run 3 :** Covoiturage [6]
- **Prod :** Covoiturage [4, 6]
- Catégories instables sur : Covoiturage

## CA Rochefort Océan (4026)

- Fiches : **75** — stables sur les 3 runs : **50** (67%), instables : **25**
- Paires levier × catégorie distinctes proposées : 103 — 3/3 runs : 45, 2/3 runs : 24, 1/3 runs : 34
- Vote majoritaire = prod : 24/52 fiches classées d'un côté ou de l'autre
- Réponses JSON invalides rejouées : 0
- Appels : 9 — tokens d'entrée 29 481 (dont 0 en cache, 0%), sortie 57 819 — coût estimé 0.14 $ pour les 3 runs
- Date : 2026-10-30 15:07

### Classée dans certains runs, aucun levier dans d'autres (8)

#### Fiche 87215 — Action 1 - Piloter et animer le PLPDMA pour prioriser les actions

- **Run 1 :** (aucun levier)
- **Run 2 :** Prévention des déchets [4]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Prévention des déchets (1/3)

> Gouvernance : Mobiliser les élus du territoire Assurer un pilotage politique de la démarche Assurer la cohérence de la politique de transition écologique de la collectivité et renforcer la transversalité de la démarche Associer les agents et acteurs mobilisés dans la mise en œuvre à la gouvernance Garantir l’évolutivité du programme en fonction des réalités pratiques et des opportunités Pilotage : Assurer la mise en œuvre et le suivi opérationnel du projet Garantir un suivi effectif des actions…

#### Fiche 87226 — Action 12 - Promouvoir les produits et acteurs locaux

- **Run 1 :** (aucun levier)
- **Run 2 :** Efficacité et sobriété logistique [6]
- **Run 3 :** Efficacité et sobriété logistique [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Efficacité et sobriété logistique (2/3)

> Encourager à la consommation de produits locaux à travers des ateliers cuisine

#### Fiche 87251 — Action 37 - Etudier l'opportunité d’une part plus incitative dans la tarification

- **Run 1 :** (aucun levier)
- **Run 2 :** Prévention des déchets [3, 4]
- **Run 3 :** Prévention des déchets [3]
- **Prod :** (aucun levier)
- Leviers intermittents : Prévention des déchets (2/3)

> Les contributions reçues lors de la mise en consultation du PLPDMA ont montré une attention des habitants à la tarification incitative, et des avis divergents. Il apparaît important de mener sur ce sujet une réflexion partagée.

#### Fiche 87252 — Action 1 - Renforcer la signalétique envers de nouvelles exploitations pour développer les circuits courts

- **Run 1 :** (aucun levier)
- **Run 2 :** Efficacité et sobriété logistique [1]
- **Run 3 :** Réduction des déplacements [1]
- **Prod :** (aucun levier)
- Leviers intermittents : Efficacité et sobriété logistique (1/3), Réduction des déplacements (1/3)

> Flécher de nouvelles exploitations pour les mettre en lumière

#### Fiche 87253 — Action 2 - Animer le PAT et mobiliser l’ensemble des acteurs

- **Run 1 :** (aucun levier)
- **Run 2 :** Efficacité et sobriété logistique [4]
- **Run 3 :** Réduction des déplacements [4]
- **Prod :** (aucun levier)
- Leviers intermittents : Efficacité et sobriété logistique (1/3), Réduction des déplacements (1/3)

> Animation de temps d'échanges et de rencontres pour créer du lien et mobiliser les acteurs locaux

#### Fiche 87255 — Action 4 - Faciliter et aider à l'installation de nouvelles exploitations pour augmenter l'autonomie alimentaire du territoire

- **Run 1 :** (aucun levier)
- **Run 2 :** Efficacité et sobriété logistique [6]
- **Run 3 :** Réduction des déplacements [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Efficacité et sobriété logistique (1/3), Réduction des déplacements (1/3)

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="5b1dc081-608a-4d60-8226-581a498e5482"><div class="bn-block" data-node-type="blockContainer" data-id="5b1dc081-608a-4d60-8226-581a498e5482"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]">Faciliter et aider à l'installation de nouvelles exploitations pour augmenter l'autonomie alimentaire du…

#### Fiche 87264 — Action 13 - Définir une stratégie de rénovation des bâtiments à long terme

- **Run 1 :** Changement de chaudière à fioul (tertiaire) [2, 5] | Changement de chaudière à gaz (tertiaire) [2, 5] | Sobriété et isolation des bâtiments (tertiaire) [2, 5]
- **Run 2 :** Changement de chaudière à fioul (tertiaire) [2, 5] | Changement de chaudière à gaz (tertiaire) [2, 5] | Sobriété et isolation des bâtiments (tertiaire) [2, 5]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Changement de chaudière à fioul (tertiaire) (2/3), Changement de chaudière à gaz (tertiaire) (2/3), Sobriété et isolation des bâtiments (tertiaire) (2/3)

> Définir le schéma directeur immobilier énergétique

#### Fiche 128297 — Logistique urbaine

- **Run 1 :** (aucun levier)
- **Run 2 :** (aucun levier)
- **Run 3 :** Efficacité et sobriété logistique [1] | Fret décarboné et multimodalité [1]
- **Prod :** (aucun levier)
- Leviers intermittents : Efficacité et sobriété logistique (1/3), Fret décarboné et multimodalité (1/3)

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="df3bb99d-b8f0-468e-b379-e22fb6fa8cf2"><div class="bn-block" data-node-type="blockContainer" data-id="df3bb99d-b8f0-468e-b379-e22fb6fa8cf2"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]">Logistique urbain</p></div></div></div></div>

### Levier présent dans certains runs seulement (7)

#### Fiche 87219 — Action 5 - Faire des visites apprenantes et des journées d'échanges

- **Run 1 :** Prévention des déchets [6]
- **Run 2 :** Prévention des déchets [6] | Valorisation matière des déchets [6]
- **Run 3 :** Prévention des déchets [6]
- **Prod :** Prévention des déchets [6]
- Leviers intermittents : Valorisation matière des déchets (1/3)

> Poursuivre Novembre vert Créer un groupe de travail permettant d’identifier les évènements auxquels il sera pertinent d’être présent, avec l’aide du service Culture et du service des Sports, de l’Office de Tourisme, des communes, d’identifier d’autres évènements, de définir les besoins matériels et la communication associée Relayer les visites du Centre Multifilières de Valorisation des Déchets et proposer ces visites aux écoles du territoire. Etre innovant et aller chercher tous les publics.

#### Fiche 87237 — Action 23 - Déployer et valoriser les pratiques de prêts et dons en interne

- **Run 1 :** Prévention des déchets [5]
- **Run 2 :** Valorisation matière des déchets [5]
- **Run 3 :** Prévention des déchets [5]
- **Prod :** (aucun levier)
- Leviers intermittents : Prévention des déchets (2/3), Valorisation matière des déchets (1/3)

> Favoriser le don aux associations, favoriser le recours aux matériaux de réemploi.

#### Fiche 87238 — Action 24 - Définir et mettre en place une stratégie numérique, notamment autour du réemploi du matériel informatique

- **Run 1 :** Prévention des déchets [5]
- **Run 2 :** Valorisation matière des déchets [5]
- **Run 3 :** Prévention des déchets [5]
- **Prod :** (aucun levier)
- Leviers intermittents : Prévention des déchets (2/3), Valorisation matière des déchets (1/3)

> Prolonger la durée de vie des équipements, favoriser le réemploi des terminaux et matériels informatiques.

#### Fiche 87248 — Action 34 - Créer de zones de réemploi en déchèterie et former des agents valoristes

- **Run 1 :** Prévention des déchets [1, 5, 6] | Valorisation matière des déchets [1, 5, 6]
- **Run 2 :** Prévention des déchets [1, 4, 5, 6]
- **Run 3 :** Valorisation matière des déchets [1, 5]
- **Prod :** Valorisation matière des déchets [1, 5]
- Leviers intermittents : Prévention des déchets (2/3), Valorisation matière des déchets (2/3)

> Mettre en place des espaces dédiés au réemploi en déchèterie Valoriser la pratique du réemploi par les agents de déchèterie Communiquer sur la pratique de réemploi en déchèterie Développer des partenariats pour augmenter le réemploi sur le territoire à partir des dons récupérés en déchèterie Proposer des alternatives pour réduire les déchets en déchèterie.

#### Fiche 87254 — Action 3 - Travailler à la logistique de l’approvisionnement local

- **Run 1 :** Fret décarboné et multimodalité [1, 4]
- **Run 2 :** Efficacité et sobriété logistique [1]
- **Run 3 :** Efficacité et sobriété logistique [1, 4]
- **Prod :** (aucun levier)
- Leviers intermittents : Efficacité et sobriété logistique (2/3), Fret décarboné et multimodalité (1/3)

> Création d'une plateforme de distribution de produits locaux pour la restauration (dont scolaire)

#### Fiche 87276 — Action 25 - Adopter un PLPDMA avec un volet ECi

- **Run 1 :** Prévention des déchets [2] | Valorisation matière des déchets [2]
- **Run 2 :** Prévention des déchets [2] | Valorisation matière des déchets [2]
- **Run 3 :** Prévention des déchets [2]
- **Prod :** Prévention des déchets [2]
- Leviers intermittents : Valorisation matière des déchets (2/3)

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="080b4533-b890-4298-8999-37275157cff7"><div class="bn-block" data-node-type="blockContainer" data-id="080b4533-b890-4298-8999-37275157cff7"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]">Définir un plan d'action et une stratégie sur la réduction des DMA, avec un vision ECi. Il fera partie d…

#### Fiche 87280 — Action 29 - Consolider la démarche ECi en direction du grand public et des associations du territoire notamment via Novembre Vert

- **Run 1 :** Prévention des déchets [6]
- **Run 2 :** Prévention des déchets [6] | Valorisation matière des déchets [6]
- **Run 3 :** Prévention des déchets [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Valorisation matière des déchets (1/3)

> Poursuite de l'action Novembre Vert et la décliner toute l'année.

### Levier intermittent et catégories instables (2)

#### Fiche 87246 — Action 32 - Faciliter la gestion de proximité des déchets verts

- **Run 1 :** Prévention des déchets [1, 6] | Valorisation matière des déchets [1]
- **Run 2 :** Prévention des déchets [6]
- **Run 3 :** Prévention des déchets [6]
- **Prod :** Prévention des déchets [6]
- Leviers intermittents : Valorisation matière des déchets (1/3)
- Catégories instables sur : Prévention des déchets

> Réduction des apports de déchets verts en déchèterie Réduction des apports de déchets verts au SIL Convaincre les usagers de changer leurs pratiques de gestion des déchets verts

#### Fiche 87250 — Action 36 - Réduire le nombre de passages en déchèterie

- **Run 1 :** Prévention des déchets [6] | Réduction des déplacements [6]
- **Run 2 :** Prévention des déchets [1, 4, 5, 6]
- **Run 3 :** Prévention des déchets [6]
- **Prod :** Prévention des déchets [1, 4, 6]
- Leviers intermittents : Réduction des déplacements (1/3)
- Catégories instables sur : Prévention des déchets

> Mettre en place des espaces dédiés au réemploi en déchèterie Valoriser la pratique du réemploi par les agents de déchèterie Communiquer sur la pratique de réemploi en déchèterie Développer des partenariats pour augmenter le réemploi sur le territoire à partir des dons récupérés en déchèterie Proposer des alternatives pour réduire les déchets en déchèterie.

### Mêmes leviers, catégories différentes (8)

#### Fiche 87222 — Action 8 - Accompagner la mise en œuvre de matériauthèques thématiques (culture, pro…)

- **Run 1 :** Valorisation matière des déchets [1]
- **Run 2 :** Valorisation matière des déchets [1, 6]
- **Run 3 :** Valorisation matière des déchets [1]
- **Prod :** Prévention des déchets [1]
- Catégories instables sur : Valorisation matière des déchets

> Détourner plus d’objets des bennes de déchèteries. Faire changer les modes de consommation. Mettre en avant la seconde vie des objets et matières par la réutilisation et la réparation. Développer une recyclerie vitrine du réemploi sur le territoire, qui soit complémentaire des solutions déjà existantes. Innover en impulsant la création de recycleries-matériauthèques spécialisées (culturelles, sportives, etc.). L’objectif est de détourner 400 tonnes de déchets par an à terme

#### Fiche 87223 — Action 9 - Créer un forum du réemploi pour particuliers et entreprises

- **Run 1 :** Valorisation matière des déchets [4]
- **Run 2 :** Valorisation matière des déchets [4, 6]
- **Run 3 :** Valorisation matière des déchets [6]
- **Prod :** Prévention des déchets [6]
- Catégories instables sur : Valorisation matière des déchets

> Identifier les acteurs du réemploi, les solliciter et co-construire (définition du besoin, identification d'un lieu) et organiser le forum. Réaliser un bilan en fin d’évènement.Faciliter le réemploi / réparation pour qu’il devienne un réflexe

#### Fiche 87225 — Action 11 - Mobiliser les acteurs de la réparation et du réemploi et les faire connaitre

- **Run 1 :** Valorisation matière des déchets [4, 6]
- **Run 2 :** Valorisation matière des déchets [4, 6]
- **Run 3 :** Valorisation matière des déchets [6]
- **Prod :** Prévention des déchets [6]
- Catégories instables sur : Valorisation matière des déchets

> Identifier les acteurs et les solutions en faveur de la prévention et de l’économie circulaire (réparation, réemploi) en co-construction avec Circule’R, la CCI et la CMA. Créer un annuaire et le diffuser sur le site internet de la CARO et les réseaux. Promouvoir le label Repar’acteurs et les formations autour de la réparation.Faciliter le réemploi / réparation pour qu’il devienne un réflexe

#### Fiche 87228 — Action 14 - Soutenir les projets de consommation responsable

- **Run 1 :** Prévention des déchets [3]
- **Run 2 :** Prévention des déchets [3, 6]
- **Run 3 :** Prévention des déchets [3]
- **Prod :** Prévention des déchets [3]
- Catégories instables sur : Prévention des déchets

> Soutenir financièrement un projet favorisant la consommation responsable sur le territoire et construire une culture de la consommation responsable, grâce à des messages adaptés

#### Fiche 87232 — Action 18 - Amplifier la pratique du compostage individuel

- **Run 1 :** Valorisation matière des déchets [3, 6]
- **Run 2 :** Valorisation matière des déchets [3, 6]
- **Run 3 :** Valorisation matière des déchets [1, 6]
- **Prod :** Valorisation matière des déchets [3, 6]
- Catégories instables sur : Valorisation matière des déchets

> Augmenter le taux d’équipement des foyers en composteurs individuels. S’assurer de la pratique effective. (mobiliser les foyers équipés qui ne pratiquent pas et équiper de nouveaux foyers).

#### Fiche 87249 — Action 35 - Réduire les apports des professionnels en déchèterie

- **Run 1 :** Prévention des déchets [6]
- **Run 2 :** Prévention des déchets [1, 4, 5, 6]
- **Run 3 :** Prévention des déchets [6]
- **Prod :** (aucun levier)
- Catégories instables sur : Prévention des déchets

> Mettre en place des espaces dédiés au réemploi en déchèterie Valoriser la pratique du réemploi par les agents de déchèterie Communiquer sur la pratique de réemploi en déchèterie Développer des partenariats pour augmenter le réemploi sur le territoire à partir des dons récupérés en déchèterie Proposer des alternatives pour réduire les déchets en déchèterie.

#### Fiche 87270 — Action 19 - Développer les biocarburants pour les bus et les véhicules électriques sur les transports à la demande

- **Run 1 :** Bus et cars décarbonés [1] | Véhicules électriques [1]
- **Run 2 :** Bus et cars décarbonés [5] | Véhicules électriques [5]
- **Run 3 :** Bus et cars décarbonés [1] | Véhicules électriques [1]
- **Prod :** Bus et cars décarbonés [5] | Efficacité et carburants décarbonés des véhicules privés [5] | Véhicules électriques [5]
- Catégories instables sur : Bus et cars décarbonés, Véhicules électriques

> Proposer une flotte de véhicules qui roule à l'électrique ou aux biocarburants

#### Fiche 87278 — Action 27 - Accentuer la démarche d’EIT

- **Run 1 :** Valorisation matière des déchets [6]
- **Run 2 :** Valorisation matière des déchets [4]
- **Run 3 :** Valorisation matière des déchets [4]
- **Prod :** (aucun levier)
- Catégories instables sur : Valorisation matière des déchets

> Action visant à développer les actions en direction des entreprises, en complément du travail réalisé par l'association Circule'R.

## CA Guingamp-Paimpol Agglomération de l'Armor à l'Argoat (4097)

- Fiches : **102** — stables sur les 3 runs : **52** (51%), instables : **50**
- Paires levier × catégorie distinctes proposées : 307 — 3/3 runs : 103, 2/3 runs : 60, 1/3 runs : 144
- Vote majoritaire = prod : 12/53 fiches classées d'un côté ou de l'autre
- Réponses JSON invalides rejouées : 3
- Appels : 15 — tokens d'entrée 223 986 (dont 0 en cache, 0%), sortie 128 084 — coût estimé 0.42 $ pour les 3 runs
- Date : 2026-10-30 15:07

### Classée dans certains runs, aucun levier dans d'autres (9)

#### Fiche 2216 — 1.3 Mobiliser et faire participer les citoyens à la transition

- **Run 1 :** Prévention des déchets [6]
- **Run 2 :** Electricité renouvelable [6] | Prévention des déchets [6]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Electricité renouvelable (1/3), Prévention des déchets (2/3)

> Le climat change. Et moi ? , programme sur 2020-2022 de mobilisation pour la participation des citoyens dans la transition écologique est lauréat d'un appel à projet porté par la Région Bretagne et l'ADEME (Ambition Climat). Il a été élaboré en associant les services et le plus largement possible des partenaires identifiés du territoire. Le choix de s'appuyer sur les acteurs locaux (environnementaux, sociaux, associatifs, institutionnels...) ancre le projet dans les réseaux existants, renforce …

#### Fiche 2247 — 2.6 Développer une politque anticipant les effets du changement climatique

- **Run 1 :** Sobriété des bâtiments (résidentiel) [4, 6]
- **Run 2 :** (aucun levier)
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété des bâtiments (résidentiel) (1/3)

> Le Contrat Local de Santé est un outil de santé publique contactualisé entre les territoires de Guingamp-Paimpol Agglomération et Leef-Armor communauté (échelle du Pays de Guingamp) et l'Agence Régionale de Santé. Sa finalité est de lutter cotnre les inégalités sociales et territoriales de santé en s'appuyant sur une approche transversale. Un premier CLS a été mis en place de 2017 à 2019. Un second CLS est en ocurs d'élaboration ce qui a permis d'explorer les liens et les enjeux entre santé et …

#### Fiche 2343 — 4.3 Réduire l’empreinte environnementale de la pêche en mer artisanale

- **Run 1 :** (aucun levier)
- **Run 2 :** Valorisation matière des déchets [6]
- **Run 3 :** Efficacité et carburants décarbonés des véhicules privés [3, 4, 6]
- **Prod :** (aucun levier)
- Leviers intermittents : Efficacité et carburants décarbonés des véhicules privés (1/3), Valorisation matière des déchets (1/3)

> Les ports de Loguivy-de-la-Mer et Pors Even à Ploubazlanec et le port de Paimpol appartiennent au Quartier maritime de Paimpol, qui compte 115 bateaux. La pratique de la pêche locale amène de nombreux bâtiments à changer de localisation sur le quartier maritime dans le courant de l’année. Par conséquent, afin de prendre en compte cette spécificité, les données de la pêche du Quartier maritime seront comptabilisées à l’échelle des deux EPCI Lannion Trégor Communauté (50%) et Guingamp-Paimpol Agg…

#### Fiche 21890 — Valorisation des productions locales

- **Run 1 :** (aucun levier)
- **Run 2 :** (aucun levier)
- **Run 3 :** Efficacité et sobriété logistique [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Efficacité et sobriété logistique (1/3)

> *Animations auprès des gestionnaires et cuisiniers de la restauration collective pour, au-delà du respect de la loi Egalim, accroitre l’approvisionnement local : groupes d’échange, formations * Défis auprès des publics scolaires et du grand public pour valoriser les produits locaux et de saison * Animation auprès des artisans de bouche et restaurateurs privés pour la structuration de filières locales d’approvisionnement et la mise en avant des bonnes pratiques (labellisation) * Mise à jour et d…

#### Fiche 21891 — Actions en faveur de la biodiversité

- **Run 1 :** (aucun levier)
- **Run 2 :** (aucun levier)
- **Run 3 :** Pratiques stockantes [1, 5, 6]
- **Prod :** (aucun levier)
- Leviers intermittents : Pratiques stockantes (1/3)

> *Mise en place d’actions de gestion sur des terrains appartenant à l’Agglomération, ou gérés par l’Agglomération (terrains du Conservatoire du littoral), * Animation des sites Natura 2000 dont l’Agglomération est opérateur (Trégor Goëlo et Têtes de bassin du Blavet et de l’Hyères) : définition et mise en oeuvre de plan de gestion et réalisation de travaux grâce à des contrats Natura 2000 *Réalisation d’études de terrain et de synthèse de données *Développement d’actions de communication (film, …

#### Fiche 21898 — Préservation des milieux aquatiques et prévention contre les inondations

- **Run 1 :** (aucun levier)
- **Run 2 :** (aucun levier)
- **Run 3 :** Pratiques stockantes [1]
- **Prod :** (aucun levier)
- Leviers intermittents : Pratiques stockantes (1/3)

> *Mise en place de programmes d’actions en faveur des milieux aquatiques dans le cadre de contrats de bassin versant (Grand Trieux, Jaudy Guindy Bizien et Léguer) *Elaboration et mise en oeuvre de plan de gestion sur les cours d’eau d’intérêt majeur : entretien de la ripisylve et gestion des embâcles *Réalisation de travaux en faveur de la continuité écologique et de la prévention des inondations * Amélioration des ouvrages GEMAPI (situés à Paimpol) * Etude inondations sur le bassin versant du Q…

#### Fiche 21931 — Accompagnement des communes sur l’aménagement des espaces publics

- **Run 1 :** Prévention des déchets [6]
- **Run 2 :** Prévention des déchets [6]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Prévention des déchets (2/3)

> *Rencontre avec les communes autour de la « charte Nature + » (ancienne charte 0 phyto) : entretien des espaces verts, gestion des eaux pluviales, réduction des déchets, biodiversité, communication…) *Accompagnement des communes sur le volet environnemental dans le cadre de l’appel à projet revitalisation de l’Agglomération *Organisation d’évènements et de formations pour sensibiliser les communes aux enjeux environnementaux (Formations CNFPT, sensibilisation sur le frelon asiatique, journées d…

#### Fiche 31888 — ECI 3. Réaliser des achats responsables

- **Run 1 :** Fret décarboné et multimodalité [5] | Prévention des déchets [5] | Valorisation matière des déchets [5]
- **Run 2 :** Prévention des déchets [5] | Valorisation matière des déchets [5]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Fret décarboné et multimodalité (1/3), Prévention des déchets (2/3), Valorisation matière des déchets (2/3)

> Les achats responsables consistent à acheter en tenant compte, à chaque étape du cycle de vie d'un produit ou d'une prestation, des impacts économiques (producteurs locaux, ...), environnementaux (produits et services labélisés Ecolabel européen ou autre label recommandé par l'ADEME, transport, émissions polluantes, consommation de ressources,...) et sociaux (respect des conditions de travail, égalité des sexes, accès à l'emploi pour les handicapés, ESS,...) qui sont générés.

#### Fiche 31890 — ECI 5. Soutenir et accompagner l'économie de la fonctionnalité et de la coopération

- **Run 1 :** (aucun levier)
- **Run 2 :** Prévention des déchets [6]
- **Run 3 :** Prévention des déchets [4, 6]
- **Prod :** (aucun levier)
- Leviers intermittents : Prévention des déchets (2/3)

> L’économie de la fonctionnalité et de la coopération établit une nouvelle relation entre l’offre et la demande qui n’est plus uniquement basée sur la simple vente de biens ou de services. La contractualisation repose sur les effets utiles (bénéfices) et l’offre s’adapte aux besoins réels des personnes, des entreprises et des collectivités ainsi qu’aux enjeux relatifs au développement durable. Ce modèle économique induit plus largement des transformations profondes dans les modes de production e…

### Levier présent dans certains runs seulement (10)

#### Fiche 2239 — 2.1 Finaliser un PLUi intégrateur des enjeux transversaux de sobriété

- **Run 1 :** Electricité renouvelable [2] | Sobriété des bâtiments (résidentiel) [2] | Sobriété foncière [2]
- **Run 2 :** Biogaz [2] | Electricité renouvelable [2] | Pratiques stockantes [2] | Sobriété foncière [2] | Vélo et transport en commun [2]
- **Run 3 :** Electricité renouvelable [2] | Sobriété des bâtiments (résidentiel) [2] | Sobriété foncière [2]
- **Prod :** Electricité renouvelable [2] | Réduction des déplacements [2] | Sobriété foncière [2]
- Leviers intermittents : Biogaz (1/3), Pratiques stockantes (1/3), Sobriété des bâtiments (résidentiel) (2/3), Vélo et transport en commun (1/3)

> Le PLUi est en cours d'élaboration. Toutefois, le PADD, qui fixe les grands enjeux et objectifs du PLUi, est voté. Il est organisé autour de trois axes décliné du projet de territoire et fixe les objectifs suivants en lien direct avec le PCAET : I. L'excellence environnementale, un atout majeur de valorisation et d'amélioration du cadre de vie 1 - L'eau, un milieu à protéger, une ressource à préserver : en assurant un développement cohérent avec les ressources disponibles et tenant compte des m…

#### Fiche 21910 — Création d’une Véloroute entre Ploubazlanec et Carhaix

- **Run 1 :** Réduction des déplacements [1] | Vélo et transport en commun [1]
- **Run 2 :** Vélo et transport en commun [1]
- **Run 3 :** Vélo et transport en commun [1]
- **Prod :** Vélo et transport en commun [1]
- Leviers intermittents : Réduction des déplacements (1/3)

> Le projet de véloroute vise à créer un itinéraire structurant traversant le territoire depuis Ploubazlanec à Carhaix afin de mettre en lumière l’ensemble du territoire et de contribuer à son rayonnement et à son attractivité. Ce projet s’intègre dans les ambitions politiques « des nouvelles dynamiques territoriales » et dans le schéma du tourisme et des loisirs 2023-2030. Éléments de calendrier : Lancement du marché pour la fourniture et la pose de la signalétique ainsi que des travaux de voiri…

#### Fiche 21920 — Suivre et animer un Opération Programmée d’Amélioration de l’Habitat et Renouvellement Urbain (OPAH-RU) sur les 4 communes « Petites Villes de Demain (PVD)

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [3, 6] | Changement chaudières gaz + rénovation (résidentiel) [3, 6] | Sobriété des bâtiments (résidentiel) [3, 6] | Sobriété foncière [3, 6]
- **Run 2 :** Sobriété des bâtiments (résidentiel) [3, 6] | Sobriété foncière [3, 6]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [3, 6] | Changement chaudières gaz + rénovation (résidentiel) [3, 6] | Sobriété des bâtiments (résidentiel) [3, 6] | Sobriété foncière [3, 6]
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [3, 6] | Changement chaudières gaz + rénovation (résidentiel) [3, 6] | Sobriété foncière [3, 6]
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (2/3), Changement chaudières gaz + rénovation (résidentiel) (2/3)

> Les 4 communes PVD et l’agglomération sont signataires d’une convention d’Opération de Revitalisation Territoriale (ORT), dont le volet habitat se traduit de manière opérationnelle par la mise en œuvre d’un outil d’amélioration du parc privé de logement : l’OPAH-RU. Ce dispositif contractuel avec l’Anah vise à concentrer de l’ingénierie et des moyens financiers en vue de redonner de l’attractivité résidentielle aux centralités de ces 4 villes prioritaires. L’OPAH-RU s’adresse aux propriétaires …

#### Fiche 21921 — Création d’une Maison de l’Habitat et de la Rénovation (MHER)

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6] | Sobriété des bâtiments (résidentiel) [6]
- **Run 2 :** Sobriété des bâtiments (résidentiel) [6]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6] | Sobriété des bâtiments (résidentiel) [6]
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6] | Sobriété des bâtiments (résidentiel) [6]
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (2/3), Changement chaudières gaz + rénovation (résidentiel) (2/3)

> Proposer une offre de service « France RENOV+ », déclinaison locale d’un dispositif national, lisible et de proximité permettant : • Un lieu ressource bien identifié sur Guingamp via une communication grand public, remplissant le rôle de « guichet unique » ; • Un accueil et une information de premier niveau pour tous les ménages, sans condition de ressources adossé aux marques « France Renov’ » (niveau national) et « Rénov’ Habitat Bretagne » (niveau régional) • Une information neutre, fiable e…

#### Fiche 21922 — DSP Mobilité 2026/2031

- **Run 1 :** Bus et cars décarbonés [4] | Vélo et transport en commun [4]
- **Run 2 :** Vélo et transport en commun [4]
- **Run 3 :** Bus et cars décarbonés [4] | Vélo et transport en commun [4]
- **Prod :** Vélo et transport en commun [2]
- Leviers intermittents : Bus et cars décarbonés (2/3)

> DSP Mobilités : - Transport scolaire, - Transport urbain sur les aires guingampaise et paimpolaises, - Location de vélo, - Transport à la demande. Éléments de calendrier : 1er janvier 2026 démarrage du contrat Durée : 6 ans et 1 mois Échéance : 31 janvier 2032

#### Fiche 21924 — Plan vélo

- **Run 1 :** Réduction des déplacements [1, 6] | Vélo et transport en commun [1, 6]
- **Run 2 :** Vélo et transport en commun [1, 6]
- **Run 3 :** Vélo et transport en commun [1, 6]
- **Prod :** Vélo et transport en commun [1, 6]
- Leviers intermittents : Réduction des déplacements (1/3)

> Développer les infrastructures, aménagements, actions de communication et animations autour du vélo

#### Fiche 31807 — CAE 2. Mettre en place un schéma directeur des énergies et des réseaux de chaleur

- **Run 1 :** Electricité renouvelable [2] | Réseaux de chaleur décarbonés [2]
- **Run 2 :** Biogaz [2] | Electricité renouvelable [2] | Réseaux de chaleur décarbonés [2]
- **Run 3 :** Electricité renouvelable [2] | Réseaux de chaleur décarbonés [2]
- **Prod :** Electricité renouvelable [2] | Réseaux de chaleur décarbonés [2]
- Leviers intermittents : Biogaz (1/3)

> La collectivité a établi une programmation énergétique à l’échelle territoriale, détaillant des stratégies et des directives concrètes pour : réduire la consommation d'énergie et améliorer l'efficacité énergétique ; exploiter pleinement le potentiel de production locale d'énergie renouvelable afin d'atteindre les objectifs du territoire ; accroître l'utilisation des énergies renouvelables à travers un plan de développement spécifique ; évelopper des réseaux de chaleur/froid renouvelable et de r…

#### Fiche 31809 — CAE 3. Utiliser les documents d'urbanisme pour transcrire les enjeux climat-air-énergie et de préservation des ressources naturelles, tout en luttant contre l'artificialisation des sols.

- **Run 1 :** Réduction des déplacements [2] | Sobriété foncière [2]
- **Run 2 :** Sobriété foncière [2] | Vélo et transport en commun [2]
- **Run 3 :** Sobriété foncière [2]
- **Prod :** Electricité renouvelable [2] | Réduction des déplacements [2] | Réseaux de chaleur décarbonés [2] | Sobriété foncière [2]
- Leviers intermittents : Réduction des déplacements (1/3), Vélo et transport en commun (1/3)

> Les documents d’urbanisme sont en cohérence avec la stratégie climat-air-énergie de la collectivité, permettant une traduction spatiale de ces objectifs dans une logique d'économie circulaire et de solidarité rural/urbain. Des dispositions incitatives et contraignantes sont prévues pour favoriser la conception bioclimatique, des formes urbaines resserrées, une mobilité durable, l’efficacité énergétique, les énergies renouvelables, ainsi que les réseaux de chaleur et de froid. Elles visent égale…

#### Fiche 31814 — CAE 8. Organiser et développer les mobilités alternatives sur le territoire

- **Run 1 :** Réduction des déplacements [1] | Vélo et transport en commun [1]
- **Run 2 :** Vélo et transport en commun [1]
- **Run 3 :** Réduction des déplacements [1] | Vélo et transport en commun [1]
- **Prod :** Vélo et transport en commun [1]
- Leviers intermittents : Réduction des déplacements (2/3)

> Pour réduire les consommations d'énergie et les émissions de gaz à effet de serre, la collectivité développe le réseau cyclable, la signalisation et le stationnements associés afin d'encourager le développement de ce mode de déplacement tout en développant et améliorant les performances du service public de transports publics dans une perspective d'augmentation de son usage et de diminution du recours à la voiture.

#### Fiche 31889 — ECI 4. Soutenir et accompagner la consommation responsable et la sobriété des acteurs du territoire

- **Run 1 :** Prévention des déchets [6]
- **Run 2 :** Prévention des déchets [6]
- **Run 3 :** Prévention des déchets [6] | Réduction des déplacements [6] | Sobriété des bâtiments (résidentiel) [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Réduction des déplacements (1/3), Sobriété des bâtiments (résidentiel) (1/3)

> La consommation responsable correspond à un engagement civique actif en vue de la qualité de vie des citoyens, mais aussi en faveur de la collectivité dans son ensemble. Elle concerne aussi bien le citoyen consommateur que l'acheteur professionnel (privé ou public). La consommation responsable consiste à nous questionner sur la pertinence de nos besoins dans une logique de sobriété (c'est-à-dire une logique qui consiste à éviter les demandes d’énergie, de matériaux, de terres et d’eau dans le c…

### Levier intermittent et catégories instables (21)

#### Fiche 2217 — 1.4 Mettre en œuvre "Trajectoire Zéro Déchet" (PDPLMA 2020-2026 : programme local de prévention des déchets ménagers et assimilés

- **Run 1 :** Biogaz [2, 4] | Prévention des déchets [2, 4, 6]
- **Run 2 :** Biogaz [4, 6] | Prévention des déchets [2, 3, 4, 5, 6] | Valorisation matière des déchets [6]
- **Run 3 :** Prévention des déchets [2, 3, 4, 5, 6] | Valorisation matière des déchets [2, 4, 5, 6]
- **Prod :** Prévention des déchets [2, 4, 5, 6]
- Leviers intermittents : Biogaz (2/3), Valorisation matière des déchets (2/3)
- Catégories instables sur : Prévention des déchets

> L'élaboration des programmes locaux de prévention des déchets ménagers et assimilés (PLPDMA) est obligatoire depuis le 1er janvier 2012, et est une condition essentielle à la mise en œuvre d'une démarche territoriale d'économie circulaire. Conformément au principe d'économie circulaire, le plan régional de prévention et de gestion des déchets de Bretagne affiche clairement la trajectoire "zéro enfouissement des déchets", ceux-ci devant être considérés comme des ressources. PLPDMA coordonne l'en…

#### Fiche 2218 — 1.5 Développer un projet éducatif en faveur de l'engagement citoyen

- **Run 1 :** Prévention des déchets [6] | Sobriété et isolation des bâtiments (tertiaire) [6]
- **Run 2 :** Sobriété et isolation des bâtiments (tertiaire) [6]
- **Run 3 :** Sobriété et isolation des bâtiments (tertiaire) [3, 4, 6]
- **Prod :** (aucun levier)
- Leviers intermittents : Prévention des déchets (1/3)
- Catégories instables sur : Sobriété et isolation des bâtiments (tertiaire)

> Guingamp-Paimpol Agglomération s’est doté de la compétence de coordination d’une politique en faveur de la petite enfance (0-3 ans), de l’enfance (3-12 ans) et de la jeunesse (12-25) qui comprend la création, l’organisation et le développement des services, des équipements et des actions d’intérêt communautaire pour ces trois publics. Le projet pédagogique de l’agglomération donne le cadre dans lequel les structures du territoire développent leur propre projet d’établissement. Les enjeux de tra…

#### Fiche 2219 — 1.6 Organiser la transition énergétique du patrimoine immobilier public

- **Run 1 :** Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 2 :** Electricité renouvelable [5] | Sobriété et isolation des bâtiments (tertiaire) [3, 4, 5]
- **Run 3 :** Sobriété et isolation des bâtiments (tertiaire) [3, 5, 6]
- **Prod :** Changement de chaudière à fioul (tertiaire) [3, 4, 5, 6] | Changement de chaudière à gaz (tertiaire) [3, 4, 5, 6] | Sobriété et isolation des bâtiments (tertiaire) [3, 4, 5, 6]
- Leviers intermittents : Electricité renouvelable (1/3)
- Catégories instables sur : Sobriété et isolation des bâtiments (tertiaire)

> Le diagnostic du Plan Climat a mis en évidence un bâti public plutôt ancien et énergivore mais parfois à forte valeur patrimoniale. Ceci rend complexe leur rénovation thermique, notamment pour les plus petites communes rurales. Le décret n°2019-771 du 23 juillet 2019 dit "décret tertiaire" fixe une obligation de réduction de la consommation d'énergie pour les bâtiments d'activité tertiaire de plus de 1000m2 de 40% pour 2030, 50% pour 2040 et 60% pour 2050 par rapport à 2010. 1.6.1 Développer le…

#### Fiche 2240 — 2.2 Lutter contre l'érosion de la biodiversité et des milieux

- **Run 1 :** Gestion des forêts et produits bois [1, 2] | Gestion des haies [1, 2]
- **Run 2 :** Gestion des forêts et produits bois [6] | Gestion des haies [1, 2, 6] | Pratiques stockantes [1, 2]
- **Run 3 :** Gestion des forêts et produits bois [1, 4] | Gestion des haies [1, 2, 4]
- **Prod :** (aucun levier)
- Leviers intermittents : Pratiques stockantes (1/3)
- Catégories instables sur : Gestion des forêts et produits bois, Gestion des haies

> Le territoire de l'agglomération se caractérise par une grande richesse patrimoniale liée à la diversité des milieux représentés (littoral, fluvial, forestier, plaines, valons etc...). Trois grands site Natura 2000, gérés par Guingamp-Paimpol Agglomération, posent des limites géographiques au Nord et au Sud et de nombreux espaces à forte valeur patrimoniale ponctuent le territoire : 3 sites du conservatoire du littoral, gérés par l'agglomération et de nombreux Espaces naturels sensibles gérés p…

#### Fiche 2248 — 3.1 (Re-)dynamiser des centres villes pour un mode de vie sobre en énergie

- **Run 1 :** Réduction des déplacements [1] | Sobriété des bâtiments (résidentiel) [1] | Sobriété foncière [1, 2] | Vélo et transport en commun [1]
- **Run 2 :** Réduction des déplacements [1, 2] | Sobriété des bâtiments (résidentiel) [1, 2] | Sobriété foncière [1, 2] | Vélo et transport en commun [1]
- **Run 3 :** Réduction des déplacements [1, 2] | Sobriété des bâtiments (résidentiel) [1, 3] | Sobriété foncière [1, 2, 3]
- **Prod :** Réduction des déplacements [1, 2] | Sobriété foncière [1, 2]
- Leviers intermittents : Vélo et transport en commun (2/3)
- Catégories instables sur : Réduction des déplacements, Sobriété des bâtiments (résidentiel), Sobriété foncière

> La ville de Guingamp et Guingamp-Paimpol Agglomération sont signataires depuis 2016 d'une convention de revitalisation du centre-ville et de développement du territoire (CRCDT). Cette convention 2017-2022 les engage sur 5 volets d'action en faveur de la centralité de Guingamp mais aussi, par capitalisation, de l'ensemble des centralités du territoire. Depuis, l'Agglomération est partenaire de 2 protocoles régionaux (Guingamp, Paimpol) dans le cadre des appels à projets "centres-bourgs" régionau…

#### Fiche 2336 — 3.4 Mettre en œuvre le Programme Local de l’Habitat 2020-2025

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [3, 6] | Changement chaudières gaz + rénovation (résidentiel) [3, 6] | Sobriété des bâtiments (résidentiel) [3, 6]
- **Run 2 :** Sobriété des bâtiments (résidentiel) [2, 3, 6]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [2, 3, 6] | Changement chaudières gaz + rénovation (résidentiel) [2, 3, 6] | Sobriété des bâtiments (résidentiel) [2, 3, 6]
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [2, 3, 6] | Changement chaudières gaz + rénovation (résidentiel) [2, 3, 6] | Sobriété des bâtiments (résidentiel) [2, 3, 6]
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (2/3), Changement chaudières gaz + rénovation (résidentiel) (2/3)
- Catégories instables sur : Sobriété des bâtiments (résidentiel)

> Historiquement, seuls les deux secteurs urbains disposaient d’un PLH (Guingamp et Paimpol). Lors de la création de l’agglomération, le PLH a été étendu à l’ensemble du territoire. Le diagnostic a mise en évidence des problèmes forts de confort, d’indignité, de besoins d’adaptation et de précarité énergétique. 60 à 65% des foyers de l’agglomération sont éligibles au logement social. Sur le secteur guingampais, cette proportion monte à près de 80% des foyers. Une filière artisanale encore fragile…

#### Fiche 2338 — 3.5 Structurer une « maison de l’habitat » PLRH pour dynamiser le marché de la rénovation thermique en direction du particulier

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [3, 6] | Changement chaudières gaz + rénovation (résidentiel) [3, 6] | Sobriété des bâtiments (résidentiel) [3, 6]
- **Run 2 :** Sobriété des bâtiments (résidentiel) [3, 6]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [3, 4, 6] | Changement chaudières gaz + rénovation (résidentiel) [3, 4, 6] | Sobriété des bâtiments (résidentiel) [3, 4, 6]
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6]
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (2/3), Changement chaudières gaz + rénovation (résidentiel) (2/3)
- Catégories instables sur : Sobriété des bâtiments (résidentiel)

> Le service public de la performance énergétique de l’habitat (SPPEH) est inscrit dans la loi. Si elle confie l’organisation du SPEEH aux régions, elle ne précise pas certains points cruciaux tant quant a sa mise en œuvre, son financement, son pilotage et plus largement l’organisation territoriale de la rénovation énergétique.En Bretagne, la Région, l’État et l’ADEME favorisent le déploiement de Plateformes locales de rénovation de l’habitat. Point d’information et de contact avec les particulie…

#### Fiche 2340 — 4.1 Accompagner les entreprises du secondaire et du tertiaire dans la mise en œuvre de la transition

- **Run 1 :** Changement de chaudière à fioul (tertiaire) [6] | Changement de chaudière à gaz (tertiaire) [6] | Production Industrielle [6] | Prévention des déchets [6] | Sobriété et isolation des bâtiments (tertiaire) [6]
- **Run 2 :** Production Industrielle [6] | Prévention des déchets [6]
- **Run 3 :** Production Industrielle [4, 6] | Prévention des déchets [4, 6] | Valorisation matière des déchets [4, 6]
- **Prod :** Changement de chaudière à fioul (tertiaire) [6] | Changement de chaudière à gaz (tertiaire) [6] | Prévention des déchets [6] | Sobriété et isolation des bâtiments (tertiaire) [6]
- Leviers intermittents : Changement de chaudière à fioul (tertiaire) (1/3), Changement de chaudière à gaz (tertiaire) (1/3), Sobriété et isolation des bâtiments (tertiaire) (1/3), Valorisation matière des déchets (1/3)
- Catégories instables sur : Production Industrielle, Prévention des déchets

> La performance environnementale des entreprises est devenu un enjeu essentiel de leur développement et une condition de leur durabilité. L'économie circulaire est désormais un facteur clé de performance et de compétitivité du développement économique des entreprises. Mais la mise en œuvre d’une démarche globale de prise en compte de l’environnement reste complexe pour les TPE, qui peuvent difficilement avoir accès à certaines expertises. Pour les accompagner, le réseau des Métiers de Bretagne e…

#### Fiche 2344 — 4.4 Développer un projet touristique qui intègre et s’appuie sur les enjeux de la transition

- **Run 1 :** Réduction des déplacements [6] | Sobriété et isolation des bâtiments (tertiaire) [6] | Vélo et transport en commun [1, 6]
- **Run 2 :** Réduction des déplacements [6] | Vélo et transport en commun [6]
- **Run 3 :** Réduction des déplacements [1, 6] | Vélo et transport en commun [1, 6]
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété et isolation des bâtiments (tertiaire) (1/3)
- Catégories instables sur : Réduction des déplacements, Vélo et transport en commun

> Le Schéma de développement touristique réalisé en 2018 par Guingamp-Paimpol Agglomération met en évidence des caractéristiques locales largement valorisables dans un projet de tourisme vert / tourisme nature. Le territoire bénéficie en effet de nombreux atouts patrimoniaux sur lesquels appuyer le développement d’un tourisme respectueux de l’environnement : les paysages ruraux et littoraux, un patrimoine riche et singulier tant sur le plan culturel, paysager, qu’architectural, des productions ar…

#### Fiche 2345 — 4.5 Accompagner la transition et mobiliser la capacité de résilience du secteur agricole

- **Run 1 :** Biogaz [6] | Bâtiments & Machines agricoles [6] | Changements de pratiques de fertilisation azotée [6] | Elevage durable [6] | Gestion des haies [6] | Gestion des prairies [6] | Pratiques stockantes [6]
- **Run 2 :** Biogaz [6] | Bâtiments & Machines agricoles [6] | Changements de pratiques de fertilisation azotée [6] | Elevage durable [6] | Gestion des haies [6] | Pratiques stockantes [6]
- **Run 3 :** Biogaz [4, 6] | Bâtiments & Machines agricoles [4, 6] | Changements de pratiques de fertilisation azotée [4, 6] | Elevage durable [4, 6] | Gestion des haies [4, 6] | Gestion des prairies [4, 6] | Pratiques stockantes [4, 6]
- **Prod :** (aucun levier)
- Leviers intermittents : Gestion des prairies (2/3)
- Catégories instables sur : Biogaz, Bâtiments & Machines agricoles, Changements de pratiques de fertilisation azotée, Elevage durable, Gestion des haies, Pratiques stockantes

> La Bretagne est un territoire d’exportation agricole essentiel à l’échelle française et internationale. Elle regroupe des exploitations variées avec des fonctionnements et des modèles économiques très différents. Les crises récentes (sanitaires, de consommation, événements climatiques…) ont mis en évidence des vulnérabilités de certains modèles agricoles, notamment les moins autonomes. Dès 2019, l’agglomération a fait le choix du renforcement des filières locales par l’engagement de la restaura…

#### Fiche 2346 — 5.1 Engager les collectivités locales dans la planification énergétique territoriale et la production d’énergies renouvelables

- **Run 1 :** Biogaz [2, 4] | Electricité renouvelable [1, 2, 4] | Gestion des forêts et produits bois [1, 4] | Réseaux de chaleur décarbonés [1, 4]
- **Run 2 :** Biogaz [1, 2] | Electricité renouvelable [1, 2, 4] | Réseaux de chaleur décarbonés [1] | Sobriété foncière [2]
- **Run 3 :** Biogaz [1, 4] | Electricité renouvelable [1, 2, 4, 5] | Réseaux de chaleur décarbonés [1, 4]
- **Prod :** Electricité renouvelable [2, 4]
- Leviers intermittents : Gestion des forêts et produits bois (1/3), Sobriété foncière (1/3)
- Catégories instables sur : Biogaz, Electricité renouvelable, Réseaux de chaleur décarbonés

> Le diagnostic du Plan Climat a mis en évidence les nombreuses ressources en énergie renouvelables mobilisables sur le territoire de Guingamp-Paimpol Agglomération. Afin d’optimiser ces ressources, le territoire développe une approche de planification, qui applique les principes de renforcement de l’adéquation entre les ressources et l’utilisation locales, la sécurisation des besoins fondamentaux et la solidarité avec les territoires moins bien dotés en ressources énergétiques. La planification …

#### Fiche 4071 — 5.2 Poursuivre le projet de chaufferie en économie circulaire avec réseau de chaleur urbain et réseau de vapeur industrielle

- **Run 1 :** Réseaux de chaleur décarbonés [1]
- **Run 2 :** Réseaux de chaleur décarbonés [1, 4] | Valorisation matière des déchets [1, 4]
- **Run 3 :** Réseaux de chaleur décarbonés [1] | Valorisation matière des déchets [1]
- **Prod :** Réseaux de chaleur décarbonés [1, 4] | Valorisation matière des déchets [1]
- Leviers intermittents : Valorisation matière des déchets (2/3)
- Catégories instables sur : Réseaux de chaleur décarbonés

> Le projet s’appuie sur la logique de d’économie circulaire. Inscrit dans les travaux préparatoires du PRPGD (Plan Régional de Prévention et de Gestion des Déchets) porté par la Région Bretagne, il répond à plusieurs enjeux territoriaux : d’une part, il permet l’approvisionnement en chaleur à la fois d’un réseau industriel vapeur (dont une entreprise soumise au Programme National d’Allocation des Quotas d’Emission) et d’un réseau urbain d’eau chaude intégrant le Centre hospitalier de Pabu. D’aut…

#### Fiche 4079 — 5.5 Développer la filière bois énergie, notamment issue du bocage

- **Run 1 :** Gestion des haies [2, 4, 6] | Réseaux de chaleur décarbonés [1]
- **Run 2 :** Gestion des forêts et produits bois [4, 6] | Gestion des haies [2, 4, 6] | Réseaux de chaleur décarbonés [1, 5]
- **Run 3 :** Gestion des haies [1, 4, 6] | Réseaux de chaleur décarbonés [1]
- **Prod :** Gestion des haies [4] | Réseaux de chaleur décarbonés [4]
- Leviers intermittents : Gestion des forêts et produits bois (1/3)
- Catégories instables sur : Gestion des haies, Réseaux de chaleur décarbonés

> Guingamp-Paimpol Agglomération est le territoire de Bretagne ayant la plus importante ressource forestière (données OEB 2020). Sur le territoire, le développement de la filière bois énergie se construit prioritairement sur la mobilisation d’une importante ressource bocagère, dont les enjeux sont multiples : milieu, biodiversité, qualité de l’eau, infiltration des eaux pluviales, maintien des sols et production de bois. Son exploitation est limitée d’une part par le manque d’exutoire en valorisa…

#### Fiche 4083 — 5.7 Développer l'accès aux carburants alternatifs

- **Run 1 :** Efficacité et carburants décarbonés des véhicules privés [1, 5] | Véhicules électriques [1]
- **Run 2 :** Bus et cars décarbonés [1, 5] | Fret décarboné et multimodalité [1, 6] | Véhicules électriques [1, 4]
- **Run 3 :** Efficacité et carburants décarbonés des véhicules privés [1] | Véhicules électriques [1]
- **Prod :** Efficacité et carburants décarbonés des véhicules privés [1] | Véhicules électriques [1]
- Leviers intermittents : Bus et cars décarbonés (1/3), Efficacité et carburants décarbonés des véhicules privés (2/3), Fret décarboné et multimodalité (1/3)
- Catégories instables sur : Véhicules électriques

> Développement des bornes électriques et Axéo Auto : Le réseau Brev’Car (Bornes de recharge électrique pour véhicules en Côtes d’Armor) compte 164 bornes accélérées en Côtes d’Armor et 33 sur territoire de l’Agglomération. Les bornes de Guingamp et Paimpol comptent parmi les 10 bornes les plus utilisées du département avec plus de 70 usagers chacune. Pour le développement du service d’autopartage Axéo Auto (inclus dans la DSP Transport déléguée à Transdev), Guingamp-Paimpol agglomération a conve…

#### Fiche 21892 — Actions en faveur du bocage

- **Run 1 :** Gestion des haies [2, 6]
- **Run 2 :** Gestion des haies [2, 4, 6]
- **Run 3 :** Gestion des haies [1, 4, 5, 6] | Pratiques stockantes [1]
- **Prod :** Gestion des forêts et produits bois [1, 4] | Gestion des haies [1, 2, 4]
- Leviers intermittents : Pratiques stockantes (1/3)
- Catégories instables sur : Gestion des haies

> *Réalisation de chantiers de plantations et de gestion de haies chez les agriculteurs *Mise en place de travaux de gestion du bois bord de route avec les communes *Instruction des déclarations préalables et des dossiers BCAE8 pour le déplacement de haies *Assurer une gestion durable des boisements de l’Agglomération *Mise en place de Plan de Gestion Durable des Haies (PGDH) pour les agriculteurs producteurs de la SCIC Bocagénèse Éléments de calendrier : 2023/2027 : mise en œuvre de la stratégie…

#### Fiche 21919 — Accompagnement des bailleurs sociaux

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [3, 4] | Changement chaudières gaz + rénovation (résidentiel) [3, 4] | Sobriété des bâtiments (résidentiel) [3, 4] | Sobriété foncière [3, 4]
- **Run 2 :** Sobriété des bâtiments (résidentiel) [3, 4] | Sobriété foncière [3, 4]
- **Run 3 :** Sobriété des bâtiments (résidentiel) [3] | Sobriété foncière [3]
- **Prod :** Sobriété foncière [3]
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (1/3), Changement chaudières gaz + rénovation (résidentiel) (1/3)
- Catégories instables sur : Sobriété des bâtiments (résidentiel), Sobriété foncière

> 1/ Inciter à la réalisation de programmes de logements sociaux répondant aux besoins du territoire : • Dans un objectif de développement accéléré d’une offre abordable à destination des ménages (très) modestes : par un soutien financier continu des programmes de logement social (subventions de droit commun dédiées aux programmes neufs et « à partir de l’existant ») • Dans un objectif de sobriété foncière et de revitalisation des centralités : par la mobilisation du Fonds d’Intervention Foncière…

#### Fiche 31812 — CAE 6. Inciter à la réduction des consommations et à l’achat d’électricité verte tout en augmentant la production d'électricité issue d'énergies renouvelables sur le territoire.

- **Run 1 :** Electricité renouvelable [4, 6]
- **Run 2 :** Electricité renouvelable [1, 6] | Sobriété des bâtiments (résidentiel) [6] | Sobriété et isolation des bâtiments (tertiaire) [6]
- **Run 3 :** Electricité renouvelable [6]
- **Prod :** Electricité renouvelable [4, 6]
- Leviers intermittents : Sobriété des bâtiments (résidentiel) (1/3), Sobriété et isolation des bâtiments (tertiaire) (1/3)
- Catégories instables sur : Electricité renouvelable

> La collectivité, en lien avec les gestionnaires et concessionnaires de réseaux d’électricité, de gaz et de chaleur, veille à la qualité du service rendu et à la contribution de cette mission à sa stratégie d'efficacité énergétique, de développement des énergies renouvelables et de lutte contre le changement climatique. Des réflexions et des actions pour une optimisation du réseau, notamment via la flexibilité de la demande, de la production et/ou du stockage (SmartGrid), sont menées. En partena…

#### Fiche 31816 — CAE 11. Accompagner et coopérer avec les acteurs professionnels et les particulier pour la rénovation et la construction durable de leur logement

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [3, 4, 6] | Changement chaudières gaz + rénovation (résidentiel) [3, 4, 6] | Sobriété des bâtiments (résidentiel) [3, 4, 6] | Sobriété et isolation des bâtiments (tertiaire) [6]
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [3, 6] | Changement chaudières gaz + rénovation (résidentiel) [3, 6] | Changement de chaudière à fioul (tertiaire) [6] | Changement de chaudière à gaz (tertiaire) [6] | Sobriété des bâtiments (résidentiel) [3, 6] | Sobriété et isolation des bâtiments (tertiaire) [6]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [3, 6] | Changement chaudières gaz + rénovation (résidentiel) [3, 6] | Sobriété des bâtiments (résidentiel) [3, 6] | Sobriété et isolation des bâtiments (tertiaire) [3, 6]
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [3, 6] | Changement chaudières gaz + rénovation (résidentiel) [3, 6] | Changement de chaudière à fioul (tertiaire) [6] | Changement de chaudière à gaz (tertiaire) [6] | Sobriété et isolation des bâtiments (tertiaire) [6]
- Leviers intermittents : Changement de chaudière à fioul (tertiaire) (1/3), Changement de chaudière à gaz (tertiaire) (1/3)
- Catégories instables sur : Changement chaudières fioul + rénovation (résidentiel), Changement chaudières gaz + rénovation (résidentiel), Sobriété des bâtiments (résidentiel), Sobriété et isolation des bâtiments (tertiaire)

> La collectivité joue un rôle d’animateur territorial pour impulser une dynamique sur le territoire en matière de climat, air et énergie. Elle informe et incite les acteurs professionnels du bâtiment (bailleurs sociaux, promoteurs, investisseurs, artisans, bureaux d'études, administrateurs de biens, notaires, agents immobiliers, etc.) à intégrer ces enjeux dans leurs activités. Ces actions sont réalisées via des espaces conseils France Rénov ou des conventions volontaires, qui incluent des stand…

#### Fiche 31882 — CAE 12. Favoriser les activités économiques durables sur le territoire

- **Run 1 :** Production Industrielle [4, 6] | Prévention des déchets [4, 6] | Valorisation matière des déchets [4, 6]
- **Run 2 :** Production Industrielle [4]
- **Run 3 :** Production Industrielle [4]
- **Prod :** (aucun levier)
- Leviers intermittents : Prévention des déchets (1/3), Valorisation matière des déchets (1/3)
- Catégories instables sur : Production Industrielle

> La collectivité initie, soutient ou participe à des projets de coopération avec les acteurs de l'économie locale ou régionale sur le climat, l'air et l'énergie, afin d'encourager la mutation des activités économiques vers un modèle bas-carbon. Elle participe notamment au développement des projets d’écologie industrielle et plus généralement d'économie circulaire sur le territoire. Elle contribue à l'amélioration de la qualité environnementale des zones d’activités .

#### Fiche 31884 — CAE 14. Soutenir une agriculture et une alimentation plus durable

- **Run 1 :** Changements de pratiques de fertilisation azotée [4, 6] | Elevage durable [4, 6] | Gestion des haies [4, 6] | Gestion des prairies [4, 6] | Pratiques stockantes [4, 6] | Prévention des déchets [5, 6] | Sobriété foncière [2]
- **Run 2 :** Changements de pratiques de fertilisation azotée [3, 6] | Elevage durable [3, 6] | Gestion des prairies [3, 6] | Pratiques stockantes [3, 6] | Prévention des déchets [3, 6] | Sobriété foncière [2, 3, 6]
- **Run 3 :** Bâtiments & Machines agricoles [3, 6] | Changements de pratiques de fertilisation azotée [3, 6] | Elevage durable [3, 6] | Pratiques stockantes [3, 6] | Prévention des déchets [5, 6] | Sobriété foncière [2]
- **Prod :** Bâtiments & Machines agricoles [4, 6] | Changements de pratiques de fertilisation azotée [4, 6] | Elevage durable [4, 6] | Pratiques stockantes [4, 6] | Prévention des déchets [5, 6]
- Leviers intermittents : Bâtiments & Machines agricoles (1/3), Gestion des haies (1/3), Gestion des prairies (2/3)
- Catégories instables sur : Changements de pratiques de fertilisation azotée, Elevage durable, Pratiques stockantes, Prévention des déchets, Sobriété foncière

> Au travers de ses compétences, la collectivité soutient, promeut et encourage des pratiques agricoles et alimentaires durables sur son territoire et sur ses territoires d’approvisionnement : en menant des actions visant à réduire les émissions de gaz à effet de serre, de particules et plus globalement les impacts environnementaux du secteur agricole (formation aux pratiques agro-écologiques, certification environnementale des exploitations...) ; préservant le foncier agricole au travers des doc…

#### Fiche 31887 — ECI 2. Améliorer l'efficience du système de collecte

- **Run 1 :** Prévention des déchets [1, 3, 6] | Valorisation matière des déchets [1, 3, 6]
- **Run 2 :** Efficacité et sobriété logistique [1, 3] | Fret décarboné et multimodalité [1, 3] | Prévention des déchets [1, 3]
- **Run 3 :** Prévention des déchets [3, 6] | Valorisation matière des déchets [5, 6]
- **Prod :** Efficacité et sobriété logistique [1, 6] | Valorisation matière des déchets [1, 6]
- Leviers intermittents : Efficacité et sobriété logistique (1/3), Fret décarboné et multimodalité (1/3), Valorisation matière des déchets (2/3)
- Catégories instables sur : Prévention des déchets

> Souvent responsable des plus gros impacts environnementaux et des plus gros coûts, la collecte des déchets doit être pensée pour être plus efficiente en elle-même mais également être en lien avec la prévention dans une logique de réduction des déchets et en cohérence avec les moyens de traitement. L’optimisation de la collecte commence chez le producteur du déchet et doit donc être associée à une communication efficace notamment lors du déploiement de nouvelles solutions (passage de « Porte A P…

### Mêmes leviers, catégories différentes (10)

#### Fiche 2220 — 1.7 Décarboner la mobilité des collectivités 

- **Run 1 :** Réduction des déplacements [5] | Véhicules électriques [5]
- **Run 2 :** Réduction des déplacements [5] | Véhicules électriques [5]
- **Run 3 :** Réduction des déplacements [5] | Véhicules électriques [3, 5, 6]
- **Prod :** Réduction des déplacements [5] | Véhicules électriques [5]
- Catégories instables sur : Véhicules électriques

> La loi prévoit le verdissement de la flotte de véhicule publics (LTECV, LAURE, LOM) avec une part minimale de 30% de véhicules renouvelés à faibles émissions de CO2 et polluants (électriques et hybrides rechargeables) pour les collectivités à partir du 1er juillet 2021 et 37,4% à très faible émissions à partir du 1er janvier 2026. En outre, les services de l'agglomération sont répartis sur l'ensemble du territoire, ce qui implique de nombreux déplacements et la question de leur optimisation s'e…

#### Fiche 2334 — 3.2 Développer des alternatives quotidiennes à l'autosolisme

- **Run 1 :** Bus et cars décarbonés [1, 2] | Covoiturage [1, 3] | Réduction des déplacements [1] | Véhicules électriques [1, 3] | Vélo et transport en commun [1, 2, 3]
- **Run 2 :** Bus et cars décarbonés [1] | Covoiturage [1, 3] | Réduction des déplacements [2, 6] | Véhicules électriques [1, 3] | Vélo et transport en commun [1, 3, 6]
- **Run 3 :** Bus et cars décarbonés [1, 4] | Covoiturage [1, 3, 4] | Réduction des déplacements [6] | Véhicules électriques [1, 3] | Vélo et transport en commun [1, 3, 4]
- **Prod :** Covoiturage [1, 2] | Vélo et transport en commun [1, 2, 4]
- Catégories instables sur : Bus et cars décarbonés, Covoiturage, Réduction des déplacements, Vélo et transport en commun

> Les territoires ruraux cumulentles difficultés en matière de mobilité : à l'éloignement des pôles commerciaux et des bassins d'emploi s'ajoute le difficile maintien des services de proximité et des transports collectifs qui conduisent à privilégier de manière quasi exclusive le mode automobile. Pour être une option crédible, l'offre de transport alternative doit tenir compte des besoins spécifiques de mobilités (isolement géographique, faible densité, personnes agées, etc.). Le PADD du PLUi int…

#### Fiche 2335 — 3.3 Explorer les intermodalités rail-route

- **Run 1 :** Fret décarboné et multimodalité [2, 4]
- **Run 2 :** Fret décarboné et multimodalité [1, 2]
- **Run 3 :** Fret décarboné et multimodalité [1, 2, 4]
- **Prod :** Fret décarboné et multimodalité [1, 2]
- Catégories instables sur : Fret décarboné et multimodalité

> Le territoire est traversé par deux voies ferroviaires qui se croisent à Guingamp. L'axe Paimpol-Carhaix relie le Nord au Sud du territoire et l'axe Rennes-Brest relie l'Est et l'Ouest. Une offre de TER circule régulièrement sur les deux axes. Guingamp, au centre de ce dispositif ferroviaire, est intégrée au réseau des gares accueillent le TGV. La production agricole et agroalimentaire du territoire, très largement supérieur aux besoins des habitants, est principalement à vocation d'exportation…

#### Fiche 2339 — 3.6 Porter un projet exemplaire de réhabilitation de bâtiment

- **Run 1 :** Electricité renouvelable [1] | Sobriété des bâtiments (résidentiel) [1]
- **Run 2 :** Electricité renouvelable [1] | Sobriété des bâtiments (résidentiel) [1]
- **Run 3 :** Electricité renouvelable [1] | Sobriété des bâtiments (résidentiel) [1, 4]
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [1, 3] | Changement chaudières gaz + rénovation (résidentiel) [1, 3] | Sobriété des bâtiments (résidentiel) [1, 3]
- Catégories instables sur : Sobriété des bâtiments (résidentiel)

> La ville de Paimpol compte 576 logements sociaux. Le parc est composé à 98% de logements collectifs, avec une offre importante de grands logements, ce qui parait inadaptée aujourd’hui au vu des caractéristiques d’une population vieillissante et où la part des personnes seule prédomine. Dans ce contexte, les 233 logements sociaux construits en 1968 au cœur du quartier de Kernoa font l’objet d’un projet de restructuration pour s’adapter aux besoins des habitants. Proche du centre-ville, du port, …

#### Fiche 4073 — 5.3 Pérenniser le site d'expérimentation d'hydroliennes

- **Run 1 :** Electricité renouvelable [4]
- **Run 2 :** Electricité renouvelable [4]
- **Run 3 :** Electricité renouvelable [1, 4]
- **Prod :** (aucun levier)
- Catégories instables sur : Electricité renouvelable

> En théorie, l’énergie hydrolienne mobilisable dans la Manche serait de 3 GW. Pour confirmer ces données dans la pratique, le projet TIGER (Tidal Stream Industry Energise) soutient l’expérimentation et le développement de turbines submergées au large des côtes françaises et anglaises exploitant l’énergie des courants des marées. Le site dit « Paimpol-Bréhat » est intégré au programme pour le volet expérimentation de turbines. Ce parc démonstrateur d’EDF a été autorisé à installer 4 hydroliennes …

#### Fiche 4078 — 5.4 Développer le portage de projets d'énergie citoyenne

- **Run 1 :** Electricité renouvelable [4, 6]
- **Run 2 :** Electricité renouvelable [4, 6]
- **Run 3 :** Electricité renouvelable [4, 5]
- **Prod :** Electricité renouvelable [4, 6]
- Catégories instables sur : Electricité renouvelable

> Les projets citoyens d’énergies renouvelables sont définis par la Charte d’Énergie Partagée et doivent, au-delà du seul bilan énergétique favorable, répondre aux critères suivants : - l’ancrage local d’un société d’exploitation contrôlée par des acteurs locaux et leurs groupements - une gouvernance démocratique et transparence totale sur le fonctionnement et les aspects financiers - la rémunération du capital limitée au profit du réinvestissement, de l’action pédagogique et solidaire - l’engage…

#### Fiche 21895 — Conseiller en Energie Partagé

- **Run 1 :** Sobriété et isolation des bâtiments (tertiaire) [6]
- **Run 2 :** Sobriété et isolation des bâtiments (tertiaire) [5, 6]
- **Run 3 :** Sobriété et isolation des bâtiments (tertiaire) [6]
- **Prod :** Sobriété et isolation des bâtiments (tertiaire) [6]
- Catégories instables sur : Sobriété et isolation des bâtiments (tertiaire)

> Guider les communes dans leurs actions d’économie d’énergie, notamment dans les travaux à engager. Éléments de calendrier : Action sur une dizaine d’années au vu du patrimoine concerné au niveau des communes et de l’Agglomération

#### Fiche 21897 — Création d’un Tiers-lieu écoresponsable à Mazéas

- **Run 1 :** Prévention des déchets [1] | Valorisation matière des déchets [1]
- **Run 2 :** Prévention des déchets [1, 6] | Valorisation matière des déchets [1, 6]
- **Run 3 :** Prévention des déchets [1] | Valorisation matière des déchets [1]
- **Prod :** Prévention des déchets [1] | Valorisation matière des déchets [1]
- Catégories instables sur : Prévention des déchets, Valorisation matière des déchets

> Création d’un tiers-lieu écoresponsable sur le site de l’îlot Mazéas au sein du quartier de la gare de Guingamp : * Recyclerie (logistique, tri, reconditionnement, vente) * Espaces partagés et équipés en matériel pour les artisans * Espaces d’animation, de formation, de création artistique, de loisir * Offre tertiaire en lien avec la proximité de la gare

#### Fiche 21932 — Baie d'armor industrie

- **Run 1 :** Covoiturage [4, 6] | Efficacité et sobriété logistique [4] | Fret décarboné et multimodalité [4] | Production Industrielle [4, 6] | Sobriété foncière [4]
- **Run 2 :** Covoiturage [4, 6] | Efficacité et sobriété logistique [4, 6] | Fret décarboné et multimodalité [4, 6] | Production Industrielle [4, 6] | Sobriété foncière [4]
- **Run 3 :** Covoiturage [6] | Efficacité et sobriété logistique [4] | Fret décarboné et multimodalité [4] | Production Industrielle [4] | Sobriété foncière [6]
- **Prod :** Covoiturage [6] | Production Industrielle [6]
- Catégories instables sur : Covoiturage, Efficacité et sobriété logistique, Fret décarboné et multimodalité, Production Industrielle, Sobriété foncière

> • Mobilités : Coordination des mobilités multimodales et promotion du covoiturage inter-entreprises ; logistique durable. • Habitat : Accessibilité de l’offre de logement pour les travailleurs permanents et saisonniers • Emploi & formation : Impulsion d'une dynamique commune sur l'attractivité des métiers de l'industrie et renforcement des compétences du secteur avec une ouverture à l’insertion des personnes éloignées de l’emploi • Innovation : Développement des filières d’excellence avec un ef…

#### Fiche 31883 — CAE 13. Développer un tourisme durable

- **Run 1 :** Réduction des déplacements [4]
- **Run 2 :** Réduction des déplacements [2]
- **Run 3 :** Réduction des déplacements [2]
- **Prod :** (aucun levier)
- Catégories instables sur : Réduction des déplacements

> La collectivité élabore une stratégie touristique durable prenant en compte de manière intégrée les impacts du tourisme sur les ressources naturelles et les écosystèmes (la pression sur la ressource locale en eau, …), en matière d'émissions GES (notamment liées au transport) et l'accès aux activités touristiques pour tous. Elle prend des mesures pour réduire ces impacts.

## CC Creuse Sud Ouest (4111)

- Fiches : **80** — stables sur les 3 runs : **54** (68%), instables : **26**
- Paires levier × catégorie distinctes proposées : 73 — 3/3 runs : 19, 2/3 runs : 20, 1/3 runs : 34
- Vote majoritaire = prod : 5/30 fiches classées d'un côté ou de l'autre
- Réponses JSON invalides rejouées : 1
- Appels : 12 — tokens d'entrée 56 766 (dont 0 en cache, 0%), sortie 61 886 — coût estimé 0.17 $ pour les 3 runs
- Date : 2026-10-30 12:12

### Classée dans certains runs, aucun levier dans d'autres (10)

#### Fiche 63975 — 2.3.6 Initier un travail avec les acteurs du bâtiment sur les enjeux des transitions

- **Run 1 :** Sobriété et isolation des bâtiments (tertiaire) [4]
- **Run 2 :** (aucun levier)
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété et isolation des bâtiments (tertiaire) (1/3)

> Contexte : Le secteur du bâtiment est un levier majeur de transition, tant en matière d’énergie, de ressources que d’adaptation au changement climatique. À ce jour, les échanges entre ces professionnels et la collectivité restent ponctuels et non structurés. Éléments de calendrier : 2026 : cartographie, premiers échanges, rencontre partenariale 2027 et années suivantes : structuration des suites (groupe, charte, projets pilotes)

#### Fiche 63976 — 2.3.7 Poursuivre et mettre en œuvre les actions du PAT départemental

- **Run 1 :** Bâtiments & Machines agricoles [4] | Changements de pratiques de fertilisation azotée [4] | Elevage durable [4] | Gestion des haies [4] | Gestion des prairies [4] | Pratiques stockantes [4]
- **Run 2 :** (aucun levier)
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Bâtiments & Machines agricoles (1/3), Changements de pratiques de fertilisation azotée (1/3), Elevage durable (1/3), Gestion des haies (1/3), Gestion des prairies (1/3), Pratiques stockantes (1/3)

> Contexte : Le territoire dispose d’un tissu agricole local diversifié, mais la mise en relation entre producteurs, consommateurs et acteurs de la restauration collective reste à renforcer. Éléments de calendrier : 2025 : Participation aux travaux du PAT 2026 et années suivantes : Participation aux travaux du PAT et relais des actions

#### Fiche 63981 — 2.4.5 Réaliser les diagnostics énergétiques de l'ensemble des bâtiments communautaires

- **Run 1 :** (aucun levier)
- **Run 2 :** Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 3 :** Sobriété et isolation des bâtiments (tertiaire) [5]
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété et isolation des bâtiments (tertiaire) (2/3)

> Le contexte : Face aux obligations réglementaires croissantes, Creuse Sud-Ouest est appelée à mieux connaître et piloter la performance énergétique de son patrimoine bâti. Éléments de calendrier : 2025 : Identifier les logements concernés par la démarche 2025-2030 : Réaliser les visites techniques des bâtiments 2026-2045 : Identifier les gains réalisés

#### Fiche 64525 — 1.2.1 Engager le programme des baux à réhabilitation

- **Run 1 :** (aucun levier)
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [3] | Changement chaudières gaz + rénovation (résidentiel) [3] | Sobriété des bâtiments (résidentiel) [3]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [3] | Changement chaudières gaz + rénovation (résidentiel) [3] | Sobriété des bâtiments (résidentiel) [3]
- **Prod :** (aucun levier)
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (2/3), Changement chaudières gaz + rénovation (résidentiel) (2/3), Sobriété des bâtiments (résidentiel) (2/3)

> <p class="!text-base !text-grey-8 font-[Marianne]">Le parc locatif est inexistant et l'urgence à gagner des habitants impose de pouvoir les loger.</p> Éléments de calendrier :

#### Fiche 64526 — 1.2.2 Elaborer un programme d'aide à l'habitat CSO

- **Run 1 :** (aucun levier)
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [3] | Changement chaudières gaz + rénovation (résidentiel) [3] | Sobriété des bâtiments (résidentiel) [3]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [3] | Changement chaudières gaz + rénovation (résidentiel) [3] | Sobriété des bâtiments (résidentiel) [3]
- **Prod :** (aucun levier)
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (2/3), Changement chaudières gaz + rénovation (résidentiel) (2/3), Sobriété des bâtiments (résidentiel) (2/3)

> <p class="!text-base !text-grey-8 font-[Marianne]">La Communauté de Communes s'est doté d'un projet de territoire ambitieux en termes d'accueil et d'attractivité pour gagner des habitants et maintenir l'existant. L'habitat est un levier essentiel.</p> Éléments de calendrier : - 2025 - T3 2026: Diagnostic du besoin en corrélation avec une enquête ménage et enquête auprès des agences immobilières - T4 2026 Evaluation de l’enveloppe financière à mobiliser et articulations avec les dispositifs déjà…

#### Fiche 64545 — 1.4.6 Mettre en place un fond vitrine pour redynamiser les centres bourgs

- **Run 1 :** Sobriété et isolation des bâtiments (tertiaire) [3]
- **Run 2 :** (aucun levier)
- **Run 3 :** (aucun levier)
- **Prod :** Sobriété et isolation des bâtiments (tertiaire) [3]
- Leviers intermittents : Sobriété et isolation des bâtiments (tertiaire) (1/3)

> Le diagnostic ACP sur le Sud Creusois, par une enquête en ligne auprès des commerçants, a identifié des besoins de travaux sur les vitrines. Aucun dispositif de soutien ne cible à ce jour les vitrines, CSO préférant agir sur un programme de rénovation d’énergétique d’ensemble du local commercial. Cette démarche nécessitera d’impliquer également les propriétaires bailleurs de locaux commerciaux, car les exploitants sont locataires. Éléments de calendrier : Calendrier Action annuelle et récurrent…

#### Fiche 64550 — 1.5.2 Préserver la continuité écologique (rivière, forêt, milieux naturels…)

- **Run 1 :** Pratiques stockantes [1]
- **Run 2 :** (aucun levier)
- **Run 3 :** Gestion des forêts et produits bois [1] | Pratiques stockantes [1]
- **Prod :** (aucun levier)
- Leviers intermittents : Gestion des forêts et produits bois (1/3), Pratiques stockantes (2/3)

> Sur le territoire de la collectivité, des milliers d'ouvrages (seuils, étangs, passages busés, ...) impactent la continuité écologique (hydraulique, sédimentaire et piscicole). Instance de gouvernance : En interne : commissions, bureaux et conseils communautaires En externe : comités de pilotages, comités techniques, comités des financeurs, commissions Éléments de calendrier : Selon une programmation annuelle dans le cadre des contrats territoriaux o 12 en 2025 o 8 en 2026 o 3 en 2027 o 9 en 20…

#### Fiche 64551 — 1.5.3 Développer les sports nature

- **Run 1 :** (aucun levier)
- **Run 2 :** Vélo et transport en commun [1]
- **Run 3 :** Vélo et transport en commun [1]
- **Prod :** (aucun levier)
- Leviers intermittents : Vélo et transport en commun (2/3)

> Le territoire de la CCCSO dispose de nombreux circuits communaux et intercommunaux permettant la pratique de certains sports natures telles que la randonnée, le VTT et l’équitation. Les circuits de trail, running, gravel et nautiques (kayak, canoë) ne sont pas présents et méritent d’être développés. Les sports natures incluent de nombreuses disciplines qu’elles soient terrestres (randonnée, VTT, gravel, trail, running, équestre) ou nautiques (kayak, canoé)

#### Fiche 64561 — 3.2.1 Sensibiliser à la consommation responsable

- **Run 1 :** (aucun levier)
- **Run 2 :** Prévention des déchets [6]
- **Run 3 :** Prévention des déchets [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Prévention des déchets (2/3)

> <p class="!text-base !text-grey-8 font-[Marianne]">La collectivité s'est engagée dans un COT et souhaite interroger la consommation d'usages des agents, élus et usagers.</p>

#### Fiche 64570 — 3.3.3 Créer des campagnes de communication avec Creuse Tourisme

- **Run 1 :** (aucun levier)
- **Run 2 :** Vélo et transport en commun [6]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Vélo et transport en commun (1/3)

> Contexte : Creuse Sud-Ouest souhaite développer sa notoriété et son image touristique. La collaboration avec Creuse Tourisme, opérateur départemental de la promotion touristique, demeure un levier fort pour mutualiser les efforts de communication, bénéficier d’un relais professionnel et mieux cibler les touristes. Éléments de calendrier : - 2026 : identification des atouts touristiques du territoire et production d’une revue de presse touristique et d’un guide touristique local de qualité. Renc…

### Levier présent dans certains runs seulement (9)

#### Fiche 63965 — 2.2.1 Optimiser le service public des déchets

- **Run 1 :** Efficacité et sobriété logistique [4] | Prévention des déchets [4] | Valorisation matière des déchets [4]
- **Run 2 :** Efficacité et sobriété logistique [5]
- **Run 3 :** Prévention des déchets [1] | Valorisation matière des déchets [1]
- **Prod :** Prévention des déchets [2, 3] | Valorisation matière des déchets [2, 3]
- Leviers intermittents : Efficacité et sobriété logistique (2/3), Prévention des déchets (2/3), Valorisation matière des déchets (2/3)

> Contexte : Dans le cadre de l'objectif ambitieux de réduire de moitié les déchets par habitant d'ici 2027, Creuse Sud-Ouest a pris une délibération de principe pour réorganiser la collecte des ordures ménagères (OM) et des emballages, en optant pour un système de collecte en porte-à-porte. Éléments de calendrier : 2025 : Lancement de l'étude 2026 : Enquête de dotation de bacs, distribution des équipements 2027 : Déploiement du nouveau schéma de collecte optimisé et expérimentation de la TI Anné…

#### Fiche 63966 — 2.2.2 Mettre en œuvre une nouvelle collecte des déchets avec une tarification incitative

- **Run 1 :** Prévention des déchets [3]
- **Run 2 :** Prévention des déchets [3]
- **Run 3 :** Prévention des déchets [3] | Valorisation matière des déchets [3]
- **Prod :** Prévention des déchets [3]
- Leviers intermittents : Valorisation matière des déchets (1/3)

> Contexte : En 2024, Creuse Sud-Ouest a coordonné une étude mutualisée avec quatre autres EPCI portant sur l’optimisation du service public de gestion des déchets. Les conclusions de cette étude recommandent de coupler la collecte de l’ensemble des flux de déchets en porte-à-porte (objet d’une autre fiche action) et d’instaurer une tarification incitative. Cette action a pour pré requis la réalisation de l'action "2.2.1 Optimiser le service public de gestion des déchets"

#### Fiche 63967 — 2.2.3 Déployer une déchèterie mobile

- **Run 1 :** Réduction des déplacements [1] | Valorisation matière des déchets [1]
- **Run 2 :** Valorisation matière des déchets [1]
- **Run 3 :** Valorisation matière des déchets [1]
- **Prod :** Valorisation matière des déchets [1, 3]
- Leviers intermittents : Réduction des déplacements (1/3)

> Contexte : Le territoire couvert par la régie Creuse Sud-ouest couvre 27 communes et plus de 630 Km2. La collectivité ne dispose que d'une déchèterie dont la position n'est pas centrale. Une proportion importante des habitants est située à plus 20 minutes en voiture de ce service. Éléments de calendrier : 2025 : travail préliminaire sur besoin du territoire et matériel 2026 : acquisition de l'équipement et déploiement Années suivantes : suivi et ajustements

#### Fiche 63968 — 2.2.4 Mettre en œuvre les actions du PLPDMA

- **Run 1 :** Prévention des déchets [4] | Valorisation matière des déchets [4]
- **Run 2 :** Prévention des déchets [4]
- **Run 3 :** Prévention des déchets [4] | Valorisation matière des déchets [4]
- **Prod :** Prévention des déchets [2, 4] | Valorisation matière des déchets [2, 4]
- Leviers intermittents : Valorisation matière des déchets (2/3)

> Contexte : Le PLPDMA 2025-2030 a été adopté en mars 2025. Il fixe des objectifs ambitieux, dont une réduction de 50 % des déchets ménagers et assimilés d’ici 2027. Éléments de calendrier : Les actions sont mise en œuvre selon le planning prévu au PLPDMA

#### Fiche 63969 — 2.2.5 Consolider le travail avec la ressourcerie

- **Run 1 :** Prévention des déchets [4] | Valorisation matière des déchets [4]
- **Run 2 :** Valorisation matière des déchets [4]
- **Run 3 :** Valorisation matière des déchets [4]
- **Prod :** (aucun levier)
- Leviers intermittents : Prévention des déchets (1/3)

> Contexte : Le partenariat entre la collectivité et la ressourcerie locale date de 2015. Ses termes n'ont pas évolués depuis et les comptes-rendus annuels n'ont plus lieux. Éléments de calendrier : 2025 : Refonte de la convention 2026 : Adaptation selon nouvelle situation géographique Années suivantes : travail sur diversification des activités en lien avec les besoins du territoire.

#### Fiche 63971 — 2.3.2 Impulser la valorisation locale des biodéchets (végétaux, alimentaires…)

- **Run 1 :** Biogaz [4] | Prévention des déchets [4] | Valorisation matière des déchets [4]
- **Run 2 :** Biogaz [4]
- **Run 3 :** Valorisation matière des déchets [4]
- **Prod :** Valorisation matière des déchets [1, 4]
- Leviers intermittents : Biogaz (2/3), Prévention des déchets (1/3), Valorisation matière des déchets (2/3)

> Contexte : Si le compostage fait l’objet de fiches actions spécifiques du PLPDMA, la présente action s’attache à développer les exutoires de valorisation des biodéchets sur le territoire. La réalisation du diagnostic territorial d’économie circulaire (objet d’une fiche action) est un prérequis. Éléments de calendrier : 2027 : Identification des besoins, acteurs, constitution du groupe de travail, évaluation des filières 2028 : choix de projets pilotes et montage des dossiers - expérimentation

#### Fiche 63979 — 2.4.3 Réaliser des opérations de rénovation énergétique sur les bâtiments communautaires pour améliorer leur efficacité

- **Run 1 :** Changement de chaudière à fioul (tertiaire) [5] | Changement de chaudière à gaz (tertiaire) [5] | Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 2 :** Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 3 :** Sobriété et isolation des bâtiments (tertiaire) [5]
- **Prod :** Sobriété et isolation des bâtiments (tertiaire) [5]
- Leviers intermittents : Changement de chaudière à fioul (tertiaire) (1/3), Changement de chaudière à gaz (tertiaire) (1/3)

> Contexte : L'enjeu majeur pour réduire la consommation d'énergie, diminuer les coûts et limiter l'impact environnemental Éléments de calendrier : 2026 : Recenser et prioriser le patrimoine concerné 2026-2027 : Réaliser les audits énergétiques et techniques 2028 : Evaluer le potentiel de recours aux énergies renouvelables 2030-2045 : Réaliser les opérations de rénovations énergétiques

#### Fiche 63983 — 2.5.2 Réaliser un schéma directeur des mobilités douces

- **Run 1 :** Réduction des déplacements [2] | Vélo et transport en commun [2]
- **Run 2 :** Vélo et transport en commun [2]
- **Run 3 :** Vélo et transport en commun [2]
- **Prod :** Vélo et transport en commun [2]
- Leviers intermittents : Réduction des déplacements (1/3)

> Contexte : La promotion des mobilités actives (marche, vélo) est un levier essentiel des transitions, de la qualité de vie et de la santé publique. Éléments de calendrier : 2027 : état des lieux, diagnostic partagé, concertation, définition du schéma et fiches action

#### Fiche 64534 — 1.4.2 Impulser la mise en œuvre d'une boucle d'écologie industrielle territoriale (EIT)

- **Run 1 :** Prévention des déchets [4] | Valorisation matière des déchets [4]
- **Run 2 :** Prévention des déchets [4] | Valorisation matière des déchets [4]
- **Run 3 :** Production Industrielle [4] | Prévention des déchets [4] | Valorisation matière des déchets [4]
- **Prod :** (aucun levier)
- Leviers intermittents : Production Industrielle (1/3)

> Contexte : Le territoire de Creuse Sud-Ouest est vaste et les acteurs économiques y sont répartis de façon très diffuse. Pour autant tous gèrent des approvisionnements, de l’énergie et des déchets. Une dynamique d'EIT est un moteur efficace pour la création d'un cluster dédié au réemploi et aux déchets. Éléments de calendrier : 2026 : Diagnostic économie circulaire territorial (cf fiche action 1.4.8) 2027 : Mobilisation des acteurs autour des filières à enjeu et expérimentation 2028 : Suivi et …

### Levier intermittent et catégories instables (2)

#### Fiche 63973 — 2.3.4 Réduire les déplacements, la consommation des flux : énergie, eau, déchets

- **Run 1 :** Prévention des déchets [5] | Réduction des déplacements [5] | Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 2 :** Réduction des déplacements [5, 6] | Sobriété et isolation des bâtiments (tertiaire) [5, 6]
- **Run 3 :** Prévention des déchets [6] | Réduction des déplacements [6] | Sobriété et isolation des bâtiments (tertiaire) [6]
- **Prod :** Prévention des déchets [4, 6] | Réduction des déplacements [4, 6]
- Leviers intermittents : Prévention des déchets (2/3)
- Catégories instables sur : Réduction des déplacements, Sobriété et isolation des bâtiments (tertiaire)

> Contexte : Cette action en complète d’autres déjà engagées sur la rénovation énergétique ou l’optimisation des équipements en mettant l’accent sur le facteur humain : la sobriété repose en grande partie sur les usages, les arbitrages du quotidien et les comportements individuels et collectifs. Éléments de calendrier : 2026 : Réalisation du diagnostic par service et type d'usagers 2027 : Préconisations et sensibilisations 2028 - 2045 : Déploiement et révision

#### Fiche 63985 — 2.5.4 Etudier la potentialité de déploiement d’« aires de mobilités »

- **Run 1 :** Covoiturage [2] | Vélo et transport en commun [2]
- **Run 2 :** Covoiturage [2]
- **Run 3 :** Covoiturage [4]
- **Prod :** Covoiturage [1] | Vélo et transport en commun [1]
- Leviers intermittents : Vélo et transport en commun (1/3)
- Catégories instables sur : Covoiturage

> Contexte : Encourager la pratique de covoiturage et plus généralement, la mobilité douce, passe par la nécessité de rendre désirable la pratique. Ainsi, concevoir des aires multi-services conviviales et interconnectées (physiquement et virtuellement) pourrait être un premier pas vers une plus grande sobriété de la pratique des transports dans un contexte rural ou la voiture reste largement dominante.

### Mêmes leviers, catégories différentes (5)

#### Fiche 46721 — 2.1.1 Se doter d’une feuille de route pour le développement des énergies renouvelables sur le territoire

- **Run 1 :** Electricité renouvelable [4]
- **Run 2 :** Electricité renouvelable [2, 4]
- **Run 3 :** Electricité renouvelable [4]
- **Prod :** Electricité renouvelable [2, 4]
- Catégories instables sur : Electricité renouvelable

> Contexte : La nécessité de développer la production d’Energies Renouvelables génère des impacts positifs et négatifs sur un territoire. Éléments de calendrier : 2024 : Etat des lieux et diagnostic, concertation des communes 2025 : Rédaction de la feuille de route. Etudes de préfaisabilité et projet pilote.

#### Fiche 63927 — 2.1.3 Informer les communes pour développer les EnR sur leur patrimoine

- **Run 1 :** Electricité renouvelable [6]
- **Run 2 :** Electricité renouvelable [4, 6]
- **Run 3 :** Electricité renouvelable [6]
- **Prod :** (aucun levier)
- Catégories instables sur : Electricité renouvelable

> Contexte : Le patrimoine des communes membres représente un levier de production d’énergie renouvelable encore peu mobilisé. Un besoin d’acculturation et d’appui à la décision émerge fortement. Éléments de calendrier : 2025 : 1ere mobilisation des communes sur la thématique des EnR sur leur patrimoine 2027 : Ré interrogation des élus communautaires sur une deuxième vague de préfaisabilité.

#### Fiche 63928 — 2.1.4 Impulser un projet EnR citoyen

- **Run 1 :** Electricité renouvelable [4]
- **Run 2 :** Electricité renouvelable [3, 4]
- **Run 3 :** Electricité renouvelable [4]
- **Prod :** Electricité renouvelable [2, 4]
- Catégories instables sur : Electricité renouvelable

> Contexte : Il n’existe pas de projet EnR citoyen à ce jour sur le territoire de Creuse Sud-Ouest. Éléments de calendrier : 2027 : Identification d’un site propice 2028 : Concertation des acteurs et citoyens 2029 : Structuration du projet et de son financement 2030 : Mise en service

#### Fiche 63984 — 2.5.3 Encourager la mise en place de services itinérants

- **Run 1 :** Réduction des déplacements [6]
- **Run 2 :** Réduction des déplacements [4]
- **Run 3 :** Réduction des déplacements [6]
- **Prod :** Réduction des déplacements [1, 2]
- Catégories instables sur : Réduction des déplacements

> Contexte : Le territoire, caractérisé par un habitat très dispersé et un éloignement relatif des centralités, souffre d’un accès limité aux services essentiels, particulièrement pour les personnes âgées, à mobilité réduite et/ou isolées. Les déplacements étant contraints par des distances importantes et un usage majoritaire de la voiture individuelle, il est nécessaire d’imaginer des solutions alternatives pour rapprocher les services des habitants, tout en favorisant la cohésion sociale et la …

#### Fiche 64535 — 1.4.3 Se doter d'une réserve foncière / immobilier d'entreprise

- **Run 1 :** Sobriété foncière [1]
- **Run 2 :** Sobriété foncière [2, 3]
- **Run 3 :** Sobriété foncière [1]
- **Prod :** (aucun levier)
- Catégories instables sur : Sobriété foncière

> Dans le cadre de sa politique d’accueil attractivité et de sa politique de développement économique, Creuse Sud-Ouest souhaite en complément de sa veille immobilière se doter d’une réserve foncière pour accueillir de nouvelles entreprises sur son territoire. Éléments de calendrier : - 2026 : Diagnostic des friches industrielles et commerciales - 2027 : Réflexion technique et financière sur l'acquisition et la réhabilitation et la remise sur le marché - 2026-2030 : Intégrer les besoins du territ…

## Bordeaux Métropole (4322)

- Fiches : **55** — stables sur les 3 runs : **16** (29%), instables : **39**
- Paires levier × catégorie distinctes proposées : 313 — 3/3 runs : 105, 2/3 runs : 74, 1/3 runs : 134
- Vote majoritaire = prod : 3/37 fiches classées d'un côté ou de l'autre
- Réponses JSON invalides rejouées : 0
- Appels : 9 — tokens d'entrée 61 749 (dont 0 en cache, 0%), sortie 75 653 — coût estimé 0.20 $ pour les 3 runs
- Date : 2026-10-30 12:12

### Classée dans certains runs, aucun levier dans d'autres (6)

#### Fiche 34933 — Action 7. Renforcer la transition énergétique et écologique dans les partenariats avec les communes,  les territoires voisins et à l’international

- **Run 1 :** Electricité renouvelable [4]
- **Run 2 :** (aucun levier)
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Electricité renouvelable (1/3)

> 1. Renforcer le soutien apporté à la transition énergétique et écologique des communes métropolitaines au travers les contrats de CODEV et des règlements d’intervention en mesurant l’impact carbone des projets soutenus et leur contribution au bilan carbone de la Métropole 2. Approfondir ce soutien aux communes en leur offrant la possibilité de participer pleinement à la co construction des stratégies et outils nécessaires à l'atteinte de leurs objectifs de décarbonation. Afin de concrétiser ce …

#### Fiche 34935 — Action 9. Créer une coopérative carbone territoriale en lien avec les territoires voisins

- **Run 1 :** (aucun levier)
- **Run 2 :** Captage de méthane dans les ISDND [3, 4] | Gestion des forêts et produits bois [3, 4] | Pratiques stockantes [3, 4]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Captage de méthane dans les ISDND (1/3), Gestion des forêts et produits bois (1/3), Pratiques stockantes (1/3)

> 1. Mettre en place un groupe de travail réunissant les directions métropolitaines actrices de la transition, le conseil des partenaires et les territoires girondins 2. Définir une stratégie territorialisée de réduction des émissions et de compensation carbone : analyse quantitative du potentiel permettant d’évaluer le périmètre de la coopérative carbone, analyse qualitative avec identification des acteurs locaux, analyse de la demande de compensation et des besoins de réduction des émissions, é…

#### Fiche 34949 — Action 23. Massifier et faire connaître les jardins collectifs

- **Run 1 :** Pratiques stockantes [1, 3, 6]
- **Run 2 :** Pratiques stockantes [1, 2, 3, 6]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Pratiques stockantes (2/3)

> 1. Actualiser la carte des jardins collectifs 2. Soutenir les communes pour la création de jardins partagés au travers du contrat de co-développement 3. Accompagner la vie des jardins partagés au travers du soutien apporté aux associations 4. Développer le maillage de jardins partagés sur le territoire métropolitain avec l’appui de structures partenaires en charge d’accompagner à la création de nouveaux jardins et l’animation de jardins existants 5. Réserver des espaces dans les opérations d’am…

#### Fiche 34951 — Action 25. Créer des îlots de fraîcheur urbains en déminéralisant, désimperméabilisant et végétalisant la ville, et lutter simultanément contre les îlots de chaleur urbains

- **Run 1 :** Pratiques stockantes [1, 2, 6]
- **Run 2 :** Gestion des forêts et produits bois [1, 2] | Pratiques stockantes [1, 2] | Sobriété foncière [1, 2]
- **Run 3 :** (aucun levier)
- **Prod :** Sobriété foncière [1, 2, 6]
- Leviers intermittents : Gestion des forêts et produits bois (1/3), Pratiques stockantes (2/3), Sobriété foncière (1/3)

> 1. Intégrer les recommandations et résultats des études stratégiques : (1)Définir et territorialiser précisément les îlots de fraicheur urbains ainsi que les quartiers à haut risque d’îlots de chaleur urbains, et identifier ceux où les populations sont les plus vulnérables et les plus précaires (2)Etablir et diffuser des préconisations pratiques par type de bâtiments et d’usages du territoire afin de réduire le besoin en refroidissement, inspirées du label du bâtiment frugal bordelais (3)Contin…

#### Fiche 34952 — Action 26. Anticiper les emplois de demain et accompagner les filières économiques émergeantes nécessaires à l’atteinte des objectifs du plan climat

- **Run 1 :** (aucun levier)
- **Run 2 :** (aucun levier)
- **Run 3 :** Fret décarboné et multimodalité [3, 4, 6] | Gestion des forêts et produits bois [4, 6] | Production Industrielle [3, 4, 6] | Prévention des déchets [4, 6] | Valorisation matière des déchets [4, 6]
- **Prod :** (aucun levier)
- Leviers intermittents : Fret décarboné et multimodalité (1/3), Gestion des forêts et produits bois (1/3), Production Industrielle (1/3), Prévention des déchets (1/3), Valorisation matière des déchets (1/3)

> 1. Lancer une étude « état des lieux et perspectives de développement des emplois verts » dans le cadre de la convention entre Bordeaux Métropole et l’A’urba pour anticiper la création des emplois de demain et la formation initiale et continue en lien avec la transition écologique du tissu économique. Coordonner avec la Région Nouvelle-Aquitaine, les ambitions métropolitaine de développement économique et de formation. 2. Massifier les clauses d’insertion dans la commande publique métropolitain…

#### Fiche 34978 — Action 52. Promouvoir un urbanisme durable et favorable à la santé

- **Run 1 :** (aucun levier)
- **Run 2 :** Pratiques stockantes [1] | Sobriété des bâtiments (résidentiel) [6] | Sobriété et isolation des bâtiments (tertiaire) [6]
- **Run 3 :** Electricité renouvelable [2] | Pratiques stockantes [2] | Réduction des déplacements [2]
- **Prod :** (aucun levier)
- Leviers intermittents : Electricité renouvelable (1/3), Pratiques stockantes (2/3), Réduction des déplacements (1/3), Sobriété des bâtiments (résidentiel) (1/3), Sobriété et isolation des bâtiments (tertiaire) (1/3)

> 1. Imposer un référentiel d’aménagement inspiré du label bâtiment frugal bordelais, regroupant l'ensemble des critères à respecter pour les projets d'aménagements permettant de faciliter l'appropriation des enjeux environnementaux par l’ensemble des acteurs concernés (bilan carbone, biodiversité, mobilité, énergies renouvelables, air, …) 2. Systématiser la réalisation de bilan carbone des opérations d’aménagement 3. Multiplier les évaluations d'impact en santé dans les projets d'aménagement pou…

### Levier présent dans certains runs seulement (8)

#### Fiche 34955 — Action 29. Accompagner les acteurs économiques dans l’adoption de process sobres en énergie et en carbone

- **Run 1 :** Electricité renouvelable [6] | Production Industrielle [3, 4, 6] | Prévention des déchets [6] | Sobriété et isolation des bâtiments (tertiaire) [6]
- **Run 2 :** Production Industrielle [3, 4, 6]
- **Run 3 :** Electricité renouvelable [6] | Production Industrielle [3, 4, 6] | Prévention des déchets [6] | Sobriété et isolation des bâtiments (tertiaire) [3, 4, 6]
- **Prod :** Production Industrielle [3, 4, 6]
- Leviers intermittents : Electricité renouvelable (2/3), Prévention des déchets (2/3), Sobriété et isolation des bâtiments (tertiaire) (2/3)

> 1. Co-construire et diffuser un kit d'accompagnement à la transition écologique des acteurs économiques visant à˚: (1)présenter l'offre de service globale de la Métropole sur les thématiques mobilités, 1M d’arbres, rénovation énergétique, étudier techniquement et économiquement l’installation de panneaux photovoltaïques, numérique responsable, déchets, … (2)accélérer et amplifier le passage à l'acte des entreprises (3)optimiser la prospection et la promotion des dispositifs d'accompagnement de …

#### Fiche 34959 — Action 33. Renforcer l’exemplarité des pratiques métropolitaines

- **Run 1 :** Electricité renouvelable [5] | Gestion des forêts et produits bois [5] | Pratiques stockantes [5] | Prévention des déchets [5] | Sobriété et isolation des bâtiments (tertiaire) [5] | Valorisation matière des déchets [5]
- **Run 2 :** Electricité renouvelable [5] | Gestion des forêts et produits bois [5] | Prévention des déchets [5] | Sobriété et isolation des bâtiments (tertiaire) [5] | Valorisation matière des déchets [5]
- **Run 3 :** Electricité renouvelable [5] | Gestion des forêts et produits bois [5] | Prévention des déchets [5] | Sobriété et isolation des bâtiments (tertiaire) [5] | Valorisation matière des déchets [5]
- **Prod :** Electricité renouvelable [5] | Sobriété et isolation des bâtiments (tertiaire) [5]
- Leviers intermittents : Pratiques stockantes (1/3)

> 1. Mettre en place une démarche interne visant à définir des axes d’amélioration des pratiques des directions métropolitaines et valoriser les résultats obtenus 2. Evaluer les volumes de consommations à venir des matériaux dans le cadre des marchés publics ou projets d'aménagement portés par Bordeaux Métropole afin de donner des perspectives claires aux entreprises et leur montrer qu'il y a un marché potentiel "assuré" 3. Mettre en œuvre le schéma de promotion des achats publics socialement et …

#### Fiche 34961 — Action 35. Amplifier l'usage du vélo

- **Run 1 :** Réduction des déplacements [1, 3, 4, 6] | Vélo et transport en commun [1, 3, 4, 6]
- **Run 2 :** Vélo et transport en commun [1, 3, 4, 6]
- **Run 3 :** Réduction des déplacements [1, 3, 4, 6] | Vélo et transport en commun [1, 3, 4, 6]
- **Prod :** Vélo et transport en commun [1, 3, 5, 6]
- Leviers intermittents : Réduction des déplacements (2/3)

> 1. Développer un réseau cyclable performant grâce au réseau vélo express (ReVE), à l’entretien et au développement des aménagements cyclables, à une mise à jour du guide des aménagements cyclables, à un jalonnement d’itinéraires cyclables 2. Permettre de stationner son vélo en toute sécurité par le déploiement d’arceaux vélos, le développement d’offre de stationnement vélo sécurisé et l’amélioration des locaux à vélos dans les constructions neuves 3. Développer les services autour du vélo notam…

#### Fiche 34962 — Action 36. Favoriser la pratique de la marche

- **Run 1 :** Réduction des déplacements [1, 2, 6]
- **Run 2 :** Vélo et transport en commun [1, 2, 6]
- **Run 3 :** Réduction des déplacements [1, 2, 6]
- **Prod :** Vélo et transport en commun [1, 2, 6]
- Leviers intermittents : Réduction des déplacements (2/3), Vélo et transport en commun (1/3)

> 1. Concevoir un espace public plus marchable par la mise en œuvre de zones marchables, le désencombrement des trottoirs, l’intégration dans les documents de planification, l’élaboration de plan d’accessibilité de la voirie et des espaces publics, la mise en conformité des passages piétons 2. Favoriser des déplacements scolaires piétons autonomes par l’expérimentation de fermeture de rues d’écoles, d’incitation à l’écomobilité scolaire (pédibus, vélobus) 3. Articuler la marche et les transports …

#### Fiche 34966 — Action 40. Définir une zone à Faibles Emissions mobilité

- **Run 1 :** Efficacité et carburants décarbonés des véhicules privés [2, 4, 6] | Véhicules électriques [2, 4, 6]
- **Run 2 :** Efficacité et carburants décarbonés des véhicules privés [2, 4, 6]
- **Run 3 :** Efficacité et carburants décarbonés des véhicules privés [2, 4, 6] | Réduction des déplacements [2, 4] | Véhicules électriques [3, 4]
- **Prod :** Efficacité et carburants décarbonés des véhicules privés [2, 3] | Véhicules électriques [2, 3] | Vélo et transport en commun [1, 2]
- Leviers intermittents : Réduction des déplacements (1/3), Véhicules électriques (2/3)

> 1. Déploiement d’une concertation ciblée (acteurs économiques, associatifs, acteurs de la santé, institutionnels) au premier semestre 2022 2. Mise en place d’une signalétique adaptée aux abords de la rocade notamment en 2023 3. Déploiement du dispositif de contrôle à partir de fin 2023 (travail avec l’Etat sur le contrôle semi-automatisé 4. Mettre en place un dispositif de suivi avec une gouvernance associée pour apporter les ajustements nécessaires dans le déploiement de la ZFE-m 5. Mettre en …

#### Fiche 34970 — Action 44. Accompagner la transition vers des usages plus sobres en énergie

- **Run 1 :** Sobriété des bâtiments (résidentiel) [4, 6] | Sobriété et isolation des bâtiments (tertiaire) [4, 6]
- **Run 2 :** Sobriété des bâtiments (résidentiel) [4, 6] | Sobriété et isolation des bâtiments (tertiaire) [4, 6]
- **Run 3 :** Réseaux de chaleur décarbonés [6] | Sobriété des bâtiments (résidentiel) [4, 6] | Sobriété et isolation des bâtiments (tertiaire) [4, 6]
- **Prod :** Sobriété des bâtiments (résidentiel) [6] | Sobriété et isolation des bâtiments (tertiaire) [6]
- Leviers intermittents : Réseaux de chaleur décarbonés (1/3)

> 1. Réaliser une vaste étude d’identification et d’évaluation des principaux postes de consommations d’énergie au sein des ménages et des entreprises. 2. Concevoir un panel de solutions permettant de réduire les consommations identifiées 3. Définir une feuille de route sobriété en rappelant les postes de consommations identifiés, les leviers comportementaux envisagés pour les réduire et détaillant l’ensemble des dispositifs d’accompagnement à bâtir pour accompagner ces changements 4. Réaliser un…

#### Fiche 34973 — Action 47. Lutter contre le gaspillage alimentaire

- **Run 1 :** Prévention des déchets [4, 6]
- **Run 2 :** Prévention des déchets [4, 6]
- **Run 3 :** Prévention des déchets [4, 6] | Valorisation matière des déchets [4]
- **Prod :** Prévention des déchets [1, 5, 6]
- Leviers intermittents : Valorisation matière des déchets (1/3)

> 1. Poursuivre les engagements d'accompagnement des communes dans la lutte contre le gaspillage alimentaire en milieu scolaire et sensibiliser les restaurateurs 2. Déployer des frigos anti-gaspillage 3. Créer et animer un groupement de commandes des restes alimentaires pour les acteurs publics de la Métropole 4. Encourager la lutte contre le gaspillage alimentaire dans les marchés de traiteurs et l’organisation de manifestations

#### Fiche 34977 — Action 51. Renforcer la prise en compte des thématiques Climat-Air-Energie-Carbone dans les documents d’urbanisme

- **Run 1 :** Pratiques stockantes [2] | Réduction des déplacements [2] | Sobriété foncière [2]
- **Run 2 :** Electricité renouvelable [2] | Pratiques stockantes [2] | Réduction des déplacements [2] | Sobriété foncière [2]
- **Run 3 :** Electricité renouvelable [2] | Pratiques stockantes [2] | Réduction des déplacements [2] | Sobriété foncière [2]
- **Prod :** Réduction des déplacements [2] | Sobriété foncière [2]
- Leviers intermittents : Electricité renouvelable (2/3)

> 1. Intégrer dans le PLUi les objectifs climat-air-énergie-carbone au moyen d’OAP thématiques (énergies renouvelables, carbone, biodiversité, climat, agriculture) 2. Evaluer et renforcer le PLUi pour améliorer sa contribution à l’adaptation au changement climatique. 3. Dans les orientations stratégiques du PLU et du SCOT, favoriser la création de logements au plus près des lieux d’activités économiques pour limiter les déplacements domicile-travail et concevoir systématiquement des nouveaux quar…

### Levier intermittent et catégories instables (17)

#### Fiche 34943 — Action 17. Développer la production de chaleur et de froid renouvelables et locaux

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [3, 6] | Réseaux de chaleur décarbonés [1, 4]
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [3, 6] | Changement chaudières gaz + rénovation (résidentiel) [3, 6] | Changement de chaudière à fioul (tertiaire) [3, 5] | Changement de chaudière à gaz (tertiaire) [3, 5] | Réseaux de chaleur décarbonés [1, 3]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [3, 6] | Réseaux de chaleur décarbonés [1, 2]
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [3, 6] | Changement chaudières gaz + rénovation (résidentiel) [3, 6] | Changement de chaudière à fioul (tertiaire) [3, 6] | Changement de chaudière à gaz (tertiaire) [3, 6] | Réseaux de chaleur décarbonés [1, 3]
- Leviers intermittents : Changement chaudières gaz + rénovation (résidentiel) (1/3), Changement de chaudière à fioul (tertiaire) (1/3), Changement de chaudière à gaz (tertiaire) (1/3)
- Catégories instables sur : Réseaux de chaleur décarbonés

> 1. Etudier les réseaux de chaleur dans tous les quartiers présentant une densité thermique suffisante et définir une stratégie et un plan d’action spécifique aux réseaux de froid adapté aux différentes typologie de quartiers et de bâtiments 2. Réaliser tous les projets de réseau de chaleur présentant une faisabilité technico-économique, en gestion en régie ou déléguée. 3. "Proposer des équipements performants et décarbonés à fort taux d’énergie renouvelable adaptés à chaque cible (industrie, te…

#### Fiche 34948 — Action 22. Soutenir un modèle agricole économiquement viable, socialement et écologiquement responsable

- **Run 1 :** Bâtiments & Machines agricoles [1, 3] | Changements de pratiques de fertilisation azotée [6] | Pratiques stockantes [6] | Sobriété foncière [2]
- **Run 2 :** Bâtiments & Machines agricoles [1, 3] | Changements de pratiques de fertilisation azotée [6] | Gestion des haies [6] | Pratiques stockantes [6] | Sobriété foncière [2, 3]
- **Run 3 :** Pratiques stockantes [4, 6] | Sobriété foncière [2]
- **Prod :** Gestion des haies [3, 4, 6] | Pratiques stockantes [3, 4, 6] | Sobriété foncière [2]
- Leviers intermittents : Bâtiments & Machines agricoles (2/3), Changements de pratiques de fertilisation azotée (2/3), Gestion des haies (1/3)
- Catégories instables sur : Pratiques stockantes, Sobriété foncière

> 1. Adopter et mettre en œuvre une politique foncière agricole et naturelle métropolitaine de maintien du foncier agricole existant 2. Encourager le développement d'initiatives d'agriculture urbaine et périurbaine sur la Métropole sobres en énergie, en eau et respectueuses de l’environnement (qualité de l’air) 3. Accompagner et faciliter l'installation de nouveaux agriculteurs dans les projets en agriculture biologique et en circuits courts de proximité en s'appuyant sur le tissu agricole exista…

#### Fiche 34950 — Action 24. Protéger, valoriser et diversifier les espaces forestiers existants et mettre en œuvre le projet « 1 million d’arbres »

- **Run 1 :** Gestion des forêts et produits bois [1, 2, 4] | Gestion des haies [2, 6] | Pratiques stockantes [1, 6]
- **Run 2 :** Gestion des forêts et produits bois [1, 2, 3, 4] | Gestion des haies [1, 2] | Pratiques stockantes [1, 2]
- **Run 3 :** Gestion des forêts et produits bois [1, 2, 3, 4, 6] | Gestion des haies [1, 2, 6]
- **Prod :** Gestion des forêts et produits bois [1, 2, 4, 6] | Gestion des haies [1, 2, 4, 6]
- Leviers intermittents : Pratiques stockantes (2/3)
- Catégories instables sur : Gestion des forêts et produits bois, Gestion des haies

> 1. Adopter une Stratégie métropolitaine en faveur de la forêt pour protéger le patrimoine existant et poursuivre son développement et mettre en place une charte de la forêt métropolitaine en coopération avec les communes et l’écosystème des acteurs de sa préservation (privés/particuliers, acteurs institutionnels et économiques, bailleurs et gestionnaires…) (1)Mettre en œuvre les actions de la charte forestière de territoire (2)Mobiliser et mettre en réseau sur le territoire l’ensemble des acteu…

#### Fiche 34953 — Action 27. Accompagner les projets d’écologie industrielle territoriale (EIT)

- **Run 1 :** Prévention des déchets [3, 4, 6] | Valorisation matière des déchets [3, 4, 6]
- **Run 2 :** Production Industrielle [4, 6] | Prévention des déchets [4, 6] | Valorisation matière des déchets [4, 6]
- **Run 3 :** Production Industrielle [3, 4] | Prévention des déchets [3, 4, 6] | Valorisation matière des déchets [3, 4, 6]
- **Prod :** Prévention des déchets [3, 4] | Valorisation matière des déchets [3, 4]
- Leviers intermittents : Production Industrielle (2/3)
- Catégories instables sur : Prévention des déchets, Valorisation matière des déchets

> 1. Participer au déploiement de l’économie de la fonctionnalité et de l’usage et de l’économie collaborative par l’innovation et l’expérimentation notamment en lançant un appel à manifestation d’intérêt dans le cadre du Bordeaux Métropole City Lab 2. Mettre en place sur le territoire des rencontres dédiées à la coopération et à la circularité entre entreprises permettant à ces dernières de développer de nouveaux marchés, d’optimiser leurs coûts et de réduire leurs consommations de ressources 3.…

#### Fiche 34954 — Action 28. Faire de Bordeaux une destination durable reconnue

- **Run 1 :** Changements de pratiques de fertilisation azotée [6] | Elevage durable [6] | Prévention des déchets [6] | Réduction des déplacements [4, 6] | Véhicules électriques [1]
- **Run 2 :** Prévention des déchets [6] | Sobriété et isolation des bâtiments (tertiaire) [6] | Vélo et transport en commun [6]
- **Run 3 :** Prévention des déchets [4, 6] | Réduction des déplacements [4, 6]
- **Prod :** Véhicules électriques [1]
- Leviers intermittents : Changements de pratiques de fertilisation azotée (1/3), Elevage durable (1/3), Réduction des déplacements (2/3), Sobriété et isolation des bâtiments (tertiaire) (1/3), Véhicules électriques (1/3), Vélo et transport en commun (1/3)
- Catégories instables sur : Prévention des déchets

> 2. Accompagner les professionnels du tourisme dans une meilleure gestion de leurs déchets et de l’énergie au travers de la charte des établissements hôteliers 3. Renforcer les circuits courts dans les métiers de l’HCR (hôtellerie, café et restauration) et dans les visites organisées ou dans les produits proposés à la boutique OTCBM 4. Accompagner la filière oenotouristique dans la valorisation des pratiques viticoles durables 5. Communiquer de façon positive sur un comportement responsable, en …

#### Fiche 34956 — Action 30. Privilégier les matériaux moins polluants (biosourcés, issus du réemploi, bas carbone), pour toutes les filières économiques

- **Run 1 :** Gestion des forêts et produits bois [3, 6] | Pratiques stockantes [3, 6] | Prévention des déchets [2, 3, 6] | Valorisation matière des déchets [2, 3, 6]
- **Run 2 :** Gestion des forêts et produits bois [5, 6] | Production Industrielle [5, 6] | Prévention des déchets [2, 6] | Valorisation matière des déchets [3, 5, 6]
- **Run 3 :** Gestion des forêts et produits bois [2, 3, 6] | Pratiques stockantes [2, 6] | Production Industrielle [2, 3, 4, 6] | Prévention des déchets [2, 3, 6] | Valorisation matière des déchets [2, 3, 6]
- **Prod :** Valorisation matière des déchets [2, 5, 6]
- Leviers intermittents : Pratiques stockantes (2/3), Production Industrielle (2/3)
- Catégories instables sur : Gestion des forêts et produits bois, Prévention des déchets, Valorisation matière des déchets

> 1. Lancer une étude pour caractériser les ressources pouvant être considérées comme matériaux moins polluants et identifier les besoins en développement de filières. Pour ce faire, Bordeaux Métropole évaluera sur ses constructions et dans le cadre des opérations d’aménagement à venir, ses consommations en matériaux de manière à offrir aux entreprises des potentiels de développement de ces marchés 2. Sensibiliser les entreprises sur le recours aux matériaux moins polluants dans leur process au t…

#### Fiche 34958 — Action 32. Réduire l’impact environnemental des constructions

- **Run 1 :** Gestion des forêts et produits bois [1, 2, 5, 6] | Pratiques stockantes [1, 2, 5] | Production Industrielle [4, 6] | Prévention des déchets [1, 2, 5, 6]
- **Run 2 :** Gestion des forêts et produits bois [1, 2, 5, 6] | Production Industrielle [3, 4] | Prévention des déchets [2, 6] | Valorisation matière des déchets [1, 2, 5]
- **Run 3 :** Gestion des forêts et produits bois [1, 2, 5] | Pratiques stockantes [1, 2, 5] | Production Industrielle [1, 2, 4, 5] | Prévention des déchets [1, 2, 5] | Valorisation matière des déchets [1, 2, 5]
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [1, 2, 6] | Changement chaudières gaz + rénovation (résidentiel) [1, 2, 6] | Sobriété et isolation des bâtiments (tertiaire) [1, 2, 5, 6]
- Leviers intermittents : Pratiques stockantes (2/3), Valorisation matière des déchets (2/3)
- Catégories instables sur : Gestion des forêts et produits bois, Production Industrielle, Prévention des déchets

> 1. Au travers des opérations d’aménagement métropolitaines, renforcer la production de bâtiments en recourant aux matériaux biosourcés et géosourcés en lien avec les référentiels et labels Odéys, « bâtiment frugal bordelais » pour viser a minima 2 ouvrages par type de famille de construction 2. Imposer la prise en compte des matériaux biosourcés, géosourcés et issus du réemploi dans les documents de planification (PLU, PLH, SCOT) pour limiter le recours systématique aux matériaux carbonés et/ou…

#### Fiche 34960 — Action 34. Améliorer l'offre de transport en commun

- **Run 1 :** Réduction des déplacements [1, 4] | Vélo et transport en commun [1, 4]
- **Run 2 :** Vélo et transport en commun [1, 3]
- **Run 3 :** Réduction des déplacements [1, 3] | Vélo et transport en commun [1, 3]
- **Prod :** Vélo et transport en commun [1, 3]
- Leviers intermittents : Réduction des déplacements (2/3)
- Catégories instables sur : Vélo et transport en commun

> 1. Développer les cars express qui relient les habitations en périphérie aux bassins d’emplois (ex. Bordeaux –Cenon) 2. Développer le RER métropolitain par application de la feuille de route partenariale (Etat, Région, Département, Métropole, SNCF) 3. Améliorer le réseau de TBM existant et le développer : extension de la ligne A du tramway, amélioration et développement du réseau de bus-express 4. Proposer des offres tarifaires attractives de transports en commun pour les touristes « Pack Accue…

#### Fiche 34963 — Action 37. Développer les usages partagés de l'automobile

- **Run 1 :** Covoiturage [1, 4, 6] | Réduction des déplacements [1, 4, 6]
- **Run 2 :** Covoiturage [1, 4, 6]
- **Run 3 :** Covoiturage [1, 6] | Réduction des déplacements [1, 6]
- **Prod :** Covoiturage [1, 4, 6]
- Leviers intermittents : Réduction des déplacements (2/3)
- Catégories instables sur : Covoiturage

> 1. Développer le covoiturage pour les déplacements de moyenne et longue distance grâce à un plan coordonné multipartenarial de covoiturage afin de développer les voies réservées au covoiturage, les aires de covoiturage 2. Développer l’autopartage en incitant les communes à dédier des voiries, en proposant aux gestionnaires de parkings ouverts de créer des places réservées, en expérimentant un service d’autopartage dans des opérations immobilières mixtes et en sensibilisant les salariés des entr…

#### Fiche 34965 — Action 39. Favoriser les circuits courts et adapter la logistique urbaine pour la rendre plus efficiente

- **Run 1 :** Efficacité et sobriété logistique [2, 4] | Fret décarboné et multimodalité [1, 2, 4]
- **Run 2 :** Efficacité et sobriété logistique [1, 6] | Fret décarboné et multimodalité [1, 3, 4]
- **Run 3 :** Efficacité et sobriété logistique [2, 4, 6] | Fret décarboné et multimodalité [1, 2, 4, 6] | Réduction des déplacements [2, 6]
- **Prod :** Efficacité et sobriété logistique [1, 2, 4] | Fret décarboné et multimodalité [4]
- Leviers intermittents : Réduction des déplacements (1/3)
- Catégories instables sur : Efficacité et sobriété logistique, Fret décarboné et multimodalité

> 1. Elaborer un Plan logistique urbaine à l'échelle métropolitaine et avec les territoires voisins permettant d'organiser les livraisons des derniers kilomètres, d'organiser la circulation poids-lourds et de réguler les horaires d'accès 2. Expérimenter un tarif spécifique poids lourds en heure de pointe sur les autoroutes d'approche 3. Contractualiser avec la SNCF/Région et l’Etat le lancement d'une étude de diagnostic et remise en état du site de triage (fret ferroviaire) d'Hourcade 4. Favorise…

#### Fiche 34968 — Action 42. Rénover et décarboner les logements de la Métropole

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [3, 6] | Changement chaudières gaz + rénovation (résidentiel) [3, 6] | Sobriété des bâtiments (résidentiel) [3, 6]
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [3, 6] | Changement chaudières gaz + rénovation (résidentiel) [3, 6] | Sobriété des bâtiments (résidentiel) [3, 6]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [3, 4, 6] | Changement chaudières gaz + rénovation (résidentiel) [3, 4, 6] | Electricité renouvelable [3, 6] | Sobriété des bâtiments (résidentiel) [3, 4, 6]
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [2, 3, 6] | Changement chaudières gaz + rénovation (résidentiel) [2, 3, 6]
- Leviers intermittents : Electricité renouvelable (1/3)
- Catégories instables sur : Changement chaudières fioul + rénovation (résidentiel), Changement chaudières gaz + rénovation (résidentiel), Sobriété des bâtiments (résidentiel)

> 1. Engager un plan de communication pour faire connaître l'ambition (11 500 logements rénovés par an) et l'accompagnement mis en œuvre par la Métropole 2. Mener une campagne de sensibilisation à destination des ménages dont le logement est identifié comme passoire thermique 3. Veiller au développement sur le territoire de Bordeaux Métropole d'une offre de qualité de conseillers "Mon 4. Accompagnateur Rénov" et soutenir le financement des prestations via ses règlements d'intervention 5. Faire év…

#### Fiche 34971 — Action 45. Promouvoir les nouvelles formes d’habiter

- **Run 1 :** Sobriété foncière [1, 2, 5, 6]
- **Run 2 :** Sobriété foncière [2, 4, 5, 6]
- **Run 3 :** Pratiques stockantes [1, 6] | Sobriété des bâtiments (résidentiel) [2, 5, 6] | Sobriété foncière [1, 2, 5, 6]
- **Prod :** Sobriété des bâtiments (résidentiel) [1, 5, 6] | Sobriété et isolation des bâtiments (tertiaire) [1, 5, 6] | Sobriété foncière [1, 5]
- Leviers intermittents : Pratiques stockantes (1/3), Sobriété des bâtiments (résidentiel) (1/3)
- Catégories instables sur : Sobriété foncière

> 1. Identifier les espaces disponibles du territoire : bureaux vacants, logements vacants, résidences secondaires, locaux sous-utilisés 2. Interroger systématiquement l’acte de construction en imposant ce principe issu du label du bâtiment frugal bordelais 3. Être exemplaire dans les opérations d’aménagement ou sur patrimoine public dans l’optimisation et la mutualisation des espaces 4. Intensifier et développer les outils de mise à disposition de locaux inutilisés des collectivités à dispositio…

#### Fiche 34972 — Action 46. Pour une alimentation locale, de qualité, bio, plus végétale et accessible pour toutes et tous

- **Run 1 :** Bâtiments & Machines agricoles [6] | Changements de pratiques de fertilisation azotée [3, 4, 6] | Efficacité et sobriété logistique [4, 6] | Elevage durable [3, 4, 6] | Réduction des déplacements [3, 6]
- **Run 2 :** Changements de pratiques de fertilisation azotée [6] | Efficacité et sobriété logistique [4, 6] | Elevage durable [6]
- **Run 3 :** Bâtiments & Machines agricoles [4, 6] | Changements de pratiques de fertilisation azotée [4, 6] | Efficacité et sobriété logistique [4, 6] | Elevage durable [4, 6] | Fret décarboné et multimodalité [1, 4, 6] | Gestion des prairies [6] | Pratiques stockantes [6]
- **Prod :** Efficacité et sobriété logistique [6]
- Leviers intermittents : Bâtiments & Machines agricoles (2/3), Fret décarboné et multimodalité (1/3), Gestion des prairies (1/3), Pratiques stockantes (1/3), Réduction des déplacements (1/3)
- Catégories instables sur : Changements de pratiques de fertilisation azotée, Elevage durable

> 1. Consolider et accompagner les initiatives de sensibilisation du grand public et des scolaires à une alimentation plus locale, de qualité, notamment bio, végétale et équitable. 2. Accompagner et former les employés de la restauration collective à la végétalisation des menus en travaillant avec des nutritionnistes à des menus intégrant des protéines végétales diversifiées pour proposer dans un chaque commune des repas végétariens dont le nombre sera défini dans le cadre de la stratégie de rési…

#### Fiche 34974 — Action 48. Eviter les emballages jetables

- **Run 1 :** Prévention des déchets [2, 5, 6] | Valorisation matière des déchets [6]
- **Run 2 :** Prévention des déchets [2, 5, 6]
- **Run 3 :** Prévention des déchets [1, 2, 5, 6]
- **Prod :** Prévention des déchets [1, 2, 5, 6]
- Leviers intermittents : Valorisation matière des déchets (1/3)
- Catégories instables sur : Prévention des déchets

> 1. Engager un travail législatif pour une réduction et/ou une interdiction de mise sur le marché des emballages et des suremballages et supprimer les plastiques à usage unique sur le territoire de Bordeaux Métropole 2. Sensibiliser les grandes et moyennes surfaces (GMS) sur la réduction à la source des emballages 3. Encourager l’implantation des épiceries de vrac sans emballage jetable 4. Mettre en place les extensions de consignes de tri élargies à l’ensemble des emballages (films plastiques, …

#### Fiche 34976 — Action 50. Privilégier le réemploi pour donner une 2ème vie aux objets

- **Run 1 :** Prévention des déchets [1, 3, 4, 5, 6] | Valorisation matière des déchets [1, 3, 4, 5, 6]
- **Run 2 :** Valorisation matière des déchets [1, 3, 4, 5]
- **Run 3 :** Prévention des déchets [1, 3, 4, 5] | Valorisation matière des déchets [1, 3, 4, 5]
- **Prod :** Prévention des déchets [1, 3, 5, 6]
- Leviers intermittents : Prévention des déchets (2/3)
- Catégories instables sur : Valorisation matière des déchets

> 1. Etudier la mise en place d'un « Allo 2nde vie » en partenariat avec des associations 2. Accompagner techniquement la structuration du réseau des ressourceries à l'échelle métropolitaine 3. Participer à la réalisation du projet Ikos (village du réemploi) en apportant un soutien technique et financier aux porteurs du projet 4. Développer les boites à dons dans les lieux ouverts au public D’ici à 2028, mettre en place six aires de réemploi éphémères installées temporairement à fréquence réguliè…

#### Fiche 34979 — Action 53. Sanctuariser les puits de carbone et les zones à enjeux pour la biodiversité en renforçant la place de la nature et en appliquant le principe « zéro artificialisation nette » (ZAN)

- **Run 1 :** Gestion des forêts et produits bois [1, 6] | Gestion des haies [1, 6] | Pratiques stockantes [1, 2, 6] | Sobriété foncière [2]
- **Run 2 :** Gestion des haies [1, 2] | Pratiques stockantes [1, 2] | Sobriété foncière [2]
- **Run 3 :** Gestion des forêts et produits bois [2] | Gestion des haies [1, 2] | Pratiques stockantes [1, 2] | Sobriété foncière [1, 2]
- **Prod :** Gestion des haies [1, 2] | Pratiques stockantes [1] | Sobriété foncière [1, 2]
- Leviers intermittents : Gestion des forêts et produits bois (2/3)
- Catégories instables sur : Gestion des haies, Pratiques stockantes, Sobriété foncière

> 1. Au travers des documents de planification urbaine, renforcer et sanctuariser la place des espaces naturels favorables à la biodiversité (modification du classement des zonages, classement des arbres, renforcement des espaces réservés au développement de l’agriculture, intégration au plan de zonage des zones humides et des enjeux écologiques, renforcement des haies séparatives…) 2. Créer des sous-zonage pour identifier les espaces agricoles, naturels et forestiers présentant un fort enjeu de …

#### Fiche 34980 — Action 54. Concilier aménagement de la métropole et gestion des milieux aquatiques et des zones humides.

- **Run 1 :** Pratiques stockantes [1, 2]
- **Run 2 :** Pratiques stockantes [1]
- **Run 3 :** Pratiques stockantes [1] | Sobriété foncière [1]
- **Prod :** Sobriété foncière [1]
- Leviers intermittents : Sobriété foncière (1/3)
- Catégories instables sur : Pratiques stockantes

> 1. Construire des stratégies pour répondre aux futures crises causées par l’inondation fluviomaritime : (1)Définir des scénarios de crises en cas d’inondation fluviomaritime (2)Actualiser la connaissance de l’aléa inondation fluviomaritime sous changement climatique en intégrant un évènement « fréquent » et actualiser les documents de gestion du risque sur cette base (3)Organiser et animer un exercice de prospective pour définir une stratégie de gestion du risque d’inondation fluviomaritime à m…

### Mêmes leviers, catégories différentes (8)

#### Fiche 34944 — Action 18. Développer la production d'électricité renouvelable et locale

- **Run 1 :** Electricité renouvelable [1, 5, 6]
- **Run 2 :** Electricité renouvelable [1, 2, 5, 6]
- **Run 3 :** Electricité renouvelable [1, 6]
- **Prod :** Electricité renouvelable [1, 5, 6]
- Catégories instables sur : Electricité renouvelable

> 1. "Développer les installations photovoltaïques sur ombrières : (1) Objectif de 100 MWc installés à l’horizon 2028 (production de 105 GWh) puis 160 MWc à long terme (2) Privilégier les installations de grande taille (plus de 5 000m²) et a minima sur des parkings de plus de 1 500m² (projets de plus de 100 kWc). (3)Equilibrer les objectifs énergétiques et les objectifs écologiques : équiper à terme environ 60% des parkings d’ombrières photovoltaïques (et 85% des parkings de plus de 5 000 m²), et…

#### Fiche 34945 — Action 19. Valoriser la récupération de chaleur issue de l'industrie

- **Run 1 :** Réseaux de chaleur décarbonés [4]
- **Run 2 :** Réseaux de chaleur décarbonés [1, 4]
- **Run 3 :** Réseaux de chaleur décarbonés [4, 6]
- **Prod :** Réseaux de chaleur décarbonés [1, 4]
- Catégories instables sur : Réseaux de chaleur décarbonés

> 1. Localiser les sites industriels mettant en jeu des procédés dégageant des quantités importantes de chaleur (fours, chaudières, incinérateurs, turbines…), notamment dans le cadre d’un travail partenarial global avec les plus gros consommateurs d’énergie du territoire (« palmarès ») situés principalement le long de la Garonne (Ambès, Bègles, Bassens) : industries de l’aéronautique, du spatial et de la défense, industrie pharmaceutique, industries agroalimentaires... L’accompagnement ciblera da…

#### Fiche 34946 — Action 20. Développer la production locale de gaz renouvelable

- **Run 1 :** Biogaz [1, 4]
- **Run 2 :** Biogaz [1, 2, 4]
- **Run 3 :** Biogaz [1, 4, 6]
- **Prod :** Biogaz [1, 4]
- Catégories instables sur : Biogaz

> 1. Développer des projets de méthanisation sur les stations d'épuration de Bordeaux Métropole pour injecter a minima 50 GWh de biogaz d’ici 2026 2. Valoriser 50% a minima de la collecte des biodéchets en production de biogaz à 2028 3. Développer un méthaniseur industriel de 30 GWh d’ici 2026 : projet Cap vert énergie sur le port avec du biogaz injecté dans le réseau 4. Etudier et engager le développement de deux projets de méthaniseurs de 30GWh à l’horizon 2032 et 2038 avec les territoires vois…

#### Fiche 34957 — Action 31. Réduire la production des déchets

- **Run 1 :** Prévention des déchets [2, 3, 4, 6] | Valorisation matière des déchets [6]
- **Run 2 :** Prévention des déchets [3, 4, 6] | Valorisation matière des déchets [6]
- **Run 3 :** Prévention des déchets [2, 3, 6] | Valorisation matière des déchets [6]
- **Prod :** Prévention des déchets [2, 3, 6] | Valorisation matière des déchets [6]
- Catégories instables sur : Prévention des déchets

> 1. Développer les actions de sensibilisation et d'animation à destination de tous les publics sur l'ensemble des thématiques zéro déchet zéro gaspillage (évènements zéro déchets, communications de proximité, Juniors du développement durable, etc.) 2. Réduire les déchets des entreprises : information sur leurs obligations réglementaires, mise à disposition d'outils et mise en place d'un réseau d'entreprise 3. Accompagner les communes vers des actions de réduction des déchets auprès de leurs habi…

#### Fiche 34964 — Action 38. Décarboner les véhicules motorisés

- **Run 1 :** Bus et cars décarbonés [1, 5] | Efficacité et carburants décarbonés des véhicules privés [1, 5] | Fret décarboné et multimodalité [1, 4] | Véhicules électriques [1, 2, 4, 5]
- **Run 2 :** Bus et cars décarbonés [5] | Efficacité et carburants décarbonés des véhicules privés [1, 2, 3] | Fret décarboné et multimodalité [1] | Véhicules électriques [1, 5]
- **Run 3 :** Bus et cars décarbonés [1, 5] | Efficacité et carburants décarbonés des véhicules privés [2, 4, 5] | Fret décarboné et multimodalité [1, 4, 5] | Véhicules électriques [1, 2, 5]
- **Prod :** Bus et cars décarbonés [1] | Efficacité et carburants décarbonés des véhicules privés [5] | Véhicules électriques [1] | Vélo et transport en commun [2]
- Catégories instables sur : Bus et cars décarbonés, Efficacité et carburants décarbonés des véhicules privés, Fret décarboné et multimodalité, Véhicules électriques

> 1. Etablir un schéma directeur des installations de recharge des véhicule électrique (SDIRVE), planifiant notamment la mise à disposition au public d’un vaste parc de bornes de recharge pour véhicules électriques en exploitant de nouveau les 170 bornes de l’ancien serMettre progressivement en place une flotte de bus TBM décarbonée pour remplacer d’ici 2028 les bus diesel et hybrides par des bus électriques et bioGNVvice Bluecub et en incitant au déploiement d’offres privées 2. Mettre progressiv…

#### Fiche 34967 — Action 41. Accompagner le développement du télétravail

- **Run 1 :** Réduction des déplacements [3, 4, 6]
- **Run 2 :** Réduction des déplacements [3, 4, 6]
- **Run 3 :** Réduction des déplacements [3, 4]
- **Prod :** Réduction des déplacements [1, 4, 6]
- Catégories instables sur : Réduction des déplacements

> 1. Réaliser une étude pour mesurer l’adhésion des entreprises de la métropole et de leurs salariés à la mise en place de lieux de travail à distance partagés (analyse des pratiques et appétence des entreprises pour réduire leur empreinte immobilière et carbone, évaluation de la valeur potentielle du service, recensement des besoins d’accompagnement ; étude des conditions d’adhésion des salariés résidant dans la métropole et dans les EPCI voisins, analyse de la localisation potentielle des sites…

#### Fiche 34969 — Action 43. Rénover et décarboner le secteur tertiaire public et privé

- **Run 1 :** Changement de chaudière à fioul (tertiaire) [3, 5, 6] | Changement de chaudière à gaz (tertiaire) [3, 6] | Sobriété et isolation des bâtiments (tertiaire) [3, 5, 6]
- **Run 2 :** Changement de chaudière à fioul (tertiaire) [3, 5, 6] | Changement de chaudière à gaz (tertiaire) [6] | Sobriété et isolation des bâtiments (tertiaire) [5, 6]
- **Run 3 :** Changement de chaudière à fioul (tertiaire) [3, 5, 6] | Changement de chaudière à gaz (tertiaire) [3, 5, 6] | Sobriété et isolation des bâtiments (tertiaire) [3, 5, 6]
- **Prod :** Changement de chaudière à fioul (tertiaire) [5] | Sobriété et isolation des bâtiments (tertiaire) [3, 5, 6]
- Catégories instables sur : Changement de chaudière à gaz (tertiaire), Sobriété et isolation des bâtiments (tertiaire)

> 1. Sur le patrimoine public, réaliser un diagnostic énergétique de l’ensemble des bâtiments, un schéma directeur immobilier pour prioriser les rénovations et proposer un conseiller en énergie partagé pour tous les bâtiments communaux, y compris ceux inférieurs à 1000 m2. 2. Accélérer la conversion des équipements de chauffage carbonés (et en priorité ceux au fioul) des bâtiments publics vers de la chaleur renouvelable en accompagnement de la loi Climat et résilience 3. Accompagner les maitres d…

#### Fiche 34975 — Action 49. Inciter à une consommation sobre, utile et durable

- **Run 1 :** Prévention des déchets [5, 6]
- **Run 2 :** Prévention des déchets [5, 6]
- **Run 3 :** Prévention des déchets [3, 5, 6]
- **Prod :** Prévention des déchets [5, 6]
- Catégories instables sur : Prévention des déchets

> 1. Intégrer l'empreinte carbone dans les marchés à chaque fois que pertinent et une évaluation des gaz à effet de serre lors de l’exécution du marché 2. Intégrer des clauses incitatives ou des critères de sélection dédiés dans ses marchés pour contribuer à la lutte contre l’obsolescence programmée et à l’allongement de la durée d’usage notamment dans le secteur du numérique 3.Etudier la faisabilité de promouvoir les achats responsables dans les politiques d'achat communales 4. Dans le cadre du …

## CC de la Forêt (4576)

- Fiches : **94** — stables sur les 3 runs : **39** (41%), instables : **55**
- Paires levier × catégorie distinctes proposées : 202 — 3/3 runs : 63, 2/3 runs : 55, 1/3 runs : 84
- Vote majoritaire = prod : 13/63 fiches classées d'un côté ou de l'autre
- Réponses JSON invalides rejouées : 0
- Appels : 12 — tokens d'entrée 37 845 (dont 0 en cache, 0%), sortie 77 931 — coût estimé 0.19 $ pour les 3 runs
- Date : 2026-10-30 15:07

### Classée dans certains runs, aucun levier dans d'autres (20)

#### Fiche 40455 — 2.5 Etudier la possibilité d'organiser des services itinérants

- **Run 1 :** (aucun levier)
- **Run 2 :** Réduction des déplacements [1, 6]
- **Run 3 :** Réduction des déplacements [1, 6]
- **Prod :** (aucun levier)
- Leviers intermittents : Réduction des déplacements (2/3)

> <p>Recenser les commerces ambulants existants ainsi que les services itinérants déjà présents sur le territoire</p><p>Renforcer l’offre de santé sur le territoire, notamment dans le cadre du Contrat local de santé du PETR FOLS et travailler sur l’e-santé</p><p>Rendre accessibles les maisons France Services à travers du transport à la demande ou des solutions de mobilité</p><p>Promouvoir le passage du bus France Services sur le territoire et informer les habitants des permanences proposées</p>

#### Fiche 40464 — 2.14 Etudier la possibilité de mettre en place dans certaines communes une borne de recharge centrale et véhicule électrique partagé

- **Run 1 :** (aucun levier)
- **Run 2 :** (aucun levier)
- **Run 3 :** Véhicules électriques [1, 4]
- **Prod :** (aucun levier)
- Leviers intermittents : Véhicules électriques (1/3)

> <p>Etudier la possibilité de dupliquer le prêt d’un véhicule électrique aux personnes sans solution de mobilité (cf CCVS)</p><p>Etudier la possibilité de proposer quelques véhicules électriques en autopartage dans les centralités du territoire</p>

#### Fiche 40472 — 4.22 Accompagner les entreprises du territoire dans la transition écologique

- **Run 1 :** Production Industrielle [6]
- **Run 2 :** (aucun levier)
- **Run 3 :** Changement de chaudière à fioul (tertiaire) [3, 6] | Changement de chaudière à gaz (tertiaire) [3, 6] | Production Industrielle [3, 6] | Sobriété et isolation des bâtiments (tertiaire) [3, 6]
- **Prod :** (aucun levier)
- Leviers intermittents : Changement de chaudière à fioul (tertiaire) (1/3), Changement de chaudière à gaz (tertiaire) (1/3), Production Industrielle (2/3), Sobriété et isolation des bâtiments (tertiaire) (1/3)

> Sensibiliser les entreprises locales aux enjeux climatiques et aux aides auxquelles elles peuvent prétendre pour leurs investissements en faveur de l'environnement

#### Fiche 40478 — 5.28 Mener des études précises sur les potentiels et les espaces les plus adaptés du territoire pour y développer des équipements en énergie renouvelables

- **Run 1 :** (aucun levier)
- **Run 2 :** Electricité renouvelable [4] | Gestion des forêts et produits bois [4] | Réseaux de chaleur décarbonés [4]
- **Run 3 :** Electricité renouvelable [4] | Réseaux de chaleur décarbonés [4]
- **Prod :** (aucun levier)
- Leviers intermittents : Electricité renouvelable (2/3), Gestion des forêts et produits bois (1/3), Réseaux de chaleur décarbonés (2/3)

> <p>Réaliser une étude des potentiels de production d’énergie renouvelable de notre territoire&nbsp;: étudier le potentiel géothermique des sols à partir des travaux du BRGM, étudier les centralités qui permettraient d’accueillir un réseau de chaleur urbain, étudier le potentiel de l’hydroélectricité (turbine), élaborer un cadastre solaire, étudier les différentes offres et filières possibles concernant le bois énergie</p>

#### Fiche 40554 — 1.2.1 Etudier le potentiel de développement des réseaux de chaleur et schéma directeur énergie renouvelable via une note d'opportunité (Fibois) dans toute les communes

- **Run 1 :** (aucun levier)
- **Run 2 :** Gestion des forêts et produits bois [6] | Réseaux de chaleur décarbonés [6]
- **Run 3 :** Réseaux de chaleur décarbonés [4, 6]
- **Prod :** (aucun levier)
- Leviers intermittents : Gestion des forêts et produits bois (1/3), Réseaux de chaleur décarbonés (2/3)

> Communiquer et encourager l'action de Fibois et les notes d'opportunité dans les communes de la CCF

#### Fiche 40555 — 1.2.2 Etudier l'opportunité de mettre en place un cadastre solaire

- **Run 1 :** (aucun levier)
- **Run 2 :** Electricité renouvelable [4]
- **Run 3 :** Electricité renouvelable [4]
- **Prod :** (aucun levier)
- Leviers intermittents : Electricité renouvelable (2/3)

> Etudier la pertinence de la réalisation d'un cadastre solaire mutualisé à l'échelle des 4 CC du territoire

#### Fiche 40556 — 1.2.3 Produire de l'électricité et de la chaleur renouvelable sur le territoire : identifier les projets prévus sur le territoire

- **Run 1 :** (aucun levier)
- **Run 2 :** Electricité renouvelable [4] | Sobriété des bâtiments (résidentiel) [4]
- **Run 3 :** Electricité renouvelable [4] | Réseaux de chaleur décarbonés [4] | Sobriété des bâtiments (résidentiel) [4] | Sobriété et isolation des bâtiments (tertiaire) [4]
- **Prod :** (aucun levier)
- Leviers intermittents : Electricité renouvelable (2/3), Réseaux de chaleur décarbonés (1/3), Sobriété des bâtiments (résidentiel) (2/3), Sobriété et isolation des bâtiments (tertiaire) (1/3)

> Etude sobriété énergétique en groupement de commande

#### Fiche 40557 — 1.3.1 Etude de la collecte biodéchets et potentiel de méthanisation

- **Run 1 :** (aucun levier)
- **Run 2 :** Biogaz [4] | Valorisation matière des déchets [4]
- **Run 3 :** Biogaz [4] | Valorisation matière des déchets [4]
- **Prod :** (aucun levier)
- Leviers intermittents : Biogaz (2/3), Valorisation matière des déchets (2/3)

> Les syndicats de déchets du territoire réalisent des études pour la mise en place de la collecte des biodéchets et réfléchissent au potentiel de la méthanisation.

#### Fiche 40558 — 1.3.2 Elaborer un schéma directeur des mobilités

- **Run 1 :** (aucun levier)
- **Run 2 :** Réduction des déplacements [2] | Vélo et transport en commun [2]
- **Run 3 :** Réduction des déplacements [2] | Vélo et transport en commun [2]
- **Prod :** (aucun levier)
- Leviers intermittents : Réduction des déplacements (2/3), Vélo et transport en commun (2/3)

> La CCF réalise une étude mobilité sur son territoire pour mettre en place une offre de services en lien avec la Région Centre-Val de Loire.

#### Fiche 40559 — 2.1.1 Construire un tableau de bord des consommations de fluide (eau et énergie) des bâtiments

- **Run 1 :** (aucun levier)
- **Run 2 :** Sobriété et isolation des bâtiments (tertiaire) [4, 5]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété et isolation des bâtiments (tertiaire) (1/3)

> La CCF participe au groupe de travail Patrimoine du COT Transition avec les autres communautés de communes, participe aux réflexions communes et à la formalisation d'outils de suivi des consommations

#### Fiche 40560 — 2.1.2 Diffuser le tableau de bord aux communes pour qu'elles se l'approprient

- **Run 1 :** (aucun levier)
- **Run 2 :** Sobriété et isolation des bâtiments (tertiaire) [6]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété et isolation des bâtiments (tertiaire) (1/3)

> Proposer aux communes le tableau vierge et les aides à la prise en main

#### Fiche 40571 — 4.1.1 Mise en place d'une offre de véhicules en auto-partage en lien avec la Région CVL

- **Run 1 :** (aucun levier)
- **Run 2 :** (aucun levier)
- **Run 3 :** Réduction des déplacements [1]
- **Prod :** Covoiturage [1]
- Leviers intermittents : Réduction des déplacements (1/3)

> Dispositif en test sur plusieurs territoires de la région. A terme, le service devrait être déployé sur les CC non AOM

#### Fiche 40573 — 4.1.3 Mise en place des actions découlant du schéma directeur des mobilités

- **Run 1 :** (aucun levier)
- **Run 2 :** Réduction des déplacements [1]
- **Run 3 :** Réduction des déplacements [1] | Vélo et transport en commun [1]
- **Prod :** (aucun levier)
- Leviers intermittents : Réduction des déplacements (2/3), Vélo et transport en commun (1/3)

> Décliner des actions mobilité découlant du schéma directeur

#### Fiche 40584 — 3. Mettre en place une culture territoriale de l'usage des matériaux écologiques

- **Run 1 :** Pratiques stockantes [6]
- **Run 2 :** Gestion des forêts et produits bois [6]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Gestion des forêts et produits bois (1/3), Pratiques stockantes (1/3)

> La CCF partage les ressources existantes sur les matériaux biosourcés et géosourcés. Elle relaie les informations des fédérations et réseaux de la construction et des éco-matériaux auprès des entreprises.

#### Fiche 40585 — 4. Soutenir le développement des filières d'éco-matériaux (paille, bois, chanvre…)

- **Run 1 :** Pratiques stockantes [5]
- **Run 2 :** Gestion des forêts et produits bois [5]
- **Run 3 :** (aucun levier)
- **Prod :** Gestion des forêts et produits bois [5]
- Leviers intermittents : Gestion des forêts et produits bois (1/3), Pratiques stockantes (1/3)

> Les filières d'éco-matériaux (paille, bois, chanvre…) sont developées via la commande publique de la CCF. Des clauses sont intégrées dans les marchés pour intégrer des éco-matéiraux dans les constructions des collectivités.

#### Fiche 40590 — 9. Réaliser un état des lieux des opportunités sur l'écologie industrielle et territoriale (EIT) et la déployer sur les zones d'activités opportunes

- **Run 1 :** Production Industrielle [4]
- **Run 2 :** Production Industrielle [4]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Production Industrielle (2/3)

> Une étude est réalisée pour identifier les zones d'activités et flux du territoire les plus appropriés pour la création de synergies de ressources. Elle pourra comprendre une enquête auprès des entreprises mais également des réunions collectives.

#### Fiche 40591 — 10. Animer une démarche d'écologie industrielle et territoriale (EIT) sur les territoires

- **Run 1 :** Production Industrielle [4]
- **Run 2 :** Production Industrielle [4]
- **Run 3 :** (aucun levier)
- **Prod :** Efficacité et sobriété logistique [4, 6] | Valorisation matière des déchets [4, 6]
- Leviers intermittents : Production Industrielle (2/3)

> La CCF met en relation les entreprises pour identifier les synergies de ressources. Pour cela des réunions sont réalisées durant lesquelles les approvisionnements et déchets ou co-produits par entreprise sont listés afin d'identifier les synergies possibles entre les besoins des uns et co-produits des autres.

#### Fiche 40592 — 11. Informer et sensibiliser les entreprises au sujet de l'économie circulaire

- **Run 1 :** Prévention des déchets [6]
- **Run 2 :** Prévention des déchets [6]
- **Run 3 :** (aucun levier)
- **Prod :** Prévention des déchets [6] | Valorisation matière des déchets [6]
- Leviers intermittents : Prévention des déchets (2/3)

> La CCF sensibilise et forme les entreprises en enjeux de l'économie circulaire par l'intermédiaire des clubs et des réseaux. Elle assure également un rôle d'accompagnement technique des entreprises du territoire sur l'ECi (décryptage des réglementations, veille des dispositifs de subvention, mise en réseau, information sur les obligations de gestion de leurs déchets...)

#### Fiche 40595 — 14. Soutenir la production agricole de proximité et les circuits courts

- **Run 1 :** Efficacité et sobriété logistique [3, 4]
- **Run 2 :** Efficacité et sobriété logistique [1, 3]
- **Run 3 :** (aucun levier)
- **Prod :** Efficacité et sobriété logistique [3, 4]
- Leviers intermittents : Efficacité et sobriété logistique (2/3)

> Le PETR FOLS soutient les AMAP ainsi que les commerces de vente directe des producteurs, au travers d'un appui financier, de mise en valeur ou de mise à disposition de foncier, en lien avec le PAT du territoire.

#### Fiche 40596 — 15. Célébrer un événement annuel de l'économie circulaire

- **Run 1 :** Prévention des déchets [6]
- **Run 2 :** Prévention des déchets [6]
- **Run 3 :** (aucun levier)
- **Prod :** Prévention des déchets [6]
- Leviers intermittents : Prévention des déchets (2/3)

> Le PETR FOLS sensibilise le grand public lors d'un événement annuel festif rassemblant les acteurs de l'économie circulaire. L'événement permettra de mettre en valeur les acteurs associatifs de l'ECi et de partager des bonnes pratiques au travers d'ateliers.

### Levier présent dans certains runs seulement (9)

#### Fiche 40462 — 2.12 Développer le réseau cyclable sur le territoire à travers la mise en place d'un schéma directeur cyclable

- **Run 1 :** Vélo et transport en commun [1, 2, 6]
- **Run 2 :** Réduction des déplacements [1, 2, 6] | Vélo et transport en commun [1, 2, 6]
- **Run 3 :** Réduction des déplacements [1, 2, 6] | Vélo et transport en commun [1, 2, 6]
- **Prod :** Vélo et transport en commun [1, 2, 6]
- Leviers intermittents : Réduction des déplacements (2/3)

> <p>Elaborer un schéma directeur cyclable et/ou une étude mobilité avec un volet cyclable</p><p>Développer de nouveaux aménagements cyclables reliant les points d’intérêt du territoire</p><p>Développer l’écosystème vélo&nbsp;(réparation, location, services, box sécurisés…)</p><p>Travailler avec les écoles et les parents d’élèves sur des ramassages scolaires alternatifs (pédibus, vélobus…)</p>

#### Fiche 40477 — 4.27 Maintenir la sensibilisation au recyclage à destination des habitants

- **Run 1 :** Valorisation matière des déchets [6]
- **Run 2 :** Prévention des déchets [6] | Valorisation matière des déchets [6]
- **Run 3 :** Prévention des déchets [6] | Valorisation matière des déchets [6]
- **Prod :** Prévention des déchets [6] | Valorisation matière des déchets [6]
- Leviers intermittents : Prévention des déchets (2/3)

> <p>Organiser des campagnes Zéro déchets</p><p>Sensibiliser aux consignes de tri (habitants, scolaires…)</p><p>Faire connaître les outils numériques au service du recyclage et du réemploi</p>

#### Fiche 40488 — 7.38 Rendre exemplaires les déplacements des administrations

- **Run 1 :** Covoiturage [5] | Réduction des déplacements [5] | Véhicules électriques [5]
- **Run 2 :** Covoiturage [5] | Efficacité et carburants décarbonés des véhicules privés [5] | Réduction des déplacements [5]
- **Run 3 :** Covoiturage [5] | Réduction des déplacements [5] | Véhicules électriques [5]
- **Prod :** (aucun levier)
- Leviers intermittents : Efficacité et carburants décarbonés des véhicules privés (1/3), Véhicules électriques (2/3)

> <p>Rendre les flottes autombiles communales et intercommunales moins émettrices lors du renouvellement du parc</p><p>Poursuivre et étendre la politique d’achats de véhicules groupés, entre les structures</p><p>Rendre possibles les échanges de bonnes pratiques entre collectivités en matière de déplacements professionnels</p><p>Limiter, quand cela est possible, les besoins de se déplacer, favoriser le covoiturage</p><p>Communiquer sur Rezo Pouce auprès des agents des collectivités</p>

#### Fiche 40563 — 2.1.5 Envisager les constructions neuves de manière exemplaire

- **Run 1 :** Electricité renouvelable [5] | Réseaux de chaleur décarbonés [5] | Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 2 :** Electricité renouvelable [5] | Sobriété et isolation des bâtiments (tertiaire) [5] | Sobriété foncière [5]
- **Run 3 :** Electricité renouvelable [5] | Réseaux de chaleur décarbonés [5] | Sobriété et isolation des bâtiments (tertiaire) [5]
- **Prod :** Electricité renouvelable [5] | Sobriété foncière [5]
- Leviers intermittents : Réseaux de chaleur décarbonés (2/3), Sobriété foncière (1/3)

> La CCF envisage les constructions neuves de manière exemplaire. Construction du siège : panneaux PV, géothermie, récupération des eaux de pluies. Parking non imperméabilisée.

#### Fiche 40572 — 4.1.2 Construction de pôles d'échanges intermodaux en lien avec le Département du Loiret

- **Run 1 :** Vélo et transport en commun [1]
- **Run 2 :** Vélo et transport en commun [1]
- **Run 3 :** Réduction des déplacements [1] | Vélo et transport en commun [1]
- **Prod :** (aucun levier)
- Leviers intermittents : Réduction des déplacements (1/3)

> Participer aux réflexions et études engagées par le CD 45

#### Fiche 40574 — 4.1.4 Diagnostic et verdissement de la flotte interne de la collectivité

- **Run 1 :** Véhicules électriques [5]
- **Run 2 :** Bus et cars décarbonés [5] | Efficacité et carburants décarbonés des véhicules privés [5] | Véhicules électriques [5]
- **Run 3 :** Véhicules électriques [5]
- **Prod :** (aucun levier)
- Leviers intermittents : Bus et cars décarbonés (1/3), Efficacité et carburants décarbonés des véhicules privés (1/3)

> Elaborer un diagnostic de renouvellement et de la flotte de véhicules de la collectivités et y intégrer les communes éventuellement

#### Fiche 40588 — 7. Soutenir le réemploi des matériaux du BTP

- **Run 1 :** Valorisation matière des déchets [4, 6]
- **Run 2 :** Prévention des déchets [6]
- **Run 3 :** Valorisation matière des déchets [6]
- **Prod :** Prévention des déchets [2, 6] | Valorisation matière des déchets [2, 6]
- Leviers intermittents : Prévention des déchets (1/3), Valorisation matière des déchets (2/3)

> La CCF informe les MOA privés au sujet du diagnostic PEMD de manière à généraliser la démarche sur le territoire, par exemple au moment de la délivrance du permis de démolir. Le PETR FOLS se charge de créer ou récupérer une fiche commune sur le diagnostic POMD et la gestion des 7 flux de matières pour la transmettre aux services urbanisme de la CCF.

#### Fiche 40589 — 8. Soutenir la mise en place de matériauthèques

- **Run 1 :** Valorisation matière des déchets [3]
- **Run 2 :** Prévention des déchets [3]
- **Run 3 :** Valorisation matière des déchets [3]
- **Prod :** Prévention des déchets [3]
- Leviers intermittents : Prévention des déchets (1/3), Valorisation matière des déchets (2/3)

> Le PETR FOLS soutient financièrement la mise en place de nouvelles matériauthèques sur le territoire via les financements du CRST. Une étude des gisements et de la faisabilité pourra être réalisée en amont afin de définir au mieux le statut juridique, l'emplacement et les horaires d'ouverture des matériauthèques.

#### Fiche 40599 — 18.Mener un appel à projets pour développer les ressourceries du territoire

- **Run 1 :** Valorisation matière des déchets [3, 4]
- **Run 2 :** Prévention des déchets [4]
- **Run 3 :** Valorisation matière des déchets [3]
- **Prod :** Prévention des déchets [3, 4]
- Leviers intermittents : Prévention des déchets (1/3), Valorisation matière des déchets (2/3)

> Un appel à projet ou AMI est lancé sur le territoire du PETR FOLS pour faire émerger des porteurs de projet, notamment en matière de création de ressourcerie. Le PETR aura un rôle de facilitateur en porposant un mode d'emploi pour financer les projets et les faire émerger.

### Levier intermittent et catégories instables (8)

#### Fiche 40457 — 2.7 Rendre plus efficients les transports en commun

- **Run 1 :** Vélo et transport en commun [4, 6]
- **Run 2 :** Réduction des déplacements [1, 4, 6] | Vélo et transport en commun [1, 6]
- **Run 3 :** Vélo et transport en commun [1, 4, 6]
- **Prod :** Vélo et transport en commun [4, 6]
- Leviers intermittents : Réduction des déplacements (1/3)
- Catégories instables sur : Vélo et transport en commun

> <p>Etre force de proposition vis-à-vis des services de la Région Centre-Val de Loire pour soumettre des pistes d’amélioration des transports en commun</p><p>Promouvoir la plateforme JVMalin qui centralise toutes les informations de mobilité au niveau régional</p><p>Etudier la possibilité de mettre en place des parkings à vélo sécurisés aux principaux arrêts de bus et dans les aires de covoiturage</p><p>Soutenir et valoriser les projets mobilité portés par les communes (navettes dans le cadre de…

#### Fiche 40458 — 2.8 Soutenir la création d'une ligne de transports en commun Orléans-Châteauneuf

- **Run 1 :** Vélo et transport en commun [4]
- **Run 2 :** Réduction des déplacements [4] | Vélo et transport en commun [4]
- **Run 3 :** Vélo et transport en commun [1, 4]
- **Prod :** Vélo et transport en commun [4]
- Leviers intermittents : Réduction des déplacements (1/3)
- Catégories instables sur : Vélo et transport en commun

> Soutenir les projets favorisant la réouverture de la ligne Orléans-Châteauneuf

#### Fiche 40465 — 3.15 Encourager les exploitants à avoir des pratiques agro-écologiques

- **Run 1 :** Changements de pratiques de fertilisation azotée [3, 6] | Elevage durable [3, 6] | Gestion des haies [3, 6] | Pratiques stockantes [3, 6]
- **Run 2 :** Changements de pratiques de fertilisation azotée [3, 6] | Gestion des haies [3, 6] | Pratiques stockantes [3, 6]
- **Run 3 :** Changements de pratiques de fertilisation azotée [3, 4, 6] | Elevage durable [3, 4, 6] | Pratiques stockantes [3, 4, 6]
- **Prod :** Pratiques stockantes [3, 6]
- Leviers intermittents : Elevage durable (2/3), Gestion des haies (2/3)
- Catégories instables sur : Changements de pratiques de fertilisation azotée, Pratiques stockantes

> <p>Faciliter l’accès des exploitants à des formations et proposer des accompagnements pour faciliter la transition vers des pratiques agro-écologiques</p><p>Accentuer l’information aux agriculteurs sur l’ensemble des aides auxquelles ils peuvent avoir droit pour faire évoluer leurs pratiques</p><p>Soutenir les investissements en matière d’adaptation des pratiques à travers le CRST notamment</p><p>Agir pour soutenir les efforts faits en matière d’agroforesterie et accentuer l’information sur les…

#### Fiche 40466 — 3.16 Faciliter l'adaptation au changement climatique en soutenant les expérimentations et les nouvelles initiatives

- **Run 1 :** Bâtiments & Machines agricoles [3, 6] | Elevage durable [3, 6] | Pratiques stockantes [3, 6]
- **Run 2 :** Bâtiments & Machines agricoles [3, 6] | Pratiques stockantes [3, 6]
- **Run 3 :** Bâtiments & Machines agricoles [3, 4, 6] | Changements de pratiques de fertilisation azotée [3, 4, 6] | Elevage durable [3, 4, 6]
- **Prod :** (aucun levier)
- Leviers intermittents : Changements de pratiques de fertilisation azotée (1/3), Elevage durable (2/3), Pratiques stockantes (2/3)
- Catégories instables sur : Bâtiments & Machines agricoles

> <p>Accompagner les agriculteurs désireux de réaliser un diagnostic permettant d’identifier les vulnérabilités et atouts de leur exploitation</p><p>Dégager des pistes pour modifier les pratiques, réduire les consommations, notamment à travers l’outil CAP’2ER pour les éleveurs</p><p>Informer les agriculteurs sur les études réalisées sur les conduites de culture et sur le changement d’espèces permettant une meilleure adaptation au changement climatique</p><p>Soutenir les expérimentations agricoles…

#### Fiche 40468 — 3.18 Agir pour préserver et accroître la biodiversité du territoire

- **Run 1 :** Gestion des haies [2, 6] | Sobriété foncière [2, 6]
- **Run 2 :** Gestion des haies [1, 6] | Sobriété foncière [2]
- **Run 3 :** Gestion des haies [1, 2] | Pratiques stockantes [1] | Sobriété foncière [2]
- **Prod :** Gestion des haies [6] | Sobriété foncière [2]
- Leviers intermittents : Pratiques stockantes (1/3)
- Catégories instables sur : Gestion des haies, Sobriété foncière

> <p>Inciter les communes à mettre en place un inventaire ou un atlas de la biodiversité communale</p><p>Diffuser les appels à projets recensés par l’Agence régionale de biodiversité</p><p>Communiquer sur les actions biodiversité menées par le PETR (rando-bio, biodiv’pratique…)</p><p>Mettre en place un Plan Haies</p><p>Sensibiliser le grand public en organisant des événements ponctuels autour de l’environnement en lien avec les associations ou organismes locaux (Maison de Loire, Graine Centre, Fr…

#### Fiche 40489 — 7.39 Faire des collectivités des acteurs agissant en faveur de la biodiversité

- **Run 1 :** Gestion des prairies [1] | Pratiques stockantes [1]
- **Run 2 :** Gestion des haies [1, 6] | Pratiques stockantes [1, 6]
- **Run 3 :** Gestion des haies [4, 6] | Gestion des prairies [1, 6] | Pratiques stockantes [1, 4, 6]
- **Prod :** (aucun levier)
- Leviers intermittents : Gestion des haies (2/3), Gestion des prairies (2/3)
- Catégories instables sur : Pratiques stockantes

> <p>Diffuser les bonnes pratiques pour favoriser la biodiversité dans les communes</p><p>Initier des plantations de vergers communaux, de jardins partagés et privilégier l’éco-pâturage</p><p>Déployer l’action Rando bio qui permet aux élus et agents des collectivités de participer à des visites de terrain thématiques sur la biodiversité</p><p>Communiquer sur les Solutions fondées sur la nature (SFN)</p><p>Inciter les communes à réaliser un inventaire de biodiversité communale (IBC)</p><p>Elaborer…

#### Fiche 40579 — 5.1.1 Mettre en place une convention avec l'ADIL dans le cadre de France Rénov

- **Run 1 :** Sobriété des bâtiments (résidentiel) [6]
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [4, 6] | Changement chaudières gaz + rénovation (résidentiel) [4, 6] | Sobriété des bâtiments (résidentiel) [4, 6]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6] | Sobriété des bâtiments (résidentiel) [6]
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [4] | Changement chaudières gaz + rénovation (résidentiel) [4]
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (2/3), Changement chaudières gaz + rénovation (résidentiel) (2/3)
- Catégories instables sur : Sobriété des bâtiments (résidentiel)

> Signature d'un Pacte Territorial

#### Fiche 40597 — 16. Sensibiliser les habitants à la sobriété

- **Run 1 :** Prévention des déchets [6] | Valorisation matière des déchets [1, 6]
- **Run 2 :** Prévention des déchets [1, 6]
- **Run 3 :** Prévention des déchets [6]
- **Prod :** Prévention des déchets [1, 6]
- Leviers intermittents : Valorisation matière des déchets (1/3)
- Catégories instables sur : Prévention des déchets

> Les syndicats de collecte des déchets mettent en place des actions de sensibilisation du grand public (à la sobriété, au recyclage et aux enjeux de l'économie circulaire) pour accompagner l'évolution des pratiques. Des boîtes à livre et espaces de dons sont mis en place au sein des communes.

### Mêmes leviers, catégories différentes (18)

#### Fiche 40456 — 2.6 Développer un réseau de coworking sur le territoire

- **Run 1 :** Réduction des déplacements [1, 6]
- **Run 2 :** Réduction des déplacements [1, 6]
- **Run 3 :** Réduction des déplacements [1, 4, 6]
- **Prod :** Réduction des déplacements [1, 4, 6]
- Catégories instables sur : Réduction des déplacements

> <p>Recenser les lieux déjà existants et les faire connaître</p><p>Travailler avec les acteurs du territoire pour qu’ils s’impliquent dans la création de lieux de coworking</p><p>Accompagner et soutenir les projets de tiers lieux en émergence sur le territoire</p><p>Réaliser un diagnostic de la couverture téléphonique et internet du territoire pour construire les infrastructures nécessaires</p>

#### Fiche 40459 — 2.9 Promouvoir et accompagner le développement des véhicules basses émissions pour les véhicules légers et la logistique

- **Run 1 :** Véhicules électriques [1, 6]
- **Run 2 :** Véhicules électriques [1]
- **Run 3 :** Véhicules électriques [1]
- **Prod :** Véhicules électriques [1]
- Catégories instables sur : Véhicules électriques

> Etudier les besoins du territoire et créer davantage de bornes de recharge sur le territoire

#### Fiche 40461 — 2.11 Inciter les entreprises et commerçants à coordonner les déplacements

- **Run 1 :** Covoiturage [6] | Réduction des déplacements [6]
- **Run 2 :** Covoiturage [6] | Réduction des déplacements [6]
- **Run 3 :** Covoiturage [4, 6] | Réduction des déplacements [4, 6]
- **Prod :** Covoiturage [6] | Réduction des déplacements [6]
- Catégories instables sur : Covoiturage, Réduction des déplacements

> <p>Travailler avec les entreprises à l’échelle des zones d’activités (plans de mobilité employeur, promotion du covoiturage, regroupement des déplacements professionnels…)</p>

#### Fiche 40463 — 2.13 Développer Rezo Pouce : le faire connaître largement et le prolonger au-delà du territoire

- **Run 1 :** Covoiturage [4, 6]
- **Run 2 :** Covoiturage [6]
- **Run 3 :** Covoiturage [4, 6]
- **Prod :** Covoiturage [4, 6]
- Catégories instables sur : Covoiturage

> <p>Dynamiser la communication sur le dispositif</p><p>Prévoir des animations de présentation de Rezo Pouce auprès des publics spécifiques&nbsp;: jeunes, entreprises…</p><p>Organiser un maillage hors territoire avec les territoires voisins</p><p>Engager des réflexions avec les entreprises pour promouvoir Rezo Pouce auprès de leurs salariés</p>

#### Fiche 40469 — 3.19 Prévenir et anticiper les conséquences déjà visibles du changement climatique sur les forêts

- **Run 1 :** Gestion des forêts et produits bois [4, 6]
- **Run 2 :** Gestion des forêts et produits bois [1, 4, 6]
- **Run 3 :** Gestion des forêts et produits bois [1, 4, 6]
- **Prod :** (aucun levier)
- Catégories instables sur : Gestion des forêts et produits bois

> <p>Travailler avec l’ONF et le CRPF sur la gestion des forêts et leur adaptation au changement climatique</p><p>Réaliser une veille active sur l’adaptation des forêts au changement climatique</p><p>Travailler sur la prévention des feux de forêts (sensibilisation, formation des pompiers, aménagements spécifiques…)</p><p>Sensibiliser le grand public aux conséquences du changement climatique sur les forêts et soutenir ce type d’actions</p>

#### Fiche 40473 — 4.23 Développer l'économie circulaire

- **Run 1 :** Prévention des déchets [6] | Valorisation matière des déchets [6]
- **Run 2 :** Prévention des déchets [6] | Valorisation matière des déchets [6]
- **Run 3 :** Prévention des déchets [4, 6] | Valorisation matière des déchets [4, 6]
- **Prod :** Prévention des déchets [6]
- Catégories instables sur : Prévention des déchets, Valorisation matière des déchets

> Accompagner le territoire dans la démarche COT Transition de l'ADEME pour soutenir la politique d'économie circulaire de la collectivité et lancer une opération Eco-défis auprès des artisans et des commerçants

#### Fiche 40474 — 4.24 Sensibiliser les acteurs du tourisme et agir pour le tourisme local

- **Run 1 :** Réduction des déplacements [6] | Vélo et transport en commun [6]
- **Run 2 :** Réduction des déplacements [1, 6] | Vélo et transport en commun [1, 6]
- **Run 3 :** Réduction des déplacements [4, 6] | Vélo et transport en commun [4, 6]
- **Prod :** (aucun levier)
- Catégories instables sur : Réduction des déplacements, Vélo et transport en commun

> <p>Développer avec les acteurs économiques un tourisme d’entreprise en valorisant les entreprises les plus engagées en matière climatique</p><p>Organiser avec les agriculteurs et les producteurs bio des circuits de découverte écologique du territoire</p><p>Développer l’offre de tourisme à vélo et communiquer</p><p>Informer et mobiliser les acteurs du tourisme en faveur des labels verts auxquels ils peuvent prétendre en adaptant leurs pratiques&nbsp;; valoriser les acteurs respectueux de l’envir…

#### Fiche 40475 — 4.25 Développer de nouvelles filières de recyclage

- **Run 1 :** Prévention des déchets [6] | Valorisation matière des déchets [6]
- **Run 2 :** Prévention des déchets [6] | Valorisation matière des déchets [6]
- **Run 3 :** Prévention des déchets [4, 6] | Valorisation matière des déchets [4, 6]
- **Prod :** Prévention des déchets [6]
- Catégories instables sur : Prévention des déchets, Valorisation matière des déchets

> <p>Accompagner le développement des ressourceries sur le territoire</p><p>Lancer des réflexions sur la collecte des biodéchets</p>

#### Fiche 40480 — 5.30 Développer le solaire photovoltaïque et le solaire thermique sur les bâtiments

- **Run 1 :** Electricité renouvelable [5, 6]
- **Run 2 :** Electricité renouvelable [5, 6]
- **Run 3 :** Electricité renouvelable [4, 5, 6]
- **Prod :** Electricité renouvelable [5, 6]
- Catégories instables sur : Electricité renouvelable

> <p>Faire réaliser un cadastre solaire pour identifier les zones les plus propices au développement du solaire PV et thermique</p><p>Contacter les entreprises dont les bâtiments peuvent héberger des équipements PV et solaires et leur proposer des solutions adaptées</p><p>Travailler avec les agriculteurs pour développer le solaire sur les bâtiments agricoles</p><p>Promouvoir le solaire thermique dans le cadre du COT EnR</p><p>Porter des projets d’énergies renouvelables sur les bâtiments (CCL, CCF…

#### Fiche 40482 — 5.32 Initier et soutenir des projets "nouvelles énergies" appuyés sur une participation citoyenne

- **Run 1 :** Electricité renouvelable [6]
- **Run 2 :** Electricité renouvelable [4, 6]
- **Run 3 :** Electricité renouvelable [3, 4, 6]
- **Prod :** Electricité renouvelable [4, 6]
- Catégories instables sur : Electricité renouvelable

> <p>Accompagner l’émergence et le déploiement de collectifs citoyens porteurs de projets d’énergies renouvelables en travaillant sur le sujet avec Energie partagée</p><p>Communiquer sur la possibilité pour les citoyens de porter des projets de production d’énergie renouvelable</p><p>Informer les citoyens sur les possibilités de financement de ces projets et soutenir ces projets via les contrats du PETR</p><p>Impulser des dynamiques entre élus et citoyens pour développer des projets d’énergie cit…

#### Fiche 40487 — 7.37 Rendre exemplaires les bâtiments et l'éclairage public

- **Run 1 :** Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 2 :** Sobriété et isolation des bâtiments (tertiaire) [5, 6]
- **Run 3 :** Sobriété et isolation des bâtiments (tertiaire) [5]
- **Prod :** Changement de chaudière à fioul (tertiaire) [5] | Changement de chaudière à gaz (tertiaire) [5] | Sobriété et isolation des bâtiments (tertiaire) [5]
- Catégories instables sur : Sobriété et isolation des bâtiments (tertiaire)

> <p>Informer les communes sur les subventions possibles pour leurs projets de rénovation de bâtiments et de modernisation de l’éclairage public et communiquer sur les guides réalisés par l’ADEME sur ces sujets</p><p>Réaliser un diagnostic de l’ensemble des bâtiments publics du territoire et proposer à chaque commune d’engager un plan de rénovation énergétique</p><p>Favoriser les matériaux locaux et biosourcés dans les futures constructions publiques</p><p>Travailler sur la diminution de l’intens…

#### Fiche 40562 — 2.1.4 Construire une trajectoire de rénovation et d'amélioration cohérente avec le PCAET et la trajectoire du décret Tertiaire

- **Run 1 :** Sobriété et isolation des bâtiments (tertiaire) [4]
- **Run 2 :** Sobriété et isolation des bâtiments (tertiaire) [4, 5]
- **Run 3 :** Sobriété et isolation des bâtiments (tertiaire) [2, 5]
- **Prod :** (aucun levier)
- Catégories instables sur : Sobriété et isolation des bâtiments (tertiaire)

> Possible de créer un groupement de commande pour embarquer les commandes. Rôle de la coordination de la CCF.

#### Fiche 40575 — 4.1.5 Mener des réflexions sur le covoiturage (Mobicoop, incitation financière, bassin de mobilité en lien avec OM)

- **Run 1 :** Covoiturage [6]
- **Run 2 :** Covoiturage [4, 6]
- **Run 3 :** Covoiturage [6]
- **Prod :** (aucun levier)
- Catégories instables sur : Covoiturage

> Accueillir des animations sur le territoire de la CCF Relai de communication des actions menées par le PETR Réflexions communes sur la pratique du covoiturage

#### Fiche 40578 — 4.1.8 Suivre le schéma directeur départemental des développements des bornes électriques

- **Run 1 :** Véhicules électriques [4]
- **Run 2 :** Véhicules électriques [1]
- **Run 3 :** Véhicules électriques [1]
- **Prod :** (aucun levier)
- Catégories instables sur : Véhicules électriques

> Suivre les travaux autour du SDIRVE

#### Fiche 40586 — 5. Intégrer la sobriété foncière dans les projets d'aménagement

- **Run 1 :** Sobriété foncière [2]
- **Run 2 :** Sobriété foncière [1]
- **Run 3 :** Sobriété foncière [1]
- **Prod :** Sobriété foncière [1, 2]
- Catégories instables sur : Sobriété foncière

> La CCF décline les objectifs de limitation de l'artificialisation des sols dans ses projets d'aménagement (ZAE). Elle appuie les communes sur le sujet.

#### Fiche 40587 — 6. Recenser et caractériser les friches industrielles et tertiaires

- **Run 1 :** Sobriété foncière [4]
- **Run 2 :** Sobriété foncière [4]
- **Run 3 :** Sobriété foncière [1]
- **Prod :** Sobriété foncière [1, 2]
- Catégories instables sur : Sobriété foncière

> La CCF recense les friches industrielles et tertiaires du territoire avec l'intention de créer de nouveaux espaces de construction sans augmenter le taux d'artificialisation des sols. Le PETR FOLS aide au recensement et agrège ces informations;

#### Fiche 40598 — 17. Développer les ateliers de réparation et d'auto-réparation

- **Run 1 :** Prévention des déchets [3, 4]
- **Run 2 :** Prévention des déchets [6]
- **Run 3 :** Prévention des déchets [6]
- **Prod :** Prévention des déchets [3, 4]
- Catégories instables sur : Prévention des déchets

> En lien avec les associations, la CCF soutient des ateliers d'autoréparation des vélos. La CCF soutient les Repair Café sur le territoire (en coportage avec les communes et les associations locales).

#### Fiche 40600 — 19. Soutenir le tri à la source des biodéchets et appuyer le développement de nouvelles filières de recyclage

- **Run 1 :** Valorisation matière des déchets [3, 4]
- **Run 2 :** Valorisation matière des déchets [1, 3]
- **Run 3 :** Valorisation matière des déchets [3]
- **Prod :** Valorisation matière des déchets [3, 4]
- Catégories instables sur : Valorisation matière des déchets

> Les syndicats de déchets mettent en place des moyens de tri à la source des biodéchets en 2024. Le PETR FOLS soutient les syndicats pour le développement de nouvelles filières de recyclage par la rechrche de financement d'études pré-opérationnelles.

## CC Baugeois Vallée (4637)

- Fiches : **91** — stables sur les 3 runs : **32** (35%), instables : **59**
- Paires levier × catégorie distinctes proposées : 282 — 3/3 runs : 110, 2/3 runs : 72, 1/3 runs : 100
- Vote majoritaire = prod : 11/69 fiches classées d'un côté ou de l'autre
- Réponses JSON invalides rejouées : 0
- Appels : 12 — tokens d'entrée 142 086 (dont 0 en cache, 0%), sortie 82 276 — coût estimé 0.27 $ pour les 3 runs
- Date : 2026-10-30 15:07

### Classée dans certains runs, aucun levier dans d'autres (12)

#### Fiche 31808 — COT 3. Définir et mettre en oeuvre une politique d'achats durables

- **Run 1 :** (aucun levier)
- **Run 2 :** (aucun levier)
- **Run 3 :** Production Industrielle [5] | Prévention des déchets [5]
- **Prod :** (aucun levier)
- Leviers intermittents : Production Industrielle (1/3), Prévention des déchets (1/3)

> - Etablir un diagnostic de l’existant, avec une cartographie des achats (par type) pour identifier là où on peut développer des pratiques plus responsables, notamment des clauses environnementales et sociales - Formaliser la stratégie à travers un mini-SPASER et un outil de suivi de sa mise en œuvre - Etablir et renseigner régulièrement un outil de suivi des marchés publics durables (avec des indicateurs adaptés) - Approuver cette stratégie d’achats publics responsables en conseil communautaire…

#### Fiche 32289 — COT 7. Suivre les consommations énergétiques par service

- **Run 1 :** (aucun levier)
- **Run 2 :** Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 3 :** Sobriété et isolation des bâtiments (tertiaire) [5]
- **Prod :** Sobriété et isolation des bâtiments (tertiaire) [5]
- Leviers intermittents : Sobriété et isolation des bâtiments (tertiaire) (2/3)

> Consommation des bâtiments - Renseigner le tableau de suivi avec les surfaces de chaque bâtiment - Renseigner le tableau de suivi avec les consommations énergétiques par bâtiment et par an - Produire des indicateurs de suivi : consommation globale des bâtiments, rapportés à la surface totale et à la population totale - Communiquer sur ces indicateurs (rapport d’activités) - Relancer le partenariat avec le SIEML (conseil en énergie partagé) pour établir un diagnostic énergétique de nos bâtiments…

#### Fiche 32290 — COT 8. Mettre en place des actions pour réduire la vacance des logements

- **Run 1 :** (aucun levier)
- **Run 2 :** (aucun levier)
- **Run 3 :** Sobriété foncière [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété foncière (1/3)

> Encourager les propriétaires de logements vacants à les remettre sur le marché.

#### Fiche 32299 — COT 18. Identifier et développer une filière à enjeu en lien avec l'économie circulaire sur le territoire

- **Run 1 :** Prévention des déchets [4, 6] | Valorisation matière des déchets [4, 6]
- **Run 2 :** (aucun levier)
- **Run 3 :** Production Industrielle [4, 6]
- **Prod :** (aucun levier)
- Leviers intermittents : Production Industrielle (1/3), Prévention des déchets (1/3), Valorisation matière des déchets (1/3)

> <p>Dans le cadre de son Contrat d’Objectifs Territorial (COT) signé avec l’ADEME, la Communauté de communes Baugeois-Vallée engage une démarche de structuration de l’économie circulaire sur son territoire.<br>L’objectif est d’identifier une filière économique à enjeu local (industrie, bâtiment, agriculture, services…) et d’y déployer une stratégie opérationnelle d’économie circulaire, en s’appuyant sur les acteurs économiques, les réseaux professionnels et les dispositifs régionaux existants.</…

#### Fiche 32301 — COT 20. Elaborer une stratégie touristique durable

- **Run 1 :** (aucun levier)
- **Run 2 :** (aucun levier)
- **Run 3 :** Prévention des déchets [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Prévention des déchets (1/3)

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="b4726a72-6c33-4671-9d1e-d9f097e5307c"><div class="bn-block" data-node-type="blockContainer" data-id="b4726a72-6c33-4671-9d1e-d9f097e5307c"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]">Dans la stratégie touristique renouvelée pour 2024-2026 (approuvée en décembre 2023), l’objectif « dével…

#### Fiche 32303 — COT 22. Se doter d'un observatoire des projets ENR sur le territoire (publics et privés)

- **Run 1 :** (aucun levier)
- **Run 2 :** Biogaz [4] | Electricité renouvelable [4] | Réseaux de chaleur décarbonés [4]
- **Run 3 :** Biogaz [4] | Electricité renouvelable [4]
- **Prod :** (aucun levier)
- Leviers intermittents : Biogaz (2/3), Electricité renouvelable (2/3), Réseaux de chaleur décarbonés (1/3)

> Avoir une vision en temps réel et prospective des énergies renouvelables sur le territoire Mettre en lien les projets des communes et les volontés des élus afin de prévoir le mix énergétique du territoire Réfléchir en vision d’ensemble plutôt que par projet

#### Fiche 32313 — COT 13. Accompagner les communes dans la mise en place de liaisons intercommunales cyclables

- **Run 1 :** Vélo et transport en commun [1, 3, 4]
- **Run 2 :** (aucun levier)
- **Run 3 :** Vélo et transport en commun [1, 2, 4, 6]
- **Prod :** (aucun levier)
- Leviers intermittents : Vélo et transport en commun (2/3)

> Etat des lieux des aménagements existants et futurs des communes - Production d'un Schéma Directeur des Modes Actifs Intercommunal - Réunions annuelles avec les communes pour déterminer l'avancée du Schéma DIrecteur des Modes Actifs - Veille active sur les aides existantes et les proposer aux communes - Faciliter les démarches de demande de subventions

#### Fiche 72493 — 11. Renforcer l'accompagnement du grand public et des professionnels pour une alimentation locale et de qualité

- **Run 1 :** Prévention des déchets [6]
- **Run 2 :** (aucun levier)
- **Run 3 :** Prévention des déchets [4, 5, 6]
- **Prod :** (aucun levier)
- Leviers intermittents : Prévention des déchets (2/3)

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="5c56c298-25be-400c-af0b-9bacb52ea19e"><div class="bn-block" data-node-type="blockContainer" data-id="5c56c298-25be-400c-af0b-9bacb52ea19e"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]">La CCBV s’est engagée pour une alimentation locale et durable grâce au Projet Alimentaire Territorial me…

#### Fiche 72497 — 15. Promouvoir le transport à la demande

- **Run 1 :** Vélo et transport en commun [3, 4, 6]
- **Run 2 :** (aucun levier)
- **Run 3 :** Vélo et transport en commun [3, 4, 6]
- **Prod :** (aucun levier)
- Leviers intermittents : Vélo et transport en commun (2/3)

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="a44767a0-7378-48be-aa35-c3350b53dafc"><div class="bn-block" data-node-type="blockContainer" data-id="a44767a0-7378-48be-aa35-c3350b53dafc"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]">Dans un territoire rural comme Baugeois-Vallée, l’accès aux services et à la mobilité reste inégal, nota…

#### Fiche 72512 — 29. Optimiser l’irrigation agricole

- **Run 1 :** (aucun levier)
- **Run 2 :** Pratiques stockantes [6]
- **Run 3 :** (aucun levier)
- **Prod :** Bâtiments & Machines agricoles [6] | Gestion des haies [6] | Pratiques stockantes [6]
- Leviers intermittents : Pratiques stockantes (1/3)

> <p>Le territoire de la CCBV est fortement concerné par les effets du changement climatique sur la ressource en eau. L’agriculture, très présente localement, représente un poste majeur de consommation, et sa résilience dépend d’une gestion plus économe et partagée de cette ressource. Cette action s’inscrit dans les objectifs du PCAET, renforcés par les dynamiques régionales portées par la Chambre d’agriculture et les SAGE Loir et Authion.</p><p>&nbsp;</p><p>·&nbsp;&nbsp;&nbsp;&nbsp; <strong>Prom…

#### Fiche 144030 — Action 31 : Soutien aux campagnes annuelles de nettoyage de la nature

- **Run 1 :** (aucun levier)
- **Run 2 :** (aucun levier)
- **Run 3 :** Prévention des déchets [3, 6]
- **Prod :** (aucun levier)
- Leviers intermittents : Prévention des déchets (1/3)

> Achat de matériel : gants, pinces à déchets, flamme de communication, peson ou balance facile à transporter. Procédure de prêt sous convention. Création d’un module de sensibilisation pour le jour de l’opération, soit à utiliser en autonomie ou avec la présence de l’agent tri-prévention, pour faciliter le tri, apporter de l'information sur les déchets.

#### Fiche 144031 — Action 32 : Établir un diagnostic et programme d’action en transversalité avec le service eau et assainissement

- **Run 1 :** Prévention des déchets [2]
- **Run 2 :** (aucun levier)
- **Run 3 :** Prévention des déchets [4]
- **Prod :** (aucun levier)
- Leviers intermittents : Prévention des déchets (2/3)

> Etablir un Plan Plastique Territorial avec le service Eau et Assainissement. Etablir un programme de visites de STEP.

### Levier présent dans certains runs seulement (15)

#### Fiche 32300 — COT 19. Améliorer la qualité des zones d'activité (consommation d'espace, biodiversité, mobilité…)

- **Run 1 :** Sobriété foncière [1] | Vélo et transport en commun [1]
- **Run 2 :** Vélo et transport en commun [1]
- **Run 3 :** Vélo et transport en commun [1]
- **Prod :** Sobriété foncière [1] | Vélo et transport en commun [1]
- Leviers intermittents : Sobriété foncière (1/3)

> Requalification des zone d'activités du territoire : - Réhabilitation des bassins de rétention (retisser le lien entre la ville, la nature et l’activité économique, offrir de nouveaux usages aux espaces publics, répondre aux enjeux climatiques et hydrauliques de demain) - modification de la voirie (voie partagée entre voitures et vélos) et réfection des trottoirs - revégétaliser certaines places de parking et perméabiliser certaines autres - renouvellement des arbres qui n'ont jamais prit - rel…

#### Fiche 32304 — COT 23. Soutenir les énergies citoyennes

- **Run 1 :** Electricité renouvelable [4, 6]
- **Run 2 :** Biogaz [4, 6] | Electricité renouvelable [4, 6] | Réseaux de chaleur décarbonés [4, 6]
- **Run 3 :** Biogaz [4, 6] | Electricité renouvelable [4, 6]
- **Prod :** (aucun levier)
- Leviers intermittents : Biogaz (2/3), Réseaux de chaleur décarbonés (1/3)

> Avec la signature de la charte citoyenne , la CCBV s’engage à faire intervenir plus de citoyens dans les projets L'intérêt est de faire valoir l'apport de l'intégration des citoyens dans les projets au niveau politique avec les élus de la CCBV. La CCBV à adhéré au partenaire RECIT cela permet d'être intégré dans le réseau et d'avoir accès à des webinaires et des formations L'objectif est de sensibiliser les élus mais également de parler aux habitants en montrant qu’ils peuvent s’inscrire dans l…

#### Fiche 72490 — 8. Revitaliser les centres-bourgs

- **Run 1 :** Sobriété des bâtiments (résidentiel) [3, 6]
- **Run 2 :** Sobriété foncière [2, 3]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [2, 3, 6] | Changement chaudières gaz + rénovation (résidentiel) [2, 3, 6] | Sobriété des bâtiments (résidentiel) [2, 3, 6]
- **Prod :** (aucun levier)
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (1/3), Changement chaudières gaz + rénovation (résidentiel) (1/3), Sobriété des bâtiments (résidentiel) (2/3), Sobriété foncière (1/3)

> <p>En 2022, 7,9% des logements du territoire de Baugeois-Vallée sont vacants (INSEE, 2022). Le Programme Local de l’Habitat et le plan d’actions du COT adoptés respectivement en 2022 et en 2024 intègrent des objectifs de réduction des logements vacants et de réhabilitation du parc existant.</p><p>&nbsp;</p><p>·&nbsp;&nbsp;&nbsp;&nbsp; <strong>Encourager les propriétaires à réhabiliter leurs logements vacants pour les remettre sur le marché via la prime « sortie de vacances »&nbsp;</strong>: pou…

#### Fiche 72506 — 23. Favoriser une gouvernance partagée et les projets citoyens pour les projets d’ENR

- **Run 1 :** Biogaz [4, 6] | Electricité renouvelable [4, 6]
- **Run 2 :** Biogaz [4, 6] | Electricité renouvelable [4, 6]
- **Run 3 :** Electricité renouvelable [4, 6]
- **Prod :** (aucun levier)
- Leviers intermittents : Biogaz (2/3)

> <p>Le développement des énergies renouvelables (ENR) suscite des interrogations et nécessite une meilleure acceptabilité. Les projets citoyens ou à gouvernance partagée permettent d’impliquer les habitants et collectivités dans la transition énergétique, en leur offrant une participation directe aux décisions et aux bénéfices. Avec la signature en 2023 de la charte pour des projets d’énergies renouvelables à gouvernance locale en Maine-et-Loire, la CCBV s’engage à faire intervenir plus de citoy…

#### Fiche 144002 — Action 3 : Réduire l’impact climatique des déchets sur le territoire

- **Run 1 :** Captage de méthane dans les ISDND [5, 6]
- **Run 2 :** Prévention des déchets [6]
- **Run 3 :** Prévention des déchets [1, 6]
- **Prod :** (aucun levier)
- Leviers intermittents : Captage de méthane dans les ISDND (1/3), Prévention des déchets (2/3)

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="d3be00f1-0f74-4de1-a0fc-bff01dfde2a9"><div class="bn-block" data-node-type="blockContainer" data-id="d3be00f1-0f74-4de1-a0fc-bff01dfde2a9"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]">Le service gestion et valorisation des déchets, en transversalité avec les autres services de la collect…

#### Fiche 144010 — Action 11 : Lancement d’un appel à manifestation d’intérêts à associations locales pour l’achat et la mise à disposition de broyeurs à végétaux

- **Run 1 :** Valorisation matière des déchets [3, 4]
- **Run 2 :** Prévention des déchets [3, 4]
- **Run 3 :** Valorisation matière des déchets [3, 6]
- **Prod :** Valorisation matière des déchets [3]
- Leviers intermittents : Prévention des déchets (1/3), Valorisation matière des déchets (2/3)

> Une enveloppe peut être proposée à toute structure associative du territoire pour l’achat d’un broyeur à végétaux, voulant s’engager dans la mise à disposition de ce dernier pour les habitants. Cela peut être pour un broyeur à végétaux électrique ou thermique. Pour cela, un appel à manifestation d’intérêt sera proposé.

#### Fiche 144012 — Action 13 : Accompagner des producteurs/commerçants sur les marchés locaux pour réduire le gaspillage alimentaire vers des marchés éco-responsables

- **Run 1 :** Prévention des déchets [4, 6]
- **Run 2 :** Prévention des déchets [4, 6]
- **Run 3 :** Prévention des déchets [4, 6] | Valorisation matière des déchets [6]
- **Prod :** Prévention des déchets [6]
- Leviers intermittents : Valorisation matière des déchets (1/3)

> Accompagnement par Baugeois-Vallée pour réaliser un diagnostic de pesée de tous les flux sur les marchés et sensibilisation au tri. Réalisation d’une charte marchés Eco-responsables et animation auprès des communes et acteurs du marché. Animations auprès des consommateurs. Collecte systématisée des denrées consommables en fin de marché et redistribution (sous une tente anti-gaspi/tente des glaneurs, etc.) ou valorisation invendus dans une conserverie (exemple : valorise) ou en compost des biodé…

#### Fiche 144015 — Action 16 : Inciter à l’acquisition de composteur individuel ou de poulailler

- **Run 1 :** Valorisation matière des déchets [3]
- **Run 2 :** Prévention des déchets [3]
- **Run 3 :** Valorisation matière des déchets [3]
- **Prod :** Valorisation matière des déchets [3, 6]
- Leviers intermittents : Prévention des déchets (1/3), Valorisation matière des déchets (2/3)

> Soutenir les particuliers dans l’équipement en matière de solutions de tri et de valorisation des biodéchets.

#### Fiche 144016 — Action 17 : Développer le compostage partagé de quartier et pour les habitats collectifs

- **Run 1 :** Prévention des déchets [1]
- **Run 2 :** Valorisation matière des déchets [1]
- **Run 3 :** Valorisation matière des déchets [1]
- **Prod :** Valorisation matière des déchets [1, 3]
- Leviers intermittents : Prévention des déchets (1/3), Valorisation matière des déchets (2/3)

> Installation de composteur collectif partagé.

#### Fiche 144017 — Action 18 : Accompagner les établissements scolaires au tri à la source des biodéchets

- **Run 1 :** Prévention des déchets [5, 6]
- **Run 2 :** Valorisation matière des déchets [6]
- **Run 3 :** Valorisation matière des déchets [3, 6]
- **Prod :** Valorisation matière des déchets [1, 5, 6]
- Leviers intermittents : Prévention des déchets (1/3), Valorisation matière des déchets (2/3)

> Accompagner techniquement les demandes des établissements scolaires pour l’installation d’un composteur partagé. Fournir le matériel. Former les référents adultes et les utilisateurs (élèves, enseignantes, autre personnel).

#### Fiche 144018 — Action 19 : Promouvoir la gestion différenciée et le broyage des déchets verts auprès des particuliers

- **Run 1 :** Prévention des déchets [1, 6]
- **Run 2 :** Valorisation matière des déchets [6]
- **Run 3 :** Valorisation matière des déchets [6]
- **Prod :** Valorisation matière des déchets [3, 6]
- Leviers intermittents : Prévention des déchets (1/3), Valorisation matière des déchets (2/3)

> Promouvoir et sensibiliser à une gestion différenciée des espaces verts. Faciliter l’adoption des habitudes de broyage des végétaux pour les valoriser sur son terrain (location de broyeurs, opération en déchèterie, etc.).

#### Fiche 144019 — Action 20 : Installation d’une zone au réemploi en déchèterie

- **Run 1 :** Prévention des déchets [1]
- **Run 2 :** Prévention des déchets [1]
- **Run 3 :** Valorisation matière des déchets [1]
- **Prod :** Prévention des déchets [1] | Valorisation matière des déchets [1]
- Leviers intermittents : Prévention des déchets (2/3), Valorisation matière des déchets (1/3)

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="6b4b674f-29e3-4737-b578-aebe73b2dfa8"><div class="bn-block" data-node-type="blockContainer" data-id="6b4b674f-29e3-4737-b578-aebe73b2dfa8"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]">Installation d’un caisson de réemploi fixe en déchèterie de Baugé, Beaufort et peut-être Noyant. Modalit…

#### Fiche 144021 — Action 22 : Communiquer sur les pratiques réemploi/réparation et mettre en valeur les acteurs du territoire

- **Run 1 :** Prévention des déchets [6]
- **Run 2 :** Prévention des déchets [6]
- **Run 3 :** Valorisation matière des déchets [6]
- **Prod :** Prévention des déchets [6]
- Leviers intermittents : Prévention des déchets (2/3), Valorisation matière des déchets (1/3)

> Communication sur les acteurs du réemploi, de la réparation en transversalité avec le Plan Economie Circulaire. Distribution de guides : « Comment faire de la place chez soi ? ». Proposer plusieurs animations par an sur le don/réemploi : atelier de désencombrement, atelier de réparation, atelier de customisation, etc. Participation à des événements locaux.

#### Fiche 144022 — Action 23 : Accompagner la création d’un repair’café dans le Noyantais

- **Run 1 :** Prévention des déchets [6]
- **Run 2 :** Prévention des déchets [6]
- **Run 3 :** Valorisation matière des déchets [4, 6]
- **Prod :** Prévention des déchets [3, 4, 6]
- Leviers intermittents : Prévention des déchets (2/3), Valorisation matière des déchets (1/3)

> Organiser et animer des événements sur la réparation sur tout le territoire. Accompagner une expérience collective de création d’une association autonome type repair’café sur le Noyantais (animer des réunions de mobilisation autour du projet de repair’café, faciliter la recherche et l’installation dans un local adapté, accompagner l’acquisition de matériel pour démarrer le repair’café). Communication : apport d’un soutien technique au démarrage et relayer les informations du repair’café.

#### Fiche 144027 — Action 28 : Faciliter des collectes spécifiques et le réemploi par les entreprises

- **Run 1 :** Prévention des déchets [6]
- **Run 2 :** Prévention des déchets [4, 6]
- **Run 3 :** Valorisation matière des déchets [6]
- **Prod :** Prévention des déchets [6] | Valorisation matière des déchets [4, 6]
- Leviers intermittents : Prévention des déchets (2/3), Valorisation matière des déchets (1/3)

> Co-assurer l’organisation de collectes spécifiques ou la sensibilisation à certains outils facilitateurs avec le plan Economie Circulaire. Relayer la communication des collectes spécifiques auprès des professionnels.

### Levier intermittent et catégories instables (6)

#### Fiche 32293 — COT 11. Accompagner les restaurants collectifs sur leurs approvisionnements et la sensibilisation des convives

- **Run 1 :** Efficacité et sobriété logistique [6] | Prévention des déchets [6]
- **Run 2 :** Prévention des déchets [4, 6]
- **Run 3 :** Efficacité et sobriété logistique [6] | Prévention des déchets [6]
- **Prod :** Prévention des déchets [6]
- Leviers intermittents : Efficacité et sobriété logistique (2/3)
- Catégories instables sur : Prévention des déchets

> Etape 1 : Diagnostic du fonctionnement des restaurants collectifs du territoire et identifier leurs besoins. Etape 2 : Mettre en place un réseau des restaurants collectifs du territoire afin d’échanger entre pairs autour des bonnes pratiques et de proposer des visites et réunions d’informations (visite de fermes pour les approvisionnements, visite de restaurants collectifs « modèles », démonstrations d’outils d’approvisionnements en produits locaux …) Etape 3 : Proposer 3 accompagnements distin…

#### Fiche 32311 — COT 29. Préserver l'aire de captage de Beaufort

- **Run 1 :** Changements de pratiques de fertilisation azotée [3, 6] | Gestion des haies [4, 6] | Pratiques stockantes [3, 4, 6]
- **Run 2 :** Gestion des haies [2, 4, 6] | Pratiques stockantes [2, 4, 6]
- **Run 3 :** Changements de pratiques de fertilisation azotée [2, 3, 4, 6] | Gestion des haies [2, 3, 4, 6]
- **Prod :** (aucun levier)
- Leviers intermittents : Changements de pratiques de fertilisation azotée (2/3), Pratiques stockantes (2/3)
- Catégories instables sur : Gestion des haies

> Fiabiliser la délimitation de l’aire d’alimentation de captage Mettre en place un comité de suivi Déployer le programme agro environnemental et climatique : - Diagnostic agricole - Dossier de demande auprès de la DRAFF - Communication sur le dispositif - Sollicitation d’agriculteurs volontaires - Accompagnement des agriculteurs Sensibiliser à des pratiques vertueuses (changement de pratique, rotation des cultures…) Réfléchir à une politique foncière autour des captages, maîtrise foncière avec b…

#### Fiche 72498 — 16. Accompagner les employeurs publics/privés et leurs salariés vers l’écomobilité

- **Run 1 :** Covoiturage [3, 4, 5, 6] | Réduction des déplacements [3, 4, 5, 6] | Véhicules électriques [3, 5] | Vélo et transport en commun [3, 4, 5, 6]
- **Run 2 :** Covoiturage [4, 5, 6] | Efficacité et carburants décarbonés des véhicules privés [5, 6] | Réduction des déplacements [4, 5, 6] | Véhicules électriques [4, 5] | Vélo et transport en commun [4, 5, 6]
- **Run 3 :** Covoiturage [4, 5, 6] | Efficacité et carburants décarbonés des véhicules privés [5, 6] | Réduction des déplacements [5, 6] | Véhicules électriques [4, 5, 6] | Vélo et transport en commun [5, 6]
- **Prod :** (aucun levier)
- Leviers intermittents : Efficacité et carburants décarbonés des véhicules privés (2/3)
- Catégories instables sur : Covoiturage, Réduction des déplacements, Véhicules électriques, Vélo et transport en commun

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="d3253af6-2b45-4542-baca-d39f29364681"><div class="bn-block" data-node-type="blockContainer" data-id="d3253af6-2b45-4542-baca-d39f29364681"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]">84% des trajets domicile-travail sur le territoire de Baugeois-Vallée sont effectués en voiture en 2017.…

#### Fiche 72499 — 17. Poursuivre la valorisation de l’énergie produite par l’UVE du SIVERT de l’Anjou

- **Run 1 :** Réseaux de chaleur décarbonés [1, 3, 4]
- **Run 2 :** Electricité renouvelable [4] | Réseaux de chaleur décarbonés [1, 4]
- **Run 3 :** Réseaux de chaleur décarbonés [1, 4, 6]
- **Prod :** Réseaux de chaleur décarbonés [1]
- Leviers intermittents : Electricité renouvelable (1/3)
- Catégories instables sur : Réseaux de chaleur décarbonés

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="da3837c6-1bf7-424a-b202-abca4d871796"><div class="bn-block" data-node-type="blockContainer" data-id="da3837c6-1bf7-424a-b202-abca4d871796"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]">L’Unité de Valorisation Énergétique (UVE) du SIVERT de l’Anjou constitue un atout stratégique pour la pr…

#### Fiche 72507 — 24. Encourager la plantation de haies et d’arbres

- **Run 1 :** Gestion des forêts et produits bois [3, 4, 6] | Gestion des haies [3, 4, 6] | Pratiques stockantes [3, 4, 6]
- **Run 2 :** Gestion des haies [1, 3, 4, 6] | Pratiques stockantes [1, 3, 4, 6]
- **Run 3 :** Gestion des forêts et produits bois [3, 6] | Gestion des haies [3, 6] | Pratiques stockantes [6]
- **Prod :** Gestion des haies [2, 3, 6] | Pratiques stockantes [3, 6]
- Leviers intermittents : Gestion des forêts et produits bois (2/3)
- Catégories instables sur : Gestion des haies, Pratiques stockantes

> <p>La préservation des zones humides et des arbres en place, en particulier les arbres isolés, les haies et les boisements fait partie des grands enjeux du territoire sous l’effet des activités humaines. La CCBV s’inscrit dans une dynamique de reconquête de son paysage et écosystème, appuyée par la charte forestière de territoire, la politique agricole locale et les dispositifs de replantation de haies.</p><p>&nbsp;</p><p>·&nbsp;&nbsp;&nbsp;&nbsp; <strong>Renforcer les plantations de haies et l…

#### Fiche 72508 — 25. Restaurer la biodiversité et les milieux aquatiques

- **Run 1 :** Gestion des haies [1, 4] | Pratiques stockantes [1, 3, 4]
- **Run 2 :** Pratiques stockantes [1, 3, 4, 6]
- **Run 3 :** Gestion des haies [1, 6] | Pratiques stockantes [1, 3] | Sobriété foncière [1]
- **Prod :** Gestion des haies [1] | Gestion des prairies [1] | Pratiques stockantes [1, 3]
- Leviers intermittents : Gestion des haies (2/3), Sobriété foncière (1/3)
- Catégories instables sur : Pratiques stockantes

> <p>Le territoire bénéficie d’un maillage bocager dense et d’un réseau hydrographique riche (rivières, zones humides, nappes phréatiques) aujourd’hui menacés par l’artificialisation, l’intensification des pratiques agricoles, l’urbanisation, et les effets du changement climatique. Ces milieux constituent un levier fort pour répondre aux enjeux croisés de préservation de la biodiversité, gestion de la ressource en eau et adaptation du territoire. L'accord de territoire piloté par le SMBAA, les ac…

### Mêmes leviers, catégories différentes (26)

#### Fiche 32294 — COT 12. Accompagner les banques alimentaires sur leurs approvisionnements et la sensibilisation des bénéficiaires

- **Run 1 :** Prévention des déchets [6]
- **Run 2 :** Prévention des déchets [4, 6]
- **Run 3 :** Prévention des déchets [6]
- **Prod :** Prévention des déchets [6]
- Catégories instables sur : Prévention des déchets

> Pour mener à bien cette action, plusieurs initiatives sont mises en œuvre. D’une part, il s’agit de former les producteurs aux dons agricoles et de les mettre en relation avec les structures d’aide alimentaire. D’autre part, il s’agit de proposer des ateliers cuisine aux bénéficiaires de l’aide alimentaire. 1. Mise en relation des producteurs et des structures d’aide alimentaire Pour cette initiative, la communauté de communes travaille en partenariat avec la Chambre d’agriculture. Celle-ci con…

#### Fiche 32296 — COT 15. Etablir un plan de mobilité interne et mettre en place le forfait mobilité durable

- **Run 1 :** Covoiturage [3, 5] | Réduction des déplacements [3, 5] | Vélo et transport en commun [3, 5]
- **Run 2 :** Covoiturage [3, 5] | Réduction des déplacements [3, 5] | Vélo et transport en commun [3, 5]
- **Run 3 :** Covoiturage [5] | Réduction des déplacements [5] | Vélo et transport en commun [5]
- **Prod :** Covoiturage [5] | Réduction des déplacements [5] | Vélo et transport en commun [3, 5]
- Catégories instables sur : Covoiturage, Réduction des déplacements, Vélo et transport en commun

> - Etablir un diagnostic des déplacements existants domicile-travail et professionnels des agents - Elaborer un plan de mobilité interne et détailler les incitations financières mises en place dans le cadre du FMD (abordant tous les modes de déplacements : marche à pied, vélo, covoiturage, transport en commun, télétravail : redonner les explications si ce n’est pas pris en compte…) - Mettre en œuvre le plan de mobilité interne, communiquer auprès des agents sur le FMD

#### Fiche 32298 — COT 17. Structurer une démarche d'éco-conception auprès des entreprises, avec des outils financiers pour accompagner l'innovation

- **Run 1 :** Production Industrielle [3, 6]
- **Run 2 :** Production Industrielle [3, 4, 6]
- **Run 3 :** Production Industrielle [3, 6]
- **Prod :** Production Industrielle [3, 6]
- Catégories instables sur : Production Industrielle

> L’écoconception vise à réduire significativement l’impact environnemental des organisations en veillant à intégrer de manière systémique la prise en compte des points ci-dessous : 1. Moindre consommation de matières premières et d’énergie 2. Limiter les rejets en milieu naturel et autres pollutions 3. Limiter les incidences sur la biodiversité et le climat L’objectif de l’entreprise est de « faire mieux, avec moins », en veillant à limiter son impact dans son fonctionnement et dans la conceptio…

#### Fiche 32302 — COT 21. Accompagner le développement d'une offre de tourisme et de loisirs "sans ma voiture"

- **Run 1 :** Réduction des déplacements [6] | Vélo et transport en commun [6]
- **Run 2 :** Réduction des déplacements [4, 6] | Vélo et transport en commun [4, 6]
- **Run 3 :** Réduction des déplacements [6] | Vélo et transport en commun [6]
- **Prod :** (aucun levier)
- Catégories instables sur : Réduction des déplacements, Vélo et transport en commun

> - Recenser l’ensemble des offres de transports : Vers Baugeois- Vallée Vers les métropoles (gares) Pointer les Forces, Faiblesses, Opportunités et Menaces. Recensement des offres touristiques et de loisirs sur Baugeois-vallée Rechercher ce qui se fait ailleurs et comment Recouper les données et construire les offres Impliquer les prestataires / habitants (Greeters) / élus dans la démarche Tester Promouvoir/Communiquer

#### Fiche 32306 — COT 24. Mettre en œuvre le plan de prévention des déchets, avec le suivi des objectifs et indicateurs

- **Run 1 :** Prévention des déchets [2, 6]
- **Run 2 :** Prévention des déchets [2, 4]
- **Run 3 :** Prévention des déchets [2, 4]
- **Prod :** (aucun levier)
- Catégories instables sur : Prévention des déchets

> La communauté de communes Baugeois-Vallée, en charge de la compétence « collecte, gestion et valorisation des déchets », doit mettre en place son propre programme, comme prévu par le décret n°2015- 662 du 14 juin 2015. Ce PLPDMA est un document de planification territorial obligatoire depuis le 1er janvier 2012, règlementé par le décret n°2015-662 du 10 juin 2015. Ce plan a été élaboré en 2022 puis validé en 2023. L’objectif du PLPDMA vise la réduction des déchets ménagers et assimilés et d’une…

#### Fiche 32307 — COT 25. Amener les publics éloignés vers l’économie circulaire et la consommation responsable 

- **Run 1 :** Prévention des déchets [3, 6] | Valorisation matière des déchets [3, 6]
- **Run 2 :** Prévention des déchets [3, 4, 6] | Valorisation matière des déchets [3, 4, 6]
- **Run 3 :** Prévention des déchets [3, 6] | Valorisation matière des déchets [3, 6]
- **Prod :** Prévention des déchets [6]
- Catégories instables sur : Prévention des déchets, Valorisation matière des déchets

> Baugeois-Vallée souhaite déployer un programme de sensibilisation et d’accompagnement au changement pour les habitants du territoire. Jusqu’à présent, les actions d’économie circulaire ont surtout été déployées à destination des entreprises du territoire. Il s’agit aujourd’hui de s’adresser également aux citoyens. L’objectif est de cibler plus spécifiquement les publics éloignés de l’économie circulaire et de la consommation responsable. Pour ce faire, le but est de s’adresser à un public dans …

#### Fiche 32308 — COT 26. Engager sur le long terme une démarche globale pour la biodiversité

- **Run 1 :** Gestion des forêts et produits bois [1, 2, 6] | Gestion des haies [1, 2, 6] | Gestion des prairies [1, 2, 6] | Pratiques stockantes [1, 2, 6]
- **Run 2 :** Gestion des forêts et produits bois [1, 2, 6] | Gestion des haies [1, 2, 6] | Gestion des prairies [1, 2, 6] | Pratiques stockantes [1, 2, 6]
- **Run 3 :** Gestion des forêts et produits bois [1, 4, 6] | Gestion des haies [1, 4, 6] | Gestion des prairies [1, 4, 6] | Pratiques stockantes [1, 4, 6]
- **Prod :** (aucun levier)
- Catégories instables sur : Gestion des forêts et produits bois, Gestion des haies, Gestion des prairies, Pratiques stockantes

> 1) Connaitre ABC, diagnostic, état des lieux, SRCE, histoire, dire d’éxpert, inventaire, état de conservation S’appuyer sur les travaux existants 2) Protéger Plan de gestion : préconisation de gestion, actions, aménagements Protection réglementaire et contractuelle Être relais pour les communes te les projets 3) Sensibiliser Animation territoriale Grand public Scolaire Support de communication Se greffer aux évènements existants 28 juin 2025 : etang de belleville et tourbières de Turbily Baugé …

#### Fiche 32309 — COT 27. Préserver et restaurer les zones humides

- **Run 1 :** Pratiques stockantes [1, 4, 6]
- **Run 2 :** Pratiques stockantes [1, 2, 3, 4, 6]
- **Run 3 :** Pratiques stockantes [1, 2, 3, 4, 6]
- **Prod :** (aucun levier)
- Catégories instables sur : Pratiques stockantes

> Définition des objectifs (préservation ressource en eau, stockage de carbone, biodiversité …), identification via l’inventaire des zones humides des sites d’intervention, restaurations, mesures de protections, animations et communication. Mise en œuvre du plan d’actions pour la préservation et la restauration des zones humides Communication auprès du grand public et des acteurs en lien avec les zones humides Plan d’actions : Reprise de l’inventaire des zones humides pour sélectionner avec les c…

#### Fiche 32310 — COT 28. Elaborer une charte forestière, avec un plan d'actions pour préserver et valoriser la forêt

- **Run 1 :** Gestion des forêts et produits bois [4]
- **Run 2 :** Gestion des forêts et produits bois [2, 4]
- **Run 3 :** Gestion des forêts et produits bois [2, 4]
- **Prod :** (aucun levier)
- Catégories instables sur : Gestion des forêts et produits bois

> • Pré diagnostic: Rencontre des interlocuteurs, se donner une vision globale du territoire à un instant t • Diagnostic: Groupe de travail avec des catégories d’acteurs + Groupe de travail hétérogène (mélanger les acteurs) + Diagnostic technique (récolte et analyse de données…) • Plan d’action: 1) Construction : Décrire les actions (solutions possibles, moyens humains et financier, pilotage, partenaires, outils, etc…) 2) Priorisation des actions : Définir lesquelles sont les plus importantes, le…

#### Fiche 72479 — 6. Eco-concevoir et rénover les bâtiments publics de façon écologique, et optimiser l’éclairage public

- **Run 1 :** Electricité renouvelable [5] | Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 2 :** Electricité renouvelable [5] | Sobriété et isolation des bâtiments (tertiaire) [5, 6]
- **Run 3 :** Electricité renouvelable [5, 6] | Sobriété et isolation des bâtiments (tertiaire) [5]
- **Prod :** Electricité renouvelable [5] | Sobriété et isolation des bâtiments (tertiaire) [5]
- Catégories instables sur : Electricité renouvelable, Sobriété et isolation des bâtiments (tertiaire)

> <p>La transition écologique impose une rénovation ambitieuse des bâtiments publics de Baugeois-Vallée, pour réduire leur impact environnemental. Il est crucial d’intégrer des solutions innovantes favorisant le confort d’été, la sobriété énergétique et la biodiversité.</p><p>&nbsp;</p><p>·&nbsp;&nbsp;&nbsp;&nbsp; <strong>Diffuser la charte d’écoconstruction de la CCBV</strong>, structurer l’ingénierie de l’écoconstruction et promouvoir l’utilisation de matériaux biosourcés dans les rénovations p…

#### Fiche 72483 — 7. Renaturer les espaces et équipements publics

- **Run 1 :** Pratiques stockantes [1, 5]
- **Run 2 :** Pratiques stockantes [1, 5]
- **Run 3 :** Pratiques stockantes [1, 5, 6]
- **Prod :** (aucun levier)
- Catégories instables sur : Pratiques stockantes

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="31ab4416-3265-40fc-a1fd-c38543e81fff"><div class="bn-block" data-node-type="blockContainer" data-id="31ab4416-3265-40fc-a1fd-c38543e81fff"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]">Le changement climatique appelle à repenser les aménagements publics. Végétaliser les espaces permet de …

#### Fiche 72491 — 9. Renforcer l'information et l’accompagnement des aides pour les particuliers

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [5, 6] | Changement chaudières gaz + rénovation (résidentiel) [5, 6] | Sobriété des bâtiments (résidentiel) [5, 6]
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [4, 6] | Changement chaudières gaz + rénovation (résidentiel) [4, 6] | Sobriété des bâtiments (résidentiel) [4, 6]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [4, 6] | Changement chaudières gaz + rénovation (résidentiel) [4, 6] | Sobriété des bâtiments (résidentiel) [4, 6]
- **Prod :** (aucun levier)
- Catégories instables sur : Changement chaudières fioul + rénovation (résidentiel), Changement chaudières gaz + rénovation (résidentiel), Sobriété des bâtiments (résidentiel)

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="1dab58aa-8e4a-47f5-8b22-f63240166fd5"><div class="bn-block" data-node-type="blockContainer" data-id="1dab58aa-8e4a-47f5-8b22-f63240166fd5"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]">Le territoire de Baugeois-Vallée compte un parc de logements anciens, dont une part significative pourra…

#### Fiche 72494 — 12. Favoriser le réemploi, la réutilisation et la réparation

- **Run 1 :** Prévention des déchets [1, 3, 6] | Valorisation matière des déchets [1]
- **Run 2 :** Prévention des déchets [1, 3, 4, 6] | Valorisation matière des déchets [1, 3, 4, 6]
- **Run 3 :** Prévention des déchets [1, 3, 4, 6] | Valorisation matière des déchets [1, 3, 4, 6]
- **Prod :** (aucun levier)
- Catégories instables sur : Prévention des déchets, Valorisation matière des déchets

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="7ee77302-ce71-4aab-85ba-0afb7bf3d348"><div class="bn-block" data-node-type="blockContainer" data-id="7ee77302-ce71-4aab-85ba-0afb7bf3d348"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]">La CCBV s’est engagé à élargir son action sur l’économie circulaire dans son COT, notamment sur la conso…

#### Fiche 72495 — 13. Favoriser la pratique du vélo, de la marche à pied et l'activité physique

- **Run 1 :** Vélo et transport en commun [1, 4, 6]
- **Run 2 :** Vélo et transport en commun [1, 2, 4, 6]
- **Run 3 :** Vélo et transport en commun [1, 2, 4, 6]
- **Prod :** Vélo et transport en commun [1]
- Catégories instables sur : Vélo et transport en commun

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="25a5b06d-b8f3-4522-a7fe-7dbf006f8cb9"><div class="bn-block" data-node-type="blockContainer" data-id="25a5b06d-b8f3-4522-a7fe-7dbf006f8cb9"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]">Le secteur des transports routiers constitue le premier poste consommateur d’énergie sur le territoire d…

#### Fiche 72496 — 14. Encourager le covoiturage

- **Run 1 :** Covoiturage [1, 3, 5, 6]
- **Run 2 :** Covoiturage [3, 4, 5, 6]
- **Run 3 :** Covoiturage [1, 3, 4, 5, 6]
- **Prod :** (aucun levier)
- Catégories instables sur : Covoiturage

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="82e0b1f7-1039-4444-b418-21e37dce8746"><div class="bn-block" data-node-type="blockContainer" data-id="82e0b1f7-1039-4444-b418-21e37dce8746"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]">Le secteur des transports routiers constitue le premier poste consommateur d’énergie sur le territoire d…

#### Fiche 72500 — 18. Structurer une filière locale bois-énergie

- **Run 1 :** Gestion des forêts et produits bois [3, 4, 6]
- **Run 2 :** Gestion des forêts et produits bois [3, 4, 6]
- **Run 3 :** Gestion des forêts et produits bois [1, 3, 4, 6]
- **Prod :** (aucun levier)
- Catégories instables sur : Gestion des forêts et produits bois

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="2c28c6de-7683-4c99-9935-eadd9427c5e2"><div class="bn-block" data-node-type="blockContainer" data-id="2c28c6de-7683-4c99-9935-eadd9427c5e2"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]">La gestion forestière sur le territoire Baugeois-Vallée est marquée par une interaction complexe entre l…

#### Fiche 72501 — 19. Développer la méthanisation

- **Run 1 :** Biogaz [4, 6]
- **Run 2 :** Biogaz [4, 6]
- **Run 3 :** Biogaz [2, 4, 6]
- **Prod :** Biogaz [2, 4]
- Catégories instables sur : Biogaz

> <p>Le territoire de la CCBV présente un fort potentiel agricole et des enjeux d’autonomie énergétique, mais le développement de la filière de méthanisation nécessite une structuration cohérente, une bonne acceptabilité sociale, et une coordination étroite entre acteurs publics, agriculteurs et habitants.</p><p>&nbsp;</p><p><strong>Définir une stratégie territoriale de développement de la méthanisation</strong></p><ul><li><p><strong>Identifier les potentiels et acteurs concernés</strong> : carto…

#### Fiche 72503 — 21. Installer des panneaux solaires sur son toit et favoriser l’installation d’ombrières

- **Run 1 :** Electricité renouvelable [5, 6]
- **Run 2 :** Electricité renouvelable [1, 4, 5, 6]
- **Run 3 :** Electricité renouvelable [1, 5, 6]
- **Prod :** Electricité renouvelable [5, 6]
- Catégories instables sur : Electricité renouvelable

> <p>La CCBV dispose d’un gisement solaire important, mis en évidence dans les études du SIEML (cadastre solaire) et l’estimation du potentiel dans le diagnostic du PCAET. Dans le cadre du programme « Le Solaire en Anjou », la collectivité s’est engagée à favoriser l’émergence de projets photovoltaïques sur son territoire, notamment sur les bâtiments publics, les toitures privées et les espaces de stationnement. Cette dynamique s’inscrit aussi dans les obligations réglementaires de solarisation d…

#### Fiche 72504 — 22. Développer le solaire au sol

- **Run 1 :** Electricité renouvelable [2, 4, 6]
- **Run 2 :** Electricité renouvelable [2, 4, 6]
- **Run 3 :** Electricité renouvelable [2, 6]
- **Prod :** Electricité renouvelable [2, 6]
- Catégories instables sur : Electricité renouvelable

> <p>Le territoire bénéficie d’un bon ensoleillement et de nombreuses surfaces disponibles (zones d’activités, friches, anciennes carrières, foncier agricole). L’atlas des sites favorables au solaire et les travaux sur les ZAEnR permettent d’identifier les parcelles à fort potentiel. La CCBV souhaite structurer le développement du solaire au sol en conciliant production d’énergie, respect des sols et de la biodiversité.</p><p>&nbsp;</p><p>·&nbsp;&nbsp;&nbsp;&nbsp; <strong>Identifier les opportuni…

#### Fiche 72509 — 26. Soutenir les agriculteurs vers des pratiques plus durables et adaptées au changement climatique

- **Run 1 :** Changements de pratiques de fertilisation azotée [4, 6] | Elevage durable [4, 6] | Pratiques stockantes [4, 6]
- **Run 2 :** Changements de pratiques de fertilisation azotée [4, 6] | Elevage durable [4, 6] | Pratiques stockantes [4, 6]
- **Run 3 :** Changements de pratiques de fertilisation azotée [6] | Elevage durable [6] | Pratiques stockantes [6]
- **Prod :** Changements de pratiques de fertilisation azotée [6] | Gestion des haies [6] | Gestion des prairies [6] | Pratiques stockantes [3, 6]
- Catégories instables sur : Changements de pratiques de fertilisation azotée, Elevage durable, Pratiques stockantes

> <p>L’agriculture est le premier poste émetteur de gaz à effet de serre sur le territoire de Baugeois-Vallée (41% des émissions en 2023), mais elle constitue aussi un levier majeur d’atténuation grâce au stockage de carbone dans les sols et la biomasse. Elle peut également jouer un rôle central dans l’adaptation au changement climatique en favorisant des systèmes plus résilients et économes en ressources. Toutefois, elle reste très exposée aux impacts climatiques : sécheresses plus fréquentes, p…

#### Fiche 144001 — Action 2 : Animation du PLPDMA

- **Run 1 :** Prévention des déchets [2, 4]
- **Run 2 :** Prévention des déchets [4, 6]
- **Run 3 :** Prévention des déchets [2, 4]
- **Prod :** (aucun levier)
- Catégories instables sur : Prévention des déchets

> Planification et mise en œuvre des actions. Des groupes de travail thématique peuvent émerger en fonction des axes. Les données de résultats et indicateurs sont collectées. Les canaux de communication sont utilisés pour valoriser les actions réalisées. Une synthèse annuelle réalisée à l’issue du programme de 6 ans. Celle-ci est mise à disposition de tous et doit servir de support de communication.

#### Fiche 144003 — Action 4 : Sensibiliser les acteurs des administrations publiques à la prévention des déchets

- **Run 1 :** Prévention des déchets [5, 6]
- **Run 2 :** Prévention des déchets [5, 6]
- **Run 3 :** Prévention des déchets [5]
- **Prod :** Prévention des déchets [5]
- Catégories instables sur : Prévention des déchets

> Etablir un diagnostic des déchets et une pratique commune des administrations publiques et de leurs établissements. Renforcer la politique de consommation éco-responsable de papier bureautique et de dématérialisation des procédures. Renforcer et systématiser la prise en compte de la prévention des déchets dans les politiques d’achats publics. Installer et pérenniser des sites de compostages collectifs pour les employés des collectivités. Envisager la création d’une charte d’engagement des admin…

#### Fiche 144007 — Action 8 : Promotion des initiatives « zéro déchet », consommation durable et ateliers « fait maison »

- **Run 1 :** Prévention des déchets [4, 6]
- **Run 2 :** Prévention des déchets [4, 6]
- **Run 3 :** Prévention des déchets [6]
- **Prod :** Prévention des déchets [6]
- Catégories instables sur : Prévention des déchets

> Transmettre les informations de la collectivité sur la prévention, l’économie circulaire et communiquer sur les actions des groupes ou commerçants. Animer un réseau de groupes « zéro déchet » sur le territoire en proposant des rencontres thématiques. Challenge inter-écoles « zéro déchet ». Parrainage entre citoyens pour partager « trucs et astuces ». Intégrer ces groupes et commerçants dans le temps fort de l’année.

#### Fiche 144011 — Action 12 : Accompagnement de la restauration collective

- **Run 1 :** Prévention des déchets [4, 6]
- **Run 2 :** Prévention des déchets [6]
- **Run 3 :** Prévention des déchets [6]
- **Prod :** (aucun levier)
- Catégories instables sur : Prévention des déchets

> Compléter les diagnostics et accompagner les restaurants collectifs engagés. Participer aux actions de sensibilisations, communications, informations et mises en réseau sur le territoire, notamment initiée par le PAT.

#### Fiche 144014 — Action 15 : Développer chez les métiers de bouches/restaurateurs l’initiative de « doggy bag »

- **Run 1 :** Prévention des déchets [4, 6]
- **Run 2 :** Prévention des déchets [6]
- **Run 3 :** Prévention des déchets [6]
- **Prod :** Prévention des déchets [4, 6]
- Catégories instables sur : Prévention des déchets

> Accompagnement individualisé sur le conventionnement avec les partenaires du développement économique. Campagne de communication.

#### Fiche 144023 — Action 24 : Accompagnement des manifestations responsables

- **Run 1 :** Prévention des déchets [1, 6]
- **Run 2 :** Prévention des déchets [6]
- **Run 3 :** Prévention des déchets [3, 6]
- **Prod :** Prévention des déchets [3, 6] | Valorisation matière des déchets [3, 6]
- Catégories instables sur : Prévention des déchets

> Renforcer l’accompagnement des organisateurs pour réduire et trier correctement. Formation des bénévoles et faire une équipe du tri. Prêt de matériel : points tri (jaune/verre/OMR), panneaux, gobelets réutilisables… Mettre en place Progressivement un accompagnement complet pour les manifestations.

## CC du Pays de Colombey et du Sud Toulois (4707)

- Fiches : **83** — stables sur les 3 runs : **35** (42%), instables : **48**
- Paires levier × catégorie distinctes proposées : 149 — 3/3 runs : 59, 2/3 runs : 48, 1/3 runs : 42
- Vote majoritaire = prod : 19/67 fiches classées d'un côté ou de l'autre
- Réponses JSON invalides rejouées : 0
- Appels : 12 — tokens d'entrée 26 244 (dont 0 en cache, 0%), sortie 72 869 — coût estimé 0.17 $ pour les 3 runs
- Date : 2026-10-30 15:07

### Classée dans certains runs, aucun levier dans d'autres (2)

#### Fiche 51851 — Accompagner des structures éducatives  autour de projets de promotion d’une alimentation saine et durable

- **Run 1 :** Prévention des déchets [6]
- **Run 2 :** Prévention des déchets [6]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Prévention des déchets (2/3)

> Généraliser les partenariats entre cantines et agriculteurs locaux avec des prix convenables

#### Fiche 51863 — création d'une concerverie

- **Run 1 :** Prévention des déchets [1]
- **Run 2 :** (aucun levier)
- **Run 3 :** Prévention des déchets [1]
- **Prod :** (aucun levier)
- Leviers intermittents : Prévention des déchets (2/3)

### Levier présent dans certains runs seulement (18)

#### Fiche 51803 — Promouvoir la VMC double flux

- **Run 1 :** Sobriété des bâtiments (résidentiel) [6]
- **Run 2 :** Sobriété des bâtiments (résidentiel) [6]
- **Run 3 :** Sobriété des bâtiments (résidentiel) [6] | Sobriété et isolation des bâtiments (tertiaire) [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété et isolation des bâtiments (tertiaire) (1/3)

#### Fiche 51804 — Développer, promouvoir la géothermie auprès des particuliers

- **Run 1 :** Réseaux de chaleur décarbonés [6]
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (2/3), Changement chaudières gaz + rénovation (résidentiel) (2/3), Réseaux de chaleur décarbonés (1/3)

#### Fiche 51805 — Communiquer sur les moyens d'isolation

- **Run 1 :** Sobriété des bâtiments (résidentiel) [6]
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6] | Sobriété des bâtiments (résidentiel) [6]
- **Run 3 :** Sobriété des bâtiments (résidentiel) [6] | Sobriété et isolation des bâtiments (tertiaire) [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (1/3), Changement chaudières gaz + rénovation (résidentiel) (1/3), Sobriété et isolation des bâtiments (tertiaire) (1/3)

#### Fiche 51807 — Promouvoir les matériaux biosourcés (laine de bois, laine de mouton …) garantissant à la fois un confort d’été

- **Run 1 :** Sobriété des bâtiments (résidentiel) [6]
- **Run 2 :** Sobriété des bâtiments (résidentiel) [6]
- **Run 3 :** Sobriété des bâtiments (résidentiel) [6] | Sobriété et isolation des bâtiments (tertiaire) [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété et isolation des bâtiments (tertiaire) (1/3)

#### Fiche 51808 — Agir spécifiquement en direction des copropriétés sur la rénovation énergétique

- **Run 1 :** Sobriété des bâtiments (résidentiel) [6]
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6] | Sobriété des bâtiments (résidentiel) [6]
- **Run 3 :** Sobriété des bâtiments (résidentiel) [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (1/3), Changement chaudières gaz + rénovation (résidentiel) (1/3)

#### Fiche 51809 — Donner la priorité à la rénovation énergétique chez les particuliers

- **Run 1 :** Sobriété des bâtiments (résidentiel) [3]
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [3] | Changement chaudières gaz + rénovation (résidentiel) [3] | Sobriété des bâtiments (résidentiel) [3]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [3] | Changement chaudières gaz + rénovation (résidentiel) [3] | Sobriété des bâtiments (résidentiel) [3]
- **Prod :** (aucun levier)
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (2/3), Changement chaudières gaz + rénovation (résidentiel) (2/3)

#### Fiche 51811 — Sensibiliser les décideurs locaux (élus et pétitionnaire lors des dépôts de permis de construire) aux économies d’énergies et énergies renouvelables.

- **Run 1 :** Electricité renouvelable [6] | Sobriété des bâtiments (résidentiel) [6]
- **Run 2 :** Sobriété des bâtiments (résidentiel) [6] | Sobriété et isolation des bâtiments (tertiaire) [6]
- **Run 3 :** Electricité renouvelable [6] | Sobriété des bâtiments (résidentiel) [6] | Sobriété et isolation des bâtiments (tertiaire) [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Electricité renouvelable (2/3), Sobriété et isolation des bâtiments (tertiaire) (2/3)

#### Fiche 51817 — Explorer les possibilités réglementaires (PLUI) pour encourager les plantations

- **Run 1 :** Gestion des forêts et produits bois [2] | Pratiques stockantes [2]
- **Run 2 :** Gestion des forêts et produits bois [2] | Pratiques stockantes [2]
- **Run 3 :** Gestion des forêts et produits bois [2] | Gestion des haies [2]
- **Prod :** Gestion des forêts et produits bois [2]
- Leviers intermittents : Gestion des haies (1/3), Pratiques stockantes (2/3)

> dans les espaces constructibles, les zones commerciales, industrielles (végétalisation, arbres..). Sanctuariser certains secteurs de forêts

#### Fiche 51819 — Connaître et protéger les terres agricoles et les espaces naturels de l’artificialisation des sols via les documents d’urbanisme et la politique foncière associée

- **Run 1 :** Sobriété foncière [2]
- **Run 2 :** Gestion des prairies [2] | Pratiques stockantes [2] | Sobriété foncière [2]
- **Run 3 :** Pratiques stockantes [2] | Sobriété foncière [2]
- **Prod :** Sobriété foncière [2]
- Leviers intermittents : Gestion des prairies (1/3), Pratiques stockantes (2/3)

#### Fiche 51820 — Développer un réseau de pistes cyclables sécurisées en site propre.

- **Run 1 :** Vélo et transport en commun [1]
- **Run 2 :** Réduction des déplacements [1] | Vélo et transport en commun [1]
- **Run 3 :** Vélo et transport en commun [1]
- **Prod :** Vélo et transport en commun [1]
- Leviers intermittents : Réduction des déplacements (1/3)

> Développer un réseau de pistes cyclables sécurisées en site propre pour un usage utilitaire au quotidien, sur les routes départementales et nationales entre les communes mais aussi dans les centre-ville

#### Fiche 51821 — Mettre en place certaines voies vertes (en réflexion avec le département)

- **Run 1 :** Vélo et transport en commun [1]
- **Run 2 :** Réduction des déplacements [1] | Vélo et transport en commun [1]
- **Run 3 :** Vélo et transport en commun [1]
- **Prod :** (aucun levier)
- Leviers intermittents : Réduction des déplacements (1/3)

#### Fiche 51822 — Mise à jour de la "Mobilité", dans le PLUi

- **Run 1 :** Réduction des déplacements [2]
- **Run 2 :** Covoiturage [2] | Réduction des déplacements [2] | Vélo et transport en commun [2]
- **Run 3 :** Réduction des déplacements [2]
- **Prod :** (aucun levier)
- Leviers intermittents : Covoiturage (1/3), Vélo et transport en commun (1/3)

#### Fiche 51823 — Promouvoir le covoiturage sur des axes passants (ligne de covoiturage)

- **Run 1 :** Covoiturage [6]
- **Run 2 :** Covoiturage [6] | Réduction des déplacements [6]
- **Run 3 :** Covoiturage [6]
- **Prod :** Covoiturage [6]
- Leviers intermittents : Réduction des déplacements (1/3)

#### Fiche 51824 — Covoiturage de proximité

- **Run 1 :** Covoiturage [6]
- **Run 2 :** Covoiturage [6] | Réduction des déplacements [6]
- **Run 3 :** Covoiturage [6]
- **Prod :** Covoiturage [4]
- Leviers intermittents : Réduction des déplacements (1/3)

> : essaimer la démarché initiée dans la commune de Courcelles en proposant aux habitants de partager une boite mail covoiturage.[nomdelacommune]@_____.fr : chaque habitant peut proposer un trajet ponctuel ou régulier sur la boite mail.

#### Fiche 51825 — Créer un groupe d'ambassadeurs qui informe la population sur les offres de mobilité dans chaque village

- **Run 1 :** Réduction des déplacements [6]
- **Run 2 :** Covoiturage [6] | Réduction des déplacements [6] | Vélo et transport en commun [6]
- **Run 3 :** Covoiturage [6] | Réduction des déplacements [6] | Vélo et transport en commun [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Covoiturage (2/3), Vélo et transport en commun (2/3)

#### Fiche 51840 — Coordonner les documents d'urbanisme et la transition écologique

- **Run 1 :** Electricité renouvelable [2]
- **Run 2 :** Sobriété foncière [2]
- **Run 3 :** Electricité renouvelable [2] | Sobriété foncière [2]
- **Prod :** (aucun levier)
- Leviers intermittents : Electricité renouvelable (2/3), Sobriété foncière (2/3)

> Concilier Transition écologique et autorisation des EnR dans "l'architecture" et dans "l'aménagement" du territoire / SCOT, PLUi, PLU…

#### Fiche 51841 — Accompagner les démarches de plantation et de gestion de l’arbre agricole

- **Run 1 :** Gestion des haies [6] | Pratiques stockantes [6]
- **Run 2 :** Pratiques stockantes [6]
- **Run 3 :** Pratiques stockantes [6]
- **Prod :** Pratiques stockantes [6]
- Leviers intermittents : Gestion des haies (1/3)

#### Fiche 51857 — Engager une démarche d'Ecologie Industrielle Territoriale

- **Run 1 :** Efficacité et sobriété logistique [4] | Production Industrielle [4] | Valorisation matière des déchets [4]
- **Run 2 :** Efficacité et sobriété logistique [4] | Production Industrielle [4] | Prévention des déchets [4] | Valorisation matière des déchets [4]
- **Run 3 :** Production Industrielle [4] | Valorisation matière des déchets [4]
- **Prod :** Efficacité et sobriété logistique [4] | Production Industrielle [4]
- Leviers intermittents : Efficacité et sobriété logistique (2/3), Prévention des déchets (1/3)

### Levier intermittent et catégories instables (5)

#### Fiche 51810 — Responsabiliser les propriétaires à effectuer des travaux efficaces

- **Run 1 :** Sobriété des bâtiments (résidentiel) [2]
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [2] | Changement chaudières gaz + rénovation (résidentiel) [2] | Sobriété des bâtiments (résidentiel) [2]
- **Run 3 :** Sobriété des bâtiments (résidentiel) [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (1/3), Changement chaudières gaz + rénovation (résidentiel) (1/3)
- Catégories instables sur : Sobriété des bâtiments (résidentiel)

#### Fiche 51848 — Les surplus de broyage des plates-formes sont proposés en apport carbone pour épandage.

- **Run 1 :** Pratiques stockantes [1] | Valorisation matière des déchets [1]
- **Run 2 :** Pratiques stockantes [6]
- **Run 3 :** Pratiques stockantes [1]
- **Prod :** Pratiques stockantes [6]
- Leviers intermittents : Valorisation matière des déchets (1/3)
- Catégories instables sur : Pratiques stockantes

#### Fiche 51854 — Favoriser l’arbre dans les politiques d’entretien des cours d’eau (ripisylve)

- **Run 1 :** Gestion des haies [1] | Pratiques stockantes [1]
- **Run 2 :** Gestion des haies [1] | Pratiques stockantes [1]
- **Run 3 :** Pratiques stockantes [2]
- **Prod :** Gestion des forêts et produits bois [1] | Gestion des haies [1]
- Leviers intermittents : Gestion des haies (2/3)
- Catégories instables sur : Pratiques stockantes

#### Fiche 51862 — lavage de laine, re localisation et mutualisation d'un outil de lavage

- **Run 1 :** Fret décarboné et multimodalité [4] | Production Industrielle [4]
- **Run 2 :** Efficacité et sobriété logistique [4] | Production Industrielle [1, 4]
- **Run 3 :** Efficacité et sobriété logistique [1, 4] | Production Industrielle [1, 4]
- **Prod :** (aucun levier)
- Leviers intermittents : Efficacité et sobriété logistique (2/3), Fret décarboné et multimodalité (1/3)
- Catégories instables sur : Production Industrielle

#### Fiche 51878 — Réduire les déchets à la source en déchetterie et mettre en place une recyclerie

- **Run 1 :** Prévention des déchets [6] | Valorisation matière des déchets [1]
- **Run 2 :** Prévention des déchets [1] | Valorisation matière des déchets [1]
- **Run 3 :** Prévention des déchets [1, 6]
- **Prod :** Prévention des déchets [1] | Valorisation matière des déchets [1]
- Leviers intermittents : Valorisation matière des déchets (2/3)
- Catégories instables sur : Prévention des déchets

> Mise en place d'une recyclerie sur la ccpcst

### Mêmes leviers, catégories différentes (23)

#### Fiche 51813 — Elargir la mission du conseiller Energie Collectivité sur l'accompagnement global air - climat - énergie des collectivités locales (dont l'adaptation aux changements climatiques)

- **Run 1 :** Sobriété des bâtiments (résidentiel) [6]
- **Run 2 :** Sobriété des bâtiments (résidentiel) [4, 6]
- **Run 3 :** Sobriété des bâtiments (résidentiel) [4, 6]
- **Prod :** Sobriété des bâtiments (résidentiel) [6] | Sobriété et isolation des bâtiments (tertiaire) [6]
- Catégories instables sur : Sobriété des bâtiments (résidentiel)

> Rendre accessible l’information sur le confort d’été et les techniques permettant d’améliorer le confort d’été ; communiquer sur des actions simples à mettre en œuvre, promouvoir les isolants biosourcés. Cibles : collectivités et particuliers

#### Fiche 51826 — Positionner la gare de Barisey la Côte comme gare de ferroutage (en lien avec la sortie de l’A31 à Allain)

- **Run 1 :** Fret décarboné et multimodalité [1, 4]
- **Run 2 :** Fret décarboné et multimodalité [1]
- **Run 3 :** Fret décarboné et multimodalité [1]
- **Prod :** Fret décarboné et multimodalité [4]
- Catégories instables sur : Fret décarboné et multimodalité

#### Fiche 51828 — Quid du contexte COVID19 et de l'arrivée de la fibre optique sur le territoire, les habitants se lancent dans le télétravail, coworking, etc.

- **Run 1 :** Réduction des déplacements [1, 6]
- **Run 2 :** Réduction des déplacements [6]
- **Run 3 :** Réduction des déplacements [6]
- **Prod :** (aucun levier)
- Catégories instables sur : Réduction des déplacements

#### Fiche 51829 — Favoriser et accompagner le développement de parcs solaires au sol dans le cadre d'un AMI photovoltaïque participatif

- **Run 1 :** Electricité renouvelable [3, 4]
- **Run 2 :** Electricité renouvelable [4, 6]
- **Run 3 :** Electricité renouvelable [3, 6]
- **Prod :** Electricité renouvelable [4]
- Catégories instables sur : Electricité renouvelable

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="bee41327-d1b9-4e91-ae35-1e4de3cfcdf9"><div class="bn-block" data-node-type="blockContainer" data-id="bee41327-d1b9-4e91-ae35-1e4de3cfcdf9"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]">Inciter des collectivités à l'investissement dans des parcs solaires, sur des surfaces toitures, friches…

#### Fiche 51830 — Développer des projets collectifs d'installations photovoltaïques en autoconsommation collective notamment sur les zones d'activités du territoire (4 zones en expérimentation : zone en Prave)

- **Run 1 :** Electricité renouvelable [2, 6]
- **Run 2 :** Electricité renouvelable [4, 6]
- **Run 3 :** Electricité renouvelable [4]
- **Prod :** Electricité renouvelable [4]
- Catégories instables sur : Electricité renouvelable

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="d910f251-69de-4bac-a065-3701983298e8"><div class="bn-block" data-node-type="blockContainer" data-id="d910f251-69de-4bac-a065-3701983298e8"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]">4 zones en expérimentation : Zone en Prave sur la Communauté de Communes</p></div></div></div></div>

#### Fiche 51835 — Initier une réflexion territoriale sur la méthanisation

- **Run 1 :** Biogaz [1, 4]
- **Run 2 :** Biogaz [1, 4]
- **Run 3 :** Biogaz [4]
- **Prod :** Biogaz [4] | Réseaux de chaleur décarbonés [4]
- Catégories instables sur : Biogaz

> Organiser une collecte des biodéchets pour la méthanisation du territoire : déchets de cantine, … Valoriser la chaleur des unité de méthanisation en cogénération

#### Fiche 51837 — Mettre en place (ou accompagner la mise en place) une filière locale bois énergie

- **Run 1 :** Gestion des forêts et produits bois [1, 4] | Réseaux de chaleur décarbonés [1]
- **Run 2 :** Gestion des forêts et produits bois [4] | Réseaux de chaleur décarbonés [1]
- **Run 3 :** Gestion des forêts et produits bois [4] | Réseaux de chaleur décarbonés [1]
- **Prod :** Gestion des forêts et produits bois [4] | Réseaux de chaleur décarbonés [1]
- Catégories instables sur : Gestion des forêts et produits bois

> ...de la forêt à la chaufferie bois. Création d'une usine de production de plaquette, pellet, ressource forestière : stockage de ressource territoire. Bois bûche, pellet, plaquette, bois broyé, etc. Favoriser le déploiement de réseaux de chaleur biomasse dans les communes « compactes » (village rue « lorrain ») forestières pour l’entretien des forêts communales

#### Fiche 51839 — Saisir les opportunités d'énergie verte et de stockage

- **Run 1 :** Electricité renouvelable [1]
- **Run 2 :** Electricité renouvelable [4]
- **Run 3 :** Electricité renouvelable [1]
- **Prod :** Electricité renouvelable [1]
- Catégories instables sur : Electricité renouvelable

> Créer de l'énergie verte avec les ENRs afin de fabriquer de l'hydrogène, Installation d'une petite unité de production d'hydrogène

#### Fiche 51842 — Travailler au développement d’une agriculture alternative favorisant la préservation des sols

- **Run 1 :** Pratiques stockantes [6]
- **Run 2 :** Pratiques stockantes [6]
- **Run 3 :** Pratiques stockantes [4]
- **Prod :** (aucun levier)
- Catégories instables sur : Pratiques stockantes

#### Fiche 51844 — Elaborer et mettre en oeuvre un Plan d'Approvisionnement Territorial Bois (PAT)

- **Run 1 :** Gestion des forêts et produits bois [2]
- **Run 2 :** Gestion des forêts et produits bois [2]
- **Run 3 :** Gestion des forêts et produits bois [4]
- **Prod :** (aucun levier)
- Catégories instables sur : Gestion des forêts et produits bois

#### Fiche 51845 — Mobiliser les propriétaires forestiers pour un développement de la filière forêt-bois locale

- **Run 1 :** Gestion des forêts et produits bois [6]
- **Run 2 :** Gestion des forêts et produits bois [4, 6]
- **Run 3 :** Gestion des forêts et produits bois [4]
- **Prod :** Gestion des forêts et produits bois [4]
- Catégories instables sur : Gestion des forêts et produits bois

#### Fiche 51847 — Développer l'agroforesterie sur le territoire , favoriser la plantation de haies. Rendre l'entretien des haies gratuit pour les agriculteurs

- **Run 1 :** Gestion des haies [3, 6] | Pratiques stockantes [3, 6]
- **Run 2 :** Gestion des haies [1, 3, 6] | Pratiques stockantes [6]
- **Run 3 :** Gestion des haies [1, 3] | Pratiques stockantes [1]
- **Prod :** Gestion des haies [3, 6] | Pratiques stockantes [3, 6]
- Catégories instables sur : Gestion des haies, Pratiques stockantes

#### Fiche 51849 — Recenser le foncier agricole communal disponible

- **Run 1 :** Sobriété foncière [2, 3, 6]
- **Run 2 :** Sobriété foncière [3, 4]
- **Run 3 :** Sobriété foncière [2, 3, 6]
- **Prod :** (aucun levier)
- Catégories instables sur : Sobriété foncière

> Aider à l'implantation de producteurs locaux « cultures végétales » (mobilisation du foncier disponible, subvention à l’installation …) dont les productions sont destinées au marché local

#### Fiche 51852 — Mettre en place (ou accompagner la mise en place) une filière locale bois énergie

- **Run 1 :** Gestion des forêts et produits bois [1, 4] | Réseaux de chaleur décarbonés [1]
- **Run 2 :** Gestion des forêts et produits bois [4] | Réseaux de chaleur décarbonés [1]
- **Run 3 :** Gestion des forêts et produits bois [1, 4] | Réseaux de chaleur décarbonés [1, 4]
- **Prod :** Gestion des forêts et produits bois [1, 4] | Réseaux de chaleur décarbonés [1, 4]
- Catégories instables sur : Gestion des forêts et produits bois, Réseaux de chaleur décarbonés

> ...de la forêt à la chaufferie bois. Création d'une usine de production de plaquette, pellet, ressource forestière : stockage de ressource territoire. Bois bûche, pellet, plaquette, bois broyé, etc. Favoriser le déploiement de réseaux de chaleur biomasse dans les communes « compactes » (village rue « lorrain ») forestières pour l’entretien des forêts communales

#### Fiche 51853 — Développer un plan « Haies

- **Run 1 :** Gestion des haies [4]
- **Run 2 :** Gestion des haies [2, 4]
- **Run 3 :** Gestion des haies [2]
- **Prod :** Gestion des haies [2]
- Catégories instables sur : Gestion des haies

#### Fiche 51855 — Mobiliser les enfants et les enseignants : politiques de plantation par les écoles, associer les enfants à la démarche de plantation de la commune, Instaurer un seuil minimal de plantations dans les villages

- **Run 1 :** Pratiques stockantes [1, 6]
- **Run 2 :** Pratiques stockantes [1, 6]
- **Run 3 :** Pratiques stockantes [6]
- **Prod :** Gestion des forêts et produits bois [1, 6]
- Catégories instables sur : Pratiques stockantes

#### Fiche 51858 — Développer des projets collectifs d'installations photovoltaïques

- **Run 1 :** Electricité renouvelable [1, 4]
- **Run 2 :** Electricité renouvelable [1, 4]
- **Run 3 :** Electricité renouvelable [1]
- **Prod :** Electricité renouvelable [1, 4]
- Catégories instables sur : Electricité renouvelable

#### Fiche 51859 — Mettre en place une station de lavage et de location de gobelets réutilisables à destination des acteurs culturels, entreprises

- **Run 1 :** Prévention des déchets [1]
- **Run 2 :** Prévention des déchets [1, 4]
- **Run 3 :** Prévention des déchets [1]
- **Prod :** Prévention des déchets [1]
- Catégories instables sur : Prévention des déchets

#### Fiche 51860 — Espace télétravail, coworking, tier-lieux

- **Run 1 :** Réduction des déplacements [1]
- **Run 2 :** Réduction des déplacements [1, 4]
- **Run 3 :** Réduction des déplacements [1]
- **Prod :** Réduction des déplacements [1]
- Catégories instables sur : Réduction des déplacements

> Quid du contexte COVID19 et de l'arrivée de la fibre optique sur le territoire, les habitants se lancent dans le télétravail, coworking, etc.

#### Fiche 51864 — limiter la production de déchets et le gaspillage alimentaire auprès des artisans des métiers de bouche et des commerçants du territoire Terres de Lorraine

- **Run 1 :** Prévention des déchets [6]
- **Run 2 :** Prévention des déchets [4, 6]
- **Run 3 :** Prévention des déchets [6]
- **Prod :** Prévention des déchets [6]
- Catégories instables sur : Prévention des déchets

#### Fiche 51866 — flux de déchets autres (ex : filière carton ?)

- **Run 1 :** Valorisation matière des déchets [1, 4]
- **Run 2 :** Valorisation matière des déchets [1, 4]
- **Run 3 :** Valorisation matière des déchets [1]
- **Prod :** (aucun levier)
- Catégories instables sur : Valorisation matière des déchets

#### Fiche 51879 — Favoriser un compostage et paillage de qualité afin de réduire les Gaz à Effet de Serre

- **Run 1 :** Valorisation matière des déchets [6]
- **Run 2 :** Valorisation matière des déchets [4]
- **Run 3 :** Valorisation matière des déchets [6]
- **Prod :** Valorisation matière des déchets [6]
- Catégories instables sur : Valorisation matière des déchets

#### Fiche 140199 — Prioriser les construction neuves dans les dents creuses et notamment dans le sud du territoire. Croiser et coordonner les axes air climat énergie du PADD et le PCAET

- **Run 1 :** Sobriété foncière [2]
- **Run 2 :** Sobriété foncière [2, 4]
- **Run 3 :** Sobriété foncière [2]
- **Prod :** Sobriété foncière [2]
- Catégories instables sur : Sobriété foncière

## CC du Pays de Barr (4939)

- Fiches : **41** — stables sur les 3 runs : **29** (71%), instables : **12**
- Paires levier × catégorie distinctes proposées : 51 — 3/3 runs : 32, 2/3 runs : 9, 1/3 runs : 10
- Vote majoritaire = prod : 23/39 fiches classées d'un côté ou de l'autre
- Réponses JSON invalides rejouées : 0
- Appels : 6 — tokens d'entrée 261 246 (dont 0 en cache, 0%), sortie 36 279 — coût estimé 0.25 $ pour les 3 runs
- Date : 2026-10-30 14:38

### Classée dans certains runs, aucun levier dans d'autres (2)

#### Fiche 130822 — 4.1. Créer une plateforme de mobilité pour accompagner individuellement les habitants aux besoins particuliers

- **Run 1 :** (aucun levier)
- **Run 2 :** Vélo et transport en commun [6]
- **Run 3 :** Vélo et transport en commun [6]
- **Prod :** Vélo et transport en commun [6]
- Leviers intermittents : Vélo et transport en commun (2/3)

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="f0e19d0e-ee66-40f7-93bf-8b396b1df8c4"><div class="bn-block" data-node-type="blockContainer" data-id="f0e19d0e-ee66-40f7-93bf-8b396b1df8c4"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]"></p></div></div></div><div class="bn-block-outer" data-node-type="blockOuter" data-id="d63c0cde-1a50-4b8…

#### Fiche 130823 — 4.2. Transformer le Transport à la demande pour y inclure une visée sociale

- **Run 1 :** (aucun levier)
- **Run 2 :** Vélo et transport en commun [1]
- **Run 3 :** (aucun levier)
- **Prod :** Vélo et transport en commun [1]
- Leviers intermittents : Vélo et transport en commun (1/3)

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="44762517-63fe-40e0-91be-20c2c24e371e"><div class="bn-block" data-node-type="blockContainer" data-id="44762517-63fe-40e0-91be-20c2c24e371e"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]"></p></div></div></div><div class="bn-block-outer" data-node-type="blockOuter" data-id="282eee0c-f822-4fd…

### Levier présent dans certains runs seulement (3)

#### Fiche 88373 — 3.1.1.3. Accompagner les entreprises à réaliser leur plan de mobilités

- **Run 1 :** Covoiturage [6] | Réduction des déplacements [6] | Vélo et transport en commun [6]
- **Run 2 :** Réduction des déplacements [6] | Vélo et transport en commun [6]
- **Run 3 :** Réduction des déplacements [6]
- **Prod :** Réduction des déplacements [6] | Vélo et transport en commun [6]
- Leviers intermittents : Covoiturage (1/3), Vélo et transport en commun (2/3)

> <p class="!text-base !text-grey-8 font-[Marianne]">Le territoire du Pays de Barr est structuré par&nbsp;9 zones d’activités et artisanales au centre du territoire (Barr, Andlau, Saint-Pierre, Valff, Epfig), au sud (Dambach-la-Ville) et au Nord (Valff).</p><p>&nbsp;</p><p class="!text-base !text-grey-8 font-[Marianne]">Sur le territoire, 80% des entreprises compte moins de 10 salariés (1376 entreprises), 12% plus de 10 (201 entreprises) et 8% sont sans salarié.</p><p>&nbsp;</p><p class="!text-ba…

#### Fiche 130281 — 1.3. Accompagner les entreprises à réaliser leur plan de mobilités

- **Run 1 :** Covoiturage [6] | Réduction des déplacements [6] | Vélo et transport en commun [6]
- **Run 2 :** Réduction des déplacements [6] | Vélo et transport en commun [6]
- **Run 3 :** Réduction des déplacements [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Covoiturage (1/3), Vélo et transport en commun (2/3)

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="454f05cc-f6a8-42c9-b5e8-afe523b4da04"><div class="bn-block" data-node-type="blockContainer" data-id="454f05cc-f6a8-42c9-b5e8-afe523b4da04"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]"></p></div></div></div><div class="bn-block-outer" data-node-type="blockOuter" data-id="cc84fa66-4286-4db…

#### Fiche 130317 — 2.4. Créer des services de proximité et un pôle multimodal en gare de Barr

- **Run 1 :** Covoiturage [1] | Vélo et transport en commun [1]
- **Run 2 :** Covoiturage [1] | Vélo et transport en commun [1]
- **Run 3 :** Vélo et transport en commun [1]
- **Prod :** Réduction des déplacements [1] | Vélo et transport en commun [1]
- Leviers intermittents : Covoiturage (2/3)

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="5ab76ae6-4e49-4cb5-bda5-a4730093df88"><div class="bn-block" data-node-type="blockContainer" data-id="5ab76ae6-4e49-4cb5-bda5-a4730093df88"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]"></p></div></div></div><div class="bn-block-outer" data-node-type="blockOuter" data-id="e0120c6d-91fc-4c8…

### Mêmes leviers, catégories différentes (7)

#### Fiche 88612 — 3.1.3.2. Accompagner les communes dans la réalisation de plans vélos communaux

- **Run 1 :** Vélo et transport en commun [4]
- **Run 2 :** Vélo et transport en commun [4, 6]
- **Run 3 :** Vélo et transport en commun [4]
- **Prod :** Vélo et transport en commun [4]
- Catégories instables sur : Vélo et transport en commun

> <p class="!text-base !text-grey-8 font-[Marianne]">En 2022, la Communauté de communes a lancé l’étude de son Plan vélo intercommunal.</p><p class="!text-base !text-grey-8 font-[Marianne]">Ce plan ne concerne que les liaisons intercommunales&nbsp;: pour assurer une continuité à l’échelle intra-communale, il est essentiel que les communes aménagent les agglomérations en tendant vers des espaces partagés, le tout en suivant les recommandations du CEREMA.</p><p class="!text-base !text-grey-8 font-[…

#### Fiche 88652 — 3.1.4.1. Former les élus aux aménagements de voirie partagée

- **Run 1 :** Vélo et transport en commun [4]
- **Run 2 :** Vélo et transport en commun [6]
- **Run 3 :** Vélo et transport en commun [4]
- **Prod :** Vélo et transport en commun [6]
- Catégories instables sur : Vélo et transport en commun

> <p class="!text-base !text-grey-8 font-[Marianne]">Le territoire est caractérisé par un déséquilibre dans le partage de voirie. Cette situation pousse les individus à utiliser la voiture au détriment des modes actifs.</p><p class="!text-base !text-grey-8 font-[Marianne]">Par conséquent, le territoire est marqué par une part modale du vélo relativement faible, tous motifs de déplacements confondus.</p><p class="!text-base !text-grey-8 font-[Marianne]">Le vélo est principalement utilisé à des fin…

#### Fiche 130806 — 3.5. Accompagner les communes dans la réalisation de plan vélos communaux

- **Run 1 :** Vélo et transport en commun [6]
- **Run 2 :** Vélo et transport en commun [4, 6]
- **Run 3 :** Vélo et transport en commun [6]
- **Prod :** Vélo et transport en commun [4]
- Catégories instables sur : Vélo et transport en commun

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="abee81b8-a6ab-4f16-a9e9-cb988b067b3c"><div class="bn-block" data-node-type="blockContainer" data-id="abee81b8-a6ab-4f16-a9e9-cb988b067b3c"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]"></p></div></div></div><div class="bn-block-outer" data-node-type="blockOuter" data-id="cfcde562-d1e0-45c…

#### Fiche 130824 — 5.1. Expérimenter le covoiturage

- **Run 1 :** Covoiturage [4]
- **Run 2 :** Covoiturage [1]
- **Run 3 :** Covoiturage [4]
- **Prod :** Covoiturage [4]
- Catégories instables sur : Covoiturage

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="018c22db-db47-4cf5-9b9d-975787ec3367"><div class="bn-block" data-node-type="blockContainer" data-id="018c22db-db47-4cf5-9b9d-975787ec3367"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]"></p></div></div></div><div class="bn-block-outer" data-node-type="blockOuter" data-id="fe0b0584-6aaa-472…

#### Fiche 130825 — 5.2. Expérimenter l'autopartage

- **Run 1 :** Véhicules électriques [4]
- **Run 2 :** Véhicules électriques [1]
- **Run 3 :** Véhicules électriques [1]
- **Prod :** Covoiturage [1, 4]
- Catégories instables sur : Véhicules électriques

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="d8117350-defc-4817-8217-b8eb26890dd9"><div class="bn-block" data-node-type="blockContainer" data-id="d8117350-defc-4817-8217-b8eb26890dd9"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]"></p></div></div></div><div class="bn-block-outer" data-node-type="blockOuter" data-id="18b7ecca-7a02-4e4…

#### Fiche 130868 — 6.2. Former les élus aux aménagements de voirie partagée

- **Run 1 :** Vélo et transport en commun [4]
- **Run 2 :** Vélo et transport en commun [6]
- **Run 3 :** Vélo et transport en commun [6]
- **Prod :** Vélo et transport en commun [6]
- Catégories instables sur : Vélo et transport en commun

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="9f37cfe2-3c85-4371-a203-be884b8bbce9"><div class="bn-block" data-node-type="blockContainer" data-id="9f37cfe2-3c85-4371-a203-be884b8bbce9"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]"></p></div></div></div><div class="bn-block-outer" data-node-type="blockOuter" data-id="95bac590-a7ec-49a…

#### Fiche 130869 — 6.3. Former les agents pour accompagner les citoyens dans leur mobilité

- **Run 1 :** Vélo et transport en commun [5]
- **Run 2 :** Vélo et transport en commun [6]
- **Run 3 :** Vélo et transport en commun [5]
- **Prod :** Vélo et transport en commun [6]
- Catégories instables sur : Vélo et transport en commun

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="96bd6404-258c-4f99-b999-8d417e3f0ba2"><div class="bn-block" data-node-type="blockContainer" data-id="96bd6404-258c-4f99-b999-8d417e3f0ba2"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]"></p></div></div></div><div class="bn-block-outer" data-node-type="blockOuter" data-id="786a2034-973b-49d…

## CC Sundgau (4973)

- Fiches : **37** — stables sur les 3 runs : **22** (59%), instables : **15**
- Paires levier × catégorie distinctes proposées : 62 — 3/3 runs : 34, 2/3 runs : 12, 1/3 runs : 16
- Aucune classification en prod pour cette collectivité
- Réponses JSON invalides rejouées : 0
- Appels : 6 — tokens d'entrée 14 304 (dont 0 en cache, 0%), sortie 39 104 — coût estimé 0.09 $ pour les 3 runs
- Date : 2026-10-30 14:38

### Classée dans certains runs, aucun levier dans d'autres (3)

#### Fiche 17145 — Déploiement d'ateliers de cuisine à destination des habitants

- **Run 1 :** Prévention des déchets [6]
- **Run 2 :** Prévention des déchets [6]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Prévention des déchets (2/3)

#### Fiche 53163 — organiser des visites de jardins et prise de parole de jardiniers

- **Run 1 :** Pratiques stockantes [6] | Prévention des déchets [6]
- **Run 2 :** (aucun levier)
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Pratiques stockantes (1/3), Prévention des déchets (1/3)

#### Fiche 53164 — diffuser le savoir-faire des éco-jardiniers du Sundgau

- **Run 1 :** Pratiques stockantes [6] | Prévention des déchets [6]
- **Run 2 :** (aucun levier)
- **Run 3 :** Pratiques stockantes [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Pratiques stockantes (2/3), Prévention des déchets (1/3)

### Levier présent dans certains runs seulement (10)

#### Fiche 42050 — Mettre en place une politique de mobilité alternative des agents et des élu.e.s

- **Run 1 :** Covoiturage [5] | Efficacité et carburants décarbonés des véhicules privés [5] | Réduction des déplacements [5] | Véhicules électriques [5] | Vélo et transport en commun [5]
- **Run 2 :** Covoiturage [5] | Réduction des déplacements [5] | Véhicules électriques [5] | Vélo et transport en commun [5]
- **Run 3 :** Covoiturage [5] | Réduction des déplacements [5] | Véhicules électriques [5] | Vélo et transport en commun [5]
- **Prod :** (aucun levier)
- Leviers intermittents : Efficacité et carburants décarbonés des véhicules privés (1/3)

> Mettre en place une politique de mobilité alternative des agents et des élu.e.s, visant le changement de comportement, en adoptant une approche diversifiée pour couvrir tant les déplacements professionnels que ceux domicile-travail. Cette politique devrait inclure l'optimisation et le renouvellement de la flotte de véhicules, une gestion optimisée des déplacements, le développement de l'usage du vélo, des campagnes de communication et de sensibilisation, ainsi que la promotion des transports co…

#### Fiche 42051 — Sensibiliser aux enjeux des mobilités alternatives à la voiture individuelle

- **Run 1 :** Covoiturage [6] | Réduction des déplacements [6] | Vélo et transport en commun [6]
- **Run 2 :** Covoiturage [6] | Réduction des déplacements [6] | Vélo et transport en commun [6]
- **Run 3 :** Covoiturage [6] | Vélo et transport en commun [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Réduction des déplacements (2/3)

> Sensibiliser aux enjeux des mobilités alternatives à la voiture individuelle/autosolisme, en prenant en compte les publics précaires. \n- Recenser les actions déjà menées en faveur des mobilités alternatives à la voiture individuelle/autosolisme - Valoriser ces actions - Définir les publics ciblés par les démarches de sensibilisation - Initier et/ou poursuivre les actions de sensibilisation, information et communication en identifiant les formats adaptés en fonction des publics ciblés (exemples…

#### Fiche 42053 — Réaliser des achats durables via la commande publique

- **Run 1 :** Prévention des déchets [5] | Valorisation matière des déchets [5]
- **Run 2 :** Prévention des déchets [5] | Valorisation matière des déchets [5]
- **Run 3 :** Efficacité et sobriété logistique [5] | Prévention des déchets [5] | Valorisation matière des déchets [5]
- **Prod :** (aucun levier)
- Leviers intermittents : Efficacité et sobriété logistique (1/3)

> Mobiliser la commande publique pour réaliser des achats durables sur l'ensemble des produits, bien et services gérés par la collectivité. Contenu à aborder : favoriser les achats de proximité / réduire les déchets d'emballage via la commande publique / Inclure le critère de consommation énergétique dans les choix de matériels informatiques / stopper les achats non équitables ou non éthiques, intégrer dans les marchés publics des critères d'efficacité énergétique, de réduction de l'impact enviro…

#### Fiche 42054 — Sensibiliser le grand public aux enjeux de la transition écologique 

- **Run 1 :** Prévention des déchets [6] | Réduction des déplacements [6]
- **Run 2 :** Prévention des déchets [6] | Réduction des déplacements [6] | Sobriété des bâtiments (résidentiel) [6]
- **Run 3 :** Prévention des déchets [6] | Réduction des déplacements [6] | Sobriété des bâtiments (résidentiel) [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété des bâtiments (résidentiel) (2/3)

> Sensibiliser le grand public au enjeux de la transition écologique en abordant plusieurs thématiques (modes déplacements, choix de consommation, déchets, habitation, etc.) \n- Initier et/ou poursuivre les actions de sensibilisation, information et communication en identifiant les formats adaptés en fonction des différents publics (jeunes, actifs, personnes âgées, etc.) - Créer des supports d'information et de communication - Mettre en œuvre des animations régulières - Mettre en place d'un budge…

#### Fiche 53167 — Organiser un défi "Pelouses fleuries" - retarder la première tonte

- **Run 1 :** Gestion des prairies [6] | Pratiques stockantes [6]
- **Run 2 :** Gestion des prairies [6]
- **Run 3 :** Pratiques stockantes [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Gestion des prairies (2/3), Pratiques stockantes (2/3)

#### Fiche 53168 — Organiser des opérations de broyage sur placettes

- **Run 1 :** Valorisation matière des déchets [1]
- **Run 2 :** Prévention des déchets [6]
- **Run 3 :** Valorisation matière des déchets [1]
- **Prod :** (aucun levier)
- Leviers intermittents : Prévention des déchets (1/3), Valorisation matière des déchets (2/3)

#### Fiche 53171 — Gérer les espaces verts intercommunaux en gestion différenciée

- **Run 1 :** Gestion des prairies [5] | Pratiques stockantes [5]
- **Run 2 :** Gestion des prairies [1]
- **Run 3 :** Pratiques stockantes [1]
- **Prod :** (aucun levier)
- Leviers intermittents : Gestion des prairies (2/3), Pratiques stockantes (2/3)

#### Fiche 53173 — Former les élus et agents communaux à la gestion différenciée des espaces verts

- **Run 1 :** Pratiques stockantes [5]
- **Run 2 :** Gestion des prairies [5]
- **Run 3 :** Pratiques stockantes [5]
- **Prod :** (aucun levier)
- Leviers intermittents : Gestion des prairies (1/3), Pratiques stockantes (2/3)

#### Fiche 61657 — Créer une liste des solutions locales et acteurs pour le réemploi, la réparation, la lutte contre les gaspillages, le jardinage au naturel

- **Run 1 :** Prévention des déchets [6] | Valorisation matière des déchets [6]
- **Run 2 :** Prévention des déchets [6] | Valorisation matière des déchets [6]
- **Run 3 :** Pratiques stockantes [6] | Prévention des déchets [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Pratiques stockantes (1/3), Valorisation matière des déchets (2/3)

#### Fiche 61679 — Organiser des sessions d'information et formation pour les maîtres d'ouvrages

- **Run 1 :** Prévention des déchets [6]
- **Run 2 :** Sobriété des bâtiments (résidentiel) [6] | Sobriété et isolation des bâtiments (tertiaire) [6]
- **Run 3 :** Prévention des déchets [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Prévention des déchets (2/3), Sobriété des bâtiments (résidentiel) (1/3), Sobriété et isolation des bâtiments (tertiaire) (1/3)

### Levier intermittent et catégories instables (1)

#### Fiche 42052 — Promouvoir et encourager les initiatives de réparation sur le territoire

- **Run 1 :** Prévention des déchets [1, 6] | Valorisation matière des déchets [1, 6]
- **Run 2 :** Prévention des déchets [1, 4, 6]
- **Run 3 :** Prévention des déchets [1, 4, 6]
- **Prod :** (aucun levier)
- Leviers intermittents : Valorisation matière des déchets (1/3)
- Catégories instables sur : Prévention des déchets

> Soutenir des initiatives de recyclerie ou de réparation de matériel en proposant des lieux à des associations ou à des acteurs de l’économie social et solidaire qui s’engagent sur cette pratique. Une animation du réseau peut venir amplifier la dynamique et créer une synergie entre les différents acteurs. \n- Identifier les acteurs de la réparation existants sur le territoire (association, acteurs de l'économie sociale et solidaire, etc.). Une carte interactive identifiant et localisant les acte…

### Mêmes leviers, catégories différentes (1)

#### Fiche 61654 — Lancer un appel à projets pour soutenir les démarches de prévention des déchets menées par les associations

- **Run 1 :** Prévention des déchets [3]
- **Run 2 :** Prévention des déchets [3, 4]
- **Run 3 :** Prévention des déchets [3, 4]
- **Prod :** (aucun levier)
- Catégories instables sur : Prévention des déchets

## CC du Pays de l'Arbresle (CCPA) (4994)

- Fiches : **96** — stables sur les 3 runs : **41** (43%), instables : **55**
- Paires levier × catégorie distinctes proposées : 185 — 3/3 runs : 59, 2/3 runs : 41, 1/3 runs : 85
- Vote majoritaire = prod : 16/65 fiches classées d'un côté ou de l'autre
- Réponses JSON invalides rejouées : 0
- Appels : 12 — tokens d'entrée 47 229 (dont 0 en cache, 0%), sortie 83 886 — coût estimé 0.21 $ pour les 3 runs
- Date : 2026-10-30 15:07

### Classée dans certains runs, aucun levier dans d'autres (16)

#### Fiche 61649 — 1.6 Intégrer dans le plan de formation de la collectivité des formations pour agents et élus sur les thématiques de l’économie circulaire (Exemplarité CCPA)

- **Run 1 :** Prévention des déchets [5] | Valorisation matière des déchets [5]
- **Run 2 :** (aucun levier)
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Prévention des déchets (1/3), Valorisation matière des déchets (1/3)

> Cette action vise à développer une culture commune de l’économie circulaire au sein de la collectivité en intégrant dans le plan de formation institutionnel des modules à destination : des agents techniques et administratifs (gestion des déchets, achats, urbanisme, mobilité, etc.) ; des élus, pour favoriser l’appropriation politique et la cohérence des décisions locales.

#### Fiche 61650 — 1.1 S’améliorer sur les achats durables – Élaboration et mise en œuvre du SPASER et integration dans un reseau d'acheteurs

- **Run 1 :** Prévention des déchets [5] | Valorisation matière des déchets [5]
- **Run 2 :** Prévention des déchets [5] | Valorisation matière des déchets [5]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Prévention des déchets (2/3), Valorisation matière des déchets (2/3)

> L’objectif de cette action est d’intégrer des critères environnementaux et sociaux dans la commande publique de la Communauté de Communes du Pays de l’Arbresle (CCPA), en s’appuyant sur la mise en œuvre d’un SPASER (Schéma de Promotion des Achats Publics Socialement et Écologiquement Responsables). Cette démarche vise à faire des achats un levier stratégique pour l’économie circulaire.

#### Fiche 61651 — 1.2 Sensibilisation Interne : Faire ou poursuivre une campagne de communication sur les éco-gestes et accompagner les changements de pratiques auprès des agents

- **Run 1 :** Prévention des déchets [5]
- **Run 2 :** (aucun levier)
- **Run 3 :** (aucun levier)
- **Prod :** Sobriété et isolation des bâtiments (tertiaire) [5]
- Leviers intermittents : Prévention des déchets (1/3)

> Cette action vise à sensibiliser et mobiliser les agents de la collectivité autour des éco-gestes, dans une logique d’exemplarité et de changement de comportement au quotidien. Elle permet de renforcer l’ancrage de la démarche économie circulaire en interne.

#### Fiche 61664 — 2.4 Acculturer sensibiliser et inspirer les entreprises lors d’événements organisés par la collectivité ou animés par le club d'entreprises, pour les sensibiliser à l’économie circulaire et encourager le réseautage via leur convention

- **Run 1 :** Prévention des déchets [6] | Valorisation matière des déchets [6]
- **Run 2 :** (aucun levier)
- **Run 3 :** (aucun levier)
- **Prod :** Prévention des déchets [6]
- Leviers intermittents : Prévention des déchets (1/3), Valorisation matière des déchets (1/3)

> <p class="!text-sm !text-primary-9 font-[Marianne]">Cette action vise à faire de l’économie circulaire un axe structurant des relations entre la collectivité et les structures représentatives du monde économique (associations d’entreprises, clubs, CCI, CMA, pôles territoriaux de coopération économique, etc.).<br><br>Dans le cadre du renouvellement ou de la mise à jour des conventions de partenariat, la collectivité proposera d’y intégrer des engagements concrets en matière de :<br><br>Sensibili…

#### Fiche 61669 — 2.2 Développer et animer la plateforme locale Mon Pays de L’Arbresle.fr

- **Run 1 :** Prévention des déchets [6] | Réduction des déplacements [6]
- **Run 2 :** Prévention des déchets [6] | Réduction des déplacements [6]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Prévention des déchets (2/3), Réduction des déplacements (2/3)

> <p class="!text-sm !text-primary-9 font-[Marianne]">La plateforme Mon Pays de L’<a target="_blank" rel="noopener noreferrer nofollow" href="http://Arbresle.fr">Arbresle.fr</a> a été créée en 2022 afin de :</p><ul><li><p class="!text-sm !text-primary-9 font-[Marianne]">Offrir une meilleure connaissance des acteurs économiques et associatifs du Pays de L’Arbresle</p></li><li><p class="!text-sm !text-primary-9 font-[Marianne]">Valoriser la dynamique locale afin que les habitants aient prioritairem…

#### Fiche 62264 — Programme de rencontres pour les entreprises en lien avec leurs démarches RSE

- **Run 1 :** Prévention des déchets [6] | Réduction des déplacements [6] | Sobriété et isolation des bâtiments (tertiaire) [6]
- **Run 2 :** Changement de chaudière à fioul (tertiaire) [6] | Changement de chaudière à gaz (tertiaire) [6] | Réduction des déplacements [6] | Sobriété et isolation des bâtiments (tertiaire) [6]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Changement de chaudière à fioul (tertiaire) (1/3), Changement de chaudière à gaz (tertiaire) (1/3), Prévention des déchets (1/3), Réduction des déplacements (2/3), Sobriété et isolation des bâtiments (tertiaire) (2/3)

> <p class="!text-base !text-grey-8 font-[Marianne]">Energie : travail de sensibilisation de l'ALTE et liens avec CCI et CMA (renovation) + AURA entreprises pour aide à la recherche de financement pour les industriels</p><p class="!text-base !text-grey-8 font-[Marianne]">&gt; Sensibiliser les entreprises à la rénovation et aux éco-gestes lors de rencontres des clubs d'entreprises <br>&gt; Rappeler l'intérêt des CEE et de leur valorisation<br>&gt; Informations sur le decret tertiaire</p><p>&nbsp;<…

#### Fiche 62265 — Animations pour les scolaires

- **Run 1 :** Prévention des déchets [6] | Réduction des déplacements [6] | Vélo et transport en commun [6]
- **Run 2 :** Prévention des déchets [6] | Vélo et transport en commun [6]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Prévention des déchets (2/3), Réduction des déplacements (1/3), Vélo et transport en commun (2/3)

> <p class="!text-base !text-grey-8 font-[Marianne]">Proposer des animations scolaires dans un catalogue d'animations plus complet : </p><ul><li><p class="!text-base !text-grey-8 font-[Marianne]">Pour la Biodiversité, il est proposé une animation en classe ou école du dehors" sur les sites naturels remarquables proches des écoles ou sur un ENS du territoire pour découvrir les thèmes suivants : les oiseaux, les insectes, les prairies et les haies, les forêts et les zones humides.</p></li><li><p cl…

#### Fiche 62269 — Divers supports de com, refonte du site internet, articles réguliers sur les sujets de sensibilisation

- **Run 1 :** Réduction des déplacements [6] | Vélo et transport en commun [6]
- **Run 2 :** Réduction des déplacements [6]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Réduction des déplacements (2/3), Vélo et transport en commun (1/3)

> <p class="!text-sm !text-primary-9 font-[Marianne]">Articles réguliers sur la transition écologique sur les différents supports de communaication Magazine de la CCPA, reseaux sociaux<br>Mobilité : Valorisation des usagers utilisa, réalisation d'un guide mobilité à destination des habitants et des usagers du territoire<br><br>Éléments de calendrier : 2025-2027</p>

#### Fiche 62282 — Développer la mobilité solidaire

- **Run 1 :** Vélo et transport en commun [1]
- **Run 2 :** (aucun levier)
- **Run 3 :** Vélo et transport en commun [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Vélo et transport en commun (2/3)

> Continuité du service AMI destiné à faciliter les déplacements des personnes en situation de précarité. Travailler l'évolution du service en lien avec les nouveaux services mis en place progressivement par les communes. Coordination des actions avec les acteurs locaux accompagnant les publics en situation de précarité et le service solidarité de la CCPA. Tarification solidaire dans les services de mobilité. Éléments de calendrier : 2025-2027

#### Fiche 62300 — Suivre le patrimoine de la CCPA et les consommations énergétiques et envisager un suivi des émissions GES

- **Run 1 :** (aucun levier)
- **Run 2 :** Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 3 :** Sobriété et isolation des bâtiments (tertiaire) [5]
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété et isolation des bâtiments (tertiaire) (2/3)

> 1/EF diagnostique l'ensemble des bâtiments de la CCPA qui ne l'ont pas été et émet des recommandations 2/EF met en place une procédure pour le suivi des consommations et émissions de GES 3/EF met en place un outil de suivi (logiciel)

#### Fiche 62310 — Solliciter la filière bois énergie locale

- **Run 1 :** (aucun levier)
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6] | Changement de chaudière à fioul (tertiaire) [5] | Changement de chaudière à gaz (tertiaire) [5] | Gestion des forêts et produits bois [5, 6]
- **Run 3 :** Gestion des forêts et produits bois [4, 6]
- **Prod :** (aucun levier)
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (1/3), Changement chaudières gaz + rénovation (résidentiel) (1/3), Changement de chaudière à fioul (tertiaire) (1/3), Changement de chaudière à gaz (tertiaire) (1/3), Gestion des forêts et produits bois (2/3)

> Favoriser l'exemplarité de la collectivité > identifier les besoins de conversion des appareils de chauffage des bâtiments public Encourager l'approvisionnement en bois local pour les particuliers et les communes > recenser et identifier dans un document unique les fournisseurs de bois local sur le territoire > diffuser le document dans les communications communales via l'ALTE > sensibiliser dans le même temps sur l'importance d'achat de bois suffisamment sec (pour le bois bûche) > encourager l…

#### Fiche 62341 — Poursuite du suivi des ENS  pour la préservation de la biodiversité, suivi des plans de gestion

- **Run 1 :** (aucun levier)
- **Run 2 :** Gestion des forêts et produits bois [4] | Pratiques stockantes [4]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Gestion des forêts et produits bois (1/3), Pratiques stockantes (1/3)

> <p class="!text-sm !text-primary-9 font-[Marianne]">Rédaction de 3 plans de gestion des ENS en cours:</p><ul><li><p class="!text-sm !text-primary-9 font-[Marianne]">ENS des Crêts Boisés de l'Ouest Lyonnais: création du premier plan de gestion et révision du plan de gestion vec La tourbière du Chatelard qui est gérée à part avec le concours du CEN pour la préserver</p></li><li><p class="!text-sm !text-primary-9 font-[Marianne]">ENS des Carrières de Glay et du Bois des Oncins, révision en lien av…

#### Fiche 62355 — Réflechir à la réutilisation de l'eau de la piscine

- **Run 1 :** (aucun levier)
- **Run 2 :** Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété et isolation des bâtiments (tertiaire) (1/3)

> <p class="!text-sm !text-primary-9 font-[Marianne]">Réflexion sur la mise en place d'un système de récupérateur d'eau et de calories</p>

#### Fiche 62356 — Lancer une reflexion sur une prime pour les rénovations énergétiques des particuliers  performantes en particulier pour l'utilisation de matériaux bio-sourcés

- **Run 1 :** (aucun levier)
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [3] | Changement chaudières gaz + rénovation (résidentiel) [3] | Gestion des forêts et produits bois [3] | Sobriété des bâtiments (résidentiel) [3]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [3] | Changement chaudières gaz + rénovation (résidentiel) [3] | Sobriété des bâtiments (résidentiel) [3]
- **Prod :** (aucun levier)
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (2/3), Changement chaudières gaz + rénovation (résidentiel) (2/3), Gestion des forêts et produits bois (1/3), Sobriété des bâtiments (résidentiel) (2/3)

#### Fiche 88771 — 1.7 Nommer un élu à l'économie circulaire et assurer un portage politique

- **Run 1 :** (aucun levier)
- **Run 2 :** Prévention des déchets [4] | Valorisation matière des déchets [4]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Prévention des déchets (1/3), Valorisation matière des déchets (1/3)

#### Fiche 90936 — 1.8 Suivre, évaluer, améliorer le déploiement de la politique Economie Circulaire

- **Run 1 :** (aucun levier)
- **Run 2 :** Prévention des déchets [4] | Valorisation matière des déchets [4]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Prévention des déchets (1/3), Valorisation matière des déchets (1/3)

### Levier présent dans certains runs seulement (18)

#### Fiche 61655 — 1.4 Poursuivre le plan de sobriété dans la collectivité

- **Run 1 :** Prévention des déchets [5] | Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 2 :** Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 3 :** Réduction des déplacements [5] | Sobriété et isolation des bâtiments (tertiaire) [5]
- **Prod :** (aucun levier)
- Leviers intermittents : Prévention des déchets (1/3), Réduction des déplacements (1/3)

> Cette action vise à maintenir et renforcer la dynamique de sobriété initiée au sein de la collectivité, à travers un plan structuré d’optimisation des consommations de ressources (énergie, eau, papier, carburant, matériel informatique...) et d’évolution des pratiques professionnelles.

#### Fiche 62262 — Sensibilisation et accompagnement au changement en interne

- **Run 1 :** Réduction des déplacements [5] | Sobriété et isolation des bâtiments (tertiaire) [5] | Vélo et transport en commun [5]
- **Run 2 :** Réduction des déplacements [5] | Sobriété et isolation des bâtiments (tertiaire) [5] | Véhicules électriques [5]
- **Run 3 :** Réduction des déplacements [5] | Vélo et transport en commun [5]
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété et isolation des bâtiments (tertiaire) (2/3), Véhicules électriques (1/3), Vélo et transport en commun (2/3)

> <p class="!text-base !text-grey-8 font-[Marianne]">Envisager la mise en place d'une sensibilisation interne à la collectivité avec le personnel et les élus lors du prochain mandat.organisation régulière d'ateliers sur les thèmes suivants : changement climatique, économies d'énergie dans les bâtiments (rénovation, éco-gestes, rafraichissement), aménagement et adaptation, ressource en eau (qualité, quantité et inondations) qualité de l'air<br>Mobilité : sensibilisation des agents en participant a…

#### Fiche 62278 — Véhicules intermédiaires

- **Run 1 :** Réduction des déplacements [1]
- **Run 2 :** Réduction des déplacements [1]
- **Run 3 :** Véhicules électriques [1]
- **Prod :** Vélo et transport en commun [1]
- Leviers intermittents : Réduction des déplacements (2/3), Véhicules électriques (1/3)

> Développer l'usage des véhicules intermédiaires pour réduire l'utilisation de la voiture individuelle sur le territoire en expérimentant des services de mise à disposition aux habitants. Éléments de calendrier : 2025-2027

#### Fiche 62280 — Plan piéton

- **Run 1 :** Vélo et transport en commun [2]
- **Run 2 :** Réduction des déplacements [2]
- **Run 3 :** Vélo et transport en commun [2]
- **Prod :** Vélo et transport en commun [2]
- Leviers intermittents : Réduction des déplacements (1/3), Vélo et transport en commun (2/3)

> Réaliser un plan piéton à l'échelle du Pays de l'Arbresle (prévu dans le PDM des territoires lyonnais) Éléments de calendrier : 2025-2027

#### Fiche 62284 — Mise en place de Lignes de Cars à Haut Niveau de Service

- **Run 1 :** Bus et cars décarbonés [1]
- **Run 2 :** Vélo et transport en commun [1, 4]
- **Run 3 :** Bus et cars décarbonés [1]
- **Prod :** Vélo et transport en commun [1]
- Leviers intermittents : Bus et cars décarbonés (2/3), Vélo et transport en commun (1/3)

> Mise en place de deux lignes de bus express avec Sytral Mobilité. Ligne 142 express et ligne 118 express afin de renforcer la desserte des zones d'emplois en périphéries de Lyon, et l'accès direct au centre de Lyon. Éléments de calendrier : 2025-2027

#### Fiche 62285 — Développement et renforcement des lignes de bus régulières

- **Run 1 :** Bus et cars décarbonés [1]
- **Run 2 :** Vélo et transport en commun [1, 4]
- **Run 3 :** Bus et cars décarbonés [1]
- **Prod :** Vélo et transport en commun [1]
- Leviers intermittents : Bus et cars décarbonés (2/3), Vélo et transport en commun (1/3)

> Continuer le déploiement des lignes régulières pour désenclaver les territoires moins denses et renforcer la desserte des lignes existantes. Avec Sytral Mobilités. Suivi régulier de la fréquentation des lignes. Éléments de calendrier : 2025-2027

#### Fiche 62286 — Ouverture d'un service de Transport à la Demande

- **Run 1 :** Bus et cars décarbonés [1]
- **Run 2 :** Vélo et transport en commun [1]
- **Run 3 :** Bus et cars décarbonés [1]
- **Prod :** Vélo et transport en commun [1]
- Leviers intermittents : Bus et cars décarbonés (2/3), Vélo et transport en commun (1/3)

> Mettre en place un service de Transport à la Demande dans les communes non desservies par les transports en commun : Bibost, Saint-Julien-sur-Bibost et Courzieu Éléments de calendrier : 2025-2027

#### Fiche 62289 — Accompagner le développement des Pédibus / Vélobus / Trottibus

- **Run 1 :** Vélo et transport en commun [6]
- **Run 2 :** Réduction des déplacements [6]
- **Run 3 :** Vélo et transport en commun [6]
- **Prod :** Vélo et transport en commun [6]
- Leviers intermittents : Réduction des déplacements (1/3), Vélo et transport en commun (2/3)

> Conseiller et acocmpagner les communes et/ou acteurs qui souhaitent mettre en place des groupes d'élèves allant à l'école à pied, à vélo ou en trottinette. Continuer les réflexions permettant de renforcer la sécurité des déplacements des élèves vers l'école. Éléments de calendrier : 2025-2027

#### Fiche 62290 — Expérimenter des alternatives au transport scolaire motorisé

- **Run 1 :** Vélo et transport en commun [6]
- **Run 2 :** Réduction des déplacements [6]
- **Run 3 :** Vélo et transport en commun [6]
- **Prod :** Vélo et transport en commun [1, 6]
- Leviers intermittents : Réduction des déplacements (1/3), Vélo et transport en commun (2/3)

> Expérimenter le bus vélo ou l'hippo mobilité pour les déplacements domicile-école. Mettre en place le Savoir Rouler à Vélo dans les écoles. Éléments de calendrier : 2025-2027

#### Fiche 62294 — Programme d’intérêt Général (CCPA hors communes de L’Arbresle et Sain Bel) 2023-2028

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [3, 6] | Changement chaudières gaz + rénovation (résidentiel) [3, 6] | Sobriété des bâtiments (résidentiel) [3, 6]
- **Run 2 :** Sobriété des bâtiments (résidentiel) [3, 6]
- **Run 3 :** Sobriété des bâtiments (résidentiel) [3, 6]
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [3, 6]
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (1/3), Changement chaudières gaz + rénovation (résidentiel) (1/3)

> <p class="!text-base !text-grey-8 font-[Marianne]">&nbsp;</p><p class="!text-base !text-grey-8 font-[Marianne]">Dispositif visant à accompagner les ménages à revenus modestes ou très modestes et les propriétaires bailleurs privés éligibles aux aides de l'Anah dans leur projet de rénovation de l'habitat (rénovation énergétique, adaptation à l'âge, habitat indigne) - L'accompagnement technique et administratif est assuré par l'association SOLIHA (prestation d'accompagnement prise en charge par la…

#### Fiche 62295 — Opération Programmée d’Amélioration de l’Habitat Renouvellement Urbain de L’Arbresle et Sain Bel  2023-2028

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [3, 6] | Changement chaudières gaz + rénovation (résidentiel) [3, 6] | Sobriété des bâtiments (résidentiel) [3, 6]
- **Run 2 :** Sobriété des bâtiments (résidentiel) [3, 6]
- **Run 3 :** Sobriété des bâtiments (résidentiel) [3, 6]
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [3, 6]
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (1/3), Changement chaudières gaz + rénovation (résidentiel) (1/3)

> <p class="!text-base !text-grey-8 font-[Marianne]">Dispositif visant à accompagner les ménages à revenus modestes ou très modestes et les propriétaires bailleurs privés éligibles aux aides de l'Anah dans leur projet de rénovation de l'habitat (rénovation énergétique, adaptation à l'âge, habitat indigne) - L'accompagnement technique et administratif est assuré par l'association SOLIHA (prestation d'accompagnement prise en charge par la CCPA via marché public) - Attribution de subventions CCPA en…

#### Fiche 62296 — Mise en œuvre du Service Public de la Rénovation de l’Habitat (habitat privé) - Pacte Territorial du Pays de L'Arbresle

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6] | Sobriété des bâtiments (résidentiel) [6]
- **Run 2 :** Sobriété des bâtiments (résidentiel) [6]
- **Run 3 :** Sobriété des bâtiments (résidentiel) [6]
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [6]
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (1/3), Changement chaudières gaz + rénovation (résidentiel) (1/3)

> <p class="!text-base !text-grey-8 font-[Marianne]">Information/sensibilisation des acteurs de la rénovation de l'habitat privé et des ménages pour tous projets (rénovation énergétique, maintien à domicile, lutte contre l'habitat indigne/dégradé) - Professionnels et particuliers </p> Éléments de calendrier : 2025-2027

#### Fiche 62298 — Visite énergie CCI et CMA

- **Run 1 :** Changement de chaudière à fioul (tertiaire) [6] | Changement de chaudière à gaz (tertiaire) [6] | Sobriété et isolation des bâtiments (tertiaire) [6]
- **Run 2 :** Sobriété et isolation des bâtiments (tertiaire) [6]
- **Run 3 :** Sobriété et isolation des bâtiments (tertiaire) [6]
- **Prod :** Sobriété et isolation des bâtiments (tertiaire) [6]
- Leviers intermittents : Changement de chaudière à fioul (tertiaire) (1/3), Changement de chaudière à gaz (tertiaire) (1/3)

> > Diffuser aux entreprises du territoire une communication sur les accompagnements de la CMA et de la CCI (diagnostics et accompagnements de type "Visite énergie", etc.)

#### Fiche 62303 — Accompagner techniquement les communes de la CCPA pour la rénovation de leur parc

- **Run 1 :** Changement de chaudière à fioul (tertiaire) [6] | Changement de chaudière à gaz (tertiaire) [6] | Sobriété et isolation des bâtiments (tertiaire) [6]
- **Run 2 :** Sobriété et isolation des bâtiments (tertiaire) [6]
- **Run 3 :** Sobriété et isolation des bâtiments (tertiaire) [6]
- **Prod :** Sobriété et isolation des bâtiments (tertiaire) [6]
- Leviers intermittents : Changement de chaudière à fioul (tertiaire) (1/3), Changement de chaudière à gaz (tertiaire) (1/3)

> l'économe de flux conseille et accompagne les communes dans leurs projets de rénovation en lien avec l'ALTE.

#### Fiche 62304 — Soutenir financièrement les rénovations énergétiques ambitieuses des bâtiments communaux

- **Run 1 :** Changement de chaudière à fioul (tertiaire) [3] | Changement de chaudière à gaz (tertiaire) [3] | Sobriété et isolation des bâtiments (tertiaire) [3]
- **Run 2 :** Sobriété et isolation des bâtiments (tertiaire) [3]
- **Run 3 :** Sobriété et isolation des bâtiments (tertiaire) [3]
- **Prod :** Sobriété et isolation des bâtiments (tertiaire) [5]
- Leviers intermittents : Changement de chaudière à fioul (tertiaire) (1/3), Changement de chaudière à gaz (tertiaire) (1/3)

> Poursuite du fonds de concours rénovation énergétique des bâtiments communaux finançant jusqu'à 80 000€ les rénovations énergétiques exemplaires des bâtiments communaux Éléments de calendrier : jusqu'à la fin du mandat

#### Fiche 62325 — Développer le réemploi et la réparation :

- **Run 1 :** Valorisation matière des déchets [3, 6]
- **Run 2 :** Prévention des déchets [6] | Valorisation matière des déchets [4, 6]
- **Run 3 :** Prévention des déchets [3, 6]
- **Prod :** Prévention des déchets [3, 6]
- Leviers intermittents : Prévention des déchets (2/3), Valorisation matière des déchets (2/3)

> Accompagner et soutenir la ressourcerie le repair café et d'autres projets de réemploi type matheriauthèque) notemment pour leur recherche de nouveau lieu Éléments de calendrier : 2026 puis nouveau PLPDMA

#### Fiche 62333 — Valorisation des boues d'épuration

- **Run 1 :** Changements de pratiques de fertilisation azotée [4]
- **Run 2 :** Valorisation matière des déchets [4]
- **Run 3 :** Valorisation matière des déchets [4]
- **Prod :** (aucun levier)
- Leviers intermittents : Changements de pratiques de fertilisation azotée (1/3), Valorisation matière des déchets (2/3)

> Poursuite du traitement des boues de station en partenariat avec les agriculteurs locaux : plan d'épandage annuel avec les agriculteurs partenaires

#### Fiche 62334 — Encourager une gestion partagée et durable de la ressource forêt/bois

- **Run 1 :** Gestion des forêts et produits bois [1, 4, 6] | Pratiques stockantes [1, 4, 6]
- **Run 2 :** Gestion des forêts et produits bois [1, 4, 6]
- **Run 3 :** Gestion des forêts et produits bois [1, 4, 6]
- **Prod :** Gestion des forêts et produits bois [1, 4, 6]
- Leviers intermittents : Pratiques stockantes (1/3)

> Sensibiliser, former et informer les propriétaires forestiers et les élus > communiquer sur les enjeux de la gestion des parcelles forestières et la multifonctionnalité de la forêt (biodiversité, rôle social…) > communiquer sur les outils et accompagnements existants, notamment l'accompagnement technique du CRPF Mettre en place les conditions favorables à une gestion de la forêt > améliorer la desserte forestière (voiries d’accès, plateforme de dépôt…) en s'appuyant sur le schéma de desserte > …

### Levier intermittent et catégories instables (2)

#### Fiche 62305 — Mettre en place un dispositif de valorisation et massification des CEE sur le territoire

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [3] | Changement chaudières gaz + rénovation (résidentiel) [3] | Changement de chaudière à fioul (tertiaire) [3] | Changement de chaudière à gaz (tertiaire) [3] | Sobriété des bâtiments (résidentiel) [3] | Sobriété et isolation des bâtiments (tertiaire) [3]
- **Run 2 :** Sobriété des bâtiments (résidentiel) [3, 4] | Sobriété et isolation des bâtiments (tertiaire) [3, 4]
- **Run 3 :** Sobriété des bâtiments (résidentiel) [3] | Sobriété et isolation des bâtiments (tertiaire) [3]
- **Prod :** (aucun levier)
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (1/3), Changement chaudières gaz + rénovation (résidentiel) (1/3), Changement de chaudière à fioul (tertiaire) (1/3), Changement de chaudière à gaz (tertiaire) (1/3)
- Catégories instables sur : Sobriété des bâtiments (résidentiel), Sobriété et isolation des bâtiments (tertiaire)

> <p class="!text-sm !text-primary-9 font-[Marianne]">Poursuivre l'optimisation la massification et la valorisation des CEE via un courtier à l'échelle dule SOL<br><br>Éléments de calendrier : 2024 jusqu'à la fin du mandat</p>

#### Fiche 91446 — 1.9  Réemployer la flotte de VAE récupérée de Vel’Ouest

- **Run 1 :** Prévention des déchets [5]
- **Run 2 :** Prévention des déchets [5] | Vélo et transport en commun [5]
- **Run 3 :** Prévention des déchets [1] | Vélo et transport en commun [1]
- **Prod :** (aucun levier)
- Leviers intermittents : Vélo et transport en commun (2/3)
- Catégories instables sur : Prévention des déchets

> <p class="!text-base !text-grey-8 font-[Marianne]">Description de l'action :</p><p class="!text-base !text-grey-8 font-[Marianne]">Cette action vise à donner une seconde vie à une flotte de Vélos à Assistance Électrique (VAE) issue du service Vel’Ouest, en cohérence avec les objectifs d’allongement de la durée d’usage des équipements, de sobriété matérielle, et de mobilité durable.</p>

### Mêmes leviers, catégories différentes (19)

#### Fiche 61661 — 1.3 Rédiger une charte « Événements responsables » à destination des associations et l’appliquer à tous les événements organisés et soutenus par la collectivité

- **Run 1 :** Prévention des déchets [5, 6] | Réduction des déplacements [5, 6]
- **Run 2 :** Prévention des déchets [4, 5, 6] | Réduction des déplacements [4, 5, 6]
- **Run 3 :** Prévention des déchets [6] | Réduction des déplacements [6]
- **Prod :** (aucun levier)
- Catégories instables sur : Prévention des déchets, Réduction des déplacements

> <p class="!text-sm !text-primary-9 font-[Marianne]">Cette action vise à proposer aux associations du territoire un document reprenant tous les axes de la transition pour que les évenements soutenus par la CCPA aient une même charte / réduction des déchets, consommation d'énergie, mobilité durable.</p><p class="!text-sm !text-primary-9 font-[Marianne]">Cela vise également à formaliser les engagements de la collectivité en matière d’organisation d’événements écoresponsables, en l'applicant à tous…

#### Fiche 62270 — Développer la pratique du covoiturage sur le territoire

- **Run 1 :** Covoiturage [1]
- **Run 2 :** Covoiturage [4]
- **Run 3 :** Covoiturage [1]
- **Prod :** (aucun levier)
- Catégories instables sur : Covoiturage

> Etudier la faisabilité technique et financière de création de deux lignes de covoiturage à haut ou moyen niveau de service dans la vallée de la Brévenne et la vallée de la Turdine. Éléments de calendrier : 2025-2027

#### Fiche 62274 — Schéma directeur vélo

- **Run 1 :** Vélo et transport en commun [2]
- **Run 2 :** Vélo et transport en commun [2]
- **Run 3 :** Vélo et transport en commun [1, 2]
- **Prod :** Vélo et transport en commun [2]
- Catégories instables sur : Vélo et transport en commun

> Poursuivre la mise en œuvre du schéma vélo et réaliser une évaluation à mi-parcours en 2027 Éléments de calendrier : 2025-2027

#### Fiche 62279 — Travaux - Réalisation des voies cyclables

- **Run 1 :** Vélo et transport en commun [1, 3]
- **Run 2 :** Vélo et transport en commun [1, 3]
- **Run 3 :** Vélo et transport en commun [1]
- **Prod :** Vélo et transport en commun [1]
- Catégories instables sur : Vélo et transport en commun

> Réaliser les aménagements cyclables prévus au schéma vélo, continuer les études de faisabilité d'aménagements cyclables et d'apaisement de voirie. Continuer le fonds de concours mobilités actives de la CCPA versées aux communes pour les aménagements cyclables et piétons sur les voiries communales. Réaliser des travaux de sécurisation des points noirs et de résorption des coupures urbaines pour assurer la sécurité des usagers et la continuté des cheminements. Éléments de calendrier : 2025-2027

#### Fiche 62287 — Développement du train

- **Run 1 :** Vélo et transport en commun [1]
- **Run 2 :** Vélo et transport en commun [1, 4]
- **Run 3 :** Vélo et transport en commun [1, 4]
- **Prod :** Vélo et transport en commun [4]
- Catégories instables sur : Vélo et transport en commun

> Continuer le dialogue engagé pour l'exentesion du tram-train jusqu'à la Giraudière en passant par La Brévenne. Suivi du déploiement du SERM avec l'ensembe des acteurs concernés. Éléments de calendrier : 2025-2027

#### Fiche 62307 — Accompagner et suivre les communes pour la définition de Zones d'accélération des ENR et leurs modifications éventuelles

- **Run 1 :** Electricité renouvelable [6]
- **Run 2 :** Electricité renouvelable [2, 6]
- **Run 3 :** Electricité renouvelable [2, 6]
- **Prod :** Electricité renouvelable [2, 6]
- Catégories instables sur : Electricité renouvelable

> Poursuivre l'accompagnement par la CCPA des communes dans la déclaration de leurs ZAER en lien avec la DDT

#### Fiche 62308 — Acheter de l'electricité d'origine renouvelable pour la consommation de la CCPA

- **Run 1 :** Electricité renouvelable [5]
- **Run 2 :** Electricité renouvelable [3, 5]
- **Run 3 :** Electricité renouvelable [5]
- **Prod :** (aucun levier)
- Catégories instables sur : Electricité renouvelable

> envisager au niveau budgétaire l'incidence de ce choix proposé par le service patrimoine

#### Fiche 62309 — Développer les chaufferies collectives bois en lien avec le CCR

- **Run 1 :** Réseaux de chaleur décarbonés [1, 2, 6]
- **Run 2 :** Réseaux de chaleur décarbonés [1, 2]
- **Run 3 :** Réseaux de chaleur décarbonés [2, 6]
- **Prod :** Réseaux de chaleur décarbonés [1, 2, 6]
- Catégories instables sur : Réseaux de chaleur décarbonés

> Prévoir la mise en œuvre de chaufferies collectives dans les nouveaux aménagements > encourager, dans les OAP des documents d'urbanisme locaux, la réalisation d'une étude d'installation d'une chaufferie collective pour les projets d'aménagement d'ensemble > identifier les possibilités de création de réseaux de chaleur dans les projets d'aménagement > s'assurer que les performances des chaufferies bois sont alignées sur les plus faibles niveaux d'émissions pouvant être techniquement atteints Dév…

#### Fiche 62311 — Financement de panneaux plug & play pour les particuliers

- **Run 1 :** Electricité renouvelable [3, 6]
- **Run 2 :** Electricité renouvelable [6]
- **Run 3 :** Electricité renouvelable [6]
- **Prod :** Electricité renouvelable [3, 6]
- Catégories instables sur : Electricité renouvelable

> > relayer la communication sur le cadastre solaire en lien avec le SOL > communiquer sur le centre de ressources photovoltaïque et sur le conseil de l'ALTE pour les particuliers > organiser des évènements d'information et de sensibilisation (ateliers techniques, conférences sur les idées reçues concernant le photovoltaïque, etc)

#### Fiche 62312 — Encadrer l'agri-voltaisme

- **Run 1 :** Electricité renouvelable [4, 6]
- **Run 2 :** Electricité renouvelable [4, 6]
- **Run 3 :** Electricité renouvelable [4]
- **Prod :** (aucun levier)
- Catégories instables sur : Electricité renouvelable

> Poursuivre la formation des élus et techniciens sur le sujet afin d'aboutir sur un positionnement commun pour la CCPA et réfléchir à accompagner des éventuels projets expérimentaux

#### Fiche 62313 — Grappe de projets PV avec le SYDER

- **Run 1 :** Electricité renouvelable [5]
- **Run 2 :** Electricité renouvelable [3, 4, 5]
- **Run 3 :** Electricité renouvelable [5]
- **Prod :** Electricité renouvelable [3]
- Catégories instables sur : Electricité renouvelable

> suivre les installations sur les toitures des bâtiments publics sur les communes de la CCPA suite aux études strucures financées par la CCPA pour les bâtiments de la phase 2

#### Fiche 62314 — Solarisation du patrimoine CCPA et création d'une boucle d'autoconsommation collective

- **Run 1 :** Electricité renouvelable [5]
- **Run 2 :** Electricité renouvelable [4, 5]
- **Run 3 :** Electricité renouvelable [5]
- **Prod :** Electricité renouvelable [5]
- Catégories instables sur : Electricité renouvelable

> <p class="!text-sm !text-primary-9 font-[Marianne]">réaliser une étude de faisabilité pour étudier la possibilité d'une opérationautoconsommation avec les bâtiments de la CCPA et éventuellement des ombrières</p>

#### Fiche 62317 — Encourager l'autoconsommation collective sur les ZAE

- **Run 1 :** Electricité renouvelable [3, 6]
- **Run 2 :** Electricité renouvelable [2, 3, 4, 6]
- **Run 3 :** Electricité renouvelable [3, 6]
- **Prod :** Electricité renouvelable [3, 6]
- Catégories instables sur : Electricité renouvelable

> Encourager l'autoconsommation collective sur les zones d'activité : poursuivre le financement d'une étude d'oportunité et l' accompagnement des entreprises concernées par le projet expérimentale sur la ZAE des Garelles, étudier la possibilité d'une dérogation afin d'étendre la boucle à d'autres ZAE

#### Fiche 62318 — Methanisation : Rester en veille pour accompagner d'éventuels porteurs de projets

- **Run 1 :** Biogaz [6]
- **Run 2 :** Biogaz [4, 6]
- **Run 3 :** Biogaz [4, 6]
- **Prod :** (aucun levier)
- Catégories instables sur : Biogaz

> Mettre en place une communication autour des projets (si il y en ) pour en faciliter l'acceptation Suivre le développement à l'echelle départemental

#### Fiche 62319 — Valoriser la chaleur fatale : projet de reseau de chaleur sur Sain Bel, L'Abresle Savigny avec l'entreprise la SMAD

- **Run 1 :** Réseaux de chaleur décarbonés [4, 6]
- **Run 2 :** Réseaux de chaleur décarbonés [1, 4]
- **Run 3 :** Réseaux de chaleur décarbonés [1, 4]
- **Prod :** Réseaux de chaleur décarbonés [4]
- Catégories instables sur : Réseaux de chaleur décarbonés

> accompagnement du projet de récupération de chaleur fatale sur les communes de L'Arbresle, Sain Bel et Savigny en lien avec le SYDER

#### Fiche 62322 — Réduire les déchets verts, développer le compostage et sensibiliser à l'interdiction de brûlage

- **Run 1 :** Prévention des déchets [6] | Valorisation matière des déchets [6]
- **Run 2 :** Prévention des déchets [1, 6] | Valorisation matière des déchets [1, 6]
- **Run 3 :** Prévention des déchets [6] | Valorisation matière des déchets [1, 6]
- **Prod :** Valorisation matière des déchets [1, 6]
- Catégories instables sur : Prévention des déchets, Valorisation matière des déchets

> <p class="!text-base !text-grey-8 font-[Marianne]">Compostage : poursuivre le déploiement des solutions de tri à la source des biodéchets pour tous les publics (compostage domestique, collectif ou borne de collecte)<br>Déchets verts : proposer un dispositif de gestion des déchets verts aux usagers pour limiter l'apport en déchèterie et sensibiliser à l'interdiction de brûlage.</p> Éléments de calendrier : Déploiement solution biodéchets d'ici fin 2027 Solutions déchets verts : 2026

#### Fiche 62326 — 2.5 Impulser et soutenir les initiatives locales en ECI des acteurs du territoire

- **Run 1 :** Prévention des déchets [3, 6] | Valorisation matière des déchets [3, 6]
- **Run 2 :** Prévention des déchets [3, 6] | Valorisation matière des déchets [3, 4, 6]
- **Run 3 :** Prévention des déchets [3, 4, 6] | Valorisation matière des déchets [3, 4, 6]
- **Prod :** Prévention des déchets [3, 6]
- Catégories instables sur : Prévention des déchets, Valorisation matière des déchets

> <p class="!text-sm !text-primary-9 font-[Marianne]">soutenir les actuers locaux dans les dynamiques de création de projets en lien avec l'économie circulaire : matheriauthèque, remploi...</p><p class="!text-sm !text-primary-9 font-[Marianne]">Plus particulièremimpulser la consigne pour le réemploi du verre en lien avec Rebooteille, lien et soutien du projet de la ferme du Réemploi (pôle pluriactivité avec tiers lieu et mathériauthèque, formation, lieu de résidence pour artistes et artisants); p…

#### Fiche 62327 — Amplifier la collecte de déchets spécifiques

- **Run 1 :** Valorisation matière des déchets [4]
- **Run 2 :** Valorisation matière des déchets [1, 4]
- **Run 3 :** Valorisation matière des déchets [1, 4]
- **Prod :** Valorisation matière des déchets [1]
- Catégories instables sur : Valorisation matière des déchets

> Poursuivre l'organisation de la collecte annuelle de plastiques agricoles et d'amiante, collecte solidaire (souris d'ordinateurs, smart phone…); Éléments de calendrier : 2026 puis nouveau PLPDMA

#### Fiche 62336 — Travailler sur un cahier des charges pour encadrer les ZAE (pour les bâtiments neufs)

- **Run 1 :** Sobriété foncière [2]
- **Run 2 :** Sobriété foncière [2, 4]
- **Run 3 :** Sobriété foncière [2]
- **Prod :** (aucun levier)
- Catégories instables sur : Sobriété foncière

> Gestion de l'espace sur les zones d'activité de manière globale et durable : - proposition de travail sur une zone test à Fleurieux sur l'Arbresle - refonte du cahier des charges de cession sur les ZAE - accompagnement du CAUE sur les projets de construction en ZAE - mutualisation des espaces logistiques, espaces verts plus vastes - prescription environnementales - étude de faisabilité en 2025

## Métropole de Lyon (4999)

- Fiches : **81** — stables sur les 3 runs : **41** (51%), instables : **40**
- Paires levier × catégorie distinctes proposées : 241 — 3/3 runs : 82, 2/3 runs : 45, 1/3 runs : 114
- Vote majoritaire = prod : 12/47 fiches classées d'un côté ou de l'autre
- Réponses JSON invalides rejouées : 0
- Appels : 12 — tokens d'entrée 102 750 (dont 0 en cache, 0%), sortie 81 625 — coût estimé 0.24 $ pour les 3 runs
- Date : 2026-10-30 12:12

### Classée dans certains runs, aucun levier dans d'autres (10)

#### Fiche 65618 — Action n° 29 - Accompagner et outiller les acteurs culturels dans leur prise en compte des enjeux climatiques

- **Run 1 :** (aucun levier)
- **Run 2 :** (aucun levier)
- **Run 3 :** Réduction des déplacements [6] | Sobriété et isolation des bâtiments (tertiaire) [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Réduction des déplacements (1/3), Sobriété et isolation des bâtiments (tertiaire) (1/3)

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="b06cc4a7-76da-461e-860a-4b324f2dbcb8"><div class="bn-block" data-node-type="blockContainer" data-id="b06cc4a7-76da-461e-860a-4b324f2dbcb8"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]">Le secteur de la culture présente une empreinte carbone élevée, notamment du fait des émissions causées …

#### Fiche 65619 — Action n°30 - Restaurer le cycle naturel de l’eau et les milieux aquatiques

- **Run 1 :** (aucun levier)
- **Run 2 :** Pratiques stockantes [1, 2, 4]
- **Run 3 :** Pratiques stockantes [1, 2]
- **Prod :** (aucun levier)
- Leviers intermittents : Pratiques stockantes (2/3)

> <p>Territoire largement imperméabilisé et urbanisé, la Métropole de Lyon fait face à des événements météorologiques de plus en plus extrêmes :</p><ul><li><p>Les sécheresses, qui menacent la végétation et la biodiversité ;</p></li><li><p>Les pluies extrêmes, qui font courir des risques aux biens comme aux personnes ;</p></li><li><p>Les canicules qui affectent le vivant.</p></li></ul><p>&nbsp;</p><p>Pour faire face à ces défis, la Métropole s’est dotée de plusieurs politiques publiques qui conver…

#### Fiche 65621 — Action n°32 - Préserver et restaurer la biodiversité métropolitaine

- **Run 1 :** (aucun levier)
- **Run 2 :** Gestion des forêts et produits bois [1, 2] | Gestion des haies [1, 2] | Gestion des prairies [1, 2] | Pratiques stockantes [1, 2]
- **Run 3 :** Gestion des forêts et produits bois [1, 2] | Pratiques stockantes [1, 2]
- **Prod :** (aucun levier)
- Leviers intermittents : Gestion des forêts et produits bois (2/3), Gestion des haies (1/3), Gestion des prairies (1/3), Pratiques stockantes (2/3)

> <p class="!text-sm !text-primary-9 font-[Marianne]">De par sa localisation entre la confluence de la Saône et du Rhône, et sa position au carrefour des régions biogéographiques médio-européennes, atlantiques et méditerranéennes, la Métropole de Lyon accueille une grande diversité de milieux naturels et agricoles, qui représentent 30% du territoire. Cependant, l’élévation moyenne des températures, la modification du régime des pluies, la sécheresse des sols, les canicules mais aussi le développe…

#### Fiche 90526 — D9 - Conforter la prise en compte de la stratégie territoriale du PCAET dans les chantiers collectifs conduits au titre du Livre Blanc de l’Habitat

- **Run 1 :** (aucun levier)
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [2, 4] | Changement chaudières gaz + rénovation (résidentiel) [2, 4] | Sobriété des bâtiments (résidentiel) [2, 4]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [4] | Changement chaudières gaz + rénovation (résidentiel) [4] | Sobriété des bâtiments (résidentiel) [4]
- **Prod :** (aucun levier)
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (2/3), Changement chaudières gaz + rénovation (résidentiel) (2/3), Sobriété des bâtiments (résidentiel) (2/3)

#### Fiche 90531 — D13 - Préfigurer les adaptations des infrastructures de mobilité face au changement climatique (transports en commun, voies lyonnaises, magistrales piétonnes, etc.) 

- **Run 1 :** (aucun levier)
- **Run 2 :** Vélo et transport en commun [1]
- **Run 3 :** Vélo et transport en commun [1]
- **Prod :** (aucun levier)
- Leviers intermittents : Vélo et transport en commun (2/3)

#### Fiche 90535 — D17 - Privilégier et massifier l’achat d’intrants recyclés ou bio/géosourcés ou issus du réemploi ou moins carbonés par la création de filières de proximités (écoconception et R&D) et un approvisionnement responsable

- **Run 1 :** Production Industrielle [4, 6]
- **Run 2 :** (aucun levier)
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Production Industrielle (1/3)

#### Fiche 90539 — D22 - COP : Contribuer à mobiliser toutes les TPE, PME et ETI pour la décarbonation

- **Run 1 :** Production Industrielle [4, 6]
- **Run 2 :** (aucun levier)
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Production Industrielle (1/3)

#### Fiche 90546 — D29 - Travailler sur le long terme avec les concessionnaires de réseaux enterrés et aériens pour libérer des emprises plantables sur le domaine de voirie

- **Run 1 :** Pratiques stockantes [1, 4]
- **Run 2 :** Pratiques stockantes [1, 4]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Pratiques stockantes (2/3)

#### Fiche 90548 — D31 - Mieux connaître et partager avec les parties prenantes les données relatives à l’évolution des surfaces végétales, leur gestion, le choix des végétaux appropriés, la répartition des moyens associés 

- **Run 1 :** Pratiques stockantes [6]
- **Run 2 :** (aucun levier)
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Pratiques stockantes (1/3)

#### Fiche 90555 — D37 - Explorer des modalités d’accompagnement de modèles circulaires au regard de leur rentabilité

- **Run 1 :** (aucun levier)
- **Run 2 :** (aucun levier)
- **Run 3 :** Prévention des déchets [4, 6] | Valorisation matière des déchets [4, 6]
- **Prod :** (aucun levier)
- Leviers intermittents : Prévention des déchets (1/3), Valorisation matière des déchets (1/3)

### Levier présent dans certains runs seulement (3)

#### Fiche 65596 — Action n°7 - Lutter contre la précarité énergétique

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [3, 6] | Changement chaudières gaz + rénovation (résidentiel) [3, 6] | Sobriété des bâtiments (résidentiel) [3, 6]
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [3, 6] | Changement chaudières gaz + rénovation (résidentiel) [3, 6] | Réseaux de chaleur décarbonés [6] | Sobriété des bâtiments (résidentiel) [3, 6]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [3, 6] | Changement chaudières gaz + rénovation (résidentiel) [3, 6] | Réseaux de chaleur décarbonés [3, 6] | Sobriété des bâtiments (résidentiel) [3, 6]
- **Prod :** Sobriété des bâtiments (résidentiel) [6]
- Leviers intermittents : Réseaux de chaleur décarbonés (2/3)

> <p class="!text-sm !text-primary-9 font-[Marianne]">Selon la loi du 12 juillet 2010 relative à «&nbsp;l’engagement national pour l’environnement&nbsp;», une personne est considérée en situation de précarité énergétique lorsqu’elle «&nbsp; éprouve dans son logement des difficultés particulières à disposer de la fourniture d’énergie nécessaire à la satisfaction de ses besoins élémentaires en raison de l’inadaptation de ses ressources ou de ses conditions d’habitat ».</p><p>&nbsp;</p><p class="!te…

#### Fiche 65600 — Action n°11 - Développer des quartiers à énergie positive 

- **Run 1 :** Electricité renouvelable [1, 4] | Sobriété des bâtiments (résidentiel) [1] | Vélo et transport en commun [1]
- **Run 2 :** Electricité renouvelable [1, 4] | Sobriété des bâtiments (résidentiel) [1, 4] | Sobriété et isolation des bâtiments (tertiaire) [1, 4] | Vélo et transport en commun [1]
- **Run 3 :** Electricité renouvelable [1, 4] | Réduction des déplacements [1, 4] | Réseaux de chaleur décarbonés [1, 4]
- **Prod :** Electricité renouvelable [1] | Sobriété et isolation des bâtiments (tertiaire) [1]
- Leviers intermittents : Réduction des déplacements (1/3), Réseaux de chaleur décarbonés (1/3), Sobriété des bâtiments (résidentiel) (2/3), Sobriété et isolation des bâtiments (tertiaire) (1/3), Vélo et transport en commun (2/3)

> <p class="!text-sm !text-primary-9 font-[Marianne]">Le défi climatique et énergétique est tel que le développement urbain se doit d’évoluer et d’apporter des réponses adaptées aux contextes locaux. Le concept de Quartier à Énergie Positive est une solution innovante car elle permet de dépasser l’échelle du bâtiment individuel et de trouver un équilibre entre la production locale d'énergies renouvelables et la réduction des consommations énergétiques à l’échelle du quartier. Selon l’IPC Urban Eu…

#### Fiche 90553 — D35 - Échanger avec les acteurs économiques pour remobiliser les parcs tertiaires, notamment dans les zones obsolètes (pour mieux comprendre les freins et identifier les leviers pour recréer de la valeur)

- **Run 1 :** Sobriété foncière [4]
- **Run 2 :** Sobriété foncière [4]
- **Run 3 :** Sobriété et isolation des bâtiments (tertiaire) [4]
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété et isolation des bâtiments (tertiaire) (1/3), Sobriété foncière (2/3)

### Levier intermittent et catégories instables (11)

#### Fiche 65599 — Action n°10 - Décarboner les aménagements

- **Run 1 :** Réduction des déplacements [1, 2] | Sobriété des bâtiments (résidentiel) [1, 2] | Sobriété et isolation des bâtiments (tertiaire) [1, 2] | Sobriété foncière [1, 2]
- **Run 2 :** Gestion des forêts et produits bois [1, 2] | Sobriété foncière [1, 2, 4] | Vélo et transport en commun [1, 2]
- **Run 3 :** Réduction des déplacements [1] | Sobriété foncière [1, 2] | Valorisation matière des déchets [1, 5]
- **Prod :** (aucun levier)
- Leviers intermittents : Gestion des forêts et produits bois (1/3), Réduction des déplacements (2/3), Sobriété des bâtiments (résidentiel) (1/3), Sobriété et isolation des bâtiments (tertiaire) (1/3), Valorisation matière des déchets (1/3), Vélo et transport en commun (1/3)
- Catégories instables sur : Sobriété foncière

> <p class="!text-sm !text-primary-9 font-[Marianne]">La feuille de route nationale décarbonation de l’aménagement publiée en 2022 s’inscrit dans l’objectif de réduction de 55% des émissions brutes de gaz à effet de serre en 2030 et d’atteinte de la neutralité carbone de la France en 2050. Destinée à l’ensemble des acteurs de la chaîne de valeur de l’aménagement, elle permet de :</p><ul><li><p class="!text-sm !text-primary-9 font-[Marianne]">mettre en avant les moyens pour apprécier l’impact carb…

#### Fiche 65601 — Action n°12 - Créer les conditions de la mutabilité et de la réversibilité des bâtiments 

- **Run 1 :** Sobriété foncière [1, 2]
- **Run 2 :** Sobriété foncière [2, 4]
- **Run 3 :** Prévention des déchets [1] | Sobriété foncière [1, 2, 3]
- **Prod :** Sobriété foncière [2]
- Leviers intermittents : Prévention des déchets (1/3)
- Catégories instables sur : Sobriété foncière

> <p class="!text-sm !text-primary-9 font-[Marianne]">Au regard des enjeux auxquels est confronté le territoire (lutte contre le réchauffement climatique et préservation des ressources, notamment les sols, la biodiversité et l’eau), la Métropole vise désormais le zéro artificialisation net (ZAN). </p><p>&nbsp;</p><p class="!text-sm !text-primary-9 font-[Marianne]">Ainsi, dans un contexte de tension foncière et d’optimisation des espaces déjà bâtis, la Métropole œuvre pour être en capacité de cont…

#### Fiche 65603 — Action n°14 - Encourager et accélérer le report modal de la voiture particulière vers les transports en commun 

- **Run 1 :** Réduction des déplacements [1, 2] | Vélo et transport en commun [1, 2]
- **Run 2 :** Vélo et transport en commun [1, 2, 4]
- **Run 3 :** Vélo et transport en commun [1, 2]
- **Prod :** Vélo et transport en commun [1]
- Leviers intermittents : Réduction des déplacements (1/3)
- Catégories instables sur : Vélo et transport en commun

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="4de000fc-42c0-4fb6-9d33-e8b1819a1084"><div class="bn-block" data-node-type="blockContainer" data-id="4de000fc-42c0-4fb6-9d33-e8b1819a1084"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]">En 2021, 24% des émissions de gaz à effet de serre cadastrales sur la Métropole étaient dues au transpor…

#### Fiche 65608 — Action n°19 - Maintenir et développer une activité industrielle en la circularisant

- **Run 1 :** Production Industrielle [4, 6]
- **Run 2 :** Production Industrielle [2, 3, 4, 6]
- **Run 3 :** Production Industrielle [4, 6] | Prévention des déchets [4, 6] | Valorisation matière des déchets [4, 6]
- **Prod :** Production Industrielle [4, 6]
- Leviers intermittents : Prévention des déchets (1/3), Valorisation matière des déchets (1/3)
- Catégories instables sur : Production Industrielle

> <p class="!text-sm !text-primary-9 font-[Marianne]">L’industrie est prépondérante et fragile sur le territoire de la Métropole de Lyon :</p><ul><li><p class="!text-sm !text-primary-9 font-[Marianne]">Prépondérante car elle représente près de 80 500 emplois (13,4 % des emplois du territoire), 60 % de la richesse créée, et fournit certains produits nécessaires aux habitants du territoire,</p></li><li><p class="!text-sm !text-primary-9 font-[Marianne]">Fragile car elle est fortement dépendante d’i…

#### Fiche 65613 — Action n°24 - Structurer une stratégie territoriale de valorisation de la biomasse pour la production d’énergie

- **Run 1 :** Biogaz [4] | Gestion des forêts et produits bois [4]
- **Run 2 :** Biogaz [4] | Gestion des forêts et produits bois [4]
- **Run 3 :** Biogaz [1, 2] | Réseaux de chaleur décarbonés [1, 2]
- **Prod :** Biogaz [2] | Réseaux de chaleur décarbonés [2]
- Leviers intermittents : Gestion des forêts et produits bois (2/3), Réseaux de chaleur décarbonés (1/3)
- Catégories instables sur : Biogaz

> <p class="!text-sm !text-primary-9 font-[Marianne]">La biomasse représente un gisement important valorisable en énergies renouvelables. Cette valorisation peut se réaliser soit par combustion, soit par un processus de transformation de la ressource (méthanisation, pyrolyse, etc.) – pour produire du gaz vert issu de la décomposition de la matière organique.</p><p>&nbsp;</p><p class="!text-sm !text-primary-9 font-[Marianne]">Le bois énergie représente 35% de la production locale d’EnR&amp;R, soit…

#### Fiche 65623 — Action n°34 - Soutenir les agriculteurs et développer une agriculture durable de proximité

- **Run 1 :** Bâtiments & Machines agricoles [2, 3, 4, 6] | Changements de pratiques de fertilisation azotée [3, 4, 6] | Elevage durable [3, 4, 6] | Gestion des haies [1, 3, 4, 6] | Gestion des prairies [3, 4, 6] | Pratiques stockantes [3, 4, 6]
- **Run 2 :** Bâtiments & Machines agricoles [3, 6] | Changements de pratiques de fertilisation azotée [3, 6] | Elevage durable [3, 6] | Gestion des prairies [3, 6] | Pratiques stockantes [3, 6]
- **Run 3 :** Changements de pratiques de fertilisation azotée [2, 4, 6] | Elevage durable [4, 6] | Pratiques stockantes [4, 6]
- **Prod :** (aucun levier)
- Leviers intermittents : Bâtiments & Machines agricoles (2/3), Gestion des haies (1/3), Gestion des prairies (2/3)
- Catégories instables sur : Changements de pratiques de fertilisation azotée, Elevage durable, Pratiques stockantes

> <p class="!text-sm !text-primary-9 font-[Marianne]">La Métropole de Lyon dispose de 21 370 ha de surfaces agricoles et naturelles, dont 11 186 ha classés en périmètre de Protection des Espaces Naturels et Agricoles Périurbains (PENAP). La Surface agricole utile (SAU) est de 10 622 ha (pour 230 exploitations) dont 2 041 ha en bio (pour 60 exploitations), soit 19,2 % de la SAU en bio.</p><p>&nbsp;</p><p class="!text-sm !text-primary-9 font-[Marianne]">Les productions agricoles dominantes sur le t…

#### Fiche 65632 — Action n°42 - Réduire les consommations énergétiques des services publics d’eau et d’assainissement

- **Run 1 :** Biogaz [1, 5] | Réseaux de chaleur décarbonés [1, 5]
- **Run 2 :** Biogaz [5]
- **Run 3 :** Biogaz [5] | Réseaux de chaleur décarbonés [5]
- **Prod :** Biogaz [5] | Réseaux de chaleur décarbonés [5]
- Leviers intermittents : Réseaux de chaleur décarbonés (2/3)
- Catégories instables sur : Biogaz

> <p class="!text-sm !text-primary-9 font-[Marianne]">Les Services Publics d’Eau et d’Assainissement (SPEA) représentent une part importante du bilan énergétique global de la collectivité, notamment le volet traitement en station d’épuration : en 2023, la part de l’assainissement s’élevait à 62% des consommations électriques (28,5 GWh) de la Métropole et 22% des consommations de gaz (1,6 million de Nm3).</p><ul><li><p class="!text-sm !text-primary-9 font-[Marianne]">Concernant l’eau, la Régie Eau…

#### Fiche 90525 — D8 - COP : Contribuer à la sobriété énergétique des bâtiments tertiaires, en élaborant et mettant en œuvre des schémas directeurs immobilier et énergétique

- **Run 1 :** Sobriété et isolation des bâtiments (tertiaire) [2, 4, 6]
- **Run 2 :** Changement de chaudière à fioul (tertiaire) [2] | Changement de chaudière à gaz (tertiaire) [2] | Sobriété et isolation des bâtiments (tertiaire) [2]
- **Run 3 :** Changement de chaudière à fioul (tertiaire) [2, 4] | Changement de chaudière à gaz (tertiaire) [2, 4] | Sobriété et isolation des bâtiments (tertiaire) [2, 4]
- **Prod :** Sobriété et isolation des bâtiments (tertiaire) [5]
- Leviers intermittents : Changement de chaudière à fioul (tertiaire) (2/3), Changement de chaudière à gaz (tertiaire) (2/3)
- Catégories instables sur : Sobriété et isolation des bâtiments (tertiaire)

#### Fiche 90534 — D16 - COP : Contribuer, pour les déplacements de marchandises, à réduire les distances parcourues et à massifie le recours au fret (ferroviaire et fluvial)

- **Run 1 :** Efficacité et sobriété logistique [4] | Fret décarboné et multimodalité [2, 4]
- **Run 2 :** Fret décarboné et multimodalité [4]
- **Run 3 :** Efficacité et sobriété logistique [4] | Fret décarboné et multimodalité [4]
- **Prod :** Fret décarboné et multimodalité [4]
- Leviers intermittents : Efficacité et sobriété logistique (2/3)
- Catégories instables sur : Fret décarboné et multimodalité

#### Fiche 90550 — D32 - Faciliter le retour à la terre des biodéchets et résidus de taille de végétaux 

- **Run 1 :** Valorisation matière des déchets [1, 6]
- **Run 2 :** Valorisation matière des déchets [4]
- **Run 3 :** Pratiques stockantes [4] | Valorisation matière des déchets [4]
- **Prod :** Valorisation matière des déchets [6]
- Leviers intermittents : Pratiques stockantes (1/3)
- Catégories instables sur : Valorisation matière des déchets

#### Fiche 90557 — Soutenir et structurer les actions locales en faveur du changement de comportement des habitants,  en matière de réduction des consommations d’énergie, de mobilité, des déchets et de l’eau dans une approche multi-thématiques afin de renforcer leur efficacité

- **Run 1 :** Prévention des déchets [6] | Réduction des déplacements [6] | Sobriété des bâtiments (résidentiel) [6]
- **Run 2 :** Prévention des déchets [6] | Réduction des déplacements [6] | Sobriété des bâtiments (résidentiel) [6] | Valorisation matière des déchets [6]
- **Run 3 :** Covoiturage [4, 6] | Prévention des déchets [4, 6] | Réduction des déplacements [4, 6] | Sobriété des bâtiments (résidentiel) [4, 6] | Vélo et transport en commun [4, 6]
- **Prod :** Prévention des déchets [6] | Réduction des déplacements [6] | Sobriété des bâtiments (résidentiel) [6]
- Leviers intermittents : Covoiturage (1/3), Valorisation matière des déchets (1/3), Vélo et transport en commun (1/3)
- Catégories instables sur : Prévention des déchets, Réduction des déplacements, Sobriété des bâtiments (résidentiel)

### Mêmes leviers, catégories différentes (16)

#### Fiche 65602 — Action n°13 - Amplifier la rénovation énergétique globale et performante du parc de logements pour le confort d’été et d’hiver

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [3, 6] | Changement chaudières gaz + rénovation (résidentiel) [3, 6] | Sobriété des bâtiments (résidentiel) [3, 6]
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [3, 4, 6] | Changement chaudières gaz + rénovation (résidentiel) [3, 4, 6] | Sobriété des bâtiments (résidentiel) [3, 4, 6]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [3, 6] | Changement chaudières gaz + rénovation (résidentiel) [3, 6] | Sobriété des bâtiments (résidentiel) [3, 6]
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [3] | Changement chaudières gaz + rénovation (résidentiel) [3]
- Catégories instables sur : Changement chaudières fioul + rénovation (résidentiel), Changement chaudières gaz + rénovation (résidentiel), Sobriété des bâtiments (résidentiel)

> <p class="!text-sm !text-primary-9 font-[Marianne]">Le PCAET 2026-2031 fixe de nouveaux objectifs de rénovation énergétique pour la baisse des consommations d’énergie et de la décarbonation des logements&nbsp;:</p><p class="!text-sm !text-primary-9 font-[Marianne]"><strong>Sur la période 2020-2030</strong>&nbsp;: 66 700 logements rénovés dans le cadre d’opérations de rénovations énergétiques dans le parc existant public et privé dont :&nbsp;</p><ul><li><p class="!text-sm !text-primary-9 font-[M…

#### Fiche 65604 — Action n°15 - Développer et sécuriser les infrastructures dédiées aux modes actifs 

- **Run 1 :** Vélo et transport en commun [1, 2]
- **Run 2 :** Vélo et transport en commun [1, 2]
- **Run 3 :** Vélo et transport en commun [1]
- **Prod :** Vélo et transport en commun [1]
- Catégories instables sur : Vélo et transport en commun

> <p class="!text-sm !text-primary-9 font-[Marianne]">En 2021, 24% des émissions de gaz à effet de serre cadastrales sur la Métropole étaient dues au transport routier, dont la moitié environ aux véhicules particuliers (le reste relevant des poids lourds et véhicules utilitaires).</p><p>&nbsp;</p><p class="!text-sm !text-primary-9 font-[Marianne]">Le Plan de Mobilité des Territoires Lyonnais (PDM) vise à réduire ces émissions de 64% sur le territoire de SYTRAL Mobilités d’ici 2040, notamment par …

#### Fiche 65606 — Action n°17 - Préfigurer un modèle de logistique de chantier et de logistique urbaine sobre et décarbonée

- **Run 1 :** Efficacité et sobriété logistique [1, 4, 6] | Fret décarboné et multimodalité [1, 4, 6]
- **Run 2 :** Efficacité et sobriété logistique [1, 4] | Fret décarboné et multimodalité [1, 4]
- **Run 3 :** Efficacité et sobriété logistique [1, 4] | Fret décarboné et multimodalité [1, 4]
- **Prod :** Efficacité et sobriété logistique [1, 4, 6] | Fret décarboné et multimodalité [1, 4, 6]
- Catégories instables sur : Efficacité et sobriété logistique, Fret décarboné et multimodalité

> <p class="!text-sm !text-primary-9 font-[Marianne]">Une immense majorité des activités urbaines sont génératrices de flux de marchandises. Les volumes traités sont très importants : ils représentent sur la Métropole de Lyon en moyenne 35 tonnes de marchandises par an par habitant. Sur les 200 000 livraisons quotidiennes réalisées sur le territoire de la Métropole de Lyon, 80% sont à destination des établissements économiques et 20% à destination des ménages. Aujourd’hui, le fonctionnement des c…

#### Fiche 65609 — Action n°20 - Transformer l’économie linéaire en économie circulaire au profit des habitants 

- **Run 1 :** Prévention des déchets [3, 6] | Valorisation matière des déchets [3, 6]
- **Run 2 :** Prévention des déchets [3, 6] | Valorisation matière des déchets [3, 6]
- **Run 3 :** Prévention des déchets [1, 3, 5, 6] | Valorisation matière des déchets [1, 3, 5, 6]
- **Prod :** Prévention des déchets [3, 6] | Valorisation matière des déchets [1, 3, 5, 6]
- Catégories instables sur : Prévention des déchets, Valorisation matière des déchets

> <p class="!text-sm !text-primary-9 font-[Marianne]">Pour atteindre ses objectifs de prévention et gestion des déchets, la Métropole doit aussi s’appuyer sur les acteurs économiques qui développent de nouvelles offres circulaires (entreprises nativement circulaires ou en « en transition »).</p><p>&nbsp;</p><p class="!text-sm !text-primary-9 font-[Marianne]">Pour soutenir ces acteurs économiques la Métropole de Lyon utilise 4 leviers :</p><ul><li><p class="!text-sm !text-primary-9 font-[Marianne]…

#### Fiche 65611 — Action n°22 - Poursuivre le développement de la production de chaleur et de froid renouvelable

- **Run 1 :** Réseaux de chaleur décarbonés [1]
- **Run 2 :** Réseaux de chaleur décarbonés [1, 3]
- **Run 3 :** Réseaux de chaleur décarbonés [1, 3]
- **Prod :** Réseaux de chaleur décarbonés [1, 3, 4]
- Catégories instables sur : Réseaux de chaleur décarbonés

> <p class="!text-sm !text-primary-9 font-[Marianne]">Les données de l’ORCAE (2022) mettent en évidence qu’un tiers des consommations énergétiques du territoire métropolitain répondent aux besoins en chauffage (27,6%), eau chaude sanitaire (4,3%) et climatisation&nbsp;des bâtiments (1,1%), aujourd’hui essentiellement couverts par des énergies fossiles (fioul, gaz).&nbsp;</p><p>&nbsp;</p><p class="!text-sm !text-primary-9 font-[Marianne]">Pour réduire les émissions qui en résultent, la Métropole d…

#### Fiche 65612 — Action n°23 - Accompagner la réduction des consommations énergétiques à destination des ménages, des acteurs publics et des entreprises

- **Run 1 :** Sobriété des bâtiments (résidentiel) [6] | Sobriété et isolation des bâtiments (tertiaire) [6]
- **Run 2 :** Sobriété des bâtiments (résidentiel) [6] | Sobriété et isolation des bâtiments (tertiaire) [6]
- **Run 3 :** Sobriété des bâtiments (résidentiel) [6] | Sobriété et isolation des bâtiments (tertiaire) [5, 6]
- **Prod :** Sobriété des bâtiments (résidentiel) [6] | Sobriété et isolation des bâtiments (tertiaire) [6]
- Catégories instables sur : Sobriété et isolation des bâtiments (tertiaire)

> <p class="!text-sm !text-primary-9 font-[Marianne]">La trajectoire de réduction des consommations énergétiques inscrite dans le PCAET prévoit une baisse de 16% en 2030, 32% en 2040 et 49% en 2050 par rapport à 2021. Cette forte ambition impose à la collectivité et aux acteurs du territoire d’être pro-actifs aussi bien en matière d’efficacité que de sobriété énergétique, et ce dans tous les secteurs d’activité (transports, industrie, bâtiments résidentiels et tertiaires). Si l’efficacité énergét…

#### Fiche 65614 — Action n°25 - Massifier le recours à l‘énergie solaire photovoltaïque

- **Run 1 :** Electricité renouvelable [2, 6]
- **Run 2 :** Electricité renouvelable [2, 4, 6]
- **Run 3 :** Electricité renouvelable [1, 2, 6]
- **Prod :** Electricité renouvelable [2, 4, 6]
- Catégories instables sur : Electricité renouvelable

> <p class="!text-sm !text-primary-9 font-[Marianne]">La production d’électricité solaire sur le territoire métropolitain s’élève à 92,6 GWh en 2023, soit environ 10% de la production locale d’électricité renouvelable et 1% de la consommation d’électricité, tous secteurs et usages confondus. Elle a été multipliée par 1,5 entre 2020 et 2023. </p><p>&nbsp;</p><p class="!text-sm !text-primary-9 font-[Marianne]">Les obligations réglementaires issues de la loi APER (Loi relative à l'accélération de la…

#### Fiche 65617 — Action n°28 - Réduire l’empreinte carbone de l’alimentation

- **Run 1 :** Prévention des déchets [2, 4, 6]
- **Run 2 :** Prévention des déchets [6]
- **Run 3 :** Prévention des déchets [6]
- **Prod :** (aucun levier)
- Catégories instables sur : Prévention des déchets

> <p class="!text-sm !text-primary-9 font-[Marianne]">En 2019, la Métropole de Lyon a adopté une stratégie alimentaire élaborée en concertation avec les acteurs locaux. Cette initiative découle d’un diagnostic approfondi révélant deux enjeux majeurs : la faible autonomie alimentaire du territoire et la nécessité de coopérer avec les territoires voisins, ainsi qu’une précarité alimentaire significative. L'objectif principal est de permettre à tous les habitants d’accéder à une alimentation de qual…

#### Fiche 65622 — Action n°33 - Déployer une stratégie globale de végétalisation intégrant une trame boisée et agro-bocagère

- **Run 1 :** Gestion des forêts et produits bois [1, 2, 6] | Gestion des haies [1, 6] | Pratiques stockantes [1]
- **Run 2 :** Gestion des forêts et produits bois [1, 2, 4] | Gestion des haies [1, 2, 4] | Pratiques stockantes [1, 2]
- **Run 3 :** Gestion des forêts et produits bois [1] | Gestion des haies [1] | Pratiques stockantes [1, 2]
- **Prod :** Gestion des forêts et produits bois [1] | Gestion des haies [1]
- Catégories instables sur : Gestion des forêts et produits bois, Gestion des haies, Pratiques stockantes

> <p class="!text-sm !text-primary-9 font-[Marianne]">La végétalisation du territoire constitue un marqueur fort du mandat actuel. Ce sont ainsi 180 000 arbres et arbustes qui ont été plantés depuis 2020 dans des espaces publics et privés. Pour autant, et alors que ce couvert arboré joue un rôle multiple (écologique, paysager, productif, rafraîchissant, protecteur pour le cycle de l’eau et la captation carbone), il existe de fortes différences en matière de taux de canopée au sein du territoire m…

#### Fiche 90522 — D5 - COP : Forêt  : contribuer à gérer les risques (sanitaires, incendies, tempêtes) : anticiper et planifier la gestion de ces risques 

- **Run 1 :** Gestion des forêts et produits bois [1, 4]
- **Run 2 :** Gestion des forêts et produits bois [2, 4]
- **Run 3 :** Gestion des forêts et produits bois [4]
- **Prod :** (aucun levier)
- Catégories instables sur : Gestion des forêts et produits bois

#### Fiche 90524 — D7 - Développer un réflexe « confort d’été » dans tous les projets, études et bouquets d’actions, dans le cadre de la rénovation, de la construction et de la transition énergétique du bâti

- **Run 1 :** Sobriété des bâtiments (résidentiel) [1, 2, 6] | Sobriété et isolation des bâtiments (tertiaire) [1, 2, 6]
- **Run 2 :** Sobriété des bâtiments (résidentiel) [1, 2, 6] | Sobriété et isolation des bâtiments (tertiaire) [1, 2, 6]
- **Run 3 :** Sobriété des bâtiments (résidentiel) [2] | Sobriété et isolation des bâtiments (tertiaire) [2]
- **Prod :** (aucun levier)
- Catégories instables sur : Sobriété des bâtiments (résidentiel), Sobriété et isolation des bâtiments (tertiaire)

#### Fiche 90527 — D10 - Explorer les dispositifs alternatifs à la climatisation individuelle ainsi que le développement d’espaces rafraîchis à l’échelle de plusieurs résidences ou immeubles pour limiter le recours à la climatisation individuelle

- **Run 1 :** Sobriété des bâtiments (résidentiel) [1, 6]
- **Run 2 :** Sobriété des bâtiments (résidentiel) [1, 4]
- **Run 3 :** Sobriété des bâtiments (résidentiel) [1, 4]
- **Prod :** (aucun levier)
- Catégories instables sur : Sobriété des bâtiments (résidentiel)

#### Fiche 90532 — D14 - Renforcer le développement du transport ferré et fluvial de marchandises  pour améliorer les dessertes intra-territoriales

- **Run 1 :** Fret décarboné et multimodalité [1]
- **Run 2 :** Fret décarboné et multimodalité [1]
- **Run 3 :** Fret décarboné et multimodalité [1, 4]
- **Prod :** Fret décarboné et multimodalité [4]
- Catégories instables sur : Fret décarboné et multimodalité

#### Fiche 90538 — D21 - COP : Contribuer à construire avec exemplarité : promouvoir l’utilisation du bois dans le secteur du bâtiment (énergie et construction)

- **Run 1 :** Gestion des forêts et produits bois [6]
- **Run 2 :** Gestion des forêts et produits bois [6]
- **Run 3 :** Gestion des forêts et produits bois [4, 6]
- **Prod :** Gestion des forêts et produits bois [6]
- Catégories instables sur : Gestion des forêts et produits bois

#### Fiche 90540 — D23 - COP : Contribuer à encourager la sobriété et accélérer la rénovation thermique des logements : sortir du fioul 

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [6] | Sobriété des bâtiments (résidentiel) [6]
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [3, 6] | Sobriété des bâtiments (résidentiel) [6]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [4, 6] | Sobriété des bâtiments (résidentiel) [4, 6]
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [6]
- Catégories instables sur : Changement chaudières fioul + rénovation (résidentiel), Sobriété des bâtiments (résidentiel)

#### Fiche 111906 — D20 - COP : Contribuer à accélerer la montée en compétence des acteurs de la rénovation

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6] | Changement de chaudière à fioul (tertiaire) [6] | Changement de chaudière à gaz (tertiaire) [6] | Sobriété des bâtiments (résidentiel) [6] | Sobriété et isolation des bâtiments (tertiaire) [6]
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6] | Changement de chaudière à fioul (tertiaire) [6] | Changement de chaudière à gaz (tertiaire) [6] | Sobriété des bâtiments (résidentiel) [6] | Sobriété et isolation des bâtiments (tertiaire) [6]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [4, 6] | Changement chaudières gaz + rénovation (résidentiel) [4, 6] | Changement de chaudière à fioul (tertiaire) [4, 6] | Changement de chaudière à gaz (tertiaire) [4, 6] | Sobriété des bâtiments (résidentiel) [4, 6] | Sobriété et isolation des bâtiments (tertiaire) [4, 6]
- **Prod :** (aucun levier)
- Catégories instables sur : Changement chaudières fioul + rénovation (résidentiel), Changement chaudières gaz + rénovation (résidentiel), Changement de chaudière à fioul (tertiaire), Changement de chaudière à gaz (tertiaire), Sobriété des bâtiments (résidentiel), Sobriété et isolation des bâtiments (tertiaire)

## CC Val de Gray (5005)

- Fiches : **42** — stables sur les 3 runs : **29** (69%), instables : **13**
- Paires levier × catégorie distinctes proposées : 87 — 3/3 runs : 46, 2/3 runs : 13, 1/3 runs : 28
- Aucune classification en prod pour cette collectivité
- Réponses JSON invalides rejouées : 1
- Appels : 6 — tokens d'entrée 22 897 (dont 0 en cache, 0%), sortie 41 636 — coût estimé 0.10 $ pour les 3 runs
- Date : 2026-10-30 14:38

### Classée dans certains runs, aucun levier dans d'autres (7)

#### Fiche 12589 — Limiter l'emprise de la publicité

- **Run 1 :** (aucun levier)
- **Run 2 :** Prévention des déchets [2, 3, 6]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Prévention des déchets (1/3)

> - Sensibiliser les habitants à travers des actions rapides et efficaces tel que la promotion et généralisation du Stop Pub pour réduire les imprimés - Faire respecter les obligations concernant les enseignes lumineuses des commerces et l'affichage sur la voie publique - Mettre en place une taxe locale sur les enseignes et publicités extérieures (TPLE) - Devenir une ville sans publicité en instaurant une Zone de Publicité Restreinte et en supprimant la publicité commerciale au profit d'une publi…

#### Fiche 12593 — Optimiser la gestion des eaux pluviales

- **Run 1 :** (aucun levier)
- **Run 2 :** (aucun levier)
- **Run 3 :** Sobriété foncière [1]
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété foncière (1/3)

> Privilégier l'infiltration à la parcelle et réduire les surfaces imperméabilisées afin de réduire les risques et la fréquence des pollution des milieux aquatiques lors des épisodes de forte pluie

#### Fiche 12604 — Mettre en place une politique d'achat exemplaires pour avoir un impact positif sur le territoire

- **Run 1 :** Prévention des déchets [5]
- **Run 2 :** Prévention des déchets [5]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Prévention des déchets (2/3)

> Définir des objectifs cibles à atteindre à moyen et long terme pour l’augmentation de la part des marches publics socialement et écologiquement responsables. Intégrer systématiquement dans les marchés publics d'achat de biens matériels ou de services, des critères d'efficacité énergétique, de réduction de l'impact environnemental (y compris qualité de l'air), de coût du cycle de vie s'ils existent

#### Fiche 12605 — Diagnostic des flux matières/ressources/Economie circulaire sur le territoire

- **Run 1 :** Prévention des déchets [4] | Valorisation matière des déchets [4]
- **Run 2 :** (aucun levier)
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Prévention des déchets (1/3), Valorisation matière des déchets (1/3)

> Effectuer une analyse de l'Economie circulaire pour le territoire, de manière quantitative et qualitative (renouveler cette analyse au maximum tous les 6 ans) Suivre annuellement l'évolution de la production de déchets du territoire

#### Fiche 12610 — Prévenir et lutter contre la précarité énergétique

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [2, 6] | Changement chaudières gaz + rénovation (résidentiel) [2, 6] | Sobriété des bâtiments (résidentiel) [2, 6]
- **Run 2 :** (aucun levier)
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [2, 3, 6] | Changement chaudières gaz + rénovation (résidentiel) [2, 3, 6] | Sobriété des bâtiments (résidentiel) [2, 3, 6]
- **Prod :** (aucun levier)
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (2/3), Changement chaudières gaz + rénovation (résidentiel) (2/3), Sobriété des bâtiments (résidentiel) (2/3)

> Engager une politique de prévention et de lutte contre la précarité énergétique (liée au logement et à la mobilité) et l'inscrire dans ses documents stratégiques. Réaliser un travail d’inventaire des acteurs de la précarité énergétique et des actions existantes, sur lesquelles construire le dispositif. Utiliser au mieux les moyens humains à disposition pour identifier des situations de précarité énergétique du logement et orienter les familles directement vers les dispositifs existants ou indir…

#### Fiche 12613 — Connaitre le potentiel de développement des ENR du territoire et programmer leur développement

- **Run 1 :** Biogaz [4] | Electricité renouvelable [4] | Réseaux de chaleur décarbonés [4]
- **Run 2 :** (aucun levier)
- **Run 3 :** Biogaz [2, 4] | Electricité renouvelable [2, 4] | Réseaux de chaleur décarbonés [2, 4]
- **Prod :** (aucun levier)
- Leviers intermittents : Biogaz (2/3), Electricité renouvelable (2/3), Réseaux de chaleur décarbonés (2/3)

> - Prendre en compte et quantifier tous les potentiels de développement - Programmer la mise en oeuvre de l'ensemble du potentiel de production d'énergie renouvelable locale

#### Fiche 12618 — Favoriser un tourisme durable

- **Run 1 :** (aucun levier)
- **Run 2 :** Réduction des déplacements [2]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Réduction des déplacements (1/3)

> Elaborer une stratégie touristique durable pour réduire les impacts du tourisme sur les ressources naturelles et les écosystèmes (la pression sur la ressource locale en eau, …), en matière d'émissions GES (notamment liées au transport) et l'accès aux activités touristiques pour tous

### Levier présent dans certains runs seulement (2)

#### Fiche 12598 — Protéger toutes les aires d'alimentation de captage en eau potable, y compris celles étant non prioritaires

- **Run 1 :** Changements de pratiques de fertilisation azotée [2] | Elevage durable [2] | Production Industrielle [2]
- **Run 2 :** Changements de pratiques de fertilisation azotée [2] | Elevage durable [2]
- **Run 3 :** Changements de pratiques de fertilisation azotée [2] | Elevage durable [2]
- **Prod :** (aucun levier)
- Leviers intermittents : Production Industrielle (1/3)

> Protéger toutes les aires d'alimentation de captage en eau potable "y compris celles étant non prioritaires" avec des politiques précises de restriction des usages sur la zone (Agriculture : Conversion et installation en agriculture biologique, Élevage extensif ; Activités économiques & industrie : 0 rejets)

#### Fiche 12599 — Développer le réseau piétonnier

- **Run 1 :** Vélo et transport en commun [1]
- **Run 2 :** Réduction des déplacements [1]
- **Run 3 :** Réduction des déplacements [1]
- **Prod :** (aucun levier)
- Leviers intermittents : Réduction des déplacements (2/3), Vélo et transport en commun (1/3)

> Le réseau piétonnier et la marchabilité est priorisée dans tous les aménagements du territoire

### Levier intermittent et catégories instables (3)

#### Fiche 12594 — Soutenir une agriculture et une alimentation plus durable

- **Run 1 :** Bâtiments & Machines agricoles [6] | Changements de pratiques de fertilisation azotée [3, 6] | Elevage durable [3, 6] | Prévention des déchets [5, 6] | Sobriété foncière [2]
- **Run 2 :** Changements de pratiques de fertilisation azotée [3, 4, 6] | Elevage durable [2, 3, 4, 6] | Prévention des déchets [5, 6] | Sobriété foncière [2]
- **Run 3 :** Bâtiments & Machines agricoles [3, 6] | Changements de pratiques de fertilisation azotée [3, 6] | Elevage durable [3, 6] | Pratiques stockantes [3, 6] | Prévention des déchets [5, 6] | Sobriété foncière [2]
- **Prod :** (aucun levier)
- Leviers intermittents : Bâtiments & Machines agricoles (2/3), Pratiques stockantes (1/3)
- Catégories instables sur : Changements de pratiques de fertilisation azotée, Elevage durable

> Soutenir, promouvoir et encourager des pratiques agricoles et alimentaires durables sur son territoire et sur ses territoires d’approvisionnement : - en menant des actions visant à réduire les émissions de gaz à effet de serre, de particules et plus globalement les impacts environnementaux du secteur agricole (formation aux pratiques agro-écologiques, certification environnementale des exploitations...) - en préservant le foncier agricole au travers des documents d’urbanisme et en accompagnant …

#### Fiche 12597 — Récupérer la chaleur industrielle, pratiquer la cogénération, utiliser les réseaux de chaleur/froid comme vecteur

- **Run 1 :** Production Industrielle [1, 4] | Réseaux de chaleur décarbonés [1]
- **Run 2 :** Réseaux de chaleur décarbonés [1]
- **Run 3 :** Réseaux de chaleur décarbonés [1, 4]
- **Prod :** (aucun levier)
- Leviers intermittents : Production Industrielle (1/3)
- Catégories instables sur : Réseaux de chaleur décarbonés

> Les possibilités de récupération de chaleur des grandes entreprises industrielles et des centrales électriques, y compris à partir et pour la production de froid, sont exploitées. Le potentiel de cogénération voire de tri-génération (à partir d’énergies renouvelables prioritairement, puis de gaz naturel) par exemple pour le secteur du chauffage ou du rafraîchissement, est connu et exploité. Les technologies et les sources d’énergie utilisées sont choisies dans une approche multicritère climat-a…

#### Fiche 12609 — Préserver la biodiversité du territoire et développer des espaces verts

- **Run 1 :** Gestion des forêts et produits bois [1] | Pratiques stockantes [1, 2]
- **Run 2 :** Pratiques stockantes [1]
- **Run 3 :** Gestion des forêts et produits bois [1, 2] | Pratiques stockantes [1]
- **Prod :** (aucun levier)
- Leviers intermittents : Gestion des forêts et produits bois (2/3)
- Catégories instables sur : Pratiques stockantes

> Protéger les espaces naturels existants et développer les trames vertes et bleues. Végétaliser en plantant des arbres et en développant les espaces verts avec une approche prenant en considération les risques d'évolution climatique sur le territoire et en choisissant des espèces permettant de supprimer (ou a minima de limiter) les besoins d'arrosage.

### Mêmes leviers, catégories différentes (1)

#### Fiche 12591 — Élaborer une politique de stationnement volontariste

- **Run 1 :** Réduction des déplacements [1, 2, 3]
- **Run 2 :** Réduction des déplacements [2, 3, 6]
- **Run 3 :** Réduction des déplacements [2, 3]
- **Prod :** (aucun levier)
- Catégories instables sur : Réduction des déplacements

> Mettre en place une politique de stationnement dans le centre-ville et/ ou les zones de forte pression (commerces de quartier, etc.) Mettre en place une tarification différenciée si besoin Pour les communes en zones rurale, mettre l'accent sur la sensibilisation et l’information auprès des habitants sur le besoin de gérer l’usage de la voiture et de marquer les places réservées au stationnement et le développement de zones bleues le cas échéant autour des zones de trafic. Faire respecter la rég…

## CC Brionnais Sud Bourgogne (5033)

- Fiches : **111** — stables sur les 3 runs : **74** (67%), instables : **37**
- Paires levier × catégorie distinctes proposées : 117 — 3/3 runs : 56, 2/3 runs : 29, 1/3 runs : 32
- Vote majoritaire = prod : 18/73 fiches classées d'un côté ou de l'autre
- Réponses JSON invalides rejouées : 0
- Appels : 15 — tokens d'entrée 28 119 (dont 0 en cache, 0%), sortie 97 993 — coût estimé 0.22 $ pour les 3 runs
- Date : 2026-10-30 15:07

### Classée dans certains runs, aucun levier dans d'autres (22)

#### Fiche 57551 — 2.2.6 Réaliser une chronomap vélo (en lien avec SDMA de CCBSB)

- **Run 1 :** Vélo et transport en commun [2]
- **Run 2 :** (aucun levier)
- **Run 3 :** (aucun levier)
- **Prod :** Vélo et transport en commun [6]
- Leviers intermittents : Vélo et transport en commun (1/3)

#### Fiche 57554 — 2.3.3 Être exemplaire au niveau des collectivités

- **Run 1 :** (aucun levier)
- **Run 2 :** Véhicules électriques [5]
- **Run 3 :** Véhicules électriques [5]
- **Prod :** (aucun levier)
- Leviers intermittents : Véhicules électriques (2/3)

#### Fiche 57562 — 3.1.3 Inciter les communes qui ne l'ont pas fait à réaliser un diagnostic énergétique de leurs bâtiments publics

- **Run 1 :** Sobriété et isolation des bâtiments (tertiaire) [4]
- **Run 2 :** Sobriété et isolation des bâtiments (tertiaire) [4]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété et isolation des bâtiments (tertiaire) (2/3)

#### Fiche 57563 — 3.1.4 Inciter les communes à faire appel à un "Conseiller en Energie partagée"

- **Run 1 :** Sobriété et isolation des bâtiments (tertiaire) [4]
- **Run 2 :** Sobriété et isolation des bâtiments (tertiaire) [4]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété et isolation des bâtiments (tertiaire) (2/3)

#### Fiche 57564 — 3.1.5 Réaliser un groupement de commandes pour les DPE manquants

- **Run 1 :** Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 2 :** Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété et isolation des bâtiments (tertiaire) (2/3)

#### Fiche 57565 — 3.1.6 Mettre en place un suivi des consommations énergétiques

- **Run 1 :** Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 2 :** Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété et isolation des bâtiments (tertiaire) (2/3)

#### Fiche 57566 — 3.1.7 Etudier la possibilité de grouper les achats de combustibles des 3 CC

- **Run 1 :** (aucun levier)
- **Run 2 :** Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété et isolation des bâtiments (tertiaire) (1/3)

#### Fiche 57567 — 3.2.1 Compiler les bonnes pratiques de chaque commune, les résultats obtenus en termes de baisse des consommations et d'impact sur le budget de toutes les communes

- **Run 1 :** Sobriété et isolation des bâtiments (tertiaire) [4]
- **Run 2 :** Sobriété et isolation des bâtiments (tertiaire) [4]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété et isolation des bâtiments (tertiaire) (2/3)

#### Fiche 57568 — 3.2.2 Proposer une charte des bonnes pratiques aux communes

- **Run 1 :** Sobriété et isolation des bâtiments (tertiaire) [4]
- **Run 2 :** Sobriété et isolation des bâtiments (tertiaire) [4]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété et isolation des bâtiments (tertiaire) (2/3)

#### Fiche 57572 — 3.3.2 Communiquer sur les aides existantes

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6] | Sobriété des bâtiments (résidentiel) [6]
- **Run 2 :** Sobriété des bâtiments (résidentiel) [6]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (1/3), Changement chaudières gaz + rénovation (résidentiel) (1/3), Sobriété des bâtiments (résidentiel) (2/3)

#### Fiche 57574 — 3.3.4 Organiser des réunions publiques avec des spécialistes de la rénovation énergétique

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6] | Sobriété des bâtiments (résidentiel) [6]
- **Run 2 :** Sobriété des bâtiments (résidentiel) [6]
- **Run 3 :** (aucun levier)
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6]
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (1/3), Changement chaudières gaz + rénovation (résidentiel) (1/3), Sobriété des bâtiments (résidentiel) (2/3)

#### Fiche 57575 — 3.3.5 Informer les habitants sur des éco-conceptions exemplaires de la région, des retours d'expériences avant/après rénovation, visites

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6] | Sobriété des bâtiments (résidentiel) [6]
- **Run 2 :** Sobriété des bâtiments (résidentiel) [6]
- **Run 3 :** (aucun levier)
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6]
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (1/3), Changement chaudières gaz + rénovation (résidentiel) (1/3), Sobriété des bâtiments (résidentiel) (2/3)

#### Fiche 57576 — 3.3.6 Organiser des formations sur la thématique "rénovation énergétique" (chantiers exemples, ateliers, constructions éco-conçues…)

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6] | Sobriété des bâtiments (résidentiel) [6]
- **Run 2 :** Sobriété des bâtiments (résidentiel) [6]
- **Run 3 :** (aucun levier)
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6]
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (1/3), Changement chaudières gaz + rénovation (résidentiel) (1/3), Sobriété des bâtiments (résidentiel) (2/3)

#### Fiche 57577 — 3.3.7 Organiser un Salon de l'Habitat

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6] | Sobriété des bâtiments (résidentiel) [6]
- **Run 2 :** Sobriété des bâtiments (résidentiel) [6]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (1/3), Changement chaudières gaz + rénovation (résidentiel) (1/3), Sobriété des bâtiments (résidentiel) (2/3)

#### Fiche 57579 — 3.4.2 Travailler avec les artisans pour la formation et l'information

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [4] | Changement chaudières gaz + rénovation (résidentiel) [4] | Sobriété des bâtiments (résidentiel) [4]
- **Run 2 :** Sobriété des bâtiments (résidentiel) [6]
- **Run 3 :** (aucun levier)
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [4] | Changement chaudières gaz + rénovation (résidentiel) [4]
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (1/3), Changement chaudières gaz + rénovation (résidentiel) (1/3), Sobriété des bâtiments (résidentiel) (2/3)

#### Fiche 57583 — 4.2.1 Mettre en place un suivi des consommations dans les bâtiments publics

- **Run 1 :** (aucun levier)
- **Run 2 :** Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété et isolation des bâtiments (tertiaire) (1/3)

#### Fiche 57584 — 4.2.2 Mettre en place des systèmes plus économes

- **Run 1 :** (aucun levier)
- **Run 2 :** Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 3 :** (aucun levier)
- **Prod :** Sobriété et isolation des bâtiments (tertiaire) [5]
- Leviers intermittents : Sobriété et isolation des bâtiments (tertiaire) (1/3)

#### Fiche 57587 — 4.3.1 Désimperméabiliser lorsque cela est possible

- **Run 1 :** Sobriété foncière [1]
- **Run 2 :** Sobriété foncière [1]
- **Run 3 :** (aucun levier)
- **Prod :** Sobriété foncière [1]
- Leviers intermittents : Sobriété foncière (2/3)

#### Fiche 57588 — 4.3.2 Intégrer les aménagements nécessaires pour chaque construction ou rénovation

- **Run 1 :** (aucun levier)
- **Run 2 :** Sobriété foncière [2]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété foncière (1/3)

#### Fiche 57618 — 6.2.4 Promouvoir les acteurs de l’économie circulaire

- **Run 1 :** (aucun levier)
- **Run 2 :** Prévention des déchets [6]
- **Run 3 :** Prévention des déchets [6] | Valorisation matière des déchets [6]
- **Prod :** Prévention des déchets [6]
- Leviers intermittents : Prévention des déchets (2/3), Valorisation matière des déchets (1/3)

> -> Ex : Diffuser la carte ADEME « Longue Vie aux objets » (réparation, réemploi, seconde main, don)

#### Fiche 57622 — 6.3.3 Analyser les biodéchets dans les poubelles du territoire

- **Run 1 :** (aucun levier)
- **Run 2 :** (aucun levier)
- **Run 3 :** Valorisation matière des déchets [4]
- **Prod :** (aucun levier)
- Leviers intermittents : Valorisation matière des déchets (1/3)

#### Fiche 57635 — 7.3.1 Créer des jardins partagés

- **Run 1 :** (aucun levier)
- **Run 2 :** Pratiques stockantes [1]
- **Run 3 :** Pratiques stockantes [1]
- **Prod :** (aucun levier)
- Leviers intermittents : Pratiques stockantes (2/3)

### Levier présent dans certains runs seulement (8)

#### Fiche 57545 — 2.1.1 Mise en place de navettes

- **Run 1 :** Réduction des déplacements [1] | Vélo et transport en commun [1]
- **Run 2 :** Vélo et transport en commun [1]
- **Run 3 :** Vélo et transport en commun [1]
- **Prod :** Vélo et transport en commun [1]
- Leviers intermittents : Réduction des déplacements (1/3)

#### Fiche 57578 — 3.4.1 Dans le cadre du Pacte territorial, accompagner les propriétaires du début à la fin de leurs démarches

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6] | Sobriété des bâtiments (résidentiel) [6]
- **Run 2 :** Sobriété des bâtiments (résidentiel) [6]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6] | Sobriété des bâtiments (résidentiel) [6]
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6]
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (2/3), Changement chaudières gaz + rénovation (résidentiel) (2/3)

> (démarches administratives, obtention d’aides financières, simulations...) => avoir une personne dédiée /!\ Que la personne soit formée à la fois pour les particuliers mais aussi pour les collectivités (pas les mêmes dispositifs d'aide, pas les mêmes démarches)

#### Fiche 57580 — 3.4.3 Créer un Espace Info Energie

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6] | Sobriété des bâtiments (résidentiel) [6]
- **Run 2 :** Sobriété des bâtiments (résidentiel) [6]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6] | Sobriété des bâtiments (résidentiel) [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (2/3), Changement chaudières gaz + rénovation (résidentiel) (2/3)

#### Fiche 57607 — 5.2.6 Développer des projets de chaufferies bois locales

- **Run 1 :** Réseaux de chaleur décarbonés [1]
- **Run 2 :** Gestion des forêts et produits bois [4] | Réseaux de chaleur décarbonés [1]
- **Run 3 :** Réseaux de chaleur décarbonés [1]
- **Prod :** Réseaux de chaleur décarbonés [1, 3]
- Leviers intermittents : Gestion des forêts et produits bois (1/3)

#### Fiche 57616 — 6.2.2 Développer des espaces ressourceries dans les déchetteries non équipées

- **Run 1 :** Valorisation matière des déchets [1]
- **Run 2 :** Prévention des déchets [1]
- **Run 3 :** Valorisation matière des déchets [1]
- **Prod :** Prévention des déchets [1]
- Leviers intermittents : Prévention des déchets (1/3), Valorisation matière des déchets (2/3)

#### Fiche 57630 — 7.1.1 Replanter des arbres dans les haies et les prés

- **Run 1 :** Gestion des haies [1] | Gestion des prairies [1] | Pratiques stockantes [1]
- **Run 2 :** Gestion des haies [1] | Pratiques stockantes [1]
- **Run 3 :** Gestion des haies [1] | Pratiques stockantes [1]
- **Prod :** Gestion des haies [1]
- Leviers intermittents : Gestion des prairies (1/3)

#### Fiche 57633 — 7.2.1 Planter des haies et des arbres

- **Run 1 :** Gestion des haies [1]
- **Run 2 :** Gestion des haies [1] | Pratiques stockantes [1]
- **Run 3 :** Gestion des haies [1] | Pratiques stockantes [1]
- **Prod :** Gestion des forêts et produits bois [1] | Gestion des haies [1]
- Leviers intermittents : Pratiques stockantes (2/3)

#### Fiche 57640 — 7.3.6 Organiser des ateliers (compostage, Do it yourself, cuisine éco-responable…)

- **Run 1 :** Prévention des déchets [6] | Valorisation matière des déchets [6]
- **Run 2 :** Prévention des déchets [6] | Valorisation matière des déchets [6]
- **Run 3 :** Prévention des déchets [6]
- **Prod :** Prévention des déchets [6] | Valorisation matière des déchets [6]
- Leviers intermittents : Valorisation matière des déchets (2/3)

### Levier intermittent et catégories instables (1)

#### Fiche 57571 — 3.3.1 Poursuivre et soutenir la rénovation énergétique de l’habitat (continuité des OPAH -> Pacte Territorial)

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [3, 6] | Changement chaudières gaz + rénovation (résidentiel) [3, 6] | Sobriété des bâtiments (résidentiel) [3, 6]
- **Run 2 :** Sobriété des bâtiments (résidentiel) [3]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [3, 6] | Changement chaudières gaz + rénovation (résidentiel) [3, 6] | Sobriété des bâtiments (résidentiel) [3, 6]
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [3] | Changement chaudières gaz + rénovation (résidentiel) [3]
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (2/3), Changement chaudières gaz + rénovation (résidentiel) (2/3)
- Catégories instables sur : Sobriété des bâtiments (résidentiel)

### Mêmes leviers, catégories différentes (6)

#### Fiche 57553 — 2.3.2 Travailler en collaboration avec le SYDESL sur leur SDIRVE

- **Run 1 :** Véhicules électriques [4]
- **Run 2 :** Véhicules électriques [2, 4]
- **Run 3 :** Véhicules électriques [4]
- **Prod :** (aucun levier)
- Catégories instables sur : Véhicules électriques

#### Fiche 57596 — 5.1.4 Développer le solaire photovoltaïque sur les bâtiments industriels et agricoles

- **Run 1 :** Electricité renouvelable [6]
- **Run 2 :** Electricité renouvelable [4]
- **Run 3 :** Electricité renouvelable [4]
- **Prod :** (aucun levier)
- Catégories instables sur : Electricité renouvelable

#### Fiche 57597 — 5.1.5 Respecter l'obligation de solarisation des parkings > 1500 m²

- **Run 1 :** Electricité renouvelable [2]
- **Run 2 :** Electricité renouvelable [2]
- **Run 3 :** Electricité renouvelable [2, 5]
- **Prod :** Electricité renouvelable [2]
- Catégories instables sur : Electricité renouvelable

#### Fiche 57621 — 6.3.2 Généraliser des actions permettant de réduire les tonnages produits (réduction des bacs de regroupement, fermeture des bacs d'ordures ménagères, fréquence de collecte…)

- **Run 1 :** Prévention des déchets [2]
- **Run 2 :** Prévention des déchets [1]
- **Run 3 :** Prévention des déchets [1]
- **Prod :** Prévention des déchets [2]
- Catégories instables sur : Prévention des déchets

#### Fiche 57632 — 7.1.3 Reboiser des terrains communaux avec potentiellement des projets participatifs

- **Run 1 :** Gestion des forêts et produits bois [1] | Pratiques stockantes [1]
- **Run 2 :** Gestion des forêts et produits bois [1, 6] | Pratiques stockantes [1, 6]
- **Run 3 :** Gestion des forêts et produits bois [1] | Pratiques stockantes [1]
- **Prod :** Gestion des forêts et produits bois [1]
- Catégories instables sur : Gestion des forêts et produits bois, Pratiques stockantes

#### Fiche 57634 — 7.2.2 Avoir une gestion plus durable des haies

- **Run 1 :** Gestion des haies [4, 6]
- **Run 2 :** Gestion des haies [4]
- **Run 3 :** Gestion des haies [4]
- **Prod :** Gestion des haies [1]
- Catégories instables sur : Gestion des haies

> Se renseigner sur des exemples d'entretien et valorisation des haies délégués à un tiers

## Le Havre Seine Métropole (5119)

- Fiches : **88** — stables sur les 3 runs : **56** (64%), instables : **32**
- Paires levier × catégorie distinctes proposées : 157 — 3/3 runs : 75, 2/3 runs : 25, 1/3 runs : 57
- Vote majoritaire = prod : 16/46 fiches classées d'un côté ou de l'autre
- Réponses JSON invalides rejouées : 0
- Appels : 12 — tokens d'entrée 70 989 (dont 0 en cache, 0%), sortie 69 413 — coût estimé 0.19 $ pour les 3 runs
- Date : 2026-10-30 12:12

### Classée dans certains runs, aucun levier dans d'autres (8)

#### Fiche 26076 — 1.2.4 Maîtriser les coûts de l'énergie, améliorer la gestion des achats du groupement à l'échelle du territoire

- **Run 1 :** (aucun levier)
- **Run 2 :** (aucun levier)
- **Run 3 :** Electricité renouvelable [5, 6]
- **Prod :** (aucun levier)
- Leviers intermittents : Electricité renouvelable (1/3)

> L'action vise à modifier le mode d'achat du groupement pour intégrer plus de flexibilité, maîtriser les coûts et augmenter la part d'énergie verte dans l'approvisionnement gaz et électricité. L'action comporte également un volet d'accompagnement des tiers (TPE/PME et particuliers) pour leurs achats d'énergie.

#### Fiche 26125 — 2.2.4 Accompagner l'électrification des quais pour contribuer à la réduction de l'impact carbone du transport maritime

- **Run 1 :** (aucun levier)
- **Run 2 :** Fret décarboné et multimodalité [1]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Fret décarboné et multimodalité (1/3)

> L’électrification des quais croisière, qui permet aux navires de se raccorder à l’électricité lors de leurs escales, est un enjeu majeur de réduction des émissions de gaz à effet de serre et plus largement de polluants atmosphériques. Préalablement au lancement des travaux, le raccordement au réseau de distribution public d’électricité réalisé par Enedis a nécessité la création de 3 km de réseau souterrain composé de 3 câbles 20 000 volts et l’ajout d’un transformateur HTB/HTA 40MVA au poste so…

#### Fiche 26707 — 3.2.2 Développer la filière de production d'hydrogène

- **Run 1 :** (aucun levier)
- **Run 2 :** Production Industrielle [4]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Production Industrielle (1/3)

> La Communauté urbaine Le Havre Seine Métropole s’inscrit dans la démarche « Normandie hydrogène » portée par la Région Normandie, qui vise à accélérer la transition énergétique normande et la décarbonation de l’économie et à constituer une filière industrielle d’avenir. En effet, la Normandie, région industrielle de premier plan, souhaite capitaliser sur ses potentiels (tissu industriel dense, projets fluviaux nombreux et forts enjeux de mobilité) afin d’être pionnière dans le développement de …

#### Fiche 26723 — 3.2.3 Etudier l'opportunité des énergies alternatives

- **Run 1 :** (aucun levier)
- **Run 2 :** Electricité renouvelable [4]
- **Run 3 :** Electricité renouvelable [4]
- **Prod :** (aucun levier)
- Leviers intermittents : Electricité renouvelable (2/3)

> Cette action vise à étudier les potentiels de production des types d'énergie renouvelable suivants, dans le but d'atteindre les objectifs de réduction des émissions de GES à l’horizon 2050 et accroître l’autonomie énergétique du territoire : - énergies marines (hydrolienne, marémotrice, osmotique, thermique) - hydroélectricité - pile à combustible - gazéification hydrothermale - pyrogazéification - géothermie.

#### Fiche 27277 — 4.1.2 Consolider la commercialisation des produits agricoles en circuits courts

- **Run 1 :** (aucun levier)
- **Run 2 :** Réduction des déplacements [4, 6]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Réduction des déplacements (1/3)

> L’objectif est de renforcer la capacité d’auto-approvisionnement du territoire et donc sa résilience alimentaire, ainsi que d’assurer l’accessibilité de produits agricoles durables et de qualité auprès du plus grand nombre. L'action se décompose en sous-actions : 1. Valoriser les circuits courts pour accompagner la distribution de produits locaux 2. Soutenir l'opportunité d'implantation d'outils filière (stockage, transformation, logistique) 3. Proposer un accompagnement à la restauration colle…

#### Fiche 27279 — 4.2.1 Améliorer la gestion globale de la protection de la ressource en eau

- **Run 1 :** (aucun levier)
- **Run 2 :** Changements de pratiques de fertilisation azotée [2, 3, 6] | Gestion des prairies [2, 3, 6]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Changements de pratiques de fertilisation azotée (1/3), Gestion des prairies (1/3)

> L'action vise à assurer le bon état qualitatif et quantitatif des ressources en eau pour l’approvisionnement en eau potable (et en eau industrielle), en améliorant la connaissance et le suivi. Elle se compose de 5 sous-actions, dont 3 fondamentales déjà en cours, qui seront complétées par les actions 4 et 5. Elles se dérouleront en parallèle. 1. Mise en œuvre et révision des Déclarations d’Utilité Publique liées aux captages d’eau a. Mise en œuvre des DUP b. Protection des périmètres de captage…

#### Fiche 37494 — Définition du plan d'actions de rénovation du patrimoine (selon DEET)

- **Run 1 :** Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 2 :** (aucun levier)
- **Run 3 :** Sobriété et isolation des bâtiments (tertiaire) [5]
- **Prod :** Sobriété et isolation des bâtiments (tertiaire) [4]
- Leviers intermittents : Sobriété et isolation des bâtiments (tertiaire) (2/3)

> Les bâtiments les plus énergivores seront identifiés en priorité et bénéficieront d'opérations ultérieures de rénovations énergétiques.

#### Fiche 37628 — Mise en œuvre de GEMINI

- **Run 1 :** Electricité renouvelable [5] | Véhicules électriques [5]
- **Run 2 :** (aucun levier)
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Electricité renouvelable (1/3), Véhicules électriques (1/3)

> Mise en place du projet permettant de suivre en temps réel (jumeau numérique) la production PV, les IRVE, la qualité de l'air, la qualité de l'eau, le MPGP grâce à la GED et l'IA, protocole BUS.

### Levier présent dans certains runs seulement (3)

#### Fiche 26093 — 2.1.1 Favoriser le recours aux transports en commun grâce à l'extension du réseau de tramway

- **Run 1 :** Véhicules électriques [1] | Vélo et transport en commun [1]
- **Run 2 :** Vélo et transport en commun [1]
- **Run 3 :** Vélo et transport en commun [1]
- **Prod :** Vélo et transport en commun [1]
- Leviers intermittents : Véhicules électriques (1/3)

> Le projet d’extension du réseau de tramway s’inscrit dans le Plan des Mobilités de la Communauté urbaine. Avec 14 km de voies supplémentaires, la nouvelle ligne de tramway permettra d’améliorer la desserte des quartiers prioritaires de la Ville ainsi que des pôles urbains de Harfleur et de Montivilliers bénéficiant actuellement d’une offre de desserte moins large. Le projet d’extension du réseau de tramway propose une ligne de transport 100% électrique, reprenant notamment une partie du tracé d…

#### Fiche 26109 — 2.2.1 Améliorer la performance énergétique de la flotte de véhicules de la Communauté urbaine (bus, parc automobile) et sensibiliser les agents à l'écoconduite

- **Run 1 :** Bus et cars décarbonés [5] | Véhicules électriques [5]
- **Run 2 :** Bus et cars décarbonés [5]
- **Run 3 :** Bus et cars décarbonés [5] | Véhicules électriques [5]
- **Prod :** Bus et cars décarbonés [5] | Efficacité et carburants décarbonés des véhicules privés [5] | Réduction des déplacements [5]
- Leviers intermittents : Véhicules électriques (2/3)

> Conformément à la directive (UE) 2019/1161 qui impose d'atteindre la part de 37,4% de véhicules à très faibles émissions au 1er janvier 2026, et à la loi d'orientation des mobilités qui fixe des objectifs en matière de renouvellement des parcs de véhicules lourds et légers par des véhicules propres et économes en énergie, la Communauté urbaine s'engage dans une amélioration continue de sa flotte de véhicules. L'action comporte également un volet interne de sensibilisation à la réduction des dép…

#### Fiche 27273 — 4.1.1 Agir en faveur des filières agricoles durables

- **Run 1 :** Changements de pratiques de fertilisation azotée [3, 6] | Elevage durable [3, 6] | Pratiques stockantes [3, 6]
- **Run 2 :** Changements de pratiques de fertilisation azotée [3, 6] | Elevage durable [3, 6]
- **Run 3 :** Changements de pratiques de fertilisation azotée [3, 6] | Elevage durable [3, 6] | Gestion des prairies [3, 6]
- **Prod :** (aucun levier)
- Leviers intermittents : Gestion des prairies (1/3), Pratiques stockantes (1/3)

> En 2020, la CU LHSM a engagé un travail prospectif visant à fixer les tendances à suivre à moyen et long terme en matière de transition agricole locale. Cette démarche conclut sur la nécessité de : - Diversifier massivement les productions (fruits, légumes, volailles, légumineuses…) ; - Pérenniser les systèmes d’élevage valorisant les ressources en herbe orientés vers les filières de qualité, plus résilients et autonomes ; - Développer les surfaces cultivées en agriculture biologique. Cette act…

### Levier intermittent et catégories instables (5)

#### Fiche 26728 — 3.3.3 Structurer la filière énergie et améliorer l'intégration des ENR&R au territoire

- **Run 1 :** Electricité renouvelable [6]
- **Run 2 :** Biogaz [4, 6] | Electricité renouvelable [4, 6] | Réseaux de chaleur décarbonés [4, 6]
- **Run 3 :** Electricité renouvelable [4, 6]
- **Prod :** (aucun levier)
- Leviers intermittents : Biogaz (1/3), Réseaux de chaleur décarbonés (1/3)
- Catégories instables sur : Electricité renouvelable

> Cette action vise à : - Faire connaître les énergies renouvelables au grand public afin d’améliorer l’acceptabilité indispensable à la mise en œuvre des projets - Former les jeunes du territoire aux énergies de demain afin d’en garantir la continuité et l’acceptabilité

#### Fiche 26729 — 3.3.4 Structurer les réseaux de transport et de distribution d'énergie pour participer à la résilience du territoire

- **Run 1 :** Electricité renouvelable [1, 2]
- **Run 2 :** Biogaz [2] | Electricité renouvelable [2]
- **Run 3 :** Electricité renouvelable [1, 4]
- **Prod :** (aucun levier)
- Leviers intermittents : Biogaz (1/3)
- Catégories instables sur : Electricité renouvelable

> L'ambition de la Communauté urbaine de quadrupler la production locale d'ENR&R sur le territoire entre 2019 et 2040 suppose une hausse de la quantité d’énergie injectée dans les réseaux de transport et de distribution de gaz et d’électricité du territoire. L’électrification des usages est également à prendre en compte pour le déploiement futur des réseaux. Cette action vise à anticiper les besoins en matière de transport et de distribution de l'énergie, en tenant compte des évolutions des usage…

#### Fiche 27356 — 5.2.1 Accompagner l’essor d’une démarche d’écologie industrielle et territoriale  (EIT) vers la transformation bas-carbone de l'industrie

- **Run 1 :** Biogaz [4, 6] | Production Industrielle [4, 6] | Prévention des déchets [4, 6] | Valorisation matière des déchets [4, 6]
- **Run 2 :** Production Industrielle [4, 6] | Prévention des déchets [4, 6] | Valorisation matière des déchets [4, 6]
- **Run 3 :** Biogaz [4, 6] | Production Industrielle [4, 6] | Prévention des déchets [4, 5, 6] | Valorisation matière des déchets [4, 5, 6]
- **Prod :** Production Industrielle [4, 6]
- Leviers intermittents : Biogaz (2/3)
- Catégories instables sur : Prévention des déchets, Valorisation matière des déchets

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="39deab80-929b-4e62-b362-e22588c0268b"><div class="bn-block" data-node-type="blockContainer" data-id="39deab80-929b-4e62-b362-e22588c0268b"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]">L’économie circulaire nous invite à interroger la notion de besoin, à transformer nos déchets en ressour…

#### Fiche 27357 — 5.3.1 Sensibiliser les acteurs à la réduction du volume de déchets à travers le déploiement du PLPDMA

- **Run 1 :** Prévention des déchets [6] | Valorisation matière des déchets [6]
- **Run 2 :** Prévention des déchets [6] | Valorisation matière des déchets [1, 6]
- **Run 3 :** Prévention des déchets [2, 6]
- **Prod :** Prévention des déchets [6]
- Leviers intermittents : Valorisation matière des déchets (2/3)
- Catégories instables sur : Prévention des déchets

> La réduction du volume de déchets produits permet de réduire la quantité d’ordures à traiter ainsi que d’optimiser la collecte. L’efficacité gagnée par ces deux leviers permet la réduction des émissions de GES du secteur. Si le problème se trouve principalement à la source, sur la production d’emballages en trop grande quantité et souvent non-recyclables, les évolutions comportementales des consommateurs permettent d’agir sur le volume produit. L'action vise à réduire le volume de déchets produ…

#### Fiche 27362 — 5.3.3 Mettre en place une politique globale de gestion des biodéchets sur le territoire

- **Run 1 :** Biogaz [1, 4] | Prévention des déchets [1, 4, 6] | Valorisation matière des déchets [1, 6]
- **Run 2 :** Biogaz [1] | Captage de méthane dans les ISDND [1] | Valorisation matière des déchets [1, 6]
- **Run 3 :** Biogaz [1] | Prévention des déchets [1, 2, 6] | Valorisation matière des déchets [1, 6]
- **Prod :** Prévention des déchets [1, 3, 6] | Valorisation matière des déchets [1, 3, 6]
- Leviers intermittents : Captage de méthane dans les ISDND (1/3), Prévention des déchets (2/3)
- Catégories instables sur : Biogaz

> L'action vise à : - Généraliser le tri à la source des biodéchets ; - Réduire les déchets et améliorer la valorisation organique ; - Extraire de la matière fermentescible contenue dans les bacs OMR (ordures ménagères résiduelles) ; - Réduire les déchets incinérés et limiter les impacts de la TGAP (Taxe générale sur les activités polluantes) sur la valorisation énergétique. Enjeu d’économie circulaire fort, par retour à la terre de la matière fermentescible ; - Possibilité de créer des énergies …

### Mêmes leviers, catégories différentes (16)

#### Fiche 26004 — 1.1.1 Accélérer la rénovation énergétique des logements privés

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [3, 4, 6] | Changement chaudières gaz + rénovation (résidentiel) [3, 4, 6] | Sobriété des bâtiments (résidentiel) [3, 4, 6]
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [3, 6] | Changement chaudières gaz + rénovation (résidentiel) [3, 6] | Sobriété des bâtiments (résidentiel) [3, 6]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [3, 4, 6] | Changement chaudières gaz + rénovation (résidentiel) [3, 4, 6] | Sobriété des bâtiments (résidentiel) [3, 4, 6]
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [3, 6] | Changement chaudières gaz + rénovation (résidentiel) [3, 6]
- Catégories instables sur : Changement chaudières fioul + rénovation (résidentiel), Changement chaudières gaz + rénovation (résidentiel), Sobriété des bâtiments (résidentiel)

> La CU participe à la rénovation du parc privé, en lien avec l’Agence Nationale de l’Habitat (l’ANAH) dans le cadre de la délégation des aides à la pierre de l’État en matière d’habitat privé. Cet accompagnement se fait notamment via l'Espace conseil rénovation, créée en 2016, guichet unique pour les demandes relatives à la rénovation de l'habitat privé et labellisé Espace France Rénov. La CU est également opérateur du Pacte Territorial, ainsi que des OPAH-RU du territoire pour les publics modes…

#### Fiche 26007 — 1.1.2 Accélérer la rénovation énergétique du parc de logements sociaux

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [3] | Changement chaudières gaz + rénovation (résidentiel) [3] | Sobriété des bâtiments (résidentiel) [3]
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [3] | Changement chaudières gaz + rénovation (résidentiel) [3] | Sobriété des bâtiments (résidentiel) [3]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [3, 4] | Changement chaudières gaz + rénovation (résidentiel) [3, 4] | Sobriété des bâtiments (résidentiel) [3, 4]
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [3] | Changement chaudières gaz + rénovation (résidentiel) [3]
- Catégories instables sur : Changement chaudières fioul + rénovation (résidentiel), Changement chaudières gaz + rénovation (résidentiel), Sobriété des bâtiments (résidentiel)

> Dans le cadre du programme d’action du Programme Local de l’Habitat (PLH) 2022-2027, et dans la perspective d’améliorer la qualité du parc social, la CU soutient les opérations menées par les bailleurs sociaux visant l’amélioration de la performance énergétique des logements et des bâtiments. Le parc locatif social compte un logement sur deux de plus de 40 ans, avec des performances énergétiques nécessitant des travaux de rénovation thermique (environ 15% du parc en étiquettes énergie E, F ou G…

#### Fiche 26107 — 2.1.3 Contribuer à l'évolution des usages en développant le covoiturage et l'autopartage

- **Run 1 :** Covoiturage [1]
- **Run 2 :** Covoiturage [1, 6]
- **Run 3 :** Covoiturage [1, 4]
- **Prod :** Covoiturage [1, 6]
- Catégories instables sur : Covoiturage

> Cette action vise à développer les pratiques de covoiturage et d’autopartage auprès de l’ensemble des citoyens du territoire. Le covoiturage doit être considéré comme un autre mode de transport collectif, pour répondre notamment aux déplacements domicile-travail. En cela, la Communauté urbaine ambitionne de mutualiser les déplacements automobiles individuels, permettant de réduire les émissions de GES, ou en tout cas de les contenir à mobilité croissante. Cela passe par : - le développement d'o…

#### Fiche 26115 — 2.2.2 Accélérer le déploiement des infrastructures de recharge pour véhicules électriques

- **Run 1 :** Véhicules électriques [1]
- **Run 2 :** Véhicules électriques [1, 6]
- **Run 3 :** Véhicules électriques [1, 6]
- **Prod :** Véhicules électriques [1, 3]
- Catégories instables sur : Véhicules électriques

> L'action vise à mettre en œuvre le schéma directeur des infrastructures de recharge pour véhicules électriques sur le territoire de la Communauté urbaine : - déploiement de bornes de recharge sur la voie publique - incitation des copropriétés à s'équiper d'infrastructures de recharge.

#### Fiche 26121 — 2.2.3 Encourager une logistique urbaine durable

- **Run 1 :** Efficacité et sobriété logistique [1, 4, 6] | Fret décarboné et multimodalité [1, 4, 6]
- **Run 2 :** Efficacité et sobriété logistique [4, 6] | Fret décarboné et multimodalité [1, 4, 6]
- **Run 3 :** Efficacité et sobriété logistique [4, 6] | Fret décarboné et multimodalité [4, 6]
- **Prod :** Efficacité et sobriété logistique [2, 6] | Fret décarboné et multimodalité [2, 6]
- Catégories instables sur : Efficacité et sobriété logistique, Fret décarboné et multimodalité

> La Communauté urbaine a lancé en 2023 l’étude Interlud (Innovations Territoriales et Logistique Urbaine Durable) dont les objectifs sont les suivants : • informer, sensibiliser et accompagner les collectivités et les opérateurs économiques à l’échelle territoriale sur les enjeux de la logistique urbaine ; • structurer les filières économiques et leurs représentations ; • favoriser la participation des acteurs privés dans le cadre des chartes logistiques urbaines et les faire dialoguer avec les …

#### Fiche 26703 — 3.1.2 Créer de nouveaux réseaux de chaleur urbains vertueux

- **Run 1 :** Réseaux de chaleur décarbonés [1]
- **Run 2 :** Réseaux de chaleur décarbonés [1]
- **Run 3 :** Réseaux de chaleur décarbonés [4]
- **Prod :** Réseaux de chaleur décarbonés [1, 2]
- Catégories instables sur : Réseaux de chaleur décarbonés

> La Communauté urbaine a pour objectif de développer les réseaux de chaleur sur son territoire. Ainsi un marché de prestations intellectuelles est en cours de rédaction afin de lancer des études de faisabilité de création de réseaux de chaleur sur quatre communes clairement identifiées : Saint-Romain de Colbosc, Criquetot l’Esneval, Montivilliers et Octeville-sur-Mer.

#### Fiche 26725 — 3.2.4 Réaliser une étude du gisement bois-énergie et gérer durablement la ressource biomasse

- **Run 1 :** Gestion des forêts et produits bois [4, 6]
- **Run 2 :** Gestion des forêts et produits bois [6]
- **Run 3 :** Gestion des forêts et produits bois [4, 6]
- **Prod :** (aucun levier)
- Catégories instables sur : Gestion des forêts et produits bois

> Cette action vise à étudier le gisement bois-énergie du territoire, actuellement fortement sollicité, dans le but de développer un approvisionnement local géré durablement. L’enjeu est de recréer une filière bois locale à la fois pour inciter les acteurs à gérer durablement la ressource existante mais aussi pour inciter à planter, pour un territoire plus résilient. Cette action se décompose en sous-actions : - Recenser les besoins en bois (créer un observatoire des projets, énergétiques ou non,…

#### Fiche 26727 — 3.3.2 Accélérer le développement de l'énergie photovoltaïque

- **Run 1 :** Electricité renouvelable [1, 3, 6]
- **Run 2 :** Electricité renouvelable [1, 3, 6]
- **Run 3 :** Electricité renouvelable [3, 4, 6]
- **Prod :** Electricité renouvelable [1, 2, 4, 6]
- Catégories instables sur : Electricité renouvelable

> Cette action vise à traduire de manière concrète l'objectif fixé dans le PCAET de production de 808 GWh via le photovoltaïque en 2040. Cela passe par : - la mise en oeuvre d'EUCF - le développement de projets avec la SEM ASER - l'accompagnement des communes dans leurs projets photovoltaïques - l'accompagnement des acteurs privés et publics - le développement d'un cadastre solaire - la numérisation des données et la mise en place d'un outil de comptabilisation des projets développés et de la pui…

#### Fiche 27318 — 4.3.1 Gérer durablement les réservoirs de biodiversité

- **Run 1 :** Gestion des haies [1, 3] | Pratiques stockantes [2, 3]
- **Run 2 :** Gestion des haies [1, 3, 4] | Pratiques stockantes [3, 4]
- **Run 3 :** Gestion des haies [1, 3, 4] | Pratiques stockantes [1, 3, 4]
- **Prod :** Gestion des forêts et produits bois [3, 4] | Gestion des haies [3, 4] | Sobriété foncière [2, 4]
- Catégories instables sur : Gestion des haies, Pratiques stockantes

> Cette action vise à renforcer la préservation et la séquestration du carbone par les puits naturels sur le territoire. Cela passe par les mesures suivantes : 1. Développer la plantation de haies sur le territoire a. Programme d’action « Opération Normandie Haie » b. Agir avec les partenaires sur la filière aval notamment en créant/accompagnant la filière de valorisation de l’entretien de la haie via le bois énergie. 2. Déployer Carbolocal, startup de territoire pour accélérer la transition écol…

#### Fiche 27319 — 4.3.2 Préserver les forêts et renforcer la séquestration carbone

- **Run 1 :** Gestion des forêts et produits bois [2, 3, 4] | Pratiques stockantes [2, 3]
- **Run 2 :** Gestion des forêts et produits bois [3, 4, 6] | Pratiques stockantes [3, 6]
- **Run 3 :** Gestion des forêts et produits bois [1, 3, 4] | Pratiques stockantes [1, 3, 4]
- **Prod :** Gestion des forêts et produits bois [2, 4, 6] | Gestion des haies [2, 4, 6] | Sobriété foncière [2, 4]
- Catégories instables sur : Gestion des forêts et produits bois, Pratiques stockantes

> Les forêts, marais, zones humides, estuaires, prairies, haies, mares, … constituent des espaces tampons et des obstacles face aux aléas climatiques. Ils sont des remparts naturels contre la montée des eaux, l’érosion des sols et du littoral ou encore la dégradation de la qualité de l’eau. Les actions de préservation et la restauration de ces écosystèmes sont donc cruciales pour augmenter la résilience des territoires face aux effets des changements climatiques. Ce sont en outre des alternatives…

#### Fiche 27360 — 5.3.2 Renforcer la collecte des objets et favoriser les pratiques de réparation, de réemploi et de lutte contre le gaspillage alimentaire

- **Run 1 :** Prévention des déchets [3, 6] | Valorisation matière des déchets [3, 6]
- **Run 2 :** Prévention des déchets [3, 4, 6] | Valorisation matière des déchets [3, 4, 6]
- **Run 3 :** Prévention des déchets [3, 6] | Valorisation matière des déchets [3, 6]
- **Prod :** Prévention des déchets [3, 4, 6]
- Catégories instables sur : Prévention des déchets, Valorisation matière des déchets

> Chaque habitant du territoire produit en moyenne près de 600 kilos de déchets par an. Malgré le nombre croissant de filières de recyclage, ne pas produire de déchets reste de loin la meilleure des solutions pour éviter tout gaspillage. La loi anti-gaspillage pour une économie circulaire (Agec) dont l’orientation vise à favoriser le réemploi de matériaux et objets. Elle prévoit notamment de « sortir du plastique jetable, mieux informer les consommateurs, lutter contre le gaspillage et pour le ré…

#### Fiche 37503 — Rénovation énergétique du gymnase de Saint-Romain de Colbosc

- **Run 1 :** Sobriété et isolation des bâtiments (tertiaire) [1]
- **Run 2 :** Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 3 :** Sobriété et isolation des bâtiments (tertiaire) [5]
- **Prod :** Sobriété et isolation des bâtiments (tertiaire) [5]
- Catégories instables sur : Sobriété et isolation des bâtiments (tertiaire)

> Rénovation de l'ancien gymnase (un nouvel équipement a été construit à proximité) Instance de gouvernance : présentation au Directeur DEMB

#### Fiche 37514 — Rénovation énergétique de la maison du territoire de Criquetot l'Esneval

- **Run 1 :** Sobriété et isolation des bâtiments (tertiaire) [1]
- **Run 2 :** Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 3 :** Sobriété et isolation des bâtiments (tertiaire) [5]
- **Prod :** Sobriété et isolation des bâtiments (tertiaire) [5]
- Catégories instables sur : Sobriété et isolation des bâtiments (tertiaire)

> isolation thermique, équipement de CVC, remplacement des menuiseries, etc. Instance de gouvernance : Présentation au Directeur DEMB

#### Fiche 37542 — Rénovation énergétique de logements communautaires

- **Run 1 :** Sobriété des bâtiments (résidentiel) [1]
- **Run 2 :** Sobriété des bâtiments (résidentiel) [1]
- **Run 3 :** Sobriété des bâtiments (résidentiel) [5]
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [5]
- Catégories instables sur : Sobriété des bâtiments (résidentiel)

> Rénovation énergétique de 3 logements rattachés à la DCE (Direction Cycle de l'Eau) : Radicatel, Saint-Laurent de Brèvedent et Conti

#### Fiche 37622 — Création de nouveaux réseaux de chaleur

- **Run 1 :** Réseaux de chaleur décarbonés [1]
- **Run 2 :** Réseaux de chaleur décarbonés [2]
- **Run 3 :** Réseaux de chaleur décarbonés [1]
- **Prod :** Réseaux de chaleur décarbonés [1]
- Catégories instables sur : Réseaux de chaleur décarbonés

> 2024 : études de faisabilité pour la création de RCU (Montivilliers, St Romain de Colbosc, Criquetot l’Esneval, Octeville) 2025 : études de faisabilités complémentaires (Harfleur, Gainneville, Angerville l’Orcher, Rolleville) Ressources étudiées : bois-énergie, solaire thermique, chaleur fatale. Instance de gouvernance : rencontres avec les élus des communes du territoire

#### Fiche 37623 — Développer des réseaux de chaleur communaux

- **Run 1 :** Réseaux de chaleur décarbonés [6]
- **Run 2 :** Réseaux de chaleur décarbonés [6]
- **Run 3 :** Réseaux de chaleur décarbonés [4, 6]
- **Prod :** Réseaux de chaleur décarbonés [4, 6]
- Catégories instables sur : Réseaux de chaleur décarbonés

> Sensibilisation des communes du territoire. Animation de la filière bois-énergie. Accompagnement des communes désireuses de créer un réseau de chaleur communal.

## CC du Pays des Achards (5300)

- Fiches : **103** — stables sur les 3 runs : **75** (73%), instables : **28**
- Paires levier × catégorie distinctes proposées : 148 — 3/3 runs : 65, 2/3 runs : 31, 1/3 runs : 52
- Vote majoritaire = prod : 16/46 fiches classées d'un côté ou de l'autre
- Réponses JSON invalides rejouées : 0
- Appels : 15 — tokens d'entrée 70 332 (dont 0 en cache, 0%), sortie 64 143 — coût estimé 0.18 $ pour les 3 runs
- Date : 2026-10-30 15:07

### Classée dans certains runs, aucun levier dans d'autres (3)

#### Fiche 23031 — 3.3 Sensibiliser les scolaires et le grand public sur les problématiques énergie-climat

- **Run 1 :** Prévention des déchets [6] | Sobriété des bâtiments (résidentiel) [6]
- **Run 2 :** (aucun levier)
- **Run 3 :** Prévention des déchets [6] | Réduction des déplacements [6] | Sobriété des bâtiments (résidentiel) [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Prévention des déchets (2/3), Réduction des déplacements (1/3), Sobriété des bâtiments (résidentiel) (2/3)

> La réussite d’un PCAET, et surtout de la mise en oeuvre de ses actions, repose pour une grande part sur l’animation et la mobilisation des acteurs du territoire. Pour la CC Pays des Achards, il est primordial de mettre en place un réseau de sensibilisation et d’échanges à destination du grand public et des scolaires, sur l’ensemble des thématiques portées par un PCAET. Il s’agit également par ce biais de valoriser les initiatives existantes et d’en impulser de nouvelles. Cela passe par l’organi…

#### Fiche 23043 — 6.3 Promouvoir la culture environnementale auprès des acteurs économiques

- **Run 1 :** (aucun levier)
- **Run 2 :** Production Industrielle [6] | Sobriété et isolation des bâtiments (tertiaire) [6]
- **Run 3 :** Production Industrielle [6] | Sobriété et isolation des bâtiments (tertiaire) [6]
- **Prod :** Changement de chaudière à fioul (tertiaire) [6] | Changement de chaudière à gaz (tertiaire) [6] | Sobriété et isolation des bâtiments (tertiaire) [6]
- Leviers intermittents : Production Industrielle (2/3), Sobriété et isolation des bâtiments (tertiaire) (2/3)

> Les filières économiques sont d’autant plus vulnérables aux enjeux énergie-climat que ces derniers impactent leur compétitivité. Dans le cadre du PCAET, la CCPA souhaite déployer un dispositif d’accompagnement au service de ses entreprises. En lien avec les partenaires (ORACE, CCI, CMA) un travail ciblé sur les entreprises les plus consommatrices (industriels) ainsi que sur le commerce de proximité sera engagé. Des actions de sensibilisation grand public seront également menées, dans le but d’i…

#### Fiche 85996 — FA 14 : Construire un Plan d'Actions commun en faveur des Mobilités Solidaires

- **Run 1 :** (aucun levier)
- **Run 2 :** Réduction des déplacements [2]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Réduction des déplacements (1/3)

### Levier présent dans certains runs seulement (6)

#### Fiche 23029 — 3.1 Maîtriser les consommations d’énergie sur le patrimoine et les transports

- **Run 1 :** Covoiturage [5] | Réduction des déplacements [5] | Sobriété et isolation des bâtiments (tertiaire) [5] | Véhicules électriques [5] | Vélo et transport en commun [5]
- **Run 2 :** Covoiturage [5] | Réduction des déplacements [5] | Sobriété et isolation des bâtiments (tertiaire) [5] | Véhicules électriques [5]
- **Run 3 :** Covoiturage [5] | Réduction des déplacements [5] | Sobriété et isolation des bâtiments (tertiaire) [5] | Véhicules électriques [5]
- **Prod :** Changement de chaudière à fioul (tertiaire) [5] | Changement de chaudière à gaz (tertiaire) [5] | Efficacité et carburants décarbonés des véhicules privés [5] | Sobriété et isolation des bâtiments (tertiaire) [5]
- Leviers intermittents : Vélo et transport en commun (1/3)

> Selon le Programme des Nations Unies pour l’Environnement (PNUE), 15% des émissions de GES sont directement issues des décisions prises par les collectivités territoriales, concernant leur patrimoine (bâtiment, éclairage public, flotte de véhicules) et leurs compétences (transports, déchets, etc). La collectivité a donc un rôle d’exemplarité. Pour les petites et moyennes communes, la dépense consacrée à l’énergie représente en moyenne 6% du budget de fonctionnement. La Communauté de communes so…

#### Fiche 80556 — Aménagements paysagers déchèterie des ACHARDS

- **Run 1 :** Gestion des haies [1] | Prévention des déchets [1]
- **Run 2 :** Gestion des haies [1] | Valorisation matière des déchets [1]
- **Run 3 :** Gestion des haies [1] | Prévention des déchets [1]
- **Prod :** Gestion des haies [1] | Valorisation matière des déchets [1]
- Leviers intermittents : Prévention des déchets (2/3), Valorisation matière des déchets (1/3)

> <p>Gestion différenciée sur les sites des déchèteries de la Communauté de Communes. Proposer des aménagements visuels (déchèterie vitrine) apportant des solutions concrètes de gestion des végétaux en local (fascines, haies tressées, plantations bocagères, hauteurs de tontes, paillage, pâturage...) </p>

#### Fiche 80557 — Formation des néo compostants

- **Run 1 :** Valorisation matière des déchets [6]
- **Run 2 :** Prévention des déchets [6]
- **Run 3 :** Prévention des déchets [6]
- **Prod :** Valorisation matière des déchets [6]
- Leviers intermittents : Prévention des déchets (2/3), Valorisation matière des déchets (1/3)

> <p>Formation proposée aux néo-compostants pour expliquer les bases du compostage</p> Éléments de calendrier : Information donnée lors des sessions de distribution de composteurs (modifications des modalités de retrait des composteurs individuels)

#### Fiche 80561 — Les ateliers conso'responsable

- **Run 1 :** Prévention des déchets [6] | Valorisation matière des déchets [6]
- **Run 2 :** Prévention des déchets [6] | Valorisation matière des déchets [6]
- **Run 3 :** Prévention des déchets [6]
- **Prod :** Prévention des déchets [6] | Valorisation matière des déchets [6]
- Leviers intermittents : Valorisation matière des déchets (2/3)

> <p>Programme d'ateliers à destination du public pour sensibiliser à la consommation responsable :</p><ul><li><p>Réparation</p></li><li><p>Achat de seconde main</p></li><li><p>Compostage</p></li></ul>

#### Fiche 80579 — Attractivité des locaux réemploi en déchèterie

- **Run 1 :** Prévention des déchets [1]
- **Run 2 :** Valorisation matière des déchets [1]
- **Run 3 :** Prévention des déchets [1]
- **Prod :** (aucun levier)
- Leviers intermittents : Prévention des déchets (2/3), Valorisation matière des déchets (1/3)

> <p>Optimiser le rangement et l'organisation des locaux réemploi pour favoriser le stockage et la récupération des objets.</p>

#### Fiche 85989 — FA 8 : Renforcer la communication mobilité et la notoriété des offres du bassin

- **Run 1 :** Covoiturage [6] | Vélo et transport en commun [6]
- **Run 2 :** Réduction des déplacements [6]
- **Run 3 :** Covoiturage [6] | Vélo et transport en commun [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Covoiturage (2/3), Réduction des déplacements (1/3), Vélo et transport en commun (2/3)

### Levier intermittent et catégories instables (10)

#### Fiche 23024 — 1.1 Inciter les professionnels du bâtiment à l’écoconstruction et à la mise en place d’ENR

- **Run 1 :** Prévention des déchets [4, 6] | Valorisation matière des déchets [4, 6]
- **Run 2 :** Valorisation matière des déchets [4, 6]
- **Run 3 :** Electricité renouvelable [4, 6] | Gestion des forêts et produits bois [4, 6] | Valorisation matière des déchets [1, 6]
- **Prod :** Electricité renouvelable [6] | Valorisation matière des déchets [6]
- Leviers intermittents : Electricité renouvelable (1/3), Gestion des forêts et produits bois (1/3), Prévention des déchets (1/3)
- Catégories instables sur : Valorisation matière des déchets

> Les filières économiques de la construction et de la rénovation sont assez développées sur le territoire de la CC Pays des Achards. Dans le cadre du PCAET, la CCPA souhaite développer les échanges avec les artisans et leur permettre de se former plus facilement, en lien avec la CAPEB, les chambres consulaires et organismes professionnels du secteur. Un travail ciblé sur les entreprises à intégrer sera à réaliser (artisans, promoteurs, producteurs d’éco-matériaux du territoire, …). L’objectif es…

#### Fiche 23025 — 1.2 Engager une rénovation énergétique de masse des logements existants

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [3, 4, 6] | Changement chaudières gaz + rénovation (résidentiel) [3, 4, 6] | Sobriété des bâtiments (résidentiel) [3, 4, 6]
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [3, 6] | Changement chaudières gaz + rénovation (résidentiel) [3, 6] | Sobriété des bâtiments (résidentiel) [3, 6]
- **Run 3 :** Sobriété des bâtiments (résidentiel) [3, 6]
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [3, 4, 6] | Changement chaudières gaz + rénovation (résidentiel) [3, 4, 6] | Sobriété des bâtiments (résidentiel) [3, 4, 6]
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (2/3), Changement chaudières gaz + rénovation (résidentiel) (2/3)
- Catégories instables sur : Sobriété des bâtiments (résidentiel)

> Le secteur résidentiel représente 32% des consommations du territoire. De nombreuses habitations se révèlent énergivores. La mise en place d’un guichet unique de l’habitat sur le Pays des Achards, animé à partir d’une Plateforme Territoriale de Rénovation Energétique de l’Habitat (PTREH) et d’une Opération Programmée d’Amélioration de l’Habitat (OPAH), permettra d’inciter techniquement et financièrement les propriétaires et bailleurs à la rénovation énergétique de leur patrimoine. La CCPA cherc…

#### Fiche 23026 — 1.3 Encourager la sobriété énergétique sur le bâti

- **Run 1 :** Changement de chaudière à fioul (tertiaire) [5] | Sobriété des bâtiments (résidentiel) [6]
- **Run 2 :** Changement de chaudière à fioul (tertiaire) [6] | Sobriété des bâtiments (résidentiel) [6] | Sobriété et isolation des bâtiments (tertiaire) [6]
- **Run 3 :** Changement de chaudière à fioul (tertiaire) [6] | Sobriété des bâtiments (résidentiel) [6]
- **Prod :** Changement de chaudière à fioul (tertiaire) [5] | Sobriété des bâtiments (résidentiel) [6]
- Leviers intermittents : Sobriété et isolation des bâtiments (tertiaire) (1/3)
- Catégories instables sur : Changement de chaudière à fioul (tertiaire)

> Les consommations d’énergie pour le chauffage des bâtiments à usage d’habitation et les bâtiments publics représentent une part prépondérante des consommations du territoire. La CC Pays des Achards souhaite développer un volet spécifique sur la performance des systèmes de chauffage. Pour les logements, cela passe par une incitation au remplacement des équipements de chauffage biomasse vétustes (foyers ouverts) par des installations plus efficaces en termes de consommation de bois et de combusti…

#### Fiche 23027 — 2.1 Encourager le développement opérationnel des énergies renouvelables

- **Run 1 :** Electricité renouvelable [4] | Gestion des forêts et produits bois [3, 4]
- **Run 2 :** Gestion des forêts et produits bois [4, 5]
- **Run 3 :** Electricité renouvelable [4] | Gestion des forêts et produits bois [4] | Réseaux de chaleur décarbonés [3]
- **Prod :** Gestion des forêts et produits bois [4, 6]
- Leviers intermittents : Electricité renouvelable (2/3), Réseaux de chaleur décarbonés (1/3)
- Catégories instables sur : Gestion des forêts et produits bois

> La CC Pays des Achards souhaite encourager le développement opérationnel des énergies renouvelables sur son territoire, qui présente des potentiels importants. Pour cela, deux axes de travail sont envisagés : améliorer la connaissance du potentiel de développement des ENR et encourager plus particulièrement le développement de la biomasse sur le territoire. Une étude sur le potentiel de développement des énergies renouvelables sur le territoire est en cours par le SyDEV. Le développement d’une …

#### Fiche 23033 — 4.1 Accompagner la mobilité alternative à la voiture individuelle

- **Run 1 :** Covoiturage [1, 6] | Réduction des déplacements [1, 4] | Vélo et transport en commun [1, 4]
- **Run 2 :** Covoiturage [1, 6] | Vélo et transport en commun [1, 6]
- **Run 3 :** Covoiturage [6] | Réduction des déplacements [6] | Vélo et transport en commun [6]
- **Prod :** Covoiturage [1, 6] | Vélo et transport en commun [1, 6]
- Leviers intermittents : Réduction des déplacements (2/3)
- Catégories instables sur : Covoiturage, Vélo et transport en commun

> Compte tenu de la part prépondérante des consommations d’énergie dans les transports, des nuisances que représentent le tout voiture en matière de pollution de l’air, de bruit, d’accidentologie, la mobilité apparaît comme un axe majeur sur lequel il faut agir. Elle l’est d’autant plus en milieu rural que certains publics (ainés, retraités, jeunes), peuvent se retrouver isolés et sans moyen de se déplacer ; et que l’augmentation des coûts des carburants et des normes sur les véhicules peuvent au…

#### Fiche 23035 — 4.3 Accompagner les entreprises et les acteurs du territoire vers une gestion optimisée de leurs déplacements

- **Run 1 :** Covoiturage [4] | Réduction des déplacements [1, 4]
- **Run 2 :** Réduction des déplacements [1, 4]
- **Run 3 :** Covoiturage [4, 6] | Réduction des déplacements [4, 6]
- **Prod :** Covoiturage [4, 6] | Réduction des déplacements [1, 4, 6]
- Leviers intermittents : Covoiturage (2/3)
- Catégories instables sur : Réduction des déplacements

> Afin de renforcer l’offre d’accompagnement aux entreprises en matière de mobilité, il est proposé de soutenir les démarches collectives entre entreprises en faveur de la mutualisation des déplacements, et de les accompagner dans la mise en place de Plans de Déplacement Inter-Entreprises (PDIE). Encourager la mise en place d’espaces de coworking et du télétravail permet également de réduire les déplacements et l’empreinte carbone des entreprises et de leurs salariés. DETAILS DE L'ACTION Développ…

#### Fiche 23037 — 5.2 Maintenir et développer la séquestration carbone

- **Run 1 :** Gestion des forêts et produits bois [3, 4] | Gestion des haies [4, 6]
- **Run 2 :** Gestion des forêts et produits bois [3, 4] | Gestion des haies [4, 6] | Gestion des prairies [4, 6] | Pratiques stockantes [4, 6]
- **Run 3 :** Gestion des forêts et produits bois [3, 4] | Gestion des haies [6] | Gestion des prairies [6]
- **Prod :** Gestion des forêts et produits bois [3, 4] | Gestion des haies [4, 6] | Gestion des prairies [4, 6]
- Leviers intermittents : Gestion des prairies (2/3), Pratiques stockantes (1/3)
- Catégories instables sur : Gestion des haies

> En France, entre 3 à 4 milliards de tonnes de carbone sont stockés tout juste sous nos pieds. La capacité de stockage du sol dépend de l’affectation qui lui a été donnée. Plus le sol se retrouve « artificialisé », plus sa capacité de stockage est réduite. La CCPA possède 95% de surface non artificialisée/imperméabilisée. De manière un peu contre-intuitive, pour que le bocage se maintienne, il faut le « couper » régulièrement : une haie qui n'est pas entretenue dépérit à terme. En dehors des enj…

#### Fiche 23040 — 5.5 Adapter l’agriculture aux changements climatiques

- **Run 1 :** Pratiques stockantes [4, 6]
- **Run 2 :** Gestion des prairies [4, 6] | Pratiques stockantes [4, 6]
- **Run 3 :** Pratiques stockantes [6] | Réduction des déplacements [6]
- **Prod :** Bâtiments & Machines agricoles [6] | Pratiques stockantes [6]
- Leviers intermittents : Gestion des prairies (1/3), Réduction des déplacements (1/3)
- Catégories instables sur : Pratiques stockantes

> L’identification des opportunités de développement économique du territoire conciliant réalités économiques et anticipation des impacts du changement climatique est indispensable pour le territoire de la CCPA, notamment pour le secteur agricole. La volonté de la CCPA est de faire évoluer les pratiques pour favoriser une agriculture locale et durable, tant d’un point de vue de la production que de la consommation. DETAILS DE L'ACTION Assurer le maintien d’une agriculture économe en eau : > Etabl…

#### Fiche 23042 — 6.2 Favoriser la croissance verte et les actions d’économie circulaire

- **Run 1 :** Prévention des déchets [1, 3, 4] | Valorisation matière des déchets [1, 4]
- **Run 2 :** Valorisation matière des déchets [1, 4]
- **Run 3 :** Prévention des déchets [6] | Valorisation matière des déchets [1, 6]
- **Prod :** Prévention des déchets [4, 5] | Valorisation matière des déchets [4, 5]
- Leviers intermittents : Prévention des déchets (2/3)
- Catégories instables sur : Valorisation matière des déchets

> L’économie circulaire a pour objectif de passer du modèle linéaire de production (extraire, produire, consommer, jeter), consommateur de ressources et générateur de déchets, à un cercle vertueux qui évite le gaspillage des ressources et leur extraction non respectueuse de l’environnement, optimise la longévité des produits et valorise les déchets. L’économie circulaire présente un double intérêt. Outre les bénéfices attendus par rapport à l’environnement, elle suppose de créer des synergies ent…

#### Fiche 85991 — FA 9 : Expérimenter des "maisons de la mobilité" sur le bassin

- **Run 1 :** Covoiturage [1, 6] | Vélo et transport en commun [1, 6]
- **Run 2 :** Vélo et transport en commun [1]
- **Run 3 :** Vélo et transport en commun [1, 6]
- **Prod :** Covoiturage [6] | Vélo et transport en commun [6]
- Leviers intermittents : Covoiturage (1/3)
- Catégories instables sur : Vélo et transport en commun

### Mêmes leviers, catégories différentes (9)

#### Fiche 23028 — 2.2 Accompagner le développement des projets d’énergie renouvelable

- **Run 1 :** Biogaz [3, 4, 6] | Electricité renouvelable [3, 4, 6]
- **Run 2 :** Biogaz [4, 6] | Electricité renouvelable [4, 6]
- **Run 3 :** Biogaz [4, 6] | Electricité renouvelable [4, 6]
- **Prod :** Biogaz [4, 6] | Electricité renouvelable [4, 6]
- Catégories instables sur : Biogaz, Electricité renouvelable

> Des projets d’énergie renouvelable sont à l’étude sur le territoire ; la CC Pays des Achards souhaite les soutenir et les valoriser dans leur mise en oeuvre. Sur le volet méthanisation, à partir de l’étude du potentiel méthanisable conduite par le SyDEV, l’intercommunalité souhaite, en partenariat avec la Chambre d’agriculture et GRDF, associer les agriculteurs du territoire et sensibiliser les habitants, pour favoriser l’acceptabilité et donc la réalisation des projets méthanisation. Sur le vo…

#### Fiche 23032 — 3.4 Lutter contre le gaspillage et promouvoir l’économie circulaire

- **Run 1 :** Prévention des déchets [1, 3, 6] | Valorisation matière des déchets [1, 3, 6]
- **Run 2 :** Prévention des déchets [3, 6] | Valorisation matière des déchets [1, 6]
- **Run 3 :** Prévention des déchets [3, 6] | Valorisation matière des déchets [1, 6]
- **Prod :** Prévention des déchets [3, 6] | Valorisation matière des déchets [1, 6]
- Catégories instables sur : Prévention des déchets, Valorisation matière des déchets

> La prévention des déchets consiste à mener des actions visant à éviter, réduire, voire retarder l'apparition d'un déchet, à limiter sa nocivité et faciliter son traitement. Pour inciter les usagers à un comportement vertueux, la collectivité poursuivra le travail engagé sur la redevance incitative, et mènera des actions pour : - éviter la production de déchets via une sensibilisation des publics au gaspillage, au réemploi des objets et à la réparation (recyclerie) - de réduire les volumes de dé…

#### Fiche 23036 — 5.1 Mettre en place une stratégie d'aménagement du territoire économe en foncier et en énergie

- **Run 1 :** Sobriété foncière [1, 2]
- **Run 2 :** Sobriété foncière [2]
- **Run 3 :** Sobriété foncière [2]
- **Prod :** Sobriété foncière [2, 6]
- Catégories instables sur : Sobriété foncière

> L’étalement urbain est fortement générateur d’émissions de Gaz à Effet de Serre (GES) et de polluants atmosphériques, en particulier dans les domaines des transports et du bâtiment. Consommateur de terres agricoles et d’espaces naturels, il génère également des coûts pour la collectivité (extension des réseaux et services collectifs). L’artificialisation des sols est également particulièrement impactante sur la biodiversité et le risque inondation, aggravant ainsi les impacts des changements cl…

#### Fiche 23041 — 6.1 Développer et maintenir les emplois et les services de proximité

- **Run 1 :** Réduction des déplacements [1, 6]
- **Run 2 :** Réduction des déplacements [1, 4]
- **Run 3 :** Réduction des déplacements [6]
- **Prod :** Réduction des déplacements [1, 6]
- Catégories instables sur : Réduction des déplacements

> L’objectif de la CCPA à travers cette action est de proposer à sa population des alternatives pour pouvoir consommer et travailler localement. Cette action aura également un fort impact en termes de réduction des petits trajets quotidiens. DETAILS DE L'ACTION Accompagner et maintenir les projets d’associations de commerçants pour proposer des commerces de proximité Développer les espaces de coworking (Cf. action 4.3) Éléments de calendrier : 2020-2021 : Développer les espaces de coworking (Cf. …

#### Fiche 80542 — Accompagner les habitants et les services publics

- **Run 1 :** Gestion des haies [6] | Prévention des déchets [6]
- **Run 2 :** Gestion des haies [6] | Prévention des déchets [6]
- **Run 3 :** Gestion des haies [1, 6] | Prévention des déchets [6]
- **Prod :** Gestion des haies [6] | Pratiques stockantes [6] | Valorisation matière des déchets [5, 6]
- Catégories instables sur : Gestion des haies

> <p>Accompagner des habitants et les pouvoirs publics dans une gestion plus raisonnée des espaces verts afin de diminuer les apports en déchèterie. Les produits issus de l'entretien des espaces constituent une RESSOURCE pour le sol et des pratiques adaptées permettent la réduction voire la suppression des apports en déchèterie :</p><p>-Gestion locale (mulching, broyage, paillage)</p><p>-Plantations bocagères (réflexion sur les aménagements, choix des essences)</p><p>-Formation continue sur les b…

#### Fiche 80578 — Evènement vide ta déchèt'

- **Run 1 :** Prévention des déchets [1, 6]
- **Run 2 :** Prévention des déchets [6]
- **Run 3 :** Prévention des déchets [6]
- **Prod :** Prévention des déchets [6]
- Catégories instables sur : Prévention des déchets

> <p>Favoriser le réemploi des objets en ouvrant un "vide grenier" en déchèterie avec les objets sauvés des bennes/ donner au local réemploi.</p>

#### Fiche 85731 — FA.01 : Développer un système covoituragesur le bassin

- **Run 1 :** Covoiturage [1, 6]
- **Run 2 :** Covoiturage [1, 4, 6]
- **Run 3 :** Covoiturage [1, 4, 6]
- **Prod :** Covoiturage [1, 4]
- Catégories instables sur : Covoiturage

> <p class="!text-base !text-grey-8 font-[Marianne]">VOLET COMMUNICATION : </p><p class="!text-base !text-grey-8 font-[Marianne]">• Bilan croisé des démarches d’animation : Aller plus loin collectivement par retour d’expérience, mutualisation d’actions : Cette action peut ensuite se raccrocher à une animation portée par un groupement d'EPCI : soit par la mutualisation du contrat avec un opérateur de covoiturage soit une animation par des agents, ETP mutualisé pour animer le lien avec les zones éc…

#### Fiche 85997 — FA 15 : Développer l'écosystème vélo sur le bassin

- **Run 1 :** Vélo et transport en commun [1, 6]
- **Run 2 :** Vélo et transport en commun [1]
- **Run 3 :** Vélo et transport en commun [1, 4, 6]
- **Prod :** Vélo et transport en commun [1]
- Catégories instables sur : Vélo et transport en commun

#### Fiche 88609 — Accompagnement des agents intercommunaux

- **Run 1 :** Prévention des déchets [5] | Valorisation matière des déchets [5]
- **Run 2 :** Prévention des déchets [5, 6] | Valorisation matière des déchets [5, 6]
- **Run 3 :** Prévention des déchets [5] | Valorisation matière des déchets [5]
- **Prod :** Prévention des déchets [5]
- Catégories instables sur : Prévention des déchets, Valorisation matière des déchets

> <p class="!text-base !text-grey-8 font-[Marianne]">Etablir un diagnostic des déchets au sein des structures publiques intercommunales. Accompagner les agents dans des changements de comportement en proposant des solutions de prévention déchets, amélioration qualité du tri, formation...</p>

## Paris Est Marne & Bois (5390)

- Fiches : **141** — stables sur les 3 runs : **85** (60%), instables : **56**
- Paires levier × catégorie distinctes proposées : 160 — 3/3 runs : 62, 2/3 runs : 37, 1/3 runs : 61
- Vote majoritaire = prod : 22/75 fiches classées d'un côté ou de l'autre
- Réponses JSON invalides rejouées : 0
- Appels : 18 — tokens d'entrée 33 795 (dont 0 en cache, 0%), sortie 109 107 — coût estimé 0.25 $ pour les 3 runs
- Date : 2026-10-30 15:07

### Classée dans certains runs, aucun levier dans d'autres (25)

#### Fiche 84849 — Créer un maillage de zones de ressourcement

- **Run 1 :** (aucun levier)
- **Run 2 :** Pratiques stockantes [1]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Pratiques stockantes (1/3)

> <ol><li><p>Études sur le gisement disponible de zones de ressourcement. </p></li><li><p>Aménagement de zones de ressourcement. </p></li><li><p>Information et communication sur ces zones.</p></li></ol>

#### Fiche 84864 — Etudier la réouverture et la renaturation des cours d'eau canalisés

- **Run 1 :** (aucun levier)
- **Run 2 :** (aucun levier)
- **Run 3 :** Pratiques stockantes [1]
- **Prod :** (aucun levier)
- Leviers intermittents : Pratiques stockantes (1/3)

#### Fiche 84867 — Contribuer à l'amélioration de la qualité écologique de la Marne et de ses affluents

- **Run 1 :** (aucun levier)
- **Run 2 :** (aucun levier)
- **Run 3 :** Pratiques stockantes [1]
- **Prod :** (aucun levier)
- Leviers intermittents : Pratiques stockantes (1/3)

> <ol><li><p>S’engager sur l’objectif baignade en 2022</p></li><li><p>Réaménagement des berges de la Marne en faveur de la biodiversité et du bien-être des populations</p></li></ol>

#### Fiche 84959 — Revégétaliser les berges de Marne

- **Run 1 :** (aucun levier)
- **Run 2 :** Pratiques stockantes [1]
- **Run 3 :** Pratiques stockantes [1]
- **Prod :** (aucun levier)
- Leviers intermittents : Pratiques stockantes (2/3)

#### Fiche 84962 — Créer un maillage de zones de biodiversité qui s'appuiera sur plusieurs mesures

- **Run 1 :** (aucun levier)
- **Run 2 :** Pratiques stockantes [1]
- **Run 3 :** Pratiques stockantes [1]
- **Prod :** (aucun levier)
- Leviers intermittents : Pratiques stockantes (2/3)

#### Fiche 84963 — Végétaliser les cours d'établissements scolaires, les parvis et autres espaces publics

- **Run 1 :** (aucun levier)
- **Run 2 :** Pratiques stockantes [1]
- **Run 3 :** Pratiques stockantes [1]
- **Prod :** (aucun levier)
- Leviers intermittents : Pratiques stockantes (2/3)

#### Fiche 84969 — Mobiliser les ressources immobilières inexploitées

- **Run 1 :** Sobriété foncière [2]
- **Run 2 :** Sobriété foncière [4]
- **Run 3 :** (aucun levier)
- **Prod :** Sobriété foncière [2]
- Leviers intermittents : Sobriété foncière (2/3)

#### Fiche 84972 — Encourager l'expérimentation dans les projets d'aménagement et de rénovation urbains

- **Run 1 :** (aucun levier)
- **Run 2 :** (aucun levier)
- **Run 3 :** Sobriété des bâtiments (résidentiel) [1]
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété des bâtiments (résidentiel) (1/3)

#### Fiche 84976 — Mettre en place un partenariat avec les agriculteurs de l'est Francilien

- **Run 1 :** (aucun levier)
- **Run 2 :** (aucun levier)
- **Run 3 :** Changements de pratiques de fertilisation azotée [4] | Elevage durable [4] | Pratiques stockantes [4]
- **Prod :** (aucun levier)
- Leviers intermittents : Changements de pratiques de fertilisation azotée (1/3), Elevage durable (1/3), Pratiques stockantes (1/3)

#### Fiche 85358 — Etudier la faisabilité d'un transport public fluvial

- **Run 1 :** (aucun levier)
- **Run 2 :** Vélo et transport en commun [4]
- **Run 3 :** Vélo et transport en commun [4]
- **Prod :** (aucun levier)
- Leviers intermittents : Vélo et transport en commun (2/3)

#### Fiche 85367 — Lancer officiellement la démarche d'élaboration du PLD

- **Run 1 :** (aucun levier)
- **Run 2 :** Réduction des déplacements [2]
- **Run 3 :** Réduction des déplacements [2]
- **Prod :** (aucun levier)
- Leviers intermittents : Réduction des déplacements (2/3)

#### Fiche 85368 — Réaliser les études nécessaires et rédiger le plan : Financement des études à 25% par IDFM et à 50% par la région IDF

- **Run 1 :** (aucun levier)
- **Run 2 :** Réduction des déplacements [2, 3]
- **Run 3 :** Réduction des déplacements [3]
- **Prod :** (aucun levier)
- Leviers intermittents : Réduction des déplacements (2/3)

#### Fiche 85371 — Participer à la consultation internationale sur le devenir des autoroutes du Grand Paris

- **Run 1 :** (aucun levier)
- **Run 2 :** Réduction des déplacements [4]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Réduction des déplacements (1/3)

#### Fiche 85373 — Réaliser une étude de faisabilité technique et financière des solutions proposées par les équipes internationales

- **Run 1 :** (aucun levier)
- **Run 2 :** Réduction des déplacements [4]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Réduction des déplacements (1/3)

#### Fiche 85672 — Structurer un réseau d'acteurs et co-porter la plateforme de lutte contre la précarité énergétique à l'échelle Territoriale

- **Run 1 :** Sobriété des bâtiments (résidentiel) [4]
- **Run 2 :** Sobriété des bâtiments (résidentiel) [4]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété des bâtiments (résidentiel) (2/3)

#### Fiche 85679 — Etudier le potentiel de développement des ENR&R sur le Territoire

- **Run 1 :** Biogaz [4] | Electricité renouvelable [4] | Réseaux de chaleur décarbonés [4]
- **Run 2 :** (aucun levier)
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Biogaz (1/3), Electricité renouvelable (1/3), Réseaux de chaleur décarbonés (1/3)

#### Fiche 85680 — Informer quant aux subventions disponibles pour l'installation d'ENR&R

- **Run 1 :** Biogaz [6] | Electricité renouvelable [6] | Réseaux de chaleur décarbonés [6]
- **Run 2 :** Biogaz [6] | Electricité renouvelable [6] | Réseaux de chaleur décarbonés [6]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Biogaz (2/3), Electricité renouvelable (2/3), Réseaux de chaleur décarbonés (2/3)

#### Fiche 85696 — Inciter à la réalisation d'actions de responsabilité sociétale des entreprises et de développement durable (PDE...)

- **Run 1 :** Réduction des déplacements [6]
- **Run 2 :** Réduction des déplacements [6]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Réduction des déplacements (2/3)

#### Fiche 85701 — Associer la population à la végétalisation de l'espace urbain

- **Run 1 :** (aucun levier)
- **Run 2 :** Pratiques stockantes [1, 6]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Pratiques stockantes (1/3)

#### Fiche 85710 — Sensibilisation au gaspillage alimentaire dans les établissements scolaires

- **Run 1 :** (aucun levier)
- **Run 2 :** Prévention des déchets [6]
- **Run 3 :** Prévention des déchets [6]
- **Prod :** Prévention des déchets [6]
- Leviers intermittents : Prévention des déchets (2/3)

#### Fiche 85717 — Formaliser une politique d'achats durables pour le Territoire

- **Run 1 :** (aucun levier)
- **Run 2 :** Prévention des déchets [5]
- **Run 3 :** Prévention des déchets [5]
- **Prod :** (aucun levier)
- Leviers intermittents : Prévention des déchets (2/3)

#### Fiche 85721 — Formation des agents à l'éco-conduite

- **Run 1 :** (aucun levier)
- **Run 2 :** Efficacité et carburants décarbonés des véhicules privés [5]
- **Run 3 :** (aucun levier)
- **Prod :** Efficacité et carburants décarbonés des véhicules privés [5]
- Leviers intermittents : Efficacité et carburants décarbonés des véhicules privés (1/3)

#### Fiche 85724 — Réaliser un plan de mobilité pour l'administration PEMB

- **Run 1 :** Réduction des déplacements [5]
- **Run 2 :** Réduction des déplacements [5]
- **Run 3 :** (aucun levier)
- **Prod :** Réduction des déplacements [5]
- Leviers intermittents : Réduction des déplacements (2/3)

#### Fiche 120929 — 4-1 Encadrer les activités humaines au sein des zones d'importance pour la biodiversité

- **Run 1 :** (aucun levier)
- **Run 2 :** (aucun levier)
- **Run 3 :** Sobriété foncière [2]
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété foncière (1/3)

#### Fiche 120937 — 5-2 Rédiger une charte de l'arbre

- **Run 1 :** Pratiques stockantes [2]
- **Run 2 :** (aucun levier)
- **Run 3 :** Pratiques stockantes [2]
- **Prod :** (aucun levier)
- Leviers intermittents : Pratiques stockantes (2/3)

### Levier présent dans certains runs seulement (16)

#### Fiche 84960 — Sauvegarder la Pleine Terre et restaurer les services écosystémiques des sols

- **Run 1 :** Sobriété foncière [2]
- **Run 2 :** Pratiques stockantes [1]
- **Run 3 :** Pratiques stockantes [1]
- **Prod :** Sobriété foncière [2]
- Leviers intermittents : Pratiques stockantes (2/3), Sobriété foncière (1/3)

#### Fiche 84973 — Gérer et valoriser localement les terres et autres matériaux de déconstruction dans les projets d'aménagement

- **Run 1 :** Valorisation matière des déchets [1]
- **Run 2 :** Prévention des déchets [1] | Valorisation matière des déchets [1]
- **Run 3 :** Valorisation matière des déchets [1]
- **Prod :** Prévention des déchets [1, 2]
- Leviers intermittents : Prévention des déchets (1/3)

#### Fiche 85345 — Proposer des solutions de stationnement favorisant les mobilités partagées

- **Run 1 :** Covoiturage [1]
- **Run 2 :** Covoiturage [1]
- **Run 3 :** Covoiturage [1] | Vélo et transport en commun [1]
- **Prod :** Covoiturage [1]
- Leviers intermittents : Vélo et transport en commun (1/3)

#### Fiche 85346 — Informer et communiquer sur les subventions existantes pour l'achat de véhicules propres

- **Run 1 :** Efficacité et carburants décarbonés des véhicules privés [6]
- **Run 2 :** Efficacité et carburants décarbonés des véhicules privés [6] | Véhicules électriques [6]
- **Run 3 :** Véhicules électriques [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Efficacité et carburants décarbonés des véhicules privés (2/3), Véhicules électriques (2/3)

#### Fiche 85347 — Augmenter le nombre de points de ravitaillement pour les véhicules propres

- **Run 1 :** Efficacité et carburants décarbonés des véhicules privés [1] | Véhicules électriques [1]
- **Run 2 :** Efficacité et carburants décarbonés des véhicules privés [1] | Véhicules électriques [1]
- **Run 3 :** Véhicules électriques [1]
- **Prod :** Véhicules électriques [1]
- Leviers intermittents : Efficacité et carburants décarbonés des véhicules privés (2/3)

#### Fiche 85348 — Définir une stratégie de déploiement de stations GNV et Bio GNV

- **Run 1 :** Efficacité et carburants décarbonés des véhicules privés [4]
- **Run 2 :** Biogaz [4] | Efficacité et carburants décarbonés des véhicules privés [4]
- **Run 3 :** Efficacité et carburants décarbonés des véhicules privés [4]
- **Prod :** (aucun levier)
- Leviers intermittents : Biogaz (1/3)

#### Fiche 85354 — Coopérer avec les autorités organisatrices de transport

- **Run 1 :** Bus et cars décarbonés [4] | Vélo et transport en commun [4]
- **Run 2 :** Vélo et transport en commun [4]
- **Run 3 :** Vélo et transport en commun [4]
- **Prod :** (aucun levier)
- Leviers intermittents : Bus et cars décarbonés (1/3)

#### Fiche 85357 — Développer et étendre les transports existants sur la Marne

- **Run 1 :** Fret décarboné et multimodalité [1]
- **Run 2 :** Fret décarboné et multimodalité [1] | Vélo et transport en commun [1]
- **Run 3 :** Fret décarboné et multimodalité [1] | Vélo et transport en commun [1]
- **Prod :** Vélo et transport en commun [1]
- Leviers intermittents : Vélo et transport en commun (2/3)

#### Fiche 85359 — Sensibiliser les professionnels du Territoire aux enjeu de la gestion du dernier kilomètre

- **Run 1 :** Efficacité et sobriété logistique [6]
- **Run 2 :** Efficacité et sobriété logistique [6] | Fret décarboné et multimodalité [6]
- **Run 3 :** Efficacité et sobriété logistique [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Fret décarboné et multimodalité (1/3)

#### Fiche 85369 — Adopter le PLD en conseil de Territoire

- **Run 1 :** Réduction des déplacements [2] | Vélo et transport en commun [2]
- **Run 2 :** Réduction des déplacements [2]
- **Run 3 :** Réduction des déplacements [2]
- **Prod :** Bus et cars décarbonés [2] | Covoiturage [2] | Réduction des déplacements [2] | Vélo et transport en commun [2]
- Leviers intermittents : Vélo et transport en commun (1/3)

#### Fiche 85678 — Construire des stratégies partenariales pour les ENR&R

- **Run 1 :** Biogaz [4] | Electricité renouvelable [4] | Réseaux de chaleur décarbonés [4]
- **Run 2 :** Biogaz [4] | Electricité renouvelable [4]
- **Run 3 :** Biogaz [4] | Electricité renouvelable [4] | Réseaux de chaleur décarbonés [4]
- **Prod :** (aucun levier)
- Leviers intermittents : Réseaux de chaleur décarbonés (2/3)

#### Fiche 85681 — Proposer des quotas ENR&R dans les opérations d'aménagement

- **Run 1 :** Biogaz [2] | Electricité renouvelable [2] | Réseaux de chaleur décarbonés [2]
- **Run 2 :** Biogaz [2] | Electricité renouvelable [2] | Réseaux de chaleur décarbonés [2]
- **Run 3 :** Electricité renouvelable [2] | Réseaux de chaleur décarbonés [2]
- **Prod :** Electricité renouvelable [2]
- Leviers intermittents : Biogaz (2/3)

#### Fiche 85686 — Optimiser et valoriser la collecte des biodéchets

- **Run 1 :** Valorisation matière des déchets [1]
- **Run 2 :** Biogaz [1] | Valorisation matière des déchets [1]
- **Run 3 :** Valorisation matière des déchets [1]
- **Prod :** Valorisation matière des déchets [1]
- Leviers intermittents : Biogaz (1/3)

#### Fiche 85689 — Structurer un réseau vertueux d'économie circulaire animé par PEMB

- **Run 1 :** Valorisation matière des déchets [4]
- **Run 2 :** Valorisation matière des déchets [4]
- **Run 3 :** Prévention des déchets [4] | Valorisation matière des déchets [4]
- **Prod :** Prévention des déchets [4]
- Leviers intermittents : Prévention des déchets (1/3)

#### Fiche 85690 — Valoriser les terres issues des travaux du Grand Paris Express

- **Run 1 :** Valorisation matière des déchets [4]
- **Run 2 :** Valorisation matière des déchets [1]
- **Run 3 :** Prévention des déchets [4]
- **Prod :** (aucun levier)
- Leviers intermittents : Prévention des déchets (1/3), Valorisation matière des déchets (2/3)

#### Fiche 120941 — 6-2 En bords de Marne, fermer une voie de shunt (sous un pont) et réaliser des opérations de désimperméabilisation (exemple Pont du Petit Parc)

- **Run 1 :** Pratiques stockantes [1] | Réduction des déplacements [1]
- **Run 2 :** Pratiques stockantes [1] | Réduction des déplacements [2]
- **Run 3 :** Pratiques stockantes [1] | Vélo et transport en commun [1]
- **Prod :** Sobriété foncière [1]
- Leviers intermittents : Réduction des déplacements (2/3), Vélo et transport en commun (1/3)

### Levier intermittent et catégories instables (7)

#### Fiche 84975 — Favorisant l'agriculture urbaine durable

- **Run 1 :** Changements de pratiques de fertilisation azotée [1] | Pratiques stockantes [1]
- **Run 2 :** Pratiques stockantes [4]
- **Run 3 :** Pratiques stockantes [6]
- **Prod :** Pratiques stockantes [6]
- Leviers intermittents : Changements de pratiques de fertilisation azotée (1/3)
- Catégories instables sur : Pratiques stockantes

#### Fiche 84981 — Lancer et soutenir les pratiques en faveur de la ville-nature

- **Run 1 :** Pratiques stockantes [1, 6]
- **Run 2 :** Gestion des forêts et produits bois [1] | Pratiques stockantes [1]
- **Run 3 :** Gestion des haies [1] | Pratiques stockantes [1]
- **Prod :** (aucun levier)
- Leviers intermittents : Gestion des forêts et produits bois (1/3), Gestion des haies (1/3)
- Catégories instables sur : Pratiques stockantes

#### Fiche 85344 — Créer une plateforme Territoriale de mobilités partagées

- **Run 1 :** Covoiturage [1] | Réduction des déplacements [1]
- **Run 2 :** Covoiturage [1, 4]
- **Run 3 :** Covoiturage [4] | Vélo et transport en commun [4]
- **Prod :** Covoiturage [1]
- Leviers intermittents : Réduction des déplacements (1/3), Vélo et transport en commun (1/3)
- Catégories instables sur : Covoiturage

#### Fiche 85351 — Soutenir les initiatives territoriales en faveur des modes actifs

- **Run 1 :** Réduction des déplacements [4] | Vélo et transport en commun [4]
- **Run 2 :** Vélo et transport en commun [4]
- **Run 3 :** Vélo et transport en commun [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Réduction des déplacements (1/3)
- Catégories instables sur : Vélo et transport en commun

#### Fiche 85370 — Mettre en œuvre le plan sur 5 années

- **Run 1 :** Réduction des déplacements [1, 2] | Vélo et transport en commun [1, 2]
- **Run 2 :** Réduction des déplacements [4]
- **Run 3 :** Covoiturage [2] | Réduction des déplacements [2] | Vélo et transport en commun [2]
- **Prod :** Bus et cars décarbonés [2] | Covoiturage [2] | Réduction des déplacements [2] | Vélo et transport en commun [2]
- Leviers intermittents : Covoiturage (1/3), Vélo et transport en commun (2/3)
- Catégories instables sur : Réduction des déplacements

#### Fiche 85377 — Impliquer davantage les professionnels du cadre bâti dans la rénovation énergétique

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [4, 6] | Changement chaudières gaz + rénovation (résidentiel) [4, 6] | Sobriété des bâtiments (résidentiel) [4, 6]
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6] | Sobriété des bâtiments (résidentiel) [6]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6] | Changement de chaudière à fioul (tertiaire) [6] | Changement de chaudière à gaz (tertiaire) [6] | Sobriété des bâtiments (résidentiel) [6] | Sobriété et isolation des bâtiments (tertiaire) [6]
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6] | Sobriété des bâtiments (résidentiel) [6]
- Leviers intermittents : Changement de chaudière à fioul (tertiaire) (1/3), Changement de chaudière à gaz (tertiaire) (1/3), Sobriété et isolation des bâtiments (tertiaire) (1/3)
- Catégories instables sur : Changement chaudières fioul + rénovation (résidentiel), Changement chaudières gaz + rénovation (résidentiel), Sobriété des bâtiments (résidentiel)

#### Fiche 120930 — 4-2 Fermer les bords de Marne à la circulation routière (cohérence intercommunale et augmentation des périodes de fermeture)

- **Run 1 :** Réduction des déplacements [1]
- **Run 2 :** Réduction des déplacements [2]
- **Run 3 :** Réduction des déplacements [1] | Vélo et transport en commun [1]
- **Prod :** Réduction des déplacements [2]
- Leviers intermittents : Vélo et transport en commun (1/3)
- Catégories instables sur : Réduction des déplacements

### Mêmes leviers, catégories différentes (8)

#### Fiche 85355 — Etudier des solutions de stationnement qui faciliteraient l'intermodalité

- **Run 1 :** Vélo et transport en commun [1]
- **Run 2 :** Vélo et transport en commun [4]
- **Run 3 :** Vélo et transport en commun [4]
- **Prod :** (aucun levier)
- Catégories instables sur : Vélo et transport en commun

#### Fiche 85374 — Adhérer à l'Agence Locale de l'Energie et du Climat - MVE pour permettre aux habitants d'accéder au service public de la performance énergétique de l'habitat

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [4, 6] | Changement chaudières gaz + rénovation (résidentiel) [4, 6] | Sobriété des bâtiments (résidentiel) [4, 6]
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [4, 6] | Changement chaudières gaz + rénovation (résidentiel) [4, 6] | Sobriété des bâtiments (résidentiel) [4, 6]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6] | Sobriété des bâtiments (résidentiel) [6]
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [4, 6] | Changement chaudières gaz + rénovation (résidentiel) [4, 6] | Sobriété des bâtiments (résidentiel) [4, 6]
- Catégories instables sur : Changement chaudières fioul + rénovation (résidentiel), Changement chaudières gaz + rénovation (résidentiel), Sobriété des bâtiments (résidentiel)

#### Fiche 85379 — Renforcer l'efficacité énergétique des bâtiments dans le parc social

- **Run 1 :** Sobriété des bâtiments (résidentiel) [1]
- **Run 2 :** Sobriété des bâtiments (résidentiel) [5]
- **Run 3 :** Sobriété des bâtiments (résidentiel) [1]
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [3]
- Catégories instables sur : Sobriété des bâtiments (résidentiel)

#### Fiche 85671 — Concevoir une plate-forme territoriale pour repérer et accompagner les ménages en situation de précarité énergétique

- **Run 1 :** Sobriété des bâtiments (résidentiel) [4, 6]
- **Run 2 :** Sobriété des bâtiments (résidentiel) [4]
- **Run 3 :** Sobriété des bâtiments (résidentiel) [6]
- **Prod :** (aucun levier)
- Catégories instables sur : Sobriété des bâtiments (résidentiel)

#### Fiche 85674 — Identifier les aides mobilisables pour le développement des réseaux de chaleur

- **Run 1 :** Réseaux de chaleur décarbonés [3, 6]
- **Run 2 :** Réseaux de chaleur décarbonés [3]
- **Run 3 :** Réseaux de chaleur décarbonés [3]
- **Prod :** (aucun levier)
- Catégories instables sur : Réseaux de chaleur décarbonés

#### Fiche 85675 — Encourager le raccordement aux réseaux de chaleur existants

- **Run 1 :** Réseaux de chaleur décarbonés [1, 6]
- **Run 2 :** Réseaux de chaleur décarbonés [6]
- **Run 3 :** Réseaux de chaleur décarbonés [6]
- **Prod :** Réseaux de chaleur décarbonés [6]
- Catégories instables sur : Réseaux de chaleur décarbonés

#### Fiche 85682 — Développer le compost individuel sur le Territoire

- **Run 1 :** Valorisation matière des déchets [1, 6]
- **Run 2 :** Valorisation matière des déchets [1]
- **Run 3 :** Valorisation matière des déchets [1, 6]
- **Prod :** Valorisation matière des déchets [1, 6]
- Catégories instables sur : Valorisation matière des déchets

#### Fiche 85699 — Création d'un réseau de tiers-lieux coopératifs pour favoriser la création d'activités locales et de start-up

- **Run 1 :** Réduction des déplacements [1]
- **Run 2 :** Réduction des déplacements [1, 4]
- **Run 3 :** Réduction des déplacements [1, 4]
- **Prod :** Réduction des déplacements [1]
- Catégories instables sur : Réduction des déplacements

## SM du SCoT Sambre Avesnois (6030)

- Fiches : **73** — stables sur les 3 runs : **28** (38%), instables : **45**
- Paires levier × catégorie distinctes proposées : 176 — 3/3 runs : 56, 2/3 runs : 38, 1/3 runs : 82
- Vote majoritaire = prod : 6/53 fiches classées d'un côté ou de l'autre
- Réponses JSON invalides rejouées : 0
- Appels : 9 — tokens d'entrée 50 394 (dont 0 en cache, 0%), sortie 65 421 — coût estimé 0.17 $ pour les 3 runs
- Date : 2026-10-30 15:07

### Classée dans certains runs, aucun levier dans d'autres (13)

#### Fiche 126656 — 1.1.1. Mettre en œuvre le Programme Local de l'Habitat 2025-2030

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [2] | Changement chaudières gaz + rénovation (résidentiel) [2] | Sobriété des bâtiments (résidentiel) [2]
- **Run 2 :** (aucun levier)
- **Run 3 :** Sobriété des bâtiments (résidentiel) [2]
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [2] | Changement chaudières gaz + rénovation (résidentiel) [2]
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (1/3), Changement chaudières gaz + rénovation (résidentiel) (1/3), Sobriété des bâtiments (résidentiel) (2/3)

> Elaboré pour 6 ans, le PLH est un document réglementaire définissant la stratégie et les actions à mener dans le cadre de la politique de l’habitat. Le PLH porte des objectifs ambitieux sur les thématiques de rénovation et de lutte contre la précarité énergétique.

#### Fiche 126657 — 1.1.2. Mise en œuvre du POA Habitat (PLUi-H), incluant la lutte contre la précarité énergétique, l'adaptation de l'offre, … (2023-2029)

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [2] | Changement chaudières gaz + rénovation (résidentiel) [2] | Sobriété des bâtiments (résidentiel) [2]
- **Run 2 :** (aucun levier)
- **Run 3 :** Sobriété des bâtiments (résidentiel) [2]
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [2] | Changement chaudières gaz + rénovation (résidentiel) [2]
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (1/3), Changement chaudières gaz + rénovation (résidentiel) (1/3), Sobriété des bâtiments (résidentiel) (2/3)

> La CC Cœur de l'Avesnois a souhaité intégrer des dispositions habitat au sein de son PLUi tenant lieu de Programme Local pour l’Habitat (PLH) à travers la rédaction d’un Programme d’Orientations et d’Actions Habitat. Elaboré pour 6 ans, le PLH est un document réglementaire définissant la stratégie et les actions à mener dans le cadre de la politique de l’habitat. Le POA Habitat de la CC Cœur de l'Avesnois porte des objectifs ambitieux sur les questions de lutte contre la vacance, contre l’insal…

#### Fiche 126661 — 1.3.1. Accompagner le développement des quartiers résilients

- **Run 1 :** (aucun levier)
- **Run 2 :** Pratiques stockantes [1]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Pratiques stockantes (1/3)

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="6f2571c1-4bd5-40d9-97cc-04faf78c38f4"><div class="bn-block" data-node-type="blockContainer" data-id="6f2571c1-4bd5-40d9-97cc-04faf78c38f4"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]">Dans un contexte de réchauffement climatique et de dérèglement météorologique, l'adaptation des villes d…

#### Fiche 126663 — 1.4.1. Former les professionnels des métiers du bâtiment et les porteurs de projets aux dernières règles thermiques et aux éco-matériaux

- **Run 1 :** Sobriété des bâtiments (résidentiel) [6] | Sobriété et isolation des bâtiments (tertiaire) [6]
- **Run 2 :** (aucun levier)
- **Run 3 :** Sobriété des bâtiments (résidentiel) [6] | Sobriété et isolation des bâtiments (tertiaire) [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété des bâtiments (résidentiel) (2/3), Sobriété et isolation des bâtiments (tertiaire) (2/3)

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="c40bce75-53f2-4731-9856-50ae89fb20f5"><div class="bn-block" data-node-type="blockContainer" data-id="c40bce75-53f2-4731-9856-50ae89fb20f5"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]">Les éco-matériaux sont des matériaux de construction respectueux de l'environnement, conçus pour minimis…

#### Fiche 126664 — 1.4.2. Promouvoir les rénovations et constructions vertueuses

- **Run 1 :** Sobriété des bâtiments (résidentiel) [6] | Sobriété et isolation des bâtiments (tertiaire) [6]
- **Run 2 :** (aucun levier)
- **Run 3 :** Sobriété des bâtiments (résidentiel) [6] | Sobriété et isolation des bâtiments (tertiaire) [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété des bâtiments (résidentiel) (2/3), Sobriété et isolation des bâtiments (tertiaire) (2/3)

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="a217bbb3-d1c9-4ad3-becd-a61fcda80536"><div class="bn-block" data-node-type="blockContainer" data-id="a217bbb3-d1c9-4ad3-becd-a61fcda80536"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]">Un projet à forte ambition environnemental comprend notamment l'utilisation d'éco-matériaux, la mise en …

#### Fiche 126666 — 2.1.1. Renforcer l’ingénierie et l’assistance conseil en énergies au travers de la SIRPP Sambre-Avesnois

- **Run 1 :** Changement de chaudière à fioul (tertiaire) [6] | Changement de chaudière à gaz (tertiaire) [6] | Electricité renouvelable [6] | Sobriété et isolation des bâtiments (tertiaire) [6]
- **Run 2 :** (aucun levier)
- **Run 3 :** Electricité renouvelable [4] | Sobriété et isolation des bâtiments (tertiaire) [4]
- **Prod :** Electricité renouvelable [5] | Sobriété et isolation des bâtiments (tertiaire) [5]
- Leviers intermittents : Changement de chaudière à fioul (tertiaire) (1/3), Changement de chaudière à gaz (tertiaire) (1/3), Electricité renouvelable (2/3), Sobriété et isolation des bâtiments (tertiaire) (2/3)

> La Stratégie d’Intervention et de Réhabilitation du patrimoine Public (SIRPP) Sambre-Avesnois met à disposition auprès des communes du territoire des conseillers en énergies partagés (CEP) depuis 2019. Ils accompagnent le suivi des consommations, réalisent des prédiagnostics et assurent le montage de projets de rénovation ou de déploiement des énergies renouvelables au sein des communes. La SIRPP est co-animée par le PNR de l’Avesnois et l’ADU.

#### Fiche 126675 — 3.1.1. Ecrire une stratégie partagée à l'échelle de l'arrondissement

- **Run 1 :** Covoiturage [4] | Réduction des déplacements [4] | Vélo et transport en commun [4]
- **Run 2 :** (aucun levier)
- **Run 3 :** Réduction des déplacements [2] | Vélo et transport en commun [2]
- **Prod :** Covoiturage [4] | Vélo et transport en commun [4]
- Leviers intermittents : Covoiturage (1/3), Réduction des déplacements (2/3), Vélo et transport en commun (2/3)

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="d621758c-9e86-4894-bac1-10cd01b5bc5a"><div class="bn-block" data-node-type="blockContainer" data-id="d621758c-9e86-4894-bac1-10cd01b5bc5a"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]">Historiquement centré sur les transports urbain, Sambre-Mobilités (ex SMTUS) agit désormais en tant qu’A…

#### Fiche 126676 — 3.1.2. Accompagner la mise en œuvre de plans de mobilité intercommunaux

- **Run 1 :** Réduction des déplacements [6]
- **Run 2 :** (aucun levier)
- **Run 3 :** Réduction des déplacements [2] | Vélo et transport en commun [2]
- **Prod :** (aucun levier)
- Leviers intermittents : Réduction des déplacements (2/3), Vélo et transport en commun (1/3)

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="efe16c93-87da-41ad-bd77-d3ed165004f8"><div class="bn-block" data-node-type="blockContainer" data-id="efe16c93-87da-41ad-bd77-d3ed165004f8"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]">Le Plan de Déplacements Urbains (PDU) est un outil de planification qui a été créé par la Loi d’Orientat…

#### Fiche 126698 — 5.2.1. Identifier et soutenir les filières  de matières premières existantes sur le territoire

- **Run 1 :** Efficacité et sobriété logistique [4, 6]
- **Run 2 :** Efficacité et sobriété logistique [3, 4, 6] | Fret décarboné et multimodalité [3, 4, 6]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Efficacité et sobriété logistique (2/3), Fret décarboné et multimodalité (1/3)

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="8fc4fdec-242a-44fd-9ba6-7340ace0c8f2"><div class="bn-block" data-node-type="blockContainer" data-id="8fc4fdec-242a-44fd-9ba6-7340ace0c8f2"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]">Consommer local permet de soutenir l'économie locale, réduire l'empreinte carbone des produits, proposer…

#### Fiche 126710 — 6.4.1. MR 1  - Réduire les impacts des projets de méthanisation

- **Run 1 :** (aucun levier)
- **Run 2 :** (aucun levier)
- **Run 3 :** Sobriété foncière [4]
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété foncière (1/3)

> La méthanisation présente un intérêt certain pour l’environnement, le dévelepommeent énergétique et économique locale comme présenté dans l'action 6,3,4. Des impacts environnementaux sont cependant possibles à l’échelle locale : artificialisation des sols, risque de pollution des eaux. Les nuisances pour les riverains doivent être prises en considération en amont des projets (risque de nuisances olfactives, nuisances sonores via le flux de camions…). Il s'agira pour le territoire de limiter ces…

#### Fiche 126712 — 6.4.3. MR3 - Planification du développement des énergies renouvelables

- **Run 1 :** Biogaz [2] | Electricité renouvelable [2] | Réseaux de chaleur décarbonés [2]
- **Run 2 :** (aucun levier)
- **Run 3 :** Electricité renouvelable [2] | Sobriété foncière [2]
- **Prod :** Biogaz [2] | Electricité renouvelable [2]
- Leviers intermittents : Biogaz (1/3), Electricité renouvelable (2/3), Réseaux de chaleur décarbonés (1/3), Sobriété foncière (1/3)

> Le territoire prévoit un soutien au développement des énergies renouvelables, avec notamment l’aide à la diversification des activités agricoles. En complément des mesures MR1 pour la méthanisation et MR2 pour le chauffage au bois, il s’agira de porter une attention particulière au développement de toutes les énergies renouvelables de manière à limiter les impacts sur le paysage et le milieu naturel. Il faudra veiller à la bonne intégration des enjeux dans les études d'impact et à l'application…

#### Fiche 126715 — 7.2.1. Encourager et soutenir les changements de pratiques agricoles

- **Run 1 :** Changements de pratiques de fertilisation azotée [6] | Elevage durable [6] | Pratiques stockantes [6]
- **Run 2 :** (aucun levier)
- **Run 3 :** Changements de pratiques de fertilisation azotée [6] | Elevage durable [6] | Pratiques stockantes [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Changements de pratiques de fertilisation azotée (2/3), Elevage durable (2/3), Pratiques stockantes (2/3)

> L’agriculture, comme de nombreux secteurs d’activité, doit évoluer afin de réduire son impact environnemental et d’adapter au changement climatique. Les territoires, en proposant des formations, des moments d’échange et de sensibilisations, peuvent accompagner le changement des pratiques agricoles vers des méthodes plus respectueuses de l’environnement et apte à supporter les changements climatiques à venir.

#### Fiche 126723 — 8.3.2. Déminéraliser, végétaliser des espaces dans les communes (trame verte et bleue)

- **Run 1 :** (aucun levier)
- **Run 2 :** Pratiques stockantes [1]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Pratiques stockantes (1/3)

> Les centre-ville sont souvent fortement imperméables, avec l'emploi d'enrobé et de béton. Déminéraliser et végétaliser les espaces publics comme les places et les cours d'écoles permet de réduire les effets d' îlots de chaleur urbains, d'améliorer la gestion des eaux pluviales, et de favoriser la biodiversité.

### Levier présent dans certains runs seulement (10)

#### Fiche 126665 — 1.4.3. Accompagner les particuliers sur le remplacement des systèmes de chauffage polluants par des systèmes performants alimentés en énergie renouvelable

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [6] | Sobriété des bâtiments (résidentiel) [6]
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [6]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [6] | Sobriété des bâtiments (résidentiel) [6]
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6]
- Leviers intermittents : Sobriété des bâtiments (résidentiel) (2/3)

> L'une des causes principales d'émissions de gaz à effet de serre, d'émissions de polluants comme les PM2,5, et de précarité enrgétique provient du nombre importants de logements se chauffant avec des systèmes énergétiques vétustes. Ces systèmes sont les cheminées traditionnelles en foyer ouvert ou fermé, les chaudières au fioul ou encore les chaudières au charbon. Tous ses systèmes peuvent etre remplacés par des poeles à bois à haute performante environnementale, ou bien des pompes à chaleur ai…

#### Fiche 126667 — 2.1.2. Planifier la rénovation énergétique des bâtiments publics (communes/EPCI)

- **Run 1 :** Changement de chaudière à fioul (tertiaire) [5] | Changement de chaudière à gaz (tertiaire) [5] | Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 2 :** Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 3 :** Sobriété et isolation des bâtiments (tertiaire) [5]
- **Prod :** Sobriété et isolation des bâtiments (tertiaire) [2]
- Leviers intermittents : Changement de chaudière à fioul (tertiaire) (1/3), Changement de chaudière à gaz (tertiaire) (1/3)

> Les collectivités disposent d’un patrimoine important, pour lequel il est parfois difficile de savoir par où commencer les travaux de rénovations. Les schémas directeur immobilier énergétique (SDIE) permettent de planifier au sein des collectivités la gestion et la rénovation des bâtiments, et ils peuvent faire l'objet d'un soutien financier de l'ADEME. Pour les communes de moins de 5000 habitants, où un SDIE n’est pas toujours l’outil le plus adapté du fait d’un patrimoine moins conséquent, la…

#### Fiche 126669 — 2.2.2. Poursuivre la mise en œuvre des projets de rénovations et de recours aux énergies renouvelables des collectivités

- **Run 1 :** Changement de chaudière à fioul (tertiaire) [5] | Changement de chaudière à gaz (tertiaire) [5] | Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 2 :** Electricité renouvelable [5] | Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 3 :** Sobriété et isolation des bâtiments (tertiaire) [5]
- **Prod :** Electricité renouvelable [5] | Sobriété et isolation des bâtiments (tertiaire) [5]
- Leviers intermittents : Changement de chaudière à fioul (tertiaire) (1/3), Changement de chaudière à gaz (tertiaire) (1/3), Electricité renouvelable (1/3)

> Le décret tertiaire ambitionne une forte baisse des consommations énergétique du patrimoine public avec pour première échéance 2030. Pour y arriver, une rénovation énergétique de chaque bâtiment ancien, en priorisant les plus consommateurs, doit être mise en œuvre.

#### Fiche 126671 — 2.3.2. Développer des bâtiments publics « producteurs » et « sobres » en énergies

- **Run 1 :** Electricité renouvelable [5] | Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 2 :** Electricité renouvelable [5]
- **Run 3 :** Electricité renouvelable [5] | Sobriété et isolation des bâtiments (tertiaire) [5]
- **Prod :** Electricité renouvelable [5]
- Leviers intermittents : Sobriété et isolation des bâtiments (tertiaire) (2/3)

> Les bâtiments publics représentent un potentiel important de toiture non exploité pour la production d'énergie ou la récupération des eaux pluviales. Une réflexion est à porter sur le développement des énergies renouvelables au sein des bâtiments publics existants et futurs et les possibilités de stockage.

#### Fiche 126677 — 3.1.3. Inciter le monde économique à déployer des actions de mobilité décarbonée

- **Run 1 :** Covoiturage [5, 6] | Réduction des déplacements [5, 6]
- **Run 2 :** Réduction des déplacements [5, 6]
- **Run 3 :** Covoiturage [6] | Réduction des déplacements [5, 6]
- **Prod :** Réduction des déplacements [4, 5, 6]
- Leviers intermittents : Covoiturage (2/3)

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="75f0f0bb-2464-4b5d-b34e-9d8923721dd3"><div class="bn-block" data-node-type="blockContainer" data-id="75f0f0bb-2464-4b5d-b34e-9d8923721dd3"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]">La voiture est prépondérante dans les trajets domicile - travail sur le territoire. La mise en place de …

#### Fiche 126678 — 3.2.1. Provoquer un changement de comportement

- **Run 1 :** Vélo et transport en commun [6]
- **Run 2 :** Réduction des déplacements [6] | Vélo et transport en commun [6]
- **Run 3 :** Réduction des déplacements [6] | Vélo et transport en commun [6]
- **Prod :** Vélo et transport en commun [6]
- Leviers intermittents : Réduction des déplacements (2/3)

> Il existe sur le territoire des moyens de se déplacer sans recourir à la voiture mais qui sont trop peu connu du grand public. Pour accompagner le développement massif des mobilités douces et des transports en commun, une communication auprès du grand public doit se faire pour informer et inciter les habitants et entreprises à changer leurs habitudes de déplacement.

#### Fiche 126684 — 3.3.2. Réduire l’usage individuel de la voiture

- **Run 1 :** Véhicules électriques [6]
- **Run 2 :** Efficacité et carburants décarbonés des véhicules privés [6] | Véhicules électriques [6]
- **Run 3 :** Véhicules électriques [6]
- **Prod :** Efficacité et carburants décarbonés des véhicules privés [6] | Véhicules électriques [6]
- Leviers intermittents : Efficacité et carburants décarbonés des véhicules privés (1/3)

> Les véhicules électriques, hybrides, et autres véhicules à faibles émissions offrent une alternative durable aux véhicules traditionnels à combustion, diminuant ainsi la pollution atmosphérique et sonore. En promouvant l'adoption de ces véhicules, les collectivités peuvent contribuer significativement à la lutte contre le changement climatique et à la protection de la santé publique.

#### Fiche 126690 — 4.2.3. Réduire les déchets dans la poubelle

- **Run 1 :** Prévention des déchets [6] | Valorisation matière des déchets [6]
- **Run 2 :** Prévention des déchets [6]
- **Run 3 :** Prévention des déchets [6] | Valorisation matière des déchets [6]
- **Prod :** Prévention des déchets [6]
- Leviers intermittents : Valorisation matière des déchets (2/3)

> La réduction des déchets dans la poubelle est une initiative cruciale pour minimiser l'empreinte environnementale et promouvoir une gestion durable des déchets. Elle passe par la sensibilisation et l'adoption de comportements tels que le compostage des déchets organiques, l'utilisation de sacs réutilisables et de contenants durables, ainsi que la réduction de l'emballage superflu.

#### Fiche 126692 — 4.3.1. Développer le compostage pour tous

- **Run 1 :** Valorisation matière des déchets [1, 6]
- **Run 2 :** Prévention des déchets [1, 6] | Valorisation matière des déchets [1, 6]
- **Run 3 :** Valorisation matière des déchets [1, 6]
- **Prod :** Valorisation matière des déchets [1, 6]
- Leviers intermittents : Prévention des déchets (1/3)

> Les biodéchets constituent environ 30% des ordures ménagères, actuellement incinérées. Les habitants de logements collectifs n’ont actuellement pas possibilité de trier en composteur cette ressource. Les particuliers ont aussi besoin d'être guidés dans la pratique et d'être informés pour éviter les aprioris sur le compostage.

#### Fiche 126724 — 8.3.3. Expérimenter l’urbanisme favorable à la santé (UFS)

- **Run 1 :** Vélo et transport en commun [1]
- **Run 2 :** Réduction des déplacements [1] | Vélo et transport en commun [1]
- **Run 3 :** Réduction des déplacements [1] | Vélo et transport en commun [1]
- **Prod :** (aucun levier)
- Leviers intermittents : Réduction des déplacements (2/3)

> L'urbanisme favorable à la santé (UFS) vise à concevoir et organiser les espaces urbains de manière à promouvoir le bien-être physique et mental des habitants. Cela inclut la création de zones végétalisés, l'amélioration des infrastructures pour les piétons et les mobilités douces, la réduction de la pollution de l'air et du bruit, et l'accès facilité aux services de santé et aux activités de loisirs.

### Levier intermittent et catégories instables (13)

#### Fiche 126659 — 1.2.2. Lutter contre la précarité énergétique des ménages

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [6] | Sobriété des bâtiments (résidentiel) [6]
- **Run 2 :** Sobriété des bâtiments (résidentiel) [6]
- **Run 3 :** Sobriété des bâtiments (résidentiel) [3, 6]
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6]
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (1/3)
- Catégories instables sur : Sobriété des bâtiments (résidentiel)

> La précarité énergétique des ménages désigne la difficulté, voire l'incapacité, à chauffer correctement le logement, en raison de revenus insuffisants et/ou d'une mauvaise performance énergétique du bâti. La Sambre-Avesnois est particulièrement sensible à ce phénomène du fait d'un bâti ancien et d'une population à faible revenu médiant. Des dispositifs existent, comme l'espace info énergie, porté par le PNR de l'Avenois, le PIG "Habiter mieux" ou encore le dispositif CEE précarité, afin d'accom…

#### Fiche 126660 — 1.2.3. Lutter contre la précarité énergétique des ménages (PLH 2025-2030)

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [2] | Sobriété des bâtiments (résidentiel) [2]
- **Run 2 :** Sobriété des bâtiments (résidentiel) [6]
- **Run 3 :** Sobriété des bâtiments (résidentiel) [2]
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [2] | Changement chaudières gaz + rénovation (résidentiel) [2]
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (1/3)
- Catégories instables sur : Sobriété des bâtiments (résidentiel)

> La précarité énergétique des ménages désigne la difficulté, voire l'incapacité, à chauffer correctement le logement, en raison de revenus insuffisants et/ou d'une mauvaise performance énergétique du bâti. Le Programme Local de l’Habitat 2025-2030 de la CA Maubeuge Val-de-Sambre inclut plusieurs actions pour agir contre la précarité énergétique et qui sont reprises dans le PCAET..

#### Fiche 126679 — 3.2.2. Développer les mobilités douces, notamment le vélo

- **Run 1 :** Vélo et transport en commun [1, 6]
- **Run 2 :** Réduction des déplacements [1, 6] | Vélo et transport en commun [1, 6]
- **Run 3 :** Covoiturage [6] | Réduction des déplacements [6] | Vélo et transport en commun [6]
- **Prod :** Covoiturage [6] | Vélo et transport en commun [1, 6]
- Leviers intermittents : Covoiturage (1/3), Réduction des déplacements (2/3)
- Catégories instables sur : Vélo et transport en commun

> Sur le territoire, les ménages sont fortement dépendant de la voiture individuelle pour les déplacements du quotidien. Un enjeu important porte sur la réduction des déplacements en voiture individuelle (covoiturage), le développement des autres moyens de déplacements et l'accompagnement des ménages sur l'adoption de véhicules plus propres. Les mobilités douces sont essentielles pour créer des environnements urbains plus durables, sûrs et agréables. Elles englobent principalement la marche à pie…

#### Fiche 126680 — 3.2.3. Développer l’usage des transports en commun

- **Run 1 :** Vélo et transport en commun [1, 3]
- **Run 2 :** Réduction des déplacements [1, 3, 6] | Vélo et transport en commun [1, 3, 6]
- **Run 3 :** Vélo et transport en commun [1, 3]
- **Prod :** Vélo et transport en commun [1, 3]
- Leviers intermittents : Réduction des déplacements (1/3)
- Catégories instables sur : Vélo et transport en commun

> Les transports en commun, tels que les bus, tramways et trains, offrent une alternative efficace et durable à la voiture individuelle, permettant de transporter un grand nombre de personnes tout en réduisant l'empreinte carbone par passager. En investissant dans des infrastructures modernes et accessibles, en améliorant la fréquence et la fiabilité des services, et en offrant des tarifs attractifs, les collectivités peuvent encourager davantage de citoyens à opter pour les transports en commun.

#### Fiche 126685 — 4.1.1. Développer et mettre en œuvre les PLPDMA (programme local de déchets ménagers et assimilés) à l'échelle des EPCI

- **Run 1 :** Prévention des déchets [2, 4]
- **Run 2 :** Prévention des déchets [2, 4] | Valorisation matière des déchets [2, 4]
- **Run 3 :** Prévention des déchets [2] | Valorisation matière des déchets [2]
- **Prod :** Prévention des déchets [2] | Valorisation matière des déchets [2]
- Leviers intermittents : Valorisation matière des déchets (2/3)
- Catégories instables sur : Prévention des déchets

> Le PLPDMA (programme local de déchets ménagers et assimilés) vise à réduire la quantité de déchets produits, à encourager le tri séléctif et le recyclage, ainsi qu'à optimiser la collecte et le traitement des déchets. Un PLPDMA bien conçu contribue non seulement à préserver les ressources naturelles et à réduire les émissions de gaz à effet de serre, mais aussi à créer des communautés plus durables et résilientes.

#### Fiche 126686 — 4.1.2. Mise en place d'une démarche d'écologie industrielle territoriale (EIT)

- **Run 1 :** Valorisation matière des déchets [4]
- **Run 2 :** Production Industrielle [4] | Prévention des déchets [4, 6] | Valorisation matière des déchets [4, 6]
- **Run 3 :** Prévention des déchets [4] | Valorisation matière des déchets [4]
- **Prod :** (aucun levier)
- Leviers intermittents : Production Industrielle (1/3), Prévention des déchets (2/3)
- Catégories instables sur : Valorisation matière des déchets

> L'écologie industrielle territoriale (EIT) consiste en une quantification des flux de ressources utilisées et produites au sein d'un territoire, permettant de faire émerger des logiques de mutualisation et d'économie circulaire.

#### Fiche 126691 — 4.2.4. Développer le réemploi et la réutilisation

- **Run 1 :** Valorisation matière des déchets [1, 4]
- **Run 2 :** Prévention des déchets [1, 4, 6] | Valorisation matière des déchets [1, 4, 6]
- **Run 3 :** Prévention des déchets [1, 4] | Valorisation matière des déchets [1, 4]
- **Prod :** Prévention des déchets [4, 6]
- Leviers intermittents : Prévention des déchets (2/3)
- Catégories instables sur : Valorisation matière des déchets

> Le réemploi consiste à réutiliser des objets ou matériaux pour leur donner une seconde vie, cela permettant notamment une réduction de la production de déchets et une économie de ressources. Les territoires peuvent s'appuyer sur le Réseau National des Ressourceries et Recycleries (RNRR) pour la mise en place de projets de ressourceries sur le territoire.

#### Fiche 126693 — 4.3.2. Valoriser les déchets du BTP et des industriels

- **Run 1 :** Valorisation matière des déchets [4]
- **Run 2 :** Production Industrielle [4, 6] | Valorisation matière des déchets [4, 6]
- **Run 3 :** Valorisation matière des déchets [4]
- **Prod :** Valorisation matière des déchets [4]
- Leviers intermittents : Production Industrielle (1/3)
- Catégories instables sur : Valorisation matière des déchets

> Le recyclage et réutilisation des déchets des industries permet la mise en place de démarches vertueuses au sein du territoire, tout en limitant la consommation de ressources. Des démarches comme l'écologie industrielle territorial (EIT), et la représentation écosystémique par les Toiles, sont des outils à disposition des territoires permettant d'engager des échanges et des mises en relation des acteurs industriels sur leurs besoins.

#### Fiche 126694 — 4.4.3. Valoriser énergétiquement les déchets produits sur le territoire

- **Run 1 :** Biogaz [1, 4]
- **Run 2 :** Biogaz [1, 4]
- **Run 3 :** Biogaz [1] | Valorisation matière des déchets [1]
- **Prod :** Biogaz [1] | Valorisation matière des déchets [1]
- Leviers intermittents : Valorisation matière des déchets (1/3)
- Catégories instables sur : Biogaz

> Les déchets produits sur le territoire sont une ressource qu'il est possible d'exploiter. Les déchets agro-alimentaires en particulier, peuvent être utilisés en compost, ou encore dans une unité de méthanisation, permettant de produire du gaz renouvelable localement.

#### Fiche 126699 — 5.2.2. Favoriser le rapprochement entre producteurs et consommateurs, notamment en développant les circuits courts Mesure 32 de la charte du PNR de l’Avesnois

- **Run 1 :** Efficacité et sobriété logistique [4, 6]
- **Run 2 :** Efficacité et sobriété logistique [4, 5, 6] | Fret décarboné et multimodalité [4, 5, 6]
- **Run 3 :** Efficacité et sobriété logistique [4, 5]
- **Prod :** Efficacité et sobriété logistique [5, 6]
- Leviers intermittents : Fret décarboné et multimodalité (1/3)
- Catégories instables sur : Efficacité et sobriété logistique

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="0836816e-f0ba-46a9-9010-79bc82e4d4eb"><div class="bn-block" data-node-type="blockContainer" data-id="0836816e-f0ba-46a9-9010-79bc82e4d4eb"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]">La Sambre Avesnois a la chance de disposer de nombreux producteurs locaux. Pour soutenir cette activité,…

#### Fiche 126701 — 6.1.1. Accompagner la mise en œuvre de la loi APER

- **Run 1 :** Electricité renouvelable [2, 6]
- **Run 2 :** Biogaz [2, 4, 6] | Electricité renouvelable [2, 4, 6] | Réseaux de chaleur décarbonés [2, 4, 6]
- **Run 3 :** Electricité renouvelable [2, 6]
- **Prod :** Electricité renouvelable [6]
- Leviers intermittents : Biogaz (1/3), Réseaux de chaleur décarbonés (1/3)
- Catégories instables sur : Electricité renouvelable

> La loi APER (Accélération de la Production des Énergies Renouvelables) vise à renforcer le développement des énergies renouvelables en France en identifiant et en aménageant des zones d’accélération dédiées. L’action vise a un accompagnement des communes dans la définition des ZAEnR et des porteurs de projets dans la mise en œuvre de projets ambitieux sur les zones définies.

#### Fiche 126713 — 7.1.1. Améliorer la séquestration du carbone en préservant les haies bocagères

- **Run 1 :** Gestion des haies [4] | Pratiques stockantes [4]
- **Run 2 :** Gestion des haies [1]
- **Run 3 :** Gestion des haies [2, 6] | Pratiques stockantes [6]
- **Prod :** Gestion des haies [1]
- Leviers intermittents : Pratiques stockantes (2/3)
- Catégories instables sur : Gestion des haies

> La séquestration du carbone consiste en un captage du CO2 présent dans l'air dans de la biomasse ou des produits bois. Il est nécessaire de la renforcer afin d'atteindre la neutralité carbone en 2050. Sur les terres agricoles, cela comprend la préservation et le développement du bocage.

#### Fiche 126717 — 7.2.3. Accompagner la diversification des activités

- **Run 1 :** Biogaz [2, 6] | Electricité renouvelable [2, 6] | Gestion des forêts et produits bois [2, 6] | Réseaux de chaleur décarbonés [2, 6]
- **Run 2 :** Biogaz [6] | Electricité renouvelable [6] | Gestion des forêts et produits bois [6]
- **Run 3 :** Biogaz [2, 6] | Electricité renouvelable [2, 6] | Réseaux de chaleur décarbonés [2, 6]
- **Prod :** Biogaz [6] | Electricité renouvelable [6]
- Leviers intermittents : Gestion des forêts et produits bois (2/3), Réseaux de chaleur décarbonés (2/3)
- Catégories instables sur : Biogaz, Electricité renouvelable

> Les agriculteurs peuvent mettre en place des activités annexes de productions et de valorisations énergétiques sur leur terrain. De la méthanisation à la production de bois déchiqueté de bocage pour les chaufferies, ces activités participent à la valorisation des ressources du territoire et apportent aux agriculteurs un complément de revenu non négligeable. Porter une attention particulière au développement de toutes les énergies renouvelables et en particulier à l’éolien et à l’agrivoltaïsme, …

### Mêmes leviers, catégories différentes (9)

#### Fiche 126670 — 2.3.1. Accompagner les communes SIRPP dans le suivi des consommations

- **Run 1 :** Sobriété et isolation des bâtiments (tertiaire) [6]
- **Run 2 :** Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 3 :** Sobriété et isolation des bâtiments (tertiaire) [5]
- **Prod :** (aucun levier)
- Catégories instables sur : Sobriété et isolation des bâtiments (tertiaire)

> Un suivi des consommations et des dépenses du patrimoine public permet aux collectivités de prendre conscience de l’impact des énergies sur les budgets, et d’identifier rapidement les bâtiments où des dépenses anormales sont relevées. Aussi, le décret tertiaire oblige les bâtiments assujettis à effectuer une remontée annuelle des consommations sur la plateforme OPERAT.

#### Fiche 126682 — 3.2.5. Reconversion des flottes de véhicules thermiques

- **Run 1 :** Véhicules électriques [5, 6]
- **Run 2 :** Véhicules électriques [2, 5, 6]
- **Run 3 :** Véhicules électriques [5, 6]
- **Prod :** Efficacité et carburants décarbonés des véhicules privés [5, 6] | Véhicules électriques [5, 6]
- Catégories instables sur : Véhicules électriques

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="9d811b7d-1e96-4d79-8dcf-31ad51a43b66"><div class="bn-block" data-node-type="blockContainer" data-id="9d811b7d-1e96-4d79-8dcf-31ad51a43b66"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]">Les entreprises et les collectivités disposent de flottes de véhicules conséquents. La reconversion des …

#### Fiche 126683 — 3.3.1. Repenser la place de la voiture dans les centres-villes

- **Run 1 :** Réduction des déplacements [1, 2] | Vélo et transport en commun [1, 2]
- **Run 2 :** Réduction des déplacements [1, 2] | Vélo et transport en commun [1, 2]
- **Run 3 :** Réduction des déplacements [1, 2] | Vélo et transport en commun [1]
- **Prod :** Réduction des déplacements [1] | Vélo et transport en commun [1]
- Catégories instables sur : Vélo et transport en commun

> <div class="bn-block-group" data-node-type="blockGroup"><div class="bn-block-outer" data-node-type="blockOuter" data-id="27e980a3-341e-4ecf-8d80-09e5af8ee251"><div class="bn-block" data-node-type="blockContainer" data-id="27e980a3-341e-4ecf-8d80-09e5af8ee251"><div class="bn-block-content !p-0" data-content-type="paragraph"><p class="bn-inline-content !text-sm !text-primary-9 font-[Marianne]">Repenser la place de la voiture dans les centres-villes est crucial pour créer des espaces urbains plus …

#### Fiche 126696 — 5.1.2. Engager une démarche d’exemplarité environnementale des zones d’activités économiques

- **Run 1 :** Sobriété foncière [1, 2]
- **Run 2 :** Sobriété foncière [1, 2, 4]
- **Run 3 :** Sobriété foncière [2]
- **Prod :** (aucun levier)
- Catégories instables sur : Sobriété foncière

> Le territoire souhaite poursuivre son développement économique en proposant des zones d’activités pour l’implantation de nouvelles entreprises. A l’aune de la loi Zéro artificialisation nette (ZAN) et du besoin d’adaptation du territoire au changement climatique, il est nécessaire de mettre en place une démarche d’exemplarité sur les ZAE afin de concilier le développement du territoire et la lutte contre le changement climatique.

#### Fiche 126706 — 6.3.1. Développer l’énergie solaire thermique et photovoltaïque

- **Run 1 :** Electricité renouvelable [5, 6]
- **Run 2 :** Electricité renouvelable [4, 6]
- **Run 3 :** Electricité renouvelable [6]
- **Prod :** Electricité renouvelable [6]
- Catégories instables sur : Electricité renouvelable

> Le PCAET porte de fortes ambitions sur le déploiement de la filière photovoltaïque sur le territoire. Pour la filière solaire thermique, il n'existe que très peu de sites installées sur le territoire. Une communication spécifique et la mise en œuvre de projets démonstrateurs pour alimenter des bâtiments à forte consommation d'eau chaude (piscine municipale, EHPAD, hôpital, ...) permettra de mettre en œuvre cette technologie.

#### Fiche 126707 — 6.3.2. Poursuivre le développement de la filière bois énergie

- **Run 1 :** Gestion des forêts et produits bois [4] | Réseaux de chaleur décarbonés [4]
- **Run 2 :** Gestion des forêts et produits bois [4] | Réseaux de chaleur décarbonés [4]
- **Run 3 :** Gestion des forêts et produits bois [4] | Réseaux de chaleur décarbonés [4, 6]
- **Prod :** Réseaux de chaleur décarbonés [4]
- Catégories instables sur : Réseaux de chaleur décarbonés

> En Sambre-Avesnois, la filière bois-énergie est animée par le PNR de l'Avesnois et son chargé de mission bois-énergie. En 2024, il existe 58 chaufferies à bois déchiqueté sur le territoire pour alimenter des exploitations agricoles ou des réseaux de chaleur technique de collectivités. Le PNR de l’Avesnois veille à la bonne gestion de la ressource bocagère et au respect des normes environnementales avec par exemple des filtres à particules efficaces. La Sambre-Avesnois compte des surfaces forest…

#### Fiche 126708 — 6.3.3. Développer la géothermie basse énergie et très basse énergie

- **Run 1 :** Réseaux de chaleur décarbonés [6]
- **Run 2 :** Réseaux de chaleur décarbonés [4, 6]
- **Run 3 :** Réseaux de chaleur décarbonés [6]
- **Prod :** (aucun levier)
- Catégories instables sur : Réseaux de chaleur décarbonés

> La géothermie basse énergie permet de récupérer les calories présentes dans le sous-sol afin d'alimenter une pompe à chaleur et ainsi chauffer des bâtiments à bas cout. Ces systèmes sont très peu développés sur le territoire malgré les avantages de cette technologie. La promotion de ces dispositifs et la mise en œuvre de projets démonstrateur visent à engager une dynamique vertueuse afin d'atteindre les objectifs fixés dans le PCAET.

#### Fiche 126709 — 6.3.4. Mettre en œuvre des projets de méthanisation

- **Run 1 :** Biogaz [6]
- **Run 2 :** Biogaz [4, 6]
- **Run 3 :** Biogaz [4, 6]
- **Prod :** Biogaz [1] | Valorisation matière des déchets [1]
- Catégories instables sur : Biogaz

> La Sambre-Avesnois compte 9 unités de méthanisation, dont une seule unité réalisant de l'injection de gaz dans le réseau. Le potentiel sur le territoire est important du fait d'une activité agricole et agroalimentaire importante. L'intéret de la méthanisation est multiple : valorisation des déchets, limitations de la pollution agricole, production de digestat pouvant se substituer aux engrais minéraux, production de biogaz renforçant l'indépendance énergétique de la Sambre-Avesnois, apporter un…

#### Fiche 126714 — 7.1.2. Œuvrer pour la préservation du parcellaire herbager

- **Run 1 :** Gestion des prairies [2, 3]
- **Run 2 :** Gestion des prairies [2, 3]
- **Run 3 :** Gestion des prairies [2, 3, 6]
- **Prod :** Gestion des prairies [3]
- Catégories instables sur : Gestion des prairies

> Maintenir et restaurer les prairies est essentiel pour préserver leur rôle écologique. Cela implique de soutenir les pratiques agricoles durables, de fournir des aides pour l'entretien et la restauration des prairies, et de réguler leur conversion en d'autres usages.
