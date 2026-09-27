# Part 1 - Python Core (cho C/C++ Engineer)

Nền tảng object model của Python: name binding, pass-by-object-reference, class attribute vs instance attribute.
Đây là nhóm câu hỏi hay bị trượt nhất khi dân C/C++ chuyển sang Python.

> Feedback thất bại đã gặp:
> - "Failed to answer Python question of pass by reference"
> - "Failed Python task of class attribute recognizing (equivalent to C++ static variable)"

---

## ROADMAP HỌC — ưu tiên từ trên xuống (chung cho cả 4 part)

| # | Chủ đề | Part | Vì sao cần | Mục tiêu |
|---|--------|------|-----------|----------|
| 1 | Object model: name binding, `id()`, `is` vs `==` | 1 | Nền tảng của mọi câu hỏi pass-by-ref | Vẽ được sơ đồ name -> object |
| 2 | Mutable vs immutable, pass-by-object-reference | 1 | Câu hỏi phỏng vấn kinh điển | Đoán đúng output mọi snippet |
| 3 | Class attribute vs instance attribute, `@classmethod` | 1 | Tương đương `static` trong C++ | Viết được instance counter |
| 4 | Scope LEGB, closure, late binding | 1 | Bug thường gặp trong loop | Giải thích được bug và fix |
| 5 | Exception, context manager (`with`) | 1 | RAII của Python | Viết custom context manager |
| 6 | Generator / iterator | 1 | Memory + lazy pipeline | Viết generator đọc file lớn |
| 7 | Decorator, `*args/**kwargs` | 1 | Đọc được code người khác | Viết decorator đo thời gian |
| 8 | Data model: `__eq__`, `__hash__`, dataclass | 1 | Dùng dict/set đúng cách | Biết khi nào object hashable |
| 9 | Memory: refcount + GC cycle, weakref | 1 | Debug leak | Dùng `tracemalloc`, `gc` |
| 10 | GIL, threading vs multiprocessing vs asyncio | 1 | Câu hỏi senior chắc chắn có | So sánh được 3 mô hình |
| 11 | pdb / breakpoint / post-mortem | 2 | Debug Python thực chiến | Debug không cần print |
| 12 | Đọc traceback, logging, pytest `--pdb` | 2 | Làm việc hằng ngày | Tự tin trong live task |
| 13 | gdb workflow cho segfault | 3 | Điểm trượt lần trước | Có checklist thuộc lòng |
| 14 | Watchpoint, ASAN/Valgrind, core dump | 3 | Tìm nguồn dữ liệu sai | Bắt được writer phá memory |
| 15 | Debug mixed Python/C (`py-bt`, faulthandler) | 2, 3 | Vị trí hybrid | Lấy được cả 2 stack |

**Lịch gợi ý (2 tuần):** tuần 1 làm Part 1 + Part 2 (mỗi ngày 6-8 câu + gõ lại code). Tuần 2 làm Part 3 + Part 4 (mỗi ngày 1 bài thực chiến, bấm giờ 25 phút như phỏng vấn).

---

### Q1. Python chạy như thế nào? CPython, bytecode, interpreter khác gì compile C++?

**A:**

| Bước | C++ | Python (CPython) |
|------|-----|------------------|
| Source | `.cpp` | `.py` |
| Dịch | compile -> object -> link -> native binary | compile -> **bytecode** (`.pyc`, thư mục `__pycache__`) |
| Chạy | CPU chạy trực tiếp | **CPython VM** đọc bytecode, thực thi vòng lặp eval |
| Type check | compile time (static) | runtime (dynamic, duck typing) |
| Lỗi | nhiều lỗi bắt lúc compile | hầu hết lỗi chỉ nổ lúc runtime |

Xem bytecode:

```python
import dis
def add(a, b):
    return a + b
dis.dis(add)
# LOAD_FAST a / LOAD_FAST b / BINARY_OP + / RETURN_VALUE
```

Ý nghĩa khi debug: không có "undefined behavior" như C++, nhưng **lỗi chỉ lộ ra khi dòng code đó được chạy** -> test coverage và logging quan trọng hơn nhiều.

---

### Q2. "Everything is an object" nghĩa là gì? Biến trong Python khác biến trong C++ ra sao?

