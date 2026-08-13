# 07 - Concurrency & Multi-threading

---

## 1) Thread Co Ban

### Q1. `std::thread` hoat dong nhu the nao?

**A:** `std::thread` wrap OS thread (pthread tren Linux, Win32 thread tren Windows).

```cpp
#include <thread>
#include <mutex>

void worker(int id) {
    printf("Thread %d running\n", id);
}

// Tao thread
std::thread t(worker, 42);  // start ngay lap tuc

// Bat buoc phai join hoac detach truoc khi destructor chay
t.join();     // cho thread ket thuc
// hoac
t.detach();   // tach ra, chay doc lap (khong the join lai)

// Kiem tra
t.joinable(); // true neu chua join/detach
```

**`std::jthread` (C++20) — tu dong join:**
```cpp
{
    std::jthread t(worker, 42);
    // Khi ra khoi scope: destructor tu dong join
    // Khong bi std::terminate nhu std::thread
}
```

**Truyen tham so:**
```cpp
void modify(int& x) { x = 99; }

int val = 0;
std::thread t(modify, std::ref(val));  // phai dung std::ref cho reference
t.join();
printf("%d\n", val);  // 99
```

---

### Q2. `std::mutex` va cac wrapper cua no?

**A:**

```cpp
std::mutex mtx;

// Cach 1: lock/unlock thu cong (BAD: co the quen unlock khi exception)
mtx.lock();
// ... critical section ...
mtx.unlock();

// Cach 2: lock_guard (RAII, unlock khi ra scope)
{
    std::lock_guard<std::mutex> guard(mtx);
    // ... critical section ...
}  // tu dong unlock

// Cach 3: unique_lock (flexible hon, co the unlock som, dung voi condition_variable)
{
    std::unique_lock<std::mutex> lock(mtx);
    // ... critical section ...
    lock.unlock();          // co the unlock som
    // ... code khong can lock ...
    lock.lock();            // co the lock lai
}

// Khoa nhieu mutex cung luc (tranh deadlock):
std::mutex m1, m2;
std::lock(m1, m2);  // lock ca hai, khong bao gio deadlock
std::lock_guard<std::mutex> lg1(m1, std::adopt_lock);
std::lock_guard<std::mutex> lg2(m2, std::adopt_lock);

// C++17: scoped_lock (don gian hon)
std::scoped_lock lock(m1, m2);  // lock ca hai, RAII
```

---

### Q3. `std::atomic` la gi? Khi nao dung?

**A:** `atomic<T>` dam bao **read-modify-write** la indivisible — khong can mutex cho cac phep tinh don gian.

```cpp
#include <atomic>

std::atomic<int> counter{0};

// Thread-safe increment
counter++;                        // atomic fetch_add
counter.fetch_add(1);            // explicit
counter.fetch_add(1, std::memory_order_relaxed);  // voi ordering hint

// Load va store
int val = counter.load();
counter.store(42);

// Compare-and-swap (CAS) — nen tang cua lock-free algorithms
int expected = 5;
bool ok = counter.compare_exchange_strong(expected, 10);
// ok = true  -> doi 5 thanh 10 thanh cong
// ok = false -> expected duoc cap nhat bang gia tri hien tai

// compare_exchange_weak: co the fail gia (spurious), dung trong vong lap
int exp = 0;
while (!counter.compare_exchange_weak(exp, exp + 1)) {}  // atomic increment
```

**Cac phep tinh atomic:**
```cpp
// Cho int, long, pointer, ...
counter.fetch_add(n);
counter.fetch_sub(n);
counter.fetch_and(mask);
counter.fetch_or(mask);
counter.fetch_xor(mask);
counter.exchange(new_val);  // set va lay gia tri cu
```

---

### Q4. Memory order la gi? Cac gia tri?

**A:** Memory order xac dinh **bao dam thu tu** cac memory operation giua cac threads. CPU va compiler co the reorder operations de toi uu.

```
Strongest (cha nhat)
        |
memory_order_seq_cst    // Sequential consistency (mac dinh)
memory_order_acq_rel    // Acquire + Release (cho RMW ops)
memory_order_release    // Release: writes truoc no duoc thay
memory_order_acquire    // Acquire: reads sau no thay duoc writes truoc release
memory_order_consume    // Yeu hon acquire (it dung)
memory_order_relaxed    // Khong bao dam thu tu (chi atomicity)
        |
Weakest (nhanh nhat)
```

