from health_check import parse_interfaces, summarize_interfaces, check_router
from unittest.mock import patch, MagicMock


def test_parse_interfaces_ignores_frr_warnings():
    sample_output = """% Can't open configuration file /etc/frr/vtysh.conf due to 'No such file or directory'.
Configuration file[/etc/frr/frr.conf] processing failure: 11
Interface       Status  VRF             Addresses
---------       ------  ---             ---------
eth0            up      default         172.17.0.2/16
lo              up      default
"""

    interfaces = parse_interfaces(sample_output)

    assert len(interfaces) == 2
    assert interfaces[0]["name"] == "eth0"
    assert interfaces[1]["name"] == "lo"


def test_parse_interfaces():
    sample_output = """Interface       Status  VRF             Addresses
---------       ------  ---             ---------
eth0            up      default         172.17.0.2/16
dummy0          down    default
lo              up      default
"""

    interfaces = parse_interfaces(sample_output)

    assert interfaces[0]["name"] == "eth0"
    assert interfaces[0]["status"] == "up"
    assert interfaces[0]["address"] == "172.17.0.2/16"

    assert interfaces[1]["name"] == "dummy0"
    assert interfaces[1]["status"] == "down"
    assert interfaces[1]["address"] == "none"


def test_summarize_interfaces():
    interfaces = [
        {"name": "eth0", "status": "up"},
        {"name": "dummy0", "status": "down"},
        {"name": "lo", "status": "up"},
    ]

    up_count, down_count = summarize_interfaces(interfaces)

    assert up_count == 2
    assert down_count == 1

def test_check_router_success():
    fake_connection = MagicMock()

    fake_connection.send_command.return_value = """Interface       Status  VRF             Addresses
---------       ------  ---             ---------
eth0            up      default         172.17.0.2/16
lo              up      default
"""

    router = {
        "name": "test-router",
        "host": "127.0.0.1",
        "port": 2222,
        "username": "netadmin",
    }

    with patch("health_check.ConnectHandler", return_value=fake_connection):
        result = check_router(router, "fake-password")

    assert result["router"] == "test-router"
    assert result["up_count"] == 2
    assert result["down_count"] == 0

from netmiko.exceptions import NetmikoTimeoutException


def test_check_router_timeout():
    router = {
        "name": "test-router",
        "host": "127.0.0.1",
        "port": 2222,
        "username": "netadmin",
    }

    with patch(
        "health_check.ConnectHandler",
        side_effect=NetmikoTimeoutException
    ):
        result = check_router(router, "fake-password")

    assert result["router"] == "test-router"
    assert result["error"] == "connection failed"


from netmiko.exceptions import NetmikoAuthenticationException


def test_check_router_authentication_failure():
    router = {
        "name": "test-router",
        "host": "127.0.0.1",
        "port": 2222,
        "username": "netadmin",
    }

    with patch(
        "health_check.ConnectHandler",
        side_effect=NetmikoAuthenticationException
    ):
        result = check_router(router, "fake-password")

    assert result["router"] == "test-router"
    assert result["error"] == "authentication failed"
