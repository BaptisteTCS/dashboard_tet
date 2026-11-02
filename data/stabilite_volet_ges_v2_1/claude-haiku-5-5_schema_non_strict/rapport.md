# Stabilité Mistral Large 4 — classification volet GES

Modèle `claude-haiku-5-5`, raisonnement `aucun`, température par défaut de l'API. Prompt v2 (`prompts/classification_volet_ges_v2.md`), une fiche par appel, codes de leviers et JSON contraint, 3 runs indépendants. Lecture seule sur la prod.

Mis à jour le 2026-11-02 13:11.

## Synthèse

| Collectivité | Fiches | Stables | Instables | % stable | Paires 3/3 | Majorité = prod |
|---|---:|---:|---:|---:|---:|---:|
| CC Sundgau (4973) | 37 | 33 | 4 | 89% | 35/42 | non classée en prod |
| Paris Est Marne & Bois (5390) | 141 | 131 | 10 | 93% | 64/82 | 18/68 |
| **Total** | **178** | **164** | **14** | **92%** | | |

« Paires 3/3 » : paires levier × catégorie données par les 3 runs, sur toutes les paires proposées au moins une fois.

## CC Sundgau (4973)

- Fiches : **37** — stables sur les 3 runs : **33** (89%), instables : **4**
- Paires levier × catégorie distinctes proposées : 42 — 3/3 runs : 35, 2/3 runs : 4, 1/3 runs : 3
- Aucune classification en prod pour cette collectivité
- Réponses JSON invalides rejouées : 0
- Appels : 111 — tokens d'entrée 1 054 329 (dont 1 012 320 en cache, 96%), sortie 6 289 — coût estimé 0.02 $ pour les 3 runs
- Date : 2026-11-02 13:11

### Classée dans certains runs, aucun levier dans d'autres (1)

#### Fiche 53163 — organiser des visites de jardins et prise de parole de jardiniers

- **Run 1 :** (aucun levier)
- **Run 2 :** Prévention des déchets [6]
- **Run 3 :** Prévention des déchets [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Prévention des déchets (2/3)

### Levier présent dans certains runs seulement (1)

#### Fiche 42050 — Mettre en place une politique de mobilité alternative des agents et des élu.e.s

- **Run 1 :** Covoiturage [6] | Réduction des déplacements [5, 6] | Vélo et transport en commun [5, 6]
- **Run 2 :** Efficacité et carburants décarbonés des véhicules privés [5, 6] | Réduction des déplacements [5, 6] | Vélo et transport en commun [5, 6]
- **Run 3 :** Efficacité et carburants décarbonés des véhicules privés [5] | Réduction des déplacements [5, 6] | Vélo et transport en commun [5, 6]
- **Prod :** (aucun levier)
- Leviers intermittents : Covoiturage (1/3), Efficacité et carburants décarbonés des véhicules privés (2/3)

> Mettre en place une politique de mobilité alternative des agents et des élu.e.s, visant le changement de comportement, en adoptant une approche diversifiée pour couvrir tant les déplacements professionnels que ceux domicile-travail. Cette politique devrait inclure l'optimisation et le renouvellement de la flotte de véhicules, une gestion optimisée des déplacements, le développement de l'usage du vélo, des campagnes de communication et de sensibilisation, ainsi que la promotion des transports co…

### Mêmes leviers, catégories différentes (2)

#### Fiche 53170 — Organiser la commande groupée de composteurs de cuisine

- **Run 1 :** Prévention des déchets [3]
- **Run 2 :** Prévention des déchets [1]
- **Run 3 :** Prévention des déchets [1]
- **Prod :** (aucun levier)
- Catégories instables sur : Prévention des déchets

#### Fiche 61676 — Créer un "appartement du futur et du réemploi" à visée pédagogique

- **Run 1 :** Prévention des déchets [1]
- **Run 2 :** Prévention des déchets [1, 6]
- **Run 3 :** Prévention des déchets [1, 6]
- **Prod :** (aucun levier)
- Catégories instables sur : Prévention des déchets

## Paris Est Marne & Bois (5390)

- Fiches : **141** — stables sur les 3 runs : **131** (93%), instables : **10**
- Paires levier × catégorie distinctes proposées : 82 — 3/3 runs : 64, 2/3 runs : 10, 1/3 runs : 8
- Vote majoritaire = prod : 18/68 fiches classées d'un côté ou de l'autre
- Réponses JSON invalides rejouées : 0
- Appels : 423 — tokens d'entrée 4 015 416 (dont 3 857 760 en cache, 96%), sortie 20 512 — coût estimé 0.06 $ pour les 3 runs
- Date : 2026-11-02 13:11

### Classée dans certains runs, aucun levier dans d'autres (4)

#### Fiche 85354 — Coopérer avec les autorités organisatrices de transport

- **Run 1 :** (aucun levier)
- **Run 2 :** Vélo et transport en commun [4]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Vélo et transport en commun (1/3)

#### Fiche 85370 — Mettre en œuvre le plan sur 5 années

- **Run 1 :** Covoiturage [2] | Vélo et transport en commun [2]
- **Run 2 :** Covoiturage [2] | Vélo et transport en commun [2]
- **Run 3 :** (aucun levier)
- **Prod :** Bus et cars décarbonés [2] | Covoiturage [2] | Réduction des déplacements [2] | Vélo et transport en commun [2]
- Leviers intermittents : Covoiturage (2/3), Vélo et transport en commun (2/3)

#### Fiche 85377 — Impliquer davantage les professionnels du cadre bâti dans la rénovation énergétique

- **Run 1 :** Sobriété des bâtiments (résidentiel) [4]
- **Run 2 :** (aucun levier)
- **Run 3 :** (aucun levier)
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6] | Sobriété des bâtiments (résidentiel) [6]
- Leviers intermittents : Sobriété des bâtiments (résidentiel) (1/3)

