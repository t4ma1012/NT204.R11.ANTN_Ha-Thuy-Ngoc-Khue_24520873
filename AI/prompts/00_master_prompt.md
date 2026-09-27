# MASTER PROMPT — Dán đầu mọi session Claude mới

Dùng đoạn này làm tin nhắn ĐẦU TIÊN mỗi khi mở một session Claude mới
(dù đổi account, đổi máy, hay đổi cửa sổ VS Code). Claude không có bộ nhớ
giữa các session — toàn bộ trạng thái project nằm trong các file dưới đây,
không nằm trong lịch sử chat.

---

Trước khi làm bất kỳ việc gì, đọc đầy đủ các file sau theo đúng thứ tự:

```
AI/MASTER_CONTEXT.md
AI/PROJECT_RULES.md
AI/CURRENT_STATUS.md
AI/ARCHITECTURE.md
AI/TASK_BOARD.md
AI/DECISIONS.md
AI/CHANGELOG.md
```

Sau khi đọc xong, tóm tắt ngắn gọn lại cho tôi:
1. Assignment hiện tại là gì
2. Task tiếp theo cần làm là task nào (task đầu tiên chưa tick trong TASK_BOARD.md)
3. Có quyết định kiến trúc quan trọng nào trong DECISIONS.md cần lưu ý không

Sau đó DỪNG LẠI và hỏi tôi có muốn bắt đầu task đó không — KHÔNG tự ý code
hay sửa file nào trước khi tôi xác nhận.

## Quy tắc bắt buộc trong suốt session (tóm tắt từ PROJECT_RULES.md)

* Chỉ làm đúng 1 task tại một thời điểm (Rule 05 — Minimal Changes).
* Không tự ý đổi function signature / class interface / data model /
  event schema / CLI behavior nếu ảnh hưởng module khác (Rule 06).
  Nếu bắt buộc phải đổi → ghi vào AI/DECISIONS.md.
* Không thêm dependency mới nếu không thật sự cần (Rule 07).
* Parser phải xử lý an toàn, không crash với malformed/truncated/missing
  data (Rule 08).
* Mỗi feature quan trọng phải có test, không xóa test vì nó đang fail
  (Rule 09).
* KHÔNG tự động `git commit` — chỉ đề xuất lệnh + commit message, tôi tự
  chạy (Rule 11).
* Không tự implement task/assignment tương lai khi tôi chỉ yêu cầu task
  hiện tại (Rule 12).
* Sau khi hoàn thành task: cập nhật AI/CURRENT_STATUS.md, AI/TASK_BOARD.md,
  AI/CHANGELOG.md nếu trạng thái đổi (Rule 13), rồi báo cáo đầy đủ theo
  Rule 15 (file nào đổi, thay đổi gì, test nào đã chạy, kết quả, ảnh hưởng
  kiến trúc, vấn đề còn tồn tại, commit message đề xuất).

## Về yêu cầu nộp bài (không thuộc code, nhưng bắt buộc theo đề)

* Repo GitHub: 1 repo duy nhất cho toàn bộ bài tập lớn, đặt tên theo
  format `NT204.R11.ANTN_Ha.Thuy.Ngoc.Khue_24520873`, để public, nhánh mặc định `main`.
* Mỗi task / mỗi test case → 1 commit riêng, không gộp.
* Kết quả từng test case lưu vào thư mục `TEST/`.
* Nếu dùng AI hỗ trợ code, phải ghi rõ trong README.md: công cụ gì,
  dùng để làm gì, phần code nào có AI hỗ trợ.