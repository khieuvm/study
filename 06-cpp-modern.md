# 06 - Modern C++ (C++11/14/17/20) — Bilingual VI/EN

---

## 1) C++11 — Nên Tăng

### Q1. Rvalue reference và move semantics là gì?

**A:**
- EN: An **rvalue** is a temporary with no name. An **rvalue reference** (`T&&`) allows "stealing" its resources instead of copying — O(1) vs O(n). The move constructor takes ownership of the source's internal buffer and leaves the source in a valid-but-unspecified state.
- VI: **Rvalue** là giá trị tạm thời không có tên. **Rvalue reference** (`T&&`) cho phép "cướp" resource thay vì copy — O(1) thay vì O(n). Move constructor lấy ownership buffer nội bộ và để source o trang thai valid-but-unspecified.

```cpp
std::string s1 = "hello";
std::string s2 = s1;              // COPY: new allocation + copy content
std::string s3 = std::move(s1);   // MOVE: steal s1's buffer, s1 now empty

class MyString {
    char* data_;
public:
    MyString(const MyString& o) : data_(new char[strlen(o.data_)+1]) {
        strcpy(data_, o.data_);                // Copy: O(n)
    }
    MyString(MyString&& o) noexcept : data_(o.data_) {
        o.data_ = nullptr;                     // Move: O(1)
    }
};
```

- EN: Move is triggered automatically for: returned locals (NRVO or move), rvalue arguments, and explicit `std::move`.
- VI: Move tự động xảy ra khi: return local (NRVO hoặc move), argument là rvalue, và `std::move` tường minh.

Follow-up (EN): What happens if a move constructor is not `noexcept`?

---

### Q2. `auto` và type deduction hoạt động thế nào?

**A:**
- EN: `auto` tells the compiler to **deduce the type** from the initializer, following the same rules as template type deduction. Important: `auto` drops `const` and references by default — use `auto&`, `const auto&`, or `auto&&` to preserve them.
- VI: `auto` báo compiler **suy diễn kiểu** từ biểu thức khởi tạo, theo cùng quy tắc như template type deduction. Quan trọng: `auto` bỏ `const` và reference mặc định — dùng `auto&`, `const auto&`, hoặc `auto&&` để giữ chung.

```cpp
auto x = 42;           // int
auto y = 3.14;         // double
const int ci = 42;
auto a = ci;           // int (drops const!)
auto& b = ci;          // const int& (preserves)
const auto c = ci;     // const int

// decltype: get type of expression without evaluating
decltype(x)    d1;     // int
decltype((x))  d2;     // int& (parenthesized lvalue -> reference)
```

Follow-up (EN): What is the difference between `auto` and `decltype(auto)`?

---

### Q3. Lambda expression là gì? Capture modes?

**A:**
- EN: A lambda is an **anonymous function object** that can capture variables from its enclosing scope. Capture modes: `[x]` by value (copy), `[&x]` by reference, `[=]` all by value, `[&]` all by reference. Use `mutable` keyword to modify captured copies.
- VI: Lambda là **anonymous function object** có thể capture biến từ scope bao quanh. Capture mode: `[x]` by value (copy), `[&x]` by reference, `[=]` tất cả by value, `[&]` tất cả by reference. Dùng `mutable` để thay đổi captured copy.

```cpp
int x = 10, y = 20;
auto f1 = [x]()  { return x; };       // capture by value
auto f2 = [&x]() { return x; };       // capture by reference
auto f3 = [=]()  { return x + y; };   // all by value
auto f4 = [&]()  { return x + y; };   // all by reference
auto f5 = [=, &x]() { return x+y; };  // all by value except x by ref

// Mutable: modify captured copy
int count = 0;
auto inc = [count]() mutable { return ++count; };
inc();  // returns 1, but outer count still 0

// Generic lambda (C++14)
auto print = [](auto x) { std::cout << x << "\n"; };
```

Follow-up (EN): What is a lambda's closure type and how does the compiler implement it?

---

### Q4. `nullptr` và tại sao không dùng `NULL`?

**A:**
- EN: `nullptr` is a keyword of type `std::nullptr_t` — it's type-safe for pointer contexts. `NULL` is a macro that expands to `0` (an integer), causing ambiguity in overload resolution.
- VI: `nullptr` là keyword kiểu `std::nullptr_t` — type-safe cho pointer. `NULL` là macro = `0` (integer), gây nhầm lẫn trong overload resolution.

```cpp
void f(int x)   { printf("int\n"); }
void f(int* p)  { printf("ptr\n"); }

f(NULL);    // calls f(int)!  NULL = 0 = int literal
f(nullptr); // calls f(int*): correct intent
```

Follow-up (EN): Can `nullptr` be implicitly converted to `bool`? (Yes — it converts to `false`.)

---

### Q5. Uniform initialization (`{}`) là gì? Uu và nhược điểm?

