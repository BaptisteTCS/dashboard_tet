# PostHog (HogQL) et croisements avec la base

## Quand utiliser PostHog

- PostHog contient les evenements de l'application (pages vues, clics, navigation, sessions, usage fin d'une fonctionnalite).
- Pour compter des utilisateurs actifs / la frequentation, PRIVILEGIE `public.activite_semaine` (source de verite, contourne les ad-blockers qui bloquent PostHog). PostHog sert au detail : quelles pages, quels parcours, quelles fonctionnalites.
- Si la question peut etre resolue uniquement avec Postgres, n'utilise pas PostHog.

## Ecrire une requete HogQL

- Table principale : `events` (colonnes `event`, `timestamp`, `distinct_id`, `properties`, `person`).
- Proprietes d'evenement : `properties.<nom>` (ex : `properties.collectivite_id`, `properties.$current_url`, `properties.$pathname`).
- Proprietes de la personne : `person.properties.<nom>` (ex : `person.properties.email`).
- Evenement de page vue : `event = '$pageview'`. Pour decouvrir les autres evenements :
  `SELECT event, count() AS n FROM events WHERE timestamp >= now() - INTERVAL 30 DAY GROUP BY event ORDER BY n DESC LIMIT 200`
- Pour decouvrir les proprietes d'un evenement, regarde quelques lignes : `SELECT properties FROM events WHERE event = '...' LIMIT 5`.
- Filtre l'app de production : `properties.$current_url ILIKE '%app.territoiresentransitions.fr%'`.
- Fonctions de date utiles : `toStartOfWeek(timestamp)`, `toStartOfMonth(timestamp)`, `toDate(timestamp)`, `now() - INTERVAL 90 DAY`.
- Mets TOUJOURS un `LIMIT` explicite (maximum 50000). Sans LIMIT, PostHog ne renvoie que 100 lignes.
- Agrege et filtre au maximum cote PostHog (GROUP BY, DISTINCT, filtre d'URL, d'evenement) : ne rapatrie pas d'evenements bruts.
- Donne des alias simples en minuscules a toutes les colonnes (ex : `AS email`, `AS collectivite_id`, `AS semaine`).
- En cas de doute sur une fonction ou une syntaxe HogQL, consulte la doc avec web_search (posthog.com).

## Decoupage par mois ({start} / {end})

Une requete HogQL renvoie au maximum 50000 lignes. Pour une periode longue, utilise les marqueurs `{start}` et `{end}` et fournis `date_from` (et `date_to`, sinon maintenant) : la requete est executee mois par mois puis les resultats sont concatenes et dedoublonnes. Si `meta.truncated_windows` n'est pas vide, une fenetre a atteint la limite : ajoute des filtres ou agrege davantage.

Exemple (`date_from = '2025-01-01'`, `date_to = null`, `save_as = 'ph_pageviews'`) :

```sql
SELECT DISTINCT
    toStartOfWeek(timestamp) AS semaine,
    properties.collectivite_id AS collectivite_id,
    person.properties.email AS email,
    properties.$current_url AS url
FROM events
WHERE event = '$pageview'
  AND properties.collectivite_id IS NOT NULL
  AND timestamp >= toDateTime('{start}', 'UTC')
  AND timestamp < toDateTime('{end}', 'UTC')
  AND properties.$current_url ILIKE '%app.territoiresentransitions.fr%'
LIMIT 50000
```

Sans marqueurs, la requete est executee une seule fois (mets alors toi-meme un filtre sur `timestamp`).

## Utilisateurs internes

Les lignes dont la colonne `email` appartient a `public.internal_users` sont retirees automatiquement des resultats PostHog (`meta.internal_rows_removed`). Pour en beneficier, nomme la colonne email exactement `email`. Cote Postgres, exclus-les toi-meme (voir requete ci-dessous).

## Croiser PostHog et la base (workspace DuckDB)

Le workspace est un ensemble de tables propres a la conversation, interrogeables en SQL DuckDB via `query_workspace` ou `display_table` / `display_chart` avec `source='workspace'`. Les tables Postgres n'y sont PAS accessibles directement : enregistre d'abord ce dont tu as besoin avec `run_sql_query(save_as=...)`, en filtrant et agregeant cote Postgres.

La jointure PostHog <-> base se fait TOUJOURS sur `collectivite_id` ET `email`, via les droits utilisateurs :

```sql
SELECT pud.collectivite_id, lower(au.email) AS email, pud.niveau_acces
FROM prod.private_utilisateur_droit pud
JOIN prod.auth_users au ON au.id = pud.user_id
WHERE pud.active
  AND lower(au.email) NOT IN (SELECT lower(email) FROM public.internal_users WHERE email IS NOT NULL)
```

-> `run_sql_query(sql=..., save_as='users_collectivites')`. Ajoute les colonnes / jointures metier utiles (ex : `prod.collectivite` pour le nom, en excluant `type = 'test'`).

Dans DuckDB :
- `collectivite_id` vient de PostHog en texte : caste-le (`TRY_CAST(ph.collectivite_id AS BIGINT)`).
- Compare les emails en minuscules (`lower(ph.email) = u.email`).
- Les dates PostHog arrivent souvent en texte ISO : caste-les (`CAST(semaine AS DATE)` ou `TRY_CAST(... AS TIMESTAMP)`).
- Les tables s'appellent directement par leur nom (`ph_pageviews`, `users_collectivites`), sans prefixe de schema.

Exemple :

```sql
SELECT u.collectivite_id, count(DISTINCT ph.email) AS nb_utilisateurs, count(*) AS nb_lignes
FROM ph_pageviews ph
JOIN users_collectivites u
  ON TRY_CAST(ph.collectivite_id AS BIGINT) = u.collectivite_id
 AND lower(ph.email) = u.email
GROUP BY u.collectivite_id
ORDER BY nb_utilisateurs DESC
```

## Enchainement type

1. `run_hogql_query(..., save_as='ph_xxx')`
2. `run_sql_query(..., save_as='users_collectivites')` (ou autre table utile)
3. `query_workspace(...)` pour repondre en texte, ou `display_table(source='workspace')` / `display_chart(source='workspace')` pour afficher.

Le workspace est conserve pendant toute la conversation : reutilise les tables deja enregistrees (listees dans `workspace` des reponses d'outils) plutot que de relancer les requetes.
