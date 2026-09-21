# IDS ARCHITECTURE

## 1. Overall Architecture

```text
                    ┌─────────────────┐
                    │   Live Traffic  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Packet Capture  │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ Network Parser  │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │Transport Parser │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │Protocol Detector│
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │Protocol Parser  │
                    └────────┬────────┘
                             │
                             ▼
                 ┌──────────────────────┐
                 │ Normalized IDS Event │
                 └──────────┬───────────┘
                            │
             ┌──────────────┼──────────────┐
             ▼              ▼              ▼
        Features       Detection        Storage
                           │
                           ▼
                         Alerts
```

PCAP input must enter the same parser pipeline:

```text
PCAP
 ↓
Packet Reader
 ↓
Same Parser Pipeline
 ↓
Normalized IDS Event
```

## 2. Capture Layer

Responsibilities:

* receive live packets
* read packets from PCAP
* provide packets to the parser pipeline

The capture layer should not contain application protocol parsing logic.

---

## 3. Network Parser

Responsibilities:

* parse network layer
* identify IPv4
* extract source IP
* extract destination IP
* extract protocol information

---

## 4. Transport Parser

Responsibilities:

* identify TCP
* identify UDP
* extract transport information

TCP information may include:

* source port
* destination port
* flags
* sequence information
* acknowledgement information
* payload

UDP information may include:

* source port
* destination port
* length
* payload

---

## 5. Application Protocol Detector

Responsibilities:

* determine possible application protocol
* use port information when useful
* use payload signatures when necessary
* support non-standard ports

Potential protocols:

* HTTP
* DNS
* SMTP
* UNKNOWN

Detection should not depend exclusively on ports.

---

## 6. Application Protocol Parser

Responsibilities:

* parse application payload
* extract protocol-specific information
* safely handle malformed payloads

Examples:

```text
HTTP → method, URL, headers, body
DNS  → query, response, records
SMTP → command, response
```

---

## 7. Normalized IDS Event

The normalized event is the interface between parsing and future IDS modules.

Conceptually:

```text
NormalizedEvent
├── timestamp
├── network
├── transport
├── application
└── metadata
```

The exact schema will be defined in the relevant implementation task.

---

## 8. Feature Extraction

Future module.

Input:

```text
Normalized IDS Event
```

Output:

```text
Feature Vector
```

This layer must not access raw packet objects.

---

## 9. Detection Engine

Future module.

Input:

```text
Feature Vector
```

Output:

```text
Detection Result
```

Possible future techniques may include:

* rule-based detection
* statistical detection
* machine learning
* anomaly detection

The specific techniques will be decided by future assignments.

---

## 10. Alert Engine

Future module.

Responsibilities:

* convert detection results into alerts
* assign severity
* store alert information
* provide data for dashboard/output

---

## 11. Storage / Dashboard

Future module.

Potential outputs:

* JSONL
* database
* logs
* dashboard

These are future extension points and should not be implemented unless requested.
