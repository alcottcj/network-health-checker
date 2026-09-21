# Network Health Checker

![Tests](https://github.com/alcottcj/network-health-checker/actions/workflows/tests.yml/badge.svg)

A Python-based network automation project that connects to FRRouting devices over SSH, collects interface status information, and identifies interfaces that are down.

## Current Features

- Connects to network devices using Netmiko
- Reads device information from a YAML inventory file
- Prompts securely for the device password
- Runs FRRouting `show interface brief`
- Parses interface information into structured Python data
- Reports the number of interfaces that are up or down
- Flags interfaces that are not operational
- Supports multiple routers
- Handles connection and authentication failures
- Generates JSON health reports
- Includes automated tests with pytest
- Runs tests automatically with GitHub Actions

## Technologies

- Python
- Netmiko
- PyYAML
- pytest
- SSH
- FRRouting
- Docker
- Linux
- GitHub Actions

## Lab Environment

The current lab uses FRRouting containers running on a Linux Mint host. SSH access to the containers is exposed on local TCP ports so the Python automation script can query the routers.

## How to Run

1. Activate the Python virtual environment:

    python3 -m venv .venv
    source .venv/bin/activate

2. Install dependencies:

    pip install -r requirements.txt

3. Make sure the FRR test routers are running.

4. Run the health checker:

    python3 health_check.py

5. Enter the router password when prompted.

## Example Output

    Password:

    Checking frr-router-1
    3 interfaces checked
    2 up
    1 down
    WARNING: dummy0 is down

    Checking frr-router-2
    2 interfaces checked
    2 up
    0 down

The script also creates a machine-readable `health_report.json` file containing the results.

## Testing

Run the automated tests with:

    pytest -v

## Project Status

This project is under active development.
