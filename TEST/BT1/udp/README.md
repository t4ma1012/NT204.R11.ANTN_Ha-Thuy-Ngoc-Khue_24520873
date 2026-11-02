# Testcase 03 - UDP

## 1. Mục tiêu

Kiểm tra khả năng nhận diện và parse một UDP packet.

## 2. Input

**File:** `input.pcap`

Packet được tạo bằng Scapy để kiểm tra UDP parser.

Packet sử dụng:

- Source port: `12345`
- Destination port: `53`

## 3. Thành phần đã thay đổi

### UDP Parser

**File:** `src/parser/transport/udp.py`

Parser lấy các thông tin:

- Source port
- Destination port
- UDP length
- Payload length
- Payload

### Parser Pipeline

**File:** `src/pipeline/parser_pipeline.py`

Pipeline được bổ sung khả năng phân biệt:

- TCP → TCP Parser
- UDP → UDP Parser
- Khác → unknown

## 4. Chạy testcase

```bash
python main.py --pcap TEST/udp/input.pcap --output TEST/udp/output.jsonl
```

## 5. Kết quả

**Input:**

- 1 UDP packet

**Output:**

- 1 JSON event

UDP packet được nhận diện thành công với:

- Source port: `12345`
- Destination port: `53`
- UDP length: `24`
- Payload length: `4`

Kết quả được ghi vào: `TEST/udp/output.jsonl`
![image](https://hackmd.io/_uploads/rk4fqyw5Gg.png)
