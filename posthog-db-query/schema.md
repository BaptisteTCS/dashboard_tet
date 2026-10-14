# Tables du warehouse : rôle et usage

Ce fichier décrit **à quoi sert chaque table** et **quand l'utiliser**. Les colonnes et leurs types ne sont pas listés ici : lis-les avec le connecteur PostHog (schéma du data warehouse), qui est toujours à jour. Seules les colonnes qui comptent pour les jointures ou qui ont un piège sont mentionnées.

Les noms ci-dessous sont les noms logiques (`prod.xxx`, `xxx` pour les tables de stats). Le nom réel dans le warehouse peut porter un préfixe de source : vérifie-le avec le connecteur.

La base contient deux familles de tables :
- **Tables de stats (schéma `public`)** : pré-calculées chaque jour. Les collectivités de test et les utilisateurs internes en sont déjà exclus. **À privilégier pour toute question de stats.**
- **Tables `prod.*`** : miroir des données applicatives de production. À utiliser pour le détail fin (contenu d'une fiche, d'un plan, d'un indicateur, droits utilisateurs). Les collectivités de test et les utilisateurs internes n'en sont **pas** exclus.

Plusieurs tables portent le même nom dans les deux familles (`collectivite`, `labellisation`, `cot`, `score_snapshot`) : leurs colonnes et leur sens diffèrent. Vérifie toujours laquelle tu interroges.

---

## Tables de stats (public)

### Activité et utilisateurs

| Table | Une ligne = | Rôle et usage |
|---|---|---|
| `activite_semaine` | (semaine, collectivite_id, email) | **Source de vérité de l'usage.** Un email présent signifie que la personne a visité l'app cette semaine-là pour cette collectivité. La table exclut les internes, les conseillers, les BE et les adresses @ademe.fr. Elle inclut la détection des modifications côté app, ce qui contourne les bloqueurs de publicité qui gênent PostHog. `semaine` est du texte, `collectivite_id` un flottant. |
| `user_actif_12_mois` | (mois, collectivite_id, email) | Utilisateurs actifs à 12 mois, dérivés de `activite_semaine`. Pour chaque mois, on prend ce mois et les 11 précédents. |
| `user_actifs_ct_mois` | (mois, collectivite_id, email) | Utilisateurs actifs par collectivité et par mois, **BE et conseillers compris**. À utiliser seulement pour la fréquentation globale, pas pour les seuls agents des collectivités. `mois` est du texte. |
| `internal_users` | email | Emails des utilisateurs internes TET. À exclure dès que tu travailles sur `prod.*` ou sur les événements PostHog. |
| `utilisateurs` / `utilisateurs_droits` | utilisateur / (utilisateur, collectivité) | Exports ADEME des utilisateurs et de leurs droits, avec la fonction. La jointure de référence reste `prod.private_utilisateur_droit` + `prod.auth_users`. |
| `feature` | utilisation d'une fonctionnalité | Suivi des fonctionnalités mises en production : `datetime`, `collectivite_id`, `email`, `feature`, `sub-feature`. |

### Collectivités

| Table | Une ligne = | Rôle et usage |
|---|---|---|
| `ct_actives` | collectivité activée | Collectivités activées : `date_activation` (première attribution d'un membre hors BE, partenaires et conseillers) et `categorie` (EPCI, Syndicats, Communes, Départements, Régions). À utiliser pour l'activation et pour les croisements par catégorie. **Pas pour l'activité** (voir `activite_semaine`). Peut inclure des collectivités qui n'ont que des conseillers ou des BE si la fonction n'est pas renseignée. |
| `collectivite` | collectivité | Export ADEME. Contient population, région, département, complétude CAE/ECI, `activee`, `date_activation_tet`. Pour les stats, préférer `ct_actives`. |
| `cot` | collectivité sous COT | Export COT pour l'ADEME. |
| `pipeline` | (collectivite_id, semaine) | Étape du pipeline commercial de la collectivité chaque semaine. |

### Plans d'action et fiches

| Table | Une ligne = | Rôle et usage |
|---|---|---|
| `pap_date_passage` | plan devenu PAP | **Table critique.** Date de passage en PAP de chaque plan (`collectivite_id`, `plan`, `passage_pap`). `SELECT DISTINCT collectivite_id` donne les collectivités PAP. |
| `passage_pap_region` | plan PAP + géographie | Version de `pap_date_passage` enrichie de la région et du département, utilisée par les stats publiques. |
| `plan_distrib` | plan | Statut d'un plan : `actif_12_mois` (au moins 5 fiches modifiées en 12 mois), `score_sup_5`, `pilotable`, département et région. |
| `pap_statut_5_fiches_modifiees_52_semaines` | (mois, plan) | **North Star publique** : `statut = 'actif'` si au moins 5 fiches pilotables ont été modifiées sur 52 semaines. Pour la valeur actuelle, prendre le dernier `mois`. |
| `pap_statut_5_fiches_modifiees_13_semaines` | (mois, plan) | **North Star interne** : même calcul sur 13 semaines, plus exigeant. |
| `statut_fiche_13_semaines` / `statut_fiche_52_semaines` | (fiche_id, mois) | Statut mensuel d'une fiche, selon qu'elle a été modifiée ou non sur les 13 ou 52 dernières semaines. `mois` est du texte. |
| `nb_fap_13` / `nb_fap_52`, `nb_fap_pilote_13` / `nb_fap_pilote_52` | (mois, fiche_id) | Fiches action pilotables actives sur 13 ou 52 semaines. Réservées aux OKRs internes ; redondantes avec les tables `statut_fiche_*`. |
| `fa_distrib` | (mois, département, région) | Nombre de fiches, de fiches pilotables, de fiches pilotables actives et de fiches réalisées. **Valeurs cumulées** : ne pas les sommer d'un mois à l'autre. Sur le site public, « action » = action pilotable. |
| `fa_sharing` | mois | Nombre de fiches partagées entre collectivités. |
| `fiche_action_plan` | (fiche_id, plan) | Lien direct entre une fiche et son plan. Plus simple que de passer par `prod.fiche_action_axe` et `prod.axe`. |

### Notation des plans et fiches

| Table | Rôle et usage |
|---|---|
| `note_plan_historique` | **Nouveau scoring des plans, sur 10** (moyenne des notes des fiches), par plan et par mois (`mois` en texte). Historisé dans `note_plan_historique_backup`. |
| `note_plan_semaine` | Note des plans par semaine. |
| `note_fiche_historique` | Nouveau scoring des fiches, sur 10, avec le détail des critères (`score_*`) et `note_fa`. Historisé dans `note_fiche_historique_backup`. |
| `pap_note`, `pap_note_snapshot`, `pap_note_backup` | **Ancien scoring sur 5**, en cours de migration. Encore utilisé par des dashboards : à n'utiliser que si on te demande explicitement l'ancienne note. |

### Labellisation

| Table | Rôle et usage |
|---|---|
| `labellisation` | Historique de toutes les labellisations (`collectivite_id`, `referentiel` = `cae` ou `eci`, `etoiles`, `obtenue_le`). Le niveau actuel est la dernière valeur par référentiel. |
| `labellisation_region` | La même chose, enrichie de la région et du département. **À préférer** à `evolution_labellisation`. |
| `labellisation_stock_evolution` | Stock mensuel de collectivités par niveau d'étoiles, par département et région. |
| `evolution_labellisation` | Labellisations cumulées par mois. Préférer `labellisation_region` et recalculer. |

### Indicateurs

| Table | Rôle et usage |
|---|---|
| `evolution_ind_pers` | Évolution mensuelle des indicateurs personnalisés (`nb_ind_perso`, `nb_ind_perso_ct`) par département et région. |
| `evolution_ind_od` | Évolution mensuelle du nombre cumulé de valeurs d'indicateurs open data, par département et région. |
| `ind_od_producteur_indicateur` | Couples indicateur / producteur open data, par département et région. |
| `indicateurs_od` | Liste des indicateurs disponibles en open data. |

### Support, satisfaction et commercial

| Table | Rôle et usage |
|---|---|
| `crisp_conversation` | Conversations de support Crisp (email, segments, opérateur, dates). |
| `crisp_nb_conversation`, `crisp_nb_message`, `crisp_rating`, `crisp_temps_reponse`, `crisp_temps_resoluton` | Agrégats mensuels du support Crisp (attention à la faute dans `resoluton`). |
| `taux_contact_support` | Taux mensuel de contact du support pour un bug. |
| `notion_ticket` | Tickets bug et support (thématique, criticité, statut, temps de résolution, email, `id_collectivite`). |
| `nps` | Score NPS. |
| `airtable_sync` | Synchronisation quotidienne avec le CRM Airtable. Une ligne par collectivité, avec de nombreuses stats prêtes à l'emploi : contributeurs, fiches modifiées sur 3, 6 et 12 mois, PAP, note du plan, dernière visite, pipeline. |
| `airtable_sync_semaine` | Sauvegarde hebdomadaire de `airtable_sync`. |
| `bizdev_A_F_contact`, `bizdev_note_de_suivi_contact`, `bizdev_contact_collectivite` | Contacts et suivi BizDev (attention à la casse de `bizdev_A_F_contact`). |
| `calendly_events`, `calendly_invitees`, `evenements_airtable` | Rendez-vous Calendly et leur synchronisation vers Airtable. |

### Exports ADEME

`audit`, `auditeur`, `visite_annuelle`, `Score_mesures` (S majuscule), `score_snapshot` (version export, différente de `prod.score_snapshot`) : exports pour l'ADEME. À n'utiliser que si la question porte sur ces exports.

### Extraits PostHog déjà présents dans la base

| Table | Rôle et usage |
|---|---|
| `url_posthog` | Pages vues extraites de PostHog (`distinct_id`, `session_id`, `current_url`, `email`, `collectivite_id`, `timestamp` en texte). |
| `posthog_next_path` | Transitions de navigation (page courante, page suivante, horodatages) par email et collectivité. |

Ces deux tables évitent de requêter `events` pour les questions de navigation courantes. Pour des données plus récentes ou un autre événement, interroge `events` directement.

### Tables à ignorer

`action_referentiel`, `tmp_backup_indicateur_source_metadonnee`, `tmp_backup_indicateur_valeur`, `indicateur_definition` (version stats ; utilise `prod.indicateur_definition`), `indicateurs_valeurs_olap`, `mapping_levier_mesure`, `modelisation_impact`, `priorisation*`, `tr_comm`, `airtable_sync_semaine_old`, `pap_note_region` (obsolète).

`stats_hero_section_site` alimente la page d'accueil du site public : tu peux la lire, mais ses chiffres ne sont pas une source de calcul.

---

## Tables prod.* (données applicatives)

À filtrer systématiquement : `prod.collectivite.type != 'test'` et utilisateurs internes (voir [pieges.md](pieges.md)).

### Collectivités et utilisateurs

| Table | Rôle et usage |
|---|---|
| `prod.collectivite` | Référentiel des collectivités (`id`, `nom`, `type`, codes géographiques, `population`). **`type = 'test'` signale une collectivité de test.** |
| `prod.collectivite_carte_identite` | Identité enrichie : type, région, département, population totale, `is_cot`. |
| `prod.auth_users` | Comptes utilisateurs. `id` (texte) correspond à `user_id` ; contient `email`. |
| `prod.private_utilisateur_droit` | Droit d'un utilisateur sur une collectivité : `user_id`, `collectivite_id`, `active`, `niveau_acces`. **Pivot de la jointure email / collectivité.** |
| `prod.private_collectivite_membre` | Fonction d'un membre dans une collectivité (`fonction`, `details_fonction`, `est_referent`, `champ_intervention`). `fonction = 'conseiller'` désigne un conseiller. |
| `prod.cot` | Collectivités sous COT. Une collectivité absente de la table n'a pas de COT. |

### Plans, axes et fiches action

| Table | Rôle et usage |
|---|---|
| `prod.axe` | Plans et axes. **Un plan est un axe dont `id = plan`.** Les sous-axes pointent vers leur plan via `plan` et vers leur parent via `parent`. |
| `prod.fiche_action` | Fiches action. `parent_id` non nul signale une **sous-action** ; `deleted` signale une fiche supprimée. |
| `prod.fiche_action_axe` | Lien entre une fiche et un axe (`fiche_id`, `axe_id`). |
| `prod.fiche_action_lien` | Fiches liées entre elles (`fiche_une`, `fiche_deux`). |
| `prod.fiche_action_action` | Lien entre une fiche et une mesure du référentiel (`action_id`). |
| `prod.fiche_action_budget` | Budgets d'une fiche par année. `type = 'investissement'` pour le budget d'investissement. |
| `prod.fiche_action_pilote`, `prod.fiche_action_referent` | Pilotes et référents d'une fiche (utilisateur ou tag). |
| `prod.fiche_action_*_tag`, `prod.fiche_action_thematique`, `prod.fiche_action_sous_thematique`, `prod.fiche_action_indicateur`, `prod.fiche_action_etape`, `prod.fiche_action_note`, `prod.fiche_action_sharing` | Attributs d'une fiche : services, structures, financeurs, partenaires, thématiques, indicateurs liés, étapes, notes de suivi, partages. |
| `prod.plan_pilote`, `prod.plan_referent` | Pilotes et référents d'un plan. |
| `prod.historique_fiche_action`, `prod.historique_fiche_action_pilote`, `prod.historique_action_statut` | Historiques des modifications. |

### Référentiels (mesures)

| Table | Rôle et usage |
|---|---|
| `prod.action_definition`, `prod.action_relation` | Mesures des référentiels CAE et ECI, et leur hiérarchie. Une « mesure » est une `action` dans ces tables. |
| `prod.action_statut` | Avancement d'une mesure par collectivité. |
| `prod.action_pilote`, `prod.action_service`, `prod.action_commentaire` | Pilotes, services et commentaires d'une mesure. |
| `prod.score_snapshot` | Snapshots des scores par collectivité et référentiel (`point_fait`, `point_programme`, `point_pas_fait`, `point_potentiel`, `type_jalon`, `date`). |
| `prod.referentiel_definition`, `prod.referentiel_tag` | Définition des référentiels. |

### Indicateurs

| Table | Rôle et usage |
|---|---|
| `prod.indicateur_definition` | Définitions des indicateurs. `identifiant_referentiel` (ex. `cae_43.a`, `covoit_lieu`) est l'identifiant parlé. **`collectivite_id` non nul signale un indicateur personnalisé.** |
| `prod.indicateur_valeur` | Valeurs des indicateurs (`indicateur_id`, `collectivite_id`, `date_valeur`, `resultat`, `objectif`, `metadonnee_id`). **`metadonnee_id` nul = valeur saisie par un utilisateur ; non nul = source open data.** |
| `prod.indicateur_source_metadonnee`, `prod.indicateur_source` | Sources open data (producteur, diffuseur, méthodologie). |
| `prod.indicateur_collectivite`, `prod.indicateur_pilote`, `prod.indicateur_*` | Favoris, pilotes, thématiques et liens des indicateurs. |

### Labellisation

| Table | Rôle et usage |
|---|---|
| `prod.labellisation` | Labellisations obtenues (`etoiles`, `referentiel`, `obtenue_le`). |
| `prod.labellisation_audit`, `prod.labellisation_demande`, `prod.labellisation_action_audit_state`, `prod.labellisation_preuve_base`, `prod.labellisation_etoile_meta` | Processus de labellisation : demandes, audits, preuves. |

---

## Jointures de référence

- **Toutes les tables** se rejoignent par `collectivite_id`, ou `prod.collectivite.id`.
- **Email ↔ collectivité** : `prod.private_utilisateur_droit pud JOIN prod.auth_users au ON au.id = pud.user_id`, avec `pud.active`.
- **Fiche → plan** : `fiche_action_plan`, ou `prod.fiche_action_axe` → `prod.axe` (colonne `plan`).
- **Événements PostHog ↔ base** : sur `collectivite_id` ET `email`. Les conversions de type sont dans [pieges.md](pieges.md).
