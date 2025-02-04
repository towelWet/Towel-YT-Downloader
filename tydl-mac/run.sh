#!/bin/bash

# Get the directory where the script is running (should be in MacOS)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
RESOURCES_DIR="${SCRIPT_DIR}/../Resources"

# Add Resources directory to PATH so yt-dlp can be found
export PATH="${RESOURCES_DIR}:$PATH"

# Ensure yt-dlp exists and is executable
if [ ! -f "${RESOURCES_DIR}/yt-dlp" ]; then
    echo "Error: yt-dlp not found at ${RESOURCES_DIR}/yt-dlp"
    exit 1
fi
chmod +x "${RESOURCES_DIR}/yt-dlp"

# Change to Resources directory
cd "$RESOURCES_DIR"

# Make main program executable and run it
chmod +x "./Towel YT Downloader"
"./Towel YT Downloader"