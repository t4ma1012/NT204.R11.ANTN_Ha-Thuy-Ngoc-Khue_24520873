# T13 – Flow Statistics

## Mục tiêu

Kiểm tra Flow Tracker cập nhật chính xác các thống kê của một flow
khi flow có nhiều packet theo cả hai chiều.

## Input

Một TCP flow gồm nhiều packet theo hai chiều:

1. Client → Server: SYN
2. Server → Client: SYN/ACK
3. Client → Server: ACK + 100 bytes payload
4. Server → Client: ACK + 200 bytes payload

Các packet thuộc cùng một flow.

## Expected

- Tất cả packet được gắn vào cùng một `flow_id`.
- `packet_count` bằng 4.
- `byte_count` bằng 300 bytes.
- `forward_packets` bằng 2.
- `backward_packets` bằng 2.
- `forward_bytes` bằng 100 bytes.
- `backward_bytes` bằng 200 bytes.
- `syn_count` bằng 2.
- `ack_count` bằng 2.
- Duration được tính từ timestamp đầu tiên đến timestamp cuối cùng.
- Không tạo thêm flow ngoài flow ban đầu.

## Output

Kết quả thực tế được ghi tự động vào:

`output.json`

![image](https://hackmd.io/_uploads/S1E-RahcMl.png)
![image](https://hackmd.io/_uploads/S1hW063qMg.png)
