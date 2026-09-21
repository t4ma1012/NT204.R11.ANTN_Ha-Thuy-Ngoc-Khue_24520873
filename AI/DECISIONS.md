# ARCHITECTURE DECISIONS

File này ghi lại các quyết định quan trọng ảnh hưởng tới kiến trúc project.

---

## Decision 001 — One Repository

### Decision

Tất cả assignment của IDS được phát triển trong một repository.

### Reason

Project là một hệ thống IDS dài hạn. Các assignment sau sẽ sử dụng và mở rộng code của assignment trước.

### Status

Accepted.

---

## Decision 002 — Shared Parsing Pipeline

### Decision

Live traffic và PCAP phải sử dụng cùng một parsing pipeline.

### Reason

Tránh duplicate logic và đảm bảo behavior của parser nhất quán giữa live traffic và PCAP.

### Status

Accepted.

---

## Decision 003 — Normalized Event Boundary

### Decision

Normalized IDS Event là interface giữa parser và các module IDS phía sau.

### Reason

Detection Engine trong tương lai không được phụ thuộc trực tiếp vào packet object của thư viện capture.

### Status

Accepted.

---

## Decision 004 — Incremental Development

### Decision

Project được phát triển theo từng task nhỏ.

### Reason

Dễ test, dễ debug, dễ review và giữ Git history rõ ràng.

### Status

Accepted.

---

## Decision 005 — AI-Assisted Development

### Decision

AI được sử dụng để hỗ trợ architecture, implementation, review và debugging.

### Reason

Tăng tốc quá trình phát triển nhưng vẫn yêu cầu người thực hiện kiểm tra và hiểu code.

### Status

Accepted.

---

## Future Decisions

Các quyết định kiến trúc mới sẽ được thêm vào đây.

Format:

```text
## Decision XXX — Title

### Decision

...

### Reason

...

### Alternatives

...

### Status

Accepted / Rejected / Superseded
```
