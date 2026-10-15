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
auth.users: instance_id (uuid), id (uuid), aud (character varying(255)), role (character varying(255)), email (character varying(255)), encrypted_password (character varying(255)), email_confirmed_at (timestamp with time zone), invited_at (timestamp with time zone), confirmation_token (character varying(255)), confirmation_sent_at (timestamp with time zone), recovery_token (character varying(255)), recovery_sent_at (timestamp with time zone), email_change_token_new (character varying(255)), email_change (character varying(255)), email_change_sent_at (timestamp with time zone), last_sign_in_at (timestamp with time zone), raw_app_meta_data (jsonb), raw_user_meta_data (jsonb), is_super_admin (boolean), created_at (timestamp with time zone), updated_at (timestamp with time zone), phone (text), phone_confirmed_at (timestamp with time zone), phone_change (text), phone_change_token (character varying(255)), phone_change_sent_at (timestamp with time zone), confirmed_at (timestamp with time zone), email_change_token_current (character varying(255)), email_change_confirm_status (smallint), banned_until (timestamp with time zone), reauthentication_token (character varying(255)), reauthentication_sent_at (timestamp with time zone), is_sso_user (boolean), deleted_at (timestamp with time zone), is_anonymous (boolean)
historique.action_precision: id (integer), collectivite_id (integer), action_id (action_id), precision (text), previous_precision (text), modified_by (uuid), previous_modified_by (uuid), modified_at (timestamp with time zone), previous_modified_at (timestamp with time zone)
historique.action_statut: id (integer), collectivite_id (integer), action_id (action_id), avancement (avancement), previous_avancement (avancement), avancement_detaille (numeric[]), previous_avancement_detaille (numeric[]), concerne (boolean), previous_concerne (boolean), modified_by (uuid), previous_modified_by (uuid), modified_at (timestamp with time zone), previous_modified_at (timestamp with time zone)
historique.fiche_action: id (integer), fiche_id (integer), titre (character varying(300)), previous_titre (character varying(300)), description (character varying(20000)), previous_description (character varying(20000)), piliers_eci (text[]), previous_piliers_eci (text[]), objectifs (character varying(10000)), previous_objectifs (character varying(10000)), resultats_attendus (text[]), previous_resultats_attendus (text[]), cibles (text[]), previous_cibles (text[]), ressources (character varying(10000)), previous_ressources (character varying(10000)), financements (text), previous_financements (text), budget_previsionnel (numeric(12,0)), previous_budget_previsionnel (numeric(12,0)), statut (text), previous_statut (text), niveau_priorite (text), previous_niveau_priorite (text), date_debut (timestamp with time zone), previous_date_debut (timestamp with time zone), date_fin_provisoire (timestamp with time zone), previous_date_fin_provisoire (timestamp with time zone), amelioration_continue (boolean), previous_amelioration_continue (boolean), maj_termine (boolean), previous_maj_termine (boolean), collectivite_id (integer), created_at (timestamp with time zone), modified_at (timestamp with time zone), previous_modified_at (timestamp with time zone), modified_by (uuid), previous_modified_by (uuid), restreint (boolean), previous_restreint (boolean), deleted (boolean)
historique.fiche_action_pilote: id (integer), fiche_historise_id (integer), user_id (uuid), tag_nom (text), previous (boolean)
historique.justification: id (integer), collectivite_id (integer), question_id (question_id), modified_by (uuid), previous_modified_by (uuid), modified_at (timestamp with time zone), previous_modified_at (timestamp with time zone), texte (text), previous_texte (text)
historique.justification_ajustement: id (integer), collectivite_id (integer), action_id (action_id), modified_by (uuid), previous_modified_by (uuid), modified_at (timestamp with time zone), previous_modified_at (timestamp with time zone), texte (text), previous_texte (text)
historique.reponse_binaire: id (integer), collectivite_id (integer), question_id (question_id), reponse (boolean), previous_reponse (boolean), modified_by (uuid), modified_at (timestamp with time zone)
historique.reponse_choix: id (integer), collectivite_id (integer), question_id (question_id), reponse (choix_id), previous_reponse (choix_id), modified_by (uuid), modified_at (timestamp with time zone)
historique.reponse_proportion: id (integer), collectivite_id (integer), question_id (question_id), reponse (double precision), previous_reponse (double precision), modified_by (uuid), modified_at (timestamp with time zone)
labellisation.action_audit_state: id (integer), audit_id (integer), action_id (action_id), collectivite_id (integer), modified_by (uuid), modified_at (timestamp with time zone), ordre_du_jour (boolean), avis (text), statut (audit_statut)
labellisation.audit: id (integer), collectivite_id (integer), referentiel (referentiel), demande_id (integer), date_debut (timestamp with time zone), date_fin (timestamp with time zone), valide (boolean), date_cnl (timestamp with time zone), valide_labellisation (boolean), clos (boolean)
labellisation.bibliotheque_fichier: id (integer), collectivite_id (integer), hash (character varying(160)), filename (text), confidentiel (boolean)
labellisation.demande: id (integer), en_cours (boolean), collectivite_id (integer), referentiel (referentiel), etoiles (labellisation.etoile), date (timestamp with time zone), sujet (labellisation.sujet_demande), modified_at (timestamp with time zone), envoyee_le (timestamp with time zone), demandeur (uuid), associated_collectivite_id (integer)
labellisation.etoile_meta: etoile (labellisation.etoile), prochaine_etoile (labellisation.etoile), long_label (character varying(30)), short_label (character varying(15)), min_realise_percentage (integer), min_realise_score (double precision)
labellisation.preuve_base: collectivite_id (integer), fichier_id (integer), url (text), titre (text), commentaire (text), modified_by (uuid), modified_at (timestamp with time zone), lien (jsonb)
notifications.notification: id (integer), entity_id (text), status (text), send_to (uuid), sent_at (timestamp with time zone), sent_to_email (text), error_message (text), retries (integer), created_by (uuid), created_at (timestamp with time zone), notified_on (text), notification_data (jsonb), send_after (timestamp with time zone)
public.abstract_any_indicateur_value: modified_at (timestamp with time zone), valeur (double precision), annee (integer)
public.abstract_modified_at: modified_at (timestamp with time zone)
public.action_commentaire: collectivite_id (integer), action_id (action_id), commentaire (text), modified_by (uuid), modified_at (timestamp with time zone)
public.action_computed_points: modified_at (timestamp with time zone), action_id (action_id), value (double precision)
public.action_de_reference: id (integer), titre (text), description (text), code (text), leviers (levier_ges_id[]), categories (volet_categorie[])
public.action_de_reference_fiche: action_de_reference_id (integer), fiche_id (integer)
public.action_definition: modified_at (timestamp with time zone), action_id (action_id), referentiel (referentiel), identifiant (text), nom (text), description (text), contexte (text), exemples (text), ressources (text), preuve (text), points (double precision), pourcentage (double precision), reduction_potentiel (text), perimetre_evaluation (text), categorie (action_categorie), referentiel_id (character varying(30)), referentiel_version (character varying(16)), expr_score (text), adaptation_niveau (text), thematique_sgpe (text)
public.action_definition_tag: referentiel_id (character varying(30)), action_id (character varying(30)), tag_ref (character varying(300))
public.action_impact: id (integer), titre (text), description (text), description_complementaire (text), nb_collectivite_en_cours (integer), nb_collectivite_realise (integer), action_continue (boolean), temps_de_mise_en_oeuvre (integer), fourchette_budgetaire (integer), impact_tier (integer), subventions_mobilisables (jsonb), ressources_externes (jsonb), rex (jsonb), competences_communales (boolean), independamment_competences (boolean), typologie_id (integer)
public.action_impact_action: action_impact_id (integer), action_id (action_id)
public.action_impact_banatic_competence: action_impact_id (integer), competence_code (integer)
public.action_impact_categorie: id (text), nom (text)
public.action_impact_categorie_fnv: action_impact_id (integer), categorie_fnv_id (integer)
public.action_impact_complexite: niveau (integer), nom (text)
public.action_impact_effet_attendu: action_impact_id (integer), effet_attendu_id (integer)
public.action_impact_fiche_action: fiche_id (integer), action_impact_id (integer)
public.action_impact_fourchette_budgetaire: niveau (integer), nom (text)
public.action_impact_indicateur: action_impact_id (integer), indicateur_id (integer)
public.action_impact_panier: panier_id (uuid), action_id (integer)
public.action_impact_partenaire: action_impact_id (integer), partenaire_id (integer)
public.action_impact_sous_thematique: action_impact_id (integer), sous_thematique_id (integer)
public.action_impact_state: action (action_impact), statut (action_impact_statut), isinpanier (boolean), panier (panier)
public.action_impact_statut: panier_id (uuid), action_id (integer), categorie_id (text)
public.action_impact_temps_de_mise_en_oeuvre: niveau (integer), nom (text)
public.action_impact_thematique: action_impact_id (integer), thematique_id (integer), ordre (integer)
public.action_impact_tier: niveau (integer), nom (text)
public.action_impact_typologie: id (integer), nom (text)
public.action_origine: referentiel_id (character varying(30)), action_id (character varying(30)), origine_referentiel_id (character varying(30)), origine_action_id (character varying(30)), ponderation (double precision)
public.action_origine_texte: referentiel_id (character varying(30)), action_id (character varying(30)), origine_referentiel_id (character varying(30)), origine_action_id (character varying(30))
public.action_pilote: collectivite_id (integer), action_id (action_id), user_id (uuid), tag_id (integer)
public.action_relation: id (action_id), referentiel (referentiel), parent (action_id)
public.action_score_indicateur_valeur: action_id (action_id), collectivite_id (integer), indicateur_id (integer), indicateur_valeur_id (integer), type_score (text)
public.action_service: collectivite_id (integer), action_id (action_id), service_tag_id (integer)
public.action_statut: collectivite_id (integer), action_id (action_id), avancement (avancement), concerne (boolean), modified_by (uuid), modified_at (timestamp with time zone), avancement_detaille (double precision[])
public.ai_plan_import_job: id (uuid), collectivite_id (integer), created_by (uuid), status (text), options (jsonb), step_states (jsonb), source_path (text), draft (jsonb), error (text), created_at (timestamp with time zone), modified_at (timestamp with time zone), created_plan_id (integer), fichier_id (integer), started_at (timestamp with time zone), finished_at (timestamp with time zone), stats (jsonb), checkpoint (jsonb), attempt (integer)
public.ai_plan_import_step_run: id (uuid), job_id (uuid), step (text), status (text), started_at (timestamp with time zone), ended_at (timestamp with time zone), duration_ms (integer), llm_calls (integer), failed_calls (integer), rate_limited_calls (integer), tokens (jsonb), models (text[]), details (jsonb), error (text), attempt (integer)
public.analysis_run: id (integer), started_at (timestamp with time zone), finished_at (timestamp with time zone)
public.annexe: id (integer), collectivite_id (integer), fichier_id (integer), url (text), titre (text), commentaire (text), modified_by (uuid), modified_at (timestamp with time zone), lien (jsonb), fiche_id (integer)
public.audit_auditeur: audit_id (integer), auditeur (uuid), created_at (timestamp with time zone)
public.audit_preuves_archive: id (uuid), collectivite_id (integer), referentiel_id (text), audit_id (integer), requested_by (uuid), status (text), total_files (integer), processed_files (integer), storage_path (text), error_message (text), created_at (timestamp with time zone), modified_at (timestamp with time zone), expires_at (timestamp with time zone)
public.axe: modified_at (timestamp with time zone), id (integer), nom (text), collectivite_id (integer), parent (integer), created_at (timestamp with time zone), modified_by (uuid), plan (integer), type (integer), panier_id (uuid), description (text), date_debut (date), date_fin (date), source (text), verified_at (timestamp with time zone), verified_by (uuid), status (text)
public.axe_indicateur: indicateur_id (integer), axe_id (integer), created_at (timestamp with time zone), created_by (uuid)
public.banatic_2021_2025_crosswalk: id (bigint), code_2021 (integer), code_2025 (integer), mapping_type (text)
public.banatic_2025_competence: competence_code (integer), intitule (text), version (character varying(16))
public.banatic_competence: code (integer), nom (text)
public.banner_info: id (integer), type (text), info (text), modified_at (timestamp with time zone), modified_by (uuid), active (boolean)
public.categorie_fnv: id (integer), nom (text)
public.categorie_tag: id (integer), groupement_id (integer), collectivite_id (integer), nom (text), visible (boolean), created_at (timestamp with time zone), created_by (uuid)
public.client_scores: collectivite_id (integer), referentiel (referentiel), scores (jsonb), modified_at (timestamp with time zone), payload_timestamp (timestamp with time zone)
public.collectivite: id (integer), created_at (timestamp with time zone), modified_at (timestamp with time zone), access_restreint (boolean), nom (text), type (text), commune_code (codegeo), siren (siren), departement_code (character varying(3)), region_code (character varying(2)), nature_insee (text), population (integer), dans_aire_urbaine (boolean), nic (character varying(5)), preferences (jsonb), sinoe_id (character varying(32))
public.collectivite_banatic_2025_competence: collectivite_id (integer), competence_code (integer), exercice (boolean), created_at (timestamp with time zone)
public.collectivite_banatic_2025_perimetre: collectivite_id (integer), nb_communes_membres (integer), created_at (timestamp with time zone)
public.collectivite_banatic_2025_transfert: collectivite_id (integer), competence_code (integer), nature_transfert (text), created_at (timestamp with time zone), nb_communes_transferees (integer)
public.collectivite_banatic_competence: collectivite_id (integer), competence_code (integer)
public.collectivite_banatic_type: id (text), nom (text), type (text)
public.collectivite_bucket: collectivite_id (integer), bucket_id (text)
public.collectivite_levier_ges_pertinence: collectivite_id (integer), levier_id (levier_ges_id), categorie (volet_categorie), pertinence (levier_pertinence), modified_at (timestamp with time zone), modified_by (uuid)
public.collectivite_perimetre_secondaire: id (integer), collectivite_id (integer), region_code (character varying(2)), departement_code (character varying(3)), source (text), created_at (timestamp with time zone)
public.collectivite_relations: id (integer), parent_id (integer)
public.collectivite_test: id (integer), collectivite_id (integer), nom (character varying(300))
public.collectivite_volet_ges: collectivite_id (integer), levier_id (levier_ges_id), categorie (volet_categorie), note (smallint), fiche_ids (integer[]), created_at (timestamp with time zone)
public.commune: id (integer), collectivite_id (integer), nom (character varying(300)), code (codegeo)
public.cot: collectivite_id (integer), actif (boolean), signataire (integer)
public.dcp: user_id (uuid), nom (text), prenom (text), email (text), limited (boolean), deleted (boolean), created_at (timestamp with time zone), modified_at (timestamp with time zone), telephone (character varying(30)), cgu_acceptees_le (timestamp with time zone), preferences (jsonb)
public.demarche: id (integer), collectivite_id (integer), type (text), titre (text), description (text), status (text), obligation (text), launched_at (timestamp with time zone), published_at (timestamp with time zone), transmitted_at (timestamp with time zone), avis_deadline_at (timestamp with time zone), created_at (timestamp with time zone), created_by (uuid), modified_at (timestamp with time zone), modified_by (uuid), adopted_at (date), transmitted_off_platform (boolean), is_scot_aec (boolean)
public.demarche_definition: demarche_type (text), documents_additional_amont (boolean), documents_additional_aval (boolean), documents_formats_autorises (text[]), documents_mime_types_autorises (text[]), created_at (timestamp with time zone), modified_at (timestamp with time zone)
public.demarche_document: id (integer), collectivite_id (integer), fichier_id (integer), url (text), titre (text), commentaire (text), modified_by (uuid), modified_at (timestamp with time zone), lien (jsonb), demarche_id (integer), document_id (text), etape (text)
public.demarche_document_additional: id (integer), collectivite_id (integer), fichier_id (integer), url (text), titre (text), commentaire (text), modified_by (uuid), modified_at (timestamp with time zone), lien (jsonb), demarche_id (integer), etape (text)
public.demarche_document_definition: id (text), demarche_type (text), nom (text), description (text), requis (boolean), ordre (integer), created_at (timestamp with time zone), modified_at (timestamp with time zone), etape (text), expr_applicable (text)
public.demarche_document_substitution: document_id (text), substitut_id (text), automatic (boolean)
public.demarche_pcaet_avis: id (uuid), demande_avis_id (integer), emetteur_collectivite_id (integer), au_titre_de (text), fichier_ref (text), valide_le (timestamp with time zone), depose_par (uuid), depose_le (timestamp with time zone), modifie_le (timestamp with time zone), envoye_le (timestamp with time zone)
public.demarche_pcaet_demande_avis: id (integer), demarche_id (integer), instructeur_collectivite_id (integer), source (text), created_at (timestamp with time zone), perimetre (text)
public.demarche_pcaet_source_metadonnee: demarche_id (integer), collectivite_id (integer), metadonnee_id (integer)
public.demarche_pcaet_vulnerabilite_thematique: id (integer), code (text), label (text), collectivite_id (integer), requis (boolean), display_order (integer), created_at (timestamp with time zone), created_by (uuid), modified_at (timestamp with time zone), modified_by (uuid), parent_id (integer)
public.demarche_pcaet_vulnerabilite_valeur: demarche_id (integer), thematique_id (integer), niveau_maintenant (text), niveau_2050 (text), niveau_2100 (text), objectifs_2050 (text), objectifs_2100 (text), created_at (timestamp with time zone), created_by (uuid), modified_at (timestamp with time zone), modified_by (uuid)
public.demarche_pilote: demarche_id (integer), tag_id (integer), user_id (uuid), created_at (timestamp with time zone), created_by (uuid)
public.demarche_plan_action: demarche_id (integer), plan_action_id (integer), created_at (timestamp with time zone), created_by (uuid)
public.demarche_status_history: id (integer), demarche_id (integer), from_status (text), to_status (text), transition (text), created_at (timestamp with time zone), created_by (uuid)
public.discussion: id (integer), collectivite_id (integer), action_id (action_id), created_by (uuid), created_at (timestamp with time zone), modified_at (timestamp with time zone), status (action_discussion_statut)
public.discussion_message: id (integer), created_by (uuid), created_at (timestamp with time zone), discussion_id (integer), message (text)
public.effet_attendu: id (integer), nom (text), notice (text)
public.epci: id (integer), collectivite_id (integer), nom (character varying(300)), siren (siren), nature (nature)
public.fiche_action: modified_at (timestamp with time zone), id (integer), titre (character varying(300)), description (character varying(20000)), piliers_eci (fiche_action_piliers_eci[]), objectifs (character varying(10000)), resultats_attendus (fiche_action_resultats_attendus[]), cibles (text[]), ressources (character varying(10000)), financements (text), budget_previsionnel (numeric(12,0)), statut (fiche_action_statuts), niveau_priorite (fiche_action_niveaux_priorite), date_debut (timestamp with time zone), date_fin_provisoire (timestamp with time zone), amelioration_continue (boolean), maj_termine (boolean), collectivite_id (integer), created_at (timestamp with time zone), modified_by (uuid), restreint (boolean), instance_gouvernance (text), participation_citoyenne (text), participation_citoyenne_type (character varying(30)), temps_de_mise_en_oeuvre_id (integer), created_by (uuid), parent_id (integer), deleted (boolean)
public.fiche_action_action: fiche_id (integer), action_id (action_id)
public.fiche_action_analysis: fiche_id (integer), collectivite_id (integer), fingerprint (text), status (text), retry_count (integer), analyzed_at (timestamp with time zone)
public.fiche_action_axe: fiche_id (integer), axe_id (integer), created_at (timestamp with time zone), created_by (uuid)
public.fiche_action_budget: id (integer), fiche_id (integer), type (text), unite (text), annee (integer), budget_previsionnel (numeric(14,2)), budget_reel (numeric(14,2)), est_etale (boolean)
public.fiche_action_effet_attendu: fiche_id (integer), effet_attendu_id (integer)
public.fiche_action_etape: id (integer), fiche_id (integer), nom (text), ordre (integer), realise (boolean), modified_at (timestamp with time zone), created_at (timestamp with time zone), modified_by (uuid), created_by (uuid)
public.fiche_action_financeur_tag: id (integer), fiche_id (integer), financeur_tag_id (integer), montant_ttc (integer)
public.fiche_action_import_csv: axe (text), sous_axe (text), sous_sous_axe (text), num_action (text), titre (text), description (text), objectifs (text), resultats_attendus (text), cibles (text), structure_pilote (text), moyens (text), partenaires (text), personne_referente (text), elu_referent (text), financements (text), budget (text), statut (text), priorite (text), date_debut (text), date_fin (text), amelioration_continue (text), calendrier (text), notes (text), collectivite_id (text), plan_nom (text), service (text), financeur_un (text), montant_un (text), financeur_deux (text), montant_deux (text), financeur_trois (text), montant_trois (text)
public.fiche_action_indicateur: indicateur_id (integer), fiche_id (integer), created_at (timestamp with time zone), created_by (uuid)
public.fiche_action_instance_de_gouvernance_tag: fiche_action_id (integer), instance_de_gouvernance_tag_id (integer), created_by (uuid), created_at (timestamp without time zone)
public.fiche_action_libre_tag: fiche_id (integer), libre_tag_id (integer), created_at (timestamp with time zone), created_by (uuid)
public.fiche_action_lien: fiche_une (integer), fiche_deux (integer)
public.fiche_action_note: fiche_id (integer), date_note (date), note (text), modified_at (timestamp with time zone), created_at (timestamp with time zone), modified_by (uuid), created_by (uuid), id (integer)
public.fiche_action_partenaire_tag: fiche_id (integer), partenaire_tag_id (integer)
public.fiche_action_pilote: fiche_id (integer), user_id (uuid), tag_id (integer), created_at (timestamp with time zone), created_by (uuid)
public.fiche_action_referent: fiche_id (integer), user_id (uuid), tag_id (integer), created_at (timestamp with time zone), created_by (uuid)
public.fiche_action_secteur_attribution: fiche_id (integer), secteurs (secteur_reglementaire[]), origine (text), methode (text), reponse_communs (jsonb), modified_at (timestamp with time zone), modified_by (uuid), justification (text)
public.fiche_action_service_tag: fiche_id (integer), service_tag_id (integer)
public.fiche_action_sharing: fiche_id (integer), collectivite_id (integer), created_at (timestamp with time zone), created_by (uuid)
public.fiche_action_sous_thematique: fiche_id (integer), thematique_id (integer), created_at (timestamp with time zone), created_by (uuid)
public.fiche_action_structure_tag: fiche_id (integer), structure_tag_id (integer)
public.fiche_action_thematique: fiche_id (integer), thematique_id (integer), created_at (timestamp with time zone), created_by (uuid)
public.fiche_action_volet_ges: fiche_id (integer), levier_id (levier_ges_id), categorie (volet_categorie), created_at (timestamp with time zone)
public.filtre_intervalle: type (collectivite_filtre_type), id (character varying(30)), libelle (text), intervalle (numrange)
public.financeur_tag: id (integer), nom (text), collectivite_id (integer), created_at (timestamp with time zone), created_by (uuid)
public.groupement: id (integer), nom (text)
public.groupement_collectivite: groupement_id (integer), collectivite_id (integer)
public.indicateur_action: indicateur_id (integer), action_id (action_id)
public.indicateur_artificialisation: collectivite_id (integer), total (double precision), activite (double precision), habitat (double precision), mixte (double precision), routiere (double precision), ferroviaire (double precision), inconnue (double precision)
public.indicateur_categorie_tag: categorie_tag_id (integer), indicateur_id (integer)
public.indicateur_collectivite: indicateur_id (integer), collectivite_id (integer), commentaire (text), confidentiel (boolean), favoris (boolean), modified_by (uuid), modified_at (timestamp with time zone), is_applicable (boolean), is_suivi (boolean)
public.indicateur_definition: id (integer), groupement_id (integer), collectivite_id (integer), identifiant_referentiel (text), titre (text), titre_long (text), description (text), unite (text), borne_min (double precision), borne_max (double precision), participation_score (boolean), sans_valeur_utilisateur (boolean), valeur_calcule (text), modified_at (timestamp with time zone), created_at (timestamp with time zone), modified_by (uuid), created_by (uuid), titre_court (text), version (character varying(16)), precision (integer), expr_cible (text), expr_seuil (text), libelle_cible_seuil (text), periodicite (text), aggregation_resultat (text), aggregation_objectif (text)
public.indicateur_groupe: parent (integer), enfant (integer)
public.indicateur_objectif: indicateur_id (integer), date_valeur (date), formule (text)
public.indicateur_pilote: id (integer), indicateur_id (integer), user_id (uuid), tag_id (integer), collectivite_id (integer)
public.indicateur_service_tag: indicateur_id (integer), service_tag_id (integer), collectivite_id (integer)
public.indicateur_source: id (text), libelle (text), ordre_affichage (integer)
public.indicateur_source_metadonnee: id (integer), source_id (text), date_version (timestamp without time zone), nom_donnees (text), diffuseur (text), producteur (text), methodologie (text), limites (text)
public.indicateur_source_source_calcul: source_id (text), source_calcul_id (text)
public.indicateur_sous_thematique: indicateur_id (integer), sous_thematique_id (integer)
public.indicateur_thematique: indicateur_id (integer), thematique_id (integer)
public.indicateur_valeur: id (integer), indicateur_id (integer), collectivite_id (integer), date_valeur (date), metadonnee_id (integer), resultat (double precision), resultat_commentaire (text), objectif (double precision), objectif_commentaire (text), estimation (double precision), modified_at (timestamp with time zone), created_at (timestamp with time zone), modified_by (uuid), created_by (uuid), calcul_auto (boolean), calcul_auto_identifiants_manquants (text[]), periodicite (text)
public.indicateur_vue: id (uuid), collectivite_id (integer), nom (character varying(100)), filtres (jsonb), created_at (timestamp with time zone), modified_at (timestamp with time zone), created_by (uuid), modified_by (uuid)
public.instance_de_gouvernance_tag: id (integer), nom (character varying(255)), collectivite_id (integer), created_by (uuid), created_at (timestamp without time zone)
public.justification: collectivite_id (integer), question_id (question_id), modified_by (uuid), texte (text), modified_at (timestamp with time zone)
public.justification_ajustement: collectivite_id (integer), action_id (action_id), texte (text), modified_by (uuid), modified_at (timestamp with time zone)
public.labellisation: id (integer), collectivite_id (integer), referentiel (referentiel), obtenue_le (timestamp without time zone), annee (double precision), etoiles (integer), score_realise (double precision), score_programme (double precision), audit_id (integer)
public.labellisation_action_critere: etoile (labellisation.etoile), prio (integer), referentiel (referentiel), action_id (action_id), formulation (text), min_realise_percentage (integer), min_programme_percentage (integer), min_realise_score (double precision), min_programme_score (double precision)
public.labellisation_calendrier: referentiel (referentiel), information (text)
public.labellisation_fichier_critere: referentiel (referentiel), etoile (labellisation.etoile), description (text)
public.libre_tag: id (integer), nom (text), collectivite_id (integer), created_at (timestamp with time zone), created_by (uuid)
public.panier: id (uuid), created_at (timestamp with time zone), created_by (uuid), collectivite_id (integer), collectivite_preset (integer), latest_update (timestamp with time zone), private (boolean)
public.panier_partenaire: id (integer), nom (text)
public.partenaire_tag: id (integer), nom (text), collectivite_id (integer), created_at (timestamp with time zone), created_by (uuid)
public.personnalisation_consequence: modified_at (timestamp with time zone), collectivite_id (integer), consequences (jsonb), payload_timestamp (timestamp with time zone)
public.personnalisation_regle: action_id (action_id), type (regle_type), formule (text), description (text), modified_at (timestamp with time zone)
public.personne_tag: id (integer), nom (text), collectivite_id (integer), created_at (timestamp with time zone), created_by (uuid)
public.plan_action_type: id (integer), categorie (text), type (text), detail (text)
public.plan_action_type_categorie: categorie (text)
public.plan_pilote: plan_id (integer), tag_id (integer), user_id (uuid), created_at (timestamp with time zone), created_by (uuid)
public.plan_referent: plan_id (integer), tag_id (integer), user_id (uuid), created_at (timestamp with time zone), created_by (uuid)
public.plan_report_generation: id (uuid), plan_id (integer), template_ref (text), file_id (integer), options (jsonb), status (text), error_message (text), created_at (timestamp with time zone), modified_at (timestamp with time zone), created_by (uuid), collectivite_id (integer), name (text)
public.post_audit_scores: collectivite_id (integer), referentiel (referentiel), scores (jsonb), modified_at (timestamp with time zone), payload_timestamp (timestamp with time zone), audit_id (integer)
public.pre_audit_scores: collectivite_id (integer), referentiel (referentiel), scores (jsonb), modified_at (timestamp with time zone), payload_timestamp (timestamp with time zone), audit_id (integer)
public.preuve_action: preuve_id (preuve_id), action_id (action_id)
public.preuve_audit: id (integer), collectivite_id (integer), fichier_id (integer), url (text), titre (text), commentaire (text), modified_by (uuid), modified_at (timestamp with time zone), lien (jsonb), audit_id (integer)
public.preuve_complementaire: id (integer), collectivite_id (integer), fichier_id (integer), url (text), titre (text), commentaire (text), modified_by (uuid), modified_at (timestamp with time zone), lien (jsonb), action_id (action_id)
public.preuve_labellisation: id (integer), collectivite_id (integer), fichier_id (integer), url (text), titre (text), commentaire (text), modified_by (uuid), modified_at (timestamp with time zone), lien (jsonb), demande_id (integer), objet (labellisation.objet_preuve)
public.preuve_rapport: id (integer), collectivite_id (integer), fichier_id (integer), url (text), titre (text), commentaire (text), modified_by (uuid), modified_at (timestamp with time zone), lien (jsonb), date (timestamp with time zone)
public.preuve_reglementaire: id (integer), collectivite_id (integer), fichier_id (integer), url (text), titre (text), commentaire (text), modified_by (uuid), modified_at (timestamp with time zone), lien (jsonb), preuve_id (preuve_id)
public.preuve_reglementaire_definition: id (preuve_id), nom (text), description (text)
public.private_collectivite_membre: user_id (uuid), collectivite_id (integer), fonction (membre_fonction), details_fonction (text), champ_intervention (referentiel[]), created_at (timestamp with time zone), modified_at (timestamp with time zone), est_referent (boolean)
public.private_utilisateur_droit: id (integer), user_id (uuid), collectivite_id (integer), active (boolean), created_at (timestamp with time zone), modified_at (timestamp with time zone), niveau_acces (niveau_acces), invitation_id (uuid)
public.question: id (question_id), thematique_id (character varying), ordonnancement (integer), types_collectivites_concernees (text[]), type (question_type), description (text), formulation (text), version (character varying(16)), competence_code (integer), consignes_justification (text), expr_visible (text)
public.question_action: question_id (question_id), action_id (action_id)
public.question_choix: question_id (question_id), id (choix_id), ordonnancement (integer), formulation (text), version (character varying(16))
public.question_thematique: id (character varying(30)), nom (text)
public.referentiel_definition: id (character varying(30)), nom (character varying(300)), version (character varying(16)), hierarchie (action_type[]), created_at (timestamp with time zone), modified_at (timestamp with time zone), locked (boolean)
public.referentiel_tag: ref (character varying(300)), nom (character varying(300)), type (character varying(300))
public.reponse_binaire: modified_at (timestamp with time zone), collectivite_id (integer), question_id (question_id), reponse (boolean)
public.reponse_choix: modified_at (timestamp with time zone), collectivite_id (integer), question_id (question_id), reponse (choix_id)
public.reponse_proportion: modified_at (timestamp with time zone), collectivite_id (integer), question_id (question_id), reponse (double precision)
public.row_count: datid (oid), datname (name), pid (integer), leader_pid (integer), usesysid (oid), usename (name), application_name (text), client_addr (inet), client_hostname (text), client_port (integer), backend_start (timestamp with time zone), xact_start (timestamp with time zone), query_start (timestamp with time zone), state_change (timestamp with time zone), wait_event_type (text), wait_event (text), state (text), backend_xid (xid), backend_xmin (xid), query_id (bigint), query (text), backend_type (text)
public.score_snapshot: collectivite_id (integer), referentiel_id (character varying(30)), referentiel_version (character varying(16)), audit_id (integer), date (timestamp with time zone), ref (character varying(30)), nom (character varying(300)), type_jalon (character varying(30)), point_fait (double precision), point_programme (double precision), point_pas_fait (double precision), point_potentiel (double precision), referentiel_scores (jsonb), personnalisation_reponses (jsonb), created_by (uuid), created_at (timestamp with time zone), modified_by (uuid), modified_at (timestamp with time zone), etoiles (integer)
public.service_tag: id (integer), nom (text), collectivite_id (integer), created_at (timestamp with time zone), created_by (uuid)
public.site_contact: modified_at (timestamp with time zone), email (text), formulaire (jsonb)
public.sous_thematique: id (integer), sous_thematique (text), thematique_id (integer)
public.structure_tag: id (integer), nom (text), collectivite_id (integer), created_at (timestamp with time zone), created_by (uuid)
public.tableau_de_bord_module: id (uuid), collectivite_id (integer), user_id (uuid), titre (character varying), default_key (character varying), type (character varying), options (jsonb), created_at (timestamp with time zone), modified_at (timestamp with time zone)
public.thematique: nom (text), id (integer), md_id (character varying)
public.typologie_sinoe: id (character varying(32)), code_sinoe (character varying(4)), libelle (text)
public.usage: time (timestamp with time zone), fonction (usage_fonction), action (usage_action), page (visite_page), user_id (uuid), collectivite_id (integer)
public.usage_backup: time (timestamp with time zone), fonction (usage_fonction), action (usage_action), page (visite_page), user_id (uuid), collectivite_id (integer)
public.user_api_key: client_id (text), user_id (uuid), client_secret_hash (text), client_secret_truncated (text), permissions (text[]), created_at (timestamp with time zone), modified_at (timestamp with time zone)
public.utilisateur_identite_oidc: provider (text), sub (text), user_id (uuid), email (text), siret (text), idp_id (text), claims (jsonb), created_at (timestamp with time zone), last_sign_in_at (timestamp with time zone)
public.utilisateur_identite_oidc_invitation: id (uuid), token_hash (text), provider (text), sub (text), claims (jsonb), email_provider (text), initial_mail (text), user_id (uuid), created_at (timestamp with time zone), expires_at (timestamp with time zone), confirmed_at (timestamp with time zone)
public.utilisateur_invitation_envoi: collectivite_id (integer), email (text), motif (text), invitation_id (uuid), envoye_le (timestamp with time zone), tentatives (integer), dernier_echec (text), created_at (timestamp with time zone), modified_at (timestamp with time zone)
public.utilisateur_support: user_id (uuid), support (boolean), is_support_mode_enabled (boolean)
public.utilisateur_verifie: user_id (uuid), verifie (boolean)
public.visite: time (timestamp with time zone), page (visite_page), tag (visite_tag), onglet (visite_onglet), user_id (uuid), collectivite_id (integer)
public.visite_backup: time (timestamp with time zone), page (visite_page), tag (visite_tag), onglet (visite_onglet), user_id (uuid), collectivite_id (integer)
"""