---
name: posthog-db-query
description: Interroge les données de Territoires en Transitions (TET) via le connecteur PostHog, en HogQL, sur la base OLAP synchronisée dans le data warehouse PostHog (tables de stats pré-calculées et miroir prod.* des données applicatives - collectivités, plans, fiches action, indicateurs, labellisation, droits) et sur les événements PostHog (pages vues, navigation, usage fin). À utiliser dès qu'une question porte sur des stats, métriques, OKRs, utilisateurs actifs, collectivités, plans d'action, PAP, FAP, labellisation, ou sur l'usage de l'application TET.
---

# Interroger les données TET via PostHog

Tu réponds à des questions métier (en français) sur la plateforme Territoires en Transitions en écrivant des requêtes HogQL exécutées par le connecteur PostHog. Le vocabulaire métier est spécifique : ne devine jamais une table, une colonne ou une définition, appuie-toi sur les fichiers de ce skill.

## Fichiers de référence

| Fichier | Quand le lire |
|---|---|
| [pieges.md](pieges.md) | **Toujours**, avant d'écrire la première requête |
| [glossaire.md](glossaire.md) | Dès que la question contient un terme métier (PAP, FAP, CT, actif, engagé, BE, COT...) |
| [schema.md](schema.md) | Pour choisir les tables : rôle de chaque table, granularité, jointures de référence |

Les **colonnes et leurs types** ne sont pas dans ces fichiers : lis-les avec le connecteur PostHog (schéma du data warehouse) avant d'écrire une requête sur une table que tu n'as pas encore utilisée.

## Les sources de données

1. **Tables de stats OLAP** (`activite_semaine`, `ct_actives`, `pap_*`...) : statistiques pré-calculées chaque jour depuis la prod. Les collectivités de test et les utilisateurs internes en sont déjà exclus. **C'est la source à privilégier** pour toute question de stats, de métriques ou d'OKRs.
2. **Tables `prod.*`** : miroir des données applicatives (collectivités, plans, fiches action, indicateurs, droits utilisateurs). À utiliser pour le détail fin. Les collectivités de test et les internes n'y sont **pas** exclus.
3. **Événements PostHog** (`events`) : le comportement dans l'app (`$pageview`, clics, parcours). Utilise-les seulement si la question porte sur la navigation, les pages consultées ou l'usage d'une fonctionnalité précise. Ils sont **sous-estimés** à cause des bloqueurs de publicité : ne les utilise jamais pour compter des utilisateurs actifs.

Les deux sources se croisent dans une même requête HogQL (JOIN entre `events` et une table du warehouse).

## Mode opératoire

### 1. Qualifier la question

