# 04 - STL, Algorithm, Complexity — Bilingual VI/EN

Kiến thức STL và algorithm cho phỏng vấn Senior C++.

---

## 1) Container Selection

### Q1. `vector` vs `list` — khi nào dùng cái nào?

**A:**
- EN: `vector` wins in almost all cases due to cache locality (contiguous memory). `list` only wins when you need O(1) splice or stable iterators during frequent mid-insertions with existing iterators. Even for mid-insertions, `vector` is often faster on small/medium sizes due to cache effects.
- VI: `vector` thắng gần như mọi trường hợp nhờ cache locality (bộ nhớ liên tục). `list` chỉ thắng khi cần O(1) splice hoặc iterator ổn định khi insert giữa thường xuyên với iterator có sẵn. Ngay cả insert giữa, `vector` thường nhanh hơn trên kích thước nhỏ/trung bình nhờ cache.

```cpp
// vector: default choice — contiguous, cache-friendly
std::vector<int> v = {1, 2, 3, 4, 5};

// list: rare, only for splice or iterator stability
std::list<int> l = {1, 2, 3};
auto it = l.begin(); std::advance(it, 1);
l.insert(it, 99);  // iterators to other elements remain valid
```

Follow-up (EN): What is Chandler Carruth's "vector is always faster" argument?

---

### Q2. `map` vs `unordered_map`?

**A:**
- EN: `map` (red-black tree): O(log n), sorted by key, stable iterators, requires `operator<`. `unordered_map` (hash table): O(1) average, no order, iterators invalidated on rehash, requires hash + `operator==`. Default: `unordered_map` for lookup speed; `map` when ordering or range queries needed.
- VI: `map` (red-black tree): O(log n), sorted theo key, iterator ổn định, cần `operator<`. `unordered_map` (hash table): O(1) trung bình, không thứ tự, iterator invalid khi rehash, cần hash + `operator==`. Mặc định: `unordered_map` cho tốc độ lookup; `map` khi cần thứ tự hoặc range query.

```cpp
std::unordered_map<std::string, int> fast;  // O(1) lookup
fast["key"] = 42;

std::map<std::string, int> sorted;          // O(log n), sorted
auto it = sorted.lower_bound("prefix");     // range query
```

Follow-up (EN): What happens when `unordered_map` has many hash collisions?

---

### Q3. `deque` dùng khi nào?

**A:**
- EN: When you need efficient push/pop at **both ends** plus random access. Internally: array of fixed-size blocks. Unlike `vector`, never invalidates references on `push_front`/`push_back` (unless size changes cause reallocation of the block map). Common use: `std::queue` and `std::stack` default to `deque`.
- VI: Khi cần push/pop hiệu quả ở **cả hai đầu** kèm random access. Bên trong: mảng các block cố định. Khác `vector`, không invalidate reference khi `push_front`/`push_back`. Dùng phổ biến: `std::queue` và `std::stack` mặc định dùng `deque`.

Follow-up (EN): Why doesn't `deque` guarantee contiguous memory?

---

## 2) Iterator Invalidation

### Q4. `vector::push_back` có invalidation không?

**A:**
- EN: **Yes, potentially.** If `size() == capacity()`, reallocation occurs — ALL iterators, pointers, and references are invalidated. If no reallocation, only `end()` is invalidated. Use `reserve()` to prevent unexpected invalidation.
- VI: **Có thể có.** Nếu `size() == capacity()`, reallocation xảy ra — TẤT CẢ iterator, pointer, reference đều invalid. Nếu không realloc, chỉ `end()` bị invalid. Dùng `reserve()` để tránh invalidation bất ngờ.

```cpp
std::vector<int> v = {1, 2, 3};
int* ptr = &v[0];
v.push_back(4);  // may reallocate
*ptr = 10;        // UB if reallocation happened!

v.reserve(100);
ptr = &v[0];
v.push_back(5);  // no realloc: ptr still valid (size < 100)
```

Follow-up (EN): What is the amortized O(1) guarantee of `push_back`?

---

### Q5. `list` iterator có ổn định hơn không?

**A:**
- EN: Yes. `list` iterators remain valid after insert/erase of **other** nodes. Only the iterator to the erased node itself becomes invalid. This is because each node is separately heap-allocated — no contiguous reallocation.
- VI: Có. Iterator của `list` vẫn valid sau insert/erase **node khác**. Chỉ iterator tới node bị erase mới invalid. Vì mỗi node cấp phát riêng trên heap — không có realloc liên tục.

Follow-up (EN): How does `std::list::splice` work in O(1)?

---

## 3) Algorithm

### Q6. Vì sao ưu tiên STL algorithm hơn loop thủ công?

