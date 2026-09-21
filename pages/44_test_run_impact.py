import streamlit as st

st.set_page_config(
    page_title="Test variance implication",
    page_icon="🧪",
    layout="wide",
)

from pathlib import Path

from openai import OpenAI

from utils.collectivite_selection import (
    default_collectivite_index,
    set_selected_collectivite,
)
from utils.priorisation_data import load_collectivites_priorisees
from utils.test_run_impact import (
    FLEX_TIMEOUT_S,
    append_result,
    cache_hit_pct,
    classification_from_json,
    collect_action_ids,
    compute_stats,
    estimate_run_costs,
    file_label,
    find_incomplete_runs,
    format_usd,
    format_usage_cost_line,
    init_payload,
    load_fiches_by_ids,
    load_payload,
    load_run_inputs,
    list_run_files,
    new_run_path,
    payload_cost_usd,
    payload_is_flex,
    payload_token_totals,
    pause_between_calls,
    pending_work,
    save_payload,
    score_one_lever,
    score_one_lever_mock,
    typical_tokens_per_call,
    uncached_input_tokens,
    usage_cost_usd,
)

SESSION_LAST_FILE = "test_run_impact_last_file"

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"], timeout=FLEX_TIMEOUT_S)

st.title("Test de variance — prompt d'implication")
st.markdown(
    "Relance le **même prompt d'implication** (mobilisation 0–3) plusieurs fois "
    "sur une classification OLAP déjà figée, pour mesurer la variance des notes. "
    "Aucune écriture en base : les résultats sont checkpointés dans un JSON."
)

df_collectivites = load_collectivites_priorisees()
if df_collectivites.empty:
    st.warning("Aucune collectivité avec des actions déjà classifiées en OLAP.")
    st.stop()

nom_par_id = df_collectivites.set_index("collectivite_id")["nom"].to_dict()
collectivite_ids = df_collectivites["collectivite_id"].tolist()

collectivite_id = st.selectbox(
    "Collectivité",
    options=collectivite_ids,
    index=default_collectivite_index(collectivite_ids),
    format_func=lambda cid: nom_par_id[cid],
    key="test_run_impact_collectivite",
)
set_selected_collectivite(collectivite_id)

col_cfg1, col_cfg2, col_cfg3, col_cfg4 = st.columns(4)
with col_cfg1:
    n_runs = st.number_input(
        "Nombre de runs",
        min_value=2,
        max_value=30,
        value=10,
        step=1,
    )
with col_cfg2:
    debug_mode = st.toggle(
        "Mode débogage (notes aléatoires, sans API)",
        value=False,
    )
with col_cfg3:
    reasoning_low = st.toggle(
        "Low reasoning (medium par défaut)",
        value=False,
    )
with col_cfg4:
    use_flex = st.toggle(
        "Flex (tarif batch, plus lent)",
        value=True,
        help=(
            "Même tarif que le Batch (−50 %), mais synchrone. "
            "Le cache réduit l'entrée ; Flex réduit aussi la sortie (raisonnement)."
        ),
    )

try:
    inputs = load_run_inputs(int(collectivite_id))
except Exception as e:
    st.error(f"Impossible de charger les données : {e}")
    st.stop()

n_appels = inputs["n_leviers"] * int(n_runs)
st.info(
    f"**{inputs['collectivite_nom']}** (ID {collectivite_id}) — "
    f"population {inputs['population']:,} — "
    f"**{inputs['n_leviers']} leviers** classifiés, "
    f"**{inputs['n_volets']} volets** avec au moins une action, "
    f"**{inputs['n_actions']} fiches**. "
    f"Un run complet = **{n_appels} appels** "
    f"({inputs['n_leviers']} leviers × {int(n_runs)} runs)."
)

avg_in, avg_out = typical_tokens_per_call(int(collectivite_id))
estimates = estimate_run_costs(
    inputs["n_leviers"],
    int(n_runs),
    avg_in,
    avg_out,
)
chosen_estimate = estimates["flex_cache"] if use_flex else estimates["cache"]
st.caption(
    f"Coût estimé (moy. {avg_in:,} tokens entrée / {avg_out:,} sortie par appel) — "
    f"standard sans cache **{format_usd(float(estimates['standard']))}** · "
    f"cache **{format_usd(float(estimates['cache']))}** · "
    f"Flex + cache **{format_usd(float(estimates['flex_cache']))}**. "
    f"Lancement actuel : **{format_usd(float(chosen_estimate))}**."
)

