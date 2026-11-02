
# Testcase 08 - DNS Response

## 1. Mục tiêu

Kiểm tra khả năng phát hiện và phân tích DNS Response trong gói tin UDP.

## 2. Input

File:

`input.pcap`

Gói tin chứa:

- Source IP: `8.8.8.8`
- Destination IP: `192.168.1.10`
- Source port: `53`
- Destination port: `12345`
- DNS Response cho `example.com`
- Query Type: `A`
- Answer: `93.184.216.34`
- TTL: `300`

## 3. Parser

DNS parser tại:

`src/parser/application/dns.py`

Parser thực hiện:

- Nhận diện DNS Response.
- Phân tích DNS Question.
- Phân tích DNS Answer.
- Lấy domain name.
- Lấy record type.
- Lấy record class.
- Lấy TTL.
- Lấy dữ liệu trả về.

## 4. Pipeline

```text
Packet
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

DNS Response được nhận diện với:

```text
type = response
```

Answer:

```text
example.com. → 93.184.216.34
```

## 6. Test

Chạy:

```bash
pytest
```

Kết quả:

```text
12 passed
```

## 7. JSONL Test

Chạy:

```bash
python main.py --pcap TEST/dns_response/input.pcap --output TEST/dns_response/output.jsonl
```

Kết quả:

```text
Events written: 1
```
![image](https://hackmd.io/_uploads/S1aNfxD9fe.png)

![image](https://hackmd.io/_uploads/ryj-Mxw9Mx.png)
