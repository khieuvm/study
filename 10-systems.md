# 10 - Systems Programming (OS, Networking, IPC) — Bilingual VI/EN

---

## 1) Process & Thread

### Q1. Process vs Thread khác nhau thế nào?

**A:**
- EN: A **process** has its own virtual address space — crash isolation but expensive to create and communicate (IPC). A **thread** shares the process address space — cheap to create but one thread crash can kill the whole process. Context switch is faster for threads (same address space, nó TLB flush).
- VI: **Process** có không gian địa chỉ riêng — cách ly crash nhưng đặt để tạo và giao tiếp (IPC). **Thread** chia sẻ không gian địa chỉ — rẻ để tạo nhưng 1 thread crash có thể giet ca process. Context switch nhanh hơn cho thread (cũng address space, không flush TLB).

| | Process | Thread |
|---|---|---|
| Memory | Own address space | Shared with other threads |
| Creation cost | Expensive (`fork`) | Cheap (`pthread_create`) |
| Communication | IPC (pipe, socket, shm) | Shared memory (need sync) |
| Crash isolation | Yes | No — one crash kills all |
| Context switch | Expensive (TLB flush) | Cheaper (same address space) |

```cpp
pid_t pid = fork();
if (pid == 0) {
    execv("/bin/ls", args);  // replace process image
    _exit(1);
} else {
    waitpid(pid, &status, 0);
}
```

Follow-up (EN): What is copy-on-write (COW) in `fork()` and why is it efficient?

---

### Q2. Virtual memory là gì?

**A:**
- EN: Each process sees its own **private address space** (4GB on 32-bit, 128TB on x86-64). The OS maps virtual addresses to physical addresses via a **page table**. Pages are 4KB. A **page fault** occurs when accessing a page not in RAM — the OS loads it from disk (or triggers SIGSEGV for invalid access). **TLB** caches recent page table lookups.
- VI: Mọi process thay **không gian địa chỉ riêng** (4GB trên 32-bit, 128TB trên x86-64). OS map virtual address sáng physical address qua **page table**. Page là 4KB. **Page fault** xảy ra khi truy cập page chưa o RAM — OS load từ disk (hoặc SIGSEGV nếu truy cập không hợp le). **TLB** cache các page table lookup gần đầy.

```cpp
// mmap: map file directly into virtual memory (zero-copy)
void* ptr = mmap(nullptr, size, PROT_READ, MAP_PRIVATE, fd, 0);
// Access file like memory: ptr[0], ptr[1], ...
// OS loads pages on-demand (lazy)
munmap(ptr, size);
```

Follow-up (EN): What is a TLB shootdown and when does it happen?

---

### Q3. Stack frame trong function call là gì?

**A:**
- EN: Each function call creates a **stack frame** containing: return address, saved registers, local variables, and arguments. Stack grows downward. Stack overflow occurs when frames exceed the stack size limit (deep recursion, oversized local arrays).
- VI: Mọi function call tạo 1 **stack frame** chưa: return address, saved registers, local variables, và arguments. Stack lớn xuống dưới. Stack overflow xảy ra khi frame vuot giới hạn stack (đệ quy sau, local array qua lớn).

```
Stack (grows down):
+-------------------+  <- Stack pointer (RSP)
| local variables   |
| saved registers   |
| return address    |  <- Base pointer (RBP)
+-------------------+  <- Caller's frame
```

```cpp
// x86-64 Linux ABI: first 6 integer args in registers (rdi, rsi, rdx, rcx, r8, r9)
void foo(int a, int b) {    // a in rdi, b in rsi
    int local = a + b;      // on stack: [rbp - 4]
}
```

Follow-up (EN): What is the red zone in the x86-64 ABI?

---

## 2) Signals

### Q4. Signal trong Unix/Linux là gì?

