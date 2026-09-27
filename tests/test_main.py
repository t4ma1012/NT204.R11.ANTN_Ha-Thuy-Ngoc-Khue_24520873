import subprocess
import sys


def test_help():
    result = subprocess.run(
        [sys.executable, "main.py", "--help"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
    assert "Packet Capture & Parser" in result.stdout


def test_pcap_mode():
    result = subprocess.run(
        [
            sys.executable,
            "main.py",
            "--pcap",
            "data/pcap/test.pcap"
        ],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
    assert "PCAP mode" in result.stdout


def test_interface_mode():
    result = subprocess.run(
        [
            sys.executable,
            "main.py",
            "--interface",
            "eth0"
        ],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
    assert "Live capture mode" in result.stdout