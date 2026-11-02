# Stabilité Mistral Large 4 — classification volet GES

Modèle `mistral-small-2603`, raisonnement `none`, température par défaut de l'API. Prompt v2 (`prompts/classification_volet_ges_v2.md`), une fiche par appel, codes de leviers et JSON contraint, 3 runs indépendants. Lecture seule sur la prod.

Mis à jour le 2026-11-02 13:10.

## Synthèse

| Collectivité | Fiches | Stables | Instables | % stable | Paires 3/3 | Majorité = prod |
|---|---:|---:|---:|---:|---:|---:|
| CC Ardennes Thiérache (3914) | 104 | 86 | 18 | 83% | 81/121 | 10/47 |
| CC Sundgau (4973) | 37 | 27 | 10 | 73% | 27/44 | non classée en prod |
| CC Brionnais Sud Bourgogne (5033) | 111 | 94 | 17 | 85% | 62/90 | 18/66 |
| Paris Est Marne & Bois (5390) | 141 | 124 | 17 | 88% | 79/111 | 16/71 |
| **Total** | **393** | **331** | **62** | **84%** | | |

« Paires 3/3 » : paires levier × catégorie données par les 3 runs, sur toutes les paires proposées au moins une fois.

## CC Ardennes Thiérache (3914)

- Fiches : **104** — stables sur les 3 runs : **86** (83%), instables : **18**
- Paires levier × catégorie distinctes proposées : 121 — 3/3 runs : 81, 2/3 runs : 17, 1/3 runs : 23
- Vote majoritaire = prod : 10/47 fiches classées d'un côté ou de l'autre
- Réponses JSON invalides rejouées : 0
- Appels : 312 — tokens d'entrée 1 684 353 (dont 1 641 417 en cache, 97%), sortie 7 194 — coût estimé 0.26 $ pour les 3 runs
- Date : 2026-11-02 13:10

### Classée dans certains runs, aucun levier dans d'autres (5)

#### Fiche 76386 — Renforcer le lien entre les producteurs, les transformateurs, les distributeurs

