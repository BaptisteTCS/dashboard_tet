"""CLI : reclassifie des fiches via GPT et compare avec la prod (lecture seule).

Exemples :

    python scripts/verify_classification_volet_ges.py 5119 4999
    python scripts/verify_classification_volet_ges.py 5119 --batch-size 20
    python scripts/verify_classification_volet_ges.py 5119 --from-json 5119=data/.../5119_classification_gpt.json
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.verify_classification_volet_ges import (  # noqa: E402
    DEFAULT_MODEL,
    run_verification,
)


def parse_from_json(values: list[str] | None) -> dict[int, Path]:
    mapping: dict[int, Path] = {}
    for raw in values or []:
        if "=" not in raw:
            raise argparse.ArgumentTypeError(
                f"--from-json attend ID=CHEMIN, reçu {raw!r}"
            )
        cid_raw, path_raw = raw.split("=", 1)
        mapping[int(cid_raw)] = Path(path_raw)
    return mapping


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Reclassification GPT des fiches d'une ou plusieurs collectivités, "
            "comparée à fiche_action_volet_ges (prod, lecture seule)."
        )
    )
    parser.add_argument(
        "collectivite_ids",
        nargs="+",
        type=int,
        help="Identifiants de collectivités (ex. 5119 4999)",
    )
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Modèle OpenAI")
    parser.add_argument("--batch-size", type=int, default=25, help="Fiches par appel GPT")
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limiter le nombre de fiches par collectivité (smoke test)",
    )
    parser.add_argument(
        "--reasoning-low",
        action="store_true",
        help="Effort de raisonnement low (medium par défaut, comme 26_run_impact)",
    )
    parser.add_argument(
        "--skip-llm",
        action="store_true",
        help="Ne pas appeler GPT (rapport à partir de la prod uniquement)",
    )
    parser.add_argument(
        "--from-json",
        action="append",
        default=[],
        metavar="ID=CHEMIN",
        help="Reprendre une classification GPT déjà sauvée (répétable sans rappel API)",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Reprendre les JSON GPT déjà présents dans --output-dir (lots manquants seulement)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Dossier de sortie (défaut : data/verify_classification_volet_ges/<horodatage>)",
    )
    args = parser.parse_args()

    output_dir = run_verification(
        args.collectivite_ids,
        model=args.model,
        batch_size=args.batch_size,
        reasoning_low=args.reasoning_low,
        skip_llm=args.skip_llm,
        limit=args.limit,
        from_json=parse_from_json(args.from_json),
        resume=args.resume,
        output_dir=args.output_dir,
    )
    print(f"\nTerminé. Fichiers dans {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
