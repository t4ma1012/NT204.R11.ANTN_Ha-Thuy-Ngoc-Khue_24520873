# T11 - Distance / Within

## Mục tiêu

Kiểm tra hai content theo thứ tự và ràng buộc vị trí tương đối: `distance` đặt khoảng cách tối thiểu từ cuối content trước đến đầu content tiếp theo; `within` giới hạn vùng tính từ cuối content trước đến hết content tiếp theo. Các giới hạn tuyệt đối `offset`/`depth` trên content thứ hai giao với các ràng buộc tương đối.

## Dữ liệu đầu vào

`input.rules` xác định `HEAD` rồi `TAIL`. Content thứ hai cần ít nhất 2 byte khoảng cách, phải kết thúc trong 8 byte tính từ cuối `HEAD`, đồng thời nằm trong vùng tuyệt đối bắt đầu tại byte 6, dài 6 byte.

## Cách chạy riêng T11

```cmd
python -m pytest -q tests\test_rule_loader.py -k test_content_distance_within
```

## Kết quả mong đợi

- `HEAD--TAIL`, `HEAD---TAIL` và `HEAD----TAIL` match.
- Khoảng cách dưới `distance`, hoặc content vượt ngoài `within`/`offset`/`depth`, không match.
- Rule có modifier quan hệ thiếu content trước đó hoặc giá trị âm/không dương bị phân loại `invalid`.

## Kết quả thực tế

Đạt: cả ba payload có `TAIL` trong vùng giới hạn tạo detection; payload có khoảng cách không đủ, vượt vùng hoặc sai thứ tự đều không match. Kiểm thử riêng `distance` và `within` cũng xác nhận từng cận dưới/cận trên, đồng thời xác nhận `offset`/`depth` giao với các ràng buộc quan hệ và giá trị sai bị phân loại `invalid`.
