# winder

[![BLDC motor winding machine](http://img.youtube.com/vi/486nUU2FjGU/0.jpg)](http://www.youtube.com/watch?v=486nUU2FjGU "BLDC Motor Winding Machine")

Winding the wire for a BLDC motor is a time-consuming and labor-intensive process. This winding machine automates this tedious tasks.

## Motors
This machine uses four motors to perform the winding operation:
<img src="/.github/images/motor-name.png" alt="Motor name" width="500"/>

- **M0**: Move M1 unit (closed loop control)
- **M1**: Rotate the stator (closed loop control)
- **M2**: Wind the wire (closed loop control)
- **M3**: Adjust the wire tension (closed loop torque control using voltage)

code: [Aotenjo One](https://github.com/aotenjo-xyz/one)

## Master Controller
All motors are controlled by Aotenjo Master, a master controller board based on the STM32G431CBU6 microcontroller. It communicates with the host computer via USB and controls the motors via CAN bus.

<img src="/.github/images/master-diagram.png" alt="Master Diagram" width="500"/>

code: [Aotenjo Master](https://github.com/aotenjo-xyz/master)

## Power Supply
Power supply: 18V 1.5A

## Hardware
- M0: GBM5208 gimbal motor or BE4108 75T gimbal motor (built with this machine)
- M1: GBM5208 gimbal motor
- M2: GBM5208 gimbal motor
- M3: BE4108 60T gimbal motor (built with this machine)

## Result
BE4108 75T gimbal motor

<img src="/.github/images/result.png" alt="Result" width="500"/>

This motor was initially a drone motor.


[![Drone motor vs DIY gimbal motor](http://img.youtube.com/vi/56WxTAfKFDU/0.jpg)](https://www.youtube.com/shorts/56WxTAfKFDU "Drone motor vs DIY gimbal motor")

## Simulation with Godot

[![Simulation with Godot](http://img.youtube.com/vi/1gFa7yNvHWc/0.jpg)](https://www.youtube.com/shorts/1gFa7yNvHWc "Simulation with Godot")

See [simulation/README.md](simulation/README.md) for details.