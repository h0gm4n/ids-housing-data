#!/bin/bash

echo "Installing frontend (npm) dependencies..."
npm install

echo "Installing backend (Python) dependencies..."
pip install -r requirements.txt

echo "Setup complete! You can now run the servers."