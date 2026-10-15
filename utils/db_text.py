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
bibliotheque_fichier — relations :
  labellisation.bibliotheque_fichier.collectivite_id → public.collectivite.id
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
action_computed_points — relations :
  public.action_computed_points.action_id → public.action_relation.id
action_de_reference_fiche — relations :
  public.action_de_reference_fiche.action_de_reference_id → public.action_de_reference.id
  public.action_de_reference_fiche.fiche_id → public.fiche_action.id
action_definition — relations :
  public.action_definition.action_id → public.action_relation.id
  public.action_definition.referentiel_id → public.referentiel_definition.id
action_definition_tag — relations :
  public.action_definition_tag.action_id → public.action_relation.id
  public.action_definition_tag.referentiel_id → public.referentiel_definition.id
  public.action_definition_tag.tag_ref → public.referentiel_tag.ref
action_impact — relations :
  public.action_impact.fourchette_budgetaire → public.action_impact_fourchette_budgetaire.niveau
  public.action_impact.impact_tier → public.action_impact_tier.niveau
  public.action_impact.temps_de_mise_en_oeuvre → public.action_impact_temps_de_mise_en_oeuvre.niveau
  public.action_impact.typologie_id → public.action_impact_typologie.id
action_impact_action — relations :
  public.action_impact_action.action_id → public.action_definition.action_id
  public.action_impact_action.action_impact_id → public.action_impact.id
action_impact_banatic_competence — relations :
  public.action_impact_banatic_competence.action_impact_id → public.action_impact.id
  public.action_impact_banatic_competence.competence_code → public.banatic_competence.code
action_impact_categorie_fnv — relations :
  public.action_impact_categorie_fnv.action_impact_id → public.action_impact.id
  public.action_impact_categorie_fnv.categorie_fnv_id → public.categorie_fnv.id
action_impact_effet_attendu — relations :
  public.action_impact_effet_attendu.action_impact_id → public.action_impact.id
  public.action_impact_effet_attendu.effet_attendu_id → public.effet_attendu.id
action_impact_fiche_action — relations :
  public.action_impact_fiche_action.action_impact_id → public.action_impact.id
  public.action_impact_fiche_action.fiche_id → public.fiche_action.id
action_impact_indicateur — relations :
  public.action_impact_indicateur.action_impact_id → public.action_impact.id
  public.action_impact_indicateur.indicateur_id → public.indicateur_definition.id
action_impact_panier — relations :
  public.action_impact_panier.action_id → public.action_impact.id
  public.action_impact_panier.panier_id → public.panier.id
action_impact_partenaire — relations :
  public.action_impact_partenaire.action_impact_id → public.action_impact.id
  public.action_impact_partenaire.partenaire_id → public.panier_partenaire.id
action_impact_sous_thematique — relations :
  public.action_impact_sous_thematique.action_impact_id → public.action_impact.id
  public.action_impact_sous_thematique.sous_thematique_id → public.sous_thematique.id
action_impact_statut — relations :
  public.action_impact_statut.action_id → public.action_impact.id
  public.action_impact_statut.categorie_id → public.action_impact_categorie.id
  public.action_impact_statut.panier_id → public.panier.id
action_impact_thematique — relations :
  public.action_impact_thematique.action_impact_id → public.action_impact.id
  public.action_impact_thematique.thematique_id → public.thematique.id
action_origine — relations :
  public.action_origine.action_id → public.action_relation.id
  public.action_origine.origine_action_id → public.action_relation.id
  public.action_origine.origine_referentiel_id → public.referentiel_definition.id
  public.action_origine.referentiel_id → public.referentiel_definition.id
action_origine_texte — relations :
  public.action_origine_texte.action_id → public.action_relation.id
  public.action_origine_texte.origine_action_id → public.action_relation.id
  public.action_origine_texte.origine_referentiel_id → public.referentiel_definition.id
  public.action_origine_texte.referentiel_id → public.referentiel_definition.id
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
ai_plan_import_job — relations :
  public.ai_plan_import_job.collectivite_id → public.collectivite.id
  public.ai_plan_import_job.created_by → auth.users.id
  public.ai_plan_import_job.created_plan_id → public.axe.id
  public.ai_plan_import_job.fichier_id → labellisation.bibliotheque_fichier.id
ai_plan_import_step_run — relations :
  public.ai_plan_import_step_run.job_id → public.ai_plan_import_job.id
annexe — relations :
  public.annexe.fiche_id → public.fiche_action.id
audit_auditeur — relations :
  public.audit_auditeur.audit_id → labellisation.audit.id
  public.audit_auditeur.auditeur → auth.users.id
audit_preuves_archive — relations :
  public.audit_preuves_archive.audit_id → labellisation.audit.id
  public.audit_preuves_archive.collectivite_id → public.collectivite.id
  public.audit_preuves_archive.requested_by → auth.users.id
axe — relations :
  public.axe.collectivite_id → public.collectivite.id
  public.axe.modified_by → auth.users.id
  public.axe.panier_id → public.panier.id
  public.axe.parent → public.axe.id
  public.axe.plan → public.axe.id
  public.axe.type → public.plan_action_type.id
  public.axe.verified_by → auth.users.id
axe_indicateur — relations :
  public.axe_indicateur.axe_id → public.axe.id
  public.axe_indicateur.created_by → auth.users.id
  public.axe_indicateur.indicateur_id → public.indicateur_definition.id
banatic_2021_2025_crosswalk — relations :
  public.banatic_2021_2025_crosswalk.code_2021 → public.banatic_competence.code
  public.banatic_2021_2025_crosswalk.code_2025 → public.banatic_2025_competence.competence_code
banner_info — relations :
  public.banner_info.modified_by → public.dcp.user_id
categorie_tag — relations :
  public.categorie_tag.collectivite_id → public.collectivite.id
  public.categorie_tag.created_by → auth.users.id
  public.categorie_tag.groupement_id → public.groupement.id
client_scores — relations :
  public.client_scores.collectivite_id → public.collectivite.id
collectivite — relations :
  public.collectivite.nature_insee → public.collectivite_banatic_type.id
  public.collectivite.sinoe_id → public.typologie_sinoe.id
collectivite_banatic_2025_competence — relations :
  public.collectivite_banatic_2025_competence.collectivite_id → public.collectivite.id
  public.collectivite_banatic_2025_competence.competence_code → public.banatic_2025_competence.competence_code
collectivite_banatic_2025_perimetre — relations :
  public.collectivite_banatic_2025_perimetre.collectivite_id → public.collectivite.id
collectivite_banatic_2025_transfert — relations :
  public.collectivite_banatic_2025_transfert.collectivite_id → public.collectivite.id
  public.collectivite_banatic_2025_transfert.competence_code → public.banatic_2025_competence.competence_code
collectivite_banatic_competence — relations :
  public.collectivite_banatic_competence.collectivite_id → public.collectivite.id
  public.collectivite_banatic_competence.competence_code → public.banatic_competence.code
collectivite_bucket — relations :
  public.collectivite_bucket.collectivite_id → public.collectivite.id
collectivite_levier_ges_pertinence — relations :
  public.collectivite_levier_ges_pertinence.collectivite_id → public.collectivite.id
  public.collectivite_levier_ges_pertinence.modified_by → auth.users.id
collectivite_perimetre_secondaire — relations :
  public.collectivite_perimetre_secondaire.collectivite_id → public.collectivite.id
collectivite_relations — relations :
  public.collectivite_relations.id → public.collectivite.id
  public.collectivite_relations.parent_id → public.collectivite.id
collectivite_test — relations :
  public.collectivite_test.collectivite_id → public.collectivite.id
collectivite_volet_ges — relations :
  public.collectivite_volet_ges.collectivite_id → public.collectivite.id
commune — relations :
  public.commune.collectivite_id → public.collectivite.id
cot — relations :
  public.cot.collectivite_id → public.collectivite.id
  public.cot.signataire → public.collectivite.id
dcp — relations :
  public.dcp.user_id → auth.users.id
demarche — relations :
  public.demarche.collectivite_id → public.collectivite.id
  public.demarche.created_by → auth.users.id
