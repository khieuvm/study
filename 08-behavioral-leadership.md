# 08 - Behavioral và Leadership (Senior/Lead)

## 1) Các nhóm câu hỏi thường gặp

### Q1. Kế ve 1 lần ban xử lý production incident kho.
Khung trả lỗi STAR:
- S: context hệ thống, impact
- T: trach nhiem của ban
- A: hanh đóng cụ thể (triage, rollback, fix)
- R: kết quả do được + bài hoc + prevention

### Q2. Kế ve 1 lần bắt đóng kỹ thuật với đóng nghiep.
Dap an mạnh:
- Tap trung data và user impact
- Tránh cổng kích ca nhận
- Có experiment/prototype đệ quyết định

### Q3. Ban mentor junior như thế nào?
Dap an mạnh:
- Pair programming có mục tiêu
- Code review theo rubric
- Follow-up theo tien do 2-4 tuan

## 2) Ownership

### Q4. Senior ownership nghĩa là gì?
A: Không chỉ viết code. Bao gồm requirement clarity, quality gate, observability, rollout, incident handling.

### Q5. Làm sao cần bảng toc do và chất lượng?
A: Tách must-have vs nice-to-have, release increment, có guardrail test + monitoring.

## 3) Communication

### Q6. Cách giải thích van để kỹ thuật cho PM/Business?
A: Dùng ngon ngu impact: money, risk, timeline, user pain; tránh jargon qua sau.

### Q7. Khi nào cần escalate?
A: Khi rủi ro vuot authority/pham vì, ảnh hưởng deadline/SLA, cần quyết định cross-team.

## 4) Conflict management

### Q8. Nếu teammate review rat kho tinh?
A: Đóng bỏ expectation coding standard, tách issue objective, hen call ngan nếu chat dai đóng.

### Q9. Nếu ban làm sai trong production?
A: Nhận trach nhiem, rollback/fix nhanh, mình bach postmortem, để xuat preventive actions.

## 5) Career signal cho senior

### Q10. Dieu gì phân biệt mid và senior trong phỏng vấn?
A:
- Mid: giai bài toan code tốt
- Senior: quyết định trade-off, thiết kế hệ thống, ownership end-to-end, nang team

## 6) Mau câu trả lỗi ngan (để hoc)

- "Em ưu tiên data và impact trước, opinion sau."
- "Em để xuat 2 option kem trade-off, estimate, và risk rollback."
- "Sau mọi incident, em có action item với owner rõ ràng, không để bài hoc bi quen."
