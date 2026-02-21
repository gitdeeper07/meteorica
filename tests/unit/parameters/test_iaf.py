"""
Unit tests for Isotopic Anomaly Fingerprint
"""

import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from meteorica.parameters.iaf import calculate_iaf, detect_presolar_grains


class TestIAF(unittest.TestCase):
    """Test IAF calculations"""
    
    def test_calculate_iaf(self):
        """Test IAF calculation"""
        # CI chondrite (solar)
        ci_data = {
            'ε⁵⁰Ti': 0.0,
            'ε⁵⁴Cr': 0.0,
            'ε⁹⁶Mo': 0.0,
            'ε¹⁰⁰Mo': 0.0,
            'ε⁹²Ru': 0.0,
            'ε¹³⁷Ba': 0.0,
            'ε¹⁴²Nd': 0.0
        }
        result = calculate_iaf(ci_data)
        self.assertEqual(result['group'], 'CI')
        self.assertGreater(result['iaf'], 0.9)
        
        # CM chondrite
        cm_data = {
            'ε⁵⁰Ti': 1.2,
            'ε⁵⁴Cr': 0.88,
            'ε⁹⁶Mo': -0.3,
            'ε¹⁰⁰Mo': -0.2,
            'ε⁹²Ru': 0.1,
            'ε¹³⁷Ba': -0.1,
            'ε¹⁴²Nd': 0.0
        }
        result = calculate_iaf(cm_data)
        self.assertEqual(result['group'], 'CM')
        
        # Test outlier detection
        self.assertIn('is_outlier', result)
    
    def test_detect_presolar_grains(self):
        """Test presolar grain detection"""
        # Normal specimen
        normal = {
            'ε⁵⁰Ti': 0.5,
            'ε⁵⁴Cr': 0.3,
            'ε⁹⁶Mo': 0.1,
            'ε¹⁰⁰Mo': 0.05,
            'ε⁹²Ru': 0.02,
            'ε¹³⁷Ba': 0.01,
            'ε¹⁴²Nd': 0.0
        }
        result = detect_presolar_grains(normal)
        self.assertFalse(result['presolar_detected'])
        
        # Anomalous specimen (possible presolar)
        anomalous = {
            'ε⁵⁰Ti': 5.0,
            'ε⁵⁴Cr': 4.0,
            'ε⁹⁶Mo': -3.0,
            'ε¹⁰⁰Mo': -2.0,
            'ε⁹²Ru': 2.0,
            'ε¹³⁷Ba': -1.0,
            'ε¹⁴²Nd': 0.5
        }
        result = detect_presolar_grains(anomalous)
        self.assertTrue(result['presolar_detected'])


if __name__ == '__main__':
    unittest.main()
