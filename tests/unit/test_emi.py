"""
Unit tests for EMI calculator
"""

import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from meteorica.emi import calculate_emi, normalize_parameter, CLASSIFICATION_LEVELS


class TestEMI(unittest.TestCase):
    """Test EMI calculation"""
    
    def test_normalize_parameter(self):
        """Test parameter normalization"""
        # Test within range
        result = normalize_parameter(0.5, 'mcc')
        self.assertAlmostEqual(result, 0.5)
        
        # Test below min
        result = normalize_parameter(-0.1, 'mcc')
        self.assertAlmostEqual(result, 0.0)
        
        # Test above max
        result = normalize_parameter(1.5, 'mcc')
        self.assertAlmostEqual(result, 1.0)
        
        # Test ATP temperature
        result = normalize_parameter(3000, 'atp')
        self.assertAlmostEqual(result, 0.5, places=2)
    
    def test_calculate_emi(self):
        """Test EMI calculation"""
        params = {
            'mcc': 0.85,
            'smg': 0.45,
            'twi': 0.25,
            'iaf': 0.78,
            'atp': 4820,
            'pbdr': 0.35,
            'cnea': 22.5
        }
        
        emi = calculate_emi(params)
        
        # EMI should be between 0 and 1
        self.assertGreaterEqual(emi, 0)
        self.assertLessEqual(emi, 1)
        
        # Test with missing parameter - should not raise error now
        emi2 = calculate_emi({'mcc': 0.5})
        self.assertGreaterEqual(emi2, 0)
    
    def test_classification_levels(self):
        """Test classification levels"""
        self.assertEqual(len(CLASSIFICATION_LEVELS), 5)
        
        # Test each level exists
        levels = [level['name'] for level in CLASSIFICATION_LEVELS]
        expected = ['UNAMBIGUOUS', 'HIGH CONFIDENCE', 'BOUNDARY ZONE', 
                   'ANOMALOUS', 'UNGROUPED CANDIDATE']
        self.assertEqual(levels, expected)


if __name__ == '__main__':
    unittest.main()
