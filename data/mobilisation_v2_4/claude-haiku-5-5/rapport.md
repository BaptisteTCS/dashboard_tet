# Notes de mobilisation calculées (classification v2.4) — stabilité et comparaison avec la prod

Mis à jour le 2026-11-05 15:50. Claude Haiku 5.5, prompt `prompts/classification_volet_ges_v2_4.md`, une fiche par appel, 3 runs. Lecture seule sur la prod.

## Synthèse

- Fiches : **1650** dans 21 collectivités
- Classification identique (leviers + catégories) sur tous les runs : **88%**
- Classification et verdicts « structurante » identiques : **86%**
- Verdict « structurante » identique, pour les leviers retenus par tous les runs : **94%** (1228 paires fiche × levier)
- Cases levier × catégorie notées dans au moins un run : **886**
- … dont note identique sur tous les runs : **74%** ; écart de 1 point : 19% ; écart de 2 points ou plus : 7%
- Coût : 1.22 $ — réponses invalides rejouées : 0 — tronquées à 3 leviers : 7

## Par collectivité

| Collectivité | Type | Population | Fiches | Classif. stable | Cases notées | Notes stables |
|---|---|---:|---:|---:|---:|---:|
| Hélette (13693) | commune | 775 | 41 | 95% | 26 | 85% |
| Saint-Jean-de-Braye (1609) | commune | 21983 | 36 | 86% | 24 | 67% |
| CA Privas Centre Ardèche (3893) | communauté d'agglomération | 45008 | 100 | 94% | 49 | 71% |
| CC Ardennes Thiérache (3914) | communauté de communes | 9843 | 100 | 89% | 56 | 75% |
| CA Rochefort Océan (4026) | communauté d'agglomération | 65272 | 75 | 85% | 24 | 62% |
| CA Guingamp-Paimpol Agglomération de l'Armor à l'Argoat (4097) | communauté d'agglomération | 75886 | 101 | 78% | 73 | 66% |
| CC Creuse Sud Ouest (4111) | communauté de communes | 14140 | 76 | 91% | 27 | 78% |
| Bordeaux Métropole (4322) | métropole | 830284 | 55 | 71% | 77 | 69% |
| CC de la Forêt (4576) | communauté de communes | 17716 | 92 | 96% | 50 | 86% |
| CC Baugeois Vallée (4637) | communauté de communes | 35657 | 84 | 81% | 60 | 68% |
| CC du Pays de Colombey et du Sud Toulois (4707) | communauté de communes | 11436 | 83 | 89% | 33 | 79% |
| CC du Pays de Barr (4939) | communauté de communes | 24710 | 41 | 93% | 12 | 92% |
| CC Sundgau (4973) | communauté de communes | 48832 | 37 | 81% | 18 | 83% |
| CC du Pays de l'Arbresle (CCPA) (4994) | communauté de communes | 39444 | 96 | 94% | 42 | 86% |
| Métropole de Lyon (4999) | métropole | 1428062 | 81 | 80% | 49 | 67% |
| CC Val de Gray (5005) | communauté de communes | 21148 | 42 | 93% | 27 | 85% |
| CC Brionnais Sud Bourgogne (5033) | communauté de communes | 15370 | 111 | 95% | 41 | 83% |
| Le Havre Seine Métropole (5119) | communauté urbaine | 268985 | 86 | 83% | 62 | 73% |
| CC du Pays des Achards (5300) | communauté de communes | 19819 | 102 | 89% | 44 | 73% |
| Paris Est Marne & Bois (5390) | EPT | 514520 | 138 | 96% | 45 | 84% |
| SM du SCoT Sambre Avesnois (6030) | epci | 226108 | 73 | 86% | 47 | 64% |

## Répartition des notes (note retenue, cases notées dans au moins un run)

- Nouvelle note : {0: 66, 1: 201, 2: 451, 3: 168}

## Comparaison avec la note actuelle en prod (17 collectivités notées en prod)

- Cases non nulles dans l'une ou l'autre : 942
- Même note : 25% ; nouvelle plus haute : 39% ; plus basse : 36%
- Note moyenne : prod 1.32, nouvelle 1.40

Croisement (lignes : note prod, colonnes : nouvelle note) :

| prod \ nouvelle | 0 | 1 | 2 | 3 |
|---|---:|---:|---:|---:|
| 0 | 0 | 64 | 111 | 29 |
| 1 | 144 | 50 | 82 | 20 |
| 2 | 121 | 35 | 159 | 64 |
| 3 | 13 | 2 | 20 | 28 |

## Comparaison des règles de notation

Mêmes classifications ; seule la règle qui transforme les comptes de fiches en note change.

| Règle | Notes stables (3 runs) | Écart ≥ 2 points | Répartition (cases notées) | Même note que la prod | Note moyenne (prod → nouvelle) |
|---|---:|---:|---|---:|---|
| Règle A — 1 : une peu importante · 2 : plusieurs peu importantes ou une structurante · 3 : au moins deux structurantes | 74% | 7% | {0: 66, 1: 201, 2: 451, 3: 168} | 25% | 1.32 → 1.40 |
| Règle B — 1 : une peu importante · 2 : deux peu importantes · 3 : une structurante ou au moins trois peu importantes | 80% | 10% | {0: 66, 1: 201, 2: 49, 3: 570} | 12% | 1.32 → 1.75 |