if debug_mode:
    st.warning("Mode débogage activé — les notes seront tirées au hasard.")

incomplete_paths = find_incomplete_runs(int(collectivite_id))
resume_path: Path | None = None
if incomplete_paths:
    st.subheader("Run incomplet")
    resume_path = st.selectbox(
        "Reprendre un JSON interrompu",
        options=incomplete_paths,
        format_func=file_label,
        key="test_run_impact_resume",
    )
    resume_payload = load_payload(resume_path)
    n_pending = len(pending_work(resume_payload))
    st.caption(
        f"{n_pending} appels restants dans `{resume_path.name}` "
        f"(statut : {resume_payload.get('meta', {}).get('status')})."
    )

col_run, col_resume = st.columns(2)
launch = col_run.button("Lancer un nouveau test", type="primary")
resume = col_resume.button(
    "Reprendre le run sélectionné",
    disabled=resume_path is None,
)


def _run_loop(path: Path, payload: dict) -> None:
    pending = pending_work(payload)
    total = len(payload["results"]) + len(pending)
    done_at_start = len(payload["results"])
    classification = classification_from_json(payload["classification"])
    plan = load_fiches_by_ids(collect_action_ids(classification))
    nom = payload["meta"]["collectivite_nom"]
    population = int(payload["meta"]["population"])
    debug = bool(payload["meta"].get("debug"))
    low = payload["meta"].get("reasoning") == "low"
    flex = payload_is_flex(payload)
    cache_key = str(
        payload["meta"].get("prompt_cache_key")
        or f"test-run-impact:{payload['meta']['collectivite_id']}"
    )

    progress = st.progress(done_at_start / total if total else 1.0)
    with st.status("Exécution en cours…", expanded=True) as status:
        try:
            for idx, (run, levier) in enumerate(pending, start=1):
                status.write(
                    f"Run {run}/{payload['meta']['n_runs']} — "
                    f"levier {idx}/{len(pending)} restants : {levier}"
                )
                actions_by_cat = classification[levier]
                if debug:
                    scores, usage = score_one_lever_mock(actions_by_cat)
                else:
                    scores, usage = score_one_lever(
                        client=client,
                        plan=plan,
                        levier=levier,
                        actions_by_cat=actions_by_cat,
                        collectivite_nom=nom,
                        population=population,
                        status_container=status,
                        reasoning_low=low,
                        prompt_cache_key=cache_key,
                        use_flex=flex,
                    )
                append_result(payload, run, levier, scores, usage)
                save_payload(path, payload)
                call_cost = usage_cost_usd(usage, flex)
                status.write(
                    format_usage_cost_line(
                        usage,
                        call_cost=call_cost,
                        total_cost=payload_cost_usd(payload),
                    )
                )
                progress.progress((done_at_start + idx) / total if total else 1.0)
                pause_between_calls(debug)

            payload["meta"]["status"] = "complete"
            payload["meta"]["last_error"] = None
            save_payload(path, payload)
            status.update(label="Exécution terminée", state="complete")
        except Exception as e:
            payload["meta"]["status"] = "running"
            payload["meta"]["last_error"] = f"{type(e).__name__}: {e}"
            save_payload(path, payload)
            status.update(label="Erreur — JSON conservé, vous pouvez reprendre", state="error")
            st.error(f"Erreur pendant le run : {e}")
            st.caption(f"Fichier : `{path}`")
            return

    st.success(f"Résultats enregistrés dans `{path}`")


active_path: Path | None = None

if launch:
    path = new_run_path(int(collectivite_id))
    payload = init_payload(
        inputs,
        n_runs=int(n_runs),
        reasoning_low=reasoning_low,
        debug=debug_mode,
        use_flex=use_flex,
    )
    save_payload(path, payload)
    st.session_state[SESSION_LAST_FILE] = str(path)
    _run_loop(path, payload)
    active_path = path
elif resume and resume_path is not None:
    payload = load_payload(resume_path)
    st.session_state[SESSION_LAST_FILE] = str(resume_path)
    _run_loop(resume_path, payload)
    active_path = resume_path

st.markdown("---")
st.subheader("Stats depuis un JSON")

