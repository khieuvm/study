# 07 - Debugging, Profiling, Performance

## 1) Performance process

### Q1. Nguyen tac vang?
A: Do truoc, toi uu sau. Khong toi uu theo cam giac.

### Q2. KPI thuong dung?
A: p50/p95/p99 latency, throughput, CPU%, RSS, alloc/sec, cache miss rate.

### Q3. Benchmark sai thuong gap?
A: Khong warmup, benchmark nho qua, bi dead-code elimination, environment khong on dinh.

## 2) Tooling

### Q4. Linux profiler thuong dung?
A: `perf`, `heaptrack`, `valgrind`, `flamegraph`.

### Q5. Sanitizer nao cho gi?
A:
- ASan: memory error
- UBSan: undefined behavior
- TSan: data race
- MSan: uninitialized read

### Q6. Co nen bat sanitizer o production?
A: Thuong khong (chi phi cao), nhung nen bat trong CI/nightly/staging.

## 3) Memory

### Q7. Memory leak debug flow?
A:
1. Reproduce
2. Dung ASan/leak sanitizer
3. Khoanh life-time object
4. Xac nhan ownership contract

### Q8. Fragmentation vs leak?
A: Leak la mat tham chieu khong giai phong. Fragmentation la heap con free nhung tan man kho dung.

## 4) CPU-level awareness

### Q9. Cache locality vi sao quan trong?
A: Truy cap lien tiep bo nho giam cache miss, tang throughput dang ke.

### Q10. Branch misprediction la gi?
A: CPU doan sai nhanh dieu kien, phai flush pipeline.

### Q11. SIMD co nen ap dung mac dinh?
A: Khong. Dung khi hotspot ro va du lieu phu hop vectorization.

## 5) Build optimization

### Q12. `-O2` vs `-O3`?
A: `-O3` aggressive hon, khong luon nhanh hon toan cuc, co the tang size code.

### Q13. LTO/PGO la gi?
A: 
- LTO: toi uu luc link toan chuong trinh
- PGO: toi uu dua tren profile runtime thuc te

## 6) Incident response

### Q14. Service latency tang dot bien, xu ly sao?
A:
1. Kiem tra recent deploy
2. Xem saturation CPU/memory/IO
3. So sánh p95 theo endpoint
4. Rollback neu can
5. Mo postmortem

### Q15. Postmortem tot gom gi?
A: Timeline, root cause, impact, phat hien giup som hon, action item co owner + due date.
