# T11 – Concurrent Flows

## Mục tiêu

Kiểm tra Flow Tracker xử lý đồng thời nhiều flow mà không gộp nhầm các kết nối.

## Input

Hai TCP connection:

- Flow 1: `10.0.0.1:5000 → 10.0.0.2:80`
- Flow 2: `10.0.0.1:5001 → 10.0.0.2:80`

Hai flow có cùng IP và destination port nhưng khác source port.

## Expected

- Tạo ít nhất hai flow khác nhau.
- Mỗi flow có `flow_id` riêng.
- Không gộp hai connection thành một flow.
- Endpoint và port của từng flow được giữ chính xác.

## Output

Kết quả thực tế được ghi vào:

`output.json`

![image](https://hackmd.io/_uploads/HJqn5T39fx.png)
![image](https://hackmd.io/_uploads/ByR69ah5fx.png)
