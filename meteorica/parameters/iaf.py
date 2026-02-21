"""
Isotopic Anomaly Fingerprint (IAF)
7-dimensional nucleosynthetic space for group discrimination.
"""

import numpy as np
from typing import Dict, List, Optional, Tuple

# Group centroids in 7D isotope space
# Format: (ε⁵⁰Ti, ε⁵⁴Cr, ε⁹⁶Mo, ε¹⁰⁰Mo, ε⁹²Ru, ε¹³⁷Ba, ε¹⁴²Nd)
GROUP_ISOTOPE_CENTROIDS = {
    'CI': np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
    'CM': np.array([1.2, 0.88, -0.3, -0.2, 0.1, -0.1, 0.0]),
    'CR': np.array([2.1, 1.53, -0.8, -0.5, 0.3, -0.2, -0.1]),
    'CO': np.array([1.8, 1.20, -0.5, -0.3, 0.2, -0.15, -0.05]),
    'CV': np.array([1.5, 1.05, -0.4, -0.25, 0.15, -0.12, -0.03]),
    'H': np.array([0.5, 0.3, 0.1, 0.05, 0.02, 0.01, 0.0]),
    'L': np.array([0.6, 0.4, 0.15, 0.08, 0.03, 0.02, 0.0]),
    'LL': np.array([0.7, 0.5, 0.2, 0.1, 0.04, 0.03, 0.0]),
    'EH': np.array([-0.2, -0.1, 0.0, 0.0, 0.0, 0.0, 0.0]),
    'EL': np.array([-0.15, -0.05, 0.0, 0.0, 0.0, 0.0, 0.0]),
}

# Intra-group dispersion (sigma) for each group
GROUP_DISPERSION = {
    'CI': 0.5,
    'CM': 0.6,
    'CR': 0.7,
    'CO': 0.6,
    'CV': 0.6,
    'H': 0.4,
    'L': 0.4,
    'LL': 0.4,
    'EH': 0.3,
    'EL': 0.3,
}

# Isotope names for reference
ISOTOPE_NAMES = [
    'ε⁵⁰Ti',
    'ε⁵⁴Cr',
    'ε⁹⁶Mo',
    'ε¹⁰⁰Mo',
    'ε⁹²Ru',
    'ε¹³⁷Ba',
    'ε¹⁴²Nd'
]


def calculate_iaf(isotope_data: Dict[str, float]) -> Dict[str, any]:
    """
    Calculate Isotopic Anomaly Fingerprint.
    
    IAF = exp(−d_iso² / 2σ²_group)
    
    Args:
        isotope_data: Dictionary with isotope anomalies (ε units)
        
    Returns:
        Dictionary with IAF value and nearest group
    """
    # Build observation vector in correct order
    obs = np.array([
        isotope_data.get('ε⁵⁰Ti', 0),
        isotope_data.get('ε⁵⁴Cr', 0),
        isotope_data.get('ε⁹⁶Mo', 0),
        isotope_data.get('ε¹⁰⁰Mo', 0),
        isotope_data.get('ε⁹²Ru', 0),
        isotope_data.get('ε¹³⁷Ba', 0),
        isotope_data.get('ε¹⁴²Nd', 0),
    ])
    
    min_distance = float('inf')
    best_group = None
    best_centroid = None
    all_distances = {}
    
    # Calculate distance to each group centroid
    for group, centroid in GROUP_ISOTOPE_CENTROIDS.items():
        # Euclidean distance in isotope space
        distance = np.sqrt(np.sum((obs - centroid) ** 2))
        all_distances[group] = distance
        
        if distance < min_distance:
            min_distance = distance
            best_group = group
            best_centroid = centroid
    
    # Get dispersion for best group
    sigma = GROUP_DISPERSION.get(best_group, 0.5)
    
    # Calculate IAF
    iaf = np.exp(-(min_distance ** 2) / (2 * sigma ** 2))
    
    # Check if outlier
    is_outlier = iaf < 0.3
    
    return {
        'iaf': iaf,
        'group': best_group,
        'distance': min_distance,
        'sigma': sigma,
        'is_outlier': is_outlier,
        'all_distances': all_distances,
        'centroid': best_centroid.tolist() if best_centroid is not None else None
    }


def detect_presolar_grains(isotope_data: Dict[str, float], 
                          threshold: float = 0.3) -> Dict[str, any]:
    """
    Detect potential presolar grain signatures.
    
    Args:
        isotope_data: Dictionary with isotope anomalies
        threshold: IAF threshold for outlier detection
        
    Returns:
        Dictionary with detection results
    """
    iaf_result = calculate_iaf(isotope_data)
    
    if iaf_result['is_outlier']:
        # This could be a presolar grain signature
        return {
            'presolar_detected': True,
            'iaf': iaf_result['iaf'],
            'nearest_group': iaf_result['group'],
            'confidence': 1.0 - iaf_result['iaf'],
            'recommendation': 'NanoSIMS analysis recommended'
        }
    else:
        return {
            'presolar_detected': False,
            'iaf': iaf_result['iaf'],
            'nearest_group': iaf_result['group'],
            'confidence': iaf_result['iaf']
        }
