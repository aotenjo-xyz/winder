# winder
[![Docs](https://img.shields.io/badge/Docs-aotenjo.xyz-blue?style=flat-square)](https://aotenjo.xyz/docs/winder/overview) | [![YouTube](https://img.shields.io/badge/YouTube-red?style=flat-square&logo=youtube)](https://www.youtube.com/@yuchi0.1) | [![TikTok](https://img.shields.io/badge/TikTok-black?style=flat-square&logo=tiktok)](https://www.tiktok.com/@yuchi0.1) | [![Instagram](https://img.shields.io/badge/Instagram-E1306C?style=flat-square&logo=instagram)](https://www.instagram.com/aotenjo.xyz) | [![X](https://img.shields.io/badge/X-000000?style=flat-square&logo=x)](https://x.com/aotenjo_xyz)

[![BLDC motor winding machine](http://img.youtube.com/vi/-ggH2UGuAuA/0.jpg)](http://www.youtube.com/watch?v=-ggH2UGuAuA "BLDC Motor Winding Machine")

Winding the wire for a BLDC motor is a time-consuming and labor-intensive process. This winding machine automates this tedious tasks.

## Motors
This machine uses four motors to perform the winding operation:
<img src="/.github/images/motor-name.jpg" alt="Motor name" width="500"/>

- **M0**: Move M1 unit (closed loop control)
- **M1**: Rotate the stator (closed loop control)
- **M2**: Wind the wire (closed loop control)
- **M3**: Adjust the wire tension (closed loop torque control using voltage)

code: [Aotenjo One](https://github.com/aotenjo-xyz/one)

## Master Controller
All motors are controlled by Aotenjo Master, a master controller board based on the STM32G431CBU6 microcontroller. It communicates with the host computer via USB and controls the motors via CAN bus.

<img src="/.github/images/master-diagram.png" alt="Master Diagram" width="500"/>

code: [Aotenjo Master](https://github.com/aotenjo-xyz/master)

## Installation

You can set up the environment with either conda or
[uv](https://docs.astral.sh/uv/). Both install the same pinned dependency
versions.

### Option A — conda

Prerequisite: [Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/main).

1. Clone the Winder repository and enter it:
   ```bash
   git clone https://github.com/aotenjo-xyz/winder.git
   cd winder
   ```
2. Create a new conda environment and install the required dependencies:
   ```bash
   conda env create -f environment.yml
   ```
3. Activate the conda environment:
   ```bash
   conda activate winding
   export PYTHONPATH=$PWD
   ```
4. Create a `settings.yml` file based on `settings-example.yml` and update the
   settings as needed:
   ```bash
   cp settings-example.yml settings.yml
   ```

### Option B — uv

Prerequisite: [install uv](https://docs.astral.sh/uv/getting-started/installation/).

1. Clone the Winder repository and enter it:
   ```bash
   git clone https://github.com/aotenjo-xyz/winder.git
   cd winder
   ```
2. Create the virtual environment and install all dependencies (uv installs
   Python 3.12 automatically if needed):
   ```bash
   uv sync
   ```
3. Create a `settings.yml` file based on `settings-example.yml` and update the
   settings as needed:
   ```bash
   cp settings-example.yml settings.yml
   ```

That's it — no need to set `PYTHONPATH`. Run any command inside the environment
with `uv run`, e.g. `uv run python scripts/main.py -s` or `uv run pytest`.


## Hardware
- M0: BE4108 75T gimbal motor (built with this machine)
- M1: BE4108 75T gimbal motor (built with this machine)
- M2: BE4108 75T gimbal motor (built with this machine)
- M3: BE4108 60T gimbal motor (built with this machine)

## Result
BE4108 75T gimbal motor

<img src="/.github/images/result.png" alt="Result" width="500"/>

This motor was initially a drone motor.


[![Drone motor vs DIY gimbal motor](http://img.youtube.com/vi/56WxTAfKFDU/0.jpg)](https://www.youtube.com/shorts/56WxTAfKFDU "Drone motor vs DIY gimbal motor")

## Simulation with Godot

[Quickstart](simulation/README.md)

[![Simulation with Godot](http://img.youtube.com/vi/92i8CDEzeJ8/0.jpg)](https://www.youtube.com/watch?v=92i8CDEzeJ8 "Simulation with Godot")

See [simulation/README.md](simulation/README.md) for details.