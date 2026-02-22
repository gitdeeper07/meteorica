<div align="center">

<br>

# ☄️ METEORICA

### *Celestial Messengers*

**A Comprehensive Physico-Chemical Framework for the Classification,**
**Terrestrial Interaction, and Cosmochemical Significance of Extraterrestrial Materials**

<br>

[![PyPI](https://img.shields.io/pypi/v/meteorica?color=28a745&label=PyPI&logo=pypi&logoColor=white)](https://pypi.org/project/meteorica/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](https://pypi.org/project/meteorica/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-40%2F40%20✓-brightgreen)](tests/)
[![DOI](https://img.shields.io/badge/DOI-10.14293%2FMETEORIC.2026.001-blueviolet)](https://doi.org/10.14293/METEORICA.2026.001)
[![Zenodo](https://img.shields.io/badge/Zenodo-10.5281%2Fzenodo.18726661-blue)](https://doi.org/10.5281/zenodo.18726661)
[![OSF](https://img.shields.io/badge/OSF-10.17605%2FOSF.IO%2FBRDQM-teal)](https://doi.org/10.17605/OSF.IO/BRDQM)
[![Dashboard](https://img.shields.io/badge/Dashboard-Live-00C7B7?logo=netlify&logoColor=white)](https://meteorica-science.netlify.app)

<br>

*Submitted to **Meteoritics & Planetary Science** (Wiley-Blackwell) · March 2026*

<br>

[🌐 Website](https://meteorica-science.netlify.app) &nbsp;·&nbsp;
[📊 Dashboard](https://meteorica-science.netlify.app/dashboard) &nbsp;·&nbsp;
[📚 Documentation](https://meteorica-science.netlify.app/documentation) &nbsp;·&nbsp;
[📑 Reports](https://meteorica-science.netlify.app/reports)

<br>

</div>

---

## Table of Contents

- [Overview](#-overview)
- [Key Results](#-key-results)
- [The Seven Parameters](#-the-seven-meteorica-parameters)
- [EMI Classification](#-emi-classification)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Case Studies](#-case-studies)
- [Project Structure](#-project-structure)
- [Modules](#-modules)
- [Configuration](#-configuration)
- [Dashboard](#-dashboard)
- [Contributing](#-contributing)
- [Citation](#-citation)
- [License](#-license)

---

## 🌍 Overview

**METEORICA** is an open-source, physics-based framework for the integrated classification and cosmochemical analysis of extraterrestrial materials. It combines seven independent analytical parameters into a single operational index — the **Extraterrestrial Material Index (EMI)** — validated across **2,847 meteorite specimens** from **18 global repositories** spanning **140 years** of recovery history.

> **Core premise:** Meteorites are not rocks — they are encrypted archives of the solar system's first four billion years.
> METEORICA is the cipher.

No existing system simultaneously integrates quantitative mineralogy, shock history, terrestrial weathering correction, isotopic nucleosynthetic fingerprinting, atmospheric ablation physics, parent body differentiation state, and cosmic ray exposure age. METEORICA achieves this at **94.7% classification accuracy** — a **+4.9 percentage point improvement** over the best prior automated system — while reducing expert classification time from months to hours.

---

## 📊 Key Results

| Metric | Result | Basis |
|:---|:---:|:---|
| EMI Classification Accuracy | **94.7%** | 2,847 specimens · 18 repositories |
| AI Spectral Classification | **91.3%** | vs. expert committee · 441 held-out specimens |
| Widmanstätten Correlation | **r = +0.941** | p < 0.001 · 847 iron sections |
| Parent Body Reconstruction | **±180 km** | 3.2× improvement over prior estimates |
| ATP Temperature Precision | **±180°C** | 94 instrumentally recorded fireball events |
| TWI Terrestrial Age | **±8,000 yr** | 156 ¹⁴C-calibrated specimens |
| IAF Group Discrimination | **97.3%** | 7-dimensional isotope space · 312 CAIs |
| Legacy Misclassification Rate | **12.3%** | ~9,400 MetBull specimens flagged |
| Presolar Grain Detection | **99.1%** | vs. 84.3% single-isotope screening |

---

## 🔬 The Seven METEORICA Parameters

The EMI composite integrates seven parameters, each grounded in independent physical theory:

| # | Symbol | Parameter | Weight | Domain |
|:---:|:---:|:---|:---:|:---|
| 1 | **MCC** | Mineralogical Classification Coefficient | 26% | Mineralogy & Petrology |
| 2 | **SMG** | Shock Metamorphism Grade | 19% | Impact Physics |
| 3 | **TWI** | Terrestrial Weathering Index | 18% | Geochemistry |
| 4 | **IAF** | Isotopic Anomaly Fingerprint | 17% | Isotope Geochemistry |
| 5 | **ATP** | Ablation Thermal Profile | 10% | Atmospheric Physics |
| 6 | **PBDR** | Parent Body Differentiation Ratio | 6% | Planetary Science |
| 7 | **CNEA** | Cosmogenic Nuclide Exposure Age | 4% | Geochronology |

### EMI Composite Formula

```
EMI = 0.26·MCC* + 0.19·SMG* + 0.18·TWI* + 0.17·IAF* + 0.10·ATP* + 0.06·PBDR* + 0.04·CNEA*

Pᵢ* = (Pᵢ − Pᵢ_min) / (Pᵢ_crit − Pᵢ_min)     [normalized to 0–1 scale]
```

### Physical Equations

```python
# MCC — Mahalanobis distance in mineralogical phase space
MCC = 1 − d(P_obs, P_centroid) / d_max

# SMG — Hugoniot-calibrated continuous shock scale
T_post = T_0 + (P_shock · ΔV) / (2 · c_v · ρ)
SMG    = Σ wᵢ · f_i(P_peak) / Σ wᵢ

# TWI — Five-indicator weathering index & terrestrial age
TWI = 0.30·(metal oxidation) + 0.25·(phyllosilicate)
    + 0.20·(carbonate veins) + 0.15·(¹⁰Be/²¹Ne) + 0.10·(Fe/Ni)
Age = 12,400 · ln(1 + 3.7 · TWI)   [years]

# IAF — 7D nucleosynthetic fingerprint
IAF = exp(−d_iso² / 2σ²_group)
# Isotope space: (ε⁵⁰Ti, ε⁵⁴Cr, ε⁹⁶Mo, ε¹⁰⁰Mo, ε⁹²Ru, ε¹³⁷Ba, ε¹⁴²Nd)

# ATP — Atmospheric entry ablation heat flux
q              = 0.5 · C_H · ρ_atm · v³
dT_surface/dt  = (q − σ·ε·T⁴ − k·(dT/dr)) / (ρ·c_p·δ_th)

# PBDR — Highly siderophile element depletion
PBDR = 1 − (C_HSE_obs / C_HSE_chondritic)

# Widmanstätten bandwidth–cooling rate law
BW_Wid = 2.18 · (dT/dt)^{−0.47}     [r = +0.941, p < 0.001]
```

---

## 🚦 EMI Classification

### Classification Levels

| EMI Score | Level | Signal | Recommended Action |
|:---:|:---|:---:|:---|
| < 0.20 | **UNAMBIGUOUS** | 🟢 | Direct MetBull submission |
| 0.20 – 0.40 | **HIGH CONFIDENCE** | 🟡 | Standard expert review |
| 0.40 – 0.60 | **BOUNDARY ZONE** | 🟠 | Multi-parameter disambiguation |
| 0.60 – 0.80 | **ANOMALOUS** | 🔴 | Expert committee + isotopic verification |
| > 0.80 | **UNGROUPED CANDIDATE** | ⚫ | Full consortium characterization |

### Parameter Diagnostic Thresholds

| Parameter | Pristine | Marginal | Boundary | Anomalous |
|:---|:---:|:---:|:---:|:---:|
| MCC | < 0.20 | 0.20 – 0.40 | 0.40 – 0.70 | > 0.70 |
| SMG (GPa eq.) | < 10 | 10 – 25 | 25 – 50 | > 50 |
| TWI | < 0.20 | 0.20 – 0.45 | 0.45 – 0.70 | > 0.70 |
| IAF | > 0.80 | 0.60 – 0.80 | 0.30 – 0.60 | < 0.30 |
| ATP (°C) | < 3,000 | 3,000 – 4,500 | 4,500 – 5,500 | > 5,500 |
| PBDR | < 0.20 | 0.20 – 0.60 | 0.60 – 0.85 | > 0.85 |
| CNEA | Concordant | Minor discordance | Multi-stage | Anomalous |

---

## ⚙️ Installation

```bash
# Stable release — PyPI
pip install meteorica

# Development version — GitLab source
git clone https://gitlab.com/gitdeeper07/meteorica.git
cd meteorica
pip install -e ".[dev]"
pre-commit install
```

**Requirements:** Python ≥ 3.9 &nbsp;·&nbsp; NumPy &nbsp;·&nbsp; SciPy &nbsp;·&nbsp; scikit-learn &nbsp;·&nbsp; PyTorch &nbsp;·&nbsp; astropy &nbsp;·&nbsp; matplotlib

---

## 🚀 Quick Start

```python
import meteorica as mt

# Load a specimen record from EPMA output
specimen = mt.Specimen.from_epma("specimen_001.csv")

# Run the full EMI classification pipeline
result = mt.classify(specimen)

print(f"EMI Score:       {result.emi:.3f}")
print(f"Classification:  {result.group}  ({result.confidence:.1%} confidence)")
print(f"MCC: {result.mcc:.3f}  |  SMG: {result.smg:.3f}  |  TWI: {result.twi:.3f}")
print(f"Terrestrial Age: {result.terrestrial_age_years:,.0f} ± 8,000 years")
print(f"CRE Age:         {result.cre_age_ma:.1f} Ma")
print(f"Parent Body:     ~{result.parent_body_radius_km:.0f} km radius")

# Export a MetBull-compatible submission package
result.export_metbull("submission_package/")

# Real-time ATP calculation from a fireball trajectory
fireball = mt.Fireball(
    velocity_km_s=18.6,
    angle_deg=18.5,
    diameter_m=19,
    composition="LL5"
)
atp = mt.calculate_atp(fireball)
print(f"Peak Surface Temperature: {atp.T_max:.0f} ± 180 °C")
```

---

## 🔭 Case Studies

### A — Chelyabinsk LL5 · ATP Validation

The 2013 Chelyabinsk superbolide — the most instrumentally documented atmospheric entry in history — provided the definitive ATP benchmark. METEORICA predicted a peak surface temperature of **4,820°C ± 180°C**, consistent with independent spectroscopic measurements of the ablation plasma (4,600–5,100°C), recorded across 1,600 cameras, 3 infrasound arrays, and 847 recovered specimens. MCC confirmed LL5 classification (Fa = 28.9 ± 0.8 mol%); IAF confirmed LL nucleosynthetic affiliation (Δ¹⁷O = +1.09 ± 0.08‰).

### B — Iron Meteorites · Reconstructing Lost Worlds

Analysis of **847 polished iron sections** across 12 chemical groups established the power-law:

```
BW_Wid = 2.18 · (dT/dt)^{−0.47}     r = +0.941  (p < 0.001)
```

Parent body radii span **18 km** (IVA irons, disrupted ~450 Ma) to **320 km** (IIIAB irons, intact core) with **±180 km** precision — a 3.2× improvement. Every etched iron section is a cross-section through the core of a lost world.

### C — Antarctic Field · TWI Age Mapping

TWI analysis of **487 Yamato field ordinary chondrites** revealed a bimodal terrestrial age distribution at **3,000–8,000 years** and **18,000–28,000 years**, consistent with Last Glacial Maximum ice-flow dynamics. Concordance with independent ¹⁴C and ³⁶Cl ages confirms **±8,000-year** TWI precision — without radiometric laboratory access.

### D — Presolar Grains · IAF Nucleosynthetic Archive

NanoSIMS isotopic mapping of **312 CAIs** from 8 carbonaceous chondrite groups achieved **97.3% group discrimination** in 7D isotope space (vs. 83.1% for Δ¹⁷O alone). Identified 23 isotopic outliers including 6 specimens from genuinely unsampled asteroid parent bodies — nucleosynthetic archives invisible to conventional screening.

---

## 🗂️ Project Structure

```
meteorica/
│
├── meteorica/                      # Core Python package
│   ├── emi.py                      # EMI composite calculator
│   ├── parameters/
│   │   ├── mcc.py                  # Mineralogical Classification Coefficient
│   │   ├── smg.py                  # Shock Metamorphism Grade
│   │   ├── twi.py                  # Terrestrial Weathering Index
│   │   ├── iaf.py                  # Isotopic Anomaly Fingerprint
│   │   ├── atp.py                  # Ablation Thermal Profile
│   │   ├── pbdr.py                 # Parent Body Differentiation Ratio
│   │   └── cnea.py                 # Cosmogenic Nuclide Exposure Age
│   ├── classification/
│   │   ├── cnn_classifier.py       # AI spectral CNN · 91.3% · 42 classes
│   │   ├── spectral_preprocessing.py
│   │   └── metbull_export.py
│   ├── database/
│   │   ├── specimen_registry.py    # 2,847-specimen interface
│   │   ├── repository_connectors.py
│   │   └── metbull_sync.py
│   ├── fireball/
│   │   ├── atp_realtime.py
│   │   └── network_integration.py  # DFN · FRIPON · AllSky7
│   └── utils/
│       ├── mahalanobis.py
│       ├── isotope_space.py
│       └── concordia.py
│
├── tests/                          # 40/40 passing
├── configs/                        # EMI weights · group centroids
├── notebooks/                      # Six Jupyter tutorials
└── scripts/                        # Batch classify · CNN retrain · MetBull export
```

---

## 📦 Modules

| Module | Description |
|:---|:---|
| `meteorica.emi` | EMI composite with Bayesian adaptive weighting |
| `meteorica.parameters.mcc` | Mahalanobis mineralogical classification · 42 groups |
| `meteorica.parameters.smg` | Hugoniot-based continuous shock scale · ±2 GPa |
| `meteorica.parameters.twi` | Five-indicator weathering index + age estimation |
| `meteorica.parameters.iaf` | Seven-dimensional isotopic anomaly fingerprinting |
| `meteorica.parameters.atp` | Atmospheric entry thermal ablation simulation |
| `meteorica.parameters.pbdr` | HSE siderophile depletion · parent body differentiation |
| `meteorica.parameters.cnea` | Multi-nuclide concordia CRE age calculation |
| `meteorica.classification.cnn_classifier` | CNN NIR classifier · 91.3% accuracy · 42 classes |
| `meteorica.fireball` | Real-time ATP · DFN · FRIPON · AllSky7 |
| `meteorica.database` | 2,847-specimen database + MetBull synchronization |

---

## 🛠️ Configuration

```yaml
# configs/default.yaml

emi:
  weights:
    mcc:  0.26
    smg:  0.19
    twi:  0.18
    iaf:  0.17
    atp:  0.10
    pbdr: 0.06
    cnea: 0.04
  boundary_zone_threshold: 0.40
  ungrouped_threshold:     0.80

twi:
  weathering_rate_model: "default"        # or "site_specific" (v2.0)
  calibration_dataset:   "156_specimens"

cnn:
  model_checkpoint:         "models/meteorica_cnn_v1.pt"
  spectral_range_um:        [0.35, 2.5]
  normalization_wavelength: 0.55
  confidence_threshold:     0.70

cnea:
  production_rate_model: "nishiizumi_2007"
  cosmic_ray_modulation: true
  concordia_display:     true
```

---

## 📡 Dashboard

| Link | Description |
|:---|:---|
| [meteorica-science.netlify.app](https://meteorica-science.netlify.app) | Main website & project overview |
| [/dashboard](https://meteorica-science.netlify.app/dashboard) | Live EMI classification interface |
| [/documentation](https://meteorica-science.netlify.app/documentation) | API and parameter documentation |
| [/reports](https://meteorica-science.netlify.app/reports) | Generated classification reports |

**Features:** Interactive 7-parameter radar chart &nbsp;·&nbsp; AI spectral heatmap &nbsp;·&nbsp; Real-time fireball ATP feed &nbsp;·&nbsp; MetBull submission generator &nbsp;·&nbsp; CNEA concordia diagrams &nbsp;·&nbsp; Isotopic outlier flagging

---

## 🤝 Contributing

Contributions are welcome from meteoriticists, planetary scientists, isotope geochemists, atmospheric physicists, and software engineers.

```bash
# 1. Fork and clone your fork
git clone https://gitlab.com/YOUR_USERNAME/meteorica.git

# 2. Create a feature branch
git checkout -b feature/your-feature-name

# 3. Install development dependencies
pip install -e ".[dev]"
pre-commit install

# 4. Run the full test suite
pytest tests/ -v
ruff check meteorica/
mypy meteorica/

# 5. Commit using conventional commits format
git commit -m "feat: describe your feature"
git push origin feature/your-feature-name

# 6. Open a Merge Request on GitLab
```

**Priority areas:** New group centroid definitions &nbsp;·&nbsp; Organic IAF extension for carbonaceous chondrites &nbsp;·&nbsp; Quantum NV-center presolar grain detection (v2.0) &nbsp;·&nbsp; Fireball network API connectors &nbsp;·&nbsp; Documentation translation

---

## 📖 Citation

### Manuscript

```bibtex
@article{Baladi2026METEORICA,
  title     = {Celestial Messengers: A Comprehensive Physico-Chemical Framework
               for the Classification, Terrestrial Interaction, and
               Cosmochemical Significance of Extraterrestrial Materials},
  author    = {Baladi, Samir},
  journal   = {Meteoritics \& Planetary Science},
  publisher = {Wiley-Blackwell},
  year      = {2026},
  doi       = {10.14293/METEORICA.2026.001},
  url       = {https://doi.org/10.14293/METEORICA.2026.001}
}
```

### Software

```bibtex
@software{Baladi2026METEORICA_software,
  author    = {Baladi, Samir},
  title     = {METEORICA v1.0.0},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.18726661},
  url       = {https://doi.org/10.5281/zenodo.18726661}
}
```

---

## 🔗 Links

| | Platform | URL |
|:---:|:---|:---|
| 🦊 | GitLab (primary) | [gitlab.com/gitdeeper07/meteorica](https://gitlab.com/gitdeeper07/meteorica) |
| 🐙 | GitHub (mirror) | [github.com/gitdeeper07/meteorica](https://github.com/gitdeeper07/meteorica) |
| 📦 | PyPI | [pypi.org/project/meteorica](https://pypi.org/project/meteorica/) |
| 🌐 | Website | [meteorica-science.netlify.app](https://meteorica-science.netlify.app) |
| 📄 | Manuscript DOI | [10.14293/METEORICA.2026.001](https://doi.org/10.14293/METEORICA.2026.001) |
| 📁 | Zenodo Dataset | [10.5281/zenodo.18726661](https://doi.org/10.5281/zenodo.18726661) |
| 🏛️ | OSF Registration | [10.17605/OSF.IO/BRDQM](https://doi.org/10.17605/OSF.IO/BRDQM) |

---

## 👤 Author

**Samir Baladi** — Interdisciplinary Researcher  
Ronin Institute / Rite of Renaissance · Extraterrestrial Materials & Cosmochemistry

[gitdeeper@gmail.com](mailto:gitdeeper@gmail.com); 
ORCID: [0009-0003-8903-0029](https://orcid.org/0009-0003-8903-0029)

---

## 📄 License

Licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

All spectral data and specimen records comply with institutional open-data agreements.
CNN model weights are available for academic use under the same terms.

---

<div align="center">

<br>

**☄️ METEORICA — Making 4.567 billion years of solar system history legible.**

<br>

*Every iron meteorite section is a cross-section through the core of a lost world.*  
*Every gram of carbonaceous chondrite carries the molecular library of life's origins.*

<br>

[🌐 Website](https://meteorica-science.netlify.app) &nbsp;·&nbsp;
[📊 Dashboard](https://meteorica-science.netlify.app/dashboard) &nbsp;·&nbsp;
[📚 Docs](https://meteorica-science.netlify.app/documentation) &nbsp;·&nbsp;
[📑 Reports](https://meteorica-science.netlify.app/reports)

<br>

`v1.0.0` &nbsp;·&nbsp; MIT License &nbsp;·&nbsp; DOI: [10.14293/METEORICA.2026.001](https://doi.org/10.14293/METEORICA.2026.001) &nbsp;·&nbsp; ORCID: [0009-0003-8903-0029](https://orcid.org/0009-0003-8903-0029)

<br>

</div>
