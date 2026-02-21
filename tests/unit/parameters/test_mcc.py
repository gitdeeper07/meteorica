"""
Unit tests for Mineralogical Classification Coefficient
"""

import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from meteorica.parameters.mcc import calculate_mcc, mahalanobis_distance
import numpy as np


class TestMCC(unittest.TestCase):
    """Test MCC calculations"""
    
    def test_mahalanobis_distance(self):
        """Test Mahalanobis distance calculation"""
        x = np.array([18.5, 16.5, 0.75])
        centroid = np.array([18.5, 16.5, 0.75])
        cov = np.eye(3)
        
        # Same point should have distance 0
        dist = mahalanobis_distance(x, centroid, cov)
        self.assertAlmostEqual(dist, 0.0)
        
        # Different point should have positive distance
        x2 = np.array([20.0, 18.0, 0.8])
        dist2 = mahalanobis_distance(x2, centroid, cov)
        self.assertGreater(dist2, 0)
    
    def test_calculate_mcc_stony(self):
        """Test MCC for stony meteorites"""
        # H chondrite
        h_data = {'fa': 18.5, 'fs': 16.5, 'd17O': 0.75}
        result = calculate_mcc(h_data)
        
        self.assertIn('mcc', result)
        self.assertIn('group', result)
        self.assertGreater(result['mcc'], 0.8)
        self.assertEqual(result['group'], 'H')
        
        # L chondrite
        l_data = {'fa': 24.5, 'fs': 21.0, 'd17O': 1.05}
        result = calculate_mcc(l_data)
        self.assertEqual(result['group'], 'L')
        
        # LL chondrite
        ll_data = {'fa': 29.0, 'fs': 24.5, 'd17O': 1.25}
        result = calculate_mcc(ll_data)
        self.assertEqual(result['group'], 'LL')
    
    def test_calculate_mcc_iron(self):
        """Test MCC for iron meteorites"""
        # IAB iron
        iron_data = {'ni': 8.5}
        result = calculate_mcc(iron_data)
        self.assertEqual(result['group'], 'IAB')
        
        # IVB iron
        iron_data = {'ni': 16.5}
        result = calculate_mcc(iron_data)
        self.assertEqual(result['group'], 'IVB')
    
    def test_boundary_zone(self):
        """Test boundary zone specimens"""
        # Between H and L
        boundary = {'fa': 21.5, 'fs': 19.0, 'd17O': 0.9}
        result = calculate_mcc(boundary)
        
        # MCC should be lower for boundary specimens
        self.assertLess(result['mcc'], 0.9)


if __name__ == '__main__':
    unittest.main()
