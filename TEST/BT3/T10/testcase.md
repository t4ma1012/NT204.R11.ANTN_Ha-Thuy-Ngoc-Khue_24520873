# T10 - Offset / Depth

## Mục tiêu

Kiểm tra `offset` xác định vị trí bắt đầu tìm content và `depth` giới hạn độ dài vùng tìm kiếm tính từ offset (hoặc từ đầu payload nếu không có offset). Modifier được áp dụng cho content đứng trước; `depth` là số byte tối đa tính từ `offset` (0 nếu không khai báo `offset`).

## Dữ liệu đầu vào

`input.rules` gồm một rule kết hợp `offset` và `depth`, cùng một rule chỉ có `depth`. Kiểm thử chạy qua Rule Loader, Parser, Repository, Evaluator và Content Matcher với payload đã chuẩn hóa.

## Cách chạy riêng T10

```cmd
python -m pytest -q tests\test_rule_loader.py -k test_content_offset_depth
```

## Kết quả mong đợi

- `ALERT` xuất hiện trọn trong vùng byte `[4, 10)` thì match; nếu nằm ngoài vùng thì không match.
- `TOKEN` nằm trọn trong 5 byte đầu thì match; nếu chỉ xuất hiện sau vùng đó thì không match.
- Không có payload không tạo detection; modifier sai, thiếu content hoặc giá trị không hợp lệ được xử lý an toàn.

## Kết quả thực tế

Đạt: hai trường hợp trong vùng tạo detection; hai trường hợp ngoài vùng và event thiếu payload không tạo detection. Các rule thiếu content, có offset âm, hoặc depth bằng 0 được phân loại `invalid` với reason cụ thể. Kiểm thử cũng xác nhận offset/depth đếm byte UTF-8.
- T10:
![image](https://hackmd.io/_uploads/S1DtQASTMe.png)

- - Toàn bộ pytest: `40 passed`, 6 cảnh báo deprecation từ Scapy.
![image](https://hackmd.io/_uploads/ByziXAB6Gl.png)
