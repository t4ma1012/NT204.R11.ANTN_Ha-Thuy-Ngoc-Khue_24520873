# T09 - Content matching and nocase

## Mục tiêu

Kiểm tra content matching trên payload/application data: mặc định phân biệt hoa thường, còn `nocase` thì không phân biệt. Xác nhận detection result ghi lại content và field đã khớp.

## Dữ liệu đầu vào

`input.rules` gồm một rule `content` thường và một rule có `nocase`. Unit test dùng application data đã decoded, không dùng raw packet.

## Cách chạy

```cmd
python -m pytest -q tests\test_rule_loader.py -k test_content_matching
```

## Kết quả mong đợi

- Với application data `ADMIN`, chỉ rule có `nocase` match.
- Với application data `Admin`, cả hai rule match.
- Match information ghi pattern, field chứa match và trạng thái `nocase`.

## Kết quả thực tế

Đạt: kiểm thử xác nhận `ADMIN` chỉ match rule có `nocase`; `Admin` match cả hai rule. Cả hai detection đều ghi pattern, field và trạng thái `nocase` trong `match_info`.
