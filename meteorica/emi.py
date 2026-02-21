"""
Extraterrestrial Material Index (EMI) calculator.
Combines seven parameters into a unified classification metric.
"""

from typing import Dict, Optional, Tuple, Any
import numpy as np

# Default weights from the METEORICA framework
DEFAULT_WEIGHTS = {
    'mcc': 0.26,   # Mineralogical Classification Coefficient
    'smg': 0.19,   # Shock Metamorphism Grade
    'twi': 0.18,   # Terrestrial Weathering Index
    'iaf': 0.17,   # Isotopic Anomaly Fingerprint
    'atp': 0.10,   # Ablation Thermal Profile
    'pbdr': 0.06,  # Parent Body Differentiation Ratio
    'cnea': 0.04,  # Cosmogenic Nuclide Exposure Age
}

# Critical thresholds for normalization
CRITICAL_THRESHOLDS = {
    'mcc': {'min': 0.0, 'max': 1.0},
    'smg': {'min': 0.0, 'max': 1.0},
    'twi': {'min': 0.0, 'max': 1.0},
    'iaf': {'min': 0.0, 'max': 1.0},
    'atp': {'min': 0.0, 'max': 6000.0},  # Temperature in °C
    'pbdr': {'min': 0.0, 'max': 1.0},
    'cnea': {'min': 0.0, 'max': 100.0},  # Age in Ma
}

# EMI classification levels
CLASSIFICATION_LEVELS = [
    {'name': 'UNAMBIGUOUS', 'range': (0.0, 0.20), 'color': '🟢', 
     'action': 'Direct MetBull submission'},
    {'name': 'HIGH CONFIDENCE', 'range': (0.20, 0.40), 'color': '🟡', 
     'action': 'Standard expert review'},
    {'name': 'BOUNDARY ZONE', 'range': (0.40, 0.60), 'color': '🟠', 
     'action': 'Multi-parameter disambiguation required'},
    {'name': 'ANOMALOUS', 'range': (0.60, 0.80), 'color': '🔴', 
     'action': 'Expert committee + isotopic verification'},
    {'name': 'UNGROUPED CANDIDATE', 'range': (0.80, 1.01), 'color': '⚫', 
     'action': 'Full consortium characterization'},
]


class Specimen:
    """Represents a meteorite specimen with its analytical data."""
    
    def __init__(self, data: Dict[str, Any]):
        self.data = data
    
    @classmethod
    def from_epma(cls, filepath: str):
        """Load specimen data from EPMA analysis file."""
        # TODO: Implement loading from file
        return cls({})
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Create specimen from dictionary."""
        return cls(data)


class Fireball:
    """Represents a fireball event for ATP calculation."""
    
    def __init__(self, velocity_km_s: float, angle_deg: float, 
                 diameter_m: float, composition: str):
        self.velocity_km_s = velocity_km_s
        self.angle_deg = angle_deg
        self.diameter_m = diameter_m
        self.composition = composition
    
    def to_dict(self):
        """Convert to dictionary for ATP calculation."""
        return {
            'velocity_km_s': self.velocity_km_s,
            'angle_deg': self.angle_deg,
            'diameter_m': self.diameter_m,
            'composition': self.composition
        }


def normalize_parameter(value: float, param_name: str, 
                        thresholds: Optional[Dict] = None) -> float:
    """
    Normalize a parameter value to [0, 1] range based on critical thresholds.
    
    Args:
        value: Raw parameter value
        param_name: Parameter name (mcc, smg, etc.)
        thresholds: Optional custom thresholds
        
    Returns:
        Normalized value in [0, 1]
    """
    if thresholds is None:
        thresholds = CRITICAL_THRESHOLDS
    
    if param_name not in thresholds:
        raise ValueError(f"Unknown parameter: {param_name}")
    
    t = thresholds[param_name]
    
    # Clip to bounds
    clipped = np.clip(value, t['min'], t['max'])
    
    # Normalize
    if t['max'] == t['min']:
        return 0.5  # Avoid division by zero
    return (clipped - t['min']) / (t['max'] - t['min'])


def calculate_emi(parameters: Dict[str, float], 
                  weights: Optional[Dict[str, float]] = None,
                  thresholds: Optional[Dict] = None) -> float:
    """
    Calculate Extraterrestrial Material Index (EMI).
    
    EMI = Σ(weight_i * P_i_norm)
    
    Args:
        parameters: Dictionary of parameter values
        weights: Optional custom weights (uses defaults if None)
        thresholds: Optional custom thresholds
        
    Returns:
        EMI score in [0, 1]
    """
    if weights is None:
        weights = DEFAULT_WEIGHTS
    
    # Use only parameters that exist in the input
    available_params = {}
    missing_params = []
    
    for param in weights.keys():
        if param in parameters:
            available_params[param] = parameters[param]
        else:
            missing_params.append(param)
    
    # If no parameters, return 0
    if not available_params:
        return 0.0
    
    # Calculate weighted sum with available parameters
    total_weight = 0.0
    weighted_sum = 0.0
    
    for param, value in available_params.items():
        weight = weights[param]
        norm_val = normalize_parameter(value, param, thresholds)
        weighted_sum += weight * norm_val
        total_weight += weight
    
    # Normalize by total weight used
    if total_weight > 0:
        emi = weighted_sum / total_weight
    else:
        emi = 0.0
    
    return emi


def classify(specimen: Specimen) -> Dict[str, Any]:
    """
    Run full EMI pipeline on a specimen.
    
    Args:
        specimen: Specimen object with analytical data
        
    Returns:
        Dictionary with classification results
    """
    # TODO: Implement full classification pipeline
    # This will call all seven parameter calculators
    
    result = {
        'emi': 0.0,
        'group': 'Unknown',
        'confidence': 0.0,
        'mcc': 0.0,
        'smg': 0.0,
        'twi': 0.0,
        'iaf': 0.0,
        'atp': 0.0,
        'pbdr': 0.0,
        'cnea': 0.0,
        'terrestrial_age_years': 0,
        'cre_age_ma': 0.0,
        'parent_body_radius_km': 0.0
    }
    
    return result


def calculate_atp(fireball: Fireball) -> Dict[str, float]:
    """
    Calculate Ablation Thermal Profile for a fireball event.
    
    Args:
        fireball: Fireball object with entry parameters
        
    Returns:
        Dictionary with ATP results including T_max
    """
    # Import here to avoid circular imports
    from meteorica.parameters.atp import calculate_atp as calculate_atp_func
    
    return calculate_atp_func(fireball.to_dict())