**A:**

Trong C++, `int x = 5;` là **một ô nhớ** tên `x` chứa giá trị 5. Gán lại `x = 7` ghi đè ô nhớ đó.

Trong Python, `x = 5` tạo object `int(5)` trên heap và **bind tên `x` vào object đó**. Tên chỉ là một nhãn (label) trong namespace (dict).

```python
x = 5
y = x        # y trỏ vào CÙNG object
x = 7        # rebind x sang object mới, y KHÔNG đổi
print(y)     # 5
```

Sơ đồ tư duy (phải vẽ được trong phỏng vấn):

```
trước:  x ──▶ [int 5] ◀── y
sau  :  x ──▶ [int 7]     y ──▶ [int 5]
```

Mỗi object có 3 thứ: **identity** (`id()`, giống địa chỉ), **type** (`type()`), **value**. Identity và type không đổi sau khi tạo; value đổi được hay không phụ thuộc mutable/immutable.

Analogy C++: biến Python giống `std::shared_ptr<PyObject>`. Gán biến = gán con trỏ, không copy object.

---

### Q3. Python là pass by value hay pass by reference? (CÂU KINH ĐIỂN — phải trả lời chuẩn)

**A:**

**Cả hai đều sai.** Python là **pass by object reference** (còn gọi là *call by sharing*).

Cách nói an toàn nhất trong phỏng vấn:

> "Python truyền **giá trị của tham chiếu** — tức là copy cái con trỏ, không copy object. Hàm nhận được một tên mới trỏ vào cùng object. Vì vậy **mutate object thì caller thấy được**, nhưng **rebind tên thì caller không thấy**. Hành vi quan sát được giống C++ khi ta truyền `T* const p` — sửa `*p` thì thấy, gán `p = ...` thì không."

Chứng minh bằng 3 case:

```python
def rebind(lst):
    lst = [99]          # chỉ đổi nhãn local -> caller KHÔNG thấy
def mutate(lst):
    lst.append(99)      # đổi chính object -> caller THẤY
def rebind_immutable(n):
    n += 1              # int immutable -> luôn tạo object mới -> caller KHÔNG thấy

a = [1]; rebind(a);           print(a)  # [1]
b = [1]; mutate(b);           print(b)  # [1, 99]
c = 1;   rebind_immutable(c); print(c)  # 1
```

Bảng quyết định:

| Trong hàm bạn làm gì | Caller có thấy không |
|----------------------|----------------------|
| `x = ...` (rebind tên) | KHÔNG |
| `x.append(...)`, `x[0] = ...`, `x.attr = ...`, `x.update(...)` | CÓ (nếu object mutable) |
| `x += ...` với list (in-place `__iadd__`) | CÓ |
| `x = x + ...` với list | KHÔNG |
| Bất kỳ thao tác nào trên `int/str/tuple/frozenset` | KHÔNG (immutable) |

Bẫy cực kinh điển `+=` vs `= +`:

```python
def f(lst): lst += [1]      # gọi list.__iadd__ -> extend TẠI CHỖ -> caller thấy
def g(lst): lst = lst + [1] # tạo list mới rồi rebind -> caller không thấy
```

Muốn "trả về" giá trị cho caller một cách tường minh: `return` giá trị mới, hoặc truyền một container mutable (list/dict/object) rồi mutate nó. Không có `&` hay `*` như C++.

---

### Q4. Mutable vs immutable — liệt kê và vì sao quan trọng?

**A:**

| Immutable | Mutable |
|-----------|---------|
| `int`, `float`, `bool`, `str`, `bytes`, `tuple`, `frozenset`, `None`, `range` | `list`, `dict`, `set`, `bytearray`, hầu hết object tự định nghĩa |

Quan trọng vì:
- Quyết định hàm có "sửa được" đối số hay không (Q3).
- Chỉ immutable/hashable mới làm key của `dict` hoặc phần tử `set`.
- Immutable an toàn khi chia sẻ giữa threads, dùng làm default argument.

Bẫy: tuple immutable nhưng có thể chứa phần tử mutable.

```python
t = ([1], 2)
t[0].append(9)   # OK -> ([1, 9], 2)
t[0] = [9]       # TypeError
t = ([1], 2); hash(t)   # TypeError: unhashable (vì chứa list)
```

