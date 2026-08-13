# 06 - Modern C++ (C++11/14/17/20)

---

## 1) C++11 — Nen Tang

### Q1. Rvalue reference va move semantics la gi?

**A:** **Rvalue** la gia tri tam thoi, khong co ten, khong the lay dia chi. **Rvalue reference** (`T&&`) cho phep "cuop" resource cua no thay vi copy.

```cpp
std::string s1 = "hello";
std::string s2 = s1;              // COPY: cap phat bo nho moi, copy noi dung
std::string s3 = std::move(s1);   // MOVE: lay buffer cua s1, s1 bay gio rong (valid nhung unspecified)

// Move constructor (thuc hien "cuop"):
class MyString {
    char* data_;
public:
    // Copy: cap phat moi + copy noi dung — O(n)
    MyString(const MyString& o) : data_(new char[strlen(o.data_)+1]) {
        strcpy(data_, o.data_);
    }
    // Move: chi copy pointer — O(1)
    MyString(MyString&& o) noexcept : data_(o.data_) {
        o.data_ = nullptr;  // "steal" resource
    }
};
```

**Khi nao move duoc goi tu dong:**
```cpp
// 1. Return local variable (NRVO hoac move)
MyString create() {
    MyString s = "hello";
    return s;  // move (hoac NRVO — Named Return Value Optimization)
}

// 2. Truyen rvalue
func(MyString("temp"));  // arg la rvalue -> move constructor

// 3. std::move explicit
MyString a("hello");
MyString b(std::move(a));  // explicit move
```

---

### Q2. `auto` va type deduction hoat dong the nao?

**A:** `auto` bao compiler **suy dien kieu** tu dau vao, giong template type deduction.

```cpp
auto x = 42;          // int
auto y = 3.14;        // double
auto z = "hello";     // const char*
auto s = std::string("hi");  // std::string

// QUAN TRONG: auto bo const va reference
const int ci = 42;
auto a = ci;          // int (khong phai const int!)
auto& b = ci;         // const int& (giu ref)
const auto c = ci;    // const int

int i = 0;
auto& r = i;          // int&
auto  v = i;          // int (copy)

// decltype: lay kieu cua bieu thuc ma khong tinh toan
decltype(i)   d1;     // int
decltype(ci)  d2;     // const int
decltype((i)) d3;     // int& (them () -> lvalue ref)
```

**`auto` trong ham (C++14 trailing return type):**
```cpp
auto add(int a, int b) -> int { return a + b; }  // trailing return type
auto add(int a, int b) { return a + b; }          // C++14: suy dien return type
```

---

### Q3. Lambda expression la gi? Capture modes?

**A:** Lambda la **anonymous function object** co the capture bien tu scope xung quanh.

```cpp
// Cu phap: [capture](params) -> return_type { body }
auto add = [](int a, int b) { return a + b; };
add(3, 4);  // 7

// Capture modes:
int x = 10, y = 20;

auto f1 = [x]() { return x; };       // capture x by value (copy)
auto f2 = [&x]() { return x; };      // capture x by reference
auto f3 = [=]() { return x + y; };   // capture all by value
auto f4 = [&]() { return x + y; };   // capture all by reference
auto f5 = [=, &x]() { return x+y; }; // all by value, ngoai tru x by ref
auto f6 = [x, &y]() { return x+y; }; // x by value, y by ref

x = 100;
f1();  // 10 (da copy luc tao lambda)
f2();  // 100 (reference, lay gia tri hien tai)
```

**Mutable lambda:**
```cpp
int count = 0;
auto inc = [count]() mutable {  // can 'mutable' de thay doi captured copy
    count++;
    return count;
};
inc();  // 1, nhung count ben ngoai van = 0
```

**Generic lambda (C++14):**
```cpp
auto print = [](auto x) { std::cout << x << "\n"; };
print(42);
print("hello");
print(3.14);
```

---

### Q4. `nullptr` va tai sao khong dung `NULL`?

**A:** `nullptr` la **keyword co kieu `std::nullptr_t`** — type-safe hon `NULL` (la macro = 0).

```cpp
// Van de voi NULL:
void f(int x)   { printf("int\n"); }
void f(int* p)  { printf("ptr\n"); }

f(NULL);    // Goi f(int)! Vi NULL = 0 (int literal)
f(nullptr); // Goi f(int*): dung y dinh

// nullptr co the assign cho bat ky pointer type:
int*    p1 = nullptr;
char*   p2 = nullptr;
Foo*    p3 = nullptr;

// nullptr khong chuyen duoc sang int:
int x = nullptr;   // ERROR
int x = NULL;      // OK (nhung sai y dinh)
```

