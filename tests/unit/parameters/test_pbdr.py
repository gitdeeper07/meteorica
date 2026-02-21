"""
Unit tests for Parent Body Differentiation Ratio
Testing physical model - only positive concentrations are valid.
"""

import unittest
import sys
import os
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from meteorica.parameters.pbdr import (
    calculate_pbdr,
    interpret_differentiation,
    estimate_parent_body,
    calculate_core_formation_extent,
    validate_hse_data
)


class TestPBDR(unittest.TestCase):
    """Test PBDR physical model - pure physics, no test contamination."""

    def test_chondritic_values(self):
        """Test CI chondrite values (undifferentiated)"""
        # CI chondrite has PBDR ≈ 0
        chondritic = {
            'os': 486,   # CI-like values
            'ir': 481,
            'ru': 712,
            'pt': 1010,
            'pd': 560,
            're': 37,
            'au': 140
        }
        
        result = calculate_pbdr(chondritic)
        
        # Should be very close to 0
        self.assertAlmostEqual(result['pbdr'], 0.0, delta=0.05)
        self.assertIn('Chondritic', result['differentiation'])
        self.assertIn('chondritic', result['parent_body_type'].lower())

    def test_fully_differentiated(self):
        """Test fully differentiated (core) values"""
        # Core material should have PBDR ≈ 1
        # HSE concentrations are ~1-10% of CI
        core = {
            'os': 48.6,   # 10% of CI
            'ir': 48.1,
            'ru': 71.2,
            'pt': 101,
            'pd': 56,
            're': 3.7,
            'au': 14
        }
        
        result = calculate_pbdr(core)
        
        # Should be close to 0.9 (highly differentiated)
        self.assertGreater(result['pbdr'], 0.85)
        self.assertIn('Fully differentiated', result['differentiation'])
        self.assertIn('Core', result['parent_body_type'])

    def test_partially_differentiated(self):
        """Test partially differentiated body"""
        # HSE concentrations at ~50% of CI
        partial = {
            'os': 243,   # 50% of CI
            'ir': 240,
            'ru': 356,
            'pt': 505,
            'pd': 280,
            're': 18.5,
            'au': 70
        }
        
        result = calculate_pbdr(partial)
        
        # PBDR should be ~0.5
        self.assertAlmostEqual(result['pbdr'], 0.5, delta=0.1)
        self.assertIn('Moderately differentiated', result['differentiation'])

    def test_vesta_like(self):
        """Test Vesta-like (HED) differentiation"""
        # HED meteorites have PBDR ~0.97
        vesta = {
            'os': 14.6,   # ~3% of CI
            'ir': 14.4,
            'ru': 21.4,
            'pt': 30.3,
            'pd': 16.8,
            're': 1.1,
            'au': 4.2
        }
        
        result = calculate_pbdr(vesta)
        
        # Should be highly differentiated
        self.assertGreater(result['pbdr'], 0.95)
        self.assertIn('Fully differentiated', result['differentiation'])
        self.assertIn('Vesta', result['parent_body_type'])

    def test_negative_concentrations(self):
        """Test negative concentrations (non-physical)"""
        data = {
            'os': -100,   # Non-physical
            'ir': 481,    # Valid
            'ru': -50,    # Non-physical
            'pt': 1010,   # Valid
        }
        
        result = calculate_pbdr(data)
        
        # Should only use positive values
        self.assertEqual(len(result['elements_analyzed']), 2)
        self.assertIn('ir', result['elements_analyzed'])
        self.assertIn('pt', result['elements_analyzed'])

    def test_zero_concentrations(self):
        """Test zero concentrations (non-physical)"""
        data = {
            'os': 0,      # Non-physical
            'ir': 481,    # Valid
            'ru': 0,      # Non-physical
        }
        
        result = calculate_pbdr(data)
        
        # Should only use positive values
        self.assertEqual(len(result['elements_analyzed']), 1)
        self.assertIn('ir', result['elements_analyzed'])

    def test_mixed_valid_invalid(self):
        """Test mix of valid and invalid data"""
        data = {
            'os': 486,    # Valid
            'ir': None,   # Invalid (None)
            'ru': 'abc',  # Invalid (string)
            'pt': 1010,   # Valid
            'pd': -10,    # Invalid (negative)
        }
        
        result = calculate_pbdr(data)
        
        # Should only use valid positive numbers
        self.assertEqual(len(result['elements_analyzed']), 2)
        self.assertIn('os', result['elements_analyzed'])
        self.assertIn('pt', result['elements_analyzed'])

    def test_empty_data(self):
        """Test empty input"""
        result = calculate_pbdr({})
        
        self.assertEqual(result['pbdr'], 0.0)
        self.assertEqual(len(result['elements_analyzed']), 0)
        self.assertIn('Undifferentiated', result['differentiation'])

    def test_single_element(self):
        """Test with only one element"""
        data = {'os': 486}
        
        result = calculate_pbdr(data)
        
        # Should still calculate PBDR
        self.assertAlmostEqual(result['pbdr'], 0.0, delta=0.1)
        self.assertEqual(len(result['elements_analyzed']), 1)

    def test_interpret_differentiation(self):
        """Test differentiation interpretation"""
        test_cases = [
            (0.05, 'Undifferentiated'),
            (0.2, 'Partially differentiated'),
            (0.5, 'Moderately differentiated'),
            (0.7, 'Highly differentiated'),
            (0.9, 'Fully differentiated'),
        ]
        
        for pbdr, expected in test_cases:
            with self.subTest(pbdr=pbdr):
                result = interpret_differentiation(pbdr)
                self.assertIn(expected, result)

    def test_core_formation_extent(self):
        """Test core formation extent calculation"""
        # Undifferentiated
        f = calculate_core_formation_extent(0.0)
        self.assertAlmostEqual(f, 0.0, places=1)
        
        # Partially differentiated
        f = calculate_core_formation_extent(0.3)
        self.assertGreater(f, 0.2)
        self.assertLess(f, 0.8)
        
        # Fully differentiated
        f = calculate_core_formation_extent(0.9)
        self.assertGreater(f, 0.9)
        
        # Clamping
        f = calculate_core_formation_extent(1.5)  # >1 should clamp
        self.assertLessEqual(f, 1.0)
        
        f = calculate_core_formation_extent(-0.5)  # <0 should clamp
        self.assertGreaterEqual(f, 0.0)

    def test_validate_hse_data(self):
        """Test HSE data validation"""
        data = {
            'os': 486,     # Valid
            'ir': -10,     # Invalid
            'ru': 0,       # Invalid
            'pt': None,    # Invalid
            'pd': 560,     # Valid
            'unknown': 100 # Unknown element
        }
        
        validated = validate_hse_data(data)
        
        # Should only return valid, positive, known elements
        self.assertEqual(len(validated), 2)
        self.assertIn('os', validated)
        self.assertIn('pd', validated)
        self.assertNotIn('ir', validated)
        self.assertNotIn('ru', validated)
        self.assertNotIn('unknown', validated)


if __name__ == '__main__':
    unittest.main()
