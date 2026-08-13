# 06 - System Design voi C++ (Senior Interview)

## 1) Design mindset

### Q1. Trong system design C++ can nhan manh gi?
A: Latency, throughput, memory footprint, failure mode, observability, deployability, ABI/runtime constraints.

### Q2. Cach phan ra module cho codebase lon?
A: Theo bounded context, API ro ownership, dependency 1 chieu, tan dung interface stable.

### Q3. Hexagonal/Clean architecture co phu hop C++?
A: Co, dac biet cho testing va tach domain khoi IO/framework.

## 2) Cach tra loi bai design

### Q4. Khung tra loi 7 buoc?
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
- neu luu 7 ngay log: 50MB/s * 86400 * 7 ~= 30TB (chua compress)

## 3) C++ specific design

### Q6. Plugin architecture trong C++ can de y gi?
A: ABI boundary, symbol visibility, versioning, C API bridge de on dinh giua compiler.

### Q7. Vi sao co the dung C wrapper cho C++ lib?
A: C ABI on dinh hon, de binding sang ngon ngu khac va tranh ABI fragility C++.

### Q8. Serialization format chon sao?
A: Proto/FlatBuffers/Cap'n Proto tuy can bang schema evolution, speed, zero-copy.

### Q9. Batch vs streaming pipeline?
A: Batch de quan ly don gian, streaming cho low-latency. Nhieu he thong hybrid.

## 4) Reliability

### Q10. Circuit breaker/retry/backoff trong service C++?
A: Phai co timeout ro rang, retry idempotent, exponential backoff + jitter.

### Q11. Idempotency key dung de lam gi?
A: Tranh xu ly trung request khi retry/network duplicate.

### Q12. Exactly-once co that khong?
A: Thuong la "effectively-once" nho idempotency + dedup + transaction boundary.

## 5) Observability

### Q13. 3 tru cot observability?
A: Metrics, logs, traces.

### Q14. Golden signals?
A: Latency, traffic, errors, saturation.

### Q15. Senior nen thiet ke dashboard nhu the nao?
A: Theo user journey/SLO, drill-down tu service -> endpoint -> dependency.

## 6) Interview deep dive prompts

### Q16. Design rate limiter?
A: Token bucket/leaky bucket, phan tan state (Redis), consistent hashing, fail-open/fail-closed.

### Q17. Design message queue nho?
A: Partition, ordering guarantee, ack/retry, dead-letter queue, retention.

### Q18. Design cache layer cho service C++?
A: TTL, invalidation policy, stampede protection, warmup, fallback khi cache down.

## 7) Senior signal

### Q19. Lam sao quyet dinh giua optimize latency va dev velocity?
A: Dua tren SLO/SLI va business impact, profile diem nong truoc, khong optimize vo tong.

### Q20. Khi nao no voi yeu cau "too risky"?
A: Khi chua co rollback, observability, test load, hoac pha ABI/protocol ma khong migration plan.
