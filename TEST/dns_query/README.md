# Testcase 07 - DNS Query

## 1. Mục tiêu

Kiểm tra khả năng phát hiện và phân tích DNS Query trong gói tin UDP.

## 2. Input

File:

`input.pcap`

Gói tin chứa:

- Source IP: `192.168.1.10`
- Destination IP: `8.8.8.8`
- Source port: `12345`
- Destination port: `53`
- DNS Query: `example.com`
- Query Type: `A`

## 3. Parser

DNS parser tại:

`src/parser/application/dns.py`

Parser thực hiện:

- Nhận diện DNS packet.
- Xác định Query/Response.
- Phân tích domain name.
- Phân tích query type.
- Phân tích query class.

## 4. Pipeline

Packet được xử lý theo flow:

```text
IP
 ↓
UDP
 ↓
DNS Detection
 ↓
DNS Parser
 ↓
Normalized Event
 ↓
JSONL
```

## 5. Kết quả

Output:

`output.jsonl`

Kết quả chính:

```json
{
  "protocol": "DNS",
  "application": {
    "type": "query",
    "query": {
      "name": "example.com.",
      "type": 1,
      "class": 1
    }
  }
}
```

`type = 1` tương ứng với DNS query type `A`.

## 6. Test

Chạy:

```bash
pytest
```

Kết quả:

```text
11 passed
```

Có 3 `DeprecationWarning` từ Scapy liên quan đến DNS fields. Các warning này không làm test thất bại.

## 7. JSONL Test

Chạy:

```bash
python main.py --pcap TEST/dns_query/input.pcap --output TEST/dns_query/output.jsonl
```

Kết quả:

```text
Events written: 1
```
![image](https://hackmd.io/_uploads/S13iglw5Ge.png)

![image](https://hackmd.io/_uploads/r1JixxD5Gx.png)

