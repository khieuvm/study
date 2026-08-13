# 04 - C++ Templates & Generic Programming — Bilingual VI/EN

---

## 1) Template Cơ bản

### Q1. Function template và class template khác nhau thế nào?

**A:**
- EN: Function templates can deduce template arguments from call arguments; class templates require explicit types (until C++17 CTAD). Function templates cannot be partially specialized; class templates can.
- VI: Function template có thể suy diễn kiểu từ argument khi gọi; class template phải chỉ rõ kiểu (cho đến C++17 CTAD). Function template không thể partial specialization; class template thì có.

```cpp
// Function template: type deduced from arguments
template<typename T>
T max_val(T a, T b) { return a > b ? a : b; }
max_val(3, 5);          // T = int (deduced)
max_val<long>(3, 5);    // T = long (explicit)

// Class template: must specify type (pre-C++17)
template<typename T>
class Stack {
    std::vector<T> data_;
public:
    void push(const T& x) { data_.push_back(x); }
    T    pop()             { T v = data_.back(); data_.pop_back(); return v; }
};
Stack<int> si;       // must specify <int>
// C++17: Stack s{3}; // CTAD deduces Stack<int>
```

Follow-up (EN): What is CTAD (Class Template Argument Deduction) and when does it fail?

---

### Q2. Template specialization là gì? Full vs Partial?

**A:**
- EN: Template specialization provides a **custom implementation** for specific types. **Full specialization** matches exactly one type. **Partial specialization** matches a family of types (only for class templates, not function templates).
- VI: Template specialization cung cấp **implementation riêng** cho các kiểu cụ thể. **Full specialization** khớp đúng 1 kiểu. **Partial specialization** khớp 1 ho kiểu (chi ap dùng cho class template, không cho function template).

```cpp
// Primary template
template<typename T>
struct Serialize {
    static std::string to_string(T val) { return std::to_string(val); }
};

// Full specialization for bool
template<>
struct Serialize<bool> {
    static std::string to_string(bool val) { return val ? "true" : "false"; }
};

// Partial specialization: when T is a pointer
template<typename T>
struct Serialize<T*> {
    static std::string to_string(T* val) { return val ? Serialize<T>::to_string(*val) : "null"; }
};
```

Follow-up (EN): Why can't function templates be partially specialized? (Use overloading instead.)

---

### Q3. Typename vs Class trong template parameter?

**A:**
- EN: In a template parameter list, `typename` and `class` are **identical**. However, `typename` has a second use: disambiguating **dependent types** inside template bodies — telling the compiler that a name is a type, not a value.
- VI: Trong template parameter list, `typename` và `class` **giống hoàn toàn**. Tuy nhiên, `typename` còn dùng để chỉ rõ **dependent type** trong than template — báo compiler ten do là kiểu, không phải giá trị.

```cpp
template<typename T> void f(T x);   // OK
template<class    T> void f(T x);   // identical

// Second use of typename: disambiguating dependent type
template<typename T>
void foo() {
    typename T::value_type x;   // required: T::value_type could be a static member
}
```

Follow-up (EN): When is the `template` keyword needed to disambiguate in a similar way?

---

## 2) SFINAE và Type Traits

### Q4. SFINAE là gì? Dùng để làm gì?

**A:**
- EN: **SFINAE (Substitution Failure Is Not An Error)**: when the compiler substitutes types into a template and the result is invalid, that template is silently removed from the overload set instead of causing a compile error. This enables compile-time conditional function selection.
- VI: **SFINAE**: khi compiler substitute kiểu vào template mà kết quả không hợp lệ, template do bi loại âm thầm khỏi overload set thay vì báo lỗi. Dieu này cho phép chon hàm có điều kiện tại compile time.

```cpp
// Only enabled if T has value_type member
template<typename T>
typename T::value_type sum(T container) {
    typename T::value_type total{};
    for (auto& x : container) total += x;
    return total;
}

sum(std::vector<int>{1,2,3});   // OK: vector has value_type
sum(42);                         // SFINAE: silently excluded, looks for another overload
```

```cpp
// SFINAE with std::enable_if
template<typename T>
std::enable_if_t<std::is_integral_v<T>, T>
double_it(T x) { return x * 2; }

template<typename T>
std::enable_if_t<std::is_floating_point_v<T>, T>
double_it(T x) { return x * 2.0; }
```

Follow-up (EN): What is the difference between "hard errors" and SFINAE-friendly errors?

---

### Q5. `std::enable_if` vs `if constexpr` vs Concepts?

