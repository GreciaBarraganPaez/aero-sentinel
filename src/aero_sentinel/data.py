"""Read and validate NASA C-MAPSS train, test, and RUL files."""
from pathlib import Path
import pandas as pd

COLUMNS = (
    ["engine_id", "cycle"]
    + [f"setting_{i}" for i in range(1, 4)]
    + [f"sensor_{i}" for i in range(1, 22)]
)


class DataValidationError(ValueError):
    """Raised when a C-MAPSS file has an invalid structure."""


def load_sensor_file(path: str | Path) -> pd.DataFrame:
    """Load whitespace-separated C-MAPSS measurements (26 numeric columns)."""
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"Dataset not found: {path}")
    try:
        frame = pd.read_csv(path, sep=r"\s+", header=None)
    except pd.errors.EmptyDataError as exc:
        raise DataValidationError(f"Empty sensor file: {path}") from exc
    if frame.shape[1] != len(COLUMNS):
        raise DataValidationError(
            f"Expected 26 columns in {path.name}; found {frame.shape[1]}"
        )
    frame.columns = COLUMNS
    for column in COLUMNS:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    if frame.isna().any().any():
        raise DataValidationError(f"Missing or nonnumeric values in {path.name}")
    for col in ("engine_id", "cycle"):
        if not (frame[col] > 0).all() or not (frame[col] % 1 == 0).all():
            raise DataValidationError(f"{col} must contain positive integers")
        frame[col] = frame[col].astype("int64")
    if frame.duplicated(["engine_id", "cycle"]).any():
        raise DataValidationError("Duplicate (engine_id, cycle) rows found")
    for _, group in frame.groupby("engine_id", sort=False):
        if not group["cycle"].is_monotonic_increasing:
            raise DataValidationError("Cycles are not ordered within an engine")
    return frame


def load_rul_file(path: str | Path, expected_engines: int | None = None) -> pd.Series:
    """Load test RUL values, one per test engine in engine-ID order."""
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"RUL file not found: {path}")
    try:
        frame = pd.read_csv(path, sep=r"\s+", header=None)
    except pd.errors.EmptyDataError as exc:
        raise DataValidationError(f"Empty RUL file: {path}") from exc
    if frame.shape[1] != 1:
        raise DataValidationError(f"Expected one RUL column; found {frame.shape[1]}")
    values = pd.to_numeric(frame.iloc[:, 0], errors="coerce")
    if values.isna().any() or (values < 0).any() or not (values % 1 == 0).all():
        raise DataValidationError("RUL values must be nonnegative integers")
    if expected_engines is not None and len(values) != expected_engines:
        raise DataValidationError(
            f"RUL entries ({len(values)}) != test engine count ({expected_engines})"
        )
    return values.astype("int64").rename("rul_at_last_observed_cycle")


def describe_dataset(frame: pd.DataFrame) -> dict:
    """Produce JSON-compatible statistics for a validated sensor dataframe."""
    lengths = frame.groupby("engine_id")["cycle"].size()
    sensors = [f"sensor_{i}" for i in range(1, 22)]
    return {
        "rows": int(len(frame)),
        "columns": int(frame.shape[1]),
        "engines": int(frame["engine_id"].nunique()),
        "cycle_min": int(frame["cycle"].min()),
        "cycle_max": int(frame["cycle"].max()),
        "engine_sequence_length_min": int(lengths.min()),
        "engine_sequence_length_median": float(lengths.median()),
        "engine_sequence_length_max": int(lengths.max()),
        "missing_values": int(frame.isna().sum().sum()),
        "duplicate_engine_cycles": int(frame.duplicated(["engine_id", "cycle"]).sum()),
        "constant_sensors": [
            sensor for sensor in sensors if frame[sensor].nunique(dropna=False) <= 1
        ],
        "sensor_count": len(sensors),
    }
