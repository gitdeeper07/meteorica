# Installation

## From PyPI

```bash
pip install meteorica
```

From Source

```bash
git clone https://gitlab.com/gitdeeper07/meteorica.git
cd meteorica
pip install -e ".[dev]"
```

Requirements

· Python ≥ 3.9
· NumPy ≥ 1.24.0
· SciPy ≥ 1.10.0
· scikit-learn ≥ 1.3.0
· PyTorch ≥ 2.0.0 (for CNN classifier)
· astropy ≥ 5.3.0

Development Installation

For development, install with all extras:

```bash
pip install -e ".[dev,docs,dashboard]"
pre-commit install
```

