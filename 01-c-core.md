# 01 - C Core (Bilingual VI/EN)

Tài liệu này giữ format Q&A gốc để dùng với app parser, đồng thời bổ sung nội dung song ngữ để luyện phỏng vấn tiếng Anh.

---

## 1) Data type, memory layout, ABI

### Q1. `char`, `short`, `int`, `long`, `long long` có size cố định không?

**A:**
- EN: No. The standard only guarantees ordering (`char <= short <= int <= long <= long long`) and `sizeof(char) == 1`.
- VI: Không. Standard chỉ đảm bảo thứ tự kích thước và `sizeof(char) == 1`, không đảm bảo số byte cụ thể.

| ABI   | Platform           | `int` | `long` | `pointer` |
|---|---|---:|---:|---:|
| ILP32 | 32-bit Linux/Win   | 4 | 4 | 4 |
| LP64  | 64-bit Linux/macOS | 4 | 8 | 8 |
| LLP64 | 64-bit Windows     | 4 | 4 | 8 |

- EN: For binary protocol/file format, use fixed-width types.
- VI: Khi làm protocol/file binary, dùng type có size cố định.

```c
#include <stdint.h>
int32_t x;
uint64_t y;
```

Follow-up (EN): Why prefer `int32_t` over `int` for serialization?

---

### Q2. `struct` và `padding` là gì? Tại sao cần biết?

**A:**
- EN: Compilers insert padding bytes to satisfy alignment.
- VI: Compiler chèn byte đệm để căn lề dữ liệu theo yêu cầu CPU.

```c
struct A {
    char a;
    // 3 bytes padding
    int  b;
    char c;
    // 3 bytes tail padding
};
// sizeof(A) == 12 on common ABI
```

```c
struct B {
    int  b;
    char a;
    char c;
    // 2 bytes padding
};
// sizeof(B) == 8
```

- EN: Reorder fields (large to small) to reduce padding.
- VI: Sắp xếp field từ lớn đến nhỏ để giảm padding.

---

### Q3. `volatile` có thay thế mutex/atomic được không?

**A:**
- EN: No. `volatile` is not a synchronization primitive.
- VI: Không. `volatile` không thay được mutex/atomic trong đa luồng.

`volatile` does NOT guarantee:
- atomicity
- ordering
- cross-thread synchronization

Dùng đúng:
```c
volatile uint32_t* const uart_status = (volatile uint32_t*)0x40001000;
while (!(*uart_status & 0x1)) {}
```

Dùng cho multi-threading là sai:
```c
volatile int counter = 0;
counter++; // race condition
```

Dùng đúng:
```c
#include <stdatomic.h>
atomic_int counter = 0;
atomic_fetch_add(&counter, 1);
```

---

### Q4. Endianness là gì?

**A:**
- EN: Byte order of multi-byte values in memory.
- VI: Thứ tự sắp xếp byte của giá trị nhiều byte trong memory.

```text
0x12345678 at address 0x100
Little-endian: 78 56 34 12
Big-endian:    12 34 56 78
```

Kiểm tra:
```c
int check_endian(void) {
    uint32_t x = 1;
    return *(uint8_t*)&x; // 1 little, 0 big
}
```

- EN: Network byte order is big-endian (`htonl`, `ntohl`).
- VI: Network order là big-endian.

---

## 2) Pointer, array, string

### Q5. Sự khác nhau giữa `int a[10]` và `int* p`?

**A:**
- EN: `a` stores 10 ints, `p` stores only an address.
- VI: `a` chứa 10 phần tử int, `p` chỉ chứa địa chỉ.

| Feature | `int a[10]` | `int* p` |
|---|---|---|
| `sizeof` | full array size | pointer size |
| Rebind address | no | yes |
| Memory | data itself | address only |

```c
int a[10];
int* p = a;

sizeof(a); // 40 on typical 32-bit int
sizeof(p); // 8 on 64-bit

p++; // OK
a++; // ERROR
```

---

### Q6. Vì sao `arr` thường bị decay thành pointer?

**A:**
- EN: In most expressions, arrays decay to pointer-to-first-element.
- VI: Trong hầu hết biểu thức, array tự động chuyển thành con trỏ đến phần tử đầu.

```c
int a[5] = {1,2,3,4,5};
int* p = a;
```

Ngoại lệ không decay:
- `sizeof(a)`
- `&a`
- array initialization

Hệ quả quan trọng:
```c
void f(int arr[]) { // actually int* arr
    sizeof(arr);     // pointer size
}
```

---

### Q7. `const char*`, `char* const`, `const char* const` khác nhau thế nào?

**A:**
- EN: Read right-to-left.
- VI: Đọc từ phải sang trái.

```c
const char* p1;      // pointer to const char
char* const p2 = 0;  // const pointer to char
const char* const p3 = 0; // const pointer to const char
```

- EN: Const before `*` => data const; const after `*` => pointer const.
- VI: `const` trước `*` là data const; sau `*` là pointer const.

---

### Q8. `strcpy` nguy hiểm ở điểm nào?

**A:**
- EN: No destination size check; can overflow buffer.
- VI: Không check size buffer đích; dễ bị overflow.

```c
char dst[8];
strcpy(dst, "Hello, World!"); // overflow
```

An toàn hơn:
```c
snprintf(dst, sizeof(dst), "%s", src);
```

- EN: In C++, prefer `std::string`.
- VI: Trong C++, ưu tiên `std::string`.

---

## 3) Storage duration và linkage

### Q9. `auto`, `static`, `extern`, `register` trong C?

**A:**
- EN: C has four storage-class specifiers that control lifetime and linkage of variables.
- VI: C có 4 storage-class specifier quy định thời gian tồn tại và linkage của biến.

