# Theory and Modeling Assumptions

## Atmospheric Model

This simulation uses the International Standard Atmosphere (ISA) model up to 20 km altitude. The ISA divides the atmosphere into layers with defined temperature gradients:

- **Troposphere (0–11 km):** A constant temperature lapse rate of −6.49 K/km is applied.
- **Stratosphere (11–20 km):** Temperature is held constant at 216.65 K.

Using the ISA model, temperature, pressure, air density, and speed of sound are computed with standard relations. These atmospheric properties are essential for evaluating aerodynamic forces and engine performance.

## Aerodynamic Assumptions

- **Lift** is calculated using:
  \
  L = (1/2) * ρ * V^2 * C_L * S
  \
  where ρ is air density, V is true airspeed, C_L is the lift coefficient, and S is wing area.

- **Drag** includes both parasitic and induced drag:
  \
  D = (1/2) * ρ * V^2 * C_D * S
  \
  with:
  \
  C_D = C_D0 + (C_L^2) / (π * e * AR)
  \
  where C_D0 is the zero-lift drag coefficient, e is Oswald efficiency factor, and AR is the aspect ratio.

## Climb Model

Climb performance is based on **excess power**:

\
dh/dt = ((T - D) * V) / W
\

Thrust is reduced as a function of altitude. Fuel consumption during climb is estimated using engine SFC (Specific Fuel Consumption) and thrust required.

## Cruise Model

Cruise is simulated as a steady-state phase at constant TAS and altitude. Thrust balances drag, and fuel flow is derived from:

\
Fuel Rate = SFC * T
\

Alternatively, range can be estimated using the Breguet range equation:

\
Range = (V / SFC) * (L/D) * ln(W_i / W_f)
\

## Descent Model

Descent is modeled using either a fixed vertical speed or a constant descent angle (e.g., 3° glide slope). It assumes:

- Reduced or idle thrust
- Smooth profile from cruise to landing
- Basic aerodynamic forces similar to climb in reverse

## Limitations and Assumptions

- **Subsonic-only model:** The CAS to TAS conversion uses compressible flow assumptions valid only for subsonic speeds. Transonic and supersonic effects are not accounted for.
- **No wind effects:** The simulation assumes calm air with no headwinds, tailwinds, or crosswinds.
- **No detailed engine modeling:** Thrust is reduced with altitude but does not account for temperature, throttle control, or transient behavior.
- **No configuration changes:** Flaps, gear, and control surfaces are not modeled. Aerodynamic coefficients are held constant per phase.
- **No environmental variation:** Weather, turbulence, or humidity are not simulated.
- **No flight control systems:** There is no autopilot, trim, or feedback control implemented.
- **Descent and landing simplifications:** The descent profile is geometric, and landing is modeled as a simple deceleration segment.
