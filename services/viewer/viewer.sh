#!/bin/bash

URL="http://localhost:83000/stream"
BROWSER_CMD="chromium --kiosk --app=$URL"

function is_monitor_connected() {
    xrandr | grep " connected" | grep -v "disconnected" > /dev/null
    return $?
}

echo "=== Viewer Start $(date) ===" | tee -a "$LOGFILE"

while true; do
    if is_monitor_connected; then
        if ! pgrep -f "chromium" > /dev/null; then
            $BROWSER_CMD &
        fi
    else
        if pgrep -f "chromium" > /dev/null; then
            pkill -f chromium
        else
    fi
    sleep 5
done
