class mission:
    def __init__(self):
        # Mission Parameters 
        self.cruise_altitude = 11000        # Crusie Altitude in m
        self.cruise_mach = 0.78             # Speed in Mach
        self.climb_cas = [250 , 300]        # Constant Climb Speed in knots (alt <= 10000ft , alt > 10000ft)
        self.range = 5700                   # Horizontal Range in km
        self.payload = 19000                # (Passenger + Cargo) Mass in kg
        self.initial_fuel = 18000           # Fuel in kg
        self.reserve_fuel = 3000            # Fuel held in reserve in kg
        self.rolling_friction = 0.02        # Rolling Friction Constant 
        self.descent_end_altitude = 0       # meters above ground
        self.descent_rate = 5               # m/s (~1000 fpm)
        self.descent_cas = 250              # knots CAS for descent
        self.landing_mu = 0.4               # Friction Coef for Landing

