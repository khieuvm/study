# Part 2 - Python Debugging

Đọc traceback, pdb, post-mortem, logging, segfault trong C extension, leak và profiling.

> Feedback thất bại đã gặp:
> - "Had no idea how/where to start debugging, even after got the stack — needed a lot of hints"

---

### Q1. Đọc traceback Python thế nào cho đúng?

**A:**

```
Traceback (most recent call last):
  File "app.py", line 42, in <module>
    run(cfg)
  File "core.py", line 17, in run
    return parse(cfg["path"])
  File "core.py", line 8, in parse
    return int(raw)
ValueError: invalid literal for int() with base 10: 'abc'
```

Quy trình đọc:
1. **Đọc từ dưới lên**: dòng cuối = loại lỗi + thông điệp -> biết *chuyện gì* xảy ra.
2. Frame ngay trên cùng = **nơi nổ** (`core.py:8`).
3. Đọc ngược lên để biết **đường đi dữ liệu** — `'abc'` đến từ `cfg["path"]`, từ `app.py:42`.
4. Bỏ qua các frame thuộc thư viện/framework ở giữa, tập trung frame **code của bạn** — đó là nơi fix.
5. Nếu có `During handling of the above exception, another exception occurred` -> có 2 lỗi, đọc block **dưới** trước (lỗi thực tế), block trên là nguyên nhân gốc. Với `raise ... from e` sẽ hiện `The above exception was the direct cause`.

Câu trả lời mẫu cho interviewer: "Tôi đọc dòng cuối để biết loại lỗi, frame dưới cùng trong code của tôi để biết vị trí, rồi đi ngược lên để tìm nguồn dữ liệu sai — mục tiêu là tìm nơi dữ liệu **được tạo ra**, không phải nơi nó phát nổ."

---

### Q2. Dùng `pdb` thực chiến — cheat sheet

**A:**

Đặt breakpoint: `breakpoint()` (Python 3.7+) ngay trong code, hoặc chạy `python -m pdb app.py`.

| Lệnh | Ý nghĩa |
|------|---------|
| `l` / `ll` | xem code quanh vị trí / cả hàm |
| `n` | next (bước qua, không vào hàm) |
| `s` | step (vào hàm) |
| `r` | chạy đến khi hàm hiện tại return |
| `c` | continue |
| `until N` | chạy đến dòng N (thoát vòng lặp) |
| `b file.py:42`, `b func` | đặt breakpoint |
| `b file.py:42, x > 10` | **conditional breakpoint** |
| `tbreak` | breakpoint dùng 1 lần |
| `w` (where) | in stack trace |
| `u` / `d` | lên/xuống frame (xem biến của caller) |
| `a` | in đối số của hàm hiện tại |
| `p expr` / `pp expr` | in / pretty-print |
| `display expr` | tự in mỗi lần dừng |
| `interact` | mở REPL với namespace hiện tại |
| `q` | thoát |

Mẹo: biến trùng tên lệnh (`n`, `c`, `s`, `l`) phải in bằng `p n`. `pdb` không hợp với multithread -> dùng trong thread chính hoặc chuyển sang logging/py-spy.

---

### Q3. Debug post-mortem — khi lỗi đã xảy ra rồi thì làm sao xem lại?

**A:**

```bash
python -m pdb -c continue app.py      # chạy bình thường, nổ lỗi thì rơi vào pdb ngay tại frame lỗi
```

Trong code:

```python
import pdb, sys, traceback
try:
    main()
except Exception:
    traceback.print_exc()
    pdb.post_mortem(sys.exc_info()[2])   # hoặc chỉ pdb.pm() trong REPL
```

Với pytest: `pytest --pdb` (vào pdb khi test fail), `pytest -x --pdb -k test_parse`, `pytest -l` (in local variables trong traceback), `pytest --tb=long`.