---

### Q5. Viết hàm mutate object truyền vào — các cách đúng và các bẫy (TASK HAY RA)

**A:**

Đề bài kiểu: "viết hàm sửa nội dung list/dict/object mà caller thấy được".

```python
def add_item(lst, item):
    lst.append(item)              # đúng

def clear_and_fill(lst, values):
    lst[:] = values               # đúng: slice assignment = ghi tại chỗ
    # lst = list(values)          # SAI: chỉ rebind local

def bump(d, key):
    d[key] = d.get(key, 0) + 1    # đúng với dict

class Counter:
    def __init__(self): self.n = 0

def tick(c):
    c.n += 1                      # đúng: sửa attribute của object
    # c = Counter()               # SAI: rebind
```

Với object tự định nghĩa, `c.n += 1` **là** mutation vì nó dịch thành `c.n = c.n + 1` -> `setattr(c, 'n', ...)` -> sửa `c.__dict__`. Khác hẳn `n += 1` trên biến local.

Bẫy cuối cùng hay bị hỏi: sửa list **trong khi đang duyệt**.

```python
xs = [1, 2, 3, 4]
for x in xs:
    if x % 2 == 0:
        xs.remove(x)   # BUG: bỏ sót phần tử (index trượt)
# Đúng: xs[:] = [x for x in xs if x % 2]
```

---

### Q6. `is` vs `==` khác nhau thế nào? Vì sao `256 is 256` True mà `1000 is 1000` có thể False?

**A:**

- `==` gọi `__eq__`: so sánh **giá trị**.
- `is`: so sánh **identity** (cùng object, tương đương so sánh địa chỉ trong C++).

```python
a = [1, 2]; b = [1, 2]
a == b   # True
a is b   # False
```

CPython cache sẵn object `int` trong khoảng `[-5, 256]` và intern một số string -> `a = 256; b = 256; a is b` cho `True`. Với `1000` thì tùy cách compile (cùng một dòng code có thể được constant-folded nên vẫn True; hai dòng khác nhau thường False). **Đây là chi tiết implementation, không bao giờ được dựa vào.**

Quy tắc: chỉ dùng `is` với singleton: `None`, `True`, `False`, sentinel object riêng.

```python
if x is None: ...        # đúng
if x == None: ...        # sai phong cách, có thể bị __eq__ ghi đè làm sai
```

---

### Q7. Shallow copy vs deep copy?

**A:**

```python
import copy
orig = [[1, 2], [3, 4]]

s1 = orig[:]                 # shallow
s2 = list(orig)              # shallow
s3 = copy.copy(orig)         # shallow
d  = copy.deepcopy(orig)     # deep

s1[0].append(99)
print(orig)   # [[1, 2, 99], [3, 4]]  <- inner list dùng chung
d[1].append(77)
print(orig)   # không đổi
```

Shallow copy = copy container ngoài, **chia sẻ các object bên trong** (giống copy mảng con trỏ trong C++). Deep copy = đệ quy copy tất cả, xử lý cả cycle, nhưng chậm và có thể phá vỡ invariant (socket, file handle, lock). Muốn kiểm soát: implement `__copy__` / `__deepcopy__`.

---

### Q8. Bẫy mutable default argument — vì sao xảy ra và fix thế nào?

**A:**

```python
def append_to(item, target=[]):    # BUG
    target.append(item)
    return target

append_to(1)   # [1]
append_to(2)   # [1, 2]  <- vẫn là list cũ!
```

Nguyên nhân: **default value được evaluate MỘT LẦN lúc định nghĩa hàm**, rồi lưu trong `func.__defaults__` — không phải mỗi lần gọi. Kiểm chứng: `print(append_to.__defaults__)`.

Fix chuẩn:

```python
def append_to(item, target=None):
    if target is None:
        target = []
    target.append(item)
    return target
```

Cùng bản chất với "class attribute bị chia sẻ" ở Q10 — đều là **object sống lâu hơn kỳ vọng**.

---

### Q9. Class attribute vs instance attribute — tương đương `static` trong C++? (CÂU ĐÃ TỪNG TRƯỢT)

**A:**

