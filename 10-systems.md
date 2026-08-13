# 10 - Systems Programming (OS, Networking, IPC)

---

## 1) Process & Thread

### Q1. Process vs Thread khac nhau the nao?

**A:**

| | Process | Thread |
|---|---|---|
| Memory space | Rieng (virtual address space) | Chia se voi threads khac cung process |
| Tao moi | Ton kem (`fork`/`CreateProcess`) | Nhanh hon (`pthread_create`/`CreateThread`) |
| Giao tiep | IPC (pipe, socket, shm) | Shared memory, de hon nhung can sync |
| Loi | Crash 1 process khong anh huong process khac | 1 thread crash co the kill ca process |
| Context switch | Ton kem (flush TLB, swap page table) | Nhanh hon (cung address space) |

```cpp
// Fork in Linux: tao process con la ban sao cua cha
pid_t pid = fork();
if (pid < 0) {
    perror("fork failed");
} else if (pid == 0) {
    // Con
    printf("Child PID: %d\n", getpid());
    execv("/bin/ls", args);  // thay the process image
    _exit(1);
} else {
    // Cha
    printf("Parent, child PID: %d\n", pid);
    int status;
    waitpid(pid, &status, 0);  // cho con ket thuc
}
```

---

### Q2. Virtual memory la gi?

**A:** Moi process thay no co **khong gian dia chi rieng** (4GB tren 32-bit, 128TB tren x86-64). OS map virtual address -> physical address qua **page table**.

```
Virtual address: 0x0000 - 0x7FFF... (user space)
                 0x8000 - 0xFFFF... (kernel space)

Page: 4KB unit cua virtual/physical memory
Page table: map virtual page -> physical frame
TLB (Translation Lookaside Buffer): cache cua page table lookups
```

**Page fault**: truy cap page chua o RAM -> OS load tu disk (swap/page file). Neu page khong hop le -> SIGSEGV (segmentation fault).

```cpp
// mmap: map file vao virtual memory
int fd = open("data.bin", O_RDONLY);
size_t size = get_file_size(fd);
void* ptr = mmap(nullptr, size, PROT_READ, MAP_PRIVATE, fd, 0);
// Bây gio doc file nhu doc memory: ptr[0], ptr[1], ...
// OS load pages on-demand (lazy)
munmap(ptr, size);
close(fd);
```

---

### Q3. Stack frame trong function call la gi?

**A:** Moi function call tao 1 **stack frame** (activation record) tren stack, chua: return address, saved registers, local variables, arguments.

```
Stack (grow down):
+-------------------+  <- Stack pointer (RSP)
| local vars        |
| saved registers   |
| return address    |  <- base pointer (RBP)
+-------------------+  <- caller's frame
| caller's locals   |
| ...               |
```

```cpp
// Stack frame layout (x86-64 Linux ABI):
void foo(int a, int b) {    // a, b truyen qua register (rdi, rsi)
    int local = a + b;      // local tren stack: [rbp - 4]
    bar(local);             // push return addr, jump to bar
}

// Stack overflow:
void infinite() { infinite(); }  // moi call them 1 frame -> SIGSEGV
```

---

## 2) Signals

### Q4. Signal trong Unix/Linux la gi?

**A:** Signal la **notification** gui cho process ve mot su kien. Process co the: ignore, catch (custom handler), hoac default action (thuong la terminate).

```cpp
#include <signal.h>

// Pho bien nhat:
// SIGINT  (2):  Ctrl+C
// SIGTERM (15): kill command (request terminate)
// SIGKILL (9):  kill -9 (cannot catch/ignore)
// SIGSEGV (11): Segmentation fault
// SIGABRT (6):  abort()
// SIGALRM (14): Timer

// Custom handler:
volatile sig_atomic_t g_running = 1;  // volatile la can thiet o day

void sigint_handler(int sig) {
    g_running = 0;  // safe: sig_atomic_t, assignment atomic
    // KHONG goi: printf, malloc, non-reentrant functions!
    // KHONG throw exception!
}

int main() {
    signal(SIGINT, sigint_handler);   // hoac sigaction (tot hon)
    // sigaction cho phep more control va reset sau signal
    struct sigaction sa{};
    sa.sa_handler = sigint_handler;
    sa.sa_flags   = SA_RESTART;       // restart interrupted syscalls
    sigaction(SIGINT, &sa, nullptr);

    while (g_running) {
        // main loop
    }
}
```

---

## 3) IPC (Inter-Process Communication)

### Q5. Cac phuong phap IPC chinh?

**A:**

| Phuong phap | Toc do | Pham vi | Su dung |
|---|---|---|---|
| Pipe (anonymous) | Nhanh | Same host, parent-child | Shell pipes |
| Named pipe (FIFO) | Nhanh | Same host | Unrelated processes |
| Unix socket | Nhanh | Same host | Client-server local |
| TCP/UDP socket | Cham hon (network stack) | Any host | Network |
| Shared memory | Nhanh nhat | Same host | High-throughput |
| Message queue | Trung binh | Same host | Async messaging |
| Signal | Rat cham | Same host | Notification only |

