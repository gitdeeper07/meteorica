#!/bin/bash
# Daily copy script - copies JSON files to exports

DATE=$(date +%Y-%m-%d)
SOURCE_DIR="./reports/exports/json"
DEST_DIR="./reports/exports/archive/$DATE"

mkdir -p "$DEST_DIR"

echo "Copying JSON files to $DEST_DIR..."

# Copy all JSON files
cp "$SOURCE_DIR"/*.json "$DEST_DIR/" 2>/dev/null

# Create a copy with date suffix
for file in "$SOURCE_DIR"/*.json; do
    if [ -f "$file" ]; then
        basename=$(basename "$file" .json)
        cp "$file" "$SOURCE_DIR/${basename}_${DATE}.json"
    fi
done

echo "Daily copy complete!"
