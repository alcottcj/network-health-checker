import json
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException
from netmiko import ConnectHandler
import yaml
from getpass import getpass


with open("/home/christopher/network-health-checker/devices.yaml", "r") as file:
    inventory = yaml.safe_load(file)
password = getpass("Password: ")

report = []

for router in inventory["routers"]:
    print(f"\nChecking {router['name']}")

    device = {
        "device_type": "linux",
        "host": router["host"],
        "port": router["port"],
        "username": router["username"],
        "password": password,
    }

    try:
        connection = ConnectHandler(**device)

        output = connection.send_command("vtysh -c 'show interface brief'")

        connection.disconnect()

    except NetmikoAuthenticationException:
        print(f"ERROR: Authentication failed for {router['name']}")
        report.append({
            "router": router["name"],
            "error": "authentication failed"
        })
        continue

    except NetmikoTimeoutException:
        print(f"ERROR: Could not connect to {router['name']}")
        report.append({
            "router": router["name"],
            "error": "authentication failed"
        })
        continue

    lines = output.splitlines()

    interfaces = []

    for line in lines[4:]:
        fields = line.split()

        interface = {
            "name": fields[0],
            "status": fields[1],
            "vrf": fields[2],
            "address": fields[3] if len(fields) > 3 else "none",
        }

        interfaces.append(interface)

    up_count = 0
    down_count = 0

    for interface in interfaces:
        if interface["status"] == "up":
            up_count += 1
        else:
            down_count += 1

    print(f"{len(interfaces)} interfaces checked")
    print(f"{up_count} up")
    print(f"{down_count} down")

    for interface in interfaces:
        if interface["status"] != "up":
            print(f"WARNING: {interface['name']} is {interface['status']}")
    
    report.append({
        "router": router["name"],
        "interfaces": interfaces,
        "up_count": up_count,
        "down_count": down_count
    })

with open("health_report.json", "w") as file:
    json.dump(report, file, indent=4)
    
