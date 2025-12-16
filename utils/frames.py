import numpy as np
from .constants import EARTH_ROTATION_RATE

def eci_to_ecef(position_eci, t):
    """
    Rotates a position vector from Earth-Centered Inertial (ECI) 
    to Earth-Centered Earth-Fixed (ECEF) frames based on time t.
    Assumes t=0 aligns the X-axes.
    """
    theta = EARTH_ROTATION_RATE * t
    
    # Rotation matrix around Z-axis
    c, s = np.cos(theta), np.sin(theta)
    R = np.array([
        [ c, s, 0],
        [-s, c, 0],
        [ 0, 0, 1]
    ])
    
    return R @ position_eci

def ecef_to_eci(position_ecef, t):
    """Inverse rotation (ECEF -> ECI)."""
    theta = EARTH_ROTATION_RATE * t
    c, s = np.cos(theta), np.sin(theta)
    
    # Transpose of rotation matrix is the inverse
    R = np.array([
        [ c, -s, 0],
        [ s,  c, 0],
        [ 0,  0, 1]
    ])
    
    return R @ position_ecef