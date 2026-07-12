from dataclasses import dataclass
from math import sqrt


@dataclass(frozen=True)
class AtmosphereState:
    temperature_k: float
    pressure_pa: float
    density_kg_m3: float
    speed_of_sound_m_s: float


def standard_atmosphere(altitude_m: float) -> AtmosphereState:
    """
    Approximate International Standard Atmosphere up to 20 km.

    The model uses a troposphere relation below 11 km and an isothermal
    approximation from 11 km to 20 km.
    """
    if not 0 <= altitude_m <= 20_000:
        raise ValueError("This simplified atmosphere model supports 0-20,000 m.")

    g = 9.80665
    gas_constant = 287.05
    gamma = 1.4
    sea_level_temperature = 288.15
    sea_level_pressure = 101_325.0
    lapse_rate = -0.0065

    if altitude_m <= 11_000:
        temperature = sea_level_temperature + lapse_rate * altitude_m
        pressure = sea_level_pressure * (
            temperature / sea_level_temperature
        ) ** (-g / (lapse_rate * gas_constant))
    else:
        tropopause_temperature = 216.65
        tropopause_pressure = 22_632.06
        temperature = tropopause_temperature
        pressure = tropopause_pressure * (
            2.718281828459045
            ** (
                -g
                * (altitude_m - 11_000)
                / (gas_constant * tropopause_temperature)
            )
        )

    density = pressure / (gas_constant * temperature)
    speed_of_sound = sqrt(gamma * gas_constant * temperature)

    return AtmosphereState(
        temperature_k=temperature,
        pressure_pa=pressure,
        density_kg_m3=density,
        speed_of_sound_m_s=speed_of_sound,
    )
