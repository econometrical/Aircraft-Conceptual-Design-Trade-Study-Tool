from dataclasses import dataclass
from math import pi


@dataclass(frozen=True)
class AerodynamicState:
    dynamic_pressure_pa: float
    lift_coefficient: float
    induced_drag_coefficient: float
    drag_coefficient: float
    drag_n: float
    lift_to_drag_ratio: float


def evaluate_cruise_aerodynamics(
    *,
    weight_n: float,
    speed_m_s: float,
    density_kg_m3: float,
    wing_area_m2: float,
    aspect_ratio: float,
    zero_lift_drag_coefficient: float,
    oswald_efficiency: float,
) -> AerodynamicState:
    """
    Evaluate steady, level cruise with a parabolic drag polar.

    Assumptions:
    - lift equals aircraft weight;
    - coefficients are evaluated at one cruise condition;
    - compressibility and detailed geometry effects are not modeled.
    """
    if min(
        weight_n,
        speed_m_s,
        density_kg_m3,
        wing_area_m2,
        aspect_ratio,
        zero_lift_drag_coefficient,
        oswald_efficiency,
    ) <= 0:
        raise ValueError("Aerodynamic inputs must be positive.")

    dynamic_pressure = 0.5 * density_kg_m3 * speed_m_s**2
    lift_coefficient = weight_n / (dynamic_pressure * wing_area_m2)

    induced_drag_coefficient = (
        lift_coefficient**2 / (pi * oswald_efficiency * aspect_ratio)
    )
    drag_coefficient = (
        zero_lift_drag_coefficient + induced_drag_coefficient
    )
    drag_n = dynamic_pressure * wing_area_m2 * drag_coefficient
    lift_to_drag_ratio = lift_coefficient / drag_coefficient

    return AerodynamicState(
        dynamic_pressure_pa=dynamic_pressure,
        lift_coefficient=lift_coefficient,
        induced_drag_coefficient=induced_drag_coefficient,
        drag_coefficient=drag_coefficient,
        drag_n=drag_n,
        lift_to_drag_ratio=lift_to_drag_ratio,
    )
