
# Hackerbot Lib

Hackerbot Lib (`hackerbot_lib`) is a project that includes modules for controlling and managing the Hackerbot system.

## Installation

Follow these steps to clone the repository and set up the required dependencies.

### 1. Clone the Repository
Use SSH to clone the repository:
```bash
git clone git@github.com:AllenChienXXX/hackerbot_lib.git
```
This will create a directory named `hackerbot_lib` and download all necessary files.

### 2. Navigate to the Modules Directory
Move into the `hackerbot_modules` directory:
```bash
cd hackerbot_lib/hackerbot_modules/
```

### 3. Install Dependencies
Install the `hackerbot-helper` package using `pip`:
```bash
pip install .
```
This will install the package locally for your Python environment.

## Usage
Once installed, you can import `hackerbot_helper` in your Python scripts:
```python
import hackerbot_helper
```

### 4. Testing
To run the unit tests run:
```bash
cd hackerbot_modules/test
python -m unittest discover
```

## Troubleshooting
If you run into issues with the installation, try the following:
- Ensure you're using a virtual environment:  
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
- Upgrade `pip` before installation:  
  ```bash
  pip install --upgrade pip
  ```
