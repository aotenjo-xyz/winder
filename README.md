# winder

[![BLDC motor winding machine](http://img.youtube.com/vi/486nUU2FjGU/0.jpg)](http://www.youtube.com/watch?v=486nUU2FjGU "BLDC Motor Winding Machine")

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

## Prerequisites

- [Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/main): Download and install Miniconda for your operating system.

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

4. Activate the conda environment:
   ```bash
   conda activate winding
   export PYTHONPATH=$PWD
   ```

5. Create a `settings.yml` file based on `settings_example.yml` and update the settings as needed.
   ```bash
   cp settings_example.yml settings.yml
   ```


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