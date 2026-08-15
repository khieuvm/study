# 03 - Modern C++ (11/14/17/20/23) — Bilingual VI/EN

Tổng hợp tính năng Modern C++ quan trọng cho phỏng vấn Senior.

---

## 1) C++11/14 Cốt lõi

### Q1. `auto` dùng sao cho đúng?

**A:**
- EN: Use `auto` to avoid type repetition and iterator verbosity. Avoid when it obscures the type in public APIs. Remember: `auto` drops `const` and references by default — use `const auto&` or `auto&&` to preserve them.
- VI: Dùng `auto` để tránh lặp type và iterator dài dòng. Tránh khi nó làm mờ type trong public API. Lưu ý: `auto` bỏ `const` và reference mặc định — dùng `const auto&` hoặc `auto&&` để giữ.

```cpp
auto it = map.find(key);         // OK: avoids verbose iterator type
const auto& ref = container[0];  // OK: preserves const ref
auto x = expensive_obj;          // careful: copies!
```

Follow-up (EN): What is the difference between `auto` and `decltype(auto)` for return types?

---

### Q2. `decltype(auto)` khi nào cần?

**A:**
- EN: `decltype(auto)` preserves the exact type and value category of the expression, including references and const. Use for perfect-forwarding return types in generic code.
- VI: `decltype(auto)` giữ nguyên kiểu và value category của biểu thức, bao gồm reference và const. Dùng cho return type trong generic code cần perfect-forwarding.

```cpp
template<typename F, typename... Args>
decltype(auto) call(F&& f, Args&&... args) {
    return std::forward<F>(f)(std::forward<Args>(args)...);
    // If f returns int& → decltype(auto) = int&
    // If f returns int  → decltype(auto) = int
}
```

Follow-up (EN): What does `decltype((x))` return vs `decltype(x)`? (Extra parens → reference.)

---

### Q3. Lambda capture `[=]` và `[&]` có rủi ro gì?

**A:**
- EN: `[=]` copies all used variables — may silently capture `this` (dangling if object destroyed), or copy expensive objects. `[&]` captures by reference — dangling if lambda outlives captured scope (e.g., returned or stored). Prefer explicit captures: `[x]`, `[&x]`, `[this]`, `[*this]`.
- VI: `[=]` copy tất cả biến dùng — có thể bắt `this` âm thầm (dangling nếu object bị hủy), hoặc copy object nặng. `[&]` capture bằng reference — dangling nếu lambda sống lâu hơn scope. Ưu tiên capture tường minh: `[x]`, `[&x]`, `[this]`, `[*this]`.

```cpp
auto make_lambda() {
    std::string s = "hello";
    return [&s]() { return s; };  // BUG: s destroyed, lambda dangles
    return [s]() { return s; };   // OK: s copied into lambda
}
```

Follow-up (EN): What does `[*this]` capture (C++17)?

---

## 2) C++17 Phải biết

### Q4. `std::optional` dùng khi nào?

**A:**
- EN: When a function may legitimately have no result — replaces nullable pointers, sentinel values (`-1`, `""`) and out-parameters. Accessing empty optional via `*` is UB; `.value()` throws `bad_optional_access`.
- VI: Khi hàm có thể không có kết quả hợp lệ — thay thế nullable pointer, giá trị sentinel (`-1`, `""`) và out-parameter. Truy cập optional rỗng bằng `*` là UB; `.value()` throw `bad_optional_access`.

```cpp
std::optional<User> find_user(int id) {
    if (auto it = db.find(id); it != db.end()) return *it;
    return std::nullopt;
}
auto user = find_user(42);
if (user) process(*user);
int age = user.value_or(default_user).age;
```

Follow-up (EN): How does `std::optional` differ from a pointer for representing "no value"?

---

### Q5. `std::variant` và `std::visit`?

**A:**
- EN: `std::variant<A,B,C>` is a type-safe tagged union — knows which type is active, calls destructors correctly. Access via `std::get<T>` (throws on wrong type) or `std::get_if<T>` (returns nullptr). `std::visit` dispatches a visitor to the active type.
- VI: `std::variant<A,B,C>` là tagged union type-safe — biết kiểu nào đang active, gọi destructor đúng. Truy cập qua `std::get<T>` (throw nếu sai kiểu) hoặc `std::get_if<T>` (trả nullptr). `std::visit` dispatch visitor tới kiểu active.

```cpp
using Value = std::variant<int, double, std::string>;
Value v = "hello";

std::visit([](auto&& arg) {
    using T = std::decay_t<decltype(arg)>;
    if constexpr (std::is_same_v<T, int>) printf("int\n");
    else if constexpr (std::is_same_v<T, std::string>) printf("str\n");
}, v);
```

