# 07 - Debugging, Profiling, Performance — Bilingual VI/EN

Kiến thức debug, profiling, và performance cho phỏng vấn Senior C++.

---

## 1) Performance Process

### Q1. Nguyên tắc vàng của optimization?

**A:**
- EN: **Measure first, optimize second.** Never optimize based on intuition. Profile to find the actual hotspot — it's rarely where you think. Amdahl's Law: optimizing a part that's 10% of runtime can yield at most 10% improvement, no matter how fast you make it.
- VI: **Đo trước, tối ưu sau.** Không bao giờ tối ưu theo cảm giác. Profile để tìm điểm nóng thực tế — hiếm khi ở chỗ bạn nghĩ. Luật Amdahl: tối ưu phần chiếm 10% runtime chỉ cải thiện tối đa 10%, dù bạn làm nhanh thế nào.

Follow-up (EN): What is Amdahl's Law and how does it limit optimization?

---

### Q2. KPI hiệu năng thường dùng?

**A:**
- EN: **Latency**: p50 (median), p95, p99, p99.9 — tail latency matters most. **Throughput**: requests/s, messages/s. **Resource**: CPU%, RSS (memory), alloc/sec, cache miss rate, context switches/sec. Always measure percentiles, not averages — averages hide tail latency.
- VI: **Latency**: p50 (median), p95, p99, p99.9 — tail latency quan trọng nhất. **Throughput**: requests/s, messages/s. **Resource**: CPU%, RSS (memory), alloc/sec, cache miss rate, context switches/sec. Luôn đo percentile, không phải trung bình — trung bình che giấu tail latency.

Follow-up (EN): Why is p99 latency more important than average latency?

---

### Q3. Benchmark sai thường gặp?

**A:**
- EN: **(1)** No warmup — first runs include JIT/cache priming. **(2)** Benchmark too small — fits entirely in cache, unrealistic. **(3)** Dead code elimination — compiler removes your benchmark code. **(4)** Unstable environment — other processes, frequency scaling. Fix: use Google Benchmark with `DoNotOptimize`, pin CPU frequency, isolate cores.
- VI: **(1)** Không warmup — lần chạy đầu bao gồm khởi tạo cache. **(2)** Benchmark quá nhỏ — vừa hết vào cache, không thực tế. **(3)** Dead code elimination — compiler loại bỏ code benchmark. **(4)** Môi trường không ổn định — process khác, frequency scaling. Fix: dùng Google Benchmark với `DoNotOptimize`, pin CPU frequency, cô lập core.

```cpp
static void BM_sort(benchmark::State& state) {
    std::vector<int> data(state.range(0));
    for (auto _ : state) {
        state.PauseTiming();
        std::iota(data.begin(), data.end(), 0);
        std::shuffle(data.begin(), data.end(), rng);
        state.ResumeTiming();
        std::sort(data.begin(), data.end());
        benchmark::DoNotOptimize(data.data());
    }
}
BENCHMARK(BM_sort)->Range(64, 1 << 20);
```

Follow-up (EN): What is `benchmark::DoNotOptimize` and why is it needed?

---

## 2) Tooling

### Q4. Linux profiler thường dùng?

**A:**
- EN: **`perf`**: CPU sampling profiler — shows hot functions, cache misses, branch mispredictions. **`perf record` + `flamegraph`**: visual call-stack profiling. **Valgrind/callgrind**: instruction-level profiling (slow but precise). **`heaptrack`**: heap allocation tracking. **`perf stat`**: hardware counter summary.
- VI: **`perf`**: CPU sampling profiler — hiển thị hàm nóng, cache miss, branch misprediction. **`perf record` + `flamegraph`**: profiling call-stack trực quan. **Valgrind/callgrind**: profiling mức instruction (chậm nhưng chính xác). **`heaptrack`**: theo dõi heap allocation. **`perf stat`**: tóm tắt hardware counter.

```bash
perf stat ./program                    # summary: IPC, cache misses, branches
perf record -g ./program && perf report # hot functions + call graph
valgrind --tool=callgrind ./program    # instruction-level
```

Follow-up (EN): How do you generate and read a flamegraph?

---

### Q5. Sanitizer nào phát hiện gì?

**A:**
- EN: **ASan** (AddressSanitizer): buffer overflow, use-after-free, double-free, memory leak. **UBSan** (UndefinedBehaviorSanitizer): signed overflow, null deref, alignment violations. **TSan** (ThreadSanitizer): data races. **MSan** (MemorySanitizer): uninitialized memory reads. Cannot combine ASan+TSan or ASan+MSan — use separate builds.
- VI: **ASan**: buffer overflow, use-after-free, double-free, memory leak. **UBSan**: signed overflow, null deref, alignment violation. **TSan**: data race. **MSan**: đọc memory chưa khởi tạo. Không thể kết hợp ASan+TSan hoặc ASan+MSan — dùng build riêng.

```bash
g++ -fsanitize=address,undefined -fno-omit-frame-pointer -g -o prog src.cpp
g++ -fsanitize=thread -g -o prog_tsan src.cpp   # separate build
```

