# Prompt de mobilisation : décisions et suite

Novembre 2026. Le prompt qui note la mobilisation de chaque case levier × catégorie (étape 2 de run impact, `build_prompt_implication` dans `pages/26_run_impact.py`) est remplacé. Ce document donne les décisions prises le 5 novembre, ce qu'il reste à trancher et le plan de mise en œuvre.

## En bref

- **On ne demande plus de note au modèle.** La classification v2.3 dit en plus, pour chaque levier d'une fiche, si l'action est **structurante** ou **peu importante**. Le code calcule ensuite la note de chaque case. Il n'y a plus qu'un seul prompt, une fiche par appel.
- **Structurante = portée ET durée.** Les moyens (budget, poste) ne comptent pas.
- **Run impact utilise la classification v2.3**, à la place de l'ancienne classification de tout le plan en un seul appel.
- **Chaque fiche est envoyée avec ses sous-actions,** et avec le type et la population de la collectivité. Les fiches abandonnées ou en pause sont exclues.

## 1. Décisions

| # | Sujet | Décision |
|---|---|---|
| R1 | Classification de run impact | Remplacée par la classification v2.3 (une fiche par appel, Claude Haiku 5.5) |
| R2 | Note | Le modèle juge « structurante » ou non pour chaque levier de la fiche, dans le même appel que la classification (option A). Le code calcule la note. |
| R3 | Définition de « structurante » | Portée ET durée, précisées par catégorie (section 2). Les moyens ne comptent pas. |
| R4 | Statut, budget, dates | Pas transmis au modèle : ces champs sont trop inégalement remplis pour être un critère objectif |
| R5 | Taille de la collectivité | Le modèle ne module plus la note selon la taille. Le type et la population sont donnés seulement pour juger la portée (T2). |
| R6 | Justification | Aucune : le modèle ne renvoie que la classification et le booléen |
| R7 | Définitions | Une seule source : le prompt de classification, qui absorbe la mobilisation |
| R8 | Mesure | Stabilité sur 3 runs et relecture de « structurante » sur le jeu de 100 fiches, avant déploiement |
| R9 | Écrans de priorisation | Libellés et seuils à revoir ; toutes les collectivités à recalculer |
| T3 | Qu'est-ce qu'une action | Une fiche : son titre, sa description, et la liste de ses sous-actions ajoutée à la description |
| T4 | Statuts | Fiches « Abandonné » et « En pause » exclues par le code, avant le modèle |
| T5 | Fiche sur plusieurs cases | Elle compte dans chaque case levier × catégorie |
| T6 | « Plusieurs » | À partir de 2 |
| T7 | 1 structurante + des actions peu importantes | Note 2 : le 3 exige au moins 2 actions structurantes |
| T8 | Études et observatoires | Étude seule = peu importante ; observatoire permanent = structurant |
| T9 | Catégorie 6 | Pas de traitement à part : la définition de la section 2 suffit |
| T11 | Où placer le jugement | Dans l'appel de classification (option A) |

## 2. Définition de « structurante »

Une action est **structurante** pour un levier si elle remplit les deux conditions :

- **Portée :** elle couvre tout le territoire de la collectivité, ou tout le public visé par le levier (tous les ménages, toutes les entreprises concernées, tout le patrimoine de la collectivité, tous ses agents), ou elle crée un équipement qui dessert une large part du territoire. La portée se juge par rapport au territoire de la collectivité, d'où le type et la population dans le message.
- **Durée :** c'est un dispositif permanent ou pluriannuel, ou une règle qui s'impose durablement (voir T1).

Sinon, elle est **peu importante.** Par exemple : un événement, une campagne, une expérimentation, une étude, une action unique ou localisée (un bâtiment, une rue, quelques installations), une intention.

| Catégorie | Structurante | Peu importante |
|---|---|---|
| 1 Aménagement | Réseau ou programme d'équipement à l'échelle du territoire : réseau cyclable intercommunal, réseau de chaleur, déploiement de bornes sur toutes les communes | Aménagement localisé : une rue, un parking, quelques arceaux, une borne, une expérimentation |
| 2 Planification | Document ou règle à l'échelle du territoire, avec un contenu sur le levier : PLUi avec règles ou OAP sur le sujet, SCoT, schéma directeur vélo, ZFE | Simple mention du sujet dans un document ; règle localisée (un arrêté de circulation sur une rue) |
| 3 Financement | Aide ou tarification permanente ou pluriannuelle, ouverte à tout le public visé : prime vélo reconduite, aide à la rénovation, redevance incitative généralisée | Appel à projets ponctuel, aide unique, aide limitée à un quartier ou à une expérimentation |
| 4 Gouvernance | Instance permanente (comité, COP), poste ou service dédié, observatoire, convention pluriannuelle | Étude ou diagnostic seul, réunion, lettre d'intention, partenariat ponctuel |
| 5 Exemplarité | Plan pluriannuel sur tout le patrimoine, toute la flotte ou tous les agents : rénovation de l'ensemble des bâtiments, renouvellement de la flotte, plan de mobilité pour tous les agents | Un bâtiment, quelques véhicules, une formation ponctuelle |
| 6 Sensibilisation | Dispositif permanent ouvert à tout le public visé : guichet France Rénov', conseil en énergie partagé, programme annuel d'animations | Un événement, une campagne, un atelier, une page d'information |

