from scapy.all import sniff, rdpcap


def capture_live(interface, count=10):
    """
    Capture packets from a live network interface.
    """
    packets = sniff(iface=interface, count=count)
    return packets


def read_pcap(filepath):
    """
    Read packets from a PCAP file.
    """
    packets = rdpcap(filepath)
    return packets