**A:**
- EN: Three ways to conditionally enable template code, from oldest to newest: `enable_if` (C++11, verbose but flexible), `if constexpr` (C++17, simple but single function), Concepts (C++20, cleanest syntax and best error messages).
- VI: Ba cách điều kiện hóa template code, từ cũ đến mọi: `enable_if` (C++11, verbose nhưng linh hoạt), `if constexpr` (C++17, đơn giản nhưng 1 hàm), Concepts (C++20, cú pháp dep nhất và lỗi báo rõ nhất).

```cpp
// if constexpr (C++17) — simplest
template<typename T>
auto describe(T x) {
    if constexpr (std::is_integral_v<T>)
        return "integer: " + std::to_string(x);
    else
        return std::string("other");
}

// enable_if (C++11) — verbose
template<typename T, std::enable_if_t<std::is_integral_v<T>, int> = 0>
void process(T x) { printf("integral\n"); }

// Concepts (C++20) — clearest
template<std::integral T>
void process(T x) { printf("integral\n"); }
```

Follow-up (EN): Can `if constexpr` replace all uses of `enable_if`? (No — it can't create separate overloads.)

---

### Q6. Type traits phổ biến nhất cần biết?

**A:**
- EN: Type traits (`<type_traits>`) provide compile-time type queries and transformations. Key categories: type checking (`is_integral`, `is_pointer`), property queries (`is_const`, `is_trivially_copyable`), type transformations (`remove_const`, `decay`), and conditionals (`conditional`).
- VI: Type traits (`<type_traits>`) cung cấp truy vấn và biến đổi kiểu tại compile time. Các nhóm chính: kiểm tra kiểu (`is_integral`, `is_pointer`), thuoc tinh (`is_const`, `is_trivially_copyable`), biến đổi kiểu (`remove_const`, `decay`), và điều kiện (`conditional`).

```cpp
#include <type_traits>

// Type checks
std::is_integral_v<int>              // true
std::is_floating_point_v<double>     // true
std::is_pointer_v<int*>              // true
std::is_same_v<int, int32_t>         // usually true

// Property queries
std::is_trivially_copyable_v<T>      // true -> safe to memcpy
std::is_default_constructible_v<T>

// Type transformations
std::remove_const_t<const int>       // int
std::remove_reference_t<int&>        // int
std::decay_t<int[5]>                 // int*
std::decay_t<int&>                   // int

// Conditional
std::conditional_t<true, int, double>   // int
```

Follow-up (EN): What does `std::is_trivially_copyable` guarantee and why is it important for serialization?

---

## 3) Variadic Templates

### Q7. Variadic template là gì? Parameter pack là gì?

**A:**
- EN: Variadic templates accept **any number of arguments** of any types via parameter packs (`typename... Args`). Before C++17, expansion used recursion; C++17 introduced **fold expressions** for concise expansion.
- VI: Variadic template nhận **bất kỳ số lượng argument** của bất kỳ kiểu qua parameter pack (`typename... Args`). Trước C++17, mở rộng dùng đệ quy; C++17 giới thiệu **fold expression** để mở rộng gọn hơn.

```cpp
// C++17 fold expression
template<typename... Args>
void print_all(Args&&... args) {
    ((std::cout << args << " "), ...);
    std::cout << "\n";
}
print_all(1, 2.0, "hello", true);

// Count elements
template<typename... T>
constexpr size_t count() { return sizeof...(T); }

// Recursive expansion (pre-C++17)
void log() {}  // base case
template<typename T, typename... Rest>
void log(T first, Rest... rest) {
    std::cout << first << " ";
    log(rest...);
}
```

```cpp
// Fold expressions (C++17)
template<typename... T>
auto sum(T... args) { return (args + ...); }   // right fold
sum(1, 2, 3, 4);  // 10
```

Follow-up (EN): What are the four forms of fold expressions (unary/binary, left/right)?

---

### Q8. Perfect forwarding và `std::forward` là gì?

**A:**
- EN: Perfect forwarding preserves the **value category** (lvalue/rvalue) of arguments when passing them through template functions. `T&&` in a template is a **forwarding reference** (not an rvalue reference). `std::forward<T>(arg)` casts back to the original category.
- VI: Perfect forwarding bảo toàn **value category** (lvalue/rvalue) của argument khi truyền qua template function. `T&&` trong template là **forwarding reference** (không phải rvalue reference). `std::forward<T>(arg)` cast ve category ban đầu.

```cpp
// Without forwarding: rvalue becomes lvalue
template<typename T>
void wrapper(T arg) { foo(arg); }  // arg is always lvalue!

// With perfect forwarding
template<typename T>
void wrapper(T&& arg) {
    foo(std::forward<T>(arg));     // preserves lvalue/rvalue
}

// Real-world: make_unique implementation
template<typename T, typename... Args>
std::unique_ptr<T> make_unique(Args&&... args) {
    return std::unique_ptr<T>(new T(std::forward<Args>(args)...));
}
```

Follow-up (EN): What is reference collapsing and how does it enable forwarding references?

---

## 4) Template Metaprogramming

### Q9. `constexpr` vs template metaprogramming?

**A:**
- EN: Both compute at compile time. Template metaprogramming (TMP) uses recursive template instantiation — powerful but hard to read. `constexpr` (C++11+) looks like normal code and is preferred. Use TMP for type-level computation; use `constexpr` for value computation.
- VI: Cả hai đều tính tại compile time. Template metaprogramming (TMP) dùng recursive template instantiation — mạnh nhưng khó đọc. `constexpr` (C++11+) trang như code thường và được ưu tiên. Dùng TMP cho type-level computation; dùng `constexpr` cho value computation.

```cpp
// TMP (C++03 style) — hard to read
template<int N>
struct Fib {
    static const int value = Fib<N-1>::value + Fib<N-2>::value;
};
template<> struct Fib<0> { static const int value = 0; };
template<> struct Fib<1> { static const int value = 1; };
int x = Fib<10>::value;

// constexpr (C++11+) — readable
constexpr int fib(int n) {
    if (n <= 1) return n;
    return fib(n-1) + fib(n-2);
}
constexpr int x = fib(10);  // compile-time
int y = fib(n);              // also works at runtime
```

Follow-up (EN): What limitations does C++11 `constexpr` have that C++14/17/20 removed?

---

### Q10. Concepts (C++20) là gì?

**A:**
- EN: Concepts are **named constraints** on template parameters. They produce clear error messages (instead of pages of template substitution errors), serve as documentation, and enable overload resolution based on constraints.
- VI: Concepts là **named constraints** cho template parameters. Chúng tạo lỗi báo rõ ràng (thay vì nhiều trang lỗi template substitution), làm tài liệu, và cho phép overload resolution dua trên constraints.

```cpp
// Define concept
template<typename T>
concept Addable = requires(T a, T b) {
    { a + b } -> std::convertible_to<T>;
};

template<typename T>
concept Container = requires(T c) {
    { c.begin() } -> std::input_iterator;
    { c.end()   } -> std::input_iterator;
    { c.size()  } -> std::convertible_to<std::size_t>;
};

// Use concept
template<Addable T>
T sum(T a, T b) { return a + b; }

// Standard library concepts
std::integral<T>            // int, long, ...
std::floating_point<T>      // float, double
std::same_as<T, U>          // T is same as U
std::derived_from<T, Base>  // T inherits Base
std::invocable<F, Args...>  // F callable with Args
```

Follow-up (EN): How do concepts interact with overload resolution when multiple constrained overloads match?

---

## 5) Non-type Template Parameters

### Q11. Non-type template parameter là gì?

**A:**
- EN: Template parameters can be **values** (not just types): integers, enums, pointers, and (since C++20) floating-point and literal class types. Common use: compile-time array sizes, policy selection, fixed-point precision.
- VI: Template parameter có thể là **giá trị** (không chi kiểu): integer, enum, pointer, và (từ C++20) floating-point và literal class type. Ứng dụng phổ biến: kích thước mạng compile-time, policy selection, fixed-point precision.

```cpp
template<typename T, std::size_t N>
class FixedArray {
    T data_[N];
public:
    T& operator[](size_t i) { return data_[i]; }
    constexpr size_t size() const { return N; }
};

FixedArray<int, 10> arr;     // 10 ints on stack, nó heap
FixedArray<double, 3> vec;   // 3 doubles

// C++20: floating-point NTTP
template<double D>
constexpr double scale(double x) { return x * D; }
auto y = scale<2.5>(10.0);  // 25.0 at compile time
```

Follow-up (EN): What types are allowed as non-type template parameters in C++20 vs C++17?

---

## Flash card

| Question / Câu hỏi | Quick answer / Trả lỗi nhanh |
|---|---|
| SFINAE là gì? | Substitution failure → silently excluded, not an error |
| `typename` in template body? | Disambiguate dependent type: `typename T::type` |
| `sizeof...(T)` does? | Count elements in parameter pack |
| `std::forward<T>(arg)` does? | Preserves lvalue/rvalue category |
| Full vs partial specialization? | Full: one specific type; Partial: a family of types |
| `if constexpr` vs `enable_if`? | `if constexpr` simpler; `enable_if` for separate overloads |
| Concepts (C++20) advantage? | Clean syntax, clear errors, constraint documentation |
| `std::decay_t<int[5]>` result? | `int*` (array-to-pointer decay) |
| TMP vs constexpr? | constexpr more readable; prefer it for value computation |
| Non-type template param? | Compile-time value: `template<int N>` |
