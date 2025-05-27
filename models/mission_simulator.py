import numpy as np
from models.atmosphere import isa_atmosphere
from models.aerodynamics import compute_drag , compute_drag_coefficient , compute_lift_coefficient , compute_l_over_d
from models.performance import compute_fuel_burn , convert_cas_to_tas  , calculate_final_weight_from_range , calculate_range_breguet


def sim_takeoff(aircraft , mission):
    ## --- Setup ---
    # At-Sea-Level Atmosphere 
    temp_SeaLevel , pressure_SeaLevel , atmos_Density_SeaLevel , speedSound_Sealevel , g = isa_atmosphere(0) # Initializing Sea-Level Atmospheric Constants 

    # Aircraft Details
    empty_Mass = aircraft.empty_Mass 
    wing_Area = aircraft.wing_area
    cdo = aircraft.cdo
    clto = aircraft.clto
    aspect_Ratio = aircraft.aspect_ratio
    eff = aircraft.oswald_eff
    thrust = aircraft.engine_thrust

    # Mission Details
    initial_Fuel = mission.initial_fuel
    res_Fuel = mission.reserve_fuel
    payload = mission.payload
    roll_Friction_Const = mission.rolling_friction

    # Calculations
    total_Initial_Fuel = initial_Fuel + res_Fuel                            # Total Initial Fuel in kg
    total_Initial_Mass = empty_Mass + total_Initial_Fuel + payload          # Total Initial Mass of Aircraft 

    ## --- Begin Simulation ---
    initial_time = 0
    initial_vel = 0
    initial_dist = 0
    lift = 0
    dt = 0.1

    # Empty Lists to Store Values
    time = [initial_time] 
    vel = [initial_vel]
    dist = [initial_dist]

    cdto = cdo + ((clto ** 2) / (np.pi * eff * aspect_Ratio))

    while lift <= (total_Initial_Mass * g):
        lift = 0.5 * atmos_Density_SeaLevel * (vel[-1] ** 2) * wing_Area * clto
        drag = 0.5 * atmos_Density_SeaLevel * (vel[-1] ** 2) * wing_Area * cdto
        rolling_Fric = roll_Friction_Const * (total_Initial_Mass - lift)

        acc = (thrust - drag - rolling_Fric) / (total_Initial_Mass)

        vel.append( vel[-1] + acc * dt )
        dist.append( dist[-1] + vel[-1] * dt )
        time.append( time[-1] + dt )

    return time , dist , vel


def sim_climb(aircraft , mission, inital_vel):
    ## --- Setup ---
    gamma = 1.4

    # At-Sea-Level Atmosphere 
    temp_SeaLevel , pressure_SeaLevel , atmos_Density_SeaLevel , speedSound_Sealevel , g = isa_atmosphere(0) # Initializing Sea-Level Atmospheric Constants 
    
    # Aircraft Details
    empty_Mass = aircraft.empty_Mass 
    wing_Area = aircraft.wing_area
    aspect_Ratio = aircraft.aspect_ratio
    eff = aircraft.oswald_eff
    thrust_SeaLevel = aircraft.engine_thrust
    height_com = aircraft.height_com
    sfc = aircraft.sfc
    coef_DO = aircraft.cdo

    # Mission Details
    initial_Fuel = mission.initial_fuel
    res_Fuel = mission.reserve_fuel
    payload = mission.payload
    cruise_alt = mission.cruise_altitude
    climb_cas = mission.climb_cas 

    # Calculations
    total_Initial_Fuel = initial_Fuel + res_Fuel                            # Total Initial Fuel in kg
    total_Initial_Mass = empty_Mass + total_Initial_Fuel + payload          # Total Initial Mass of Aircraft 

    ## --- Begin Simulation ---
    initial_altitude = height_com
    altitude = [initial_altitude]
    fuel_log = [total_Initial_Fuel]
    tas_log = [inital_vel]
    time = [0]
    dt = 0.1

    transition_duration = 30  # seconds
    target_cas = mission.climb_cas[0]  # CAS in knots
    target_tas = convert_cas_to_tas(target_cas, altitude[-1])  # implement this

    while altitude[-1] < cruise_alt: 
        temp , static_pressure , atmos_Density , speedSound , g = isa_atmosphere(0.3048 * altitude[-1])

        # During first few seconds after takeoff
        if time[-1] < transition_duration:
            climb_tas = np.interp(time[-1], [0, transition_duration], [tas_log[-1], target_tas])
        else:
            # Use regular CAS logic after transition
            cas = mission.climb_cas[0] if altitude[-1] < 3048 else mission.climb_cas[1]
            climb_tas = convert_cas_to_tas(cas, altitude[-1])

        tas_log.append(climb_tas)

        thrust = thrust_SeaLevel * (atmos_Density / atmos_Density_SeaLevel) ** 0.8

        fuel_used = (compute_fuel_burn(sfc , thrust) * dt)
        fuel_log.append(fuel_log[-1] - fuel_used)
        mass = empty_Mass + payload + fuel_log[-1]
        weight = mass * g

        lift_coef = compute_lift_coefficient(weight , atmos_Density , climb_tas , wing_Area)
        drag_coef = compute_drag_coefficient(coef_DO, aspect_Ratio, eff, lift_coef)
        drag = compute_drag(atmos_Density , climb_tas , wing_Area , drag_coef)

        power_excess = (thrust - drag) * climb_tas

        climb_rate = power_excess / weight

        altitude.append(altitude[-1] + climb_rate*dt) 
        time.append(time[-1] + dt)

    return time , altitude , tas_log , fuel_log

