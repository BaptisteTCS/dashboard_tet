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

tables_text_2 = """
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

tables_text = """
prod.action_commentaire: collectivite_id (bigint), action_id (text), commentaire (text), modified_by (text), modified_at (timestamp with time zone)
prod.action_definition: modified_at (timestamp with time zone), action_id (text), referentiel (text), identifiant (text), nom (text), description (text), contexte (text), exemples (text), ressources (text), reduction_potentiel (text), perimetre_evaluation (text), preuve (text), points (double precision), pourcentage (double precision), categorie (text), referentiel_id (text), referentiel_version (text), expr_score (text), adaptation_niveau (text), thematique_sgpe (text)
prod.action_definition_tag: referentiel_id (text), action_id (text), tag_ref (text)
prod.action_pilote: collectivite_id (bigint), action_id (text), user_id (text), tag_id (double precision)
prod.action_relation: id (text), referentiel (text), parent (text)
prod.action_score_indicateur_valeur: action_id (text), collectivite_id (bigint), indicateur_id (bigint), indicateur_valeur_id (bigint), type_score (text)
prod.action_service: collectivite_id (bigint), action_id (text), service_tag_id (bigint)
prod.action_statut: collectivite_id (bigint), action_id (text), avancement (text), avancement_detaille (json), concerne (boolean), modified_by (text), modified_at (timestamp with time zone)
prod.auth_users: instance_id (text), id (text), aud (text), role (text), email (text), encrypted_password (text), email_confirmed_at (timestamp with time zone), invited_at (text), confirmation_token (text), confirmation_sent_at (timestamp with time zone), recovery_token (text), recovery_sent_at (timestamp with time zone), email_change_token_new (text), email_change (text), email_change_sent_at (timestamp with time zone), last_sign_in_at (timestamp with time zone), raw_app_meta_data (json), raw_user_meta_data (json), is_super_admin (boolean), created_at (timestamp with time zone), updated_at (timestamp with time zone), phone (text), phone_confirmed_at (text), phone_change (text), phone_change_token (text), phone_change_sent_at (text), confirmed_at (timestamp with time zone), email_change_token_current (text), email_change_confirm_status (bigint), banned_until (timestamp with time zone), reauthentication_token (text), reauthentication_sent_at (text), is_sso_user (boolean), deleted_at (text), is_anonymous (boolean)
prod.axe: modified_at (timestamp with time zone), id (bigint), nom (text), collectivite_id (bigint), parent (double precision), created_at (timestamp with time zone), modified_by (text), plan (bigint), type (double precision), panier_id (text), description (text), date_debut (timestamp with time zone), date_fin (timestamp with time zone)
prod.banatic_competence: code (bigint), nom (text)
prod.categorie_tag: id (bigint), groupement_id (double precision), collectivite_id (text), nom (text), visible (boolean), created_at (timestamp with time zone), created_by (text)
prod.collectivite: id (bigint), created_at (timestamp with time zone), modified_at (timestamp with time zone), access_restreint (boolean), nom (text), type (text), commune_code (text), siren (text), departement_code (text), region_code (text), nature_insee (text), population (double precision), dans_aire_urbaine (boolean), nic (text), preferences (json)
prod.collectivite_banatic_competence: collectivite_id (bigint), competence_code (bigint)
prod.collectivite_banatic_type: id (text), nom (text), type (text)
prod.collectivite_bucket: collectivite_id (bigint), bucket_id (text)
prod.collectivite_carte_identite: collectivite_id (bigint), nom (text), type_collectivite (text), code_siren_insee (text), region_name (text), departement_name (text), population_source (text), population_totale (bigint), is_cot (boolean)
prod.collectivite_identite: id (bigint), population (json), type (json), localisation (json)
prod.collectivite_relations: id (text), parent_id (text)
prod.commune: id (bigint), collectivite_id (bigint), nom (text), code (text)
prod.cot: collectivite_id (bigint), actif (boolean), signataire (bigint)
prod.effet_attendu: id (bigint), nom (text), notice (text)
prod.fiche_action: modified_at (timestamp with time zone), id (bigint), titre (text), description (text), piliers_eci (text), objectifs (text), resultats_attendus (text), cibles (json), ressources (text), financements (text), budget_previsionnel (double precision), statut (text), niveau_priorite (text), date_debut (timestamp with time zone), date_fin_provisoire (timestamp with time zone), amelioration_continue (boolean), maj_termine (boolean), collectivite_id (bigint), created_at (timestamp with time zone), modified_by (text), restreint (boolean), instance_gouvernance (text), participation_citoyenne (text), participation_citoyenne_type (text), temps_de_mise_en_oeuvre_id (double precision), created_by (text), parent_id (double precision), deleted (boolean)
prod.fiche_action_action: fiche_id (bigint), action_id (text)
prod.fiche_action_axe: fiche_id (bigint), axe_id (bigint)
prod.fiche_action_budget: id (bigint), fiche_id (bigint), type (text), unite (text), annee (double precision), budget_previsionnel (double precision), budget_reel (double precision), est_etale (boolean)
prod.fiche_action_effet_attendu: fiche_id (bigint), effet_attendu_id (bigint)
prod.fiche_action_etape: id (bigint), fiche_id (bigint), nom (text), ordre (bigint), realise (boolean), modified_at (timestamp with time zone), created_at (timestamp with time zone), modified_by (text), created_by (text)
prod.fiche_action_financeur_tag: id (bigint), fiche_id (bigint), financeur_tag_id (bigint), montant_ttc (double precision)
prod.fiche_action_import_csv: axe (text), sous_axe (text), sous_sous_axe (text), num_action (text), titre (text), description (text), objectifs (text), resultats_attendus (text), cibles (text), structure_pilote (text), moyens (text), partenaires (text), personne_referente (text), elu_referent (text), financements (text), budget (text), statut (text), priorite (text), date_debut (text), date_fin (text), amelioration_continue (text), calendrier (text), notes (text), collectivite_id (text), plan_nom (text), service (text), financeur_un (text), montant_un (text), financeur_deux (text), montant_deux (text), financeur_trois (text), montant_trois (text)
prod.fiche_action_indicateur: indicateur_id (bigint), fiche_id (bigint)
prod.fiche_action_libre_tag: fiche_id (bigint), libre_tag_id (bigint), created_at (timestamp with time zone), created_by (text)
prod.fiche_action_lien: fiche_une (bigint), fiche_deux (bigint)
prod.fiche_action_note: fiche_id (bigint), date_note (timestamp with time zone), note (text), modified_at (timestamp with time zone), created_at (timestamp with time zone), modified_by (text), created_by (text), id (bigint)
prod.fiche_action_partenaire_tag: fiche_id (bigint), partenaire_tag_id (bigint)
prod.fiche_action_personne_pilote: collectivite_id (text), nom (text), user_id (text), tag_id (text)
prod.fiche_action_pilote: fiche_id (bigint), user_id (text), tag_id (double precision)
prod.fiche_action_referent: fiche_id (bigint), user_id (text), tag_id (double precision)
prod.fiche_action_service_tag: fiche_id (bigint), service_tag_id (bigint)
prod.fiche_action_sharing: fiche_id (bigint), collectivite_id (bigint), created_at (timestamp with time zone), created_by (text)
prod.fiche_action_sous_thematique: fiche_id (bigint), thematique_id (bigint)
prod.fiche_action_structure_tag: fiche_id (bigint), structure_tag_id (bigint)
prod.fiche_action_thematique: fiche_id (bigint), thematique_id (bigint)
prod.financeur_tag: id (bigint), nom (text), collectivite_id (bigint), created_at (timestamp with time zone), created_by (text)
prod.groupement: id (bigint), nom (text)
prod.groupement_collectivite: groupement_id (bigint), collectivite_id (bigint)
prod.historique_action_statut: id (bigint), collectivite_id (bigint), action_id (text), avancement (text), previous_avancement (text), avancement_detaille (json), previous_avancement_detaille (json), concerne (boolean), previous_concerne (boolean), modified_by (text), previous_modified_by (text), modified_at (timestamp with time zone), previous_modified_at (timestamp with time zone)
prod.historique_fiche_action: id (bigint), fiche_id (bigint), titre (text), previous_titre (text), description (text), previous_description (text), piliers_eci (json), previous_piliers_eci (json), objectifs (text), previous_objectifs (text), resultats_attendus (json), previous_resultats_attendus (json), cibles (json), previous_cibles (json), ressources (text), previous_ressources (text), financements (text), previous_financements (text), budget_previsionnel (double precision), previous_budget_previsionnel (double precision), statut (text), previous_statut (text), niveau_priorite (text), previous_niveau_priorite (text), date_debut (timestamp with time zone), previous_date_debut (timestamp with time zone), date_fin_provisoire (timestamp with time zone), previous_date_fin_provisoire (timestamp with time zone), amelioration_continue (boolean), previous_amelioration_continue (boolean), maj_termine (boolean), previous_maj_termine (boolean), collectivite_id (double precision), created_at (timestamp with time zone), modified_at (timestamp with time zone), previous_modified_at (timestamp with time zone), modified_by (text), previous_modified_by (text), restreint (boolean), previous_restreint (boolean), deleted (boolean)
prod.historique_fiche_action_pilote: id (bigint), fiche_historise_id (bigint), user_id (text), tag_nom (text), previous (boolean)
prod.indicateur_action: indicateur_id (bigint), action_id (text)
prod.indicateur_artificialisation: collectivite_id (bigint), total (double precision), activite (double precision), habitat (double precision), mixte (double precision), routiere (double precision), ferroviaire (double precision), inconnue (double precision)
prod.indicateur_categorie_tag: categorie_tag_id (bigint), indicateur_id (bigint)
prod.indicateur_collectivite: indicateur_id (bigint), collectivite_id (bigint), commentaire (text), confidentiel (boolean), favoris (boolean), modified_by (text), modified_at (timestamp with time zone)
prod.indicateur_definition: id (bigint), groupement_id (double precision), collectivite_id (double precision), identifiant_referentiel (text), titre (text), titre_long (text), description (text), unite (text), borne_min (text), borne_max (text), participation_score (boolean), sans_valeur_utilisateur (boolean), valeur_calcule (text), modified_at (timestamp with time zone), created_at (timestamp with time zone), modified_by (text), created_by (text), titre_court (text), version (text), precision (bigint), expr_cible (text), expr_seuil (text), libelle_cible_seuil (text)
prod.indicateur_groupe: parent (bigint), enfant (bigint)
prod.indicateur_objectif: indicateur_id (text), date_valeur (text), formule (text)
prod.indicateur_pilote: id (bigint), indicateur_id (bigint), user_id (text), tag_id (double precision), collectivite_id (bigint)
prod.indicateur_service_tag: indicateur_id (bigint), service_tag_id (bigint), collectivite_id (bigint)
prod.indicateur_source: id (text), libelle (text), ordre_affichage (bigint)
prod.indicateur_source_metadonnee: id (bigint), source_id (text), date_version (timestamp with time zone), nom_donnees (text), diffuseur (text), producteur (text), methodologie (text), limites (text)
prod.indicateur_source_source_calcul: source_id (text), source_calcul_id (text)
prod.indicateur_sous_thematique: indicateur_id (text), sous_thematique_id (text)
prod.indicateur_thematique: indicateur_id (bigint), thematique_id (bigint)
prod.indicateur_valeur: id (bigint), indicateur_id (bigint), collectivite_id (bigint), date_valeur (timestamp with time zone), metadonnee_id (double precision), resultat (double precision), objectif (double precision), modified_at (timestamp with time zone), created_at (timestamp with time zone), modified_by (text), created_by (text)
prod.labellisation: id (bigint), collectivite_id (bigint), referentiel (text), obtenue_le (timestamp with time zone), annee (double precision), etoiles (bigint), score_realise (double precision), score_programme (double precision), audit_id (double precision)
prod.labellisation_action_audit_state: id (bigint), audit_id (bigint), action_id (text), collectivite_id (bigint), modified_by (text), modified_at (timestamp with time zone), ordre_du_jour (boolean), avis (text), statut (text)
prod.labellisation_audit: id (bigint), collectivite_id (bigint), referentiel (text), demande_id (double precision), date_debut (timestamp with time zone), date_fin (timestamp with time zone), valide (boolean), date_cnl (timestamp with time zone), valide_labellisation (boolean), clos (boolean)
prod.labellisation_demande: id (bigint), en_cours (boolean), collectivite_id (bigint), referentiel (text), etoiles (text), date (timestamp with time zone), sujet (text), modified_at (timestamp with time zone), envoyee_le (timestamp with time zone), demandeur (text), associated_collectivite_id (double precision)
prod.labellisation_etoile_meta: etoile (text), prochaine_etoile (text), long_label (text), short_label (text), min_realise_percentage (bigint), min_realise_score (double precision)
prod.labellisation_preuve_base: collectivite_id (text), fichier_id (text), url (text), titre (text), commentaire (text), modified_by (text), modified_at (text), lien (text)
prod.libre_tag: id (bigint), nom (text), collectivite_id (bigint), created_at (timestamp with time zone), created_by (text)
prod.notifications_notification: id (text), entity_id (text), status (text), send_to (text), sent_at (text), sent_to_email (text), error_message (text), retries (text), created_by (text), created_at (text), notified_on (text), notification_data (text), send_after (text)
prod.partenaire_tag: id (bigint), nom (text), collectivite_id (bigint), created_at (timestamp with time zone), created_by (text)
prod.personne_tag: id (bigint), nom (text), collectivite_id (bigint), created_at (timestamp with time zone), created_by (text)
prod.plan_pilote: plan_id (text), tag_id (text), user_id (text), created_at (text), created_by (text)
prod.plan_referent: plan_id (text), tag_id (text), user_id (text), created_at (text), created_by (text)
prod.private_collectivite_membre: user_id (text), collectivite_id (bigint), fonction (text), details_fonction (text), champ_intervention (text), created_at (timestamp with time zone), modified_at (timestamp with time zone), est_referent (boolean)
prod.private_utilisateur_droit: id (bigint), user_id (text), collectivite_id (bigint), active (boolean), created_at (timestamp with time zone), modified_at (timestamp with time zone), niveau_acces (text), invitation_id (text)
prod.referentiel_definition: id (text), nom (text), version (text), hierarchie (text), created_at (timestamp with time zone), modified_at (timestamp with time zone), locked (boolean)
prod.referentiel_tag: ref (text), nom (text), type (text)
prod.score_snapshot: collectivite_id (bigint), referentiel_id (text), referentiel_version (text), audit_id (double precision), date (timestamp with time zone), ref (text), nom (text), type_jalon (text), point_fait (double precision), point_programme (double precision), point_pas_fait (double precision), point_potentiel (double precision), created_by (text), created_at (timestamp with time zone), modified_by (text), modified_at (timestamp with time zone), etoiles (bigint)
prod.service_tag: id (bigint), nom (text), collectivite_id (bigint), created_at (timestamp with time zone), created_by (text)
prod.structure_tag: id (bigint), nom (text), collectivite_id (bigint), created_at (timestamp with time zone), created_by (text)
public.Score_mesures: siren (text), nom (text), referentiel_id (text), date_fin_audit (timestamp with time zone), sujet (text), date (timestamp with time zone), type_jalon (text), actionId (text), pointFait (double precision), pointPasFait (double precision), pointProgramme (double precision), pointPotentiel (double precision), actionid (text), nom_mesure (text)
public.action_referentiel: action_id (text), referentiel (text), depth (bigint), type (text), nom (text), exemples (text)
public.activite_semaine: semaine (text), collectivite_id (double precision), email (text)
public.airtable_sync: collectivite_id (bigint), key (text), type (text), derniere_modif (text), derniere_creation_compte (text), user_derniere_creation_compte (text), top_contributeur (text), pageviews_plan (bigint), nb_contributeurs (bigint), nb_super_contributeurs (bigint), nb_fiches_modifiees_3_mois (bigint), nb_fiches_modifiees_6_mois (bigint), nb_fiches_modifiees_12_mois (bigint), nb_pap (bigint), passage_pap (text), owner_plan (text), url_plan (text), activite_depuis_pap (bigint), ct_tete (double precision), nb_fa (bigint), nb_fa_pilotables (bigint), nb_indicateur_perso (bigint), plans_type (text), pap_3_mois (text), pap_12_mois (text), pap_multiplan_3_mois (text), pap_multiplan_12_mois (text), note_plan (double precision), nombre_pap_bizdev (double precision), derniere_visite (text), user_derniere_visite (text), pipeline (text), semaine (text), semaine_passage_retention (text)
public.airtable_sync_semaine: collectivite_id (bigint), semaine (text), pipeline (text), semaine_passage_retention (text)
public.airtable_sync_semaine_old: collectivite_id (bigint), key (text), derniere_modif (text), derniere_creation_compte (text), top_contributeur (text), pageviews_plan (bigint), nb_contributeurs (bigint), nb_super_contributeurs (bigint), nb_contribution (bigint), note_max_pap (double precision), nb_pap (bigint), passage_pap (text), score (double precision), score_pilotabilite (double precision), score_indicateur (double precision), score_objectif (double precision), score_budget (double precision), score_avancement (double precision), score_referentiel (double precision), owner_plan (text), activite_depuis_pap (bigint), ct_tete (double precision), statut (text), nb_fa (bigint), nb_fa_pilotables (bigint), nb_indicateur_perso (bigint), plans_type (text), derniere_visite (text), pipeline (text), semaine (text)
public.audit: audit_id (bigint), collectivite_id (bigint), referentiel (text), audit_debut (timestamp with time zone), audit_fin (timestamp with time zone), date_cnl (timestamp with time zone), audit_valide (boolean), clos (boolean), type (text), valide_labellisation (boolean), date_demande (timestamp with time zone)
public.auditeur: user_id (text), audit_id (bigint), date_attribution (timestamp with time zone), nom_auditeur (text), prenom_auditeur (text), email_auditeur (text)
public.bizdev_A_F_contact: date (text), echange_type (text), collectivite_id (double precision)
public.bizdev_contact_collectivite: collectivite_id (bigint), date_contact (timestamp without time zone)
public.bizdev_note_de_suivi_contact: collectivite_id (bigint), date (timestamp without time zone)
public.calendly_events: uri (text), event_type (text), name (text), start_time (text), status (text), nb_participants_reel (bigint)
public.calendly_invitees: uri_event (text), email (text), status (text), reponse (text)
public.collectivite: collectivite_id (bigint), nom (text), type_collectivite (text), nature_collectivite (text), code_siren_insee (text), region_name (text), region_code (text), departement_name (text), departement_code (text), population_totale (bigint), departement_iso_3166 (text), region_iso_3166 (text), completude_cae (double precision), completude_eci (double precision), pa_pilotables (double precision), date_activation_tet (timestamp without time zone), activee (boolean)
public.cot: collectivite_id (bigint), actif (boolean), signataire (bigint)
public.crisp_conversation: session_id (text), nickname (text), email (text), segments (text), created_at (timestamp with time zone), updated_at (timestamp with time zone), operator (character varying)
public.crisp_nb_conversation: mois (timestamp without time zone), nb_conversation (bigint)
public.crisp_nb_message: mois (timestamp without time zone), nb_messages_operator (bigint), hits (bigint), unique_hits (bigint)
public.crisp_rating: mois (timestamp without time zone), rating (double precision), hits (bigint), unique_hits (bigint)
public.crisp_temps_reponse: mois (timestamp without time zone), response_time_h (double precision), hits (bigint), unique_hits (bigint)
public.crisp_temps_resoluton: mois (timestamp without time zone), temps_resolution_h (double precision), hits (bigint), unique_hits (bigint)
public.ct_actives: collectivite_id (bigint), nature_insee (text), type (text), nom (text), siren (text), departement_name (text), region_name (text), date_activation (timestamp with time zone), categorie (text)
public.evenements_airtable: index (bigint), Date (timestamp without time zone), evenements (text)
public.evolution_ind_od: mois (text), departement_name (text), region_name (text), nb_values_od_cum (double precision)
public.evolution_ind_pers: region_name (text), departement_name (text), mois (text), nb_ind_perso (double precision), nb_lignes (double precision), nb_ind_perso_ct (double precision)
public.evolution_labellisation: mois (timestamp without time zone), nb_labellisation_cumule (bigint)
public.fa_distrib: mois (timestamp without time zone), departement_name (text), action (bigint), action_pilotable (double precision), region_name (text), action_pilotable_actives (double precision), nb_fiches (double precision), realise (double precision)
public.fa_sharing: mois (timestamp without time zone), nb_fa_shared (bigint)
public.feature: datetime (timestamp with time zone), collectivite_id (bigint), email (text), sub-feature (json), feature (text)
public.fiche_action_plan: fiche_id (bigint), plan (bigint)
public.ind_od_producteur_indicateur: titre (text), producteur (text), departement_name (text), region_name (text)
public.internal_users: email (text)
public.labellisation: collectivite_id (bigint), obtenue_le (timestamp without time zone), referentiel (text), etoiles (bigint), score_realise (double precision), score_programme (double precision), points_potentiels (double precision)
public.labellisation_region: collectivite_id (bigint), referentiel (text), obtenue_le (timestamp without time zone), etoiles (bigint), departement_name (text), region_name (text)
public.labellisation_stock_evolution: year (bigint), referentiel (text), etoiles (bigint), departement_name (text), region_name (text), nb_collectivites (bigint)
public.mapping_levier_mesure: levier (text), mesure (text)
public.modelisation_impact: Secteur (text), Leviers SGPE (text), identifiant_referentiel (text), reduction (double precision), reduction_leveir (double precision), implication (double precision), reduction_theorique (double precision), justification (text), ids (text), collectivite_id (bigint), created_at (timestamp without time zone)
public.nb_fap_13: mois (text), statut (text), fiche_id (bigint)
public.nb_fap_52: mois (text), statut (text), fiche_id (bigint)
public.nb_fap_pilote_13: mois (text), statut (text), fiche_id (bigint)
public.nb_fap_pilote_52: mois (text), statut (text), fiche_id (bigint)
public.note_fiche_historique: fiche_id (bigint), collectivite_id (bigint), nom_ct (text), score_titre (bigint), score_description (bigint), score_statut (bigint), score_pilote (double precision), score_pilote_user (double precision), score_date_debut (double precision), score_date_fin (double precision), score_indicateur (bigint), score_objectif (double precision), score_budget (bigint), score_suivi (bigint), score_modif_12_mois (double precision), score_modif_6_mois (double precision), note_fa (double precision), mois (text)
public.note_fiche_historique_backup: fiche_id (bigint), collectivite_id (bigint), nom_ct (text), score_titre (bigint), score_description (bigint), score_statut (bigint), score_pilote (double precision), score_pilote_user (double precision), score_date_debut (double precision), score_date_fin (double precision), score_indicateur (bigint), score_objectif (double precision), score_budget (bigint), score_suivi (bigint), score_modif_12_mois (double precision), score_modif_6_mois (double precision), note_fa (double precision), mois (text)
public.note_plan_historique: plan (bigint), note_plan (double precision), mois (text)
public.note_plan_historique_backup: plan (bigint), note_plan (double precision), mois (text)
public.note_plan_semaine: plan (text), note_plan (numeric), semaine (date)
public.notion_ticket: id_ticket (text), titre (text), type_bug_support (text), thematique (text), criticite (text), impact_potentiel (text), statut (text), bloque (text), temps_resolution (double precision), createur_id (text), responsable (text), personnes_associees (text), email_utilisateur (text), id_collectivite (double precision), epic_name (text), tickets_lies (text), feedback (text), created_at (text), date_remontee_crisp (text), last_edited_at (text), url (text)
public.nps: nps (double precision)
public.pap_date_passage: collectivite_id (bigint), nom (text), plan (bigint), passage_pap (timestamp with time zone), type (double precision), nom_plan (text), nom_plan_ct (text), createur_plan (text), import (text)
public.pap_note: collectivite_id (bigint), plan_id (bigint), nom (text), type (double precision), nb_fiche_action_total (bigint), nom_ct (text), key (text), score_pilotabilite (double precision), score_budget (double precision), score_indicateur (double precision), score_objectif (double precision), score_avancement (double precision), score_referentiel (double precision), c_referentiel (double precision), score (double precision), etoiles_visuelles (text), semaine (text)
public.pap_note_backup: collectivite_id (bigint), plan_id (bigint), nom (text), type (double precision), nb_fiche_action_total (bigint), nom_ct (text), key (text), score_pilotabilite (double precision), score_budget (double precision), score_indicateur (double precision), score_objectif (double precision), score_avancement (double precision), score_referentiel (double precision), c_referentiel (double precision), score (double precision), etoiles_visuelles (text), semaine (text)
public.pap_note_region: collectivite_id (bigint), score (double precision), semaine (text), plan_id (bigint), nom_plan (text), departement_name (text), region_name (text), nom (text)
public.pap_note_snapshot: collectivite_id (bigint), plan_id (bigint), nom (text), type (double precision), nb_fiche_action_total (bigint), nom_ct (text), key (text), score_pilotabilite (double precision), score_budget (double precision), score_indicateur (double precision), score_objectif (double precision), score_avancement (double precision), score_referentiel (double precision), c_referentiel (double precision), score (double precision), etoiles_visuelles (text), semaine (text)
public.pap_statut_5_fiches_modifiees_13_semaines: mois (timestamp without time zone), plan (bigint), statut (text), collectivite_id (bigint), nb_pilotes (bigint)
public.pap_statut_5_fiches_modifiees_52_semaines: mois (timestamp without time zone), plan (bigint), statut (text), collectivite_id (bigint), nb_pilotes (bigint), nom_plan (text)
public.passage_pap_region: collectivite_id (bigint), nom_plan (text), plan (bigint), departement_name (text), region_name (text), mois (text)
public.pipeline: collectivite_id (bigint), pipeline (text), semaine (text)
public.plan_distrib: plan (bigint), departement_name (text), region_name (text), actif_12_mois (boolean), score_sup_5 (boolean), pilotable (boolean)
public.posthog_next_path: email (text), collectivite_id (text), timestamp (timestamp with time zone), next_timestamp (timestamp with time zone), next_path_clean (text), current_path_clean (text)
public.priorisation: id (bigint), collectivite_id (bigint), secteur (text), identifiant_referentiel (text), levier (text), categorie (smallint), note (smallint), ids (text), created_at (timestamp with time zone)
public.priorisation_action: id (integer), collectivite_id (integer), levier (text), categorie (integer), fiche_action_id (integer), created_at (timestamp with time zone), reference (boolean)
public.priorisation_action_reference: levier (text), categorie (bigint), titre (text), description (text), id (bigint)
public.priorisation_categorie_levier: categorie (bigint), Captage de méthane dans les ISDND (double precision), Biogaz (double precision), Véhicules électriques (double precision), Efficacité et carburants décarbonés des véhicules privés (double precision), Sobriété des bâtiments (résidentiel) (double precision), Pratiques stockantes (double precision), Changement chaudières gaz + rénovation (résidentiel) (double precision), Vélo et transport en commun (double precision), Bus et cars décarbonés (double precision), Changement de chaudière à fioul (tertiaire) (double precision), Réduction des déplacements (double precision), Sobriété et isolation des bâtiments (tertiaire) (double precision), Gestion des forêts et produits bois (double precision), Changements de pratiques de fertilisation azotée (double precision), Elevage durable (double precision), Bâtiments & Machines agricoles (double precision), Valorisation matière des déchets (double precision), Changement chaudières fioul + rénovation (résidentiel) (double precision), Gestion des haies (double precision), Sobriété foncière (double precision), Réseaux de chaleur décarbonés (double precision), Prévention des déchets (double precision), Changement de chaudière à gaz (tertiaire) (double precision), Fret décarboné et multimodalité (double precision), Electricité renouvelable (double precision), Efficacité et sobriété logistique (double precision), Covoiturage (double precision), Production Industrielle (double precision), Gestion des prairies (double precision)
public.priorisation_faisabilite: id (integer), collectivite_id (integer), levier (text), categorie (integer), faisabilite (integer), created_at (timestamp with time zone)
public.priorisation_hors_competence: id (integer), collectivite_id (integer), levier (text), categorie (integer), created_at (timestamp with time zone)
public.priorisation_reduction_levier: id (integer), collectivite_id (integer), levier (text), reduction (double precision), created_at (timestamp without time zone)
public.score_snapshot: siren (text), nom (text), referentiel_id (text), sujet (text), date_fin_audit (timestamp with time zone), date (timestamp with time zone), type_jalon (text), point_fait (double precision), point_programme (double precision), point_pas_fait (double precision), point_potentiel (double precision), etoiles (bigint)
public.stats_hero_section_site: nb_ct_actif_12_mois (bigint), nb_user_actif_12_mois (bigint), nb_pap_actif_12_mois (bigint), nb_action_pilotable_active_12_mois (bigint)
public.statut_fiche_13_semaines: fiche_id (bigint), mois (text), statut (text)
public.statut_fiche_52_semaines: fiche_id (bigint), mois (text), statut (text)
public.taux_contact_support: month (timestamp without time zone), taux_support_bug_% (double precision)
public.tmp_backup_indicateur_source_metadonnee: id (bigint), source_id (text), date_version (timestamp without time zone), nom_donnees (text), diffuseur (text), producteur (text), methodologie (text), limites (text)
public.tmp_backup_indicateur_valeur: id (bigint), indicateur_id (bigint), collectivite_id (bigint), date_valeur (timestamp without time zone), metadonnee_id (bigint), resultat (double precision), resultat_commentaire (text), objectif (text), objectif_commentaire (text), estimation (text), modified_at (timestamp with time zone), created_at (timestamp with time zone), modified_by (text), created_by (text), calcul_auto (boolean), calcul_auto_identifiants_manquants (text)
public.tr_comm: id_tech_comm (bigint), cd_comm (text), lb_comm_majs (text), cd_sirn_comm (double precision)
public.url_posthog: distinct_id (text), session_id (text), current_url (text), email (text), collectivite_id (text), timestamp (text)
public.user_actif_12_mois: mois (timestamp without time zone), collectivite_id (double precision), email (text)
public.user_actifs_ct_mois: mois (text), collectivite_id (bigint), email (text), departement_name (text), region_name (text)
public.utilisateurs: user_id (text), nom (text), prenom (text), email (text), telephone (text)
public.utilisateurs_droits: user_id (text), collectivite_id (bigint), fonction (text), details_fonction (text), est_referent (boolean), champ_intervention (text), niveau_acces (text), date_creation (timestamp with time zone), invitation (boolean)
public.visite_annuelle: collectivite_id (bigint), derniere_date (timestamp with time zone)
"""