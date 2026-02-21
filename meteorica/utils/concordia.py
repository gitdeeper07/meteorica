"""
Concordia diagrams for cosmogenic nuclide exposure ages.
Multi-nuclide concordia for single-stage vs multi-stage irradiation.
"""

import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import matplotlib.pyplot as plt
from datetime import datetime


@dataclass
class NuclideAge:
    """Cosmogenic nuclide age data."""
    nuclide: str
    age_ma: float
    uncertainty_ma: float
    is_radioactive: bool
    half_life_ma: Optional[float] = None


class ConcordiaDiagram:
    """
    Concordia diagram for multi-nuclide exposure ages.
    Detects single-stage vs multi-stage irradiation histories.
    """
    
    # Nuclide properties
    NUCLIDES = {
        'he3': {'type': 'stable', 'half_life': None},
        'ne21': {'type': 'stable', 'half_life': None},
        'ar38': {'type': 'stable', 'half_life': None},
        'be10': {'type': 'radioactive', 'half_life': 1.387},
        'al26': {'type': 'radioactive', 'half_life': 0.717},
        'cl36': {'type': 'radioactive', 'half_life': 0.301},
        'ca41': {'type': 'radioactive', 'half_life': 0.103},
    }
    
    def __init__(self):
        """Initialize concordia diagram."""
        self.ages: Dict[str, NuclideAge] = {}
        self.reference_age: Optional[float] = None
    
    def add_nuclide(self, name: str, age_ma: float, uncertainty_ma: float):
        """
        Add a nuclide age.
        
        Args:
            name: Nuclide name (e.g., 'he3', 'ne21', 'be10')
            age_ma: Exposure age in Ma
            uncertainty_ma: Uncertainty in Ma
        """
        props = self.NUCLIDES.get(name, {'type': 'stable', 'half_life': None})
        
        self.ages[name] = NuclideAge(
            nuclide=name,
            age_ma=age_ma,
            uncertainty_ma=uncertainty_ma,
            is_radioactive=props['type'] == 'radioactive',
            half_life_ma=props['half_life']
        )
    
    def is_concordant(self, threshold_sigma: float = 2.0) -> bool:
        """
        Check if ages are concordant (single-stage exposure).
        
        From research paper: 73% of specimens are single-stage.
        
        Args:
            threshold_sigma: Maximum deviation in sigma
            
        Returns:
            True if concordant (single-stage)
        """
        if len(self.ages) < 2:
            return True
        
        # Calculate weighted mean of stable nuclides
        stable_ages = []
        stable_uncertainties = []
        
        for name, age in self.ages.items():
            if not age.is_radioactive:
                stable_ages.append(age.age_ma)
                stable_uncertainties.append(age.uncertainty_ma)
        
        if stable_ages:
            weights = [1/u**2 for u in stable_uncertainties]
            mean_age = np.average(stable_ages, weights=weights)
            self.reference_age = mean_age
        else:
            # Use first age as reference
            first_age = list(self.ages.values())[0]
            mean_age = first_age.age_ma
        
        # Check all ages against reference
        for name, age in self.ages.items():
            sigma = abs(age.age_ma - mean_age) / age.uncertainty_ma
            if sigma > threshold_sigma:
                return False
        
        return True
    
    def get_exposure_history(self) -> Dict[str, Any]:
        """
        Determine exposure history type.
        
        Returns:
            Dictionary with exposure history information
        """
        is_conc = self.is_concordant()
        
        if is_conc:
            history_type = "Single-stage"
            confidence = 0.85  # From research paper
        else:
            history_type = "Multi-stage"
            confidence = 0.75
            
            # Try to identify number of stages
            n_stages = self._estimate_stages()
        ages_list = list(self.ages.values())
        
        return {
            'type': history_type,
            'is_concordant': is_concordant,
            'confidence': confidence,
            'mean_age_ma': self.reference_age,
            'n_nuclides': len(self.ages),
            'n_stages': n_stages if not is_conc else 1,
            'ages': {name: {'age_ma': age.age_ma, 
                           'uncertainty_ma': age.uncertainty_ma}
                    for name, age in self.ages.items()}
        }
    
    def _estimate_stages(self) -> int:
        """Estimate number of exposure stages for discordant data."""
        if len(self.ages) < 2:
            return 1
        
        # Simple heuristic based on age spread
        ages = [age.age_ma for age in self.ages.values()]
        age_range = max(ages) - min(ages)
        mean_age = np.mean(ages)
        
        if age_range / mean_age > 0.5:
            return 3  # Multiple stages
        elif age_range / mean_age > 0.2:
            return 2  # Two stages
        else:
            return 1  # Single stage
    
    def plot(self, ax: Optional[plt.Axes] = None, 
            show_uncertainties: bool = True) -> plt.Axes:
        """
        Plot concordia diagram.
        
        Args:
            ax: Matplotlib axes (creates new if None)
            show_uncertainties: Show error bars
            
        Returns:
            Matplotlib axes
        """
        if ax is None:
            fig, ax = plt.subplots(figsize=(8, 6))
        
        # Prepare data
        names = list(self.ages.keys())
        ages = [self.ages[n].age_ma for n in names]
        uncertainties = [self.ages[n].uncertainty_ma for n in names]
        colors = ['red' if self.ages[n].is_radioactive else 'blue' 
                 for n in names]
        
        # Plot ages
        x = np.arange(len(names))
        ax.bar(x, ages, yerr=uncertainties if show_uncertainties else None,
              color=colors, alpha=0.7, capsize=5)
        
        # Add reference line if concordant
        if self.reference_age:
            ax.axhline(y=self.reference_age, color='green', 
                      linestyle='--', alpha=0.5,
                      label=f'Mean: {self.reference_age:.1f} Ma')
        
        # Customize plot
        ax.set_xticks(x)
        ax.set_xticklabels(names)
        ax.set_ylabel('Exposure Age (Ma)')
        ax.set_title('Cosmogenic Nuclide Concordia Diagram')
        ax.legend(['Stable (blue)', 'Radioactive (red)'])
        
        # Add concordance info
        is_conc = self.is_concordant()
        status = "CONCORDANT ✓" if is_conc else "DISCORDANT ⚠"
        ax.text(0.02, 0.98, f"Status: {status}", 
               transform=ax.transAxes, va='top',
               color='green' if is_conc else 'red',
               fontweight='bold')
        
        return ax


