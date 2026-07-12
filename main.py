from pprint import pprint

from src.aircraft_design.analysis import analyze_aircraft
from src.aircraft_design.models import AircraftInputs
from src.aircraft_design.trade_study import run_trade_study


def main() -> None:
    aircraft = AircraftInputs()

    print("BASELINE ANALYSIS")
    print("=" * 60)
    result = analyze_aircraft(aircraft)
    pprint(result.to_dict())

    print("\nWING-AREA TRADE STUDY")
    print("=" * 60)
    study = run_trade_study(
        baseline=aircraft,
        variable="wing_area_m2",
        values=[90, 100, 110, 120, 130, 140, 150],
    )
    print(
        study[
            [
                "wing_area_m2",
                "wing_loading_kg_m2",
                "lift_to_drag_ratio",
                "range_km",
                "drag_kn",
            ]
        ].to_string(index=False)
    )


if __name__ == "__main__":
    main()
