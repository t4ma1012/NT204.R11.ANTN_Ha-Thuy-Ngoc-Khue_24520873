# CURRENT STATUS

## Project

IDS Project

## Current Assignment

Assignment 01 — Packet Capture & Parser

## Current Phase

Phase 1 — Core Data Model.

## Completed

* [x] Project directory created
* [x] Project structure created
* [x] README created
* [x] .gitignore created
* [x] requirements.txt created
* [x] requirements-dev.txt created
* [x] main.py placeholder created
* [x] AI project context initialized

## In Progress

Ready for the next task after completing the normalized event model.

## Not Started

* [ ] Git repository initialization
* [ ] Packet capture
* [ ] PCAP reader
* [ ] Shared parsing pipeline
* [ ] IPv4 parser
* [ ] TCP parser
* [ ] UDP parser
* [ ] Application protocol detector
* [ ] HTTP parser
* [ ] DNS parser
* [ ] SMTP parser
* [ ] JSONL logging
* [ ] Assignment tests
* [ ] Assignment report

## Current Architecture

```text
Raw Packet
    ↓
Capture
    ↓
Parsing
    ↓
Application Protocol Detection
    ↓
Application Protocol Parsing
    ↓
Normalized IDS Event
    ↓
Future Detection Engine
```

## Current Task

T01 — Normalized IDS Event model (completed).

## Last Completed Task

T01 — Normalized IDS Event model.

## Known Issues

No implementation issues yet.

## Dependencies

Current runtime dependency:

* scapy

Development dependencies:

* pytest
* pytest-cov
* ruff

## Next Step

T00.5 — Initialize the Git repository.

## Important

Do not implement the complete IDS at once.

Development must proceed task by task.
