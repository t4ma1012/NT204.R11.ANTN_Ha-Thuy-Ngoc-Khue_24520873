# T01 - HTTP URL Percent Decode

## Mục tiêu

Kiểm tra Decoder có thể giải mã URL percent-encoding trong HTTP URI.

## Input

```text
/search?q=%27%20OR%201%3D1
```

## Expected

URI sau khi giải mã:

```text
/search?q=' OR 1=1
```

Giá trị URI ban đầu phải được giữ lại để có thể đối chiếu với dữ liệu đã giải mã.

## Nội dung kiểm tra

- Giữ nguyên `raw_path`.
- Tạo `decoded_path`.
- Giải mã đúng các ký tự percent-encoded.
- Decoder không làm thay đổi dữ liệu gốc.

## Test

```bash
pytest tests/test_decoder.py::test_http_url_percent_decode -v
```

## Result

```text
PASS
```
![image](https://hackmd.io/_uploads/rJQesIo5zl.png)

