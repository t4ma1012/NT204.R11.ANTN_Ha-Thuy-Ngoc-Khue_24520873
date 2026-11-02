
# Testcase 12 - Malformed Packet

## 1. Mục tiêu

Kiểm tra hệ thống có thể xử lý packet không hợp lệ mà không làm chương trình bị crash.

## 2. Input

Packet chứa dữ liệu không đủ để tạo thành một IPv4 packet hoàn chỉnh.

Payload:

```text
45 00 00
```

## 3. Kết quả mong đợi

Hệ thống không phát sinh exception và trả về:

```json
{
  "protocol": "unknown"
}
```

## 4. Test

```bash
pytest -q
```

Kết quả mong đợi:

```text
16 passed
```

## 5. Kết luận

TC12 đạt khi malformed packet được xử lý an toàn và pipeline không bị crash.

## 6. Pipeline test

```powershell
python main.py --pcap TEST/malformed_packet/input.pcap --output TEST/malformed_packet/output.jsonl
```

![image](https://hackmd.io/_uploads/rJzIDgw5Gl.png)
![image](https://hackmd.io/_uploads/SJr0vxDcGe.png)