```python
class Dog:
    count = 0                  # CLASS attribute ~ static member C++, chia sẻ mọi instance

    def __init__(self, name):
        self.name = name       # INSTANCE attribute, riêng từng object
        Dog.count += 1         # phải dùng Dog.count (hoặc type(self).count)

a = Dog("Rex"); b = Dog("Max")
print(Dog.count, a.count, b.count)   # 3 giá trị đều = 2
```

Cơ chế tìm attribute khi đọc `obj.x`:

```
1. type(obj).__mro__ có data descriptor tên x?  -> dùng nó
2. obj.__dict__['x']            -> instance attribute
3. type(obj).__dict__['x'] và các lớp cha (MRO) -> class attribute
4. __getattr__                  -> nếu có
5. AttributeError
```

Khi **ghi** `obj.x = v` thì **luôn** ghi vào `obj.__dict__` (trừ khi có data descriptor / `__slots__`) -> tạo ra instance attribute che mất class attribute. Đây là bẫy chết người:

```python
a.count += 1        # = a.count (đọc class attr = 2) + 1 rồi GHI vào a.__dict__
print(a.count, Dog.count, b.count)   # 3 2 2  <- a có bản sao riêng!
print(a.__dict__)                    # {'name': 'Rex', 'count': 3}
del a.count                          # xóa shadow -> a.count quay lại 2
```

So sánh với C++:

| C++ | Python |
|-----|--------|
| `static int count;` + định nghĩa ngoài lớp | `count = 0` trong thân class |
| `Dog::count++` | `Dog.count += 1` hoặc `cls.count += 1` |
| `static` method không có `this` | `@staticmethod` (không `self`/`cls`) |
| không có tương đương trực tiếp | `@classmethod` (nhận `cls`, kế thừa đúng lớp con) |
| gán qua instance `d.count = 5` vẫn sửa static | gán qua instance **tạo bản sao riêng** (khác biệt lớn nhất!) |

Cách viết an toàn (nên dùng khi làm task trên bảng):

```python
class Dog:
    _count = 0

    def __init__(self, name):
        self.name = name
        type(self)._count += 1     # dùng lớp thật -> subclass có counter riêng nếu khai báo lại

    @classmethod
    def total(cls):
        return cls._count

    def __del__(self):
        type(self)._count -= 1     # lưu ý: __del__ không đảm bảo thời điểm
```

Câu hỏi follow-up hay gặp: "Nếu `Puppy(Dog)` và `Puppy` không khai báo `_count` thì sao?" -> `Puppy._count += 1` sẽ **đọc** từ `Dog` nhưng **ghi** vào `Puppy.__dict__`, từ đó `Puppy` có counter riêng bắt đầu từ giá trị kế thừa. Muốn đếm chung thì luôn dùng `Dog._count` tường minh.

---

### Q10. Vì sao class attribute kiểu mutable lại nguy hiểm?

**A:**

```python
class Team:
    members = []             # BUG: một list duy nhất cho mọi instance

t1 = Team(); t2 = Team()
t1.members.append("A")       # mutate, KHÔNG rebind -> không tạo bản sao
print(t2.members)            # ['A']
```

Vì `append` là mutation nên quy tắc "ghi thì tạo instance attribute" không áp dụng — ta chỉ *đọc* `t1.members` rồi sửa object dùng chung.

Fix: khởi tạo trong `__init__`.

```python
class Team:
    def __init__(self):
        self.members = []
```

Quy tắc trí nhớ: **class attribute chỉ dùng cho constant, config, counter. Mọi state mutable phải nằm trong `__init__`.**

---

### Q11. `self`, `@classmethod`, `@staticmethod` khác nhau thế nào?

**A:**

```python
class C:
    tag = "base"

    def inst(self):        return f"instance {self}"
    @classmethod
    def cm(cls):           return f"class {cls.tag}"    # cls = lớp THỰC TẾ khi gọi
    @staticmethod
    def sm(x):             return x * 2                 # không nhận self/cls

class D(C):
    tag = "derived"

C.cm()   # 'class base'
D.cm()   # 'class derived'   <- đây là lý do classmethod hơn staticmethod
```

