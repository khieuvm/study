# 02 - C++ Core (Senior Must-Know) — Bilingual VI/EN

Tổng hợp kiến thức C++ cốt lõi cho phỏng vấn Senior. Mỗi câu ngắn gọn nhưng đủ sâu.

---

## 1) OOP, Object Model

### Q1. Class và struct khác nhau gì trong C++?

**A:**
- EN: The only language difference is default access: `class` is `private`, `struct` is `public`. Convention: `struct` for POD/aggregate types, `class` for types with invariants and encapsulation.
- VI: Chỉ khác default access: `class` là `private`, `struct` là `public`. Convention: `struct` cho POD/aggregate, `class` cho type có invariant và encapsulation.

```cpp
struct Point { int x, y; };       // public by default — data-only
class BankAccount {                // private by default — has invariants
    double balance_ = 0;
public:
    void deposit(double amount);
};
```

Follow-up (EN): Can a struct have virtual functions, constructors, and destructors? (Yes — it's identical to class except default access.)

---

### Q2. Virtual function table (vtable) là gì?

**A:**
- EN: When a class has at least one virtual function, the compiler generates a **vtable** — an array of function pointers. Each object stores a hidden **vptr** pointing to its class's vtable. Virtual calls go: `obj->vptr -> vtable[slot] -> function`. Cost: +8 bytes per object, one indirection per call, prevents inlining.
- VI: Khi class có ít nhất 1 virtual function, compiler tạo **vtable** — mảng function pointer. Mỗi object chứa **vptr** ẩn trỏ tới vtable của class nó. Virtual call: `obj->vptr -> vtable[slot] -> function`. Chi phí: +8 byte mỗi object, 1 indirection mỗi lần gọi, không thể inline.

```cpp
class Base {
public:
    virtual void speak() { puts("Base"); }
    virtual ~Base() = default;
};
class Dog : public Base {
    void speak() override { puts("Woof"); }
};

Base* p = new Dog();
p->speak();  // vptr -> Dog::vtable -> Dog::speak()
delete p;    // virtual dtor ensures ~Dog() runs
```

Follow-up (EN): When can the compiler devirtualize a virtual call? (When the concrete type is known — e.g., local object, `final` class.)

---

### Q3. Khi nào destructor cần virtual?

**A:**
- EN: Whenever you delete a derived object through a base pointer. Without virtual dtor, only the base destructor runs — causing resource leaks and UB. Rule: if a class has **any** virtual function, give it a virtual destructor.
- VI: Khi nào delete derived object qua base pointer. Không có virtual dtor, chỉ base destructor chạy — gây leak và UB. Quy tắc: class có **bất kỳ** virtual function nào thì phải có virtual destructor.

```cpp
class Base {
public:
    virtual ~Base() = default;  // MUST be virtual
    virtual void process() = 0;
};
class Derived : public Base {
    std::vector<int> data_;
    void process() override { /* ... */ }
};

Base* p = new Derived();
delete p;  // safe: virtual ~Base() dispatches to ~Derived()
```

Follow-up (EN): Does a `final` class need a virtual destructor? (Yes, if it's held by base pointer.)

---

### Q4. Rule of 3/5/0 là gì?

**A:**
- EN: **Rule of 3** (C++03): if you write any of {destructor, copy ctor, copy assignment}, write all three. **Rule of 5** (C++11): add move ctor + move assignment. **Rule of 0**: best practice — use RAII members (`vector`, `unique_ptr`) so compiler-generated defaults are correct.
- VI: **Rule of 3** (C++03): nếu viết bất kỳ cái nào trong {destructor, copy ctor, copy=}, viết cả 3. **Rule of 5** (C++11): thêm move ctor + move=. **Rule of 0**: tốt nhất — dùng RAII members (`vector`, `unique_ptr`) để compiler tự sinh đúng.

```cpp
// Rule of 0 — preferred
class Document {
    std::string title_;
    std::vector<Page> pages_;
    // No special members needed — compiler generates all 5 correctly
};

// Rule of 5 — when managing raw resource
class Socket {
    int fd_;
public:
    explicit Socket(int fd) : fd_(fd) {}
    ~Socket() { if (fd_ >= 0) close(fd_); }
    Socket(const Socket&) = delete;             // non-copyable
    Socket& operator=(const Socket&) = delete;
    Socket(Socket&& o) noexcept : fd_(o.fd_) { o.fd_ = -1; }
    Socket& operator=(Socket&& o) noexcept {
        if (this != &o) { if (fd_ >= 0) close(fd_); fd_ = o.fd_; o.fd_ = -1; }
        return *this;
    }
};
```

Follow-up (EN): What happens if you define a copy constructor but not a move constructor? (Move operations are implicitly deleted — copies will be used instead.)

---

## 2) Value Category + Move Semantics

### Q5. lvalue, xvalue, prvalue là gì?

**A:**
- EN: Every expression has a **value category**: **lvalue** (has identity, can take address — variables, dereferenced pointers), **prvalue** (pure temporary — `42`, `std::string("hi")`), **xvalue** (expiring — result of `std::move()`, cast to `T&&`). xvalue + prvalue = rvalue. lvalue + xvalue = glvalue.
- VI: Mỗi biểu thức có **value category**: **lvalue** (có danh tính, lấy được địa chỉ — biến, con trỏ dereference), **prvalue** (temporary thuần — `42`, `std::string("hi")`), **xvalue** (sắp hết đời — kết quả `std::move()`, cast sang `T&&`). xvalue + prvalue = rvalue. lvalue + xvalue = glvalue.

```cpp
int x = 10;          // x is lvalue
int* p = &x;         // OK — lvalue has address

int&& r = 42;        // 42 is prvalue, bound to rvalue ref
std::string s = "hi";
std::string t = std::move(s);  // std::move(s) is xvalue
// s is now valid but unspecified
```

Follow-up (EN): Why does `std::move` on a `const` object not actually move? (const rvalue matches `const T&`, so copy ctor is called.)

---

### Q6. `std::move` có thực sự move không?

**A:**
- EN: **No.** `std::move` is just a cast to rvalue reference (`static_cast<T&&>`). The actual move happens when a move constructor or move assignment receives that rvalue. After move, the source is in a **valid but unspecified** state — safe to destroy or reassign.
- VI: **Không.** `std::move` chỉ là cast sang rvalue reference (`static_cast<T&&>`). Move thực sự xảy ra khi move constructor hoặc move assignment nhận rvalue đó. Sau move, source ở trạng thái **hợp lệ nhưng không xác định** — an toàn để destroy hoặc gán lại.

```cpp
std::vector<int> a = {1, 2, 3};
std::vector<int> b = std::move(a);  // move ctor: steals a's buffer
// a.size() is unspecified (likely 0), but a is still valid
a = {4, 5};  // OK: reassign
```

Follow-up (EN): What is the difference between `std::move` and `std::forward`?

---

### Q7. Khi nào không nên move?

**A:**
- EN: Don't move when: (1) you still need the object's value afterward, (2) the object is small and trivially copyable (copy is equally fast), (3) the object is `const` (move degrades to copy), (4) inside a return statement where NRVO applies (move/copy is elided).
- VI: Không nên move khi: (1) vẫn cần giá trị của object sau đó, (2) object nhỏ và trivially copyable (copy cũng nhanh), (3) object là `const` (move thành copy), (4) trong return statement khi NRVO áp dụng (move/copy được bỏ qua).

```cpp
std::string make() {
    std::string s = "hello";
    return s;          // NRVO — don't std::move(s), it prevents elision
}

int x = 42;
int y = std::move(x);  // pointless — int copies are just as fast
```

Follow-up (EN): What is guaranteed copy elision in C++17?

---

### Q8. `noexcept` liên quan gì đến move?

**A:**
- EN: `std::vector::push_back` uses move only if the move constructor is `noexcept`. Otherwise it falls back to copy to maintain the **strong exception guarantee** (if move throws mid-reallocation, the original data is corrupted). Always mark move ctor/assignment `noexcept`.
- VI: `std::vector::push_back` chỉ dùng move nếu move constructor là `noexcept`. Nếu không, nó fallback sang copy để đảm bảo **strong exception guarantee** (nếu move throw giữa reallocation, data gốc bị hỏng). Luôn đánh dấu move ctor/assignment là `noexcept`.

```cpp
class Widget {
public:
    Widget(Widget&& o) noexcept;             // vector will use this
    Widget& operator=(Widget&& o) noexcept;  // always noexcept
};
// Without noexcept: vector::push_back copies instead of moving!
```

Follow-up (EN): How does `std::move_if_noexcept` work?

---

## 3) Smart Pointer + Ownership

### Q9. `unique_ptr` vs `shared_ptr` — khi nào dùng cái nào?

**A:**
- EN: **Default to `unique_ptr`** — zero overhead, exclusive ownership. Use `shared_ptr` only when ownership is genuinely shared (multiple owners, unclear lifetime). `shared_ptr` costs: 2 pointers per handle (16 bytes), atomic ref count on copy/destroy, separate control block allocation (unless `make_shared`).
- VI: **Mặc định dùng `unique_ptr`** — không overhead, ownership độc quyền. Chỉ dùng `shared_ptr` khi ownership thực sự chia sẻ (nhiều owner, lifetime không rõ). Chi phí `shared_ptr`: 2 pointer mỗi handle (16 byte), atomic ref count khi copy/destroy, cấp phát control block riêng (trừ khi `make_shared`).

```cpp
// unique_ptr — default choice
auto widget = std::make_unique<Widget>();
process(*widget);  // borrow via reference

// shared_ptr — only when truly shared
auto config = std::make_shared<Config>();
thread1.set_config(config);  // shared ownership
thread2.set_config(config);
```

Follow-up (EN): Why is `make_shared` more efficient than `shared_ptr<T>(new T)`? (Single allocation for object + control block.)

---

### Q10. `weak_ptr` dùng để làm gì?

**A:**
- EN: `weak_ptr` is a non-owning observer of `shared_ptr`. It does not increment the ref count. Primary use: **break circular references** that would otherwise cause memory leaks. Must call `lock()` before use — returns `shared_ptr` if alive, `nullptr` if expired.
- VI: `weak_ptr` là non-owning observer của `shared_ptr`. Không tăng ref count. Mục đích chính: **phá vòng circular reference** gây leak. Phải gọi `lock()` trước khi dùng — trả về `shared_ptr` nếu còn sống, `nullptr` nếu đã hết.

```cpp
struct Node {
    std::shared_ptr<Node> next;
    std::weak_ptr<Node> prev;    // weak breaks the cycle
};

void use(std::weak_ptr<Node> wp) {
    if (auto sp = wp.lock()) {   // safe access
        sp->process();
    }
}
```

Follow-up (EN): What other use cases does `weak_ptr` have? (Caches, observer pattern.)

---

### Q11. Tại sao không nên truyền `shared_ptr` by value mọi nơi?

**A:**
- EN: Copying `shared_ptr` increments an **atomic** ref count — expensive on multi-core (cache line bouncing). It also obscures ownership intent. Guidelines: pass `T&` or `T*` if you just use the object; pass `const shared_ptr<T>&` if you might share; pass `shared_ptr<T>` by value only when transferring/sharing ownership.
- VI: Copy `shared_ptr` tăng **atomic** ref count — đắt trên multi-core (cache line bouncing). Nó cũng làm mờ ý định ownership. Hướng dẫn: truyền `T&` hoặc `T*` nếu chỉ dùng object; truyền `const shared_ptr<T>&` nếu có thể share; truyền `shared_ptr<T>` by value chỉ khi chuyển/chia sẻ ownership.

```cpp
// BAD: unnecessary atomic increment
void process(std::shared_ptr<Widget> w) { w->run(); }

// GOOD: just borrow
void process(const Widget& w) { w.run(); }

// OK: intentionally sharing ownership
void cache(std::shared_ptr<Widget> w) { cache_[id] = std::move(w); }
```

Follow-up (EN): What is the Herb Sutter guideline for smart pointer parameters?

---

### Q12. RAII là gì? Tại sao quan trọng?

**A:**
- EN: **Resource Acquisition Is Initialization** — tie resource lifetime to object lifetime. Constructor acquires, destructor releases. Makes code exception-safe and leak-free regardless of control flow. RAII is **the** most important C++ idiom.
- VI: **RAII** — gắn vòng đời resource với vòng đời object. Constructor cấp phát, destructor giải phóng. Code trở nên exception-safe và không leak bất kể control flow. RAII là idiom **quan trọng nhất** trong C++.

```cpp
void process() {
    std::lock_guard lock(mtx);        // RAII: auto unlock
    auto data = std::make_unique<Data>(); // RAII: auto delete
    std::ifstream file("in.txt");     // RAII: auto close
    
    if (error) return;  // all resources cleaned up automatically
}
```

Follow-up (EN): Name 5 standard RAII wrappers. (`unique_ptr`, `shared_ptr`, `lock_guard`, `fstream`, `jthread`.)

---

## 4) Exception Safety

### Q13. Ba mức exception guarantee là gì?

**A:**
- EN: **(1) Basic guarantee**: invariants preserved, no leaks, but state may change. **(2) Strong guarantee**: operation succeeds completely or has no effect (commit-or-rollback). **(3) No-throw guarantee**: operation never throws (`noexcept`). Destructors, move ops, and swap should be no-throw.
- VI: **(1) Basic guarantee**: invariant được giữ, không leak, nhưng state có thể thay đổi. **(2) Strong guarantee**: thao tác thành công hoàn toàn hoặc không có hiệu ứng (commit-or-rollback). **(3) No-throw guarantee**: thao tác không bao giờ throw (`noexcept`). Destructor, move ops, và swap nên là no-throw.

```cpp
// Strong guarantee via copy-and-swap idiom
class Widget {
    std::vector<int> data_;
public:
    Widget& operator=(Widget other) noexcept {  // copy made first
        swap(*this, other);                      // noexcept swap
        return *this;                            // old data destroyed via other
    }
    friend void swap(Widget& a, Widget& b) noexcept {
        using std::swap;
        swap(a.data_, b.data_);
    }
};
```

Follow-up (EN): How does the copy-and-swap idiom provide the strong guarantee?

---

### Q14. Nếu constructor ném exception thì sao?

**A:**
- EN: The object is **not fully constructed** — its destructor will NOT run. However, destructors of **already-constructed members and bases** DO run (reverse order). This is why RAII members are critical: they self-clean even when the containing constructor throws.
- VI: Object **chưa được tạo hoàn chỉnh** — destructor của nó sẽ KHÔNG chạy. Tuy nhiên, destructor của **các member và base đã tạo xong** SẼ chạy (thứ tự ngược). Đây là lý do RAII members quan trọng: chúng tự dọn dẹp ngay cả khi constructor throw.

```cpp
class Connection {
    std::unique_ptr<Socket> sock_;  // already constructed
    std::unique_ptr<Buffer> buf_;   // if this throws...
public:
    Connection() 
        : sock_(std::make_unique<Socket>())
        , buf_(std::make_unique<Buffer>())  // throws here?
    {
        // sock_ auto-destroyed because it's a completed member
    }
};
```

Follow-up (EN): What is two-phase initialization and when is it used instead of throwing from constructors?

---

### Q15. Có nên ném exception trong destructor?

**A:**
- EN: **No.** Destructors should be `noexcept` (implicit since C++11). If an exception is thrown during stack unwinding (another exception active) and a destructor throws, `std::terminate` is called. If cleanup can fail, log the error and swallow the exception.
- VI: **Không.** Destructor nên là `noexcept` (mặc định từ C++11). Nếu exception được throw trong stack unwinding (đang có exception khác) và destructor throw, `std::terminate` sẽ được gọi. Nếu cleanup có thể fail, log lỗi và nuốt exception.

```cpp
class File {
    int fd_;
public:
    ~File() noexcept {
        if (::close(fd_) < 0) {
            // DON'T throw — log and move on
            std::cerr << "close failed: " << errno << "\n";
        }
    }
    void close() {  // explicit close can throw
        if (::close(fd_) < 0) throw std::system_error(errno, std::generic_category());
        fd_ = -1;
    }
};
```

Follow-up (EN): What changed about destructor noexcept in C++11 vs C++03?

---

## 5) Templates (Senior Level)

### Q16. Template instantiation và code bloat?

**A:**
- EN: Templates are instantiated at compile time — each unique type combination generates new code. This can increase binary size (**code bloat**). Mitigations: explicit instantiation (limit where code is generated), type erasure (`std::function`, `std::any`), factor out type-independent logic into non-template base.
- VI: Template được instantiate tại compile time — mỗi tổ hợp kiểu tạo ra code mới. Điều này có thể tăng binary size (**code bloat**). Giảm thiểu: explicit instantiation (giới hạn nơi sinh code), type erasure (`std::function`, `std::any`), tách logic không phụ thuộc kiểu vào base non-template.

```cpp
// Explicit instantiation — controls where code is generated
// header.h
template<typename T> void process(T val);

// impl.cpp
template<typename T> void process(T val) { /* ... */ }
template void process<int>(int);        // instantiate here
template void process<double>(double);  // and here only
```

Follow-up (EN): What is the "thin template" idiom?

---

### Q17. SFINAE là gì?

**A:**
- EN: **Substitution Failure Is Not An Error** — if substituting template arguments produces an invalid type, that overload is silently removed from the candidate set instead of causing a compile error. Used for compile-time function selection. C++20 Concepts are the modern replacement.
- VI: **SFINAE** — nếu thay thế tham số template tạo ra kiểu không hợp lệ, overload đó bị loại âm thầm khỏi candidate set thay vì gây lỗi compile. Dùng để chọn hàm tại compile time. C++20 Concepts là thay thế hiện đại.

```cpp
// C++11 SFINAE with enable_if
template<typename T, std::enable_if_t<std::is_integral_v<T>, int> = 0>
T double_it(T x) { return x * 2; }

// C++20 Concepts — cleaner
template<std::integral T>
T double_it(T x) { return x * 2; }
```

Follow-up (EN): What is the difference between SFINAE-friendly and hard errors in template substitution?

---

### Q18. `constexpr` và `consteval` khác nhau thế nào?

**A:**
- EN: `constexpr` functions **can** be evaluated at compile time (if all inputs are constexpr) but also work at runtime. `consteval` (C++20) functions **must** be evaluated at compile time — calling with runtime values is a compile error. `constinit` (C++20) ensures static variables are initialized at compile time.
- VI: Hàm `constexpr` **có thể** tính tại compile time (nếu mọi input là constexpr) nhưng cũng chạy được runtime. Hàm `consteval` (C++20) **bắt buộc** tính tại compile time — gọi với giá trị runtime là lỗi compile. `constinit` (C++20) đảm bảo biến static được khởi tạo tại compile time.

```cpp
constexpr int square(int n) { return n * n; }
constexpr int a = square(5);  // compile-time: 25
int x = 5;
int b = square(x);            // runtime: OK for constexpr

consteval int cube(int n) { return n * n * n; }
constexpr int c = cube(3);    // compile-time: 27
// int d = cube(x);           // ERROR: consteval requires compile-time args
```

Follow-up (EN): What limitations did C++11 `constexpr` have that C++14/17/20 removed?

---

## 6) API Design (Senior)

### Q19. Khi nào dùng pass-by-value + move?

**A:**
- EN: When a function needs its own copy of the argument and the type has a cheap move. The caller can either copy (lvalue) or move (rvalue) into the parameter. This replaces writing two overloads (`const T&` + `T&&`) with one simple signature.
- VI: Khi hàm cần bản sao riêng của argument và kiểu có move rẻ. Caller có thể copy (lvalue) hoặc move (rvalue) vào parameter. Thay thế việc viết 2 overload (`const T&` + `T&&`) bằng 1 signature đơn giản.

```cpp
class Widget {
    std::string name_;
public:
    // One function handles both copy and move
    void set_name(std::string name) {
        name_ = std::move(name);  // move from the parameter
    }
    // Caller:
    // widget.set_name("hello");     // prvalue -> move into param -> move into member
    // widget.set_name(existing_str); // copy into param -> move into member
};
```

Follow-up (EN): When is this pattern suboptimal? (When assignment can reuse existing capacity — e.g., `std::string` buffer reuse.)

---

### Q20. Cách thiết kế API ít UB?

**A:**
- EN: **(1)** Use strong types instead of raw `int`/`bool` parameters. **(2)** Prefer `span`, `string_view` over raw pointers (but watch lifetime!). **(3)** Document preconditions clearly. **(4)** Use `[[nodiscard]]` for functions where ignoring the return value is likely a bug. **(5)** Avoid owning raw pointers in APIs.
- VI: **(1)** Dùng strong type thay vì `int`/`bool` thô. **(2)** Ưu tiên `span`, `string_view` hơn raw pointer (nhưng cẩn thận lifetime!). **(3)** Document precondition rõ ràng. **(4)** Dùng `[[nodiscard]]` cho hàm mà bỏ qua return value là bug. **(5)** Tránh owning raw pointer trong API.

```cpp
// BAD: easy to mix up parameters
void connect(const char* host, int port, bool use_tls, bool verify);
connect("api.com", 443, true, false);  // what do true/false mean?

// GOOD: strong types
enum class TLS { Enabled, Disabled };
enum class CertVerify { Yes, No };
void connect(std::string_view host, uint16_t port, TLS tls, CertVerify verify);
connect("api.com", 443, TLS::Enabled, CertVerify::No);  // self-documenting
```

Follow-up (EN): What is the "bool parameter" anti-pattern?

---

## 7) Câu hỏi "xoáy" thường gặp

### Q21. `new`/`delete` khi nào nên tránh?

**A:**
- EN: Almost always. Prefer `make_unique`/`make_shared` for heap objects, containers for arrays. Raw `new`/`delete` only in: custom allocators, placement new, low-level framework code. If you see `delete` in application code, it's usually a code smell.
- VI: Gần như luôn luôn nên tránh. Ưu tiên `make_unique`/`make_shared` cho heap object, container cho mảng. Raw `new`/`delete` chỉ dùng trong: custom allocator, placement new, framework low-level. Nếu thấy `delete` trong application code, thường là code smell.

```cpp
// BAD
Widget* w = new Widget();
process(w);
delete w;  // leak if process() throws

// GOOD
auto w = std::make_unique<Widget>();
process(*w);  // automatic cleanup
```

Follow-up (EN): When is placement `new` appropriate?

---

### Q22. `dynamic_cast` có xấu không?

**A:**
- EN: Not inherently, but heavy use often signals a design problem — you're likely fighting the type system instead of using polymorphism. Legitimate uses: plugin systems, multi-method dispatch, downcasting in visitor-like patterns. Performance: involves RTTI, O(depth) in some implementations.
- VI: Bản thân không xấu, nhưng dùng nhiều thường là dấu hiệu thiết kế có vấn đề — bạn đang chống lại type system thay vì dùng polymorphism. Dùng hợp lý: plugin system, multi-method dispatch, downcast trong visitor pattern. Hiệu năng: dùng RTTI, O(depth) trong một số implementation.

```cpp
// Acceptable: plugin system
if (auto* graphic = dynamic_cast<GraphicPlugin*>(plugin)) {
    graphic->render(canvas);
}

// Red flag: chain of dynamic_casts
if (auto* a = dynamic_cast<TypeA*>(obj)) { ... }
else if (auto* b = dynamic_cast<TypeB*>(obj)) { ... }  // consider visitor
```

Follow-up (EN): How does `dynamic_cast` differ from `static_cast` for downcasting?

---

### Q23. Có nên inline mọi thứ?

**A:**
- EN: No. The compiler decides inlining based on heuristics (function size, call frequency, optimization level). The `inline` keyword's primary purpose in modern C++ is **ODR compliance** — allowing function definitions in headers. Excessive manual inlining can hurt: larger binary → more cache misses → slower.
- VI: Không. Compiler tự quyết định inline dựa trên heuristics (kích thước hàm, tần suất gọi, mức tối ưu). Mục đích chính của `inline` trong C++ hiện đại là **tuân thủ ODR** — cho phép định nghĩa hàm trong header. Ép inline quá nhiều có thể hại: binary lớn hơn → nhiều cache miss → chậm hơn.

```cpp
// inline for ODR: function defined in header, included by multiple TUs
inline int helper(int x) { return x * 2; }

// Let compiler decide for performance — use LTO instead
// g++ -O2 -flto ...  // whole-program optimization
```

Follow-up (EN): What is LTO (Link-Time Optimization) and how does it help with inlining?

---

### Q24. PIMPL idiom — trade-off là gì?

**A:**
- EN: PIMPL hides implementation behind an opaque pointer. **Pros**: faster recompilation (impl changes don't recompile users), ABI stability, hides dependencies. **Cons**: heap allocation for impl, pointer indirection on every method call, more boilerplate. Use when: library APIs, large projects with slow builds.
- VI: PIMPL ẩn implementation sau opaque pointer. **Ưu điểm**: compile nhanh hơn (thay đổi impl không recompile user), ABI ổn định, ẩn dependency. **Nhược điểm**: cấp phát heap cho impl, pointer indirection mỗi lần gọi method, boilerplate nhiều hơn. Dùng khi: library API, project lớn build chậm.

```cpp
// widget.h — stable public header
class Widget {
public:
    Widget();
    ~Widget();
    void draw();
private:
    struct Impl;
    std::unique_ptr<Impl> pimpl_;
};

// widget.cpp — changes here don't recompile users
struct Widget::Impl {
    HeavyRenderer renderer_;
    std::vector<Mesh> meshes_;
    void do_draw() { /* ... */ }
};
Widget::Widget() : pimpl_(std::make_unique<Impl>()) {}
Widget::~Widget() = default;  // must be in .cpp
void Widget::draw() { pimpl_->do_draw(); }
```

Follow-up (EN): Why must the destructor be defined in the .cpp file when using PIMPL with `unique_ptr`?

---

## Flash card (ôn nhanh)

| Câu hỏi / Question | Trả lời nhanh / Quick answer |
|---|---|
| struct vs class? | Chỉ khác default access: public vs private |
| vtable chi phí? | +8 bytes/object, 1 indirection/call, no inlining |
| Virtual dtor khi nào? | Khi class có bất kỳ virtual function nào |
| Rule of 0? | Dùng RAII members, không viết special members |
| `std::move` move thật không? | Không — chỉ cast sang rvalue reference |
| `noexcept` move? | Bắt buộc để vector dùng move khi realloc |
| `unique_ptr` vs `shared_ptr`? | Default `unique_ptr`; `shared_ptr` khi thực sự shared |
| `weak_ptr` dùng khi? | Phá vòng circular reference |
| 3 exception guarantees? | Basic, Strong (commit-or-rollback), No-throw |
| Constructor throw? | Object chưa hoàn chỉnh, dtor không chạy, members tự dọn |
| Destructor throw? | Không — có thể gây `std::terminate` |
| SFINAE? | Substitution failure → loại overload, không lỗi |
| `constexpr` vs `consteval`? | constexpr: có thể compile-time; consteval: bắt buộc |
| PIMPL trade-off? | Nhanh compile + ABI ổn định vs heap alloc + indirection |
