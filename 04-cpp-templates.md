# 04 - C++ Templates & Generic Programming

---

## 1) Template Co Ban

### Q1. Function template va class template khac nhau the nao?

**A:**

```cpp
// Function template: suy dien kieu tu argument
template<typename T>
T max_val(T a, T b) { return a > b ? a : b; }

max_val(3, 5);          // T = int, suy dien tu dau vao
max_val(3.0, 5.0);      // T = double
max_val<long>(3, 5);    // explicit: T = long

// Class template: phai chi ro kieu (tru C++17 deduction guide)
template<typename T>
class Stack {
    std::vector<T> data_;
public:
    void push(const T& x) { data_.push_back(x); }
    T    pop()             { T v = data_.back(); data_.pop_back(); return v; }
};

Stack<int>    si;    // phai chi ro <int>
Stack<double> sd;
// C++17: Stack s{3}; // deduction guide co the suy dien
```

---

### Q2. Template specialization la gi? Full vs Partial?

**A:** Cho phep cung cap implementation **dac biet** cho mot kieu cu the.

**Full specialization** — cho dung 1 kieu:
```cpp
// Primary template
template<typename T>
struct Serialize {
    static std::string to_string(T val) { return std::to_string(val); }
};

// Full specialization cho bool
template<>
struct Serialize<bool> {
    static std::string to_string(bool val) { return val ? "true" : "false"; }
};

// Full specialization cho const char*
template<>
struct Serialize<const char*> {
    static std::string to_string(const char* val) { return val; }
};
```

**Partial specialization** — cho 1 lop kieu (chi voi class template):
```cpp
// Primary
template<typename T, typename U>
struct Pair { ... };

// Partial: khi ca hai kieu giong nhau
template<typename T>
struct Pair<T, T> { ... };   // dung khi A == B

// Partial: khi T la pointer
template<typename T>
struct Pair<T*, T*> { ... };
```

---

### Q3. Typename vs Class trong template parameter?

**A:** Trong template parameter, `typename` va `class` **hoan toan giong nhau**:

```cpp
template<typename T> void f(T x);   // OK
template<class    T> void f(T x);   // OK, y het

// Khac nhau: 'typename' con dung de chi ro dependent type
template<typename T>
void foo() {
    typename T::value_type x;   // "typename" can thiet vi T::value_type la dependent type
    // T::value_type co the la static member, khong phai type
    // "typename" bao compiler "day la kieu"
}
```

---

## 2) SFINAE va Type Traits

### Q4. SFINAE la gi? Dung de lam gi?

**A:** **SFINAE = Substitution Failure Is Not An Error.** Khi compiler thu substitute type vao template, neu bi loi, no **khong bao loi** ma chi loai template do khoi overload set.

```cpp
// Chi enable neu T co member type `value_type`
template<typename T>
typename T::value_type sum(T container) {  // Neu T khong co value_type -> substitution failure
    typename T::value_type total{};
    for (auto& x : container) total += x;
    return total;
}

sum(std::vector<int>{1,2,3});   // OK: vector co value_type
sum(42);                         // Khong chon ham nay (substitution failure), tim ham khac
```

**SFINAE voi `std::enable_if`:**
```cpp
// Chi enable cho integral types
template<typename T>
std::enable_if_t<std::is_integral_v<T>, T>
double_it(T x) { return x * 2; }

// Chi enable cho floating point
template<typename T>
std::enable_if_t<std::is_floating_point_v<T>, T>
double_it(T x) { return x * 2.0; }

double_it(5);     // goi version integral
double_it(3.14);  // goi version floating point
double_it("hi");  // ERROR: khong co version nao match
```

---

### Q5. `std::enable_if` vs `if constexpr` vs Concepts?

**A:** Ba cach dieu kien hoa template, theo do phuc tap tang dan (hoac giam dan):

**`if constexpr` (C++17) — don gian nhat:**
```cpp
template<typename T>
auto describe(T x) {
    if constexpr (std::is_integral_v<T>) {
        return "integer: " + std::to_string(x);
    } else if constexpr (std::is_floating_point_v<T>) {
        return "float: " + std::to_string(x);
    } else {
        return std::string("unknown");
    }
}
// Nhanh, de doc, nhung van la 1 ham cho moi kieu
```

