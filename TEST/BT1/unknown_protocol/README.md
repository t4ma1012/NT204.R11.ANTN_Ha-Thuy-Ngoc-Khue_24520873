# Testcase 11 - Unknown Protocol

## 1. Mục tiêu

Kiểm tra hệ thống xử lý một protocol không được hỗ trợ mà không làm chương trình bị crash.

## 2. Input

PCAP:

`TEST/unknown_protocol/input.pcap`

Packet sử dụng GRE, là protocol chưa được parser hỗ trợ.

Payload:

```text
UNKNOWN_PROTOCOL_DATA
```

## 3. Kết quả mong đợi

Packet không được parser nhận diện và được chuẩn hóa thành:

```json
{
  "protocol": "unknown"
}
```

Hệ thống không được crash.

## 4. Test

```bash
pytest -q
```

Kết quả mong đợi:

```text
15 passed
```

## 5. Pipeline test

```bash
python main.py --pcap TEST/unknown_protocol/input.pcap --output TEST/unknown_protocol/output.jsonl
```

Output:

`TEST/unknown_protocol/output.jsonl`

Kết quả phải chứa:

```json
{"protocol": "unknown"}
```

![image](https://hackmd.io/_uploads/HyoIIeD9zg.png)
![image](https://hackmd.io/_uploads/HJG_Lgvqfe.png)
