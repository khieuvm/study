# 05 - C++ STL (Standard Template Library) — Bilingual VI/EN

---

## 1) Containers

### Q1. Các container chính trong STL và khi nào dùng cái nào?

**A:**
- EN: STL containers fall into three categories: **sequence** (vector, deque, list, array), **associative** (map, set — sorted), and **unordered** (unordered_map, unordered_set — hash-based). Default choice: `vector` for sequences, `unordered_map` for key-value lookup.
- VI: STL container gồm 3 nhóm: **sequence** (vector, deque, list, array), **associative** (map, set — sorted), và **unordered** (unordered_map, unordered_set — hash). Mặc định: `vector` cho sequence, `unordered_map` cho key-value lookup.

| Container | Structure | Access | Insert/Delete | Use when |
|---|---|---|---|---|
| `vector<T>` | Dynamic array | O(1) random | O(1) back, O(n) mid | Default sequence container |
| `deque<T>` | Chunked array | O(1) random | O(1) both ends | Queue + random access |
| `list<T>` | Doubly-linked | O(n) | O(1) anywhere (with iter) | Frequent mid insert/delete |
| `array<T,N>` | Static array | O(1) | Not allowed | Fixed-size on stack |
| `map<K,V>` | Red-black tree | O(log n) | O(log n) | Sorted key-value |
| `unordered_map<K,V>` | Hash table | O(1) avg | O(1) avg | Fast lookup, nó order needed |
| `set<T>` / `unordered_set<T>` | Tree / Hash | O(log n) / O(1) | Same | Unique membership |
| `priority_queue<T>` | Binary heap | O(1) top | O(log n) push/pop | Max/min element fast |

Follow-up (EN): Why is `vector` usually faster than `list` even for mid-insertions on small sizes? (Cache locality.)

---

### Q2. `vector` hoạt động như thế nào? Khi nào reallocation xảy ra?

**A:**
- EN: `vector` is a contiguous dynamic array. When `size == capacity`, it allocates a new (typically 2x) buffer, moves all elements, and frees the old buffer. This **invalidates all pointers/iterators**. Use `reserve()` to avoid reallocation when the size is known.
- VI: `vector` là mảng liên tục. Khi `size == capacity`, nó cấp phát buffer mới (thường gấp đôi), move tất cả phần tử, và giải phóng buffer cũ. Dieu này **invalidate tất cả pointer/iterator**. Dùng `reserve()` để tránh reallocation khi biết trước kích thước.

```cpp
std::vector<int> v;
v.reserve(100);     // pre-allocate, nó reallocation until size > 100

// Iterator invalidation
auto* ptr = &v[0];
v.push_back(99);    // IF realloc occurs -> ptr is dangling!
```

- EN: Prefer `emplace_back` over `push_back` — constructs in-place, avoids extra copy/move.
- VI: Ưu tiên `emplace_back` hơn `push_back` — construct tại chỗ, tránh copy/move thừa.

```cpp
v.push_back(MyObj(1, 2));    // ctor + move
v.emplace_back(1, 2);        // ctor only
```

Follow-up (EN): What is the amortized complexity of `push_back` and why?

---

### Q3. `map` vs `unordered_map` — khi nào dùng cái nào?

**A:**
- EN: `map`: red-black tree, O(log n) operations, keys sorted, stable iterators. `unordered_map`: hash table, O(1) average operations, nó order, iterators invalidated on rehash. Use `map` when you need ordering or range queries; use `unordered_map` for pure lookup speed.
- VI: `map`: red-black tree, O(log n), key sorted, iterator ổn định. `unordered_map`: hash table, O(1) trung bình, không thứ tự, iterator bị invalidate khi rehash. Dùng `map` khi cần thứ tự hoặc range query; dùng `unordered_map` cho toc do lookup.

| | `map` | `unordered_map` |
|---|---|---|
| Structure | Red-black tree | Hash table |
| Lookup | O(log n) | O(1) avg, O(n) worst |
| Ordered | Yes (sorted by key) | No |
| Iterator invalidation | Only erased node | On rehash |
| Key requirement | `operator<` | Hash function + `==` |

```cpp
// Custom hash for user-defined types
struct MyKeyHash {
    size_t operator()(const MyKey& k) const {
        return std::hash<int>()(k.id) ^ (std::hash<std::string>()(k.name) << 1);
    }
};
std::unordered_map<MyKey, Value, MyKeyHash> m;
```

Follow-up (EN): What happens when `unordered_map` has many hash collisions? How to prevent it?

---

### Q4. Iterator categories là gì?

**A:**
- EN: Iterators are classified by capability: **Input** (single-pass read), **Output** (single-pass write), **Forward** (multi-pass read/write), **Bidirectional** (+backward), **Random Access** (+jump to any position), **Contiguous** (C++20, guaranteed contiguous memory). Algorithms require minimum iterator categories — e.g., `std::sort` needs Random Access.
- VI: Iterator phần loại theo khả năng: **Input** (đọc 1 lần), **Output** (ghi 1 lần), **Forward** (đọc/ghi nhiều lần), **Bidirectional** (+lui), **Random Access** (+nhảy bất kỳ), **Contiguous** (C++20, memory liên tục). Algorithm yêu cầu iterator tối thìểu — VD `std::sort` cần Random Access.

