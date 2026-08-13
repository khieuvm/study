# 08 - Design Patterns trong C++

---

## 1) Creational Patterns

### Q1. Singleton — implement thread-safe trong C++11?

**A:** Singleton dam bao chi co **1 instance** cua class. C++11 dam bao static local variable initialization la **thread-safe**.

```cpp
class Singleton {
public:
    static Singleton& instance() {
        static Singleton inst;  // C++11: thread-safe, lazy init
        return inst;
    }

    void do_something() { printf("doing\n"); }

    // Xoa copy/move
    Singleton(const Singleton&) = delete;
    Singleton& operator=(const Singleton&) = delete;

private:
    Singleton() { printf("Singleton created\n"); }
    ~Singleton() { printf("Singleton destroyed\n"); }
};

// Su dung:
Singleton::instance().do_something();
```

**Van de voi Singleton:**
- Kho test (global state, kho mock)
- Hidden dependencies
- Thu tu destruction khi co nhieu singleton (static destruction order)

**Khi nao dung:** Logger, Config, Registry — nhung objects thuc su can global unique access.

---

### Q2. Factory Method va Abstract Factory?

**A:**

**Factory Method**: cung cap interface tao object, de subclass quyet dinh class cu the.
```cpp
// Product interface
class Button {
public:
    virtual ~Button() = default;
    virtual void click() = 0;
};

class WinButton : public Button { void click() override { printf("Win click\n"); } };
class MacButton : public Button { void click() override { printf("Mac click\n"); } };

// Factory
class Dialog {
public:
    virtual std::unique_ptr<Button> create_button() = 0;
    void render() {
        auto btn = create_button();  // goi factory method
        btn->click();
    }
};

class WinDialog : public Dialog {
    std::unique_ptr<Button> create_button() override { return make_unique<WinButton>(); }
};
class MacDialog : public Dialog {
    std::unique_ptr<Button> create_button() override { return make_unique<MacButton>(); }
};
```

**Abstract Factory**: tao **family** cua cac objects lien quan.
```cpp
// Abstract factory: tao ca bo {Button, Checkbox, ...} cho 1 platform
class GUIFactory {
public:
    virtual ~GUIFactory() = default;
    virtual std::unique_ptr<Button>   create_button()   = 0;
    virtual std::unique_ptr<Checkbox> create_checkbox() = 0;
};

class WinFactory : public GUIFactory {
    std::unique_ptr<Button>   create_button()   override { return make_unique<WinButton>(); }
    std::unique_ptr<Checkbox> create_checkbox() override { return make_unique<WinCheckbox>(); }
};

// Client chi biet GUIFactory, khong biet Win/Mac
void build_ui(GUIFactory& factory) {
    auto btn = factory.create_button();
    auto chk = factory.create_checkbox();
}
```

---

### Q3. Builder Pattern?

**A:** Tach viec **xay dung** object phuc tap ra khoi **bieu dien** cua no.

```cpp
class HttpRequest {
public:
    std::string method, url, body;
    std::map<std::string, std::string> headers;
    int timeout_ms = 5000;
};

class HttpRequestBuilder {
    HttpRequest req_;
public:
    HttpRequestBuilder& method(std::string m) { req_.method = std::move(m); return *this; }
    HttpRequestBuilder& url(std::string u)    { req_.url    = std::move(u); return *this; }
    HttpRequestBuilder& body(std::string b)   { req_.body   = std::move(b); return *this; }
    HttpRequestBuilder& header(std::string k, std::string v) {
        req_.headers[std::move(k)] = std::move(v);
        return *this;
    }
    HttpRequestBuilder& timeout(int ms) { req_.timeout_ms = ms; return *this; }
    HttpRequest build() { return std::move(req_); }
};

// Fluent interface:
auto req = HttpRequestBuilder{}
    .method("POST")
    .url("https://api.example.com/data")
    .header("Content-Type", "application/json")
    .body(R"({"key":"value"})")
    .timeout(3000)
    .build();
```

---

## 2) Structural Patterns

### Q4. PIMPL (Pointer to IMPLementation) Idiom?

