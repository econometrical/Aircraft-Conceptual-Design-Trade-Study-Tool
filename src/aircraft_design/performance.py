from dataclasses import dataclass
from math import log


@dataclass(frozen=True)
class MissionPerformance:
    fuel_fraction: float
    final_mass_kg: float
    range_m: float
    endurance_s: float


def evaluate_jet_cruise_performance(
    *,
    initial_mass_kg: float,
    fuel_mass_kg: float,
    speed_m_s: float,
    lift_to_drag_ratio: float,
    tsfc_per_s: float,
) -> MissionPerformance:
    """
    Estimate cruise range with a simplified Breguet jet relation.

    Range = V / c * (L/D) * ln(W_initial / W_final)

    Because weight is proportional to mass under constant gravity,
    the mass ratio can be used in the logarithm.
    """
    if min(
        initial_mass_kg,
        fuel_mass_kg,
        speed_m_s,
        lift_to_drag_ratio,
        tsfc_per_s,
    ) <= 0:
        raise ValueError("Mission-performance inputs must be positive.")

    final_mass_kg = initial_mass_kg - fuel_mass_kg
    if final_mass_kg <= 0:
        raise ValueError("Fuel mass must be lower than initial mass.")

    mass_ratio_log = log(initial_mass_kg / final_mass_kg)
    range_m = (
        speed_m_s
        / tsfc_per_s
        * lift_to_drag_ratio
        * mass_ratio_log
    )
    endurance_s = (
        1.0
        / tsfc_per_s
        * lift_to_drag_ratio
        * mass_ratio_log
    )

    return MissionPerformance(
        fuel_fraction=fuel_mass_kg / initial_mass_kg,
        final_mass_kg=final_mass_kg,
        range_m=range_m,
        endurance_s=endurance_s,
    )
