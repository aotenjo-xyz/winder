# Simulation with Godot

## Overview
[![Simulation with Godot](http://img.youtube.com/vi/92i8CDEzeJ8/0.jpg)](https://www.youtube.com/shorts/92i8CDEzeJ8 "Simulation with Godot")

[Tutorial Video](https://www.youtube.com/watch?v=92i8CDEzeJ8)

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
   conda env create -f environment.yml
   ```

## Build

Export the Godot project to a standalone binary (no Godot editor required to run):

```bash
conda activate winding
export PYTHONPATH=$PWD
make export-simulation
```

This produces `simulation/bin/simulation.x86_64`. Export templates must be installed in Godot beforehand (`Editor → Manage Export Templates`).

### Build for other platforms

The Makefile supports preset-driven exports:

```bash
make export-simulation-linux
make export-simulation-windows
make export-simulation-macos
```

Equivalent generic form:

```bash
make export-simulation SIM_EXPORT_PRESET="Windows" SIM_EXPORT_PATH="bin/simulation.exe"
make export-simulation SIM_EXPORT_PRESET="macOS" SIM_EXPORT_PATH="bin/simulation.app"
```

Important: Godot must have matching export presets named `Linux`, `Windows`, and `macOS` in `simulation/export_presets.cfg`. These presets are included in this repository; if you edit them in Godot (`Project -> Export`), save the updated file.

Notes:
- Windows export from Linux/macOS usually works with templates only.
- macOS export can be produced on Linux, but signing and notarization typically require macOS tooling.

### Godot executable setup

The Makefile uses `godot` by default. For team portability, avoid committing machine-specific paths.

Option 1 (recommended): add Godot to your `PATH`, then use:

```bash
make export-simulation
```

Option 2 (one-off override):

```bash
make GODOT="/absolute/path/to/Godot_v4.6.3-stable_linux.x86_64" export-simulation
```

Option 3 (local persistent override): create an untracked `.make.local` file in the repository root:

```make
GODOT := /absolute/path/to/Godot_v4.6.3-stable_linux.x86_64
```

Then run:

```bash
make export-simulation
```

## Quickstart (built binary)

After building, run the interactive controller and simulation as separate processes.

Terminal 1 (interactive controller):

```bash
conda activate winding
export PYTHONPATH=$PWD
python scripts/main.py -s
```

Terminal 2 (WebSocket bridge):

```bash
conda activate winding
export PYTHONPATH=$PWD
python scripts/ws.py
```

Terminal 3 (simulation window):

```bash
conda activate winding
export PYTHONPATH=$PWD
make simulate
```

`make simulate` launches the exported simulation binary only. Use the terminal running `main.py` to select `wind wires` and continue through the interactive prompts.

## Quickstart (Godot editor)

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
6. Select `wind wires` and follow the prompts in the terminal to start the winding process in the simulation.