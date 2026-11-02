# Stabilité Mistral Large 4 — classification volet GES

Modèle `mistral-large-4`, `reasoning_effort=low`, température par défaut de l'API. Prompt v2 (`prompts/classification_volet_ges_v2.md`), une fiche par appel, codes de leviers et JSON contraint, 3 runs indépendants. Lecture seule sur la prod.

Mis à jour le 2026-10-30 17:08.

## Synthèse

| Collectivité | Fiches | Stables | Instables | % stable | Paires 3/3 | Majorité = prod |
|---|---:|---:|---:|---:|---:|---:|
| CC Ardennes Thiérache (3914) | 104 | 79 | 25 | 76% | 88/149 | 12/57 |
| CC Sundgau (4973) | 37 | 29 | 8 | 78% | 31/48 | non classée en prod |
| CC Brionnais Sud Bourgogne (5033) | 111 | 95 | 16 | 86% | 73/99 | 23/72 |
| Paris Est Marne & Bois (5390) | 141 | 120 | 21 | 85% | 69/113 | 20/71 |
| **Total** | **393** | **323** | **70** | **82%** | | |

« Paires 3/3 » : paires levier × catégorie données par les 3 runs, sur toutes les paires proposées au moins une fois.

## CC Ardennes Thiérache (3914)

- Fiches : **104** — stables sur les 3 runs : **79** (76%), instables : **25**
- Paires levier × catégorie distinctes proposées : 149 — 3/3 runs : 88, 2/3 runs : 15, 1/3 runs : 46
- Vote majoritaire = prod : 12/57 fiches classées d'un côté ou de l'autre
- Réponses JSON invalides rejouées : 0
- Appels : 312 — tokens d'entrée 1 588 608 (dont 1 526 016 en cache, 96%), sortie 611 217 — coût estimé 1.43 $ pour les 3 runs
- Date : 2026-10-30 17:08

### Classée dans certains runs, aucun levier dans d'autres (7)

#### Fiche 76377 — Mettre en place la Trame Verte et Bleue

- **Run 1 :** (aucun levier)
- **Run 2 :** Gestion des forêts et produits bois [1, 2] | Gestion des haies [1, 2] | Gestion des prairies [2, 6]
- **Run 3 :** (aucun levier)
- **Prod :** Gestion des haies [1, 2, 6] | Gestion des prairies [1, 2] | Pratiques stockantes [1] | Sobriété foncière [2]
- Leviers intermittents : Gestion des forêts et produits bois (1/3), Gestion des haies (1/3), Gestion des prairies (1/3)

> <p>Objectif : Protéger les continuités écologiques grâce aux documents d’urbanisme à travers notamment la Trame Verte et Bleue du SCOT et l’intégration dans le PLUi en cours de finalisation Le SCOT a pour but de décliner la Trame Verte et Bleue (TVB) régionale du SRADDET, à travers 4 sous-trames : Milieux humides, Milieux aquatiques, Milieux ouverts, Milieux boisés.</p><p>Le PNR des Ardennes porte également des actions en faveur du maintien et du développement des continuités écologiques dans l…

#### Fiche 76381 — Faire du tourisme durable un nouvel axe de développement économique

- **Run 1 :** Efficacité et sobriété logistique [6]
- **Run 2 :** (aucun levier)
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Efficacité et sobriété logistique (1/3)

> <p><em>Cette action vise à faire du territoire une destination verte.</em></p><p>•Mener une politique de marketing territorial avec la création d’outils de communication pour concilier sports nature et patrimoine naturel tout en développant l’image touristique de la destination : carte VTT FFC, carte enduro VTT, carte VTT transfrontalier, guide touristique, Eductour</p><p>•Organiser les activités de pleine nature sur le territoire (hors nouveau Schéma)</p><p>•Evaluer la création d’un observatoi…

#### Fiche 76489 — Mise en place d'un relais sénior

- **Run 1 :** Réduction des déplacements [1]
- **Run 2 :** (aucun levier)
- **Run 3 :** Réduction des déplacements [1]
- **Prod :** (aucun levier)
- Leviers intermittents : Réduction des déplacements (2/3)

#### Fiche 76490 — Mise en place d'une MSP multisite Rouvroy sur Audry / Liart

- **Run 1 :** (aucun levier)
- **Run 2 :** Réduction des déplacements [1]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Réduction des déplacements (1/3)

#### Fiche 76547 — Création et animation d'une Union commerciale industrielle et artisanale (UCIA)

- **Run 1 :** Sobriété foncière [4]
- **Run 2 :** (aucun levier)
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété foncière (1/3)

#### Fiche 76548 — Poursuite et développement des services mutualisés

- **Run 1 :** Sobriété foncière [1]
- **Run 2 :** (aucun levier)
- **Run 3 :** Réduction des déplacements [1]
- **Prod :** (aucun levier)
- Leviers intermittents : Réduction des déplacements (1/3), Sobriété foncière (1/3)

#### Fiche 76585 — Diagnostics "Ponts"

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [2] | Changement chaudières gaz + rénovation (résidentiel) [2]
- **Run 2 :** (aucun levier)
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (1/3), Changement chaudières gaz + rénovation (résidentiel) (1/3)

### Levier présent dans certains runs seulement (3)

#### Fiche 76374 — Mettre en place un service de transports à la demande

- **Run 1 :** Bus et cars décarbonés [1] | Vélo et transport en commun [1]
- **Run 2 :** Vélo et transport en commun [1]
- **Run 3 :** Bus et cars décarbonés [1] | Vélo et transport en commun [1]
- **Prod :** Véhicules électriques [1, 3] | Vélo et transport en commun [1, 3, 4]
- Leviers intermittents : Bus et cars décarbonés (2/3)

> <p><strong>Mettre en place un service de Transports à la Demande</strong></p><p><strong>Action en réflexion avancée :</strong></p><p>-le service visera à apporter une solution de mobilités aux personnes en incapacité de se déplacer et/ou qui justifient d'un isolement. Les principales dessertes seront les services de santé, les marchés, les activités culturelles de proximité</p><p>-la CCAT est en train de déposer un dossier pour un minibus électrique</p><p>-réfléchir à ce qui peut être mutualisé…

