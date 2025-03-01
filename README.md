# hackerbot_bobby

## Overview
`hackerbot_bobby` is a project designed to navigate a robot based on user input commands. This project includes a set of modules for handling navigation logic and user interaction.

## Installation

### Step 1: SSH into Raspberry Pi (Bobby Board)
To connect to the Raspberry Pi (Bobby Board) remotely, use SSH:

```bash
ssh bobby@bobby
```

- **Username**: `bobby`
- **Password**: `uhohhotdog`

### Step 2: Create a Virtual Environment
After logging into the Raspberry Pi, create a Python virtual environment to isolate the project's dependencies:

```bash
python3 -m venv venv
```

### Step 3: Activate the Virtual Environment
Activate the virtual environment:

- **On Linux/macOS**:

  ```bash
  source venv/bin/activate
  ```

- **On Windows** (if applicable on your environment):

  ```bash
  .\venv\Scripts\activate
  ```

### Step 4: Install Project Dependencies
Navigate to the `hackerbot_modules` directory and install the required modules:

```bash
cd hackerbot_modules
pip install .
```

### Step 5: Run the Robot Navigation
Once the dependencies are installed, go to the `bobby` directory and run the `navigate_robot.py` script to begin navigating the robot using user input commands:

```bash
cd ../bobby
python3 navigate_robot.py
```

This will start the program, and the robot will execute navigation tasks based on the commands provided by the user.
