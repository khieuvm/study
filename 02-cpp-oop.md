# 02 - C++ OOP (Object-Oriented Programming)

---

## 1) Class, Constructor, Destructor

### Q1. Phan biet `struct` va `class` trong C++?

**A:** Chi co **mot su khac biet duy nhat**: default access modifier.
- `struct`: members la `public` mac dinh
- `class`: members la `private` mac dinh

```cpp
struct S { int x; };    // x la public
class  C { int x; };    // x la private

// Convention thong thuong:
// - struct: POD (Plain Old Data), data container don gian
// - class: co invariant, encapsulation, methods
```

---

### Q2. Rule of 3, Rule of 5, Rule of 0 la gi?

**A:** Quy tac quyet dinh khi nao can tu viet cac special member functions.

**Rule of 3** (C++03): Neu ban viet mot trong ba cai nay, ban can viet ca ba:
1. Destructor
2. Copy constructor
3. Copy assignment operator

**Rule of 5** (C++11): Them 2 cai nua:
4. Move constructor
5. Move assignment operator

**Rule of 0**: Tot nhat la khong viet cai nao — dung RAII wrapper (`vector`, `unique_ptr`, ...) de compiler tu sinh.

```cpp
// Rule of 5 day du
class Buffer {
    char* data_;
    size_t size_;
public:
    Buffer(size_t n) : data_(new char[n]), size_(n) {}

    // Destructor
    ~Buffer() { delete[] data_; }

    // Copy constructor
    Buffer(const Buffer& o) : data_(new char[o.size_]), size_(o.size_) {
        std::memcpy(data_, o.data_, size_);
    }

    // Copy assignment
    Buffer& operator=(const Buffer& o) {
        if (this != &o) {           // self-assignment check
            delete[] data_;
            data_ = new char[o.size_];
            size_ = o.size_;
            std::memcpy(data_, o.data_, size_);
        }
        return *this;
    }

    // Move constructor
    Buffer(Buffer&& o) noexcept : data_(o.data_), size_(o.size_) {
        o.data_ = nullptr;
        o.size_ = 0;
    }

    // Move assignment
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

**Rule of 0 — tot hon:**
```cpp
class Buffer {
    std::vector<char> data_;  // vector tu quan ly memory
public:
    Buffer(size_t n) : data_(n) {}
    // Khong can viet gi them — compiler sinh dung
};
```

---

### Q3. Constructor co the fail khong? Nen xu ly the nao?

**A:** Constructor **khong co return value**, cach duy nhat bao loi la **throw exception**.

```cpp
class File {
    FILE* f_;
public:
    File(const char* path) {
        f_ = fopen(path, "r");
        if (!f_) throw std::runtime_error("Cannot open file");
        // Neu throw o day, destructor KHONG duoc goi
        // -> khong co resource nao bi leak (chua acquire gi ca)
    }
    ~File() { fclose(f_); }
};
```

**Luu y quan trong:** Neu constructor throw sau khi da cap phat mot so resource, phan da cap phat **phai duoc don sach truoc khi throw** (vi destructor se khong chay).

```cpp
class TwoResources {
    int* a_;
    int* b_;
public:
    TwoResources() {
        a_ = new int(1);
        b_ = new int(2);  // neu day throw -> a_ bi leak
    }
};
// Giai phap: dung unique_ptr
class TwoResources {
    std::unique_ptr<int> a_{new int(1)};
    std::unique_ptr<int> b_{new int(2)};  // neu throw, a_ tu dong duoc giai phong
};
```

---

### Q4. Initializer list vs assignment trong constructor?

**A:** **Luon dung initializer list** khi co the — no goi constructor truc tiep, thay vi default-construct roi assign.

```cpp
class Foo {
    std::string name_;
    int value_;
public:
    // BAD: default-construct name_ roi goi operator=
    Foo(std::string n, int v) {
        name_ = n;    // 2 buoc: default ctor + copy assign
        value_ = v;
    }

