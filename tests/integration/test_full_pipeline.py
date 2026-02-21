"""
Integration tests for full METEORICA pipeline
"""

import unittest
import sys
import os
import json
import tempfile
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from meteorica.emi import calculate_emi, classify, Specimen
from meteorica.parameters.mcc import calculate_mcc
from meteorica.parameters.twi import calculate_twi, estimate_terrestrial_age
from meteorica.parameters.iaf import calculate_iaf
from meteorica.parameters.atp import calculate_atp
from meteorica.classification.metbull_export import MetBullExporter


class TestFullPipeline(unittest.TestCase):
    """Test complete METEORICA pipeline"""
    
    def setUp(self):
        """Set up test data"""
        self.test_specimen = {
            'id': 'TEST001',
            'name': 'Test Meteorite',
            'fa': 18.5,  # H chondrite
            'fs': 16.5,
            'd17O': 0.75,
            'ni': None,
            'metal_oxidation': 0.05,
            'phyllosilicate': 0.02,
            'carbonate_veins': 0.0,
            'ε⁵⁰Ti': 0.5,
            'ε⁵⁴Cr': 0.3,
            'ε⁹⁶Mo': 0.1,
            'ε¹⁰⁰Mo': 0.05,
            'ε⁹²Ru': 0.02,
            'ε¹³⁷Ba': 0.01,
            'ε¹⁴²Nd': 0.0
        }
    
    def test_mineral_classification(self):
        """Test mineralogical classification"""
        result = calculate_mcc(self.test_specimen)
        self.assertEqual(result['group'], 'H')
        self.assertGreater(result['mcc'], 0.8)
    
    def test_weathering_analysis(self):
        """Test weathering analysis"""
        weathering_data = {
            'metal_oxidation': 0.05,
            'phyllosilicate': 0.02,
            'carbonate_veins': 0.0,
            'be_ne_deviation': 0.01,
            'fe_ni_deviation': 0.01
        }
        twi = calculate_twi(weathering_data)
        age = estimate_terrestrial_age(twi)
        
        self.assertLess(twi, 0.15)
        self.assertLess(age['age_years'], 1000)
    
    def test_isotopic_analysis(self):
        """Test isotopic analysis"""
        result = calculate_iaf(self.test_specimen)
        self.assertIn('iaf', result)
        self.assertIn('group', result)
    
    def test_emi_calculation(self):
        """Test EMI calculation with all parameters"""
        params = {
            'mcc': 0.92,
            'smg': 0.35,
            'twi': 0.12,
            'iaf': 0.88,
            'atp': 4820,
            'pbdr': 0.05,
            'cnea': 22.5
        }
        
        emi = calculate_emi(params)
        self.assertGreater(emi, 0.5)
        self.assertLess(emi, 1.0)
    
    def test_fireball_atp(self):
        """Test fireball ATP calculation"""
        fireball_params = {
            'velocity_km_s': 18.6,
            'angle_deg': 18.5,
            'diameter_m': 19,
            'density_kg_m3': 3300,
            'composition': 'LL5'
        }
        
        result = calculate_atp(fireball_params)
        self.assertIn('T_max_c', result)
        self.assertAlmostEqual(result['T_max_c'], 4820, delta=500)
    
    def test_export_to_metbull(self):
        """Test MetBull export"""
        with tempfile.TemporaryDirectory() as tmpdir:
            exporter = MetBullExporter(tmpdir)
            
            specimen = {'id': 'TEST001', 'name': 'Test'}
            result = {'group': 'H', 'emi': 0.92}
            
            filepath = exporter.export(specimen, result)
            self.assertTrue(os.path.exists(filepath))
            
            # Check file content
            with open(filepath) as f:
                data = json.load(f)
                self.assertIn('specimen', data)
                self.assertIn('classification', data)


if __name__ == '__main__':
    unittest.main()
