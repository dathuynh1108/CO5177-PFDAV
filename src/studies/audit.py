"""Recompute Tabular/Text scores and optionally verify saved local classifiers."""

import argparse
import json

from studies.evidence import audit

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--models", action="store_true", help="Require private local model artifacts"
    )
    options = parser.parse_args()
    print(
        json.dumps(
            [
                audit(track, check_models=options.models)
                for track in ["tabular", "text"]
            ],
            indent=2,
        )
    )