```cpp
// Pattern acquire-release pho bien:
std::atomic<bool> ready{false};
std::string data;

// Thread 1 (producer):
data = "hello";                               // A
ready.store(true, std::memory_order_release); // B: "A xay ra truoc B"

// Thread 2 (consumer):
while (!ready.load(std::memory_order_acquire)) {}  // C: cho den khi thay B
printf("%s\n", data.c_str());                      // D: thay duoc A

// memory_order_relaxed: chi dung cho counter, khong can ordering
stats.fetch_add(1, std::memory_order_relaxed);
```

---

### Q5. `condition_variable` dung de lam gi?

**A:** `condition_variable` cho phep thread **cho** (block) den khi mot dieu kien duoc thoa man boi thread khac.

```cpp
#include <condition_variable>

std::mutex mtx;
std::condition_variable cv;
std::queue<int> data_queue;
bool done = false;

// Consumer thread:
void consumer() {
    std::unique_lock<std::mutex> lock(mtx);
    cv.wait(lock, []{ return !data_queue.empty() || done; });
    // wait: unlock mutex, block cho den khi cv.notify_*() duoc goi
    //       sau khi duoc notify: lock lai mutex, kiem tra predicate
    //       neu predicate false: tiep tuc cho (tranh spurious wakeup)
    while (!data_queue.empty()) {
        int item = data_queue.front();
        data_queue.pop();
        printf("Got: %d\n", item);
    }
}

// Producer thread:
void producer() {
    for (int i = 0; i < 10; ++i) {
        {
            std::lock_guard<std::mutex> lock(mtx);
            data_queue.push(i);
        }
        cv.notify_one();   // wake up 1 consumer
    }
    {
        std::lock_guard<std::mutex> lock(mtx);
        done = true;
    }
    cv.notify_all();       // wake up tat ca consumers
}
```

---

## 2) Van De Concurrency

### Q6. Deadlock la gi? Lam sao tranh?

**A:** **Deadlock**: hai hay nhieu thread cho nhau giai phong lock — khong ai tien duoc.

```cpp
// Deadlock kinh dien:
// Thread 1:     Thread 2:
// lock(A)       lock(B)
// lock(B)  <->  lock(A)   <-- each cho cai kia
// unlock(B)     unlock(A)
// unlock(A)     unlock(B)

std::mutex A, B;
void thread1() { A.lock(); B.lock(); /* ... */ B.unlock(); A.unlock(); }
void thread2() { B.lock(); A.lock(); /* ... */ A.unlock(); B.unlock(); }
// Deadlock co the xay ra
```

**Cach tranh:**

1. **Lock ordering**: luon lock theo cung thu tu
```cpp
void thread1() { A.lock(); B.lock(); /* ... */ }
void thread2() { A.lock(); B.lock(); /* ... */ }  // cung thu tu A truoc B
```

2. **std::lock / scoped_lock**: lock nhieu mutex an toan
```cpp
std::scoped_lock lk(A, B);  // deadlock-free algorithm
```

3. **Lock hierarchy**: gan priority cho mutex, chi lock theo chieu giam
4. **Tranh nested locking** khi co the
5. **Try-lock voi timeout**:
```cpp
if (A.try_lock()) {
    if (B.try_lock()) { /* ... */ B.unlock(); }
    A.unlock();
}
```

---

### Q7. Data race la gi? Phan biet voi race condition?

**A:**

**Data race**: hai threads doc/ghi cung 1 bien cung luc, it nhat 1 thread ghi, khong co synchronization -> **UB trong C++**.
```cpp
int x = 0;
// Thread 1: x++;      \
// Thread 2: x++;       -> Data race: UB!
// Ket qua co the la 1 hoac 2
```

**Race condition**: loi logic phu thuoc vao thu tu thuc hien cua threads (co the xay ra du khong co data race).
```cpp
// Thread-safe counter nhung van co race condition:
std::atomic<int> count{0};
if (count < 10) {        // Thread 1 kiem tra: count = 9
    // Thread 2 cung kiem tra: count = 9
    count++;             // Thread 1: count = 10
    // Thread 2: count = 11 -> vuot gioi han!
}
// Giai phap: dung compare_exchange hoac mutex boc ca 2 buoc
```

---

### Q8. `std::future` va `std::promise` la gi?

**A:** Mechanism truyen ket qua giua threads — producer set gia tri qua `promise`, consumer lay qua `future`.

