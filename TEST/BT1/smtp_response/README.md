# Testcase 10 - SMTP Response

## 1. Mục tiêu

Kiểm tra khả năng phát hiện và phân tích SMTP response, bao gồm mã trạng thái SMTP.

## 2. Input

PCAP:

`TEST/smtp_response/input.pcap`

Packet được trích từ:

`data/pcap/all.pcapng`

Packet số: `22`

Payload:

```text
220 victim.sanogo.de ESMTP Postfix (Ubuntu)
```

## 3. Kết quả mong đợi

SMTP response được nhận diện với:

- Type: `response`
- Status code: `220`
- Message: `victim.sanogo.de ESMTP Postfix (Ubuntu)`

## 4. Test

```bash
pytest -q
```

Kết quả mong đợi:

```text
14 passed
```

## 5. Pipeline test

```bash
python main.py --pcap TEST/smtp_response/input.pcap --output TEST/smtp_response/output.jsonl
```

Kết quả phải được ghi ra JSON Lines tại:

`TEST/smtp_response/output.jsonl`

![image](https://hackmd.io/_uploads/SyLDrev9Me.png)
![image](https://hackmd.io/_uploads/H1aOBlDqMg.png)
