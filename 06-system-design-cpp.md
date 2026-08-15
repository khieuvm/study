# 06 - System Design với C++ (Senior Interview) — Bilingual VI/EN

Kiến thức system design cho phỏng vấn Senior C++.

---

## 1) Design Mindset

### Q1. Trong system design C++ cần nhấn mạnh gì?

**A:**
- EN: C++ system design emphasizes: **latency** (p99, not just average), **memory footprint** (no GC — you control allocation), **failure modes** (crash vs hang vs data corruption), **ABI/deployment** (static vs dynamic linking), **observability** (metrics, logs, traces). Unlike web system design, you own the hardware-software boundary.
- VI: System design C++ nhấn mạnh: **latency** (p99, không chỉ trung bình), **memory footprint** (không GC — bạn kiểm soát cấp phát), **failure mode** (crash vs hang vs data corruption), **ABI/deployment** (static vs dynamic linking), **observability** (metrics, logs, traces). Khác web system design, bạn kiểm soát ranh giới phần cứng-phần mềm.

Follow-up (EN): How does C++ system design differ from Java/Go system design?

---

### Q2. Cách phân chia module cho codebase lớn?

**A:**
- EN: **(1)** Bounded contexts — each module owns its domain. **(2)** Clear API boundaries with explicit ownership (who allocates, who frees). **(3)** One-directional dependencies (DAG, no cycles). **(4)** Stable interfaces — use PIMPL or abstract base for internal evolution. **(5)** Separate build targets for independent compilation.
- VI: **(1)** Bounded context — mỗi module sở hữu domain riêng. **(2)** API boundary rõ ràng với ownership tường minh (ai cấp phát, ai giải phóng). **(3)** Dependency một chiều (DAG, không cycle). **(4)** Interface ổn định — dùng PIMPL hoặc abstract base. **(5)** Tách build target cho compilation độc lập.

Follow-up (EN): How do you handle circular dependencies between modules?

---

### Q3. Hexagonal/Clean architecture có phù hợp C++ không?

**A:**
- EN: Yes — separating domain logic from I/O and frameworks improves testability significantly. In C++, use abstract interfaces (or templates) as ports, with concrete adapters for file I/O, network, database. Trade-off: more indirection and boilerplate vs much easier unit testing.
- VI: Có — tách domain logic khỏi I/O và framework cải thiện testability đáng kể. Trong C++, dùng abstract interface (hoặc template) làm port, adapter cụ thể cho file I/O, network, database. Đánh đổi: nhiều indirection và boilerplate hơn nhưng unit test dễ hơn nhiều.

Follow-up (EN): How do you inject dependencies in C++ without a DI framework?

---

## 2) Cách trả lời bài Design

### Q4. Khung trả lời 7 bước?

**A:**
- EN: **(1)** Clarify requirements (functional + non-functional). **(2)** Define scope — what's in/out. **(3)** Capacity estimate (QPS, storage, bandwidth). **(4)** High-level architecture (boxes + arrows). **(5)** Data model + API/protocol design. **(6)** Bottleneck analysis + failure handling. **(7)** Trade-offs + rollout plan. **Always communicate trade-offs** — there's no single right answer.
- VI: **(1)** Clarify yêu cầu (functional + non-functional). **(2)** Xác định scope — gì trong/ngoài. **(3)** Ước lượng capacity (QPS, storage, bandwidth). **(4)** Kiến trúc tổng quan (box + arrow). **(5)** Data model + API/protocol. **(6)** Phân tích bottleneck + xử lý failure. **(7)** Trade-off + kế hoạch rollout. **Luôn nêu trade-off** — không có đáp án duy nhất đúng.

Follow-up (EN): How do you handle ambiguous requirements during a design interview?

---

### Q5. Capacity estimate mẫu?

**A:**
- EN: Back-of-envelope calculation: 50k req/s × 1KB payload = ~50MB/s. If storing 7 days of logs: 50MB/s × 86400 × 7 ≈ 30TB (before compression). Key numbers to memorize: 1 day ≈ 86400s ≈ 10⁵s, 1 year ≈ 3×10⁷s, 1GB/s ≈ 86TB/day.
- VI: Tính nhẩm: 50k req/s × 1KB payload = ~50MB/s. Lưu 7 ngày log: 50MB/s × 86400 × 7 ≈ 30TB (chưa nén). Số cần nhớ: 1 ngày ≈ 86400s ≈ 10⁵s, 1 năm ≈ 3×10⁷s, 1GB/s ≈ 86TB/ngày.

Follow-up (EN): What are Jeff Dean's latency numbers every programmer should know?

---

## 3) C++ Specific Design

### Q6. Plugin architecture trong C++ cần lưu ý gì?

**A:**
- EN: **(1)** ABI boundary — plugins compiled with different compilers may not be compatible. **(2)** Use C API at the boundary (C ABI is stable). **(3)** Symbol visibility (`__attribute__((visibility("default")))` or `__declspec(dllexport)`). **(4)** Version the plugin interface. **(5)** Handle plugin load/unload lifecycle (`dlopen`/`dlclose`).
- VI: **(1)** ABI boundary — plugin biên dịch khác compiler có thể không tương thích. **(2)** Dùng C API tại boundary (C ABI ổn định). **(3)** Symbol visibility. **(4)** Versioning plugin interface. **(5)** Quản lý lifecycle load/unload (`dlopen`/`dlclose`).

Follow-up (EN): Why is C ABI more stable than C++ ABI?

---

### Q7. Vì sao dùng C wrapper cho C++ library?

**A:**
- EN: C ABI is stable across compilers and versions — C++ is not (name mangling, vtable layout, exception handling differ). C wrappers enable: FFI bindings to other languages (Python, Rust, Go), plugin systems, and long-term ABI compatibility for shared libraries.
- VI: C ABI ổn định giữa các compiler và version — C++ thì không (name mangling, vtable layout, exception handling khác nhau). C wrapper cho phép: FFI binding sang ngôn ngữ khác (Python, Rust, Go), plugin system, và ABI compatibility lâu dài cho shared library.

```cpp
// C++ implementation
class Engine { public: void start(); void stop(); };

// C wrapper (stable ABI)
extern "C" {
    void* engine_create() { return new Engine(); }
    void engine_start(void* e) { static_cast<Engine*>(e)->start(); }
    void engine_destroy(void* e) { delete static_cast<Engine*>(e); }
}
```

Follow-up (EN): What is `extern "C"` and what does it do?

---

### Q8. Serialization format chọn sao?

**A:**
- EN: **Protobuf**: schema evolution, wide ecosystem, moderate speed. **FlatBuffers/Cap'n Proto**: zero-copy access, fastest deserialization, less flexible schema evolution. **JSON**: human-readable, slow, no schema. **Custom binary**: fastest but maintenance burden. Choose based on: schema evolution needs, latency requirements, ecosystem compatibility.
- VI: **Protobuf**: schema evolution, ecosystem rộng, tốc độ trung bình. **FlatBuffers/Cap'n Proto**: zero-copy access, deserialize nhanh nhất, schema evolution hạn chế hơn. **JSON**: đọc được, chậm, không schema. **Binary tùy chỉnh**: nhanh nhất nhưng tốn bảo trì. Chọn theo: nhu cầu schema evolution, yêu cầu latency, ecosystem.

Follow-up (EN): What is zero-copy deserialization?

---

### Q9. Batch vs streaming pipeline?

**A:**
- EN: **Batch**: process data in chunks on schedule — simpler to manage, higher latency. **Streaming**: process data as it arrives — lower latency, more complex (back-pressure, ordering, exactly-once). Many production systems are **hybrid**: streaming for real-time signals, batch for heavy analytics.
- VI: **Batch**: xử lý data theo lô định kỳ — đơn giản hơn, latency cao. **Streaming**: xử lý data khi đến — latency thấp, phức tạp hơn (back-pressure, ordering, exactly-once). Nhiều hệ thống production là **hybrid**: streaming cho tín hiệu real-time, batch cho analytics nặng.

Follow-up (EN): What is back-pressure in a streaming system?

---

## 4) Reliability

### Q10. Circuit breaker / retry / backoff trong C++ service?

**A:**
- EN: **(1)** Always set explicit timeouts — no unbounded waits. **(2)** Retry only idempotent operations. **(3)** Exponential backoff with jitter (prevents thundering herd). **(4)** Circuit breaker: after N failures, stop trying for a cooldown period, then probe with a single request.
- VI: **(1)** Luôn đặt timeout tường minh — không chờ vô thời hạn. **(2)** Chỉ retry thao tác idempotent. **(3)** Exponential backoff với jitter (tránh thundering herd). **(4)** Circuit breaker: sau N lần fail, ngừng thử trong khoảng cooldown, rồi thăm dò bằng 1 request.

