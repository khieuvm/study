# 09 - Performance & Optimization — Bilingual VI/EN

---

## 1) Cache và Memory Hierarchy

### Q1. Cache hierarchy hoạt động thế nào? Tại sao quan trọng?

**A:**
- EN: Modern CPUs have a multi-level cache hierarchy: L1 (~4 cycles, 32-64KB per core), L2 (~12 cycles, 256KB-1MB), L3 (~40 cycles, 4-32MB shared), RAM (~100 cycles). The **cache line** (64 bytes) is the minimum transfer unit. Accessing data sequentially (row-major) is 5-10x faster than striding (column-major) on large arrays due to cache locality.
- VI: CPU hiện đại có cache nhiều cấp: L1 (~4 chu kỳ, 32-64KB mỗi core), L2 (~12 chu kỳ, 256KB-1MB), L3 (~40 chu kỳ, 4-32MB shared), RAM (~100 chu kỳ). **Cache line** (64 byte) là đơn vị truyen tối thìểu. Truy cập dữ liệu tương tự (row-major) nhanh gap 5-10 lan số với nhảy (column-major) trên mạng lớn nhỏ cache locality.

```cpp
// BAD: column-major access — cache miss every element
for (int j = 0; j < 1000; j++)
    for (int i = 0; i < 1000; i++)
        sum += matrix[i][j];

// GOOD: row-major access — cache-friendly
for (int i = 0; i < 1000; i++)
    for (int j = 0; j < 1000; j++)
        sum += matrix[i][j];
```

Follow-up (EN): How would you measure cache miss rate in your code?

---

### Q2. False sharing là gì? Làm sao tránh?

**A:**
- EN: **False sharing**: two threads write to different variables that happen to share the same cache line — each write invalidates the other core's cache line, causing severe performance degradation. Fix: pad or align data số each thread's data occupies its own cache line (64 bytes). C++17: `std::hardware_destructive_interference_size`.
- VI: **False sharing**: 2 thread ghi vào 2 biến khác nhau nhưng cũng cache line — mỗi lần ghi invalidate cache line của core kia, làm giảm hiệu suất nghiêm trọng. Fix: padding hoặc align data để data của mỗi thread o cache line riêng (64 byte). C++17: `std::hardware_destructive_interference_size`.

```cpp
// BAD: counter1 and counter2 share same cache line
struct Counters { int counter1; int counter2; };

// GOOD: each on its own cache line
struct alignas(64) PaddedCounter { std::atomic<int> value{0}; };
PaddedCounter counters[2];
```

Follow-up (EN): How would you detect false sharing using `perf`?

---

### Q3. Data-Oriented Design (DOD) là gì?

**A:**
- EN: DOD organizes data for **cache efficiency** rather than object hierarchy. Instead of Array-of-Structures (AoS, OOP-traditional), use Structure-of-Arrays (SoA) — each field in a contiguous array. SoA is cache-friendly and SIMD-friendly, enabling auto-vectorization.
- VI: DOD tổ chức dữ liệu theo **hiệu quả cache** thay vì phân cấp object. Thay vì Array-of-Structures (AoS, OOP truyền thống), dùng Structure-of-Arrays (SoA) — mọi field trong 1 mạng liên tục. SoA cache-friendly và SIMD-friendly, cho phép auto-vectorization.

```cpp
// AoS (traditional OOP) — cache waste when accessing only x,y,z
struct Particle { float x, y, z, vx, vy, vz, mass; int id; };
std::vector<Particle> particles(N);

// SoA (DOD) — contiguous access, SIMD-friendly
struct Particles {
    std::vector<float> x, y, z, vx, vy, vz;
    std::vector<float> mass;
    std::vector<int> id;
};

// Position update: touches only x,vx,y,vy,z,vz — all contiguous
for (int i = 0; i < N; i++) {
    ps.x[i] += ps.vx[i] * dt;  // compiler can auto-vectorize
}
```

Follow-up (EN): When is AoS actually better than SoA?

---

## 2) Compiler Optimizations

### Q4. Các compiler optimization quan trọng nhất?

