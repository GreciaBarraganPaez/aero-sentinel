"""RUL baseline unit tests using synthetic engine trajectories."""
import pandas as pd
from aero_sentinel.rul_baseline import add_train_rul, holdout_snapshots, scores


def test_rul_targets_are_engine_specific_and_capped():
    frame = pd.DataFrame({
        "engine_id": [1, 1, 1, 2, 2],
        "cycle": [1, 2, 3, 1, 2],
    })
    result = add_train_rul(frame)
    assert result.rul_true.tolist() == [2, 1, 0, 1, 0]
    assert result.rul_target.tolist() == [2, 1, 0, 1, 0]


def test_holdout_snapshots_exclude_failure_cycle():
    frame = pd.DataFrame({
        "engine_id": [1] * 10 + [2] * 10,
        "cycle": list(range(1, 11)) * 2,
    })
    frame = add_train_rul(frame)
    result = holdout_snapshots(frame)
    assert result.engine_id.nunique() == 2
    assert result.cycle.max() < 10
    assert (result.rul_true > 0).all()


def test_scores():
    report = scores([10, 20], [12, 18])
    assert report["mae_cycles"] == 2
    assert report["rmse_cycles"] == 2
    assert report["observations"] == 2
