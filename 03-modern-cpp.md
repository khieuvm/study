# 03 - Modern C++ (11/14/17/20/23)

## 1) C++11/14 cot loi

### Q1. `auto` dung sao cho dung?
A: Dung de giam lap type dai va tranh mismatch. Khong nen dung neu lam mo nghia API/public interface.

### Q2. `decltype(auto)` khi nao can?
A: Khi muon giu nguyen value category/constness cua bieu thuc tra ve.

### Q3. Lambda capture `[=]` va `[&]` rui ro gi?
A: `[=]` co the copy object nang/khong dong bo; `[&]` de dang dangling reference neu lambda song lau hon scope.

## 2) C++17 phai biet

### Q4. `std::optional` dung khi nao?
A: Ham co the khong co gia tri tra ve, thay vi sentinel value/null pointer.

### Q5. `std::variant` va `std::visit`?
A: Sum type an toan kieu, thay cho union + tag thu cong.

### Q6. `std::string_view` loi ich va bay?
A: Tranh copy string, nhung khong so huu du lieu. De dính dangling view.

### Q7. Structured binding co copy khong?
A: Tuy context. Co the copy hoac bind reference. Can chu y `auto` vs `auto&`.

## 3) C++20

### Q8. Concept dung de lam gi?
A: Rang buoc template ro rang, loi compile de doc hon, API generic de hieu hon.

### Q9. `ranges` cai thien gi?
A: Compose algorithm + view de lazy evaluation, code declarative hon.

### Q10. Coroutines la gi (muc senior can noi)?
A: Co che suspend/resume compile-time transform. Dung cho async/generator, toi uu hon callback spaghetti.

### Q11. `std::span` dung khi nao?
A: Truyen view cua contiguous memory (pointer + size) an toan hon cap doi tham so.

## 4) Template nang cao

### Q12. Fold expression la gi?
A: Rut gon parameter pack, vi du `(args + ...)`.

### Q13. CRTP dung khi nao?
A: Static polymorphism, tranh virtual dispatch runtime.

### Q14. Type traits de lam gi?
A: Kiem tra/ra quyet dinh kieu o compile-time (`is_trivially_copyable`, `is_same`, ...).

## 5) Build va package ecosystem

### Q15. Vi sao senior can biet CMake target-based?
A: Vi truyen include/define/link options theo target ro rang, tranh global state kho debug.

### Q16. `FetchContent`, `find_package`, `add_subdirectory` trade-off?
A:
- `find_package`: tot cho dependency duoc cai san
- `FetchContent`: reproducible hon, nhung tang thoi gian configure
- `add_subdirectory`: tiep can source truc tiep

### Q17. Co nen header-only moi thu?
A: Khong. Build cham, code bloat, leakage implementation. Dung khi thu vien nho/template-heavy.

## 6) Cac diem hay hoi de phan cap senior

### Q18. ABI compatibility la gi?
A: Tuong thich binary giua version/library/compiler settings. Pha ABI co the crash du compile pass.

### Q19. Inline namespace cho versioning?
A: Giup version symbol trong C++ library ma van giu API de dung.

### Q20. Khi nao dung module (C++20 modules)?
A: Du an lon can giam compile time va an implementation; he sinh thai toolchain con dang truong thanh.