---

### Q5. Uniform initialization (`{}`) la gi? Uu va nhuoc diem?

**A:** `{}` (brace initialization) la cach khoi tao thong nhat cho moi kieu trong C++11.

```cpp
int x{42};
double d{3.14};
std::vector<int> v{1, 2, 3, 4};
std::map<int,std::string> m{{1,"one"}, {2,"two"}};

struct Point { int x, y; };
Point p{10, 20};  // aggregate init

// UU DIEM: ngan narrowing conversion
int a{3.14};    // ERROR: narrowing (mat phan thap phan)
int b = 3.14;   // OK (implicit conversion, co the mat data)
int c(3.14);    // OK (implicit conversion)
```

**Nhuoc diem — `initializer_list` co the "chiem" constructor:**
```cpp
std::vector<int> v1(10, 5);   // 10 phan tu, moi cai la 5
std::vector<int> v2{10, 5};   // 2 phan tu: 10 va 5!
// {} uu tien initializer_list constructor neu co
```

---

## 2) C++11 — Smart Pointers va Move

### Q6. `std::move` co thuc su "move" gi khong?

**A:** **Khong.** `std::move` chi la **cast sang rvalue reference** — no khong move gi ca. Viec move thuc su xay ra khi move constructor/operator= duoc goi.

```cpp
std::string s = "hello";
std::string t = std::move(s);  // std::move(s) -> chi cast thanh string&&
                                // move constructor cua string moi thuc su move

// Sau std::move, s van la valid object nhung trong (unspecified state)
s.empty();    // true
s.size();     // 0
s = "world";  // OK: co the dung lai sau khi da reset
```

---

## 3) C++17 — Tien Ich Moi

### Q7. Structured bindings la gi?

**A:** C++17 cho phep **unpack** struct, pair, tuple, array vao nhieu bien.

```cpp
// pair
std::pair<int, std::string> p = {42, "hello"};
auto [id, name] = p;  // id = 42, name = "hello"

// map iteration (truoc C++17: verbose lam)
std::map<std::string, int> scores = {{"Alice", 95}, {"Bob", 87}};
for (auto& [name, score] : scores) {
    printf("%s: %d\n", name.c_str(), score);
}

// struct
struct Point { int x, y, z; };
Point pt{1, 2, 3};
auto [x, y, z] = pt;  // x=1, y=2, z=3

// Voi reference:
auto& [rx, ry, rz] = pt;
rx = 100;  // thay doi pt.x
```

---

### Q8. `if constexpr` la gi va dung khi nao?

**A:** `if constexpr` la **compile-time if** — nhanh bi loai bo tai compile time, khong sinh code cho nhanh sai.

```cpp
template<typename T>
std::string to_str(T val) {
    if constexpr (std::is_same_v<T, bool>) {
        return val ? "true" : "false";
    } else if constexpr (std::is_arithmetic_v<T>) {
        return std::to_string(val);
    } else {
        return std::string(val);  // assume string-like
    }
    // Nhanh khong duoc chon se khong compile (khong can phai valid cho moi T)
}

// So sanh voi runtime if:
template<typename T>
void bad(T val) {
    if (std::is_same_v<T, bool>) {
        // Code trong day van phai compile hop le voi moi T!
        // Neu T = int, std::to_string(val) OK nhung val ? "t" : "f" cung OK
    }
}
```

---

### Q9. `std::filesystem` (C++17)?

**A:** API chuan de lam viec voi file system, thay the platform-specific code.

```cpp
#include <filesystem>
namespace fs = std::filesystem;

// Kiem tra ton tai
fs::path p = "/home/user/file.txt";
fs::exists(p);         // bool
fs::is_directory(p);   // bool

// Tao/xoa
fs::create_directories("/tmp/a/b/c");
fs::remove("/tmp/file.txt");
fs::remove_all("/tmp/folder");  // xoa recursive

// Copy
fs::copy("src.txt", "dst.txt");
fs::copy("src_dir", "dst_dir", fs::copy_options::recursive);

// Iterate directory
for (auto& entry : fs::directory_iterator("/tmp")) {
    printf("%s\n", entry.path().c_str());
}

// Path operations
fs::path p = "/home/user/doc/file.txt";
p.stem();       // "file"
p.extension();  // ".txt"
p.parent_path();// "/home/user/doc"
p.filename();   // "file.txt"
```

