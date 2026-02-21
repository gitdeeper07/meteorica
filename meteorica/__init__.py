"""
METEORICA: Celestial Messengers - A Comprehensive Physico-Chemical Framework
for the Classification, Terrestrial Interaction, and Cosmochemical Significance
of Extraterrestrial Materials.

Version: 1.0.0
DOI: 10.14293/METEORICA.2026.001
"""

__version__ = "1.0.0"
__author__ = "Samir Baladi"
__email__ = "gitdeeper@gmail.com"
__doi__ = "10.14293/METEORICA.2026.001"

# استيرادات نسبية من داخل الحزمة
from .emi import calculate_emi, classify
from .parameters import mcc, smg, twi, iaf, atp, pbdr, cnea

__all__ = [
    "calculate_emi",
    "classify",
    "mcc",
    "smg",
    "twi",
    "iaf",
    "atp",
    "pbdr",
    "cnea",
]
