# MASTER CONTEXT — IDS PROJECT

## 1. Project

Tên project:

**IDS Project — Intrusion Detection System**

Đây là project dài hạn. Project được phát triển qua nhiều assignment nhỏ và tất cả assignment phải được tích hợp vào cùng một hệ thống.

Assignment hiện tại:

**Assignment 01 — Packet Capture & Parser**

## 2. Mục tiêu tổng thể

Xây dựng một hệ thống IDS có kiến trúc:

```text
Raw Packet
    ↓
Packet Capture
    ↓
Network Parser
    ↓
Transport Parser
    ↓
Application Protocol Detector
    ↓
Application Protocol Parser
    ↓
Normalized IDS Event
    ↓
Feature Extraction
    ↓
Detection Engine
    ↓
Alert Engine
    ↓
Storage / Dashboard
```

Không được thiết kế mỗi assignment thành một project độc lập.

## 3. Assignment hiện tại

Assignment 01 tập trung vào:

* Packet Capture
* PCAP input
* IPv4 parsing
* TCP parsing
* UDP parsing
* Application protocol detection
* HTTP/1.x parsing
* DNS parsing
* SMTP parsing
* Normalized IDS Event
* JSON Lines logging
* Error handling
* Test cases

## 4. Input

Hệ thống phải hỗ trợ:

### Live traffic

Ví dụ:

```bash
python main.py --interface eth0
```

### PCAP

Ví dụ:

```bash
python main.py --pcap test.pcap
```

Live traffic và PCAP phải đi qua cùng một parsing pipeline.

## 5. Core architecture rule

Raw packet chỉ tồn tại ở tầng capture/parser.

Các module phía sau parser phải sử dụng:

**Normalized IDS Event**

Detection Engine trong các assignment tương lai không được truy cập trực tiếp vào Scapy/PyShark packet object.

## 6. Application protocol detection

Protocol detection không được phụ thuộc hoàn toàn vào port.

Payload-based detection cần được hỗ trợ khi phù hợp.

Ví dụ HTTP có thể chạy trên port khác 80/8080.

## 7. Error handling

Các trường hợp sau không được làm chương trình crash:

* malformed packet
* unsupported protocol
* missing header
* empty payload
* truncated packet
* decode error
* incomplete packet

Hệ thống phải xử lý an toàn và tiếp tục xử lý packet tiếp theo.

## 8. Logging

Event phải có khả năng được ghi dưới dạng JSON Lines.

Mỗi packet/event tương ứng với một dòng JSON.

## 9. Testing

Assignment 01 cần test tối thiểu:

1. TCP handshake
2. TCP data
3. UDP
4. HTTP GET
5. HTTP POST with body
6. HTTP response
7. DNS query
8. DNS response
9. SMTP command
10. SMTP response
11. Unknown protocol
12. Malformed packet

## 10. Development philosophy

Project được phát triển từng task nhỏ.

AI phải:

1. Đọc context trước.
2. Hiểu kiến trúc hiện tại.
3. Chỉ sửa phần cần thiết.
4. Không rewrite toàn project.
5. Không tự ý thay đổi interface đã tồn tại.
6. Không thêm dependency nếu không cần.
7. Chạy test sau khi thay đổi.
8. Cập nhật project context sau task.

## 11. AI roles

### Claude

Primary implementation assistant.

Có thể hỗ trợ:

* architecture
* implementation
* refactoring
* integration

### Gemini

Reviewer.

Có thể hỗ trợ:

* requirement verification
* architecture review
* code review
* missing cases

### DeepSeek

Testing/debugging assistant.

Có thể hỗ trợ:

* debugging
* edge cases
* malformed input
* regression testing

## 12. Important rule

Không AI nào được coi project là một project mới nếu repository đã tồn tại.

Luôn đọc:

```text
AI/MASTER_CONTEXT.md
AI/PROJECT_RULES.md
AI/CURRENT_STATUS.md
AI/ARCHITECTURE.md
AI/TASK_BOARD.md
AI/DECISIONS.md
AI/CHANGELOG.md
```

trước khi thực hiện task lớn.

## 13. Current state

Thông tin trạng thái chi tiết nằm trong:

```text
AI/CURRENT_STATUS.md
```

Task list nằm trong:

```text
AI/TASK_BOARD.md
```