- `self` không phải keyword, chỉ là quy ước; Python tự truyền instance vào tham số đầu (bound method).
- `@classmethod` hay dùng làm **alternative constructor**: `datetime.fromtimestamp`, `cls.from_json(...)`.
- `@staticmethod` chỉ là hàm đặt trong namespace của class.

---

### Q12. `__dict__` và `__slots__`?

**A:**

Mỗi instance bình thường có một `dict` lưu attribute -> linh hoạt nhưng tốn bộ nhớ (~56 byte + hash table) và chậm hơn.

```python
class P:
    __slots__ = ("x", "y")     # cấp phát slot cố định, không có __dict__
    def __init__(self, x, y):
        self.x, self.y = x, y

p = P(1, 2)
p.z = 3        # AttributeError
```

Dùng `__slots__` khi tạo hàng triệu object nhỏ (giống `struct` chặt trong C++): tiết kiệm 30-50% RAM, truy cập nhanh hơn. Đánh đổi: không thêm attribute động, phải khai báo lại trong subclass, một số thư viện (pickle cũ, weakref nếu không khai báo) cần lưu ý.

---

### Q13. LEGB scope, `global`, `nonlocal`?

**A:**

Thứ tự tìm tên: **L**ocal -> **E**nclosing -> **G**lobal (module) -> **B**uiltins.

```python
x = "global"
def outer():
    x = "enclosing"
    def inner():
        nonlocal x          # trỏ vào biến của outer
        x = "changed"
    inner()
    return x                # 'changed'
```

Bẫy kinh điển:

```python
count = 0
def f():
    count += 1              # UnboundLocalError!
```

Chỉ cần **gán** tên trong hàm là Python coi tên đó là local cho cả hàm -> đọc trước khi gán thì lỗi. Fix: `global count` (tránh) hoặc tốt hơn là truyền/`return` giá trị, hoặc bọc trong class.

Khác C++: Python **không có block scope**. Biến khai trong `if`/`for` vẫn sống sau khi ra khỏi block.

---

### Q14. Closure và bug late binding trong vòng lặp?

**A:**

```python
fs = [lambda: i for i in range(3)]
print([f() for f in fs])       # [2, 2, 2]  <- không phải [0, 1, 2]
```

Closure trong Python bắt **biến** chứ không bắt **giá trị** (giống capture by reference trong C++ lambda `[&]`). Khi các lambda được gọi, `i` đã bằng 2.

Fix 1 — bắt giá trị bằng default argument (giống capture by value `[=]`):

```python
fs = [lambda i=i: i for i in range(3)]     # [0, 1, 2]
```

Fix 2 — dùng factory:

```python
def make(i):
    return lambda: i
fs = [make(i) for i in range(3)]
```

Bug này rất hay xuất hiện với callback, `functools.partial`, `Thread(target=...)`.

---

### Q15. Decorator là gì? Viết một decorator đo thời gian.

**A:**

Decorator = hàm nhận hàm, trả về hàm (higher-order function). `@d` chỉ là đường cú pháp cho `f = d(f)`.

```python
import functools, time

def timed(func):
    @functools.wraps(func)            # giữ __name__, __doc__, __wrapped__
    def wrapper(*args, **kwargs):
        t0 = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            print(f"{func.__name__} took {time.perf_counter() - t0:.3f}s")
    return wrapper

@timed
def work(n):
    return sum(range(n))
```

Thiếu `functools.wraps` -> `work.__name__` thành `'wrapper'`, phá hỏng log/doc/introspection và làm traceback khó đọc. Decorator có tham số cần thêm một lớp hàm nữa (`def retry(times): def deco(f): ...`).

Ứng dụng debug: log input/output, retry, cache (`functools.lru_cache`), đo thời gian, kiểm tra quyền.

---

### Q16. Generator và `yield` — khác gì trả về list?

**A:**

```python
def read_lines(path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            yield line.rstrip("\n")      # lazy: mỗi lần chỉ giữ 1 dòng

total = sum(1 for _ in read_lines("huge.log"))   # RAM O(1)
```

- Gọi generator function **không chạy thân hàm**, chỉ tạo generator object. Chỉ chạy khi `next()`.
- Giữ nguyên state giữa các lần `next()` (giống coroutine/state machine).
- Kết thúc -> `StopIteration`.
- Khác list: không index được, chỉ duyệt một lần, tiết kiệm RAM.

