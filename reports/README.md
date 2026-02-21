# METEORICA Reports System

## Directory Structure

```

reports/
├── daily/           # Daily reports - new classifications, fireballs
├── weekly/          # Weekly reports - statistics, analysis
├── monthly/         # Monthly reports - summaries, trends
├── alerts/          # Alerts - important events, discoveries
├── archive/         # Archived old reports
├── exports/         # Exported copies in different formats
│   ├── json/       # JSON copies for automated processing
│   ├── csv/        # CSV copies for spreadsheets
│   └── metbull/    # MetBull-compatible exports
└── templates/       # Report templates

```

## Report Types

### Daily Reports 📅
- New meteorite classifications
- Recorded fireball events
- Database updates
- Immediate alerts

### Weekly Reports 📆
- Classification statistics
- Group analysis
- Weekly discoveries
- Project progress

### Monthly Reports 📊
- Monthly summary
- Trends and discoveries
- Advanced statistics
- Next month plans

### Alerts ⚠️
- Ungrouped meteorites
- Large fireball events
- Important updates
- Classification errors

## Export System

All important reports are copied to `exports/` in:
- **JSON**: For automated analysis
- **CSV**: For spreadsheets
- **MetBull**: For database compatibility

## Naming Convention

- Daily: `YYYY-MM-DD_daily.{txt,md,json}`
- Weekly: `YYYY-Www_weekly.{txt,md,json}` (ww = week number)
- Monthly: `YYYY-MM_monthly.{txt,md,json}`
- Alerts: `alert_YYYYMMDD_HHMMSS_{type}.{txt,md,json}`

## Usage Example

```python
from reports.generator import ReportGenerator

# Generate daily report
gen = ReportGenerator()
gen.daily_report()

# Export as JSON
gen.export_json("daily/2026-02-20.json")

# Create alert
gen.alert("Ungrouped meteorite detected", "high")
```