#### Fiche 76384 — Réduire les émissions de GES liées au centre de traitement des déchets

- **Run 1 :** Captage de méthane dans les ISDND [1]
- **Run 2 :** Captage de méthane dans les ISDND [1]
- **Run 3 :** Biogaz [1] | Captage de méthane dans les ISDND [1]
- **Prod :** Biogaz [1, 3, 4] | Captage de méthane dans les ISDND [1, 3, 4]
- Leviers intermittents : Biogaz (1/3)

> <p><strong>IVEDA d'Eteignières</strong></p><p><strong>Valorisation énergétique du biogaz capté :</strong></p><p>•Production Electricité via deux moteurs de COGENERATION&nbsp;: Revente sur le marché libre</p><p>•Production de chaleur via &nbsp;deux moteurs de COGENERATION et utilisation de celle-ci ( Bassin biologique, Tour de désulfuration, Chauffage des serres)</p><p>•Améliorations techniques&nbsp;: Mise en place d’un système bioréacteur afin de maîtriser la fermentation des déchets et notamme…

#### Fiche 76560 — Réhabilitation du pole scolaire de Signy-le-Petit

- **Run 1 :** Changement de chaudière à fioul (tertiaire) [5] | Changement de chaudière à gaz (tertiaire) [5] | Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 2 :** Changement de chaudière à fioul (tertiaire) [5] | Changement de chaudière à gaz (tertiaire) [5] | Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 3 :** Changement de chaudière à fioul (tertiaire) [5] | Changement de chaudière à gaz (tertiaire) [5]
- **Prod :** Sobriété et isolation des bâtiments (tertiaire) [5]
- Leviers intermittents : Sobriété et isolation des bâtiments (tertiaire) (2/3)

### Levier intermittent et catégories instables (6)

#### Fiche 76363 — Améliorer la performance énergétique des logements sociaux

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [4, 6] | Changement chaudières gaz + rénovation (résidentiel) [4, 6]
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [6] | Changement chaudières gaz + rénovation (résidentiel) [6] | Sobriété des bâtiments (résidentiel) [6]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [2, 6] | Changement chaudières gaz + rénovation (résidentiel) [2, 6]
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [4, 6] | Changement chaudières gaz + rénovation (résidentiel) [4, 6] | Sobriété des bâtiments (résidentiel) [6]
- Leviers intermittents : Sobriété des bâtiments (résidentiel) (1/3)
- Catégories instables sur : Changement chaudières fioul + rénovation (résidentiel), Changement chaudières gaz + rénovation (résidentiel)

> <p><strong>Bailleurs sociaux : Espace Habitat, Habitat 08</strong></p><p>Un des objectifs principaux est l'amélioration des performances thermiques des logements (c'est le cas pour Habitat08 sur tout le périmètre du SCoT)</p><p>•Organiser des réunions entre le PNR des Ardennes, la CCAT, Espace Habitat et Habitat 08 pour coordonner les démarches de rénovation portant sur les logements sociaux</p><p>&nbsp;</p><p>•Travailler avec les bailleurs sociaux en vue de l’amélioration des performances ther…

#### Fiche 76370 — Etudier et soutenir le développement des filières locales hydrogène et bioGNV

- **Run 1 :** Biogaz [2] | Bus et cars décarbonés [2] | Efficacité et carburants décarbonés des véhicules privés [2]
- **Run 2 :** Biogaz [2, 6] | Bus et cars décarbonés [2] | Fret décarboné et multimodalité [2, 6]
- **Run 3 :** Biogaz [2] | Bus et cars décarbonés [2] | Efficacité et carburants décarbonés des véhicules privés [2]
- **Prod :** Biogaz [2, 4] | Bus et cars décarbonés [4] | Fret décarboné et multimodalité [4]
- Leviers intermittents : Efficacité et carburants décarbonés des véhicules privés (2/3), Fret décarboné et multimodalité (1/3)
- Catégories instables sur : Biogaz

> <p><strong>Hydrogène</strong></p><p>Le gisement de consommation actuel est insuffisant pour avoir une unité hydrogène sur le territoire</p><p>•Etudier les gisements de consommation possibles : demande industrielle, TER, etc.</p><p>•Etudier le potentiel de développement d’une filière hydrogène (partenaire : SEM EnR)</p><p>•Point de vigilance : veiller à un approvisionnement en hydrogène bas-carbone (hydrogène vert, jaune)</p><p>•</p><p><strong>Biogaz</strong></p><p>Une filière peut voir le jour …

#### Fiche 76383 — Revitaliser les centres de villages et développer des services de proximité

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [2] | Changement chaudières gaz + rénovation (résidentiel) [2] | Réduction des déplacements [1, 2]
- **Run 2 :** Réduction des déplacements [1] | Sobriété foncière [2] | Véhicules électriques [1]
- **Run 3 :** Covoiturage [1] | Réduction des déplacements [1, 6] | Sobriété foncière [2, 3]
- **Prod :** Réduction des déplacements [1, 2]
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (1/3), Changement chaudières gaz + rénovation (résidentiel) (1/3), Covoiturage (1/3), Sobriété foncière (2/3), Véhicules électriques (1/3)
- Catégories instables sur : Réduction des déplacements

> <p><strong>Mettre en place des projets de revitalisation dans le cadre des ORT (5 communes) et du dispositif Petites Villes de Demain (Signy-le-Petit)</strong></p><p>Exemples d'actions</p><p>-Fédérer les commerçants</p><p>-Développer des cafés multiservices</p><p>-Mettre en place des IRVE, des stationnements vélos, des aires de covoiturage,</p><p>-Maintenir le commerce existant</p><p>-Vitrophanie</p><p>-Lutter contre le logement vacant</p><p>-OPAH</p><p>-THLV</p><p>-Rénovation du bâti ancien</p…

#### Fiche 76386 — Renforcer le lien entre les producteurs, les transformateurs, les distributeurs

- **Run 1 :** Efficacité et sobriété logistique [4, 6] | Prévention des déchets [4, 6]
- **Run 2 :** Efficacité et sobriété logistique [4]
- **Run 3 :** Efficacité et sobriété logistique [1, 4] | Prévention des déchets [4]
- **Prod :** (aucun levier)
- Leviers intermittents : Prévention des déchets (2/3)
- Catégories instables sur : Efficacité et sobriété logistique

