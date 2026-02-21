# METEORICA Scripts

## Available Scripts

### `generate_reports.py`
Generate daily, weekly, and monthly reports.
```bash
python scripts/generate_reports.py --daily
python scripts/generate_reports.py --weekly
python scripts/generate_reports.py --monthly
python scripts/generate_reports.py --archive 30
```

alert_manager.py

Manage alerts and notifications.

```bash
python scripts/alert_manager.py list
python scripts/alert_manager.py resolve alert_20260220_123456_ungrouped
```

export_reports.sh

Export reports to different formats.

```bash
./scripts/export_reports.sh
```

daily_copy.sh

Daily copy of JSON files to exports.

```bash
./scripts/daily_copy.sh
```

weekly_cleanup.sh

Weekly cleanup and archiving.

```bash
./scripts/weekly_cleanup.sh
```

Automated Tasks (Cron)

Add to crontab for automation:

```
# Daily report at 23:59
59 23 * * * cd /path/to/meteorica && python scripts/generate_reports.py --daily

# Weekly report every Sunday at 23:59
59 23 * * 0 cd /path/to/meteorica && python scripts/generate_reports.py --weekly

# Monthly report on 1st at 23:59
59 23 1 * * cd /path/to/meteorica && python scripts/generate_reports.py --monthly

# Daily copy at 00:05
5 0 * * * cd /path/to/meteorica && ./scripts/daily_copy.sh

# Weekly cleanup at 01:00 on Sunday
0 1 * * 0 cd /path/to/meteorica && ./scripts/weekly_cleanup.sh
```

