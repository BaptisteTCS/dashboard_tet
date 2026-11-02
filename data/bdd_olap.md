# vvDocumentation Base de données OLAP - Territoires en Transitions

> Base de données analytique alimentée quotidiennement depuis la base de production via Datalore. Contient l'ensemble des métriques, agrégations et exports pour les dashboards internes, statistiques publiques et partenaires externes.

---

## 📖 Glossaire


| Terme                        | Définition                                                                                                                            |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| **PAP**                      | Plan d'Action Pilotable - Un plan d'action qui a au moins 5 fiches avec un titre, un statut, une personne ou service/direction pilote |
| **PAP actif 13/52 semaines** | Un plan d'action pilotable qui a eu au moins 5 fiches modifiées au cours des 13/52 dernières semaines                                 |
| **FAP**                      | Fiche Action Pilotable - Une fiche action qui a au moins un titre, un statut et une personne ou service/direction pilote              |
| **BE**                       | Bureau d'Études (partenaire en back sur l'app)                                                                                        |
| **CT**                       | Collectivité                                                                                                                          |
| **OD**                       | Open Data (indicateurs)                                                                                                               |
| **CAE**                      | Climat-Air-Énergie (référentiel de labellisation)                                                                                     |
| **ECI**                      | Économie Circulaire (référentiel de labellisation)                                                                                    |
| **COT**                      | Contrat d'Objectif Territoriale                                                                                                       |
| **North Star**               | Métrique principale de succès de Territoires en Transitions                                                                           |


---



## ⚠️ Notes Importantes

1. **Filtrage systématique** : Toutes les stats doivent exclurent par défaut les utilisateurs internes et collectivités tests

---



## Tables Principales



### Activité & Engagement



#### `feature_all`

**Description :** Donne l'utilisation de toutes les features de l'app (plan, action, export, indicateurs, etc). Il y a autant de lignes par [mois,collectivite_id,email] que l'user a utlisé la feature ce mois-ci.

#### `activite_semaine`

**Description :** Source de vérité pour mesurer l'utilisation de l'application. Trace l'activité hebdomadaire par collectivité et par utilisateur.

**Contenu :**

- Activité hebdomadaire par collectivité et utilisateur : par (semaine/collectivite_id) il y a un email si la personne a visité l'app
- Exclut : utilisateurs internes, conseillers, BE (partenaires), adresses @ademe.fr
- Inclut : détection des modifications côté application (contourne les ad-blockers Posthog)

---



#### `user_actif_12_mois`

**Description :** Agrégation mensuelle des utilisateurs actifs à 12 mois, dérivée de `activite_semaine`. Pour chaque mois, on regarde ce mois et les 11 précédents et on compte le nombre de distinct email dans `activite_semaine`.

---



#### `user_actifs_ct_mois`

**Description :** Liste des utilisateurs actifs par collectivité et par mois. ⚠️ Inclut les BE et conseillers (contrairement à `activite_semaine`). C'est à utiliser quand on veut les stats globales de fréquentation (tous les utilisateurs) mais pas dans la plupart des cas quand on veut juste les utilisateurs des collectivités (agents)

---



### Collectivités



#### `ct_actives`

**Description :** Table des collectivités activées avec métadonnées enrichies. Utile pour les stats notamment avec la colonne catégorie qui es pertinente. Cette table n'est uniquement à utiliser pour faire des croisements et/ou quand on parle d'activation. Pour l'activité, c'est activite_semaine à utiliser.

**Contenu :**

- Date d'activation : première attribution d'un membre (hors BE/partenaires/conseillers)
- Catégorisation : EPCI, Syndicats, Communes, Départements, Régions
- ⚠️ Peut inclure des collectivités ayant uniquement des conseillers/BE si fonction non renseignée

---



#### `collectivite`

**Description :** Export de la table collectivités pour l'ADEME via Metabase. Contient toutes les info nécessaires sur les collectivités. Sauf cas spécifique, pour les stats on préfère utiliser ct_actives pour directement avoir les ct activés.

---



#### `internal_users`

**Description :** Liste des emails des utilisateurs internes TET, utilisée pour filtrer les stats.

**Usage :** Filtrage systématique dans toutes les métriques publiques/clients

---



### Plans d'Action



