<<<<<<< HEAD
# IDS Project

## Packet Capture & Parser

This project implements the Packet Capture & Parser module for a simple Intrusion Detection System (IDS).

The module is designed to:

- Capture packets from a network interface.
- Read packets from PCAP files.
- Parse IPv4, TCP, UDP, HTTP/1.x, DNS, and SMTP traffic.
- Detect application protocols.
- Convert packets into a normalized IDS event.
- Write parsed events in JSON Lines format.
- Handle malformed and unsupported packets without crashing.

## Input Modes

### Live Capture

```bash
python main.py --interface eth0
```

### PCAP Import

```bash
python main.py --pcap data/pcap/test.pcap
```

## Output

The parsed events will be written in JSON Lines format.

Default output:

```text
output/events.jsonl
```

Each line represents one packet/event.

## Project Structure

```text
IDS-Project/
├── AI/
├── data/
│   ├── pcap/
│   └── raw/
├── docs/
├── output/
├── src/
│   ├── capture/
│   ├── detection/
│   ├── logging/
│   ├── models/
│   ├── parser/
│   ├── pipeline/
│   ├── response/
│   └── utils/
├── TEST/
├── tests/
├── main.py
├── requirements.txt
└── README.md
```

## AI Usage

AI tools may be used during development for:

- Explaining networking and packet parsing concepts.
- Suggesting project structure.
- Debugging errors.
- Reviewing code.

All AI-assisted code will be reviewed and understood before submission.

## Current Status

- [x] Project setup
- [ ] Packet capture
- [ ] PCAP reader
- [ ] IPv4 parser
- [ ] TCP parser
- [ ] UDP parser
- [ ] Application protocol detection
- [ ] HTTP parser
- [ ] DNS parser
- [ ] SMTP parser
- [ ] Normalized IDS event
- [ ] JSONL output
- [ ] Error handling
- [ ] Required test cases
=======
# NT204.R11.ANTN_Ha-Thuy-Ngoc-Khue_24520873
>>>>>>> 13f1ff9a33af101c02168cd24014f4765f0471e4
