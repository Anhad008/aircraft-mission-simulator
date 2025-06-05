# Aircraft Mission Simulation

This project simulates the full mission profile of a fixed-wing, subsonic aircraft, including takeoff, climb, cruise, descent, and landing. It is intended as an educational and analytical tool for early-stage aerospace engineering development and can be extended for more advanced research.

## Overview

The simulation is modular, physics-based, and customizable. Users can define aircraft parameters, mission profiles, and atmospheric models to observe performance metrics such as velocity, altitude, fuel consumption, and total mission time. The code is implemented in Python with a structured, object-oriented architecture.

## Features

- Modular simulation of complete mission profile
- ISA-based atmospheric modeling
- Lift, drag, and thrust calculations using standard aerodynamic models
- Time-step-based fuel and velocity tracking
- Configurable aircraft and mission parameters
- CSV logging of mission summary data
- Plots of key mission metrics (altitude, TAS, fuel)

## Physics and Governing Equations

| Parameter     | Equation |
|--------------|----------|
| Lift          | \( L = \frac{1}{2} \rho V^2 S C_L \) |
| Drag          | \( D = \frac{1}{2} \rho V^2 S \left(C_{D_0} + \frac{C_L^2}{\pi e AR}\right) \) |
| Thrust        | Defined per phase or assumed constant |
| Atmosphere    | Based on ISA: piecewise lapse rate model |
| Fuel Burn     | \( \dot{m}_{fuel} = \frac{T \cdot SFC}{g} \) |
| TAS from CAS  | Based on compressibility corrections (subsonic only) |

## Project Structure

```
aircraft_mission_sim/
│
├── main.py                      # Entry point for the simulation
│
├── configs/
│   ├── aircraft_config.py       # Aircraft parameters
│   └── mission_config.py        # Mission setup (altitude, reserve fuel, etc.)
│
├── models/
│   ├── atmosphere.py            # ISA atmosphere model
│   ├── aerodynamics.py          # Lift, drag, and thrust models
│   ├── performance.py           # Climb, cruise, descent performance
│   └── mission.py               # Segment controller
│
├── simulator/
│   └── mission_simulator.py     # Runs mission segments in sequence
│
├── plots/
│   └── visualizer.py            # Plotting functions for mission metrics
│
├── utils/
│   └── log_results.py           # CSV logging utility
│
├── data/
│   └── aircraft_profiles.csv    # Optional input database
│
├── docs/
│   ├── theory.md                # Theory, assumptions, and model references
│   └── sample_plots/           # Example mission outputs (PNG)
│
└── logs/
    └── mission_logs.csv         # Simulation output logs
```

## Example Output Plots

- Altitude vs. Time  
- Fuel Remaining vs. Time  
- True Airspeed (TAS) vs. Time  

(See `docs/sample_plots/` for visuals.)

## Installation

Clone the repository:
```bash
git clone https://github.com/yourusername/aircraft-mission-simulator.git
cd aircraft-mission-simulator
```

Install required packages (if any):
```bash
pip install -r requirements.txt
```

## Running the Simulation

```bash
python main.py
```

## Logging Results

After execution, mission summary results are stored in `outputs/output.csv` and can be used for post-analysis or performance tracking.

## Assumptions and Limitations

- Subsonic aircraft only
- ISA atmosphere; no weather, wind, or humidity effects
- Flat Earth assumption (no curvature or Coriolis effects)
- Constant SFC and thrust within each phase
- No flap/gear configuration changes during flight

## License

This project is intended for educational and research purposes.

## Contact

Author: Anhad Khurana  
AAE Undergraduate, Purdue University  
LinkedIn: [linkedin.com/in/anhadkhurana](https://www.linkedin.com/in/anhadkhurana)
