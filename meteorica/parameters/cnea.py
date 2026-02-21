"""
Cosmogenic Nuclide Exposure Age (CNEA)
Multi-nuclide concordia for cosmic ray exposure history.
Physical model: only positive concentrations are valid.
"""

import numpy as np
from typing import Dict, Tuple, List

# Production rates for common cosmogenic nuclides (atoms/g/Ma)
PRODUCTION_RATES = {
    'he3': 1.5,
    'ne21': 0.35,
    'ar38': 0.08,
    'be10': 0.05,
    'al26': 0.07,
    'cl36': 0.03,
}

# Half-lives of radioactive nuclides (Ma)
HALF_LIVES = {
    'be10': 1.387,
    'al26': 0.717,
    'cl36': 0.301,
}

def calculate_cnea(nuclide_data: Dict[str, float]) -> Dict[str, object]:
    ages: Dict[str, float] = {}
    uncertainties: Dict[str, float] = {}

    # Stable nuclides
    for nuclide in ('he3', 'ne21', 'ar38'):
        if nuclide in nuclide_data:
            concentration = nuclide_data[nuclide]
            if concentration is None or concentration <= 0:
                continue
            P = PRODUCTION_RATES.get(nuclide, 0.0)
            if P > 0:
                age = concentration / P
                ages[nuclide] = age
                uncertainties[nuclide] = 0.08 * age

    # Radioactive nuclides
    for nuclide in ('be10', 'al26', 'cl36'):
        if nuclide in nuclide_data:
            concentration = nuclide_data[nuclide]
            if concentration is None or concentration <= 0:
                continue
            P = PRODUCTION_RATES.get(nuclide, 0.0)
            half_life = HALF_LIVES.get(nuclide)
            if P > 0 and half_life:
                decay_const = np.log(2) / half_life
                N_sat = P / decay_const
                if concentration < N_sat:
                    age = -np.log(1.0 - concentration / N_sat) / decay_const
                    uncertainties[nuclide] = 0.12 * age
                else:
                    age = 3.0 * half_life
                    uncertainties[nuclide] = 0.20 * age
                ages[nuclide] = age

    if not ages:
        return {
            'cnea': 0.0,
            'age_ma': 0.0,
            'exposure_history': 'Unknown',
            'is_concordant': True,
            'ages': {},
            'uncertainties': {},
            'nuclides_analyzed': []
        }

    # Weighted mean age
    weights, values = [], []
    for nuclide, age in ages.items():
        sigma = uncertainties.get(nuclide, 0.0)
        if sigma > 0:
            weights.append(1.0 / sigma**2)
            values.append(age)
    mean_age = np.average(values, weights=weights) if weights else np.mean(list(ages.values()))

    # Concordance
    is_concordant, concordance = check_concordance(ages, uncertainties, threshold=2.0)
    exposure_history = 'Single-stage' if is_concordant else 'Multi-stage'

    return {
        'cnea': mean_age / 100.0,
        'age_ma': mean_age,
        'exposure_history': exposure_history,
        'is_concordant': is_concordant,
        'ages': ages,
        'uncertainties': uncertainties,
        'concordia': concordance,
        'nuclides_analyzed': list(ages.keys())
    }

def check_concordance(
    ages: Dict[str, float],
    uncertainties: Dict[str, float],
    threshold: float = 2.0
) -> Tuple[bool, Dict]:
    if len(ages) < 2:
        mean = next(iter(ages.values()), 0.0)
        return True, {
            'mean_age': mean,
            'max_deviation_sigma': 0.0,
            'threshold_sigma': threshold,
            'deviations': {},
            'is_concordant': True
        }

    mean_age = np.mean(list(ages.values()))
    max_dev = 0.0
    deviations = {}
    for nuclide, age in ages.items():
        sigma = uncertainties.get(nuclide, 0.0)
        if sigma > 0:
            dev = abs(age - mean_age) / sigma
            deviations[nuclide] = dev
            max_dev = max(max_dev, dev)
    is_concordant = max_dev <= threshold
    return is_concordant, {
        'mean_age': mean_age,
        'max_deviation_sigma': max_dev,
        'threshold_sigma': threshold,
        'deviations': deviations,
        'is_concordant': is_concordant
    }

def estimate_shielding_depth(ne21_al26_ratio: float) -> float:
    if ne21_al26_ratio <= 0:
        return 0.0
    if ne21_al26_ratio < 5.0:
        return 10.0
    if ne21_al26_ratio < 10.0:
        return 25.0
    if ne21_al26_ratio < 20.0:
        return 50.0
    return 100.0