Follow-up (EN): What is `std::monostate` and when is it needed with variant?

---

### Q6. `std::string_view` — lợi ích và bẫy?

**A:**
- EN: Non-owning, non-allocating reference to a character sequence — avoids copies when passing strings. **Trap**: never return a `string_view` to a local `std::string` — it will dangle. Never store `string_view` with longer lifetime than the source.
- VI: Non-owning, không allocate, reference tới chuỗi ký tự — tránh copy khi truyền string. **Bẫy**: không bao giờ trả `string_view` tới local `std::string` — sẽ dangling. Không lưu `string_view` có lifetime dài hơn source.

```cpp
void process(std::string_view sv);  // no copy: accepts string, char*, sv
process("hello");          // no allocation
process(some_string);      // no copy

// DANGER:
std::string_view bad() {
    std::string s = "temp";
    return s;  // dangling!
}
```

Follow-up (EN): When should you prefer `const std::string&` over `std::string_view`?

---

### Q7. Structured binding có copy không?

**A:**
- EN: Depends on how you declare: `auto [a,b]` copies/moves; `auto& [a,b]` binds by reference; `const auto& [a,b]` binds by const reference. Same rules as regular `auto` deduction.
- VI: Tùy cách khai báo: `auto [a,b]` copy/move; `auto& [a,b]` bind bằng reference; `const auto& [a,b]` bind bằng const reference. Cùng quy tắc như `auto` thông thường.

```cpp
std::map<std::string, int> scores;
for (auto& [name, score] : scores) {   // reference: no copy
    score += 10;                        // modifies map
}
for (const auto& [name, score] : scores) {  // const ref: read-only
    printf("%s: %d\n", name.c_str(), score);
}
```

Follow-up (EN): Can structured bindings be used with private members?

---

## 3) C++20

### Q8. Concept dùng để làm gì?

**A:**
- EN: Concepts are named constraints on template parameters. They produce readable error messages (instead of pages of template errors), serve as documentation, and enable constrained overload resolution.
- VI: Concepts là named constraints cho template parameter. Tạo lỗi biên dịch dễ đọc (thay vì hàng trang lỗi template), làm tài liệu, và cho phép constrained overload resolution.

```cpp
template<typename T>
concept Sortable = std::random_access_iterator<std::ranges::iterator_t<T>>
    && std::sortable<std::ranges::iterator_t<T>>;

void process(Sortable auto& container) {
    std::ranges::sort(container);
}
```

Follow-up (EN): How do concepts interact with SFINAE?

---

### Q9. `ranges` cải thiện gì so với STL cũ?

**A:**
- EN: Ranges provide **lazy, composable** pipelines via the `|` operator. No intermediate containers created. Range algorithms accept containers directly (no `.begin()/.end()` pairs). Views are lightweight — they don't own data.
- VI: Ranges cung cấp **lazy, composable** pipeline qua toán tử `|`. Không tạo container trung gian. Range algorithm nhận container trực tiếp (không cần `.begin()/.end()`). View nhẹ — không sở hữu data.

```cpp
auto result = numbers
    | std::views::filter([](int n) { return n % 2 == 0; })
    | std::views::transform([](int n) { return n * n; })
    | std::views::take(5);
// Lazy: nothing computed until iteration
for (int x : result) printf("%d ", x);
```

Follow-up (EN): What is the difference between a view and a container in Ranges?

---

### Q10. Coroutines — mức senior cần biết gì?

**A:**
- EN: Coroutines can **suspend** and **resume** without blocking a thread. C++20 provides low-level machinery (`co_await`, `co_yield`, `co_return`); libraries (cppcoro, Asio) provide high-level abstractions. Use for: generators, async I/O, cooperative multitasking.
- VI: Coroutines có thể **suspend** và **resume** mà không block thread. C++20 cung cấp cơ chế thấp (`co_await`, `co_yield`, `co_return`); thư viện (cppcoro, Asio) cung cấp abstraction cao. Dùng cho: generator, async I/O, cooperative multitasking.

```cpp
Generator<int> fibonacci() {
    int a = 0, b = 1;
    while (true) {
        co_yield a;
        std::tie(a, b) = std::pair{b, a + b};
    }
}
for (int x : fibonacci() | std::views::take(10))
    printf("%d ", x);
```

Follow-up (EN): What is the difference between stackful and stackless coroutines?

---

### Q11. `std::span` dùng khi nào?