all_files = list_run_files()
if not all_files:
    st.info("Aucun fichier de run pour l'instant. Lancez un test pour en créer un.")
    st.stop()

default_file = None
last = st.session_state.get(SESSION_LAST_FILE)
if active_path is not None:
    default_file = active_path
elif last:
    last_path = Path(last)
    if last_path in all_files:
        default_file = last_path

default_index = all_files.index(default_file) if default_file in all_files else 0

selected_file = st.selectbox(
    "Fichier",
    options=all_files,
    index=default_index,
    format_func=file_label,
    key="test_run_impact_json",
)

payload = load_payload(selected_file)
accord_cutoff = st.slider(
    "Seuil d'accord majoritaire",
    min_value=0,
    max_value=100,
    value=80,
    step=1,
    format="%d %%",
    help=(
        "Si l'accord majoritaire d'un volet est supérieur ou égal à ce seuil, "
        "il n'est pas considéré comme instable."
    ),
    key="test_run_impact_accord_cutoff",
)
st.caption(
    f"Un volet n'est instable que si l'accord majoritaire est **strictement "
    f"inférieur à {int(accord_cutoff)} %**."
)
stats = compute_stats(payload, accord_cutoff=float(accord_cutoff))
meta = payload.get("meta", {})
tokens = payload_token_totals(payload)
cost_total = payload_cost_usd(payload)
flex_run = payload_is_flex(payload)
hit_pct = cache_hit_pct(tokens)
uncached = uncached_input_tokens(tokens)

if stats["incomplete"]:
    st.warning(
        f"Run incomplet : {stats['n_pending']} appels restants "
        f"(statut JSON : {meta.get('status')}). "
        "Les stats portent sur les résultats déjà sauvegardés."
    )
if meta.get("last_error"):
    st.error(f"Dernière erreur enregistrée : {meta['last_error']}")

st.caption(
    f"Modèle {meta.get('model')} — reasoning {meta.get('reasoning')} — "
    f"{meta.get('service_tier', 'standard')} — "
    f"{'debug' if meta.get('debug') else 'API'} — "
    f"démarré {meta.get('started_at')} — mis à jour {meta.get('updated_at')} — "
    f"{format_usage_cost_line(tokens, total_cost=cost_total)}"
)

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Volets (avec actions)", stats["n_volets"])
c2.metric("Volets instables", stats["n_unstable"])
c3.metric(
    "Part instable",
    f"{stats['pct_unstable']:.0f} %" if stats["pct_unstable"] is not None else "—",
)
c4.metric(
    "Plus grande étendue",
    stats["max_range"] if stats["max_range"] is not None else "—",
)
c5.metric("Coût total", format_usd(cost_total))

cost1, cost2, cost3, cost4 = st.columns(4)
cost1.metric(
    "Tokens entrée / sortie",
    f"{tokens['input_tokens']:,} / {tokens['output_tokens']:,}",
)
cost2.metric(
    "Cached / write / uncached",
    (
        f"{int(tokens.get('cached_tokens', 0)):,} / "
        f"{int(tokens.get('cache_write_tokens', 0)):,} / "
        f"{uncached:,}"
    ),
)
cost3.metric(
    "Hit cache",
    f"{hit_pct:.0f} %" if hit_pct is not None else "—",
)
cost4.metric(
    "Tarif",
    "Flex (−50 %)" if flex_run else "Standard",
)

v1, v2, v3, v4 = st.columns(4)
v1.metric(
    "Variance moyenne (volets)",
    f"{stats['mean_variance_global']:.3f}"
    if stats["mean_variance_global"] is not None
    else "—",
)
v2.metric(
    "Variance moyenne (leviers)",
    f"{stats['mean_variance_per_levier']:.3f}"
    if stats["mean_variance_per_levier"] is not None
    else "—",
)
v3.metric(
    "Écart-type moyen",
    f"{stats['mean_stdev_global']:.3f}"
    if stats["mean_stdev_global"] is not None
    else "—",
)
v4.metric(
    "Stables (identique à chaque run)",
    f"{stats.get('n_stable', 0)} / {stats.get('n_usable', 0)}",
)

if stats["max_range_row"]:
    row = stats["max_range_row"]
    st.markdown(
        f"**Plus grande différence :** {row['levier']} × {row['categorie_libelle']} "
        f"— étendue {row['etendue']} (min {row['min']} / max {row['max']}) "
        f"— scores : `{row['scores_str']}`"
    )

