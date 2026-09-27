# Part 3 - C/C++ Debugging Thực Chiến (GDB)

Từ segfault / stack trace đi ngược về **root cause**, không chỉ làm cho hết crash.

> Feedback thất bại đã gặp:
> - "Eventually prevented the segfault but could not find the source of invalid data"
> - "Moderate troubleshooting skills, stuck with gdb and had no clue even when running inside gdb"
> - "Could not point out the root cause nor make the fix"

---

### Q1. Bạn có stack trace của một segfault. Bắt đầu từ đâu? (CHECKLIST PHẢI THUỘC)

**A:**

Nói to quy trình này trong phỏng vấn, từng bước:

1. **Đọc thông tin crash**: signal gì (SIGSEGV/SIGABRT/SIGFPE), địa chỉ lỗi. `0x0` -> null pointer. Địa chỉ nhỏ (`0x8`, `0x10`) -> null + offset field. Địa chỉ rác (`0xdeadbeef`, `0x5f5f...`) -> **con trỏ rác / use-after-free / buffer overflow**. `0xbebebebe` hoặc pattern lặp -> memory đã bị ghi đè bằng pattern.
2. **Xem stack**: `bt` (hoặc `bt full`). Tìm **frame đầu tiên thuộc code của mình** — đó là điểm xuất phát điều tra.
3. **Vào frame đó**: `frame N`, `info locals`, `info args`, `list`.
4. **Xác định biến nào sai**: in từng con trỏ/index. `p ptr`, `p *ptr`, `p obj`, `p idx`, `p vec.size()`.
5. **Hỏi: giá trị sai này đến từ đâu?** Đây là bước mà đa số người trượt. Đi ngược: ai ghi vào nó? Truyền từ hàm nào? Đọc từ file/socket nào?
6. **Chứng minh** bằng công cụ thay vì đoán:
   - `watch ptr` / `watch -l obj.field` — dừng ngay khi có ai ghi vào.
   - Chạy lại với **ASAN** (`-fsanitize=address,undefined -g -O1`) -> báo chính xác allocation nào, ai free, ai ghi tràn.
   - `valgrind --track-origins=yes` -> báo giá trị chưa khởi tạo bắt nguồn từ đâu.
   - `rr record` + `rr replay` rồi `reverse-continue` -> chạy ngược thời gian về thời điểm giá trị bị hỏng.
7. **Root cause và phân loại**: null deref / use-after-free / double free / out-of-bounds / uninitialized / race / lifetime (trả về con trỏ tới local, dangling iterator/reference).
8. **Fix ở đúng tầng**: sửa nơi tạo ra dữ liệu sai, không phải chỉ thêm `if (ptr)` ở chỗ nó crash. Nếu thêm null check, phải giải thích được **vì sao nó có thể null hợp lệ**.
9. **Chứng minh đã fix**: reproduce lại, chạy ASAN/TSAN, thêm unit test/assert cho invariant.

Câu chốt cho interviewer: **"Crash là triệu chứng tại nơi đọc; bug thường nằm ở nơi ghi. Tôi không dừng lại khi hết crash — tôi phải giải thích được tại sao dữ liệu đó tồn tại."**

---

### Q2. gdb cheat sheet — những lệnh thực sự dùng khi điều tra

**A:**

```bash
gcc -g -O0 -fno-omit-frame-pointer prog.c -o prog   # LUÔN build -g
gdb ./prog                 # hoặc: gdb --args ./prog arg1 arg2
gdb ./prog core.1234       # phân tích core dump
gdb -p 1234                # attach vào process đang chạy
```

| Nhóm | Lệnh |
|------|------|
| Chạy | `run`, `start` (break ở main), `continue`, `kill` |
| Bước | `next` / `step` / `finish` / `until` |
| Stack | `bt`, `bt full`, `frame N`, `up`, `down`, `info frame` |
| Biến | `info locals`, `info args`, `p expr`, `p/x`, `p *arr@10`, `ptype x` |
| Breakpoint | `b file.c:42`, `b func`, `b file.c:42 if i == 99`, `info b`, `delete N`, `disable N` |
| Watchpoint | `watch var`, `watch -l p->field`, `rwatch` (đọc), `awatch` (đọc/ghi) |
| Memory | `x/16xb ptr`, `x/8gx ptr`, `x/s ptr`, `info proc mappings` |
| Thread | `info threads`, `thread N`, `thread apply all bt` |
| Khác | `catch throw`, `set var x=5`, `call func(1)`, `info sharedlibrary`, `disassemble` |

