import json
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException
from netmiko import ConnectHandler
import yaml
from getpass import getpass


def parse_interfaces(output):
    interfaces = []
    in_interface_table = False

    for line in output.splitlines():
        line = line.strip()

        if line.startswith("Interface") and "Status" in line and "VRF" in line:
            in_interface_table = True
            continue

        if not in_interface_table:
            continue

        if not line:
            continue

        if line.startswith("---------"):
            continue

        fields = line.split()

        if len(fields) < 3:
            continue

        interface = {
            "name": fields[0],
            "status": fields[1],
            "vrf": fields[2],
            "address": fields[3] if len(fields) > 3 else "none",
        }

        interfaces.append(interface)

    return interfaces


def summarize_interfaces(interfaces):
    up_count = 0
    down_count = 0

    for interface in interfaces:
        if interface["status"] == "up":
            up_count += 1
        else:
            down_count += 1

    return up_count, down_count


def print_health_summary(router_name, interfaces, up_count, down_count):
    print(f"\nChecking {router_name}")
    print(f"{len(interfaces)} interfaces checked")
    print(f"{up_count} up")
    print(f"{down_count} down")

    for interface in interfaces:
        if interface["status"] != "up":
            print(f"WARNING: {interface['name']} is {interface['status']}")


def check_router(router, password):
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
        return {
            "router": router["name"],
            "error": "authentication failed"
        }

    except NetmikoTimeoutException:
        print(f"ERROR: Could not connect to {router['name']}")
        return {
            "router": router["name"],
            "error": "connection failed"
        }

    interfaces = parse_interfaces(output)
    up_count, down_count = summarize_interfaces(interfaces)

    print_health_summary(
        router["name"],
        interfaces,
        up_count,
        down_count
    )

    return {
        "router": router["name"],
        "interfaces": interfaces,
        "up_count": up_count,
        "down_count": down_count
    }


def main():
    with open("/home/christopher/network-health-checker/devices.yaml", "r") as file:
        inventory = yaml.safe_load(file)

    password = getpass("Password: ")
    report = []

    for router in inventory["routers"]:
        result = check_router(router, password)
        report.append(result)

    with open("health_report.json", "w") as file:
        json.dump(report, file, indent=4)


if __name__ == "__main__":
    main()
