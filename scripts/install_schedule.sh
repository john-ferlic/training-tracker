#!/usr/bin/env bash
# Install a macOS LaunchAgent that runs the daily briefing.
#
# Usage:   scripts/install_schedule.sh [HOUR] [MINUTE]
# Example: scripts/install_schedule.sh 6 30      # 6:30 AM daily (default)
#
# Uninstall:  launchctl unload ~/Library/LaunchAgents/com.trainingtracker.daily.plist
#             rm ~/Library/LaunchAgents/com.trainingtracker.daily.plist
set -euo pipefail

HOUR="${1:-6}"
MINUTE="${2:-30}"

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON="$DIR/.venv/bin/python3"
LABEL="com.trainingtracker.daily"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
LOGDIR="$DIR/data/logs"

if [ ! -x "$PYTHON" ]; then
  echo "No venv found at $PYTHON"
  echo "Create it first:"
  echo "  python3 -m venv \"$DIR/.venv\" && \"$DIR/.venv/bin/pip\" install -r \"$DIR/requirements.txt\""
  exit 1
fi

mkdir -p "$LOGDIR" "$HOME/Library/LaunchAgents"

cat > "$PLIST" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>$LABEL</string>
    <key>ProgramArguments</key>
    <array>
        <string>$PYTHON</string>
        <string>-m</string>
        <string>trainingtracker</string>
        <string>run</string>
    </array>
    <key>WorkingDirectory</key>
    <string>$DIR</string>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>$HOUR</integer>
        <key>Minute</key>
        <integer>$MINUTE</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>$LOGDIR/daily.out.log</string>
    <key>StandardErrorPath</key>
    <string>$LOGDIR/daily.err.log</string>
    <key>RunAtLoad</key>
    <false/>
</dict>
</plist>
PLIST

# Reload if already installed.
launchctl unload "$PLIST" 2>/dev/null || true
launchctl load -w "$PLIST"

printf 'Installed LaunchAgent %s — runs daily at %02d:%02d.\n' "$LABEL" "$HOUR" "$MINUTE"
echo "Plist:  $PLIST"
echo "Logs:   $LOGDIR/daily.{out,err}.log"
echo
echo "Test it now without waiting:   launchctl start $LABEL"
echo "Then check:                    cat \"$LOGDIR/daily.err.log\""