Follow-up (EN): What is the thundering herd problem?

---

### Q11. Idempotency key dùng để làm gì?

**A:**
- EN: An idempotency key is a unique token sent with a request so the server can detect and deduplicate retries. If the same key is seen again, return the cached response instead of re-processing. Essential for: payment processing, order creation, any mutating operation that may be retried.
- VI: Idempotency key là token duy nhất gửi kèm request để server phát hiện và loại bỏ retry trùng. Nếu thấy key đã có, trả response đã cache thay vì xử lý lại. Thiết yếu cho: thanh toán, tạo đơn hàng, mọi thao tác mutate có thể bị retry.

Follow-up (EN): Where should idempotency keys be stored (in-memory, Redis, database)?

---

### Q12. Exactly-once delivery có thực sự tồn tại không?

**A:**
- EN: In distributed systems, true exactly-once is impossible (FLP impossibility). What we achieve is **effectively-once**: at-least-once delivery + idempotent processing + deduplication. The combination makes it appear exactly-once to the application.
- VI: Trong hệ thống phân tán, exactly-once thực sự là bất khả thi (FLP impossibility). Cái đạt được là **effectively-once**: at-least-once delivery + xử lý idempotent + dedup. Kết hợp lại trông giống exactly-once đối với ứng dụng.

Follow-up (EN): What is the FLP impossibility result?

---

## 5) Observability

### Q13. Ba trụ cột observability?

**A:**
- EN: **(1) Metrics**: numeric time-series (counters, gauges, histograms) — for alerting and dashboards. **(2) Logs**: structured events with context — for debugging. **(3) Traces**: distributed request flow across services — for latency analysis. All three are complementary — metrics tell you WHAT, logs tell you WHY, traces tell you WHERE.
- VI: **(1) Metrics**: chuỗi số theo thời gian (counter, gauge, histogram) — cho alerting và dashboard. **(2) Logs**: sự kiện có cấu trúc và context — cho debugging. **(3) Traces**: luồng request phân tán qua các service — cho phân tích latency. Ba cái bổ sung nhau — metrics cho biết CÁI GÌ, logs cho biết TẠI SAO, traces cho biết Ở ĐÂU.

Follow-up (EN): What is OpenTelemetry?

---

### Q14. Golden signals là gì?

**A:**
- EN: Four key metrics for any service (from Google SRE book): **(1) Latency** — time to process request. **(2) Traffic** — request rate (QPS). **(3) Errors** — error rate or ratio. **(4) Saturation** — how full the system is (CPU%, memory%, queue depth). If you can only monitor 4 things, monitor these.
- VI: Bốn metric chính cho mọi service (từ Google SRE book): **(1) Latency** — thời gian xử lý request. **(2) Traffic** — tốc độ request (QPS). **(3) Errors** — tỷ lệ lỗi. **(4) Saturation** — hệ thống đầy bao nhiêu (CPU%, memory%, queue depth). Nếu chỉ monitor được 4 thứ, monitor những cái này.

Follow-up (EN): What is the difference between SLI, SLO, and SLA?

---

### Q15. Senior nên thiết kế dashboard như thế nào?

**A:**
- EN: Design dashboards by **user journey**, not by component. Top level: SLO/SLI status. Drill down: service → endpoint → dependency. Include: error budget burn rate, p95/p99 latency trends, saturation warnings. Avoid: vanity metrics (total requests ever), too many panels without hierarchy.
- VI: Thiết kế dashboard theo **user journey**, không theo component. Tầng trên: SLO/SLI status. Drill down: service → endpoint → dependency. Bao gồm: error budget burn rate, xu hướng latency p95/p99, cảnh báo saturation. Tránh: vanity metric (tổng request từ trước tới giờ), quá nhiều panel không có hierarchy.

Follow-up (EN): What is error budget and how does it drive engineering decisions?

---

## 6) Interview Deep Dive

### Q16. Design rate limiter?

**A:**
- EN: **Token bucket** (smooth rate) or **sliding window** (exact counting). Distributed state: Redis + Lua script for atomic check-and-decrement. Handle: per-user vs global limits, fail-open vs fail-closed (deny on Redis failure?), rate limit headers (`X-RateLimit-Remaining`). C++ specific: embed in middleware layer, use `steady_clock` for timing.
- VI: **Token bucket** (rate mượt) hoặc **sliding window** (đếm chính xác). State phân tán: Redis + Lua script cho atomic check-and-decrement. Xử lý: limit per-user vs global, fail-open vs fail-closed (deny khi Redis fail?), rate limit header. C++ specific: embed trong middleware layer, dùng `steady_clock` cho timing.

