"""
MetBull-compatible export utilities.
Generate submission packages for Meteoritical Bulletin Database.
"""

import json
import yaml
import csv
from datetime import datetime
from typing import Dict, List, Optional, Any
import os


class MetBullExporter:
    """
    Export classification results to MetBull-compatible format.
    """
    
    def __init__(self, output_dir: str = "./metbull_exports"):
        """
        Initialize exporter.
        
        Args:
            output_dir: Directory for export files
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def export(self, specimen_data: Dict[str, Any], 
               classification_result: Dict[str, Any]) -> str:
        """
        Export specimen classification to MetBull format.
        
        Args:
            specimen_data: Original specimen metadata
            classification_result: METEORICA classification results
            
        Returns:
            Path to exported file
        """
        # Create MetBull entry
        entry = self._create_metbull_entry(specimen_data, classification_result)
        
        # Generate filename
        specimen_id = specimen_data.get('id', 'unknown')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{specimen_id}_{timestamp}.metbull"
        filepath = os.path.join(self.output_dir, filename)
        
        # Export as JSON (can also do YAML, CSV)
        with open(filepath, 'w') as f:
            json.dump(entry, f, indent=2)
        
        return filepath
    
    def _create_metbull_entry(self, specimen: Dict, result: Dict) -> Dict:
        """
        Create MetBull-compatible dictionary entry.
        """
        return {
            'metadata': {
                'exporter': 'METEORICA v1.0.0',
                'export_date': datetime.now().isoformat(),
                'doi': '10.14293/METEORICA.2026.001'
            },
            'specimen': {
                'id': specimen.get('id', ''),
                'name': specimen.get('name', ''),
                'collection': specimen.get('collection', ''),
                'repository': specimen.get('repository', ''),
                'recovery_date': specimen.get('recovery_date', ''),
                'recovery_location': specimen.get('recovery_location', {}),
                'mass_g': specimen.get('mass_g', 0)
            },
            'classification': {
                'group': result.get('group', 'Unknown'),
                'type': result.get('type', ''),
                'petrologic_type': result.get('petrologic_type', ''),
                'shock_stage': result.get('shock_stage', ''),
                'weathering_grade': result.get('weathering_grade', ''),
                'confidence': result.get('confidence', 0)
            },
            'parameters': {
                'emi': result.get('emi', 0),
                'mcc': result.get('mcc', 0),
                'smg': result.get('smg', 0),
                'twi': result.get('twi', 0),
                'iaf': result.get('iaf', 0),
                'atp': result.get('atp', 0),
                'pbdr': result.get('pbdr', 0),
                'cnea': result.get('cnea', 0)
            },
            'analyses': specimen.get('analyses', {}),
            'references': specimen.get('references', [])
        }
    
    def export_batch(self, specimens: List[Dict], 
                     results: List[Dict]) -> List[str]:
        """
        Export multiple specimens.
        
        Args:
            specimens: List of specimen data
            results: List of classification results
            
        Returns:
            List of exported file paths
        """
        exported = []
        for specimen, result in zip(specimens, results):
            filepath = self.export(specimen, result)
            exported.append(filepath)
        return exported
    
    def export_summary(self, specimens: List[Dict], 
                       results: List[Dict]) -> str:
        """
        Export summary CSV of all classifications.
        
        Args:
            specimens: List of specimen data
            results: List of classification results
            
        Returns:
            Path to summary CSV
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"metbull_summary_{timestamp}.csv"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow([
                'Specimen ID', 'Name', 'Group', 'EMI', 'MCC', 'SMG', 'TWI',
                'IAF', 'ATP', 'PBDR', 'CNEA', 'Confidence'
            ])
            
            # Rows
            for specimen, result in zip(specimens, results):
                writer.writerow([
                    specimen.get('id', ''),
                    specimen.get('name', ''),
                    result.get('group', ''),
                    result.get('emi', 0),
                    result.get('mcc', 0),
                    result.get('smg', 0),
                    result.get('twi', 0),
                    result.get('iaf', 0),
                    result.get('atp', 0),
                    result.get('pbdr', 0),
                    result.get('cnea', 0),
                    result.get('confidence', 0)
                ])
        
        return filepath


def export_to_metbull(specimen: Dict, result: Dict, 
                     output_dir: str = "./metbull_exports") -> str:
    """
    Convenience function to export a single specimen.
    
    Args:
        specimen: Specimen data
        result: Classification results
        output_dir: Output directory
        
    Returns:
        Path to exported file
    """
    exporter = MetBullExporter(output_dir)
    return exporter.export(specimen, result)
