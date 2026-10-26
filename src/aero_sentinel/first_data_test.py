"""Generate a data-quality report and sensor plots for C-MAPSS FD001."""
import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from .data import describe_dataset, load_rul_file, load_sensor_file


def run(data_dir: Path, output_dir: Path) -> dict:
    train = load_sensor_file(data_dir / "train_FD001.txt")
    test = load_sensor_file(data_dir / "test_FD001.txt")
    rul = load_rul_file(
        data_dir / "RUL_FD001.txt", expected_engines=test["engine_id"].nunique()
    )
    report = {
        "dataset": "NASA C-MAPSS FD001",
        "train": describe_dataset(train),
        "test": describe_dataset(test),
        "test_rul": {
            "entries": int(len(rul)),
            "min": int(rul.min()),
            "median": float(rul.median()),
            "max": int(rul.max()),
        },
        "limitations": [
            "Physical degradation onset is not labeled.",
            "Descriptive analysis is not evidence of predictive model performance.",
        ],
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "fd001_quality_report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    engine_id = int(train["engine_id"].iloc[0])
    engine = train.loc[train["engine_id"] == engine_id]
    fig, ax = plt.subplots(figsize=(9, 4.5))
    for name in ("sensor_2", "sensor_3", "sensor_4"):
        values = engine[name]
        sigma = float(values.std())
        if sigma > 0:
            ax.plot(engine["cycle"], (values - values.mean()) / sigma, label=name)
    ax.set(
        xlabel="Cycle",
        ylabel="Within-engine standardized sensor value",
        title=f"FD001 engine {engine_id}: relative sensor changes",
    )
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_dir / "fd001_engine_sensor_trends.png", dpi=150)
    plt.close(fig)

    fig, axes = plt.subplots(3, 1, figsize=(9, 8), sharex=True)
    for ax, sensor in zip(axes, ("sensor_2", "sensor_11", "sensor_15")):
        for eid in sorted(train["engine_id"].unique())[:5]:
            subset = train.loc[train["engine_id"] == eid]
            ax.plot(
                subset["cycle"] / subset["cycle"].max(),
                subset[sensor],
                label=f"Engine {eid}",
                alpha=0.8,
            )
        ax.set_ylabel(sensor)
        ax.grid(alpha=0.2)
    axes[0].legend(ncol=5, fontsize=8)
    axes[-1].set_xlabel("Fraction of engine lifetime (1 = simulated failure)")
    fig.suptitle("FD001: selected sensor trajectories")
    fig.tight_layout()
    fig.savefig(output_dir / "fd001_engine_lifetime_trends.png", dpi=150)
    plt.close(fig)
    print(json.dumps(report, indent=2))
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze NASA C-MAPSS FD001")
    parser.add_argument("--data-dir", type=Path, default=Path("data/raw"))
    parser.add_argument("--output-dir", type=Path, default=Path("results/figures"))
    args = parser.parse_args()
    run(args.data_dir, args.output_dir)


if __name__ == "__main__":
    main()