Pipeline kiểu Unix:

```python
lines   = read_lines("app.log")
errors  = (l for l in lines if "ERROR" in l)
codes   = (l.split()[-1] for l in errors)
```

Khi debug: generator lazy nên exception nổ ra **tại chỗ tiêu thụ**, không phải chỗ định nghĩa -> đọc traceback phải chú ý.

---

### Q17. Iterator protocol hoạt động thế nào? `for` thực chất làm gì?

**A:**

```python
for x in obj: ...
# tương đương
it = iter(obj)            # gọi obj.__iter__()
while True:
    try:    x = next(it)  # gọi it.__next__()
    except StopIteration: break
```

Tự viết:

```python
class Countdown:
    def __init__(self, n): self.n = n
    def __iter__(self):    return self          # iterable + iterator
    def __next__(self):
        if self.n <= 0: raise StopIteration
        self.n -= 1
        return self.n + 1
```

Iterable (có `__iter__`) khác iterator (có cả `__iter__` và `__next__`). `list` là iterable nhưng không phải iterator — mỗi lần `iter(list)` trả về iterator mới, nên duyệt được nhiều lần. Generator là iterator -> chỉ duyệt một lần (bug hay gặp: duyệt lần 2 được rỗng).

---

### Q18. Comprehension vs `map`/`filter`/loop?

**A:**

```python
squares = [x * x for x in range(10) if x % 2 == 0]
lookup  = {u.id: u for u in users}
uniq    = {w.lower() for w in words}
gen     = (x * x for x in range(10))        # generator expression, không tạo list
```

Ưu tiên comprehension vì rõ ràng và nhanh hơn loop `append` (bỏ append LOAD_METHOD). Dùng generator expression khi data lớn hoặc chỉ duyệt một lần. Nếu logic phức tạp (nhiều điều kiện, nested 3 tầng) thì quay lại `for` cho dễ đọc.

Lưu ý: trong Python 3, biến lặp của comprehension có **scope riêng**, không rò rỉ ra ngoài (khác Python 2).

---

### Q19. Exception: `try/except/else/finally`, EAFP vs LBYL?

**A:**

```python
try:
    f = open(path)
except FileNotFoundError as e:        # bắt cụ thể, không bắt Exception tràn lan
    log.warning("missing %s: %s", path, e)
    raise ConfigError(path) from e    # giữ nguyên chuỗi nguyên nhân
else:
    data = f.read()                   # chạy khi KHÔNG có exception
finally:
    ...                               # luôn chạy (cleanup)
```

- **EAFP** (Easier to Ask Forgiveness than Permission) là phong cách Python: cứ làm rồi bắt lỗi.
- **LBYL** (Look Before You Leap): kiểm tra trước — dễ dính race condition (file bị xóa giữa `exists()` và `open()`).

Cấm kỵ khi debug: `except: pass` và `except Exception: pass` — nuốt lỗi, xóa stack, biến bug thành im lặng. Nếu buộc phải nuốt thì tối thiểu `log.exception(...)`.

Khác C++: Python không có destructor deterministic ở mọi trường hợp -> dùng `finally` hoặc `with` để cleanup.

---

### Q20. Context manager (`with`) — RAII của Python?

**A:**

```python
class Timer:
    def __enter__(self):
        self.t0 = time.perf_counter()
        return self                      # giá trị gán cho "as"
    def __exit__(self, exc_type, exc, tb):
        self.dt = time.perf_counter() - self.t0
        return False                     # False = KHÔNG nuốt exception

with Timer() as t:
    heavy()
print(t.dt)
```

Hoặc ngắn gọn:

```python
from contextlib import contextmanager

@contextmanager
def chdir(p):
    old = os.getcwd(); os.chdir(p)
    try:
        yield
    finally:
        os.chdir(old)                    # tương đương destructor
```

So với C++ RAII: `__exit__` được đảm bảo gọi khi ra khỏi block (kể cả khi exception), giống destructor. Khác biệt: RAII gắn với **lifetime của object**, `with` gắn với **block**. Nên dùng `with` cho file, socket, lock (`threading.Lock` là context manager), transaction, mock/patch.

---

