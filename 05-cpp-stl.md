# 05 - C++ STL (Standard Template Library)

---

## 1) Containers

### Q1. Cac container chinh trong STL va khi nao dung cai nao?

**A:**

| Container | Cau truc | Access | Insert/Delete | Dung khi |
|---|---|---|---|---|
| `vector<T>` | Dynamic array | O(1) random | O(1) cuoi, O(n) giua | Mac dinh cho sequence |
| `deque<T>` | Chunked array | O(1) random | O(1) hai dau | Queue + random access |
| `list<T>` | Doubly-linked | O(n) | O(1) bat ky (neu co iter) | Nhieu insert/delete giua |
| `forward_list<T>` | Singly-linked | O(n) | O(1) sau node | Memory constraint |
| `array<T,N>` | Static array | O(1) | Khong duoc | Fixed-size on stack |
| `map<K,V>` | Red-black tree | O(log n) | O(log n) | Sorted key-value |
| `unordered_map<K,V>` | Hash table | O(1) avg | O(1) avg | Fast lookup, no order |
| `set<T>` | Red-black tree | O(log n) | O(log n) | Sorted unique elements |
| `unordered_set<T>` | Hash table | O(1) avg | O(1) avg | Fast membership test |
| `priority_queue<T>` | Heap | O(1) top | O(log n) push/pop | Max/min element nhanh |
| `stack<T>` | deque adapter | O(1) top | O(1) | LIFO |
| `queue<T>` | deque adapter | O(1) front/back | O(1) | FIFO |

---

### Q2. `vector` hoat dong nhu the nao? Khi nao reallocation xay ra?

**A:** `vector` la **dynamic array** — khi day, no cap phat mang moi (thuong gap doi kich thuoc) va copy/move tat ca phan tu.

```cpp
std::vector<int> v;
v.reserve(10);      // pre-allocate, tranh reallocation

v.push_back(1);
v.push_back(2);

v.size();           // so phan tu hien tai
v.capacity();       // so phan tu co the chua truoc khi realloc

// Reallocation xay ra khi size == capacity:
for (int i = 0; i < 100; ++i) {
    v.push_back(i); // co the realloc o step 1, 2, 4, 8, 16, 32, 64, 128
}
```

**Invalidation sau reallocation:**
```cpp
auto* ptr = &v[0];    // raw pointer vao vector
v.push_back(99);      // NẾU realloc xay ra -> ptr bi invalidate!
*ptr = 5;             // UB!

// Tuong tu voi iterators
auto it = v.begin();
v.push_back(99);      // it co the bi invalidate
*it = 5;              // UB!
```

**`emplace_back` vs `push_back`:**
```cpp
// push_back: construct object roi copy/move vao vector
v.push_back(MyObj(1, 2, 3));     // ctor + move ctor

// emplace_back: forward args, construct in-place
v.emplace_back(1, 2, 3);         // chi ctor, khong move
// Uu tien dung emplace_back
```

---

### Q3. `map` vs `unordered_map` — khi nao dung cai nao?

**A:**

| | `map` | `unordered_map` |
|---|---|---|
| Cau truc | Red-black tree | Hash table |
| Access | O(log n) | O(1) avg, O(n) worst |
| Ordered | Co (sorted by key) | Khong |
| Iterator invalidate | Khong (chi xoa node do) | Khi rehash |
| Memory | Cao hon (node per entry) | Cao hon (hash table) |
| Key requirement | Operator `<` | Hash function + `==` |

```cpp
// map: keys luon duoc sorted
std::map<std::string, int> m;
m["banana"] = 2;
m["apple"]  = 1;
for (auto& [k, v] : m) printf("%s\n", k.c_str());  // in: apple, banana (sorted)

// unordered_map: nhanh hon, khong sorted
std::unordered_map<std::string, int> um;
um["banana"] = 2;
um["apple"]  = 1;
// Khi iterate: thu tu khong xac dinh
```

**Khi nao dung `map`:**
- Can iterate theo thu tu key
- Can `lower_bound`, `upper_bound`, `equal_range`
- Key khong co hash function

**Khi nao dung `unordered_map`:**
- Toc do lookup quan trong (O(1) vs O(log n))
- Khong can ordered

**Custom hash:**
```cpp
struct MyKeyHash {
    size_t operator()(const MyKey& k) const {
        return std::hash<int>()(k.id) ^ (std::hash<std::string>()(k.name) << 1);
    }
};
std::unordered_map<MyKey, Value, MyKeyHash> m;
```

