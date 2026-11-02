# T12 - TCP Flags and Dsize

## Mục tiêu

Kiểm tra TCP `flags` và độ dài payload `dsize` theo event đã parse. Điều kiện trong cùng rule kết hợp theo AND. Hỗ trợ dsize chính xác, `>`, `<` và khoảng `min<>max` bao gồm hai đầu mút.

## Dữ liệu đầu vào

`input.rules` gồm rule kết hợp `flags:S` với ngưỡng dsize, rule độ dài chính xác và rule độ dài theo khoảng.

## Cách chạy riêng T12

```cmd
python -m pytest -q tests\test_rule_loader.py -k test_tcp_flags_and_dsize
```

## Kết quả mong đợi

- Rule có `flags:S; dsize:>4` match khi TCP event có S và payload dài hơn 4 byte; các điều kiện sai không match.
- `dsize:4` match đúng độ dài 4; `dsize:2<>6` match hai đầu mút và các giá trị nằm giữa.
- Rule có `flags` không match event UDP. Rule chỉ có `dsize` có thể match UDP nếu event cung cấp `payload_length`; thiếu độ dài hoặc sai kiểu không tạo detection.

## Kết quả thực tế

Đạt: rule `flags:S; dsize:>4` chỉ match TCP event có S và payload dài hơn 4 byte; exact size và hai đầu mút dsize range được kiểm tra riêng. Điều kiện flags fail closed với UDP hoặc thiếu field; dsize-only vẫn match TCP/UDP khi có `payload_length` hợp lệ.
- T12:

![image](https://hackmd.io/_uploads/S1FoB0BTfg.png)

- Toàn bộ pytest: `42 passed`, 6 cảnh báo deprecation từ Scapy.
![image](https://hackmd.io/_uploads/S1cnS0STfe.png)