Follow-up (EN): What is the leaky bucket algorithm?

---

### Q17. Design message queue đơn giản?

**A:**
- EN: Core: **partitioned log** (like Kafka). Producers append to partition, consumers track offset. Design decisions: ordering guarantee (per-partition), ack/retry semantics, dead-letter queue for poison messages, retention policy (time-based or size-based), replication for durability.
- VI: Core: **partitioned log** (như Kafka). Producer append vào partition, consumer track offset. Quyết định thiết kế: ordering guarantee (per-partition), ack/retry semantics, dead-letter queue cho poison message, retention policy (theo thời gian hoặc kích thước), replication cho durability.

Follow-up (EN): What is the difference between at-most-once, at-least-once, and exactly-once delivery?

---

### Q18. Design cache layer cho C++ service?

**A:**
- EN: **Cache-aside** (app checks cache, falls through to DB). TTL-based expiration. **Stampede protection**: only one thread fetches on miss, others wait. Warmup strategy for cold start. Fallback when cache is down (degrade gracefully). C++ implementation: `std::unordered_map` + `shared_mutex` for reader-writer lock, or concurrent hash map library.
- VI: **Cache-aside** (app kiểm tra cache, miss thì đọc DB). Hết hạn theo TTL. **Stampede protection**: chỉ 1 thread fetch khi miss, các thread khác chờ. Warmup cho cold start. Fallback khi cache down (giảm cấp nhẹ nhàng). C++ implementation: `std::unordered_map` + `shared_mutex` cho reader-writer lock.

Follow-up (EN): What is cache stampede and how do you prevent it?

---

## 7) Senior Signal

### Q19. Làm sao quyết định giữa optimize latency và dev velocity?

**A:**
- EN: Base decision on **SLO/SLI and business impact**: (1) If SLO is met with margin → prioritize dev velocity. (2) If SLO is at risk → optimize. (3) Always profile first — optimize the measured hotspot, not the imagined one. (4) Time-box optimization efforts. Never optimize "just in case."
- VI: Dựa trên **SLO/SLI và business impact**: (1) SLO đạt với margin → ưu tiên dev velocity. (2) SLO có rủi ro → optimize. (3) Luôn profile trước — tối ưu điểm nóng đo được, không phải tưởng tượng. (4) Time-box effort tối ưu. Không optimize "phòng hờ."

Follow-up (EN): What is the YAGNI principle applied to performance optimization?

---

### Q20. Khi nào nói "không" với yêu cầu quá rủi ro?

**A:**
- EN: When there's no: **(1)** rollback plan, **(2)** observability to detect problems, **(3)** load testing evidence, **(4)** migration path for breaking changes. Frame it constructively: "I support this goal, but we need X, Y, Z before it's safe to ship." Propose incremental approach with feature flags.
- VI: Khi không có: **(1)** kế hoạch rollback, **(2)** observability để phát hiện vấn đề, **(3)** bằng chứng load test, **(4)** migration path cho breaking change. Nói xây dựng: "Tôi ủng hộ mục tiêu này, nhưng cần X, Y, Z trước khi an toàn để ship." Đề xuất cách tiếp cận incremental với feature flag.

Follow-up (EN): How do feature flags help reduce deployment risk?

---

## Flash card (ôn nhanh)

| Câu hỏi / Question | Trả lời nhanh / Quick answer |
|---|---|
| C++ system design nhấn mạnh gì? | Latency, memory, failure modes, ABI, observability |
| 7 bước trả lời design? | Clarify → Scope → Capacity → Architecture → Data → Bottleneck → Trade-off |
| Plugin architecture lưu ý? | C ABI at boundary, symbol visibility, versioning |
| Serialization chọn sao? | Protobuf (evolution), FlatBuffers (speed), JSON (human) |
| Circuit breaker? | After N fails → cooldown → probe |
| Exactly-once? | Effectively-once: at-least-once + idempotent + dedup |
| 3 trụ observability? | Metrics, Logs, Traces |
| Golden signals? | Latency, Traffic, Errors, Saturation |
| Rate limiter? | Token bucket + Redis + Lua |
| Cache stampede? | One thread fetches, others wait |