---

### Q4. Iterator categories la gi?

**A:** Iterators duoc phan loai theo kha nang ho tro:

| Category | Kha nang | Vi du |
|---|---|---|
| Input | Read once, forward only | `istream_iterator` |
| Output | Write once, forward only | `ostream_iterator` |
| Forward | Read/write, multi-pass, forward | `forward_list::iterator` |
| Bidirectional | + backward (`--`) | `list::iterator`, `map::iterator` |
| Random Access | + jump (`+=n`, `[n]`) | `vector::iterator`, `deque::iterator` |
| Contiguous (C++20) | + contiguous memory | `array::iterator`, `vector::iterator` |

```cpp
std::vector<int> v = {1,2,3,4,5};
auto it = v.begin();
it += 3;       // Random access: jump 3 vi tri
*(it - 1);     // Random access: tro lui
std::sort(v.begin(), v.end());  // sort yeu cau Random access iterator

std::list<int> l = {1,2,3};
auto lit = l.begin();
++lit;         // Bidirectional: chi tien 1 buoc
--lit;         // Bidirectional: lui 1 buoc
// lit += 2;   // ERROR: list khong ho tro random access
```

---

## 2) Algorithms

### Q5. Cac algorithm quan trong nhat can biet?

**A:**

```cpp
#include <algorithm>
#include <numeric>

std::vector<int> v = {5, 2, 8, 1, 9, 3};

// --- Sorting ---
std::sort(v.begin(), v.end());                    // O(n log n)
std::stable_sort(v.begin(), v.end());             // giu thu tu relative
std::partial_sort(v.begin(), v.begin()+3, v.end()); // 3 phan tu nho nhat o dau

// --- Searching ---
std::find(v.begin(), v.end(), 8);                 // O(n)
std::binary_search(v.begin(), v.end(), 8);        // O(log n), phai sorted
auto it = std::lower_bound(v.begin(), v.end(), 5); // first >= 5
auto it = std::upper_bound(v.begin(), v.end(), 5); // first > 5

// --- Transform / Modify ---
std::for_each(v.begin(), v.end(), [](int& x){ x *= 2; });
std::transform(v.begin(), v.end(), out.begin(), [](int x){ return x*x; });
std::fill(v.begin(), v.end(), 0);
std::replace(v.begin(), v.end(), 5, 99);          // thay 5 bang 99

// --- Remove / Partition ---
auto end = std::remove(v.begin(), v.end(), 0);    // KHONG xoa, chi dich
v.erase(end, v.end());                            // erase-remove idiom
std::partition(v.begin(), v.end(), [](int x){ return x % 2 == 0; });

// --- Numeric ---
int total = std::accumulate(v.begin(), v.end(), 0);  // sum
std::iota(v.begin(), v.end(), 1);  // fill 1,2,3,4,...

// --- Min/Max ---
auto [mn, mx] = std::minmax_element(v.begin(), v.end());
```

---

### Q6. Erase-remove idiom la gi?

**A:** `std::remove` khong xoa phan tu khoi container — no **dich** phan tu con lai ve dau, tra ve iterator toi phan tu "rac" cuoi. Phai goi `erase` de thuc su xoa.

```cpp
std::vector<int> v = {1, 2, 3, 2, 4, 2, 5};

// SAII: std::remove khong xoa khoi vector
std::remove(v.begin(), v.end(), 2);  // v van co 7 phan tu!

// DUNG: erase-remove idiom
v.erase(std::remove(v.begin(), v.end(), 2), v.end());
// Ket qua: {1, 3, 4, 5}

// C++20: std::erase ngan gon hon
std::erase(v, 2);                    // xoa tat ca phan tu == 2
std::erase_if(v, [](int x){ return x % 2 == 0; });  // xoa theo dieu kien
```

---

## 3) Utilities Quan Trong

### Q7. `std::optional` dung khi nao?

**A:** `std::optional<T>` bieu dien mot gia tri **co the co hoac khong** — thay cho pointer hoac sentinel value.

```cpp
#include <optional>

// Thay cho "tra nullptr de bao that bai"
std::optional<int> find_user(const std::string& name) {
    if (name == "admin") return 42;
    return std::nullopt;  // khong co gia tri
}

auto result = find_user("admin");
if (result) {
    printf("Found: %d\n", *result);  // hoac result.value()
}
// Tranh:
int id = result.value_or(-1);       // -1 neu khong co

// Sai: truy cap khi rong
result = std::nullopt;
*result;         // UB!
result.value();  // throw std::bad_optional_access
```

