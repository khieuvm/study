# Part 4 - Bài Tập Thực Chiến

Làm trước, xem đáp án sau. Bấm giờ 25 phút mỗi bài như phỏng vấn thật.

---

### Q1. [Python task] Đoán output và giải thích — pass by reference

**A:**

Đề bài:

```python
def f(a, b, c, d):
    a = a + 1
    b.append(1)
    c = c + [1]
    d["k"] = 1

x = 0; y = []; z = []; w = {}
f(x, y, z, w)
print(x, y, z, w)
```

Đáp án: `0 [1] [] {'k': 1}`

Giải thích chuẩn:
- `a = a + 1`: `int` immutable, phép cộng tạo object mới, chỉ rebind tên local -> `x` không đổi.
- `b.append(1)`: mutate chính object -> `y` thay đổi.
- `c = c + [1]`: tạo list **mới** rồi rebind local -> `z` không đổi. (Nếu là `c += [1]` thì `z` sẽ thành `[1]` vì `__iadd__` extend tại chỗ.)
- `d["k"] = 1`: `__setitem__` mutate dict -> `w` thay đổi.

Câu kết: "Python pass by object reference — copy tham chiếu, không copy object. Mutate thì thấy, rebind thì không."

---

### Q2. [Python task] Đếm số instance đã tạo (tương đương static variable C++)

**A:**

Yêu cầu: `Dog("a"); Dog("b")` -> `Dog.total()` trả về 2; thêm `Puppy(Dog)` thì đếm chung.

```python
class Dog:
    _count = 0                      # class attribute = static member

    def __init__(self, name):
        self.name = name            # instance attribute
        Dog._count += 1             # ghi qua TÊN LỚP -> một counter duy nhất

    @classmethod
    def total(cls):
        return Dog._count

class Puppy(Dog):
    pass

Dog("a"); Puppy("b")
print(Dog.total())                  # 2
```

Những điểm interviewer chấm:
- Biết `_count = 0` đặt **trong thân class**, ngoài `__init__`.
- Biết `self._count += 1` là **SAI** (tạo instance attribute che class attribute, counter toàn cục không tăng).
- Phân biệt `Dog._count` (một counter chung) vs `type(self)._count` (mỗi subclass tự tách counter riêng khi ghi) — nếu đề bài muốn subclass đếm riêng thì dùng `type(self)`.
- Biết `@classmethod` nhận `cls` và hoạt động đúng với kế thừa.

Biến thể hay hỏi tiếp: "Đếm số instance **đang sống**" -> giảm trong `__del__` hoặc dùng `weakref.WeakSet`:

```python
import weakref

class Dog:
    _alive = weakref.WeakSet()       # không giữ sống object -> không leak
    def __init__(self, name):
        self.name = name
        Dog._alive.add(self)
    @classmethod
    def alive(cls):
        return len(Dog._alive)
```

---

### Q3. [Python task] Tìm bug trong đoạn code sau

**A:**

Đề bài:

```python
class Cart:
    items = []                          # (1)

    def add(self, item, log=[]):        # (2)
        self.items.append(item)
        log.append(item)
        return log

def apply_discount(prices):
    for p in prices:
        p = p * 0.9                     # (3)
    return prices
```

Ba bug:
1. `items = []` là class attribute mutable -> **mọi cart dùng chung giỏ hàng**. Fix: chuyển vào `__init__` thành `self.items = []`.
2. `log=[]` là mutable default -> tích lũy qua mọi lần gọi và qua mọi instance. Fix: `log=None` + `if log is None: log = []`.
3. `p = p * 0.9` chỉ rebind biến vòng lặp, `prices` không đổi. Fix: `prices[:] = [p * 0.9 for p in prices]` (mutate tại chỗ) hoặc `return [p * 0.9 for p in prices]` (thuần hàm — nên hơn).

Bản đầy đủ:

```python
class Cart:
    def __init__(self):
        self.items = []

    def add(self, item, log=None):
        log = [] if log is None else log
        self.items.append(item)
        log.append(item)
        return log

def apply_discount(prices):
    return [p * 0.9 for p in prices]
```