Thiết lập tiện nghi trong `~/.gdbinit`:

```
set pagination off
set print pretty on
set print elements 0
set history save on
set confirm off
```

Với C++: bật pretty printer của libstdc++ (`p vec` hiện ra phần tử), `catch throw` để dừng ngay khi ném exception, `bt -frame-arguments all`.

---

### Q3. Crash tại `0x0`, `0x10`, `0xdeadbeef`, hoặc trong `memcpy` — đọc được gì từ địa chỉ?

**A:**

| Địa chỉ lỗi | Chẩn đoán đầu tiên |
|-------------|--------------------|
| `0x0` | Null pointer deref |
| Số nhỏ `0x8`, `0x10`, `0x28` | Null + offset -> deref field/member của con trỏ null, hoặc `this == nullptr` |
| Giá trị "có vẻ dữ liệu" (`0x4141...`, ASCII) | Con trỏ bị ghi đè bằng **string/dữ liệu** -> buffer overflow |
| Pattern (`0xdeadbeef`, `0xbaadf00d`, `0xfeeefeee`, `0xcdcdcdcd`) | Memory đã free/chưa init — pattern do allocator/debug runtime điền |
| Địa chỉ rất lớn/không align | Con trỏ rác, đọc sai kiểu, hoặc stack bị hỏng |
| Crash **trong** `memcpy`/`strlen`/`free` | Gần như chắc chắn **heap corruption** — thủ phạm là đoạn code **trước đó**, không phải `memcpy` |

Quan trọng: khi crash trong `free()` hoặc `malloc()`, liên tưởng ngay "có ai đó ghi tràn ra ngoài vùng cấp phát trước đây" -> chuyển sang ASAN, đừng ngồi đếm code trong gdb.

`this == nullptr`: gọi method trên object null -> crash ở dòng truy cập member đầu tiên, `p this` sẽ ra `0x0`.

---

### Q4. "Tôi ngăn được segfault nhưng không tìm ra nguồn dữ liệu sai" — làm gì tiếp? (ĐIỂM TRƯỢT)

**A:**

Đây là bước chuyển từ "fix triệu chứng" sang "root cause". Bốn vũ khí theo thứ tự chi phí:

**1. Hardware watchpoint — bắt tận tay kẻ ghi vào ô nhớ**

```
(gdb) b main
(gdb) run
(gdb) watch -l obj->state      # -l: chốt vào ĐỊA CHỈ, không phải biểu thức
(gdb) continue
Hardware watchpoint 2: -location obj->state
Old value = 1
New value = 61680             # <- giá trị rác
0x... in fill_buffer () at io.c:88
(gdb) bt                      # stack của KẺ GHI = root cause
```

Với vùng nhớ bị ghi tràn, đặt watchpoint tại địa chỉ cụ thể: `watch *(int*)0x7fff1234`.

**2. ASAN — chỉ thẳng ra allocation, kẻ free, kẻ ghi**

```bash
g++ -g -O1 -fsanitize=address,undefined -fno-omit-frame-pointer app.cpp
ASAN_OPTIONS=detect_stack_use_after_return=1:abort_on_error=1 ./a.out
```

Report cho bạn cả 3 stack: nơi crash, nơi **cấp phát**, nơi **free** -> trả lời trực tiếp câu hỏi "dữ liệu sai đến từ đâu".

**3. Valgrind `--track-origins=yes`** cho giá trị chưa khởi tạo: báo đúng dòng đã tạo ra biến uninitialized.

**4. `rr` — reverse debugging (mạnh nhất)**

```bash
rr record ./prog
rr replay
(rr) continue           # đến lúc crash
(rr) p ptr              # thấy giá trị rác
(rr) watch -l ptr
(rr) reverse-continue   # CHẠY NGƯỢC đến lần ghi gần nhất vào ptr
(rr) bt                 # chính là thủ phạm
```

**5. Nếu không dùng được công cụ**: thu hẹp bằng **invariant + assert**. Đặt `assert(check_invariant(obj))` ở đầu/cuối mỗi giai đoạn xử lý, chạy lại -> assert đầu tiên fail cho biết đoạn code nào phá dữ liệu. Kỹ thuật này giống binary search trên thời gian, và luôn áp dụng được cả trong sản phẩm đóng.

