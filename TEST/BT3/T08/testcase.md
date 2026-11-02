# T08 - Flow matching

## Mục tiêu

Kiểm tra `flow:to_server`, `flow:to_client`, `flow:established` và `flow:not_established` dựa trên Flow Tracker context.

## Dữ liệu đầu vào

`input.rules` gồm rule cho request đã established, response đã established và request chưa established. Unit test tạo handshake qua `FlowTracker`, sau đó truyền context trả về từ tracker cho evaluator.

## Cách chạy

```cmd
python -m pytest -q tests\test_rule_loader.py -k flow_conditions
```

## Kết quả mong đợi

- Flow Tracker xác định `to_server` từ TCP SYN đầu tiên và `to_client` ở chiều phản hồi.
- `established` chỉ match khi context báo `ESTABLISHED`.
- `not_established` match context `NEW` hoặc `HANDSHAKE`, không match khi state đã established.
- Thiếu context không gây crash và không match rule có flow conditions.

## Kết quả thực tế

Đạt. Flow Tracker cung cấp `ESTABLISHED/to_server` cho request, `ESTABLISHED/to_client` cho response, và `HANDSHAKE/to_server` trước khi kết nối established. Mỗi context chỉ match đúng rule flow tương ứng. Khi không truyền context, không có rule flow nào match. Kết quả được lưu trong `output.json`.

- T08: `1 passed`.

![image](https://hackmd.io/_uploads/ryjLxCSTzl.png)

- Toàn bộ pytest: `38 passed`, 6 cảnh báo deprecation từ Scapy.
![image](https://hackmd.io/_uploads/SJg_e0Spze.png)
