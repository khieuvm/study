# 03 - C++ Memory Management

---

## 1) Stack vs Heap

### Q1. Stack va Heap khac nhau the nao? Khi nao dung cai nao?

**A:**

| Dac diem | Stack | Heap |
|---|---|---|
| Quan ly boi | Compiler tu dong | Lap trinh vien (hoac allocator) |
| Toc do cap phat | O(1) — chi dich con tro | Cham hon (tim block trong) |
| Kich thuoc | Gioi han (thuong 1-8 MB) | Rat lon (gioi han RAM) |
| Lifetime | Theo scope | Tu khi malloc/new den free/delete |
| Fragmentation | Khong | Co the xay ra |

```cpp
void foo() {
    int x = 10;             // stack: tu giai phong khi ra khoi ham
    int arr[100];           // stack: 400 byte tren stack
    int* p = new int(10);   // heap: ton tai sau khi ham ket thuc
    delete p;               // phai giai phong thu cong
}
```

**Khi nao dung heap:**
- Object co lifetime vuot ngoai scope hien tai
- Kich thuoc qua lon cho stack
- Kich thuoc chua biet tai compile time
- Can polymorphism qua pointer

**Stack overflow xay ra khi:**
- De quy qua sau
- Cap phat array qua lon tren stack
```cpp
void bad() {
    int huge[10000000];  // 40MB tren stack -> crash
}
```

---

### Q2. `new`/`delete` khac `malloc`/`free` the nao?

**A:**

| | `malloc`/`free` | `new`/`delete` |
|---|---|---|
| Nguon goc | C standard library | C++ operator |
| Constructor/Destructor | KHONG goi | **Co goi** |
| Kieu tra ve | `void*` (phai cast) | Kieu chinh xac |
| Loi | Tra ve `NULL` | Throw `std::bad_alloc` |
| Realloc | `realloc()` | Khong co truc tiep |

```cpp
// malloc: chi cap phat memory, KHONG goi constructor
Foo* p = (Foo*)malloc(sizeof(Foo));  // Foo chua duoc khoi tao!
free(p);                              // KHONG goi ~Foo

// new: cap phat + goi constructor
Foo* p = new Foo();   // cap phat + Foo::Foo()
delete p;             // ~Foo() + giai phong

// KHONG duoc tron:
Foo* p = new Foo();
free(p);     // UB: goi free tren bo nho cua new
```

**`new[]` va `delete[]`:**
```cpp
int* arr = new int[10];
delete[] arr;   // phai dung delete[], khong phai delete
// delete arr;  // UB: chi destroy 1 phan tu, leak 9 phan tu con lai
```

---

### Q3. Memory layout cua mot process trong Linux?

**A:**
```
High address
+------------------+
|      Stack       |  <- grow xuong, local vars, function frames
+------------------+
|        |         |
|        v         |  (stack grow down)
|        ^         |  (heap grow up)
|        |         |
+------------------+
|       Heap       |  <- dynamic allocation (malloc, new)
+------------------+
|  BSS segment     |  <- global/static uninitialized vars (zero-init)
+------------------+
|  Data segment    |  <- global/static initialized vars
+------------------+
|  Text segment    |  <- code (read-only)
+------------------+
Low address
```

```cpp
int g_uninit;           // BSS
int g_init = 42;        // Data segment
const char* msg = "hi"; // Text segment (string literal)

void foo() {
    int local = 1;      // Stack
    int* p = new int;   // p tren Stack, *p tren Heap
}
```

---

## 2) Smart Pointers

### Q4. `unique_ptr` la gi? Khi nao dung?

**A:** `unique_ptr` the hien **exclusive ownership** — chi co 1 owner, khi owner bi destroy thi resource duoc giai phong tu dong.

```cpp
#include <memory>

// Tao
auto p = std::make_unique<int>(42);     // preferred
auto p2 = std::unique_ptr<int>(new int(42));  // OK nhung verbose

// Truy cap
*p = 100;
p->member;   // voi struct/class

// Transfer ownership (move, khong copy)
auto p2 = std::move(p);   // p bay gio la nullptr, p2 so huu
if (p) { ... }            // check truoc khi dung

// Release ownership
int* raw = p.release();   // p = nullptr, ban phai tu free(raw)
p.reset();                // giai phong ngay lap tuc
p.reset(new int(5));      // giai phong cu, nhan moi
```

