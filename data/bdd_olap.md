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

Score_mesures: type_jalon (text), siren (text), pointProgramme (double precision), date_fin_audit (timestamp with time zone), pointFait (double precision), pointPotentiel (double precision), pointPasFait (double precision), referentiel_id (text), nom (text), actionid (text), sujet (text), nom_mesure (text), actionId (text), date (timestamp with time zone)
action_referentiel: depth (bigint), nom (text), action_id (text), type (text), exemples (text), referentiel (text)
activite_semaine: collectivite_id (double precision), semaine (text), email (text)
airtable_sync: nb_super_contributeurs (bigint), top_contributeur (text), nb_fiches_modifiees_3_mois (bigint), nb_fa (bigint), pipeline (text), pap_multiplan_3_mois (text), derniere_visite (text), pap_3_mois (text), note_plan (double precision), pap_12_mois (text), url_plan (text), passage_pap (text), pageviews_plan (bigint), semaine (text), semaine_passage_retention (text), pap_multiplan_12_mois (text), plans_type (text), derniere_modif (text), user_derniere_visite (text), ct_tete (double precision), nb_indicateur_perso (bigint), collectivite_id (bigint), nb_fiches_modifiees_6_mois (bigint), key (text), nb_pap (bigint), nb_fiches_modifiees_12_mois (bigint), type (text), nombre_pap_bizdev (double precision), nb_contributeurs (bigint), activite_depuis_pap (bigint), owner_plan (text), user_derniere_creation_compte (text), nb_fa_pilotables (bigint), derniere_creation_compte (text)
airtable_sync_semaine: collectivite_id (bigint), semaine (text), semaine_passage_retention (text), pipeline (text)
airtable_sync_semaine_old: nb_indicateur_perso (bigint), pipeline (text), score_referentiel (double precision), collectivite_id (bigint), ct_tete (double precision), nb_fa (bigint), derniere_creation_compte (text), statut (text), score_objectif (double precision), nb_contributeurs (bigint), score_indicateur (double precision), semaine (text), nb_contribution (bigint), score (double precision), derniere_visite (text), activite_depuis_pap (bigint), top_contributeur (text), score_pilotabilite (double precision), nb_pap (bigint), score_budget (double precision), nb_super_contributeurs (bigint), derniere_modif (text), passage_pap (text), note_max_pap (double precision), score_avancement (double precision), key (text), pageviews_plan (bigint), owner_plan (text), plans_type (text), nb_fa_pilotables (bigint)
audit: audit_valide (boolean), audit_id (bigint), date_cnl (timestamp with time zone), type (text), date_demande (timestamp with time zone), collectivite_id (bigint), audit_debut (timestamp with time zone), referentiel (text), audit_fin (timestamp with time zone), valide_labellisation (boolean), clos (boolean)
auditeur: audit_id (bigint), date_attribution (timestamp with time zone), prenom_auditeur (text), user_id (text), nom_auditeur (text), email_auditeur (text)
bizdev_A_F_contact: collectivite_id (double precision), date (text), echange_type (text)
bizdev_contact_collectivite: collectivite_id (bigint), date_contact (timestamp without time zone)
bizdev_note_de_suivi_contact: date (timestamp without time zone), collectivite_id (bigint)
calendly_events: event_type (text), status (text), nb_participants_reel (bigint), start_time (text), uri (text), name (text)
calendly_invitees: email (text), uri_event (text), status (text), reponse (text)
collectivite: region_name (text), collectivite_id (bigint), code_siren_insee (text), type_collectivite (text), completude_cae (double precision), pa_pilotables (double precision), departement_name (text), nom (text), population_totale (bigint), region_iso_3166 (text), activee (boolean), completude_eci (double precision), departement_code (text), nature_collectivite (text), departement_iso_3166 (text), region_code (text), date_activation_tet (timestamp without time zone)
cot: signataire (bigint), collectivite_id (bigint), actif (boolean)
crisp_conversation: created_at (timestamp with time zone), email (text), session_id (text), operator (character varying), updated_at (timestamp with time zone), segments (text), nickname (text)
crisp_nb_conversation: mois (timestamp without time zone), nb_conversation (bigint)
crisp_nb_message: nb_messages_operator (bigint), mois (timestamp without time zone), unique_hits (bigint), hits (bigint)
crisp_rating: hits (bigint), mois (timestamp without time zone), rating (double precision), unique_hits (bigint)
crisp_temps_reponse: unique_hits (bigint), response_time_h (double precision), mois (timestamp without time zone), hits (bigint)
crisp_temps_resoluton: mois (timestamp without time zone), temps_resolution_h (double precision), unique_hits (bigint), hits (bigint)
ct_actives: departement_name (text), siren (text), categorie (text), nom (text), region_name (text), nature_insee (text), type (text), date_activation (timestamp with time zone), collectivite_id (bigint)
evenements_airtable: Date (timestamp without time zone), evenements (text), index (bigint)
evolution_ind_od: mois (text), region_name (text), nb_values_od_cum (double precision), departement_name (text)
evolution_ind_pers: mois (text), nb_ind_perso_ct (double precision), region_name (text), nb_ind_perso (double precision), nb_lignes (double precision), departement_name (text)
evolution_labellisation: nb_labellisation_cumule (bigint), mois (timestamp without time zone)
fa_distrib: nb_fiches (double precision), region_name (text), action (bigint), action_pilotable_actives (double precision), realise (double precision), mois (timestamp without time zone), departement_name (text), action_pilotable (double precision)
fa_sharing: nb_fa_shared (bigint), mois (timestamp without time zone)
feature: email (text), datetime (timestamp with time zone), collectivite_id (bigint), sub-feature (json), feature (text)
fiche_action_plan: plan (bigint), fiche_id (bigint)
ind_od_producteur_indicateur: departement_name (text), producteur (text), titre (text), region_name (text)
indicateur_definition: id (bigint), indicateur_specifique (text), titre_long (text), identifiant_referentiel (text), description (text), unite (text), titre (text)
indicateurs_od: types_collectivite (text), identifiant_referentiel (text), thematique (text), sources_libelle (text), unite (text), titre (text)
indicateurs_valeurs_olap: collectivite_id (double precision), identifiant_referentiel (text), api_nom_cube (text), resultat (double precision), metadonnee_id (bigint), date_valeur (timestamp without time zone), indicateur_id (bigint)
internal_users: email (text)
labellisation: score_realise (double precision), obtenue_le (timestamp without time zone), score_programme (double precision), referentiel (text), points_potentiels (double precision), etoiles (bigint), collectivite_id (bigint)
labellisation_region: departement_name (text), referentiel (text), region_name (text), collectivite_id (bigint), etoiles (bigint), obtenue_le (timestamp without time zone)
labellisation_stock_evolution: etoiles (bigint), region_name (text), departement_name (text), year (bigint), nb_collectivites (bigint), referentiel (text)
mapping_levier_mesure: mesure (text), levier (text)
modelisation_impact: implication (double precision), justification (text), reduction_leveir (double precision), identifiant_referentiel (text), Secteur (text), reduction_theorique (double precision), Leviers SGPE (text), created_at (timestamp without time zone), ids (text), collectivite_id (bigint), reduction (double precision)
nb_fap_13: statut (text), mois (text), fiche_id (bigint)
nb_fap_52: mois (text), statut (text), fiche_id (bigint)
nb_fap_pilote_13: statut (text), mois (text), fiche_id (bigint)
nb_fap_pilote_52: mois (text), statut (text), fiche_id (bigint)
note_fiche_historique: score_objectif (double precision), score_date_debut (double precision), mois (text), fiche_id (bigint), score_pilote (double precision), score_statut (bigint), nom_ct (text), score_titre (bigint), score_indicateur (bigint), collectivite_id (bigint), score_modif_12_mois (double precision), score_pilote_user (double precision), score_date_fin (double precision), score_suivi (bigint), note_fa (double precision), score_modif_6_mois (double precision), score_description (bigint), score_budget (bigint)
note_fiche_historique_backup: score_modif_6_mois (double precision), note_fa (double precision), score_modif_12_mois (double precision), score_pilote_user (double precision), nom_ct (text), score_objectif (double precision), score_titre (bigint), fiche_id (bigint), score_indicateur (bigint), score_description (bigint), score_date_debut (double precision), score_date_fin (double precision), mois (text), score_budget (bigint), collectivite_id (bigint), score_statut (bigint), score_pilote (double precision), score_suivi (bigint)
note_plan_historique: note_plan (double precision), plan (bigint), mois (text)
note_plan_historique_backup: plan (bigint), note_plan (double precision), mois (text)
note_plan_semaine: plan (text), note_plan (numeric), semaine (date)
notion_ticket: criticite (text), url (text), email_utilisateur (text), titre (text), feedback (text), statut (text), createur_id (text), personnes_associees (text), type_bug_support (text), id_ticket (text), date_remontee_crisp (text), thematique (text), responsable (text), last_edited_at (text), tickets_lies (text), created_at (text), temps_resolution (double precision), bloque (text), epic_name (text), impact_potentiel (text), id_collectivite (double precision)
nps: nps (double precision)
pap_date_passage: import (text), nom_plan_ct (text), passage_pap (timestamp with time zone), nom (text), createur_plan (text), type (double precision), collectivite_id (bigint), nom_plan (text), plan (bigint)
pap_note: semaine (text), nom_ct (text), score_pilotabilite (double precision), score_avancement (double precision), score_indicateur (double precision), plan_id (bigint), score_objectif (double precision), nb_fiche_action_total (bigint), score_budget (double precision), key (text), nom (text), score_referentiel (double precision), c_referentiel (double precision), score (double precision), collectivite_id (bigint), etoiles_visuelles (text), type (double precision)
pap_note_backup: etoiles_visuelles (text), score_referentiel (double precision), score_indicateur (double precision), plan_id (bigint), score (double precision), c_referentiel (double precision), nom (text), semaine (text), score_budget (double precision), nom_ct (text), key (text), score_objectif (double precision), score_pilotabilite (double precision), score_avancement (double precision), nb_fiche_action_total (bigint), collectivite_id (bigint), type (double precision)
pap_note_region: region_name (text), nom_plan (text), plan_id (bigint), collectivite_id (bigint), departement_name (text), nom (text), semaine (text), score (double precision)
pap_note_snapshot: key (text), score (double precision), score_indicateur (double precision), score_avancement (double precision), nom_ct (text), score_pilotabilite (double precision), nom (text), semaine (text), c_referentiel (double precision), score_budget (double precision), score_objectif (double precision), etoiles_visuelles (text), nb_fiche_action_total (bigint), score_referentiel (double precision), type (double precision), collectivite_id (bigint), plan_id (bigint)
pap_statut_5_fiches_modifiees_13_semaines: collectivite_id (bigint), plan (bigint), statut (text), nb_pilotes (bigint), mois (timestamp without time zone)
pap_statut_5_fiches_modifiees_52_semaines: mois (timestamp without time zone), plan (bigint), collectivite_id (bigint), statut (text), nb_pilotes (bigint), nom_plan (text)
passage_pap_region: plan (bigint), departement_name (text), mois (text), collectivite_id (bigint), nom_plan (text), region_name (text)
pipeline: semaine (text), pipeline (text), collectivite_id (bigint)
plan_distrib: score_sup_5 (boolean), pilotable (boolean), plan (bigint), actif_12_mois (boolean), region_name (text), departement_name (text)
priorisation: categorie (smallint), collectivite_id (bigint), levier (text), secteur (text), note (smallint), created_at (timestamp with time zone), id (bigint), identifiant_referentiel (text), ids (text)
priorisation_action: categorie (integer), levier (text), collectivite_id (integer), created_at (timestamp with time zone), id (integer), fiche_action_id (integer)
priorisation_action_reference: description (text), levier (text), categorie (bigint), titre (text)
priorisation_categorie_levier: Réduction des déplacements (double precision), Biogaz (double precision), Vélo et transport en commun (double precision), Covoiturage (double precision), Electricité renouvelable (double precision), Captage de méthane dans les ISDND (double precision), Valorisation matière des déchets (double precision), Gestion des haies (double precision), Gestion des prairies (double precision), Elevage durable (double precision), Changements de pratiques de fertilisation azotée (double precision), Changement de chaudière à fioul (tertiaire) (double precision), categorie (bigint), Sobriété et isolation des bâtiments (tertiaire) (double precision), Changement chaudières gaz + rénovation (résidentiel) (double precision), Réseaux de chaleur décarbonés (double precision), Gestion des forêts et produits bois (double precision), Bâtiments & Machines agricoles (double precision), Production Industrielle (double precision), Pratiques stockantes (double precision), Efficacité et carburants décarbonés des véhicules privés (double precision), Sobriété foncière (double precision), Véhicules électriques (double precision), Sobriété des bâtiments (résidentiel) (double precision), Changement de chaudière à gaz (tertiaire) (double precision), Changement chaudières fioul + rénovation (résidentiel) (double precision), Prévention des déchets (double precision), Fret décarboné et multimodalité (double precision), Efficacité et sobriété logistique (double precision), Bus et cars décarbonés (double precision)
priorisation_faisabilite: collectivite_id (integer), created_at (timestamp with time zone), faisabilite (integer), id (integer), levier (text), categorie (integer)
priorisation_hors_competence: id (integer), collectivite_id (integer), categorie (integer), levier (text), created_at (timestamp with time zone)
priorisation_reduction_levier: collectivite_id (integer), levier (text), reduction (double precision), id (integer), created_at (timestamp without time zone)
score_snapshot: point_pas_fait (double precision), siren (text), point_potentiel (double precision), etoiles (bigint), date (timestamp with time zone), date_fin_audit (timestamp with time zone), point_programme (double precision), nom (text), referentiel_id (text), point_fait (double precision), sujet (text), type_jalon (text)
stats_hero_section_site: nb_action_pilotable_active_12_mois (bigint), nb_pap_actif_12_mois (bigint), nb_user_actif_12_mois (bigint), nb_ct_actif_12_mois (bigint)
statut_fiche_13_semaines: fiche_id (bigint), statut (text), mois (text)
statut_fiche_52_semaines: fiche_id (bigint), statut (text), mois (text)
taux_contact_support: taux_support_bug_% (double precision), month (timestamp without time zone)
tmp_backup_indicateur_source_metadonnee: methodologie (text), source_id (text), date_version (timestamp without time zone), id (bigint), limites (text), nom_donnees (text), diffuseur (text), producteur (text)
tmp_backup_indicateur_valeur: estimation (text), collectivite_id (bigint), indicateur_id (bigint), calcul_auto (boolean), created_by (text), modified_at (timestamp with time zone), metadonnee_id (bigint), modified_by (text), id (bigint), objectif (text), resultat_commentaire (text), calcul_auto_identifiants_manquants (text), objectif_commentaire (text), resultat (double precision), date_valeur (timestamp without time zone), created_at (timestamp with time zone)
tr_comm: lb_comm_majs (text), id_tech_comm (bigint), cd_comm (text), cd_sirn_comm (double precision)
user_actif_12_mois: mois (timestamp without time zone), email (text), collectivite_id (double precision)
user_actifs_ct_mois: region_name (text), email (text), departement_name (text), collectivite_id (bigint), mois (text)
utilisateurs: telephone (text), prenom (text), email (text), nom (text), user_id (text)
utilisateurs_droits: user_id (text), date_creation (timestamp with time zone), est_referent (boolean), niveau_acces (text), champ_intervention (text), fonction (text), collectivite_id (bigint), invitation (boolean), details_fonction (text)
visite_annuelle: derniere_date (timestamp with time zone), collectivite_id (bigint)

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
