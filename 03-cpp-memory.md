# 03 - C++ Memory Management — Bilingual VI/EN

---

## 1) Stack vs Heap

### Q1. Stack và Heap khác nhau thế nào? Khi nào dùng cái nào?

**A:**
- EN: Stack is fast (O(1) allocation via pointer bump), automatically managed, limited in size (1-8 MB typical). Heap is slower (must find free block), manually managed, virtually unlimited. Use heap when: object outlives scope, size unknown at compile time, or polymorphism via pointer is needed.
- VI: Stack nhanh (O(1) cấp phát bảng dịch con trỏ), tự động quản lý, giới hạn kích thước (1-8 MB). Heap chậm hơn (phải tìm block trống), quản lý thủ công, gần như không giới hạn. Dùng heap khi: object sóng qua scope, kích thước chưa biết lúc compile, hoặc cần polymorphism qua pointer.

| Feature | Stack | Heap |
|---|---|---|
| Managed by | Compiler auto | Programmer / allocator |
| Speed | O(1) pointer bump | Slower (free-list search) |
| Size | Limited (1-8 MB) | Large (RAM limit) |
| Lifetime | Scope-bound | malloc/new to free/delete |
| Fragmentation | No | Yes |

```cpp
void foo() {
    int x = 10;             // stack
    int arr[100];           // stack (400 bytes)
    int* p = new int(10);   // p on stack, *p on heap
    delete p;
}
```

Follow-up (EN): What causes a stack overflow and how would you detect it?

---

### Q2. `new`/`delete` khác `malloc`/`free` thế nào?

**A:**
- EN: `new` allocates memory AND calls the constructor; `delete` calls the destructor then frees. `malloc`/`free` do neither — just raw memory. Never mix them (`new` with `free` or `malloc` with `delete` is UB). Always use `delete[]` for arrays allocated with `new[]`.
- VI: `new` cấp phát memory Và gọi constructor; `delete` gọi destructor rồi giải phóng. `malloc`/`free` không làm gì cả — chỉ memory thô. không được tron (`new` với `free` hoặc `malloc` với `delete` là UB). Luôn dùng `delete[]` cho array cấp phát bảng `new[]`.

| | `malloc`/`free` | `new`/`delete` |
|---|---|---|
| Origin | C standard library | C++ operator |
| Constructor/Destructor | Does NOT call | **Calls thêm** |
| Return type | `void*` (must cast) | Correct type |
| On failure | Returns `NULL` | Throws `std::bad_alloc` |
| Realloc | `realloc()` | No direct equivalent |

```cpp
Foo* p = (Foo*)malloc(sizeof(Foo));  // Foo NOT constructed
free(p);                              // ~Foo NOT called

Foo* p = new Foo();   // allocate + Foo::Foo()
delete p;             // ~Foo() + free
```

Follow-up (EN): What is `nothrow new` and when would you use it?

---

### Q3. Memory layout của một process trong Linux?

**A:**
- EN: A Linux process address space (top to bottom): Stack (grows down), Heap (grows up), BSS (uninitialized globals, zero-filled), Data (initialized globals), Text (code, read-only).
- VI: Không gian địa chỉ process Linux (từ cao xuống thấp): Stack (lớn xuống), Heap (lớn lên), BSS (global chưa khởi tạo, zero-filled), Data (global đã khởi tạo), Text (code, chỉ đọc).

```
High address
+------------------+
|      Stack       |  <- grows down, local vars, return addresses
+------------------+
|        v         |  (stack grows down)
|        ^         |  (heap grows up)
+------------------+
|       Heap       |  <- dynamic allocation (malloc, new)
+------------------+
|  BSS segment     |  <- uninitialized global/static (zero-init)
+------------------+
|  Data segment    |  <- initialized global/static
+------------------+
|  Text segment    |  <- code (read-only, executable)
+------------------+
Low address
```

```cpp
int g_uninit;           // BSS
int g_init = 42;        // Data segment
const char* msg = "hi"; // Text segment (string literal)

void foo() {
    int local = 1;      // Stack
    int* p = new int;   // p on Stack, *p on Heap
}
```

Follow-up (EN): Where does `mmap` memory go in this layout?

---

## 2) Smart Pointers

### Q4. `unique_ptr` là gì? Khi nào dùng?

**A:**
- EN: `unique_ptr` represents **exclusive ownership** — exactly one owner, resource is freed when the owner is destroyed. Zero overhead compared to raw pointer. Cannot be copied, only moved. This is the default smart pointer you should use.
- VI: `unique_ptr` thể hiện **exclusive ownership** — dùng 1 owner, resource được giải phóng khi owner bị destroy. không có overhead so với raw pointer. không thể copy, chi move được. Đầy là smart pointer mặc định nên dùng.

```cpp
auto p = std::make_unique<int>(42);     // preferred
auto p2 = std::move(p);                 // transfer ownership, p = nullptr

// Passing to functions:
void use(const int* p);                  // borrow, nó ownership transfer
void take(std::unique_ptr<int> p);       // transfer ownership
void maybe_take(std::unique_ptr<int>& p); // may or may not take
```