Post-mortem mạnh vì bạn **giữ nguyên toàn bộ stack và biến tại thời điểm lỗi** — dùng `u`/`d` di chuyển frame để xem dữ liệu ban đầu từ đâu ra. Đây chính là cách trả lời "tìm nguồn dữ liệu sai".

---

### Q4. `print` vs `logging` — khi nào dùng gì?

**A:**

```python
import logging
log = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(filename)s:%(lineno)d | %(message)s",
)

log.debug("parsing %s", path)       # lazy format: không tốn chi phí nếu level cao hơn
try:
    ...
except Exception:
    log.exception("parse failed")   # tự đính kèm traceback
```

- `print` cho script/REPL ngắn; `logging` cho mọi thứ chạy lâu hoặc trên server: có level, timestamp, module, tắt bật không cần sửa code, ghi file/rotate.
- Dùng `log.debug("x=%s", x)` **không** dùng f-string để tránh format khi bị lọc bỏ.
- `log.exception` chỉ gọi trong `except`.
- Level: DEBUG (chi tiết dev) / INFO (mốc chính) / WARNING (bất thường còn chạy) / ERROR (thao tác thất bại) / CRITICAL (chết).

---

### Q5. Chương trình Python bị segfault / crash im lặng — debug thế nào?

**A:**

Segfault trong Python thuần gần như không xảy ra -> nghi ngay C extension, ctypes, đệ quy sâu, hoặc thư viện native (numpy, opencv, driver).

```bash
python -X faulthandler app.py       # in stack Python khi nhận SIGSEGV/SIGFPE/SIGABRT
```

```python
import faulthandler
faulthandler.enable()                       # in traceback khi crash
faulthandler.dump_traceback_later(30, exit=True)   # bắt treo: 30s không xong thì dump
```

Nếu là đệ quy: `RecursionError` -> `sys.setrecursionlimit` chỉ là băng phủ, phải sửa thuật toán.

Lấy cả hai stack (Python + C) bằng gdb:

```bash
gdb --args python app.py
(gdb) run
# crash
(gdb) bt            # C stack
(gdb) py-bt         # Python stack (cần python3-dbg / python-gdb.py)
(gdb) py-locals
```

Chạy dưới `valgrind`/ASAN thì đặt `PYTHONMALLOC=malloc` để tránh false positive từ pymalloc.

---

### Q6. Tìm memory leak trong Python?

**A:**

```python
import tracemalloc
tracemalloc.start(25)                 # lưu 25 frame

snap1 = tracemalloc.take_snapshot()
do_work()
snap2 = tracemalloc.take_snapshot()

for stat in snap2.compare_to(snap1, "lineno")[:10]:
    print(stat)                       # dòng code nào cấp phát tăng nhiều nhất
```

Bộ công cụ:
- `tracemalloc` — dòng nào cấp phát, so sánh snapshot (chuẩn nhất cho leak logic).
- `objgraph.show_growth()` / `show_backrefs()` — loại object nào tăng, **ai đang giữ nó**.
- `gc.get_referrers(obj)` — truy ngược người giữ reference.
- `psutil` / `RSS` — xác nhận leak thật hay chỉ là fragmentation/arena của allocator.
- `memray` — profiler bộ nhớ mạnh (có cả native allocation).

Quy trình: xác nhận RSS tăng bền vững -> chụp 2 snapshot cách nhau 1 chu kỳ -> xem top diff -> truy backrefs -> tìm reference giữ sống (thường là cache global, list log, closure).

---

### Q7. Profiling Python: tìm chỗ chậm?

**A:**

```bash
python -m cProfile -s cumtime app.py | head -40       # hàm nào tốn nhiều thời gian nhất
py-spy top --pid 1234                                 # sampling, không cần sửa code, chạy trên prod
py-spy dump --pid 1234                                # stack của MỌI thread ngay lập tức (bắt treo/deadlock)
py-spy record -o prof.svg --pid 1234                  # flamegraph
```