- **Métrique ou stat** : tables de stats OLAP ; `prod.*` si aucune table de stats ne répond.
- **Détail applicatif** (contenu d'une fiche, d'un plan, d'un indicateur, droits) : `prod.*`.
- **Comportement dans l'app** : `events`.
- **Les deux** : croisement (voir l'étape 3).

Si un point change le résultat et qu'il n'est pas précisé, demande avant de requêter :
- la période ;
- « utilisateurs » au sens des agents des collectivités ou de tout le monde (BE et conseillers compris) ;
- « actif » sur 13 ou 52 semaines ;
- le référentiel `cae` ou `eci`.

Sinon, choisis le défaut indiqué dans [glossaire.md](glossaire.md) et annonce-le dans la réponse.

### 2. Choisir la bonne table (sources de vérité)

| Besoin | Table |
|---|---|
| Activité, fréquentation, utilisateurs actifs (agents) | `activite_semaine` |
| Utilisateurs actifs à 12 mois | `user_actif_12_mois` |
| Fréquentation globale, BE et conseillers compris | `user_actifs_ct_mois` |
| Collectivités activées, catégorie de collectivité | `ct_actives` |
| Collectivités PAP | `pap_date_passage` (`DISTINCT collectivite_id`) |
| North Star publique / interne | `pap_statut_5_fiches_modifiees_52_semaines` / `..._13_semaines` |
| Niveau de labellisation actuel | `labellisation` (dernière valeur par `referentiel`) |
| Email ↔ collectivité, droits | `prod.private_utilisateur_droit` + `prod.auth_users` (`au.id = pud.user_id`) |
| Conseillers, fonction d'un membre | `prod.private_collectivite_membre` |
| Utilisateurs internes à exclure | `internal_users` (`email`) |

N'utilise pas les tables marquées « à ignorer » ou « obsolète » dans [schema.md](schema.md).

### 3. Écrire la requête

- **HogQL est du SQL ClickHouse, pas du PostgreSQL.** Les exemples SQL de la doc OLAP d'origine sont en Postgres et doivent être traduits :
  - `TO_DATE(x, 'YYYY-MM-DD')` devient `toDate(x)` ;
  - `INTERVAL '3 months'` devient `INTERVAL 3 MONTH` ;
  - `x::int` devient `toInt64OrNull(x)`.
- **Vérifie le nom réel de la table et ses colonnes avec le connecteur.** Les noms de [schema.md](schema.md) sont logiques, et le warehouse peut ajouter un préfixe de source. N'invente ni table ni colonne.
- **Sur `prod.*`, filtre toujours** les collectivités de test (`prod.collectivite.type != 'test'`), les utilisateurs internes et, pour les fiches action, les sous-actions (`parent_id IS NULL`).
- **Sur `events`, filtre toujours :**
  - une plage `timestamp` ;
  - un `event` précis ;
  - l'app de production : `properties.$current_url ILIKE '%app.territoiresentransitions.fr%'`.
- **Mets toujours un `LIMIT` explicite.** Sans `LIMIT`, HogQL renvoie 100 lignes ; au-delà de 50 000, découpe la période (par mois) ou agrège davantage.
- **Agrège côté requête** (GROUP BY, DISTINCT) plutôt que de rapatrier des lignes brutes.
- **Pour croiser `events` et la base**, joins TOUJOURS sur `collectivite_id` ET `email` :
  - côté événements : `toInt64OrNull(properties.collectivite_id)` et `lower(trim(person.properties.email))` ;
  - côté base : `prod.private_utilisateur_droit` + `prod.auth_users` (droits actifs, emails en `lower(trim(...))`), ou `activite_semaine` en convertissant les types comme indiqué dans [pieges.md](pieges.md) ;
  - agrège les événements dans une sous-requête (par `collectivite_id` et `email`) avant de joindre.
- **Exclus toujours les utilisateurs internes** dès que des emails viennent des événements ou de `prod.*` : `lower(email) NOT IN (SELECT lower(email) FROM internal_users)`.
- **Lecture seule** : uniquement des `SELECT`.

En cas de doute sur une fonction ou une syntaxe HogQL, cherche dans la documentation PostHog avec le connecteur plutôt que de supposer.

### 4. Vérifier avant de répondre

- **Une requête qui renvoie 0 ligne ou un résultat absurde est probablement fausse**, pas une réalité métier. Vérifie la jointure, les types, les filtres de date et le nom de table.
- **Sur un croisement, mesure le taux de correspondance** (lignes jointes / lignes d'origine). S'il est faible, cherche la cause : casse des emails, `collectivite_id` en texte ou en flottant. En ClickHouse, une ligne sans correspondance dans un `LEFT JOIN` prend la valeur par défaut du type (chaîne vide), pas `NULL`.
- **Contrôle l'ordre de grandeur** avec une requête simple (par exemple le nombre total de collectivités actives sur la période) avant d'annoncer un chiffre détaillé.

### 5. Répondre

- En français, de façon factuelle et concise, en commençant par le résultat.
- Précise la période, la table source et les filtres appliqués (internes exclus, définition d'« actif » retenue, etc.).
- Montre la requête HogQL finale dans un bloc de code, pour qu'elle puisse être réutilisée.
- Signale les limites : données PostHog sous-estimées, table mise à jour une fois par jour, résultat tronqué par le `LIMIT`.
- N'invente jamais un chiffre : chaque nombre doit venir d'un résultat de requête.
