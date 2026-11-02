# T06 - Rule Repository / Indexer

## Mục tiêu

Kiểm tra repository chọn đúng candidate theo protocol TCP/UDP, địa chỉ IPv4/CIDR, port đơn/range và wildcard `any`.

## Dữ liệu đầu vào

`input.rules` gồm rule TCP/UDP có selector cụ thể, rule wildcard và rule không phù hợp địa chỉ.

## Cách chạy

```cmd
python -m pytest -q tests\test_rule_loader.py -k repository_index
```

## Kết quả mong đợi

- Candidate chỉ chứa rule có protocol, IP, port và direction phù hợp event.
- Rule có selector `any` vẫn được xét như wildcard.
- Rule thuộc protocol hoặc địa chỉ không phù hợp bị loại khỏi kết quả.

## Kết quả thực tế

Đạt. TCP event chỉ nhận được rule TCP phù hợp CIDR/port và rule TCP wildcard; UDP queries nhận đúng rule wildcard hoặc CIDR/port-range tương ứng. Rule có protocol hoặc source network không phù hợp không xuất hiện trong candidate list. Kết quả được lưu trong `output.json`.

- T06: `1 passed`.
![image](https://hackmd.io/_uploads/rkOY06rpzg.png)

- Toàn bộ pytest: `36 passed`, 6 cảnh báo deprecation từ Scapy.
![image](https://hackmd.io/_uploads/B1hcCpHpze.png)
