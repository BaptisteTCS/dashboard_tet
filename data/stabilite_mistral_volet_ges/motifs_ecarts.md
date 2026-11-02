# Motifs des écarts entre runs — Mistral Large 4

Le même prompt (`pages/26_run_impact.py`) est envoyé 3 fois sur les mêmes lots de 25 fiches.
Modèle : `mistral-large-4`, `reasoning_effort=low`. La valeur `none` est refusée par l'API pour ce modèle.
La température est celle par défaut de l'API.
Ce fichier s'enrichit à chaque nouvelle collectivité :

```bash
python scripts/stabilite_mistral_volet_ges.py <id> [<id> ...]
```

Le bloc « Statistiques » plus bas est recalculé automatiquement. La partie « Analyse » est mise à jour à la main après chaque lot.

## Collectivités traitées

| Date | Collectivités | Fiches | Stables 3/3 |
|---|---|---:|---:|
| 2026-10-30 | CC Creuse Sud Ouest (4111), Bordeaux Métropole (4322), Métropole de Lyon (4999), Le Havre Seine Métropole (5119) | 304 | 167 (55 %) |
| 2026-10-30 | CC Val de Gray (5005), Saint-Jean-de-Braye (1609), CC Sundgau (4973), CC du Pays de Barr (4939), Hélette (13693) | 197 | 127 (64 %) |
| 2026-10-30 | CA Guingamp-Paimpol (4097), CC Pays des Achards (5300), SM SCoT Sambre Avesnois (6030), CC Baugeois Vallée (4637), CA Rochefort Océan (4026), Paris Est Marne & Bois (5390), CA Privas Centre Ardèche (3893), CC Ardennes Thiérache (3914), CC de la Forêt (4576), CC Pays de l'Arbresle (4994), CC Pays de Colombey et Sud Toulois (4707), CC Brionnais Sud Bourgogne (5033) | 1 173 | 628 (54 %) |
| **Cumul** | **21 collectivités** | **1 674** | **922 (55 %)** |

Remarque : 5005, 1609, 4973 et 13693 n'ont aucune classification en prod. Pour elles, seule la stabilité entre runs est mesurée.

## Analyse

### En bref

- **55 % des fiches sont stables**, mais le chiffre est trompeur : 567 fiches ne reçoivent aucun levier dans aucun des 3 runs.
  Parmi les fiches classées au moins une fois (1 107), **seules 355 (32 %) reçoivent exactement la même classification 3 fois**.
- **Le nombre de paires levier × catégorie est le facteur dominant**, et c'est confirmé sur 3 lots et 21 collectivités. La corrélation avec la stabilité vaut −0,59. Elle n'est que de −0,10 pour la longueur de la description.

  | Paires (max sur les 3 runs) | Fiches | Stables |
  |---|---:|---:|
  | 0 | 567 | 100 % |
  | 1 | 442 | 63 % |
  | 2–3 | 435 | 15 % |
  | 4–6 | 162 | 7 % |
  | 7 et plus | 68 | 1 % |

- **La stabilité par collectivité va de 29 % (Bordeaux) à 73 % (Pays des Achards).** Les moins stables sont celles où Mistral classe beaucoup de fiches avec beaucoup de leviers : Baugeois Vallée (35 %), SCoT Sambre Avesnois (38 %), CC de la Forêt (41 %).
  Les fiches sans description, avec le titre seul (3914, 4707, 4973, 5033, 5390), ne sont pas plus stables : entre 42 et 67 %.
- **Même avec une seule paire, le choix n'est pas fiable** : 37 % des fiches à une seule paire changent de levier ou de catégorie entre les runs.
- Répartition des écarts : 30 % ne touchent que les catégories, 28 % sont du tout ou rien, et 42 % concernent un levier présent dans certains runs seulement.
- **Le vote majoritaire ne correspond à la prod que sur 242 des 921 fiches (26 %)** classées d'un côté ou de l'autre, pour les 17 collectivités qui ont une classification en prod.

### M1 — La catégorie 4 « Gouvernance » apparaît et disparaît

C'est le motif n°1 sur les 3 lots : **232 fiches** ont la catégorie 4 dans certains runs seulement pour un même levier, deux fois plus que la catégorie 6 (102).
Le modèle l'ajoute dès que le texte évoque un pilotage, une coopération, une « COP », une feuille de route, des partenaires ou un accompagnement des communes.
Le prompt l'autorise implicitement (« une action peut relever de plusieurs catégories »).

