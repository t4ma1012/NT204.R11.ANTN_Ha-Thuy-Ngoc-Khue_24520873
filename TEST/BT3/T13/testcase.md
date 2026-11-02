# T13 - Multiple Rules Matching

## Mục tiêu

Xác nhận Rule Evaluation Engine duyệt toàn bộ candidate rules cho một event, trả về mọi detection match và không tạo kết quả cho rule không match.

## Dữ liệu đầu vào

`input.rules` gồm hai rule tìm `ALPHA`/`BETA` và một rule control tìm `GAMMA`. Một event TCP có payload chứa hai pattern đầu nhưng không chứa pattern control.

## Cách chạy riêng T13

```cmd
python -m pytest -q tests\test_rule_loader.py -k test_multiple_rules_matching_single_event
```

## Kết quả mong đợi

- Một event trả về hai detection, một cho mỗi rule match.
- Rule tìm `GAMMA` không có trong kết quả.
- Cả hai detection giữ đúng rule và thông tin content match.

## Kết quả thực tế

Đạt: Repository trả về 3 candidate rules; event tạo đúng 2 detection cho SID `1000040` và `1000041`, với content khớp tương ứng `ALPHA` và `BETA`. Rule `GAMMA` không tạo kết quả.

- T13:
![image](https://hackmd.io/_uploads/HyKVIRBTzl.png)


- Toàn bộ pytest: `43 passed`, 6 cảnh báo deprecation từ Scapy.
![image](https://hackmd.io/_uploads/Syiv80STfl.png)
