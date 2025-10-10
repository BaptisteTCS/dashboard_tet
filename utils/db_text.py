relations_text = """
fiche_action_pilote — relations :
  historique.fiche_action_pilote.fiche_historise_id → historique.fiche_action.id
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
action_discussion — relations :
  public.action_discussion.action_id → public.action_relation.id
  public.action_discussion.collectivite_id → public.collectivite.id
  public.action_discussion.created_by → auth.users.id
action_discussion_commentaire — relations :
  public.action_discussion_commentaire.created_by → auth.users.id
  public.action_discussion_commentaire.discussion_id → public.action_discussion.id
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
auth.users: recovery_sent_at (timestamp with time zone), recovery_token (character varying), confirmation_sent_at (timestamp with time zone), confirmation_token (character varying), invited_at (timestamp with time zone), email_confirmed_at (timestamp with time zone), encrypted_password (character varying), email (character varying), role (character varying), aud (character varying), id (uuid), instance_id (uuid), email_change_sent_at (timestamp with time zone), last_sign_in_at (timestamp with time zone), raw_app_meta_data (jsonb), raw_user_meta_data (jsonb), is_super_admin (boolean), created_at (timestamp with time zone), updated_at (timestamp with time zone), phone (text), phone_confirmed_at (timestamp with time zone), phone_change (text), phone_change_token (character varying), phone_change_sent_at (timestamp with time zone), confirmed_at (timestamp with time zone), is_anonymous (boolean), deleted_at (timestamp with time zone), is_sso_user (boolean), reauthentication_token (character varying), reauthentication_sent_at (timestamp with time zone), banned_until (timestamp with time zone), email_change_token_current (character varying), email_change_confirm_status (smallint), email_change (character varying), email_change_token_new (character varying)
historique.action_statut: id (integer), collectivite_id (integer), action_id (character varying), avancement (USER-DEFINED), previous_avancement (USER-DEFINED), avancement_detaille (ARRAY), previous_avancement_detaille (ARRAY), concerne (boolean), previous_concerne (boolean), modified_by (uuid), previous_modified_by (uuid), modified_at (timestamp with time zone), previous_modified_at (timestamp with time zone)
historique.fiche_action: previous_piliers_eci (ARRAY), piliers_eci (ARRAY), previous_description (character varying), description (character varying), previous_titre (character varying), titre (character varying), fiche_id (integer), id (integer), resultats_attendus (ARRAY), deleted (boolean), previous_restreint (boolean), restreint (boolean), previous_modified_by (uuid), modified_by (uuid), previous_modified_at (timestamp with time zone), modified_at (timestamp with time zone), created_at (timestamp with time zone), collectivite_id (integer), previous_maj_termine (boolean), maj_termine (boolean), previous_notes_complementaires (character varying), notes_complementaires (character varying), previous_calendrier (character varying), calendrier (character varying), previous_amelioration_continue (boolean), amelioration_continue (boolean), previous_date_fin_provisoire (timestamp with time zone), date_fin_provisoire (timestamp with time zone), previous_date_debut (timestamp with time zone), date_debut (timestamp with time zone), previous_niveau_priorite (text), niveau_priorite (text), previous_statut (text), statut (text), previous_budget_previsionnel (numeric), budget_previsionnel (numeric), previous_financements (text), financements (text), previous_ressources (character varying), ressources (character varying), previous_cibles (ARRAY), cibles (ARRAY), previous_resultats_attendus (ARRAY), previous_objectifs (character varying), objectifs (character varying)
historique.fiche_action_pilote: user_id (uuid), tag_nom (text), previous (boolean), id (integer), fiche_historise_id (integer)
public.action_commentaire: modified_by (uuid), modified_at (timestamp with time zone), collectivite_id (integer), action_id (character varying), commentaire (text)
public.action_definition: perimetre_evaluation (text), modified_at (timestamp with time zone), action_id (character varying), reduction_potentiel (text), pourcentage (double precision), points (double precision), preuve (text), ressources (text), exemples (text), contexte (text), description (text), nom (text), referentiel (USER-DEFINED), identifiant (text), expr_score (text), referentiel_version (character varying), referentiel_id (character varying), categorie (USER-DEFINED)
public.action_definition_tag: tag_ref (character varying), referentiel_id (character varying), action_id (character varying)
public.action_discussion: created_at (timestamp with time zone), modified_at (timestamp with time zone), status (USER-DEFINED), created_by (uuid), action_id (character varying), collectivite_id (integer), id (integer)
public.action_discussion_commentaire: message (text), id (integer), created_by (uuid), created_at (timestamp with time zone), discussion_id (integer)
public.action_discussion_feed: created_by (uuid), commentaires (ARRAY), status (USER-DEFINED), modified_at (timestamp with time zone), id (integer), collectivite_id (integer), action_id (character varying), created_at (timestamp with time zone)
public.action_pilote: user_id (uuid), action_id (character varying), collectivite_id (integer), tag_id (integer)
public.action_relation: id (character varying), referentiel (USER-DEFINED), parent (character varying)
public.action_score_indicateur_valeur: action_id (character varying), indicateur_valeur_id (integer), type_score (text), collectivite_id (integer), indicateur_id (integer)
public.action_service: service_tag_id (integer), action_id (character varying), collectivite_id (integer)
public.action_statut: collectivite_id (integer), action_id (character varying), avancement (USER-DEFINED), concerne (boolean), modified_by (uuid), modified_at (timestamp with time zone), avancement_detaille (ARRAY)
public.axe: modified_at (timestamp with time zone), id (integer), nom (text), collectivite_id (integer), parent (integer), created_at (timestamp with time zone), modified_by (uuid), plan (integer), type (integer), panier_id (uuid)
public.banatic_competence: code (integer), nom (text)
public.categorie_tag: id (integer), groupement_id (integer), collectivite_id (integer), nom (text), visible (boolean), created_at (timestamp with time zone), created_by (uuid)
public.collectivite: id (integer), created_at (timestamp with time zone), modified_at (timestamp with time zone), access_restreint (boolean), nom (text), type (text), commune_code (character varying), siren (character varying), departement_code (character varying), region_code (character varying), nature_insee (text), population (integer), dans_aire_urbaine (boolean), nic (character varying)
public.collectivite_banatic_competence: collectivite_id (integer), competence_code (integer)
public.collectivite_banatic_type: type (text), id (text), nom (text)
public.collectivite_bucket: collectivite_id (integer), bucket_id (text)
public.collectivite_carte_identite: collectivite_id (integer), is_cot (boolean), population_totale (integer), population_source (text), departement_name (character varying), region_name (character varying), code_siren_insee (character varying), type_collectivite (text), nom (text)
public.collectivite_identite: type (ARRAY), population (ARRAY), id (integer), localisation (ARRAY)
public.collectivite_niveau_acces: niveau_acces (USER-DEFINED), access_restreint (boolean), est_auditeur (boolean), nom (character varying), collectivite_id (integer)
public.collectivite_relations: id (integer), parent_id (integer)
public.commune: code (character varying), collectivite_id (integer), id (integer), nom (character varying)
public.comparaison_scores_audit: collectivite_id (integer), pre_audit (USER-DEFINED), referentiel (USER-DEFINED), action_id (character varying), courant (USER-DEFINED)
public.cot: actif (boolean), signataire (integer), collectivite_id (integer)
public.effet_attendu: notice (text), nom (text), id (integer)
public.fiche_action: modified_at (timestamp with time zone), piliers_eci (ARRAY), description (character varying), titre (character varying), id (integer), created_by (uuid), temps_de_mise_en_oeuvre_id (integer), participation_citoyenne_type (character varying), participation_citoyenne (text), instance_gouvernance (text), restreint (boolean), modified_by (uuid), created_at (timestamp with time zone), collectivite_id (integer), maj_termine (boolean), notes_complementaires (character varying), calendrier (character varying), amelioration_continue (boolean), date_fin_provisoire (timestamp with time zone), date_debut (timestamp with time zone), niveau_priorite (USER-DEFINED), statut (USER-DEFINED), budget_previsionnel (numeric), financements (text), ressources (character varying), cibles (ARRAY), resultats_attendus (ARRAY), objectifs (character varying)
public.fiche_action_action: action_id (character varying), fiche_id (integer)
public.fiche_action_axe: fiche_id (integer), axe_id (integer)
public.fiche_action_budget: fiche_id (integer), id (integer), type (text), unite (text), annee (integer), budget_previsionnel (numeric), budget_reel (numeric), est_etale (boolean)
public.fiche_action_effet_attendu: fiche_id (integer), effet_attendu_id (integer)
public.fiche_action_etape: nom (text), fiche_id (integer), id (integer), created_by (uuid), modified_by (uuid), created_at (timestamp with time zone), modified_at (timestamp with time zone), realise (boolean), ordre (integer)
public.fiche_action_financeur_tag: montant_ttc (integer), fiche_id (integer), id (integer), financeur_tag_id (integer)
public.fiche_action_import_csv: notes (text), montant_trois (text), financeur_trois (text), montant_deux (text), financeur_deux (text), montant_un (text), financeur_un (text), service (text), plan_nom (text), axe (text), sous_axe (text), sous_sous_axe (text), num_action (text), titre (text), description (text), objectifs (text), resultats_attendus (text), cibles (text), structure_pilote (text), moyens (text), partenaires (text), personne_referente (text), elu_referent (text), financements (text), budget (text), statut (text), priorite (text), date_debut (text), date_fin (text), amelioration_continue (text), calendrier (text), collectivite_id (text)
public.fiche_action_indicateur: indicateur_id (integer), fiche_id (integer)
public.fiche_action_libre_tag: fiche_id (integer), created_at (timestamp with time zone), libre_tag_id (integer), created_by (uuid)
public.fiche_action_lien: fiche_deux (integer), fiche_une (integer)
public.fiche_action_note: created_at (timestamp with time zone), date_note (date), fiche_id (integer), note (text), id (integer), created_by (uuid), modified_by (uuid), modified_at (timestamp with time zone)
public.fiche_action_partenaire_tag: partenaire_tag_id (integer), fiche_id (integer)
public.fiche_action_personne_pilote: user_id (uuid), tag_id (integer), nom (text), collectivite_id (integer)
public.fiche_action_personne_referente: user_id (uuid), tag_id (integer), collectivite_id (integer), nom (text)
public.fiche_action_pilote: user_id (uuid), fiche_id (integer), tag_id (integer)
public.fiche_action_referent: user_id (uuid), fiche_id (integer), tag_id (integer)
public.fiche_action_service_tag: fiche_id (integer), service_tag_id (integer)
public.fiche_action_sharing: created_at (timestamp with time zone), fiche_id (integer), created_by (uuid), collectivite_id (integer)
public.fiche_action_sous_thematique: thematique_id (integer), fiche_id (integer)
public.fiche_action_structure_tag: fiche_id (integer), structure_tag_id (integer)
public.fiche_action_thematique: thematique_id (integer), fiche_id (integer)
public.financeur_tag: collectivite_id (integer), nom (text), id (integer)
public.groupement: id (integer), nom (text)
public.groupement_collectivite: collectivite_id (integer), groupement_id (integer)
public.indicateur_action: action_id (character varying), indicateur_id (integer)
public.indicateur_artificialisation: mixte (double precision), habitat (double precision), activite (double precision), total (double precision), collectivite_id (integer), routiere (double precision), ferroviaire (double precision), inconnue (double precision)
public.indicateur_categorie_tag: categorie_tag_id (integer), indicateur_id (integer)
public.indicateur_collectivite: collectivite_id (integer), indicateur_id (integer), modified_at (timestamp with time zone), modified_by (uuid), confidentiel (boolean), favoris (boolean), commentaire (text)
public.indicateur_definition: modified_by (uuid), libelle_cible_seuil (text), expr_seuil (text), expr_cible (text), precision (integer), version (character varying), titre_court (text), id (integer), groupement_id (integer), collectivite_id (integer), identifiant_referentiel (text), titre (text), titre_long (text), description (text), unite (text), borne_min (double precision), borne_max (double precision), participation_score (boolean), sans_valeur_utilisateur (boolean), valeur_calcule (text), modified_at (timestamp with time zone), created_at (timestamp with time zone), created_by (uuid)
public.indicateur_groupe: enfant (integer), parent (integer)
public.indicateur_objectif: date_valeur (date), indicateur_id (integer), formule (text)
public.indicateur_pilote: tag_id (integer), user_id (uuid), indicateur_id (integer), id (integer), collectivite_id (integer)
public.indicateur_service_tag: collectivite_id (integer), indicateur_id (integer), service_tag_id (integer)
public.indicateur_source: ordre_affichage (integer), id (text), libelle (text)
public.indicateur_source_metadonnee: source_id (text), id (integer), limites (text), methodologie (text), producteur (text), diffuseur (text), nom_donnees (text), date_version (timestamp without time zone)
public.indicateur_source_source_calcul: source_calcul_id (text), source_id (text)
public.indicateur_sous_thematique: sous_thematique_id (integer), indicateur_id (integer)
public.indicateur_thematique: thematique_id (integer), indicateur_id (integer)
public.indicateur_valeur: date_valeur (date), collectivite_id (integer), indicateur_id (integer), id (integer), calcul_auto_identifiants_manquants (ARRAY), calcul_auto (boolean), created_by (uuid), modified_by (uuid), created_at (timestamp with time zone), modified_at (timestamp with time zone), estimation (double precision), objectif_commentaire (text), objectif (double precision), resultat_commentaire (text), resultat (double precision), metadonnee_id (integer)
public.labellisation: score_programme (double precision), id (integer), collectivite_id (integer), obtenue_le (timestamp without time zone), etoiles (integer), annee (double precision), score_realise (double precision), referentiel (USER-DEFINED)
public.libre_tag: created_by (uuid), created_at (timestamp with time zone), collectivite_id (integer), nom (text), id (integer)
public.partenaire_tag: collectivite_id (integer), id (integer), nom (text)
public.personne_tag: id (integer), nom (text), collectivite_id (integer)
public.plan_pilote: user_id (uuid), plan_id (integer), tag_id (integer), created_at (timestamp with time zone), created_by (uuid)
public.plan_referent: plan_id (integer), tag_id (integer), user_id (uuid), created_at (timestamp with time zone), created_by (uuid)
public.private_collectivite_membre: created_at (timestamp with time zone), est_referent (boolean), user_id (uuid), collectivite_id (integer), fonction (USER-DEFINED), details_fonction (text), champ_intervention (ARRAY), modified_at (timestamp with time zone)
public.private_utilisateur_droit: niveau_acces (USER-DEFINED), id (integer), user_id (uuid), collectivite_id (integer), active (boolean), created_at (timestamp with time zone), modified_at (timestamp with time zone), invitation_id (uuid)
public.referentiel_definition: id (character varying), locked (boolean), modified_at (timestamp with time zone), created_at (timestamp with time zone), hierarchie (ARRAY), version (character varying), nom (character varying)
public.referentiel_json: created_at (timestamp with time zone), children (jsonb), definitions (jsonb)
public.referentiel_tag: type (character varying), nom (character varying), ref (character varying)
public.score_snapshot: modified_at (timestamp with time zone), collectivite_id (integer), referentiel_id (character varying), referentiel_version (character varying), audit_id (integer), date (timestamp with time zone), ref (character varying), nom (character varying), type_jalon (character varying), point_fait (double precision), point_programme (double precision), point_pas_fait (double precision), point_potentiel (double precision), referentiel_scores (jsonb), personnalisation_reponses (jsonb), created_by (uuid), created_at (timestamp with time zone), modified_by (uuid)
public.service_tag: collectivite_id (integer), id (integer), nom (text)
public.structure_tag: collectivite_id (integer), nom (text), id (integer)
"""