**Pipe example:**
```cpp
int pipefd[2];
pipe(pipefd);  // pipefd[0] = read end, pipefd[1] = write end

pid_t pid = fork();
if (pid == 0) {
    // Con: chi ghi
    close(pipefd[0]);
    write(pipefd[1], "hello", 5);
    close(pipefd[1]);
    _exit(0);
} else {
    // Cha: chi doc
    close(pipefd[1]);
    char buf[10];
    read(pipefd[0], buf, 10);
    close(pipefd[0]);
    printf("Got: %s\n", buf);
}
```

**Shared memory:**
```cpp
// POSIX shared memory
int fd = shm_open("/my_shm", O_CREAT|O_RDWR, 0666);
ftruncate(fd, 4096);
void* ptr = mmap(nullptr, 4096, PROT_READ|PROT_WRITE, MAP_SHARED, fd, 0);

// Viet tu process nay
*(int*)ptr = 42;

// Doc tu process khac (mo cung ten /my_shm)
int val = *(int*)ptr;

munmap(ptr, 4096);
shm_unlink("/my_shm");  // xoa khi xong
```

---

## 4) Networking

### Q6. Socket programming co ban trong C?

**A:**

```cpp
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

// TCP Server:
int server_fd = socket(AF_INET, SOCK_STREAM, 0);

// Cho phep reuse port (tranh "Address already in use")
int opt = 1;
setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

struct sockaddr_in addr{};
addr.sin_family      = AF_INET;
addr.sin_addr.s_addr = INADDR_ANY;
addr.sin_port        = htons(8080);

bind(server_fd, (sockaddr*)&addr, sizeof(addr));
listen(server_fd, 10);  // backlog = 10 pending connections

while (true) {
    sockaddr_in client_addr{};
    socklen_t len = sizeof(client_addr);
    int client_fd = accept(server_fd, (sockaddr*)&client_addr, &len);

    char buf[1024];
    ssize_t n = recv(client_fd, buf, sizeof(buf), 0);
    send(client_fd, "HTTP/1.1 200 OK\r\n\r\nHello", 24, 0);
    close(client_fd);
}

// TCP Client:
int sock = socket(AF_INET, SOCK_STREAM, 0);
struct sockaddr_in server{};
server.sin_family = AF_INET;
server.sin_port   = htons(8080);
inet_pton(AF_INET, "127.0.0.1", &server.sin_addr);
connect(sock, (sockaddr*)&server, sizeof(server));
send(sock, "GET / HTTP/1.0\r\n\r\n", 18, 0);
```

---

### Q7. Non-blocking I/O va epoll/select?

**A:** Default socket la **blocking** — `recv()` block thread den khi co data. Non-blocking I/O + event loop cho phep 1 thread xu ly nhieu connections.

```cpp
// select: portable nhung chiem khi nhieu fd
fd_set read_fds;
FD_ZERO(&read_fds);
FD_SET(sock, &read_fds);
struct timeval tv{5, 0};  // timeout 5 giay
int ready = select(sock+1, &read_fds, nullptr, nullptr, &tv);
if (ready > 0 && FD_ISSET(sock, &read_fds)) {
    recv(sock, buf, sizeof(buf), 0);
}

// epoll: Linux-specific, hieu qua O(1) cho nhieu connections
int epfd = epoll_create1(0);

struct epoll_event ev{};
ev.events  = EPOLLIN | EPOLLET;  // level-triggered hoac edge-triggered
ev.data.fd = server_fd;
epoll_ctl(epfd, EPOLL_CTL_ADD, server_fd, &ev);

struct epoll_event events[64];
while (true) {
    int n = epoll_wait(epfd, events, 64, -1);  // block cho den khi co event
    for (int i = 0; i < n; i++) {
        if (events[i].data.fd == server_fd) {
            // New connection
            int client = accept(server_fd, nullptr, nullptr);
            epoll_ctl(epfd, EPOLL_CTL_ADD, client, &ev);
        } else {
            // Data ready on events[i].data.fd
            recv(events[i].data.fd, buf, sizeof(buf), 0);
        }
    }
}
```

---

## 5) ELF & Build

### Q8. ELF format la gi? Sections chinh?

**A:** **ELF (Executable and Linkable Format)** la format binary tren Linux/Unix.

```
ELF Header
+------------------+
| .text            |  Machine code (executable)
| .rodata          |  Read-only data (string literals, const)
| .data            |  Initialized global/static variables
| .bss             |  Uninitialized global/static (zero-filled, khong chiem disk)
| .symtab          |  Symbol table (for linking, debug)
| .strtab          |  String table (symbol names)
| .debug_info      |  DWARF debug info (khi -g)
| .plt             |  Procedure Linkage Table (dynamic linking)
| .got             |  Global Offset Table (dynamic linking)
+------------------+
```

```bash
# Xem symbols:
nm -C prog              # C++ demangled symbols
readelf -s prog         # raw symbols
objdump -d prog         # disassemble

# Xem size cac section:
size prog

# Xem shared library dependencies:
ldd prog

# Xem section headers:
readelf -S prog
```

---

