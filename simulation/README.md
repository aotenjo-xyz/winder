# Simulation with Godot

## Overview
scripts/main.py: This script initializes and runs the winding machine motor control program and store motor data to sqlite database.

scripts/ws.py: This script implements a WebSocket server to stream motor data to Godot.

## Requirements
- Install Godot
- Install Miniconda or Anaconda

## Quick Start
1. Import this project into Godot.
2. Create a conda environment using the provided `environment.yml` file:
   ```bash
   make create-env
   ```
3. Run `scripts/main.py` to start the motor control program and `scripts/ws.py` to start the WebSocket server.
4. In Godot, run the project to visualize the winding machine simulation.

## Motivation
This will let people test and develop software without needing the hardware first.