**A:**
- EN: Brace initialization `{}` works for all types and **prevents narrowing conversions** (e.g., `int x{3.14}` is an error). Downside: when a constructor accepts `initializer_list`, braces prefer it — causing surprising behavior like `vector<int>{10, 5}` creating 2 elements instead of 10 copies of 5.
- VI: Khởi tạo bằng `{}` hoạt động với mọi kiểu và **ngăn narrowing conversion** (VD: `int x{3.14}` là lỗi). Nhược điểm: khi constructor nhận `initializer_list`, `{}` ưu tiên no — gây bắt ngo như `vector<int>{10, 5}` tạo 2 phần tử thay vì 10 bản sao của 5.

```cpp
int a{3.14};    // ERROR: narrowing
int b = 3.14;   // OK (silent data loss)

std::vector<int> v1(10, 5);   // 10 elements, each = 5
std::vector<int> v2{10, 5};   // 2 elements: 10 and 5!
```

Follow-up (EN): When should you use `()` vs `{}` initialization?

---

## 2) C++11 — Smart Pointers và Move

### Q6. `std::move` có thực sự "move" gì không?

**A:**
- EN: **No.** `std::move` is just a **cast to rvalue reference** — it doesn't move anything. The actual move happens when a move constructor or move assignment operator receives that rvalue reference. After the move, the source is in a valid-but-unspecified state.
- VI: **Không.** `std::move` chỉ là **cast sang rvalue reference** — không move gì cả. Việc move thực sự xảy ra khi move constructor hoặc move assignment operator nhận rvalue reference do. Sau move, source o trang thai valid-but-unspecified.

```cpp
std::string s = "hello";
std::string t = std::move(s);  // std::move = cast only; string's move ctor does the work
// s is now valid but empty
s = "world";  // OK: can reuse after reassignment
```

Follow-up (EN): Does `std::move` on a `const` object actually move? (No — a const rvalue matches const& overload, số it copies.)

---

## 3) C++17 — Tien Ich Mọi

### Q7. Structured bindings là gì?

**A:**
- EN: C++17 structured bindings allow **unpacking** structs, pairs, tuples, and arrays into named variables in a single declaration. Works with `auto`, `auto&`, and `const auto&`.
- VI: C++17 structured bindings cho phép **unpack** struct, pair, tuple, và array vào các biến có tên trong 1 khai báo. Hoạt động với `auto`, `auto&`, và `const auto&`.

```cpp
// Pair
auto [id, name] = std::pair{42, std::string("hello")};

// Map iteration
std::map<std::string, int> scores = {{"Alice", 95}, {"Bob", 87}};
for (auto& [name, score] : scores) {
    printf("%s: %d\n", name.c_str(), score);
}

// Struct
struct Point { int x, y, z; };
auto& [rx, ry, rz] = pt;  // references to pt's members
```

Follow-up (EN): Can structured bindings be used with classes that have private members?

---

### Q8. `if constexpr` là gì và dùng khi nào?

**A:**
- EN: `if constexpr` is a **compile-time if** — the false branch is completely discarded and doesn't need to be valid for the given template type. Unlike runtime `if`, it can branch on type traits without generating invalid code paths.
- VI: `if constexpr` là **compile-time if** — nhánh sai bị bỏ hoàn toàn và không cần hợp lệ cho kiểu template đang dùng. Khác runtime `if`, nó có thể chia nhanh theo type traits mà không sinh code không hợp lệ.

```cpp
template<typename T>
std::string to_str(T val) {
    if constexpr (std::is_same_v<T, bool>)
        return val ? "true" : "false";
    else if constexpr (std::is_arithmetic_v<T>)
        return std::to_string(val);
    else
        return std::string(val);
    // False branches are NOT compiled — don't need to be valid for T
}
```

Follow-up (EN): Can `if constexpr` be used outside of templates?

---

### Q9. `std::filesystem` (C++17)?

**A:**
- EN: A standard cross-platform API for file system operations: checking existence, creating/removing directories, copying files, iterating directories, and path manipulation. Replaces platform-specific code (`stat`, `opendir`, `FindFirstFile`).
- VI: API chuẩn đã nền tảng cho thao tác file system: kiểm tra tồn tại, tạo/xóa thư mục, copy file, duyệt thư mục, và xử lý đường dẫn. Thay thể code platform-specific (`stat`, `opendir`, `FindFirstFile`).

```cpp
namespace fs = std::filesystem;

fs::exists("/tmp/file.txt");
fs::create_directories("/tmp/a/b/c");
fs::copy("src.txt", "dst.txt");
fs::remove_all("/tmp/folder");

for (auto& entry : fs::directory_iterator("/tmp"))
    printf("%s\n", entry.path().c_str());

fs::path p = "/home/user/file.txt";
p.stem();         // "file"
p.extension();    // ".txt"
p.parent_path();  // "/home/user"
```

Follow-up (EN): What are the error handling options for `std::filesystem` functions?

---

## 4) C++20 — Tính năng Lớn

### Q10. Concepts trong C++20 là gì?

**A:**
- EN: See 04-cpp-templates.md Q10 for detailed coverage. Concepts are **named constraints** on template parameters with clean syntax and clear error messages.
- VI: Xem 04-cpp-templates.md Q10 để có nội dung chi tiết. Concepts là **named constraints** cho template parameter với cú pháp sạch và lỗi báo rõ ràng.

