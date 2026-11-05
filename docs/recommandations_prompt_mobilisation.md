# Prompt de mobilisation : recommandations et points à trancher

Novembre 2026. Analyse du prompt qui note la mobilisation de chaque case levier × catégorie (étape 2 de run impact), avec la nouvelle échelle décidée par l'équipe.

## En bref

- **Le prompt demande un jugement que le texte des fiches ne permet pas de trancher** : comparer la collectivité à « ce qui serait raisonnablement attendu ». Aucune référence n'est fournie, donc chaque run imagine son propre étalon.
- **La nouvelle échelle est une règle de comptage.** Elle permet de ne plus demander de note au modèle : il suffit qu'il dise, pour chaque action, si elle est structurante ou non. Le code calcule ensuite la note. C'est la recommandation principale.
- **Une grande partie de l'instabilité vient de l'étape d'avant.** La classification de run impact utilise encore l'ancien prompt, avec tout le plan en un seul appel. Il faut d'abord la remplacer par la classification v2.3.
- **Le point à trancher en premier est la définition d'une action « structurante ».** Tout le reste en découle. Une proposition est faite en section 5.

## 1. Où est le prompt et comment il est utilisé

- **Prompt en service :** `build_prompt_implication` dans `pages/26_run_impact.py`.
  - Modèle `gpt-5.1-2025-11-13`, raisonnement « medium » (« low » si l'option est cochée).
  - Sortie en JSON libre (`json_object`), sans schéma.
  - Un appel par levier, qui renvoie 6 notes de 0 à 3, une par catégorie.
- **Variante de test :** une version plus récente est dans `utils/test_run_impact.py`. Son échelle est déjà fondée sur le nombre d'actions et la notion de « structurante », mais elle n'est pas branchée dans run impact.
- **Enchaînement :**
  1. Étape 1 : classification de tout le plan en un seul appel (ancien prompt, GPT-5.1).
  2. Regroupement des fiches par case levier × catégorie.
  3. Étape 2 : une note de 0 à 3 par case. Une case sans fiche est forcée à 0 par le code.
  4. Écriture dans la table `priorisation` (OLAP).
- **Usage en aval :**
  - libellés « Non mobilisé », « Partiellement mobilisé », « Bien mobilisé », « Pleinement mobilisé » ;
  - % de mobilisation d'un levier = moyenne des notes pondérée par les poids des catégories, divisée par 3 ;
  - « angles morts » et cibles d'actions = cases notées 0 ou 1.
- **En prod TeT :** la table `collectivite_volet_ges` a aussi une colonne `note`. Si TeT a sa propre copie de ce prompt, il faudra la changer aussi (même démarche que pour la classification).

## 2. Ce que montrent les tests existants

Les fichiers de `data/test_run_impact/` notent 10 fois chaque levier, avec une classification figée. On isole donc la seule instabilité de l'étape 2.

| Modèle | Collectivités | Cases notées | Note identique sur les 10 runs |
|---|---|---:|---:|
| Mistral Large 4, sans raisonnement | Lyon | 92 | 77 à 84 % |
| GPT-5.6 Terra, raisonnement medium | Lyon, Annecy, Poitiers | 58 à 101 | 55 à 88 % |
| gpt-oss-120b | Lyon | 18 à 59 | 33 à 42 % |

- **Environ 1 case sur 4 change d'un point d'un run à l'autre**, même avec le meilleur modèle.
- **Le libellé de l'échelle change fortement le niveau des notes.** Sur Lyon, avec le même modèle et trois versions du prompt, le nombre de notes 3 passe de 17 à 206 sur 920 notes. Les notes reflètent donc surtout la formulation de l'échelle.
- **En conditions réelles, l'instabilité s'additionne à celle de l'étape 1.** Avec l'ancien prompt de classification, seulement 55 % des fiches étaient classées pareil d'un run à l'autre (test sur 21 collectivités, avec Mistral Large 4). Une fiche qui change de case change les notes de deux cases.

## 3. Pourquoi le prompt actuel est instable

1. **Un étalon imaginaire.** La note compare la collectivité à « ce qu'une collectivité comparable et volontariste ferait ». Aucune liste de référence n'est jamais fournie, donc le modèle invente l'attendu à chaque appel.
2. **La population est donnée sans règle.** Le modèle doit « raisonner relativement à la taille », sans savoir comment, et ajuste au jugé.
3. **Des critères invisibles dans le texte.** La portée, la durée, et le fait qu'une action soit financée ou engagée ne figurent pas dans le titre et la description. Le statut, le budget et les dates de la fiche ne sont pas transmis.
4. **6 notes dans une même réponse.** Les notes d'une catégorie influencent celles des autres (effet d'ancrage).
5. **Des définitions de catégories différentes de la classification v2.3.** Par exemple, la catégorie 4 contient encore « stratégie et feuille de route », et la 1 contient « espaces verts, renaturation ». Le modèle peut rejuger la catégorie au lieu de noter.
6. **Des règles floues :**
   - « ne pas surévaluer les actions incitatives, sauf en catégorie 6 » ;
   - « en cas de doute, le niveau le plus bas » ;
   - « une action annoncée ne peut pas porter un 3 », alors que le modèle ne voit pas le statut.
