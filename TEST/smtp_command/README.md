# Testcase 09 - SMTP Command

## 1. Mục tiêu

Kiểm tra khả năng phát hiện và phân tích SMTP Command trong gói tin TCP.

## 2. Input

File:

`input.pcap`

Packet được trích từ:

`data/pcap/all.pcapng`

SMTP command được kiểm tra:

```text
EHLO attacker
```

Thông tin transport:

```text
Source port: 48350
Destination port: 25
TCP flags: PA
```

## 3. Parser

SMTP parser:

`src/parser/application/smtp.py`

Parser hỗ trợ các SMTP command:

- EHLO
- HELO
- MAIL FROM
- RCPT TO

## 4. Pipeline

```text
Packet
 ↓
TCP Parser
 ↓
SMTP Detection
 ↓
SMTP Parser
 ↓
Normalized Event
 ↓
JSONL
```

## 5. Kết quả

SMTP packet được nhận diện:

```text
protocol = SMTP
```

Application event:

```json
{
  "type": "command",
  "command": "EHLO",
  "argument": "attacker"
}
```

## 6. Test

Chạy:

```bash
pytest
```

Kết quả dự kiến:

```text
13 passed
```

## 7. JSONL Test

Chạy:

```bash
python main.py --pcap TEST/smtp_command/input.pcap --output TEST/smtp_command/output.jsonl
```

Kết quả:

```text
Events written: 1
```

![image](https://hackmd.io/_uploads/S10T7xwqze.png)
![image](https://hackmd.io/_uploads/Sk60XeP9Mg.png)
