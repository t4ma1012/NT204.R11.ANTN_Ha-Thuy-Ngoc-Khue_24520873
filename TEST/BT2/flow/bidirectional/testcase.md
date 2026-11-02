# T08 – Bidirectional Flow

## Mục tiêu

Kiểm tra hai chiều A → B và B → A được xem là cùng một flow.

## Input

Hai TCP packet:

1. A → B
2. B → A

Hai packet có cùng cặp endpoint nhưng đảo chiều.

## Expected

- Hai packet có cùng `flow_id`.
- Chỉ tồn tại một flow.
- Packet A → B được tính là forward.
- Packet B → A được tính là backward.
- Forward/backward packet count chính xác.

## Output

Kết quả thực tế được ghi vào:

`output.json`
![image](https://hackmd.io/_uploads/BkKQF6nqMg.png)
![image](https://hackmd.io/_uploads/HJZItp39fl.png)