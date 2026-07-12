from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class AircraftInputs:
    """High-level inputs used during conceptual aircraft analysis."""

    wing_area_m2: float = 120.0
    aspect_ratio: float = 9.0
    takeoff_mass_kg: float = 38_000.0
    fuel_mass_kg: float = 9_000.0
    payload_mass_kg: float = 2_000.0
    cruise_mach: float = 0.82
    cruise_altitude_m: float = 11_000.0
    zero_lift_drag_coefficient: float = 0.020
    oswald_efficiency: float = 0.82

    # Approximate jet thrust-specific fuel consumption in 1/s.
    # This is a deliberately simplified, constant cruise value.
    tsfc_per_s: float = 1.7e-4

    def validate(self) -> None:
        positive_fields = {
            "wing_area_m2": self.wing_area_m2,
            "aspect_ratio": self.aspect_ratio,
            "takeoff_mass_kg": self.takeoff_mass_kg,
            "fuel_mass_kg": self.fuel_mass_kg,
            "cruise_mach": self.cruise_mach,
            "tsfc_per_s": self.tsfc_per_s,
        }
        for name, value in positive_fields.items():
            if value <= 0:
                raise ValueError(f"{name} must be positive.")

        if self.fuel_mass_kg >= self.takeoff_mass_kg:
            raise ValueError("fuel_mass_kg must be below takeoff_mass_kg.")

        if not 0 < self.oswald_efficiency <= 1:
            raise ValueError("oswald_efficiency must be in (0, 1].")

        if self.zero_lift_drag_coefficient <= 0:
            raise ValueError("zero_lift_drag_coefficient must be positive.")

        if self.cruise_altitude_m < 0:
            raise ValueError("cruise_altitude_m cannot be negative.")


@dataclass(frozen=True)
class AircraftResults:
    cruise_speed_m_s: float
    air_density_kg_m3: float
    dynamic_pressure_pa: float
    wing_loading_kg_m2: float
    lift_coefficient: float
    induced_drag_coefficient: float
    drag_coefficient: float
    drag_n: float
    lift_to_drag_ratio: float
    fuel_fraction: float
    final_mass_kg: float
    range_km: float
    endurance_hr: float

    def to_dict(self) -> dict[str, float]:
        return asdict(self)
