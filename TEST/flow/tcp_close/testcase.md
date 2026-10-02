# T09 – TCP Close

## Mục tiêu

Kiểm tra Flow Tracker nhận diện quá trình đóng kết nối TCP.

## Input

Hai TCP packet:

1. A → B: FIN
2. B → A: FIN

## Expected

- Hai packet thuộc cùng một `flow_id`.
- `fin_count` bằng 2.
- TCP state chuyển sang `CLOSED`.

## Output

Kết quả thực tế được ghi vào:

`output.json`

![image](https://hackmd.io/_uploads/r1ZTtp29Me.png)
![image](https://hackmd.io/_uploads/SyxCFph5Mx.png)