def sim_cruise(aircraft, mission, initial_fuel):
    ## --- Setup ---
    gamma = 1.4

    # At-Sea-Level Atmosphere 
    temp_SeaLevel , pressure_SeaLevel , atmos_Density_SeaLevel , speedSound_Sealevel , g = isa_atmosphere(0)  # Sea-level reference

    # Aircraft Details
    empty_Mass = aircraft.empty_Mass 
    wing_Area = aircraft.wing_area
    aspect_Ratio = aircraft.aspect_ratio
    eff = aircraft.oswald_eff
    thrust_SeaLevel = aircraft.engine_thrust
    sfc = aircraft.sfc
    coef_DO = aircraft.cdo

    # Mission Details
    payload = mission.payload
    cruise_alt = mission.cruise_altitude
    cruise_mach = mission.cruise_mach
    cruise_range = mission.range * 1000 # in meters

    # Atmosphere at Cruise
    temp , pressure , atmos_Density , speedSound , g = isa_atmosphere(cruise_alt * 0.3048)  # Convert feet to meters
    tas = cruise_mach * speedSound

    # Mass & Weight
    total_Initial_Mass = empty_Mass + initial_fuel + payload
    weight = total_Initial_Mass * g

    # Aerodynamics
    cl = compute_lift_coefficient(weight , atmos_Density , tas , wing_Area)
    l_d = compute_l_over_d(coef_DO, eff, aspect_Ratio , cl)

    ## --- Begin Simulation ---
    # Fuel Burn (Breguet)
    wf = calculate_final_weight_from_range(tas, sfc, l_d, total_Initial_Mass, cruise_range)
    fuel_burned = total_Initial_Mass - wf
    remaining_fuel = fuel_burned - (empty_Mass + payload - wf)
    cruise_time = cruise_range / tas

    # Logs
    time = [0, cruise_time]
    altitude = [cruise_alt, cruise_alt]
    tas_log = [tas, tas]
    fuel_log = [initial_fuel, initial_fuel - fuel_burned]

    return time, altitude, tas_log, fuel_log

def sim_descent(aircraft, mission, initial_altitude, initial_fuel, initial_tas):
    ## --- Setup ---
    gamma = 1.4

    # Atmospheric Constants
    temp_SeaLevel, pressure_SeaLevel, rho_SeaLevel, speedSound_SeaLevel, g = isa_atmosphere(0)

    # Aircraft Details
    empty_Mass = aircraft.empty_Mass 
    wing_Area = aircraft.wing_area
    aspect_Ratio = aircraft.aspect_ratio
    eff = aircraft.oswald_eff
    thrust_SeaLevel = aircraft.engine_thrust
    sfc = aircraft.sfc
    coef_DO = aircraft.cdo

    # Mission Details
    payload = mission.payload
    descent_rate = mission.descent_rate  # m/s
    descent_final_alt = mission.descent_end_altitude  # in meters
    descent_cas = mission.descent_cas  # CAS in knots

    ## --- Begin Simulation ---
    dt = 0.1
    altitude = [initial_altitude]
    time = [0]
    tas_log = [initial_tas]
    fuel_log = [initial_fuel]

    while altitude[-1] > descent_final_alt:
        temp, pressure, rho, speedSound, g = isa_atmosphere(altitude[-1])
        tas = convert_cas_to_tas(descent_cas, altitude[-1])
        tas_log.append(tas)

        thrust = 0.3 * thrust_SeaLevel * (rho / rho_SeaLevel)**0.8  # idle thrust
        mass = empty_Mass + payload + fuel_log[-1]
        weight = mass * g

        cl = compute_lift_coefficient(weight, rho, tas, wing_Area)
        cd = compute_drag_coefficient(coef_DO, aspect_Ratio, eff, cl)
        drag = compute_drag(rho, tas, wing_Area, cd)

        fuel_used = compute_fuel_burn(sfc, thrust) * dt
        fuel_log.append(fuel_log[-1] - fuel_used)

        # Constant descent rate
        next_alt = altitude[-1] - descent_rate * dt
        altitude.append(next_alt)
        time.append(time[-1] + dt)

    return time, altitude, tas_log, fuel_log

def sim_landing(aircraft, mission, landing_speed, initial_fuel):
    ## --- Setup ---
    gamma = 1.4

    # Atmospheric Conditions (assume sea level)
    temp, pressure, rho, speedSound, g = isa_atmosphere(0)

    # Aircraft
    empty_Mass = aircraft.empty_Mass 
    wing_Area = aircraft.wing_area
    aspect_Ratio = aircraft.aspect_ratio
    eff = aircraft.oswald_eff
    sfc = aircraft.sfc
    coef_DO = aircraft.cdo

    # Mission
    payload = mission.payload
    mu = mission.landing_mu  # braking friction coefficient

    # Initial State
    mass = empty_Mass + payload + initial_fuel
    weight = mass * g
    tas = landing_speed  # m/s at touchdown
    dt = 0.1

    time = [0]
    velocity = [tas]
    distance = [0]
    fuel_log = [initial_fuel]

    while velocity[-1] > 1:  # until nearly stopped
        cl = 0.0  # no lift post-flare
        cd = coef_DO  # assume clean configuration
        drag = compute_drag(rho, velocity[-1], wing_Area, cd)
        braking_force = mu * weight
        decel = (drag + braking_force) / mass

        new_vel = velocity[-1] - decel * dt
        new_vel = max(new_vel, 0)
        velocity.append(new_vel)

        distance.append(distance[-1] + new_vel * dt)
        time.append(time[-1] + dt)

        fuel_burn = compute_fuel_burn(sfc, 0.05 * weight) * dt  # minimal idle power
        fuel_log.append(fuel_log[-1] - fuel_burn)

    return time, distance, velocity, fuel_log