#### `pap_date_passage`

**Description :** 🔑 **Table critique** - Historique des dates de passage PAP (Plan d'Action Pilotable) pour chaque plan.

**Contenu :**

- Permet de déduire les collectivités PAP via `SELECT DISTINCT collectivite_id`

**Cas d'usage typique :** "Donne-moi les stats uniquement pour les collectivités PAP" → récupérer les ids depuis cette table

---



#### `passage_pap_region`

**Description :** Enrichissement de `pap_date_passage` avec région/département. Utilisée par les statistiques publiques.

**Calculé dans :** [Stats > Evolution pap region](https://datalore.jetbrains.com/notebook/3z8wdKwizolR7wA321R4Rl/zDBnbKbrbzhC1RYZAKnhxB/)

**Différence avec** `pap_date_passage` **:** Ajoute la dimension géographique, version utilisée en front

---



#### `plan_distrib`

**Description :** Statut et caractéristiques des plans d'action.

**Contenu :**

- Statut "actif à 12 mois" (≥5 fiches modifiées dans les 12 derniers mois)
- Score > 5
- Plan pilotable (oui/non)
- Département et région

---



#### `pap_statut_5_fiches_modifiees_52_semaines`

**Description :** 🌟 **North Star publique** - Plans avec ≥5 fiches pilotables modifiées dans les 52 dernières semaines.

**Indicateur clé :** Mesure l'engagement actif des collectivités (critère public)

---



#### `pap_statut_5_fiches_modifiees_13_semaines`

**Description :** 🌟 **North Star interne** - Version 13 semaines de la métrique ci-dessus.

**Indicateur clé :** Mesure l'engagement actif des collectivités (critère interne, plus exigeant)

---



### Scoring



#### `pap_note`

**Description :** Ancien système de notation des plans (échelle sur 5). ⚠️ En cours de migration vers le nouveau scoring sur 10.

**Historisation :** `pap_note_backup` contient l'évolution temporelle

---



#### `pap_note_snapshot`

## **Description :** Snapshot actuel des notes (sans historique), version instantanée de `pap_note`.



#### `note_plan_historique`

**Description :** Nouveau système de notation des plans (échelle sur 10), calculé comme moyenne des notes des actions.

**Historisation :** `note_plan_historique_backup`

---



#### `note_fiche_historique`

**Description :** Nouveau système de notation des fiches d'action (échelle sur 10).

**Historisation :** `note_fiche_historique_backup`

---



#### `pap_note_region`

**Description :** ⚠️ Table obsolète - Ancien scoring associé aux régions/départements

**Statut :** Utilisé par dashboard interne, à faire évoluer

---



### Fiches d'Action



#### `fa_distrib`

**Description :** Distribution des fiches d'action par département/région et par mois (valeurs cumulées).

**Contenu :**

- Nombre d'actions
- Nombre d'actions pilotables
- Nombre d'actions pilotables actives
- Nombre d'actions réalisées

**Terminologie front :** "action" = action pilotable, "action active" = action pilotable active

---



#### `nb_fap_13` / `nb_fap_52`

**Description :** Nombre de fiches d'action pilotables (FAP) actives sur 13/52 semaines.

**Note :** Redondant avec calcul A-1, à factoriser. Utilisé uniquement pour OKRs internes.

---



#### `nb_fap_pilote_13` / `nb_fap_pilote_52`

**Description :** Variante "pilotable" des tables ci-dessus.

#### `statut_fiche_13_semaines` / `statut_fiche_52_semaines`

**Description :** Donne pour chaque mois le statut d'une fiche en prenant comme critère une modification sur les 13/52 dernières semaines

---



### Indicateurs



#### `evolution_ind_pers`

**Description :** Évolution mensuelle des indicateurs personnalisés par département/région.

**Contenu :**

- `nb_ind_perso` : nombre d'indicateurs personnalisés créés
- `nb_ind_perso_ct` : nombre de collectivités ayant créé des indicateurs personnalisés

---



#### `evolution_ind_od`

**Description :** Évolution mensuelle du nombre de valeurs OD (Objectif et Données) cumulées par département/région.

---



#### `ind_od_producteur_indicateur`

**Description :** Couples indicateurs/producteurs par département/région.

---



### Labellisation



#### `labellisation`

**Description :** Historique complet de toutes les labellisations.

**Usage :** Pour connaître le niveau d'étoiles actuel d'une collectivité → prendre la dernière valeur de `etoiles` pour le référentiel souhaité (`cae` ou `eci`)

---



#### `labellisation_region`

**Description :** Enrichissement de `labellisation` avec données géographiques (région/département).

**Recommandation :** Préférer cette table à `evolution_labellisation` et recalculer à la volée si nécessaire

---



#### `labellisation_stock_evolution`

**Description :** Évolution mensuelle du stock de collectivités par niveau d'étoiles, par département/région.

---



#### `evolution_labellisation`

**Description :** Nombre de labellisations cumulées par mois.

**Recommandation :** Préférer `labellisation_region` et recalculer à la volée

---



### Statistiques Publiques



#### `stats_hero_section_site`

**Description :** Statistiques affichées dans la hero section de la landing page du site public.

---



## 📤 Tables Export & Intégrations



### Export ADEME (via Metabase)



#### `audit`

**Description :** Export des données d'audit pour l'ADEME.

---



#### `auditeur`

**Description :** Export des données auditeurs pour l'ADEME.

---



#### `visite_annuelle`

**Description :** Export des visites annuelles pour l'ADEME.

---



#### `cot`

**Description :** Export COT (Conseiller en Organisation Territoriale) pour l'ADEME.

---



#### `Score_mesures`

## **Description :** ⚠️ Attention à la casse (S majuscule) - Scores par mesure exportés vers l'ADEME.



#### `score_snapshot`

**Description :** Snapshot des scores pour l'ADEME

---



#### `utilisateurs`

**Description :** Export de la table utilisateurs pour l'ADEME.

---



#### `utilisateurs_droits`

**Description :** Export des droits utilisateurs pour l'ADEME.

---



### Synchro Airtable & stats bizdevs



#### `airtable_sync`

**Description :** Synchronisation quotidienne avec le CRM Airtable. Contient de nombreuses stats majeures par collectivité.

---



#### `airtable_sync_semaine`

**Description :** Sauvegarde hebdomadaire de l'état de `airtable_sync`.

---



#### `bizdev_A_F_contact`

**Description :** Contacts BizDev pour le tableau de bord commercial

---



#### `bizdev_note_de_suivi_contact`

**Description :** Notes de suivi des contacts BizDev.

---



#### `bizdev_contact_collectivite`

## **Description :** Mapping contacts BizDev ↔ collectivités.



#### `calendly_events`

**Description :** Événements Calendly pour le tableau de bord BizDev.

---



#### `calendly_invitees`

**Description :** Participants aux événements Calendly.

---



#### `evenements_airtable`

**Description :** Synchronisation événements Calendly → Airtable.

---



## 🔧 Tables Techniques & Versioning



#### `feature`

**Description :** Tracking des features mises en production (MEP).

---



#### `indicateurs_od`

**Description :** Listing de tous les indicateurs disponibles en open data sur Territoires en Transitions.

#### `fiche_action_plan`

**Description :** Permet de faire le lien entre les id de fiche action (fiche_id) et les plans (plan)

## 🗑️ Tables à Ignorer



#### `action_referentiel`

**Description :** Probablement utilisé par Power BI Benchmark. **À ignorer.**

---



#### `tmp_backup_indicateur_source_metadonnee`

**Description :** Backup du 13/04/2026 avant import données RARE. **À ignorer.**

---



#### `tmp_backup_indicateur_valeur`

**Description :** Backup du 13/04/2026 avant import données RARE. **À ignorer.**

---



#### `indicateur_definition`

**Description :** Définitions des indicateurs. Pourrait être utile à l'Ademe **À ignorer.**

---



#### `indicateurs_valeurs_olap`

**Description :** Utilisé par le module d'import des indicateurs Ecolab vers la prod. **À ignorer.**

---



#### `mapping_levier_mesure`

**Description :** Mapping leviers TE ↔ mesures référentiel pour l'outil de priorisation. **À ignorer.**

---



#### `modelisation_impact`

**Description :** Données pour l'outil de priorisation. **À ignorer.**

---



#### `tr_comm`

**Description :** Lien collectivités têtes ↔ format SIRET. **À ignorer.**