    // GOOD: goi copy constructor truc tiep
    Foo(std::string n, int v) : name_(std::move(n)), value_(v) {}
};
```

**Bat buoc phai dung initializer list khi:**
```cpp
class Bar {
    const int id_;        // const member phai init trong initializer list
    int& ref_;            // reference phai init trong initializer list
    Base base_;           // neu Base khong co default ctor
public:
    Bar(int id, int& r) : id_(id), ref_(r), base_(id) {}
};
```

**Thu tu khoi tao:** Theo thu tu **khai bao trong class**, khong phai thu tu trong initializer list — de gay bug.

---

## 2) Inheritance va Virtual

### Q5. `virtual` hoat dong nhu the nao? vtable la gi?

**A:** Khi mot class co it nhat 1 virtual function, compiler tao mot **vtable** (virtual dispatch table) — mot mang cac function pointer.

```
class Animal { virtual void speak(); };
class Dog : public Animal { void speak() override; };
class Cat : public Animal { void speak() override; };

vtable cua Animal: [ &Animal::speak ]
vtable cua Dog:    [ &Dog::speak    ]
vtable cua Cat:    [ &Cat::speak    ]

Moi object co 1 con tro an (vptr) tro vao vtable cua class no.
```

```cpp
Animal* a = new Dog();
a->speak();
// 1. Lay vptr tu *a  (tro vao Dog's vtable)
// 2. Lay function pointer tai offset cua speak()
// 3. Goi Dog::speak()
```

**Chi phi:**
- Moi object: them 8 byte (vptr)
- Moi virtual call: 1 indirection qua vtable (cache miss tiom nang)
- Compiler **khong the inline** virtual call (tru khi devirtualize duoc)

---

### Q6. `override` va `final` dung de lam gi?

**A:** C++11 keywords giup compiler bat loi khi override.

```cpp
class Base {
    virtual void foo(int x);
    virtual void bar();
};

class Derived : public Base {
    void foo(int x) override;  // OK
    void bar(int x) override;  // ERROR: signature khong khop -> compiler bao
    void baz() override;       // ERROR: baz khong ton tai trong Base

    void bar() final;          // final: class con khong override duoc nua
};

class Leaf final : public Derived {};  // Leaf: khong the ke thua nua
```

**Tai sao quan trong:** Neu khong co `override`, viet sai signature se tao ra function **moi** thay vi override — bug am tham.

---

### Q7. Virtual destructor quan trong the nao?

**A:** **Bat buoc** phai co `virtual destructor` khi xoa object qua base pointer. Neu khong, destructor cua derived class se **khong duoc goi** -> resource leak.

```cpp
class Base {
public:
    ~Base() { printf("~Base\n"); }  // NON-virtual
};
class Derived : public Base {
    int* data_ = new int[100];
public:
    ~Derived() { delete[] data_; printf("~Derived\n"); }
};

Base* p = new Derived();
delete p;  // Chi goi ~Base, KHONG goi ~Derived -> leak data_

// FIX:
class Base {
public:
    virtual ~Base() = default;  // virtual
};
```

**Quy tac:**
- Class co bat ky virtual function nao -> them `virtual ~Base() = default;`
- Class duoc dung lam base -> them virtual destructor
- Class `final` co the khong can (khong ai ke thua)

---

### Q8. Pure virtual function va abstract class?

**A:** Pure virtual function la function khong co implementation trong base class, buoc derived class phai implement.

```cpp
class Shape {
public:
    virtual double area() const = 0;   // pure virtual
    virtual void draw() const = 0;     // pure virtual

    // Co the co implementation du la pure virtual (it gap):
    virtual void describe() const = 0;
};
void Shape::describe() const { printf("I am a shape\n"); }

class Circle : public Shape {
    double r_;
public:
    Circle(double r) : r_(r) {}
    double area() const override { return 3.14159 * r_ * r_; }
    void draw() const override { printf("O\n"); }
    void describe() const override {
        Shape::describe();  // goi base implementation
        printf("I am a circle\n");
    }
};

// Shape s;        // ERROR: abstract class
Shape* s = new Circle(5.0);  // OK
```

---

### Q9. Diamond problem la gi? Virtual inheritance giai quyet the nao?

**A:** Diamond problem xay ra khi mot class ke thua tu hai class, ca hai cung ke thua tu mot base chung.

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
b.x = 1;       // ERROR: ambiguous (Left::x hay Right::x?)
b.Left::x = 1; // OK nhung co 2 ban sao x
```

**Giai phap: Virtual inheritance**
```cpp
class Left  : virtual public Base {};
class Right : virtual public Base {};
class Both  : public Left, public Right {};

Both b;
b.x = 1;  // OK: chi co 1 ban sao cua Base
```