if stats.get("n_usable", 0) == 0 and stats["n_volets"] > 0:
    st.info("Au moins 2 notes par volet sont nécessaires pour calculer une variance.")

st.markdown(
    f"##### Volets instables (accord inférieur à {int(accord_cutoff)} %)"
)
df_unstable = stats["df_unstable"]
if df_unstable is None or df_unstable.empty:
    st.success(
        f"Aucun volet instable (accord inférieur à {int(accord_cutoff)} %) "
        "parmi ceux qui ont au moins 2 notes."
    )
else:
    st.dataframe(
        df_unstable.rename(
            columns={
                "levier": "Levier",
                "categorie_libelle": "Catégorie",
                "nb_actions": "Nb actions",
                "nb_runs": "Nb runs",
                "scores_str": "Scores",
                "effectifs": "Effectifs",
                "mode": "Mode",
                "n_distinct": "Valeurs distinctes",
                "min": "Min",
                "max": "Max",
                "etendue": "Étendue",
                "moyenne": "Moyenne",
                "variance": "Variance",
                "stdev": "Écart-type",
                "accord_pct": "Accord majoritaire (%)",
                "note_olap": "Note OLAP",
            }
        )[
            [
                "Levier",
                "Catégorie",
                "Nb actions",
                "Nb runs",
                "Scores",
                "Effectifs",
                "Mode",
                "Valeurs distinctes",
                "Min",
                "Max",
                "Étendue",
                "Moyenne",
                "Variance",
                "Écart-type",
                "Accord majoritaire (%)",
                "Note OLAP",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )

st.markdown("##### Variance moyenne par levier")
df_leviers = stats["df_leviers"]
if df_leviers is not None and not df_leviers.empty:
    st.dataframe(
        df_leviers.rename(
            columns={
                "levier": "Levier",
                "nb_volets": "Nb volets",
                "nb_instables": "Nb instables",
                "variance_moyenne": "Variance moyenne",
                "stdev_moyen": "Écart-type moyen",
                "etendue_max": "Étendue max",
                "accord_moyen_pct": "Accord moyen (%)",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

st.markdown("##### Étendue par levier × catégorie")
df_heatmap = stats["df_heatmap"]
if df_heatmap is not None and not df_heatmap.empty:
    st.dataframe(df_heatmap, use_container_width=True)

st.markdown("##### Comparaison à la note OLAP (mode des runs vs note stockée)")
c_olap1, c_olap2 = st.columns(2)
c_olap1.metric(
    "Mode = note OLAP",
    f"{stats['olap_match_rate']:.0f} %"
    if stats["olap_match_rate"] is not None
    else "—",
)
c_olap2.metric(
    "Écart moyen |mode − OLAP|",
    f"{stats['olap_mean_abs_diff']:.2f}"
    if stats["olap_mean_abs_diff"] is not None
    else "—",
)

with st.expander("Tous les volets (y compris stables)"):
    df_volets = stats["df_volets"]
    if df_volets is not None and not df_volets.empty:
        st.dataframe(
            df_volets.rename(
                columns={
                    "levier": "Levier",
                    "categorie_libelle": "Catégorie",
                    "nb_actions": "Nb actions",
                    "nb_runs": "Nb runs",
                    "scores_str": "Scores",
                    "effectifs": "Effectifs",
                    "mode": "Mode",
                    "n_distinct": "Valeurs distinctes",
                    "min": "Min",
                    "max": "Max",
                    "etendue": "Étendue",
                    "moyenne": "Moyenne",
                    "variance": "Variance",
                    "stdev": "Écart-type",
                    "accord_pct": "Accord majoritaire (%)",
                    "note_olap": "Note OLAP",
                    "mode_eq_olap": "Mode = OLAP",
                }
            )[
                [
                    "Levier",
                    "Catégorie",
                    "Nb actions",
                    "Nb runs",
                    "Scores",
                    "Effectifs",
                    "Mode",
                    "Valeurs distinctes",
                    "Min",
                    "Max",
                    "Étendue",
                    "Moyenne",
                    "Variance",
                    "Écart-type",
                    "Accord majoritaire (%)",
                    "Note OLAP",
                    "Mode = OLAP",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )
