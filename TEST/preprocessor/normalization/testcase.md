# T05 – Normalization

## Mục tiêu

Kiểm tra Preprocessor chuẩn hóa các trường dữ liệu của event.

## Input

Event chứa protocol, IP, HTTP header, URI và timestamp ở dạng chưa chuẩn hóa.

## Expected

- Protocol được chuẩn hóa.
- IP được chuẩn hóa.
- HTTP header được chuẩn hóa.
- URI/path được chuẩn hóa an toàn.
- Timestamp được đưa về định dạng thống nhất.
- Không làm thay đổi dữ liệu ngoài phạm vi normalization.

## Output

Kết quả được ghi vào `output.json`.
![image](https://hackmd.io/_uploads/S1wpX6hqGx.png)
![image](https://hackmd.io/_uploads/HJ_14pn5fl.png)
