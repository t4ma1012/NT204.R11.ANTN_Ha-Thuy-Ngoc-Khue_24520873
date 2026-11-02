# T07 – TCP Handshake

## Mục tiêu

Kiểm tra Flow Tracker nhận diện đúng quá trình TCP 3 bước:

SYN → SYN/ACK → ACK

## Input

Ba TCP packet thuộc cùng một kết nối:

1. Client → Server: SYN
2. Server → Client: SYN/ACK
3. Client → Server: ACK

## Expected

- Ba packet được gắn vào cùng một `flow_id`.
- Chỉ tạo một flow.
- TCP state cuối cùng là `ESTABLISHED`.
- Đếm đúng SYN và ACK.

## Output

Kết quả thực tế được ghi vào:

`output.json`
![image](https://hackmd.io/_uploads/BJOjDan9Mx.png)
![image](https://hackmd.io/_uploads/rJ_nwT39fg.png)
