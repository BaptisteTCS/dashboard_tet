import time

import streamlit as st

st.set_page_config(
    page_title="Retours utilisateurs",
    page_icon="💬",
    layout="wide",
)

from utils.retour_utilisateurs_db import (
    charger_backlog,
    charger_cycles,
    charger_lot,
    charger_validations,
    pipeline_pret,
    sauvegarder_validations,
    statistiques,
)

AUTRE_TICKET = "autre"
CREER_TICKET = "creer"
IGNORER = "ignorer"

demande_scroll = st.session_state.pop("ru_scroll_haut", None)
if demande_scroll:
    # Streamlit n'expose toujours pas de scroll : le nonce force le navigateur
    # à rejouer le script à chaque validation.
    st.html(
        f"""
        <script>
            const nonce = "{demande_scroll}";
            const cible = document.querySelector('[data-testid="stMain"]')
                || document.scrollingElement;
            setTimeout(() => cible.scrollTo({{top: 0, behavior: "smooth"}}), 100);
        </script>
        """,
        unsafe_allow_javascript=True,
    )

st.title("💬 Retours utilisateurs → tickets")
st.markdown(
    "Les rapprochements sont calculés chaque nuit. Le meilleur candidat est "
    "présélectionné : il suffit de corriger les erreurs puis de valider le lot."
)

if not pipeline_pret():
    st.warning(
        "Le pipeline nocturne n'a pas encore tourné : lancez "
        "`datalore/pipeline_retours_utilisateurs.py` sur Datalore."
    )
    st.stop()

ignores = st.session_state.setdefault("ru_ignores", set())

with st.sidebar:
    taille_lot = st.selectbox("Retours par lot", [5, 10, 20], index=0)
    if ignores:
        st.caption(f"{len(ignores)} retour(s) ignoré(s) sur cette session")
        if st.button("Réafficher les ignorés", width="stretch"):
            ignores.clear()
            st.rerun()

stats = statistiques()
# Les ignorés sont sautés côté page : on en charge assez pour remplir le lot.
lot = [
    item
    for item in charger_lot(taille_lot + len(ignores))
    if item["feedback_id"] not in ignores
][:taille_lot]

c1, c2, c3 = st.columns(3)
c1.metric("Retours sans tickets", stats["sans_epic"])
c2.metric("Déjà validés", stats["valides"])
c3.metric("À trancher", stats["a_traiter"])

if not lot:
    if ignores:
        st.info("Tous les retours restants ont été ignorés sur cette session.")
    else:
        st.success("Plus rien à trancher.")
    st.stop()

# ---------------------------------------------------------------------------
# Revue des retours
# ---------------------------------------------------------------------------

tous_tickets = charger_backlog()
cycles = charger_cycles()
cycle_ids = [cid for cid, _ in cycles]
noms_cycles = dict(cycles)

# Le backlog est déjà trié par (cycle, titre) : on garde cet ordre par cycle.
tickets_par_cycle = {}
titres_tickets = {}
for t in tous_tickets:
    titres_tickets[t["ticket_id"]] = t["ticket_titre"]
    ids = tickets_par_cycle.setdefault(t["cycle_id"], [])
    if t["ticket_id"] not in ids:
        ids.append(t["ticket_id"])


def nom_cycle(cid):
    return noms_cycles.get(cid) or cid


def index_cycle(liste, cid):
    return liste.index(cid) if cid in liste else 0


cycles_backlog = sorted(tickets_par_cycle, key=nom_cycle)

CLES_ETAT = (
    "ru_choix_",
    "ru_autre_cycle_",
    "ru_autre_ticket_",
    "ru_creer_cycle_",
    "ru_creer_titre_",
)


def oublier_etat(fid):
    """Une card qui disparaît ne doit pas laisser ses widgets en session."""
    for prefixe in CLES_ETAT:
        st.session_state.pop(f"{prefixe}{fid}", None)


def ligne_validation(item):
    """(ligne à insérer, message d'erreur) selon le choix fait pour ce retour."""
    fid = item["feedback_id"]
    candidats = item["tickets"]
    choix = st.session_state[f"ru_choix_{fid}"]

    if choix.startswith("t:"):
        ticket = next(t for t in candidats if t["id"] == choix[2:])
        return {
            "ticket_id": ticket["id"],
            "cycle_id": ticket["cycle_id"],
            "ticket_titre": ticket["titre"],
            "choix_ia": ticket["id"] == candidats[0]["id"],
            "score_ia": ticket["score"],
        }, None

    if choix == AUTRE_TICKET:
        ticket_id = st.session_state.get(f"ru_autre_ticket_{fid}")
        if not ticket_id:
            return None, "aucun ticket disponible dans le cycle choisi"
        return {
            "ticket_id": ticket_id,
            "cycle_id": st.session_state[f"ru_autre_cycle_{fid}"],
            "ticket_titre": titres_tickets[ticket_id],
            "choix_ia": False,
            "score_ia": None,
        }, None

    titre_neuf = (st.session_state[f"ru_creer_titre_{fid}"] or "").strip()
    if not titre_neuf:
        return None, "titre du ticket à créer manquant"
    return {
        "ticket_id": None,
        "cycle_id": st.session_state[f"ru_creer_cycle_{fid}"],
        "ticket_titre": titre_neuf,
        "choix_ia": False,
        "score_ia": None,
    }, None


