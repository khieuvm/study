# 08 - Behavioral & Leadership (Senior/Lead) — Bilingual VI/EN

Câu hỏi behavioral và leadership cho phỏng vấn Senior/Lead C++.

---

## 1) Production & Incident

### Q1. Kể về 1 lần bạn xử lý production incident khó

**A:**
- EN: Use **STAR framework**: **S**ituation (system context, scale, impact), **T**ask (your specific responsibility), **A**ction (concrete steps: triage → mitigate → root cause → fix), **R**esult (measurable outcome + lessons learned + preventive actions). Show: calm under pressure, systematic approach, communication with stakeholders.
- VI: Dùng **khung STAR**: **S**ituation (bối cảnh hệ thống, quy mô, ảnh hưởng), **T**ask (trách nhiệm cụ thể của bạn), **A**ction (các bước cụ thể: triage → mitigate → root cause → fix), **R**esult (kết quả đo được + bài học + hành động phòng ngừa). Thể hiện: bình tĩnh dưới áp lực, cách tiếp cận có hệ thống, giao tiếp với stakeholder.

**Mẫu trả lời / Sample answer:**
> "Hệ thống giao dịch xử lý 10k req/s gặp memory leak gây latency tăng 5x trong 2 giờ. Tôi là người on-call, lập tức rollback deploy gần nhất để giảm thiểu, rồi dùng ASan trên staging tìm ra root cause: buffer không được free trong exception path hiếm gặp. Fix bằng unique_ptr, thêm unit test cho path đó. Kết quả: downtime giảm từ 2h xuống 15 phút cho incident tương tự, thêm alert cho memory growth trend."

Follow-up (EN): How do you decide between rollback and hotfix during an incident?

---

### Q2. Kể về 1 lần bất đồng kỹ thuật với đồng nghiệp

**A:**
- EN: Focus on: **(1)** data-driven discussion, not opinions. **(2)** User/business impact as the tiebreaker. **(3)** Prototype or benchmark to resolve disagreements objectively. **(4)** Disagree and commit — once decided, fully support the decision. Never make it personal.
- VI: Tập trung vào: **(1)** thảo luận dựa trên data, không ý kiến cá nhân. **(2)** User/business impact làm tiêu chí phân xử. **(3)** Prototype hoặc benchmark để giải quyết khách quan. **(4)** Disagree and commit — quyết rồi thì ủng hộ hoàn toàn. Không bao giờ công kích cá nhân.

**Mẫu trả lời / Sample answer:**
> "Đồng nghiệp muốn dùng custom lock-free queue, tôi đề xuất mutex + condition_variable. Thay vì tranh luận, tôi benchmark cả hai — mutex nhanh hơn 20% ở mức contention thấp (use case của chúng tôi) và code đơn giản hơn. Trình bày data cho team, mọi người chọn mutex. Bài học: để data nói thay."

Follow-up (EN): What do you do when the team chooses an approach you disagree with?

---

### Q3. Bạn mentor junior như thế nào?

**A:**
- EN: **(1)** Pair programming with clear learning goals (not just showing off). **(2)** Code review as teaching — explain the "why", not just "change this". **(3)** Assign stretch tasks with guardrails (review before merge, no production risk). **(4)** Regular 1:1 with progress tracking over 2-4 week cycles. **(5)** Gradually reduce oversight as competence grows.
- VI: **(1)** Pair programming với mục tiêu học rõ ràng (không phải show off). **(2)** Code review là dạy — giải thích "tại sao", không chỉ "sửa cái này". **(3)** Giao task thử thách có guardrail (review trước merge, không rủi ro production). **(4)** 1:1 định kỳ theo dõi tiến độ chu kỳ 2-4 tuần. **(5)** Dần giảm giám sát khi năng lực tăng.

Follow-up (EN): How do you handle a junior who is not improving despite mentoring?

---

## 2) Ownership & Prioritization

### Q4. Senior ownership nghĩa là gì?

**A:**
- EN: Beyond writing code. Ownership means: **(1)** Clarify requirements before building. **(2)** Design for observability and failure modes. **(3)** Quality gates: tests, code review, CI. **(4)** Rollout strategy: feature flags, canary, gradual rollout. **(5)** On-call readiness and incident response. **(6)** Proactive maintenance: tech debt, security patches, dependency updates.
- VI: Không chỉ viết code. Ownership nghĩa là: **(1)** Clarify yêu cầu trước khi xây dựng. **(2)** Thiết kế cho observability và failure mode. **(3)** Quality gate: test, code review, CI. **(4)** Chiến lược rollout: feature flag, canary, gradual rollout. **(5)** Sẵn sàng on-call và xử lý incident. **(6)** Bảo trì chủ động: tech debt, security patch, update dependency.

Follow-up (EN): How do you balance ownership with delegation?

---

### Q5. Làm sao cân bằng tốc độ và chất lượng?

**A:**
- EN: **(1)** Separate must-have from nice-to-have — ship incrementally. **(2)** Guardrails that don't slow you down: automated tests, CI, linting. **(3)** "Good enough" for the current stage — don't over-engineer. **(4)** Time-box spikes and investigations. **(5)** Monitor after ship — fix forward when possible.
- VI: **(1)** Tách must-have khỏi nice-to-have — ship dần. **(2)** Guardrail không làm chậm: test tự động, CI, linting. **(3)** "Đủ tốt" cho giai đoạn hiện tại — không over-engineer. **(4)** Time-box spike và investigation. **(5)** Monitor sau khi ship — fix forward khi có thể.

Follow-up (EN): How do you communicate trade-offs to non-technical stakeholders?

---

## 3) Communication

### Q6. Cách giải thích vấn đề kỹ thuật cho PM/Business?