**A:**
- EN: Signals are **asynchronous notifications** sent to a process. Common: SIGINT (Ctrl+C), SIGTERM (polite kill), SIGKILL (forced kill, uncatchable), SIGSEGV (segfault). Custom handlers must be **async-signal-safe** — only use `write()`, `_exit()`, `sig_atomic_t` assignments. Never call `printf`, `malloc`, or throw exceptions in signal handlers.
- VI: Signal là **notification bất đồng bộ** gửi cho process. Phổ biến: SIGINT (Ctrl+C), SIGTERM (kill binh thường), SIGKILL (kill bước, không bắt được), SIGSEGV (segfault). Custom handler phải **async-signal-safe** — chỉ dùng `write()`, `_exit()`, gần `sig_atomic_t`. không báo gio gọi `printf`, `malloc`, hoặc throw exception trong signal handler.

```cpp
volatile sig_atomic_t g_running = 1;

void handler(int sig) {
    g_running = 0;  // safe: sig_atomic_t assignment is atomic
    // Do NOT call printf, malloc, or non-reentrant functions!
}

struct sigaction sa{};
sa.sa_handler = handler;
sa.sa_flags = SA_RESTART;
sigaction(SIGINT, &sa, nullptr);

while (g_running) { /* main loop */ }
```

Follow-up (EN): Why is `sigaction` preferred over `signal`?

---

## 3) IPC (Inter-Process Communication)

### Q5. Các phuong phap IPC chính?

**A:**
- EN: IPC methods ranked by speed: **shared memory** (fastest, same host), **pipes/FIFOs** (fast, same host), **Unix sockets** (fast, same host), **TCP/UDP sockets** (network), **message queues** (async), **signals** (notification only). Choose based on: same host vs network, throughput needs, and complexity tolerance.
- VI: Các phuong phap IPC theo toc do: **shared memory** (nhanh nhất, cũng host), **pipe/FIFO** (nhanh, cũng host), **Unix socket** (nhanh, cũng host), **TCP/UDP socket** (network), **message queue** (async), **signal** (chi notification). Chọn theo: cũng host vs network, yêu cầu throughput, và do phức tạp chap nhận được.

| Method | Speed | Scope | Use case |
|---|---|---|---|
| Shared memory | Fastest | Same host | High-throughput data exchange |
| Pipe / FIFO | Fast | Same host | Parent-child, shell pipes |
| Unix socket | Fast | Same host | Client-server local |
| TCP/UDP socket | Slower | Any host | Network communication |
| Message queue | Medium | Same host | Async messaging |

```cpp
// Shared memory (POSIX)
int fd = shm_open("/my_shm", O_CREAT|O_RDWR, 0666);
ftruncate(fd, 4096);
void* ptr = mmap(nullptr, 4096, PROT_READ|PROT_WRITE, MAP_SHARED, fd, 0);
*(int*)ptr = 42;  // write from one process, read from another
```

Follow-up (EN): How do you synchronize access to shared memory between processes?

---

## 4) Networking

### Q6. Socket programming cơ bản trong C?

**A:**
- EN: Socket programming follows: **create** (`socket()`), **bind** (server: assign address), **listen** (server: accept queue), **accept** (server: new connection), **connect** (client: to server). TCP provides reliable ordered streams; UDP provides unreliable datagrams. Always set `SO_REUSEADDR` on servers to avoid "Address already in use".
- VI: Socket programming theo quy trình: **tạo** (`socket()`), **bind** (server: gần địa chỉ), **listen** (server: hang đổi accept), **accept** (server: kết nối mọi), **connect** (client: đến server). TCP cũng cấp stream đáng tin cậy; UDP cũng cấp datagram không đáng tin cậy. Luôn set `SO_REUSEADDR` trên server để tránh "Address already in use".

```cpp
// TCP Server
int fd = socket(AF_INET, SOCK_STREAM, 0);
int opt = 1;
setsockopt(fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

struct sockaddr_in addr{};
addr.sin_family = AF_INET;
addr.sin_addr.s_addr = INADDR_ANY;
addr.sin_port = htons(8080);
bind(fd, (sockaddr*)&addr, sizeof(addr));
listen(fd, 10);

int client = accept(fd, nullptr, nullptr);
recv(client, buf, sizeof(buf), 0);
send(client, "OK", 2, 0);
close(client);
```