**Chi phi:** Virtual inheritance them overhead (vbtable pointer), lam code phuc tap. Thuc te: neu thay minh can diamond inheritance, thuong la dau hieu thiet ke sai.

---

## 3) RAII

### Q10. RAII la gi? Tai sao la pattern quan trong nhat trong C++?

**A:** **RAII (Resource Acquisition Is Initialization)**: lien ket viec cap phat resource voi lifetime cua object. Khi object bi destroy (ra khoi scope, exception, ...), destructor **tu dong** giai phong resource.

```cpp
// KHONG RAII (C style):
void process() {
    FILE* f = fopen("data.txt", "r");
    if (!f) return;                     // leak neu return som
    int* buf = malloc(1024);
    if (!buf) { fclose(f); return; }    // phai nho dong f truoc
    // ... xu ly ...
    if (error) {
        free(buf); fclose(f); return;   // phai lam lai
    }
    free(buf);
    fclose(f);
}

// RAII (C++ style):
void process() {
    auto f = std::fopen("data.txt", "r");
    if (!f) return;
    struct FileGuard {
        FILE* f;
        ~FileGuard() { if(f) fclose(f); }
    } guard{f};

    std::vector<char> buf(1024);        // tu dong giai phong
    // ... xu ly ...
    if (error) return;                  // guard va buf tu dong don sach
}
// Hoac tot hon: dung ifstream, unique_ptr, etc.
```

**RAII cho moi loai resource:**
```cpp
std::unique_ptr<int>  -> heap memory
std::vector<T>        -> heap memory (array)
std::ifstream         -> file handle
std::lock_guard       -> mutex
std::jthread (C++20)  -> thread
```

---

### Q11. `explicit` keyword dung de lam gi?

**A:** Ngan compiler tu dong chuyen doi kieu (implicit conversion) qua constructor.

```cpp
class MyString {
public:
    MyString(int n);          // tao string voi n ky tu rong
    MyString(const char* s);
};

void print(MyString s);

print(42);          // implicitly: print(MyString(42)) -- co y muon vay khong?
print("hello");     // OK, kha ro rang

// FIX voi explicit:
class MyString {
public:
    explicit MyString(int n);  // ngan implicit conversion
    MyString(const char* s);   // char* -> MyString van OK
};

print(42);              // ERROR: no implicit conversion
print(MyString(42));    // OK: explicit
print("hello");         // OK: van cho phep
```

**Quy tac:** Constructor nhan 1 tham so **nen co `explicit`** tru khi thuc su muon implicit conversion (nhu `std::string` nhan `const char*`).

---

## 4) Operator Overloading

### Q12. Khi nao dung member function, khi nao dung free function khi overload operator?

**A:**

| Operator | Cach khuyen dung |
|---|---|
| `=`, `[]`, `()`, `->` | **Phai** la member function |
| Unary `+`, `-`, `++`, `--` | Member function |
| `<<`, `>>` (stream) | **Free function** (voi `friend`) |
| Binary `+`, `-`, `*`, `/` | Free function (de support `commutative`) |
| `==`, `!=`, `<`, `>` | Free function |

```cpp
class Vec2 {
public:
    float x, y;

    // Member: assignment
    Vec2& operator=(const Vec2&) = default;

    // Member: unary
    Vec2 operator-() const { return {-x, -y}; }

    // Free function: binary + (symmetric: a+b, b+a)
    friend Vec2 operator+(Vec2 a, Vec2 b) { return {a.x+b.x, a.y+b.y}; }

    // Free function: stream output
    friend std::ostream& operator<<(std::ostream& os, const Vec2& v) {
        return os << "(" << v.x << "," << v.y << ")";
    }
};
```

---

### Q13. `friend` class/function la gi? Khi nao dung?

**A:** `friend` cho phep mot function hoac class khac **truy cap private/protected members**.

```cpp
class BankAccount {
    double balance_ = 0;
    friend class Auditor;              // class friend
    friend std::ostream& operator<<(std::ostream&, const BankAccount&);  // function friend
};

class Auditor {
public:
    void inspect(const BankAccount& acc) {
        printf("Balance: %f\n", acc.balance_);  // OK
    }
};
```

**Khi nao nen dung:**
- Operator overloading can truy cap internals
- Two closely coupled classes (nhung khong muon dung inheritance)

