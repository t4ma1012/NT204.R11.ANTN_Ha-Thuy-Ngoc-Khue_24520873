# Testcase 01 - TCP Handshake

## 1. Mục tiêu

Kiểm tra khả năng parser nhận diện TCP 3-way handshake:

- SYN
- SYN/ACK
- ACK

## 2. Input

File:

`input.pcap`

PCAP được tách từ:

`data/pcap/all.pcapng`

Chỉ giữ lại 3 packet của TCP handshake.

```text
Packet 1: SYN
Packet 2: SYN/ACK
Packet 3: ACK
```

## 3. Những gì đã thực hiện

### Parser

Sử dụng parser có sẵn:

`src/parser/transport/tcp.py`

Hàm:

`parse_tcp(packet)`

Parser lấy các trường TCP:

- source port
- destination port
- flags
- sequence number
- acknowledgment number

### Pipeline

Đã cập nhật:

`src/pipeline/parser_pipeline.py`

Pipeline gọi `parse_tcp()` và chuẩn hóa kết quả thành:

```json
{
  "protocol": "TCP",
  "transport": {
    "src_port": 48350,
    "dst_port": 25,
    "flags": "S",
    "seq": 3339534815,
    "ack": 0
  }
}
```

### Main program

Đã cập nhật:

`main.py`

Chương trình hiện có thể:

- Đọc PCAP bằng Scapy.
- Đưa từng packet vào ParserPipeline.
- Ghi kết quả ra JSON Lines.
- Tạo thư mục output nếu chưa tồn tại.

## 4. Cách chạy

```bash
python main.py --pcap TEST/tcp_handshake/input.pcap --output TEST/tcp_handshake/output.jsonl
```

## 5. Kết quả

Input gồm 3 packet.

Output gồm 3 JSON events.

- Packet 1 → SYN
- Packet 2 → SYN/ACK
- Packet 3 → ACK

Kết quả đạt yêu cầu testcase TCP Handshake.




![image](https://hackmd.io/_uploads/By4m41v9fe.png)
![image](https://hackmd.io/_uploads/Hk7lSyw5Gg.png)