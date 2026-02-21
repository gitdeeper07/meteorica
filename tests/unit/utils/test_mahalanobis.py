"""
Unit tests for Mahalanobis distance utilities
"""

import unittest
import sys
import os
import numpy as np
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from meteorica.utils.mahalanobis import mahalanobis_distance, euclidean_distance


class TestMahalanobis(unittest.TestCase):
    """Test distance calculations"""
    
    def test_mahalanobis_distance(self):
        """Test Mahalanobis distance"""
        x = np.array([1, 2, 3])
        centroid = np.array([1, 2, 3])
        cov = np.eye(3)
        
        # Same point
        dist = mahalanobis_distance(x, centroid, cov)
        self.assertAlmostEqual(dist, 0.0)
        
        # Different point
        x2 = np.array([2, 3, 4])
        dist = mahalanobis_distance(x2, centroid, cov)
        self.assertGreater(dist, 0)
        
        # With covariance
        cov2 = np.array([[2, 0, 0], [0, 2, 0], [0, 0, 2]])
        dist = mahalanobis_distance(x2, centroid, cov2)
        self.assertGreater(dist, 0)
    
    def test_euclidean_distance(self):
        """Test Euclidean distance"""
        x = np.array([1, 2, 3])
        centroid = np.array([1, 2, 3])
        
        dist = euclidean_distance(x, centroid)
        self.assertAlmostEqual(dist, 0.0)
        
        x2 = np.array([2, 3, 4])
        dist = euclidean_distance(x2, centroid)
        self.assertAlmostEqual(dist, np.sqrt(3))


if __name__ == '__main__':
    unittest.main()