- `cProfile` — deterministic, chi tiết tới hàm, overhead lớn.
- `line_profiler` (`@profile` + `kernprof -l -v`) — tới từng dòng.
- `timeit` — microbenchmark đoạn nhỏ.
- `py-spy` — sampling, **đính vào process đang chạy** mà không dừng nó; vũ khí số 1 khi app trên server bị treo hoặc ăn CPU.

Thứ tự: đo trước (không đoán), tìm hotspot, kiểm tra thuật toán/độ phức tạp, rồi mới nghĩ đến vectorize (numpy), cache, hay đẩy xuống C/Cython.

---

### Q8. Debug với pytest và mock?

**A:**

```bash
pytest -x -q                    # dừng ở fail đầu tiên
pytest -k "parse and not slow"  # lọc test
pytest -l --tb=short            # in local vars, traceback gọn
pytest --pdb                    # vào debugger khi fail
pytest -s                       # không nuốt stdout (thấy print)
pytest --lf                     # chạy lại chỉ những test fail lần trước
```

```python
from unittest.mock import patch, MagicMock

def test_fetch(monkeypatch):
    monkeypatch.setattr("mymod.requests.get", lambda url, **kw: MagicMock(status_code=500))
    assert fetch("http://x") is None

@patch("mymod.time.sleep")           # patch TẠI NƠI SỬ DỤNG, không phải nơi định nghĩa
def test_retry(mock_sleep):
    ...
```

Lỗi mock hay gặp nhất: patch sai đường dẫn (phải patch `mymod.requests.get` chứ không phải `requests.get`) và quên `mock.assert_called_once_with(...)`.

---

### Q9. Những bug Python phổ biến mà C++ dev hay dính?

**A:**

| Bug | Triệu chứng | Fix |
|-----|-------------|-----|
| Mutable default arg | Kết quả "nhớ" lần gọi trước | `=None` + khởi tạo trong hàm |
| Gán qua instance để đổi class attr | Chỉ một object đổi | Dùng `Cls.attr` / `type(self).attr` |
| Late binding trong loop | Callback đều dùng giá trị cuối | `lambda i=i:` |
| `is` thay cho `==` | Sai với số lớn/string động | Chỉ dùng `is` với `None` |
| Sửa list khi đang duyệt | Bỏ sót phần tử | Duyệt bản sao hoặc tạo list mới |
| `/` vs `//` | Ra float ngoài ý muốn | `//` cho integer division |
| Shadow tên builtin/module (`list = ...`, file `random.py`) | Lỗi kỳ lạ khi import | Đổi tên |
| Không đóng file | Mất dữ liệu trên Windows | Dùng `with` |
| So sánh float `==` | Test flaky | `math.isclose` |
| `except Exception: pass` | Bug biến mất | Log + raise lại |
| Encoding mặc định khác nhau | `UnicodeDecodeError` trên Windows | Luôn `encoding="utf-8"` |
| Sửa biến global trong hàm | `UnboundLocalError` | Tránh global |

---

## FLASH CARD — Part 2

- Traceback đọc **từ dưới lên**; frame code của mình là điểm bắt đầu điều tra.
- `breakpoint()`, `python -m pdb -c continue app.py`, `pdb.post_mortem()`, `pytest --pdb -l -x`.
- Trong pdb: `w` xem stack, `u`/`d` đổi frame, `a` xem args, `b file:42, cond` breakpoint có điều kiện.
- `log.debug("x=%s", x)` (lazy) và `log.exception()` trong `except` — không dùng `print` trên server.
- Segfault -> `faulthandler`, `gdb --args python app.py` + `bt` và `py-bt`.
- Leak -> `tracemalloc` diff 2 snapshot, `objgraph.show_backrefs`, `gc.get_referrers`.
- Chậm/treo -> `py-spy top --pid`, `py-spy dump --pid` (không cần sửa code, không dừng process).
- Cấm: `except Exception: pass`.
