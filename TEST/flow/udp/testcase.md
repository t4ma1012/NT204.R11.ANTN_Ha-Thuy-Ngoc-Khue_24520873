# T10 – UDP Flow

## Mục tiêu

Kiểm tra Flow Tracker gom DNS query và response vào cùng một UDP flow.

## Input

Hai UDP packet:

1. Client → DNS Server: DNS query
2. DNS Server → Client: DNS response

Hai packet sử dụng cùng cặp endpoint nhưng ngược chiều.

## Expected

- Hai packet thuộc cùng một `flow_id`.
- Chỉ tạo một UDP flow.
- Có đúng forward và backward direction.
- `packet_count` chính xác.
- `byte_count` chính xác.
- UDP không sử dụng TCP connection state.

## Output

Kết quả thực tế được ghi vào:

`output.json`
![image](https://hackmd.io/_uploads/rJNSqThqfg.png)

![image](https://hackmd.io/_uploads/SkUU5ancMl.png)