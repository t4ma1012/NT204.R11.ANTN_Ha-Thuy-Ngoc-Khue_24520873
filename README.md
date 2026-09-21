# IDS Project

Hệ thống tìm kiếm, phát hiện và ngăn chặn xâm nhập mạng (IDS).

Đây là project dài hạn được phát triển qua nhiều bài tập/assignment. Các module của từng assignment sẽ được tích hợp dần vào cùng một hệ thống.

## 1. Mục tiêu

Project hướng tới một kiến trúc IDS gồm các thành phần:

```text
Raw Packet
    ↓
Packet Capture
    ↓
Network Parser
    ↓
Transport Parser
    ↓
Application Protocol Detector
    ↓
Application Protocol Parser
    ↓
Normalized IDS Event
    ↓
Feature Extraction
    ↓
Detection Engine
    ↓
Alert Engine
    ↓
Storage / Dashboard
```

Các assignment sau sẽ bổ sung dần từng thành phần.

## 2. Nguyên tắc kiến trúc

- Live traffic và PCAP phải sử dụng chung một parsing pipeline.
- Parser tạo ra dữ liệu chuẩn hóa (`Normalized IDS Event`).
- Các module phía sau không được phụ thuộc trực tiếp vào packet object của Scapy/PyShark.
- Module Detection Engine chỉ làm việc với dữ liệu đã được normalize.
- Protocol không được hỗ trợ không được làm chương trình crash.
- Packet lỗi, packet thiếu header, payload rỗng hoặc payload không decode được phải được xử lý an toàn.
- Mỗi assignment chỉ bổ sung phần cần thiết, không phá vỡ kiến trúc hiện tại.

## 3. Cấu trúc project

```text
AI/        - Context, rules, task board và prompt cho AI
docs/      - Tài liệu kiến trúc và báo cáo
src/       - Source code chính
tests/     - Automated tests
TEST/      - Kết quả test của từng assignment
data/      - PCAP và dữ liệu mẫu
output/    - Log và output runtime
```

## 4. AI-assisted development

Project có sử dụng AI để hỗ trợ quá trình phát triển.

Các công cụ AI có thể được sử dụng:

- Claude: architecture và implementation
- Gemini: requirement và code review
- DeepSeek: debugging và testing

AI chỉ đóng vai trò hỗ trợ. Code trước khi đưa vào project phải được kiểm tra, chạy thử và người thực hiện phải hiểu được code.

## 5. Development workflow

Mỗi task được thực hiện theo quy trình:

```text
Understand
    ↓
Plan
    ↓
Implement
    ↓
Test
    ↓
Review
    ↓
Update project context
    ↓
Commit
```

Không tự động commit nếu chưa được yêu cầu.

## 6. Git

Mỗi assignment/task/test quan trọng cần có commit riêng để giữ lịch sử phát triển rõ ràng.

Không rewrite hoặc xóa Git history của project.

## 7. Current status

Xem:

```text
AI/CURRENT_STATUS.md
```

để biết trạng thái hiện tại của project.

Xem:

```text
AI/TASK_BOARD.md
```

để biết task nào đã hoàn thành và task tiếp theo là gì.