Câu nói ghi điểm: "Tôi đặt watchpoint trên ô nhớ bị hỏng. Khi nó dừng, stack tại đó là kẻ ghi — đó mới là root cause, còn chỗ segfault chỉ là nạn nhân đọc lại."

---

### Q5. Phân tích core dump?

**A:**

```bash
ulimit -c unlimited
cat /proc/sys/kernel/core_pattern        # xem core đi đâu (có thể là systemd-coredump)
coredumpctl list ; coredumpctl gdb 1234  # hệ thống dùng systemd

gdb ./prog core.1234
(gdb) bt full
(gdb) info threads
(gdb) thread apply all bt
(gdb) info registers
(gdb) info sharedlibrary
```

Lưu ý quan trọng:
- Binary phân tích phải **đúng phiên bản** với binary sinh ra core; giữ lại symbol (`-g`) hoặc file `.debug` tách rời (`objcopy --only-keep-debug`, `set debug-file-directory`).
- Nếu thiếu symbol của thư viện -> cài debuginfo tương ứng, nếu không `bt` sẽ toàn `??`.
- Core là **ảnh chụp tĩnh**: không step được, nhưng đọc được mọi biến và mọi thread. Dùng `p`, `x/`, `info locals` sau khi `frame N`.
- Core từ sản phẩm thường build `-O2` -> nhiều biến `<optimized out>`; xem Q7.

---

### Q6. Bug chỉ xảy ra thỉnh thoảng / không reproduce được trên máy bạn?

**A:**

Chiến lược:
1. **Thu thập dữ liệu thay vì đoán**: bật core dump, thêm logging có context (id, tham số, timestamp), bật `faulthandler`/crash handler, thu thập version + config + input.
2. **Tăng xác suất**: chạy stress, tăng số thread, thêm `sleep`/`sched_yield` tại các điểm nghi ngờ để mở rộng cửa sổ race, chạy trên máy yếu hơn hoặc CPU khác.
3. **Công cụ phát hiện chủ động**: TSAN cho data race, ASAN cho memory, `-D_GLIBCXX_DEBUG` cho STL, `MALLOC_PERTURB_` để làm lộ use-after-free.
4. **Ghi lại để phát lại**: `rr record --chaos` chạy lặp đến khi dính lỗi, sau đó replay xác định bao nhiêu lần cũng ra kết quả đó.
5. **Thu hẹp đầu vào**: ghi lại input gây lỗi, dùng delta-debugging để rút gọn.
6. Nếu là sản phẩm: thêm assert/telemetry ở các invariant, release bản có canary, để lần tái hiện tiếp theo có đủ dữ liệu.

Không nói "không reproduce được nên đóng ticket" — nói "tôi làm cho nó reproduce được nhiều hơn, hoặc làm cho lần sau có đủ bằng chứng".

---

### Q7. Debug binary build `-O2`, biến bị `<optimized out>`, hàm bị inline?

**A:**

- Build lại với `-Og -g3` (tối ưu vừa phải, giữ debuggability) hoặc `-O2 -g -fno-omit-frame-pointer -fno-inline` cho bản điều tra.
- Dùng `-g3` để có cả macro (`info macro`).
- Trong gdb, frame bị inline vẫn hiện; dùng `info frame`, `bt -past-inline`, `disassemble /s` rồi đọc thanh ghi: `info registers`, `p $rdi` (tham số đầu theo SysV ABI x86-64: rdi, rsi, rdx, rcx, r8, r9).
- Nếu biến `<optimized out>`, tìm giá trị trong thanh ghi hoặc trên stack: `x/16gx $rsp`.
- Với sản phẩm không được build lại: giữ **separate debug info** (`objcopy --only-keep-debug prog prog.debug`) và build với `-g` ngay cả khi `-O2` — `-g` không làm chậm code.

---

### Q8. Debug multithread trong gdb (deadlock / race)?

**A:**

```
(gdb) info threads
(gdb) thread apply all bt          # ảnh chụp toàn bộ -> tìm vòng chờ
(gdb) thread 3
(gdb) frame 2
(gdb) p mutex->__data.__owner      # thread nào đang giữ (glibc)
(gdb) set scheduler-locking on     # chỉ cho thread hiện tại chạy khi step
```

