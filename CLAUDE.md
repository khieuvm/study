# Study — C/C++ Senior Interview Prep

Day la project hoc tap ca nhan cua toi, muc tieu chuan bi phong van vi tri **Senior C/C++ Engineer**.

## Muc tieu

He thong toan bo kien thuc C/C++ tu co ban den nang cao, bao gom dap an chi tiet, vi du code thuc te, va nhung diem de gap trong phong van senior.

## Cau truc file

| File | Noi dung |
|------|----------|
| `01-c-core.md` | C co ban: data types, pointers, UB, build pipeline, storage class |
| `02-cpp-oop.md` | OOP: class, inheritance, virtual, vtable, RAII |
| `03-cpp-memory.md` | Memory: stack/heap, smart pointers, allocators |
| `04-cpp-templates.md` | Templates, SFINAE, variadic, type traits |
| `05-cpp-stl.md` | STL containers, iterators, algorithms |
| `06-cpp-modern.md` | C++11/14/17/20: move semantics, lambda, constexpr, concepts |
| `07-concurrency.md` | Threads, mutex, atomic, memory model |
| `08-design-patterns.md` | Design patterns trong C++ |
| `09-optimization.md` | Cache, SIMD, profiling, compiler flags |
| `10-systems.md` | OS, syscall, networking, IPC, ELF/ABI |
| `11-telecom-fundamentals.md` | 3GPP, LTE/5G protocol stack, DSP, RTOS, SCTP |
| `12-system-design.md` | System design: reliability, observability, capacity |
| `13-debugging-performance.md` | Debug flow, sanitizers, profiling tools, incident response |
| `14-behavioral-leadership.md` | Behavioral: STAR, ownership, conflict, mentoring |
| `15-mock-interview-bank.md` | Ngan hang cau hoi mock interview (chua co dap an chi tiet) |

## Quy uoc file

- Moi Q&A co format: `### Q<n>. <cau hoi>`
- Dap an bat dau bang `**A:**`
- Co vi du code, bang so sanh, va best practice
- Cuoi moi file co **Flash card** de on nhanh

## Cach su dung

1. Doc Q truoc, tu tra loi, roi xem dap an
2. Nhung cau co code example -> chay thu, debug de hieu sau
3. Flash card -> on lai truoc phong van

## Luu y khi doc

- Code example la minimal, muc dich minh hoa — khong phai production code
- Cac cau "follow-up thuong gap" la nhung gi interviewer hay hoi tiep theo
- Nhung diem co note "UB" hoac "nguy hiem" -> thuoc long vi hay bi hoi trick question

## Quy tac khi update code

- Sau khi update code Streamlit, LUON verify syntax (`ast.parse`) va restart app
- Review lai logic truoc khi bao xong: widget state phai dong bo voi progress data
- Stats/metrics phai render SAU khi widgets update progress (dung placeholder pattern)
- Khong dung emoji trong code Streamlit (encoding issues tren Windows)
- Test parse_qa tren moi file `.md` sau khi thay doi parser
