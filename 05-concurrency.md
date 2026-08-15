# 05 - Concurrency & Memory Model (Senior) — Bilingual VI/EN

Kiến thức concurrency cho phỏng vấn Senior C++.

---

## 1) Threading Cơ bản

### Q1. Data race là gì?

**A:**
- EN: A data race occurs when two or more threads access the same memory location concurrently, at least one is a write, and there is no synchronization. Data races are **undefined behavior** in C++ — not just "wrong results" but potentially anything (crash, corruption, security vulnerability).
- VI: Data race xảy ra khi 2+ thread truy cập cùng vùng nhớ đồng thời, ít nhất 1 là ghi, và không có synchronization. Data race là **undefined behavior** trong C++ — không chỉ "kết quả sai" mà có thể bất kỳ điều gì (crash, corruption, lỗ hổng bảo mật).

```cpp
int counter = 0;
// Thread 1: counter++;  // read-modify-write
// Thread 2: counter++;  // same — data race → UB

// Fix:
std::atomic<int> counter{0};
counter.fetch_add(1);  // atomic: no data race
```

Follow-up (EN): How does ThreadSanitizer (TSan) detect data races?

---

### Q2. Race condition và data race có giống nhau không?

**A:**
- EN: **No.** A **data race** is a C++ memory model violation (UB). A **race condition** is a logic bug where behavior depends on thread scheduling order — can happen even with correct synchronization. Example: check-then-act on an atomic variable is race-condition-free from data races but still logically racy.
- VI: **Không.** **Data race** là vi phạm memory model C++ (UB). **Race condition** là lỗi logic khi hành vi phụ thuộc thứ tự scheduling — có thể xảy ra ngay cả khi đã sync đúng. Ví dụ: check-then-act trên atomic không có data race nhưng vẫn logically racy.

```cpp
std::atomic<int> count{0};
// Race condition (not data race):
if (count < 10) {       // Thread A checks: 9
                         // Thread B checks: 9
    count++;             // Both increment → count = 11, exceeds limit!
}
// Fix: use compare_exchange
int expected = count.load();
while (expected < 10 && !count.compare_exchange_weak(expected, expected + 1)) {}
```

Follow-up (EN): Can you have a race condition without a data race?

---

### Q3. `std::thread` và `std::jthread` khác nhau thế nào?

**A:**
- EN: `jthread` (C++20) auto-joins in destructor (no `std::terminate` risk) and supports cooperative cancellation via `stop_token`. `thread` requires explicit `join()` or `detach()` — forgetting either calls `std::terminate`.
- VI: `jthread` (C++20) tự động join trong destructor (không rủi ro `std::terminate`) và hỗ trợ cooperative cancellation qua `stop_token`. `thread` yêu cầu `join()` hoặc `detach()` tường minh — quên sẽ gây `std::terminate`.

```cpp
// std::thread — must join/detach
std::thread t(work);
t.join();  // forget this → terminate

// std::jthread (C++20) — auto-join + stop token
std::jthread jt([](std::stop_token st) {
    while (!st.stop_requested()) { do_work(); }
});
// jt auto-joins when destroyed; can request stop: jt.request_stop();
```

Follow-up (EN): How does `stop_token` enable cooperative cancellation?

---

## 2) Atomics

### Q4. `std::atomic<int>` đảm bảo gì?

**A:**
- EN: Guarantees **indivisible** read/write/read-modify-write on the variable. Does NOT guarantee atomicity of compound operations (e.g., check-then-act). Default memory order is `seq_cst` (sequential consistency — strongest, safest, slowest).
- VI: Đảm bảo read/write/read-modify-write **không thể chia** trên biến. KHÔNG đảm bảo atomicity cho thao tác phức hợp (VD: check-then-act). Memory order mặc định là `seq_cst` (sequential consistency — mạnh nhất, an toàn nhất, chậm nhất).

```cpp
std::atomic<int> x{0};
x.store(42);                    // atomic write
int v = x.load();               // atomic read
x.fetch_add(1);                 // atomic read-modify-write
bool ok = x.compare_exchange_strong(v, 100);  // CAS
```

Follow-up (EN): What is the ABA problem with CAS?

---

### Q5. Memory order có các mức nào?

