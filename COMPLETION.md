# PALMA Shell Completion

PALMA provides shell completion for bash, zsh, and fish shells to enhance command-line productivity.

## Installation

### Bash

Add to your `~/.bashrc`:
```bash
eval "$(_PALMA_COMPLETE=bash_source palma)"
```

Zsh

Add to your ~/.zshrc:

```zsh
eval "$(_PALMA_COMPLETE=zsh_source palma)"
```

Fish

Add to your ~/.config/fish/config.fish:

```fish
eval (env _PALMA_COMPLETE=fish_source palma)
```

Available Commands

```bash
palma --help
```

Core Commands

Command Description
palma compute Compute PALMA parameters
palma monitor Run monitoring pipeline
palma dashboard Launch dashboard
palma sites List monitoring sites
palma alerts Check active alerts
palma export Export data

Parameter Commands

```bash
palma compute arvc      # Aquifer Recharge Velocity
palma compute ptsi      # Phyto-Thermal Shielding
palma compute sssp      # Soil Salinity Stress
palma compute cmbf      # Canopy Microclimate
palma compute svri      # Spectral Vegetation
palma compute wepr      # Water-Energy Partition
palma compute bst       # Biodiversity Stability
palma compute ohi       # Oasis Health Index
```

Options

```bash
--site SITE           # Specify site name or ID
--start-date DATE     # Start date (YYYY-MM-DD)
--end-date DATE       # End date (YYYY-MM-DD)
--format FORMAT       # Output format (json, csv, table)
--output FILE         # Output file path
--config FILE         # Configuration file
--verbose            # Verbose output
--debug              # Debug mode
```

Examples

```bash
# Compute OHI for Draa Valley
palma compute ohi --site draa_valley

# Monitor with custom config
palma monitor --config config/palma.local.yaml

# Export data as JSON
palma export --site al_ahsa --format json --output data.json

# Check alerts for all sites
palma alerts --status active

# List all sites
palma sites --tier 1

# Run pipeline for specific date
palma pipeline run --date 2026-02-19
```

Tab Completion Features

The completion system provides:

· Command name completion
· Site name completion (from config/sites/)
· Date completion (YYYY-MM-DD format)
· File path completion for --output
· Format completion (json, csv, table)

Troubleshooting

If completion isn't working:

1. Ensure palma is installed: which palma
2. Reload shell: exec $SHELL
3. Check installation: palma --version
4. Reinstall completions: re-run the eval command

For more help: palma help completion
