# 08 - Design Patterns trong C++ — Bilingual VI/EN

---

## 1) Creational Patterns

### Q1. Singleton — implement thread-safe trong C++11?

**A:**
- EN: Singleton ensures **only one instance** exists. In C++11, a local `static` variable is guaranteed to be initialized thread-safely (Meyers' Singleton). Delete copy/move to prevent duplication. Drawbacks: hard to test (global state), hidden dependencies, static destruction order issues.
- VI: Singleton đảm bảo chỉ có **1 instance**. Trong C++11, biến `static` local được đảm bảo khởi tạo thread-safe (Meyers' Singleton). Xóa copy/move để ngan duplicate. Nhược điểm: kho test (global state), dependency an, van để thứ tự destruction.

```cpp
class Singleton {
public:
    static Singleton& instance() {
        static Singleton inst;  // C++11: thread-safe, lazy init
        return inst;
    }
    Singleton(const Singleton&) = delete;
    Singleton& operator=(const Singleton&) = delete;
private:
    Singleton() = default;
};
```

- EN: Use sparingly — Logger, Config, Registry. Prefer dependency injection for testability.
- VI: Dùng han che — Logger, Config, Registry. Ưu tiên dependency injection để để test.

Follow-up (EN): What is the "static initialization order fiasco" and how does Meyers' Singleton avoid it?

---

### Q2. Factory Method và Abstract Factory?

**A:**
- EN: **Factory Method**: defines an interface for creating objects but lets subclasses decide which class to instantiate. **Abstract Factory**: creates families of related objects without specifying concrete classes. Both decouple object creation from usage.
- VI: **Factory Method**: định nghĩa interface tạo object nhưng để subclass quyết định class cụ thể. **Abstract Factory**: tạo family các object liên quan mà không chỉ rõ concrete class. Cả hai tách rời viec tạo object khoi viec sử dụng.

```cpp
// Factory Method
class Dialog {
public:
    virtual std::unique_ptr<Button> create_button() = 0;
    void render() { auto btn = create_button(); btn->click(); }
};
class WinDialog : public Dialog {
    std::unique_ptr<Button> create_button() override { return make_unique<WinButton>(); }
};

// Abstract Factory: creates whole families
class GUIFactory {
public:
    virtual std::unique_ptr<Button>   create_button()   = 0;
    virtual std::unique_ptr<Checkbox> create_checkbox() = 0;
};
```

Follow-up (EN): When would you choose Factory Method over Abstract Factory?

---

### Q3. Builder Pattern?

**A:**
- EN: Builder separates **construction** of a complex object from its **representation**. Uses a fluent interface (method chaining) to set optional parameters step-by-step, then calls `build()` to produce the final object.
- VI: Builder tách **qua trình xảy dùng** object phức tạp khoi **bieu dien** của no. Dùng fluent interface (method chaining) để set các tham số tùy chọn từng bước, rồi gọi `build()` để tạo object cũối cũng.

```cpp
auto req = HttpRequestBuilder{}
    .method("POST")
    .url("https://api.example.com/data")
    .header("Content-Type", "application/json")
    .body(R"({"key":"value"})")
    .timeout(3000)
    .build();
```

Follow-up (EN): How does Builder differ from a constructor with default parameters?

---

## 2) Structural Patterns

### Q4. PIMPL (Pointer to IMPLementation) Idiom?

**A:**
- EN: PIMPL hides implementation details behind an opaque pointer. Benefits: reduced compile times (changing impl doesn't recompile users), ABI stability (adding private members doesn't change binary layout), and hidden dependencies (impl headers stay in .cpp).
- VI: PIMPL ẩn implementation details sau opaque pointer. Lỗi ich: giảm thời gian compile (thay đổi impl không recompile user), ABI ổn định (thêm private member không đổi binary layout), và an dependency (impl header năm trong .cpp).

```cpp
// foo.h — stable public header
class Foo {
public:
    Foo();
    ~Foo();
    void do_work();
private:
    struct Impl;
    std::unique_ptr<Impl> pimpl_;
};

// foo.cpp — implementation (changes don't affect users)
struct Foo::Impl {
    int data[1000];
    HeavyLibrary* lib;
    void internal_work() { /* ... */ }
};
Foo::Foo() : pimpl_(std::make_unique<Impl>()) {}
Foo::~Foo() = default;  // must be in .cpp (unique_ptr needs complete type)
void Foo::do_work() { pimpl_->internal_work(); }
```

Follow-up (EN): What is the performance cost of PIMPL (extra indirection, heap allocation)?

---

### Q5. Adapter Pattern?

**A:**
- EN: Adapter converts the interface of an existing class to match what the client expects — allows incompatible interfaces to work together without modifying the original class.
- VI: Adapter chuyển đổi interface của class có sẵn sáng đang client mong đổi — cho phép các interface không tương thích làm viec cũng nhau mà không sua class gốc.

```cpp
// Client expects ModernLogger
class ModernLogger {
public:
    virtual void log(std::string_view level, std::string_view msg) = 0;
};

// Legacy code (cannot change)
class OldLogger { public: void write_log(int severity, const char* fmt, ...); };

// Adapter bridges the gap
class LoggerAdapter : public ModernLogger {
    OldLogger old_;
public:
    void log(std::string_view level, std::string_view msg) override {
        int severity = (level == "ERROR") ? 3 : 1;
        old_.write_log(severity, "%s", std::string(msg).c_str());
    }
};
```

Follow-up (EN): What is the difference between class adapter (inheritance) and object adapter (composition)?

---

### Q6. Decorator Pattern?

**A:**
- EN: Decorator adds behavior to objects **dynamically** by wrapping them — each decorator implements the same interface as the wrapped object. Decorators can be stacked: `Compress(Buffer(File))`. Prefer over inheritance for combining behaviors.
- VI: Decorator thêm behavior cho object **đóng** bằng cách wrap chung — mọi decorator implement cũng interface với object được wrap. Decorator có thể xep chong: `Compress(Buffer(File))`. Ưu tiên hon inheritance cho viec kết hợp behavior.

```cpp
class Stream {
public:
    virtual ~Stream() = default;
    virtual void write(const char* data, size_t n) = 0;
};

class FileStream : public Stream { /* writes to file */ };

class BufferedStream : public Stream {
    Stream& inner_;
public:
    BufferedStream(Stream& s) : inner_(s) {}
    void write(const char* data, size_t n) override {
        // buffer data, flush to inner_ when full
    }
};

// Stack decorators:
FileStream     file("output.bin");
BufferedStream buf(file);
CompressedStream comp(buf);  // file <- buffer <- compress
```

Follow-up (EN): How does Decorator differ from Proxy pattern?

---

## 3) Behavioral Patterns

### Q7. Observer Pattern?

**A:**
- EN: Observer lets multiple objects **subscribe** to state changes and receive **notifications** when the subject changes. Modern C++ implementation uses `std::function` for type-erased callbacks, avoiding tight coupling between subject and observers.
- VI: Observer cho phép nhiều object **subscribe** vào thay đổi state và nhận **notification** khi subject thay đổi. Implementation C++ hiện đại dùng `std::function` cho type-erased callback, tránh tight coupling giữa subject và observer.

```cpp
template<typename... Args>
class Event {
    std::vector<std::function<void(Args...)>> handlers_;
public:
    void subscribe(std::function<void(Args...)> h) { handlers_.push_back(std::move(h)); }
    void fire(Args... args) { for (auto& h : handlers_) h(args...); }
};

class Button {
public:
    Event<> on_click;
    void click() { on_click.fire(); }
};

Button btn;
btn.on_click.subscribe([]{ printf("Clicked!\n"); });
btn.click();
```

Follow-up (EN): How would you handle observer lifetime (unsubscribe, weak references)?

---

### Q8. Strategy Pattern?

**A:**
- EN: Strategy defines a family of interchangeable algorithms, encapsulating each one so they can be swapped at runtime. Modern C++: use `std::function` or templates instead of virtual dispatch for simpler cases.
- VI: Strategy định nghĩa family algorithm có thể hoan đổi, đóng gói tung cai để có thể swap lúc runtime. C++ hiện đại: dùng `std::function` hoặc template thay vì virtual dispatch cho trường hợp đơn gìản.

```cpp
// Classic: virtual dispatch
class SortStrategy {
public:
    virtual void sort(std::vector<int>& data) = 0;
};

// Modern: std::function (simpler)
class DataProcessor {
    std::function<void(std::vector<int>&)> sort_fn_;
public:
    DataProcessor(std::function<void(std::vector<int>&)> fn) : sort_fn_(std::move(fn)) {}
    void process(std::vector<int>& data) { sort_fn_(data); }
};

DataProcessor dp([](auto& v){ std::sort(v.begin(), v.end()); });
```

Follow-up (EN): When would you prefer a template-based strategy over `std::function`?

---

### Q9. Command Pattern?

**A:**
- EN: Command encapsulates a request as an object — enabling queuing, logging, and **undo/redo**. Each command stores enough state to execute and reverse the operation.
- VI: Command đóng gói request thành object — cho phép queuing, logging, và **undo/redo**. Mọi command lưu đủ state để execute và reverse thao tac.

```cpp
class Command {
public:
    virtual void execute() = 0;
    virtual void undo()    = 0;
    virtual ~Command() = default;
};

class InsertCommand : public Command {
    TextEditor& editor_;
    size_t pos_;
    std::string text_;
public:
    InsertCommand(TextEditor& e, size_t pos, std::string txt)
        : editor_(e), pos_(pos), text_(std::move(txt)) {}
    void execute() override { editor_.text().insert(pos_, text_); }
    void undo()    override { editor_.text().erase(pos_, text_.size()); }
};
```

Follow-up (EN): How would you implement redo in addition to undo?

---

### Q10. RAII là Pattern hay Idiom?

**A:**
- EN: RAII is a **C++ idiom** (not a GoF pattern), but it's the **foundation** for many patterns in C++: `lock_guard` (RAII for mutex), `unique_ptr` (RAII for heap), `fstream` (RAII for files). See 02-cpp-oop.md Q10 for detailed coverage.
- VI: RAII là **C++ idiom** (không phải GoF pattern), nhưng là **nên tăng** cho nhiều pattern trong C++: `lock_guard` (RAII cho mutex), `unique_ptr` (RAII cho heap), `fstream` (RAII cho file). Xem 02-cpp-oop.md Q10 để biết chi tiết.

Follow-up (EN): Can RAII be used in C? (Partially — with GCC's `__attribute__((cleanup))`.)

---

## 4) Các Pattern Đặc thù C++

### Q11. Type Erasure Pattern?

**A:**
- EN: Type erasure hides concrete types behind a uniform interface — `std::function`, `std::any`, `std::variant` all use this technique. Implementation: a base class with virtual methods + a derived template class that wraps the actual type.
- VI: Type erasure ẩn kiểu cụ thể đang sau interface thống nhất — `std::function`, `std::any`, `std::variant` đều dùng kỹ thuật này. Implementation: base class với virtual method + derived template class wrap kiểu thực tế.

```cpp
class AnyCallable {
    struct Base { virtual void call() = 0; virtual ~Base() = default; };
    template<typename F>
    struct Derived : Base {
        F f;
        Derived(F f) : f(std::move(f)) {}
        void call() override { f(); }
    };
    std::unique_ptr<Base> ptr_;
public:
    template<typename F>
    AnyCallable(F f) : ptr_(std::make_unique<Derived<F>>(std::move(f))) {}
    void operator()() { ptr_->call(); }
};
```

Follow-up (EN): What is the performance cost of type erasure compared to templates?

---

## Flash card

| Pattern | Purpose / Mục đích |
|---|---|
| Singleton | One instance, global access point |
| Factory Method | Subclass decides concrete object type |
| Abstract Factory | Creates family of related objects |
| Builder | Complex object construction step-by-step |
| PIMPL | Hide impl, reduce compile deps, ABI stability |
| Adapter | Convert incompatible interface |
| Decorator | Add behavior dynamically by wrapping |
| Observer | Subscribe/notify on state change |
| Strategy | Swap algorithms at runtime |
| Command | Encapsulate request, support undo/redo |
| CRTP | Static polymorphism, compile-time dispatch |
| Type Erasure | Hide concrete type behind uniform interface |