**`enable_if` (C++11) — flexible nhung verbose:**
```cpp
template<typename T, std::enable_if_t<std::is_integral_v<T>, int> = 0>
void process(T x) { printf("integral\n"); }

template<typename T, std::enable_if_t<std::is_floating_point_v<T>, int> = 0>
void process(T x) { printf("floating\n"); }
```

**Concepts (C++20) — ro rang nhat:**
```cpp
template<std::integral T>
void process(T x) { printf("integral\n"); }

template<std::floating_point T>
void process(T x) { printf("floating\n"); }
```

---

### Q6. Type traits pho bien nhat can biet?

**A:**

```cpp
#include <type_traits>

// Kiem tra kieu
std::is_integral_v<int>          // true
std::is_floating_point_v<double> // true
std::is_pointer_v<int*>          // true
std::is_reference_v<int&>        // true
std::is_class_v<std::string>     // true
std::is_same_v<int, int32_t>     // phu thuoc ABI, thuong true

// Kiem tra properties
std::is_const_v<const int>       // true
std::is_trivial_v<int>           // true (co the memcpy)
std::is_trivially_copyable_v<T>  // true -> safe to memcpy
std::is_default_constructible_v<T>
std::is_copy_constructible_v<T>
std::is_move_constructible_v<T>

// Bien doi kieu
std::remove_const_t<const int>   // int
std::remove_reference_t<int&>    // int
std::remove_pointer_t<int*>      // int
std::add_const_t<int>            // const int
std::decay_t<int[5]>             // int*  (giong array decay)
std::decay_t<int&>               // int

// Conditional
std::conditional_t<true, int, double>   // int
std::conditional_t<false, int, double>  // double
```

---

## 3) Variadic Templates

### Q7. Variadic template la gi? Parameter pack la gi?

**A:** Variadic template cho phep ham/class nhan **bat ky so luong tham so** cua bat ky kieu.

```cpp
// Ham in tat ca tham so
template<typename... Args>    // Args la parameter pack
void print_all(Args&&... args) {   // args la pack cua values
    // Expand pack voi fold expression (C++17):
    ((std::cout << args << " "), ...);
    std::cout << "\n";
}

print_all(1, 2.0, "hello", true);  // OK: 4 tham so khac kieu
print_all();                        // OK: 0 tham so
```

**Dem so phan tu:**
```cpp
template<typename... T>
constexpr size_t count() { return sizeof...(T); }  // sizeof... operator

count<int, double, char>();  // 3
```

**Recursive expansion (truoc C++17):**
```cpp
// Base case
void log() {}

// Recursive case
template<typename T, typename... Rest>
void log(T first, Rest... rest) {
    std::cout << first << " ";
    log(rest...);  // goi voi pack nho di 1
}
log(1, 2.0, "three");  // in: 1 2 three
```

**Fold expressions (C++17) — ngan gon hon:**
```cpp
template<typename... T>
auto sum(T... args) {
    return (args + ...);     // unary right fold: a + (b + (c + d))
    // hoac: (... + args)    // unary left fold: ((a + b) + c) + d
    // hoac: (args + ... + 0) // binary fold voi init
}
sum(1, 2, 3, 4);  // 10
```

---

### Q8. Perfect forwarding va `std::forward` la gi?

**A:** Khi truyen argument qua nhieu lop ham, muon giu nguyen **value category** (lvalue/rvalue). `std::forward` thuc hien dieu do.

```cpp
// Van de khong co perfect forwarding:
template<typename T>
void wrapper(T arg) {
    foo(arg);   // arg luon la lvalue du T la rvalue!
}

std::string s = "hello";
wrapper(s);              // foo nhan lvalue OK
wrapper(std::string("hi")); // foo van nhan lvalue (mat rvalue optimization!)

// Giai phap: perfect forwarding
template<typename T>
void wrapper(T&& arg) {            // T&& la "forwarding reference" (universal ref)
    foo(std::forward<T>(arg));     // giu nguyen lvalue/rvalue
}
// Khi T = lvalue ref:   T&& = A& &&  = A&   -> forward nhu lvalue
// Khi T = non-ref:      T&& = A&&           -> forward nhu rvalue
```

