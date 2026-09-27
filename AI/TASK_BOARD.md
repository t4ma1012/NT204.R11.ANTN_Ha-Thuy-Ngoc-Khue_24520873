# TASK BOARD

## Assignment 01 — Packet Capture & Parser

### Phase 0 — Project Setup

* [x] T00.1 Create project structure
* [x] T00.2 Create README
* [x] T00.3 Create requirements
* [x] T00.4 Create AI context files
* [ ] T00.5 Initialize Git repository
* [ ] T00.6 Cấu hình GitHub repo: đặt tên repo theo format `Mã lớp_Họ&Tên_MSSV`, để public, nhánh mặc định là `main`

---

## Phase 1 — Core Data Model

* [x] T01 Normalized IDS Event model

---

## Phase 2 — Packet Input

* [ ] T02 Live packet capture
* [ ] T03 PCAP reader
* [ ] T04 Shared packet processing pipeline

---

## Phase 3 — Network / Transport Parsing

* [ ] T05 IPv4 parser
* [ ] T06 TCP parser
* [ ] T07 UDP parser

---

## Phase 4 — Application Protocol Detection

* [ ] T08 Application protocol detector
* [ ] T09 Unknown protocol handling

---

## Phase 5 — Application Protocol Parsers

* [ ] T10 HTTP parser
* [ ] T11 DNS parser
* [ ] T12 SMTP parser

---

## Phase 6 — Output

* [ ] T13 JSONL event writer
* [ ] T14 Error handling and logging integration

---

## Phase 7 — Required Tests

> Lưu ý bắt buộc cho toàn bộ Phase 7 (theo mục 10.2 của đề bài):
> Mỗi test case dưới đây, sau khi thực hiện, phải lưu kết quả kiểm thử (log/output/ảnh chụp)
> vào thư mục `TEST/` và **commit riêng cho từng test case** — không được gộp nhiều test case
> vào một commit.

* [ ] T15 TCP handshake
* [ ] T16 TCP data
* [ ] T17 UDP
* [ ] T18 HTTP GET
* [ ] T19 HTTP POST with body
* [ ] T20 HTTP response
* [ ] T21 DNS query
* [ ] T22 DNS response
* [ ] T23 SMTP command
* [ ] T24 SMTP response
* [ ] T25 Unknown protocol
* [ ] T26 Malformed packet

---

## Phase 8 — Finalization

* [ ] T27 Full test suite
* [ ] T28 Documentation
* [ ] T29 Assignment report
* [ ] T29.1 Cập nhật README.md: ghi rõ công cụ AI đã dùng, mục đích sử dụng, và phần source code nào có sự hỗ trợ của AI (theo yêu cầu mục 10.5 của đề bài)
* [ ] T30 Final repository review

---

# Future Assignments

Future assignments will be added here.

Possible future modules:

* Feature Extraction
* Rule-based Detection
* Statistical Detection
* Machine Learning Detection
* Alert Engine
* Storage
* Dashboard
* Performance optimization

Do not implement future modules unless explicitly requested.