```cpp
#include <future>

// std::async: cach don gian nhat
auto fut = std::async(std::launch::async, []() {
    return 42;
});
// ... lam viec khac trong khi thread chay ...
int result = fut.get();  // doi ket qua (block neu chua co)

// promise/future: kiem soat thu cong
std::promise<int> prom;
std::future<int> fut = prom.get_future();

std::thread t([&prom]() {
    // ... tinh toan ...
    prom.set_value(42);   // gui ket qua
    // hoac: prom.set_exception(make_exception_ptr(...));
});
t.detach();

int result = fut.get();   // nhan ket qua (block)
```

**`std::packaged_task`:**
```cpp
std::packaged_task<int(int, int)> task([](int a, int b){ return a + b; });
std::future<int> fut = task.get_future();

std::thread t(std::move(task), 10, 20);
t.detach();

int result = fut.get();  // 30
```

---

## 3) Lock-Free Programming

### Q9. Lock-free la gi? Khi nao can?

**A:** Lock-free: dam bao tien trien cua he thong du mot thread bi delay vo han (khong co deadlock). Dung khi:
- Lat real-time requirement
- Mutex overhead qua cao (high-frequency operations)
- Tranh priority inversion

```cpp
// Lock-free stack don gian (Treiber stack):
template<typename T>
class LockFreeStack {
    struct Node { T data; Node* next; };
    std::atomic<Node*> head_{nullptr};

public:
    void push(T val) {
        Node* node = new Node{val, nullptr};
        node->next = head_.load();
        while (!head_.compare_exchange_weak(node->next, node)) {}
        // CAS: neu head_ van bang node->next, doi sang node
        // Neu khong (ai do push truoc): thu lai voi head_ moi
    }

    std::optional<T> pop() {
        Node* old_head = head_.load();
        while (old_head && !head_.compare_exchange_weak(old_head, old_head->next)) {}
        if (!old_head) return std::nullopt;
        T val = old_head->data;
        delete old_head;  // ABA problem! Can hazard pointer hoac epoch-based reclamation
        return val;
    }
};
```

**ABA problem**: CAS co the thanh cong sai khi gia tri doi tu A->B->A (thay A nhung la A khac). Giai phap: tagged pointer, hazard pointer.

---

### Q10. Thread pool implement the nao?

**A:**

```cpp
class ThreadPool {
    std::vector<std::thread> workers_;
    std::queue<std::function<void()>> tasks_;
    std::mutex queue_mtx_;
    std::condition_variable cv_;
    bool stop_ = false;

public:
    ThreadPool(size_t n) {
        for (size_t i = 0; i < n; ++i) {
            workers_.emplace_back([this] {
                while (true) {
                    std::function<void()> task;
                    {
                        std::unique_lock<std::mutex> lock(queue_mtx_);
                        cv_.wait(lock, [this]{ return stop_ || !tasks_.empty(); });
                        if (stop_ && tasks_.empty()) return;
                        task = std::move(tasks_.front());
                        tasks_.pop();
                    }
                    task();
                }
            });
        }
    }

    template<typename F>
    auto submit(F&& f) -> std::future<decltype(f())> {
        auto task = std::make_shared<std::packaged_task<decltype(f())()>>(std::forward<F>(f));
        std::future<decltype(f())> fut = task->get_future();
        {
            std::lock_guard<std::mutex> lock(queue_mtx_);
            tasks_.emplace([task]{ (*task)(); });
        }
        cv_.notify_one();
        return fut;
    }

    ~ThreadPool() {
        { std::lock_guard<std::mutex> lock(queue_mtx_); stop_ = true; }
        cv_.notify_all();
        for (auto& w : workers_) w.join();
    }
};

// Su dung:
ThreadPool pool(4);
auto fut = pool.submit([]{ return 42; });
printf("%d\n", fut.get());
```

---

## Flash card

| Cau hoi | Tra loi nhanh |
|---|---|
| `join` vs `detach`? | join: cho thread xong; detach: tach doc lap |
| `lock_guard` vs `unique_lock`? | unique_lock flexible hon (co the unlock som) |
| Data race la gi? | 2 thread doc/ghi cung luc, 1 ghi, khong sync -> UB |
| Deadlock tranh bang? | Lock ordering, scoped_lock, tranh nested lock |
| `memory_order_relaxed` dung khi? | Chi can atomicity, khong can ordering (counter) |
| `condition_variable` luon dung voi gi? | `unique_lock` va predicate lambda |
| `std::async` tra ve gi? | `std::future<T>` |
| ABA problem la gi? | CAS sai khi A->B->A, can tagged pointer |
| `compare_exchange_weak` vs strong? | weak: co spurious fail, dung trong loop |
| `scoped_lock` C++17? | Lock nhieu mutex, deadlock-free, RAII |
