# 07 - Debugging, Profiling, Performance

## 1) Performance process

### Q1. Nguyen tac vang?
A: Do trước, tối ưu sau. không tối ưu theo cam giac.

### Q2. KPI thường dùng?
A: p50/p95/p99 latency, throughput, CPU%, RSS, alloc/sec, cache miss rate.

### Q3. Benchmark sai thường gap?
A: Không warmup, benchmark nhỏ qua, bi dead-code elimination, environment không ổn định.

## 2) Tooling

### Q4. Linux profiler thường dùng?
A: `perf`, `heaptrack`, `valgrind`, `flamegraph`.

### Q5. Sanitizer nào cho gì?
A:
- ASan: memory error
- UBSan: undefined behavior
- TSan: data race
- MSan: uninitialized read

### Q6. Có nên bắt sanitizer o production?
A: Thường không (chi phí cao), nhưng nên bắt trong CI/nightly/staging.

## 3) Memory

### Q7. Memory leak debug flow?
A:
1. Reproduce
2. Dùng ASan/leak sanitizer
3. Khoanh life-time object
4. Xác nhận ownership contract

### Q8. Fragmentation vs leak?
A: Leak là mat tham chiếu không gìải phóng. Fragmentation là heap còn free nhưng tan man kho dùng.

## 4) CPU-level awareness

### Q9. Cache locality vì sao quan trọng?
A: Truy cập lien tiếp bộ nhớ giảm cache miss, tăng throughput đang kế.

### Q10. Branch misprediction là gì?
A: CPU doan sai nhanh điều kiện, phải flush pipeline.

### Q11. SIMD có nên ap dùng mặc định?
A: Không. Dùng khi hotspot rõ và dữ liệu phù hợp vectorization.

## 5) Build optimization

### Q12. `-O2` vs `-O3`?
A: `-O3` aggressive hon, không luôn nhanh hơn toan cuc, có thể tăng size code.

### Q13. LTO/PGO là gì?
A: 
- LTO: tối ưu luc link toan chương trình
- PGO: tối ưu dua trên profile runtime thực tế

## 6) Incident response

### Q14. Service latency tăng dot biến, xử lý sao?
A:
1. Kiểm tra recent deploy
2. Xem saturation CPU/memory/IO
3. So sánh p95 theo endpoint
4. Rollback nếu cần
5. Mo postmortem

### Q15. Postmortem tốt gom gì?
A: Timeline, root cause, impact, phát hiện giúp sớm hon, action item có owner + due date.
