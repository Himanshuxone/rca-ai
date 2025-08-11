#!/bin/bash

# Usage:
# ./restart.sh          -> Quick restart (no rebuild)
# ./restart.sh rebuild  -> Full restart with rebuild

if [ "$1" == "rebuild" ]; then
    echo "🔄 Full rebuild and restart of Backend & Frontend..."
    docker-compose build backend frontend
    docker-compose up -d backend frontend
    echo "✅ Full rebuild complete!"
else
    echo "⚡ Quick restart of Backend & Frontend..."
    docker-compose restart backend frontend
    echo "✅ Quick restart complete!"
fi