---

### Q4. [C task] Debug segfault này bằng gdb — kể lại từng bước

**A:**

Đề bài:

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct { char name[8]; int id; } User;

static void load(User *u, const char *raw) {
    strcpy(u->name, raw);            // (!) không kiểm tra độ dài
    u->id = atoi(raw + 9);
}

int main(void) {
    User *users = malloc(2 * sizeof(User));
    load(&users[0], "averyverylongname 42");
    printf("%s %d\n", users[0].name, users[0].id);
    free(users);
    free(users);                      // (!) double free
    return 0;
}
```

Kịch bản trả lời mẫu (nói to như đang chạy thật):

```
$ gcc -g -O0 prog.c -o prog && ./prog
Segmentation fault (core dumped)

$ gdb ./prog
(gdb) run
Program received signal SIGABRT ... in free()
(gdb) bt
#0  __GI_raise
#1  __GI_abort
#2  malloc_printerr "double free or corruption"
#3  main () at prog.c:18
```

Các bước lập luận:
1. Crash **trong `free`** -> không phải `free` có lỗi, mà là **heap metadata bị hỏng hoặc free hai lần**. Nhìn frame `main` -> thấy `free(users)` gọi hai lần -> bug 1 rõ ràng.
2. Bỏ `free` thứ hai, chạy lại: giá trị `users[0].id` sai và `users[1]` bị hỏng. Đây là "invalid data" mà không crash -> phải đi tìm nguồn.
3. `strcpy` vào `char name[8]` với chuỗi 21 ký tự -> **buffer overflow**, tràn sang `id` và sang `users[1]`. Chứng minh trong gdb:

```
(gdb) b load
(gdb) run
(gdb) p sizeof(u->name)      # 8
(gdb) p strlen(raw)          # 21  -> tràn 13 byte
(gdb) watch -l users[1]      # đặt watch rồi continue -> dừng ngay trong strcpy
(gdb) x/32xb users           # nhìn byte: thấy ASCII đè lên vùng của users[1]
```

4. Xác nhận bằng ASAN:

```
$ gcc -g -fsanitize=address prog.c -o prog && ./prog
ERROR: AddressSanitizer: heap-buffer-overflow WRITE of size 22
    #0 strcpy
    #1 load prog.c:8
 allocated by thread T0 here: main prog.c:14
```

5. Root cause: `load` tin tưởng độ dài đầu vào. Fix ở đúng tầng:

```c
static int load(User *u, const char *raw) {
    const char *sp = strchr(raw, ' ');
    if (!sp) return -1;
    size_t n = (size_t)(sp - raw);
    if (n >= sizeof u->name) return -1;        // từ chối input không hợp lệ
    memcpy(u->name, raw, n);
    u->name[n] = '\0';
    u->id = (int)strtol(sp + 1, NULL, 10);     // strtol thay atoi để báo lỗi
    return 0;
}
```

và bỏ `free` thứ hai (hoặc `free(users); users = NULL;`).

6. Chứng minh fix: chạy lại dưới ASAN sạch, thêm test với tên dài, rà soát các `strcpy` khác trong module.

Điểm mấu chốt để nói: **"Chỗ crash (`free`) không phải chỗ có bug (`strcpy`). Tôi dùng watchpoint/ASAN để chỉ ra kẻ ghi thật sự."**

---

### Q5. [C++ task] Tìm bug lifetime / use-after-free

**A:**

Đề bài:

```cpp
#include <vector>
#include <string>

const std::string& name_of(int id) {
    std::string s = "user-" + std::to_string(id);
    return s;                                  // (1)
}