**A:**
- EN: From weakest to strongest: `relaxed` (only atomicity), `consume` (rarely used), `acquire` (see writes before a release), `release` (publish writes), `acq_rel` (both), `seq_cst` (total global order, default). Using weaker orders is an optimization — only do it when profiling shows it matters.
- VI: Từ yếu đến mạnh: `relaxed` (chỉ atomicity), `consume` (hiếm dùng), `acquire` (thấy writes trước release), `release` (công bố writes), `acq_rel` (cả hai), `seq_cst` (total global order, mặc định). Dùng order yếu hơn là tối ưu — chỉ làm khi profile cho thấy cần thiết.

Follow-up (EN): When is `memory_order_relaxed` safe to use?

---

### Q6. Acquire/Release hiểu đơn giản?

**A:**
- EN: **Release** store says "all my writes before this store are now visible." **Acquire** load says "I can see all writes that happened before the release store I'm reading." Together they form a **happens-before** relationship — the fundamental building block of lock-free programming.
- VI: **Release** store nói "tất cả writes trước store này đã visible." **Acquire** load nói "tôi thấy tất cả writes trước release store mà tôi đang đọc." Cùng nhau tạo quan hệ **happens-before** — nền tảng của lock-free programming.

```cpp
std::atomic<bool> ready{false};
int data = 0;

// Thread 1 (producer):
data = 42;                                     // A
ready.store(true, std::memory_order_release);  // B: publishes A

// Thread 2 (consumer):
while (!ready.load(std::memory_order_acquire)) {} // C: syncs with B
assert(data == 42);  // D: guaranteed to see A
```

Follow-up (EN): What does `seq_cst` add beyond acquire-release?

---

### Q7. Khi nào dùng `relaxed`?

**A:**
- EN: When you only need atomicity of the variable itself, with no ordering requirements relative to other data. Typical use: independent counters, statistics, flags that don't guard other data.
- VI: Khi chỉ cần atomicity của biến đó, không cần ordering với dữ liệu khác. Dùng phổ biến: counter độc lập, statistics, flag không bảo vệ dữ liệu khác.

```cpp
std::atomic<uint64_t> request_count{0};
void handle_request() {
    request_count.fetch_add(1, std::memory_order_relaxed);  // just counting
}
```

Follow-up (EN): Can `relaxed` operations be reordered with other `relaxed` operations on the same variable?

---

## 3) Mutex và Deadlock

### Q8. Deadlock — 4 điều kiện Coffman?

**A:**
- EN: Deadlock requires ALL four: **(1)** Mutual exclusion — resources are non-sharable. **(2)** Hold-and-wait — thread holds one resource while waiting for another. **(3)** No preemption — resources can't be forcibly taken. **(4)** Circular wait — A waits for B, B waits for A. Break any one condition to prevent deadlock.
- VI: Deadlock cần CẢ bốn: **(1)** Mutual exclusion — tài nguyên không chia sẻ được. **(2)** Hold-and-wait — thread giữ 1 tài nguyên trong khi chờ cái khác. **(3)** No preemption — không thể cưỡng chế lấy tài nguyên. **(4)** Circular wait — A chờ B, B chờ A. Phá bất kỳ 1 điều kiện để ngăn deadlock.

Follow-up (EN): Which Coffman condition is easiest to break in practice?

---

### Q9. Cách tránh deadlock trong code C++?

**A:**
- EN: **(1)** Lock ordering — always acquire mutexes in the same global order. **(2)** `std::scoped_lock` — locks multiple mutexes atomically using deadlock avoidance algorithm. **(3)** Lock hierarchy — assign levels to mutexes, only lock lower levels. **(4)** Try-lock with timeout.
- VI: **(1)** Lock ordering — luôn acquire mutex theo cùng thứ tự. **(2)** `std::scoped_lock` — lock nhiều mutex cùng lúc bằng thuật toán tránh deadlock. **(3)** Lock hierarchy — gán level cho mutex, chỉ lock level thấp hơn. **(4)** Try-lock có timeout.

```cpp
std::mutex m1, m2;
// SAFE: scoped_lock handles ordering
std::scoped_lock lock(m1, m2);  // deadlock-free

// UNSAFE:
// Thread 1: lock(m1); lock(m2);
// Thread 2: lock(m2); lock(m1);  // deadlock!
```

