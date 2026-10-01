# T02 - HTML Entity Decode

## Mục tiêu

Kiểm tra Decoder có thể giải mã HTML entity trong HTTP body.

## Input

```text
&lt;script&gt;alert(&quot;x&quot;)&lt;/script&gt;
```

## Expected

```html
<script>alert("x")</script>
```

## Nội dung kiểm tra

- Giữ nguyên `raw_body`.
- Tạo `decoded_body`.
- Giải mã đúng HTML entity.
- Decoder không làm thay đổi dữ liệu gốc.

## Test

```bash
pytest tests/test_decoder.py::test_html_entity_decode -v
```

## Result

```text
PASS
```

![image](https://hackmd.io/_uploads/SkrHjUo5Gg.png)
![image](https://hackmd.io/_uploads/SkGwoIo9Gg.png)