| Keyword | Storage duration | Linkage | Notes |
|---|---|---|---|
| `auto` | automatic | none | default local variable |
| `static` | static lifetime | internal (global) / none (local) | local static keeps value between calls |
| `extern` | static lifetime | external | declaration of symbol defined elsewhere |
| `register` | automatic | none | hint only, mostly ignored today |

```c
void counter(void) {
    static int count = 0;
    count++;
}
```

---

### Q10. Internal vs external linkage?

**A:**
- EN: Linkage controls visibility across translation units.
- VI: Linkage xác định tên có nhìn thấy qua các file .c/.cpp hay không.

```c
// external linkage
int g_counter = 0;

// internal linkage
static int s_counter = 0;
```

- EN: Use `static` for file-private symbols.
- VI: Dùng `static` cho symbol chỉ dùng trong một file.

---

## 4) Undefined behavior, implementation-defined

### Q11. UB là gì? Ví dụ?

**A:**
- EN: Undefined Behavior means the standard imposes no requirements.
- VI: UB là hành vi mà standard không quy định kết quả.

Ví dụ phổ biến:
- out-of-bounds access
- null dereference
- signed integer overflow
- use-after-free
- data race

```c
int* p = NULL;
*p = 1; // UB
```

---

### Q12. Tại sao UB nguy hiểm hon bug thông thường?

**A:**
- EN: Optimizers assume UB never happens, so generated code may look "impossible".
- VI: Compiler giả định UB không xảy ra, nên tối ưu có thể làm hành vi khó dự đoán.

Công cụ để bắt UB sớm:
- AddressSanitizer
- UndefinedBehaviorSanitizer
- ThreadSanitizer
- Valgrind

---

### Q13. Implementation-defined là gì?

**A:**
- EN: Compiler chooses behavior but must document it.
- VI: Compiler được quyền quyết định, nhưng phải tài liệu hóa.

Ví dụ:
- `char` signed hay unsigned by default
- right shift of negative signed integer
- exact width of built-in types

Phân biệt nhanh:
- Undefined: anything can happen
- Implementation-defined: deterministic per compiler/platform
- Unspecified: one of several valid outcomes

---

## 5) Build pipeline cơ bản

### Q14. Các giai đoạn build C/C++?

**A:**
- EN: Four stages: preprocess -> compile -> assemble -> link.
- VI: 4 giai đoạn: preprocess -> compile -> assemble -> link.

```text
source.c -> source.i -> source.s -> source.o -> executable
```

Lệnh thường dùng:
```bash
gcc -E source.c -o source.i
gcc -S source.c -o source.s
gcc -c source.c -o source.o
gcc source.o -o program
```

---

### Q15. Header guard dùng để làm gì?

**A:**
- EN: Prevent multiple inclusion in one translation unit.
- VI: Tránh include lặp gây redefinition.

```c
#ifndef MYHEADER_H
#define MYHEADER_H
// declarations
#endif
```

`#pragma once` là phương án gọn hơn trên hầu hết compiler hiện đại.

---

### Q16. ODR (One Definition Rule) là gì?

**A:**
- EN: A program should have exactly one definition for each non-inline entity.
- VI: Mọi entity không inline cần một định nghĩa duy nhất trong chương trình.

Vi phạm ODR thường gây linker error (multiple definition).

```cpp
inline int add(int a, int b) { return a + b; }
```

---

## 6) Câu hỏi practical senior thường hỏi

### Q17. Cách debug crash ngẫu nhiên trong C?

**A:**
- EN: Turn on debug symbols/sanitizers, reproduce, inspect core dump.
- VI: Bật symbol và sanitizer, tái hiện lỗi, phân tích core dump.

```bash
gcc -g -O0 -fsanitize=address,undefined -fno-omit-frame-pointer -o prog src.c
gdb ./prog core
```

Checklist:
- reproduce with controlled input
- inspect stack trace
- inspect locals and heap corruption signs
- bisect if regression

---

### Q18. Làm sao giảm memory fragmentation?

**A:**
- EN: Use allocation strategies that match lifetime and object shape.
- VI: Chọn strategy cấp phát phù hợp vòng đời và kích thước object.

Kỹ thuật:
- pool allocator
- slab allocator
- arena allocator
- buffer reuse + batch allocation

---

### Q19. Vì sao API C cần rõ ownership?

**A:**
- EN: Because there is no GC/smart pointer by default, ownership must be explicit.
- VI: Vì C không có GC/smart pointer mặc định, ownership phải ghi rõ.

Nên document rõ contract:
```c
// Caller owns returned memory, must free()
char* create_buffer(size_t n);

// Does NOT take ownership
void process_buffer(const char* buf, size_t n);

// Takes ownership
void consume_buffer(char* buf);
```

---

### Q20. Khi nào dùng packed struct?

**A:**
- EN: Only when fixed byte layout is required (protocol/hardware mapping).
- VI: Chỉ dùng khi cần layout byte chính xác (protocol, thanh ghi hardware).

```c
struct __attribute__((packed)) EthernetHeader {
    uint8_t  dst[6];
    uint8_t  src[6];
    uint16_t ethertype;
};
```

- EN: Beware misaligned access and portability risks.
- VI: Cẩn thận truy cập misaligned và rủi ro portability.

---

## Flash card (ôn nhanh)

| Prompt | Quick answer |
|---|---|
| `volatile` thread-safe? | No, use `atomic`/locks |
| `sizeof(array)` vs `sizeof(ptr)` | full array vs pointer size |
| UB danger | optimizer assumptions make behavior unpredictable |
| `int32_t` vs `int` | fixed width vs ABI dependent |
| `static` global linkage | internal to one translation unit |
| `const char*` | pointer to read-only chars |
