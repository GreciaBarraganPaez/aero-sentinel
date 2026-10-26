"""Leakage-aware FD001 RUL baseline using NASA C-MAPSS.

Holdout evaluation uses simulated partial trajectories from unseen engines,
not the final failure cycle (which would trivially have RUL=0).
"""
import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import GroupShuffleSplit

from .data import load_rul_file, load_sensor_file

RUL_CAP = 125
SEED = 42


def add_train_rul(frame: pd.DataFrame) -> pd.DataFrame:
    """Use complete run-to-failure trajectories to compute known RUL targets."""
    frame = frame.copy()
    end_cycle = frame.groupby("engine_id")["cycle"].transform("max")
    frame["rul_true"] = end_cycle - frame["cycle"]
    frame["rul_target"] = frame["rul_true"].clip(upper=RUL_CAP)
    return frame


def feature_columns(frame: pd.DataFrame) -> list[str]:
    """Exclude constant sensors based on the training partition only."""
    columns = ["cycle"] + [f"setting_{i}" for i in range(1, 4)]
    columns += [
        f"sensor_{i}" for i in range(1, 22)
        if frame[f"sensor_{i}"].nunique() > 1
    ]
    return columns


def holdout_snapshots(frame: pd.DataFrame) -> pd.DataFrame:
    """Choose fixed observation cutoffs from each held-out engine."""
    snapshots = []
    for _, engine in frame.groupby("engine_id", sort=True):
        engine = engine.sort_values("cycle")
        # Use partial trajectories only; do not use the failure cycle.
        positions = sorted(set(
            max(0, min(len(engine) - 2, int(len(engine) * p) - 1))
            for p in (0.50, 0.70, 0.90)
        ))
        snapshots.append(engine.iloc[positions])
    return pd.concat(snapshots, ignore_index=True)


def scores(y_true, y_pred) -> dict:
    return {
        "mae_cycles": float(mean_absolute_error(y_true, y_pred)),
        "rmse_cycles": float(np.sqrt(mean_squared_error(y_true, y_pred))),
        "observations": int(len(y_true)),
    }


def build_model() -> RandomForestRegressor:
    return RandomForestRegressor(
        n_estimators=150,
        min_samples_leaf=3,
        max_features=0.8,
        random_state=SEED,
        n_jobs=-1,
    )


def run(data_dir: Path, output_dir: Path) -> dict:
    train = add_train_rul(load_sensor_file(data_dir / "train_FD001.txt"))
    test = load_sensor_file(data_dir / "test_FD001.txt")
    test_rul = load_rul_file(
        data_dir / "RUL_FD001.txt",
        expected_engines=test.engine_id.nunique(),
    )
    splitter = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=SEED)
    tr_idx, val_idx = next(splitter.split(train, groups=train.engine_id))
    training, heldout = train.iloc[tr_idx], train.iloc[val_idx]
    assert set(training.engine_id).isdisjoint(set(heldout.engine_id))
    columns = feature_columns(training)
    model = build_model()
    model.fit(training[columns], training.rul_target)

    validation = holdout_snapshots(heldout)
    val_pred = model.predict(validation[columns])
    constant_pred = np.full(len(validation), float(training.rul_target.median()))

    # Official test data are used only after internal validation.
    final_model = build_model()
    final_columns = feature_columns(train)
    final_model.fit(train[final_columns], train.rul_target)
    test_last = (
        test.sort_values(["engine_id", "cycle"])
        .groupby("engine_id", sort=True).tail(1)
        .sort_values("engine_id").reset_index(drop=True)
    )
    if test_last.engine_id.tolist() != list(range(1, len(test_rul) + 1)):
        raise ValueError("Test engine IDs do not align with NASA RUL row order")
    test_pred = final_model.predict(test_last[final_columns])
    test_constant = np.full(len(test_rul), float(train.rul_target.median()))

    report = {
        "dataset": "FD001",
        "model": "RandomForestRegressor",
        "rul_training_cap": RUL_CAP,
        "random_seed": SEED,
        "train_engine_count": int(training.engine_id.nunique()),
        "validation_engine_count": int(heldout.engine_id.nunique()),
        "engine_overlap": 0,
        "validation_protocol": (
            "Three fixed partial-life snapshots per unseen engine "
            "at ~50%, 70%, 90% lifetime"
        ),
        "features": final_columns,
        "internal_validation": {
            "random_forest": scores(validation.rul_true, val_pred),
            "constant_median_baseline": scores(validation.rul_true, constant_pred),
        },
        "official_test_last_observation": {
            "random_forest": scores(test_rul, test_pred),
            "constant_median_baseline": scores(test_rul, test_constant),
        },
        "cautions": [
            "Training targets are capped at 125 cycles; metrics use uncapped true RUL.",
            "Validation uses hindsight to select trajectory fractions; fractions are not model features.",
            "Official test is a final benchmark, not a hyperparameter-tuning set.",
            "RUL prediction is not ground-truth physical degradation-onset detection.",
        ],
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "fd001_rul_baseline_metrics.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    pd.DataFrame({
        "engine_id": test_last.engine_id,
        "actual_rul": test_rul.to_numpy(),
        "predicted_rul": test_pred,
    }).to_csv(output_dir / "fd001_rul_test_predictions.csv", index=False)
    fig, ax = plt.subplots(figsize=(7, 6))
    limit = max(test_rul.max(), test_pred.max())
    ax.scatter(test_rul, test_pred, alpha=0.65, s=25)
    ax.plot([0, limit], [0, limit], "--", color="gray")
    ax.set(
        xlabel="Actual RUL (cycles)",
        ylabel="Predicted RUL (cycles)",
        title="FD001: Random Forest baseline on official test engines",
    )
    fig.tight_layout()
    fig.savefig(output_dir / "fd001_rul_predictions.png", dpi=160)
    plt.close(fig)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Run FD001 Random Forest RUL baseline")
    parser.add_argument("--data-dir", type=Path, default=Path("data/raw"))
    parser.add_argument("--output-dir", type=Path, default=Path("results/figures"))
    args = parser.parse_args()
    print(json.dumps(run(args.data_dir, args.output_dir), indent=2))


if __name__ == "__main__":
    main()
