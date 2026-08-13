# 01 - C Core (Bilingual VI/EN)

Tai lieu nay giu format Q&A goc de dung voi app parser, dong thoi bo sung noi dung song ngu de luyen phong van tieng Anh.

---

## 1) Data type, memory layout, ABI

### Q1. `char`, `short`, `int`, `long`, `long long` co size co dinh khong?

**A:**
- EN: No. The standard only guarantees ordering (`char <= short <= int <= long <= long long`) and `sizeof(char) == 1`.
- VI: Khong. Standard chi dam bao thu tu kich thuoc va `sizeof(char) == 1`, khong dam bao so byte cu the.

| ABI   | Platform           | `int` | `long` | `pointer` |
|---|---|---:|---:|---:|
| ILP32 | 32-bit Linux/Win   | 4 | 4 | 4 |
| LP64  | 64-bit Linux/macOS | 4 | 8 | 8 |
| LLP64 | 64-bit Windows     | 4 | 4 | 8 |

- EN: For binary protocol/file format, use fixed-width types.
- VI: Khi lam protocol/file binary, dung type co size co dinh.

```c
#include <stdint.h>
int32_t x;
uint64_t y;
```

Follow-up (EN): Why prefer `int32_t` over `int` for serialization?

---

### Q2. `struct` va `padding` la gi? Tai sao can biet?

**A:**
- EN: Compilers insert padding bytes to satisfy alignment.
- VI: Compiler chen byte dem de can le du lieu theo yeu cau CPU.

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
- VI: Sap xep field tu lon den nho de giam padding.

---

### Q3. `volatile` co thay the mutex/atomic duoc khong?

**A:**
- EN: No. `volatile` is not a synchronization primitive.
- VI: Khong. `volatile` khong thay duoc mutex/atomic trong da luong.

`volatile` does NOT guarantee:
- atomicity
- ordering
- cross-thread synchronization

Dung dung:
```c
volatile uint32_t* const uart_status = (volatile uint32_t*)0x40001000;
while (!(*uart_status & 0x1)) {}
```

Dung cho multi-threading la sai:
```c
volatile int counter = 0;
counter++; // race condition
```

Dung dung:
```c
#include <stdatomic.h>
atomic_int counter = 0;
atomic_fetch_add(&counter, 1);
```

---

### Q4. Endianness la gi?

**A:**
- EN: Byte order of multi-byte values in memory.
- VI: Thu tu sap xep byte cua so nhieu byte trong memory.

```text
0x12345678 at address 0x100
Little-endian: 78 56 34 12
Big-endian:    12 34 56 78
```

Kiem tra:
```c
int check_endian(void) {
    uint32_t x = 1;
    return *(uint8_t*)&x; // 1 little, 0 big
}
```

- EN: Network byte order is big-endian (`htonl`, `ntohl`).
- VI: Network order la big-endian.

---

## 2) Pointer, array, string

### Q5. Su khac nhau giua `int a[10]` va `int* p`?

**A:**
- EN: `a` stores 10 ints, `p` stores only an address.
- VI: `a` chua 10 phan tu int, `p` chi chua dia chi.

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

### Q6. Vi sao `arr` thuong bi decay thanh pointer?

**A:**
- EN: In most expressions, arrays decay to pointer-to-first-element.
- VI: Trong hau het bieu thuc, array tu dong doi thanh con tro den phan tu dau.

```c
int a[5] = {1,2,3,4,5};
int* p = a;
```

Ngoai le khong decay:
- `sizeof(a)`
- `&a`
- array initialization

He qua quan trong:
```c
void f(int arr[]) { // actually int* arr
    sizeof(arr);     // pointer size
}
```

---

### Q7. `const char*`, `char* const`, `const char* const` khac nhau the nao?

**A:**
- EN: Read right-to-left.
- VI: Doc tu phai sang trai.

```c
const char* p1;      // pointer to const char
char* const p2 = 0;  // const pointer to char
const char* const p3 = 0; // const pointer to const char
```

- EN: Const before `*` => data const; const after `*` => pointer const.
- VI: `const` truoc `*` la data const; sau `*` la pointer const.

---

### Q8. `strcpy` nguy hiem o diem nao?

**A:**
- EN: No destination size check; can overflow buffer.
- VI: Khong check size buffer dich; de bi overflow.

```c
char dst[8];
strcpy(dst, "Hello, World!"); // overflow
```

An toan hon:
```c
snprintf(dst, sizeof(dst), "%s", src);
```

- EN: In C++, prefer `std::string`.
- VI: Trong C++, uu tien `std::string`.

---

## 3) Storage duration va linkage

### Q9. `auto`, `static`, `extern`, `register` trong C?

