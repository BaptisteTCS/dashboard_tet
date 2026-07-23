"""Tests de non-régression du calcul des volets hors compétence.

Ces tests ne touchent pas la base de données : ils s'appuient uniquement sur
les référentiels CSV de data/priorisation_competence/. Exécutable avec pytest
ou directement : `python tests/test_priorisation_competence.py`.
"""

import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils import priorisation_competence as pc


def test_empty_baseline_retenus():
    """Une collectivité sans compétence retient un nombre constant de volets."""
    assert pc.count_empty_baseline_retenus() == pc.EMPTY_BASELINE_RETENUS


def test_structural_closures_count():
    """Les règles A et B ferment exactement 20 volets universellement."""
    assert pc.count_structural_closures() == pc.STRUCTURAL_CLOSURES_COUNT


def test_regle_a_perimetre():
    """La règle A ne contient plus que les cinq leviers agricoles/industriels."""
    attendus = {
        "Elevage durable",
        "Changements de pratiques de fertilisation azotée",
        "Bâtiments & Machines agricoles",
        "Gestion des prairies",
        "Production Industrielle",
    }
    presents = {
        unicodedata.normalize("NFC", levier)
        for levier in pc.load_exceptions_a()
    }
    assert presents == {unicodedata.normalize("NFC", x) for x in attendus}


def test_leviers_sortis_de_a_restent_exclus():
    """Captage, Efficacité logistique et Fret quittent A mais restent `exclu`."""
    exceptions_a = pc.load_exceptions_a()
    regles = pc.load_exemplarite_regles()
    for levier in (
        "Captage de méthane dans les ISDND",
        "Efficacité et sobriété logistique",
        "Fret décarboné et multimodalité",
    ):
        assert levier not in exceptions_a
        assert regles.get(levier) == "exclu"


if __name__ == "__main__":
    test_empty_baseline_retenus()
    test_structural_closures_count()
    test_regle_a_perimetre()
    test_leviers_sortis_de_a_restent_exclus()
    print("OK - tous les tests de non-régression passent")
    print("  baseline vide retenus :", pc.count_empty_baseline_retenus())
    print("  volets fermés (A+B)   :", pc.count_structural_closures())
