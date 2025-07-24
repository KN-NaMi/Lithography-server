#!/bin/bash

URL="http://localhost:8000/stream"

BROWSER_CMD="chromium-browser --no-sandbox --kiosk $URL"

LOGFILE="$HOME/browser_watchdog.log"

function is_monitor_connected() {
    xrandr | grep " connected" | grep -v "disconnected" > /dev/null
    return $?
}

echo "=== Viewer Start $(date) ===" | tee -a "$LOGFILE"

while true; do
    if is_monitor_connected; then
        if ! pgrep -f "chromium" > /dev/null; then
            echo "$(date): Monitor connected. Starting Chromium..." | tee -a "$LOGFILE"
            $BROWSER_CMD >> "$LOGFILE" 2>&1 &
        fi
    else
        if pgrep -f "chromium" > /dev/null; then
            echo "$(date): Monitor disconnected. Closing Chromium..." | tee -a "$LOGFILE"
            pkill -f chromium
        else
            echo "$(date): Monitor disconnected. Waiting..." | tee -a "$LOGFILE"
        fi
    fi
    sleep 5
done
