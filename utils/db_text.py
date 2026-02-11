relations_text = """
fiche_action_pilote — relations :
  historique.fiche_action_pilote.fiche_historise_id → historique.fiche_action.id
action_audit_state — relations :
  labellisation.action_audit_state.action_id → public.action_relation.id
  labellisation.action_audit_state.audit_id → labellisation.audit.id
  labellisation.action_audit_state.collectivite_id → public.collectivite.id
  labellisation.action_audit_state.modified_by → auth.users.id
audit — relations :
  labellisation.audit.collectivite_id → public.collectivite.id
  labellisation.audit.demande_id → labellisation.demande.id
demande — relations :
  labellisation.demande.associated_collectivite_id → public.collectivite.id
  labellisation.demande.collectivite_id → public.collectivite.id
  labellisation.demande.demandeur → auth.users.id
preuve_base — relations :
  labellisation.preuve_base.collectivite_id → public.collectivite.id
  labellisation.preuve_base.fichier_id → labellisation.bibliotheque_fichier.id
  labellisation.preuve_base.modified_by → auth.users.id
notification — relations :
  notifications.notification.send_to → auth.users.id
action_commentaire — relations :
  public.action_commentaire.action_id → public.action_relation.id
  public.action_commentaire.collectivite_id → public.collectivite.id
  public.action_commentaire.modified_by → auth.users.id
action_definition — relations :
  public.action_definition.action_id → public.action_relation.id
  public.action_definition.referentiel_id → public.referentiel_definition.id
action_definition_tag — relations :
  public.action_definition_tag.action_id → public.action_relation.id
  public.action_definition_tag.referentiel_id → public.referentiel_definition.id
  public.action_definition_tag.tag_ref → public.referentiel_tag.ref
action_pilote — relations :
  public.action_pilote.action_id → public.action_relation.id
  public.action_pilote.collectivite_id → public.collectivite.id
  public.action_pilote.tag_id → public.personne_tag.id
  public.action_pilote.user_id → public.dcp.user_id
action_relation — relations :
  public.action_relation.parent → public.action_relation.id
action_score_indicateur_valeur — relations :
  public.action_score_indicateur_valeur.action_id → public.action_definition.action_id
  public.action_score_indicateur_valeur.collectivite_id → public.collectivite.id
  public.action_score_indicateur_valeur.indicateur_id → public.indicateur_definition.id
  public.action_score_indicateur_valeur.indicateur_valeur_id → public.indicateur_valeur.id
action_service — relations :
  public.action_service.action_id → public.action_relation.id
  public.action_service.collectivite_id → public.collectivite.id
  public.action_service.service_tag_id → public.service_tag.id
action_statut — relations :
  public.action_statut.action_id → public.action_relation.id
  public.action_statut.collectivite_id → public.collectivite.id
  public.action_statut.modified_by → auth.users.id
axe — relations :
  public.axe.collectivite_id → public.collectivite.id
  public.axe.modified_by → auth.users.id
  public.axe.panier_id → public.panier.id
  public.axe.parent → public.axe.id
  public.axe.plan → public.axe.id
  public.axe.type → public.plan_action_type.id
categorie_tag — relations :
  public.categorie_tag.collectivite_id → public.collectivite.id
  public.categorie_tag.created_by → auth.users.id
  public.categorie_tag.groupement_id → public.groupement.id
collectivite — relations :
  public.collectivite.nature_insee → public.collectivite_banatic_type.id
collectivite_banatic_competence — relations :
  public.collectivite_banatic_competence.collectivite_id → public.collectivite.id
  public.collectivite_banatic_competence.competence_code → public.banatic_competence.code
collectivite_bucket — relations :
  public.collectivite_bucket.bucket_id → storage.buckets.id
  public.collectivite_bucket.collectivite_id → public.collectivite.id
collectivite_relations — relations :
  public.collectivite_relations.id → public.collectivite.id
  public.collectivite_relations.parent_id → public.collectivite.id
commune — relations :
  public.commune.collectivite_id → public.collectivite.id
cot — relations :
  public.cot.collectivite_id → public.collectivite.id
  public.cot.signataire → public.collectivite.id
fiche_action — relations :
  public.fiche_action.collectivite_id → public.collectivite.id
  public.fiche_action.created_by → auth.users.id
  public.fiche_action.modified_by → auth.users.id
  public.fiche_action.parent_id → public.fiche_action.id
  public.fiche_action.temps_de_mise_en_oeuvre_id → public.action_impact_temps_de_mise_en_oeuvre.niveau
fiche_action_action — relations :
  public.fiche_action_action.action_id → public.action_relation.id
  public.fiche_action_action.fiche_id → public.fiche_action.id
fiche_action_axe — relations :
  public.fiche_action_axe.axe_id → public.axe.id
  public.fiche_action_axe.fiche_id → public.fiche_action.id
fiche_action_budget — relations :
  public.fiche_action_budget.fiche_id → public.fiche_action.id
fiche_action_effet_attendu — relations :
  public.fiche_action_effet_attendu.effet_attendu_id → public.effet_attendu.id
  public.fiche_action_effet_attendu.fiche_id → public.fiche_action.id
fiche_action_etape — relations :
  public.fiche_action_etape.created_by → auth.users.id
  public.fiche_action_etape.fiche_id → public.fiche_action.id
  public.fiche_action_etape.modified_by → auth.users.id
fiche_action_financeur_tag — relations :
  public.fiche_action_financeur_tag.fiche_id → public.fiche_action.id
  public.fiche_action_financeur_tag.financeur_tag_id → public.financeur_tag.id
fiche_action_indicateur — relations :
  public.fiche_action_indicateur.fiche_id → public.fiche_action.id
  public.fiche_action_indicateur.indicateur_id → public.indicateur_definition.id
fiche_action_libre_tag — relations :
  public.fiche_action_libre_tag.created_by → auth.users.id
  public.fiche_action_libre_tag.fiche_id → public.fiche_action.id
  public.fiche_action_libre_tag.libre_tag_id → public.libre_tag.id
fiche_action_lien — relations :
  public.fiche_action_lien.fiche_deux → public.fiche_action.id
  public.fiche_action_lien.fiche_une → public.fiche_action.id
fiche_action_note — relations :
  public.fiche_action_note.created_by → auth.users.id
  public.fiche_action_note.fiche_id → public.fiche_action.id
  public.fiche_action_note.modified_by → auth.users.id
fiche_action_partenaire_tag — relations :
  public.fiche_action_partenaire_tag.fiche_id → public.fiche_action.id
  public.fiche_action_partenaire_tag.partenaire_tag_id → public.partenaire_tag.id
fiche_action_pilote — relations :
  public.fiche_action_pilote.fiche_id → public.fiche_action.id
  public.fiche_action_pilote.tag_id → public.personne_tag.id
  public.fiche_action_pilote.user_id → public.dcp.user_id
fiche_action_referent — relations :
  public.fiche_action_referent.fiche_id → public.fiche_action.id
  public.fiche_action_referent.tag_id → public.personne_tag.id
  public.fiche_action_referent.user_id → public.dcp.user_id
fiche_action_service_tag — relations :
  public.fiche_action_service_tag.fiche_id → public.fiche_action.id
  public.fiche_action_service_tag.service_tag_id → public.service_tag.id
fiche_action_sharing — relations :
  public.fiche_action_sharing.collectivite_id → public.collectivite.id
  public.fiche_action_sharing.created_by → auth.users.id
  public.fiche_action_sharing.fiche_id → public.fiche_action.id
fiche_action_sous_thematique — relations :
  public.fiche_action_sous_thematique.fiche_id → public.fiche_action.id
  public.fiche_action_sous_thematique.thematique_id → public.sous_thematique.id
fiche_action_structure_tag — relations :
  public.fiche_action_structure_tag.fiche_id → public.fiche_action.id
  public.fiche_action_structure_tag.structure_tag_id → public.structure_tag.id
fiche_action_thematique — relations :
  public.fiche_action_thematique.fiche_id → public.fiche_action.id
  public.fiche_action_thematique.thematique_id → public.thematique.id
financeur_tag — relations :
  public.financeur_tag.collectivite_id → public.collectivite.id
groupement_collectivite — relations :
  public.groupement_collectivite.collectivite_id → public.collectivite.id
  public.groupement_collectivite.groupement_id → public.groupement.id
indicateur_action — relations :
  public.indicateur_action.action_id → public.action_relation.id
  public.indicateur_action.indicateur_id → public.indicateur_definition.id
indicateur_artificialisation — relations :
  public.indicateur_artificialisation.collectivite_id → public.collectivite.id
indicateur_categorie_tag — relations :
  public.indicateur_categorie_tag.categorie_tag_id → public.categorie_tag.id
  public.indicateur_categorie_tag.indicateur_id → public.indicateur_definition.id
indicateur_collectivite — relations :
  public.indicateur_collectivite.collectivite_id → public.collectivite.id
  public.indicateur_collectivite.indicateur_id → public.indicateur_definition.id
  public.indicateur_collectivite.modified_by → auth.users.id
indicateur_definition — relations :
  public.indicateur_definition.collectivite_id → public.collectivite.id
  public.indicateur_definition.created_by → auth.users.id
  public.indicateur_definition.groupement_id → public.groupement.id
  public.indicateur_definition.modified_by → auth.users.id
indicateur_groupe — relations :
  public.indicateur_groupe.enfant → public.indicateur_definition.id
  public.indicateur_groupe.parent → public.indicateur_definition.id
indicateur_objectif — relations :
  public.indicateur_objectif.indicateur_id → public.indicateur_definition.id
indicateur_pilote — relations :
  public.indicateur_pilote.collectivite_id → public.collectivite.id
  public.indicateur_pilote.indicateur_id → public.indicateur_definition.id
  public.indicateur_pilote.tag_id → public.personne_tag.id
  public.indicateur_pilote.user_id → auth.users.id
indicateur_service_tag — relations :
  public.indicateur_service_tag.collectivite_id → public.collectivite.id
  public.indicateur_service_tag.indicateur_id → public.indicateur_definition.id
  public.indicateur_service_tag.service_tag_id → public.service_tag.id
indicateur_source_metadonnee — relations :
  public.indicateur_source_metadonnee.source_id → public.indicateur_source.id
indicateur_source_source_calcul — relations :
  public.indicateur_source_source_calcul.source_calcul_id → public.indicateur_source.id
  public.indicateur_source_source_calcul.source_id → public.indicateur_source.id
indicateur_sous_thematique — relations :
  public.indicateur_sous_thematique.indicateur_id → public.indicateur_definition.id
  public.indicateur_sous_thematique.sous_thematique_id → public.sous_thematique.id
indicateur_thematique — relations :
  public.indicateur_thematique.indicateur_id → public.indicateur_definition.id
  public.indicateur_thematique.thematique_id → public.thematique.id
indicateur_valeur — relations :
  public.indicateur_valeur.collectivite_id → public.collectivite.id
  public.indicateur_valeur.created_by → auth.users.id
  public.indicateur_valeur.indicateur_id → public.indicateur_definition.id
  public.indicateur_valeur.metadonnee_id → public.indicateur_source_metadonnee.id
  public.indicateur_valeur.modified_by → auth.users.id
labellisation — relations :
  public.labellisation.audit_id → labellisation.audit.id
  public.labellisation.collectivite_id → public.collectivite.id
libre_tag — relations :
  public.libre_tag.collectivite_id → public.collectivite.id
  public.libre_tag.created_by → auth.users.id
partenaire_tag — relations :
  public.partenaire_tag.collectivite_id → public.collectivite.id
personne_tag — relations :
  public.personne_tag.collectivite_id → public.collectivite.id
plan_pilote — relations :
  public.plan_pilote.created_by → auth.users.id
  public.plan_pilote.plan_id → public.axe.id
  public.plan_pilote.tag_id → public.personne_tag.id
  public.plan_pilote.user_id → public.dcp.user_id
plan_referent — relations :
  public.plan_referent.created_by → auth.users.id
  public.plan_referent.plan_id → public.axe.id
  public.plan_referent.tag_id → public.personne_tag.id
  public.plan_referent.user_id → public.dcp.user_id
private_collectivite_membre — relations :
  public.private_collectivite_membre.collectivite_id → public.collectivite.id
  public.private_collectivite_membre.user_id → auth.users.id
private_utilisateur_droit — relations :
  public.private_utilisateur_droit.collectivite_id → public.collectivite.id
  public.private_utilisateur_droit.invitation_id → utilisateur.invitation.id
  public.private_utilisateur_droit.user_id → auth.users.id
score_snapshot — relations :
  public.score_snapshot.audit_id → labellisation.audit.id
  public.score_snapshot.collectivite_id → public.collectivite.id
  public.score_snapshot.referentiel_id → public.referentiel_definition.id
service_tag — relations :
  public.service_tag.collectivite_id → public.collectivite.id
structure_tag — relations :
  public.structure_tag.collectivite_id → public.collectivite.id
"""

