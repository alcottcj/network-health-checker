from health_check import parse_interfaces, summarize_interfaces


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
