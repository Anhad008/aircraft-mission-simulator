import numpy as np


def compute_lift_coefficient(W, rho, V, S):
    
    coefL = 2 * W / (rho * (V**2) * S)
    
    return coefL

def compute_drag_coefficient(coef_DO, aspect_ratio, eff, coefL):
    k = 1 / (np.pi * eff * aspect_ratio)

    coef_D = coef_DO + (k * (coefL**2))
    
    return coef_D

def compute_drag(rho, V, S, coef_D):
    
    Drag = 0.5 * rho * (V**2) * S * coef_D

    return Drag

def compute_l_over_d(cd0, eff , aspect_ratio, cl):
    k = 1 / (np.pi * eff * aspect_ratio)

    cd = cd0 + k * cl**2

    return cl / cd