7. **Aucune justification gardée.** Le raisonnement reste interne, donc impossible à relire ou à corriger.
8. **Une sortie sans schéma**, sans `temperature` fixée, avec un modèle à raisonnement.

## 4. La nouvelle échelle

| Note | Définition retenue |
|---|---|
| 0 | Aucune action |
| 1 | Une action peu importante |
| 2 | Plusieurs actions peu importantes, ou une action structurante |
| 3 | Plusieurs actions structurantes |

**C'est une règle de comptage.** Une fois chaque action jugée « structurante » ou « peu importante », la note se calcule sans modèle :

| Actions structurantes | Actions peu importantes | Note |
|---:|---:|---:|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 0 | 2 ou plus | 2 |
| 1 | autant qu'on veut | 2 |
| 2 ou plus | autant qu'on veut | 3 |

**Conséquences :**
- **La note 0 devient automatique :** elle correspond exactement à une case vide. Le code le fait déjà.
- **Toute case avec une action vaut au moins 1.** Aujourd'hui, quelques cases avec actions sont notées 0. Elles passeront à 1.
- **L'échelle n'est pas forcément plus douce au total.** Dans les tests, la majorité des cases non vides ont déjà 2 actions ou plus :
  - Lyon : 64 cases sur 92 ;
  - Poitiers : 67 sur 101 ;
  - Annecy : 26 sur 58.

  Elles auront donc au moins 2, ce qui est proche de la répartition actuelle. Ce qui change surtout : il faudra 2 actions structurantes pour un 3, et les cases à une seule action se partageront entre 1 et 2.
- **Les grandes collectivités, qui ont plus de fiches, obtiendront plus facilement 2 et 3** (voir T6).

## 5. Recommandations

### R1 — Brancher run impact sur la classification v2.3

Remplacer l'étape 1 par la classification v2.3 : une fiche par appel, Claude Haiku 5.5, sortie contrainte. Elle est stable à 90 % sur 1 674 fiches, contre 55 % pour l'ancien prompt. Une fois la v2.3 en prod, on peut lire directement `fiche_action_volet_ges`. C'est le gain de stabilité le plus important, et il ne dépend d'aucun arbitrage.

### R2 — Ne plus demander de note : juger chaque action, puis compter

Le modèle ne répond plus qu'à une question fermée par action : « structurante » ou « peu importante », avec une justification courte. Le code applique ensuite la table de la section 4.

- **Option A, recommandée :** ajouter ce jugement à la sortie de la classification v2.3 (un champ `structurante` par levier). Pas d'appel supplémentaire, et le jugement se fait fiche par fiche, sans être influencé par les autres fiches.
- **Option B :** un appel séparé par fiche et par levier, après la classification. Plus coûteux, mais le prompt de classification reste inchangé.

Avantages :
- une question binaire par fiche est bien plus stable qu'une note qui agrège plusieurs fiches ;
- chaque note s'explique (« 2 : une action structurante, la fiche n° 123 ») ;
- si l'équipe change la règle de comptage, on recalcule les notes sans rappeler le modèle.

### R3 — Une définition observable de « structurante »

Proposition à valider (T1). Une action est **structurante** si elle remplit les deux conditions :
- **Portée :** elle concerne tout le territoire ou tout le public visé, ou elle crée un équipement ou un dispositif majeur.
- **Durée ou moyens :** c'est un dispositif permanent, pluriannuel ou opposable, ou la fiche cite des moyens dédiés (budget, poste, objectif chiffré).

Sinon, elle est **peu importante** : action ponctuelle (événement, expérimentation, une installation, un seul bâtiment), étude seule, intention, communication isolée.

Exemples par catégorie, à compléter avec l'équipe :

| Catégorie | Structurante | Peu importante |
|---|---|---|
| 1 Aménagement | Réseau cyclable ou réseau de chaleur à l'échelle du territoire | Quelques arceaux vélo, une borne |
| 2 Planification | PLUi avec règles ou OAP sur le sujet ; schéma directeur adopté | Mention du sujet dans un document |
| 3 Financement | Aide pérenne avec budget annuel | Appel à projets ponctuel |
| 4 Gouvernance | Instance permanente, poste dédié, observatoire | Une réunion, une étude seule |
| 5 Exemplarité | Plan pluriannuel de rénovation du patrimoine ; renouvellement de la flotte | Un bâtiment, un véhicule |
| 6 Sensibilisation | Guichet ou conseil permanent ; programme annuel d'animations | Un événement, une campagne isolée |

