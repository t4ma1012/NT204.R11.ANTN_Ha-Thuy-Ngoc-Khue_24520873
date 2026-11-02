# T04 - Parse TCP rule header

## Mục tiêu

Kiểm tra parser chuyển header TCP thành các trường có cấu trúc, hỗ trợ IP `any`, IPv4 đơn, CIDR và port `any`, đơn, range.

## Dữ liệu đầu vào

`input.rules` gồm ba header TCP để bao phủ các dạng địa chỉ và port trong yêu cầu.

## Cách chạy

```cmd
python -m pytest -q tests\test_rule_loader.py -k tcp_header
```

## Kết quả mong đợi

- Tất cả rule có trạng thái `valid` và protocol `tcp`.
- Trường địa chỉ chứa `type=any` hoặc network IPv4 dạng chuẩn CIDR.
- Trường port chứa `type=any`, `type=single` hoặc `type=range`, cùng giá trị bắt đầu/kết thúc.

## Kết quả thực tế

Đạt. Cả ba rule được parse thành `valid`; địa chỉ IPv4 đơn được chuẩn hóa thành `/32`, CIDR được giữ dạng network, port đơn được biểu diễn với cùng giá trị start/end và port range giữ đúng hai đầu mút. Kết quả được lưu trong `output.json`.

- T04: `1 passed`.
![image](https://hackmd.io/_uploads/rJMZipBpMl.png)

- Toàn bộ pytest: `34 passed`, 6 cảnh báo deprecation từ Scapy.
![image](https://hackmd.io/_uploads/SyXMi6Sazl.png)
