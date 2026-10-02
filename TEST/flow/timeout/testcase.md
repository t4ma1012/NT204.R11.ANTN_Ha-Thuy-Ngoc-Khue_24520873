
# T12 – Idle Timeout

## Mục tiêu

Kiểm tra Flow Tracker tự động expire flow khi vượt quá thời gian idle được cấu hình.

## Input

- Idle timeout được cấu hình là 10 giây.
- Một UDP flow được tạo tại timestamp 1.
- Không có packet mới trong flow.
- Kiểm tra tại timestamp 12.

## Expected

- Flow vượt quá idle timeout.
- Flow được đưa vào danh sách expired.
- Flow bị xóa khỏi active flow table.
- Không còn flow này trong danh sách active flows.

## Output

Kết quả thực tế được ghi vào:

`output.json`

![image](https://hackmd.io/_uploads/HJdwiT2qzx.png)
![image](https://hackmd.io/_uploads/S1yYjT35fe.png)
