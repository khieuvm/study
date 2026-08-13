# 07 - Concurrency & Multi-threading — Bilingual VI/EN

---

## 1) Thread Cơ bản

### Q1. `std::thread` hoạt động như thế nào?

**A:**
- EN: `std::thread` wraps an OS thread (pthread on Linux, Win32 thread on Windows). You **must** call `join()` (wait for completion) or `detach()` (run independently) before the thread object is destroyed — otherwise `std::terminate` is called. C++20's `std::jthread` auto-joins on destruction.
- VI: `std::thread` wrap OS thread (pthread trên Linux, Win32 thread trên Windows). **Phải** gọi `join()` (cho xong) hoặc `detach()` (chạy độc lập) trước khi thread object bị destroy — nếu không `std::terminate` được gọi. C++20 `std::jthread` tự động join khi destroy.

```cpp
std::thread t(worker, 42);   // starts immediately
t.join();                     // wait for completion
// or: t.detach();            // run independently

// C++20: auto-join
{
    std::jthread t(worker, 42);
}  // auto-joins here — nó std::terminate risk

// Pass by reference: must use std::ref
int val = 0;
std::thread t(modify, std::ref(val));
```

Follow-up (EN): What happens if a `std::thread` object is destroyed without calling `join()` or `detach()`?

---

### Q2. `std::mutex` và các wrapper của no?

**A:**
- EN: `std::mutex` provides mutual exclusion. Never lock/unlock manually — use RAII wrappers: `lock_guard` (simple, scope-based), `unique_lock` (flexible, can unlock early, works with condition_variable), `scoped_lock` (C++17, locks multiple mutexes deadlock-free).
- VI: `std::mutex` cung cấp mutual exclusion. không báo gio lock/unlock thủ công — dùng RAII wrapper: `lock_guard` (đơn giản, theo scope), `unique_lock` (linh hoạt, unlock sớm, dùng với condition_variable), `scoped_lock` (C++17, lock nhiều mutex không deadlock).

```cpp
// lock_guard: simplest RAII
{ std::lock_guard<std::mutex> guard(mtx); /* critical section */ }

// unique_lock: flexible
{ std::unique_lock<std::mutex> lock(mtx);
  lock.unlock();   // can unlock early
  lock.lock();     // re-lock
}

// scoped_lock (C++17): multiple mutexes, deadlock-free
std::scoped_lock lock(m1, m2);
```

Follow-up (EN): What is the difference between `std::mutex`, `std::recursive_mutex`, and `std::timed_mutex`?

---

### Q3. `std::atomic` là gì? Khi nào dùng?

**A:**
- EN: `atomic<T>` ensures **indivisible read-modify-write** operations without needing a mutex. Use for simple counters, flags, and lock-free algorithms. Key operation: **CAS (Compare-And-Swap)** via `compare_exchange_strong/weak` — the foundation of all lock-free data structures.
- VI: `atomic<T>` đảm bảo **read-modify-write indivisible** mà không cần mutex. Dùng cho counter, flag đơn giản, và lock-free algorithm. Phep tinh chính: **CAS (Compare-And-Swap)** qua `compare_exchange_strong/weak` — nên tăng của mọi lock-free data structure.

```cpp
std::atomic<int> counter{0};
counter++;                          // atomic increment
counter.fetch_add(1);               // explicit atomic add
int val = counter.load();           // atomic read
counter.store(42);                  // atomic write

// CAS: foundation of lock-free algorithms
int expected = 5;
bool ok = counter.compare_exchange_strong(expected, 10);
// ok=true: was 5, now 10. ok=false: expected updated to actual value
```

Follow-up (EN): What is the difference between `compare_exchange_weak` and `compare_exchange_strong`?

---

### Q4. Memory order là gì? Các giá trị?

**A:**
- EN: Memory ordering controls **visibility guarantees** between threads. CPUs and compilers reorder operations for performance. From strongest (slowest) to weakest (fastest): `seq_cst` (default, total order) → `acq_rel` → `release`/`acquire` (publish-subscribe pattern) → `relaxed` (atomicity only, nó ordering).
- VI: Memory ordering kiểm soát **đảm bảo khả năng thay** giữa các thread. CPU và compiler reorder operations để tối ưu. Từ mạnh nhất (chậm nhất) đến yếu nhất (nhanh nhất): `seq_cst` (mặc định, total order) → `acq_rel` → `release`/`acquire` (publish-subscribe pattern) → `relaxed` (chi atomicity, không ordering).