---

## 4) C++20 — Tinh Nang Lon

### Q10. Concepts trong C++20 la gi?

**A:** Da duoc mo ta trong file 04-cpp-templates.md (Q10). Tham khao lai o do.

---

### Q11. Coroutines trong C++20 la gi?

**A:** Coroutines la ham co the **tam dung** (`co_await`, `co_yield`) va **tiep tuc** sau do — khong block thread.

```cpp
#include <coroutine>

// Generator: yield tung gia tri mot
Generator<int> fibonacci() {
    int a = 0, b = 1;
    while (true) {
        co_yield a;       // tam dung, tra gia tri a cho caller
        auto next = a + b;
        a = b;
        b = next;
    }
}

for (int x : fibonacci() | std::views::take(10)) {
    printf("%d ", x);  // 0 1 1 2 3 5 8 13 21 34
}
```

**Async coroutine (voi framework nhu Asio, cppcoro):**
```cpp
Task<std::string> fetch_data(std::string url) {
    auto response = co_await http_get(url);  // khong block thread
    co_return response.body;
}
```

---

### Q12. Ranges (C++20) la gi?

**A:** Ranges cung cap **lazy, composable** operations tren sequences.

```cpp
#include <ranges>
#include <algorithm>

std::vector<int> v = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

// Pipe-based composition (lazy, khong tao trung gian)
auto result = v
    | std::views::filter([](int x) { return x % 2 == 0; })  // loc so chan
    | std::views::transform([](int x) { return x * x; })     // binh phuong
    | std::views::take(3);                                    // lay 3 phan tu dau

for (int x : result) printf("%d ", x);  // 4 16 36

// Range algorithms (khong can .begin() .end())
std::ranges::sort(v);
std::ranges::find(v, 5);
```

---

### Q13. `std::format` (C++20) la gi?

**A:** Type-safe string formatting, giong Python f-string, thay the `printf` va `sprintf`.

```cpp
#include <format>

std::string s = std::format("Hello, {}!", "world");
std::string s2 = std::format("Pi = {:.2f}", 3.14159);  // "Pi = 3.14"
std::string s3 = std::format("{0} {1} {0}", "a", "b"); // "a b a"

// So sanh:
// printf: khong type-safe, format string la runtime string
// std::format: type-safe, kiem tra tai compile time
```

---

## 5) Lambda Nang Cao

### Q14. `std::function` la gi? Chi phi?

**A:** `std::function<Signature>` la **type-erased callable wrapper** — co the wrap lambda, function pointer, functor.

```cpp
// Co the luu bat ky callable co cung signature
std::function<int(int, int)> f;

f = [](int a, int b) { return a + b; };    // lambda
f = std::plus<int>{};                       // functor
f = my_add_func;                            // function pointer

// Chi phi:
// - Type erasure: dynamic dispatch (nhu virtual call)
// - Heap allocation neu lambda capture qua lon
// - Cham hon goi truc tiep lambda/function pointer

// Thay the nhanh hon:
// 1. Template (compile time, inline duoc)
template<typename F> void use(F&& f) { f(1, 2); }

// 2. Function pointer (neu khong can capture)
using FuncPtr = int(*)(int, int);
```

---

## Flash card

| Cau hoi | Tra loi nhanh |
|---|---|
| `std::move` co move khong? | Khong, chi cast sang rvalue ref |
| Lambda `[=]` vs `[&]`? | `[=]` copy, `[&]` reference |
| `nullptr` vs `NULL`? | nullptr type-safe (nullptr_t), NULL = 0 (int) |
| `{}` init nhuoc diem? | Uu tien initializer_list, co the chon sai ctor |
| `if constexpr` vs runtime if? | Compile-time, nhanh sai khong sinh code |
| Structured binding? | `auto [a,b] = pair;` unpack |
| `auto` bo gi? | Bo const va reference (can them `const auto&`) |
| Coroutine keyword? | `co_await`, `co_yield`, `co_return` |
| `string_view` nguy hiem khi? | Tra ve reference toi local string |
| `std::format` tot hon printf vi? | Type-safe, kiem tra compile time |
