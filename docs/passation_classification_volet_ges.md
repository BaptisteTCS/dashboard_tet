# Passation : classification volet GES des fiches actions (prompt v2.3)

> Document à donner tel quel à Claude Code, ouvert dans le dépôt de prod de Territoires en Transitions (TeT).
> Il décrit ce qu'il faut remplacer dans la classification des fiches actions par levier CO2 et par catégorie : architecture, modèle, prompt exact, schéma de sortie, post-traitement et écriture en base.
> Tout ce qui est ici a été testé hors prod, en lecture seule (outil d'analyse Streamlit, novembre 2026). Rien n'a encore été modifié en prod.

## 0. Instructions pour Claude Code

Tu travailles dans le code de prod de TeT. Ta mission : remplacer la classification actuelle des fiches actions (table `fiche_action_volet_ges`) par celle décrite ici.

1. **Trouve le code actuel.** Cherche les écritures dans `fiche_action_volet_ges`, le texte du prompt actuel (« Tu es un expert en analyse d'impact carbone », « Liste des leviers CO2 », « Les 6 catégories »), et l'appel au modèle (OpenAI ou Mistral). Le prompt actuel envoie plusieurs fiches dans un même appel et attend un JSON `{"<id_fiche>": {"<libellé du levier>": [catégories]}}`.
2. **Remplace la logique** par l'architecture de la section 3 : une fiche par appel, le prompt système de la section 4 envoyé à l'identique, le modèle `claude-haiku-5-5`, et la sortie contrainte de la section 5.
3. **Ne change pas :**
   - le schéma des tables ;
   - les valeurs des enums `levier_id` et `categorie` ;
   - la sélection des fiches à classer ;
   - ce qui est calculé en aval à partir de `fiche_action_volet_ges` (par exemple `collectivite_volet_ges`).
   Si le code en aval lit des libellés de leviers plutôt que des codes, garde-le cohérent avec la table de la section 5.3.
4. **Stocke le prompt dans un fichier versionné** (par exemple `classification_volet_ges_v2.3.md`), lu tel quel. Ne le reconstruis pas avec une f-string ou un template : il contient des accolades JSON.
5. **Unique changement visible côté interface :** le levier `vehicules_electriques` s'affiche « Voiture électrique » au lieu de « Véhicules électriques ». Le code reste le même.
6. **Vérifie** avec la section 8 avant de livrer.
7. **Si le code de TeT ne correspond pas** à ce que ce document suppose (autre table, autre format de catégorie, autre déclenchement), arrête-toi et pose la question au développeur, plutôt que de deviner.

## 1. Ce qui change

| | Avant (prod actuelle) | Après (v2.3) |
|---|---|---|
| Modèle | GPT-5.1 dans la copie de référence de l'outil d'analyse. À vérifier dans TeT, sans doute un modèle OpenAI ou Mistral. | `claude-haiku-5-5` (Anthropic), sans raisonnement étendu |
| Découpage | Tout le plan, ou des lots de fiches, dans un seul appel | **Une fiche par appel**, appels en parallèle |
| Prompt | Liste des libellés de leviers, définition courte des 6 catégories, 4 règles générales | Prompt v2.3 : définition de chaque levier (ce qu'il inclut et exclut), règles par catégorie, liste des sujets sans levier, cas particuliers, 32 exemples résolus |
| Entrée | `[id=…] titre : description` concaténés dans le prompt | Message utilisateur séparé : contexte (plan > axe > sous-axe), titre, description |
| Sortie | JSON libre indexé par id de fiche, libellés de leviers en texte | JSON contraint par un schéma : `{"leviers": [{"levier": <code>, "categories": [1-6]}]}`, avec les codes de l'enum prod |
| Plafonds | Aucun | 3 leviers maximum par fiche ; au moins 1 catégorie par levier ; pas de plafond de catégories |
| Cache | Aucun | Prompt système en cache (`cache_control`), plus de 90 % des tokens d'entrée lus en cache |
| Libellé affiché | « Véhicules électriques » | « Voiture électrique » (code `vehicules_electriques` inchangé) |

## 2. Pourquoi : résultats des tests

Les tests ont été faits sur 21 collectivités, soit 1 674 fiches. Chaque fiche a été classée 3 fois avec le même prompt. Une fiche est **stable** si les 3 réponses sont identiques.

| Configuration | Fiches stables | Fiches classées stables | Coût pour 1 674 fiches, 1 passage |
|---|---:|---:|---:|
| Prompt actuel, Mistral Large 4, lots de 25 fiches (21 collectivités) | 55 % | 32 % | 1,10 $ |
| Prompt v2.0, Mistral Large 4, 1 fiche par appel (4 collectivités, 393 fiches) | 82 % | 70 % | 6,53 $ |
| Prompt v2.1, Mistral Small 2603, 1 fiche par appel (393 fiches) | 84 % | 70 % | 1,37 $ (maximum) |
| **Prompt v2.1, Claude Haiku 5.5, 1 fiche par appel (393 fiches)** | **93 %** | **88 %** | **0,26 $** |
| Prompt v2.1, Claude Haiku 5.5 (21 collectivités, 1 674 fiches) | 90 % | — | 0,30 $ |
| Prompt v2.2, Claude Haiku 5.5 (100 fiches avec description, les plus difficiles) | 80 % | — | ≈ 0,4 $ |
| **Prompt v2.3, Claude Haiku 5.5 (les mêmes 100 fiches)** | **89 %** | — | ≈ 0,45 $ |

« Fiches classées stables » se lit parmi les fiches qui ont reçu au moins un levier dans un des 3 runs.

- **Les gains viennent surtout de trois changements :**
  - une fiche par appel : dans les lots, les fiches voisines se contaminaient ;
  - des définitions de leviers avec ce qu'ils incluent et excluent ;
  - une sortie contrainte par des codes : plus de libellés inventés.
- **Haiku 5.5 est le plus stable et le moins cher.** Mistral Large 4 coûte 25 fois plus, à cause de son raisonnement, sans être plus stable.
- **La v2.2 coûte un peu plus que la v2.1.** Elle intègre les arbitrages métier de l'équipe (section 9) et son prompt est plus long : environ 11 000 tokens contre 9 100.
- **La v2.3 est la version à déployer.** Elle ajoute à la v2.2 les derniers arbitrages de l'équipe : études et observatoires en gouvernance, autopartage, collecte et achats responsables en prévention des déchets, éclairage public et confort d'été, agriculture biologique, végétalisation (section 9). Sur les 100 fiches les plus difficiles, elle passe de 80 % à 89 % de fiches stables. Le code et l'architecture ne changent pas, seul le prompt change.
- **La stabilité n'est pas la justesse.** Un jeu de référence de 100 fiches, corrigées à la main, est en cours de relecture. La précision du prompt n'est pas encore mesurée.

## 3. Architecture cible

```
pour chaque collectivité à classer :
    fiches   = sélection actuelle de TeT (inchangée)
    contexte = chemin des axes de chaque fiche (3.2)
    pour chaque fiche, en parallèle (8 appels simultanés testés) :
        message  = message utilisateur (3.3)
        réponse  = appel Haiku : prompt système en cache + outil forcé en mode strict (3.4)
        leviers  = post-traitement et validation (3.5), avec jusqu'à 3 essais si la réponse est invalide
    écriture : pour chaque fiche classée, remplacer ses lignes dans fiche_action_volet_ges (3.6)
```

### 3.1 Sélection des fiches

Ne change pas la sélection actuelle de TeT. Pour information, les tests ont porté sur les fiches de la collectivité rattachées à un axe du plan (`fiche_action_axe`), avec `parent_id IS NULL` et non supprimées.

### 3.2 Contexte : chemin des axes

Chaque fiche est précédée de sa place dans le plan, par exemple « PCAET 2024-2030 > Mobilité > Mobilités douces ». Les titres courts (« PIG », « Former les élus ») deviennent ainsi compréhensibles. Ce chemin se calcule par une requête récursive sur `axe` (colonnes `id`, `nom`, `parent`) :

```sql
WITH RECURSIVE chaine AS (
    SELECT faa.fiche_id, a.id AS depart, a.nom, a.parent, 0 AS profondeur
    FROM fiche_action_axe faa
    JOIN axe a ON a.id = faa.axe_id
    JOIN fiche_action fa ON fa.id = faa.fiche_id
    WHERE fa.collectivite_id = :cid
    UNION ALL
    SELECT c.fiche_id, c.depart, p.nom, p.parent, c.profondeur + 1
    FROM chaine c
    JOIN axe p ON p.id = c.parent
    WHERE c.profondeur < 10
)
SELECT fiche_id, depart,
       string_agg(COALESCE(NULLIF(trim(nom), ''), '(sans nom)'), ' > '
                  ORDER BY profondeur DESC) AS chemin
FROM chaine
GROUP BY fiche_id, depart
```

- La racine de la chaîne est l'axe de niveau plan : son `nom` est le nom du plan.
- Une fiche rattachée à plusieurs axes a plusieurs chemins. Trie-les, enlève les doublons et joins-les par « | ».
- Une fiche sans axe a le contexte « non renseigné ».

### 3.3 Message utilisateur

Le message utilisateur contient seulement la fiche, au format exact suivant (3 lignes) :

```
Contexte : <chemin des axes, ou « non renseigné »>
Titre : <titre>
Description : <description, ou « aucune »>
```

- Les blancs du titre et de la description (retours à la ligne, espaces multiples) sont réduits à un seul espace.
- Titre vide : « (sans titre) ».
- Description vide, nulle ou égale à « nan » : « aucune ».
- La description a été envoyée **brute**, avec son éventuel HTML. Retirer le HTML réduirait un peu le nombre de tokens, mais ce n'est pas testé. Garde la description brute pour rester identique aux tests.

### 3.4 Appel au modèle (API Messages d'Anthropic)

- **Modèle :** `claude-haiku-5-5`. Pas de raisonnement étendu (`thinking`). Pas de `temperature` fixée : les tests ont utilisé la valeur par défaut, et l'équipe a décidé de ne pas la fixer.
- **Prompt système :** envoyé comme un bloc texte avec `cache_control: {"type": "ephemeral"}`. Il est identique à chaque appel et la fiche est dans le message utilisateur : c'est ce qui permet le cache (durée de vie 5 minutes). Ne mets rien de variable dans le prompt système.
- **Sortie forcée :** un outil `classer_fiche` dont le schéma d'entrée est celui de la section 5.1, en mode `strict: true`, avec `tool_choice` qui force cet outil. Avec le mode strict, un code de levier ou une catégorie hors liste sont impossibles. Le mode strict refuse `maxItems` : le plafond de 3 leviers est appliqué en post-traitement.
- **`max_tokens` :** 1024. Une réponse fait environ 60 tokens.

Corps de la requête (`POST https://api.anthropic.com/v1/messages`, en-têtes `x-api-key` et `anthropic-version: 2023-06-01`) :

```json
{
  "model": "claude-haiku-5-5",
  "max_tokens": 1024,
  "system": [
    {"type": "text", "text": "<contenu exact du prompt de la section 4>", "cache_control": {"type": "ephemeral"}}
  ],
  "messages": [
    {"role": "user", "content": "Contexte : …\nTitre : …\nDescription : …"}
  ],
  "tools": [
    {
      "name": "classer_fiche",
      "description": "Renvoie la classification de la fiche action.",
      "input_schema": "<schéma de la section 5.1>",
      "strict": true
    }
  ],
  "tool_choice": {"type": "tool", "name": "classer_fiche"}
}
```

La réponse contient un bloc `tool_use` dont `input` est la classification, par exemple `{"leviers": [{"levier": "velo_transport_commun", "categories": [1]}]}`.

### 3.5 Post-traitement, validation et reprises

1. Si `leviers` a plus de 3 éléments, garde les 3 premiers (le modèle les donne du plus direct au moins direct). C'est arrivé environ 1 fois sur 100 appels.
2. Pour chaque élément, vérifie :
   - que le code est dans la liste de la section 5.3 ;
   - que `categories` est non vide ;
   - que chaque catégorie est un entier de 1 à 6.
   Si le même levier apparaît deux fois, fusionne ses catégories.
3. Si la réponse est invalide (pas de bloc `tool_use`, JSON illisible, contrôle 2 en échec), refais l'appel, jusqu'à 3 essais au total. En mode strict, ça n'est arrivé sur aucun des quelque 5 600 appels de test.
4. Si l'API est indisponible (HTTP 429, 500, 502, 503, 529, ou timeout), attends 10 secondes et réessaie, jusqu'à 20 fois. Ces reprises ne comptent pas dans les 3 essais.
5. Si une fiche échoue après tout ça, journalise l'erreur et **ne touche pas** à ses lignes existantes en base. Ne la vide pas.
6. `{"leviers": []}` est une réponse valide : la fiche n'a aucun levier.

### 3.6 Écriture en base

`fiche_action_volet_ges` contient une ligne par paire levier × catégorie : `fiche_id`, `levier_id` (enum), `categorie` (enum), `created_at`.

- `levier_id` = le code renvoyé par le modèle. Les codes sont exactement les valeurs de l'enum prod (section 5.3).
- `categorie` = l'entier converti en valeur d'enum (section 5.4).
- Pour une fiche classée, remplace toutes ses lignes en une seule transaction : suppression puis insertion.
- Une fiche avec `{"leviers": []}` n'a aucune ligne : elle est « non classée », comme aujourd'hui.

Exemple : la réponse `{"leviers": [{"levier": "velo_transport_commun", "categories": [1, 3]}, {"levier": "covoiturage", "categories": [1]}]}` donne 3 lignes :
- (fiche, `velo_transport_commun`, `amenagement`) ;
- (fiche, `velo_transport_commun`, `financement`) ;
- (fiche, `covoiturage`, `amenagement`).

Les tables et calculs en aval (`collectivite_volet_ges`, calcul d'impact, priorisation) gardent leur logique. Ils reçoivent des données au même format.

### 3.7 Parallélisme, cache et coûts

- **Parallélisme :** 8 appels simultanés ont été testés sans erreur de quota.
- **Cache :**
  - Le premier appel écrit le prompt système en cache (environ 12 600 tokens). Les suivants le lisent, pour 10 % du prix de l'entrée.
  - Pour éviter que les 8 premiers appels parallèles écrivent tous le cache, tu peux envoyer la première fiche seule, puis lancer les autres. C'est une optimisation facultative : le gain est inférieur à un centime par collectivité.
  - Pour vérifier que le cache fonctionne, `usage.cache_read_input_tokens` doit être supérieur à 0 à partir du 2e appel.
- **Tokens par fiche :**
  - environ 12 600 tokens de prompt système et d'outil, lus en cache ;
  - environ 800 tokens de fiche, non mis en cache ;
  - environ 60 tokens de sortie.
- **Tarifs `claude-haiku-5-5` (USD par million de tokens) :** entrée 0,10, lecture du cache 0,01, écriture du cache 0,125, sortie 0,50. Source : page tarifs d'Anthropic, pour des prompts de moins de 100 000 tokens.
- **Coût mesuré :**
  - environ 0,025 centime par fiche ;
  - environ 0,4 $ pour classer les 1 674 fiches des 21 collectivités de test ;
  - environ 0,25 $ pour 1 000 fiches.
- **Durée :** environ 3 minutes pour 1 200 appels avec 8 en parallèle.

## 4. Prompt système exact (v2.3)

À copier à l'identique dans un fichier. Ce bloc est le contenu complet du fichier, et rien d'autre. Ne modifie rien (ponctuation, espaces insécables, accolades) sans refaire les tests.

````markdown
Tu es un expert en analyse d'impact carbone des politiques publiques locales et en modélisation par leviers CO2.

# Ta tâche

On te donne UNE fiche action du plan de transition d'une collectivité : sa place dans le plan (plan, axe, sous-axe), son titre et parfois sa description.

Tu indiques :
- les leviers CO2 sur lesquels l'action agit de façon claire et directe (0 à 3 leviers) ;
- pour chaque levier retenu, la ou les catégories de type d'action par lesquelles la collectivité agit.

# Règles générales

1. La précision prime sur l'exhaustivité. Si le lien avec un levier est indirect, spéculatif ou dépend d'hypothèses non écrites, ne retiens pas ce levier.
2. Ne retiens que ce que la fiche dit. Le contexte (plan, axe, sous-axe) sert à comprendre un titre court ou ambigu ; il ne suffit pas à lui seul à retenir un levier.
3. Au maximum 3 leviers par fiche. Si plus de 3 leviers semblent concernés, l'action est transversale : garde les 3 sur lesquels elle agit le plus directement.
4. Chaque levier retenu a au moins une catégorie. Donne d'abord la catégorie principale, c'est-à-dire le moyen par lequel l'action agit le plus directement. La plupart des fiches n'ont qu'une catégorie. N'ajoute une autre catégorie que si la fiche décrit explicitement un autre moyen d'action distinct, qu'elle va réellement mettre en œuvre (par exemple : construire une piste cyclable ET verser une aide à l'achat de vélos). Un moyen possible, sous-entendu ou seulement évoqué ne compte pas. Dans le doute, une seule catégorie.
5. Les catégories décrivent l'action, pas le levier : donne les mêmes catégories à tous les leviers de la fiche. Ne les différencie que si la fiche prévoit des moyens différents selon les leviers (par exemple : des aides pour les chaudières fioul, et seulement de l'information pour les chaudières gaz).
6. Si aucun levier ne convient, renvoie une liste vide.
7. Ne déduis jamais ce que la fiche ne dit pas : pas de motorisation (électrique, bioGNV, hydrogène) si elle n'est pas citée, pas d'aide financière si aucun versement n'est cité, pas de changement de chauffage s'il n'est pas cité.

# Les 6 catégories de type d'action

La catégorie ne décrit pas l'impact carbone, mais le MOYEN par lequel la collectivité agit.

**1 — Aménagement & infrastructures.** L'action réalise un aménagement physique, un équipement ou un service ouvert au public : travaux, construction, installation, ouverture ou expérimentation d'un service (autopartage, transport à la demande, ressourcerie, déchèterie, plateforme de covoiturage). Un service numérique compte comme un service s'il permet d'agir (réserver, s'inscrire, mettre en relation, déclarer) ; un site ou une page qu'on ne peut que consulter est en 6. Un équipement porté par la commune, mais dont les bénéficiaires sont les habitants ou les entreprises (réseau de chaleur, centrale solaire partagée, borne de recharge publique), est en 1.

**2 — Réglementation & planification.** Tout document ou acte qui fixe ce qui sera fait sur le territoire : PLU/PLUi, SCoT, PCAET, PLH, plan de mobilité, schémas directeurs, stratégies et feuilles de route qui fixent des actions, programmes pluriannuels, règlements, arrêtés, ZFE, cahiers des charges imposés. Élaborer ou réviser un document est en 2. Une étude ou un diagnostic seul n'est pas en 2 (voir 4). Mettre en œuvre un schéma ou un plan existant se classe selon les moyens de sa mise en œuvre : 1 pour les travaux et équipements, plus 3 si des aides sont versées, plus 6 si de l'information ou de la sensibilisation est prévue.

**3 — Financement & fiscalité.** La collectivité verse de l'argent ou un avantage financier à un tiers : subvention, prime, aide, appel à projets doté, tarification incitative (y compris la redevance incitative des déchets), exonération. Dès qu'une aide est versée, la catégorie 3 est obligatoire. Informer sur des aides que la collectivité ne verse pas n'est pas du 3 (c'est du 6). « Soutenir », « aider », « encourager », « favoriser » ou « inciter » sans mention d'un versement d'argent ne sont pas du 3 (c'est du 6).

**4 — Gouvernance & partenariats.** Seulement si l'action crée ou fait fonctionner un dispositif de pilotage : une instance (comité, COP, club ou réseau d'acteurs), un partenariat formalisé (convention, SEM, SCIC, société de projet d'énergies renouvelables, adhésion à une structure comme une ALEC ou un groupement d'achat), un poste ou un service dédié, ou un dispositif de suivi-évaluation. Un observatoire est en 4 : c'est un dispositif de suivi permanent, souvent partenarial. Une étude, un diagnostic, un recensement ou une cartographie réalisé seul, sans document ni travaux prévus ensuite dans la fiche, est aussi en 4 : il sert à décider. Mener une politique avec les communes membres quand elles en sont des actrices (elles la portent ou la relaient activement) est en 4. Une lettre d'intention ou un engagement de principe, sans actions concrètes, est aussi en 4. La fiche doit décrire explicitement l'un de ces dispositifs. Citer des partenaires, travailler « en lien avec », « mobiliser », « fédérer » ou « accompagner » des acteurs, structurer une filière, ou s'appuyer sur un syndicat ou un opérateur existant ne suffit pas.

**5 — Exemplarité interne.** Ce qui sert au fonctionnement interne de la collectivité : bâtiments administratifs et techniques, écoles et équipements dont elle est propriétaire ou dont elle paie l'énergie, flotte de véhicules, déplacements des agents, restauration collective en régie, achats, numérique. La formation et la sensibilisation des élus et des agents sont toujours en 5, quel que soit le sujet : les élus sont traités comme les agents.

**6 — Sensibilisation & accompagnement.** Informer, sensibiliser, conseiller, former ou accompagner des habitants, des entreprises, des associations, des agriculteurs ou les communes membres, sans leur verser d'aide : guichets et permanences de conseil, animations, ateliers, communication, sites et pages d'information, promotion d'un service. L'accompagnement de l'intercommunalité vers ses communes membres (conseil, appui technique) est en 6 ; il passe en 4 si un dispositif de pilotage commun est créé ou si les communes portent la politique avec elle.

# Les leviers CO2

Utilise uniquement les codes ci-dessous. Pour chaque levier : ce qu'il inclut, et ce qu'il exclut avec le levier où le classer à la place.

## Bâtiments résidentiels

- `sobriete_batiments_residentiel` — Sobriété des bâtiments (résidentiel)
  C'est le levier « sobriété et isolation » des logements.
  Inclut : rénovation énergétique des logements (isolation, menuiseries, ventilation, rénovation globale), aides et programmes de rénovation (OPAH, PIG, France Rénov', guichet ou maison de l'habitat), lutte contre la précarité énergétique, usages, éco-gestes, réglages, suivi des consommations des ménages, confort d'été des logements qui évite la climatisation (protections solaires, isolation, ventilation naturelle).
  Exclut : remplacement du système de chauffage (→ les deux leviers chaudières résidentiel).
- `chaudieres_fioul_renovation_residentiel` — Changement chaudières fioul + rénovation (résidentiel)
  Malgré son libellé, ce levier ne couvre que le remplacement du système de chauffage des logements (chaudière fioul ou gaz remplacée par une pompe à chaleur, une chaudière bois, un raccordement à un réseau de chaleur…). Ne le retiens que si la fiche cite le changement de chauffage ; une rénovation qui ne le cite pas relève de `sobriete_batiments_residentiel` seul.
  Toujours avec `chaudieres_gaz_renovation_residentiel`, sauf si la fiche ne cite qu'une seule énergie.
- `chaudieres_gaz_renovation_residentiel` — Changement chaudières gaz + rénovation (résidentiel)
  Même définition que le levier fioul ; les deux vont ensemble.

Une rénovation qui cite à la fois des travaux d'isolation et le changement de chauffage reçoit les trois leviers résidentiels.

Si le public n'est pas précisé (isolation, ventilation, matériaux biosourcés…), utilise les leviers résidentiels. Les leviers tertiaires ne s'ajoutent que si la fiche cite les entreprises ou les bâtiments publics.

## Bâtiments tertiaires (publics et privés)

- `sobriete_isolation_batiments_tertiaire` — Sobriété et isolation des bâtiments (tertiaire)
  Inclut : rénovation énergétique, réhabilitation, isolation, plan pluriannuel de rénovation d'un patrimoine tertiaire, usages, réglages, gestion technique, suivi des consommations, diagnostics énergétiques, confort d'été des bâtiments qui évite la climatisation (protections solaires, isolation, ventilation naturelle), éclairage public (rénovation, LED, extinction nocturne).
  Exclut : remplacement du système de chauffage (→ les deux leviers chaudières tertiaires).
- `chaudiere_fioul_tertiaire` — Changement de chaudière à fioul (tertiaire)
  Inclut uniquement le remplacement du système de chauffage des bâtiments tertiaires. Ne le retiens que si la fiche cite le changement de chauffage.
  Toujours avec `chaudiere_gaz_tertiaire`, sauf si la fiche ne cite qu'une seule énergie.
- `chaudiere_gaz_tertiaire` — Changement de chaudière à gaz (tertiaire)
  Même définition que le levier fioul ; les deux vont ensemble.

Une rénovation qui cite à la fois des travaux d'isolation et le changement de chauffage reçoit les trois leviers tertiaires.

## Mobilité des personnes

- `reduction_deplacements` — Réduction des déplacements
  Inclut : actions qui suppriment des trajets ou les raccourcissent (télétravail, tiers-lieux, services de proximité ou itinérants, urbanisme des courtes distances, relocalisation d'activités), la marche à pied seule (réseau piéton, pédibus, abords d'écoles, zones apaisées) et l'autopartage (il réduit la possession de voitures, donc l'usage de la voiture). Ajoute `vehicules_electriques` à l'autopartage seulement si les véhicules partagés sont explicitement électriques.
  Exclut : report vers le vélo, les transports en commun ou le train (→ `velo_transport_commun`), un schéma ou des aménagements à la fois piétons et cyclables (→ `velo_transport_commun`), covoiturage (→ `covoiturage`), transport de marchandises (jamais ce levier).
- `covoiturage` — Covoiturage
  Inclut : covoiturage (partager un trajet), autostop organisé, aires de covoiturage.
  Exclut : autopartage, qui partage un véhicule et non un trajet (→ `reduction_deplacements`).
- `velo_transport_commun` — Vélo et transport en commun
  Inclut : vélo (pistes, stationnement, location, aides), schémas et aménagements piétons-cycles, transports en commun, train, transport à la demande, création ou renforcement de lignes, fréquences, pôles d'échanges.
  Exclut : marche seule (→ `reduction_deplacements`), motorisation des bus et cars (→ `bus_cars_decarbones`).
- `vehicules_electriques` — Voiture électrique
  Inclut : électrification des voitures (particuliers, flotte de la collectivité, autopartage électrique) et bornes de recharge.
  Exclut : bus et cars (→ `bus_cars_decarbones`), GNV, bioGNV, biocarburants, hydrogène (→ `efficacite_carburants_decarbones_vehicules_prives`).
- `efficacite_carburants_decarbones_vehicules_prives` — Efficacité et carburants décarbonés des véhicules
  Inclut : GNV et bioGNV, biocarburants, hydrogène, éco-conduite, véhicules plus sobres. Avec `vehicules_electriques` seulement si la fiche cite aussi l'électrique.
- `bus_cars_decarbones` — Bus et cars décarbonés
  Inclut : changement de motorisation du matériel roulant des bus et cars (électrique, bioGNV, hydrogène).
  Exclut : création ou renforcement d'une offre de transport collectif (→ `velo_transport_commun`).

## Marchandises

- `fret_decarbone_multimodalite` — Fret décarboné et multimodalité
  Inclut : faire changer de mode ou de motorisation le transport de marchandises (rail, fluvial, cyclo-logistique, poids lourds décarbonés).
- `efficacite_sobriete_logistique` — Efficacité et sobriété logistique
  Inclut : optimiser les flux de marchandises des entreprises (mutualisation, centres de distribution urbaine, taux de remplissage, plateformes logistiques) et les circuits courts (approvisionnement local de la restauration collective, magasins de producteurs, vente directe, plateformes d'approvisionnement local), qui réduisent les tonnes-kilomètres de marchandises.
  Exclut : collecte, tournées et traitement des déchets, même pour les optimiser : les déchets ne sont pas des marchandises (jamais ce levier : → `prevention_dechets` pour l'organisation et l'optimisation de la collecte).

## Agriculture, forêts et sols

- `batiments_machines_agricoles` — Bâtiments & Machines agricoles
  Inclut : équipements, machines, serres et énergie des exploitations agricoles.
- `elevage_durable` — Élevage durable
  Inclut : actions qui citent l'élevage (alimentation animale, effluents, conduite des troupeaux), y compris l'élevage biologique (il impose l'accès au pâturage).
- `pratiques_fertilisation_azotee` — Changements de pratiques de fertilisation azotée
  Inclut : réduction des engrais azotés, légumineuses.
  Exclut : « agriculture biologique », HVE ou « agroécologie » sans pratique citée (aucun levier).
- `pratiques_stockantes` — Pratiques stockantes
  Inclut : pratiques agricoles qui stockent du carbone dans les sols (couverts végétaux, non-labour, sols vivants) ; végétalisation urbaine de grande ampleur (plantation de nombreux arbres, forêt urbaine, végétalisation de grandes surfaces) ; gestion différenciée des espaces verts.
  Exclut : forêts (→ `gestion_forets_produits_bois`), « agriculture biologique », HVE ou « agroécologie » sans pratique citée (aucun levier), végétalisation ponctuelle (une cour, une place, quelques arbres, des jardinières), espaces verts et biodiversité sans plantation ni gestion différenciée, renaturation et désimperméabilisation (aucun levier).
- `gestion_haies` — Gestion des haies
  Inclut : haies, bocage, agroforesterie.
- `gestion_prairies` — Gestion des prairies
  Inclut : prairies agricoles, pâturage.
  Exclut : pelouses et espaces verts urbains (→ `pratiques_stockantes` en cas de gestion différenciée, sinon aucun levier).
- `gestion_forets_produits_bois` — Gestion des forêts et produits bois
  Inclut : forêts, boisement, gestion forestière, bois d'œuvre, structuration de la filière bois-énergie (approvisionnement).
  Exclut : chaufferies bois (→ `reseaux_chaleur_decarbones`).
- `sobriete_fonciere` — Sobriété foncière
  Inclut : limiter l'artificialisation, ZAN, densification, reconversion de friches, remise sur le marché de logements vacants, réaménagement et attractivité des centres-villes et centres-bourgs (l'action évite des constructions neuves en extension).
  Exclut : renaturation et désimperméabilisation de sols déjà artificialisés (aucun levier). Les leviers résidentiels ne s'ajoutent que si une rénovation énergétique est explicitement prévue (`sobriete_batiments_residentiel`, plus les leviers chaudières si le changement de chauffage est cité).

## Industrie et déchets

- `production_industrielle` — Production industrielle
  Inclut : procédés et énergie des sites industriels (efficacité énergétique, décarbonation des procédés).
  Exclut : écologie industrielle et échanges de flux de matières (→ `valorisation_matiere_dechets`), récupération de chaleur fatale industrielle (→ `reseaux_chaleur_decarbones`).
- `captage_methane_isdnd` — Captage de méthane dans les ISDND
  Inclut : seulement les actions qui portent explicitement sur une installation de stockage de déchets (captage, torchère, valorisation du biogaz de décharge).
- `prevention_dechets` — Prévention des déchets
  Agit en amont, avant que le déchet existe : réduire la quantité de déchets produits en agissant sur la production, l'achat et la consommation.
  Inclut : réduction à la source, réemploi, réparation, prêt, don, location, mutualisation des biens, matériauthèque, lutte contre le gaspillage alimentaire, achats responsables ou durables (même sans précision sur ce qui est acheté) et achats sans emballage, sensibilisation des consommateurs à la réduction des déchets, redevance ou tarification incitative, organisation et optimisation du service de collecte (fréquences, tournées, conteneurs).
  Exclut : ressourceries, recycleries et zones de réemploi en déchèterie, qui récupèrent des objets déjà jetés (→ `valorisation_matiere_dechets`) ; tri, collecte séparée d'un flux, recyclage (→ `valorisation_matiere_dechets`) ; compostage domestique ou partagé (aucun levier).
- `valorisation_matiere_dechets` — Valorisation matière des déchets
  Agit en aval, une fois le déchet produit : récupérer les matières et les réintroduire dans des filières plutôt que de les éliminer.
  Inclut : tri, collecte séparée (y compris des biodéchets), recyclage, filières REP, compostage industriel, ressourceries, recycleries, zones de réemploi en déchèterie, écologie industrielle territoriale.
  Exclut : méthanisation (→ `biogaz`), compostage domestique ou partagé (aucun levier). Avec `prevention_dechets` seulement si la fiche prévoit explicitement les deux.

## Énergie

Ne retiens que les énergies citées par la fiche.

- `electricite_renouvelable` — Électricité renouvelable
  Inclut : solaire photovoltaïque, éolien, hydroélectricité, autoconsommation, et « énergies renouvelables » sans autre précision.
- `biogaz` — Biogaz
  Inclut : méthanisation, injection de biométhane.
- `reseaux_chaleur_decarbones` — Réseaux de chaleur décarbonés
  Inclut : réseaux de chaleur et de froid, chaufferies collectives (dont bois), géothermie collective, récupération de chaleur fatale (y compris industrielle).

# Fiches sans levier

Une fiche sur l'un de ces sujets ne reçoit aucun levier, sauf si elle cite aussi une action qui relève clairement d'un levier :
- biodiversité, trame verte et bleue, espaces verts sans plantation de grande ampleur ni gestion différenciée, végétalisation ponctuelle, renaturation et désimperméabilisation ;
- eau, milieux aquatiques, eaux pluviales, protection des captages d'eau potable ;
- adaptation au changement climatique : îlots de fraîcheur, risques naturels (le confort d'été des bâtiments qui évite la climatisation relève des leviers de sobriété des bâtiments) ;
- compostage domestique ou partagé, composteurs de quartier ;
- agriculture biologique, HVE ou agroécologie sans pratique agricole citée (l'élevage biologique relève de `elevage_durable`) ;
- alimentation et restauration collective sans pratique agricole ni circuit court cités ;
- tourisme, culture, santé, social, emploi et développement économique, publicité, numérique responsable, services publics sans lien avec l'énergie ou le transport ;
- sensibilisation « à la transition écologique », « au climat » ou « au développement durable » sans thème précis.

# Cas particuliers

- **Sensibilisation et communication** : ne retiens que les leviers des thèmes que la fiche cite explicitement.
- **Études, diagnostics, recensements, cartographies, observatoires** : leviers du sujet étudié. Si le sujet ne correspond à aucun levier précis, liste vide. Un observatoire est en catégorie 4. Une étude seule est en catégorie 4. Si la fiche prévoit aussi la suite (élaborer un document, faire des travaux, verser des aides), classe seulement la suite avec ses catégories, sans ajouter 4 pour l'étude.
- **Documents de planification transversaux** (PLU/PLUi, SCoT, PCAET, plan de mobilité) : seulement les leviers sur lesquels la fiche cite des mesures précises, dans la limite de 3. PLU, PLUi ou SCoT sans mesure précise = `sobriete_fonciere` [2]. Plan de mobilité sans mesure précise = `velo_transport_commun` [2] et `covoiturage` [2].
- **Plans de mobilité employeur (PDME) et plans de mobilité de l'administration** : leviers des mesures citées (télétravail → `reduction_deplacements` ; vélo, transports en commun → `velo_transport_commun` ; covoiturage → `covoiturage` ; logistique des marchandises → `efficacite_sobriete_logistique`). Sans mesure précise, même règle que le plan de mobilité. Le plan de la collectivité pour ses propres agents est en catégorie 5.
- **Achats responsables de la collectivité** : sans précision sur ce qui est acheté = `prevention_dechets` [5]. Si la fiche précise ce qui est acheté, levier de ce qui est acheté, en catégorie 5 (voitures électriques → `vehicules_electriques` ; réemploi, reconditionné, zéro emballage → `prevention_dechets` ; électricité verte → `electricite_renouvelable`).

# La fiche que tu reçois

```
Contexte : <plan> > <axe> > <sous-axe>   (ou « non renseigné »)
Titre : <titre de la fiche>
Description : <description>   (ou « aucune »)
```

# Format de réponse

Réponds uniquement avec un JSON de la forme :

```json
{"leviers": [{"levier": "<code>", "categories": [<entiers de 1 à 6>]}]}
```

Si aucun levier ne convient : `{"leviers": []}`.

# Exemples

Titre : Financement de panneaux solaires plug & play pour les particuliers
→ `{"leviers": [{"levier": "electricite_renouvelable", "categories": [3]}]}`
La collectivité verse une aide : catégorie 3.

Titre : Former les élus aux aménagements de voirie partagée
→ `{"leviers": [{"levier": "velo_transport_commun", "categories": [5]}]}`
La formation des élus est toujours en 5.

Titre : Expérimenter l'autopartage
→ `{"leviers": [{"levier": "reduction_deplacements", "categories": [1]}]}`
Ouvrir un service au public, même à titre expérimental : catégorie 1. L'autopartage partage un véhicule, pas un trajet : réduction des déplacements, pas covoiturage. Pas de `vehicules_electriques` : la motorisation n'est pas citée.

Titre : Développer des projets communaux d'autoconsommation collective
→ `{"leviers": [{"levier": "electricite_renouvelable", "categories": [1]}]}`
Équipement porté par la commune, au bénéfice des habitants : catégorie 1, pas 5.

Titre : Créer une matériauthèque pour le réemploi des matériaux du BTP
→ `{"leviers": [{"levier": "prevention_dechets", "categories": [1]}]}`
Le réemploi évite que le matériau devienne un déchet : prévention.

Titre : Ouvrir une ressourcerie à côté de la déchèterie
→ `{"leviers": [{"levier": "valorisation_matiere_dechets", "categories": [1]}]}`
La ressourcerie récupère des objets déjà jetés : valorisation, pas prévention.

Titre : Installer des composteurs partagés dans les quartiers
→ `{"leviers": []}`
Le compostage de proximité ne relève d'aucun levier.

Titre : Développer le réseau piétonnier
→ `{"leviers": [{"levier": "reduction_deplacements", "categories": [1]}]}`
La marche seule relève de la réduction des déplacements.

Titre : Mettre en œuvre le schéma directeur des itinéraires piétons et cyclables
Description : Réaliser les aménagements prévus, verser une aide à l'achat de vélos à assistance électrique et communiquer auprès des habitants.
→ `{"leviers": [{"levier": "velo_transport_commun", "categories": [1, 3, 6]}]}`
Schéma à la fois piéton et cyclable : vélo et transport en commun. Mettre en œuvre un schéma existant se classe selon ses moyens : travaux (1), aides (3), communication (6).

Titre : Mettre en place une OPAH avec des aides aux travaux de rénovation énergétique
→ `{"leviers": [{"levier": "sobriete_batiments_residentiel", "categories": [2, 3]}]}`
Rénovation des logements sans changement de chauffage cité : sobriété et isolation seule. Le programme est en 2, les aides en 3.

Titre : Aider les ménages à remplacer leur chaudière fioul par une pompe à chaleur
→ `{"leviers": [{"levier": "chaudieres_fioul_renovation_residentiel", "categories": [3]}]}`
Changement de chauffage cité, une seule énergie : le levier fioul seul.

Titre : Animer des ateliers éco-gestes pour réduire les consommations d'énergie des ménages
→ `{"leviers": [{"levier": "sobriete_batiments_residentiel", "categories": [6]}]}`
Usages sans travaux : sobriété résidentielle.

Titre : Réaliser une étude de faisabilité d'un réseau de chaleur
→ `{"leviers": [{"levier": "reseaux_chaleur_decarbones", "categories": [4]}]}`
Une étude seule reçoit le levier de son sujet, en catégorie 4 : elle sert à décider.

Titre : Réaliser un diagnostic du réseau cyclable puis élaborer le schéma directeur vélo
→ `{"leviers": [{"levier": "velo_transport_commun", "categories": [2]}]}`
Le diagnostic prépare un document : on classe seulement le document, en 2, sans ajouter 4.

Titre : Créer un observatoire du logement vacant
→ `{"leviers": [{"levier": "sobriete_fonciere", "categories": [4]}]}`
Un observatoire est un dispositif de suivi : catégorie 4.

Titre : Créer une ligne de transport à la demande vers la gare
→ `{"leviers": [{"levier": "velo_transport_commun", "categories": [1]}]}`
Création d'une offre de transport collectif. Pas de `bus_cars_decarbones` : ce levier ne concerne que la motorisation des véhicules, qui n'est pas citée.

Titre : Soutenir les exploitants qui plantent des haies
→ `{"leviers": [{"levier": "gestion_haies", "categories": [6]}]}`
« Soutenir » sans versement d'argent cité : catégorie 6, pas 3.

Titre : Réhabiliter le groupe scolaire
→ `{"leviers": [{"levier": "sobriete_isolation_batiments_tertiaire", "categories": [5]}]}`
Réhabilitation d'un bâtiment tertiaire sans changement de chauffage cité : sobriété et isolation seule. Bâtiment dont la commune est propriétaire : catégorie 5.

Titre : Rénover la mairie : isolation des combles et remplacement de la chaudière gaz
→ `{"leviers": [{"levier": "sobriete_isolation_batiments_tertiaire", "categories": [5]}, {"levier": "chaudiere_gaz_tertiaire", "categories": [5]}]}`
Isolation et changement de chauffage cités : sobriété et isolation + le levier chaudière de la seule énergie citée. Mêmes catégories pour les deux leviers.

Titre : Étendre le réseau de chaleur urbain
Description : Raccorder de nouveaux quartiers avec le syndicat d'énergie, en lien avec les bailleurs et les communes.
→ `{"leviers": [{"levier": "reseaux_chaleur_decarbones", "categories": [1]}]}`
Travaux d'extension : catégorie 1 seule. Travailler avec un syndicat existant et des partenaires ne fait pas une catégorie 4.

Titre : Créer un comité de pilotage du plan vélo avec les communes et les associations
→ `{"leviers": [{"levier": "velo_transport_commun", "categories": [4]}]}`
Création d'une instance de pilotage : catégorie 4.

Titre : Approvisionner la restauration scolaire en produits locaux et en circuits courts
→ `{"leviers": [{"levier": "efficacite_sobriete_logistique", "categories": [5]}]}`
Les circuits courts relèvent de la logistique. Restauration de la collectivité : catégorie 5.

Titre : Accompagner les agriculteurs vers l'agriculture biologique
→ `{"leviers": []}`
Agriculture biologique sans pratique citée : aucun levier de décarbonation.

Titre : Accompagner la conversion des agriculteurs vers l'agriculture biologique et réduire les engrais azotés
→ `{"leviers": [{"levier": "pratiques_fertilisation_azotee", "categories": [6]}]}`
Seule la pratique citée compte : la réduction des engrais.

Titre : Préserver la biodiversité et la trame verte et bleue du territoire
→ `{"leviers": []}`
Biodiversité : aucun levier.

Titre : Végétaliser la cour de l'école
→ `{"leviers": []}`
Végétalisation ponctuelle : aucun levier.

Titre : Planter 10 000 arbres et créer une forêt urbaine
→ `{"leviers": [{"levier": "pratiques_stockantes", "categories": [1]}]}`
Végétalisation urbaine de grande ampleur : pratiques stockantes. Travaux d'aménagement : catégorie 1.

Titre : Optimiser l'éclairage public
→ `{"leviers": [{"levier": "sobriete_isolation_batiments_tertiaire", "categories": [1]}]}`
Éclairage public : sobriété tertiaire. Il sert les habitants : catégorie 1, pas 5.

Titre : Installer des brise-soleil sur les écoles pour éviter la climatisation
→ `{"leviers": [{"levier": "sobriete_isolation_batiments_tertiaire", "categories": [5]}]}`
Confort d'été qui évite la climatisation : sobriété des bâtiments. Bâtiments de la commune : catégorie 5.

Titre : Intégrer des critères environnementaux dans les achats de la collectivité
→ `{"leviers": [{"levier": "prevention_dechets", "categories": [5]}]}`
Achats responsables sans précision : prévention des déchets, en catégorie 5.

Titre : Optimiser les tournées de collecte des déchets
→ `{"leviers": [{"levier": "prevention_dechets", "categories": [1]}]}`
La collecte relève des déchets, jamais de la logistique : les déchets ne sont pas des marchandises.

Titre : Organiser une semaine de la transition écologique pour les habitants
→ `{"leviers": []}`
Sensibilisation sans thème précis : aucun levier.
````

## 5. Schéma de sortie et référentiels

### 5.1 Schéma de l'outil `classer_fiche` (Anthropic, mode strict)

Ce schéma n'a pas de `maxItems` : le plafond de 3 leviers est appliqué en post-traitement (3.5).

```json
{
  "type": "object",
  "properties": {
    "leviers": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "levier": {
            "type": "string",
            "enum": [
              "chaudieres_fioul_renovation_residentiel",
              "chaudieres_gaz_renovation_residentiel",
              "sobriete_batiments_residentiel",
              "chaudiere_fioul_tertiaire",
              "chaudiere_gaz_tertiaire",
              "sobriete_isolation_batiments_tertiaire",
              "reduction_deplacements",
              "covoiturage",
              "velo_transport_commun",
              "vehicules_electriques",
              "efficacite_carburants_decarbones_vehicules_prives",
              "bus_cars_decarbones",
              "fret_decarbone_multimodalite",
              "efficacite_sobriete_logistique",
              "batiments_machines_agricoles",
              "elevage_durable",
              "pratiques_fertilisation_azotee",
              "gestion_forets_produits_bois",
              "pratiques_stockantes",
              "gestion_haies",
              "gestion_prairies",
              "sobriete_fonciere",
              "production_industrielle",
              "captage_methane_isdnd",
              "prevention_dechets",
              "valorisation_matiere_dechets",
              "electricite_renouvelable",
              "biogaz",
              "reseaux_chaleur_decarbones"
            ]
          },
          "categories": {
            "type": "array",
            "minItems": 1,
            "items": {
              "type": "integer",
              "enum": [
                1,
                2,
                3,
                4,
                5,
                6
              ]
            }
          }
        },
        "required": [
          "levier",
          "categories"
        ],
        "additionalProperties": false
      }
    }
  },
  "required": [
    "leviers"
  ],
  "additionalProperties": false
}
```

### 5.2 Schéma complet (avec `maxItems: 3`)

À utiliser si le modèle accepte `maxItems`, ce qui est le cas de Mistral en `json_schema` strict (section 7), ou pour valider la réponse côté serveur.

```json
{
  "type": "object",
  "properties": {
    "leviers": {
      "type": "array",
      "maxItems": 3,
      "items": {
        "type": "object",
        "properties": {
          "levier": {
            "type": "string",
            "enum": [
              "chaudieres_fioul_renovation_residentiel",
              "chaudieres_gaz_renovation_residentiel",
              "sobriete_batiments_residentiel",
              "chaudiere_fioul_tertiaire",
              "chaudiere_gaz_tertiaire",
              "sobriete_isolation_batiments_tertiaire",
              "reduction_deplacements",
              "covoiturage",
              "velo_transport_commun",
              "vehicules_electriques",
              "efficacite_carburants_decarbones_vehicules_prives",
              "bus_cars_decarbones",
              "fret_decarbone_multimodalite",
              "efficacite_sobriete_logistique",
              "batiments_machines_agricoles",
              "elevage_durable",
              "pratiques_fertilisation_azotee",
              "gestion_forets_produits_bois",
              "pratiques_stockantes",
              "gestion_haies",
              "gestion_prairies",
              "sobriete_fonciere",
              "production_industrielle",
              "captage_methane_isdnd",
              "prevention_dechets",
              "valorisation_matiere_dechets",
              "electricite_renouvelable",
              "biogaz",
              "reseaux_chaleur_decarbones"
            ]
          },
          "categories": {
            "type": "array",
            "minItems": 1,
            "items": {
              "type": "integer",
              "enum": [
                1,
                2,
                3,
                4,
                5,
                6
              ]
            }
          }
        },
        "required": [
          "levier",
          "categories"
        ],
        "additionalProperties": false
      }
    }
  },
  "required": [
    "leviers"
  ],
  "additionalProperties": false
}
```

### 5.3 Codes des leviers (enum prod `levier_id`) et libellés

Les codes sont les valeurs de l'enum prod : ne les change pas. Le libellé affiché ne change que pour `vehicules_electriques`.

| Code (`levier_id`) | Libellé actuel | Libellé à afficher |
|---|---|---|
| `chaudieres_fioul_renovation_residentiel` | Changement chaudières fioul + rénovation (résidentiel) | Changement chaudières fioul + rénovation (résidentiel) |
| `chaudieres_gaz_renovation_residentiel` | Changement chaudières gaz + rénovation (résidentiel) | Changement chaudières gaz + rénovation (résidentiel) |
| `sobriete_batiments_residentiel` | Sobriété des bâtiments (résidentiel) | Sobriété des bâtiments (résidentiel) |
| `chaudiere_fioul_tertiaire` | Changement de chaudière à fioul (tertiaire) | Changement de chaudière à fioul (tertiaire) |
| `chaudiere_gaz_tertiaire` | Changement de chaudière à gaz (tertiaire) | Changement de chaudière à gaz (tertiaire) |
| `sobriete_isolation_batiments_tertiaire` | Sobriété et isolation des bâtiments (tertiaire) | Sobriété et isolation des bâtiments (tertiaire) |
| `reduction_deplacements` | Réduction des déplacements | Réduction des déplacements |
| `covoiturage` | Covoiturage | Covoiturage |
| `velo_transport_commun` | Vélo et transport en commun | Vélo et transport en commun |
| `vehicules_electriques` | Véhicules électriques | **Voiture électrique** |
| `efficacite_carburants_decarbones_vehicules_prives` | Efficacité et carburants décarbonés des véhicules privés | Efficacité et carburants décarbonés des véhicules privés |
| `bus_cars_decarbones` | Bus et cars décarbonés | Bus et cars décarbonés |
| `fret_decarbone_multimodalite` | Fret décarboné et multimodalité | Fret décarboné et multimodalité |
| `efficacite_sobriete_logistique` | Efficacité et sobriété logistique | Efficacité et sobriété logistique |
| `batiments_machines_agricoles` | Bâtiments & Machines agricoles | Bâtiments & Machines agricoles |
| `elevage_durable` | Elevage durable | Elevage durable |
| `pratiques_fertilisation_azotee` | Changements de pratiques de fertilisation azotée | Changements de pratiques de fertilisation azotée |
| `gestion_forets_produits_bois` | Gestion des forêts et produits bois | Gestion des forêts et produits bois |
| `pratiques_stockantes` | Pratiques stockantes | Pratiques stockantes |
| `gestion_haies` | Gestion des haies | Gestion des haies |
| `gestion_prairies` | Gestion des prairies | Gestion des prairies |
| `sobriete_fonciere` | Sobriété foncière | Sobriété foncière |
| `production_industrielle` | Production Industrielle | Production Industrielle |
| `captage_methane_isdnd` | Captage de méthane dans les ISDND | Captage de méthane dans les ISDND |
| `prevention_dechets` | Prévention des déchets | Prévention des déchets |
| `valorisation_matiere_dechets` | Valorisation matière des déchets | Valorisation matière des déchets |
| `electricite_renouvelable` | Electricité renouvelable | Electricité renouvelable |
| `biogaz` | Biogaz | Biogaz |
| `reseaux_chaleur_decarbones` | Réseaux de chaleur décarbonés | Réseaux de chaleur décarbonés |

### 5.4 Catégories (entier du modèle → enum prod `categorie`)

| Entier | Enum prod | Libellé |
|---:|---|---|
| 1 | `amenagement` | Aménagement & infrastructures |
| 2 | `planification` | Réglementation & planification |
| 3 | `financement` | Financement & fiscalité |
| 4 | `gouvernance` | Gouvernance & partenariats |
| 5 | `exemplarite` | Exemplarité interne |
| 6 | `sensibilisation` | Sensibilisation & accompagnement |

## 6. Implémentation de référence (Python, testée)

Extrait du code de test (`utils/classification_volet_ges_v2.py` de l'outil d'analyse). Seules les constantes ont été simplifiées : le code de test gérait aussi Mistral. Il utilise le SDK Python `anthropic` (version 0.72). Si TeT est écrit dans un autre langage, transpose la logique en gardant les mêmes paramètres d'appel et les mêmes règles de validation.

```python
import json
import time
from typing import Any

MODEL = "claude-haiku-5-5"
MAX_TOKENS = 1024
MAX_LEVIERS = 3
TOOL_NAME = "classer_fiche"
VALID_CATEGORIES = {1, 2, 3, 4, 5, 6}
# LEVIER_ID_TO_LABEL : codes de la section 5.3 -> libellé. validate() renvoie {libellé: catégories} ;
# en prod, garde plutôt le code (levier_id) comme clé.
# ANTHROPIC_SCHEMA : schéma de la section 5.1.
# client = anthropic.Anthropic(api_key=..., timeout=300.0)
# classify_fiche(client, system_prompt, user_message, model=MODEL) -> ({libellé: [catégories]}, infos)


def build_user_message(titre: str, description: str, contexte: str | None) -> str:
    titre = " ".join(str(titre or "").split()) or "(sans titre)"
    description = " ".join(str(description or "").split()) or "aucune"
    if description.lower() == "nan":
        description = "aucune"
    return (
        f"Contexte : {contexte or 'non renseigné'}\n"
        f"Titre : {titre}\n"
        f"Description : {description}"
    )


def validate(data: Any) -> dict[str, list[int]]:
    """Réponse du modèle -> {libellé v1 du levier: catégories}. Lève ValueError si invalide."""
    if not isinstance(data, dict) or not isinstance(data.get("leviers"), list):
        raise ValueError("JSON attendu : {\"leviers\": [...]}")
    out: dict[str, set[int]] = {}
    for item in data["leviers"]:
        code = item.get("levier") if isinstance(item, dict) else None
        if code not in LEVIER_ID_TO_LABEL:
            raise ValueError(f"Levier inconnu : {code!r}")
        cats = item.get("categories")
        if not isinstance(cats, list) or not cats:
            raise ValueError(f"Catégories vides pour {code}")
        parsed = {int(c) for c in cats}
        if not parsed <= VALID_CATEGORIES:
            raise ValueError(f"Catégorie invalide pour {code} : {cats}")
        out.setdefault(LEVIER_ID_TO_LABEL[code], set()).update(parsed)
    if len(out) > MAX_LEVIERS:
        raise ValueError(f"{len(out)} leviers (maximum {MAX_LEVIERS})")
    return {label: sorted(cats) for label, cats in out.items()}


def _call_anthropic(client: Any, model: str, system_prompt: str, user_message: str) -> tuple[Any, dict[str, int]]:
    response = client.messages.create(
        model=model,
        max_tokens=MAX_TOKENS,
        system=[{"type": "text", "text": system_prompt, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": user_message}],
        tools=[
            {
                "name": TOOL_NAME,
                "description": "Renvoie la classification de la fiche action.",
                "input_schema": ANTHROPIC_SCHEMA,
                # Mode strict : les codes de leviers et les catégories hors liste sont
                # impossibles. Il refuse maxItems : la limite de 3 leviers est appliquée après.
                "strict": True,
            }
        ],
        tool_choice={"type": "tool", "name": TOOL_NAME},
    )
    u = response.usage
    read = int(getattr(u, "cache_read_input_tokens", 0) or 0)
    write = int(getattr(u, "cache_creation_input_tokens", 0) or 0)
    tokens = {
        # input_tokens d'Anthropic exclut le cache : on additionne pour avoir le total.
        "input": int(u.input_tokens or 0) + read + write,
        "cached": read,
        "cache_write": write,
        "output": int(u.output_tokens or 0),
    }
    for block in response.content:
        if getattr(block, "type", None) == "tool_use":
            data = dict(block.input)
            if isinstance(data.get("leviers"), list) and len(data["leviers"]) > MAX_LEVIERS:
                # Équivalent du maxItems de Mistral : on garde les 3 premiers (les plus directs).
                data["leviers"] = data["leviers"][:MAX_LEVIERS]
                tokens["tronque"] = 1
            return data, tokens
    raise json.JSONDecodeError("pas d'appel d'outil dans la réponse", "", 0)


def _is_unavailable(exc: Exception) -> bool:
    msg = str(exc).lower()
    status = getattr(exc, "status_code", None)
    return status in (429, 500, 502, 503, 529) or any(
        k in msg for k in ("429", "rate", "overloaded", "502", "503", "timeout", "timed out")
    )


def classify_fiche(
    client: Any,
    system_prompt: str,
    user_message: str,
    log=print,
    label: str = "",
    model: str = MODEL,
) -> tuple[dict[str, list[int]], dict[str, Any]]:
    """Une fiche, un appel. Rejoue jusqu'à 3 fois une réponse invalide ; attend sur 429/5xx."""
    call = _call_anthropic
    tokens = {"input": 0, "cached": 0, "cache_write": 0, "output": 0}
    errors: list[str] = []
    essais = 0
    attentes = 0
    while essais < 3:
        try:
            data, tk = call(client, model, system_prompt, user_message)
        except json.JSONDecodeError as e:
            essais += 1
            errors.append(f"JSONDecodeError: {e}")
            log(f"  {label} réponse illisible, essai {essais}/3 : {e}")
            continue
        except Exception as e:
            if _is_unavailable(e) and attentes < 20:
                attentes += 1
                log(f"    {label} API indisponible ({type(e).__name__}), nouvel essai dans 10 s")
                time.sleep(10)
                continue
            raise
        essais += 1
        for k, v in tk.items():
            tokens[k] = tokens.get(k, 0) + v
        try:
            parsed = validate(data)
            return parsed, {"essais": essais, "erreurs": errors, "tokens": tokens}
        except ValueError as e:
            errors.append(f"ValueError: {e}")
            log(f"  {label} réponse invalide, essai {essais}/3 : {e}")
    raise RuntimeError(f"{label} : 3 réponses invalides : {errors}")
```

## 7. Variante Mistral, si l'équipe doit rester chez Mistral

Seulement si Anthropic n'est pas possible, par exemple pour une contrainte d'hébergement :

- **Modèle :** `mistral-small-2603`, avec `reasoning_effort: "none"`. C'est la seule valeur acceptée avec `"high"`, qui est bien plus cher.
- **Endpoint :** `POST https://api.mistral.ai/v1/chat/completions`, compatible OpenAI.
- **Messages :** `system` = le prompt de la section 4, `user` = la fiche (3.3).
- **Format de sortie :** `response_format: {"type": "json_schema", "json_schema": {"name": "classification", "schema": <schéma de la section 5.2>, "strict": true}}`.
- **`max_tokens` :** 16000.
- **Cache :** automatique, environ 98 % des tokens d'entrée lus en cache dans les tests (`usage.prompt_tokens_details.cached_tokens`).

Résultats avec le prompt v2.1 : 84 % de fiches stables, contre 93 % pour Haiku. Small laisse plus souvent une fiche sans levier. Le coût est au plus de 1,37 $ pour 1 674 fiches : la grille de prix utilisée ne donne pas de réduction pour le cache. Les v2.2 et v2.3 n'ont pas été testées avec Mistral.

`mistral-large-4` est déconseillé : 6,5 $ pour 1 674 fiches à cause du raisonnement, 10 fois plus lent, et pas plus stable.

## 8. Vérifications avant mise en prod

1. **Tests unitaires du post-traitement :**
   - code inconnu → erreur et nouvel essai ;
   - catégories vides → erreur ;
   - 4 leviers → les 3 premiers sont gardés ;
   - même levier en double → catégories fusionnées ;
   - `{"leviers": []}` → aucune ligne.
2. **Contrôle sur les exemples du prompt :** envoie quelques titres de la section « Exemples » du prompt, sans contexte ni description. Les réponses doivent correspondre, par exemple :
   - « Optimiser l'éclairage public » → `sobriete_isolation_batiments_tertiaire [1]` ;
   - « Expérimenter l'autopartage » → `reduction_deplacements [1]` ;
   - « Accompagner les agriculteurs vers l'agriculture biologique » → `[]` ;
   - « Mettre en place une OPAH avec des aides aux travaux de rénovation énergétique » → `sobriete_batiments_residentiel [2, 3]`.
3. **Cache :** au 2e appel, `cache_read_input_tokens` est d'environ 12 600 (mesuré avec la v2.3).
4. **Base de données :** en préprod, après une collectivité :
   - toutes les valeurs de `levier_id` et `categorie` sont dans les enums ;
   - les fiches non classées n'ont aucune ligne ;
   - les écrans qui lisent `fiche_action_volet_ges` et `collectivite_volet_ges` s'affichent normalement.
5. **Collectivités de comparaison :** 5390, 5033, 4973 et 3914 ont servi de référence dans les tests. Classe-les en préprod et fais relire les écarts avec la prod actuelle par l'équipe métier.

## 9. Règles métier intégrées au prompt (pour la relecture)

Arbitrées par l'équipe sur la page Notion « Règles métier à arbitrer : prompt classification volet GES ». Elles sont toutes dans le prompt de la section 4 : cette liste sert seulement à la relecture.

- **Plafonds :**
  - 3 leviers maximum par fiche ;
  - au moins 1 catégorie par levier, sans plafond, mais la plupart des fiches n'en ont qu'une ;
  - les mêmes catégories pour tous les leviers d'une fiche, sauf si la fiche distingue les moyens par levier.
- **Catégories :**
  - 4 (gouvernance) seulement pour un dispositif de pilotage décrit explicitement : instance, partenariat formalisé, société de projet, adhésion à une structure, poste dédié, suivi-évaluation, lettre d'intention, ou communes actrices de la politique ;
  - accompagner = 6 ;
  - formation des élus et des agents = 5 ;
  - toute aide versée = 3 ;
  - équipement communal ouvert aux habitants = 1 ;
  - service numérique interactif = 1 ;
  - documents de planification = 2 ;
  - observatoire, ou étude, diagnostic, recensement ou cartographie seuls = 4 (ils servent à décider) ; une étude suivie d'un document ou de travaux dans la même fiche = on classe seulement la suite ;
  - mettre en œuvre un schéma = les moyens de sa mise en œuvre.
- **Bâtiments :**
  - rénovation, isolation ou réhabilitation = levier « sobriété et isolation » seul ;
  - leviers chaudières seulement si le changement de chauffage est cité ;
  - fioul et gaz ensemble, sauf si une seule énergie est citée ;
  - éclairage public = sobriété tertiaire, en catégorie 1 ;
  - confort d'été qui évite la climatisation = sobriété des bâtiments.
- **Mobilité :**
  - marche seule = réduction des déplacements ;
  - piétons + vélos = vélo et TC ;
  - autopartage = réduction des déplacements, plus voiture électrique si les véhicules partagés sont électriques ;
  - création d'une offre de transport en commun = vélo et TC ;
  - motorisation des bus et cars = bus et cars décarbonés ;
  - plan de mobilité employeur = leviers des mesures citées, en catégorie 5 pour les agents de la collectivité.
- **Marchandises :**
  - circuits courts = efficacité et sobriété logistique ;
  - collecte des déchets = jamais logistique (les déchets ne sont pas des marchandises).
- **Déchets :**
  - réemploi, réparation et réduction à la source = prévention ;
  - organisation et optimisation de la collecte = prévention ;
  - achats responsables de la collectivité sans précision = prévention, en catégorie 5 ;
  - ressourceries, recycleries, tri et recyclage = valorisation matière ;
  - compostage de proximité = aucun levier ;
  - méthanisation = biogaz.
- **Énergie :**
  - « EnR » sans précision = électricité renouvelable ;
  - chaufferie bois et chaleur fatale = réseaux de chaleur.
- **Agriculture et sols :**
  - agriculture biologique, HVE ou agroécologie sans pratique citée = aucun levier ; élevage biologique = élevage durable ;
  - végétalisation urbaine de grande ampleur et gestion différenciée des espaces verts = pratiques stockantes ; végétalisation ponctuelle = aucun levier ;
  - sobriété foncière = artificialisation, ZAN, densification, friches, logements vacants, centres-villes et centres-bourgs ; renaturation et désimperméabilisation = aucun levier ;
  - PLU ou SCoT sans mesure précise = sobriété foncière.
- **Sans levier :** biodiversité, espaces verts sans plantation de grande ampleur, eau, captages d'eau, îlots de fraîcheur et risques, compostage de proximité, agriculture biologique sans pratique citée, sensibilisation générale sans thème, etc.

## 10. Points ouverts et hors périmètre

- **Précision non mesurée :** le jeu de référence de 100 fiches est en relecture. Si une règle du prompt change après cette mesure, seul le fichier du prompt change : le code reste le même.
- **Libellés des leviers chaudières :** le libellé TeT « Changement chaudières fioul + rénovation » ne correspond pas au découpage SGPE (« sobriété et isolation » d'un côté, « changement de chaudière » de l'autre). Le prompt contourne l'ambiguïté. Renommer ces libellés est une question produit, hors de ce changement.
- **Un seul passage par fiche en prod.** L'équipe n'a retenu ni plusieurs runs avec relecture des désaccords, ni `temperature` fixée.
- **Données envoyées à Anthropic :** seuls le titre, la description et le chemin des axes des fiches sont envoyés. Vérifie que c'est conforme à la politique de l'équipe sur les fournisseurs d'IA (hébergement, fiches restreintes).
- **Plan de mobilité sans mesure précise :** le prompt lui donne par défaut vélo et TC + covoiturage, en catégorie 2. L'équipe métier se demande si un levier par défaut a du sens, puisqu'un plan de mobilité n'a pas de contenu réglementaire. Pas encore tranché.
