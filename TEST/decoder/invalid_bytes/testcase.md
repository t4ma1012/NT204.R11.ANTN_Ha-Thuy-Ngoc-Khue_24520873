# T04 – Invalid Bytes

## Mục tiêu

Kiểm tra Decoder xử lý byte sequence không hợp lệ UTF-8 mà không làm chương trình bị crash.

## Input

```text
b"Hello \xff World"
```

## Expected

- Không phát sinh exception.
- Decoder vẫn trả về kết quả.
- Byte không hợp lệ được thay thế bằng ký tự `�`.
- `decode_status` có giá trị `partial`.
- Chương trình tiếp tục xử lý bình thường.

## Output

Kết quả thực tế được ghi tự động vào:

```text
output.json
```

![image](https://hackmd.io/_uploads/SJ8mX3hczx.png)
![image](https://hackmd.io/_uploads/HkyEm32cMe.png)
