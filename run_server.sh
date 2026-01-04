#!/bin/bash

echo "Starting Action Recognition Server..."
echo ""
echo "Make sure you have:"
echo "1. Activated your virtual environment"
echo "2. Installed all dependencies (pip install -r requirements.txt)"
echo "3. Placed cnn_lstm_action.h5 in the models/ directory"
echo ""
read -p "Press enter to continue..."

uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000

