# Testcase 06 - HTTP Response

## 1. Mục tiêu

Kiểm tra khả năng phát hiện và phân tích HTTP response, bao gồm HTTP status code và response headers.

## 2. Input

File:

`TEST/http_response/input.pcap`

Packet chứa HTTP response:

```text
HTTP/1.1 200 OK
Date: Sat, 10 May 2025 09:43:20 GMT
Server: Apache/2.4.41 (Ubuntu)
Vary: Accept-Encoding
Content-Length: 707
Content-Type: text/html; charset=UTF-8
```

Response có status code `200` và reason phrase `OK`.

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

HTTP response parser trích xuất:

- HTTP version
- Status code
- Reason phrase
- Response headers
- Response body

## 4. Chạy testcase

```bash
python main.py --pcap TEST/http_response/input.pcap --output TEST/http_response/output.jsonl
```

## 5. Kết quả

Output:

`TEST/http_response/output.jsonl`

Kết quả nhận diện:

```json
{
  "protocol": "HTTP",
  "application": {
    "type": "response",
    "version": "HTTP/1.1",
    "status_code": 200,
    "reason": "OK",
    "headers": {
      "Date": "Sat, 10 May 2025 09:43:20 GMT",
      "Server": "Apache/2.4.41 (Ubuntu)",
      "Vary": "Accept-Encoding",
      "Content-Length": "707",
      "Content-Type": "text/html; charset=UTF-8"
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
10 passed
```
![image](https://hackmd.io/_uploads/S1qlygv5fe.png)