**A:**
- EN: **(1)** Expresses intent clearly (`find`, `transform`, `accumulate` vs raw loop). **(2)** Fewer bugs (off-by-one, missing break). **(3)** Optimized implementations (vectorized, parallelized). **(4)** Composable with ranges (C++20). **(5)** Easier code review.
- VI: **(1)** Thể hiện ý định rõ ràng (`find`, `transform`, `accumulate` vs loop thô). **(2)** Ít bug hơn (off-by-one, thiếu break). **(3)** Implementation tối ưu (vectorized, parallelized). **(4)** Compose được với ranges (C++20). **(5)** Dễ code review hơn.

```cpp
// BAD: raw loop — what does this do?
int result = 0;
for (int i = 0; i < v.size(); ++i)
    if (v[i] > 0) result += v[i] * v[i];

// GOOD: algorithm — intent is clear
auto pos = v | std::views::filter([](int x){ return x > 0; })
             | std::views::transform([](int x){ return x * x; });
int result = std::accumulate(pos.begin(), pos.end(), 0);
```

Follow-up (EN): When IS a raw loop better than an algorithm?

---

### Q7. Erase-remove idiom — `remove` làm gì thực sự?

**A:**
- EN: `std::remove` does NOT erase elements from the container. It moves non-removed elements to the front and returns an iterator to the new logical end. You must call `erase()` to actually shrink the container. C++20: `std::erase(container, value)` does both in one call.
- VI: `std::remove` KHÔNG xóa phần tử khỏi container. Nó dịch phần tử còn lại về đầu và trả iterator tới vị trí kết thúc mới. Phải gọi `erase()` để thu nhỏ container thực sự. C++20: `std::erase(container, value)` làm cả hai trong một lời gọi.

```cpp
std::vector<int> v = {1, 2, 3, 2, 4, 2, 5};
// Pre-C++20:
v.erase(std::remove(v.begin(), v.end(), 2), v.end());
// C++20:
std::erase(v, 2);
```

Follow-up (EN): Why doesn't `std::remove` know about the container?

---

### Q8. `stable_sort` vs `sort`?

**A:**
- EN: `sort` (introsort): O(n log n), not stable — equal elements may be reordered. `stable_sort` (merge sort): O(n log n) with O(n) extra memory, preserves relative order of equal elements. Use `stable_sort` when relative ordering matters (e.g., sort by priority, then by name).
- VI: `sort` (introsort): O(n log n), không stable — phần tử bằng nhau có thể bị đổi chỗ. `stable_sort` (merge sort): O(n log n) với O(n) bộ nhớ thêm, giữ thứ tự tương đối của phần tử bằng nhau. Dùng `stable_sort` khi thứ tự tương đối quan trọng (VD: sort theo priority, rồi theo tên).

Follow-up (EN): What is the worst-case complexity guarantee of `std::sort`?

---

### Q9. Big-O có đủ để dự đoán tốc độ thực tế không?

**A:**
- EN: **No.** Big-O ignores constant factors, cache effects, branch prediction, and allocator cost. An O(n) linked list traversal can be slower than O(n log n) vector sort due to cache misses. Always **profile** — don't guess from complexity alone.
- VI: **Không.** Big-O bỏ qua hằng số, cache effect, branch prediction, và chi phí allocator. Duyệt O(n) trên linked list có thể chậm hơn sort O(n log n) trên vector do cache miss. Luôn **profile** — không đoán chỉ từ complexity.

Follow-up (EN): Give an example where O(n²) beats O(n log n) in practice.

---

## 4) Allocator và Memory

### Q10. Polymorphic allocator (`pmr`) có lợi ích gì?

**A:**
- EN: `std::pmr` (C++17) separates allocation policy from data structure. You can swap allocators at runtime (stack, pool, monotonic) without changing container types. Useful for: embedded systems, game engines, high-frequency trading where allocation patterns are known.
- VI: `std::pmr` (C++17) tách chính sách cấp phát khỏi cấu trúc dữ liệu. Có thể đổi allocator lúc runtime (stack, pool, monotonic) mà không đổi kiểu container. Hữu ích cho: embedded, game engine, HFT khi biết rõ pattern cấp phát.

```cpp
std::array<std::byte, 4096> buf;
std::pmr::monotonic_buffer_resource pool(buf.data(), buf.size());
std::pmr::vector<int> v(&pool);  // allocates from stack buffer
```

Follow-up (EN): What is a monotonic buffer resource?

---

### Q11. Small String Optimization (SSO) là gì?

**A:**
- EN: `std::string` stores short strings (typically ≤15 or ≤22 chars depending on implementation) **inside the object itself** — no heap allocation. This makes short string creation O(1) with zero allocator overhead. You can't rely on SSO threshold being portable.
- VI: `std::string` lưu chuỗi ngắn (thường ≤15 hoặc ≤22 ký tự tùy implementation) **bên trong chính object** — không cấp phát heap. Tạo chuỗi ngắn là O(1) không có overhead allocator. Không nên dựa vào ngưỡng SSO là portable.

