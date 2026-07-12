from dataclasses import replace

from dash import Dash, Input, Output, State, dcc, html
import plotly.express as px

from src.aircraft_design.analysis import analyze_aircraft
from src.aircraft_design.models import AircraftInputs
from src.aircraft_design.trade_study import run_trade_study


BASELINE = AircraftInputs()

app = Dash(__name__)
app.title = "Aircraft Conceptual Design Tool"

app.layout = html.Div(
    [
        html.H1("Aircraft Conceptual Design Trade-Study Tool"),
        html.P(
            "Low-fidelity educational prototype. Outputs are estimates, "
            "not certified aircraft-performance predictions."
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Label("Wing area (m²)"),
                        dcc.Input(
                            id="wing-area",
                            type="number",
                            value=BASELINE.wing_area_m2,
                            min=50,
                            max=250,
                            step=1,
                        ),
                        html.Br(),
                        html.Label("Aspect ratio"),
                        dcc.Input(
                            id="aspect-ratio",
                            type="number",
                            value=BASELINE.aspect_ratio,
                            min=4,
                            max=15,
                            step=0.1,
                        ),
                        html.Br(),
                        html.Label("Takeoff mass (kg)"),
                        dcc.Input(
                            id="mass",
                            type="number",
                            value=BASELINE.takeoff_mass_kg,
                            min=5000,
                            max=100000,
                            step=100,
                        ),
                        html.Br(),
                        html.Label("Fuel mass (kg)"),
                        dcc.Input(
                            id="fuel-mass",
                            type="number",
                            value=BASELINE.fuel_mass_kg,
                            min=100,
                            max=40000,
                            step=100,
                        ),
                        html.Br(),
                        html.Label("Cruise Mach"),
                        dcc.Input(
                            id="mach",
                            type="number",
                            value=BASELINE.cruise_mach,
                            min=0.2,
                            max=0.95,
                            step=0.01,
                        ),
                        html.Br(),
                        html.Label("Cruise altitude (m)"),
                        dcc.Input(
                            id="altitude",
                            type="number",
                            value=BASELINE.cruise_altitude_m,
                            min=0,
                            max=15000,
                            step=100,
                        ),
                        html.Br(),
                        html.Button("Run analysis", id="run-button", n_clicks=0),
                    ],
                    style={
                        "display": "grid",
                        "gap": "8px",
                        "maxWidth": "420px",
                    },
                ),
                html.Div(id="results"),
            ],
            style={
                "display": "grid",
                "gridTemplateColumns": "minmax(320px, 420px) 1fr",
                "gap": "32px",
            },
        ),
        html.H2("Wing-area trade study"),
        dcc.Graph(id="range-graph"),
        dcc.Graph(id="ld-graph"),
    ],
    style={"fontFamily": "Arial, sans-serif", "margin": "32px"},
)


@app.callback(
    Output("results", "children"),
    Output("range-graph", "figure"),
    Output("ld-graph", "figure"),
    Input("run-button", "n_clicks"),
    State("wing-area", "value"),
    State("aspect-ratio", "value"),
    State("mass", "value"),
    State("fuel-mass", "value"),
    State("mach", "value"),
    State("altitude", "value"),
)
def update_analysis(
    _n_clicks: int,
    wing_area: float,
    aspect_ratio: float,
    mass: float,
    fuel_mass: float,
    mach: float,
    altitude: float,
):
    aircraft = replace(
        BASELINE,
        wing_area_m2=float(wing_area),
        aspect_ratio=float(aspect_ratio),
        takeoff_mass_kg=float(mass),
        fuel_mass_kg=float(fuel_mass),
        cruise_mach=float(mach),
        cruise_altitude_m=float(altitude),
    )

    result = analyze_aircraft(aircraft)

    metrics = html.Ul(
        [
            html.Li(f"Cruise speed: {result.cruise_speed_m_s:.1f} m/s"),
            html.Li(f"Wing loading: {result.wing_loading_kg_m2:.1f} kg/m²"),
            html.Li(f"Lift coefficient: {result.lift_coefficient:.3f}"),
            html.Li(f"Drag coefficient: {result.drag_coefficient:.4f}"),
            html.Li(f"Lift-to-drag ratio: {result.lift_to_drag_ratio:.2f}"),
            html.Li(f"Estimated drag: {result.drag_n / 1000:.1f} kN"),
            html.Li(f"Estimated range: {result.range_km:.0f} km"),
            html.Li(f"Estimated endurance: {result.endurance_hr:.1f} h"),
        ]
    )

    minimum = max(50.0, aircraft.wing_area_m2 * 0.7)
    maximum = aircraft.wing_area_m2 * 1.3
    values = [
        minimum + i * (maximum - minimum) / 20
        for i in range(21)
    ]

    study = run_trade_study(
        baseline=aircraft,
        variable="wing_area_m2",
        values=values,
    )

    range_figure = px.line(
        study,
        x="wing_area_m2",
        y="range_km",
        markers=True,
        labels={
            "wing_area_m2": "Wing area (m²)",
            "range_km": "Estimated range (km)",
        },
        title="Wing area versus estimated range",
    )

    ld_figure = px.line(
        study,
        x="wing_area_m2",
        y="lift_to_drag_ratio",
        markers=True,
        labels={
            "wing_area_m2": "Wing area (m²)",
            "lift_to_drag_ratio": "Lift-to-drag ratio",
        },
        title="Wing area versus lift-to-drag ratio",
    )

    return metrics, range_figure, ld_figure


if __name__ == "__main__":
    app.run(debug=True)
