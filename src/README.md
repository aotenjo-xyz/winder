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

### 3. Create a `settings.yml` file based on `settings_example.yml` and update the settings as needed.
```bash
cp settings_example.yml settings.yml
```

### 4. Calibrate the motors
Before running the script, you need to calibrate the motors. This is done by running the
```bash
python calib.py
```

Update `scripts/settings.yml` with the calibration values.

### 5. Run the script
```bash
python main.py
```

#### Emergency Stop
When the emergency stop command is received, the machine will stop immediately and the motor driver(DRV8313) is going into the sleep mode.