**Ung dung pho bien:**
```cpp
// make_unique implementation:
template<typename T, typename... Args>
std::unique_ptr<T> make_unique(Args&&... args) {
    return std::unique_ptr<T>(new T(std::forward<Args>(args)...));
}
```

---

## 4) Template Metaprogramming

### Q9. `constexpr` vs template metaprogramming?

**A:** Ca hai deu tinh toan tai **compile time**, nhung khac nhau ve cach viet.

**Template metaprogramming (TMp) — C++03 style:**
```cpp
// Fibonacci tai compile time
template<int N>
struct Fib {
    static const int value = Fib<N-1>::value + Fib<N-2>::value;
};
template<> struct Fib<0> { static const int value = 0; };
template<> struct Fib<1> { static const int value = 1; };

int x = Fib<10>::value;  // tinh tai compile time
```

**`constexpr` (C++11+) — de doc hon nhieu:**
```cpp
constexpr int fib(int n) {
    if (n <= 1) return n;
    return fib(n-1) + fib(n-2);
}
constexpr int x = fib(10);  // tinh tai compile time
// Cung co the goi o runtime: int y = fib(n); // tinh o runtime
```

**Khi nao dung TMP vs constexpr:**
- `constexpr` de hon doc, uu tien dung
- TMP cho type-level computation (khong co gia tri runtime)

---

### Q10. Concepts (C++20) la gi?

**A:** Concepts la named constraints cho template parameters — lam loi bao dep hon, code ro rang hon.

```cpp
// Dinh nghia concept
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

// Dung concept
template<Addable T>
T sum(T a, T b) { return a + b; }

template<Container C>
auto first_element(const C& c) { return *c.begin(); }

// Loi bao ro rang:
sum("hello", "world");
// error: 'const char*' does not satisfy constraint 'Addable'
// Thay vi: 50 dong error template substitution cu
```

**Standard concepts pho bien:**
```cpp
std::integral<T>          // int, long, ...
std::floating_point<T>    // float, double
std::same_as<T, U>        // T giong U
std::derived_from<T, Base>// T ke thua Base
std::convertible_to<T, U> // T chuyen duoc sang U
std::invocable<F, Args...>// F co the goi voi Args
std::ranges::range<T>     // T la range
```

---

## 5) Non-type Template Parameters

### Q11. Non-type template parameter la gi?

**A:** Template parameter co the la **gia tri** thay vi kieu.

```cpp
// Size la compile-time constant
template<typename T, std::size_t N>
class FixedArray {
    T data_[N];
public:
    T& operator[](size_t i) { return data_[i]; }
    constexpr size_t size() const { return N; }
};

FixedArray<int, 10> arr;    // 10 int tren stack, khong heap
FixedArray<double, 3> vec;  // 3 double
// arr.size() = 10, tinh tai compile time

// C++20: float, pointer, cac kieu khac cung duoc
template<double D>
constexpr double scale(double x) { return x * D; }
auto y = scale<2.5>(10.0);  // y = 25.0, tinh o compile time
```

---

## Flash card

| Cau hoi | Tra loi nhanh |
|---|---|
| SFINAE la gi? | Substitution failure -> bo qua, khong bao loi |
| `typename` trong template body? | Truoc dependent type: `typename T::type` |
| `sizeof...(T)` lam gi? | Dem so phan tu trong parameter pack |
| `std::forward<T>(arg)` lam gi? | Giu nguyen lvalue/rvalue category |
| Full vs partial specialization? | Full: 1 kieu cu the; Partial: 1 lop kieu |
| `if constexpr` vs `enable_if`? | `if constexpr` de hon, du dung cho 1 ham |
| Concept (C++20) uu diem? | Loi bao dep, constraint ro rang |
| `std::decay_t<int[5]>` la gi? | `int*` (array decay) |
| TMP vs constexpr? | constexpr de doc hon, uu tien dung |
| Non-type template param? | Gia tri compile-time: `template<int N>` |
