#!/bin/bash

echo "Installing frontend (npm) dependencies..."
npm install

echo "Installing backend (Python) dependencies..."
cd housingdata/src/backend
python3 -m venv .venv
source .venv/bin/activate
pip install flask flask-cors

echo "Setup complete! You can now run the servers."