Follow-up (EN): How can you check if a string is using SSO?

---

## 5) Đánh giá Senior

### Q12. Tại sao `vector<bool>` nên tránh?

**A:**
- EN: `vector<bool>` is a specialization that packs bits — it does NOT behave like a normal vector. `operator[]` returns a proxy object, not a `bool&`. You can't take address of elements. Alternatives: `vector<char>`, `std::bitset`, `boost::dynamic_bitset`.
- VI: `vector<bool>` là specialization pack bit — KHÔNG hoạt động như vector thông thường. `operator[]` trả về proxy object, không phải `bool&`. Không thể lấy địa chỉ phần tử. Thay thế: `vector<char>`, `std::bitset`, `boost::dynamic_bitset`.

```cpp
std::vector<bool> vb = {true, false, true};
auto ref = vb[0];  // NOT bool& — it's a proxy!
bool* ptr = &vb[0]; // ERROR: can't take address
```

Follow-up (EN): Why was `vector<bool>` designed this way?

---

### Q13. Khi nào nên `reserve` cho `vector`?

**A:**
- EN: When you know (or can estimate) the final size. `reserve` prevents reallocation during growth — avoids O(n) copies and iterator invalidation. Critical in performance-sensitive loops.
- VI: Khi biết (hoặc ước lượng được) kích thước cuối cùng. `reserve` ngăn reallocation khi tăng trưởng — tránh O(n) copy và iterator invalidation. Quan trọng trong loop nhạy cảm hiệu năng.

```cpp
std::vector<std::string> lines;
lines.reserve(estimated_line_count);  // one allocation
while (getline(file, line))
    lines.push_back(std::move(line));  // no reallocation
```

Follow-up (EN): What is the difference between `reserve` and `resize`?

---

### Q14. Có nên micro-optimize algorithm sớm?

**A:**
- EN: **No.** Follow the performance process: (1) write correct, readable code, (2) measure with profiler, (3) optimize **only hot spots**. Premature optimization harms readability and maintainability. The compiler handles most micro-optimizations.
- VI: **Không.** Theo quy trình hiệu năng: (1) viết code đúng, dễ đọc, (2) đo bằng profiler, (3) tối ưu **chỉ điểm nóng**. Tối ưu sớm hại khả năng đọc và bảo trì. Compiler xử lý hầu hết micro-optimization.

Follow-up (EN): What is Amdahl's Law and how does it relate to optimization?

---

### Q15. `emplace_back` luôn tốt hơn `push_back`?

**A:**
- EN: Not always. `emplace_back` constructs in-place — useful when constructing from raw arguments (avoids temporary). When you already have the object, `push_back(std::move(obj))` is equivalent. **Gotcha**: `emplace_back` can call explicit constructors that `push_back` would reject.
- VI: Không luôn. `emplace_back` construct tại chỗ — hữu ích khi construct từ argument thô (tránh temporary). Khi đã có object, `push_back(std::move(obj))` tương đương. **Bẫy**: `emplace_back` có thể gọi explicit constructor mà `push_back` từ chối.

```cpp
std::vector<std::unique_ptr<int>> v;
v.push_back(std::make_unique<int>(42));   // OK
v.emplace_back(new int(42));              // works but raw new — risky!

std::vector<std::string> vs;
vs.emplace_back(10, 'x');  // constructs string(10,'x') in-place — no copy
vs.push_back("hello");     // equally fine for existing values
```

Follow-up (EN): When can `emplace_back` cause subtle bugs with explicit constructors?

---

## Flash card (ôn nhanh)

| Câu hỏi / Question | Trả lời nhanh / Quick answer |
|---|---|
| vector vs list? | vector gần như luôn thắng nhờ cache locality |
| map vs unordered_map? | unordered_map O(1) default; map khi cần sorted |
| vector::push_back invalidation? | Nếu realloc → tất cả invalid |
| erase-remove idiom? | `remove` dịch, `erase` xóa — hoặc C++20 `std::erase` |
| stable_sort vs sort? | stable giữ thứ tự bằng nhau, tốn O(n) extra memory |
| Big-O đủ chưa? | Không — cache, branch prediction, constant factor |
| pmr lợi ích? | Tách allocation policy, swap runtime |
| SSO là gì? | Chuỗi ngắn lưu trong object, không heap |
| vector\<bool\> tránh? | Proxy object, không true reference |
| reserve khi nào? | Khi biết/ước lượng được kích thước |
| emplace_back vs push_back? | emplace construct tại chỗ, push cần object có sẵn |