**A:**
- EN: Translate to **impact language**: money, risk, timeline, user pain. Avoid jargon. Use analogies. Structure: "The problem is X. It affects Y users/Z revenue. We have two options: A (fast, risky) or B (slower, safer). I recommend B because..." Let them make the business decision with your technical input.
- VI: Dịch sang **ngôn ngữ impact**: tiền, rủi ro, timeline, ảnh hưởng user. Tránh thuật ngữ. Dùng ví dụ tương tự. Cấu trúc: "Vấn đề là X. Ảnh hưởng Y user/Z doanh thu. Có 2 option: A (nhanh, rủi ro) hoặc B (chậm hơn, an toàn). Tôi đề xuất B vì..." Để họ quyết định business với input kỹ thuật của bạn.

Follow-up (EN): How do you handle a PM who wants to skip testing to meet a deadline?

---

### Q7. Khi nào cần escalate?

**A:**
- EN: When: **(1)** Risk exceeds your authority/scope. **(2)** Deadline/SLA is threatened and you can't resolve alone. **(3)** Cross-team decision needed. **(4)** Safety or security concern. How: bring the problem + proposed solutions + recommendation. Never escalate empty-handed.
- VI: Khi: **(1)** Rủi ro vượt authority/scope của bạn. **(2)** Deadline/SLA bị đe dọa và bạn không thể giải quyết một mình. **(3)** Cần quyết định cross-team. **(4)** Lo ngại an toàn hoặc bảo mật. Cách: đem vấn đề + giải pháp đề xuất + recommendation. Không bao giờ escalate tay không.

Follow-up (EN): How do you escalate without undermining your direct manager?

---

## 4) Conflict Management

### Q8. Teammate review rất khó tính — xử lý sao?

**A:**
- EN: **(1)** Align on coding standards/style guide beforehand — removes subjective disagreements. **(2)** Separate objective issues (bugs, performance) from style preferences. **(3)** If discussion goes long in comments, switch to a short call. **(4)** If pattern persists, discuss privately — "I value your thoroughness, can we agree on what's blocking vs nice-to-have?"
- VI: **(1)** Thống nhất coding standard/style guide trước — loại bỏ tranh luận chủ quan. **(2)** Tách vấn đề khách quan (bug, performance) khỏi sở thích style. **(3)** Nếu thảo luận dài trong comment, chuyển sang call ngắn. **(4)** Nếu vẫn tiếp diễn, nói riêng — "Tôi trân trọng sự kỹ lưỡng, có thể thống nhất gì là blocking vs nice-to-have?"

Follow-up (EN): When should you involve a tech lead in a code review disagreement?

---

### Q9. Bạn làm sai gây lỗi production — xử lý sao?

**A:**
- EN: **(1)** Own it immediately — don't hide or blame. **(2)** Mitigate first (rollback/hotfix), then investigate. **(3)** Write a blameless postmortem. **(4)** Propose preventive actions (better tests, deployment guards, review process). **(5)** The response to mistakes defines your credibility — owning mistakes builds trust.
- VI: **(1)** Nhận trách nhiệm ngay — không giấu hay đổ lỗi. **(2)** Giảm thiểu trước (rollback/hotfix), rồi điều tra. **(3)** Viết postmortem blameless. **(4)** Đề xuất hành động phòng ngừa (test tốt hơn, deployment guard, review process). **(5)** Cách xử lý sai lầm quyết định uy tín — nhận lỗi tạo niềm tin.

Follow-up (EN): What is the difference between accountability and blame?

---

## 5) Career Signal

### Q10. Điều gì phân biệt mid-level và senior trong phỏng vấn?

**A:**
- EN: **Mid**: solves well-defined problems with good code. **Senior**: **(1)** Makes trade-off decisions and explains them. **(2)** Designs systems, not just components. **(3)** Owns end-to-end: requirements → design → implementation → deployment → monitoring. **(4)** Elevates the team: mentoring, code review culture, documentation. **(5)** Communicates technical decisions to non-technical stakeholders.
- VI: **Mid**: giải bài toán rõ ràng với code tốt. **Senior**: **(1)** Quyết định trade-off và giải thích được. **(2)** Thiết kế hệ thống, không chỉ component. **(3)** Sở hữu end-to-end: yêu cầu → thiết kế → triển khai → deployment → monitoring. **(4)** Nâng team: mentoring, văn hóa code review, documentation. **(5)** Truyền đạt quyết định kỹ thuật cho stakeholder không kỹ thuật.

**Câu mẫu ngắn khi phỏng vấn / Short templates:**
- "Tôi ưu tiên data và impact trước, opinion sau."
- "Tôi đề xuất 2 option kèm trade-off, estimate, và risk rollback."
- "Sau mỗi incident, tôi có action item với owner rõ ràng — không để bài học bị quên."

Follow-up (EN): How do you demonstrate senior-level impact during an interview?

---

## Flash card (ôn nhanh)

| Câu hỏi / Question | Trả lời nhanh / Quick answer |
|---|---|
| STAR framework? | Situation → Task → Action → Result |
| Bất đồng kỹ thuật? | Data-driven, prototype/benchmark, disagree-and-commit |
| Mentor junior? | Pair programming + teaching code review + stretch tasks |
| Senior ownership? | Không chỉ code — requirements, quality, rollout, on-call |
| Tốc độ vs chất lượng? | Must-have first, guardrails, ship incremental |
| Giải thích cho PM? | Ngôn ngữ impact: tiền, rủi ro, timeline, user |
| Khi nào escalate? | Vượt authority, SLA risk, cross-team, security |
| Review khó tính? | Align standard trước, tách objective vs style, call ngắn |
| Lỗi production? | Nhận lỗi → mitigate → postmortem → preventive actions |
| Mid vs Senior? | Senior: trade-off, system design, end-to-end ownership, nâng team |