| Category | Capabilities | Example |
|---|---|---|
| Input | Read once, forward only | `istream_iterator` |
| Forward | Multi-pass read/write | `forward_list::iterator` |
| Bidirectional | + backward (`--`) | `list::iterator`, `map::iterator` |
| Random Access | + jump (`+=n`, `[n]`) | `vector::iterator`, `deque::iterator` |
| Contiguous (C++20) | + contiguous memory | `vector::iterator`, `array::iterator` |

Follow-up (EN): Why can't you use `std::sort` on a `std::list`? (Use `list::sort()` instead.)

---

## 2) Algorithms

### Q5. Các algorithm quan trọng nhất cần biết?

**A:**
- EN: Key STL algorithms: **sorting** (sort, stable_sort, partial_sort), **searching** (find, binary_search, lower_bound), **transforming** (transform, for_each, replace), **removing** (remove + erase idiom), **numeric** (accumulate, iota). All operate on iterator ranges.
- VI: Các STL algorithm chính: **sorting** (sort, stable_sort, partial_sort), **searching** (find, binary_search, lower_bound), **transforming** (transform, for_each, replace), **removing** (remove + erase idiom), **numeric** (accumulate, iota). Tất cả hoạt động trên iterator range.

```cpp
std::vector<int> v = {5, 2, 8, 1, 9, 3};

// Sorting — O(n log n)
std::sort(v.begin(), v.end());
std::stable_sort(v.begin(), v.end());             // preserves relative order

// Searching
std::find(v.begin(), v.end(), 8);                 // O(n), unsorted OK
std::binary_search(v.begin(), v.end(), 8);        // O(log n), must be sorted
auto it = std::lower_bound(v.begin(), v.end(), 5); // first element >= 5

// Transform
std::transform(v.begin(), v.end(), out.begin(), [](int x){ return x*x; });

// Remove + Erase
v.erase(std::remove(v.begin(), v.end(), 0), v.end());

// Numeric
int total = std::accumulate(v.begin(), v.end(), 0);
auto [mn, mx] = std::minmax_element(v.begin(), v.end());
```

Follow-up (EN): What is the difference between `std::sort` and `std::stable_sort` in terms of algorithm and guarantees?

---

### Q6. Erase-remove idiom là gì?

**A:**
- EN: `std::remove` does NOT erase elements — it shifts non-removed elements to the front and returns an iterator to the "garbage" tail. You must call `erase()` to actually remove. C++20 simplifies this with `std::erase` and `std::erase_if` free functions.
- VI: `std::remove` Không xóa phần tử — nó dịch phần tử còn lại về đầu và trả về iterator tới "rác" cuối. Phải gọi `erase()` để thực sự xóa. C++20 đơn giản hoa với `std::erase` và `std::erase_if`.

```cpp
std::vector<int> v = {1, 2, 3, 2, 4, 2, 5};

// Wrong: remove alone doesn't shrink
std::remove(v.begin(), v.end(), 2);  // v still has 7 elements!

// Correct: erase-remove idiom
v.erase(std::remove(v.begin(), v.end(), 2), v.end());  // {1, 3, 4, 5}

// C++20: simpler
std::erase(v, 2);
std::erase_if(v, [](int x){ return x % 2 == 0; });
```

Follow-up (EN): Why doesn't `std::remove` actually erase elements? (It works with iterators, not containers — it doesn't know the container type.)

---

## 3) Utilities Quan trọng

### Q7. `std::optional` dùng khi nào?

**A:**
- EN: `std::optional<T>` represents a value that **may or may not exist** — replaces nullable pointers and sentinel values. Accessing an empty optional via `*` is UB; `.value()` throws `bad_optional_access`.
- VI: `std::optional<T>` biểu diễn giá trị **có thể có hoặc không** — thay thế nullable pointer và sentinel value. Truy cập optional rỗng bằng `*` là UB; `.value()` throw `bad_optional_access`.

```cpp
std::optional<int> find_user(const std::string& name) {
    if (name == "admin") return 42;
    return std::nullopt;
}

auto result = find_user("admin");
if (result) printf("Found: %d\n", *result);
int id = result.value_or(-1);     // -1 if empty
```

Follow-up (EN): How does `std::optional` differ from a pointer for representing "no value"?

---

### Q8. `std::variant` là gì? Khác `union` thế nào?

**A:**
- EN: `std::variant<A,B,C>` is a **type-safe tagged union** — stores one of several types, knows which type is active, and calls destructors correctly. Unlike raw `union`, accessing the wrong type throws `bad_variant_access` instead of causing UB.
- VI: `std::variant<A,B,C>` là **type-safe tagged union** — lưu một trong nhiều kiểu, biết kiểu nào đang active, và gọi destructor đúng. Khác với `union`, truy cập sai kiểu sẽ throw `bad_variant_access` thay vì UB.