Follow-up (EN): What is the difference between `SOCK_STREAM` (TCP) and `SOCK_DGRAM` (UDP)?

---

### Q7. Non-blocking I/O và epoll/select?

**A:**
- EN: Default sockets are **blocking** — `recv()` blocks the thread. Non-blocking I/O + event multiplexing lets one thread handle many connections. **select**: portable but O(n) per call, limited to 1024 fds. **epoll** (Linux): O(1) per event, handles millions of connections. Supports **level-triggered** (default) and **edge-triggered** (EPOLLET) modes.
- VI: Socket mặc định là **blocking** — `recv()` block thread. Non-blocking I/O + event multiplexing cho 1 thread xử lý nhiều connection. **select**: portable nhưng O(n) mỗi lần gọi, giới hạn 1024 fd. **epoll** (Linux): O(1) mọi event, xử lý hang trieu connection. Ho tro **level-triggered** (mặc định) và **edge-triggered** (EPOLLET).

```cpp
// epoll: efficient event loop
int epfd = epoll_create1(0);
struct epoll_event ev{};
ev.events = EPOLLIN | EPOLLET;
ev.data.fd = server_fd;
epoll_ctl(epfd, EPOLL_CTL_ADD, server_fd, &ev);

struct epoll_event events[64];
while (true) {
    int n = epoll_wait(epfd, events, 64, -1);
    for (int i = 0; i < n; i++) {
        if (events[i].data.fd == server_fd)
            accept_new_client();
        else
            handle_client_data(events[i].data.fd);
    }
}
```

Follow-up (EN): What is the difference between level-triggered and edge-triggered epoll?

---

## 5) ELF & Build

### Q8. ELF format là gì? Sections chính?

**A:**
- EN: **ELF (Executable and Linkable Format)** is the standard binary format on Linux/Unix. Key sections: `.text` (executable code), `.rodata` (read-only data, string literals), `.data` (initialized globals), `.bss` (uninitialized globals — zero-filled, takes no disk space), `.symtab`/`.strtab` (symbols), `.plt`/`.got` (dynamic linking).
- VI: **ELF** là format binary chuan trên Linux/Unix. Sections chính: `.text` (code thực thì), `.rodata` (data chỉ đọc, string literal), `.data` (global đã khởi tạo), `.bss` (global chưa khởi tạo — zero-filled, không chiem disk), `.symtab`/`.strtab` (symbol), `.plt`/`.got` (dynamic linking).

```bash
nm -C prog           # demangled symbols
readelf -S prog      # section headers
objdump -d prog      # disassemble
ldd prog             # shared library dependencies
size prog            # section sizes
```

Follow-up (EN): What is the difference between `.plt` and `.got` in dynamic linking?

---

### Q9. Static linking vs Dynamic linking?

**A:**
- EN: **Static**: all library code embedded in binary at compile time — larger binary, nó dependencies, faster startup. **Dynamic**: libraries loaded at runtime (`.so`/`.dll`) — smaller binary, shared across processes, updatable without recompile. `-fPIC` (Position Independent Code) is required for shared libraries.
- VI: **Static**: toan bỏ code library nhưng vào binary lúc compile — binary lớn, không dependency, khởi động nhanh. **Dynamic**: library load lúc runtime (`.so`/`.dll`) — binary nhỏ, chia sẻ giữa process, update không cần recompile. `-fPIC` (Position Independent Code) cần cho shared library.

| | Static | Dynamic |
|---|---|---|
| When linked | Compile time | Runtime |
| Binary size | Large | Small |
| Dependencies | None (self-contained) | Needs `.so` on system |
| Library update | Must recompile | Just replace `.so` |

```bash
# Static library
ar rcs libmylib.a file1.o file2.o
g++ main.o -L. -lmylib -o prog

# Shared library
g++ -shared -fPIC -o libmylib.so file1.o file2.o
g++ main.o -L. -lmylib -Wl,-rpath,. -o prog
```

Follow-up (EN): What is `-Wl,-rpath` and why is it needed?

---

### Q10. `dlopen` / `dlsym` — plugin architecture?

