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

Score_mesures: pointFait (double precision), date_fin_audit (timestamp with time zone), siren (text), nom_mesure (text), nom (text), date (timestamp with time zone), sujet (text), actionId (text), pointProgramme (double precision), pointPasFait (double precision), actionid (text), referentiel_id (text), type_jalon (text), pointPotentiel (double precision)
action_referentiel: action_id (text), type (text), referentiel (text), depth (bigint), nom (text), exemples (text)
activite_semaine: email (text), collectivite_id (double precision), semaine (text)
airtable_sync: url_plan (text), semaine (text), user_derniere_visite (text), collectivite_id (bigint), nb_fiches_modifiees_12_mois (bigint), nb_fiches_modifiees_3_mois (bigint), derniere_creation_compte (text), nb_fa_pilotables (bigint), key (text), nb_fiches_modifiees_6_mois (bigint), nb_super_contributeurs (bigint), owner_plan (text), semaine_passage_retention (text), plans_type (text), nb_indicateur_perso (bigint), activite_depuis_pap (bigint), nombre_pap_bizdev (double precision), user_derniere_creation_compte (text), derniere_modif (text), nb_contributeurs (bigint), passage_pap (text), pap_3_mois (text), pipeline (text), nb_fa (bigint), top_contributeur (text), note_plan (double precision), derniere_visite (text), pap_multiplan_12_mois (text), type (text), pageviews_plan (bigint), ct_tete (double precision), pap_12_mois (text), nb_pap (bigint), pap_multiplan_3_mois (text)
airtable_sync_semaine: semaine (text), pipeline (text), semaine_passage_retention (text), collectivite_id (bigint)
airtable_sync_semaine_old: score (double precision), plans_type (text), nb_contribution (bigint), ct_tete (double precision), nb_super_contributeurs (bigint), activite_depuis_pap (bigint), collectivite_id (bigint), score_avancement (double precision), nb_contributeurs (bigint), owner_plan (text), nb_pap (bigint), note_max_pap (double precision), top_contributeur (text), pipeline (text), pageviews_plan (bigint), passage_pap (text), score_objectif (double precision), score_indicateur (double precision), derniere_modif (text), score_budget (double precision), statut (text), key (text), derniere_creation_compte (text), nb_indicateur_perso (bigint), score_referentiel (double precision), semaine (text), derniere_visite (text), score_pilotabilite (double precision), nb_fa_pilotables (bigint), nb_fa (bigint)
audit: audit_fin (timestamp with time zone), valide_labellisation (boolean), date_demande (timestamp with time zone), clos (boolean), audit_id (bigint), type (text), collectivite_id (bigint), audit_debut (timestamp with time zone), date_cnl (timestamp with time zone), referentiel (text), audit_valide (boolean)
auditeur: email_auditeur (text), user_id (text), prenom_auditeur (text), date_attribution (timestamp with time zone), nom_auditeur (text), audit_id (bigint)
bizdev_A_F_contact: collectivite_id (double precision), echange_type (text), date (text)
bizdev_contact_collectivite: date_contact (timestamp without time zone), collectivite_id (bigint)
bizdev_note_de_suivi_contact: date (timestamp without time zone), collectivite_id (bigint)
calendly_events: event_type (text), nb_participants_reel (bigint), status (text), name (text), start_time (text), uri (text)
calendly_invitees: reponse (text), email (text), uri_event (text), status (text)
collectivite: departement_name (text), type_collectivite (text), region_name (text), population_totale (bigint), completude_eci (double precision), region_code (text), pa_pilotables (double precision), region_iso_3166 (text), nom (text), nature_collectivite (text), completude_cae (double precision), date_activation_tet (timestamp without time zone), departement_code (text), collectivite_id (bigint), code_siren_insee (text), departement_iso_3166 (text), activee (boolean)
cot: signataire (bigint), actif (boolean), collectivite_id (bigint)
crisp_conversation: updated_at (timestamp with time zone), nickname (text), segments (text), session_id (text), email (text), operator (character varying), created_at (timestamp with time zone)
crisp_rating: hits (bigint), unique_hits (bigint), rating (double precision), mois (timestamp without time zone)
crisp_temps_reponse: mois (timestamp without time zone), hits (bigint), unique_hits (bigint), response_time_h (double precision)
crisp_temps_resoluton: unique_hits (bigint), hits (bigint), mois (timestamp without time zone), temps_resolution_h (double precision)
ct_actives: categorie (text), siren (text), nature_insee (text), type (text), region_name (text), departement_name (text), collectivite_id (bigint), date_activation (timestamp with time zone), nom (text)
evenements_airtable: Date (timestamp without time zone), evenements (text), index (bigint)
evolution_ind_od: departement_name (text), nb_values_od_cum (double precision), mois (text), region_name (text)
evolution_ind_pers: nb_ind_perso (double precision), mois (text), nb_lignes (double precision), region_name (text), departement_name (text), nb_ind_perso_ct (double precision)
evolution_labellisation: nb_labellisation_cumule (bigint), mois (timestamp without time zone)
fa_distrib: action_pilotable (double precision), departement_name (text), mois (timestamp without time zone), realise (double precision), region_name (text), action (bigint), action_pilotable_actives (double precision), nb_fiches (double precision)
fa_sharing: nb_fa_shared (bigint), mois (timestamp without time zone)
feature: collectivite_id (bigint), sub-feature (json), feature (text), datetime (timestamp with time zone), email (text)
fiche_action_plan: plan (bigint), fiche_id (bigint)
ind_od_producteur_indicateur: region_name (text), producteur (text), titre (text), departement_name (text)
indicateur_definition: identifiant_referentiel (text), id (bigint), titre_long (text), description (text), titre (text), unite (text), indicateur_specifique (text)
indicateurs_od: titre (text), thematique (text), types_collectivite (text), identifiant_referentiel (text), sources_libelle (text), unite (text)
indicateurs_valeurs_olap: resultat (double precision), identifiant_referentiel (text), indicateur_id (bigint), collectivite_id (double precision), date_valeur (timestamp without time zone), metadonnee_id (bigint), api_nom_cube (text)
internal_users: email (text)
labellisation: points_potentiels (double precision), obtenue_le (timestamp without time zone), score_realise (double precision), referentiel (text), score_programme (double precision), etoiles (bigint), collectivite_id (bigint)
labellisation_region: collectivite_id (bigint), departement_name (text), region_name (text), etoiles (bigint), referentiel (text), obtenue_le (timestamp without time zone)
labellisation_stock_evolution: nb_collectivites (bigint), year (bigint), etoiles (bigint), region_name (text), referentiel (text), departement_name (text)
mapping_levier_mesure: levier (text), mesure (text)
modelisation_impact: reduction_leveir (double precision), Secteur (text), justification (text), collectivite_id (bigint), Leviers SGPE (text), implication (double precision), ids (text), created_at (timestamp without time zone), identifiant_referentiel (text), reduction (double precision), reduction_theorique (double precision)
nb_fap_13: fiche_id (bigint), statut (text), mois (text)
nb_fap_52: mois (text), statut (text), fiche_id (bigint)
nb_fap_pilote_13: fiche_id (bigint), mois (text), statut (text)
nb_fap_pilote_52: fiche_id (bigint), mois (text), statut (text)
note_fiche_historique: nom_ct (text), score_objectif (double precision), score_description (bigint), score_budget (bigint), score_indicateur (bigint), score_suivi (bigint), score_modif_12_mois (double precision), score_pilote_user (double precision), score_titre (bigint), score_date_debut (double precision), score_date_fin (double precision), score_statut (bigint), fiche_id (bigint), collectivite_id (bigint), mois (text), score_pilote (double precision), note_fa (double precision), score_modif_6_mois (double precision)
note_fiche_historique_backup: fiche_id (bigint), score_suivi (bigint), score_description (bigint), score_pilote_user (double precision), note_fa (double precision), score_objectif (double precision), score_modif_6_mois (double precision), score_date_fin (double precision), score_budget (bigint), score_titre (bigint), score_date_debut (double precision), score_modif_12_mois (double precision), score_statut (bigint), nom_ct (text), collectivite_id (bigint), score_indicateur (bigint), score_pilote (double precision), mois (text)
note_plan_historique: mois (text), note_plan (double precision), plan (bigint)
note_plan_historique_backup: mois (text), plan (bigint), note_plan (double precision)
note_plan_semaine: note_plan (numeric), semaine (date), plan (text)
nps: nps (double precision)
pap_date_passage: nom_plan (text), nom_plan_ct (text), createur_plan (text), collectivite_id (bigint), type (double precision), plan (bigint), passage_pap (timestamp with time zone), nom (text), import (text)
pap_note: c_referentiel (double precision), plan_id (bigint), score_budget (double precision), semaine (text), nom (text), etoiles_visuelles (text), score_indicateur (double precision), score (double precision), nom_ct (text), type (double precision), score_pilotabilite (double precision), score_referentiel (double precision), score_objectif (double precision), key (text), nb_fiche_action_total (bigint), collectivite_id (bigint), score_avancement (double precision)
pap_note_backup: type (double precision), score_objectif (double precision), c_referentiel (double precision), score_pilotabilite (double precision), nom (text), score (double precision), key (text), nom_ct (text), score_budget (double precision), nb_fiche_action_total (bigint), score_referentiel (double precision), semaine (text), score_indicateur (double precision), score_avancement (double precision), collectivite_id (bigint), etoiles_visuelles (text), plan_id (bigint)
pap_note_region: departement_name (text), semaine (text), score (double precision), plan_id (bigint), nom_plan (text), collectivite_id (bigint), nom (text), region_name (text)
pap_note_snapshot: score_pilotabilite (double precision), score_indicateur (double precision), score_avancement (double precision), key (text), collectivite_id (bigint), nb_fiche_action_total (bigint), nom_ct (text), score_budget (double precision), semaine (text), score_objectif (double precision), etoiles_visuelles (text), plan_id (bigint), score (double precision), score_referentiel (double precision), type (double precision), c_referentiel (double precision), nom (text)
pap_statut_5_fiches_modifiees_13_semaines: mois (timestamp without time zone), plan (bigint), statut (text), nb_pilotes (bigint), collectivite_id (bigint)
pap_statut_5_fiches_modifiees_52_semaines: mois (timestamp without time zone), collectivite_id (bigint), nom_plan (text), plan (bigint), statut (text), nb_pilotes (bigint)
passage_pap_region: departement_name (text), collectivite_id (bigint), region_name (text), nom_plan (text), plan (bigint), mois (text)
pipeline: pipeline (text), collectivite_id (bigint), semaine (text)
plan_distrib: actif_12_mois (boolean), plan (bigint), region_name (text), departement_name (text), score_sup_5 (boolean), pilotable (boolean)
priorisation: id (bigint), note (smallint), identifiant_referentiel (text), secteur (text), categorie (smallint), collectivite_id (bigint), levier (text), created_at (timestamp with time zone), ids (text)
priorisation_action: collectivite_id (integer), fiche_action_id (integer), created_at (timestamp with time zone), id (integer), categorie (integer), levier (text)
priorisation_categorie_levier: Changement chaudières gaz + rénovation (résidentiel) (double precision), Gestion des prairies (double precision), Covoiturage (double precision), Changement de chaudière à gaz (tertiaire) (double precision), Changement chaudières fioul + rénovation (résidentiel) (double precision), Sobriété foncière (double precision), Efficacité et carburants décarbonés des véhicules privés (double precision), Sobriété et isolation des bâtiments (tertiaire) (double precision), Changements de pratiques de fertilisation azotée (double precision), Sobriété des bâtiments (résidentiel) (double precision), Production Industrielle (double precision), Elevage durable (double precision), Captage de méthane dans les ISDND (double precision), Véhicules électriques (double precision), Prévention des déchets (double precision), Bus et cars décarbonés (double precision), Réduction des déplacements (double precision), Valorisation matière des déchets (double precision), categorie (bigint), Réseaux de chaleur décarbonés (double precision), Bâtiments & Machines agricoles (double precision), Changement de chaudière à fioul (tertiaire) (double precision), Efficacité et sobriété logistique (double precision), Biogaz (double precision), Fret décarboné et multimodalité (double precision), Gestion des forêts et produits bois (double precision), Electricité renouvelable (double precision), Gestion des haies (double precision), Vélo et transport en commun (double precision), Pratiques stockantes (double precision)
priorisation_faisabilite: collectivite_id (integer), created_at (timestamp with time zone), faisabilite (integer), levier (text), categorie (integer), id (integer)
priorisation_hors_competence: categorie (integer), created_at (timestamp with time zone), id (integer), levier (text), collectivite_id (integer)
priorisation_reduction_levier: reduction (double precision), levier (text), created_at (timestamp without time zone), id (integer), collectivite_id (integer)
score_snapshot: siren (text), sujet (text), point_programme (double precision), point_fait (double precision), type_jalon (text), nom (text), date_fin_audit (timestamp with time zone), referentiel_id (text), date (timestamp with time zone), etoiles (bigint), point_pas_fait (double precision), point_potentiel (double precision)
stats_hero_section_site: nb_ct_actif_12_mois (bigint), nb_pap_actif_12_mois (bigint), nb_user_actif_12_mois (bigint), nb_action_pilotable_active_12_mois (bigint)
statut_fiche_13_semaines: fiche_id (bigint), statut (text), mois (text)
statut_fiche_52_semaines: statut (text), mois (text), fiche_id (bigint)
taux_contact_support: taux_support_bug_% (double precision), month (timestamp without time zone)
tmp_backup_indicateur_source_metadonnee: source_id (text), producteur (text), id (bigint), limites (text), nom_donnees (text), diffuseur (text), date_version (timestamp without time zone), methodologie (text)
tmp_backup_indicateur_valeur: objectif (text), resultat (double precision), metadonnee_id (bigint), modified_by (text), created_by (text), objectif_commentaire (text), collectivite_id (bigint), date_valeur (timestamp without time zone), resultat_commentaire (text), calcul_auto (boolean), id (bigint), estimation (text), calcul_auto_identifiants_manquants (text), indicateur_id (bigint), modified_at (timestamp with time zone), created_at (timestamp with time zone)
tr_comm: cd_comm (text), lb_comm_majs (text), id_tech_comm (bigint), cd_sirn_comm (double precision)
user_actif_12_mois: collectivite_id (double precision), mois (timestamp without time zone), email (text)
user_actifs_ct_mois: departement_name (text), region_name (text), email (text), collectivite_id (bigint), mois (text)
utilisateurs: prenom (text), email (text), nom (text), user_id (text), telephone (text)
utilisateurs_droits: invitation (boolean), niveau_acces (text), user_id (text), fonction (text), details_fonction (text), est_referent (boolean), date_creation (timestamp with time zone), collectivite_id (bigint), champ_intervention (text)
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