demarche_document — relations :
  public.demarche_document.collectivite_id → public.collectivite.id
  public.demarche_document.demarche_id → public.demarche.id
  public.demarche_document.document_id → public.demarche_document_definition.id
demarche_document_additional — relations :
  public.demarche_document_additional.collectivite_id → public.collectivite.id
  public.demarche_document_additional.demarche_id → public.demarche.id
demarche_document_substitution — relations :
  public.demarche_document_substitution.document_id → public.demarche_document_definition.id
  public.demarche_document_substitution.substitut_id → public.demarche_document_definition.id
demarche_pcaet_avis — relations :
  public.demarche_pcaet_avis.demande_avis_id → public.demarche_pcaet_demande_avis.id
  public.demarche_pcaet_avis.depose_par → auth.users.id
  public.demarche_pcaet_avis.emetteur_collectivite_id → public.collectivite.id
demarche_pcaet_demande_avis — relations :
  public.demarche_pcaet_demande_avis.demarche_id → public.demarche.id
  public.demarche_pcaet_demande_avis.instructeur_collectivite_id → public.collectivite.id
demarche_pcaet_source_metadonnee — relations :
  public.demarche_pcaet_source_metadonnee.collectivite_id → public.collectivite.id
  public.demarche_pcaet_source_metadonnee.demarche_id → public.demarche.id
  public.demarche_pcaet_source_metadonnee.metadonnee_id → public.indicateur_source_metadonnee.id
demarche_pcaet_vulnerabilite_thematique — relations :
  public.demarche_pcaet_vulnerabilite_thematique.collectivite_id → public.collectivite.id
  public.demarche_pcaet_vulnerabilite_thematique.parent_id → public.demarche_pcaet_vulnerabilite_thematique.id
demarche_pcaet_vulnerabilite_valeur — relations :
  public.demarche_pcaet_vulnerabilite_valeur.demarche_id → public.demarche.id
  public.demarche_pcaet_vulnerabilite_valeur.thematique_id → public.demarche_pcaet_vulnerabilite_thematique.id
demarche_pilote — relations :
  public.demarche_pilote.demarche_id → public.demarche.id
  public.demarche_pilote.tag_id → public.personne_tag.id
  public.demarche_pilote.user_id → public.dcp.user_id
demarche_plan_action — relations :
  public.demarche_plan_action.demarche_id → public.demarche.id
  public.demarche_plan_action.plan_action_id → public.axe.id
demarche_status_history — relations :
  public.demarche_status_history.demarche_id → public.demarche.id
discussion — relations :
  public.discussion.action_id → public.action_relation.id
  public.discussion.collectivite_id → public.collectivite.id
  public.discussion.created_by → auth.users.id
discussion_message — relations :
  public.discussion_message.created_by → auth.users.id
  public.discussion_message.discussion_id → public.discussion.id
epci — relations :
  public.epci.collectivite_id → public.collectivite.id
fiche_action — relations :
  public.fiche_action.collectivite_id → public.collectivite.id
  public.fiche_action.created_by → auth.users.id
  public.fiche_action.modified_by → auth.users.id
  public.fiche_action.parent_id → public.fiche_action.id
  public.fiche_action.temps_de_mise_en_oeuvre_id → public.action_impact_temps_de_mise_en_oeuvre.niveau
fiche_action_action — relations :
  public.fiche_action_action.action_id → public.action_relation.id
  public.fiche_action_action.fiche_id → public.fiche_action.id
fiche_action_analysis — relations :
  public.fiche_action_analysis.collectivite_id → public.collectivite.id
  public.fiche_action_analysis.fiche_id → public.fiche_action.id
fiche_action_axe — relations :
  public.fiche_action_axe.axe_id → public.axe.id
  public.fiche_action_axe.created_by → auth.users.id
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
  public.fiche_action_indicateur.created_by → auth.users.id
  public.fiche_action_indicateur.fiche_id → public.fiche_action.id
  public.fiche_action_indicateur.indicateur_id → public.indicateur_definition.id
fiche_action_instance_de_gouvernance_tag — relations :
  public.fiche_action_instance_de_gouvernance_tag.created_by → auth.users.id
  public.fiche_action_instance_de_gouvernance_tag.fiche_action_id → public.fiche_action.id
  public.fiche_action_instance_de_gouvernance_tag.instance_de_gouvernance_tag_id → public.instance_de_gouvernance_tag.id
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
  public.fiche_action_pilote.created_by → auth.users.id
  public.fiche_action_pilote.fiche_id → public.fiche_action.id
  public.fiche_action_pilote.tag_id → public.personne_tag.id
  public.fiche_action_pilote.user_id → public.dcp.user_id
fiche_action_referent — relations :
  public.fiche_action_referent.created_by → auth.users.id
  public.fiche_action_referent.fiche_id → public.fiche_action.id
  public.fiche_action_referent.tag_id → public.personne_tag.id
  public.fiche_action_referent.user_id → public.dcp.user_id
fiche_action_secteur_attribution — relations :
  public.fiche_action_secteur_attribution.fiche_id → public.fiche_action.id
  public.fiche_action_secteur_attribution.modified_by → auth.users.id
fiche_action_service_tag — relations :
  public.fiche_action_service_tag.fiche_id → public.fiche_action.id
  public.fiche_action_service_tag.service_tag_id → public.service_tag.id
fiche_action_sharing — relations :
  public.fiche_action_sharing.collectivite_id → public.collectivite.id
  public.fiche_action_sharing.created_by → auth.users.id
  public.fiche_action_sharing.fiche_id → public.fiche_action.id
fiche_action_sous_thematique — relations :
  public.fiche_action_sous_thematique.created_by → auth.users.id
  public.fiche_action_sous_thematique.fiche_id → public.fiche_action.id
  public.fiche_action_sous_thematique.thematique_id → public.sous_thematique.id
fiche_action_structure_tag — relations :
  public.fiche_action_structure_tag.fiche_id → public.fiche_action.id
  public.fiche_action_structure_tag.structure_tag_id → public.structure_tag.id
fiche_action_thematique — relations :
  public.fiche_action_thematique.created_by → auth.users.id
  public.fiche_action_thematique.fiche_id → public.fiche_action.id
  public.fiche_action_thematique.thematique_id → public.thematique.id
fiche_action_volet_ges — relations :
  public.fiche_action_volet_ges.fiche_id → public.fiche_action.id
financeur_tag — relations :
  public.financeur_tag.collectivite_id → public.collectivite.id
  public.financeur_tag.created_by → public.dcp.user_id
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
indicateur_vue — relations :
  public.indicateur_vue.collectivite_id → public.collectivite.id
  public.indicateur_vue.created_by → auth.users.id
  public.indicateur_vue.modified_by → auth.users.id
instance_de_gouvernance_tag — relations :
  public.instance_de_gouvernance_tag.collectivite_id → public.collectivite.id
  public.instance_de_gouvernance_tag.created_by → public.dcp.user_id
justification — relations :
  public.justification.modified_by → auth.users.id
  public.justification.question_id → public.question.id
justification_ajustement — relations :
  public.justification_ajustement.action_id → public.action_relation.id
  public.justification_ajustement.collectivite_id → public.collectivite.id
  public.justification_ajustement.modified_by → auth.users.id
labellisation — relations :
  public.labellisation.audit_id → labellisation.audit.id
  public.labellisation.collectivite_id → public.collectivite.id
labellisation_action_critere — relations :
  public.labellisation_action_critere.action_id → public.action_relation.id
libre_tag — relations :
  public.libre_tag.collectivite_id → public.collectivite.id
  public.libre_tag.created_by → auth.users.id
panier — relations :
  public.panier.collectivite_id → public.collectivite.id
  public.panier.collectivite_preset → public.collectivite.id
  public.panier.created_by → auth.users.id
partenaire_tag — relations :
  public.partenaire_tag.collectivite_id → public.collectivite.id
  public.partenaire_tag.created_by → public.dcp.user_id
personnalisation_consequence — relations :
  public.personnalisation_consequence.collectivite_id → public.collectivite.id
personnalisation_regle — relations :
  public.personnalisation_regle.action_id → public.action_definition.action_id
personne_tag — relations :
  public.personne_tag.collectivite_id → public.collectivite.id
  public.personne_tag.created_by → public.dcp.user_id
