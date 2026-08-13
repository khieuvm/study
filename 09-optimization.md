# 09 - Performance & Optimization

---

## 1) Cache va Memory Hierarchy

### Q1. Cache hierarchy hoat dong the nao? Tai sao quan trong?

**A:**
```
CPU Registers  ~0 cycles    ~KB
L1 Cache       ~4 cycles    32-64 KB (per core)
L2 Cache       ~12 cycles   256 KB - 1 MB (per core)
L3 Cache       ~40 cycles   4-32 MB (shared)
RAM            ~100 cycles  GB
NVMe SSD       ~10,000 cycles
HDD            ~1,000,000 cycles
```

**Cache line**: don vi nho nhat cache doc/ghi — thuong **64 bytes**. Khi ban truy cap 1 byte, CPU load 64 bytes vao cache.

```cpp
// BAD: truuy cap khong lien tuc (column-major tren row-major array)
// Cache miss nhieu vi jump 1000*4 = 4000 bytes moi phan tu
for (int j = 0; j < 1000; j++)
    for (int i = 0; i < 1000; i++)
        sum += matrix[i][j];  // access pattern: col by col

// GOOD: truy cap lien tuc (row-major)
// Cache-friendly: moi cache miss load 64 bytes, dung het
for (int i = 0; i < 1000; i++)
    for (int j = 0; j < 1000; j++)
        sum += matrix[i][j];  // access pattern: row by row
// ~5-10x nhanh hon tren matrix lon
```

---

### Q2. False sharing la gi? Lam sao tranh?

**A:** **False sharing**: 2 threads ghi vao 2 bien khac nhau nhung cung 1 cache line — moi ghi force invalidate cache line cua thread kia -> chay tham.

```cpp
// BAD: counters[0] va counters[1] co the cung 1 cache line (16 byte < 64 byte)
struct Counters {
    int counter1;  // offset 0
    int counter2;  // offset 4 — cung cache line voi counter1!
};

Counters c;
// Thread 1: c.counter1++; (invalidate cache line cho Thread 2)
// Thread 2: c.counter2++; (invalidate cache line cho Thread 1)
// Moi increment cua thread nay lam chap nhau cache cua thread kia

// FIX: padding de moi counter o cache line rieng
struct alignas(64) PaddedCounter {
    int value;
    char padding[60];  // fill du 64 bytes
};

PaddedCounter counters[2];  // moi counter o cache line rieng
// Thread 1: counters[0].value++; (khong anh huong Thread 2)
// Thread 2: counters[1].value++; (khong anh huong Thread 1)

// C++17: hardware_destructive_interference_size
struct alignas(std::hardware_destructive_interference_size) SafeCounter {
    std::atomic<int> value{0};
};
```

---

### Q3. Data-Oriented Design (DOD) la gi?

**A:** Thay vi to chuc data theo Objects (Array of Structures), to chuc theo cac mang rieng le (Structure of Arrays) de cache-friendly va SIMD-friendly.

```cpp
// AoS (Array of Structures) — OOP traditional:
struct Particle {
    float x, y, z;
    float vx, vy, vz;
    float mass;
    int   id;
};
std::vector<Particle> particles(N);  // xen ke x,y,z,vx,vy,vz,mass,id,...

// Cap nhat vi tri: chi can x,y,z,vx,vy,vz nhung load ca struct (cache waste)
for (auto& p : particles) {
    p.x += p.vx * dt;
    p.y += p.vy * dt;
    p.z += p.vz * dt;
}

// SoA (Structure of Arrays) — DOD:
struct Particles {
    std::vector<float> x, y, z;
    std::vector<float> vx, vy, vz;
    std::vector<float> mass;
    std::vector<int>   id;
};
Particles ps; ps.x.resize(N); /* ... */

// Cap nhat vi tri: chi load x[], vx[], etc. — cache-friendly, SIMD-friendly
for (int i = 0; i < N; i++) {
    ps.x[i] += ps.vx[i] * dt;  // lien tuc trong memory
    ps.y[i] += ps.vy[i] * dt;
    ps.z[i] += ps.vz[i] * dt;
}
// Compiler co the auto-vectorize (SIMD) vong lap nay
```

---

## 2) Compiler Optimizations

### Q4. Cac compiler optimization quan trong nhat?

**A:**

