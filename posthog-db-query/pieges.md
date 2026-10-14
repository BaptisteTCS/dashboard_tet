# Pièges et filtres obligatoires

À relire avant chaque première requête.

## 1. Filtres obligatoires

**Collectivités de test**
- Sur les tables `prod.*`, exclus-les toujours : `JOIN prod.collectivite c ON c.id = x.collectivite_id WHERE c.type != 'test'`.
- Les tables de stats (`activite_semaine`, `ct_actives`, `pap_*`, etc.) les excluent déjà : inutile de re-filtrer.

**Utilisateurs internes**
- Sur `prod.*` et sur `events`, exclus-les toujours : `lower(email) NOT IN (SELECT lower(email) FROM internal_users WHERE email IS NOT NULL)`.
- Les tables de stats les excluent déjà.

**Sous-actions**
- Toute stat sur les fiches action exclut les sous-actions (`prod.fiche_action.parent_id IS NULL`), sauf demande explicite.
- Exclus aussi les fiches supprimées : `coalesce(deleted, false) = false`.

**Droits actifs**
- Sur `prod.private_utilisateur_droit`, ne garde que `active = true`, sauf si on demande l'historique.

**Événements PostHog**
- Filtre toujours une plage `timestamp`, un `event` précis et l'app de production : `properties.$current_url ILIKE '%app.territoiresentransitions.fr%'`.

## 2. HogQL n'est pas du PostgreSQL

HogQL suit le dialecte ClickHouse. La documentation OLAP d'origine et les anciennes requêtes sont en Postgres : traduis-les.

| PostgreSQL | HogQL |
|---|---|
| `TO_DATE(x, 'YYYY-MM-DD')`, `x::date` | `toDate(x)` |
| `x::int`, `CAST(x AS INTEGER)` sur du texte douteux | `toInt64OrNull(x)` |
| `x::text` | `toString(x)` |
| `CURRENT_DATE`, `NOW()` | `today()`, `now()` |
| `INTERVAL '3 months'` | `INTERVAL 3 MONTH` |
| `date_trunc('month', d)` | `toStartOfMonth(d)` |
| `date_trunc('week', d)` | `toStartOfWeek(d)` (semaine commençant le dimanche ; `toMonday(d)` pour le lundi) |
| `DISTINCT ON (...)` | `argMax(valeur, date)` avec `GROUP BY` |
| `UNION` | `UNION DISTINCT` (ou `UNION ALL` puis `DISTINCT`) |
| `string_agg` | `arrayStringConcat(groupArray(x), ', ')` |

- **`count(DISTINCT x)`** fonctionne. **`uniq(x)`** est approximatif : ne l'utilise pas pour un chiffre exact.
- **Divisions** : `a / b` renvoie un flottant. Utilise `round(x, 1)` pour l'affichage et protège-toi des divisions par zéro avec `if(b = 0, NULL, a / b)`.
- **Comparaisons avec `NULL`** : `x != 'test'` est faux quand `x` est NULL. Si la colonne peut être nulle, écris `coalesce(x, '') != 'test'`.
- **`LEFT JOIN`** : une ligne sans correspondance prend la valeur par défaut du type (chaîne vide, `0`), pas `NULL`. Pour détecter l'absence de correspondance, teste `colonne != ''` (ou `= 0`), pas `IS NULL`.

## 3. Types à convertir

| Colonne | Type réel | À faire |
|---|---|---|
| `activite_semaine.semaine` | texte `YYYY-MM-DD` | `toDate(semaine)` |
| `activite_semaine.collectivite_id`, `user_actif_12_mois.collectivite_id` | flottant | `toInt64(collectivite_id)` avant de joindre |
| `user_actifs_ct_mois.mois`, `note_plan_historique.mois`, `statut_fiche_*.mois`, `nb_fap_*.mois`, `passage_pap_region.mois` | texte | `toDate(mois)` |
| `url_posthog.timestamp` | texte | `parseDateTimeBestEffort(timestamp)` |
| `prod.fiche_action.parent_id`, `prod.axe.parent`, `prod.indicateur_definition.collectivite_id`, `prod.indicateur_valeur.metadonnee_id` | flottant (nullable) | Teste `IS NULL` / `IS NOT NULL` ; `toInt64` pour joindre |
| `prod.auth_users.id`, `prod.private_utilisateur_droit.user_id` | texte | Jointure directe texte contre texte |
| `events.properties.collectivite_id`, `url_posthog.collectivite_id`, `posthog_next_path.collectivite_id` | texte | `toInt64OrNull(...)` |
| Tous les emails | texte, casse variable | `lower(trim(email))` des deux côtés |

