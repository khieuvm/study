# 06 - System Design với C++ (Senior Interview)

## 1) Design mindset

### Q1. Trong system design C++ cần nhận mạnh gì?
A: Latency, throughput, memory footprint, failure mode, observability, deployability, ABI/runtime constraints.

### Q2. Cách phần ra module cho codebase lớn?
A: Theo bounded context, API rõ ownership, dependency 1 chiều, tan dùng interface stable.

### Q3. Hexagonal/Clean architecture có phù hợp C++?
A: Có, đặc biệt cho testing và tách domain khoi IO/framework.

## 2) Cách trả lỗi bài design

### Q4. Khung trả lỗi 7 bước?
A:
1. Clarify requirement
2. Functional/non-functional
3. Capacity estimate
4. High-level architecture
5. Data model + protocol
6. Bottleneck/failure handling
7. Trade-off + rollout plan

### Q5. Capacity estimate mau?
A: 
- 50k req/s
- payload 1KB => ~50MB/s
- nếu lưu 7 ngay log: 50MB/s * 86400 * 7 ~= 30TB (chưa compress)

## 3) C++ specific design

### Q6. Plugin architecture trong C++ cần để y gì?
A: ABI boundary, symbol visibility, versioning, C API bridge để ổn định giữa compiler.

### Q7. Vì sao có thể dùng C wrapper cho C++ lib?
A: C ABI ổn định hon, để binding sáng ngon ngu khác và tránh ABI fragility C++.

### Q8. Serialization format chon sao?
A: Proto/FlatBuffers/Cấp'n Proto tuy cần bảng schema evolution, speed, zero-copy.

### Q9. Batch vs streaming pipeline?
A: Batch để quản lý đơn gìản, streaming cho low-latency. Nhiều hệ thống hybrid.

## 4) Reliability

### Q10. Circuit breaker/retry/backoff trong service C++?
A: Phải có timeout rõ rang, retry idempotent, exponential backoff + jitter.

### Q11. Idempotency key dùng để làm gì?
A: Tránh xử lý trung request khi retry/network duplicate.

### Q12. Exactly-once có that không?
A: Thường là "effectively-once" nhỏ idempotency + dedup + transaction boundary.

## 5) Observability

### Q13. 3 tru cot observability?
A: Metrics, logs, traces.

### Q14. Golden signals?
A: Latency, traffic, errors, saturation.

### Q15. Senior nên thiết kế dashboard như thế nào?
A: Theo user journey/SLO, drill-down từ service -> endpoint -> dependency.

## 6) Interview deep dive prompts

### Q16. Design rate limiter?
A: Token bucket/leaky bucket, phần tan state (Redis), consistent hashing, fail-open/fail-closed.

### Q17. Design message queue nhỏ?
A: Partition, ordering guarantee, ack/retry, dead-letter queue, retention.

### Q18. Design cache layer cho service C++?
A: TTL, invalidation policy, stampede protection, warmup, fallback khi cache down.

## 7) Senior signal

### Q19. Làm sao quyết định giữa optimize latency và dev velocity?
A: Dua trên SLO/SLI và business impact, profile điểm nong trước, không optimize vo tong.

### Q20. Khi nào no với yêu cầu "too risky"?
A: Khi chưa có rollback, observability, test load, hoặc phá ABI/protocol mà không migration plan.