**Truyen vao ham:**
```cpp
// Chi muon dung, khong transfer ownership -> dung raw pointer hoac reference
void use(const int* p);
void use(int& ref);

// Muon transfer ownership -> dung unique_ptr by value
void take(std::unique_ptr<int> p);

// Muon co the transfer hoac khong -> unique_ptr&
void maybe_take(std::unique_ptr<int>& p);
```

**Custom deleter:**
```cpp
auto file = std::unique_ptr<FILE, decltype(&fclose)>(
    fopen("data.txt", "r"), fclose
);
```

---

### Q5. `shared_ptr` hoat dong nhu the nao? Chi phi la bao nhieu?

**A:** `shared_ptr` dung **reference counting** — moi lan copy tang count, khi count ve 0 thi giai phong.

```cpp
auto p1 = std::make_shared<int>(42);  // count = 1
auto p2 = p1;                          // count = 2
{
    auto p3 = p1;                      // count = 3
}  // p3 bi destroy, count = 2
p2.reset();                            // count = 1
// p1 bi destroy -> count = 0 -> giai phong
```

**Control block cua shared_ptr:**
```
+------------------+
| reference count  |  (atomic int)
| weak count       |  (atomic int)
| deleter          |
| allocator        |
+------------------+
        ^
        | (2 pointers trong shared_ptr)
p1 -> [ptr to object] [ptr to control block]
```

**Chi phi:**
- Moi `shared_ptr`: 2 pointers (16 byte tren 64-bit)
- Moi `make_shared`: 1 allocation (object + control block cung nhau)
- Copy/destroy: atomic increment/decrement (expensive tren multi-core)
- Khong free ngay khi count = 0 neu con `weak_ptr` (chi free object)

**`make_shared` vs `new`:**
```cpp
// BAD: 2 allocations rieng re
shared_ptr<Foo> p(new Foo());

// GOOD: 1 allocation (object + control block cung nhau)
auto p = std::make_shared<Foo>();
```

---

### Q6. `weak_ptr` dung de lam gi? Giai quyet van de gi?

**A:** `weak_ptr` la **non-owning reference** den shared_ptr — khong tang reference count. Dung de phá vong **circular reference**.

**Van de circular reference:**
```cpp
struct Node {
    std::shared_ptr<Node> next;  // count se khong bao gio ve 0
    std::shared_ptr<Node> prev;  // LEAK!
};
auto a = make_shared<Node>();
auto b = make_shared<Node>();
a->next = b;
b->prev = a;  // circular: a va b giu nhau, count luon >= 1
```

**Giai phap voi weak_ptr:**
```cpp
struct Node {
    std::shared_ptr<Node> next;
    std::weak_ptr<Node>   prev;  // khong tang count
};

// Dung weak_ptr: phai lock() truoc khi dung
void use_prev(Node* n) {
    if (auto prev = n->prev.lock()) {  // tra ve shared_ptr, hoac nullptr
        // prev van con song
    }
    // Neu object da bi destroy, lock() tra ve nullptr
}
```

**Ung dung pho bien:**
- Observer pattern (observer co the bi destroy truoc subject)
- Cache (muon giu object neu ai do dang dung, giai phong neu khong)
- Parent pointer trong tree structure

---

### Q7. Khi nao dung `unique_ptr` vs `shared_ptr`?

**A:** **Quy tac nguyen tac: luon bat dau voi `unique_ptr`, chi upgrade len `shared_ptr` khi can thiet.**

```
unique_ptr  <- mac dinh, ro rang ownership, khong overhead
    |
    v (khi can shared ownership)
shared_ptr  <- nhieu owner, reference counting overhead
    |
    v (non-owning reference den shared_ptr)
weak_ptr    <- tranh circular ref, cache, observer
```

**Khi nao shared_ptr:**
- Object can duoc chia se giua nhieu noi, lifetime khong ro rang
- Callback, event handler giu tham chieu den object
- Recursive data structure (tree, graph) voi shared nodes

---

### Q8. Dangling pointer va use-after-free la gi?

**A:** **Dangling pointer**: pointer tro den memory da duoc giai phong. **Use-after-free**: dung dangling pointer -> UB.

