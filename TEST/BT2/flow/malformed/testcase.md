# T14 – Malformed Event

## Mục tiêu

Kiểm tra hệ thống xử lý event malformed mà không làm chương trình crash.

## Input

Event thiếu nhiều field bắt buộc và chứa dữ liệu không đúng kiểu:

- `protocol` không có giá trị hợp lệ.
- `src_port` chứa chuỗi không phải số.
- Thiếu `timestamp`.
- Thiếu `src_ip`.
- Thiếu `dst_ip`.

## Expected

- Không phát sinh exception.
- Event được đánh dấu `partial`.
- Có trường `reason`.
- Các field bị thiếu được biểu diễn nhất quán bằng `null`.
- Event không được đưa vào Flow Tracker như một event hợp lệ.

## Output

Kết quả thực tế được ghi tự động vào:

`output.json`
![image](https://hackmd.io/_uploads/BytYRph9fx.png)
![image](https://hackmd.io/_uploads/HkJ30a2qMg.png)
