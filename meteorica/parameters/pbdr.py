"""
Parent Body Differentiation Ratio (PBDR)
Based on Highly Siderophile Element (HSE) depletion patterns.
Physical principle: Only positive concentrations are physically valid.
"""

import numpy as np
from typing import Dict, List, Optional

# CI Chondrite HSE abundances (ng/g)
CI_HSE_ABUNDANCES = {
    'os': 486,
    'ir': 481,
    'ru': 712,
    'pt': 1010,
    'pd': 560,
    're': 37,
    'au': 140
}

# HSE partition coefficients during core formation
HSE_PARTITION_COEFFICIENTS = {
    'os': 10000,
    'ir': 10000,
    'ru': 8000,
    'pt': 5000,
    'pd': 2000,
    're': 5000,
    'au': 1000
}


def calculate_pbdr(hse_data: Dict[str, float]) -> Dict[str, any]:
    ratios = []
    elements = []

    for element, value in hse_data.items():
        # 🔴 Strict physical filter: only positive numeric values
        if value is None or not isinstance(value, (int, float)) or value <= 0 or not np.isfinite(value):
            continue

        if element in CI_HSE_ABUNDANCES:
            ci_value = CI_HSE_ABUNDANCES[element]
            if ci_value <= 0:
                continue
            ratio = value / ci_value
            ratios.append(ratio)
            elements.append(element)

    if not ratios:
        return {
            'pbdr': 0.0,
            'avg_hse_ratio': 0.0,
            'differentiation': 'Undifferentiated (Chondritic)',
            'parent_body_type': 'Undifferentiated asteroid',
            'elements_analyzed': []
        }

    avg_ratio = np.mean(ratios)
    pbdr = max(0.0, min(1.0, 1.0 - avg_ratio))

    differentiation = interpret_differentiation(pbdr)
    parent_body_type = estimate_parent_body(pbdr, hse_data)

    return {
        'pbdr': pbdr,
        'avg_hse_ratio': avg_ratio,
        'differentiation': differentiation,
        'parent_body_type': parent_body_type,
        'elements_analyzed': elements
    }


def interpret_differentiation(pbdr: float) -> str:
    if pbdr < 0.1:
        return 'Undifferentiated (Chondritic)'
    elif pbdr < 0.35:
        return 'Partially differentiated'
    elif pbdr < 0.65:
        return 'Moderately differentiated'
    elif pbdr < 0.85:
        return 'Highly differentiated'
    else:
        return 'Fully differentiated (Core/Mantle)'


def estimate_parent_body(pbdr: float, hse_data: Dict = None) -> str:
    """
    Estimate parent body type from PBDR and optionally HSE data.
    
    Args:
        pbdr: Parent Body Differentiation Ratio
        hse_data: Original HSE data for additional context
        
    Returns:
        Description of likely parent body
    """
    if pbdr < 0.1:
        return 'Undifferentiated asteroid (chondritic)'
    elif pbdr < 0.3:
        return 'Partially differentiated body'
    elif pbdr < 0.6:
        return 'Differentiated asteroid (e.g., Vesta-like)'
    elif pbdr < 0.9:
        return 'Highly differentiated body (mantle/crust sample)'
    else:
        # PBDR > 0.9 - could be Vesta-like or core material
        # Check if it's Vesta-like (HED) based on HSE pattern
        if hse_data and all(value < 50 for value in hse_data.values() if isinstance(value, (int, float))):
            # Very low HSE concentrations suggest mantle material
            return 'Vesta-like differentiated body (mantle sample)'
        else:
            return 'Core material (fully differentiated)'


def calculate_core_formation_extent(pbdr: float,
                                   partition_coeffs: Optional[Dict] = None) -> float:
    pbdr = max(0.0, min(1.0, pbdr))

    if partition_coeffs is None:
        avg_d = np.mean(list(HSE_PARTITION_COEFFICIENTS.values()))
    else:
        valid_coeffs = [v for v in partition_coeffs.values() if v > 0]
        avg_d = np.mean(valid_coeffs) if valid_coeffs else 1000.0

    if pbdr >= 0.99:
        return 1.0
    elif pbdr <= 0:
        return 0.0

    F = 1.0 - np.exp(-pbdr * 5.0)
    return min(1.0, max(0.0, F))


def validate_hse_data(hse_data: Dict[str, float]) -> Dict[str, float]:
    validated = {}
    for element, value in hse_data.items():
        if value is None or not isinstance(value, (int, float)) or value <= 0 or not np.isfinite(value):
            continue
        if element in CI_HSE_ABUNDANCES:
            validated[element] = value
    return validated
