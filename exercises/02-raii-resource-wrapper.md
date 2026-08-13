# Exercise 02 - RAII Resource Wrapper

## De bai
Thiet ke class `FileHandle` bao boi `FILE*`.

## Yeu cau
1. Constructor mo file, destructor dong file.
2. Cam copy, cho phep move.
3. Cung cap `read_all()` tra ve `std::string`.
4. Dam bao exception safety.

## Dap an goi y
- Rule of 5 (hoac 0 neu uy quyen object khac).
- Destructor `noexcept`.
- Move ctor/assign set nguon ve state hop le (`nullptr`).

## Rubric
- Dung RAII (0-4)
- Move semantics dung (0-3)
- Exception safety (0-3)