```cpp
// Acquire-Release pattern (most common)
std::atomic<bool> ready{false};
std::string data;

// Producer:
data = "hello";                                // A
ready.store(true, std::memory_order_release);  // B: guarantees A happens-before B

// Consumer:
while (!ready.load(std::memory_order_acquire)) {}  // C: sees B
printf("%s\n", data.c_str());                       // D: guaranteed to see A

// Relaxed: only for independent counters
stats.fetch_add(1, std::memory_order_relaxed);
```

Follow-up (EN): When is `memory_order_seq_cst` necessary over acquire-release?

---

### Q5. `condition_variable` dùng để làm gì?

**A:**
- EN: `condition_variable` lets a thread **block** until notified by another thread that a condition is true. Always use with `unique_lock` and a **predicate** (to handle spurious wakeups). `wait()` atomically releases the mutex and blocks; on notification it re-acquires the mutex and checks the predicate.
- VI: `condition_variable` cho thread **block** cho đến khi thread khác thông báo điều kiện dùng. Luôn dùng với `unique_lock` và **predicate** (để xử lý spurious wakeup). `wait()` atomically release mutex và block; khi được notify no rẻ-acquire mutex và kiểm tra predicate.

```cpp
std::mutex mtx;
std::condition_variable cv;
std::queue<int> queue;
bool done = false;

// Consumer:
std::unique_lock<std::mutex> lock(mtx);
cv.wait(lock, [&]{ return !queue.empty() || done; });
// on wakeup: lock held, predicate is true

// Producer:
{
    std::lock_guard<std::mutex> lock(mtx);
    queue.push(42);
}
cv.notify_one();   // wake one consumer
cv.notify_all();   // wake all consumers
```

Follow-up (EN): What is a spurious wakeup and why do we need a predicate?

---

## 2) Van Để Concurrency

### Q6. Deadlock là gì? Làm sao tránh?

**A:**
- EN: **Deadlock**: two or more threads wait for each other's locks — nó progress possible. Prevention: (1) always lock in the same order, (2) use `std::scoped_lock` for multiple mutexes, (3) avoid nested locking, (4) use try-lock with timeout.
- VI: **Deadlock**: hai hay nhiều thread cho nhau giải phóng lock — không ai tien được. Phong tránh: (1) luôn lock theo cũng thứ tự, (2) dùng `std::scoped_lock` cho nhiều mutex, (3) tránh nested locking, (4) dùng try-lock với timeout.

```cpp
// Deadlock:
// Thread 1: lock(A) -> lock(B)
// Thread 2: lock(B) -> lock(A)  — each waits for the other

// Fix 1: consistent ordering
// Both: lock(A) -> lock(B)

// Fix 2: scoped_lock (C++17)
std::scoped_lock lk(A, B);  // deadlock-free algorithm

// Fix 3: try-lock
if (A.try_lock()) {
    if (B.try_lock()) { /* ... */ B.unlock(); }
    A.unlock();
}
```

Follow-up (EN): What are the four Coffman conditions for deadlock?

---

### Q7. Data race là gì? Phân biệt với race condition?

**A:**
- EN: **Data race** (UB in C++): two threads access the same variable concurrently, at least one writes, nó synchronization. **Race condition**: logic bug dependent on thread execution order — can occur even with proper synchronization. Data race → always a bug; race condition → design problem.
- VI: **Data race** (UB trong C++): 2 thread truy cập cũng biến đồng thời, ít nhất 1 ghi, không có sync. **Race condition**: lỗi logic phụ thuộc thứ tự thực thì — có thể xảy ra đủ đã sync dùng. Data race → luôn là bug; race condition → van để thiết kế.

```cpp
// Data race (UB):
int x = 0;
// Thread 1: x++;
// Thread 2: x++;
// Result: undefined — could be 1 or 2

// Race condition (logic bug, nó UB):
std::atomic<int> count{0};
if (count < 10) {       // Thread 1: sees 9
                         // Thread 2: also sees 9
    count++;             // Both increment: count = 11 — exceeds limit!
}
// Fix: use CAS or mutex around check-and-increment
```

Follow-up (EN): How does ThreadSanitizer (TSan) detect data races?

---

### Q8. `std::future` và `std::promise` là gì?

**A:**
- EN: A **promise-future** pair is a one-shot channel for passing a result between threads. The producer sets the value via `promise::set_value()`; the consumer retrieves it via `future::get()` (blocks until ready). `std::async` is the simplest way to get a future.
- VI: Cấp **promise-future** là kênh một chiều để truyền kết quả giữa thread. Producer set giá trị qua `promise::set_value()`; consumer lấy qua `future::get()` (block cho đến khi có). `std::async` là cách đơn giản nhất để lấy future.

