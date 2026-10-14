# Glossaire : vocabulaire métier → tables, champs et événements

Quand un terme est ambigu et que la question ne précise rien, applique le **défaut** indiqué et annonce-le dans la réponse.

## Acteurs

| Terme | Signification | Où le trouver |
|---|---|---|
| **CT** | Collectivité | `prod.collectivite`, `ct_actives` |
| **Agent** / utilisateur d'une collectivité | Personne qui travaille pour une collectivité (hors BE, conseillers et internes) | `activite_semaine` (déjà filtrée) |
| **BE** | Bureau d'études, partenaire qui travaille dans l'app pour une collectivité | Inclus dans `user_actifs_ct_mois`, exclu de `activite_semaine` |
| **Conseiller** | Utilisateur qui a eu au moins une fois `prod.private_collectivite_membre.fonction = 'conseiller'` | `prod.private_collectivite_membre` |
| **Utilisateur interne** | Membre de l'équipe TET | `internal_users.email`, toujours à exclure |
| **Niveau d'accès** / droits | Droit d'un utilisateur sur une collectivité (lecture, édition, admin...) | `prod.private_utilisateur_droit.niveau_acces` |

**« Utilisateurs »** sans précision désigne par défaut les agents, via `activite_semaine`. Utilise `user_actifs_ct_mois` seulement si on parle de « tous les utilisateurs » ou de « fréquentation globale ».

## Activité et engagement

| Terme | Signification | Où le trouver |
|---|---|---|
| **Utilisateur actif** | A visité l'app (ou y a modifié quelque chose) dans la période | `activite_semaine` (DISTINCT `email`) |
| **Collectivité active** | Au moins un utilisateur actif dans la période | `activite_semaine` (DISTINCT `collectivite_id`) |
| **Actif à 12 mois** | Actif au moins une fois sur le mois et les 11 précédents | `user_actif_12_mois` |
| **Collectivité activée** / activation | A reçu son premier membre (hors BE, partenaires et conseillers) | `ct_actives.date_activation` |
| **Collectivité engagée** | A un COT ou une labellisation | `prod.cot` UNION `prod.labellisation` (DISTINCT `collectivite_id`) |
| **COT** | Contrat d'Objectif Territorial | `prod.cot` (présence dans la table = COT) |
| **Pipeline** | Étape commerciale de la collectivité | `pipeline`, `airtable_sync.pipeline` |

**« Actif »** pour un plan désigne par défaut la définition sur 52 semaines (North Star publique). Utilise 13 semaines si on parle d'OKR interne ou de « North Star interne ».

## Plans et actions

| Terme | Signification | Où le trouver |
|---|---|---|
| **Plan** / plan d'action | Axe racine | `prod.axe` où `id = plan` |
| **Axe**, sous-axe | Niveau de structuration d'un plan | `prod.axe` (`parent`, `plan`) |
| **FA**, **fiche action**, **action** | Fiche action d'un plan | `prod.fiche_action` |
| **Sous-action** | Fiche action dont `parent_id` est non nul | `prod.fiche_action.parent_id`, **exclue par défaut** de toutes les stats sur les fiches |
| **FAP** / fiche action pilotable | Fiche avec au moins un titre, un statut et un pilote (personne ou service / direction) | `fa_distrib`, `nb_fap_*`, `statut_fiche_*` |
| **Action active** (site public) | Action pilotable active | `fa_distrib.action_pilotable_actives` |
| **PAP** / plan d'action pilotable | Plan avec au moins 5 fiches pilotables | `pap_date_passage` |
| **Collectivité PAP** | Possède au moins un PAP | `SELECT DISTINCT collectivite_id FROM pap_date_passage` |
| **PAP actif 13 / 52 semaines** | PAP dont au moins 5 fiches ont été modifiées sur la période | `pap_statut_5_fiches_modifiees_13_semaines` / `_52_semaines`, `statut = 'actif'` |
| **North Star** | Métrique principale de succès : nombre de PAP actifs | Publique : 52 semaines ; interne : 13 semaines |
| **Note** / score d'un plan | Nouveau scoring sur 10 | `note_plan_historique`, `note_fiche_historique` |
| **Ancienne note** | Ancien scoring sur 5 | `pap_note`, `pap_note_snapshot` |
| **Fiche liée** | Fiche liée à une autre fiche | `prod.fiche_action_lien` |
| **Fiche liée à une mesure** | Fiche rattachée à une mesure du référentiel | `prod.fiche_action_action` |
| **Budget d'investissement** | Budget de type investissement | `prod.fiche_action_budget.type = 'investissement'` |
| **Pilote**, référent | Responsable d'une fiche ou d'un plan | `prod.fiche_action_pilote`, `prod.plan_pilote`, `*_referent` |