**A:** PIMPL an implementation details — giam compile time, che giau internals, binary compatibility.

```cpp
// foo.h — public header (it thay doi)
class Foo {
public:
    Foo();
    ~Foo();
    void do_work();
private:
    struct Impl;                   // forward declaration
    std::unique_ptr<Impl> pimpl_;  // chi can forward decl, khong include detail
};

// foo.cpp — implementation (thay doi thoai mai, chi compile file nay)
struct Foo::Impl {
    int heavy_data[1000];
    std::vector<std::string> cache;
    HeavyLibrary* lib;  // khong lo leak vao header

    void internal_work() { /* ... */ }
};

Foo::Foo() : pimpl_(std::make_unique<Impl>()) {}
Foo::~Foo() = default;  // phai dinh nghia o .cpp vi unique_ptr can complete type
void Foo::do_work() { pimpl_->internal_work(); }
```

**Loi ich:**
- Giam thoi gian compile: thay doi impl khong recompile users cua header
- Binary stability: them/bo private member khong thay doi ABI
- Che giau dependencies

---

### Q5. Adapter Pattern?

**A:** Chuyen doi interface cua class sang interface khac ma client mong doi.

```cpp
// Interface moi ma client dung:
class ModernLogger {
public:
    virtual void log(std::string_view level, std::string_view msg) = 0;
};

// Legacy code khong the thay doi:
class OldLogger {
public:
    void write_log(int severity, const char* format, ...);
};

// Adapter:
class LoggerAdapter : public ModernLogger {
    OldLogger old_;
public:
    void log(std::string_view level, std::string_view msg) override {
        int severity = (level == "ERROR") ? 3 : (level == "WARN") ? 2 : 1;
        old_.write_log(severity, "%s", std::string(msg).c_str());
    }
};

// Client dung ModernLogger, khong biet OldLogger ton tai
void process(ModernLogger& logger) {
    logger.log("INFO", "Processing...");
}
```

---

### Q6. Decorator Pattern?

**A:** Them behavior vao object **dong** ma khong sua class goc.

```cpp
// Interface
class Stream {
public:
    virtual ~Stream() = default;
    virtual void write(const char* data, size_t n) = 0;
};

// Base implementation
class FileStream : public Stream {
    FILE* f_;
public:
    FileStream(const char* path) : f_(fopen(path, "w")) {}
    ~FileStream() { fclose(f_); }
    void write(const char* data, size_t n) override { fwrite(data, 1, n, f_); }
};

// Decorator: them buffering
class BufferedStream : public Stream {
    Stream& inner_;
    std::vector<char> buf_;
    static constexpr size_t BUF_SIZE = 4096;
public:
    BufferedStream(Stream& s) : inner_(s) { buf_.reserve(BUF_SIZE); }
    void write(const char* data, size_t n) override {
        buf_.insert(buf_.end(), data, data+n);
        if (buf_.size() >= BUF_SIZE) flush();
    }
    void flush() { inner_.write(buf_.data(), buf_.size()); buf_.clear(); }
    ~BufferedStream() { flush(); }
};

// Decorator: them compression
class CompressedStream : public Stream {
    Stream& inner_;
public:
    CompressedStream(Stream& s) : inner_(s) {}
    void write(const char* data, size_t n) override {
        auto compressed = compress(data, n);
        inner_.write(compressed.data(), compressed.size());
    }
};

// Ket hop: file <- buffer <- compress
FileStream     file("output.bin");
BufferedStream buf(file);
CompressedStream comp(buf);
comp.write(data, size);
```

---

## 3) Behavioral Patterns

### Q7. Observer Pattern?

**A:** Cho phep nhieu objects **subscribe** va nhan **notification** khi state thay doi.

