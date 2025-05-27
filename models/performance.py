import numpy as np
from models.atmosphere import isa_atmosphere


def compute_fuel_burn(sfc , T):
    return (sfc * T)

def convert_cas_to_tas(cas_knots, altitude_m):
    cas_ms = cas_knots * 0.51444  # knots to m/s
    _, _, rho, _, _ = isa_atmosphere(altitude_m)
    rho0 = 1.225  # kg/m^3 at sea level
    tas = cas_ms * (rho0 / rho)**0.5
    return tas

def calculate_range_breguet(v, sfc, l_d, wi, wf):
    return (v / sfc) * l_d * np.log(wi / wf)

def calculate_final_weight_from_range(v, sfc, l_d, wi, range_m):
    exponent = -range_m * sfc / (v * l_d)
    return wi * np.exp(exponent)
