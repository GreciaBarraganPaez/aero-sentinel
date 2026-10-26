"""Unit tests with synthetic C-MAPSS-shaped rows (not NASA measurements)."""
from pathlib import Path

import pandas as pd
import pytest

from aero_sentinel.data import (
    COLUMNS, DataValidationError, describe_dataset, load_rul_file, load_sensor_file
)


def write_rows(tmp_path: Path, rows: list[list]) -> Path:
    path = tmp_path / "measurements.txt"
    path.write_text(
        "\n".join(" ".join(str(value) for value in row) for row in rows),
        encoding="utf-8",
    )
    return path


def sample_rows() -> list[list]:
    return [
        [1, 1, *([0.0] * 24)],
        [1, 2, *([1.0] * 24)],
        [2, 1, *([2.0] * 24)],
    ]


def test_schema_and_engine_counts(tmp_path):
    frame = load_sensor_file(write_rows(tmp_path, sample_rows()))
    assert list(frame.columns) == COLUMNS
    assert describe_dataset(frame)["engines"] == 2
    assert describe_dataset(frame)["rows"] == 3


def test_wrong_column_count(tmp_path):
    with pytest.raises(DataValidationError, match="26 columns"):
        load_sensor_file(write_rows(tmp_path, [[1, 1, 0]]))


def test_duplicate_engine_cycle(tmp_path):
    rows = sample_rows()
    with pytest.raises(DataValidationError, match="Duplicate"):
        load_sensor_file(write_rows(tmp_path, rows + [rows[0]]))


def test_non_numeric_values(tmp_path):
    rows = sample_rows()
    rows[0][4] = "invalid"
    with pytest.raises(DataValidationError, match="nonnumeric"):
        load_sensor_file(write_rows(tmp_path, rows))


def test_invalid_engine_id(tmp_path):
    rows = sample_rows()
    rows[0][0] = -1
    with pytest.raises(DataValidationError, match="engine_id"):
        load_sensor_file(write_rows(tmp_path, rows))


def test_rul_count_and_values(tmp_path):
    path = tmp_path / "RUL.txt"
    path.write_text("15\n20\n", encoding="utf-8")
    assert load_rul_file(path, expected_engines=2).tolist() == [15, 20]
    with pytest.raises(DataValidationError, match="engine count"):
        load_rul_file(path, expected_engines=3)


def test_constant_sensor_detection(tmp_path):
    rows = sample_rows()
    for row in rows:
        row[5] = 100.0  # sensor_1 is column index 5
    frame = load_sensor_file(write_rows(tmp_path, rows))
    assert "sensor_1" in describe_dataset(frame)["constant_sensors"]
