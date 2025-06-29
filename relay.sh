#!/bin/bash

# ============== CONFIGURATION ==============
PORT1=13370 # Target connects here
PORT2=8081  # Controller connects here
# ===========================================

# --- Script-generated variables ---
PIPE="/tmp/socat_relay_pipe_$$"

# --- Cleanup function ---
cleanup() {
    echo -e "\nCleaning up pipe and background processes..."
    rm -f "$PIPE"
    # Kill all background jobs started by this script
    kill $(jobs -p) 2>/dev/null
    echo "Cleanup complete."
}
trap cleanup EXIT

# --- Main execution ---
echo "Starting robust socat relay..."
echo "  - Target Port (PORT1): $PORT1"
echo "  - Controller Port (PORT2): $PORT2"

# Create the named pipe
mkfifo "$PIPE"

# -d -d provides debug-level logging to stderr
# TCP-LISTEN: fork allows multiple clients, reuseaddr allows fast restarts
# GOPEN:"$PIPE" creates a bidirectional connection to the named pipe

# Process A: Listens on Target Port, relays to/from pipe
echo "[Relay] Starting listener on port $PORT1..."
socat -d -d TCP-LISTEN:$PORT1,fork,reuseaddr GOPEN:"$PIPE" &

# Process B: Listens on Controller Port, relays to/from pipe
echo "[Relay] Starting listener on port $PORT2..."
socat -d -d TCP-LISTEN:$PORT2,fork,reuseaddr GOPEN:"$PIPE" &

echo "[Relay] Relay is running. Press Ctrl+C to stop."
# The 'wait' command will pause the script here, keeping it alive while background jobs run.
wait
