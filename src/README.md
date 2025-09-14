## Usage

### 1. Install dependencies
```bash
conda env create -f environment.yml
```

### 2. Activate the environment
```bash
conda activate winding
cd scripts
```

### 3. Calibrate the motors
Before running the script, you need to calibrate the motors. This is done by running the
```bash
python calib.py
```

Update `scripts/settings.yml` with the calibration values.

### 4. Run the script
```bash
python main.py
```

To wind wire A, enter 'k' when prompted.   
To wind wire B, enter 'j'.   
To wind wire C, enter 'h'.  
To stop all motors (Emergency Stop), enter 'e'.  
To exit the script, enter 'q'.  

#### Emergency Stop
When the emergency stop command is received, the machine will stop immediately and the motor driver(DRV8313) is going into the sleep mode.
