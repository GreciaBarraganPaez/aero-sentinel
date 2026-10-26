"""Compare data quality across the four NASA C-MAPSS subsets."""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from .data import describe_dataset, load_rul_file, load_sensor_file


def summarize(data_dir: Path, output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    summaries = {}
    rows = []
    for subset in ("FD001", "FD002", "FD003", "FD004"):
        train = load_sensor_file(data_dir / f"train_{subset}.txt")
        test = load_sensor_file(data_dir / f"test_{subset}.txt")
        rul = load_rul_file(
            data_dir / f"RUL_{subset}.txt",
            expected_engines=test["engine_id"].nunique(),
        )
        train_stats = describe_dataset(train)
        test_stats = describe_dataset(test)

        def count_noncontiguous(frame: pd.DataFrame) -> int:
            return sum(
                not np.array_equal(
                    group["cycle"].to_numpy(),
                    np.arange(1, len(group) + 1),
                )
                for _, group in frame.groupby("engine_id")
            )

        summaries[subset] = {
            "train": train_stats,
            "test": test_stats,
            "test_rul": {
                "count": int(len(rul)),
                "min": int(rul.min()),
                "median": float(rul.median()),
                "max": int(rul.max()),
            },
            "noncontiguous_train_engines": count_noncontiguous(train),
            "noncontiguous_test_engines": count_noncontiguous(test),
            "nonconstant_train_sensors": 21 - len(train_stats["constant_sensors"]),
        }
        rows.append({
            "subset": subset,
            "train_rows": train_stats["rows"],
            "train_engines": train_stats["engines"],
            "test_rows": test_stats["rows"],
            "test_engines": test_stats["engines"],
            "missing_train": train_stats["missing_values"],
            "missing_test": test_stats["missing_values"],
            "constant_sensors": len(train_stats["constant_sensors"]),
            "nonconstant_sensors": summaries[subset]["nonconstant_train_sensors"],
            "median_train_cycles": train_stats["engine_sequence_length_median"],
            "median_test_rul": float(rul.median()),
        })
    report = {
        "dataset": "NASA C-MAPSS",
        "subsets": summaries,
        "notes": [
            "Different subsets have different operating conditions and fault modes.",
            "Test RUL is provided at each test engine's last observed cycle.",
            "Ground-truth physical degradation onset is not labeled.",
            "These results are descriptive, not model evaluations.",
        ],
    }
    (output_dir / "cmapss_all_subsets_quality.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    pd.DataFrame(rows).to_csv(
        output_dir / "cmapss_subset_comparison.csv", index=False
    )
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare C-MAPSS subsets")
    parser.add_argument("--data-dir", type=Path, default=Path("data/raw"))
    parser.add_argument("--output-dir", type=Path, default=Path("results/figures"))
    args = parser.parse_args()
    report = summarize(args.data_dir, args.output_dir)
    for subset, stats in report["subsets"].items():
        print(
            f"{subset}: {stats['train']['rows']:,} training records, "
            f"{stats['train']['engines']} training engines, "
            f"{stats['nonconstant_train_sensors']} varying sensors"
        )


if __name__ == "__main__":
    main()