### Q9. Static linking vs Dynamic linking?

**A:**

| | Static | Dynamic |
|---|---|---|
| Luc link | Compile time (thieu vao binary) | Runtime |
| File size | To (chua tat ca) | Nho (chi tham chieu) |
| Startup | Nhanh hon | Cham hon (load .so) |
| Update library | Phai recompile | Chi update .so |
| Dependency | Khong (self-contained) | Phai co .so tren he thong |

```bash
# Static library:
ar rcs libmylib.a file1.o file2.o
g++ main.o -L. -lmylib -o prog      # link static

# Shared library:
g++ -shared -fPIC -o libmylib.so file1.o file2.o  # -fPIC: Position Independent Code
g++ main.o -L. -lmylib -Wl,-rpath,. -o prog       # link dynamic

# Check:
ldd prog   # libmylib.so => ./libmylib.so
file prog  # ELF ... dynamically linked
```

**`-fPIC` la gi?** Position-Independent Code: code co the load o bat ky dia chi, can cho shared library. Dung GOT (Global Offset Table) de truy cap global vars.

---

### Q10. `dlopen` / `dlsym` — plugin architecture?

**A:** Load shared library **at runtime** — cho phep plugin system.

```cpp
#include <dlfcn.h>

// Load plugin:
void* handle = dlopen("./plugin.so", RTLD_LAZY);
if (!handle) { fprintf(stderr, "%s\n", dlerror()); return; }

// Lay function pointer:
typedef int (*PluginFunc)(const char*);
PluginFunc fn = (PluginFunc)dlsym(handle, "plugin_run");

char* error = dlerror();
if (error) { fprintf(stderr, "%s\n", error); return; }

// Goi:
int result = fn("input data");

// Giai phong:
dlclose(handle);
```

---

## 6) System Calls

### Q11. Syscall la gi? Overhead?

**A:** **System call**: request kernel thuc hien tac vu co quyen (I/O, memory, process). Phai chuyen tu **user mode sang kernel mode** — ~100-1000ns overhead.

```cpp
// Syscalls pho bien:
read(fd, buf, n)     // doc file
write(fd, buf, n)    // ghi file
open/close           // mo/dong file
mmap/munmap          // map memory
fork/execve/wait     // process management
socket/bind/listen   // networking
futex                // fast mutex (co the o user space)

// Giam syscall overhead:
// 1. Batching: ghi nhieu o 1 syscall (writev, sendmsg)
// 2. io_uring (Linux 5.1+): async I/O, giam so syscall
// 3. Buffer: tich luy data, write 1 lan

// io_uring:
struct io_uring ring;
io_uring_queue_init(QUEUE_DEPTH, &ring, 0);

struct io_uring_sqe* sqe = io_uring_get_sqe(&ring);
io_uring_prep_read(sqe, fd, buf, len, 0);
io_uring_submit(&ring);

struct io_uring_cqe* cqe;
io_uring_wait_cqe(&ring, &cqe);  // cho ket qua
int result = cqe->res;
io_uring_cqe_seen(&ring, cqe);
```

---

### Q12. `mmap` vs `read`/`write` — khi nao dung mmap?

**A:**

**`read`/`write`**: copy data giua kernel buffer va user buffer — **2 copies**.
**`mmap`**: map file truc tiep vao virtual address space — **0 copies** (zero-copy).

```cpp
// read/write:
char buf[4096];
read(fd, buf, 4096);   // kernel -> buf copy
process(buf);
write(fd2, buf, 4096); // buf -> kernel copy

// mmap (zero-copy):
void* src = mmap(nullptr, size, PROT_READ, MAP_PRIVATE, fd, 0);
void* dst = mmap(nullptr, size, PROT_READ|PROT_WRITE, MAP_SHARED, fd2, 0);
memcpy(dst, src, size);  // direct memory copy, no syscall
```

**Khi nao dung mmap:**
- Doc file lon nhieu lan (OS cache, khong reread)
- Random access trong file lon (chi load page can)
- Inter-process shared memory
- Implementing database buffer pool

**Khi nao dung read/write:**
- Sequential access (buffered I/O hieu qua)
- Small files
- Network I/O (khong the mmap socket)

---

## Flash card

| Cau hoi | Tra loi nhanh |
|---|---|
| Process vs Thread memory? | Process: rieng biet; Thread: chia se voi process |
| Page fault la gi? | Truy cap page chua o RAM, OS load tu disk |
| Signal-safe functions? | Rat it: write(), _exit(), sem_post(), ... |
| SIGKILL vs SIGTERM? | SIGKILL: khong the catch; SIGTERM: co the catch/ignore |
| select vs epoll? | epoll O(1) voi nhieu fd; select O(n) |
| ELF .bss vs .data? | .bss: uninitialized (zero, khong chiem disk); .data: initialized |
| `-fPIC` la gi? | Position Independent Code, can cho shared library |
| `dlopen` dung de gi? | Load shared library runtime, plugin system |
| mmap zero-copy nghia la? | Map file truc tiep vao virtual memory, khong copy |
| Syscall overhead? | ~100-1000ns vi mode switch user->kernel |
