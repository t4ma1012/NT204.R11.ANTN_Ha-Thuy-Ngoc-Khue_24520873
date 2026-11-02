# T01 - Load rules with comments and blank lines

## Mục tiêu

Kiểm tra Rule Loader bỏ qua dòng trống và comment, đồng thời chỉ chuyển các dòng rule đến parser.

## Dữ liệu đầu vào

`input.rules` gồm hai rule (TCP và UDP), xen kẽ comment và dòng trống.

## Cách chạy

```powershell
python -m pytest -q tests/test_rule_loader.py
```

## Kết quả mong đợi

- Parser nhận đúng hai dòng rule theo thứ tự trong file.
- Comment và dòng trống không được chuyển đến parser.

## Kết quả thực tế

Đạt. Parser nhận đúng hai dòng rule theo thứ tự; comment và dòng trống được bỏ qua. Kết quả thực tế được lưu trong `output.json`.

- Test T01: `1 passed`.
- Toàn bộ pytest: `31 passed`, 6 cảnh báo deprecation từ Scapy.
![image](https://hackmd.io/_uploads/HyLWjnH6zg.png)
![image](https://hackmd.io/_uploads/SkBGihSafl.png)