plan_action_type — relations :
  public.plan_action_type.categorie → public.plan_action_type_categorie.categorie
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
plan_report_generation — relations :
  public.plan_report_generation.collectivite_id → public.collectivite.id
  public.plan_report_generation.created_by → auth.users.id
  public.plan_report_generation.file_id → labellisation.bibliotheque_fichier.id
  public.plan_report_generation.plan_id → public.axe.id
post_audit_scores — relations :
  public.post_audit_scores.audit_id → labellisation.audit.id
pre_audit_scores — relations :
  public.pre_audit_scores.audit_id → labellisation.audit.id
preuve_action — relations :
  public.preuve_action.action_id → public.action_relation.id
  public.preuve_action.preuve_id → public.preuve_reglementaire_definition.id
preuve_audit — relations :
  public.preuve_audit.audit_id → labellisation.audit.id
  public.preuve_audit.collectivite_id → public.collectivite.id
preuve_complementaire — relations :
  public.preuve_complementaire.action_id → public.action_relation.id
  public.preuve_complementaire.collectivite_id → public.collectivite.id
preuve_labellisation — relations :
  public.preuve_labellisation.collectivite_id → public.collectivite.id
  public.preuve_labellisation.demande_id → labellisation.demande.id
preuve_rapport — relations :
  public.preuve_rapport.collectivite_id → public.collectivite.id
preuve_reglementaire — relations :
  public.preuve_reglementaire.collectivite_id → public.collectivite.id
  public.preuve_reglementaire.preuve_id → public.preuve_reglementaire_definition.id
private_collectivite_membre — relations :
  public.private_collectivite_membre.collectivite_id → public.collectivite.id
  public.private_collectivite_membre.user_id → auth.users.id
private_utilisateur_droit — relations :
  public.private_utilisateur_droit.collectivite_id → public.collectivite.id
  public.private_utilisateur_droit.user_id → auth.users.id
question — relations :
  public.question.competence_code → public.banatic_2025_competence.competence_code
  public.question.thematique_id → public.question_thematique.id
question_action — relations :
  public.question_action.action_id → public.action_relation.id
  public.question_action.question_id → public.question.id
question_choix — relations :
  public.question_choix.question_id → public.question.id
reponse_binaire — relations :
  public.reponse_binaire.collectivite_id → public.collectivite.id
  public.reponse_binaire.question_id → public.question.id
reponse_choix — relations :
  public.reponse_choix.collectivite_id → public.collectivite.id
  public.reponse_choix.question_id → public.question.id
  public.reponse_choix.reponse → public.question_choix.id
reponse_proportion — relations :
  public.reponse_proportion.collectivite_id → public.collectivite.id
  public.reponse_proportion.question_id → public.question.id
score_snapshot — relations :
  public.score_snapshot.audit_id → labellisation.audit.id
  public.score_snapshot.collectivite_id → public.collectivite.id
  public.score_snapshot.referentiel_id → public.referentiel_definition.id
service_tag — relations :
  public.service_tag.collectivite_id → public.collectivite.id
  public.service_tag.created_by → public.dcp.user_id
sous_thematique — relations :
  public.sous_thematique.thematique_id → public.thematique.id
structure_tag — relations :
  public.structure_tag.collectivite_id → public.collectivite.id
  public.structure_tag.created_by → public.dcp.user_id
tableau_de_bord_module — relations :
  public.tableau_de_bord_module.collectivite_id → public.collectivite.id
  public.tableau_de_bord_module.user_id → public.dcp.user_id
user_api_key — relations :
  public.user_api_key.user_id → auth.users.id
utilisateur_identite_oidc — relations :
  public.utilisateur_identite_oidc.user_id → auth.users.id
utilisateur_identite_oidc_invitation — relations :
  public.utilisateur_identite_oidc_invitation.user_id → auth.users.id
utilisateur_invitation_envoi — relations :
  public.utilisateur_invitation_envoi.collectivite_id → public.collectivite.id
utilisateur_support — relations :
  public.utilisateur_support.user_id → public.dcp.user_id
utilisateur_verifie — relations :
  public.utilisateur_verifie.user_id → public.dcp.user_id
