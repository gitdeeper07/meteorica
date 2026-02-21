#!/bin/bash
# Script to export reports to different formats

REPORTS_DIR="./reports"
EXPORTS_DIR="./reports/exports"
DATE=$(date +%Y-%m-%d)

echo "Exporting reports to $EXPORTS_DIR..."

# Export daily reports to JSON
for report in $REPORTS_DIR/daily/*.md; do
    if [ -f "$report" ]; then
        filename=$(basename "$report" .md)
        echo "Exporting $filename to JSON..."
        # Convert markdown to JSON (simplified)
        echo "{\"report\": \"$filename\", \"exported\": \"$DATE\"}" > "$EXPORTS_DIR/json/$filename.json"
    fi
done

# Export to MetBull format
echo "Creating MetBull exports..."
cp $REPORTS_DIR/daily/*.md $EXPORTS_DIR/metbull/ 2>/dev/null || true

echo "Export complete!"
