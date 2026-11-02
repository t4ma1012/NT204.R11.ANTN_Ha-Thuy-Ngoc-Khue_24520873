# T02 - Syntax-invalid rule

## Mục tiêu

Kiểm tra rule sai cú pháp được trả về với trạng thái `invalid` và lý do cụ thể, đồng thời loader tiếp tục xử lý rule hợp lệ tiếp theo.

## Dữ liệu đầu vào

`input.rules` có một rule TCP thiếu dấu đóng `)` và một rule UDP hợp lệ.

## Cách chạy

```cmd
python -m pytest -q tests\test_rule_loader.py -k syntax_invalid
```

## Kết quả mong đợi

- Rule TCP được phân loại `invalid`, với lý do chỉ rõ thiếu dấu đóng `)`.
- Rule UDP tiếp theo vẫn được parse và phân loại `valid`.
- Loader hoàn tất mà không dừng tại rule lỗi.

## Kết quả thực tế

Đạt. Rule TCP được ghi nhận là `invalid` với lý do thiếu dấu đóng `)`. Loader tiếp tục parse rule UDP sau đó thành `valid`; kết quả được lưu trong `output.json`.

- T02: `1 passed`.
- T01 regression: `1 passed`.
- Toàn bộ pytest: `32 passed`, 6 cảnh báo deprecation từ Scapy.
![image](https://hackmd.io/_uploads/Bkkg_6STGg.png)
![image](https://hackmd.io/_uploads/SyEfO6S6ze.png)