### R4 — Transmettre les champs objectifs de la fiche

TeT stocke des informations plus fiables que le texte libre. Taux de remplissage sur les fiches non restreintes :

| Champ | Fiches renseignées |
|---|---:|
| Statut | 96 % |
| Description | 71 % |
| Objectifs | 36 % |
| Dates | 17 à 22 % |
| Budget prévisionnel | 10 % |

- Les donner au modèle quand ils sont remplis, pour juger « structurante ».
- Filtrer en amont, par le code, les fiches « Abandonné » (environ 600), et sans doute « En pause » (T4).

### R5 — Ne plus donner la population au modèle

Si l'équipe veut tenir compte de la taille de la collectivité, le faire par une règle dans le code (T2, T6), pas au jugé du modèle.

### R6 — Sortie contrainte, modèle sans raisonnement, justification gardée

- Même socle technique que la classification v2.3 : Claude Haiku 5.5, schéma strict (`structurante` : booléen, `justification` : texte court), prompt en cache.
- Garder la justification en base pour la relecture.
- Coût estimé : quelques centimes par collectivité.

### R7 — Aligner les définitions sur le référentiel

Le prompt de mobilisation ne doit plus redéfinir les catégories ni les leviers. Si un texte de catégorie est nécessaire, il doit être celui du référentiel v2.3 (la page Notion de référence).

### R8 — Mesurer avant de déployer

- **Stabilité :** 3 runs sur les 100 fiches du jeu de test, comme pour la classification.
- **Justesse :** faire annoter « structurante » par l'équipe sur ces 100 fiches, en même temps que la relecture de la classification.
- **Comparaison :** recalculer les notes de 4 ou 5 collectivités et les comparer aux notes actuelles, avec l'équipe métier.

### R9 — Mettre à jour les écrans de priorisation

- **Libellés des notes :** « Partiellement mobilisé » ne correspond plus au 1 (« une action peu importante »). Proposition :
  - 0 = Non mobilisé ;
  - 1 = Amorcé ;
  - 2 = Mobilisé ;
  - 3 = Fortement mobilisé.
- **Seuils :** revoir « angle mort = note 0 ou 1 » et le seuil de % de mobilisation du quadrant.
- **Historique :** recalculer toutes les collectivités. Les notes ne sont pas comparables entre l'ancienne et la nouvelle échelle.

## 6. Points à trancher

| # | Question | Proposition |
|---|---|---|
| T1 | Définition de « structurante » | Portée (tout le territoire, tout le public visé, ou équipement majeur) ET durée ou moyens (permanent, pluriannuel, opposable, ou moyens dédiés cités). Tableau d'exemples de R3. |
| T2 | « Structurante » dépend-il de la taille de la collectivité ? Une commune de 2 000 habitants qui rénove sa seule école, est-ce structurant ? | Oui pour la portée (« tout le patrimoine » d'une petite commune peut être un seul bâtiment) : le modèle juge la part du territoire ou du public couverte, pas la taille absolue. |
| T3 | Qu'est-ce qu'« une action » : une fiche, ou chaque sous-action listée dans la description ? | Une fiche. C'est objectif et stable. Une fiche qui regroupe beaucoup de mesures a plus de chances d'être structurante. |
| T4 | Quels statuts comptent ? | Exclure « Abandonné ». « En pause » : à décider. « À venir » et « À discuter » comptent, mais l'équipe peut décider qu'une action non engagée n'est jamais structurante. |
| T5 | Une fiche classée sur plusieurs leviers ou catégories compte-t-elle dans chaque case ? | Oui (c'est le cas aujourd'hui). Le jugement « structurante » peut différer d'un levier à l'autre (option A de R2). |
| T6 | « Plusieurs actions peu importantes » : à partir de 2, ou de 3 ? | 2, comme l'échelle le dit. À revoir si les grandes collectivités se retrouvent toutes à 2. |
| T7 | 1 action structurante + 5 actions peu importantes = 2 ? | Oui, selon l'échelle : le 3 exige au moins 2 actions structurantes. À confirmer. |
| T8 | Une étude seule (désormais en catégorie 4) peut-elle être structurante ? Et un observatoire ? | Étude seule = peu importante. Observatoire permanent = structurant. |
| T9 | Garder un traitement à part pour la catégorie 6 (« l'incitatif est le cœur du sujet ») ? | Inutile avec R3 : un dispositif permanent de conseil est structurant, un événement isolé ne l'est pas. |
| T10 | Libellés et seuils des écrans (R9) | Libellés proposés en R9. Angle mort = note 0 ou 1, à garder et à revoir après le premier recalcul. |
| T11 | Option A ou B de R2 (jugement dans la classification ou appel séparé) ? | A : un seul appel par fiche, moins cher, et classification et mobilisation restent cohérentes. |