---

### Q8. `std::variant` la gi? Khac `union` the nao?

**A:** `std::variant<A,B,C>` la **type-safe union** — luu mot trong nhieu kieu, biet kieu nao dang duoc luu.

```cpp
#include <variant>

std::variant<int, double, std::string> v;
v = 42;         // luu int
v = 3.14;       // luu double, int bi bo
v = "hello";    // luu string

// Truy cap
std::get<std::string>(v);    // OK
std::get<int>(v);            // throw std::bad_variant_access!

// An toan:
if (auto* p = std::get_if<std::string>(&v)) {
    printf("%s\n", p->c_str());
}

// std::visit - pattern matching
std::visit([](auto&& val) {
    using T = std::decay_t<decltype(val)>;
    if constexpr (std::is_same_v<T, int>)
        printf("int: %d\n", val);
    else if constexpr (std::is_same_v<T, std::string>)
        printf("string: %s\n", val.c_str());
}, v);
```

**Khac `union`:**
| | `union` | `variant` |
|---|---|---|
| Type safety | Khong (UB neu truy cap sai kieu) | Co (exception hoac nullopt) |
| Destructor | Khong tu goi | Tu goi khi switch kieu |
| Biet kieu hien tai | Phai tu track | Co `index()` va `holds_alternative` |

---

### Q9. `std::string_view` dung de lam gi?

**A:** `string_view` la **non-owning reference** den chuoi — khong copy, khong allocate.

```cpp
#include <string_view>

// TRUOC: ham nhan const string& buoc copy neu truyen const char*
void old_func(const std::string& s);
old_func("hello");  // Tao temporary string -> heap allocation!

// SAU: string_view khong copy
void new_func(std::string_view sv);
new_func("hello");          // OK, khong copy
new_func(some_string);      // OK, khong copy
new_func(buf, len);         // OK, tu buffer + len

// Cac thao tac khong copy:
std::string_view sv = "Hello, World!";
sv.substr(7, 5);    // tra ve string_view, khong copy
sv.find("World");   // O(n) search
sv[0];              // 'H'
```

**Luu y quan trong:**
```cpp
// Khong duoc tra string_view tro vao local string!
std::string_view dangerous() {
    std::string local = "hello";
    return local;   // string_view tro vao local da bi destroy -> dangling!
}
```

---

### Q10. `std::span` (C++20) la gi?

**A:** `span<T>` la **non-owning view** tren contiguous sequence — giong string_view nhung cho bat ky T.

```cpp
#include <span>

void process(std::span<int> data) {  // nhan array, vector, hay bat ky contiguous
    for (int& x : data) x *= 2;
}

int arr[] = {1, 2, 3, 4};
std::vector<int> vec = {1, 2, 3};

process(arr);         // OK
process(vec);         // OK
process({arr, 2});    // chi xu ly 2 phan tu dau
```

---

## 4) Move Semantics va STL

### Q11. Tai sao `std::move` quan trong voi containers?

**A:** `std::move` cho phep container **lay ownership** thay vi copy — O(1) thay vi O(n).

```cpp
std::vector<std::string> words;
std::string s = "a very long string that would be expensive to copy";

words.push_back(s);             // COPY: O(n)
words.push_back(std::move(s));  // MOVE: O(1), s bay gio rong

// Tuong tu voi container itself:
std::vector<int> a = {1, 2, 3, 4, 5};
std::vector<int> b = std::move(a);  // O(1), a bay gio rong
```

---

## Flash card

| Cau hoi | Tra loi nhanh |
|---|---|
| `vector` vs `list`? | vector: cache-friendly, O(1) random; list: O(1) insert bat ky |
| `map` vs `unordered_map`? | map: sorted, O(log n); unordered: O(1), no order |
| Erase-remove idiom? | `v.erase(remove(v.begin(),v.end(),x), v.end())` |
| `emplace_back` tot hon vi? | In-place construct, tranh copy/move |
| `string_view` uu diem? | Non-owning, khong copy, nhanh hon |
| `optional` dung khi? | Gia tri co the khong co, thay nullptr |
| `variant` vs `union`? | variant type-safe, tu goi dtor |
| Iterator invalidation khi? | vector: khi realloc; map: chi xoa node do |
| `lower_bound` tra ve gi? | Iterator toi phan tu dau tien >= value |
| `span` dung khi? | Non-owning view tren contiguous data |