Une jointure qui renvoie 0 ligne vient presque toujours d'un problème de type ou de casse, pas d'une absence de données.

## 4. Choisir la bonne table

- **Usage, utilisateurs actifs, collectivités actives** : `activite_semaine`, **jamais** les pages vues PostHog. PostHog est sous-estimé à cause des bloqueurs de publicité, alors que `activite_semaine` détecte aussi les modifications côté app.
- **`activite_semaine` vs `user_actifs_ct_mois`** : la première exclut BE, conseillers et @ademe.fr ; la seconde les inclut. Le défaut est `activite_semaine`.
- **Activation et activité** sont deux notions distinctes. `ct_actives` donne l'activation (date du premier membre), pas l'activité récente.
- **Tables homonymes** : `collectivite`, `labellisation`, `cot` et `score_snapshot` existent en version stats et en version `prod.*`, avec des colonnes et un sens différents. Les versions de stats sont des exports ADEME.
- **Labellisation actuelle** : prends la dernière valeur par collectivité et par référentiel, `argMax(etoiles, obtenue_le)`. `max(etoiles)` donne le meilleur niveau jamais atteint, qui diffère si une collectivité a perdu une étoile.
- **Tables mensuelles de statut** (`pap_statut_*`, `statut_fiche_*`, `user_actif_12_mois`) : pour la valeur actuelle, filtre sur `mois = (SELECT max(mois) FROM ...)`. Ne cumule pas les mois entre eux.
- **Tables cumulées** (`fa_distrib`, `evolution_ind_od`, `evolution_labellisation`) : chaque mois contient déjà le total. Ne somme pas les mois.
- **Tables `*_backup` et `*_historique_backup`** : historisation de l'état passé, pas l'état actuel.
- **Ancien scoring sur 5** (`pap_note*`) et **nouveau sur 10** (`note_plan_historique`, `note_fiche_historique`) : précise toujours lequel tu utilises. Le défaut est le nouveau.
- **Tables obsolètes ou à ignorer** : voir la fin de la partie stats dans [schema.md](schema.md).

## 5. Casse et noms de tables

- `Score_mesures` (S majuscule), `bizdev_A_F_contact` et la colonne `sub-feature` de `feature` doivent être entourées de backticks ou de guillemets selon ce qu'accepte HogQL.
- `crisp_temps_resoluton` s'écrit sans le second « i ».
- Le nom réel d'une table dans le warehouse peut porter un préfixe de source : vérifie-le avec le connecteur.

## 6. Limites de l'API PostHog

- **Sans `LIMIT`**, une requête renvoie 100 lignes. Le maximum est 50 000 lignes par requête.
- **Pour plus de lignes**, agrège davantage ou découpe la période par mois (une requête par mois, puis concaténation).
- **Les requêtes sur `events` sans filtre de date** sont lentes et peuvent expirer. Commence par une période courte (30 à 90 jours).
- **`person.properties.email` est nul** pour les visiteurs anonymes. Un filtre `NOT IN (internal_users)` élimine aussi ces lignes : c'est voulu pour les stats par utilisateur, mais il faut le savoir pour un comptage de pages vues brutes.
- **Données à J-1** : les tables de stats sont recalculées une fois par jour. Les événements PostHog sont quasi temps réel.

## 7. Garde-fous de réponse

- Lecture seule : uniquement des `SELECT`.
- N'annonce aucun chiffre qui ne vient pas d'un résultat de requête.
- Si un résultat vaut 0, est vide ou paraît incohérent, vérifie la requête (types, casse, filtres de date, nom de table) avant de conclure.
