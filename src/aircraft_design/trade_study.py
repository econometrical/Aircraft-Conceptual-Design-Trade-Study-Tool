from dataclasses import fields, replace
from typing import Iterable

import pandas as pd

from .analysis import analyze_aircraft
from .models import AircraftInputs


def run_trade_study(
    *,
    baseline: AircraftInputs,
    variable: str,
    values: Iterable[float],
) -> pd.DataFrame:
    """
    Sweep one AircraftInputs field while holding other inputs constant.
    """
    allowed = {field.name for field in fields(AircraftInputs)}
    if variable not in allowed:
        raise ValueError(
            f"Unknown design variable '{variable}'. "
            f"Choose one of: {sorted(allowed)}"
        )

    rows: list[dict[str, float]] = []

    for value in values:
        candidate = replace(baseline, **{variable: float(value)})
        result = analyze_aircraft(candidate)
        row = {variable: float(value), **result.to_dict()}
        row["drag_kn"] = row["drag_n"] / 1000.0
        rows.append(row)

    if not rows:
        raise ValueError("Trade study requires at least one value.")

    return pd.DataFrame(rows)
