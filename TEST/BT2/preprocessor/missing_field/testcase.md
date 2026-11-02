# T06 – Missing Field

## Mục tiêu

Kiểm tra Preprocessor xử lý event bị thiếu field mà không phát sinh exception.

## Input

Event thiếu src_ip, dst_ip và application.

## Expected

- Không phát sinh exception.
- Field thiếu được biểu diễn nhất quán.
- Event được đánh dấu partial.
- Có reason mô tả nguyên nhân.

## Output

Kết quả được ghi vào `output.json`.
![image](https://hackmd.io/_uploads/r1nIB6n5Mx.png)
![image](https://hackmd.io/_uploads/rkvFBp3cze.png)
