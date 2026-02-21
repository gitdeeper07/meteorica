"""
Shock Metamorphism Grade (SMG)
Hugoniot-based continuous shock scale from research paper.
"""

import numpy as np
from typing import Dict, List, Optional

# Indicator weights from research
INDICATOR_WEIGHTS = {
    'olivine_planar': 0.28,
    'feldspar_state': 0.24,
    'metal_melting': 0.18,
    'high_pressure_phases': 0.16,
    'sulfide_state': 0.09,
    'porosity': 0.05
}

# Pressure mapping functions
def olivine_to_pressure(indicator_value: float) -> float:
    """Convert olivine planar features to pressure (GPa)."""
    if indicator_value < 0.1:
        return 4.0  # S1
    elif indicator_value < 0.25:
        return 8.0  # S2
    elif indicator_value < 0.45:
        return 15.0  # S3
    elif indicator_value < 0.65:
        return 28.0  # S4
    elif indicator_value < 0.85:
        return 45.0  # S5
    else:
        return 70.0  # S6

def feldspar_to_pressure(indicator_value: float) -> float:
    """Convert feldspar state to pressure (GPa)."""
    if indicator_value < 0.2:
        return 4.0
    elif indicator_value < 0.4:
        return 12.0
    elif indicator_value < 0.6:
        return 25.0  # Maskelynite onset
    elif indicator_value < 0.8:
        return 40.0
    else:
        return 65.0

def metal_to_pressure(indicator_value: float) -> float:
    """Convert metal melting extent to pressure (GPa)."""
    return 8.0 + indicator_value * 55.0

def high_pressure_to_pressure(indicator_value: float) -> float:
    """Convert high-pressure phases abundance to pressure (GPa)."""
    if indicator_value < 0.1:
        return 0.0
    elif indicator_value < 0.3:
        return 22.0
    elif indicator_value < 0.6:
        return 38.0
    else:
        return 58.0

def sulfide_to_pressure(indicator_value: float) -> float:
    """Convert sulfide state to pressure (GPa)."""
    return 4.0 + indicator_value * 38.0

def porosity_to_pressure(indicator_value: float) -> float:
    """Convert porosity reduction to pressure (GPa)."""
    return 2.0 + (1.0 - indicator_value) * 48.0

# Mapping from indicator names to functions
INDICATOR_FUNCTIONS = {
    'olivine_planar': olivine_to_pressure,
    'feldspar_state': feldspar_to_pressure,
    'metal_melting': metal_to_pressure,
    'high_pressure_phases': high_pressure_to_pressure,
    'sulfide_state': sulfide_to_pressure,
    'porosity': porosity_to_pressure
}


def calculate_smg(shock_data: Dict[str, float]) -> Dict[str, float]:
    """
    Calculate Shock Metamorphism Grade.
    
    SMG = Σ wᵢ · f_i(P_peak) / Σ wᵢ
    
    Args:
        shock_data: Dictionary with shock indicator values (0-1 scale)
        
    Returns:
        Dictionary with SMG value and peak pressure
    """
    weighted_pressure_sum = 0.0
    weight_sum = 0.0
    pressures = {}
    
    for indicator, value in shock_data.items():
        if indicator in INDICATOR_WEIGHTS and indicator in INDICATOR_FUNCTIONS:
            weight = INDICATOR_WEIGHTS[indicator]
            pressure = INDICATOR_FUNCTIONS[indicator](value)
            
            weighted_pressure_sum += weight * pressure
            weight_sum += weight
            pressures[indicator] = pressure
    
    if weight_sum == 0:
        return {'smg': 0.0, 'peak_pressure_gpa': 0.0, 'shock_stage': 'S1'}
    
    peak_pressure = weighted_pressure_sum / weight_sum
    
    # Convert pressure to SMG (normalized 0-1 scale)
    smg = min(1.0, peak_pressure / 90.0)
    
    # Determine shock stage
    shock_stage = get_shock_stage(peak_pressure)
    
    return {
        'smg': smg,
        'peak_pressure_gpa': peak_pressure,
        'shock_stage': shock_stage,
        'pressures': pressures
    }


def get_shock_stage(pressure_gpa: float) -> str:
    """
    Get traditional shock stage from pressure.
    
    Args:
        pressure_gpa: Peak pressure in GPa
        
    Returns:
        Shock stage (S1-S6)
    """
    if pressure_gpa < 5:
        return 'S1'
    elif pressure_gpa < 10:
        return 'S2'
    elif pressure_gpa < 20:
        return 'S3'
    elif pressure_gpa < 35:
        return 'S4'
    elif pressure_gpa < 55:
        return 'S5'
    else:
        return 'S6'


def calculate_post_shock_temperature(t0: float, p_shock: float, 
                                     delta_v: float, c_v: float, 
                                     rho: float) -> float:
    """
    Calculate post-shock temperature using Hugoniot equation.
    
    T_post = T_0 + (P_shock · ΔV) / (2 · c_v · ρ)
    
    Args:
        t0: Initial temperature (K)
        p_shock: Shock pressure (Pa)
        delta_v: Volume change (m³/kg)
        c_v: Specific heat capacity (J/kg·K)
        rho: Density (kg/m³)
        
    Returns:
        Post-shock temperature (K)
    """
    return t0 + (p_shock * delta_v) / (2 * c_v * rho)
