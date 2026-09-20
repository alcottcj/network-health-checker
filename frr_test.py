from netmiko import ConnectHandler
import yaml
from getpass import getpass


with open("/home/christopher/network-health-checker/devices.yaml", "r") as file:
    inventory = yaml.safe_load(file)
password = getpass("Password: ")

for router in inventory["routers"]:
    print(f"\nChecking {router['name']}")

    device = {
        "device_type": "linux",
        "host": router["host"],
        "port": router["port"],
        "username": router["username"],
        "password": password,
    }

    connection = ConnectHandler(**device)

    output = connection.send_command("vtysh -c 'show interface brief'")
    connection.disconnect()

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