**Inlining** — thay the function call bang body:
```cpp
// inline goi y (compiler tu quyet)
inline int add(int a, int b) { return a + b; }

// Force inline (compiler-specific):
__attribute__((always_inline)) int add(int a, int b) { return a + b; }
__forceinline int add(int a, int b) { return a + b; }  // MSVC
```

**Loop unrolling** — giam loop overhead:
```cpp
// Compiler co the biet:
for (int i = 0; i < 4; i++) sum += arr[i];
// Thanh:
sum += arr[0]; sum += arr[1]; sum += arr[2]; sum += arr[3];
```

**NRVO (Named Return Value Optimization)**:
```cpp
std::vector<int> create() {
    std::vector<int> v = {1, 2, 3};
    return v;  // NRVO: construct truc tiep tai return location, khong move
}
```

**Alias analysis** — compiler gia dinh 2 pointer khac kieu khong alias:
```cpp
void add(float* a, float* b, float* c, int n) {
    for (int i = 0; i < n; i++)
        a[i] = b[i] + c[i];
    // Neu a alias voi b hay c, compiler khong the vectorize
}
// FIX: dung restrict (C99) hoac __restrict__ (C++)
void add(float* __restrict__ a, float* __restrict__ b, float* __restrict__ c, int n);
```

---

### Q5. SIMD (Single Instruction Multiple Data) la gi?

**A:** Thuc hien cung 1 phep tinh tren **nhieu data** dong thoi bang 1 instruction.

```
SSE2:  128-bit = 4 x float32 hoac 2 x float64
AVX2:  256-bit = 8 x float32
AVX-512: 512-bit = 16 x float32
```

```cpp
// Cach 1: de compiler auto-vectorize (uu tien)
// Chuyen phai: contiguous memory, no aliasing, no branches, simple loop
for (int i = 0; i < n; i++)
    c[i] = a[i] + b[i];
// Compile voi -O2 -march=native: compiler tu dung SIMD

// Cach 2: intrinsics (khi can control thu cong):
#include <immintrin.h>
void add_floats(float* c, const float* a, const float* b, int n) {
    int i = 0;
    for (; i <= n - 8; i += 8) {
        __m256 va = _mm256_loadu_ps(a + i);  // load 8 float
        __m256 vb = _mm256_loadu_ps(b + i);
        __m256 vc = _mm256_add_ps(va, vb);   // add 8 float cung luc
        _mm256_storeu_ps(c + i, vc);         // store 8 float
    }
    for (; i < n; i++) c[i] = a[i] + b[i];  // phan con lai
}
```

---

### Q6. Branch prediction va lam sao giup CPU?

**A:** CPU **du doan** nhanh se di theo duong nao trong if/else. Neu du doan sai, phai flush pipeline (~15-20 cycles).

```cpp
// BAD: neu data random, branch prediction 50% sai
for (int i = 0; i < N; i++) {
    if (arr[i] > 128) sum += arr[i];  // unpredictable
}

// GOOD: sort truoc -> branch predictable (lien tuc false, roi lien tuc true)
std::sort(arr, arr + N);
for (int i = 0; i < N; i++) {
    if (arr[i] > 128) sum += arr[i];
}
// ~6x nhanh hon tren data ngau nhien!

// Branchless (tranh branch hoan toan):
for (int i = 0; i < N; i++) {
    sum += arr[i] * (arr[i] > 128);  // no branch, chi multiply
}

// C++20: [[likely]] / [[unlikely]] hint cho compiler
if (error) [[unlikely]] {
    handle_error();
}
```

---

## 3) Profiling

### Q7. Cac cong cu profiling pho bien?

**A:**

**`perf` (Linux) — CPU profiling:**
```bash
perf stat ./program          # thong ke: cache miss, branch miss, IPC
perf record ./program        # record profile
perf report                  # xem hot spots

# Output mau:
# 1,234,567 cache-misses (5.23% of all cache refs)  <-- danh dau
# 98,765 branch-misses   (0.12% of all branches)
```

**`valgrind --tool=callgrind` — call graph:**
```bash
valgrind --tool=callgrind ./program
callgrind_annotate callgrind.out.*  # xem function-level time
kcachegrind callgrind.out.*         # GUI visualizer
```

