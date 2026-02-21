"""
Unit tests for Ablation Thermal Profile
"""

import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from meteorica.parameters.atp import calculate_atp, estimate_airburst


class TestATP(unittest.TestCase):
    """Test ATP calculations"""
    
    def test_calculate_atp(self):
        """Test ATP calculation"""
        # Chelyabinsk-like event
        params = {
            'velocity_km_s': 18.6,
            'angle_deg': 18.5,
            'diameter_m': 19,
            'density_kg_m3': 3300,
            'composition': 'LL5'
        }
        
        result = calculate_atp(params)
        
        # Check required fields
        self.assertIn('T_max_c', result)
        self.assertIn('T_max_k', result)
        self.assertIn('heat_flux_peak_mw_m2', result)
        self.assertIn('airburst_detected', result)
        
        # Temperature should be reasonable
        self.assertGreater(result['T_max_c'], 4000)
        self.assertLess(result['T_max_c'], 5500)
        
        # Check precision from research
        self.assertEqual(result['T_max_precision'], 180)
    
    def test_estimate_airburst(self):
        """Test airburst altitude estimation"""
        # Small event - surface impact
        alt = estimate_airburst(15000, 5, 3300)
        self.assertEqual(alt, 0)
        
        # Chelyabinsk-like
        alt = estimate_airburst(18600, 19, 3300)
        self.assertGreater(alt, 20)
        self.assertLess(alt, 30)
        
        # Large event
        alt = estimate_airburst(20000, 50, 3300)
        self.assertGreater(alt, 0)


if __name__ == '__main__':
    unittest.main()
