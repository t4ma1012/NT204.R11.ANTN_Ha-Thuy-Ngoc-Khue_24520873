# IDS

## Packet Capture & Parser

Dự án này triển khai module Packet Capture & Parser cho một hệ thống Intrusion Detection System (IDS) đơn giản.

Module được thiết kế để:

- Thu thập packet từ một network interface.
- Đọc packet từ file PCAP.
- Parse lưu lượng IPv4, TCP, UDP, HTTP/1.x, DNS và SMTP.
- Nhận diện application protocol.
- Chuyển packet thành một normalized IDS event.
- Ghi các event đã parse ra định dạng JSON Lines.
- Xử lý packet malformed và protocol không hỗ trợ mà không bị crash.

## Chế độ Input

### Live Capture

```bash
python main.py --interface eth0
```

### PCAP Import

```bash
python main.py --pcap data/pcap/test.pcap
```

## Output

Các event đã parse sẽ được ghi ra định dạng JSON Lines.

Output mặc định:

```text
output/events.jsonl
```

Mỗi dòng tương ứng với một packet/event.

## Cấu trúc Project

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

## Sử dụng AI

Các công cụ AI có thể được sử dụng trong quá trình phát triển để:

- Giải thích các khái niệm về networking và packet parsing.
- Đề xuất cấu trúc project.
- Debug lỗi.
- Review code.

Toàn bộ mã nguồn có sử dụng AI sẽ được review và hiểu rõ trước khi nộp bài.