### Q21. `__eq__` và `__hash__` — khi nào object dùng được làm key của dict?

**A:**

Object hashable khi có `__hash__` và hash không đổi trong suốt đời sống. Mặc định: hash theo `id()`, `==` theo identity.

Quy tắc vàng: **`a == b` thì bắt buộc `hash(a) == hash(b)`.**

```python
class Point:
    def __init__(self, x, y): self.x, self.y = x, y
    def __eq__(self, o):  return isinstance(o, Point) and (self.x, self.y) == (o.x, o.y)
    def __hash__(self):   return hash((self.x, self.y))
    def __repr__(self):   return f"Point({self.x}, {self.y})"
```

Nếu chỉ định nghĩa `__eq__` mà quên `__hash__` -> Python set `__hash__ = None` -> object thành unhashable, `set()`/`dict` báo `TypeError`. Đây là bug hay gặp khi refactor.

Không bao giờ hash theo field mutable rồi đổi field đó sau khi đã bỏ vào dict — phần tử sẽ "mất tích".

Nhanh gọn: `@dataclass(frozen=True)` tự sinh cả `__eq__`, `__hash__`, `__repr__`.

---

### Q22. `dataclass`, `namedtuple`, dict thường — chọn cái nào?

**A:**

```python
from dataclasses import dataclass, field

@dataclass
class Job:
    id: int
    name: str
    tags: list[str] = field(default_factory=list)   # KHÔNG được = []
```

| Lựa chọn | Khi nào |
|----------|---------|
| `dict` | dữ liệu động, schema không biết trước (JSON thô) |
| `NamedTuple` | record bất biến, nhẹ, muốn unpack |
| `@dataclass` | DTO có logic nhẹ, mutable, muốn type hint |
| `@dataclass(frozen=True)` | value object, cần hashable |
| class thường | có invariant phức tạp, nhiều behavior |

`field(default_factory=list)` chính là fix cho bẫy mutable default (Q8) — dataclass sẽ raise lỗi nếu bạn viết `tags: list = []`.

---

### Q23. MRO và `super()` trong đa kế thừa?

**A:**

```python
class A:
    def hi(self): print("A")
class B(A):
    def hi(self): print("B"); super().hi()
class C(A):
    def hi(self): print("C"); super().hi()
class D(B, C): pass

D().hi()          # B C A
print(D.__mro__)  # D, B, C, A, object
```

MRO tính bằng thuật toán **C3 linearization**. `super()` không có nghĩa "lớp cha" mà là "**lớp kế tiếp trong MRO của object thực tế**" — vì vậy `B.hi` gọi sang `C.hi` dù `B` không kế thừa `C`. Đó là cơ chế làm mixin hoạt động.

Khác C++: Python không có virtual inheritance/diamond kiểu C++; mọi method đều "virtual" (dispatch động). Quy tắc: mọi lớp trong chuỗi phải gọi `super()` và chấp nhận `**kwargs` nếu muốn cooperative multiple inheritance.

---

### Q24. Python quản lý bộ nhớ như thế nào? Có memory leak không?

**A:**

Hai cơ chế:

1. **Reference counting** — mỗi object có counter; về 0 là giải phóng ngay (deterministic, giống `shared_ptr`).
2. **Cycle collector** (`gc`) — quét định kỳ để thu hồi các cụm object tham chiếu vòng (refcount không bao giờ về 0).

```python
import sys, gc
a = []
print(sys.getrefcount(a))     # +1 vì tham số của hàm
a.append(a)                   # tự tham chiếu -> cycle
del a
gc.collect()                  # collector dọn được
```

Leak vẫn xảy ra khi:
- Giữ reference ngoài ý muốn: cache/dict global, list log, `functools.lru_cache` không giới hạn.
- Closure/bound method giữ sống object (`self` trong callback, event handler không gỡ).
- Cycle có object định nghĩa `__del__` (Python < 3.4 không dọn được; nay dọn được nhưng vẫn nên tránh).
- C extension quên `Py_DECREF`.

Công cụ: `tracemalloc`, `objgraph`, `gc.get_objects()`, `weakref` để phá cycle (kiểu `weak_ptr`).

---

### Q25. GIL là gì? Khi nào dùng threading / multiprocessing / asyncio?

