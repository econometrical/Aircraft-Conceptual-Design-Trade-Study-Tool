from dataclasses import replace

import pytest

from src.aircraft_design.analysis import analyze_aircraft
from src.aircraft_design.models import AircraftInputs
from src.aircraft_design.trade_study import run_trade_study


def test_baseline_analysis_outputs_are_positive() -> None:
    result = analyze_aircraft(AircraftInputs())

    assert result.cruise_speed_m_s > 0
    assert result.lift_coefficient > 0
    assert result.drag_coefficient > 0
    assert result.lift_to_drag_ratio > 0
    assert result.range_km > 0


def test_more_fuel_increases_breguet_range_when_other_inputs_are_fixed() -> None:
    baseline = AircraftInputs(fuel_mass_kg=7_000)
    high_fuel = replace(baseline, fuel_mass_kg=10_000)

    baseline_result = analyze_aircraft(baseline)
    high_fuel_result = analyze_aircraft(high_fuel)

    assert high_fuel_result.range_km > baseline_result.range_km


def test_higher_aspect_ratio_reduces_induced_drag_at_fixed_condition() -> None:
    low_ar = AircraftInputs(aspect_ratio=7.0)
    high_ar = replace(low_ar, aspect_ratio=11.0)

    low_result = analyze_aircraft(low_ar)
    high_result = analyze_aircraft(high_ar)

    assert (
        high_result.induced_drag_coefficient
        < low_result.induced_drag_coefficient
    )


def test_trade_study_returns_one_row_per_value() -> None:
    values = [90, 100, 110]
    study = run_trade_study(
        baseline=AircraftInputs(),
        variable="wing_area_m2",
        values=values,
    )

    assert len(study) == len(values)
    assert study["wing_area_m2"].tolist() == values


def test_invalid_fuel_mass_is_rejected() -> None:
    with pytest.raises(ValueError):
        analyze_aircraft(
            AircraftInputs(
                takeoff_mass_kg=20_000,
                fuel_mass_kg=20_000,
            )
        )