```cpp
// Custom deleter (e.g. for C resources)
auto file = std::unique_ptr<FILE, decltype(&fclose)>(
    fopen("data.txt", "r"), fclose
);
```

Follow-up (EN): What is the size of `unique_ptr` with a stateless vs stateful deleter?

---

### Q5. `shared_ptr` hoạt động như thế nào? Chi phí là báo nhiều?

**A:**
- EN: `shared_ptr` uses **atomic reference counting** — each copy increments the count, each destruction decrements it. When count reaches zero, the resource is freed. Cost: 2 pointers (16 bytes on 64-bit), atomic operations on copy/destroy (expensive on multi-core). Always prefer `make_shared` (single allocation for object + control block).
- VI: `shared_ptr` dùng **atomic reference counting** — mỗi lần copy tăng count, destroy giảm count. Count về 0 thì giải phóng. Chi phí: 2 pointers (16 byte trên 64-bit), atomic operations khi copy/destroy (đặt trên multi-core). Luôn dùng `make_shared` (1 allocation cho object + control block).

```cpp
auto p1 = std::make_shared<int>(42);  // count = 1
auto p2 = p1;                          // count = 2
p2.reset();                            // count = 1
// p1 destroyed -> count = 0 -> freed
```

```
Control block layout:
+------------------+
| ref count (atomic)|
| weak count        |
| deleter           |
| allocator         |
+------------------+
```

Follow-up (EN): Why is `make_shared` potentially problematic with `weak_ptr`? (Memory for object stays allocated until all `weak_ptr`s are gone too.)

---

### Q6. `weak_ptr` dùng để làm gì? Giải quyết van để gì?

**A:**
- EN: `weak_ptr` is a **non-owning observer** of a `shared_ptr` — it does not increment the reference count. Primary use: breaking **circular references** that would otherwise cause memory leaks. Must call `lock()` to get a `shared_ptr` before use; returns `nullptr` if the object was already destroyed.
- VI: `weak_ptr` là **non-owning observer** của `shared_ptr` — không tăng reference count. Mục đích chính: phá **vòng circular reference** để tránh leak. Phải gọi `lock()` để lấy `shared_ptr` trước khi dùng; trả về `nullptr` nếu object đã bị destroy.

```cpp
// Problem: circular reference
struct Node {
    std::shared_ptr<Node> next;
    std::shared_ptr<Node> prev;  // LEAK: mutual reference
};

// Fix: weak_ptr for back-pointer
struct Node {
    std::shared_ptr<Node> next;
    std::weak_ptr<Node>   prev;  // does not increment count
};

void use_prev(Node* n) {
    if (auto prev = n->prev.lock()) {
        // prev is valid shared_ptr
    }
}
```

- EN: Other uses: observer pattern, caches, parent pointers in trees.
- VI: Ứng dụng khác: observer pattern, cache, parent pointer trong tree.

Follow-up (EN): Can you construct a `weak_ptr` without a `shared_ptr`?

---

### Q7. Khi nào dùng `unique_ptr` vs `shared_ptr`?

**A:**
- EN: **Default to `unique_ptr`** — zero overhead, clear ownership. Upgrade to `shared_ptr` only when genuinely shared ownership is needed (multiple owners, unclear lifetime). Use `weak_ptr` as non-owning reference to break cycles.
- VI: **Mặc định dùng `unique_ptr`** — không overhead, ownership rõ ràng. Chi upgrade lên `shared_ptr` khi thực sự cần shared ownership (nhiều owner, lifetime không rõ). Dùng `weak_ptr` làm non-owning reference để phá cycle.

```
unique_ptr  <- default, zero overhead, clear ownership
    |
    v (when shared ownership needed)
shared_ptr  <- multiple owners, atomic ref counting overhead
    |
    v (non-owning reference to shared_ptr)
weak_ptr    <- break cycles, caches, observers
```

Follow-up (EN): Can you convert `unique_ptr` to `shared_ptr`? And the reverse? (Yes for unique→shared, nó for shared→unique.)

---

### Q8. Dangling pointer và use-after-free là gì?

**A:**
- EN: **Dangling pointer**: a pointer to memory that has been freed. **Use-after-free**: dereferencing a dangling pointer — undefined behavior. Can cause crashes, data corruption, or security vulnerabilities (exploitable in many real-world CVEs).
- VI: **Dangling pointer**: pointer trỏ đến memory đã bị giải phóng. **Use-after-free**: truy cập qua dangling pointer — UB. Có thể crash, hong dữ liệu, hoặc lo hong báo mat (exploit trong nhiều CVE thực tế).

```cpp
int* p = new int(42);
delete p;
*p = 100;           // USE-AFTER-FREE: UB!

// Fix: null after delete
delete p;
p = nullptr;

// Better: use smart pointers — impossible to use-after-free
auto p = std::make_unique<int>(42);
```

- EN: **Double free**: calling `delete` twice on the same pointer — also UB, can corrupt heap metadata.
- VI: **Double free**: gọi `delete` 2 lần trên cùng 1 pointer — cũng là UB, có thể corrupt heap.

