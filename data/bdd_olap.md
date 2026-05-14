# Documentation Base de données OLAP - Territoires en Transitions

> Base de données analytique alimentée quotidiennement depuis la base de production via Datalore. Contient l'ensemble des métriques, agrégations et exports pour les dashboards internes, statistiques publiques et partenaires externes.

---

## Tables Principales

### Activité & Engagement

#### `activite_semaine`
**Description :** Source de vérité pour mesurer l'utilisation de l'application. Trace l'activité hebdomadaire par collectivité et par utilisateur.

**Contenu :**
- Activité hebdomadaire par collectivité et utilisateur : par (semaine/collectivite_id) il y a un email si la personne a visité l'app
- Exclut : utilisateurs internes, conseillers, BE (partenaires), adresses @ademe.fr
- Inclut : détection des modifications côté application (contourne les ad-blockers Posthog)

**Calculé dans :** [OKRs > L-2](https://datalore.jetbrains.com/notebook/3z8wdKwizolR7wA321R4Rl/Dz9DmMwquBQiWTJN0JKlCn/)

**Utilisé pour :** Dashboard OKRs, stats publiques.

---

#### `user_actif_12_mois`
**Description :** Agrégation mensuelle des utilisateurs actifs à 12 mois, dérivée de `activite_semaine`. Pour chaque mois, on regarde ce mois et les 11 précédents et on compte le nombre de distinct email dans `activite_semaine`.

**Calculé dans :** [OKRs > L-2](https://datalore.jetbrains.com/notebook/3z8wdKwizolR7wA321R4Rl/Dz9DmMwquBQiWTJN0JKlCn/)

**Utilisé pour :** Dashboard OKRs, stats publiques.

---

#### `user_actifs_ct_mois`
**Description :** Liste des utilisateurs actifs par collectivité et par mois. ⚠️ Inclut les BE et conseillers (contrairement à `activite_semaine`). C'est à utiliser quand on veut les stats globales de fréquentation (tous les utilisateurs) mais pas dans la plupart des cas quand on veut juste les utilisateurs des collectivités (agents)

**Calculé dans :** [Stats > User actifs](https://datalore.jetbrains.com/notebook/3z8wdKwizolR7wA321R4Rl/zDBnbKbrbzhC1RYZAKnhxB/)

**Utilisé pour :** Dahsboard okrs, stats publiques.

---

### Collectivités

#### `ct_actives`
**Description :** Table des collectivités activées avec métadonnées enrichies. Utile pour les stats notamment avec la colonne catégorie qui es pertinente. Cette table n'est uniquement à utiliser pour faire des croisements et/ou quand on parle d'activation. Pour l'activité, c'est activite_semaine à utiliser.

**Contenu :**
- Date d'activation : première attribution d'un membre (hors BE/partenaires/conseillers)
- Catégorisation : EPCI, Syndicats, Communes, Départements, Régions
- ⚠️ Peut inclure des collectivités ayant uniquement des conseillers/BE si fonction non renseignée

**Calculé dans :** [Stats > Date activation](https://datalore.jetbrains.com/notebook/3z8wdKwizolR7wA321R4Rl/zDBnbKbrbzhC1RYZAKnhxB/)

**Utilisé pour :** Stat publiques.

---

#### `collectivite`
**Description :** Export de la table collectivités pour l'ADEME via Metabase. Contient toutes les info nécessaires sur les collectivités. Sauf cas spécifique, pour les stats on préfère utiliser ct_actives pour directement avoir les ct activés.

**Calculé dans :** [Export TET → Ademe > Collectivités](https://datalore.jetbrains.com/notebook/3z8wdKwizolR7wA321R4Rl/LhsccNs3HBiP4wnuv67kP7/)

**Utilisé pour :** Export ADEME

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

**Calculé dans :** [Calcul PAP & Score > Passage PAP](https://datalore.jetbrains.com/notebook/3z8wdKwizolR7wA321R4Rl/TUsBeh2ErVoeFgtptt9A8g/)

**Cas d'usage typique :** "Donne-moi les stats uniquement pour les collectivités PAP" → récupérer les ids depuis cette table

---

#### `passage_pap_region`
**Description :** Enrichissement de `pap_date_passage` avec région/département. Utilisée par les statistiques publiques.

**Calculé dans :** [Stats > Evolution pap region](https://datalore.jetbrains.com/notebook/3z8wdKwizolR7wA321R4Rl/zDBnbKbrbzhC1RYZAKnhxB/)

**Différence avec `pap_date_passage` :** Ajoute la dimension géographique, version utilisée en front

---

#### `plan_distrib`
**Description :** Statut et caractéristiques des plans d'action.

**Contenu :**
- Statut "actif à 12 mois" (≥5 fiches modifiées dans les 12 derniers mois)
- Score > 5
- Plan pilotable (oui/non)
- Département et région

**Calculé dans :** [Stats > plan_distrib](https://datalore.jetbrains.com/notebook/3z8wdKwizolR7wA321R4Rl/zDBnbKbrbzhC1RYZAKnhxB/)

---

#### `pap_statut_5_fiches_modifiees_52_semaines`
**Description :** 🌟 **North Star publique** - Plans avec ≥5 fiches pilotables modifiées dans les 52 dernières semaines.

**Calculé dans :** [OKRs > Activité fiche | A-1](https://datalore.jetbrains.com/notebook/3z8wdKwizolR7wA321R4Rl/Dz9DmMwquBQiWTJN0JKlCn/)

**Indicateur clé :** Mesure l'engagement actif des collectivités (critère public)

---

#### `pap_statut_5_fiches_modifiees_13_semaines`
**Description :** 🌟 **North Star interne** - Version 13 semaines de la métrique ci-dessus.

**Calculé dans :** [OKRs > Activité fiche | A-1](https://datalore.jetbrains.com/notebook/3z8wdKwizolR7wA321R4Rl/Dz9DmMwquBQiWTJN0JKlCn/)

**Indicateur clé :** Mesure l'engagement actif des collectivités (critère interne, plus exigeant)

---

### Scoring

#### `pap_note`
**Description :** Ancien système de notation des plans (échelle sur 5). ⚠️ En cours de migration vers le nouveau scoring sur 10.

**Calculé dans :** [Calcul PAP & Score > Score PAP](https://datalore.jetbrains.com/notebook/3z8wdKwizolR7wA321R4Rl/TUsBeh2ErVoeFgtptt9A8g/)

**Historisation :** `pap_note_backup` contient l'évolution temporelle

**Statut :** Encore utilisé par les dashboards Streamlit, migration à venir

---

#### `pap_note_snapshot`
**Description :** Snapshot actuel des notes (sans historique), version instantanée de `pap_note`.

**Calculé dans :** [Calcul PAP & Score > Score PAP](https://datalore.jetbrains.com/notebook/3z8wdKwizolR7wA321R4Rl/TUsBeh2ErVoeFgtptt9A8g/)

---

#### `note_plan_historique`
**Description :** Nouveau système de notation des plans (échelle sur 10), calculé comme moyenne des notes des actions.

**Calculé dans :** [OKRs > New pap note](https://datalore.jetbrains.com/notebook/3z8wdKwizolR7wA321R4Rl/Dz9DmMwquBQiWTJN0JKlCn/)

**Historisation :** `note_plan_historique_backup`

---

#### `note_fiche_historique`
**Description :** Nouveau système de notation des fiches d'action (échelle sur 10).

**Calculé dans :** [OKRs > New fiche note](https://datalore.jetbrains.com/notebook/3z8wdKwizolR7wA321R4Rl/Dz9DmMwquBQiWTJN0JKlCn/)

**Historisation :** `note_fiche_historique_backup`

---

#### `pap_note_region`
**Description :** ⚠️ Table obsolète - Ancien scoring associé aux régions/départements.

**Calculé dans :** [Stats > Evolution note region](https://datalore.jetbrains.com/notebook/3z8wdKwizolR7wA321R4Rl/zDBnbKbrbzhC1RYZAKnhxB/)

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

**Calculé dans :** [Stats > fa_distrib](https://datalore.jetbrains.com/notebook/3z8wdKwizolR7wA321R4Rl/zDBnbKbrbzhC1RYZAKnhxB/)

**Terminologie front :** "action" = action pilotable, "action active" = action pilotable active

---

#### `nb_fap_13` / `nb_fap_52`
**Description :** Nombre de fiches d'action pilotables (FAP) actives sur 13/52 semaines.

**Calculé dans :** [OKRs > A-3](https://datalore.jetbrains.com/notebook/3z8wdKwizolR7wA321R4Rl/Dz9DmMwquBQiWTJN0JKlCn/)

**Note :** Redondant avec calcul A-1, à factoriser. Utilisé uniquement pour OKRs internes.

---

#### `nb_fap_pilote_13` / `nb_fap_pilote_52`
**Description :** Variante "pilotable" des tables ci-dessus.

**Calculé dans :** [OKRs > A-3](https://datalore.jetbrains.com/notebook/3z8wdKwizolR7wA321R4Rl/Dz9DmMwquBQiWTJN0JKlCn/)

#### `statut_fiche_13_semaines` / `statut_fiche_52_semaines`
**Description :** Donne pour chaque mois le statut d'une fiche en prenant comme critère une modification sur les 13/52 dernières semaines

**Calculé dans :** [OKRs > Activité fiche | A-1](https://datalore.jetbrains.com/notebook/3z8wdKwizolR7wA321R4Rl/Dz9DmMwquBQiWTJN0JKlCn/)

---

### Indicateurs

#### `evolution_ind_pers`
**Description :** Évolution mensuelle des indicateurs personnalisés par département/région.

**Contenu :**
- `nb_ind_perso` : nombre d'indicateurs personnalisés créés
- `nb_ind_perso_ct` : nombre de collectivités ayant créé des indicateurs personnalisés

**Calculé dans :** [Stats > evolution ind pers et od](https://datalore.jetbrains.com/notebook/3z8wdKwizolR7wA321R4Rl/zDBnbKbrbzhC1RYZAKnhxB/)

---

#### `evolution_ind_od`
**Description :** Évolution mensuelle du nombre de valeurs OD (Objectif et Données) cumulées par département/région.

**Calculé dans :** [Stats > evolution ind pers et od](https://datalore.jetbrains.com/notebook/3z8wdKwizolR7wA321R4Rl/zDBnbKbrbzhC1RYZAKnhxB/)

---

#### `ind_od_producteur_indicateur`
**Description :** Couples indicateurs/producteurs par département/région.

**Calculé dans :** [Stats > evolution ind pers et od](https://datalore.jetbrains.com/notebook/3z8wdKwizolR7wA321R4Rl/zDBnbKbrbzhC1RYZAKnhxB/)

---

### Labellisation

#### `labellisation`
**Description :** Historique complet de toutes les labellisations.

**Usage :** Pour connaître le niveau d'étoiles actuel d'une collectivité → prendre la dernière valeur de `etoiles` pour le référentiel souhaité (`cae` ou `eci`)

**Calculé dans :** [Stats > labellisation_region](https://datalore.jetbrains.com/notebook/3z8wdKwizolR7wA321R4Rl/zDBnbKbrbzhC1RYZAKnhxB/)

---

#### `labellisation_region`
**Description :** Enrichissement de `labellisation` avec données géographiques (région/département).

**Calculé dans :** [Stats > labellisation_region](https://datalore.jetbrains.com/notebook/3z8wdKwizolR7wA321R4Rl/zDBnbKbrbzhC1RYZAKnhxB/)

**Recommandation :** Préférer cette table à `evolution_labellisation` et recalculer à la volée si nécessaire

---

#### `labellisation_stock_evolution`
**Description :** Évolution mensuelle du stock de collectivités par niveau d'étoiles, par département/région.

**Calculé dans :** [Stats > labellisation_stock_evolution](https://datalore.jetbrains.com/notebook/3z8wdKwizolR7wA321R4Rl/zDBnbKbrbzhC1RYZAKnhxB/)

---

#### `evolution_labellisation`
**Description :** Nombre de labellisations cumulées par mois.

**Calculé dans :** [OKRs > L-3](https://datalore.jetbrains.com/notebook/3z8wdKwizolR7wA321R4Rl/Dz9DmMwquBQiWTJN0JKlCn/)

**Recommandation :** Préférer `labellisation_region` et recalculer à la volée

---

### Statistiques Publiques

#### `stats_hero_section_site`
**Description :** Statistiques affichées dans la hero section de la landing page du site public.

**Calculé dans :** [OKRs > hero section stat public](https://datalore.jetbrains.com/notebook/3z8wdKwizolR7wA321R4Rl/Dz9DmMwquBQiWTJN0JKlCn/)

**⚠️ Ne pas modifier sans validation**

---

## 📤 Tables Export & Intégrations

### Export ADEME (via Metabase)

#### `audit`
**Description :** Export des données d'audit pour l'ADEME.

**Calculé dans :** [Export TET → Ademe > Audits](https://datalore.jetbrains.com/notebook/3z8wdKwizolR7wA321R4Rl/LhsccNs3HBiP4wnuv67kP7/)

---

#### `auditeur`
**Description :** Export des données auditeurs pour l'ADEME.

**Calculé dans :** [Export TET → Ademe > Audits](https://datalore.jetbrains.com/notebook/3z8wdKwizolR7wA321R4Rl/LhsccNs3HBiP4wnuv67kP7/)

---

#### `visite_annuelle`
**Description :** Export des visites annuelles pour l'ADEME.

**Calculé dans :** [Export TET → Ademe > Audits](https://datalore.jetbrains.com/notebook/3z8wdKwizolR7wA321R4Rl/LhsccNs3HBiP4wnuv67kP7/)

---

#### `cot`
**Description :** Export COT (Conseiller en Organisation Territoriale) pour l'ADEME.

**Calculé dans :** [Export TET → Ademe > Collectivités](https://datalore.jetbrains.com/notebook/3z8wdKwizolR7wA321R4Rl/LhsccNs3HBiP4wnuv67kP7/)

---

#### `Score_mesures`
**Description :** ⚠️ Attention à la casse (S majuscule) - Scores par mesure exportés vers l'ADEME.

**Calculé dans :** [Export TET → Ademe > Score mesures](https://datalore.jetbrains.com/notebook/3z8wdKwizolR7wA321R4Rl/LhsccNs3HBiP4wnuv67kP7/)

---

#### `score_snapshot`
**Description :** Snapshot des scores pour l'ADEME.

**Calculé dans :** [Export TET → Ademe > Score snapshot](https://datalore.jetbrains.com/notebook/3z8wdKwizolR7wA321R4Rl/LhsccNs3HBiP4wnuv67kP7/)

---

#### `utilisateurs`
**Description :** Export de la table utilisateurs pour l'ADEME.

**Calculé dans :** [Export TET → Ademe > Utilisateurs](https://datalore.jetbrains.com/notebook/3z8wdKwizolR7wA321R4Rl/LhsccNs3HBiP4wnuv67kP7/)

---

#### `utilisateurs_droits`
**Description :** Export des droits utilisateurs pour l'ADEME.

**Calculé dans :** [Export TET → Ademe > Utilisateurs](https://datalore.jetbrains.com/notebook/3z8wdKwizolR7wA321R4Rl/LhsccNs3HBiP4wnuv67kP7/)

---

### Synchro Airtable & stats bizdevs

#### `airtable_sync`
**Description :** Synchronisation quotidienne avec le CRM Airtable. Contient de nombreuses stats majeures par collectivité.

**Calculé dans :** [Airtable Sync > Envoi Airtable](https://datalore.jetbrains.com/notebook/3z8wdKwizolR7wA321R4Rl/D4qN6QMCVwFY39YFhLg3u2/)

---

#### `airtable_sync_semaine`
**Description :** Sauvegarde hebdomadaire de l'état de `airtable_sync`.

**Calculé dans :** [Airtable Sync > Envoi Airtable](https://datalore.jetbrains.com/notebook/3z8wdKwizolR7wA321R4Rl/D4qN6QMCVwFY39YFhLg3u2/)

---

#### `bizdev_A_F_contact`
**Description :** Contacts BizDev pour le tableau de bord commercial.

**Calculé dans :** [Airtable Sync > Airtable reach](https://datalore.jetbrains.com/notebook/3z8wdKwizolR7wA321R4Rl/D4qN6QMCVwFY39YFhLg3u2/)

---

#### `bizdev_note_de_suivi_contact`
**Description :** Notes de suivi des contacts BizDev.

**Calculé dans :** [Airtable Sync > Airtable reach](https://datalore.jetbrains.com/notebook/3z8wdKwizolR7wA321R4Rl/D4qN6QMCVwFY39YFhLg3u2/)

---

#### `bizdev_contact_collectivite`
**Description :** Mapping contacts BizDev ↔ collectivités.

**Calculé dans :** [Airtable Sync](https://datalore.jetbrains.com/notebook/3z8wdKwizolR7wA321R4Rl/D4qN6QMCVwFY39YFhLg3u2/)

---

#### `calendly_events`
**Description :** Événements Calendly pour le tableau de bord BizDev.

**Calculé dans :** [Airtable Sync > Calendly (events)](https://datalore.jetbrains.com/notebook/3z8wdKwizolR7wA321R4Rl/D4qN6QMCVwFY39YFhLg3u2/)

---

#### `calendly_invitees`
**Description :** Participants aux événements Calendly.

**Calculé dans :** [Airtable Sync > Calendly (invitees)](https://datalore.jetbrains.com/notebook/3z8wdKwizolR7wA321R4Rl/D4qN6QMCVwFY39YFhLg3u2/)

---

#### `evenements_airtable`
**Description :** Synchronisation événements Calendly → Airtable.

**Calculé dans :** [Airtable Sync > Calendly (events)](https://datalore.jetbrains.com/notebook/3z8wdKwizolR7wA321R4Rl/D4qN6QMCVwFY39YFhLg3u2/)

---

## 🔧 Tables Techniques & Versioning

#### `feature`
**Description :** Tracking des features mises en production (MEP).

**Calculé dans :** [MEPS](https://datalore.jetbrains.com/notebook/3z8wdKwizolR7wA321R4Rl/hyvTHBsHKmqrrcIzNm0UpY/) (tous les onglets alimentent cette table)
---

#### `indicateurs_od`
**Description :** Listing de tous les indicateurs disponibles en open data sur Territoires en Transitions.

**Calculé dans :** [Calcul PAP & Score > Indicateurs OD](https://datalore.jetbrains.com/notebook/3z8wdKwizolR7wA321R4Rl/TUsBeh2ErVoeFgtptt9A8g/)

#### `fiche_action_plan`
**Description :** Permet de faire le lien entre les id de fiche action (fiche_id) et les plans (plan)

**Calculé dans:** [Export TET → ADEME > fiche_action_plan](https://datalore.jetbrains.com/notebook/3z8wdKwizolR7wA321R4Rl/LhsccNs3HBiP4wnuv67kP7/)

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

**Calculé dans :** [Export TET → Ademe > Indicateurs](https://datalore.jetbrains.com/notebook/3z8wdKwizolR7wA321R4Rl/LhsccNs3HBiP4wnuv67kP7/)

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

---


## Colonnes de toutes les tables

Score_mesures: pointFait (double precision), nom (text), actionid (text), pointProgramme (double precision), type_jalon (text), siren (text), date_fin_audit (timestamp with time zone), referentiel_id (text), pointPasFait (double precision), pointPotentiel (double precision), nom_mesure (text), sujet (text), actionId (text), date (timestamp with time zone)
action_referentiel: exemples (text), action_id (text), referentiel (text), nom (text), type (text), depth (bigint)
activite_semaine: collectivite_id (double precision), email (text), semaine (text)
airtable_sync: nb_indicateur_perso (bigint), nb_fiches_modifiees_12_mois (bigint), pap_multiplan_12_mois (text), collectivite_id (bigint), nb_contributeurs (bigint), pap_multiplan_3_mois (text), pap_12_mois (text), nb_fa_pilotables (bigint), nb_pap (bigint), derniere_creation_compte (text), derniere_visite (text), nb_fa (bigint), ct_tete (double precision), owner_plan (text), key (text), pap_3_mois (text), pipeline (text), type (text), semaine_passage_retention (text), nb_fiches_modifiees_6_mois (bigint), pageviews_plan (bigint), nb_super_contributeurs (bigint), nombre_pap_bizdev (double precision), semaine (text), plans_type (text), url_plan (text), note_plan (double precision), user_derniere_visite (text), user_derniere_creation_compte (text), nb_fiches_modifiees_3_mois (bigint), derniere_modif (text), top_contributeur (text), passage_pap (text), activite_depuis_pap (bigint)
airtable_sync_semaine: note_max_pap (double precision), derniere_creation_compte (text), score_referentiel (double precision), nb_fa (bigint), semaine (text), derniere_visite (text), score_indicateur (double precision), score (double precision), nb_super_contributeurs (bigint), activite_depuis_pap (bigint), top_contributeur (text), nb_pap (bigint), score_budget (double precision), passage_pap (text), score_avancement (double precision), pipeline (text), key (text), pageviews_plan (bigint), owner_plan (text), nb_fa_pilotables (bigint), nb_indicateur_perso (bigint), plans_type (text), derniere_modif (text), score_pilotabilite (double precision), nb_contribution (bigint), collectivite_id (bigint), nb_contributeurs (bigint), ct_tete (double precision), score_objectif (double precision), statut (text)
audit: date_cnl (timestamp with time zone), type (text), audit_id (bigint), valide_labellisation (boolean), clos (boolean), collectivite_id (bigint), audit_fin (timestamp with time zone), date_demande (timestamp with time zone), referentiel (text), audit_debut (timestamp with time zone), audit_valide (boolean)
auditeur: nom_auditeur (text), user_id (text), date_attribution (timestamp with time zone), prenom_auditeur (text), email_auditeur (text), audit_id (bigint)
bizdev_A_F_contact: echange_type (text), date (text), collectivite_id (double precision)
bizdev_contact_collectivite: date_contact (timestamp without time zone), collectivite_id (bigint)
bizdev_note_de_suivi_contact: collectivite_id (bigint), date (timestamp without time zone)
calendly_events: status (text), name (text), uri (text), nb_participants_reel (bigint), start_time (text), event_type (text)
calendly_invitees: email (text), status (text), uri_event (text), reponse (text)
collectivite: region_code (text), region_iso_3166 (text), completude_eci (double precision), region_name (text), date_activation_tet (timestamp without time zone), code_siren_insee (text), nom (text), departement_code (text), collectivite_id (bigint), departement_iso_3166 (text), type_collectivite (text), completude_cae (double precision), departement_name (text), activee (boolean), population_totale (bigint), pa_pilotables (double precision), nature_collectivite (text)
cot: signataire (bigint), collectivite_id (bigint), actif (boolean)
ct_actives: type (text), date_activation (timestamp with time zone), region_name (text), collectivite_id (bigint), departement_name (text), nom (text), categorie (text), nature_insee (text), siren (text)
evenements_airtable: evenements (text), index (bigint), Date (timestamp without time zone)
evolution_ind_od: nb_values_od_cum (double precision), departement_name (text), region_name (text), mois (text)
evolution_ind_pers: nb_lignes (double precision), nb_ind_perso_ct (double precision), mois (text), nb_ind_perso (double precision), region_name (text), departement_name (text)
evolution_labellisation: nb_labellisation_cumule (bigint), mois (timestamp without time zone)
fa_distrib: action_pilotable_actives (double precision), departement_name (text), nb_fiches (double precision), realise (double precision), action_pilotable (double precision), region_name (text), mois (timestamp without time zone), action (bigint)
fa_sharing: mois (timestamp without time zone), nb_fa_shared (bigint)
feature: email (text), collectivite_id (bigint), datetime (timestamp with time zone), sub-feature (json), feature (text)
fiche_action_plan: plan (bigint), fiche_id (bigint)
ind_od_producteur_indicateur: departement_name (text), producteur (text), region_name (text), titre (text)
indicateur_definition: indicateur_specifique (text), titre_long (text), id (bigint), titre (text), unite (text), identifiant_referentiel (text), description (text)
indicateurs_od: titre (text), unite (text), sources_libelle (text), types_collectivite (text), identifiant_referentiel (text), thematique (text)
indicateurs_valeurs_olap: resultat (double precision), metadonnee_id (bigint), api_nom_cube (text), indicateur_id (bigint), date_valeur (timestamp without time zone), collectivite_id (double precision), identifiant_referentiel (text)
internal_users: email (text)
labellisation: points_potentiels (double precision), score_programme (double precision), referentiel (text), score_realise (double precision), obtenue_le (timestamp without time zone), collectivite_id (bigint), etoiles (bigint)
labellisation_region: obtenue_le (timestamp without time zone), collectivite_id (bigint), referentiel (text), region_name (text), etoiles (bigint), departement_name (text)
labellisation_stock_evolution: region_name (text), referentiel (text), departement_name (text), year (bigint), etoiles (bigint), nb_collectivites (bigint)
mapping_levier_mesure: levier (text), mesure (text)
modelisation_impact: Secteur (text), reduction (double precision), justification (text), Leviers SGPE (text), implication (double precision), ids (text), created_at (timestamp without time zone), identifiant_referentiel (text), reduction_leveir (double precision), reduction_theorique (double precision), collectivite_id (bigint)
nb_fap_13: statut (text), mois (text), fiche_id (bigint)
nb_fap_52: statut (text), mois (text), fiche_id (bigint)
nb_fap_pilote_13: mois (text), statut (text), fiche_id (bigint)
nb_fap_pilote_52: fiche_id (bigint), mois (text), statut (text)
note_fiche_historique: score_budget (bigint), fiche_id (bigint), nom_ct (text), score_date_debut (double precision), score_pilote_user (double precision), score_description (bigint), score_indicateur (bigint), note_fa (double precision), score_statut (bigint), score_suivi (bigint), score_titre (bigint), score_pilote (double precision), collectivite_id (bigint), mois (text), score_date_fin (double precision), score_objectif (double precision), score_modif_12_mois (double precision), score_modif_6_mois (double precision)
note_fiche_historique_backup: score_budget (bigint), fiche_id (bigint), score_modif_12_mois (double precision), note_fa (double precision), score_date_fin (double precision), score_date_debut (double precision), mois (text), score_objectif (double precision), score_description (bigint), score_titre (bigint), score_suivi (bigint), score_statut (bigint), nom_ct (text), score_pilote_user (double precision), collectivite_id (bigint), score_indicateur (bigint), score_modif_6_mois (double precision), score_pilote (double precision)
note_plan_historique: note_plan (double precision), mois (text), plan (bigint)
note_plan_historique_backup: mois (text), plan (bigint), note_plan (double precision)
nps: nps (double precision)
pap_date_passage: passage_pap (timestamp with time zone), nom_plan (text), import (text), collectivite_id (bigint), nom (text), type (double precision), plan (bigint), nom_plan_ct (text)
pap_note: collectivite_id (bigint), nom (text), semaine (text), nom_ct (text), plan_id (bigint), score_pilotabilite (double precision), c_referentiel (double precision), score_objectif (double precision), score_indicateur (double precision), score (double precision), score_referentiel (double precision), etoiles_visuelles (text), key (text), type (double precision), score_avancement (double precision), score_budget (double precision), nb_fiche_action_total (bigint)
pap_note_backup: score_objectif (double precision), score (double precision), score_avancement (double precision), collectivite_id (bigint), score_budget (double precision), c_referentiel (double precision), score_referentiel (double precision), score_indicateur (double precision), nom_ct (text), plan_id (bigint), semaine (text), score_pilotabilite (double precision), key (text), nom (text), nb_fiche_action_total (bigint), type (double precision), etoiles_visuelles (text)
pap_note_region: collectivite_id (bigint), nom (text), score (double precision), plan_id (bigint), departement_name (text), region_name (text), nom_plan (text), semaine (text)
pap_note_snapshot: collectivite_id (bigint), semaine (text), etoiles_visuelles (text), score_objectif (double precision), plan_id (bigint), c_referentiel (double precision), nom_ct (text), score_indicateur (double precision), score_avancement (double precision), nom (text), score_pilotabilite (double precision), score (double precision), key (text), type (double precision), score_budget (double precision), score_referentiel (double precision), nb_fiche_action_total (bigint)
pap_statut_5_fiches_modifiees_13_semaines: statut (text), plan (bigint), collectivite_id (bigint), nb_pilotes (bigint), mois (timestamp without time zone)
pap_statut_5_fiches_modifiees_52_semaines: nom_plan (text), mois (timestamp without time zone), statut (text), plan (bigint), collectivite_id (bigint), nb_pilotes (bigint)
passage_pap_region: collectivite_id (bigint), plan (bigint), region_name (text), mois (text), departement_name (text), nom_plan (text)
pipeline: pipeline (text), collectivite_id (bigint), semaine (text)
plan_distrib: departement_name (text), pilotable (boolean), plan (bigint), region_name (text), actif_12_mois (boolean), score_sup_5 (boolean)
score_snapshot: point_fait (double precision), sujet (text), referentiel_id (text), point_programme (double precision), date (timestamp with time zone), date_fin_audit (timestamp with time zone), siren (text), nom (text), point_potentiel (double precision), point_pas_fait (double precision), etoiles (bigint), type_jalon (text)
stats_hero_section_site: nb_pap_actif_12_mois (bigint), nb_user_actif_12_mois (bigint), nb_ct_actif_12_mois (bigint), nb_action_pilotable_active_12_mois (bigint)
statut_fiche_13_semaines: mois (text), fiche_id (bigint), statut (text)
statut_fiche_52_semaines: mois (text), statut (text), fiche_id (bigint)
tmp_backup_indicateur_source_metadonnee: diffuseur (text), source_id (text), nom_donnees (text), limites (text), methodologie (text), id (bigint), date_version (timestamp without time zone), producteur (text)
tmp_backup_indicateur_valeur: metadonnee_id (bigint), collectivite_id (bigint), indicateur_id (bigint), objectif (text), estimation (text), created_at (timestamp with time zone), calcul_auto_identifiants_manquants (text), created_by (text), calcul_auto (boolean), resultat_commentaire (text), resultat (double precision), id (bigint), objectif_commentaire (text), modified_by (text), date_valeur (timestamp without time zone), modified_at (timestamp with time zone)
tr_comm: cd_comm (text), cd_sirn_comm (double precision), lb_comm_majs (text), id_tech_comm (bigint)
user_actif_12_mois: collectivite_id (double precision), email (text), mois (timestamp without time zone)
user_actifs_ct_mois: collectivite_id (bigint), email (text), region_name (text), mois (text), departement_name (text)
utilisateurs: email (text), prenom (text), user_id (text), telephone (text), nom (text)
utilisateurs_droits: niveau_acces (text), fonction (text), date_creation (timestamp with time zone), details_fonction (text), champ_intervention (text), invitation (boolean), user_id (text), collectivite_id (bigint), est_referent (boolean)
visite_annuelle: collectivite_id (bigint), derniere_date (timestamp with time zone)

## Aperçu de certaines colonnes

Voici le contenu de certaines colonnes quand on fait un `select distinct`.

ct_actives.categorie : ['Syndicats', None, 'Communes', 'Départements', 'Régions', 'EPCI']
ct_activtes.type : ['region', 'departement', 'epci', 'service_public', 'commune', 'prefecture_region']
ct_actives.nature_insee : ['epci', 'POLEM', 'CA', 'commune', 'SMO', 'CC', 'CU', 'PETR', 'region', 'departement', 'EPT', 'prefecture_region', 'SIVOM', 'service_public', 'SIVU', 'METRO', 'SMF']

airtable_sync.pipeline : 
['En pilotage (à surveiller)',
 'En conversion',
 'En pilotage',
 'A acquérir',
 'En pilotage multiplans',
 'A réactiver',
 'En rétention (à surveiller)',
 'En test (+6 mois)',
 'En test (-6 mois)',
 'En rétention',
 'En activation',
 'En conversion actif']

## 📖 Glossaire

| Terme | Définition |
|-------|------------|
| **PAP** | Plan d'Action Pilotable - Un plan d'action qui a au moins 5 fiches avec un titre, un statut, une personne ou service/direction pilote |
| **PAP actif 13/52 semaines** | Un plan d'action pilotable qui a eu au moins 5 fiches modifiées au cours des 13/52 dernières semaines |
| **FAP** | Fiche Action Pilotable - Une fiche action qui a au moins un titre, un statut et une personne ou service/direction pilote |
| **BE** | Bureau d'Études (partenaire en back sur l'app) |
| **CT** | Collectivité |
| **OD** | Open Data (indicateurs) |
| **CAE** | Climat-Air-Énergie (référentiel de labellisation) |
| **ECI** | Économie Circulaire (référentiel de labellisation) |
| **COT** | Contrat d'Objectif Territoriale |
| **North Star** | Métrique principale de succès de Territoires en Transitions |

---

## 🎯 Cas d'Usage Fréquents

### "Je veux uniquement les collectivités PAP"
```sql
SELECT DISTINCT collectivite_id 
FROM pap_date_passage
```

### "Quelles sont les collectivités actives sur les 3 derniers mois"
```sql
SELECT distinct collectivite_id 
FROM activite_semaine
WHERE TO_DATE(semaine, 'YYYY-MM-DD') >= CURRENT_DATE - INTERVAL '3 months';
```

### "Niveau de labellisation actuel des collectivités sur le référentiel cae"
```sql
select collectivite_id, max(etoiles)
from labellisation l 
where referentiel ='cae'
group by collectivite_id 
```

### "PAP actifs 52 semaines (North Star publique)"
```sql
SELECT * FROM pap_statut_5_fiches_modifiees_52_semaines 
where mois= (select max(mois) from pap_statut_5_fiches_modifiees_52_semaines) 
and statut = 'actif'
```

---

## ⚠️ Notes Importantes

1. **Filtrage systématique** : Toutes les stats excluent par défaut les utilisateurs internes et collectivités tests
2. **Casse importante** : `Score_mesures` (avec S majuscule)