Follow-up (EN): How does `std::scoped_lock` avoid deadlock internally?

---

### Q10. `condition_variable` có cần loop khi wait không?

**A:**
- EN: **Yes, always.** Spurious wakeups can occur — the thread wakes without being notified. Always use the predicate form: `cv.wait(lock, predicate)` which internally loops until the predicate is true.
- VI: **Có, luôn luôn.** Spurious wakeup có thể xảy ra — thread thức dậy mà không được notify. Luôn dùng dạng predicate: `cv.wait(lock, predicate)` — bên trong tự loop cho đến khi predicate đúng.

```cpp
std::mutex mtx;
std::condition_variable cv;
std::queue<int> queue;

// Consumer:
std::unique_lock lock(mtx);
cv.wait(lock, [&]{ return !queue.empty(); });  // loops on spurious wakeup
int item = queue.front(); queue.pop();
```

Follow-up (EN): What causes spurious wakeups?

---

## 4) Lock-free Cơ bản

### Q11. Lock-free có nghĩa là luôn nhanh hơn lock?

**A:**
- EN: **No.** Lock-free guarantees system-wide progress (no deadlock) but individual operations may be slower due to CAS retry loops. Lock-free shines under high contention where mutex would serialize threads. For low contention, a simple mutex is often faster and much simpler.
- VI: **Không.** Lock-free đảm bảo tiến triển toàn hệ thống (không deadlock) nhưng từng thao tác có thể chậm hơn do CAS retry loop. Lock-free tỏa sáng khi contention cao nơi mutex sẽ serialize thread. Contention thấp thì mutex đơn giản thường nhanh hơn và đơn giản hơn nhiều.

Follow-up (EN): What is the difference between lock-free and wait-free?

---

### Q12. ABA problem là gì?

**A:**
- EN: ABA: a value changes A→B→A. CAS sees A and assumes nothing changed, but the underlying data may be different (e.g., node was freed and a new node allocated at the same address). Solutions: tagged pointers (add version counter), hazard pointers, epoch-based reclamation.
- VI: ABA: giá trị đổi A→B→A. CAS thấy A và cho rằng không đổi, nhưng dữ liệu bên dưới có thể khác (VD: node bị free và node mới được cấp phát tại cùng địa chỉ). Giải pháp: tagged pointer (thêm version counter), hazard pointer, epoch-based reclamation.

```cpp
// ABA scenario:
// Thread 1: reads head = A, gets preempted
// Thread 2: pops A, pops B, pushes A back (different A!)
// Thread 1: CAS(head, A, next_of_old_A) succeeds — but A is different!
```

Follow-up (EN): How do hazard pointers solve ABA?

---

## 5) Practical Senior

### Q13. Cách debug bug concurrency hiếm gặp?

**A:**
- EN: **(1)** Enable ThreadSanitizer (TSan) in CI — catches data races. **(2)** Structured logging with timestamp + thread ID. **(3)** Stress tests with randomized scheduling. **(4)** Minimize shared mutable state — fewer races possible. **(5)** Reproduce with controlled thread interleaving (tools like rr, CHESS).
- VI: **(1)** Bật ThreadSanitizer (TSan) trong CI — bắt data race. **(2)** Logging có timestamp + thread ID. **(3)** Stress test với scheduling ngẫu nhiên. **(4)** Giảm thiểu shared mutable state — ít chỗ race hơn. **(5)** Tái hiện với thread interleaving có kiểm soát (rr, CHESS).

Follow-up (EN): What is the `rr` (record and replay) debugger?

---

### Q14. False sharing là gì?

**A:**
- EN: Two threads write to different variables that happen to share the same **cache line** (typically 64 bytes). Each write invalidates the other core's cache line — severe performance degradation despite no logical data sharing.
- VI: Hai thread ghi vào các biến khác nhau nhưng cùng nằm trên một **cache line** (thường 64 byte). Mỗi lần ghi invalidate cache line của core kia — giảm hiệu năng nghiêm trọng dù không chia sẻ dữ liệu logic.

```cpp
// BAD: counter1 and counter2 likely share a cache line
struct { std::atomic<int> counter1; std::atomic<int> counter2; } s;

// GOOD: separate cache lines
struct alignas(64) PaddedCounter { std::atomic<int> value; };
PaddedCounter counters[2];
```

