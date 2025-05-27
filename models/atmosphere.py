import numpy as np 


def isa_atmosphere(altitude):
    if altitude >= 0 and altitude <= 11000:
        T , p , r , speed_sound , g = isa_troposphere(altitude)
    elif altitude > 11000:
        T , p , r , speed_sound , g = isa_stratosphere(altitude)
    
    return T , p , r , speed_sound , g

# Layer: Troposphere
def isa_troposphere(altitude):
    
    # Constants
    gamma = 1.4
    g = 9.80665                                     # Acceleration Due to Gravity in m/s2
    R = 287                                         # Gas Constant in J/kg K
    L = 0.00649                                     # Lapse Rate in K/m
    T_Sea = 288.15                                  # Temp at Sea Level in K
    p_Sea = 101325                                  # Pressure at Sea Level in Pa
    
    T = T_Sea - (L * altitude)                                      # Temperature in K
    p = p_Sea * np.pow((1 - (L * altitude)/T_Sea) , g/(R * L))      # Pressure in Pa
    r = p / (R * T)                                                 # Density in kg/m3
    speed_sound = np.sqrt(gamma * R * T)                            # Speed of Sound in m/s
    
    T = round(T , 5)
    p = round(p , 5)
    r = round(r , 5)
    speed_sound = round(speed_sound , 5)

    return T , p , r , speed_sound , g

import numpy as np

# Layer: Stratosphere
def isa_stratosphere(altitude):
    if altitude < 11000 or altitude > 20000:
        raise ValueError("This function is valid only for altitudes between 11000 m and 20000 m.")

    # Constants
    gamma = 1.4
    g = 9.80665                  # m/s²
    R = 287                      # J/kg·K
    T_tropopause = 216.65        # Temperature at tropopause (K)
    p_tropopause = 22632.06      # Pressure at 11 km (Pa), from ISA
    h_base = 11000               # Base altitude of stratosphere (m)

    # Temperature remains constant
    T = T_tropopause

    # Pressure using isothermal equation
    exp_factor = -g * (altitude - h_base) / (R * T)
    p = p_tropopause * np.exp(exp_factor)

    # Density
    r = p / (R * T)

    # Speed of sound
    speed_sound = np.sqrt(gamma * R * T)

    # Round values
    T = round(T, 5)
    p = round(p, 5)
    r = round(r, 5)
    speed_sound = round(speed_sound, 5)

    return T, p, r, speed_sound, g
