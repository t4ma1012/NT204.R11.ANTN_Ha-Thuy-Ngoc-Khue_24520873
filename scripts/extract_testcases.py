from pathlib import Path
from scapy.all import rdpcap, wrpcap


SOURCE = Path("data/pcap/all.pcapng")
TEST_ROOT = Path("TEST")


def save_packets(name, packets):
    output_dir = TEST_ROOT / name
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "input.pcap"
    wrpcap(str(output_file), packets)

    print(f"[OK] {name}: {len(packets)} packets -> {output_file}")


def main():
    packets = rdpcap(str(SOURCE))

    # TC01 - TCP Handshake
    # all.pcapng:
    # 11 = SYN
    # 12 = SYN/ACK
    # 13 = ACK
    save_packets(
        "tcp_handshake",
        packets[10:13]
    )
    # TC02 - TCP Data
    # Packet 92 contains a TCP payload
    save_packets("tcp_data", [packets[91]]) 


if __name__ == "__main__":
    main()