```cpp
#include <vector>
#include <functional>
#include <algorithm>

// Event system don gian:
template<typename... Args>
class Event {
    std::vector<std::function<void(Args...)>> handlers_;
public:
    void subscribe(std::function<void(Args...)> h) {
        handlers_.push_back(std::move(h));
    }
    void fire(Args... args) {
        for (auto& h : handlers_) h(args...);
    }
};

class Button {
public:
    Event<> on_click;
    Event<std::string> on_hover;

    void click()         { on_click.fire(); }
    void hover(std::string text) { on_hover.fire(text); }
};

// Su dung:
Button btn;
btn.on_click.subscribe([]{ printf("Button clicked!\n"); });
btn.on_click.subscribe([]{ printf("Logger: click event\n"); });
btn.on_hover.subscribe([](std::string t){ printf("Hover: %s\n", t.c_str()); });

btn.click();   // fire ca 2 handlers
```

---

### Q8. Strategy Pattern?

**A:** Dinh nghia mot family algorithms, dong goi chung, lam chung co the hoán doi.

```cpp
// Strategy interface
class SortStrategy {
public:
    virtual ~SortStrategy() = default;
    virtual void sort(std::vector<int>& data) = 0;
};

class QuickSort : public SortStrategy {
    void sort(std::vector<int>& data) override {
        std::sort(data.begin(), data.end());
    }
};

class MergeSort : public SortStrategy {
    void sort(std::vector<int>& data) override {
        std::stable_sort(data.begin(), data.end());
    }
};

// Context
class DataProcessor {
    std::unique_ptr<SortStrategy> strategy_;
public:
    DataProcessor(std::unique_ptr<SortStrategy> s) : strategy_(std::move(s)) {}
    void set_strategy(std::unique_ptr<SortStrategy> s) { strategy_ = std::move(s); }
    void process(std::vector<int>& data) { strategy_->sort(data); }
};

// Modern C++ version voi std::function (don gian hon):
class DataProcessor2 {
    std::function<void(std::vector<int>&)> sort_fn_;
public:
    DataProcessor2(std::function<void(std::vector<int>&)> fn) : sort_fn_(std::move(fn)) {}
    void process(std::vector<int>& data) { sort_fn_(data); }
};

DataProcessor2 dp([](auto& v){ std::sort(v.begin(), v.end()); });
```

---

### Q9. Command Pattern?

**A:** Dong goi request thanh object — de queue, undo/redo, log.

```cpp
class Command {
public:
    virtual ~Command() = default;
    virtual void execute() = 0;
    virtual void undo()    = 0;
};

class TextEditor {
    std::string text_;
    std::vector<std::unique_ptr<Command>> history_;
public:
    void execute(std::unique_ptr<Command> cmd) {
        cmd->execute();
        history_.push_back(std::move(cmd));
    }
    void undo() {
        if (!history_.empty()) {
            history_.back()->undo();
            history_.pop_back();
        }
    }

    std::string& text() { return text_; }
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

---

### Q10. RAII la Pattern hay Idiom?

**A:** RAII la **C++ Idiom** (da duoc mo ta trong file 02-cpp-oop.md), nhung no co the duoc xem la **nen tang** cho nhieu patterns khac trong C++:
- `std::lock_guard` = RAII Proxy cho mutex
- `std::unique_ptr` = RAII cho heap memory
- `std::fstream` = RAII cho file handle

---

## 4) Cac Pattern Dac Thu C++

### Q11. Type Erasure Pattern?

**A:** An kieu cu the dang sau interface — `std::function`, `std::any`, `std::variant` deu dung ky thuat nay.

```cpp
// Implement type erasure thu cong:
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

// Tuong duong std::function<void()> nhung don gian hon
AnyCallable fn = []{ printf("hello\n"); };
fn();
```

---

## Flash card

| Pattern | Muc dich chinh |
|---|---|
| Singleton | 1 instance, global access |
| Factory Method | Subclass quyet dinh kieu object tao |
| Abstract Factory | Tao family objects |
| Builder | Tao object phuc tap step-by-step |
| PIMPL | An impl, giam compile dependency |
| Adapter | Chuyen doi interface |
| Decorator | Them behaviour dong, khong sua class |
| Observer | Subscribe/notify khi state thay doi |
| Strategy | Hoán doi algorithm runtime |
| Command | Dong goi request, support undo/redo |
| CRTP | Static polymorphism, compile-time |
| Type Erasure | An kieu cu the dang sau interface |