#### Fiche 85726 — Faciliter la programmation de réhabilitation des bâtiments publics

- **Run 1 :** Sobriété et isolation des bâtiments (tertiaire) [2]
- **Run 2 :** Sobriété et isolation des bâtiments (tertiaire) [2]
- **Run 3 :** (aucun levier)
- **Prod :** Sobriété et isolation des bâtiments (tertiaire) [5]
- Leviers intermittents : Sobriété et isolation des bâtiments (tertiaire) (2/3)

### Levier présent dans certains runs seulement (3)

#### Fiche 85347 — Augmenter le nombre de points de ravitaillement pour les véhicules propres

- **Run 1 :** Efficacité et carburants décarbonés des véhicules privés [1]
- **Run 2 :** Véhicules électriques [1]
- **Run 3 :** Efficacité et carburants décarbonés des véhicules privés [1]
- **Prod :** Véhicules électriques [1]
- Leviers intermittents : Efficacité et carburants décarbonés des véhicules privés (2/3), Véhicules électriques (1/3)

#### Fiche 85355 — Etudier des solutions de stationnement qui faciliteraient l'intermodalité

- **Run 1 :** Covoiturage [2] | Vélo et transport en commun [2]
- **Run 2 :** Covoiturage [2] | Vélo et transport en commun [2]
- **Run 3 :** Vélo et transport en commun [2]
- **Prod :** (aucun levier)
- Leviers intermittents : Covoiturage (2/3)

#### Fiche 85358 — Etudier la faisabilité d'un transport public fluvial

- **Run 1 :** Fret décarboné et multimodalité [2]
- **Run 2 :** Vélo et transport en commun [2]
- **Run 3 :** Fret décarboné et multimodalité [2]
- **Prod :** (aucun levier)
- Leviers intermittents : Fret décarboné et multimodalité (2/3), Vélo et transport en commun (1/3)

### Mêmes leviers, catégories différentes (3)

#### Fiche 85367 — Lancer officiellement la démarche d'élaboration du PLD

- **Run 1 :** Covoiturage [2] | Vélo et transport en commun [2]
- **Run 2 :** Covoiturage [2] | Vélo et transport en commun [2]
- **Run 3 :** Covoiturage [4] | Vélo et transport en commun [4]
- **Prod :** (aucun levier)
- Catégories instables sur : Covoiturage, Vélo et transport en commun

#### Fiche 85692 — Optimiser les parcours de collecte

- **Run 1 :** Efficacité et sobriété logistique [2]
- **Run 2 :** Efficacité et sobriété logistique [1]
- **Run 3 :** Efficacité et sobriété logistique [2]
- **Prod :** Efficacité et sobriété logistique [4]
- Catégories instables sur : Efficacité et sobriété logistique

#### Fiche 85722 — Dispositif territoire roule propre

- **Run 1 :** Efficacité et carburants décarbonés des véhicules privés [3]
- **Run 2 :** Efficacité et carburants décarbonés des véhicules privés [1]
- **Run 3 :** Efficacité et carburants décarbonés des véhicules privés [1]
- **Prod :** (aucun levier)
- Catégories instables sur : Efficacité et carburants décarbonés des véhicules privés
