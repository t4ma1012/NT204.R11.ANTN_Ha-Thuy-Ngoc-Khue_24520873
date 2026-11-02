# T14 - Detection Event

## Mục tiêu

Kiểm tra Detection Event thống nhất chỉ được sinh sau khi rule match và chứa dữ liệu rule, normalized event, flow context cùng thông tin match.

## Dữ liệu đầu vào

`input.rules` gồm rule match content `../` với `sid`, `rev`, `msg`, `priority`, `classtype`, một rule control không match và rule chỉ có metadata cơ bản. Kiểm thử tạo flow context qua Flow Tracker rồi truyền normalized event cho Evaluation Engine.

## Cách chạy riêng T14

```cmd
python -m pytest -q tests\test_rule_loader.py -k test_detection_event_generation
```

## Kết quả mong đợi

- Rule match tạo một event có timestamp, metadata rule, 5-tuple, protocol, application protocol, flow ID và match info.
- Metadata không có trong rule không được tự tạo.
- Application protocol/flow ID thiếu thì không được tự đoán.
- Rule không match không tạo Detection Event.

## Kết quả thực tế

Đạt: event có đủ normalized fields được giữ nguyên trong detection; flow ID lấy từ Flow Tracker; rule thiếu priority/classtype không tạo các field đó; thiếu application protocol/flow context giữ giá trị `None`. Rule không match không sinh Detection Event.


- T14:
![image](https://hackmd.io/_uploads/ryEcwRBafe.png)


- Toàn bộ pytest: `44 passed`, 6 cảnh báo deprecation từ Scapy.

![image](https://hackmd.io/_uploads/SyiiDCSpfe.png)