**A:**

**GIL** = một mutex toàn cục trong CPython, chỉ cho **một thread chạy bytecode tại một thời điểm**. Vì vậy CPU-bound multithread không nhanh lên (thậm chí chậm hơn do tranh chấp). GIL được nhả ra khi làm I/O, `time.sleep`, hoặc trong code C giải phóng GIL (numpy, zlib, `hashlib`).

| Mô hình | Dùng khi | Cơ chế |
|---------|---------|--------|
| `threading` | I/O-bound (file, socket, DB), cần chia sẻ memory | nhiều thread, 1 GIL |
| `multiprocessing` / `ProcessPoolExecutor` | CPU-bound | nhiều process, mỗi process 1 GIL, IPC qua pickle |
| `asyncio` | rất nhiều kết nối I/O đồng thời | 1 thread, event loop, cooperative |
| C extension / numpy | CPU-bound trên mảng | giải phóng GIL trong C |

Lưu ý cho C++ dev: `threading.Lock` vẫn cần thiết dù có GIL, vì GIL chỉ bảo đảm atomic ở mức bytecode — `counter += 1` là 3 bytecode nên vẫn race. Python 3.13+ có chế độ free-threaded (no-GIL) thí nghiệm -> nhắc được sẽ ghi điểm.

---

### Q26. `if __name__ == "__main__"` để làm gì? Import hoạt động ra sao?

**A:**

Khi file chạy trực tiếp, `__name__ == "__main__"`; khi bị import, `__name__` là tên module. Đặt code khởi động trong khối này để import không chạy side effect — **bắt buộc** với `multiprocessing` trên Windows (nếu không sẽ fork đệ quy).

Import: Python tìm module theo `sys.path`, chạy **một lần** rồi cache vào `sys.modules`. Import lại chỉ lấy từ cache — đây là lý do sửa code rồi import lại trong REPL không thấy đổi (phải `importlib.reload`).

Circular import: A import B, B import A -> một bên nhận module chưa khởi tạo xong (`ImportError: cannot import name`). Fix: tách phần chung ra module thứ ba, import bên trong hàm, hoặc dùng `TYPE_CHECKING` cho type hint.

---

### Q27. Type hints có tác dụng gì lúc runtime?

**A:**

**Không có** — Python không ép kiểu theo hint. Hint phục vụ: đọc code, IDE autocomplete, và static checker (`mypy`, `pyright`/Pylance).

```python
from typing import Optional, Iterable

def total(xs: Iterable[int], scale: float = 1.0) -> float:
    return sum(xs) * scale

def find(uid: int) -> Optional["User"]: ...    # hoặc User | None (3.10+)
```

Muốn validate thật sự lúc runtime: `pydantic`, hoặc tự kiểm tra. Nếu phỏng vấn hỏi "bạn đảm bảo chất lượng Python thế nào": trả lời = type hints + mypy strict + pytest + ruff/flake8 + CI.

---

## FLASH CARD — Part 1

**Python object model**
- Biến = nhãn trỏ vào object; gán = rebind, không copy.
- Pass by **object reference**: mutate thấy, rebind không thấy.
- Mutable: list, dict, set, bytearray, object. Immutable: int, float, str, tuple, frozenset, bytes, None.
- `+=` trên list = in-place; `= x + y` = tạo mới.
- `is` = identity, `==` = giá trị. `is` chỉ cho `None`.

**Class attribute**
- Trong thân class = giống `static` C++, chia sẻ mọi instance.
- Đọc: instance -> class -> MRO. Ghi qua instance **luôn** tạo instance attribute.
- Tăng counter: `Cls.count += 1` hoặc `type(self).count += 1`. Không dùng `self.count += 1`.
- Class attribute mutable (`items = []`) = bug chia sẻ — đưa vào `__init__`.
- Mutable default arg = cùng bản chất; fix bằng `=None`.

**Khác**
- Closure bắt biến, không bắt giá trị -> `lambda i=i:` để bắt giá trị.
- `with` = RAII của Python (`__enter__`/`__exit__` luôn chạy).
- `__eq__` mà quên `__hash__` -> object unhashable.
- GIL: threading cho I/O, multiprocessing cho CPU, asyncio cho nhiều kết nối.