void grow(std::vector<int>& v) {
    int& first = v[0];
    for (int i = 0; i < 1000; ++i) v.push_back(i);
    first = 7;                                 // (2)
}
```

1. Trả về reference tới biến **local** -> dangling reference, đọc vào là UB (thường ra chuỗi rác hoặc crash). Compiler có cảnh báo với `-Wreturn-local-addr`. Fix: trả về `std::string` theo giá trị (có RVO/move, không tốn thêm).
2. `push_back` có thể **reallocate** -> `first` trỏ vào buffer cũ đã giải phóng -> use-after-free. Mọi reference/iterator/pointer vào `vector` bị **invalidate** khi capacity tăng. Fix: dùng index (`v[0] = 7;`) hoặc `reserve` trước và chỉ rõ invariant.

Cách bắt trong thực tế: ASAN báo `heap-use-after-free` kèm stack "freed by" (chính là `push_back`); `-D_GLIBCXX_DEBUG` bắt iterator invalidation; bật `-Wall -Wextra`.

Follow-up hay hỏi: "các thao tác nào làm invalidate iterator" -> `vector`: insert/push_back (khi realloc) invalidate tất cả, erase invalidate từ vị trí xóa; `deque`: insert giữa invalidate tất cả iterator; `list`/`map`/`set`: chỉ iterator tới phần tử bị xóa; `unordered_map`: rehash invalidate iterator nhưng **không** invalidate pointer/reference tới phần tử.

---

### Q6. [Mixed task] App Python treo (hang) trên sản phẩm — điều tra thế nào?

**A:**

Không được restart ngay (mất hiện trường). Quy trình:

1. **Xác nhận treo hay chậm**: `top`/`py-spy top --pid` -> CPU 100% (vòng lặp vô hạn/GIL spin) hay 0% (chờ I/O, deadlock).
2. **Chụp stack ngay lập tức**: `py-spy dump --pid PID` — in stack **mọi thread** mà không cần sửa code, không dừng process.
3. Nếu có sẵn `faulthandler`: dùng `faulthandler.register(signal.SIGUSR1)` đã cài trước đó để in traceback theo yêu cầu.
4. **Đọc stack**: tất cả thread nằm trong `lock.acquire` -> deadlock; nằm trong `socket.recv`/`read` -> chờ I/O không có timeout (thủ phạm phổ biến nhất); nằm trong code tính toán -> vòng lặp.
5. Nếu có C extension: `gdb -p PID` rồi `thread apply all bt` + `py-bt` để thấy cả hai tầng.
6. **Thu thập thêm**: `lsof -p PID`, `ss -tnp` (kết nối đang treo), `strace -p PID` (syscall đang chờ), `cat /proc/PID/status` (số thread, trạng thái).
7. Sau khi có bằng chứng: fix bằng timeout cho mọi I/O, thứ tự lock nhất quán, dùng `queue.Queue` thay cho lock thủ công, thêm watchdog.

Câu trả lời ngắn gọn cho phỏng vấn: "Tôi dump stack tất cả thread trước, vì đó là bằng chứng duy nhất sẽ mất khi restart."

---

### Q7. [Behavioral] "Kể về một bug khó nhất bạn từng fix" — cấu trúc trả lời

**A:**

Dùng STAR nhưng **nhấn mạnh phương pháp**, vì interviewer đang đo cách bạn tư duy:

```
Situation: Sản phẩm báo crash ngẫu nhiên ~1 lần/ngày trên một dòng máy,
           không reproduce được trên máy dev.

Task:      Tôi sở hữu từ điều tra đến fix và release.

Action:    - Bật core dump trên máy khách hàng, thu thập 3 core.
           - bt cho thấy crash trong free() -> nghi heap corruption,
             không phải lỗi tại chỗ crash.
           - Chạy lại test suite với ASAN -> lộ ra heap-buffer-overflow
             tại hàm parse header, xảy ra khi trường length = 0.
           - Đọc lại spec: length = 0 là hợp lệ nhưng code giả định >= 1.
           - Đặt watchpoint xác nhận chính hàm đó ghi đè metadata.

Result:    - Fix ở tầng parse: validate length trước khi cấp phát.
           - Thêm unit test cho biên length 0/1/max và bật ASAN trong CI.
           - Zero crash trong 3 tháng sau đó; tìm thêm 2 chỗ tương tự
             trong cùng module nhờ pattern grep.

