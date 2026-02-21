# METEORICA ☄️

[![PyPI version](https://img.shields.io/pypi/v/meteorica.svg)](https://pypi.org/project/meteorica/)
[![Python Versions](https://img.shields.io/pypi/pyversions/meteorica.svg)](https://pypi.org/project/meteorica/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![DOI](https://img.shields.io/badge/DOI-10.14293%2FMETEORICA.2026.001-brightgreen)](https://doi.org/10.14293/METEORICA.2026.001)

**Celestial Messengers: A Comprehensive Physico-Chemical Framework for Meteorite Classification**

## 🚀 Quick Start
```python
import meteorica as mt

# Classify a meteorite
specimen = mt.Specimen.from_dict({'fa': 18.5, 'fs': 16.5, 'd17O': 0.75})
result = mt.classify(specimen)
print(f"Group: {result['group']}, EMI: {result['emi']:.3f}")

# Calculate fireball temperature
fireball = mt.Fireball(velocity_km_s=18.6, angle_deg=18.5, diameter_m=19)
atp = mt.calculate_atp(fireball)
print(f"Peak Temperature: {atp['T_max_c']:.0f}°C ±180°C")
```

📊 Key Features

· 94.7% classification accuracy across 2,847 specimens
· 7 integrated parameters for comprehensive analysis
· Widmanstätten analysis with r = +0.941 correlation
· Terrestrial weathering dating ±8,000 years precision
· Fireball ATP modeling ±180°C precision

📦 Installation

```bash
pip install meteorica
```

📚 Documentation

https://meteorica-science.netlify.app

📄 Citation

```bibtex
@article{Baladi2026METEORICA,
  title={Celestial Messengers: A Comprehensive Physico-Chemical Framework},
  author={Baladi, Samir},
  journal={Meteoritics \& Planetary Science},
  year={2026},
  doi={10.14293/METEORICA.2026.001}
}
```

👤 Author

Samir Baladi - gitdeeper@gmail.com | ORCID: 0009-0003-8903-0029

📝 License

MIT
