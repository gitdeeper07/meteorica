"""
Unit tests for Terrestrial Weathering Index
"""

import unittest
import sys
import os
import numpy as np
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from meteorica.parameters.twi import (
    calculate_twi, estimate_terrestrial_age, get_weathering_grade
)


class TestTWI(unittest.TestCase):
    """Test TWI calculations"""
    
    def test_calculate_twi(self):
        """Test TWI calculation"""
        # Fresh specimen
        fresh = {
            'metal_oxidation': 0.05,
            'phyllosilicate': 0.02,
            'carbonate_veins': 0.0,
            'be_ne_deviation': 0.01,
            'fe_ni_deviation': 0.01
        }
        twi = calculate_twi(fresh)
        # Calculate expected: 0.30*0.05 + 0.25*0.02 + 0.20*0 + 0.15*0.01 + 0.10*0.01
        # = 0.015 + 0.005 + 0 + 0.0015 + 0.001 = 0.0225
        self.assertAlmostEqual(twi, 0.0225, places=4)
        self.assertLess(twi, 0.15)
        
        # Weathered specimen
        weathered = {
            'metal_oxidation': 0.6,
            'phyllosilicate': 0.5,
            'carbonate_veins': 0.4,
            'be_ne_deviation': 0.3,
            'fe_ni_deviation': 0.2
        }
        twi = calculate_twi(weathered)
        # Calculate expected: 0.30*0.6 + 0.25*0.5 + 0.20*0.4 + 0.15*0.3 + 0.10*0.2
        # = 0.18 + 0.125 + 0.08 + 0.045 + 0.02 = 0.45
        self.assertAlmostEqual(twi, 0.45, places=2)
    
    def test_estimate_terrestrial_age(self):
        """Test terrestrial age estimation"""
        # Test with actual values from the formula
        test_cases = [
            (0.0225, 12400 * np.log(1 + 3.7 * 0.0225)),  # ~1000 years
            (0.1, 12400 * np.log(1 + 3.7 * 0.1)),        # ~3900 years
            (0.45, 12400 * np.log(1 + 3.7 * 0.45)),      # ~12400 years
        ]
        
        for twi, expected in test_cases:
            age = estimate_terrestrial_age(twi)
            self.assertAlmostEqual(age['age_years'], expected, delta=100)
            self.assertEqual(age['precision'], 8000)
    
    def test_weathering_grade_thresholds(self):
        """Test weathering grade thresholds from research paper"""
        test_cases = [
            (0.1, 'W0', 'FRESH'),
            (0.2, 'W1', 'MINOR'),
            (0.4, 'W2', 'MODERATE'),
            (0.6, 'W3', 'EXTENSIVE'),
            (0.8, 'W4/5', 'SEVERE'),
        ]
        
        for twi, expected_grade, expected_name in test_cases:
            grade = get_weathering_grade(twi)
            self.assertEqual(grade['grade'], expected_grade)
            self.assertEqual(grade['name'], expected_name)
    
    def test_weathering_grade_boundaries(self):
        """Test boundaries between weathering grades"""
        # At exact boundaries, should be the higher grade
        self.assertEqual(get_weathering_grade(0.15)['grade'], 'W1')
        self.assertEqual(get_weathering_grade(0.30)['grade'], 'W2')
        self.assertEqual(get_weathering_grade(0.50)['grade'], 'W3')
        self.assertEqual(get_weathering_grade(0.70)['grade'], 'W4/5')


if __name__ == '__main__':
    unittest.main()