- **Run 1 :** Efficacité et sobriété logistique [6] | Prévention des déchets [6]
- **Run 2 :** (aucun levier)
- **Run 3 :** Efficacité et sobriété logistique [3, 6] | Prévention des déchets [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Efficacité et sobriété logistique (2/3), Prévention des déchets (2/3)

> <p>•Mutualiser des installations qui pourraient bénéficier à plusieurs acteurs (exemple : Albatros 08 possèdent un autoclave qui permet de valoriser les invendus des maraîchers)</p><p>•</p><p><strong>Association L’Environnement D’Abord (LEDA)</strong></p><p>•Agrandir le réseau des producteurs impliqués, devenir la structure coordinatrice de la distribution en circuit court sur le territoire</p><p>•Chambre d’Agriculture : les accompagner et les aider à associer le plus possible de producteurs lo…

#### Fiche 76389 — Soutenir les projets citoyens et participatifs

- **Run 1 :** (aucun levier)
- **Run 2 :** Electricité renouvelable [4, 6]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Electricité renouvelable (1/3)

> <p><em>La démarche PCAET portée nécessite d’être menée avec les différents acteurs (institutionnels, associatifs, économiques, …). Certains de ces partenaires et plusieurs citoyens se sont investis dans la phase d’élaboration du plan, en étant présents aux réunions de concertation. Néanmoins, la faible participation citoyenne constatée lors des réunions publiques montre une faible implication des habitants dans l’élaboration du PCAET. Forte de ce constat, les Communautés entendent renforcer l’a…

#### Fiche 76397 — Soutenir une alimentation locale et à faible empreinte carbone dans la restauration collective

- **Run 1 :** (aucun levier)
- **Run 2 :** Elevage durable [6] | Prévention des déchets [1, 6]
- **Run 3 :** (aucun levier)
- **Prod :** Prévention des déchets [3, 5, 6]
- Leviers intermittents : Elevage durable (1/3), Prévention des déchets (1/3)

> <p><strong>Mettre en place une cuisine centrale approvisionnée en circuit-court (PAT)</strong></p><p>-Projet validé, sera réalisé à Auvillers-les-Forges</p><p>-Fournir les établissements scolaires, les maisons de retraite, les personnes isolées (700 repas/jour)</p><p>-</p><p><strong>Mettre en place des critères sur l'empreinte carbone des repas servis dans la restauration collective</strong></p><p>-Compter et afficher systématique le "contenu carbone" des repas servis</p><p>-Réduire la quantité…

#### Fiche 76549 — Mise en place d'une ORT

- **Run 1 :** (aucun levier)
- **Run 2 :** (aucun levier)
- **Run 3 :** Sobriété foncière [2]
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété foncière (1/3)

#### Fiche 76577 — PIG

- **Run 1 :** (aucun levier)
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [2, 3] | Changement chaudières gaz + rénovation (résidentiel) [2, 3]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (1/3), Changement chaudières gaz + rénovation (résidentiel) (1/3)

### Levier présent dans certains runs seulement (3)

#### Fiche 76375 — Renforcer l’attractivité et la qualité des services de transports en commun

- **Run 1 :** Vélo et transport en commun [1]
- **Run 2 :** Covoiturage [1] | Vélo et transport en commun [1]
- **Run 3 :** Vélo et transport en commun [1]
- **Prod :** Vélo et transport en commun [1, 2, 4]
- Leviers intermittents : Covoiturage (1/3)

> <p><strong>1. Améliorer la desserte du territoire en transports en commun en ajoutant des arrêts sur les lignes traversant le territoire</strong></p><p>Un arrêt a été réalisé à Auvillers-les-Forges (hameau de Mon Idée) sur la ligne de bus Charleville - Hirson (gérée par la SNCF)</p><p><strong>2. Améliorer la flexibilité des bus qui traversent le territoire sans s'y arrêter.</strong></p><p>Un passager devrait pouvoir descendre du car/bus même en dehors des arrêts lorsque celui-ci est peu emprunt…

#### Fiche 76382 — Soutenir le développement des filières de l’économie circulaire

- **Run 1 :** Covoiturage [1] | Prévention des déchets [6] | Vélo et transport en commun [1]
- **Run 2 :** Covoiturage [1] | Prévention des déchets [6] | Vélo et transport en commun [1]
- **Run 3 :** Covoiturage [1] | Prévention des déchets [6] | Sobriété des bâtiments (résidentiel) [2, 3]
- **Prod :** Covoiturage [1] | Prévention des déchets [2, 4] | Réduction des déplacements [1, 2, 4] | Véhicules électriques [1] | Vélo et transport en commun [1]
- Leviers intermittents : Sobriété des bâtiments (résidentiel) (1/3), Vélo et transport en commun (2/3)

> <p><strong>Mettre en place des projets de revitalisation dans le cadre des ORT (5 communes) et du dispositif Petites Villes de Demain (Signy-le-Petit)</strong></p><p>Exemples d'actions</p><p>-Fédérer les commerçants</p><p>-Développer des cafés multiservices</p><p>-Mettre en place des IRVE, des stationnements vélos, des aires de covoiturage,</p><p>-Maintenir le commerce existant</p><p>-Vitrophanie</p><p>-Lutter contre le logement vacant</p><p>-OPAH</p><p>-THLV</p><p>-Rénovation du bâti ancien</p…

#### Fiche 76575 — Mise en place du tri des biodéchets

- **Run 1 :** Prévention des déchets [2] | Valorisation matière des déchets [2]
- **Run 2 :** Prévention des déchets [2]
- **Run 3 :** Prévention des déchets [2]
- **Prod :** Valorisation matière des déchets [1]
- Leviers intermittents : Valorisation matière des déchets (1/3)

### Levier intermittent et catégories instables (2)

#### Fiche 76372 — Soutenir le développement des mobilités actives

- **Run 1 :** Véhicules électriques [1, 6] | Vélo et transport en commun [2, 6]
- **Run 2 :** Véhicules électriques [1, 6] | Vélo et transport en commun [1, 6]
- **Run 3 :** Vélo et transport en commun [1, 2, 6]
- **Prod :** Véhicules électriques [1, 6] | Vélo et transport en commun [1, 2, 6]
- Leviers intermittents : Véhicules électriques (2/3)
- Catégories instables sur : Vélo et transport en commun

> <p><strong>Mettre en place un Schéma Directeur Cyclable à l'échelle de la CCAT</strong></p><p><em>Action engagée dans le cadre de l'Appel à Projet AVELO2 : la CCAT est lauréate</em></p><p>Travailler en particulier :</p><p>-au raccordement à la voie verte départementale (Eurovéloroute 19) à Hirson (Eurovéloroute 3) (doit constituer l'axe dorsal du réseau cyclable du territoire)</p><p>-à la desserte des écoles, services publics, médecins, commerces, pharmacies, etc.</p><p>-à la reconversion de la…

#### Fiche 76388 — Structurer une filière de valorisation du bois

- **Run 1 :** Gestion des forêts et produits bois [4, 6] | Réseaux de chaleur décarbonés [6]
- **Run 2 :** Gestion des forêts et produits bois [4, 6] | Réseaux de chaleur décarbonés [6]
- **Run 3 :** Gestion des forêts et produits bois [3, 4]
- **Prod :** Gestion des forêts et produits bois [1, 3, 4]
- Leviers intermittents : Réseaux de chaleur décarbonés (2/3)
- Catégories instables sur : Gestion des forêts et produits bois

> <p><em>Dans les 6 prochaines années, des volumes très importants seront à traiter sachant que la forêt ne pourra produire davantage notamment avec le changement climatique au-delà de 10 - 20 ans.</em></p><p>•Relocaliser la filière via contrats d’approvisionnement avec l’ONF</p><p>•Soutenir l’installation d’ETF (Entreprises de Travaux Forestiers) sur le territoire pour répondre au besoin de main d’œuvre de l’ONF (si ces entreprises sont prêtes à s’installer, l’ONF peut leur garantir de l’activit…

### Mêmes leviers, catégories différentes (8)

#### Fiche 76369 — Mettre en place des rénovations énergétiques sur le bâti public

- **Run 1 :** Changement de chaudière à fioul (tertiaire) [2, 3] | Changement de chaudière à gaz (tertiaire) [2, 3] | Sobriété et isolation des bâtiments (tertiaire) [2, 3]
- **Run 2 :** Changement de chaudière à fioul (tertiaire) [2] | Changement de chaudière à gaz (tertiaire) [2] | Sobriété et isolation des bâtiments (tertiaire) [2]
- **Run 3 :** Changement de chaudière à fioul (tertiaire) [2, 3] | Changement de chaudière à gaz (tertiaire) [2, 3] | Sobriété et isolation des bâtiments (tertiaire) [2, 3]
- **Prod :** Changement de chaudière à fioul (tertiaire) [5] | Changement de chaudière à gaz (tertiaire) [5] | Sobriété et isolation des bâtiments (tertiaire) [5]
- Catégories instables sur : Changement de chaudière à fioul (tertiaire), Changement de chaudière à gaz (tertiaire), Sobriété et isolation des bâtiments (tertiaire)

> <p>La communauté de communes dispose d’un parc de bâtiment de 26 000 m² dont de nombreux bâtiments publics et logements. Les 37 communes qui component Ardennes Thiérache possèdent environ 200 bâtiments publics (logements, mairies, salles communales, …) qui ont pour la plupart plus de 20 ans et sont de gros consommateurs d'énergies fossiles.</p><p>L'objectif est de pouvoir accompagner les communes dans leurs études et travaux de rénovation.</p><p><strong>Avancement de l’action :</strong></p><p>E…

#### Fiche 76376 — Réduire les besoins de déplacements en développant des services de proximité

- **Run 1 :** Réduction des déplacements [1]
- **Run 2 :** Réduction des déplacements [1]
- **Run 3 :** Réduction des déplacements [1, 2]
- **Prod :** Réduction des déplacements [1, 4]
- Catégories instables sur : Réduction des déplacements

> <p><em>Avoir accès à plus de services de proximité permet de réduire les déplacements des habitants du territoire et ainsi de réduire la consommation d’énergie et les émissions de gaz à effet de serre associées.</em></p><p><strong>Mesures initiées et perspectives :</strong></p><p>•Développer des services en ligne pour les habitants liés aux compétences (urbanisme, eau-assainissement, etc.…)</p><p>•Aménager une nouvelle Maison France Service en lien avec les services de la Communauté de Communes…

#### Fiche 76390 — Développer une centrale photovoltaïque

- **Run 1 :** Electricité renouvelable [1, 2]
- **Run 2 :** Electricité renouvelable [1, 2, 3, 4]
- **Run 3 :** Electricité renouvelable [1, 2, 3, 4, 6]
- **Prod :** Electricité renouvelable [1, 4]
- Catégories instables sur : Electricité renouvelable

> <p><em>Le Département des Ardennes équipe le site de l‘ancienne base de OTAN à Regniowez avec une centrale photovoltaïque au sol (28,6 MWc, 23 ha de pistes).</em></p><p><em>L'entreprise CVE Groupe a été retenue suite à un appel à projets en 2020 pour une durée de 40 ans.</em></p><p><strong>Intégration de critères environnementaux et sociaux :</strong></p><p>•Pas de changement de nature de sol (uniquement sur les pistes),</p><p>•Gestion des zones naturelle sera confiée au Conservatoire d'espaces…

#### Fiche 76391 — Accompagner les communes et la CCAT sur le développement des EnR (évaluation d’opportunités sur leur patrimoine et évaluation des projets photovoltaïques portés par des développeurs privés )

- **Run 1 :** Electricité renouvelable [4, 6] | Réseaux de chaleur décarbonés [4]
- **Run 2 :** Electricité renouvelable [2, 6] | Réseaux de chaleur décarbonés [4]
- **Run 3 :** Electricité renouvelable [4, 6] | Réseaux de chaleur décarbonés [4]
- **Prod :** Electricité renouvelable [4, 6]
- Catégories instables sur : Electricité renouvelable

> <p><strong>Hypothèse 1 : Création d’une structure intercommunale participative pour la mise en œuvre d’un réseau de chaleur sur la commune de Maubert Fontaine</strong></p><p><strong>Hypothèse 2 : Travailler avec l’ALE 08 à travers le dispositif Générateurs (solaire photovoltaïque) :</strong></p><p>L'ALE 08 fait partie du dispositif Les GÉnÉRATEURS :</p><p>Ce dispositif co-finance des acteurs qui peuvent intervenir auprès des communes dès l’émergence d’un projet photovoltaïque, que la commune so…

#### Fiche 76392 — Être exemplaire dans la gestion de l'énergie des bâtiments de la collectivité

- **Run 1 :** Changement de chaudière à fioul (tertiaire) [5] | Changement de chaudière à gaz (tertiaire) [5] | Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 2 :** Changement de chaudière à fioul (tertiaire) [5] | Changement de chaudière à gaz (tertiaire) [5] | Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 3 :** Changement de chaudière à fioul (tertiaire) [5] | Changement de chaudière à gaz (tertiaire) [5] | Sobriété et isolation des bâtiments (tertiaire) [5, 6]
- **Prod :** Changement de chaudière à fioul (tertiaire) [3, 5] | Changement de chaudière à gaz (tertiaire) [3, 5] | Sobriété et isolation des bâtiments (tertiaire) [5, 6]
- Catégories instables sur : Sobriété et isolation des bâtiments (tertiaire)

> <p>Pistes de travail :</p><p>-Ne plus avoir de bâtiments ou de pièces surchauffés</p><p>-En cours dans les bâtiments scolaires et les COSEC</p><p>-Installer des robinets thermostatique (dispositif CEE, financé)</p><p>-Fournir aux agents des vestes pour permettre de baisser la température de consigne dans les bâtiments (fait)</p><p>-Remplacer les systèmes de chauffage gaz/fioul des bâtiments les plus énergivores</p><p>-Installer des chauffages mutualisés sur plusieurs équipements, alimentés par …

#### Fiche 76393 — Minimiser l'impact environnemental lié aux travaux de la collectivité

- **Run 1 :** Changement de chaudière à fioul (tertiaire) [2] | Changement de chaudière à gaz (tertiaire) [2] | Sobriété et isolation des bâtiments (tertiaire) [2]
- **Run 2 :** Changement de chaudière à fioul (tertiaire) [2] | Changement de chaudière à gaz (tertiaire) [2] | Sobriété et isolation des bâtiments (tertiaire) [2, 3]
- **Run 3 :** Changement de chaudière à fioul (tertiaire) [2, 3] | Changement de chaudière à gaz (tertiaire) [2, 3] | Sobriété et isolation des bâtiments (tertiaire) [2, 3]
- **Prod :** (aucun levier)
- Catégories instables sur : Changement de chaudière à fioul (tertiaire), Changement de chaudière à gaz (tertiaire), Sobriété et isolation des bâtiments (tertiaire)

> <p><strong>Garantir que les bâtiments neufs soient performants énergétiquement</strong></p><p>-Réglementation RE2020</p><p>-Intégrer des critères sur la conception bioclimatique (en réflexion pour la construction de l'école à Maubert ?)</p><p><strong>Inclure dans les marchés publics des critères sur l'empreinte carbone des travaux</strong></p><p>-Privilégier des matériaux bio-sourcés (bois, chanvre, liège, paille, …)</p><p>-Faire appel à des artisans certifiés RGE</p><p><strong>A minima, demand…

#### Fiche 76394 — Réduire l'impact environnemental lié aux déplacements des agents

- **Run 1 :** Covoiturage [5] | Véhicules électriques [5] | Vélo et transport en commun [5]
- **Run 2 :** Covoiturage [5] | Véhicules électriques [5] | Vélo et transport en commun [5]
- **Run 3 :** Covoiturage [5] | Véhicules électriques [5] | Vélo et transport en commun [1, 5]
- **Prod :** Covoiturage [4, 5] | Réduction des déplacements [4, 5] | Véhicules électriques [4, 5] | Vélo et transport en commun [1, 5]
- Catégories instables sur : Vélo et transport en commun

> <p>Optimiser la flotte de véhicules de la collectivité Prolonger la durée de vie des véhicules Interroger les besoins pour réduire au minimum la taille de la flotte nécessaire Lors de l'achat de véhicules, privilégier des véhicules électriques, d'occasion, de faible puissance</p><p>Mise en place d’une étude territoriale sur le verdissement de la flotte de véhicules des EPCI. Combien de véhicules électriques dans la flotte de la CCAT aujourd’hui ? 2 Quels objectifs ?</p><p>Mettre en place un Pla…

#### Fiche 76396 — Réduire l’impact environnemental lié au numérique

- **Run 1 :** Prévention des déchets [5, 6]
- **Run 2 :** Prévention des déchets [5, 6]
- **Run 3 :** Prévention des déchets [5]
- **Prod :** (aucun levier)
- Catégories instables sur : Prévention des déchets

> <p><strong>Prolonger la durée de vie du parc informatique</strong></p><p>Charte d’utilisation / bonnes pratiques</p><p><strong>Mettre en place des critères exigeants sur la part de produits reconditionnés et/ou de seconde main dans les équipements informatiques et numériques</strong></p><p>-Définir des critères plus exigeants que la réglementation ?</p><p><strong>Donner une seconde vie au matériel et équipements informatiques obsolètes</strong></p><p>-Ordinateurs vieillissants donnés à Bell'Occ…

## CC Sundgau (4973)

- Fiches : **37** — stables sur les 3 runs : **27** (73%), instables : **10**
- Paires levier × catégorie distinctes proposées : 44 — 3/3 runs : 27, 2/3 runs : 5, 1/3 runs : 12
- Aucune classification en prod pour cette collectivité
- Réponses JSON invalides rejouées : 0
- Appels : 111 — tokens d'entrée 597 111 (dont 587 489 en cache, 98%), sortie 2 507 — coût estimé 0.09 $ pour les 3 runs
- Date : 2026-11-02 13:10

### Classée dans certains runs, aucun levier dans d'autres (6)

#### Fiche 42055 — Mobiliser les citoyen.ne.s dans le processus de décision sur les sujets de planification écologique

- **Run 1 :** (aucun levier)
- **Run 2 :** (aucun levier)
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [4] | Changement chaudières gaz + rénovation (résidentiel) [4] | Sobriété foncière [4]
- **Prod :** (aucun levier)
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (1/3), Changement chaudières gaz + rénovation (résidentiel) (1/3), Sobriété foncière (1/3)

> Organiser de façon régulière des groupes de travail et des dispositifs participatifs variés faisant participer les citoyen.ne.s sur les sujets de la planification écologique locale.\n

#### Fiche 53164 — diffuser le savoir-faire des éco-jardiniers du Sundgau

- **Run 1 :** (aucun levier)
- **Run 2 :** Prévention des déchets [6]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Prévention des déchets (1/3)

#### Fiche 61675 — Aménager les espaces verts en intégrant de matières réemployées

- **Run 1 :** Prévention des déchets [1]
- **Run 2 :** Prévention des déchets [1]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Prévention des déchets (2/3)

#### Fiche 61677 — Créer un document d'aide à l'organisation d'une éco-manifestation

- **Run 1 :** (aucun levier)
- **Run 2 :** Prévention des déchets [6]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Prévention des déchets (1/3)

#### Fiche 61679 — Organiser des sessions d'information et formation pour les maîtres d'ouvrages

- **Run 1 :** Prévention des déchets [6]
- **Run 2 :** (aucun levier)
- **Run 3 :** Prévention des déchets [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Prévention des déchets (2/3)

#### Fiche 61680 — Mettre en lumière des projets exemplaires en matière de réemploi et recyclage

- **Run 1 :** (aucun levier)
- **Run 2 :** Prévention des déchets [6]
- **Run 3 :** Prévention des déchets [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Prévention des déchets (2/3)

### Levier présent dans certains runs seulement (2)

#### Fiche 42053 — Réaliser des achats durables via la commande publique

- **Run 1 :** Electricité renouvelable [5] | Prévention des déchets [5] | Véhicules électriques [5]
- **Run 2 :** Electricité renouvelable [5] | Prévention des déchets [5]
- **Run 3 :** Electricité renouvelable [5] | Prévention des déchets [5] | Valorisation matière des déchets [5]
- **Prod :** (aucun levier)
- Leviers intermittents : Valorisation matière des déchets (1/3), Véhicules électriques (1/3)

> Mobiliser la commande publique pour réaliser des achats durables sur l'ensemble des produits, bien et services gérés par la collectivité. Contenu à aborder : favoriser les achats de proximité / réduire les déchets d'emballage via la commande publique / Inclure le critère de consommation énergétique dans les choix de matériels informatiques / stopper les achats non équitables ou non éthiques, intégrer dans les marchés publics des critères d'efficacité énergétique, de réduction de l'impact enviro…

#### Fiche 42056 — Identifier les personnes référentes sur les principaux sujets de la planification écologique

- **Run 1 :** Réduction des déplacements [4] | Sobriété foncière [4] | Vélo et transport en commun [4]
- **Run 2 :** Sobriété foncière [4]
- **Run 3 :** Sobriété foncière [4]
- **Prod :** (aucun levier)
- Leviers intermittents : Réduction des déplacements (1/3), Vélo et transport en commun (1/3)

> Les personnes référentes sur les sujets prioritaires (sur lesquels la collectivité dispose des compétences) sont identifiés et constituent une équipe projet qui échange facilement et régulièrement de façon transversale pour mener à bien les actions programmées.\n

### Levier intermittent et catégories instables (1)

#### Fiche 42050 — Mettre en place une politique de mobilité alternative des agents et des élu.e.s

- **Run 1 :** Covoiturage [5, 6] | Efficacité et carburants décarbonés des véhicules privés [5] | Vélo et transport en commun [5, 6]
- **Run 2 :** Efficacité et carburants décarbonés des véhicules privés [5] | Véhicules électriques [5] | Vélo et transport en commun [5, 6]
- **Run 3 :** Covoiturage [5, 6] | Efficacité et carburants décarbonés des véhicules privés [3, 5] | Vélo et transport en commun [5, 6]
- **Prod :** (aucun levier)
- Leviers intermittents : Covoiturage (2/3), Véhicules électriques (1/3)
- Catégories instables sur : Efficacité et carburants décarbonés des véhicules privés

> Mettre en place une politique de mobilité alternative des agents et des élu.e.s, visant le changement de comportement, en adoptant une approche diversifiée pour couvrir tant les déplacements professionnels que ceux domicile-travail. Cette politique devrait inclure l'optimisation et le renouvellement de la flotte de véhicules, une gestion optimisée des déplacements, le développement de l'usage du vélo, des campagnes de communication et de sensibilisation, ainsi que la promotion des transports co…

### Mêmes leviers, catégories différentes (1)

#### Fiche 61676 — Créer un "appartement du futur et du réemploi" à visée pédagogique

- **Run 1 :** Prévention des déchets [1]
- **Run 2 :** Prévention des déchets [1]
- **Run 3 :** Prévention des déchets [1, 6]
- **Prod :** (aucun levier)
- Catégories instables sur : Prévention des déchets

## CC Brionnais Sud Bourgogne (5033)

- Fiches : **111** — stables sur les 3 runs : **94** (85%), instables : **17**
- Paires levier × catégorie distinctes proposées : 90 — 3/3 runs : 62, 2/3 runs : 12, 1/3 runs : 16
- Vote majoritaire = prod : 18/66 fiches classées d'un côté ou de l'autre
- Réponses JSON invalides rejouées : 0
- Appels : 333 — tokens d'entrée 1 780 083 (dont 1 752 485 en cache, 98%), sortie 6 778 — coût estimé 0.27 $ pour les 3 runs
- Date : 2026-11-02 13:10

### Classée dans certains runs, aucun levier dans d'autres (9)

#### Fiche 57534 — 1.1.1 Former les élus et agents sur les thématiques climat air énergie et économie circulaire

- **Run 1 :** (aucun levier)
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [5] | Changement chaudières gaz + rénovation (résidentiel) [5] | Sobriété des bâtiments (résidentiel) [5]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (1/3), Changement chaudières gaz + rénovation (résidentiel) (1/3), Sobriété des bâtiments (résidentiel) (1/3)

> A compléter

#### Fiche 57553 — 2.3.2 Travailler en collaboration avec le SYDESL sur leur SDIRVE

- **Run 1 :** (aucun levier)
- **Run 2 :** Véhicules électriques [4]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Véhicules électriques (1/3)

#### Fiche 57564 — 3.1.5 Réaliser un groupement de commandes pour les DPE manquants

- **Run 1 :** (aucun levier)
- **Run 2 :** Sobriété et isolation des bâtiments (tertiaire) [2]
- **Run 3 :** Sobriété et isolation des bâtiments (tertiaire) [2]
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété et isolation des bâtiments (tertiaire) (2/3)

#### Fiche 57575 — 3.3.5 Informer les habitants sur des éco-conceptions exemplaires de la région, des retours d'expériences avant/après rénovation, visites

- **Run 1 :** Sobriété des bâtiments (résidentiel) [6]
- **Run 2 :** (aucun levier)
- **Run 3 :** Sobriété des bâtiments (résidentiel) [6]
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6]
- Leviers intermittents : Sobriété des bâtiments (résidentiel) (2/3)

#### Fiche 57590 — 4.4.2 Inciter financièrement les habitants à la récupération des eaux de pluie

- **Run 1 :** (aucun levier)
- **Run 2 :** Prévention des déchets [6]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Prévention des déchets (1/3)

#### Fiche 57598 — 5.1.6 Communiquer sur le cadastre solaire du SYDESL

- **Run 1 :** (aucun levier)
- **Run 2 :** (aucun levier)
- **Run 3 :** Electricité renouvelable [2]
- **Prod :** (aucun levier)
- Leviers intermittents : Electricité renouvelable (1/3)

#### Fiche 57599 — 5.1.7 Etudier les risques et impacts des installations agrivoltaïques

- **Run 1 :** Electricité renouvelable [2]
- **Run 2 :** Electricité renouvelable [2]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Electricité renouvelable (2/3)

#### Fiche 57624 — 6.5.1 Relancer le "STOP PUB"

- **Run 1 :** Prévention des déchets [6]
- **Run 2 :** Prévention des déchets [6]
- **Run 3 :** (aucun levier)
- **Prod :** Prévention des déchets [2, 6]
- Leviers intermittents : Prévention des déchets (2/3)

#### Fiche 57640 — 7.3.6 Organiser des ateliers (compostage, Do it yourself, cuisine éco-responable…)

- **Run 1 :** Prévention des déchets [6]
- **Run 2 :** (aucun levier)
- **Run 3 :** (aucun levier)
- **Prod :** Prévention des déchets [6] | Valorisation matière des déchets [6]
- Leviers intermittents : Prévention des déchets (1/3)

### Levier présent dans certains runs seulement (3)

#### Fiche 57555 — 2.3.4 Améliorer la mise à dispo de vélo électrique pour le tourisme

- **Run 1 :** Véhicules électriques [1] | Vélo et transport en commun [1]
- **Run 2 :** Vélo et transport en commun [1]
- **Run 3 :** Vélo et transport en commun [1]
- **Prod :** Vélo et transport en commun [1]
- Leviers intermittents : Véhicules électriques (1/3)

#### Fiche 57583 — 4.2.1 Mettre en place un suivi des consommations dans les bâtiments publics

- **Run 1 :** Sobriété des bâtiments (résidentiel) [5]
- **Run 2 :** Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 3 :** Sobriété des bâtiments (résidentiel) [5]
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété des bâtiments (résidentiel) (2/3), Sobriété et isolation des bâtiments (tertiaire) (1/3)

#### Fiche 57614 — 6.1.1 Elaborer un PLPDMA

- **Run 1 :** Prévention des déchets [2] | Valorisation matière des déchets [2]
- **Run 2 :** Prévention des déchets [2]
- **Run 3 :** Prévention des déchets [2]
- **Prod :** (aucun levier)
- Leviers intermittents : Valorisation matière des déchets (1/3)

> En collaboration avec les autres EPCI et le SMEVOM

### Levier intermittent et catégories instables (1)

#### Fiche 57594 — 5.1.2 Systématiser le photovoltaïque en toiture sur les constructions (voire rénovation) de bâtiments publics

- **Run 1 :** Electricité renouvelable [1, 5]
- **Run 2 :** Electricité renouvelable [1, 5]
- **Run 3 :** Changement de chaudière à fioul (tertiaire) [2] | Changement de chaudière à gaz (tertiaire) [2] | Electricité renouvelable [2]
- **Prod :** Electricité renouvelable [5]
- Leviers intermittents : Changement de chaudière à fioul (tertiaire) (1/3), Changement de chaudière à gaz (tertiaire) (1/3)
- Catégories instables sur : Electricité renouvelable

### Mêmes leviers, catégories différentes (4)

#### Fiche 57562 — 3.1.3 Inciter les communes qui ne l'ont pas fait à réaliser un diagnostic énergétique de leurs bâtiments publics

- **Run 1 :** Sobriété et isolation des bâtiments (tertiaire) [2, 6]
- **Run 2 :** Sobriété et isolation des bâtiments (tertiaire) [6]
- **Run 3 :** Sobriété et isolation des bâtiments (tertiaire) [2, 6]
- **Prod :** (aucun levier)
- Catégories instables sur : Sobriété et isolation des bâtiments (tertiaire)

#### Fiche 57566 — 3.1.7 Etudier la possibilité de grouper les achats de combustibles des 3 CC

- **Run 1 :** Changement de chaudière à fioul (tertiaire) [3] | Changement de chaudière à gaz (tertiaire) [3]
- **Run 2 :** Changement de chaudière à fioul (tertiaire) [3] | Changement de chaudière à gaz (tertiaire) [3]
- **Run 3 :** Changement de chaudière à fioul (tertiaire) [2] | Changement de chaudière à gaz (tertiaire) [2]
- **Prod :** (aucun levier)
- Catégories instables sur : Changement de chaudière à fioul (tertiaire), Changement de chaudière à gaz (tertiaire)

#### Fiche 57586 — 4.2.4 Mettre en place une tarification incitant à la réduction de la consommation d'eau

- **Run 1 :** Prévention des déchets [3]
- **Run 2 :** Prévention des déchets [3]
- **Run 3 :** Prévention des déchets [2]
- **Prod :** (aucun levier)
- Catégories instables sur : Prévention des déchets

> -> action à porter par les élus au niveau des syndicats de gestion des eaux potables

#### Fiche 57593 — 5.1.1 Augmenter la part de bâtiments publics équipés de panneaux solaires

- **Run 1 :** Electricité renouvelable [1]
- **Run 2 :** Electricité renouvelable [1, 5]
- **Run 3 :** Electricité renouvelable [1, 5]
- **Prod :** Electricité renouvelable [5]
- Catégories instables sur : Electricité renouvelable

## Paris Est Marne & Bois (5390)

- Fiches : **141** — stables sur les 3 runs : **124** (88%), instables : **17**
- Paires levier × catégorie distinctes proposées : 111 — 3/3 runs : 79, 2/3 runs : 14, 1/3 runs : 18
- Vote majoritaire = prod : 16/71 fiches classées d'un côté ou de l'autre
- Réponses JSON invalides rejouées : 0
- Appels : 423 — tokens d'entrée 2 276 127 (dont 2 236 812 en cache, 98%), sortie 8 783 — coût estimé 0.35 $ pour les 3 runs
- Date : 2026-11-02 13:10

### Classée dans certains runs, aucun levier dans d'autres (9)

#### Fiche 84974 — Fixer des objectifs de réduction de consommation d'énergie et limiter la pollution lumineuse dans le règlement local de publicité intercommunal

- **Run 1 :** Sobriété foncière [2]
- **Run 2 :** Sobriété foncière [2]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété foncière (2/3)

#### Fiche 85355 — Etudier des solutions de stationnement qui faciliteraient l'intermodalité

- **Run 1 :** (aucun levier)
- **Run 2 :** Vélo et transport en commun [2]
- **Run 3 :** Vélo et transport en commun [2]
- **Prod :** (aucun levier)
- Leviers intermittents : Vélo et transport en commun (2/3)

#### Fiche 85359 — Sensibiliser les professionnels du Territoire aux enjeu de la gestion du dernier kilomètre

- **Run 1 :** Efficacité et sobriété logistique [6]
- **Run 2 :** Efficacité et sobriété logistique [6]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Efficacité et sobriété logistique (2/3)

#### Fiche 85374 — Adhérer à l'Agence Locale de l'Energie et du Climat - MVE pour permettre aux habitants d'accéder au service public de la performance énergétique de l'habitat

- **Run 1 :** (aucun levier)
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [4] | Changement chaudières gaz + rénovation (résidentiel) [4]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [4] | Changement chaudières gaz + rénovation (résidentiel) [4]
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [4, 6] | Changement chaudières gaz + rénovation (résidentiel) [4, 6] | Sobriété des bâtiments (résidentiel) [4, 6]
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (2/3), Changement chaudières gaz + rénovation (résidentiel) (2/3)

#### Fiche 85689 — Structurer un réseau vertueux d'économie circulaire animé par PEMB

- **Run 1 :** Prévention des déchets [4] | Valorisation matière des déchets [4]
- **Run 2 :** Prévention des déchets [4] | Valorisation matière des déchets [4]
- **Run 3 :** (aucun levier)
- **Prod :** Prévention des déchets [4]
- Leviers intermittents : Prévention des déchets (2/3), Valorisation matière des déchets (2/3)

#### Fiche 85693 — Mettre en place des sondes dans les points d'apport volontaire

- **Run 1 :** (aucun levier)
- **Run 2 :** Prévention des déchets [2]
- **Run 3 :** Prévention des déchets [2]
- **Prod :** Efficacité et sobriété logistique [1]
- Leviers intermittents : Prévention des déchets (2/3)

#### Fiche 85695 — Créer un réseau interne de la transition écologique sur le territoire PEMB

- **Run 1 :** (aucun levier)
- **Run 2 :** Réduction des déplacements [4]
- **Run 3 :** Réduction des déplacements [4]
- **Prod :** (aucun levier)
- Leviers intermittents : Réduction des déplacements (2/3)

#### Fiche 85710 — Sensibilisation au gaspillage alimentaire dans les établissements scolaires

- **Run 1 :** (aucun levier)
- **Run 2 :** (aucun levier)
- **Run 3 :** Prévention des déchets [6]
- **Prod :** Prévention des déchets [6]
- Leviers intermittents : Prévention des déchets (1/3)

#### Fiche 85729 — Proposer des groupements de commandes

- **Run 1 :** Changement de chaudière à fioul (tertiaire) [5] | Changement de chaudière à gaz (tertiaire) [5]
- **Run 2 :** (aucun levier)
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Changement de chaudière à fioul (tertiaire) (1/3), Changement de chaudière à gaz (tertiaire) (1/3)

### Levier présent dans certains runs seulement (8)

#### Fiche 85344 — Créer une plateforme Territoriale de mobilités partagées

- **Run 1 :** Covoiturage [1] | Vélo et transport en commun [1]
- **Run 2 :** Covoiturage [1] | Véhicules électriques [1]
- **Run 3 :** Covoiturage [1] | Vélo et transport en commun [1]
- **Prod :** Covoiturage [1]
- Leviers intermittents : Véhicules électriques (1/3), Vélo et transport en commun (2/3)

#### Fiche 85351 — Soutenir les initiatives territoriales en faveur des modes actifs

- **Run 1 :** Réduction des déplacements [6] | Vélo et transport en commun [6]
- **Run 2 :** Vélo et transport en commun [6]
- **Run 3 :** Réduction des déplacements [6] | Vélo et transport en commun [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Réduction des déplacements (2/3)

#### Fiche 85379 — Renforcer l'efficacité énergétique des bâtiments dans le parc social

- **Run 1 :** Changement de chaudière à fioul (tertiaire) [5] | Changement de chaudière à gaz (tertiaire) [5] | Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 2 :** Changement de chaudière à fioul (tertiaire) [5] | Changement de chaudière à gaz (tertiaire) [5] | Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [5] | Changement chaudières gaz + rénovation (résidentiel) [5] | Sobriété et isolation des bâtiments (tertiaire) [5]
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [3]
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (1/3), Changement chaudières gaz + rénovation (résidentiel) (1/3), Changement de chaudière à fioul (tertiaire) (2/3), Changement de chaudière à gaz (tertiaire) (2/3)

#### Fiche 85691 — Acquérir des véhicules de collecte propres

- **Run 1 :** Prévention des déchets [3] | Valorisation matière des déchets [3]
- **Run 2 :** Fret décarboné et multimodalité [5]
- **Run 3 :** Efficacité et carburants décarbonés des véhicules privés [5]
- **Prod :** (aucun levier)
- Leviers intermittents : Efficacité et carburants décarbonés des véhicules privés (1/3), Fret décarboné et multimodalité (1/3), Prévention des déchets (1/3), Valorisation matière des déchets (1/3)

#### Fiche 85712 — S'engager dans la démarche cit'ergie

- **Run 1 :** Sobriété des bâtiments (résidentiel) [5] | Sobriété et isolation des bâtiments (tertiaire) [5] | Vélo et transport en commun [5]
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [5] | Changement chaudières gaz + rénovation (résidentiel) [5] | Sobriété des bâtiments (résidentiel) [5]
- **Run 3 :** Sobriété des bâtiments (résidentiel) [5]
- **Prod :** (aucun levier)
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (1/3), Changement chaudières gaz + rénovation (résidentiel) (1/3), Sobriété et isolation des bâtiments (tertiaire) (1/3), Vélo et transport en commun (1/3)

#### Fiche 85714 — Permettre aux élus de mieux appréhender les problématiques environnementales et les solutions associées

- **Run 1 :** Sobriété des bâtiments (résidentiel) [5] | Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 2 :** Sobriété des bâtiments (résidentiel) [5]
- **Run 3 :** Réduction des déplacements [5] | Sobriété des bâtiments (résidentiel) [5] | Sobriété et isolation des bâtiments (tertiaire) [5]
- **Prod :** (aucun levier)
- Leviers intermittents : Réduction des déplacements (1/3), Sobriété et isolation des bâtiments (tertiaire) (2/3)

#### Fiche 85722 — Dispositif territoire roule propre

- **Run 1 :** Véhicules électriques [5]
- **Run 2 :** Réduction des déplacements [5] | Véhicules électriques [5]
- **Run 3 :** Véhicules électriques [5]
- **Prod :** (aucun levier)
- Leviers intermittents : Réduction des déplacements (1/3)

#### Fiche 85727 — Inciter au recours aux ENR dans les équipements publics

- **Run 1 :** Electricité renouvelable [5]
- **Run 2 :** Electricité renouvelable [5]
- **Run 3 :** Biogaz [5] | Electricité renouvelable [5] | Réseaux de chaleur décarbonés [5]
- **Prod :** (aucun levier)
- Leviers intermittents : Biogaz (1/3), Réseaux de chaleur décarbonés (1/3)