## Référentiels et labellisation

| Terme | Signification | Où le trouver |
|---|---|---|
| **Référentiel** | Grille d'évaluation : `cae` ou `eci` | Colonne `referentiel` / `referentiel_id` |
| **CAE** | Climat-Air-Énergie | `referentiel = 'cae'` |
| **ECI** | Économie circulaire | `referentiel = 'eci'` |
| **Mesure**, mesure du référentiel | Une `action` du référentiel (à ne pas confondre avec une fiche action) | `prod.action_definition`, `prod.action_statut` |
| **Étoiles**, niveau de labellisation | Niveau obtenu par référentiel | `labellisation.etoiles` (dernière valeur par référentiel) |
| **Collectivité labellisée** | Au moins une ligne dans `labellisation` avec `etoiles` ≥ 1 | `labellisation` |
| **Complétion du référentiel** | `(point_fait + point_programme + point_pas_fait) / point_potentiel * 100` (%) | `prod.score_snapshot` |
| **Audit** | Audit de labellisation | `prod.labellisation_audit`, `audit` (export) |

Si le référentiel n'est pas précisé, donne les résultats **séparément pour CAE et pour ECI**.

## Indicateurs

| Terme | Signification | Où le trouver |
|---|---|---|
| **Indicateur** | Définition d'un indicateur, désigné par son `identifiant_referentiel` (ex. `cae_43.a`, `covoit_lieu`) | `prod.indicateur_definition` |
| **Indicateur personnalisé** | Indicateur créé par une collectivité | `prod.indicateur_definition.collectivite_id IS NOT NULL` |
| **Valeur d'indicateur** | Valeur à une date | `prod.indicateur_valeur` (`indicateur_id` → `prod.indicateur_definition.id`) |
| **Valeurs renseignées** | Au moins une valeur dans `resultat` | `prod.indicateur_valeur.resultat IS NOT NULL` |
| **OD** / open data | Valeur venant d'une source open data | `prod.indicateur_valeur.metadonnee_id IS NOT NULL` |
| **Valeur utilisateur** | Valeur saisie par la collectivité | `prod.indicateur_valeur.metadonnee_id IS NULL` |

Les stats sur une série de valeurs d'indicateurs se groupent **toujours par `metadonnee_id`**, pour séparer les valeurs saisies par les utilisateurs des valeurs open data.

## Événements PostHog

| Terme | Signification | Où le trouver |
|---|---|---|
| **Page vue**, visite | Affichage d'une page | `events`, `event = '$pageview'` |
| **URL**, page | Adresse ou chemin de la page | `properties.$current_url`, `properties.$pathname` |
| **Collectivité de l'événement** | Collectivité consultée | `properties.collectivite_id` (texte) |
| **Email de l'utilisateur** | Personne identifiée | `person.properties.email` |
| **App de production** | Uniquement l'app réelle | `properties.$current_url ILIKE '%app.territoiresentransitions.fr%'` |
| **Session** | Session de navigation | `$session_id` (propriété ou colonne selon le contexte) |
| **Parcours**, page suivante | Enchaînement des pages | `posthog_next_path` (table déjà calculée) ou `events` |
| **Usage d'une fonctionnalité** | Événement dédié ou page spécifique | `feature` (table), sinon `events` filtrés sur l'événement ou le chemin |

Pour découvrir les noms d'événements disponibles, agrège `events` par `event` sur une fenêtre courte (30 jours) avec un `LIMIT`, avant de filtrer sur un événement précis.
