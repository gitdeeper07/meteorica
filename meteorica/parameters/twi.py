"""
Terrestrial Weathering Index (TWI)
5-indicator weathering index with terrestrial age estimation.
"""

import numpy as np
from typing import Dict, Optional


def calculate_twi(weathering_data: Dict[str, float]) -> float:
    """
    Calculate Terrestrial Weathering Index.
    
    TWI = 0.30·(metal oxidation) + 0.25·(phyllosilicate) + 
          0.20·(carbonate veins) + 0.15·(¹⁰Be/²¹Ne deviation) + 
          0.10·(Fe/Ni deviation)
    
    Args:
        weathering_data: Dictionary with weathering indicators
        
    Returns:
        TWI value in [0, 1]
    """
    metal_ox = weathering_data.get('metal_oxidation', 0)
    phyllo = weathering_data.get('phyllosilicate', 0)
    carbonate = weathering_data.get('carbonate_veins', 0)
    be_ne_dev = weathering_data.get('be_ne_deviation', 0)
    fe_ni_dev = weathering_data.get('fe_ni_deviation', 0)
    
    # Corrected weights from research paper
    twi = (0.30 * metal_ox + 
           0.25 * phyllo + 
           0.20 * carbonate + 
           0.15 * be_ne_dev + 
           0.10 * fe_ni_dev)
    
    return min(1.0, max(0.0, twi))


def estimate_terrestrial_age(twi: float) -> Dict[str, float]:
    """
    Estimate terrestrial age from TWI.
    
    Age_terrestrial = 12,400 · ln(1 + 3.7 · TWI) years
    
    Args:
        twi: Terrestrial Weathering Index
        
    Returns:
        Dictionary with age estimate and precision
    """
    # Corrected formula
    age = 12400 * np.log(1 + 3.7 * twi)
    precision = 8000  # ±8,000 years from research
    
    return {
        'age_years': age,
        'precision': precision,
        'age_min': max(0, age - precision),
        'age_max': age + precision
    }


def get_weathering_grade(twi: float) -> Dict[str, str]:
    """
    Get weathering grade classification from TWI.
    
    Args:
        twi: Terrestrial Weathering Index
        
    Returns:
        Dictionary with grade and description
    """
    if twi < 0.15:
        return {
            'grade': 'W0',
            'name': 'FRESH',
            'description': 'Negligible weathering. <500 years terrestrial age.',
            'color': '🟢'
        }
    elif twi < 0.30:
        return {
            'grade': 'W1',
            'name': 'MINOR',
            'description': 'Slight oxidation. 500-3,000 years.',
            'color': '🟡'
        }
    elif twi < 0.50:
        return {
            'grade': 'W2',
            'name': 'MODERATE',
            'description': 'Significant oxidation. 3,000-12,000 years.',
            'color': '🟠'
        }
    elif twi < 0.70:
        return {
            'grade': 'W3',
            'name': 'EXTENSIVE',
            'description': 'Major alteration. 12,000-30,000 years.',
            'color': '🔴'
        }
    else:
        return {
            'grade': 'W4/5',
            'name': 'SEVERE',
            'description': 'Pervasive alteration. >30,000 years.',
            'color': '⚫'
        }