**`gprof` — sampling profiler:**
```bash
g++ -pg -o prog prog.cpp
./prog
gprof prog gmon.out > report.txt
```

**Micro-benchmarking voi Google Benchmark:**
```cpp
#include <benchmark/benchmark.h>

static void BM_my_function(benchmark::State& state) {
    for (auto _ : state) {
        // Code can benchmark
        benchmark::DoNotOptimize(my_function(data));
    }
}
BENCHMARK(BM_my_function);
BENCHMARK_MAIN();

// Chay:
// ./bench --benchmark_filter=BM_my_function
// BM_my_function  1234 ns/op   810 MB/s
```

---

### Q8. Compiler flags quan trong cho performance?

**A:**
```bash
# Optimization levels
-O0    # Khong optimize (debug)
-O1    # Basic optimizations
-O2    # Standard (production)
-O3    # Aggressive (coi chung correctness)
-Os    # Optimize for size
-Oz    # Aggressive size

# Architecture-specific
-march=native        # Dung tat ca instructions cua CPU hien tai
-march=x86-64-v3     # Portable nhung voi AVX2
-mtune=native        # Tune nhung khong require

# Link-time optimization
-flto                # Link-Time Optimization (whole-program optimize)

# Profile-guided optimization (PGO):
# Buoc 1: build voi instrumentation
g++ -O2 -fprofile-generate -o prog src.cpp
# Buoc 2: chay voi representative input
./prog < typical_input.txt
# Buoc 3: build lai voi profile data
g++ -O2 -fprofile-use -o prog src.cpp
# Result: compiler biet hot path, optimize tuong ung
```

---

## 4) Optimization Patterns

### Q9. String optimization trong C++?

**A:**

```cpp
// 1. SSO (Small String Optimization): string ngan (<= ~15 char) luu tren stack
std::string s = "hello";  // luu tren stack, khong heap alloc

// 2. Tranh copy voi string_view (C++17)
void old_func(const std::string& s);  // neu truyen "literal" -> tao temp string
void new_func(std::string_view sv);   // khong copy

// 3. Reserve truoc khi build string
std::string result;
result.reserve(expected_size);       // 1 allocation, tranh realloc
for (auto& part : parts) result += part;

// 4. std::string::append vs +=
s.append(other.begin(), other.end()); // tuong duong += nhung explicit

// 5. Tranh temporary string trong concatenation
// BAD: moi + tao temporary
std::string s = "Hello" + std::string(", ") + "World";

// GOOD: dung += hoac format
std::string s;
s.reserve(20);
s += "Hello";
s += ", ";
s += "World";
```

---

### Q10. Move semantics giup performance nhu the nao?

**A:**

```cpp
// Vi du: return vector lon
std::vector<int> create_data(int n) {
    std::vector<int> result(n);
    std::iota(result.begin(), result.end(), 0);
    return result;  // NRVO: khong copy, khong move (construct tai cho)
}

// Neu NRVO khong ap dung duoc -> move (O(1)) thay vi copy (O(n))
std::vector<int> a = {1,2,3,...millions...};
std::vector<int> b = std::move(a);  // O(1): chi swap 3 pointers

// Insert vao container:
std::vector<std::string> v;
std::string s = "long string...";
v.push_back(s);             // copy: heap alloc + copy
v.push_back(std::move(s));  // move: O(1)
v.emplace_back("literal");  // construct in-place: tot nhat

// Container operations:
std::sort(v.begin(), v.end()); // dung move khi swap -> nhanh hon copy
```

---

## Flash card

| Cau hoi | Tra loi nhanh |
|---|---|
| Cache line size? | Thuong 64 bytes |
| False sharing la gi? | 2 threads ghi cung cache line, invisible sync |
| AoS vs SoA? | SoA cache-friendly, SIMD-friendly |
| NRVO la gi? | Compiler construct return value truc tiep, khong copy |
| `-march=native` lam gi? | Enable tat ca CPU instructions hien co |
| Branch prediction miss chi phi? | ~15-20 cycles pipeline flush |
| `[[likely]]`/`[[unlikely]]` dung khi? | Hint compiler ve branch probability |
| PGO la gi? | Profile-Guided Optimization, optimize theo actual usage |
| `__restrict__` dung de lam gi? | Bao compiler 2 pointer khong alias |
| SSO la gi? | Small String Optimization: string ngan tren stack |
