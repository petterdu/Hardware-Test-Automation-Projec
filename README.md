Note: Currently, only CPU, GPU, memory, disk , Password management, and Library installation features have been implemented.

# Hardware Test Automation Project

This repository contains a hardware test automation project developed using Python and shell scripting. The goal of this project is to create an automated system that can perform various hardware tests, including CPU, GPU, Memory, Disk, LAN, and USB port tests. The project also includes a GUI built with PyQt5 to easily manage and monitor these tests.

## Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Folder Structure](#folder-structure)
- [Contributing](#contributing)
- [License](#license)

## Features
- Automated hardware testing for CPU, GPU, Memory, Disk, LAN, and USB ports.
- GUI built with PyQt5 for easy interaction and visualization of test results.
- Password management and library installation verification.
- Logging of test progress and results for monitoring.
- Real-time progress bar based on test execution.

## Project Structure
The project is organized into different folders and modules to ensure modularity and ease of development:

```plaintext
project_root
├── main_ui.py               # Main entry point for the UI
├── UI_folder                # UI modules for different hardware tests
│   ├── cpu_ui.py            # UI module for CPU test
│   ├── gpu_ui.py            # UI module for GPU test
│   ├── memory_ui.py         # UI module for Memory test
│   ├── disk_ui.py           # UI module for Disk test
│   ├── lan_ui.py            # UI module for LAN port test
│   ├── usb_ui.py            # UI module for USB port test
│   ├── password_ui.py       # UI module for Password management
│   └── library_install_ui.py # UI module for library installation management
├── functions                # Functional modules for different hardware tests
│   ├── cpu_test_function.py # Function module for CPU test
│   ├── gpu_test_function.py # Function module for GPU test
│   ├── memory_test_function.py # Function module for Memory test
│   ├── disk_test_function.py # Function module for Disk test
│   ├── lan_test_function.py  # Function module for LAN port test
│   ├── usb_test_function.py  # Function module for USB port test
│   └── library_install_checker.py # Library installation checking module
└── functions/scripts        # Shell scripts for hardware testing
    ├── hardware_test.sh     # Shell script to run hardware tests
    ├── install_libraries.sh # Shell script for library installation
    ├── check_libraries.sh   # Shell script for library verification
    └── password.txt         # Password storage for hardware tests
```

## Requirements
- Python 3.7+
- PyQt5
- Required Linux tools (e.g., `memtester`, `stress-ng`, `glmark2`)
- `sudo` privileges for running certain tests

## Installation
Clone the repository to your local machine:
```bash
git clone https://github.com/yourusername/hardware-test-automation.git
cd hardware-test-automation
```

> **Note**: Make sure to provide `sudo` privileges as some of the tests require elevated permissions.

## Usage
To start the GUI:
```bash
python main_ui.py
```

You can select any hardware test using the GUI interface. Each test runs independently, and a progress bar indicates the status of the ongoing test. Make sure to configure the password (`password.txt`) in `functions/scripts` for automated script execution.

## Folder Structure
- `main_ui.py`: Entry point for the UI, aggregates all different modules.
- `UI_folder`: Contains all individual UI components for managing tests and other features.
- `functions`: Contains all the core test functions that execute various hardware tests.
- `functions/scripts`: Contains all the shell scripts for executing tests at the system level, including library checks and installations.

## Key Components

### 1. User Interface
The UI for this project is built using PyQt5, which allows for real-time interaction and visualization of test progress and results.

### 2. Hardware Testing Scripts
Shell scripts (`hardware_test.sh`, `install_libraries.sh`, etc.) are used to execute system-level commands for hardware testing. These scripts can use `sudo` privileges to access hardware directly.

### 3. Password Management
The system uses a `password.txt` file to store the password used for running hardware tests with elevated permissions. The UI allows users to update this password.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