Follow-up (EN): What is the runtime overhead of each sanitizer?

---

### Q6. Có nên chạy sanitizer trên production?

**A:**
- EN: Generally no — overhead is too high (ASan ~2x slowdown, TSan ~5-15x). Run in: CI (every commit), nightly stress tests, staging environment. Exception: some companies run ASan on a small percentage of production traffic (Google's approach) to catch rare bugs.
- VI: Thường không — overhead quá cao (ASan ~2x chậm, TSan ~5-15x). Chạy trong: CI (mỗi commit), nightly stress test, staging. Ngoại lệ: một số công ty chạy ASan trên phần nhỏ traffic production (cách của Google) để bắt bug hiếm.

Follow-up (EN): What is Google's approach to running sanitizers on production traffic?

---

## 3) Memory

### Q7. Memory leak debug flow?

**A:**
- EN: **(1)** Reproduce with minimal test case. **(2)** Run with ASan leak detector (`ASAN_OPTIONS=detect_leaks=1`). **(3)** Identify the allocation site from stack trace. **(4)** Trace ownership: who should have freed it? **(5)** Fix: usually a missing `delete`, forgotten `unique_ptr`, or exception path that skips cleanup.
- VI: **(1)** Tái hiện với test case tối thiểu. **(2)** Chạy với ASan leak detector (`ASAN_OPTIONS=detect_leaks=1`). **(3)** Xác định nơi cấp phát từ stack trace. **(4)** Truy vết ownership: ai lẽ ra phải giải phóng? **(5)** Fix: thường là thiếu `delete`, quên `unique_ptr`, hoặc exception path bỏ qua cleanup.

```bash
ASAN_OPTIONS=detect_leaks=1 ./program
# Output: Direct leak of 1024 byte(s) in 1 allocation(s)
# #0 malloc ... #1 create_buffer at src.cpp:42
```

Follow-up (EN): What is the difference between a leak and a logical leak?

---

### Q8. Fragmentation vs leak?

**A:**
- EN: **Leak**: memory allocated but reference lost — can never be freed. **Fragmentation**: memory freed but heap has scattered free blocks too small to satisfy new allocations — total free memory is sufficient but unusable. Fragmentation fix: memory pools, arena allocators, object size alignment.
- VI: **Leak**: memory được cấp phát nhưng mất reference — không bao giờ giải phóng được. **Fragmentation**: memory đã free nhưng heap có các block trống phân tán quá nhỏ để phục vụ cấp phát mới — tổng memory trống đủ nhưng không dùng được. Fix fragmentation: memory pool, arena allocator, căn lề kích thước object.

Follow-up (EN): How does a pool allocator prevent fragmentation?

---

## 4) CPU-level Awareness

### Q9. Cache locality vì sao quan trọng?

**A:**
- EN: CPUs access cache ~100x faster than RAM. Accessing contiguous memory (arrays, vectors) keeps data in cache lines (64 bytes). Linked structures (list, tree with heap nodes) cause cache misses on every pointer dereference. This is why `vector` beats `list` in practice even for O(n) operations.
- VI: CPU truy cập cache nhanh ~100x so với RAM. Truy cập bộ nhớ liên tục (array, vector) giữ data trong cache line (64 byte). Cấu trúc linked (list, tree với node trên heap) gây cache miss mỗi lần dereference pointer. Đây là lý do `vector` thắng `list` trong thực tế ngay cả với thao tác O(n).

Follow-up (EN): What is Data-Oriented Design (DOD)?

---

### Q10. Branch misprediction là gì?

**A:**
- EN: CPUs predict which branch (`if`/`else`) will be taken to keep the pipeline full. A misprediction flushes the pipeline — costs ~15-20 cycles. Sorted data makes branches predictable; random data causes ~50% misprediction. Branchless code (arithmetic instead of branches) avoids the issue entirely.
- VI: CPU dự đoán nhánh nào (`if`/`else`) sẽ được chọn để giữ pipeline đầy. Dự đoán sai flush pipeline — tốn ~15-20 cycle. Data đã sort làm nhánh dự đoán được; data ngẫu nhiên gây ~50% misprediction. Code branchless (dùng phép tính thay nhánh) tránh vấn đề hoàn toàn.

```cpp
// Branchless: avoids branch misprediction
for (int i = 0; i < n; i++)
    sum += arr[i] * (arr[i] > threshold);  // no branch
```

Follow-up (EN): How does `[[likely]]`/`[[unlikely]]` help?

---

### Q11. SIMD có nên áp dụng mặc định?

**A:**
- EN: **No.** First try compiler auto-vectorization (`-O2 -march=native`). Use intrinsics only when the auto-vectorizer fails on a measured hotspot. SIMD requires: contiguous aligned data, no branches in the loop, no data dependencies between iterations. Premature SIMD makes code unreadable and non-portable.
- VI: **Không.** Thử auto-vectorization của compiler trước (`-O2 -march=native`). Dùng intrinsics chỉ khi auto-vectorizer thất bại trên điểm nóng đã đo. SIMD yêu cầu: data liên tục và aligned, không có nhánh trong loop, không phụ thuộc data giữa các iteration. SIMD sớm làm code khó đọc và không portable.

Follow-up (EN): How do you check if a loop was auto-vectorized?

---

## 5) Build Optimization

### Q12. `-O2` vs `-O3`?

**A:**
- EN: `-O2`: standard production optimization — good balance of speed and code size. `-O3`: aggressive (loop unrolling, vectorization, function cloning) — not always faster globally because larger code = more cache misses. Some specific functions may benefit from `-O3` via `__attribute__((optimize("O3")))`.
- VI: `-O2`: tối ưu production chuẩn — cân bằng tốt giữa tốc độ và kích thước code. `-O3`: aggressive (loop unrolling, vectorization, function cloning) — không luôn nhanh hơn toàn cục vì code lớn hơn = nhiều cache miss hơn. Một số hàm cụ thể có thể hưởng lợi từ `-O3` qua attribute.

Follow-up (EN): What is `-Os` and when would you use it?

---

### Q13. LTO/PGO là gì?

**A:**
- EN: **LTO (Link-Time Optimization)**: optimizer sees the whole program at link time — can inline across translation units, eliminate dead code globally. **PGO (Profile-Guided Optimization)**: compile with instrumentation → run representative workload → recompile using the profile data. PGO typically gives 10-20% speedup.
- VI: **LTO**: optimizer thấy toàn bộ chương trình lúc link — có thể inline qua translation unit, loại bỏ dead code toàn cục. **PGO**: compile với instrumentation → chạy workload đại diện → recompile dùng profile data. PGO thường cải thiện 10-20% tốc độ.

```bash
# LTO
g++ -O2 -flto -o prog *.cpp

# PGO
g++ -O2 -fprofile-generate -o prog src.cpp   # step 1: instrument
./prog < typical_input.txt                     # step 2: profile
g++ -O2 -fprofile-use -o prog src.cpp         # step 3: optimized build
```

Follow-up (EN): What is the difference between fat LTO and thin LTO?

---

## 6) Incident Response

### Q14. Service latency tăng đột biến — xử lý sao?

**A:**
- EN: **(1)** Check recent deploys — rollback if suspicious. **(2)** Check saturation: CPU, memory, I/O, network. **(3)** Compare p95 latency by endpoint — isolate the problem. **(4)** Check dependencies: database, cache, external services. **(5)** Scale if resource-bound; rollback if code-bound. **(6)** Open postmortem after resolution.
- VI: **(1)** Kiểm tra deploy gần đây — rollback nếu nghi ngờ. **(2)** Kiểm tra saturation: CPU, memory, I/O, network. **(3)** So sánh p95 latency theo endpoint — cô lập vấn đề. **(4)** Kiểm tra dependency: database, cache, external service. **(5)** Scale nếu thiếu resource; rollback nếu lỗi code. **(6)** Mở postmortem sau khi xử lý.

Follow-up (EN): What is the difference between mitigation and root cause fix?

---

### Q15. Postmortem tốt gồm gì?

**A:**
- EN: **(1)** Timeline with timestamps. **(2)** Root cause (not blame). **(3)** Impact (duration, affected users, revenue). **(4)** Detection — how was it found, how could it be found faster? **(5)** Action items with owner + due date. **(6)** What went well (acknowledge good responses). Blameless culture is essential.
- VI: **(1)** Timeline với timestamp. **(2)** Root cause (không đổ lỗi). **(3)** Impact (thời lượng, user ảnh hưởng, doanh thu). **(4)** Detection — phát hiện thế nào, làm sao phát hiện sớm hơn? **(5)** Action item có owner + deadline. **(6)** Điều làm tốt (ghi nhận phản ứng tốt). Văn hóa blameless là thiết yếu.

Follow-up (EN): What is a "5 Whys" analysis?

---

## Flash card (ôn nhanh)

| Câu hỏi / Question | Trả lời nhanh / Quick answer |
|---|---|
| Nguyên tắc optimization? | Đo trước, tối ưu sau — profile, đừng đoán |
| KPI quan trọng nhất? | p99 latency, không phải average |
| Benchmark sai thường gặp? | Không warmup, dead code elimination, env không ổn |
| ASan phát hiện gì? | Buffer overflow, use-after-free, double-free, leak |
| TSan phát hiện gì? | Data races |
| Leak vs fragmentation? | Leak: mất reference; Fragmentation: free blocks phân tán |
| Cache locality? | Contiguous memory ~100x nhanh hơn random access |
| Branch misprediction? | ~15-20 cycles penalty, sort data hoặc branchless |
| `-O2` vs `-O3`? | `-O3` không luôn nhanh hơn — code lớn = cache miss |
| LTO? | Tối ưu toàn chương trình lúc link |
| PGO? | Tối ưu dựa trên profile runtime → ~10-20% speedup |
| Postmortem tốt? | Timeline + root cause + impact + action items + blameless |
