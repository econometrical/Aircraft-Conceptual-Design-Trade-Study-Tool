from .aerodynamics import evaluate_cruise_aerodynamics
from .atmosphere import standard_atmosphere
from .models import AircraftInputs, AircraftResults
from .performance import evaluate_jet_cruise_performance


GRAVITY_M_S2 = 9.80665


def analyze_aircraft(inputs: AircraftInputs) -> AircraftResults:
    """Run the complete low-fidelity conceptual aircraft analysis."""
    inputs.validate()

    atmosphere = standard_atmosphere(inputs.cruise_altitude_m)
    cruise_speed = inputs.cruise_mach * atmosphere.speed_of_sound_m_s
    weight_n = inputs.takeoff_mass_kg * GRAVITY_M_S2

    aero = evaluate_cruise_aerodynamics(
        weight_n=weight_n,
        speed_m_s=cruise_speed,
        density_kg_m3=atmosphere.density_kg_m3,
        wing_area_m2=inputs.wing_area_m2,
        aspect_ratio=inputs.aspect_ratio,
        zero_lift_drag_coefficient=inputs.zero_lift_drag_coefficient,
        oswald_efficiency=inputs.oswald_efficiency,
    )

    mission = evaluate_jet_cruise_performance(
        initial_mass_kg=inputs.takeoff_mass_kg,
        fuel_mass_kg=inputs.fuel_mass_kg,
        speed_m_s=cruise_speed,
        lift_to_drag_ratio=aero.lift_to_drag_ratio,
        tsfc_per_s=inputs.tsfc_per_s,
    )

    return AircraftResults(
        cruise_speed_m_s=cruise_speed,
        air_density_kg_m3=atmosphere.density_kg_m3,
        dynamic_pressure_pa=aero.dynamic_pressure_pa,
        wing_loading_kg_m2=(
            inputs.takeoff_mass_kg / inputs.wing_area_m2
        ),
        lift_coefficient=aero.lift_coefficient,
        induced_drag_coefficient=aero.induced_drag_coefficient,
        drag_coefficient=aero.drag_coefficient,
        drag_n=aero.drag_n,
        lift_to_drag_ratio=aero.lift_to_drag_ratio,
        fuel_fraction=mission.fuel_fraction,
        final_mass_kg=mission.final_mass_kg,
        range_km=mission.range_m / 1000.0,
        endurance_hr=mission.endurance_s / 3600.0,
    )