---

### Q11. Coroutines trong C++20 là gì?

**A:**
- EN: Coroutines are functions that can **suspend** (`co_await`, `co_yield`) and **resume** later without blocking the thread. They enable lazy generators, async I/O, and cooperative multitasking. C++20 provides low-level machinery; frameworks like cppcoro provide high-level abstractions.
- VI: Coroutines là hàm có thể **tạm dùng** (`có_await`, `có_yield`) và **tiếp tục** sau do mà không block thread. Cho phép lazy generator, async I/O, và cooperative multitasking. C++20 cung cấp cơ chế muc thấp; framework như cppcoro cung cấp abstraction muc cao.

```cpp
// Generator: yields values one at a time
Generator<int> fibonacci() {
    int a = 0, b = 1;
    while (true) {
        co_yield a;
        auto next = a + b;
        a = b; b = next;
    }
}

// Async coroutine (with framework)
Task<std::string> fetch_data(std::string url) {
    auto response = co_await http_get(url);  // non-blocking
    co_return response.body;
}
```

Follow-up (EN): What is the difference between stackful and stackless coroutines?

---

### Q12. Ranges (C++20) là gì?

**A:**
- EN: Ranges provide **lazy, composable** pipeline operations on sequences via the pipe (`|`) operator. Views are lazy — nó intermediate containers are created. Range algorithms accept containers directly (no `.begin()/.end()` needed).
- VI: Ranges cung cấp **lazy, composable** pipeline operations trên sequence qua toan từ pipe (`|`). View là lazy — không tạo container trung gian. Range algorithms nhận container trực tiếp (không cần `.begin()/.end()`).

```cpp
std::vector<int> v = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

auto result = v
    | std::views::filter([](int x) { return x % 2 == 0; })
    | std::views::transform([](int x) { return x * x; })
    | std::views::take(3);

for (int x : result) printf("%d ", x);  // 4 16 36

// Range algorithms
std::ranges::sort(v);
std::ranges::find(v, 5);
```

Follow-up (EN): What is the difference between a view and a container in the Ranges library?

---

### Q13. `std::format` (C++20) là gì?

**A:**
- EN: Type-safe string formatting, similar to Python f-strings. Unlike `printf`, format strings are checked at compile time, and it works with user-defined types via specialization.
- VI: Type-safe string formatting, giống Python f-string. Khác `printf`, format string được kiểm tra tại compile time, và hoạt động với user-defined types qua specialization.

```cpp
std::string s = std::format("Hello, {}!", "world");
std::string s2 = std::format("Pi = {:.2f}", 3.14159);   // "Pi = 3.14"
std::string s3 = std::format("{0} {1} {0}", "a", "b");  // "a b a"
```

Follow-up (EN): How do you make `std::format` work with a custom class?

---

## 5) Lambda Nâng cao

### Q14. `std::function` là gì? Chi phí?

**A:**
- EN: `std::function<Sig>` is a **type-erased callable wrapper** — can store any callable matching the signature (lambda, function pointer, functor). Cost: dynamic dispatch (like virtual call) + possible heap allocation for large captures. Prefer templates for performance-critical code.
- VI: `std::function<Sig>` là **type-erased callable wrapper** — lưu được bất kỳ callable khớp signature (lambda, function pointer, functor). Chi phí: dynamic dispatch (như virtual call) + có thể heap allocation cho capture lớn. Ưu tiên template cho code cần performance.

```cpp
std::function<int(int, int)> f;
f = [](int a, int b) { return a + b; };   // lambda
f = std::plus<int>{};                       // functor
f = my_add_func;                            // function pointer
```

- EN: Faster alternatives: templates (compile-time, inlineable), function pointers (no capture), `std::move_only_function` (C++23, avoids copy).
- VI: Thay thể nhanh hơn: template (compile-time, inline được), function pointer (không capture), `std::move_only_function` (C++23, tránh copy).

Follow-up (EN): What is small buffer optimization (SBO) in `std::function`?

---

## Flash card

| Question / Câu hỏi | Quick answer / Trả lỗi nhanh |
|---|---|
| `std::move` actually moves? | No — just casts to rvalue ref |
| Lambda `[=]` vs `[&]`? | `[=]` copies all; `[&]` references all |
| `nullptr` vs `NULL`? | nullptr is type-safe (nullptr_t); NULL = 0 (int) |
| `{}` init drawback? | Prefers initializer_list ctor — may pick wrong one |
| `if constexpr` vs runtime if? | Compile-time; false branch not compiled |
| Structured binding? | `auto [a,b] = pair;` — unpack into named vars |
| `auto` drops what? | Drops const and reference (use `auto&` to keep) |
| Coroutine keywords? | `có_await`, `có_yield`, `có_return` |
| Ranges advantage? | Lazy composition, nó intermediate containers |
| `std::function` cost? | Type erasure + dynamic dispatch + possible heap alloc |