**A:**
- EN: `dlopen` loads a shared library at runtime; `dlsym` retrieves a function pointer by name. This enables **plugin architectures** — load/unload functionality without recompilation. `dlclose` unloads the library.
- VI: `dlopen` load shared library lúc runtime; `dlsym` lấy function pointer theo ten. Cho phép **plugin architecture** — load/unload chức năng không cần recompile. `dlclose` unload library.

```cpp
void* handle = dlopen("./plugin.so", RTLD_LAZY);
if (!handle) { fprintf(stderr, "%s\n", dlerror()); return; }

typedef int (*PluginFunc)(const char*);
PluginFunc fn = (PluginFunc)dlsym(handle, "plugin_run");
if (dlerror()) { /* handle error */ }

int result = fn("input");
dlclose(handle);
```

Follow-up (EN): What is the difference between `RTLD_LAZY` and `RTLD_NOW`?

---

## 6) System Calls

### Q11. Syscall là gì? Overhead?

**A:**
- EN: A **system call** requests the kernel to perform privileged operations (I/O, memory, processes). It requires a **mode switch** from user to kernel mode — ~100-1000ns overhead. Minimize syscalls via: batching (`writev`), buffering, `io_uring` (Linux 5.1+ async I/O).
- VI: **System call** yêu cầu kernel thực hiện tác vụ có quyền (I/O, memory, process). Cần **mode switch** từ user sáng kernel mode — ~100-1000ns overhead. Giảm syscall qua: batching (`writev`), buffering, `io_uring` (Linux 5.1+ async I/O).

```cpp
// Common syscalls: read, write, open, close, mmap, fork, socket
// Reduce overhead:
// 1. Batch: writev, sendmsg (multiple buffers in one call)
// 2. io_uring: async I/O, minimizes mode switches
// 3. Buffer: accumulate data, write once
```

Follow-up (EN): What is `io_uring` and how does it reduce syscall overhead?

---

### Q12. `mmap` vs `read`/`write` — khi nào dùng mmap?

**A:**
- EN: `read`/`write`: copies data between kernel and user buffers (two copies). `mmap`: maps file directly into virtual address space — **zero-copy**. Use mmap for: large files with random access, shared memory between processes, database buffer pools. Use `read`/`write` for: sequential access, small files, network I/O.
- VI: `read`/`write`: copy data giữa kernel và user buffer (2 ban copy). `mmap`: map file trực tiếp vào virtual address space — **zero-copy**. Dùng mmap cho: file lớn truy cập ngẫu nhiên, shared memory giữa process, database buffer pool. Dùng `read`/`write` cho: truy cập tuan từ, file nhỏ, network I/O.

```cpp
// read/write: two copies (kernel buffer <-> user buffer)
read(fd, buf, 4096);
process(buf);

// mmap: zero-copy (file mapped directly into address space)
void* ptr = mmap(nullptr, size, PROT_READ, MAP_PRIVATE, fd, 0);
process((char*)ptr);  // access like memory, OS loads pages on demand
munmap(ptr, size);
```

Follow-up (EN): What are the risks of using `mmap` (SIGBUS on truncated file, address space fragmentation)?

---

## Flash card

| Question / Câu hỏi | Quick answer / Trả lỗi nhanh |
|---|---|
| Process vs Thread memory? | Process: separate; Thread: shared |
| Page fault? | Access page not in RAM — OS loads from disk |
| Signal-safe functions? | Very few: write(), _exit(), sig_atomic_t assignment |
| SIGKILL vs SIGTERM? | SIGKILL: uncatchable; SIGTERM: catchable |
| select vs epoll? | epoll: O(1) per event; select: O(n), 1024 fd limit |
| ELF .bss vs .data? | .bss: uninitialized (zero, nó disk); .data: initialized |
| `-fPIC`? | Position Independent Code, required for shared libraries |
| `dlopen` purpose? | Load shared library at runtime — plugin system |
| mmap zero-copy? | File mapped directly into virtual memory, nó copies |
| Syscall overhead? | ~100-1000ns due to user-to-kernel mode switch |
