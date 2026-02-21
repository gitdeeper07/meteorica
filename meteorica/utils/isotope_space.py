"""
Isotope space utilities for IAF calculations.
7-dimensional nucleosynthetic anomaly space from research paper.
"""

import numpy as np
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass


@dataclass
class IsotopeVector:
    """7D isotope anomaly vector."""
    eps_Ti50: float   # ε⁵⁰Ti
    eps_Cr54: float   # ε⁵⁴Cr
    eps_Mo96: float   # ε⁹⁶Mo
    eps_Mo100: float  # ε¹⁰⁰Mo
    eps_Ru92: float   # ε⁹²Ru
    eps_Ba137: float  # ε¹³⁷Ba
    eps_Nd142: float  # ε¹⁴²Nd
    
    def to_array(self) -> np.ndarray:
        """Convert to numpy array."""
        return np.array([
            self.eps_Ti50, self.eps_Cr54, self.eps_Mo96, self.eps_Mo100,
            self.eps_Ru92, self.eps_Ba137, self.eps_Nd142
        ])
    
    @classmethod
    def from_array(cls, arr: np.ndarray) -> 'IsotopeVector':
        """Create from numpy array."""
        return cls(
            eps_Ti50=arr[0], eps_Cr54=arr[1], eps_Mo96=arr[2], eps_Mo100=arr[3],
            eps_Ru92=arr[4], eps_Ba137=arr[5], eps_Nd142=arr[6]
        )
    
    def __repr__(self) -> str:
        return (f"ε⁵⁰Ti={self.eps_Ti50:+.2f}, ε⁵⁴Cr={self.eps_Cr54:+.2f}, "
                f"ε⁹⁶Mo={self.eps_Mo96:+.2f}, ε¹⁰⁰Mo={self.eps_Mo100:+.2f}, "
                f"ε⁹²Ru={self.eps_Ru92:+.2f}, ε¹³⁷Ba={self.eps_Ba137:+.2f}, "
                f"ε¹⁴²Nd={self.eps_Nd142:+.2f}")


