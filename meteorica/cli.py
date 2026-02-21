"""
METEORICA Command Line Interface
"""

import click
import json
import yaml
from pathlib import Path
from typing import Optional

from . import __version__
from .emi import calculate_emi, classify, Specimen, Fireball, calculate_atp as emi_calculate_atp


@click.group()
@click.version_option(version=__version__)
def main():
    """METEORICA - Celestial Messengers Framework"""
    pass


@main.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--format', '-f', type=click.Choice(['json', 'yaml', 'csv']), 
              default='json', help='Input file format')
@click.option('--output', '-o', type=click.Path(), help='Output file')
def classify(input_file, format, output):
    """Classify a meteorite specimen from data file"""
    click.echo(f"Classifying specimen from {input_file}")
    
    # Load data
    data = load_data(input_file, format)
    
    # Create specimen
    specimen = Specimen.from_dict(data)
    
    # Classify
    result = classify(specimen)
    
    # Output
    if output:
        with open(output, 'w') as f:
            json.dump(result, f, indent=2)
        click.echo(f"Results saved to {output}")
    else:
        click.echo(json.dumps(result, indent=2))


@main.command()
@click.option('--velocity', '-v', type=float, required=True, 
              help='Entry velocity (km/s)')
@click.option('--angle', '-a', type=float, required=True, 
              help='Entry angle (degrees)')
@click.option('--diameter', '-d', type=float, required=True, 
              help='Meteoroid diameter (m)')
@click.option('--composition', '-c', default='LL5', 
              help='Composition type')
def fireball(velocity, angle, diameter, composition):
    """Calculate ATP for a fireball event"""
    click.echo("Calculating Ablation Thermal Profile...")
    
    fireball = Fireball(
        velocity_km_s=velocity,
        angle_deg=angle,
        diameter_m=diameter,
        composition=composition
    )
    
    result = emi_calculate_atp(fireball)
    
    click.echo(f"\nPeak Surface Temperature: {result['T_max_c']:.0f}°C ± {result['T_max_precision']}°C")
    click.echo(f"Heat Flux: {result.get('heat_flux_peak_mw_m2', 0):.2f} MW/m²")
    click.echo(f"Airburst Altitude: {result.get('airburst_altitude_km', 0):.1f} km")


@main.command()
@click.argument('spectrum_file', type=click.Path(exists=True))
@click.option('--model', '-m', type=click.Path(), 
              help='Path to CNN model weights')
def spectrum(spectrum_file, model):
    """Classify meteorite from NIR spectrum"""
    click.echo(f"Analyzing spectrum from {spectrum_file}")
    
    # Load spectrum (simplified)
    import numpy as np
    data = np.loadtxt(spectrum_file)
    wavelengths = data[:, 0]
    reflectance = data[:, 1]
    
    # Classify
    from .classification import classify_spectrum
    result = classify_spectrum({
        'wavelengths': wavelengths,
        'reflectance': reflectance
    }, model)
    
    click.echo(f"\nPredicted Group: {result['predicted_group']}")
    click.echo(f"Confidence: {result['confidence']:.1%}")
    click.echo("\nTop 5:")
    for i, pred in enumerate(result['top_5'], 1):
        click.echo(f"  {i}. {pred['group']} ({pred['confidence']:.1%})")


@main.command()
@click.option('--mcc', type=float, help='MCC value')
@click.option('--smg', type=float, help='SMG value')
@click.option('--twi', type=float, help='TWI value')
@click.option('--iaf', type=float, help='IAF value')
@click.option('--atp', type=float, help='ATP temperature (°C)')
@click.option('--pbdr', type=float, help='PBDR value')
@click.option('--cnea', type=float, help='CNEA age (Ma)')
@click.option('--all', 'all_params', is_flag=True, 
              help='Calculate all parameters from sample data')
def calculate(mcc, smg, twi, iaf, atp, pbdr, cnea, all_params):
    """Calculate EMI from individual parameters"""
    
    params = {}
    if mcc is not None:
        params['mcc'] = mcc
    if smg is not None:
        params['smg'] = smg
    if twi is not None:
        params['twi'] = twi
    if iaf is not None:
        params['iaf'] = iaf
    if atp is not None:
        params['atp'] = atp
    if pbdr is not None:
        params['pbdr'] = pbdr
    if cnea is not None:
        params['cnea'] = cnea
    
    if not params and not all_params:
        click.echo("Please provide at least one parameter or use --all")
        return
    
    if all_params:
        # Example parameters for demonstration
        params = {
            'mcc': 0.85,
            'smg': 0.45,
            'twi': 0.25,
            'iaf': 0.78,
            'atp': 4820,
            'pbdr': 0.35,
            'cnea': 22.5
        }
        click.echo("Using example parameters for demonstration")
    
    emi = calculate_emi(params)
    click.echo(f"\nEMI Score: {emi:.3f}")
    
    # Determine classification level
    if emi < 0.20:
        click.echo("Classification: UNAMBIGUOUS 🟢")
    elif emi < 0.40:
        click.echo("Classification: HIGH CONFIDENCE 🟡")
    elif emi < 0.60:
        click.echo("Classification: BOUNDARY ZONE 🟠")
    elif emi < 0.80:
        click.echo("Classification: ANOMALOUS 🔴")
    else:
        click.echo("Classification: UNGROUPED CANDIDATE ⚫")


def load_data(filepath: str, format: str) -> dict:
    """Load data from file based on format"""
    path = Path(filepath)
    
    if format == 'json':
        with open(path) as f:
            return json.load(f)
    elif format == 'yaml':
        with open(path) as f:
            return yaml.safe_load(f)
    elif format == 'csv':
        import csv
        with open(path) as f:
            reader = csv.DictReader(f)
            return next(reader)
    else:
        raise ValueError(f"Unsupported format: {format}")


if __name__ == '__main__':
    main()
