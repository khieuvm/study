# 02 - C++ OOP (Object-Oriented Programming) — Bilingual VI/EN

---

## 1) Class, Constructor, Destructor

### Q1. Phân biệt `struct` và `class` trong C++?

**A:**
- EN: The only difference is the default access: `struct` defaults to `public`, `class` defaults to `private`. By convention, `struct` is used for POD/data-only types and `class` for types with invariants and encapsulation.
- VI: Chỉ có một sự khác biệt: default access modifier. `struct` mặc định `public`, `class` mặc định `private`. Convention: `struct` cho POD, `class` cho type có encapsulation.

```cpp
struct S { int x; };    // x la public
class  C { int x; };    // x la private
```

Follow-up (EN): Can a struct have virtual functions? (Yes — it's identical to a class except for default access.)

---

### Q2. Rule of 3, Rule of 5, Rule of 0 là gì?

**A:**
- EN: Rules that determine when you must write special member functions: if you define any of {destructor, copy ctor, copy assignment}, define all three (Rule of 3). C++11 adds {move ctor, move assignment} → Rule of 5. Best practice: use RAII wrappers so the compiler generates everything → Rule of 0.
- VI: Quy tắc quyết định khi nào cần tự viết special member functions: viết 1 trong {destructor, copy ctor, copy=} thì phải viết cả 3 (Rule of 3). C++11 thêm {move ctor, move=} → Rule of 5. Tốt nhất: dùng RAII wrapper để compiler tự sinh → Rule of 0.

```cpp
// Rule of 5 đầy đủ
class Buffer {
    char* data_;
    size_t size_;
public:
    Buffer(size_t n) : data_(new char[n]), size_(n) {}

    ~Buffer() { delete[] data_; }

    Buffer(const Buffer& o) : data_(new char[o.size_]), size_(o.size_) {
        std::memcpy(data_, o.data_, size_);
    }

    Buffer& operator=(const Buffer& o) {
        if (this != &o) {
            delete[] data_;
            data_ = new char[o.size_];
            size_ = o.size_;
            std::memcpy(data_, o.data_, size_);
        }
        return *this;
    }

    Buffer(Buffer&& o) noexcept : data_(o.data_), size_(o.size_) {
        o.data_ = nullptr;
        o.size_ = 0;
    }

    Buffer& operator=(Buffer&& o) noexcept {
        if (this != &o) {
            delete[] data_;
            data_ = o.data_;
            size_ = o.size_;
            o.data_ = nullptr;
            o.size_ = 0;
        }
        return *this;
    }
};
```

**Rule of 0 — tốt hơn / Better approach:**
```cpp
class Buffer {
    std::vector<char> data_;  // vector tự quản lý memory
public:
    Buffer(size_t n) : data_(n) {}
    // Compiler-generated dtor, copy, move are all correct
};
```

Follow-up (EN): What happens if you define a copy constructor but not a move constructor? (The move operations are implicitly deleted.)

---

### Q3. Constructor có thể fail không? Nên xử lý thế nào?

**A:**
- EN: Constructors have no return value; the only way to signal failure is to **throw an exception**. If the constructor throws, the destructor is NOT called — so resources acquired before the throw must be cleaned up manually, or better, held in RAII wrappers.
- VI: Constructor không có return value; cách duy nhất báo lỗi là **throw exception**. Nếu constructor throw, destructor Không được gọi — các resource đã cấp phát trước khi throw phải được dọn sạch thủ công, hoặc tốt hơn là dùng RAII wrapper.

```cpp
class File {
    FILE* f_;
public:
    File(const char* path) {
        f_ = fopen(path, "r");
        if (!f_) throw std::runtime_error("Cannot open file");
    }
    ~File() { fclose(f_); }
};
```

```cpp
// Problem: partial construction leak
class TwoResources {
    int* a_;
    int* b_;
public:
    TwoResources() {
        a_ = new int(1);
        b_ = new int(2);  // if this throws -> a_ leaks
    }
};

// Fix: use RAII members
class TwoResources {
    std::unique_ptr<int> a_{new int(1)};
    std::unique_ptr<int> b_{new int(2)};  // if throw, a_ auto-freed
};
```

Follow-up (EN): What is a two-phase init pattern and when would you use it instead of throwing from a constructor?

---

### Q4. Initializer list vs assignment trong constructor?

**A:**
- EN: Always prefer the member initializer list — it directly constructs members, whereas assignment default-constructs first then assigns (two steps). Initializer list is **mandatory** for `const` members, references, and base classes without a default constructor.
- VI: Luôn dùng initializer list — nó gọi constructor trực tiếp, thay vì default-construct rồi assign (2 bước). Initializer list là **bắt buộc** với `const` member, reference, và base class không có default constructor.

```cpp
class Foo {
    std::string name_;
    int value_;
public:
    // BAD: default-construct name_ then copy-assign
    Foo(std::string n, int v) { name_ = n; value_ = v; }

    // GOOD: direct construction
    Foo(std::string n, int v) : name_(std::move(n)), value_(v) {}
};
```

```cpp
class Bar {
    const int id_;    // must use initializer list
    int& ref_;        // must use initializer list
public:
    Bar(int id, int& r) : id_(id), ref_(r) {}
};
```

- EN: Initialization order follows **declaration order** in the class, not the order in the initializer list.
- VI: Thứ tự khởi tạo theo **thứ tự khai báo** trong class, không phải thứ tự trong initializer list.

Follow-up (EN): What bug can occur if initializer list order differs from declaration order?

---

## 2) Inheritance và Virtual

### Q5. `virtual` hoạt động như thế nào? vtable là gì?

**A:**
- EN: When a class has at least one virtual function, the compiler generates a **vtable** (array of function pointers). Each object contains a hidden **vptr** pointing to its class's vtable. Virtual calls go through vptr → vtable → function pointer — one level of indirection.
- VI: Khi class có ít nhất 1 virtual function, compiler tạo **vtable** (mảng function pointer). Mọi object có 1 con trỏ ẩn **vptr** trỏ vào vtable của class mình. Virtual call đi qua vptr → vtable → function pointer — một mức gián tiếp.

```
vtable của Animal: [ &Animal::speak ]
vtable của Dog:    [ &Dog::speak    ]
vtable của Cat:    [ &Cat::speak    ]
```

```cpp
Animal* a = new Dog();
a->speak();
// 1. Read vptr from *a (points to Dog's vtable)
// 2. Get function pointer at speak()'s offset
// 3. Call Dog::speak()
```

- EN: Cost: +8 bytes per object (vptr), one indirection per call, prevents inlining.
- VI: Chi phí: +8 byte mỗi object (vptr), 1 indirection mỗi lần gọi, không thể inline.

Follow-up (EN): When can the compiler devirtualize a virtual call?

---

### Q6. `override` và `final` dùng để làm gì?

**A:**
- EN: `override` (C++11) tells the compiler to verify the function actually overrides a base virtual function — catches signature mismatches at compile time. `final` prevents further overriding or inheritance.
- VI: `override` (C++11) yêu cầu compiler kiểm tra function có đúng override từ base hay không — bắt lỗi sai signature lúc compile. `final` ngăn override tiếp hoặc kế thừa tiếp.

```cpp
class Base {
    virtual void foo(int x);
    virtual void bar();
};

class Derived : public Base {
    void foo(int x) override;  // OK
    void bar(int x) override;  // ERROR: signature mismatch
    void baz() override;       // ERROR: baz not in Base

    void bar() final;          // subclasses cannot override bar()
};

class Leaf final : public Derived {};  // cannot inherit from Leaf
```

Follow-up (EN): Without `override`, what happens if you get the signature wrong? (You silently create a new function instead of overriding.)

---

### Q7. Virtual destructor quan trọng thế nào?

**A:**
- EN: If you delete a derived object through a base pointer and the base destructor is **not** virtual, the derived destructor won't run — causing resource leaks and undefined behavior. Rule: any class with virtual functions must have a virtual destructor.
- VI: Nếu delete object derived qua base pointer mà destructor của base **không** virtual, destructor derived sẽ không được gọi — gây leak và UB. Quy tắc: class có virtual function phải có virtual destructor.

```cpp
class Base {
public:
    ~Base() { printf("~Base\n"); }  // NON-virtual — BUG
};
class Derived : public Base {
    int* data_ = new int[100];
public:
    ~Derived() { delete[] data_; printf("~Derived\n"); }
};

Base* p = new Derived();
delete p;  // Only ~Base runs, ~Derived skipped -> data_ leaks

// FIX:
class Base {
public:
    virtual ~Base() = default;
};
```

Follow-up (EN): Should a class marked `final` still have a virtual destructor? (If it has virtual functions or could be held by base pointer, yes.)

---

### Q8. Pure virtual function và abstract class?

**A:**
- EN: A pure virtual function (`= 0`) has no implementation in the base and forces derived classes to provide one. A class with any pure virtual function is **abstract** and cannot be instantiated. Note: a pure virtual function *can* have a body — derived classes can explicitly call it.
- VI: Pure virtual function (`= 0`) không có implementation o base, bước derived phải implement. Class có bất kỳ pure virtual function nào là **abstract**, không thể tạo object. Lưu y: pure virtual *có thể* có body — derived có thể gọi no tường mình.

```cpp
class Shape {
public:
    virtual double area() const = 0;
    virtual void draw() const = 0;
    virtual void describe() const = 0;
};
// Pure virtual with body (rare but valid)
void Shape::describe() const { printf("I am a shape\n"); }

class Circle : public Shape {
    double r_;
public:
    Circle(double r) : r_(r) {}
    double area() const override { return 3.14159 * r_ * r_; }
    void draw() const override { printf("O\n"); }
    void describe() const override {
        Shape::describe();  // call base implementation explicitly
        printf("I am a circle\n");
    }
};

// Shape s;              // ERROR: abstract class
Shape* s = new Circle(5.0);  // OK
```

Follow-up (EN): Can an abstract class have a constructor? (Yes — it's called by derived constructors.)

---

### Q9. Diamond problem là gì? Virtual inheritance gìải quyết thế nào?

**A:**
- EN: Diamond problem occurs when a class inherits from two classes that share a common base — it gets two copies of the base. Virtual inheritance ensures only one shared base instance exists, at the cost of an extra vbtable pointer and more complex construction.
- VI: Diamond problem xảy ra khi một class kế thừa từ hai class cũng chung một base — nó có 2 bản sao của base. Virtual inheritance đảm bảo chỉ có 1 bản sao base, đổi lai thêm vbtable pointer và construction phức tạp hon.

```
     Base
    /    \
 Left   Right
    \    /
     Both
```

```cpp
class Base { public: int x = 0; };
class Left  : public Base {};
class Right : public Base {};
class Both  : public Left, public Right {};

Both b;
b.x = 1;  // ERROR: ambiguous — Left::x or Right::x?
```

```cpp
// Fix: virtual inheritance
class Left  : virtual public Base {};
class Right : virtual public Base {};
class Both  : public Left, public Right {};

Both b;
b.x = 1;  // OK: only one copy of Base
```

- EN: In practice, needing diamond inheritance usually signals a design problem — prefer composition.
- VI: Thực tế, cần diamond inheritance thường là đầu hiểu thiết kế sai — nên dùng composition.

Follow-up (EN): Who is responsible for constructing the virtual base in diamond inheritance? (The most-derived class.)

---

## 3) RAII

### Q10. RAII là gì? Tại sao là pattern quan trọng nhất trong C++?

**A:**
- EN: **RAII (Resource Acquisition Is Initialization)**: tie resource lifetime to object lifetime. The constructor acquires, the destructor releases — automatically. This makes code exception-safe and eliminates resource leaks regardless of control flow (early return, exceptions, etc.).
- VI: **RAII**: gần vòng đời resource với vòng đời object. Constructor cấp phát, destructor gìải phóng — tự động. Code tro nên exception-safe và không leak resource bắt kế control flow (return sớm, exception, ...).

```cpp
// Without RAII (C style) — error-prone
void process() {
    FILE* f = fopen("data.txt", "r");
    if (!f) return;
    int* buf = (int*)malloc(1024);
    if (!buf) { fclose(f); return; }   // must remember to close f
    if (error) { free(buf); fclose(f); return; }  // repeat cleanup
    free(buf);
    fclose(f);
}

// With RAII (C++ style) — clean
void process() {
    std::ifstream f("data.txt");     // auto-closes on destruction
    if (!f) return;
    std::vector<int> buf(256);       // auto-frees on destruction
    if (error) return;               // everything cleaned up automatically
}
```

- EN: Standard RAII wrappers: `unique_ptr` (heap), `vector` (array), `ifstream` (file), `lock_guard` (mutex), `jthread` (thread).
- VI: RAII wrappers có sẵn: `unique_ptr` (heap), `vector` (array), `ifstream` (file), `lock_guard` (mutex), `jthread` (thread).

Follow-up (EN): How does RAII provide exception safety?

---

### Q11. `explicit` keyword dùng để làm gì?

**A:**
- EN: `explicit` prevents implicit conversions through single-argument constructors. Without it, the compiler can silently convert types in surprising ways. Rule: single-argument constructors should be `explicit` unless implicit conversion is intentionally desired.
- VI: `explicit` ngăn compiler tự động chuyển đổi kiểu qua constructor 1 tham số. không có no, compiler có thể chuyển đổi kiểu âm thầm. Quy tắc: constructor 1 tham số nên có `explicit` tru khi muốn implicit conversion.

```cpp
class MyString {
public:
    MyString(int n);          // creates string with n characters
    MyString(const char* s);
};

void print(MyString s);
print(42);      // compiles! implicitly calls MyString(42) — likely a bug

// Fix:
class MyString {
public:
    explicit MyString(int n);  // blocks implicit conversion
    MyString(const char* s);   // char* -> MyString still OK
};

print(42);              // ERROR: no implicit conversion
print(MyString(42));    // OK: explicit
print("hello");         // OK
```

Follow-up (EN): Does `explicit` apply to conversion operators too? (Yes, since C++11: `explicit operator bool()`.)

---

## 4) Operator Overloading

### Q12. Khi nào dùng member function, khi nào dùng free function khi overload operator?

**A:**
- EN: Some operators (`=`, `[]`, `()`, `->`) **must** be members. Symmetric binary operators (`+`, `==`) should be free functions số both operands can undergo conversion. Stream operators (`<<`, `>>`) must be free functions since the left operand is `ostream`/`istream`.
- VI: Một số operator (`=`, `[]`, `()`, `->`) **phải** là member. Binary operator đổi xung (`+`, `==`) nên là free function để cả 2 operand đều có thể convert. Stream operator (`<<`, `>>`) phải là free function vì operand trái là `ostream`/`istream`.

| Operator | Recommended form |
|---|---|
| `=`, `[]`, `()`, `->` | **Must** be member |
| Unary `+`, `-`, `++`, `--` | Member |
| `<<`, `>>` (stream) | **Free function** (with `friend`) |
| Binary `+`, `-`, `*`, `/` | Free function |
| `==`, `!=`, `<`, `>` | Free function (or `friend`) |

```cpp
class Vec2 {
public:
    float x, y;
    Vec2& operator=(const Vec2&) = default;          // member: assignment
    Vec2 operator-() const { return {-x, -y}; }      // member: unary

    friend Vec2 operator+(Vec2 a, Vec2 b) {           // free: binary
        return {a.x+b.x, a.y+b.y};
    }
    friend std::ostream& operator<<(std::ostream& os, const Vec2& v) {
        return os << "(" << v.x << "," << v.y << ")"; // free: stream
    }
};
```

Follow-up (EN): What is the spaceship operator (`<=>`) in C++20 and how does it simplify comparison operators?

---

### Q13. `friend` class/function là gì? Khi nào dùng?

**A:**
- EN: `friend` grants another function or class access to private/protected members. Use for operator overloading and tightly coupled classes. Avoid overuse — it breaks encapsulation.
- VI: `friend` cho phép function hoặc class khác truy cập private/protected members. Dùng cho operator overloading và các class liên kết chat. Tránh làm dùng — nó phá vo encapsulation.

```cpp
class BankAccount {
    double balance_ = 0;
    friend class Auditor;
    friend std::ostream& operator<<(std::ostream&, const BankAccount&);
};

class Auditor {
public:
    void inspect(const BankAccount& acc) {
        printf("Balance: %f\n", acc.balance_);  // OK via friend
    }
};
```

- EN: When to use: operator overloading, factory functions, serialization. When NOT to: if public/protected API can solve it — prefer that.
- VI: Khi nào dùng: operator overloading, factory function, serialization. Khi nào Không: nếu public/protected API gìải quyết được — ưu tiên cách do.

Follow-up (EN): Is friendship inherited or transitive? (No to both.)

---

## 5) Câu hỏi thực tế senior

### Q14. Phân biệt `public`, `protected`, `private` inheritance?

**A:**
- EN: The inheritance access specifier controls how base class members are exposed in the derived class. `public` = is-a (most common), `protected` = rare, `private` = implemented-in-terms-of (usually prefer composition instead).
- VI: Access specifier của inheritance quyết định cách members của base được expose trong derived. `public` = is-a (phổ biến nhất), `protected` = hiem, `private` = implemented-in-terms-of (thường nên dùng composition thay thể).

```cpp
class Base { public: int x; protected: int y; private: int z; };

class PubDerived  : public    Base {};  // x=public, y=protected, z=inaccessible
class ProtDerived : protected Base {};  // x=protected, y=protected, z=inaccessible
class PrivDerived : private   Base {};  // x=private, y=private, z=inaccessible
```

Follow-up (EN): Give an example where private inheritance is preferable to composition. (When you need to override virtual functions of the base.)

---

### Q15. Composition vs Inheritance — khi nào dùng cai nào?

**A:**
- EN: **Prefer composition over inheritance.** Use inheritance only for true "is-a" relationships where you need polymorphism. Use composition for "has-a" relationships and code reuse without exposing the internal interface.
- VI: **Ưu tiên composition hon inheritance.** Chỉ dùng inheritance khi có quan hệ "is-a" thực sự và cần polymorphism. Dùng composition cho quan hệ "has-a" và reuse code mà không lo interface nội bộ.

```cpp
// BAD: inheritance just for reuse
class Stack : public std::vector<int> {
    // exposes all vector API — not a real stack!
};

// GOOD: composition
class Stack {
    std::vector<int> data_;
public:
    void push(int x) { data_.push_back(x); }
    void pop()       { data_.pop_back(); }
    int  top() const { return data_.back(); }
};
```

Follow-up (EN): What is the Liskov Substitution Principle and how does it relate to inheritance?

---

### Q16. CRTP (Curiously Recurring Template Pattern) là gì?

**A:**
- EN: CRTP is a technique where a class inherits from a template instantiated with itself: `class Derived : Base<Derived>`. It achieves **static (compile-time) polymorphism** — nó vtable, nó runtime overhead, and the compiler can inline everything.
- VI: CRTP là kỹ thuật trong do class kế thừa từ template mà tham số là chính no: `class Derived : Base<Derived>`. Đặt được **static polymorphism** — không vtable, không overhead runtime, compiler có thể inline tất cả.

```cpp
// Runtime polymorphism (virtual):
struct Base { virtual void foo() = 0; };
struct Derived : Base { void foo() override { /*...*/ } };
Base* p = new Derived(); p->foo();  // vtable lookup

// Compile-time polymorphism (CRTP):
template<typename D>
struct Base {
    void interface() { static_cast<D*>(this)->implementation(); }
};
struct Concrete : Base<Concrete> {
    void implementation() { printf("Concrete\n"); }
};
Concrete c; c.interface();  // direct call, inlineable
```

- EN: Real-world uses: `std::enable_shared_from_this<T>`, mixin classes (Comparable, Serializable).
- VI: Ứng dụng thực tế: `std::enable_shared_from_this<T>`, mixin classes (Comparable, Serializable).

```cpp
template<typename T>
struct Comparable {
    bool operator!=(const T& o) const { return !(static_cast<const T&>(*this) == o); }
    bool operator> (const T& o) const { return o < static_cast<const T&>(*this); }
};
struct Point : Comparable<Point> {
    int x, y;
    bool operator==(const Point& o) const { return x==o.x && y==o.y; }
    bool operator< (const Point& o) const { return std::tie(x,y) < std::tie(o.x,o.y); }
};
```

Follow-up (EN): How does C++20 Concepts compare to CRTP for static polymorphism?

---

## Flash card

| Câu hỏi / Question | Trả lỗi nhanh / Quick answer |
|---|---|
| Rule of 5 gom gì? | dtor, copy ctor, copy=, move ctor, move= |
| virtual destructor khi nào? | When class has any virtual function |
| Pure virtual = ? | `= 0`, class becomes abstract |
| Diamond problem fix? | `virtual` inheritance — one shared base |
| RAII là gì? | Resource = object lifetime, dtor auto-releases |
| `explicit` constructor? | Prevents implicit type conversion |
| `override` keyword? | Compiler verifies correct base override |
| Composition vs Inheritance? | Prefer composition; inheritance for "is-a" only |
| CRTP dùng để gì? | Static polymorphism, nó vtable overhead |
| `friend` khi nào? | Operator overloading, tightly coupled classes |
