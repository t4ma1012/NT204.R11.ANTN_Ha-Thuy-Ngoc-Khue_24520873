# T03 - Unsupported keyword

## Mục tiêu

Kiểm tra rule có cú pháp option hợp lệ nhưng dùng keyword `pcre` ngoài phạm vi hỗ trợ được phân loại `unsupported`, không bị nhầm là `invalid`, và không làm dừng loader.

## Dữ liệu đầu vào

`input.rules` có một rule TCP chứa `pcre` và một rule UDP dùng các keyword được hỗ trợ.

## Cách chạy

```cmd
python -m pytest -q tests\test_rule_loader.py -k unsupported_keyword
```

## Kết quả mong đợi

- Rule TCP được phân loại `unsupported`, với lý do chỉ rõ keyword `pcre`.
- Rule UDP tiếp theo được phân loại `valid`.
- Loader hoàn tất mà không crash.

## Kết quả thực tế

Đạt. Rule TCP được phân loại `unsupported` với lý do `unsupported keyword 'pcre'`; loader tiếp tục và rule UDP được phân loại `valid`. Kết quả được lưu trong `output.json`.

- T03: `1 passed`.
![image](https://hackmd.io/_uploads/ryDUtpS6fe.png)


- Toàn bộ pytest: `33 passed`, 6 cảnh báo deprecation từ Scapy.
![image](https://hackmd.io/_uploads/rk4_K6B6Me.png)