Learning:  Chỗ crash khác chỗ bug. Kể từ đó tôi luôn bật ASAN/UBSAN
           trong debug build và yêu cầu mọi bug memory phải có
           unit test kèm theo.
```

Nếu chưa có câu chuyện "xịn", hãy chuẩn bị trước 2 câu: một bug memory/crash, một bug concurrency/hiệu năng. Viết ra giấy, nói to 3 lần, mỗi câu 90 giây.

---

### Q8. [Live coding] Bộ kỹ năng tối thiểu phải gõ được không cần tra cứu

**A:**

Tự luyện bấm giờ, mỗi bài 5 phút:

```python
# 1. Doc file lon, dem tu xuat hien nhieu nhat
from collections import Counter
with open("f.txt", encoding="utf-8") as f:
    c = Counter(w.lower() for line in f for w in line.split())
print(c.most_common(3))

# 2. Group theo key
from collections import defaultdict
g = defaultdict(list)
for u in users:
    g[u["dept"]].append(u["name"])

# 3. Sort nhieu tieu chi
rows.sort(key=lambda r: (-r["score"], r["name"]))

# 4. Parse log, tinh thong ke
import re
pat = re.compile(r"^(?P<ts>\S+)\s+(?P<lvl>\w+)\s+(?P<msg>.*)$")
errs = [m["msg"] for line in lines if (m := pat.match(line)) and m["lvl"] == "ERROR"]

# 5. Retry decorator
import functools, time
def retry(times=3, delay=0.1):
    def deco(f):
        @functools.wraps(f)
        def w(*a, **kw):
            for i in range(times):
                try:
                    return f(*a, **kw)
                except Exception:
                    if i == times - 1: raise
                    time.sleep(delay * 2 ** i)
        return w
    return deco

# 6. Context manager
from contextlib import contextmanager
@contextmanager
def timed(label):
    t0 = time.perf_counter()
    try: yield
    finally: print(f"{label}: {time.perf_counter()-t0:.3f}s")

# 7. Chay lenh ngoai, lay output (KHONG dung shell=True voi input nguoi dung)
import subprocess
out = subprocess.run(["ls", "-l"], capture_output=True, text=True, check=True).stdout

# 8. JSON + argparse skeleton
import json, argparse
from pathlib import Path
p = argparse.ArgumentParser()
p.add_argument("--path", required=True)
args = p.parse_args()
data = json.loads(Path(args.path).read_text(encoding="utf-8"))
```

---

### Q9. [Kiểm tra cuối] 10 câu hỏi nhanh tự dò lại kiến thức

**A:**

1. Python truyền tham số kiểu gì? -> **pass by object reference**: mutate thấy, rebind không thấy.
2. `lst += [1]` và `lst = lst + [1]` trong hàm khác gì? -> cái đầu mutate tại chỗ (caller thấy), cái sau tạo list mới (caller không thấy).
3. Tương đương `static int count` của C++ trong Python? -> class attribute; tăng bằng `Cls.count += 1`, không bao giờ `self.count += 1`.
4. Vì sao `self.count += 1` sai? -> đọc từ class nhưng **ghi vào instance `__dict__`**, tạo bản sao riêng che class attribute.
5. `is` vs `==`? -> identity vs giá trị; `is` chỉ dùng với `None`/singleton.
6. Vì sao `def f(x, acc=[])` nguy hiểm? -> default evaluate một lần lúc def, lưu trong `f.__defaults__`.
7. RAII của Python? -> context manager `with` + `__enter__`/`__exit__`, hoặc `try/finally`.
8. Crash trong `free()` có nghĩa gì? -> heap corruption/double free; thủ phạm là code **trước đó** ghi tràn.
9. Làm sao tìm kẻ ghi đè một ô nhớ? -> `watch -l addr` trong gdb, hoặc ASAN, hoặc `rr` + `reverse-continue`.
10. Bắt đầu debug thế nào khi có stack? -> frame đầu tiên thuộc code của mình -> `info locals`/`info args` -> xác định biến sai -> truy ngược nơi tạo ra nó -> chứng minh bằng watchpoint/sanitizer -> fix tại nguồn + test.
