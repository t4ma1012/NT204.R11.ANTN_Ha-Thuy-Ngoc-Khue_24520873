# Testcase 05 - HTTP POST

## 1. Mục tiêu

Kiểm tra khả năng phát hiện và phân tích HTTP POST request có HTTP body.

## 2. Input

File:

`TEST/http_post/input.pcap`

Packet chứa HTTP POST request:

```text
POST /ping.php HTTP/1.1
Host: victim.sanogo.de
User-Agent: curl/7.88.1
Accept: */*
Content-Length: 27
Content-Type: application/x-www-form-urlencoded

ip=127.0.0.1;id&submit=Ping
```

## 3. Xử lý

Pipeline xử lý packet:

```text
TCP packet
    ↓
TCP parser
    ↓
HTTP detector
    ↓
HTTP parser
    ↓
Normalized event
    ↓
JSONL
```

HTTP parser trích xuất:

- HTTP method
- Request path
- HTTP version
- HTTP headers
- HTTP body

## 4. Chạy testcase

```bash
python main.py --pcap TEST/http_post/input.pcap --output TEST/http_post/output.jsonl
```

## 5. Kết quả

Output:

`TEST/http_post/output.jsonl`

Kết quả nhận diện:

```json
{
  "protocol": "HTTP",
  "application": {
    "method": "POST",
    "path": "/ping.php",
    "version": "HTTP/1.1",
    "headers": {
      "Host": "victim.sanogo.de",
      "User-Agent": "curl/7.88.1",
      "Accept": "*/*",
      "Content-Length": "27",
      "Content-Type": "application/x-www-form-urlencoded"
    },
    "body": "ip=127.0.0.1;id&submit=Ping"
  }
}
```

## 6. Kiểm thử

Chạy:

```bash
pytest
```

Kết quả:

```text
9 passed
```
![image](https://hackmd.io/_uploads/BJ9ATkvqzx.png)
![image](https://hackmd.io/_uploads/Hy0-AyDqzx.png)
