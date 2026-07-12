# Aircraft Conceptual Design Trade-Study Tool

A learning-oriented Python prototype for rapid aircraft conceptual design studies.

This project is intentionally **low fidelity**. It is designed to demonstrate the workflow of:

1. defining aircraft design inputs;
2. evaluating simplified aerodynamic and mission-performance models;
3. running parameter sweeps;
4. visualizing engineering trade-offs;
5. validating model trends with automated tests.

It is not a certified engineering tool and must not be used for real aircraft design decisions.

## Project structure

```text
aircraft-conceptual-design-tool/
├── app.py
├── main.py
├── requirements.txt
├── src/
│   └── aircraft_design/
│       ├── __init__.py
│       ├── models.py
│       ├── atmosphere.py
│       ├── aerodynamics.py
│       ├── performance.py
│       ├── analysis.py
│       └── trade_study.py
└── tests/
    └── test_analysis.py
```

## Main inputs

- wing area, m²
- aspect ratio
- maximum takeoff mass, kg
- fuel mass, kg
- payload mass, kg
- cruise Mach number
- cruise altitude, m
- zero-lift drag coefficient
- Oswald efficiency factor
- thrust-specific fuel consumption

## Main outputs

- cruise speed
- wing loading
- dynamic pressure
- lift coefficient
- induced-drag coefficient
- total drag coefficient
- drag
- lift-to-drag ratio
- estimated range
- estimated endurance
- fuel fraction

## Model assumptions

The prototype uses:

- ISA-like troposphere approximation for atmospheric properties;
- parabolic drag polar:
  `CD = CD0 + CL² / (π e AR)`;
- steady, level cruise:
  `L = W`;
- simplified Breguet jet range relation;
- constant aerodynamic coefficients and fuel-consumption parameter during cruise;
- all listed fuel mass is treated as available for the simplified cruise segment.

These assumptions make the tool fast and understandable, but they also limit accuracy.

## Installation

Create and activate a virtual environment.

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the command-line analysis

```bash
python main.py
```

## Run the Dash application

```bash
python app.py
```

Open the local address printed in the terminal, usually:

```text
http://127.0.0.1:8050
```

## Run tests

```bash
pytest
```

## Example interview description

> I built a low-fidelity aircraft conceptual-design prototype in Python to understand how early design variables affect system-level performance. The tool separates atmospheric, aerodynamic and mission-performance models into reusable modules, then connects them in a single analysis workflow. It also supports parameter sweeps, such as changing wing area or aspect ratio, so that I can study trade-offs rather than evaluate only one configuration. I used AI-assisted coding during implementation, but I reviewed the equations, organized the architecture, tested expected physical trends and documented the assumptions and limitations.

## Suggested development history

Use separate Git commits such as:

```text
Initialize project structure and aircraft data model
Add atmosphere and aerodynamic analysis
Add Breguet range and integrated aircraft analysis
Add wing-area and aspect-ratio trade studies
Add Dash interface and plots
Add validation tests and documentation
```


## Important interpretation note

Changing one variable does not guarantee a monotonic improvement. For example,
at fixed aircraft weight and cruise speed, increasing wing area lowers lift
coefficient and induced drag, but increases parasite-drag area. The simplified
model can therefore produce an interior optimum rather than showing that a
larger wing is always better. That trade-off is one of the main lessons of the
prototype.