def calculate_concordia(ages: Dict[str, float], 
                        uncertainties: Dict[str, float]) -> Dict[str, Any]:
    """
    Calculate concordia statistics.
    
    Args:
        ages: Dictionary of ages by nuclide
        uncertainties: Dictionary of uncertainties by nuclide
        
    Returns:
        Concordia analysis results
    """
    diagram = ConcordiaDiagram()
    
    for name, age in ages.items():
        uncertainty = uncertainties.get(name, age * 0.1)  # Default 10%
        diagram.add_nuclide(name, age, uncertainty)
    
    is_concordant = diagram.is_concordant()
    history = diagram.get_exposure_history()
    
    return {
        "is_concordant": is_concordant,
        "exposure_history": history['type'],
        "confidence": history['confidence'],
        "mean_age_ma": diagram.reference_age,
        "n_nuclides": len(ages),
        "n_stages": history.get('n_stages', 1),
        "ages": history['ages'],
        "concordia_diagram": diagram
    }


def calculate_exposure_age(nuclide_concentrations: Dict[str, float],
                          production_rates: Dict[str, float]) -> Dict[str, Any]:
    """
    Calculate exposure age from nuclide concentrations.
    
    T_CRE = N / P
    
    Args:
        nuclide_concentrations: Nuclide concentrations (atoms/g)
        production_rates: Production rates (atoms/g/Ma)
        
    Returns:
        Exposure age results
    """
    ages = {}
    uncertainties = {}
    
    for nuclide, conc in nuclide_concentrations.items():
        if nuclide in production_rates:
            P = production_rates[nuclide]
            age = conc / P
            
            # Uncertainty (8% for stable, 12% for radioactive from research)
            if nuclide in ['he3', 'ne21', 'ar38']:
                uncertainty = age * 0.08
            else:
                uncertainty = age * 0.12
            
            ages[nuclide] = age
            uncertainties[nuclide] = uncertainty
    
    # Calculate concordia
    concordia = calculate_concordia(ages, uncertainties)
    
    return {
        'ages_ma': ages,
        'uncertainties_ma': uncertainties,
        'mean_age_ma': concordia['mean_age_ma'],
        'exposure_history': concordia['exposure_history'],
        'is_concordant': concordia['is_concordant'],
        'confidence': concordia['confidence'],
        'nuclides_analyzed': list(ages.keys())
    }