**A:**

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
- VI: Linkage xac dinh ten co nhin thay qua cac file .c/.cpp hay khong.

```c
// external linkage
int g_counter = 0;

// internal linkage
static int s_counter = 0;
```

- EN: Use `static` for file-private symbols.
- VI: Dung `static` cho symbol chi dung trong mot file.

---

## 4) Undefined behavior, implementation-defined

### Q11. UB la gi? Vi du?

**A:**
- EN: Undefined Behavior means the standard imposes no requirements.
- VI: UB la hanh vi ma standard khong quy dinh ket qua.

Vi du pho bien:
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

### Q12. Tai sao UB nguy hiem hon bug thong thuong?

**A:**
- EN: Optimizers assume UB never happens, so generated code may look "impossible".
- VI: Compiler gia dinh UB khong xay ra, nen toi uu co the lam hanh vi kho du doan.

Cong cu de bat UB som:
- AddressSanitizer
- UndefinedBehaviorSanitizer
- ThreadSanitizer
- Valgrind

---

### Q13. Implementation-defined la gi?

**A:**
- EN: Compiler chooses behavior but must document it.
- VI: Compiler duoc quyen quyet dinh, nhung phai tai lieu hoa.

Vi du:
- `char` signed hay unsigned by default
- right shift of negative signed integer
- exact width of built-in types

Phan biet nhanh:
- Undefined: anything can happen
- Implementation-defined: deterministic per compiler/platform
- Unspecified: one of several valid outcomes

---

## 5) Build pipeline co ban

### Q14. Cac giai doan build C/C++?

**A:**
- EN/VI: 4 stage: preprocess -> compile -> assemble -> link.

```text
source.c -> source.i -> source.s -> source.o -> executable
```

Lenh thuong dung:
```bash
gcc -E source.c -o source.i
gcc -S source.c -o source.s
gcc -c source.c -o source.o
gcc source.o -o program
```

---

### Q15. Header guard dung de lam gi?

**A:**
- EN: Prevent multiple inclusion in one translation unit.
- VI: Tranh include lap gay redefinition.

```c
#ifndef MYHEADER_H
#define MYHEADER_H
// declarations
#endif
```

`#pragma once` la phuong an gon hon tren hieu het compiler hien dai.

---

### Q16. ODR (One Definition Rule) la gi?

**A:**
- EN: A program should have exactly one definition for each non-inline entity.
- VI: Moi entity khong inline can mot dinh nghia duy nhat trong chuong trinh.

Vi pham ODR thuong gay linker error (multiple definition).

```cpp
inline int add(int a, int b) { return a + b; }
```

---

## 6) Cau hoi practical senior thuong hoi

### Q17. Cach debug crash ngau nhien trong C?

**A:**
- EN: Turn on debug symbols/sanitizers, reproduce, inspect core dump.
- VI: Bat symbol va sanitizer, tai hien loi, phan tich core dump.

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

### Q18. Lam sao giam memory fragmentation?

**A:**
- EN: Use allocation strategies that match lifetime and object shape.
- VI: Chon strategy cap phat phu hop vong doi va kich thuoc object.

Ky thuat:
- pool allocator
- slab allocator
- arena allocator
- buffer reuse + batch allocation

---

### Q19. Vi sao API C can ro ownership?

**A:**
- EN: Because there is no GC/smart pointer by default, ownership must be explicit.
- VI: Vi C khong co GC/smart pointer mac dinh, ownership phai ghi ro.

Nen document ro contract:
```c
// Caller owns returned memory, must free()
char* create_buffer(size_t n);

// Does NOT take ownership
void process_buffer(const char* buf, size_t n);

// Takes ownership
void consume_buffer(char* buf);
```

---

### Q20. Khi nao dung packed struct?

**A:**
- EN: Only when fixed byte layout is required (protocol/hardware mapping).
- VI: Chi dung khi can layout byte chinh xac (protocol, thanh ghi hardware).

```c
struct __attribute__((packed)) EthernetHeader {
    uint8_t  dst[6];
    uint8_t  src[6];
    uint16_t ethertype;
};
```

- EN: Beware misaligned access and portability risks.
- VI: Can than truy cap misaligned va rui ro portability.

---

## Flash card (on nhanh)

| Prompt | Quick answer |
|---|---|
| `volatile` thread-safe? | No, use `atomic`/locks |
| `sizeof(array)` vs `sizeof(ptr)` | full array vs pointer size |
| UB danger | optimizer assumptions make behavior unpredictable |
| `int32_t` vs `int` | fixed width vs ABI dependent |
| `static` global linkage | internal to one translation unit |
| `const char*` | pointer to read-only chars |