**Hypothèse à valider au test :** le jugement est fait par levier, pas par catégorie. Une fiche avec un grand réseau cyclable (1) et une simple communication (6) est structurante pour le levier vélo, donc dans ses deux cases. Le juger catégorie par catégorie serait plus précis, mais moins stable. On regardera les cas concernés dans le jeu de test.

## 3. Calcul de la note d'une case

Pour chaque case levier × catégorie, on compte les fiches qui y sont classées :

| Fiches structurantes | Fiches peu importantes | Note |
|---:|---:|---:|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 0 | 2 ou plus | 2 |
| 1 | autant qu'on veut | 2 |
| 2 ou plus | autant qu'on veut | 3 |

La note devient explicable : « 2 : une action structurante, la fiche n° 123 ». Si l'équipe change la règle, on recalcule sans rappeler le modèle.

## 4. Réponses aux questions

### T1 — Qu'est-ce qu'« opposable » ?

Un document ou une règle **opposable** s'impose juridiquement à tous, et on peut s'en prévaloir contre un tiers. Par exemple, un permis de construire doit respecter le PLU, et un arrêté de ZFE s'applique à tous les véhicules.

Je l'avais rangé dans « durée » parce qu'une telle règle s'applique tant qu'elle n'est pas modifiée. Dans la définition de la section 2, il est reformulé en « une règle qui s'impose durablement » (PLU, règlement, arrêté, ZFE). Concrètement, ça ne concerne que la catégorie 2.

### T2 — Donne-t-on la population ?

Oui, avec le type de collectivité, mais seulement pour juger la portée. Ce qui change par rapport à aujourd'hui : le modèle ne doit plus « noter relativement à la taille » ; il juge si l'action couvre tout le territoire ou tout le public visé.

Le type est disponible dans la table `collectivite` :
- `nature_insee` pour les EPCI : CC (996), CA (226), METRO (22), syndicats, PETR… ;
- `type` pour les communes, départements et régions.

Le message envoyé au modèle commencerait par une ligne du type :

```
Collectivité : communauté d'agglomération, 215 000 habitants
```

### T3 — Sous-actions

Ce n'est pas fait aujourd'hui. Run impact et la classification v2.3 ne prennent que les fiches parentes (`parent_id IS NULL`), sans leurs sous-actions. En prod, 8 154 fiches ont des sous-actions, 32 377 sous-actions au total. Il faut :
- ajouter à la description de la fiche une liste « Sous-actions : » avec le titre de chaque sous-action non supprimée ;
- exclure les sous-actions abandonnées ou en pause, comme les fiches.

**Reste à trancher :** ajouter les seuls titres des sous-actions, ou aussi leurs descriptions ? Je propose les titres seuls, pour garder des messages courts. Une fiche avec 40 sous-actions détaillées ferait sinon des milliers de tokens.

### T10 — Angles morts

Il y a deux calculs dans le code, et la nouvelle échelle touche les deux :
- **La matrice par levier** (`utils/priorisation_matrice_leviers.py`) : un levier est un angle mort si son impact est fort et sa mobilisation inférieure à 50 %. La mobilisation est la moyenne des notes, pondérée par les poids des catégories, divisée par 3. Le seuil de 50 % correspond à une moyenne de 1,5.
- **La page faisabilité et les cibles d'actions** (`utils/priorisation_faisabilite.py`, `utils/priorisation_tab_actions.py`) : une case est un angle mort si sa note est 0 ou 1.

Avec la nouvelle échelle, une case avec une seule action peu importante vaut 1. Elle restera donc un angle mort sur la page faisabilité. Le seuil de 50 % de la matrice est à revoir après le premier recalcul.

## 5. Reste à trancher

| # | Question | Proposition |
|---|---|---|
| T1 bis | Reformuler « opposable » en « une règle qui s'impose durablement » ? | Oui |
| T3 bis | Sous-actions : titres seuls, ou titres et descriptions ? | Titres seuls |
| T12 | « Structurante » jugé par levier ou par catégorie ? | Par levier, à vérifier sur le jeu de test (section 2) |
| T13 | Libellés des notes dans les écrans | 0 Non mobilisé, 1 Amorcé, 2 Mobilisé, 3 Fortement mobilisé |
| T14 | Seuil de 50 % de la matrice | À revoir après le recalcul de 4 ou 5 collectivités |

## 6. Plan de mise en œuvre

1. **Prompt v2.4** = v2.3 + la définition de « structurante » + le tableau par catégorie + quelques exemples. Le schéma de sortie ajoute `structurante: bool` à chaque levier.
2. **Message utilisateur :**
   - une ligne « Collectivité : type, population » ;
   - la liste des sous-actions dans la description ;
   - les fiches et sous-actions abandonnées ou en pause filtrées.
3. **Test sur les 100 fiches :** 3 runs, mesure de la stabilité de la classification et de « structurante ». Une colonne « Structurante » est ajoutée à l'Excel pour la relecture d'Emeline.
4. **Calcul des notes** dans le code (section 3), puis recalcul de 4 ou 5 collectivités et comparaison avec les notes actuelles.
5. **Branchement dans run impact :**
   - l'étape 1 est remplacée par la v2.4 ;
   - l'étape 2 (`build_prompt_implication`) est supprimée ;
   - les libellés des écrans sont mis à jour.
6. **Mise à jour du doc de passation et de la page Notion de référence.** Si TeT a sa propre copie du prompt de mobilisation (colonne `note` de `collectivite_volet_ges`), elle est remplacée aussi.
