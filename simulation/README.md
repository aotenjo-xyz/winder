# Simulation with Godot

## Overview
scripts/main.py: This script initializes and runs the winding machine motor control program and store motor data to sqlite database.

scripts/ws.py: This script implements a WebSocket server to stream motor data to Godot.

## Prerequisites

- [Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/main): Download and install Miniconda for your operating system.
- [Godot](https://godotengine.org/download): Download and install the latest stable version of Godot.

## Installation
1. Clone the Winder repository:
   ```bash
   git clone https://github.com/aotenjo-xyz/winder.git
   ```
2. Navigate to the project directory:
   ```bash
   cd winder
   ```
3. Create a new conda environment and install the required dependencies:
   ```bash
   conda env create -f scripts/environment.yml
   ```

## Quickstart
1. Activate the conda environment:
   ```bash
   conda activate winding
   ```
2. Run the winding script in simulation mode:
   ```bash
   export PYTHONPATH=$PWD
   python scripts/main.py -s
   ```
3. Open a new terminal, activate the conda environment, and run the websocket server to communicate with Godot:
   ```bash
   conda activate winding
   export PYTHONPATH=$PWD
   python scripts/ws.py
   ```
4. Open Godot and import the project:
   - Open Godot and click on "Import".
   - Select the `winder/simulation` directory you cloned earlier.
   - Click "Import & Edit".
5. Run the simulation:
   - In Godot, click on the "Play" button (triangle icon) at the top right corner to start the simulation.
   - You should see the winding machine simulation in action.
6. Enter `g` in the terminal running `main.py` to start the winding process in the simulation.