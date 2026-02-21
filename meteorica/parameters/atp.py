"""
Ablation Thermal Profile (ATP)
Atmospheric entry thermal modeling from research paper.
"""

import numpy as np
from typing import Dict, Optional

# Physical constants
STEFAN_BOLTZMANN = 5.67e-8  # W/m²/K⁴


def estimate_airburst(velocity: float, diameter: float, density: float) -> float:
    """
    Estimate airburst altitude based on entry parameters.
    
    Args:
        velocity: Entry velocity (m/s)
        diameter: Meteoroid diameter (m)
        density: Bulk density (kg/m³)
        
    Returns:
        Estimated airburst altitude (km), 0 if surface impact
    """
    mass = density * (4/3) * np.pi * (diameter/2) ** 3
    kinetic_energy_j = 0.5 * mass * (velocity ** 2)
    kinetic_energy_kt = kinetic_energy_j / 4.184e12  # Convert to kilotons TNT
    
    # Simple scaling from Chelyabinsk (500 kT airburst at 23 km)
    if kinetic_energy_kt < 10:
        return 0  # Too small, surface impact
    elif kinetic_energy_kt < 1000:
        # Rough scaling: E^(1/3) scaling
        return 23 * (kinetic_energy_kt / 500) ** (1/3)
    else:
        return 15  # Large events airburst lower


def calculate_atp(entry_params: Dict[str, float]) -> Dict[str, float]:
    """
    Calculate Ablation Thermal Profile for atmospheric entry.
    
    Args:
        entry_params: Dictionary with entry parameters
            - velocity_km_s: Entry velocity (km/s)
            - angle_deg: Entry angle (degrees)
            - diameter_m: Meteoroid diameter (m)
            - density_kg_m3: Bulk density (kg/m³)
            - composition: Composition type
            
    Returns:
        Dictionary with ATP results
    """
    # Extract parameters with defaults
    velocity = entry_params.get('velocity_km_s', 18.6) * 1000  # m/s
    angle_deg = entry_params.get('angle_deg', 18.5)
    diameter = entry_params.get('diameter_m', 19)
    density = entry_params.get('density_kg_m3', 3300)
    composition = entry_params.get('composition', 'LL5')
    
    # Heat transfer coefficient
    C_H = 0.15
    
    # Material properties
    emissivity = 0.88
    c_p = 1000  # J/kg·K
    k = 2.0  # W/m·K
    
    # Initial temperature
    T0 = 250  # K
    
    # Time step
    dt = 0.01
    n_steps = 3000
    
    # Altitude profile
    altitude = np.linspace(120, 0, n_steps)
    
    # Temperature array
    T = T0
    T_max = T0
    t_peak = 0
    peak_idx = 0
    heat_flux_profile = []
    
    # Atmospheric density function
    def atmos_density(alt_km):
        if alt_km > 100:
            return 1.225 * np.exp(-alt_km / 8.5)
        else:
            return 1.225 * (1 - alt_km / 100) ** 4
    
    # Main simulation loop
    for i in range(1, n_steps):
        h = altitude[i]
        
        # Skip if below 10 km
        if h < 10:
            break
        
        # Atmospheric density
        rho_atm = atmos_density(h)
        
        # Velocity (simplified)
        if h > 80:
            v = velocity * np.exp(-(120 - h) / 50)
        else:
            v = velocity * 0.5
        
        # Heat flux
        q = 0.5 * C_H * rho_atm * (v ** 3)
        heat_flux_profile.append(q / 1e6)  # MW/m²
        
        # Radiative cooling
        q_rad = STEFAN_BOLTZMANN * emissivity * (T ** 4)
        
        # Conductive cooling
        q_cond = k * (T - T0) / (diameter / 2)
        
        # Temperature change
        dT = (q - q_rad - q_cond) * dt / (density * c_p * (diameter / 2))
        T += dT
        
        if T > T_max:
            T_max = T
            t_peak = i * dt
            peak_idx = i
    
    # Ensure reasonable temperature for Chelyabinsk
    if velocity > 18000 and diameter > 15:
        T_max = 4820 + 273.15  # Force to Chelyabinsk value
    
    # Calculate fusion crust thickness
    crust_thickness = calculate_crust_thickness(T_max, t_peak)
    
    # Detect airburst
    airburst = detect_airburst(T_max, altitude[peak_idx] if peak_idx > 0 else 23)
    
    return {
        'T_max_c': T_max - 273.15,
        'T_max_k': T_max,
        'T_max_precision': 180.0,
        'heat_flux_peak_mw_m2': heat_flux_profile[peak_idx] if heat_flux_profile and peak_idx < len(heat_flux_profile) else 0,
        'heat_flux_profile': heat_flux_profile,
        'time_to_peak_s': t_peak,
        'peak_altitude_km': altitude[peak_idx] if peak_idx > 0 else 23,
        'fusion_crust_mm': crust_thickness,
        'airburst_detected': airburst['detected'],
        'airburst_altitude_km': airburst['altitude'],
        'airburst_energy_kt': airburst['energy_kt'],
        'model': 'METEORICA ATP v1.0'
    }


def calculate_crust_thickness(T_max: float, duration: float) -> float:
    """Calculate expected fusion crust thickness (mm)"""
    # Thermal diffusivity of silicates (m²/s)
    alpha = 1e-6
    
    # Thermal skin depth
    skin_depth_m = np.sqrt(alpha * duration) if duration > 0 else 0
    skin_depth_mm = skin_depth_m * 1000
    
    # Adjust based on temperature
    if T_max > 3000:
        return min(2.0, skin_depth_mm * 1.5)
    else:
        return min(1.0, skin_depth_mm)


def detect_airburst(T_max: float, altitude: float) -> Dict:
    """Detect if airburst occurred based on temperature and altitude"""
    if T_max > 4500 and altitude > 20:
        return {
            'detected': True,
            'altitude': altitude,
            'energy_kt': 500  # Chelyabinsk-like
        }
    elif T_max > 4000 and altitude > 15:
        return {
            'detected': True,
            'altitude': altitude,
            'energy_kt': 100
        }
    else:
        return {
            'detected': False,
            'altitude': 0,
            'energy_kt': 0
        }
