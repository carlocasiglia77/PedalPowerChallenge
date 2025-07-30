#!/bin/bash

# Wait for network + services (like InfluxDB or Grafana) to start
sleep 10

# Hide the cursor after 0.1s of inactivity
unclutter -idle 0.1 -root &

# Start the Python game in background
cd ~/PedalPowerChallenge
source pedalpower/bin/activate
python -m app.main_demo

# Open Firefox to Grafana dashboard in kiosk mode
sleep 5  # Give the game a head start
firefox --private-window --kiosk "http://localhost:3000/d/60577e3d-3ba3-4d42-9af6-8a2f73bc263a/new-dashboard?orgId=1&from=now-6h&to=now&timezone=browser&refresh=500ms&kiosk=1"