Nhận dạng **deadlock**: nhiều thread đều dừng trong `pthread_mutex_lock`/`futex_wait`; đối chiếu ai giữ lock nào -> vẽ **lock order graph** -> tìm chu trình. Fix: cố định thứ tự lock toàn hệ thống, dùng `std::scoped_lock` (lock nhiều mutex an toàn), thu hẹp critical section, dùng `try_lock` + backoff.

Nhận dạng **race**: dùng TSAN (`-fsanitize=thread`) — nó báo chính xác 2 stack truy cập xung đột; đây là công cụ đúng thay vì suy luận.

Chỗ treo ở sản phẩm: `gdb -p PID` + `thread apply all bt` (C++), `py-spy dump --pid` (Python), hoặc `gcore PID` để lấy snapshot rồi thả process ra.

---

### Q9. So sánh công cụ: gdb / ASAN / Valgrind / TSAN / UBSAN — dùng cái nào khi nào?

**A:**

| Công cụ | Bắt loại bug | Chi phí | Ghi chú |
|---------|-------------|---------|---------|
| gdb | Quan sát trạng thái, điều tra tương tác | 0 khi không chạy | Không tự phát hiện bug |
| ASAN | Heap/stack/global overflow, use-after-free, double free, leak | ~2x chậm, ~3x RAM | Cần compile lại; report có stack alloc/free |
| LeakSanitizer | Memory leak | đi kèm ASAN | `ASAN_OPTIONS=detect_leaks=1` |
| UBSAN | Integer overflow, misaligned, shift sai, null deref | thấp | Bắt các UB "yên lặng" |
| TSAN | Data race, lock order | ~5-15x chậm | Vũ khí số 1 cho bug concurrency |
| MSAN | Đọc biến chưa khởi tạo | cao | Phải build cả dependency |
| Valgrind memcheck | Giống ASAN + uninitialized, không cần build lại | 10-50x chậm | `--track-origins=yes` rất hữu ích |
| Helgrind/DRD | Race | rất chậm | Thay thế TSAN khi không build lại được |
| rr | Mọi loại — chạy ngược thời gian | ~1.5x | Mạnh nhất cho bug khó, Linux/Intel |

Quy tắc: **ASAN + UBSAN bật mặc định trong CI/debug build**, TSAN chạy định kỳ, Valgrind khi không compile lại được, gdb/rr khi cần hiểu logic.

---

### Q10. Sau khi fix xong, bạn làm gì để chắc chắn đã đúng?

**A:**

1. **Giải thích được nhân quả**: viết một câu "bug xảy ra vì X, dẫn đến Y, biểu hiện là Z" — nếu chưa viết được thì chưa tìm ra root cause.
2. **Reproduce trước/sau**: có cách làm nó crash trước khi fix, và cách đó không còn crash sau fix.
3. **Thêm test**: unit test hoặc regression test bám vào đúng invariant bị vi phạm.
4. **Chạy sanitizer** trên test suite.
5. **Rà soát cùng loại lỗi** ở chỗ khác (`grep` pattern tương tự) — bug thường đi theo đàn.
6. **Đánh giá tác động**: fix có làm thay đổi hành vi/hiệu năng/ABI không; có cần cherry-pick sang branch release không.
7. **Ghi lại**: mô tả trong commit/ticket gồm triệu chứng, root cause, cách reproduce, cách fix — đồng nghiệp sau bạn sẽ cần.

---

## FLASH CARD — Part 3

- `0x0` = null; `0x8/0x10` = null+offset (`this == nullptr`); ASCII = overflow; pattern (`0xdeadbeef`) = freed/uninit.
- Crash trong `free`/`malloc`/`memcpy` = heap corruption, thủ phạm ở **trước đó**.
- Quy trình: `bt full` -> `frame N` -> `info locals/args` -> `p` biến nghi ngờ -> hỏi "giá trị này từ đâu ra" -> `watch -l` -> `bt` của kẻ ghi.
- ASAN cho memory (có stack alloc + free), TSAN cho race, UBSAN cho UB, Valgrind khi không build lại được, `rr` + `reverse-continue` để chạy ngược.
- Không reproduce được: bật core dump, tăng stress, `rr record --chaos`, thêm assert invariant.
- `-O2` mất biến: build `-Og -g3`, đọc `$rdi/$rsi/$rdx`, giữ separate debug info.
- Deadlock: `thread apply all bt` -> vẽ lock order graph -> tìm chu trình.
- Không dừng lại khi hết crash: phải giải thích được dữ liệu sai sinh ra ở đâu + thêm test + sanitizer trong CI.