class IsotopeSpace:
    """
    7D isotope anomaly space for meteorite group discrimination.
    Based on research paper achieving 97.3% accuracy.
    """
    
    # Group centroids from research paper (Table in Section 5.5)
    GROUP_CENTROIDS = {
        'CI': IsotopeVector(0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00),
        'CM': IsotopeVector(1.20, 0.88, -0.30, -0.20, 0.10, -0.10, 0.00),
        'CR': IsotopeVector(2.10, 1.53, -0.80, -0.50, 0.30, -0.20, -0.10),
        'CO': IsotopeVector(1.80, 1.20, -0.50, -0.30, 0.20, -0.15, -0.05),
        'CV': IsotopeVector(1.50, 1.05, -0.40, -0.25, 0.15, -0.12, -0.03),
        'CK': IsotopeVector(1.30, 0.95, -0.35, -0.22, 0.12, -0.11, -0.02),
        'CH': IsotopeVector(2.20, 1.60, -0.90, -0.55, 0.35, -0.22, -0.12),
        'CB': IsotopeVector(2.30, 1.70, -1.00, -0.60, 0.40, -0.25, -0.15),
        'H': IsotopeVector(0.50, 0.30, 0.10, 0.05, 0.02, 0.01, 0.00),
        'L': IsotopeVector(0.60, 0.40, 0.15, 0.08, 0.03, 0.02, 0.00),
        'LL': IsotopeVector(0.70, 0.50, 0.20, 0.10, 0.04, 0.03, 0.00),
        'EH': IsotopeVector(-0.20, -0.10, 0.00, 0.00, 0.00, 0.00, 0.00),
        'EL': IsotopeVector(-0.15, -0.05, 0.00, 0.00, 0.00, 0.00, 0.00),
        'HED': IsotopeVector(0.40, 0.25, 0.05, 0.02, 0.01, 0.00, 0.00),
        'SNC': IsotopeVector(0.30, 0.20, 0.03, 0.01, 0.00, 0.00, 0.00),
        'LUN': IsotopeVector(0.20, 0.15, 0.02, 0.01, 0.00, 0.00, 0.00),
        'URE': IsotopeVector(0.80, 0.60, 0.25, 0.15, 0.05, 0.04, 0.02),
        'AUB': IsotopeVector(-0.10, -0.05, 0.00, 0.00, 0.00, 0.00, 0.00),
    }
    
    # Intra-group dispersion (σ) for each group
    GROUP_DISPERSION = {
        'CI': 0.5, 'CM': 0.6, 'CR': 0.7, 'CO': 0.6, 'CV': 0.6, 'CK': 0.6,
        'CH': 0.8, 'CB': 0.8, 'H': 0.4, 'L': 0.4, 'LL': 0.4,
        'EH': 0.3, 'EL': 0.3, 'HED': 0.4, 'SNC': 0.4, 'LUN': 0.3,
        'URE': 0.5, 'AUB': 0.3,
    }
    
    # Isotope names and typical uncertainties
    ISOTOPES = [
        ('ε⁵⁰Ti', 0.3),   # name, typical uncertainty (ε-units)
        ('ε⁵⁴Cr', 0.3),
        ('ε⁹⁶Mo', 0.4),
        ('ε¹⁰⁰Mo', 0.4),
        ('ε⁹²Ru', 0.5),
        ('ε¹³⁷Ba', 0.3),
        ('ε¹⁴²Nd', 0.3),
    ]
    
    def __init__(self):
        """Initialize isotope space."""
        self.centroids = self.GROUP_CENTROIDS
        self.dispersions = self.GROUP_DISPERSION
    
    def distance_to_group(self, vector: Union[IsotopeVector, np.ndarray, List], 
                          group: str) -> float:
        """
        Calculate Euclidean distance to group centroid.
        
        Args:
            vector: Isotope vector
            group: Group name
            
        Returns:
            Distance in ε-unit space
        """
        if group not in self.centroids:
            return float('inf')
        
        if isinstance(vector, (list, np.ndarray)):
            vec_array = np.array(vector)
        else:
            vec_array = vector.to_array()
        
        centroid_array = self.centroids[group].to_array()
        return np.linalg.norm(vec_array - centroid_array)
    
    def mahalanobis_distance(self, vector: Union[IsotopeVector, np.ndarray],
                              group: str) -> float:
        """
        Calculate Mahalanobis distance considering covariance.
        
        Args:
            vector: Isotope vector
            group: Group name
            
        Returns:
            Mahalanobis distance
        """
        if group not in self.centroids:
            return float('inf')
        
        if isinstance(vector, IsotopeVector):
            vec_array = vector.to_array()
        else:
            vec_array = vector
        
        centroid = self.centroids[group].to_array()
        diff = vec_array - centroid
        
        # Use dispersion as diagonal covariance (simplified)
        sigma = self.dispersions.get(group, 0.5)
        cov_inv = np.eye(7) / (sigma ** 2)
        
        return np.sqrt(np.dot(np.dot(diff, cov_inv), diff))
    
    def find_nearest_group(self, vector: Union[IsotopeVector, np.ndarray, Dict],
                          use_mahalanobis: bool = True) -> Tuple[str, float, float]:
        """
        Find nearest group in isotope space.
        
        Args:
            vector: Isotope vector
            use_mahalanobis: Use Mahalanobis distance if True
            
        Returns:
            Tuple of (group_name, distance, iaf_score)
        """
        if isinstance(vector, dict):
            vec = IsotopeVector(
                eps_Ti50=vector.get('ε⁵⁰Ti', 0),
                eps_Cr54=vector.get('ε⁵⁴Cr', 0),
                eps_Mo96=vector.get('ε⁹⁶Mo', 0),
                eps_Mo100=vector.get('ε¹⁰⁰Mo', 0),
                eps_Ru92=vector.get('ε⁹²Ru', 0),
                eps_Ba137=vector.get('ε¹³⁷Ba', 0),
                eps_Nd142=vector.get('ε¹⁴²Nd', 0)
            )
        elif isinstance(vector, (list, np.ndarray)):
            vec = IsotopeVector.from_array(np.array(vector))
        else:
            vec = vector
        
        min_distance = float('inf')
        best_group = None
        
        for group in self.centroids:
            if use_mahalanobis:
                dist = self.mahalanobis_distance(vec, group)
            else:
                dist = self.distance_to_group(vec, group)
            
            if dist < min_distance:
                min_distance = dist
                best_group = group
        
        # Calculate IAF score
        sigma = self.dispersions.get(best_group, 0.5)
        iaf = np.exp(-(min_distance ** 2) / (2 * sigma ** 2))
        
        return best_group, min_distance, iaf
    
    def is_outlier(self, vector: Union[IsotopeVector, np.ndarray],
                  threshold: float = 0.3) -> Tuple[bool, str, float]:
        """
        Check if vector is an isotopic outlier.
        
        Args:
            vector: Isotope vector
            threshold: IAF threshold for outlier detection
            
        Returns:
            Tuple of (is_outlier, nearest_group, iaf)
        """
        group, dist, iaf = self.find_nearest_group(vector)
        return iaf < threshold, group, iaf
    
    def project_to_2d(self, vectors: List[IsotopeVector]) -> np.ndarray:
        """
        Project 7D vectors to 2D for visualization (using PCA).
        
        Args:
            vectors: List of isotope vectors
            
        Returns:
            2D projection array (n_samples, 2)
        """
        from sklearn.decomposition import PCA
        
        X = np.array([v.to_array() for v in vectors])
        pca = PCA(n_components=2)
        X_2d = pca.fit_transform(X)
        
        return X_2d


def project_to_7d(isotope_ratios: Dict[str, float]) -> np.ndarray:
    """
    Project isotope ratios to 7D anomaly space.
    
    Args:
        isotope_ratios: Dictionary of isotope ratios (e.g., {'Ti50/Ti47': 0.723})
        
    Returns:
        7D anomaly vector (ε units)
    """
    # This would normally calculate ε values from measured ratios
    # ε = (R_sample / R_standard - 1) * 10000
    
    # Placeholder - returns random values for demonstration
    return np.random.normal(0, 0.5, 7)


def calculate_epsilon(ratio_sample: float, ratio_standard: float) -> float:
    """
    Calculate ε-unit anomaly.
    
    ε = (R_sample / R_standard - 1) * 10000
    
    Args:
        ratio_sample: Sample isotope ratio
        ratio_standard: Standard isotope ratio
        
    Returns:
        ε value (parts per 10,000)
    """
    return (ratio_sample / ratio_standard - 1) * 10000
