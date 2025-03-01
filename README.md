# hackerbot_bobby

## Overview
`hackerbot_bobby` is a project designed to navigate a robot based on user input commands. This project includes a set of modules for handling navigation logic and user interaction.

## Installation

### Step 1: Create a Virtual Environment
To isolate the project's dependencies, start by creating a Python virtual environment:

```bash
python3 -m venv venv
```

### Step 2: Activate the Virtual Environment
Activate the virtual environment:

- **On Linux/macOS**:

  ```bash
  source venv/bin/activate
  ```

- **On Windows**:

  ```bash
  .\venv\Scripts\activate
  ```

### Step 3: Install Project Dependencies
Navigate to the `hackerbot_modules` directory and install the required modules:

```bash
cd hackerbot_modules
pip install .
```

### Step 4: Run the Robot Navigation
Once the dependencies are installed, go to the `bobby` directory and run the `navigate_robot.py` script to begin navigating the robot using user input commands:

```bash
cd ../bobby
python3 navigate_robot.py
```

This will start the program, and the robot will execute navigation tasks based on the commands provided by the user.