- 4111/46721 « feuille de route EnR » : Electricité renouvelable [4] / [2, 4] / [4]
- 4999/65602 « rénovation énergétique » : [3, 6] / [3, 4, 6] / [3, 6]
- 4973/61654 « appel à projets prévention des déchets » : Prévention [3] / [3, 4] / [3, 4]
- 4637/72504 « développer le solaire au sol » : Electricité renouvelable [2, 4, 6] / [2, 4, 6] / [2, 6]
- 6030/126708 « géothermie » : RCU [6] / [4, 6] / [6]
- 4994/62336 « cahier des charges des ZAE » : Sobriété foncière [2] / [2, 4] / [2]

**Piste :** limiter à une catégorie principale par levier, ou à 2 au maximum. Préciser que la 4 ne s'ajoute que si l'action **crée** une instance, un partenariat formalisé ou un dispositif de suivi, pas si elle en parle seulement.

### M2 — Frontières de catégories que le prompt ne tranche pas

Le prompt donne trois distinctions explicites : 1/5, 2/4 et 3/6. Sur 21 collectivités, les échanges les plus fréquents sont :
4↔6 (38 fiches), 1↔4 (36), 1↔6 (25), 2↔4 (24, alors que la distinction existe), 1↔2 (22) et 1↔5 (14, idem).
**121 fiches à un seul levier** changent de catégorie sans changer de levier. C'est un pur problème de catégorie.

- **4 ou 6 : « accompagner » des acteurs.** 4576/40463 « développer Rezo Pouce » : Covoiturage [4, 6] / [6] / [4, 6]. 5033/57596 « solaire sur bâtiments industriels » : [6] / [4] / [4].
- **Même un financement explicite flotte.** 4994/62311 « financement de panneaux plug & play pour les particuliers » : [3, 6] / [6] / [6]. La catégorie 3 manque dans 2 runs sur 3, alors que le titre dit « financement ».
- **1 ou 2 : programme ou travaux.** 5033/57621 « réduire les tonnages » : Prévention [2] / [1] / [1]. 4111/64535 « réserve foncière » : [1] / [2, 3] / [1].
- **« Former les élus ou les agents » → 4, 5 ou 6.** 4939/88652 et 130868 : [4] / [6] / [4] et [4] / [6] / [6]. 4939/130869 « former les agents » : [5] / [6] / [5].
- **« Expérimenter » un service → 1 ou 4.** 4939/130824 covoiturage : [4] / [1] / [4]. 4939/130825 autopartage : [4] / [1] / [1].
- **Équipement communal ouvert aux habitants → 1 ou 5.** 13693/143345 chaleur renouvelable : [5] / [1] / [1]. 13693/143348 autoconsommation collective : [5] / [1] / [5].