> <p>•Mutualiser des installations qui pourraient bénéficier à plusieurs acteurs (exemple : Albatros 08 possèdent un autoclave qui permet de valoriser les invendus des maraîchers)</p><p>•</p><p><strong>Association L’Environnement D’Abord (LEDA)</strong></p><p>•Agrandir le réseau des producteurs impliqués, devenir la structure coordinatrice de la distribution en circuit court sur le territoire</p><p>•Chambre d’Agriculture : les accompagner et les aider à associer le plus possible de producteurs lo…

#### Fiche 76388 — Structurer une filière de valorisation du bois

- **Run 1 :** Gestion des forêts et produits bois [1, 3, 4]
- **Run 2 :** Gestion des forêts et produits bois [1, 3, 4] | Réseaux de chaleur décarbonés [3]
- **Run 3 :** Gestion des forêts et produits bois [3, 4]
- **Prod :** Gestion des forêts et produits bois [1, 3, 4]
- Leviers intermittents : Réseaux de chaleur décarbonés (1/3)
- Catégories instables sur : Gestion des forêts et produits bois

> <p><em>Dans les 6 prochaines années, des volumes très importants seront à traiter sachant que la forêt ne pourra produire davantage notamment avec le changement climatique au-delà de 10 - 20 ans.</em></p><p>•Relocaliser la filière via contrats d’approvisionnement avec l’ONF</p><p>•Soutenir l’installation d’ETF (Entreprises de Travaux Forestiers) sur le territoire pour répondre au besoin de main d’œuvre de l’ONF (si ces entreprises sont prêtes à s’installer, l’ONF peut leur garantir de l’activit…

#### Fiche 76419 — Développer de nouvelles filières agricoles locales

- **Run 1 :** Elevage durable [6] | Gestion des prairies [6] | Prévention des déchets [6]
- **Run 2 :** Efficacité et sobriété logistique [2, 6] | Gestion des prairies [2, 6] | Prévention des déchets [1]
- **Run 3 :** Gestion des prairies [2, 6] | Prévention des déchets [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Efficacité et sobriété logistique (1/3), Elevage durable (1/3)
- Catégories instables sur : Gestion des prairies, Prévention des déchets

> <p><strong>Actions PNR </strong>:</p><p>•Initier la réflexion pour le développement de production de fruits et légumes sur le territoire (analyse des producteurs existants, étude sur le foncier (enquêtes auprès des communes/EPCI/SAFER/Terres de lien…), les outils de transformation et les points de vente)</p><p>•Identifier une/des filières prioritaires et mettre en place un programme de développement de cette/ces filières (AMI filière ? Lait de pâturage ?) - 2e session ?</p><p><strong>Actions CC…

### Mêmes leviers, catégories différentes (9)

#### Fiche 76362 — Mise en œuvre d'un observatoire sur le logement vacant

- **Run 1 :** Sobriété foncière [2, 6]
- **Run 2 :** Sobriété foncière [2, 3]
- **Run 3 :** Sobriété foncière [2, 6]
- **Prod :** (aucun levier)
- Catégories instables sur : Sobriété foncière

> <p><strong>Diagnostic et recensement des logements vacants dans les 37 communes</strong></p><p>•Méthode : enquête auprès des propriétaires</p><p>•S'appuyer sur la connaissance du terrain par les Maires</p><p>•</p><p><strong>Réaliser un atlas de la vacance des logements</strong></p><p>•Prise de rendez-vous avec les propriétaires et orientation de ces derniers vers les dispositifs d’aides appropriés</p><p>•Mettre en place une opération programmée de l’amélioration de l’habitat avec des dispositif…

#### Fiche 76364 — Etudier la mise en place d'un Permis de louer

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [2, 6] | Changement chaudières gaz + rénovation (résidentiel) [2, 6]
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [2] | Changement chaudières gaz + rénovation (résidentiel) [2]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [2] | Changement chaudières gaz + rénovation (résidentiel) [2]
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [2, 6] | Changement chaudières gaz + rénovation (résidentiel) [2, 6]
- Catégories instables sur : Changement chaudières fioul + rénovation (résidentiel), Changement chaudières gaz + rénovation (résidentiel)

> <p><strong><em>Le permis de louer visera notamment à contraindre les bailleurs privés à rénover leurs biens.</em></strong></p><p><strong>Etape 0 : Communiquer auprès des propriétaires bailleurs </strong>l'interdiction<strong> </strong>à venir de la mise en location des passoires thermiques (G en 2025, F en 2028) pour les inciter à les rénover</p><p><strong>Etape 1: mise en place d’un Label Qualité Logement à l’échelle EPCI</strong></p><p>La CCAT souhaite mettre en place un LQL dans le cadre de …

#### Fiche 76369 — Mettre en place des rénovations énergétiques sur le bâti public

- **Run 1 :** Changement de chaudière à fioul (tertiaire) [6] | Changement de chaudière à gaz (tertiaire) [6] | Sobriété et isolation des bâtiments (tertiaire) [6]
- **Run 2 :** Changement de chaudière à fioul (tertiaire) [2, 6] | Changement de chaudière à gaz (tertiaire) [2, 6] | Sobriété et isolation des bâtiments (tertiaire) [2, 6]
- **Run 3 :** Changement de chaudière à fioul (tertiaire) [6] | Changement de chaudière à gaz (tertiaire) [6] | Sobriété et isolation des bâtiments (tertiaire) [6]
- **Prod :** Changement de chaudière à fioul (tertiaire) [5] | Changement de chaudière à gaz (tertiaire) [5] | Sobriété et isolation des bâtiments (tertiaire) [5]
- Catégories instables sur : Changement de chaudière à fioul (tertiaire), Changement de chaudière à gaz (tertiaire), Sobriété et isolation des bâtiments (tertiaire)

> <p>La communauté de communes dispose d’un parc de bâtiment de 26 000 m² dont de nombreux bâtiments publics et logements. Les 37 communes qui component Ardennes Thiérache possèdent environ 200 bâtiments publics (logements, mairies, salles communales, …) qui ont pour la plupart plus de 20 ans et sont de gros consommateurs d'énergies fossiles.</p><p>L'objectif est de pouvoir accompagner les communes dans leurs études et travaux de rénovation.</p><p><strong>Avancement de l’action :</strong></p><p>E…

#### Fiche 76373 — Lutter contre l’autosolisme

- **Run 1 :** Covoiturage [1, 2] | Véhicules électriques [1]
- **Run 2 :** Covoiturage [1] | Véhicules électriques [1]
- **Run 3 :** Covoiturage [1, 2] | Véhicules électriques [1]
- **Prod :** Covoiturage [1, 3, 4]
- Catégories instables sur : Covoiturage

> <p><strong>Mettre à disposition des véhicules électriques en autopartage</strong></p><p><strong>Création d’une aire de covoiture sur le territoire (mon Idée)</strong></p><p><strong>Créer une plateforme/un réseau de mise en relation des habitants qui souhaiteraient partager leur véhicule</strong></p><p><strong>Mettre en place une application de covoiturage à l'échelle de la CC</strong></p><p><em>Action engagée : mise en relation pour du covoiturage sur l'application de la CCAT (pas de paiement d…

#### Fiche 76387 — Soutenir les démarches vers l'agroécologie

- **Run 1 :** Changements de pratiques de fertilisation azotée [3, 6] | Elevage durable [3, 6] | Pratiques stockantes [3, 6]
- **Run 2 :** Changements de pratiques de fertilisation azotée [6] | Elevage durable [3, 6] | Pratiques stockantes [6]
- **Run 3 :** Changements de pratiques de fertilisation azotée [6] | Elevage durable [3, 6] | Pratiques stockantes [6]
- **Prod :** Changements de pratiques de fertilisation azotée [3, 6] | Elevage durable [3, 4, 6] | Pratiques stockantes [6]
- Catégories instables sur : Changements de pratiques de fertilisation azotée, Pratiques stockantes

> <p><strong>Action PNR </strong>:</p><p>•Réaliser des évènements (ciné débat/séminaire/visite...) incitant à réfléchir ensemble à travailler autrement, vers des pratiques agro-environnementales, élevage à l'herbe, autonomie alimentaire sur la ferme, adaptation au changement climatique, soin des animaux allopathiques...</p><p><strong>Actions CCAT</strong></p><p>•Apporter des conseils et des aides aux éleveurs qui s'engagent dans des démarches de réduction des émissions de GES de leur cheptel</p><…

#### Fiche 76391 — Accompagner les communes et la CCAT sur le développement des EnR (évaluation d’opportunités sur leur patrimoine et évaluation des projets photovoltaïques portés par des développeurs privés )

- **Run 1 :** Electricité renouvelable [6] | Réseaux de chaleur décarbonés [4, 6]
- **Run 2 :** Electricité renouvelable [6] | Réseaux de chaleur décarbonés [6]
- **Run 3 :** Electricité renouvelable [6] | Réseaux de chaleur décarbonés [4, 6]
- **Prod :** Electricité renouvelable [4, 6]
- Catégories instables sur : Réseaux de chaleur décarbonés

> <p><strong>Hypothèse 1 : Création d’une structure intercommunale participative pour la mise en œuvre d’un réseau de chaleur sur la commune de Maubert Fontaine</strong></p><p><strong>Hypothèse 2 : Travailler avec l’ALE 08 à travers le dispositif Générateurs (solaire photovoltaïque) :</strong></p><p>L'ALE 08 fait partie du dispositif Les GÉnÉRATEURS :</p><p>Ce dispositif co-finance des acteurs qui peuvent intervenir auprès des communes dès l’émergence d’un projet photovoltaïque, que la commune so…

#### Fiche 76394 — Réduire l'impact environnemental lié aux déplacements des agents

- **Run 1 :** Covoiturage [5] | Véhicules électriques [2, 5] | Vélo et transport en commun [5]
- **Run 2 :** Covoiturage [5] | Véhicules électriques [5] | Vélo et transport en commun [5]
- **Run 3 :** Covoiturage [5] | Véhicules électriques [2, 5] | Vélo et transport en commun [5]
- **Prod :** Covoiturage [4, 5] | Réduction des déplacements [4, 5] | Véhicules électriques [4, 5] | Vélo et transport en commun [1, 5]
- Catégories instables sur : Véhicules électriques

> <p>Optimiser la flotte de véhicules de la collectivité Prolonger la durée de vie des véhicules Interroger les besoins pour réduire au minimum la taille de la flotte nécessaire Lors de l'achat de véhicules, privilégier des véhicules électriques, d'occasion, de faible puissance</p><p>Mise en place d’une étude territoriale sur le verdissement de la flotte de véhicules des EPCI. Combien de véhicules électriques dans la flotte de la CCAT aujourd’hui ? 2 Quels objectifs ?</p><p>Mettre en place un Pla…

#### Fiche 76395 — Réduire la production de déchets et optimiser leur collecte

- **Run 1 :** Covoiturage [5] | Véhicules électriques [5] | Vélo et transport en commun [5]
- **Run 2 :** Covoiturage [5] | Véhicules électriques [5] | Vélo et transport en commun [5]
- **Run 3 :** Covoiturage [5] | Véhicules électriques [2, 5] | Vélo et transport en commun [5]
- **Prod :** Covoiturage [4, 5] | Réduction des déplacements [4, 5] | Véhicules électriques [4, 5] | Vélo et transport en commun [1, 5]
- Catégories instables sur : Véhicules électriques

> <p>Optimiser la flotte de véhicules de la collectivité Prolonger la durée de vie des véhicules Interroger les besoins pour réduire au minimum la taille de la flotte nécessaire Lors de l'achat de véhicules, privilégier des véhicules électriques, d'occasion, de faible puissance</p><p>Mise en place d’une étude territoriale sur le verdissement de la flotte de véhicules des EPCI. Combien de véhicules électriques dans la flotte de la CCAT aujourd’hui ? 2 Quels objectifs ?</p><p>Mettre en place un Pla…

#### Fiche 76577 — PIG

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [2, 3] | Changement chaudières gaz + rénovation (résidentiel) [2, 3]
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [2, 3] | Changement chaudières gaz + rénovation (résidentiel) [2, 3]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [2] | Changement chaudières gaz + rénovation (résidentiel) [2]
- **Prod :** (aucun levier)
- Catégories instables sur : Changement chaudières fioul + rénovation (résidentiel), Changement chaudières gaz + rénovation (résidentiel)

## CC Sundgau (4973)

- Fiches : **37** — stables sur les 3 runs : **29** (78%), instables : **8**
- Paires levier × catégorie distinctes proposées : 48 — 3/3 runs : 31, 2/3 runs : 8, 1/3 runs : 9
- Aucune classification en prod pour cette collectivité
- Réponses JSON invalides rejouées : 0
- Appels : 111 — tokens d'entrée 562 728 (dont 541 440 en cache, 96%), sortie 184 354 — coût estimé 0.44 $ pour les 3 runs
- Date : 2026-10-30 17:08

### Classée dans certains runs, aucun levier dans d'autres (1)

#### Fiche 42049 — Organiser des animations et communiquer sur les enjeux d'une alimentation de qualité et durable

- **Run 1 :** (aucun levier)
- **Run 2 :** Prévention des déchets [6]
- **Run 3 :** Prévention des déchets [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Prévention des déchets (2/3)

> L’éducation et la sensibilisation à l’alimentation durable est un sujet dont peuvent se saisir les collectivités en organisant des événements de sensibilisation et en faisant appel à des prestataires d'animation. Il est possible d'en profiter pour faire le lien avec d'autres politiques alimentaires de la collectivité en organisant des événements en lien avec les dispositifs menés en parallèle. 3 sujets sont particulièrement importants : la végétalisation de l'assiette, l'augmentation de la part…

### Levier présent dans certains runs seulement (1)

#### Fiche 42051 — Sensibiliser aux enjeux des mobilités alternatives à la voiture individuelle

- **Run 1 :** Covoiturage [2, 6] | Vélo et transport en commun [2, 6]
- **Run 2 :** Covoiturage [2, 6] | Vélo et transport en commun [2, 6]
- **Run 3 :** Covoiturage [2, 6] | Réduction des déplacements [2, 6] | Vélo et transport en commun [2, 6]
- **Prod :** (aucun levier)
- Leviers intermittents : Réduction des déplacements (1/3)

> Sensibiliser aux enjeux des mobilités alternatives à la voiture individuelle/autosolisme, en prenant en compte les publics précaires. \n- Recenser les actions déjà menées en faveur des mobilités alternatives à la voiture individuelle/autosolisme - Valoriser ces actions - Définir les publics ciblés par les démarches de sensibilisation - Initier et/ou poursuivre les actions de sensibilisation, information et communication en identifiant les formats adaptés en fonction des publics ciblés (exemples…

### Levier intermittent et catégories instables (1)

#### Fiche 42050 — Mettre en place une politique de mobilité alternative des agents et des élu.e.s

- **Run 1 :** Covoiturage [5] | Véhicules électriques [5] | Vélo et transport en commun [5]
- **Run 2 :** Efficacité et carburants décarbonés des véhicules privés [5] | Véhicules électriques [5] | Vélo et transport en commun [5]
- **Run 3 :** Covoiturage [3, 5] | Efficacité et carburants décarbonés des véhicules privés [3, 5] | Vélo et transport en commun [3, 5]
- **Prod :** (aucun levier)
- Leviers intermittents : Covoiturage (2/3), Efficacité et carburants décarbonés des véhicules privés (2/3), Véhicules électriques (2/3)
- Catégories instables sur : Vélo et transport en commun

> Mettre en place une politique de mobilité alternative des agents et des élu.e.s, visant le changement de comportement, en adoptant une approche diversifiée pour couvrir tant les déplacements professionnels que ceux domicile-travail. Cette politique devrait inclure l'optimisation et le renouvellement de la flotte de véhicules, une gestion optimisée des déplacements, le développement de l'usage du vélo, des campagnes de communication et de sensibilisation, ainsi que la promotion des transports co…

### Mêmes leviers, catégories différentes (5)

#### Fiche 17138 — Accompagnement de la lutte contre le gaspillage alimentaire dans les périscolaires

- **Run 1 :** Prévention des déchets [5]
- **Run 2 :** Prévention des déchets [6]
- **Run 3 :** Prévention des déchets [6]
- **Prod :** (aucun levier)
- Catégories instables sur : Prévention des déchets

> existe une initiative de pesées des restes alimentaires encourager la démarche et identifier les leviers qui permettront de réduire les quantités de restes Éléments de calendrier : début : octobre 2023, pesées des restes alimentaires au périscolaire de Spechbach

#### Fiche 42052 — Promouvoir et encourager les initiatives de réparation sur le territoire

- **Run 1 :** Prévention des déchets [1, 6]
- **Run 2 :** Prévention des déchets [1, 6]
- **Run 3 :** Prévention des déchets [6]
- **Prod :** (aucun levier)
- Catégories instables sur : Prévention des déchets

> Soutenir des initiatives de recyclerie ou de réparation de matériel en proposant des lieux à des associations ou à des acteurs de l’économie social et solidaire qui s’engagent sur cette pratique. Une animation du réseau peut venir amplifier la dynamique et créer une synergie entre les différents acteurs. \n- Identifier les acteurs de la réparation existants sur le territoire (association, acteurs de l'économie sociale et solidaire, etc.). Une carte interactive identifiant et localisant les acte…

#### Fiche 42053 — Réaliser des achats durables via la commande publique

- **Run 1 :** Prévention des déchets [5]
- **Run 2 :** Prévention des déchets [5]
- **Run 3 :** Prévention des déchets [2, 5]
- **Prod :** (aucun levier)
- Catégories instables sur : Prévention des déchets

> Mobiliser la commande publique pour réaliser des achats durables sur l'ensemble des produits, bien et services gérés par la collectivité. Contenu à aborder : favoriser les achats de proximité / réduire les déchets d'emballage via la commande publique / Inclure le critère de consommation énergétique dans les choix de matériels informatiques / stopper les achats non équitables ou non éthiques, intégrer dans les marchés publics des critères d'efficacité énergétique, de réduction de l'impact enviro…

#### Fiche 53170 — Organiser la commande groupée de composteurs de cuisine

- **Run 1 :** Prévention des déchets [3]
- **Run 2 :** Prévention des déchets [6]
- **Run 3 :** Prévention des déchets [6]
- **Prod :** (aucun levier)
- Catégories instables sur : Prévention des déchets

#### Fiche 61678 — Installer des poubelles de tri dans les ERP et la signalétique adaptée aux déchets hors foyer

- **Run 1 :** Valorisation matière des déchets [5]
- **Run 2 :** Valorisation matière des déchets [1]
- **Run 3 :** Valorisation matière des déchets [1]
- **Prod :** (aucun levier)
- Catégories instables sur : Valorisation matière des déchets

## CC Brionnais Sud Bourgogne (5033)

- Fiches : **111** — stables sur les 3 runs : **95** (86%), instables : **16**
- Paires levier × catégorie distinctes proposées : 99 — 3/3 runs : 73, 2/3 runs : 11, 1/3 runs : 15
- Vote majoritaire = prod : 23/72 fiches classées d'un côté ou de l'autre
- Réponses JSON invalides rejouées : 0
- Appels : 333 — tokens d'entrée 1 677 903 (dont 1 619 712 en cache, 97%), sortie 470 416 — coût estimé 1.14 $ pour les 3 runs
- Date : 2026-10-30 17:08

### Classée dans certains runs, aucun levier dans d'autres (4)

#### Fiche 57566 — 3.1.7 Etudier la possibilité de grouper les achats de combustibles des 3 CC

- **Run 1 :** Sobriété et isolation des bâtiments (tertiaire) [2]
- **Run 2 :** (aucun levier)
- **Run 3 :** Sobriété et isolation des bâtiments (tertiaire) [2]
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété et isolation des bâtiments (tertiaire) (2/3)

#### Fiche 57626 — 6.5.3 Organiser des journées "Nettoyons la nature"

- **Run 1 :** Valorisation matière des déchets [6]
- **Run 2 :** Valorisation matière des déchets [6]
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Valorisation matière des déchets (2/3)

#### Fiche 57638 — 7.3.4 Créer une conserverie collective dans les anciens locaux Baligand à La Clayette

- **Run 1 :** Prévention des déchets [1]
- **Run 2 :** (aucun levier)
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Prévention des déchets (1/3)

#### Fiche 57641 — 7.3.7 Inciter à une consommation plus durable (locale, circuits courts, bio, vrac…)

- **Run 1 :** (aucun levier)
- **Run 2 :** (aucun levier)
- **Run 3 :** Prévention des déchets [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Prévention des déchets (1/3)

### Levier présent dans certains runs seulement (3)

#### Fiche 57602 — 5.2.1 Etudier l'optimisation et la valorisation des haies bocagères

- **Run 1 :** Gestion des haies [2]
- **Run 2 :** Gestion des forêts et produits bois [2] | Gestion des haies [2]
- **Run 3 :** Gestion des haies [2]
- **Prod :** (aucun levier)
- Leviers intermittents : Gestion des forêts et produits bois (1/3)

#### Fiche 57606 — 5.2.5 Communiquer les aides possibles pour le bois

- **Run 1 :** Gestion des forêts et produits bois [6]
- **Run 2 :** Réseaux de chaleur décarbonés [6]
- **Run 3 :** Réseaux de chaleur décarbonés [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Gestion des forêts et produits bois (1/3), Réseaux de chaleur décarbonés (2/3)

#### Fiche 57630 — 7.1.1 Replanter des arbres dans les haies et les prés

- **Run 1 :** Gestion des haies [1]
- **Run 2 :** Gestion des haies [1] | Gestion des prairies [1]
- **Run 3 :** Gestion des haies [1] | Gestion des prairies [1]
- **Prod :** Gestion des haies [1]
- Leviers intermittents : Gestion des prairies (2/3)

### Mêmes leviers, catégories différentes (9)

#### Fiche 57559 — 2.4.3 Inciter au covoiturage dans les collectivités

- **Run 1 :** Covoiturage [6]
- **Run 2 :** Covoiturage [5]
- **Run 3 :** Covoiturage [6]
- **Prod :** Covoiturage [5]
- Catégories instables sur : Covoiturage

#### Fiche 57561 — 3.1.2 Instaurer une démarche éco-responsable auprès des acteurs utilisant les bâtiments publics

- **Run 1 :** Sobriété et isolation des bâtiments (tertiaire) [6]
- **Run 2 :** Sobriété et isolation des bâtiments (tertiaire) [6]
- **Run 3 :** Sobriété et isolation des bâtiments (tertiaire) [5]
- **Prod :** Sobriété et isolation des bâtiments (tertiaire) [6]
- Catégories instables sur : Sobriété et isolation des bâtiments (tertiaire)

#### Fiche 57562 — 3.1.3 Inciter les communes qui ne l'ont pas fait à réaliser un diagnostic énergétique de leurs bâtiments publics

- **Run 1 :** Sobriété et isolation des bâtiments (tertiaire) [2]
- **Run 2 :** Sobriété et isolation des bâtiments (tertiaire) [6]
- **Run 3 :** Sobriété et isolation des bâtiments (tertiaire) [6]
- **Prod :** (aucun levier)
- Catégories instables sur : Sobriété et isolation des bâtiments (tertiaire)

#### Fiche 57564 — 3.1.5 Réaliser un groupement de commandes pour les DPE manquants

- **Run 1 :** Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 2 :** Sobriété et isolation des bâtiments (tertiaire) [2]
- **Run 3 :** Sobriété et isolation des bâtiments (tertiaire) [2]
- **Prod :** (aucun levier)
- Catégories instables sur : Sobriété et isolation des bâtiments (tertiaire)

#### Fiche 57596 — 5.1.4 Développer le solaire photovoltaïque sur les bâtiments industriels et agricoles

- **Run 1 :** Electricité renouvelable [6]
- **Run 2 :** Electricité renouvelable [1]
- **Run 3 :** Electricité renouvelable [2]
- **Prod :** (aucun levier)
- Catégories instables sur : Electricité renouvelable

#### Fiche 57597 — 5.1.5 Respecter l'obligation de solarisation des parkings > 1500 m²

- **Run 1 :** Electricité renouvelable [1]
- **Run 2 :** Electricité renouvelable [2]
- **Run 3 :** Electricité renouvelable [2]
- **Prod :** Electricité renouvelable [2]
- Catégories instables sur : Electricité renouvelable

#### Fiche 57603 — 5.2.2 Organiser une réunion entre tous les acteurs et soutiens potentiels sur le thème de la filière bois-énergie

- **Run 1 :** Gestion des forêts et produits bois [4]
- **Run 2 :** Gestion des forêts et produits bois [6]
- **Run 3 :** Gestion des forêts et produits bois [4]
- **Prod :** (aucun levier)
- Catégories instables sur : Gestion des forêts et produits bois

> Ou Appel à Manifestation d’Intérêt Ou Atelier/groupe de travail spécifique

#### Fiche 57620 — 6.3.1 Actions de prévention et d'incitation

- **Run 1 :** Prévention des déchets [3]
- **Run 2 :** Prévention des déchets [3]
- **Run 3 :** Prévention des déchets [3, 6]
- **Prod :** (aucun levier)
- Catégories instables sur : Prévention des déchets

#### Fiche 57621 — 6.3.2 Généraliser des actions permettant de réduire les tonnages produits (réduction des bacs de regroupement, fermeture des bacs d'ordures ménagères, fréquence de collecte…)

- **Run 1 :** Prévention des déchets [1]
- **Run 2 :** Prévention des déchets [2]
- **Run 3 :** Prévention des déchets [2]
- **Prod :** Prévention des déchets [2]
- Catégories instables sur : Prévention des déchets

## Paris Est Marne & Bois (5390)

- Fiches : **141** — stables sur les 3 runs : **120** (85%), instables : **21**
- Paires levier × catégorie distinctes proposées : 113 — 3/3 runs : 69, 2/3 runs : 21, 1/3 runs : 23
- Vote majoritaire = prod : 20/71 fiches classées d'un côté ou de l'autre
- Réponses JSON invalides rejouées : 0
- Appels : 422 — tokens d'entrée 2 140 145 (dont 2 048 000 en cache, 96%), sortie 665 746 — coût estimé 1.60 $ pour les 3 runs
- Date : 2026-10-30 17:08

### Classée dans certains runs, aucun levier dans d'autres (5)

#### Fiche 84975 — Favorisant l'agriculture urbaine durable

- **Run 1 :** Changements de pratiques de fertilisation azotée [6] | Pratiques stockantes [6]
- **Run 2 :** (aucun levier)
- **Run 3 :** (aucun levier)
- **Prod :** Pratiques stockantes [6]
- Leviers intermittents : Changements de pratiques de fertilisation azotée (1/3), Pratiques stockantes (1/3)

#### Fiche 85361 — Création d'un comité citoyen de la mobilité

- **Run 1 :** Covoiturage [4] | Vélo et transport en commun [4]
- **Run 2 :** (aucun levier)
- **Run 3 :** Covoiturage [4] | Vélo et transport en commun [4]
- **Prod :** (aucun levier)
- Leviers intermittents : Covoiturage (2/3), Vélo et transport en commun (2/3)

#### Fiche 85671 — Concevoir une plate-forme territoriale pour repérer et accompagner les ménages en situation de précarité énergétique

- **Run 1 :** (aucun levier)
- **Run 2 :** (aucun levier)
- **Run 3 :** Sobriété des bâtiments (résidentiel) [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Sobriété des bâtiments (résidentiel) (1/3)

#### Fiche 85696 — Inciter à la réalisation d'actions de responsabilité sociétale des entreprises et de développement durable (PDE...)

- **Run 1 :** Covoiturage [6] | Vélo et transport en commun [6]
- **Run 2 :** (aucun levier)
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Covoiturage (1/3), Vélo et transport en commun (1/3)

#### Fiche 85704 — Etendre les initiatives d'opération de nettoyage par les citoyens

- **Run 1 :** Valorisation matière des déchets [6]
- **Run 2 :** (aucun levier)
- **Run 3 :** (aucun levier)
- **Prod :** (aucun levier)
- Leviers intermittents : Valorisation matière des déchets (1/3)

### Levier présent dans certains runs seulement (8)

#### Fiche 84973 — Gérer et valoriser localement les terres et autres matériaux de déconstruction dans les projets d'aménagement

- **Run 1 :** Valorisation matière des déchets [2]
- **Run 2 :** Prévention des déchets [2]
- **Run 3 :** Prévention des déchets [2]
- **Prod :** Prévention des déchets [1, 2]
- Leviers intermittents : Prévention des déchets (2/3), Valorisation matière des déchets (1/3)

#### Fiche 85357 — Développer et étendre les transports existants sur la Marne

- **Run 1 :** Fret décarboné et multimodalité [1]
- **Run 2 :** Fret décarboné et multimodalité [1]
- **Run 3 :** Vélo et transport en commun [1]
- **Prod :** Vélo et transport en commun [1]
- Leviers intermittents : Fret décarboné et multimodalité (2/3), Vélo et transport en commun (1/3)

#### Fiche 85672 — Structurer un réseau d'acteurs et co-porter la plateforme de lutte contre la précarité énergétique à l'échelle Territoriale

- **Run 1 :** Sobriété des bâtiments (résidentiel) [4]
- **Run 2 :** Sobriété des bâtiments (résidentiel) [4]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [4] | Changement chaudières gaz + rénovation (résidentiel) [4]
- **Prod :** (aucun levier)
- Leviers intermittents : Changement chaudières fioul + rénovation (résidentiel) (1/3), Changement chaudières gaz + rénovation (résidentiel) (1/3), Sobriété des bâtiments (résidentiel) (2/3)

#### Fiche 85679 — Etudier le potentiel de développement des ENR&R sur le Territoire

- **Run 1 :** Electricité renouvelable [2]
- **Run 2 :** Electricité renouvelable [2] | Réseaux de chaleur décarbonés [2]
- **Run 3 :** Electricité renouvelable [2] | Réseaux de chaleur décarbonés [2]
- **Prod :** (aucun levier)
- Leviers intermittents : Réseaux de chaleur décarbonés (2/3)

#### Fiche 85690 — Valoriser les terres issues des travaux du Grand Paris Express

- **Run 1 :** Prévention des déchets [6]
- **Run 2 :** Valorisation matière des déchets [6]
- **Run 3 :** Valorisation matière des déchets [6]
- **Prod :** (aucun levier)
- Leviers intermittents : Prévention des déchets (1/3), Valorisation matière des déchets (2/3)

#### Fiche 85691 — Acquérir des véhicules de collecte propres

- **Run 1 :** Fret décarboné et multimodalité [5]
- **Run 2 :** Fret décarboné et multimodalité [5]
- **Run 3 :** Efficacité et carburants décarbonés des véhicules privés [5]
- **Prod :** (aucun levier)
- Leviers intermittents : Efficacité et carburants décarbonés des véhicules privés (1/3), Fret décarboné et multimodalité (2/3)

#### Fiche 85726 — Faciliter la programmation de réhabilitation des bâtiments publics

- **Run 1 :** Changement de chaudière à fioul (tertiaire) [2] | Changement de chaudière à gaz (tertiaire) [2] | Sobriété et isolation des bâtiments (tertiaire) [2]
- **Run 2 :** Changement de chaudière à fioul (tertiaire) [2] | Changement de chaudière à gaz (tertiaire) [2] | Sobriété et isolation des bâtiments (tertiaire) [2]
- **Run 3 :** Changement de chaudière à fioul (tertiaire) [2] | Changement de chaudière à gaz (tertiaire) [2]
- **Prod :** Sobriété et isolation des bâtiments (tertiaire) [5]
- Leviers intermittents : Sobriété et isolation des bâtiments (tertiaire) (2/3)

#### Fiche 85729 — Proposer des groupements de commandes

- **Run 1 :** Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 2 :** Changement de chaudière à fioul (tertiaire) [5] | Changement de chaudière à gaz (tertiaire) [5]
- **Run 3 :** Changement de chaudière à fioul (tertiaire) [5] | Changement de chaudière à gaz (tertiaire) [5]
- **Prod :** (aucun levier)
- Leviers intermittents : Changement de chaudière à fioul (tertiaire) (2/3), Changement de chaudière à gaz (tertiaire) (2/3), Sobriété et isolation des bâtiments (tertiaire) (1/3)

### Mêmes leviers, catégories différentes (8)

#### Fiche 85360 — Proposer une charte de livraison privilégiant une logistique sobre et décarbonée

- **Run 1 :** Efficacité et sobriété logistique [2] | Fret décarboné et multimodalité [2]
- **Run 2 :** Efficacité et sobriété logistique [2] | Fret décarboné et multimodalité [2]
- **Run 3 :** Efficacité et sobriété logistique [4] | Fret décarboné et multimodalité [4]
- **Prod :** (aucun levier)
- Catégories instables sur : Efficacité et sobriété logistique, Fret décarboné et multimodalité

#### Fiche 85379 — Renforcer l'efficacité énergétique des bâtiments dans le parc social

- **Run 1 :** Changement chaudières fioul + rénovation (résidentiel) [3] | Changement chaudières gaz + rénovation (résidentiel) [3]
- **Run 2 :** Changement chaudières fioul + rénovation (résidentiel) [2] | Changement chaudières gaz + rénovation (résidentiel) [2]
- **Run 3 :** Changement chaudières fioul + rénovation (résidentiel) [2] | Changement chaudières gaz + rénovation (résidentiel) [2]
- **Prod :** Changement chaudières fioul + rénovation (résidentiel) [3]
- Catégories instables sur : Changement chaudières fioul + rénovation (résidentiel), Changement chaudières gaz + rénovation (résidentiel)

#### Fiche 85678 — Construire des stratégies partenariales pour les ENR&R

- **Run 1 :** Electricité renouvelable [4]
- **Run 2 :** Electricité renouvelable [2]
- **Run 3 :** Electricité renouvelable [4]
- **Prod :** (aucun levier)
- Catégories instables sur : Electricité renouvelable

#### Fiche 85682 — Développer le compost individuel sur le Territoire

- **Run 1 :** Prévention des déchets [1]
- **Run 2 :** Prévention des déchets [6]
- **Run 3 :** Prévention des déchets [6]
- **Prod :** Valorisation matière des déchets [1, 6]
- Catégories instables sur : Prévention des déchets

#### Fiche 85692 — Optimiser les parcours de collecte

- **Run 1 :** Valorisation matière des déchets [2]
- **Run 2 :** Valorisation matière des déchets [1]
- **Run 3 :** Valorisation matière des déchets [2]
- **Prod :** Efficacité et sobriété logistique [4]
- Catégories instables sur : Valorisation matière des déchets

#### Fiche 85699 — Création d'un réseau de tiers-lieux coopératifs pour favoriser la création d'activités locales et de start-up

- **Run 1 :** Réduction des déplacements [1]
- **Run 2 :** Réduction des déplacements [1]
- **Run 3 :** Réduction des déplacements [4]
- **Prod :** Réduction des déplacements [1]
- Catégories instables sur : Réduction des déplacements

#### Fiche 85725 — Réaliser le bilan énergétique et le suivi des consommations du patrimoine public

- **Run 1 :** Sobriété et isolation des bâtiments (tertiaire) [2]
- **Run 2 :** Sobriété et isolation des bâtiments (tertiaire) [5]
- **Run 3 :** Sobriété et isolation des bâtiments (tertiaire) [5]
- **Prod :** (aucun levier)
- Catégories instables sur : Sobriété et isolation des bâtiments (tertiaire)

#### Fiche 120930 — 4-2 Fermer les bords de Marne à la circulation routière (cohérence intercommunale et augmentation des périodes de fermeture)

- **Run 1 :** Réduction des déplacements [2]
- **Run 2 :** Réduction des déplacements [1]
- **Run 3 :** Réduction des déplacements [1]
- **Prod :** Réduction des déplacements [2]
- Catégories instables sur : Réduction des déplacements
