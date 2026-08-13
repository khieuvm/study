# Exercise 01 - Memory va Ownership Audit

## De bai
Ban duoc doan API C cu:

```c
char* load_config(const char* path);
void process_config(const char* cfg);
```

Team thuong bi leak va double-free vi ownership khong ro.

## Yeu cau
1. De xuat lai contract ownership ro rang.
2. Viet lai API theo C++ RAII (co the dung `std::string`, `std::unique_ptr<char[]>`, hoac wrapper type).
3. Liet ke 5 test case gom error path.

## Dap an goi y
- Cach 1: API tra `std::string`.
- Cach 2: Neu can C-ABI, tra struct `{char* data; size_t len;}` + ham free di kem.
- Luon tai lieu hoa ai co quyen giai phong.

## Rubric
- Ownership contract ro (0-4)
- Xu ly loi/exception path (0-3)
- Test coverage (0-3)