```cpp
// std::async: simplest
auto fut = std::async(std::launch::async, []{ return 42; });
int result = fut.get();  // blocks until ready

// promise/future: manual control
std::promise<int> prom;
std::future<int> fut = prom.get_future();
std::thread t([&prom]{ prom.set_value(42); });
int result = fut.get();
t.join();

// packaged_task: wraps callable into future
std::packaged_task<int(int,int)> task([](int a, int b){ return a+b; });
auto fut = task.get_future();
std::thread t(std::move(task), 10, 20);
int result = fut.get();  // 30
t.join();
```

Follow-up (EN): What happens if you call `future::get()` twice?

---

## 3) Lock-Free Programming

### Q9. Lock-free là gì? Khi nào cần?

**A:**
- EN: **Lock-free**: guarantees system-wide progress even if any thread is suspended — nó deadlock possible. Built on atomic CAS operations. Use when: hard real-time requirements, mutex overhead too high, or avoiding priority inversion. Beware of the **ABA problem** (CAS succeeds falsely when value changes A→B→A).
- VI: **Lock-free**: đảm bảo tien trien toan hệ thống đủ bất kỳ thread nào bi dùng — không deadlock. Xảy trên atomic CAS. Dùng khi: yêu cầu hard real-time, mutex overhead qua cao, hoặc tránh priority inversion. Chu y **ABA problem** (CAS thành cổng sai khi giá trị đổi A→B→A).

```cpp
// Lock-free stack (Treiber stack)
template<typename T>
class LockFreeStack {
    struct Node { T data; Node* next; };
    std::atomic<Node*> head_{nullptr};
public:
    void push(T val) {
        Node* node = new Node{val, nullptr};
        node->next = head_.load();
        while (!head_.compare_exchange_weak(node->next, node)) {}
    }
    std::optional<T> pop() {
        Node* old = head_.load();
        while (old && !head_.compare_exchange_weak(old, old->next)) {}
        if (!old) return std::nullopt;
        T val = old->data;
        delete old;  // ABA problem! Need hazard pointers
        return val;
    }
};
```

Follow-up (EN): What are hazard pointers and epoch-based reclamation?

---

### Q10. Thread pool implement thế nào?

**A:**
- EN: A thread pool maintains a fixed number of worker threads and a task queue. Workers block on a condition variable until tasks are available. `submit()` enqueues a task and notifies one worker. Destructor sets a stop flag, notifies all, and joins all threads.
- VI: Thread pool duy tri số luồng worker thread cố định và 1 task queue. Worker block trên condition variable cho đến khi có task. `submit()` thêm task vào queue và notify 1 worker. Destructor set stop flag, notify tất cả, và join tất cả thread.

```cpp
class ThreadPool {
    std::vector<std::thread> workers_;
    std::queue<std::function<void()>> tasks_;
    std::mutex mtx_;
    std::condition_variable cv_;
    bool stop_ = false;
public:
    ThreadPool(size_t n) {
        for (size_t i = 0; i < n; ++i)
            workers_.emplace_back([this] {
                while (true) {
                    std::function<void()> task;
                    {
                        std::unique_lock lock(mtx_);
                        cv_.wait(lock, [this]{ return stop_ || !tasks_.empty(); });
                        if (stop_ && tasks_.empty()) return;
                        task = std::move(tasks_.front());
                        tasks_.pop();
                    }
                    task();
                }
            });
    }
    template<typename F>
    auto submit(F&& f) -> std::future<decltype(f())> {
        auto task = std::make_shared<std::packaged_task<decltype(f())()>>(
            std::forward<F>(f));
        auto fut = task->get_future();
        { std::lock_guard lock(mtx_); tasks_.emplace([task]{ (*task)(); }); }
        cv_.notify_one();
        return fut;
    }
    ~ThreadPool() {
        { std::lock_guard lock(mtx_); stop_ = true; }
        cv_.notify_all();
        for (auto& w : workers_) w.join();
    }
};
```

Follow-up (EN): How would you implement work-stealing for better load balancing?

---

## Flash card

| Question / Câu hỏi | Quick answer / Trả lỗi nhanh |
|---|---|
| `join` vs `detach`? | join: wait for thread; detach: run independently |
| `lock_guard` vs `unique_lock`? | unique_lock: flexible, cần unlock early, works with cv |
| Data race? | Two threads access same var, one writes, nó sync → UB |
| Prevent deadlock? | Lock ordering, scoped_lock, avoid nested locks |
| `memory_order_relaxed` when? | Only need atomicity, nó ordering (counters) |
| `condition_variable` requires? | `unique_lock` + predicate lambda |
| `std::async` returns? | `std::future<T>` |
| ABA problem? | CAS succeeds falsely when A→B→A; use tagged pointer |
| `compare_exchange_weak` vs strong? | weak: may spuriously fail, use in loop |
| `scoped_lock` (C++17)? | Lock multiple mutexes, deadlock-free, RAII |