tables_text = """
auth.users: email_change_confirm_status (smallint), raw_user_meta_data (jsonb), raw_app_meta_data (jsonb), last_sign_in_at (timestamp with time zone), email_change_sent_at (timestamp with time zone), email_change (character varying), email_change_token_new (character varying), recovery_sent_at (timestamp with time zone), recovery_token (character varying), confirmation_sent_at (timestamp with time zone), confirmation_token (character varying), invited_at (timestamp with time zone), email_confirmed_at (timestamp with time zone), encrypted_password (character varying), email (character varying), role (character varying), aud (character varying), id (uuid), instance_id (uuid), is_sso_user (boolean), reauthentication_sent_at (timestamp with time zone), deleted_at (timestamp with time zone), phone_change_sent_at (timestamp with time zone), phone_change_token (character varying), phone_change (text), phone_confirmed_at (timestamp with time zone), phone (text), updated_at (timestamp with time zone), created_at (timestamp with time zone), confirmed_at (timestamp with time zone), email_change_token_current (character varying), banned_until (timestamp with time zone), reauthentication_token (character varying), is_super_admin (boolean), is_anonymous (boolean)
historique.action_statut: previous_avancement_detaille (ARRAY), concerne (boolean), previous_concerne (boolean), modified_by (uuid), previous_modified_by (uuid), modified_at (timestamp with time zone), previous_modified_at (timestamp with time zone), avancement (USER-DEFINED), previous_avancement (USER-DEFINED), avancement_detaille (ARRAY), id (integer), collectivite_id (integer), action_id (character varying)
historique.fiche_action: previous_description (character varying), piliers_eci (ARRAY), previous_piliers_eci (ARRAY), objectifs (character varying), previous_objectifs (character varying), resultats_attendus (ARRAY), previous_resultats_attendus (ARRAY), cibles (ARRAY), deleted (boolean), previous_restreint (boolean), restreint (boolean), previous_modified_by (uuid), modified_by (uuid), previous_modified_at (timestamp with time zone), modified_at (timestamp with time zone), created_at (timestamp with time zone), collectivite_id (integer), previous_maj_termine (boolean), maj_termine (boolean), previous_calendrier (character varying), calendrier (character varying), previous_amelioration_continue (boolean), amelioration_continue (boolean), previous_date_fin_provisoire (timestamp with time zone), date_fin_provisoire (timestamp with time zone), previous_date_debut (timestamp with time zone), date_debut (timestamp with time zone), previous_niveau_priorite (text), niveau_priorite (text), previous_statut (text), statut (text), previous_budget_previsionnel (numeric), budget_previsionnel (numeric), previous_financements (text), financements (text), previous_ressources (character varying), previous_cibles (ARRAY), ressources (character varying), id (integer), fiche_id (integer), titre (character varying), previous_titre (character varying), description (character varying)
historique.fiche_action_pilote: previous (boolean), id (integer), fiche_historise_id (integer), user_id (uuid), tag_nom (text)
labellisation.action_audit_state: statut (USER-DEFINED), avis (text), ordre_du_jour (boolean), modified_at (timestamp with time zone), modified_by (uuid), collectivite_id (integer), action_id (character varying), audit_id (integer), id (integer)
labellisation.audit: demande_id (integer), valide_labellisation (boolean), referentiel (USER-DEFINED), collectivite_id (integer), id (integer), clos (boolean), date_cnl (timestamp with time zone), valide (boolean), date_fin (timestamp with time zone), date_debut (timestamp with time zone)
labellisation.demande: etoiles (USER-DEFINED), date (timestamp with time zone), sujet (USER-DEFINED), modified_at (timestamp with time zone), envoyee_le (timestamp with time zone), demandeur (uuid), associated_collectivite_id (integer), en_cours (boolean), id (integer), collectivite_id (integer), referentiel (USER-DEFINED)
labellisation.etoile_meta: min_realise_score (double precision), etoile (USER-DEFINED), prochaine_etoile (USER-DEFINED), long_label (character varying), short_label (character varying), min_realise_percentage (integer)
labellisation.preuve_base: modified_at (timestamp with time zone), modified_by (uuid), collectivite_id (integer), fichier_id (integer), url (text), titre (text), commentaire (text), lien (jsonb)
notifications.notification: notified_on (text), send_after (timestamp with time zone), id (integer), entity_id (text), status (text), send_to (uuid), sent_at (timestamp with time zone), sent_to_email (text), error_message (text), retries (integer), created_by (uuid), created_at (timestamp with time zone), notification_data (jsonb)
public.action_commentaire: collectivite_id (integer), action_id (character varying), commentaire (text), modified_by (uuid), modified_at (timestamp with time zone)
public.action_definition: description (text), expr_score (text), referentiel_version (character varying), referentiel_id (character varying), categorie (USER-DEFINED), perimetre_evaluation (text), reduction_potentiel (text), pourcentage (double precision), points (double precision), preuve (text), ressources (text), exemples (text), contexte (text), nom (text), identifiant (text), referentiel (USER-DEFINED), action_id (character varying), modified_at (timestamp with time zone)
public.action_definition_tag: action_id (character varying), referentiel_id (character varying), tag_ref (character varying)
public.action_discussion_feed: collectivite_id (integer), id (integer), action_id (character varying), created_by (uuid), created_at (timestamp with time zone), modified_at (timestamp with time zone), status (USER-DEFINED), commentaires (ARRAY)
public.action_pilote: tag_id (integer), collectivite_id (integer), action_id (character varying), user_id (uuid)
public.action_relation: referentiel (USER-DEFINED), id (character varying), parent (character varying)
public.action_score_indicateur_valeur: type_score (text), action_id (character varying), collectivite_id (integer), indicateur_id (integer), indicateur_valeur_id (integer)
public.action_service: collectivite_id (integer), action_id (character varying), service_tag_id (integer)
public.action_statut: concerne (boolean), action_id (character varying), collectivite_id (integer), modified_at (timestamp with time zone), avancement_detaille (ARRAY), modified_by (uuid), avancement (USER-DEFINED)
public.audit: date_debut (timestamp with time zone), date_cnl (timestamp with time zone), valide (boolean), date_fin (timestamp with time zone), referentiel (USER-DEFINED), valide_labellisation (boolean), id (integer), collectivite_id (integer), clos (boolean), demande_id (integer)
public.axe: id (integer), panier_id (uuid), type (integer), plan (integer), modified_by (uuid), created_at (timestamp with time zone), parent (integer), collectivite_id (integer), nom (text), modified_at (timestamp with time zone), description (text)
public.banatic_competence: nom (text), code (integer)
public.categorie_tag: visible (boolean), id (integer), groupement_id (integer), created_at (timestamp with time zone), collectivite_id (integer), created_by (uuid), nom (text)
public.collectivite: type (text), nom (text), access_restreint (boolean), modified_at (timestamp with time zone), created_at (timestamp with time zone), id (integer), nature_insee (text), population (integer), dans_aire_urbaine (boolean), nic (character varying), region_code (character varying), departement_code (character varying), siren (character varying), commune_code (character varying)
public.collectivite_banatic_competence: competence_code (integer), collectivite_id (integer)
public.collectivite_banatic_type: nom (text), id (text), type (text)
public.collectivite_bucket: collectivite_id (integer), bucket_id (text)
public.collectivite_carte_identite: collectivite_id (integer), population_source (text), departement_name (character varying), region_name (character varying), code_siren_insee (character varying), type_collectivite (text), nom (text), is_cot (boolean), population_totale (integer)
public.collectivite_identite: localisation (ARRAY), type (ARRAY), population (ARRAY), id (integer)
public.collectivite_relations: parent_id (integer), id (integer)
public.commune: nom (character varying), collectivite_id (integer), id (integer), code (character varying)
public.comparaison_scores_audit: action_id (character varying), courant (USER-DEFINED), pre_audit (USER-DEFINED), collectivite_id (integer), referentiel (USER-DEFINED)
public.cot: collectivite_id (integer), signataire (integer), actif (boolean)
public.effet_attendu: notice (text), id (integer), nom (text)
public.fiche_action: budget_previsionnel (numeric), objectifs (character varying), resultats_attendus (ARRAY), cibles (ARRAY), ressources (character varying), financements (text), statut (USER-DEFINED), niveau_priorite (USER-DEFINED), date_debut (timestamp with time zone), date_fin_provisoire (timestamp with time zone), amelioration_continue (boolean), calendrier (character varying), maj_termine (boolean), collectivite_id (integer), created_at (timestamp with time zone), modified_by (uuid), restreint (boolean), instance_gouvernance (text), participation_citoyenne (text), participation_citoyenne_type (character varying), temps_de_mise_en_oeuvre_id (integer), created_by (uuid), parent_id (integer), deleted (boolean), modified_at (timestamp with time zone), id (integer), titre (character varying), description (character varying), piliers_eci (ARRAY)
public.fiche_action_action: action_id (character varying), fiche_id (integer)
public.fiche_action_axe: axe_id (integer), fiche_id (integer)
public.fiche_action_budget: est_etale (boolean), budget_reel (numeric), id (integer), fiche_id (integer), type (text), unite (text), annee (integer), budget_previsionnel (numeric)
public.fiche_action_effet_attendu: fiche_id (integer), effet_attendu_id (integer)
public.fiche_action_etape: created_at (timestamp with time zone), modified_by (uuid), ordre (integer), nom (text), fiche_id (integer), id (integer), realise (boolean), created_by (uuid), modified_at (timestamp with time zone)
public.fiche_action_financeur_tag: fiche_id (integer), id (integer), financeur_tag_id (integer), montant_ttc (integer)
public.fiche_action_import_csv: plan_nom (text), structure_pilote (text), moyens (text), partenaires (text), personne_referente (text), elu_referent (text), financements (text), budget (text), statut (text), priorite (text), date_debut (text), date_fin (text), amelioration_continue (text), calendrier (text), notes (text), collectivite_id (text), service (text), financeur_un (text), montant_un (text), financeur_deux (text), montant_deux (text), financeur_trois (text), montant_trois (text), axe (text), sous_axe (text), sous_sous_axe (text), num_action (text), titre (text), description (text), objectifs (text), resultats_attendus (text), cibles (text)
public.fiche_action_indicateur: indicateur_id (integer), fiche_id (integer)
public.fiche_action_libre_tag: libre_tag_id (integer), created_by (uuid), fiche_id (integer), created_at (timestamp with time zone)
public.fiche_action_lien: fiche_deux (integer), fiche_une (integer)
public.fiche_action_note: note (text), id (integer), created_by (uuid), modified_by (uuid), created_at (timestamp with time zone), modified_at (timestamp with time zone), date_note (date), fiche_id (integer)
public.fiche_action_partenaire_tag: fiche_id (integer), partenaire_tag_id (integer)
public.fiche_action_personne_pilote: tag_id (integer), collectivite_id (integer), nom (text), user_id (uuid)
public.fiche_action_personne_referente: collectivite_id (integer), nom (text), user_id (uuid), tag_id (integer)
public.fiche_action_pilote: user_id (uuid), tag_id (integer), fiche_id (integer)
public.fiche_action_referent: user_id (uuid), tag_id (integer), fiche_id (integer)
public.fiche_action_service_tag: service_tag_id (integer), fiche_id (integer)
public.fiche_action_sharing: created_at (timestamp with time zone), collectivite_id (integer), fiche_id (integer), created_by (uuid)
public.fiche_action_sous_thematique: thematique_id (integer), fiche_id (integer)
public.fiche_action_structure_tag: structure_tag_id (integer), fiche_id (integer)
public.fiche_action_thematique: thematique_id (integer), fiche_id (integer)
public.financeur_tag: nom (text), id (integer), collectivite_id (integer)
public.groupement: nom (text), id (integer)
public.groupement_collectivite: collectivite_id (integer), groupement_id (integer)
public.indicateur_action: indicateur_id (integer), action_id (character varying)
public.indicateur_artificialisation: routiere (double precision), ferroviaire (double precision), inconnue (double precision), collectivite_id (integer), total (double precision), activite (double precision), habitat (double precision), mixte (double precision)
public.indicateur_categorie_tag: indicateur_id (integer), categorie_tag_id (integer)
public.indicateur_collectivite: modified_by (uuid), favoris (boolean), confidentiel (boolean), commentaire (text), indicateur_id (integer), collectivite_id (integer), modified_at (timestamp with time zone)
public.indicateur_definition: sans_valeur_utilisateur (boolean), expr_seuil (text), borne_min (double precision), borne_max (double precision), participation_score (boolean), libelle_cible_seuil (text), valeur_calcule (text), modified_at (timestamp with time zone), created_at (timestamp with time zone), modified_by (uuid), created_by (uuid), titre_court (text), version (character varying), precision (integer), expr_cible (text), id (integer), groupement_id (integer), collectivite_id (integer), identifiant_referentiel (text), titre (text), titre_long (text), description (text), unite (text)
public.indicateur_groupe: enfant (integer), parent (integer)
public.indicateur_objectif: formule (text), indicateur_id (integer), date_valeur (date)
public.indicateur_pilote: tag_id (integer), id (integer), user_id (uuid), collectivite_id (integer), indicateur_id (integer)
public.indicateur_service_tag: indicateur_id (integer), service_tag_id (integer), collectivite_id (integer)
public.indicateur_source: libelle (text), id (text), ordre_affichage (integer)
public.indicateur_source_metadonnee: source_id (text), methodologie (text), producteur (text), diffuseur (text), nom_donnees (text), id (integer), date_version (timestamp without time zone), limites (text)
public.indicateur_source_source_calcul: source_calcul_id (text), source_id (text)
public.indicateur_sous_thematique: sous_thematique_id (integer), indicateur_id (integer)
public.indicateur_thematique: thematique_id (integer), indicateur_id (integer)
public.indicateur_valeur: objectif (double precision), indicateur_id (integer), collectivite_id (integer), date_valeur (date), metadonnee_id (integer), resultat (double precision), resultat_commentaire (text), objectif_commentaire (text), estimation (double precision), modified_at (timestamp with time zone), created_at (timestamp with time zone), modified_by (uuid), created_by (uuid), calcul_auto (boolean), calcul_auto_identifiants_manquants (ARRAY), id (integer)
public.labellisation: id (integer), etoiles (integer), annee (double precision), obtenue_le (timestamp without time zone), collectivite_id (integer), referentiel (USER-DEFINED), audit_id (integer), score_programme (double precision), score_realise (double precision)
public.libre_tag: created_at (timestamp with time zone), collectivite_id (integer), nom (text), id (integer), created_by (uuid)
public.partenaire_tag: nom (text), collectivite_id (integer), id (integer)
public.personne_tag: nom (text), collectivite_id (integer), id (integer)
public.plan_pilote: tag_id (integer), user_id (uuid), created_at (timestamp with time zone), created_by (uuid), plan_id (integer)
public.plan_referent: tag_id (integer), user_id (uuid), created_at (timestamp with time zone), created_by (uuid), plan_id (integer)
public.private_collectivite_membre: created_at (timestamp with time zone), details_fonction (text), fonction (USER-DEFINED), collectivite_id (integer), user_id (uuid), est_referent (boolean), modified_at (timestamp with time zone), champ_intervention (ARRAY)
public.private_utilisateur_droit: user_id (uuid), created_at (timestamp with time zone), collectivite_id (integer), id (integer), active (boolean), invitation_id (uuid), niveau_acces (USER-DEFINED), modified_at (timestamp with time zone)
public.referentiel_definition: version (character varying), id (character varying), locked (boolean), created_at (timestamp with time zone), modified_at (timestamp with time zone), hierarchie (ARRAY), nom (character varying)
public.referentiel_tag: type (character varying), ref (character varying), nom (character varying)
public.score_snapshot: created_at (timestamp with time zone), modified_by (uuid), modified_at (timestamp with time zone), created_by (uuid), personnalisation_reponses (jsonb), referentiel_scores (jsonb), point_potentiel (double precision), point_pas_fait (double precision), point_programme (double precision), etoiles (integer), ref (character varying), date (timestamp with time zone), audit_id (integer), referentiel_version (character varying), referentiel_id (character varying), collectivite_id (integer), point_fait (double precision), type_jalon (character varying), nom (character varying)
public.service_tag: id (integer), nom (text), collectivite_id (integer)
public.structure_tag: id (integer), nom (text), collectivite_id (integer)
"""