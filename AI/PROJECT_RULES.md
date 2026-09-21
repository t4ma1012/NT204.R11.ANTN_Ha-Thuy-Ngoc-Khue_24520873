# PROJECT RULES

Các quy tắc dưới đây áp dụng cho toàn bộ IDS Project.

## Rule 01 — One Project

Tất cả assignment phải nằm trong cùng một repository.

Không tạo repository mới cho từng assignment nếu không có yêu cầu đặc biệt.

---

## Rule 02 — Preserve Architecture

Không được tự ý thay đổi kiến trúc tổng thể.

Kiến trúc chính:

```text
Capture
→ Parsing
→ Protocol Detection
→ Protocol Parsing
→ Normalized Event
→ Features
→ Detection
→ Alerts
```

---

## Rule 03 — Shared Pipeline

Live traffic và PCAP phải sử dụng cùng parser pipeline.

Không được tạo hai parser độc lập chỉ vì input khác nhau.

---

## Rule 04 — Normalized Event

Sau tầng parser, dữ liệu phải được chuyển thành normalized event.

Các module downstream phải sử dụng normalized event.

Không cho Detection Engine phụ thuộc trực tiếp vào Scapy/PyShark packet.

---

## Rule 05 — Minimal Changes

Mỗi task chỉ được sửa những file cần thiết.

Không rewrite những module không liên quan.

---

## Rule 06 — No Silent Interface Changes

Không tự ý thay đổi:

* function signature
* class interface
* data model
* event schema
* CLI behavior

nếu thay đổi đó ảnh hưởng tới module khác.

Nếu bắt buộc phải thay đổi, phải ghi vào:

```text
AI/DECISIONS.md
```

---

## Rule 07 — No Unnecessary Dependencies

Không thêm library nếu Python standard library hoặc dependency hiện tại đã đáp ứng được yêu cầu.

Mọi dependency mới phải có lý do.

---

## Rule 08 — Error Handling

Input không hợp lệ không được làm chương trình crash toàn bộ.

Parser phải xử lý an toàn:

* malformed packets
* truncated packets
* missing fields
* empty payload
* invalid encoding
* unsupported protocols

---

## Rule 09 — Tests

Mỗi feature quan trọng phải có test.

Không xóa test chỉ vì test đang fail.

Nếu test fail:

1. tìm nguyên nhân
2. sửa implementation hoặc test nếu test sai
3. chạy lại
4. ghi nhận kết quả

---

## Rule 10 — Git History

Không:

* xóa Git history
* force push làm mất lịch sử
* squash toàn bộ lịch sử một cách tùy tiện
* rewrite commit của task cũ

Mỗi task/test quan trọng nên có commit riêng.

---

## Rule 11 — AI Must Not Auto Commit

AI không tự động commit trừ khi user yêu cầu rõ ràng.

Sau khi hoàn thành task, AI chỉ đề xuất commit message.

User sẽ kiểm tra:

```bash
git diff
git status
pytest -q
```

sau đó tự commit.

---

## Rule 12 — No Future Work Without Request

Không tự implement các assignment tương lai khi user chỉ yêu cầu task hiện tại.

Chỉ thiết kế extension point nếu cần để không phá kiến trúc.

---

## Rule 13 — Update Context

Sau mỗi task, cập nhật:

```text
AI/CURRENT_STATUS.md
AI/TASK_BOARD.md
AI/CHANGELOG.md
```

nếu trạng thái project thay đổi.

---

## Rule 14 — Understand Before Coding

AI phải đọc context và inspect code hiện tại trước khi sửa.

Không được đoán cấu trúc project.

---

## Rule 15 — Explain Important Changes

Sau khi hoàn thành task, AI phải báo:

* file nào thay đổi
* thay đổi gì
* test nào đã chạy
* kết quả test
* architecture impact
* vấn đề còn tồn tại
* commit message đề xuất