**A:**
- EN: Key optimizations: **inlining** (replace call with body), **loop unrolling** (reduce loop overhead), **NRVO** (construct return value in-place), **alias analysis** (`__restrict__` tells compiler pointers don't alias, enabling vectorization), **dead code elimination**, **constant folding**.
- VI: Các tối ưu chính: **inlining** (thay call bảng body), **loop unrolling** (giảm overhead vòng lặp), **NRVO** (construct return value tại chỗ), **alias analysis** (`__restrict__` báo compiler pointer không alias, cho phép vectorization), **dead code elimination**, **constant folding**.

```cpp
// NRVO: no copy, nó move — constructed directly at return location
std::vector<int> create() {
    std::vector<int> v = {1, 2, 3};
    return v;
}

// __restrict__: enable vectorization by promising no aliasing
void add(float* __restrict__ a, const float* __restrict__ b,
         const float* __restrict__ c, int n) {
    for (int i = 0; i < n; i++) a[i] = b[i] + c[i];
}
```

Follow-up (EN): How can you verify the compiler actually vectorized a loop? (Use `-fopt-info-vec` or Compiler Explorer.)

---

### Q5. SIMD (Single Instruction Multiple Data) là gì?

**A:**
- EN: SIMD performs the **same operation on multiple data elements** simultaneously: SSE (128-bit = 4 floats), AVX2 (256-bit = 8 floats), AVX-512 (512-bit = 16 floats). Prefer letting the compiler auto-vectorize (`-O2 -march=native`); use intrinsics only when manual control is needed.
- VI: SIMD thực hiện **cũng phep tinh trên nhiều phần tử** đồng thời: SSE (128-bit = 4 float), AVX2 (256-bit = 8 float), AVX-512 (512-bit = 16 float). Ưu tiên để compiler auto-vectorize (`-O2 -march=native`); chỉ dùng intrinsics khi cần kiểm soat thủ công.

```cpp
// Prefer: auto-vectorization (compiler does it)
for (int i = 0; i < n; i++) c[i] = a[i] + b[i];
// Compile with -O2 -march=native

// Manual intrinsics (when needed):
#include <immintrin.h>
for (int i = 0; i <= n - 8; i += 8) {
    __m256 va = _mm256_loadu_ps(a + i);
    __m256 vb = _mm256_loadu_ps(b + i);
    _mm256_storeu_ps(c + i, _mm256_add_ps(va, vb));
}
```

Follow-up (EN): What data layout requirements does SIMD have (alignment, contiguity)?

---

### Q6. Branch prediction và làm sao giúp CPU?

**A:**
- EN: CPUs **predict** which branch will be taken to keep the pipeline full. Misprediction costs ~15-20 cycles (pipeline flush). Sorting data before conditional processing makes branches predictable (~6x speedup on random data). **Branchless** code avoids the problem entirely. C++20: `[[likely]]`/`[[unlikely]]` hints.
- VI: CPU **dự đoán** nhanh nào sẽ được chon để giữ pipeline đầy. Dự đoán sai ton ~15-20 chu kỳ (flush pipeline). Sắp xếp dữ liệu trước khi xử lý có điều kiện làm nhanh dự đoán được (~6x nhanh hơn trên data ngẫu nhiên). Code **branchless** tránh hoàn toàn van để. C++20: `[[likely]]`/`[[unlikely]]` hints.

```cpp
// Sorting makes branches predictable: ~6x faster on random data
std::sort(arr, arr + N);
for (int i = 0; i < N; i++)
    if (arr[i] > 128) sum += arr[i];

// Branchless alternative:
for (int i = 0; i < N; i++)
    sum += arr[i] * (arr[i] > 128);
```

Follow-up (EN): How would you use `perf stat` to measure branch misprediction rate?

---

## 3) Profiling

### Q7. Các công cụ profiling phổ biến?

**A:**
- EN: **perf** (Linux): CPU profiling, cache misses, branch mispredictions, IPC. **Valgrind/callgrind**: call graph analysis, function-level time. **Google Benchmark**: micro-benchmarking with `DoNotOptimize`. **gprof**: sampling profiler. Profile first, optimize second — never guess the bottleneck.
- VI: **perf** (Linux): CPU profiling, cache miss, branch misprediction, IPC. **Valgrind/callgrind**: phân tích call graph, thời gian muc function. **Google Benchmark**: micro-benchmarking với `DoNotOptimize`. **gprof**: sampling profiler. Profile trước, optimize sau — không báo gio doan bottleneck.

```bash
perf stat ./program          # summary: cache misses, branch misses, IPC
perf record ./program        # record samples
perf report                  # view hot functions

valgrind --tool=callgrind ./program
kcachegrind callgrind.out.*  # GUI visualizer
```

```cpp
// Google Benchmark
static void BM_func(benchmark::State& state) {
    for (auto _ : state) {
        benchmark::DoNotOptimize(my_function(data));
    }
}
BENCHMARK(BM_func);
```

Follow-up (EN): What is Amdahl's Law and how does it limit optimization gains?

---

### Q8. Compiler flags quan trọng cho performance?

**A:**
- EN: Key flags: `-O2` (standard production), `-O3` (aggressive), `-march=native` (use all CPU instructions), `-flto` (link-time optimization, whole-program), PGO (Profile-Guided Optimization: build with `-fprofile-generate`, run, rebuild with `-fprofile-use`).
- VI: Flag chính: `-O2` (production chuan), `-O3` (aggressive), `-march=native` (dùng tất cả instruction của CPU), `-flto` (tối ưu luc link, whole-program), PGO (Profile-Guided Optimization: build với `-fprofile-generate`, chạy, build lai với `-fprofile-use`).

```bash
# Standard production
g++ -O2 -march=native -flto -o prog src.cpp

# PGO: three-step process
g++ -O2 -fprofile-generate -o prog src.cpp   # step 1: instrument
./prog < typical_input.txt                     # step 2: profile
g++ -O2 -fprofile-use -o prog src.cpp         # step 3: optimize with data
```

Follow-up (EN): What is the risk of using `-O3` vs `-O2`?

---

## 4) Optimization Patterns

### Q9. String optimization trong C++?

**A:**
- EN: Key string optimizations: **SSO** (Small String Optimization — strings <=~15 chars stored on stack, nó heap), `string_view` (no-copy reference), `reserve()` (pre-allocate to avoid reallocation), avoid temporary strings in concatenation (use `+=` or `std::format`).
- VI: Các tối ưu string chính: **SSO** (Small String Optimization — string <=~15 ky từ lưu trên stack, không heap), `string_view` (tham chiếu không copy), `reserve()` (cấp phát trước tránh reallocation), tránh temporary string khi nơi chuoi (dùng `+=` hoặc `std::format`).

```cpp
std::string s = "hello";  // SSO: on stack, nó heap allocation

// Avoid temporaries in concatenation
std::string result;
result.reserve(expected_size);
result += "Hello";
result += ", ";
result += "World";

// string_view: no copy
void process(std::string_view sv);  // accepts string, char*, string_view
```

Follow-up (EN): How many bytes is the SSO threshold in common implementations (GCC, Clang, MSVC)?

---

### Q10. Move semantics giúp performance như thế nào?

**A:**
- EN: Move semantics enable **O(1) resource transfer** instead of O(n) copy — critical for containers of expensive objects. NRVO eliminates even the move. `emplace_back` constructs in-place (best). After move, source is valid-but-unspecified.
- VI: Move semantics cho phép **chuyển tài nguyên O(1)** thay vì copy O(n) — quan trọng cho container chưa object đặt. NRVO loại bỏ ca move. `emplace_back` construct tại chỗ (tốt nhất). Sau move, source là valid-but-unspecified.

```cpp
// Return: NRVO (best) or move (O(1))
std::vector<int> create_data(int n) {
    std::vector<int> result(n);
    return result;  // NRVO: no copy, nó move
}

// Insert: move vs copy
std::string s = "long string...";
v.push_back(s);             // COPY: O(n)
v.push_back(std::move(s));  // MOVE: O(1)
v.emplace_back("literal");  // IN-PLACE: best
```

Follow-up (EN): When does NRVO fail and a move happens instead?

---

## Flash card

| Question / Câu hỏi | Quick answer / Trả lỗi nhanh |
|---|---|
| Cache line size? | Typically 64 bytes |
| False sharing? | Two threads write to same cache line — invisible contention |
| AoS vs SoA? | SoA: cache-friendly, SIMD-friendly |
| NRVO? | Compiler constructs return value directly — nó copy/move |
| `-march=native`? | Enable all CPU instructions available |
| Branch misprediction cost? | ~15-20 cycles pipeline flush |
| `[[likely]]`/`[[unlikely]]`? | Hint compiler about branch probability |
| PGO? | Profile-Guided Optimization — optimize based on actual usage |
| `__restrict__`? | Promise compiler two pointers don't alias |
| SSO? | Small String Optimization — short strings on stack |
