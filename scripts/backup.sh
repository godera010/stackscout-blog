#!/usr/bin/env bash
# backup.sh - Create timestamped SQLite backup
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKUP_DIR="$SCRIPT_DIR/../backups"
DATA_DIR="$SCRIPT_DIR/../instatic-data/data"
TIMESTAMP=$(date +"%Y-%m-%d-%H%M%S")

mkdir -p "$BACKUP_DIR"

DB_FILE="$DATA_DIR/cms.db"

if [ ! -f "$DB_FILE" ]; then
  echo "ERROR: Database file not found at $DB_FILE"
  echo "  Is the CMS running? Start with: docker compose -f compose.prod.yml -f compose.sqlite.yml up -d"
  exit 1
fi

BACKUP_FILE="$BACKUP_DIR/cms-$TIMESTAMP.db"

echo "==> Backing up SQLite database..."
cp "$DB_FILE" "$BACKUP_FILE"

if [ -f "$DB_FILE-wal" ]; then
  cp "$DB_FILE-wal" "$BACKUP_FILE-wal" 2>/dev/null || true
fi
if [ -f "$DB_FILE-shm" ]; then
  cp "$DB_FILE-shm" "$BACKUP_FILE-shm" 2>/dev/null || true
fi

echo "==> Backup created: $BACKUP_FILE"
echo "==> Size: $(du -h "$BACKUP_FILE" | cut -f1)"