**Piste :** ajouter des distinctions pour 1 vs 2 (étude, programme ou schéma = 2 ; travaux = 1) et pour 4 vs 6 (animer un réseau d'acteurs = 4 ; informer ou conseiller des publics = 6). Ajouter aussi quatre règles : « formation des élus et agents = 5 », « expérimentation d'un service = catégorie du service une fois déployé », « équipement communal partagé avec les habitants = 1 », « toute aide financière versée = 3 ».

### M3 — Fiches « au seuil » : tout ou rien selon le run

**210 fiches (28 % des instables)** reçoivent des leviers dans un run et aucun dans un autre. La règle « en cas de doute, s'abstenir » est appliquée au hasard.
Ce sont des actions **indirectes** : études et diagnostics, programmes habitat, communication, projets alimentaires territoriaux (PAT), restauration collective, coopération, biodiversité et eau, filières économiques, stratégies.

- 4111/63976 « actions du PAT départemental » : 6 leviers agricoles au run 1, rien aux runs 2 et 3
- 3893/78915 « EnR pour le chauffage » : 6 leviers au run 1, rien aux runs 2 et 3
- 3914/76578 « étude pré-opérationnelle OPAH » : 3 leviers résidentiels au run 1, rien ensuite
- 6030/126675 « stratégie mobilité partagée » : 3 leviers [4] / rien / 2 leviers [2]
- 6030/126715 « changements de pratiques agricoles » : 3 leviers / rien / 3 leviers
- 4637/72497 « transport à la demande » : Vélo et TC [3, 4, 6] / rien / [3, 4, 6]
- **Précarité énergétique**, même texte à 1609 et 5005 : tout ou rien dans les deux collectivités
- Restauration collective et Egalim (13693/143324, 1609/16445) : leviers agricoles dans 1 run sur 3
- Diagnostics (4111/63981, 5119/37494, 5005/12605)

**Piste :** donner une règle explicite pour les actions préparatoires (étude, diagnostic, schéma, stratégie, programme). Par exemple : levier retenu seulement si l'action prévoit sa mise en œuvre, sinon objet vide. Ajouter 2 ou 3 exemples de fiches « à vide » dans le prompt.

### M4 — Leviers voisins qui s'échangent ou s'ajoutent au levier principal

Le levier principal est stable, mais un levier voisin apparaît dans 1 ou 2 runs sur 3, ou le remplace.

- **Prévention ↔ Valorisation des déchets**, devenu l'échange n°1 (22 fiches). Le **réemploi**, le prêt, le don et les matériauthèques sont classés tantôt en Prévention, tantôt en Valorisation : 4026/87237 et 87238 Prévention [5] / Valorisation [5] / Prévention [5]. 4576/40588 « réemploi des matériaux du BTP » et 40589 « matériauthèques » : Valorisation / Prévention / Valorisation.
- **Rénovation de l'habitat : les chaudières fioul et gaz vont et viennent** autour de Sobriété résidentielle (45 fiches). PLH, OPAH, PIG, maison de l'habitat et permanences info-énergie reçoivent 3 leviers dans un run, 1 seul dans un autre : 4097/2336, 2338, 3914/76629, 3893/78911.
- **Vélo et TC ↔ Réduction des déplacements** (13 échanges, 85 fiches où Réduction des déplacements est intermittente) : 4322/34960, 34961, 4999/65603, 6030/126679, 126724.
- **La marche à pied n'a pas de levier propre** : elle bascule entre Réduction des déplacements et Vélo et TC (1609/16434 et 5005/12599, même texte ; 13693/143333).
- **Les espaces verts urbains, la gestion différenciée et les zones humides n'ont pas de levier propre** : ils tombent sur Prairies, Pratiques stockantes, Forêts ou Sobriété foncière (4973/53167, 53171, 1609/16437, 4637/72508, 6030/126723). Pratiques stockantes est intermittent sur 76 fiches.
- **Fret ↔ Efficacité logistique** (4 fiches), **Sobriété tertiaire + chaudières tertiaires** (4111/63979, 4999/90525), **TC ou bus + Véhicules électriques** (5119/26093, 26109).

**Piste :** règles de voisinage dans le prompt.
- « Réemploi, réparation, prêt et don = Prévention ; tri, collecte et recyclage = Valorisation. »
- « Rénovation de l'habitat sans mention d'un changement de chauffage = Sobriété résidentielle seule. »
- « Report modal et marche = Vélo et TC ; Réduction des déplacements seulement si l'action réduit le nombre ou la longueur des trajets. »
- « Pratiques stockantes = pratiques agricoles ou sols ; espaces verts et biodiversité urbaine = aucun levier. »

### M5 — Fiches longues et multi-thèmes : chaque run prend un sous-ensemble différent

Les actions « fourre-tout » touchent 4 à 8 leviers plausibles. Chaque run en garde une sélection différente, avec des catégories différentes. Seulement 1 % des fiches à 7 paires ou plus sont stables.

- 4322/34954 « destination durable » : 5, puis 3, puis 2 leviers, presque sans recouvrement
- 4322/34972 « alimentation locale » : 5, puis 3, puis 7 leviers
- 1609/16433 « plan de mobilité » : 6, puis 8, puis 8 leviers, tous en catégorie 2. Le modèle « déplie » le plan sur tous les leviers transport.
- 4637/32311 « aire de captage » : 3 leviers, catégories [3, 6], [2, 4, 6] ou [2, 3, 4, 6] selon le run

**Piste :** plafonner le nombre de leviers par fiche, par exemple aux 3 plus directs.

### M6 — Libellé de levier inventé, toujours le même

5 réponses sur 233 ont inventé **« Sobriété des bâtiments (tertiaire) »**, un mélange de « Sobriété des bâtiments (résidentiel) » et de « Sobriété et isolation des bâtiments (tertiaire) ».
Trois de ces erreurs sont tombées sur le **même lot de 4097**, une fois dans chacun des 3 runs. Ce lot contient « Organiser la transition énergétique du patrimoine public » (2219) et « Accompagner les entreprises du secondaire et du tertiaire » (2340). Certaines fiches déclenchent donc l'erreur presque à coup sûr.
La validation la rattrape à chaque fois. Sans elle, ces fiches perdraient leur levier tertiaire.

**Piste :** renommer le levier tertiaire pour qu'il ait la même forme que le résidentiel, ou donner aux leviers des codes courts (`sobriete_isolation_batiments_tertiaire`) dans le prompt et dans le JSON.

### M7 — Même texte, collectivités différentes : le vote majoritaire ne suffit pas

Saint-Jean-de-Braye (1609) et Val de Gray (5005) partagent 26 fiches au titre et à la description identiques.
Même après le vote majoritaire sur 3 runs, **8 de ces 26 textes (31 %) n'obtiennent pas la même classification** d'une collectivité à l'autre.
Exemples : précarité énergétique, potentiel EnR, biodiversité et espaces verts, stratégie patrimoniale.
Le hasard de génération explique une partie de l'écart. L'autre partie vient des **autres fiches du lot** (voir M8).

### M8 — Contagion entre fiches voisines d'un même lot

Dans **88 cas**, un run donne à une fiche exactement la classification (2 paires ou plus) d'une autre fiche du même lot, alors que les autres runs la classent autrement.
Le plus souvent, ce sont des fiches **consécutives et proches** que le modèle aligne dans un run et pas dans l'autre. C'est le cas de PIG et OPAH (3914/76577 et 76578, 4994/62294 et 62295), de deux fiches covoiturage (4707/51823 et 51824), ou de pistes cyclables et voies vertes (4707/51820 et 51821).
Quelques cas sont de **vraies erreurs d'attribution** :

- 3914/76395 « Réduire la production de déchets » reçoit au run 3 les 4 leviers mobilité [5] de la fiche précédente, « Réduire l'impact des déplacements ».
- 3914/76382 « économie circulaire » et 76383 « revitaliser les centres de villages » reçoivent au run 3 le même bloc de 9 leviers (16 paires). Les deux autres runs leur donnent 2 leviers déchets.
- 5033 run 1 : 5 fiches de communication (3.3.2 à 3.3.7 : aides, réunions publiques, formations, salon de l'habitat) reçoivent toutes la classification de la fiche 3.4.1 « Pacte territorial ».

**Piste :** tester des lots plus petits (5 à 10 fiches) ou un ordre aléatoire des fiches, puis comparer la stabilité. Le lot de 25 réduit le coût, mais rend chaque réponse dépendante de ses voisines. C'est aussi une explication probable de M7.

### Pistes transverses à tester

Elles sont classées par gain attendu et facilité de test.

1. **`temperature=0`** (aujourd'hui, la valeur par défaut de l'API) : c'est le test le plus simple pour mesurer la part du hasard pur.
2. **Des lots plus petits ou mélangés** (M7, M8) : un test sur 2 ou 3 collectivités suffirait.
3. **Une catégorie principale par levier**, ou 2 au maximum : cela réglerait l'essentiel de M1 et M2, qui représentent la moitié des écarts.
4. **Règles de voisinage entre leviers, règles pour les sujets sans levier et règle pour les actions préparatoires** (M3, M4).
5. **Codes courts pour les leviers** (M6).
6. **Vote majoritaire sur 3 runs** en dernier recours. Il ne supprime pas tout l'écart (M7), et il ne s'accorde avec la prod que sur 26 % des fiches classées. La stabilité ne garantit donc pas l'accord avec la prod.

## Statistiques

<!-- AUTO-STATS:START (régénéré par le script, ne pas éditer) -->

_Statistiques recalculées le 2026-10-30 16:16 sur 21 collectivités : Hélette (13693), Saint-Jean-de-Braye (1609), CA Privas Centre Ardèche (3893), CC Ardennes Thiérache (3914), CA Rochefort Océan (4026), CA Guingamp-Paimpol Agglomération de l'Armor à l'Argoat (4097), CC Creuse Sud Ouest (4111), Bordeaux Métropole (4322), CC de la Forêt (4576), CC Baugeois Vallée (4637), CC du Pays de Colombey et du Sud Toulois (4707), CC du Pays de Barr (4939), CC Sundgau (4973), CC du Pays de l'Arbresle (CCPA) (4994), Métropole de Lyon (4999), CC Val de Gray (5005), CC Brionnais Sud Bourgogne (5033), Le Havre Seine Métropole (5119), CC du Pays des Achards (5300), Paris Est Marne & Bois (5390), SM du SCoT Sambre Avesnois (6030)._

- Fiches analysées : **1674**, instables : **752** (45%)

### Types d'écart (fiches instables)

| Type | Fiches | Part des instables |
|---|---:|---:|
| Classée dans certains runs, aucun levier dans d'autres | 210 | 28% |
| Levier présent dans certains runs seulement | 181 | 24% |
| Levier intermittent et catégories instables | 139 | 18% |
| Mêmes leviers, catégories différentes | 222 | 30% |

### Leviers les plus intermittents (fiches où le levier n'apparaît pas dans tous les runs)

| Levier | Fiches |
|---|---:|
| Prévention des déchets | 89 |
| Réduction des déplacements | 85 |
| Pratiques stockantes | 76 |
| Valorisation matière des déchets | 71 |
| Vélo et transport en commun | 55 |
| Sobriété et isolation des bâtiments (tertiaire) | 49 |
| Changement chaudières fioul + rénovation (résidentiel) | 45 |
| Changement chaudières gaz + rénovation (résidentiel) | 44 |
| Sobriété des bâtiments (résidentiel) | 40 |
| Electricité renouvelable | 30 |
| Gestion des forêts et produits bois | 26 |
| Sobriété foncière | 24 |

### Leviers stables mais dont les catégories changent

| Levier | Fiches |
|---|---:|
| Prévention des déchets | 59 |
| Electricité renouvelable | 42 |
| Sobriété des bâtiments (résidentiel) | 36 |
| Valorisation matière des déchets | 36 |
| Vélo et transport en commun | 31 |
| Pratiques stockantes | 29 |
| Réduction des déplacements | 27 |
| Gestion des forêts et produits bois | 23 |
| Sobriété et isolation des bâtiments (tertiaire) | 22 |
| Covoiturage | 21 |
| Réseaux de chaleur décarbonés | 20 |
| Sobriété foncière | 19 |

### Catégories ajoutées ou retirées selon le run (même levier)

| Catégorie | Fiches |
|---|---:|
| 4 Gouvernance | 232 |
| 6 Sensibilisation | 102 |
| 1 Aménagement | 86 |
| 3 Financement | 74 |
| 2 Planification | 60 |
| 5 Exemplarité | 31 |

### Catégories échangées entre runs (même levier)

| Échange | Fiches |
|---|---:|
| 4 Gouvernance ↔ 6 Sensibilisation | 38 |
| 1 Aménagement ↔ 4 Gouvernance | 36 |
| 1 Aménagement ↔ 6 Sensibilisation | 25 |
| 2 Planification ↔ 4 Gouvernance | 24 |
| 1 Aménagement ↔ 2 Planification | 22 |
| 2 Planification ↔ 6 Sensibilisation | 15 |
| 1 Aménagement ↔ 5 Exemplarité | 14 |
| 3 Financement ↔ 4 Gouvernance | 13 |
| 3 Financement ↔ 6 Sensibilisation | 13 |
| 2 Planification ↔ 3 Financement | 12 |
| 4 Gouvernance ↔ 5 Exemplarité | 7 |
| 5 Exemplarité ↔ 6 Sensibilisation | 7 |

### Leviers échangés entre runs (un run met A, un autre B)

| Échange | Fiches |
|---|---:|
| Prévention des déchets ↔ Valorisation matière des déchets | 22 |
| Réduction des déplacements ↔ Vélo et transport en commun | 13 |
| Efficacité et sobriété logistique ↔ Fret décarboné et multimodalité | 4 |
| Gestion des prairies ↔ Pratiques stockantes | 4 |
| Gestion des forêts et produits bois ↔ Pratiques stockantes | 3 |
| Valorisation matière des déchets ↔ Vélo et transport en commun | 3 |
| Efficacité et sobriété logistique ↔ Réduction des déplacements | 3 |
| Réduction des déplacements ↔ Sobriété et isolation des bâtiments (tertiaire) | 3 |
| Bus et cars décarbonés ↔ Vélo et transport en commun | 3 |
| Pratiques stockantes ↔ Sobriété foncière | 2 |
| Gestion des forêts et produits bois ↔ Sobriété foncière | 2 |
| Sobriété des bâtiments (résidentiel) ↔ Sobriété foncière | 2 |

<!-- AUTO-STATS:END -->
