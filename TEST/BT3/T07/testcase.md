# T07 - Header mismatch filtering

## Mục tiêu

Xác minh event không khớp protocol, IP hoặc port bị loại bởi header trước khi gọi content matcher, và không tạo Detection Event.

## Dữ liệu đầu vào

`input.rules` có rule TCP và UDP với content `MATCHME`. Unit test gửi payload chứa content này nhưng lần lượt làm sai protocol, source IP hoặc destination port; một event khớp header được dùng làm đối chứng.

## Cách chạy

```cmd
python -m pytest -q tests\test_rule_loader.py -k header_mismatch
```

## Kết quả mong đợi

- Với header mismatch, content matcher không được gọi và không có Detection Event.
- Với header match và content match, evaluator chuyển rule đến content matcher và sinh một Detection Event.

## Kết quả thực tế

Đạt. Với rule TCP đang được kiểm tra, event UDP cùng địa chỉ và port không đến content matcher; event TCP có sai IP hoặc port cũng không đến matcher. Cả ba trường hợp không sinh Detection Event. Event đối chứng khớp header và content tạo một event. Kết quả được lưu trong `output.json`.

- T07: `1 passed`.

![image](https://hackmd.io/_uploads/SkVBkRBTMl.png)

- Toàn bộ pytest: `37 passed`, 6 cảnh báo deprecation từ Scapy.

![image](https://hackmd.io/_uploads/HkvIkCH6fe.png)

