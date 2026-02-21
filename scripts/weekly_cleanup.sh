#!/bin/bash
# Weekly cleanup - archive old reports

DAYS=30
ARCHIVE_DIR="./reports/archive/$(date +%Y-%m)"
mkdir -p "$ARCHIVE_DIR"

echo "Archiving reports older than $DAYS days..."

# Archive old daily reports
find ./reports/daily -name "*.md" -type f -mtime +$DAYS -exec mv {} "$ARCHIVE_DIR/" \;

# Archive old JSON exports
find ./reports/exports/json -name "*.json" -type f -mtime +$DAYS -exec mv {} "$ARCHIVE_DIR/" \;

echo "Cleanup complete!"