**Khi nao KHONG nen dung:**
- Tranh su dung qua nhieu — pha vo encapsulation
- Neu thay can nhieu `friend`, thuong la dau hieu thiet ke lai

---

## 5) Cau hoi thuc te senior

### Q14. Phan biet `public`, `protected`, `private` inheritance?

**A:**

```cpp
class Base { public: int x; protected: int y; private: int z; };

class PubDerived  : public    Base {};  // x=public, y=protected, z=khong truy cap
class ProtDerived : protected Base {};  // x=protected, y=protected, z=khong truy cap
class PrivDerived : private   Base {};  // x=private, y=private, z=khong truy cap
```

**Trong thuc te:** `public` inheritance la "is-a" (Dog is-a Animal). `private` inheritance la "implemented-in-terms-of" (it gap, thuong dung composition thay the).

---

### Q15. Composition vs Inheritance — khi nao dung cai nao?

**A:** **"Prefer composition over inheritance"** — nguyen tac quan trong.

**Dung inheritance khi:**
- Co quan he "is-a" thuc su (Dog is an Animal)
- Can polymorphism qua base pointer
- Override behavior can thiet

**Dung composition khi:**
- Co quan he "has-a" (Car has an Engine)
- Chi muon reuse implementation, khong phai interface
- Tranh tight coupling

```cpp
// BAD: inheritance chi de reuse
class Stack : public std::vector<int> {  // Stack la vector? KHONG!
    // Lo ra tat ca vector API (push_back, erase, ...)
};

// GOOD: composition
class Stack {
    std::vector<int> data_;  // Stack co vector de luu tru
public:
    void push(int x) { data_.push_back(x); }
    void pop()       { data_.pop_back(); }
    int  top() const { return data_.back(); }
};
```

---

### Q16. CRTP (Curiously Recurring Template Pattern) la gi?

**A:** CRTP la ky thuat dung template de thuc hien **static polymorphism** — polymorphism tai compile time, tranh overhead cua virtual dispatch.

```cpp
// Virtual (runtime polymorphism):
struct Base { virtual void foo() = 0; };
struct Derived : Base { void foo() override { ... } };
Base* p = new Derived();
p->foo();  // vtable lookup

// CRTP (compile-time polymorphism):
template<typename Derived>
struct Base {
    void interface() {
        static_cast<Derived*>(this)->implementation();  // no virtual call
    }
};
struct Concrete : Base<Concrete> {
    void implementation() { printf("Concrete\n"); }
};

Concrete c;
c.interface();  // goi truc tiep, compiler co the inline
```

**Ung dung thuc te cua CRTP:**
```cpp
// 1. Enable shared_from_this
class Foo : public std::enable_shared_from_this<Foo> { ... };

// 2. Comparable mixin
template<typename T>
struct Comparable {
    bool operator!=(const T& o) const { return !(static_cast<const T&>(*this) == o); }
    bool operator> (const T& o) const { return o < static_cast<const T&>(*this); }
    bool operator<=(const T& o) const { return !(o < static_cast<const T&>(*this)); }
    bool operator>=(const T& o) const { return !(static_cast<const T&>(*this) < o); }
};
struct Point : Comparable<Point> {
    int x, y;
    bool operator==(const Point& o) const { return x==o.x && y==o.y; }
    bool operator< (const Point& o) const { return std::tie(x,y) < std::tie(o.x,o.y); }
    // != > <= >= tu dong co tu Comparable
};
```

---

## Flash card

| Cau hoi | Tra loi nhanh |
|---|---|
| Rule of 5 gom gi? | dtor, copy ctor, copy=, move ctor, move= |
| virtual destructor khi nao? | Khi co bat ky virtual function nao |
| Pure virtual = ? | `= 0`, class tro thanh abstract |
| Diamond problem giai phap? | `virtual` inheritance |
| RAII la gi? | Resource = object lifetime, dtor tu giai phong |
| `explicit` constructor? | Ngan implicit conversion |
| `override` keyword? | Bat compiler check signature khi override |
| Composition vs Inheritance? | Prefer composition, dung inheritance cho "is-a" |
| CRTP dung de gi? | Static polymorphism, khong co vtable overhead |
| `friend` khi nao? | Operator overloading, closely coupled classes |