"""

tables_text = """
prod.auth_users: instance_id (text), id (text), aud (text), role (text), email (text), encrypted_password (text), email_confirmed_at (timestamp with time zone), invited_at (timestamp with time zone), confirmation_token (text), confirmation_sent_at (timestamp with time zone), recovery_token (text), recovery_sent_at (timestamp with time zone), email_change_token_new (text), email_change (text), email_change_sent_at (timestamp with time zone), last_sign_in_at (timestamp with time zone), raw_app_meta_data (json), raw_user_meta_data (json), is_super_admin (boolean), created_at (timestamp with time zone), updated_at (timestamp with time zone), phone (text), phone_confirmed_at (timestamp with time zone), phone_change (text), phone_change_token (text), phone_change_sent_at (timestamp with time zone), confirmed_at (timestamp with time zone), email_change_token_current (text), email_change_confirm_status (bigint), banned_until (timestamp with time zone), reauthentication_token (text), reauthentication_sent_at (timestamp with time zone), is_sso_user (boolean), deleted_at (timestamp with time zone), is_anonymous (boolean)
prod.historique_action_statut: id (bigint), collectivite_id (bigint), action_id (text), avancement (text), previous_avancement (text), avancement_detaille (text), previous_avancement_detaille (text), concerne (boolean), previous_concerne (boolean), modified_by (text), previous_modified_by (text), modified_at (timestamp with time zone), previous_modified_at (timestamp with time zone)
prod.historique_fiche_action: id (bigint), fiche_id (bigint), titre (text), previous_titre (text), description (text), previous_description (text), piliers_eci (text), previous_piliers_eci (text), objectifs (text), previous_objectifs (text), resultats_attendus (text), previous_resultats_attendus (text), cibles (text), previous_cibles (text), ressources (text), previous_ressources (text), financements (text), previous_financements (text), budget_previsionnel (double precision), previous_budget_previsionnel (double precision), statut (text), previous_statut (text), niveau_priorite (text), previous_niveau_priorite (text), date_debut (timestamp with time zone), previous_date_debut (timestamp with time zone), date_fin_provisoire (timestamp with time zone), previous_date_fin_provisoire (timestamp with time zone), amelioration_continue (boolean), previous_amelioration_continue (boolean), maj_termine (boolean), previous_maj_termine (boolean), collectivite_id (double precision), created_at (timestamp with time zone), modified_at (timestamp with time zone), previous_modified_at (timestamp with time zone), modified_by (text), previous_modified_by (text), restreint (boolean), previous_restreint (boolean), deleted (boolean)
prod.historique_fiche_action_pilote: id (bigint), fiche_historise_id (bigint), user_id (text), tag_nom (text), previous (boolean)
prod.historique_justification: id (bigint), collectivite_id (bigint), question_id (text), modified_by (text), previous_modified_by (text), modified_at (timestamp with time zone), previous_modified_at (timestamp with time zone), texte (text), previous_texte (text)
prod.historique_justification_ajustement: id (bigint), collectivite_id (bigint), action_id (text), modified_by (text), previous_modified_by (text), modified_at (timestamp with time zone), previous_modified_at (timestamp with time zone), texte (text), previous_texte (text)
prod.historique_reponse_binaire: id (bigint), collectivite_id (bigint), question_id (text), reponse (boolean), previous_reponse (boolean), modified_by (text), modified_at (timestamp with time zone)
prod.historique_reponse_choix: id (bigint), collectivite_id (bigint), question_id (text), reponse (text), previous_reponse (text), modified_by (text), modified_at (timestamp with time zone)
prod.historique_reponse_proportion: id (bigint), collectivite_id (bigint), question_id (text), reponse (double precision), previous_reponse (double precision), modified_by (text), modified_at (timestamp with time zone)
prod.labellisation_demande: id (bigint), en_cours (boolean), collectivite_id (bigint), referentiel (text), etoiles (text), date (timestamp with time zone), sujet (text), modified_at (timestamp with time zone), envoyee_le (timestamp with time zone), demandeur (text), associated_collectivite_id (double precision)
prod.labellisation_etoile_meta: etoile (text), prochaine_etoile (text), long_label (text), short_label (text), min_realise_percentage (bigint), min_realise_score (double precision)
prod.notifications_notification: id (text), entity_id (text), status (text), send_to (text), sent_at (timestamp with time zone), sent_to_email (text), error_message (text), retries (text), created_by (text), created_at (timestamp with time zone), notified_on (text), notification_data (json), send_after (timestamp with time zone)
prod.public_abstract_any_indicateur_value: modified_at (timestamp with time zone), valeur (text), annee (text)
prod.public_abstract_modified_at: modified_at (timestamp with time zone)
prod.public_action_commentaire: collectivite_id (bigint), action_id (text), commentaire (text), modified_by (text), modified_at (timestamp with time zone)
prod.public_action_computed_points: modified_at (timestamp with time zone), action_id (text), value (text)
prod.public_action_de_reference: id (text), titre (text), description (text), code (text), leviers (text), categories (text), levier (text), categorie (text)
prod.public_action_de_reference_fiche: action_de_reference_id (text), fiche_id (text)
prod.public_action_definition: modified_at (timestamp with time zone), action_id (text), referentiel (text), identifiant (text), nom (text), description (text), contexte (text), exemples (text), ressources (text), reduction_potentiel (text), perimetre_evaluation (text), preuve (text), points (double precision), pourcentage (double precision), categorie (text), referentiel_id (text), referentiel_version (text), expr_score (text), adaptation_niveau (text), thematique_sgpe (text)
prod.public_action_definition_tag: referentiel_id (text), action_id (text), tag_ref (text)
prod.public_action_impact: id (bigint), titre (text), description (text), description_complementaire (text), nb_collectivite_en_cours (bigint), nb_collectivite_realise (bigint), action_continue (boolean), temps_de_mise_en_oeuvre (bigint), fourchette_budgetaire (bigint), impact_tier (bigint), subventions_mobilisables (json), ressources_externes (json), rex (json), competences_communales (boolean), independamment_competences (boolean), typologie_id (double precision)
prod.public_action_impact_action: action_impact_id (bigint), action_id (text)
prod.public_action_impact_banatic_competence: action_impact_id (bigint), competence_code (bigint)
prod.public_action_impact_categorie: id (text), nom (text)
prod.public_action_impact_categorie_fnv: action_impact_id (text), categorie_fnv_id (text)
prod.public_action_impact_complexite: niveau (bigint), nom (text)
prod.public_action_impact_effet_attendu: action_impact_id (bigint), effet_attendu_id (bigint)
prod.public_action_impact_fiche_action: fiche_id (bigint), action_impact_id (bigint)
prod.public_action_impact_fourchette_budgetaire: niveau (bigint), nom (text)
prod.public_action_impact_indicateur: action_impact_id (bigint), indicateur_id (bigint)
prod.public_action_impact_panier: panier_id (text), action_id (bigint)
prod.public_action_impact_partenaire: action_impact_id (bigint), partenaire_id (bigint)
prod.public_action_impact_sous_thematique: action_impact_id (bigint), sous_thematique_id (bigint)
prod.public_action_impact_state: action (text), statut (text), isinpanier (text), panier (text)
prod.public_action_impact_statut: panier_id (text), action_id (bigint), categorie_id (text)
prod.public_action_impact_temps_de_mise_en_oeuvre: niveau (bigint), nom (text)
prod.public_action_impact_thematique: action_impact_id (bigint), thematique_id (bigint), ordre (bigint)
prod.public_action_impact_tier: niveau (bigint), nom (text)
prod.public_action_impact_typologie: id (bigint), nom (text)
prod.public_action_origine: referentiel_id (text), action_id (text), origine_referentiel_id (text), origine_action_id (text), ponderation (double precision)
prod.public_action_origine_texte: referentiel_id (text), action_id (text), origine_referentiel_id (text), origine_action_id (text)
prod.public_action_pilote: collectivite_id (bigint), action_id (text), user_id (text), tag_id (double precision)
prod.public_action_relation: id (text), referentiel (text), parent (text)
prod.public_action_score_indicateur_valeur: action_id (text), collectivite_id (bigint), indicateur_id (bigint), indicateur_valeur_id (bigint), type_score (text)
prod.public_action_service: collectivite_id (bigint), action_id (text), service_tag_id (bigint)
prod.public_action_statut: collectivite_id (bigint), action_id (text), avancement (text), avancement_detaille (text), concerne (boolean), modified_by (text), modified_at (timestamp with time zone)
prod.public_ai_plan_import_job: id (text), collectivite_id (text), created_by (text), status (text), options (json), step_states (json), source_path (text), draft (json), error (text), created_at (timestamp with time zone), modified_at (timestamp with time zone), created_plan_id (text), fichier_id (text), started_at (timestamp with time zone), finished_at (timestamp with time zone), stats (json), checkpoint (json), attempt (text)
prod.public_ai_plan_import_step_run: id (text), job_id (text), step (text), status (text), started_at (timestamp with time zone), ended_at (timestamp with time zone), duration_ms (text), llm_calls (text), failed_calls (text), rate_limited_calls (text), tokens (json), models (text), details (json), error (text), attempt (text)
prod.public_analysis_run: id (text), started_at (timestamp with time zone), finished_at (timestamp with time zone)
prod.public_annexe: id (bigint), collectivite_id (bigint), fichier_id (double precision), url (text), titre (text), commentaire (text), modified_by (text), modified_at (timestamp with time zone), lien (json), fiche_id (bigint)
prod.public_audit_auditeur: audit_id (bigint), auditeur (text), created_at (timestamp with time zone)
prod.public_audit_preuves_archive: id (text), collectivite_id (text), referentiel_id (text), audit_id (text), requested_by (text), status (text), total_files (text), processed_files (text), storage_path (text), error_message (text), created_at (timestamp with time zone), modified_at (timestamp with time zone), expires_at (timestamp with time zone)
prod.public_axe: modified_at (timestamp with time zone), id (bigint), nom (text), collectivite_id (bigint), parent (double precision), created_at (timestamp with time zone), modified_by (text), plan (bigint), type (double precision), panier_id (text), description (text), date_debut (timestamp with time zone), date_fin (timestamp with time zone), source (text), verified_at (timestamp with time zone), verified_by (text), status (text)
prod.public_axe_indicateur: indicateur_id (text), axe_id (text), created_at (timestamp with time zone), created_by (text)
prod.public_banatic_2021_2025_crosswalk: id (bigint), code_2021 (bigint), code_2025 (double precision), mapping_type (text)
prod.public_banatic_2025_competence: competence_code (bigint), intitule (text), version (text)
prod.public_banatic_competence: code (bigint), nom (text)
prod.public_banner_info: id (text), type (text), info (text), modified_at (timestamp with time zone), modified_by (text), active (text)
prod.public_categorie_fnv: id (bigint), nom (text)
prod.public_categorie_tag: id (bigint), groupement_id (double precision), collectivite_id (text), nom (text), visible (boolean), created_at (timestamp with time zone), created_by (text)
prod.public_client_scores: collectivite_id (text), referentiel (text), scores (json), modified_at (timestamp with time zone), payload_timestamp (timestamp with time zone)
prod.public_collectivite: id (bigint), created_at (timestamp with time zone), modified_at (timestamp with time zone), access_restreint (boolean), nom (text), type (text), commune_code (text), siren (text), departement_code (text), region_code (text), nature_insee (text), population (double precision), dans_aire_urbaine (boolean), nic (text), preferences (json), sinoe_id (text)
prod.public_collectivite_banatic_2025_competence: collectivite_id (bigint), competence_code (bigint), exercice (boolean), created_at (timestamp with time zone)
prod.public_collectivite_banatic_2025_perimetre: collectivite_id (bigint), nb_communes_membres (bigint), created_at (timestamp with time zone)
prod.public_collectivite_banatic_2025_transfert: collectivite_id (bigint), competence_code (bigint), nature_transfert (text), created_at (timestamp with time zone), nb_communes_transferees (bigint)
prod.public_collectivite_banatic_competence: collectivite_id (bigint), competence_code (bigint)
prod.public_collectivite_banatic_type: id (text), nom (text), type (text)
prod.public_collectivite_bucket: collectivite_id (bigint), bucket_id (text)
prod.public_collectivite_levier_ges_pertinence: collectivite_id (text), levier_id (text), categorie (text), pertinence (text), modified_at (timestamp with time zone), modified_by (text)
prod.public_collectivite_perimetre_secondaire: id (text), collectivite_id (text), region_code (text), departement_code (text), source (text), created_at (timestamp with time zone)
prod.public_collectivite_relations: id (text), parent_id (text)
prod.public_collectivite_test: id (bigint), collectivite_id (bigint), nom (text)
prod.public_collectivite_volet_ges: collectivite_id (text), levier_id (text), categorie (text), note (text), fiche_ids (text), created_at (timestamp with time zone)
prod.public_commune: id (bigint), collectivite_id (bigint), nom (text), code (text)
prod.public_cot: collectivite_id (bigint), actif (boolean), signataire (bigint)
prod.public_dcp: user_id (text), nom (text), prenom (text), email (text), limited (boolean), deleted (boolean), created_at (timestamp with time zone), modified_at (timestamp with time zone), telephone (text), cgu_acceptees_le (timestamp with time zone), preferences (json)
prod.public_demarche: id (text), collectivite_id (text), type (text), titre (text), description (text), status (text), obligation (text), launched_at (timestamp with time zone), published_at (timestamp with time zone), transmitted_at (timestamp with time zone), avis_deadline_at (timestamp with time zone), created_at (timestamp with time zone), created_by (text), modified_at (timestamp with time zone), modified_by (text), adopted_at (timestamp with time zone), transmitted_off_platform (text), is_scot_aec (text)
prod.public_demarche_definition: demarche_type (text), documents_additional_amont (boolean), documents_additional_aval (boolean), documents_formats_autorises (text), documents_mime_types_autorises (text), created_at (timestamp with time zone), modified_at (timestamp with time zone)
prod.public_demarche_document: id (text), collectivite_id (text), fichier_id (text), url (text), titre (text), commentaire (text), modified_by (text), modified_at (timestamp with time zone), lien (json), demarche_id (text), document_id (text), etape (text)
prod.public_demarche_document_additional: id (text), collectivite_id (text), fichier_id (text), url (text), titre (text), commentaire (text), modified_by (text), modified_at (timestamp with time zone), lien (json), demarche_id (text), etape (text)
prod.public_demarche_document_definition: id (text), demarche_type (text), nom (text), description (text), requis (boolean), ordre (bigint), created_at (timestamp with time zone), modified_at (timestamp with time zone), etape (text), expr_applicable (text)
prod.public_demarche_document_substitution: document_id (text), substitut_id (text), automatic (boolean)
prod.public_demarche_pcaet_avis: id (text), demande_avis_id (text), emetteur_collectivite_id (text), au_titre_de (text), fichier_ref (text), valide_le (timestamp with time zone), depose_par (text), depose_le (timestamp with time zone), modifie_le (timestamp with time zone), envoye_le (timestamp with time zone)
prod.public_demarche_pcaet_demande_avis: id (text), demarche_id (text), instructeur_collectivite_id (text), source (text), created_at (timestamp with time zone), perimetre (text)
prod.public_demarche_pcaet_source_metadonnee: demarche_id (text), collectivite_id (text), metadonnee_id (text)
prod.public_demarche_pcaet_vulnerabilite_thematique: id (text), code (text), label (text), collectivite_id (text), requis (text), display_order (text), created_at (timestamp with time zone), created_by (text), modified_at (timestamp with time zone), modified_by (text), parent_id (text)
prod.public_demarche_pcaet_vulnerabilite_valeur: demarche_id (text), thematique_id (text), niveau_maintenant (text), niveau_2050 (text), niveau_2100 (text), objectifs_2050 (text), objectifs_2100 (text), created_at (timestamp with time zone), created_by (text), modified_at (timestamp with time zone), modified_by (text)
prod.public_demarche_pilote: demarche_id (text), tag_id (text), user_id (text), created_at (timestamp with time zone), created_by (text)
prod.public_demarche_plan_action: demarche_id (text), plan_action_id (text), created_at (timestamp with time zone), created_by (text)
prod.public_demarche_status_history: id (text), demarche_id (text), from_status (text), to_status (text), transition (text), created_at (timestamp with time zone), created_by (text)
prod.public_discussion: id (bigint), collectivite_id (bigint), action_id (text), created_by (text), created_at (timestamp with time zone), modified_at (timestamp with time zone), status (text)
prod.public_discussion_message: id (bigint), created_by (text), created_at (timestamp with time zone), discussion_id (bigint), message (text)
prod.public_effet_attendu: id (bigint), nom (text), notice (text)
prod.public_epci: id (bigint), collectivite_id (bigint), nom (text), siren (text), nature (text)
prod.public_fiche_action: modified_at (timestamp with time zone), id (bigint), titre (text), description (text), piliers_eci (text), objectifs (text), resultats_attendus (text), cibles (text), ressources (text), financements (text), budget_previsionnel (double precision), statut (text), niveau_priorite (text), date_debut (timestamp with time zone), date_fin_provisoire (timestamp with time zone), amelioration_continue (boolean), maj_termine (boolean), collectivite_id (bigint), created_at (timestamp with time zone), modified_by (text), restreint (boolean), instance_gouvernance (text), participation_citoyenne (text), participation_citoyenne_type (text), temps_de_mise_en_oeuvre_id (double precision), created_by (text), parent_id (double precision), deleted (boolean)
prod.public_fiche_action_action: fiche_id (bigint), action_id (text)
prod.public_fiche_action_analysis: fiche_id (text), collectivite_id (text), fingerprint (text), status (text), retry_count (text), analyzed_at (timestamp with time zone)
prod.public_fiche_action_axe: fiche_id (bigint), axe_id (bigint), created_at (timestamp with time zone), created_by (text)
prod.public_fiche_action_budget: id (bigint), fiche_id (bigint), type (text), unite (text), annee (double precision), budget_previsionnel (double precision), budget_reel (double precision), est_etale (boolean)
prod.public_fiche_action_effet_attendu: fiche_id (bigint), effet_attendu_id (bigint)
prod.public_fiche_action_etape: id (bigint), fiche_id (bigint), nom (text), ordre (bigint), realise (boolean), modified_at (timestamp with time zone), created_at (timestamp with time zone), modified_by (text), created_by (text)
prod.public_fiche_action_financeur_tag: id (bigint), fiche_id (bigint), financeur_tag_id (bigint), montant_ttc (double precision)
prod.public_fiche_action_import_csv: axe (text), sous_axe (text), sous_sous_axe (text), num_action (text), titre (text), description (text), objectifs (text), resultats_attendus (text), cibles (text), structure_pilote (text), moyens (text), partenaires (text), personne_referente (text), elu_referent (text), financements (text), budget (text), statut (text), priorite (text), date_debut (text), date_fin (text), amelioration_continue (text), calendrier (text), notes (text), collectivite_id (text), plan_nom (text), service (text), financeur_un (text), montant_un (text), financeur_deux (text), montant_deux (text), financeur_trois (text), montant_trois (text)
prod.public_fiche_action_indicateur: indicateur_id (bigint), fiche_id (bigint), created_at (timestamp with time zone), created_by (text)
prod.public_fiche_action_instance_de_gouvernance_tag: fiche_action_id (text), instance_de_gouvernance_tag_id (text), created_by (text), created_at (timestamp with time zone)
prod.public_fiche_action_libre_tag: fiche_id (bigint), libre_tag_id (bigint), created_at (timestamp with time zone), created_by (text)
prod.public_fiche_action_lien: fiche_une (bigint), fiche_deux (bigint)
prod.public_fiche_action_note: fiche_id (bigint), date_note (timestamp with time zone), note (text), modified_at (timestamp with time zone), created_at (timestamp with time zone), modified_by (text), created_by (text), id (bigint)
prod.public_fiche_action_partenaire_tag: fiche_id (bigint), partenaire_tag_id (bigint)
prod.public_fiche_action_pilote: fiche_id (bigint), user_id (text), tag_id (double precision), created_at (timestamp with time zone), created_by (text)
prod.public_fiche_action_referent: fiche_id (bigint), user_id (text), tag_id (double precision), created_at (timestamp with time zone), created_by (text)
prod.public_fiche_action_secteur_attribution: fiche_id (text), secteurs (text), origine (text), methode (text), reponse_communs (json), modified_at (timestamp with time zone), modified_by (text), justification (text)
prod.public_fiche_action_service_tag: fiche_id (bigint), service_tag_id (bigint)
prod.public_fiche_action_sharing: fiche_id (bigint), collectivite_id (bigint), created_at (timestamp with time zone), created_by (text)
prod.public_fiche_action_sous_thematique: fiche_id (bigint), thematique_id (bigint), created_at (timestamp with time zone), created_by (text)
prod.public_fiche_action_structure_tag: fiche_id (bigint), structure_tag_id (bigint)
prod.public_fiche_action_thematique: fiche_id (bigint), thematique_id (bigint), created_at (timestamp with time zone), created_by (text)
prod.public_fiche_action_volet_ges: fiche_id (text), levier_id (text), categorie (text), created_at (timestamp with time zone)
prod.public_filtre_intervalle: type (text), id (text), libelle (text), intervalle (text)
prod.public_financeur_tag: id (bigint), nom (text), collectivite_id (bigint), created_at (timestamp with time zone), created_by (text)
prod.public_groupement: id (bigint), nom (text)
prod.public_groupement_collectivite: groupement_id (bigint), collectivite_id (bigint)
prod.public_indicateur_action: indicateur_id (bigint), action_id (text)
prod.public_indicateur_artificialisation: collectivite_id (bigint), total (double precision), activite (double precision), habitat (double precision), mixte (double precision), routiere (double precision), ferroviaire (double precision), inconnue (double precision)
prod.public_indicateur_categorie_tag: categorie_tag_id (bigint), indicateur_id (bigint)
prod.public_indicateur_collectivite: indicateur_id (bigint), collectivite_id (bigint), commentaire (text), confidentiel (boolean), favoris (boolean), modified_by (text), modified_at (timestamp with time zone), is_applicable (boolean), is_suivi (boolean)
prod.public_indicateur_definition: id (bigint), groupement_id (double precision), collectivite_id (double precision), identifiant_referentiel (text), titre (text), titre_long (text), description (text), unite (text), borne_min (text), borne_max (text), participation_score (boolean), sans_valeur_utilisateur (boolean), valeur_calcule (text), modified_at (timestamp with time zone), created_at (timestamp with time zone), modified_by (text), created_by (text), titre_court (text), version (text), precision (bigint), expr_cible (text), expr_seuil (text), libelle_cible_seuil (text), periodicite (text), aggregation_resultat (text), aggregation_objectif (text)
prod.public_indicateur_groupe: parent (bigint), enfant (bigint)
prod.public_indicateur_objectif: indicateur_id (text), date_valeur (timestamp with time zone), formule (text)
prod.public_indicateur_pilote: id (bigint), indicateur_id (bigint), user_id (text), tag_id (double precision), collectivite_id (bigint)
prod.public_indicateur_service_tag: indicateur_id (bigint), service_tag_id (bigint), collectivite_id (bigint)
prod.public_indicateur_source: id (text), libelle (text), ordre_affichage (double precision)
prod.public_indicateur_source_metadonnee: id (bigint), source_id (text), date_version (timestamp with time zone), nom_donnees (text), diffuseur (text), producteur (text), methodologie (text), limites (text)
prod.public_indicateur_source_source_calcul: source_id (text), source_calcul_id (text)
prod.public_indicateur_sous_thematique: indicateur_id (text), sous_thematique_id (text)
prod.public_indicateur_thematique: indicateur_id (bigint), thematique_id (bigint)
prod.public_indicateur_valeur: id (bigint), indicateur_id (bigint), collectivite_id (bigint), date_valeur (timestamp with time zone), metadonnee_id (double precision), resultat (double precision), objectif (double precision), modified_at (timestamp with time zone), created_at (timestamp with time zone), modified_by (text), created_by (text), periodicite (text)
prod.public_indicateur_vue: id (text), collectivite_id (text), nom (text), filtres (json), created_at (timestamp with time zone), modified_at (timestamp with time zone), created_by (text), modified_by (text)
prod.public_instance_de_gouvernance_tag: id (text), nom (text), collectivite_id (text), created_by (text), created_at (timestamp with time zone)
prod.public_justification: collectivite_id (bigint), question_id (text), modified_by (text), texte (text), modified_at (timestamp with time zone)
prod.public_justification_ajustement: collectivite_id (bigint), action_id (text), texte (text), modified_by (text), modified_at (timestamp with time zone)
prod.public_labellisation: id (bigint), collectivite_id (bigint), referentiel (text), obtenue_le (timestamp with time zone), annee (double precision), etoiles (bigint), score_realise (double precision), score_programme (double precision), audit_id (double precision)
prod.public_labellisation_action_critere: etoile (text), prio (bigint), referentiel (text), action_id (text), formulation (text), min_realise_percentage (bigint), min_programme_percentage (double precision), min_realise_score (double precision), min_programme_score (double precision)
prod.public_labellisation_calendrier: referentiel (text), information (text)
prod.public_labellisation_fichier_critere: referentiel (text), etoile (text), description (text)
prod.public_libre_tag: id (bigint), nom (text), collectivite_id (bigint), created_at (timestamp with time zone), created_by (text)
prod.public_nom_table: siren (text), nom (text), referentiel_id (text), date (timestamp with time zone), type_jalon (text), actionId (text), pointFait (double precision), pointPasFait (double precision), pointProgramme (text), pointPotentiel (double precision)
prod.public_panier: id (text), created_at (timestamp with time zone), created_by (text), collectivite_id (text), collectivite_preset (double precision), latest_update (timestamp with time zone), private (boolean)
prod.public_panier_partenaire: id (bigint), nom (text)
prod.public_partenaire_tag: id (bigint), nom (text), collectivite_id (bigint), created_at (timestamp with time zone), created_by (text)
prod.public_personnalisation_consequence: modified_at (timestamp with time zone), collectivite_id (text), consequences (json), payload_timestamp (timestamp with time zone)
prod.public_personnalisation_regle: action_id (text), type (text), formule (text), description (text), modified_at (timestamp with time zone)
prod.public_personne_tag: id (bigint), nom (text), collectivite_id (bigint), created_at (timestamp with time zone), created_by (text)
prod.public_plan_action_type: id (bigint), categorie (text), type (text), detail (text)
prod.public_plan_action_type_categorie: categorie (text)
prod.public_plan_pilote: plan_id (text), tag_id (text), user_id (text), created_at (timestamp with time zone), created_by (text)
prod.public_plan_referent: plan_id (text), tag_id (text), user_id (text), created_at (timestamp with time zone), created_by (text)
prod.public_plan_report_generation: id (text), plan_id (bigint), template_ref (text), file_id (double precision), options (json), status (text), error_message (text), created_at (timestamp with time zone), modified_at (timestamp with time zone), created_by (text), collectivite_id (double precision), name (text)
prod.public_post_audit_scores: collectivite_id (text), referentiel (text), scores (json), modified_at (timestamp with time zone), payload_timestamp (timestamp with time zone), audit_id (text)
prod.public_pre_audit_scores: collectivite_id (text), referentiel (text), scores (json), modified_at (timestamp with time zone), payload_timestamp (timestamp with time zone), audit_id (text)
prod.public_preuve_action: preuve_id (text), action_id (text)
prod.public_preuve_audit: id (bigint), collectivite_id (bigint), fichier_id (bigint), url (text), titre (text), commentaire (text), modified_by (text), modified_at (timestamp with time zone), lien (json), audit_id (bigint)
prod.public_preuve_complementaire: id (bigint), collectivite_id (bigint), fichier_id (double precision), url (text), titre (text), commentaire (text), modified_by (text), modified_at (timestamp with time zone), lien (json), action_id (text)
prod.public_preuve_labellisation: id (bigint), collectivite_id (bigint), fichier_id (bigint), url (text), titre (text), commentaire (text), modified_by (text), modified_at (timestamp with time zone), lien (json), demande_id (bigint), objet (text)
prod.public_preuve_rapport: id (bigint), collectivite_id (bigint), fichier_id (bigint), url (text), titre (text), commentaire (text), modified_by (text), modified_at (timestamp with time zone), lien (json), date (timestamp with time zone)
prod.public_preuve_reglementaire: id (bigint), collectivite_id (bigint), fichier_id (double precision), url (text), titre (text), commentaire (text), modified_by (text), modified_at (timestamp with time zone), lien (json), preuve_id (text)
prod.public_preuve_reglementaire_definition: id (text), nom (text), description (text)
prod.public_private_collectivite_membre: user_id (text), collectivite_id (bigint), fonction (text), details_fonction (text), champ_intervention (text), created_at (timestamp with time zone), modified_at (timestamp with time zone), est_referent (boolean)
prod.public_private_utilisateur_droit: id (bigint), user_id (text), collectivite_id (bigint), active (boolean), created_at (timestamp with time zone), modified_at (timestamp with time zone), niveau_acces (text), invitation_id (text)
prod.public_question: id (text), thematique_id (text), ordonnancement (bigint), types_collectivites_concernees (text), type (text), description (text), formulation (text), version (text), competence_code (double precision), consignes_justification (text), expr_visible (text)
prod.public_question_action: question_id (text), action_id (text)
prod.public_question_choix: question_id (text), id (text), ordonnancement (text), formulation (text), version (text)
prod.public_question_thematique: id (text), nom (text)
prod.public_referentiel_definition: id (text), nom (text), version (text), hierarchie (text), created_at (timestamp with time zone), modified_at (timestamp with time zone), locked (boolean)
prod.public_referentiel_tag: ref (text), nom (text), type (text)
prod.public_reponse_binaire: modified_at (timestamp with time zone), collectivite_id (bigint), question_id (text), reponse (boolean)
prod.public_reponse_choix: modified_at (timestamp with time zone), collectivite_id (bigint), question_id (text), reponse (text)
prod.public_reponse_proportion: modified_at (timestamp with time zone), collectivite_id (bigint), question_id (text), reponse (double precision)
prod.public_score_snapshot: collectivite_id (bigint), referentiel_id (text), referentiel_version (text), audit_id (double precision), date (timestamp with time zone), ref (text), nom (text), type_jalon (text), point_fait (double precision), point_programme (double precision), point_pas_fait (double precision), point_potentiel (double precision), created_by (text), created_at (timestamp with time zone), modified_by (text), modified_at (timestamp with time zone), etoiles (bigint)
prod.public_service_tag: id (bigint), nom (text), collectivite_id (bigint), created_at (timestamp with time zone), created_by (text)
prod.public_site_contact: modified_at (timestamp with time zone), email (text), formulaire (json)
prod.public_sous_thematique: id (bigint), sous_thematique (text), thematique_id (bigint)
prod.public_structure_tag: id (bigint), nom (text), collectivite_id (bigint), created_at (timestamp with time zone), created_by (text)
prod.public_tableau_de_bord_module: id (text), collectivite_id (bigint), user_id (text), titre (text), default_key (text), type (text), options (json), created_at (timestamp with time zone), modified_at (timestamp with time zone)
prod.public_thematique: nom (text), id (bigint), md_id (text)
prod.public_typologie_sinoe: id (text), code_sinoe (text), libelle (text)
prod.public_usage: time (timestamp with time zone), fonction (text), action (text), page (text), user_id (text), collectivite_id (double precision)
prod.public_usage_backup: time (timestamp with time zone), fonction (text), action (text), page (text), user_id (text), collectivite_id (text)
prod.public_user_api_key: client_id (text), user_id (text), client_secret_hash (text), client_secret_truncated (text), permissions (text), created_at (timestamp with time zone), modified_at (timestamp with time zone)
prod.public_utilisateur_identite_oidc: provider (text), sub (text), user_id (text), email (text), siret (text), idp_id (text), claims (json), created_at (timestamp with time zone), last_sign_in_at (timestamp with time zone)
prod.public_utilisateur_identite_oidc_invitation: id (text), token_hash (text), provider (text), sub (text), claims (json), email_provider (text), initial_mail (text), user_id (text), created_at (timestamp with time zone), expires_at (timestamp with time zone), confirmed_at (timestamp with time zone)
prod.public_utilisateur_support: user_id (text), support (boolean), is_support_mode_enabled (boolean)
prod.public_utilisateur_verifie: user_id (text), verifie (boolean)
prod.public_visite: time (timestamp with time zone), page (text), tag (text), onglet (text), user_id (text), collectivite_id (double precision)
prod.public_visite_backup: time (timestamp with time zone), page (text), tag (text), onglet (text), user_id (text), collectivite_id (text)
public.Score_mesures: siren (text), nom (text), referentiel_id (text), date_fin_audit (timestamp with time zone), sujet (text), date (timestamp with time zone), type_jalon (text), actionId (text), pointFait (double precision), pointPasFait (double precision), pointProgramme (double precision), pointPotentiel (double precision), actionid (text), nom_mesure (text)
public.action_definition: modified_at (timestamp with time zone), action_id (text), referentiel (text), identifiant (text), nom (text), description (text), contexte (text), exemples (text), ressources (text), preuve (text), points (double precision), pourcentage (double precision), reduction_potentiel (text), perimetre_evaluation (text), categorie (text), referentiel_id (text), referentiel_version (text), expr_score (text), adaptation_niveau (text), thematique_sgpe (text)
public.action_referentiel: action_id (text), referentiel (text), nom (text), type (text), exemples (text), depth (bigint)
public.activite_semaine: semaine (text), collectivite_id (double precision), email (text)
public.airtable_sync: collectivite_id (bigint), key (text), type (text), derniere_modif (text), derniere_creation_compte (text), user_derniere_creation_compte (text), top_contributeur (text), pageviews_plan (bigint), nb_contributeurs (bigint), nb_super_contributeurs (bigint), nb_fiches_modifiees_3_mois (bigint), nb_fiches_modifiees_6_mois (bigint), nb_fiches_modifiees_12_mois (bigint), nb_pap (bigint), passage_pap (text), owner_plan (text), url_plan (text), activite_depuis_pap (bigint), ct_tete (double precision), nb_fa (bigint), nb_fa_pilotables (bigint), nb_indicateur_perso (bigint), plans_type (text), pap_3_mois (text), pap_12_mois (text), pap_multiplan_3_mois (text), pap_multiplan_12_mois (text), note_plan (double precision), nombre_pap_bizdev (double precision), derniere_visite (text), user_derniere_visite (text), pipeline (text), semaine (text), semaine_passage_retention (text)
public.airtable_sync_semaine: collectivite_id (bigint), semaine (text), pipeline (text), semaine_passage_retention (text)
public.airtable_sync_semaine_old: collectivite_id (bigint), key (text), derniere_modif (text), derniere_creation_compte (text), top_contributeur (text), pageviews_plan (bigint), nb_contributeurs (bigint), nb_super_contributeurs (bigint), nb_contribution (bigint), note_max_pap (double precision), nb_pap (bigint), passage_pap (text), score (double precision), score_pilotabilite (double precision), score_indicateur (double precision), score_objectif (double precision), score_budget (double precision), score_avancement (double precision), score_referentiel (double precision), owner_plan (text), activite_depuis_pap (bigint), ct_tete (double precision), statut (text), nb_fa (bigint), nb_fa_pilotables (bigint), nb_indicateur_perso (bigint), plans_type (text), derniere_visite (text), pipeline (text), semaine (text)
public.audit: audit_id (bigint), collectivite_id (bigint), referentiel (text), audit_debut (timestamp with time zone), audit_fin (timestamp with time zone), date_cnl (timestamp with time zone), audit_valide (boolean), clos (boolean), type (text), valide_labellisation (boolean), date_demande (timestamp with time zone)
public.auditeur: user_id (text), audit_id (bigint), date_attribution (timestamp with time zone), nom_auditeur (text), prenom_auditeur (text), email_auditeur (text)
public.bizdev_A_F_contact: date (text), echange_type (text), collectivite_id (double precision)
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
public.derniere_connexion: collectivite_id (double precision), email (text), derniere_connexion (timestamp with time zone), fonction (text), nom (text), type (text)
public.evenements_airtable: index (bigint), Date (timestamp without time zone), evenements (text)
public.evolution_ind_od: mois (text), departement_name (text), region_name (text), nb_values_od_cum (double precision)
public.evolution_ind_pers: region_name (text), departement_name (text), mois (text), nb_ind_perso (double precision), nb_lignes (double precision), nb_ind_perso_ct (double precision)
public.evolution_labellisation: mois (timestamp without time zone), nb_labellisation_cumule (bigint)
public.fa_distrib: mois (timestamp without time zone), departement_name (text), action (bigint), action_pilotable (double precision), region_name (text), action_pilotable_actives (double precision), nb_fiches (double precision), realise (double precision)
public.fa_sharing: mois (timestamp without time zone), nb_fa_shared (bigint)
public.feature: datetime (timestamp with time zone), collectivite_id (bigint), email (text), sub-feature (json), feature (text)
public.feature_all: month (timestamp without time zone), collectivite_id (double precision), feature (text), email (text)
public.fiche_action_plan: fiche_id (bigint), plan (bigint)
public.ind_od_producteur_indicateur: titre (text), producteur (text), departement_name (text), region_name (text)
public.indicateur_definition: id (bigint), identifiant_referentiel (text), indicateur_specifique (text), titre (text), titre_long (text), description (text), unite (text)
public.indicateur_reference: theme (text), libelle (text), nb_ct (bigint)
public.indicateurs_od: titre (text), unite (text), identifiant_referentiel (text), types_collectivite (text), thematique (text), sources_libelle (text)
public.indicateurs_valeurs_olap: indicateur_id (bigint), collectivite_id (double precision), date_valeur (timestamp without time zone), resultat (double precision), identifiant_referentiel (text), api_nom_cube (text), metadonnee_id (bigint)
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
public.note_plan_semaine: plan (text), note_plan (numeric(3,1)), semaine (date)
public.notion_ticket: id_ticket (text), titre (text), type_bug_support (text), thematique (text), criticite (text), statut (text), temps_resolution (double precision), createur_id (text), responsable (text), personnes_associees (text), email_utilisateur (text), id_collectivite (double precision), epic_name (text), tickets_lies (text), feedback (text), created_at (text), date_remontee_crisp (text), last_edited_at (text), url (text)
public.nps: nps (double precision)
public.nps_cumule: mois (date), total_mois (bigint), total_cumule (bigint), detracteurs_cumules (bigint), passifs_cumules (bigint), promoteurs_cumules (bigint), pct_detracteurs (double precision), pct_passifs (double precision), pct_promoteurs (double precision), nps (double precision)
public.nps_mensuel: mois (date), total (bigint), detracteurs (bigint), passifs (bigint), promoteurs (bigint), pct_detracteurs (double precision), pct_passifs (double precision), pct_promoteurs (double precision), nps (double precision)
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
public.priorisation: id (bigint), collectivite_id (bigint), secteur (text), identifiant_referentiel (text), levier (text), categorie (smallint), note (smallint), ids (text), created_at (timestamp with time zone)
public.priorisation_action: id (integer), collectivite_id (integer), levier (text), categorie (integer), fiche_action_id (integer), created_at (timestamp with time zone), reference (boolean)
public.priorisation_action_reference: levier (text), categorie (bigint), titre (text), description (text), id (bigint)
public.priorisation_categorie_levier: categorie (bigint), Captage de méthane dans les ISDND (double precision), Biogaz (double precision), Véhicules électriques (double precision), Efficacité et carburants décarbonés des véhicules privés (double precision), Sobriété des bâtiments (résidentiel) (double precision), Pratiques stockantes (double precision), Changement chaudières gaz + rénovation (résidentiel) (double precision), Vélo et transport en commun (double precision), Bus et cars décarbonés (double precision), Changement de chaudière à fioul (tertiaire) (double precision), Réduction des déplacements (double precision), Sobriété et isolation des bâtiments (tertiaire) (double precision), Gestion des forêts et produits bois (double precision), Changements de pratiques de fertilisation azotée (double precision), Elevage durable (double precision), Bâtiments & Machines agricoles (double precision), Valorisation matière des déchets (double precision), Changement chaudières fioul + rénovation (résidentiel) (double precision), Gestion des haies (double precision), Sobriété foncière (double precision), Réseaux de chaleur décarbonés (double precision), Prévention des déchets (double precision), Changement de chaudière à gaz (tertiaire) (double precision), Fret décarboné et multimodalité (double precision), Electricité renouvelable (double precision), Efficacité et sobriété logistique (double precision), Covoiturage (double precision), Production Industrielle (double precision), Gestion des prairies (double precision)
public.priorisation_faisabilite: id (integer), collectivite_id (integer), levier (text), categorie (integer), faisabilite (integer), created_at (timestamp with time zone)
public.priorisation_hors_competence: id (integer), collectivite_id (integer), levier (text), categorie (integer), created_at (timestamp with time zone)
public.priorisation_levier_mesure: action_id (text), levier (text), categorie (integer)
public.priorisation_reduction_levier: id (integer), collectivite_id (integer), levier (text), reduction (double precision), created_at (timestamp without time zone)
public.retours_utilisateurs_analyse: feedback_id (text), titre (text), citation (text), url (text), created_time (text), sans_epic (boolean), cycle_id (text), cycle_name (text), confiance (text), justification (text), tickets (jsonb), ticket_justification (text), erreur (text), model (text), analyse_at (timestamp with time zone)
public.retours_utilisateurs_backlog: ticket_id (text), cycle_id (text), ticket_titre (text), statut (text), cycle_name (text), url (text), maj_at (timestamp with time zone)
public.retours_utilisateurs_cycles: cycle_id (text), cycle_name (text), maj_at (timestamp with time zone)
public.retours_utilisateurs_tickets: feedback_id (text), ticket_id (text), cycle_id (text), feedback_titre (text), ticket_titre (text), choix_ia (boolean), score_ia (double precision), valide_at (timestamp with time zone), notion_sync_at (timestamp with time zone)
public.score_snapshot: siren (text), nom (text), collectivite_id (bigint), ref (text), referentiel_id (text), referentiel_version (text), audit_id (double precision), sujet (text), date_fin_audit (timestamp with time zone), date (timestamp with time zone), type_jalon (text), point_fait (double precision), point_programme (double precision), point_pas_fait (double precision), point_potentiel (double precision), etoiles (bigint)
public.stats_hero_section_site: nb_ct_actif_12_mois (bigint), nb_user_actif_12_mois (bigint), nb_pap_actif_12_mois (bigint), nb_action_pilotable_active_12_mois (bigint)
public.statut_fiche_13_semaines: fiche_id (bigint), mois (text), statut (text)
public.statut_fiche_52_semaines: fiche_id (bigint), mois (text), statut (text)
public.taux_contact_support: month (timestamp without time zone), taux_support_bug_% (double precision)
public.tmp_backup_indicateur_source_metadonnee: id (bigint), source_id (text), date_version (timestamp without time zone), nom_donnees (text), diffuseur (text), producteur (text), methodologie (text), limites (text)
public.tmp_backup_indicateur_valeur: id (bigint), indicateur_id (bigint), collectivite_id (bigint), date_valeur (timestamp without time zone), metadonnee_id (bigint), resultat (double precision), resultat_commentaire (text), objectif (text), objectif_commentaire (text), estimation (text), modified_at (timestamp with time zone), created_at (timestamp with time zone), modified_by (text), created_by (text), calcul_auto (boolean), calcul_auto_identifiants_manquants (text)
public.tr_comm: id_tech_comm (bigint), cd_comm (text), lb_comm_majs (text), cd_sirn_comm (double precision)
public.user_actif_12_mois: mois (timestamp without time zone), collectivite_id (double precision), email (text)
public.user_actifs_ct_mois: mois (text), collectivite_id (bigint), email (text), departement_name (text), region_name (text)
public.utilisateurs: user_id (text), nom (text), prenom (text), email (text), telephone (text)
public.utilisateurs_droits: user_id (text), collectivite_id (bigint), fonction (text), details_fonction (text), est_referent (boolean), champ_intervention (text), niveau_acces (text), date_creation (timestamp with time zone), invitation (boolean)
public.visite_annuelle: collectivite_id (bigint), derniere_date (timestamp with time zone)
"""