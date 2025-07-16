#!/bin/bash

echo "🔧 Starting TechRCA Dev Environment..."

# Step 1: Activate Python backend (FastAPI)
echo "🚀 Launching FastAPI backend..."
cd backend || exit
uvicorn main:app --reload &

# Step 2: Start React frontend
echo "🖥️  Launching React frontend..."
cd ../frontend || exit
npm install
npm start

# Tip: Use 'killall uvicorn' to stop the backend after exiting
