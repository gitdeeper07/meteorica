"""
Unit tests for Shock Metamorphism Grade
"""

import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from meteorica.parameters.smg import (
    calculate_smg, get_shock_stage, calculate_post_shock_temperature
)


class TestSMG(unittest.TestCase):
    """Test SMG calculations"""
    
    def test_calculate_smg(self):
        """Test SMG calculation"""
        # Unshocked (S1)
        unshocked = {
            'olivine_planar': 0.05,
            'feldspar_state': 0.05,
            'metal_melting': 0.0,
            'high_pressure_phases': 0.0,
            'sulfide_state': 0.05,
            'porosity': 0.95
        }
        result = calculate_smg(unshocked)
        self.assertLess(result['smg'], 0.1)
        self.assertEqual(result['shock_stage'], 'S1')
        
        # Moderately shocked (S4)
        moderate = {
            'olivine_planar': 0.5,
            'feldspar_state': 0.5,
            'metal_melting': 0.4,
            'high_pressure_phases': 0.3,
            'sulfide_state': 0.4,
            'porosity': 0.6
        }
        result = calculate_smg(moderate)
        self.assertGreater(result['smg'], 0.3)
        self.assertLess(result['smg'], 0.7)
        
        # Strongly shocked (S5)
        shocked = {
            'olivine_planar': 0.75,
            'feldspar_state': 0.7,
            'metal_melting': 0.6,
            'high_pressure_phases': 0.5,
            'sulfide_state': 0.6,
            'porosity': 0.3
        }
        result = calculate_smg(shocked)
        self.assertGreater(result['smg'], 0.4)
        self.assertIn('S', result['shock_stage'])
        
        # Partial data
        partial = {'olivine_planar': 0.5}
        result = calculate_smg(partial)
        self.assertIn('smg', result)
    
    def test_get_shock_stage(self):
        """Test shock stage from pressure"""
        self.assertEqual(get_shock_stage(4), 'S1')
        self.assertEqual(get_shock_stage(7), 'S2')
        self.assertEqual(get_shock_stage(15), 'S3')
        self.assertEqual(get_shock_stage(25), 'S4')
        self.assertEqual(get_shock_stage(45), 'S5')
        self.assertEqual(get_shock_stage(60), 'S6')
    
    def test_post_shock_temperature(self):
        """Test post-shock temperature calculation"""
        T = calculate_post_shock_temperature(300, 50e9, 0.001, 1000, 3300)
        self.assertGreater(T, 300)


if __name__ == '__main__':
    unittest.main()