```cpp
int* p = new int(42);
delete p;           // giai phong
*p = 100;           // USE-AFTER-FREE: UB!
                    // Co the crash, hoac lam viec "binh thuong" (nguy hiem)

// FIX: set ve nullptr sau khi delete
delete p;
p = nullptr;
if (p) *p = 100;  // safe

// Hoac dung smart pointer
auto p = make_unique<int>(42);
// Khong the use-after-free vi p tu dong = nullptr sau khi reset/out-of-scope
```

**Double free:**
```cpp
int* p = new int(42);
delete p;
delete p;  // double free: UB, co the corrupt heap, crash
```

---

## 3) Memory Errors va Tools

### Q9. Cac loai memory error pho bien nhat?

**A:**

| Loai loi | Vi du | Cong cu phat hien |
|---|---|---|
| Buffer overflow | `arr[10]` voi `arr[5]` | ASan |
| Use-after-free | Dung sau `delete` | ASan |
| Double free | `delete` 2 lan | ASan |
| Memory leak | Quen `delete` | ASan leak detector, Valgrind |
| Uninitialized read | `int x; use(x);` | MSan, Valgrind |
| Stack overflow | De quy qua sau | OS (SIGSEGV) |
| Heap corruption | Ghi sai vao heap metadata | ASan |

**Chay voi sanitizers:**
```bash
# AddressSanitizer (ASan) - phat hien hau het memory error
g++ -fsanitize=address -fno-omit-frame-pointer -g -O1 -o prog prog.cpp
./prog

# MemorySanitizer (MSan) - phat hien uninitialized reads
g++ -fsanitize=memory -g -O1 -o prog prog.cpp

# Valgrind - cham hon nhung khong can recompile
valgrind --leak-check=full ./prog
```

---

### Q10. Placement new la gi?

**A:** Placement new cho phep **construct object tai mot vung nho cho truoc** — khong cap phat them memory.

```cpp
char buf[sizeof(Foo)];
Foo* p = new (buf) Foo(42);  // construct Foo trong buf
// ...
p->~Foo();                   // phai goi destructor thu cong (khong dung delete!)

// Ung dung thuc te:
// 1. Custom allocator (pool, arena)
// 2. Shared memory
// 3. std::optional, std::variant internals

// Vi du pool allocator don gian:
struct Pool {
    alignas(alignof(std::max_align_t)) char buf[4096];
    size_t pos = 0;

    template<typename T, typename... Args>
    T* construct(Args&&... args) {
        void* ptr = buf + pos;
        pos += sizeof(T);
        return new (ptr) T(std::forward<Args>(args)...);
    }
};
```

---

## 4) Allocators

### Q11. Custom allocator trong C++ dung de lam gi?

**A:** STL containers co the nhan **custom allocator** de kiem soat cach cap phat memory.

```cpp
// Allocator interface (simplified C++17):
template<typename T>
struct MyAllocator {
    using value_type = T;

    T* allocate(std::size_t n) {
        return static_cast<T*>(::operator new(n * sizeof(T)));
    }
    void deallocate(T* p, std::size_t) noexcept {
        ::operator delete(p);
    }
};

// Dung voi container:
std::vector<int, MyAllocator<int>> v;
```

**Ung dung thuc te:**
- Pool allocator: tranh fragmentation, giam overhead
- Stack allocator: cap phat tren stack (ultra-fast, zero overhead)
- Logging allocator: debug memory usage
- Shared memory allocator: chia se giua processes

---

## Flash card

| Cau hoi | Tra loi nhanh |
|---|---|
| `new` vs `malloc`? | `new` goi ctor/dtor, throw exception; `malloc` khong |
| `delete` vs `delete[]`? | `delete[]` cho array, thieu se UB |
| `make_shared` tot hon `new` vi? | 1 allocation thay vi 2 |
| `weak_ptr` dung khi nao? | Circular reference, observer, cache |
| Dangling pointer la gi? | Pointer tro vao memory da free |
| Placement new phai don sach bang gi? | Goi destructor thu cong: `p->~T()` |
| BSS vs Data segment? | BSS: uninitialized global, Data: initialized global |
| `unique_ptr` co the share khong? | Khong, phai `move` de transfer ownership |
| ASan phat hien gi? | Buffer overflow, use-after-free, double-free, leak |
| Stack overflow thuong do? | De quy sau, local array qua lon |