**A:**
- EN: `span<T>` is a non-owning view over contiguous memory — unifies raw arrays, `vector`, `array`, C arrays under one parameter type. Like `string_view` but for any type. Can be fixed-size (`span<int,5>`) or dynamic (`span<int>`).
- VI: `span<T>` là non-owning view trên vùng nhớ liên tục — thống nhất raw array, `vector`, `array`, C array dưới một kiểu parameter. Giống `string_view` nhưng cho mọi kiểu. Có thể cố định kích thước (`span<int,5>`) hoặc động (`span<int>`).

```cpp
void process(std::span<const int> data) {
    for (int x : data) printf("%d ", x);
}
int arr[] = {1, 2, 3};
std::vector<int> vec = {4, 5, 6};
process(arr);  // OK
process(vec);  // OK
```

Follow-up (EN): What is the difference between `span<const int>` and `const span<int>`?

---

## 4) Template nâng cao

### Q12. Fold expression là gì?

**A:**
- EN: C++17 feature that expands parameter packs with an operator. Four forms: unary left/right fold, binary left/right fold. Replaces recursive template expansion.
- VI: Tính năng C++17 mở rộng parameter pack bằng operator. 4 dạng: unary left/right fold, binary left/right fold. Thay thế recursive template expansion.

```cpp
template<typename... Args>
auto sum(Args... args) { return (args + ...); }       // unary right fold
// sum(1,2,3) = 1 + (2 + 3) = 6

template<typename... Args>
void print(Args... args) { ((std::cout << args << " "), ...); }
// print(1, "hi", 3.14) → "1 hi 3.14 "
```

Follow-up (EN): What is the difference between `(args + ...)` and `(... + args)`?

---

### Q13. CRTP dùng khi nào?

**A:**
- EN: **Curiously Recurring Template Pattern**: `class Derived : Base<Derived>`. Achieves static polymorphism — no vtable overhead, fully inlineable. Use for: mixin functionality, compile-time interface enforcement, `enable_shared_from_this`.
- VI: **CRTP**: `class Derived : Base<Derived>`. Đạt được static polymorphism — không overhead vtable, inline hoàn toàn. Dùng cho: mixin, ép tuân thủ interface lúc compile, `enable_shared_from_this`.

```cpp
template<typename T>
struct Addable {
    T operator+(const T& other) const {
        T result(static_cast<const T&>(*this));
        result += other;
        return result;
    }
};
struct Vec2 : Addable<Vec2> {
    float x, y;
    Vec2& operator+=(const Vec2& o) { x += o.x; y += o.y; return *this; }
};
// Vec2 automatically gets operator+ via CRTP
```

Follow-up (EN): How does C++20 Concepts compare to CRTP for static interfaces?

---

### Q14. Type traits dùng để làm gì?

**A:**
- EN: Compile-time type queries and transformations from `<type_traits>`. Use to: conditionally enable code (SFINAE/concepts), optimize for trivial types (memcpy instead of copy ctor), validate API constraints.
- VI: Truy vấn và biến đổi kiểu tại compile time từ `<type_traits>`. Dùng để: bật code có điều kiện (SFINAE/concepts), tối ưu cho trivial type (memcpy thay vì copy ctor), kiểm tra ràng buộc API.

```cpp
template<typename T>
void serialize(const T& obj, std::byte* buf) {
    if constexpr (std::is_trivially_copyable_v<T>) {
        std::memcpy(buf, &obj, sizeof(T));  // fast path
    } else {
        obj.serialize(buf);                  // custom serialization
    }
}
```

Follow-up (EN): What does `std::is_trivially_copyable` guarantee?

---

## 5) Build và Package Ecosystem

### Q15. Vì sao senior cần biết CMake target-based?

**A:**
- EN: Target-based CMake (`target_link_libraries`, `target_include_directories`) propagates dependencies cleanly via `PUBLIC`/`PRIVATE`/`INTERFACE`. Avoids global state (`include_directories`, `add_definitions`) which causes hard-to-debug build issues in large projects.
- VI: CMake target-based truyền dependency sạch sẽ qua `PUBLIC`/`PRIVATE`/`INTERFACE`. Tránh global state (`include_directories`, `add_definitions`) gây lỗi build khó debug trong project lớn.

```cmake
add_library(mylib src.cpp)
target_include_directories(mylib PUBLIC include/)
target_compile_definitions(mylib PRIVATE DEBUG_MODE)
target_link_libraries(app PRIVATE mylib)  # app inherits include/ but not DEBUG_MODE
```

Follow-up (EN): What is the difference between `PUBLIC`, `PRIVATE`, and `INTERFACE` in CMake?

---

### Q16. `FetchContent` vs `find_package` vs `add_subdirectory`?