Follow-up (EN): How would you detect use-after-free in production code? (AddressSanitizer, custom allocator with guard patterns.)

---

## 3) Memory Errors và Tools

### Q9. Các loại memory error phổ biến nhất?

**A:**
- EN: Common memory errors: buffer overflow, use-after-free, double free, memory leak, uninitialized read, stack overflow, heap corruption. Use sanitizers (ASan, MSan, TSan) during development and Valgrind for non-recompilable binaries.
- VI: Các lỗi memory phổ biến: buffer overflow, use-after-free, double free, memory leak, đọc biến chưa khởi tạo, stack overflow, heap corruption. Dùng sanitizers (ASan, MSan, TSan) lúc dev và Valgrind cho binary không recompile được.

| Error type | Example | Detection tool |
|---|---|---|
| Buffer overflow | `arr[10]` with `arr[5]` | ASan |
| Use-after-free | Use after `delete` | ASan |
| Double free | `delete` twice | ASan |
| Memory leak | Forgot `delete` | ASan leak detector, Valgrind |
| Uninitialized read | `int x; use(x);` | MSan, Valgrind |
| Stack overflow | Deep recursion | OS (SIGSEGV) |
| Heap corruption | Write to heap metadata | ASan |

```bash
# AddressSanitizer
g++ -fsanitize=address -fno-omit-frame-pointer -g -O1 -o prog prog.cpp

# MemorySanitizer
g++ -fsanitize=memory -g -O1 -o prog prog.cpp

# Valgrind (no recompile)
valgrind --leak-check=full ./prog
```

Follow-up (EN): Can ASan and TSan be used together? (No — they conflict. Use them in separate builds.)

---

### Q10. Placement new là gì?

**A:**
- EN: Placement `new` constructs an object at a **pre-allocated memory address** without allocating new memory. You must call the destructor explicitly (`p->~T()`) — do NOT use `delete`. Used in: custom allocators, memory pools, `std::optional`/`std::variant` internals, shared memory.
- VI: Placement `new` construct object tại **vùng nhỏ đã cấp phát sẵn** — không cấp phát thêm memory. Phải gọi destructor thủ công (`p->~T()`) — không dùng `delete`. Dùng trong: custom allocator, memory pool, `std::optional`/`std::variant` internals, shared memory.

```cpp
char buf[sizeof(Foo)];
Foo* p = new (buf) Foo(42);  // construct Foo in buf
// ...
p->~Foo();                   // must call dtor manually (NOT delete!)
```

```cpp
// Pool allocator example
struct Pool {
    alignas(alignof(std::max_align_t)) char buf[4096];
    size_t pos = 0;

    template<typename T, typename... Args>
    T* construct(Args&&... args) {
        void* ptr = buf + pos;
        pos += sizeof(T);
        return new (ptr) T(std::forward<Args>(args)...);
    }
};
```

Follow-up (EN): What alignment considerations are needed with placement new?

---

## 4) Allocators

### Q11. Custom allocator trong C++ dùng để làm gì?

**A:**
- EN: STL containers accept a custom allocator template parameter to control how memory is allocated/deallocated. Use cases: memory pools (avoid fragmentation, reduce overhead), stack allocators (ultra-fast), logging/debugging allocators, shared-memory allocators (IPC).
- VI: STL container nhận custom allocator template parameter để kiểm soát cách cấp phát/giải phóng memory. Ứng dụng: memory pool (tránh fragmentation, giảm overhead), stack allocator (cuc nhanh), logging/debug allocator, shared-memory allocator (IPC).

```cpp
template<typename T>
struct MyAllocator {
    using value_type = T;
    T* allocate(std::size_t n) {
        return static_cast<T*>(::operator new(n * sizeof(T)));
    }
    void deallocate(T* p, std::size_t) noexcept {
        ::operator delete(p);
    }
};

std::vector<int, MyAllocator<int>> v;
```

- EN: C++17 introduced `std::pmr::polymorphic_allocator` — type-erased allocators that can be switched at runtime.
- VI: C++17 giới thiệu `std::pmr::polymorphic_allocator` — type-erased allocator có thể đổi lúc runtime.

Follow-up (EN): What is the difference between `std::allocator` and `std::pmr::polymorphic_allocator`?

---

## Flash card

| Question / Câu hỏi | Quick answer / Trả lỗi nhanh |
|---|---|
| `new` vs `malloc`? | `new` calls ctor/dtor, throws; `malloc` doesn't |
| `delete` vs `delete[]`? | `delete[]` for arrays, mismatch = UB |
| `make_shared` advantage? | Single allocation instead of two |
| `weak_ptr` when? | Circular refs, observer, cache |
| Dangling pointer? | Pointer to freed memory |
| Placement new cleanup? | Manual destructor call: `p->~T()` |
| BSS vs Data segment? | BSS: uninitialized globals; Data: initialized globals |
| `unique_ptr` sharable? | No, must `std::move` to transfer |
| ASan detects? | Buffer overflow, use-after-free, double-free, leak |
| Stack overflow causes? | Deep recursion, oversized local arrays |
