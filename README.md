# Aircraft Mission Simulation

This project simulates the performance of a fixed-wing, subsonic aircraft through a complete mission profile—including takeoff, climb, cruise, descent, and landing. The simulation is modular and designed for educational and analytical use in the field of aeronautical engineering.

## Project Overview

The simulation is built using Python and structured for clarity, modularity, and extensibility. Each mission phase is represented by a dedicated function and relies on standard aerodynamic and atmospheric models.

## Directory Structure

```
aircraft_mission_sim/
│
├── main.py                        # Main script to run the mission simulation
├── configs/
│   ├── aircraft_config.py         # Aircraft parameters (from class or CSV)
│   └── mission_config.py          # Mission definitions (altitude, reserve fuel, etc.)
├── models/
│   ├── atmosphere.py              # ISA model: temperature, pressure, density, sound speed
│   ├── aerodynamics.py            # Lift, drag, thrust calculations
│   ├── performance.py             # Fuel usage, range, and climb performance
│   └── mission_simulator.py       # Controls flight phase transitions and simulation steps
├── plots/
│   └── visualizer.py              # Plots altitude, TAS, and fuel logs
├── data/
│   └── aircraft_profiles.csv      # Optional CSV for loading multiple aircraft configurations
└── docs/
    └── README.md                  # Project documentation
```

## Features

- Simulates complete flight missions with defined aircraft and mission parameters.
- Modular structure allows for easy addition or replacement of models (e.g., aerodynamic or engine models).
- Implements the International Standard Atmosphere (ISA) model.
- Uses classical equations for climb performance and fuel consumption (e.g., Breguet range).
- Generates clean plots for altitude, true airspeed (TAS), and fuel usage over time.

## How to Run

Ensure you have Python installed along with the required libraries (`numpy`, `matplotlib`). Then run:

```bash
python main.py
```

## Outputs

- Takeoff time and distance
- Climb profile (altitude, fuel usage, time)
- Cruise and descent placeholders (to be implemented)
- Visual plots:
  - Altitude vs Time
  - TAS vs Time
  - Fuel vs Time

  ### Sample Output for A320

**Altitude vs Time**
![Altitude vs Time](.../plots/sample_plots/Altitude-Time_A320.png)

**True Airspeed vs Time**
![TAS vs Time](.../plots/sample_plots/TAS-Time_A320.png)

**Fuel vs Time**
![Fuel vs Time](.../plots/sample_plots/Fuel-Time_A320.png)

## Dependencies

- Python 3.x
- NumPy
- Matplotlib

## Future Work

- Implement descent and landing simulation
- Introduce environmental effects (wind, temperature variation)
- Expand to include multiple aircraft configurations via CSV
- Enable output export to CSV or Excel for further analysis

## Author

Anhad Khurana  
Undergraduate Student, Aeronautical and Astronautical Engineering  
Purdue University