**A:**
- EN: `find_package`: uses pre-installed libraries — fast configure but requires system setup. `FetchContent`: downloads at configure time — reproducible but slower. `add_subdirectory`: includes source directly — tightest control but couples build systems.
- VI: `find_package`: dùng thư viện đã cài sẵn — configure nhanh nhưng cần setup hệ thống. `FetchContent`: tải lúc configure — reproducible nhưng chậm hơn. `add_subdirectory`: include source trực tiếp — kiểm soát chặt nhất nhưng coupling build system.

Follow-up (EN): What is the role of Conan or vcpkg as C++ package managers?

---

### Q17. Có nên header-only mọi thứ?

**A:**
- EN: No. Header-only causes: slower builds (recompiled in every TU), code bloat (templates instantiated everywhere), implementation leakage. Use header-only for: small utility libraries, template-heavy code. For large projects, prefer separate compilation.
- VI: Không. Header-only gây: build chậm (recompile mỗi TU), code bloat (template instantiate khắp nơi), lộ implementation. Dùng header-only cho: thư viện tiện ích nhỏ, code template-heavy. Project lớn nên tách compilation.

Follow-up (EN): What is the "compilation firewall" technique?

---

## 6) Phân biệt Senior

### Q18. ABI compatibility là gì?

**A:**
- EN: ABI (Application Binary Interface) compatibility means two binaries compiled separately can link and run together. Breaking ABI: changing class layout (add/remove members), changing vtable order, changing enum values, changing function signatures. C++ has no stable ABI — hence the C wrapper pattern for shared libraries.
- VI: ABI compatibility nghĩa là hai binary biên dịch riêng có thể link và chạy cùng nhau. Phá ABI: thay đổi layout class (thêm/bớt member), thay đổi thứ tự vtable, thay đổi enum, thay đổi function signature. C++ không có ABI ổn định — do đó dùng C wrapper cho shared library.

Follow-up (EN): How does the PIMPL idiom help maintain ABI stability?

---

### Q19. Inline namespace cho versioning?

**A:**
- EN: Inline namespaces make symbols available in the parent namespace while allowing version-specific overrides. Used by standard library implementations and library authors for ABI versioning.
- VI: Inline namespace làm symbol khả dụng trong parent namespace, đồng thời cho phép override theo version. Được standard library và thư viện dùng cho ABI versioning.

```cpp
namespace mylib {
    inline namespace v2 {  // current version
        struct Config { int timeout; bool tls; };
    }
    namespace v1 {
        struct Config { int timeout; };
    }
}
mylib::Config c;     // resolves to mylib::v2::Config
mylib::v1::Config old_c;  // explicit old version
```

Follow-up (EN): How does `std::literals` use inline namespaces?

---

### Q20. C++20 Modules — khi nào dùng?

**A:**
- EN: Modules replace `#include` with import declarations — faster compilation (no header re-parsing), better encapsulation (only exported symbols visible), no macro leakage. Adoption blocker: toolchain support still maturing (CMake, build systems, IDE). Use when toolchain supports it and project is large enough to benefit.
- VI: Modules thay thế `#include` bằng import — compile nhanh hơn (không re-parse header), encapsulation tốt hơn (chỉ symbol export mới thấy), không rò rỉ macro. Hạn chế: toolchain chưa hoàn thiện (CMake, build system, IDE). Dùng khi toolchain hỗ trợ và project đủ lớn để có lợi.

```cpp
// math.cppm (module interface)
export module math;
export int add(int a, int b) { return a + b; }

// main.cpp
import math;
int main() { return add(1, 2); }
```

Follow-up (EN): What is the difference between a module interface unit and a module implementation unit?

---

## Flash card (ôn nhanh)

| Câu hỏi / Question | Trả lời nhanh / Quick answer |
|---|---|
| `auto` bỏ gì? | Drops const and reference — use `const auto&` |
| `decltype(auto)` khi nào? | Perfect-forwarding return types |
| `[=]` trap? | Captures `this` silently → dangling |
| `optional` vs pointer? | Value semantics, no heap, clear intent |
| `variant` vs union? | Type-safe, calls dtors, knows active type |
| `string_view` bẫy? | Dangling if source destroyed |
| Concepts ưu điểm? | Clear errors, documents constraints |
| Ranges lazy? | Views don't compute until iterated |
| Coroutine keywords? | `co_await`, `co_yield`, `co_return` |
| CRTP dùng cho? | Static polymorphism, no vtable |
| Header-only nhược điểm? | Slow build, code bloat, leaks impl |
| ABI break khi nào? | Change class layout, vtable order, enums |
| C++20 Modules lợi ích? | Fast compile, no macro leak, better encapsulation |
