"""
Mineralogical Classification Coefficient (MCC)
Based on Mahalanobis distance in mineral phase space.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional

# Group centroids for major meteorite groups
# Format: {group_name: {'fa': olivine Fa mol%, 'fs': pyroxene Fs mol%, 
#                       'd17O': Δ¹⁷O permil, 'ni': Ni wt% (for irons)}}
GROUP_CENTROIDS = {
    # Ordinary chondrites
    'H': {'fa': 18.5, 'fs': 16.5, 'd17O': 0.75, 'ni': None},
    'L': {'fa': 24.5, 'fs': 21.0, 'd17O': 1.05, 'ni': None},
    'LL': {'fa': 29.0, 'fs': 24.5, 'd17O': 1.25, 'ni': None},
    
    # Carbonaceous chondrites
    'CI': {'fa': None, 'fs': None, 'd17O': -2.5, 'ni': None},
    'CM': {'fa': None, 'fs': None, 'd17O': -3.0, 'ni': None},
    'CO': {'fa': 12.0, 'fs': 3.5, 'd17O': -4.5, 'ni': None},
    'CV': {'fa': 8.5, 'fs': 2.0, 'd17O': -3.8, 'ni': None},
    'CR': {'fa': 3.5, 'fs': 2.0, 'd17O': -1.5, 'ni': None},
    
    # Iron meteorites (Ni content)
    'IAB': {'fa': None, 'fs': None, 'd17O': None, 'ni': 8.5},
    'IIAB': {'fa': None, 'fs': None, 'd17O': None, 'ni': 5.6},
    'IIIAB': {'fa': None, 'fs': None, 'd17O': None, 'ni': 8.2},
    'IVA': {'fa': None, 'fs': None, 'd17O': None, 'ni': 8.0},
    'IVB': {'fa': None, 'fs': None, 'd17O': None, 'ni': 16.5},
}

# Covariance matrices for each group (simplified)
# In reality, these would be calculated from reference datasets
GROUP_COVARIANCES = {
    'H': np.array([[2.5, 1.2, 0.1], [1.2, 2.3, 0.08], [0.1, 0.08, 0.04]]),
    'L': np.array([[2.8, 1.4, 0.12], [1.4, 2.6, 0.1], [0.12, 0.1, 0.05]]),
    'LL': np.array([[3.0, 1.5, 0.15], [1.5, 2.8, 0.12], [0.15, 0.12, 0.06]]),
}


def mahalanobis_distance(x: np.ndarray, centroid: np.ndarray, 
                         cov: np.ndarray) -> float:
    """
    Calculate Mahalanobis distance between observation and centroid.
    
    d = sqrt((x - μ)ᵀ Σ⁻¹ (x - μ))
    
    Args:
        x: Observation vector
        centroid: Group centroid vector
        cov: Covariance matrix
        
    Returns:
        Mahalanobis distance
    """
    diff = x - centroid
    try:
        inv_cov = np.linalg.inv(cov)
        distance = np.sqrt(np.dot(np.dot(diff, inv_cov), diff))
        return distance
    except np.linalg.LinAlgError:
        # If covariance matrix is singular, use Euclidean distance
        return np.sqrt(np.sum(diff ** 2))


def calculate_mcc(mineral_data: Dict[str, float], 
                  group: Optional[str] = None) -> Dict[str, any]:
    """
    Calculate Mineralogical Classification Coefficient.
    
    MCC = 1 − d(P_obs, P_centroid) / d_max
    
    Args:
        mineral_data: Dictionary with mineral composition
        group: Optional specific group to test against
        
    Returns:
        Dictionary with MCC value and nearest group
    """
    # Extract relevant parameters based on meteorite type
    # For ordinary chondrites: Fa, Fs, Δ¹⁷O
    # For irons: Ni
    
    if 'ni' in mineral_data and mineral_data['ni'] is not None:
        # Iron meteorite
        return _calculate_mcc_iron(mineral_data, group)
    else:
        # Stony meteorite
        return _calculate_mcc_stony(mineral_data, group)


def _calculate_mcc_stony(mineral_data: Dict[str, float], 
                         group: Optional[str] = None) -> Dict[str, any]:
    """Calculate MCC for stony meteorites."""
    
    # Build observation vector
    obs = np.array([
        mineral_data.get('fa', 0),
        mineral_data.get('fs', 0),
        mineral_data.get('d17O', 0)
    ])
    
    min_distance = float('inf')
    best_group = None
    best_centroid = None
    
    # Test against relevant groups
    for g, centroid_data in GROUP_CENTROIDS.items():
        if centroid_data['fa'] is None:
            continue  # Skip iron groups
            
        centroid = np.array([
            centroid_data['fa'],
            centroid_data['fs'],
            centroid_data['d17O']
        ])
        
        # Get covariance for this group (use default if not available)
        cov = GROUP_COVARIANCES.get(g, np.eye(3) * 2.0)
        
        distance = mahalanobis_distance(obs, centroid, cov)
        
        if distance < min_distance:
            min_distance = distance
            best_group = g
            best_centroid = centroid
    
    # Calculate MCC
    d_max = 5.0  # Maximum tolerable distance (calibrated from research)
    mcc = max(0, 1 - (min_distance / d_max))
    
    return {
        'mcc': mcc,
        'group': best_group,
        'distance': min_distance,
        'centroid': best_centroid.tolist() if best_centroid is not None else None
    }


def _calculate_mcc_iron(mineral_data: Dict[str, float], 
                        group: Optional[str] = None) -> Dict[str, any]:
    """Calculate MCC for iron meteorites."""
    
    ni_content = mineral_data.get('ni', 0)
    
    min_distance = float('inf')
    best_group = None
    
    # Test against iron groups
    for g, centroid_data in GROUP_CENTROIDS.items():
        if centroid_data['ni'] is None:
            continue  # Skip stony groups
            
        distance = abs(ni_content - centroid_data['ni'])
        
        if distance < min_distance:
            min_distance = distance
            best_group = g
    
    # Calculate MCC for irons (simplified)
    d_max = 5.0  # wt% Ni
    mcc = max(0, 1 - (min_distance / d_max))
    
    return {
        'mcc': mcc,
        'group': best_group,
        'distance': min_distance,
        'ni_content': ni_content
    }
