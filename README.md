# Network Health Checker

A Python-based network automation project that connects to FRRouting devices over SSH, collects interface status information, and identifies interfaces that are down.

## Current Features

* Connects to network devices using Netmiko
* Reads device information from a YAML inventory file
* Prompts securely for the device password
* Runs FRRouting `show interface brief`
* Parses interface information into structured Python data
* Reports the number of interfaces that are up or down
* Flags interfaces that are not operational

## Technologies

* Python
* Netmiko
* PyYAML
* SSH
* FRRouting
* Docker
* Linux

## Lab Environment

The current lab uses an FRRouting container running on a Linux Mint host. SSH access to the container is exposed on a local TCP port so the Python automation script can remotely query the router.

## Project Status

This project is under active development. Planned improvements include support for multiple routers, additional health checks, structured reporting, error handling, logging, and automated testing.
