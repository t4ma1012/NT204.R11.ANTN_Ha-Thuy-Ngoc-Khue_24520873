# CHANGELOG

## 2026-09-21

### T01 — Normalized IDS Event Model

Implemented the JSON-compatible normalized event boundary with dataclasses:

* `NormalizedEvent` with timestamp, network, transport, application, and metadata
* Extensible application data for HTTP, DNS, SMTP, and future protocols
* Explicit UNKNOWN and malformed-event fields
* `to_dict()` and `to_json()` serialization methods
* Unit tests for construction, serialization, empty data, and malformed data

### Project Initialization

Created initial IDS project structure.

Created:

* README
* requirements
* .gitignore
* AI project context
* source directories
* test directories
* data directories
* output directories

### Architecture

Established initial architecture:

```text
Capture
→ Parsing
→ Protocol Detection
→ Protocol Parsing
→ Normalized Event
→ Features
→ Detection
→ Alerts
```

### Current Assignment

Assignment 01 — Packet Capture & Parser.

### AI Usage

AI was used to help design:

* project structure
* development workflow
* architecture documentation
* task breakdown
* AI context files

No IDS implementation has been completed yet.
