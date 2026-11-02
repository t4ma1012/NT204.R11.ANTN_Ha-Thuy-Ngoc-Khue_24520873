# T05 - Rule direction

## Mục tiêu

Kiểm tra `->` chỉ khớp source đến destination, còn `<>` khớp cả chiều thuận lẫn chiều đảo giữa cùng hai endpoint.

## Dữ liệu đầu vào

`input.rules` có hai rule với cùng endpoint và selector, một rule một chiều (`->`) và một rule hai chiều (`<>`). Unit test kiểm tra mỗi rule với event theo hai hướng.

## Cách chạy

```cmd
python -m pytest -q tests\test_rule_loader.py -k direction
```

## Kết quả mong đợi

- Rule `->`: khớp event source→destination, không khớp event đảo chiều.
- Rule `<>`: khớp cả event thuận và event đảo chiều.
- Direction được giữ chính xác trong Internal Rule Object.

## Kết quả thực tế

Đạt. Rule `->` khớp chiều thuận và không khớp chiều đảo; rule `<>` khớp cả hai chiều. Kết quả được lưu trong `output.json`.

- T05: `1 passed`.
![image](https://hackmd.io/_uploads/rkff6pH6fl.png)

- Toàn bộ pytest: `35 passed`, 6 cảnh báo deprecation từ Scapy.
![image](https://hackmd.io/_uploads/ry776pBpfx.png)
