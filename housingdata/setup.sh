#!/bin/bash

echo "Installing frontend (npm) dependencies..."
npm install --production

echo "Installing backend (Python) dependencies..."
pip install -r requirements.txt

echo "Setup complete! You can now run the servers."