Follow-up (EN): How would you detect false sharing with `perf`?

---

### Q15. Cách giảm false sharing?

**A:**
- EN: Align hot variables to cache line boundaries using `alignas(64)` or `std::hardware_destructive_interference_size` (C++17). Separate frequently-written data into different cache lines. Use thread-local accumulators + periodic merge.
- VI: Align biến nóng theo cache line bằng `alignas(64)` hoặc `std::hardware_destructive_interference_size` (C++17). Tách dữ liệu ghi thường xuyên vào cache line khác nhau. Dùng thread-local accumulator + merge định kỳ.

Follow-up (EN): What is `std::hardware_destructive_interference_size`?

---

### Q16. Thread pool tại sao hữu ích?

**A:**
- EN: Thread pool maintains a fixed number of pre-created threads + task queue. Benefits: **(1)** avoids thread creation/destruction overhead, **(2)** limits concurrency level (prevents oversubscription), **(3)** stable latency (no thread spawn jitter). Used in: servers, task schedulers, parallel algorithms.
- VI: Thread pool duy trì số thread cố định đã tạo sẵn + task queue. Lợi ích: **(1)** tránh overhead tạo/hủy thread, **(2)** giới hạn mức concurrency (tránh oversubscription), **(3)** latency ổn định (không jitter do spawn thread). Dùng trong: server, task scheduler, parallel algorithm.

Follow-up (EN): How would you implement work-stealing for better load balancing?

---

## 6) Mức Senior/Leadership

### Q17. Khi nào ưu tiên đơn giản hơn lock-free?

**A:**
- EN: **Almost always.** Start with mutex + `scoped_lock`. Only consider lock-free when profiling confirms lock contention is the bottleneck. Lock-free code is extremely hard to write correctly, test, and maintain. The cost of a bug in lock-free code is much higher than the cost of a slightly slower mutex.
- VI: **Gần như luôn luôn.** Bắt đầu với mutex + `scoped_lock`. Chỉ xem xét lock-free khi profile xác nhận lock contention là bottleneck. Code lock-free cực kỳ khó viết đúng, test, và bảo trì. Chi phí của bug trong lock-free cao hơn nhiều so với mutex chậm hơn chút.

Follow-up (EN): What are the testing strategies for lock-free data structures?

---

### Q18. Cách review code concurrent của team?

**A:**
- EN: Review checklist: **(1)** Every shared mutable variable protected by a named lock or is atomic. **(2)** Lock ordering documented and consistent. **(3)** No lock held during I/O or long operations. **(4)** Exception paths release all locks (use RAII). **(5)** No `thread::detach` without clear ownership. **(6)** TSan clean in CI.
- VI: Checklist review: **(1)** Mọi biến shared mutable được bảo vệ bởi lock có tên hoặc atomic. **(2)** Thứ tự lock được document và nhất quán. **(3)** Không giữ lock khi I/O hoặc thao tác lâu. **(4)** Exception path giải phóng tất cả lock (dùng RAII). **(5)** Không `thread::detach` khi chưa rõ ownership. **(6)** TSan sạch trong CI.

Follow-up (EN): What tools besides TSan help with concurrency code review?

---

## Flash card (ôn nhanh)

| Câu hỏi / Question | Trả lời nhanh / Quick answer |
|---|---|
| Data race vs race condition? | Data race = UB (memory model); Race condition = logic bug |
| jthread vs thread? | jthread auto-join + stop_token |
| atomic đảm bảo gì? | Indivisible operations, NOT compound atomicity |
| Memory order default? | `seq_cst` — safest, slowest |
| Acquire/Release? | Release publishes writes; Acquire sees them |
| Relaxed khi nào? | Independent counters, no ordering needed |
| 4 điều kiện deadlock? | Mutual exclusion, hold-wait, no preemption, circular |
| Tránh deadlock? | Lock ordering, `scoped_lock`, try-lock |
| cv cần loop? | Có — spurious wakeup |
| Lock-free luôn nhanh? | Không — chỉ khi high contention |
| ABA problem? | A→B→A fools CAS; use tagged pointer |
| False sharing? | Variables on same cache line → ping-pong |