```cpp
std::variant<int, double, std::string> v;
v = "hello";

// Safe access
if (auto* p = std::get_if<std::string>(&v)) {
    printf("%s\n", p->c_str());
}

// Pattern matching with std::visit
std::visit([](auto&& val) {
    using T = std::decay_t<decltype(val)>;
    if constexpr (std::is_same_v<T, int>) printf("int: %d\n", val);
    else if constexpr (std::is_same_v<T, std::string>) printf("str: %s\n", val.c_str());
}, v);
```

| | `union` | `variant` |
|---|---|---|
| Type safety | No (UB on wrong access) | Yes (exception) |
| Destructor | Does not call | Calls correctly on type switch |
| Knows active type | Must track manually | `index()`, `holds_alternative` |

Follow-up (EN): What is `std::monostate` and when is it used with `variant`?

---

### Q9. `std::string_view` dùng để làm gì?

**A:**
- EN: `string_view` is a **non-owning, non-allocating** reference to a character sequence. It avoids copies when passing strings to functions. Warning: never return a `string_view` referencing a local `std::string` — it will dangle.
- VI: `string_view` là **non-owning, không allocate** reference đến chuỗi ký từ. Tránh copy khi truyền string vào hàm. Cảnh báo: không báo gio trả về `string_view` trỏ vào local `std::string` — sẽ dangle.

```cpp
void process(std::string_view sv);   // no copy, accepts string, char*, string_view

process("hello");          // no allocation
process(some_string);      // no copy
sv.substr(7, 5);           // returns string_view, nó copy
```

```cpp
// DANGER: dangling string_view
std::string_view dangerous() {
    std::string local = "hello";
    return local;   // local destroyed -> dangling!
}
```

Follow-up (EN): When should you use `const std::string&` vs `std::string_view` as a parameter type?

---

### Q10. `std::span` (C++20) là gì?

**A:**
- EN: `span<T>` is a **non-owning view** over a contiguous sequence of `T` — like `string_view` but for any type. It unifies raw arrays, `vector`, `array` under one parameter type. Can be fixed-size (`span<int, 5>`) or dynamic (`span<int>`).
- VI: `span<T>` là **non-owning view** trên sequence liên tục của `T` — giống `string_view` nhưng cho bất kỳ kiểu. Thống nhất raw array, `vector`, `array` dưới một parameter type. Có thể cố định kích thước (`span<int, 5>`) hoặc đóng (`span<int>`).

```cpp
void process(std::span<int> data) {
    for (int& x : data) x *= 2;
}

int arr[] = {1, 2, 3, 4};
std::vector<int> vec = {1, 2, 3};
process(arr);       // OK
process(vec);       // OK
process({arr, 2});  // first 2 elements only
```

Follow-up (EN): What is the difference between `span<const int>` and `const span<int>`?

---

## 4) Move Semantics và STL

### Q11. Tại sao `std::move` quan trọng với containers?

**A:**
- EN: `std::move` enables containers to **transfer ownership** of internal resources (heap buffers, handles) in O(1) instead of copying in O(n). This is critical for inserting expensive-to-copy objects (strings, vectors) and for transferring entire containers.
- VI: `std::move` cho phép container **chuyển ownership** tài nguyên nội bộ (buffer heap, handle) trong O(1) thay vì copy O(n). Quan trọng khi chen object đặt copy (string, vector) và khi chuyển nguyen container.

```cpp
std::string s = "a very long string...";
std::vector<std::string> words;

words.push_back(s);             // COPY: O(n), s unchanged
words.push_back(std::move(s));  // MOVE: O(1), s now empty

// Move entire container
std::vector<int> a = {1, 2, 3, 4, 5};
std::vector<int> b = std::move(a);  // O(1), a now empty
```

- EN: After `std::move`, the moved-from object is in a **valid but unspecified state** — safe to destroy or reassign, but don't read its value.
- VI: Sau `std::move`, object bi move o trang thai **hợp lệ nhưng không xác định** — an toàn để destroy hoặc gán lại, nhưng không đọc giá trị.

Follow-up (EN): What does "valid but unspecified state" mean in practice for standard containers?

---

## Flash card

| Question / Câu hỏi | Quick answer / Trả lỗi nhanh |
|---|---|
| `vector` vs `list`? | vector: cache-friendly, O(1) random; list: O(1) insert anywhere |
| `map` vs `unordered_map`? | map: sorted O(log n); unordered: O(1) avg, nó order |
| Erase-remove idiom? | `v.erase(remove(...), v.end())` — remove doesn't erase |
| `emplace_back` advantage? | In-place construct, avoids copy/move |
| `string_view` benefit? | Non-owning, nó copy, nó allocation |
| `optional` when? | Value may or may not exist, replaces nullptr |
| `variant` vs `union`? | variant is type-safe, calls destructors |
| Iterator invalidation? | vector: on realloc; map: only erased node |
| `lower_bound` returns? | Iterator to first element >= value |
| `span` purpose? | Non-owning view over contiguous data |
