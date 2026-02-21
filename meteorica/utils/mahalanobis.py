"""
Mahalanobis distance utilities for MCC calculation.
"""

import numpy as np


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


def euclidean_distance(x: np.ndarray, centroid: np.ndarray) -> float:
    """Calculate Euclidean distance."""
    return np.sqrt(np.sum((x - centroid) ** 2))