@st.fragment
def carte_retour(item):
    """Fragment : changer un widget ici ne recharge pas le reste de la page."""
    fid = item["feedback_id"]
    candidats = item["tickets"]

    with st.container(border=True):
        gauche, droite = st.columns([5, 4])

        with gauche:
            st.markdown(f"**{item['titre'] or '(sans titre)'}**")
            citation = (item["citation"] or "").strip()
            if citation:
                # Les retours restent lisibles d'un coup d'œil : pas de troncature.
                st.markdown("\n".join(f"> {l}" for l in citation.splitlines()))
            if item["erreur"]:
                st.caption(f":red[Analyse en échec : {item['erreur']}]")
            if item["url"]:
                st.caption(f"[Ouvrir dans Notion]({item['url']})")

        with droite:
            options = [f"t:{t['id']}" for t in candidats] + [
                AUTRE_TICKET,
                CREER_TICKET,
                IGNORER,
            ]
            libelles = {
                f"t:{t['id']}": f"{t['titre']} — *{t['cycle_name']}*"
                for t in candidats
            }
            libelles[AUTRE_TICKET] = "Autre ticket"
            libelles[CREER_TICKET] = "Créer un ticket"
            libelles[IGNORER] = "Ignorer (pour l'instant)"

            choix = st.radio(
                "Ticket retenu",
                options,
                index=0,
                format_func=lambda o: libelles[o],
                key=f"ru_choix_{fid}",
            )

            with st.expander("Autre ticket", expanded=choix == AUTRE_TICKET):
                cycle_autre = st.selectbox(
                    "Cycle",
                    cycles_backlog,
                    index=index_cycle(cycles_backlog, item["cycle_id"]),
                    format_func=nom_cycle,
                    key=f"ru_autre_cycle_{fid}",
                )
                st.selectbox(
                    "Ticket du cycle",
                    tickets_par_cycle.get(cycle_autre, []),
                    format_func=lambda tid: titres_tickets[tid],
                    key=f"ru_autre_ticket_{fid}",
                )

            with st.expander("Créer un ticket", expanded=choix == CREER_TICKET):
                st.selectbox(
                    "Cycle",
                    cycle_ids,
                    index=index_cycle(cycle_ids, item["cycle_id"]),
                    format_func=nom_cycle,
                    key=f"ru_creer_cycle_{fid}",
                )
                st.text_area(
                    "Titre du ticket à créer",
                    value=item["titre"] or "",
                    key=f"ru_creer_titre_{fid}",
                )


st.divider()

for item in lot:
    carte_retour(item)

if st.button(
    f"Valider les {len(lot)} retours", type="primary", width="stretch"
):
    lignes, problemes, sautes = [], [], []
    for item in lot:
        fid = item["feedback_id"]
        if st.session_state[f"ru_choix_{fid}"] == IGNORER:
            sautes.append(fid)
            continue
        ligne, erreur = ligne_validation(item)
        if erreur:
            problemes.append(f"« {item['titre'] or '(sans titre)'} » : {erreur}")
        else:
            lignes.append(
                {"feedback_id": fid, "feedback_titre": item["titre"], **ligne}
            )

    if problemes:
        st.error("Rien n'a été enregistré :\n\n- " + "\n- ".join(problemes))
    else:
        sauvegarder_validations(lignes)
        ignores.update(sautes)
        for item in lot:
            oublier_etat(item["feedback_id"])
        a_creer = sum(1 for l in lignes if l["ticket_id"] is None)
        details = f" — {a_creer} ticket(s) à créer" if a_creer else ""
        details += f", {len(sautes)} ignoré(s)" if sautes else ""
        st.toast(f"{len(lignes)} retours enregistrés{details}", icon="✅")
        st.session_state["ru_scroll_haut"] = time.time()
        st.rerun()

with st.expander(f"Validations enregistrées ({stats['valides']})"):
    df_valides = charger_validations()
    if df_valides.empty:
        st.caption("Aucune validation pour l'instant.")
    else:
        st.dataframe(df_valides, hide_index=True, width="stretch")
