import argparse
import json
from pathlib import Path

from scapy.all import rdpcap

from src.pipeline.parser_pipeline import ParserPipeline


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Packet Capture & Parser for a simple IDS"
    )

    source = parser.add_mutually_exclusive_group(required=True)

    source.add_argument(
        "--interface",
        help="Network interface used for live packet capture"
    )

    source.add_argument(
        "--pcap",
        help="Path to a PCAP file"
    )

    parser.add_argument(
        "--output",
        default="output/events.jsonl",
        help="Output JSON Lines file (default: output/events.jsonl)"
    )

    return parser.parse_args()


def write_jsonl(events, output_path):
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("w", encoding="utf-8") as f:
        for event in events:
            f.write(json.dumps(event) + "\n")


def main():
    args = parse_arguments()

    if args.interface:
        print("[INFO] Live capture mode")
        print(f"[INFO] Interface: {args.interface}")
        print("[INFO] Live capture is not implemented yet.")
        return

    if args.pcap:
        print("[INFO] PCAP mode")
        print(f"[INFO] PCAP file: {args.pcap}")

        packets = rdpcap(args.pcap)
        print(f"[INFO] Loaded packets: {len(packets)}")

        pipeline = ParserPipeline()
        events = pipeline.process_packets(packets)

        write_jsonl(events, args.output)

        print(f"[INFO] Output: {args.output}")
        print(f"[INFO] Events written: {len(events)}")


if __name__ == "__main__":
    main()