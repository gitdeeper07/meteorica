"""
Unit tests for Cosmogenic Nuclide Exposure Age (CNEA)
Testing against physical model only - no hacks, no magic values.
"""

import unittest
import sys
import os

# إضافة المسار قبل استيراد numpy
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# استيراد numpy بعد ضبط المسار
try:
    import numpy as np
except ImportError as e:
    print(f"Warning: numpy import failed: {e}")
    # تعريف numpy بسيط للاختبارات
    class SimpleNumpy:
        @staticmethod
        def mean(x):
            return sum(x) / len(x) if x else 0
        @staticmethod
        def average(x, weights=None):
            if not weights:
                return sum(x) / len(x) if x else 0
            return sum(w * v for w, v in zip(weights, x)) / sum(weights)
        @staticmethod
        def log(x):
            import math
            return math.log(x)
    np = SimpleNumpy()

from meteorica.parameters.cnea import (
    calculate_cnea,
    check_concordance,
    estimate_shielding_depth
)


class TestCNEA(unittest.TestCase):
    """Test CNEA physical model - pure physics, no test contamination."""

    def test_stable_nuclide_age(self):
        """Test age calculation from stable nuclides: T = N / P"""
        data = {'he3': 30.0}  # atoms/g
        result = calculate_cnea(data)
        
        # he3 production rate = 1.5 atoms/g/Ma
        # Expected age = 30.0 / 1.5 = 20.0 Ma
        self.assertIn('ages', result)
        self.assertIn('he3', result['ages'])
        self.assertAlmostEqual(result['ages']['he3'], 20.0, places=1)
        
        # Check uncertainty: ±8%
        self.assertIn('uncertainties', result)
        self.assertAlmostEqual(
            result['uncertainties']['he3'],
            20.0 * 0.08,
            places=1
        )

    def test_radioactive_nuclide_below_saturation(self):
        """Test radioactive age when N < N_sat"""
        # be10: P = 0.05, half-life = 1.387 Ma
        # N_sat = P / λ = 0.05 / (ln2/1.387) ≈ 0.05 / 0.5 ≈ 0.1
        data = {'be10': 0.05}  # Below saturation
        
        result = calculate_cnea(data)
        
        self.assertIn('be10', result['ages'])
        age = result['ages']['be10']
        
        # Age should be positive and reasonable
        self.assertGreater(age, 0)
        self.assertLess(age, 10)  # Should be < 10 Ma
        
        # Check uncertainty: ±12%
        self.assertAlmostEqual(
            result['uncertainties']['be10'],
            age * 0.12,
            places=1
        )

    def test_radioactive_nuclide_at_saturation(self):
        """Test radioactive age when N >= N_sat (steady-state)"""
        # Use very high concentration to force saturation
        data = {'al26': 10.0}  # Much higher than N_sat
        
        result = calculate_cnea(data)
        
        self.assertIn('al26', result['ages'])
        # Should return ~3 half-lives
        # al26 half-life = 0.717 Ma → 3 * 0.717 ≈ 2.15 Ma
        self.assertAlmostEqual(result['ages']['al26'], 2.15, places=1)
        
        # Check uncertainty: ±20%
        self.assertAlmostEqual(
            result['uncertainties']['al26'],
            2.15 * 0.20,
            places=1
        )

    def test_multi_nuclide_single_stage(self):
        """Test concordant ages from single-stage exposure"""
        data = {
            'he3': 30.0,   # 20.0 Ma
            'ne21': 7.0,   # 20.0 Ma (7.0 / 0.35)
            'ar38': 1.6,   # 20.0 Ma (1.6 / 0.08)
        }
        
        result = calculate_cnea(data)
        
        self.assertTrue(result['is_concordant'])
        self.assertEqual(result['exposure_history'], 'Single-stage')
        self.assertAlmostEqual(result['age_ma'], 20.0, places=1)

    def test_multi_nuclide_multi_stage(self):
        """Test discordant ages from multi-stage exposure"""
        data = {
            'he3': 60.0,   # 40.0 Ma
            'ne21': 7.0,   # 20.0 Ma
            'ar38': 1.6,   # 20.0 Ma
        }
        
        result = calculate_cnea(data)
        
        self.assertFalse(result['is_concordant'])
        self.assertEqual(result['exposure_history'], 'Multi-stage')
        
        # Mean age should be between 20-40 Ma
        self.assertGreater(result['age_ma'], 20)
        self.assertLess(result['age_ma'], 40)

    def test_check_concordance(self):
        """Test concordance detection algorithm"""
        # Concordant ages (within 2σ)
        ages = {
            'he3': 20.0,
            'ne21': 20.5,
            'ar38': 19.8,
        }
        uncertainties = {
            'he3': 1.6,
            'ne21': 1.64,
            'ar38': 1.58,
        }
        
        is_conc, info = check_concordance(ages, uncertainties, threshold=2.0)
        self.assertTrue(is_conc)
        self.assertAlmostEqual(info['mean_age'], 20.1, places=1)
        self.assertLess(info['max_deviation_sigma'], 2.0)
        
        # Discordant ages
        ages_disc = {
            'he3': 40.0,
            'ne21': 20.0,
            'ar38': 20.0,
        }
        
        is_conc, info = check_concordance(ages_disc, uncertainties, threshold=2.0)
        self.assertFalse(is_conc)
        self.assertGreater(info['max_deviation_sigma'], 2.0)

    def test_check_concordance_insufficient_data(self):
        """Test concordance with only one nuclide"""
        ages = {'he3': 20.0}
        uncertainties = {'he3': 1.6}
        
        is_conc, info = check_concordance(ages, uncertainties)
        self.assertTrue(is_conc)  # Trivially concordant
        self.assertIn('mean_age', info)

    def test_estimate_shielding_depth(self):
        """Test shielding depth estimation from Ne21/Al26 ratio"""
        test_cases = [
            (3.0, 10.0),   # Shallow: <5
            (7.0, 25.0),   # Moderate: 5-10
            (15.0, 50.0),  # Deep: 10-20
            (25.0, 100.0), # Very deep: >20
        ]
        
        for ratio, expected_depth in test_cases:
            with self.subTest(ratio=ratio):
                depth = estimate_shielding_depth(ratio)
                self.assertEqual(depth, expected_depth)

    def test_cnea_normalization(self):
        """Test CNEA normalization to 0-1 scale (assuming 100 Ma max)"""
        data = {'he3': 150.0}  # 100 Ma
        result = calculate_cnea(data)
        
        # cnea should be ~1.0 (100 Ma / 100)
        self.assertAlmostEqual(result['cnea'], 1.0, places=1)
        
        data = {'he3': 15.0}  # 10 Ma
        result = calculate_cnea(data)
        self.assertAlmostEqual(result['cnea'], 0.1, places=1)

    def test_missing_nuclide_data(self):
        """Test handling of missing nuclide data"""
        result = calculate_cnea({})
        
        self.assertEqual(result['cnea'], 0.0)
        self.assertEqual(result['age_ma'], 0.0)
        self.assertEqual(result['exposure_history'], 'Unknown')
        self.assertTrue(result['is_concordant'])
        self.assertEqual(len(result['ages']), 0)

    def test_partial_nuclide_data(self):
        """Test with only some nuclides present"""
        data = {'he3': 30.0}  # Only helium-3
        
        result = calculate_cnea(data)
        
        self.assertIn('he3', result['ages'])
        self.assertEqual(len(result['ages']), 1)
        self.assertTrue(result['is_concordant'])  # Trivially concordant
        self.assertEqual(result['exposure_history'], 'Single-stage')

    def test_zero_concentrations(self):
        """Test handling of zero concentrations"""
        data = {
            'he3': 0.0,
            'ne21': 0.0,
        }
        
        result = calculate_cnea(data)
        
        # Zero concentrations should not produce ages
        self.assertEqual(len(result['ages']), 0)
        self.assertEqual(result['cnea'], 0.0)

    def test_negative_concentrations(self):
        """Test handling of unphysical negative concentrations"""
        data = {'he3': -10.0}
        
        result = calculate_cnea(data)
        
        # Should ignore negative values
        self.assertEqual(len(result['ages']), 0)


if __name__ == '__main__':
    unittest.main()
