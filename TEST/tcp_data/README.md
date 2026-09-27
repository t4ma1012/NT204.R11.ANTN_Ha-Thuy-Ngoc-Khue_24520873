
![image](https://hackmd.io/_uploads/Hyv_wJD9Me.png)
![image](https://hackmd.io/_uploads/H1Xtvyv5zl.png)
# Testcase 02 - TCP Data

## 1. Mục tiêu

Kiểm tra khả năng parse một TCP packet có payload.

## 2. Input

File:

```text
input.pcap

Input được trích xuất từ:

data/pcap/all.pcapng

Testcase sử dụng packet TCP có payload với độ dài 185 bytes.

3. Thành phần đã thay đổi
TCP Parser

File:

src/parser/transport/tcp.py

Bổ sung khả năng lấy:

Payload length
Payload content

Payload được decode bằng UTF-8 và sử dụng errors="replace" để tránh lỗi khi dữ liệu không decode được.

Parser Pipeline

File:

src/pipeline/parser_pipeline.py

Tiếp tục sử dụng TCP parser để tạo event cho packet.

Main

File:

main.py

Đọc PCAP, xử lý packet qua pipeline và ghi kết quả ra JSON Lines.

4. Chạy testcase
python main.py --pcap TEST/tcp_data/input.pcap --output TEST/tcp_data/output.jsonl
5. Kết quả

Input:

1 TCP packet

Packet có:

TCP flags: PA
Payload length: 185 bytes

Payload bắt đầu bằng:

POST /ping.php HTTP/1.1

Kết quả được ghi vào:

TEST/tcp_data/output.jsonl
6. Kiểm tra
pytest

Kết quả:

7 passed
7. Ghi chú

Packet được sử dụng cho TC02 có chứa HTTP POST payload. Ở TC02 chỉ kiểm tra việc TCP parser nhận diện và lấy payload. Việc phân tích HTTP POST sẽ được thực hiện ở testcase HTTP POST.