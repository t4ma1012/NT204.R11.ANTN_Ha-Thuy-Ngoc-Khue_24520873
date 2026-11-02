# Testcase 04 - HTTP GET

## 1. Mục tiêu

Kiểm tra khả năng phát hiện và phân tích HTTP GET request từ TCP packet.

## 2. Input

File:

`TEST/http_get/input.pcap`

Packet chứa HTTP request:

```text
GET /index.html HTTP/1.1
Host: example.com
User-Agent: test-client
Accept: */*
```

## 3. Xử lý

Pipeline xử lý packet theo các bước:

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

## 4. Chạy testcase

```bash
python main.py --pcap TEST/http_get/input.pcap --output TEST/http_get/output.jsonl
```

## 5. Kết quả

Output:

`TEST/http_get/output.jsonl`

Kết quả nhận diện:

```json
{
  "protocol": "HTTP",
  "application": {
    "method": "GET",
    "path": "/index.html",
    "version": "HTTP/1.1",
    "headers": {
      "Host": "example.com",
      "User-Agent": "test-client",
      "Accept": "*/*"
    }
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
8 passed
```
![image](https://hackmd.io/_uploads/SJbh2yvczx.png)
