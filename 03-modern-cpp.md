# 03 - Modern C++ (11/14/17/20/23)

## 1) C++11/14 cot lỗi

### Q1. `auto` dùng sao cho dùng?
A: Dùng để giảm lặp type dai và tránh mismatch. không nên dùng nếu làm mo nghĩa API/public interface.

### Q2. `decltype(auto)` khi nào cần?
A: Khi muốn giữ nguyen value category/constness của bieu thực trả về.

### Q3. Lambda capture `[=]` và `[&]` rủi ro gì?
A: `[=]` có thể copy object nang/không đóng bỏ; `[&]` để đang dangling reference nếu lambda sóng lau hon scope.

## 2) C++17 phải biết

### Q4. `std::optional` dùng khi nào?
A: Hàm có thể không có giá trị trả về, thay vì sentinel value/null pointer.

### Q5. `std::variant` và `std::visit`?
A: Sum type an toàn kiểu, thay cho union + tag thủ công.

### Q6. `std::string_view` lỗi ich và bay?
A: Tránh copy string, nhưng không số huu dữ liệu. Để dính dangling view.

### Q7. Structured binding có copy không?
A: Tuy context. Có thể copy hoặc bind reference. Cần chu y `auto` vs `auto&`.

## 3) C++20

### Q8. Concept dùng để làm gì?
A: Rang bước template rõ rang, lỗi compile để đọc hon, API generic để hiểu hon.

### Q9. `ranges` cai thien gì?
A: Compose algorithm + view để lazy evaluation, code declarative hon.

### Q10. Coroutines là gì (muc senior cần nơi)?
A: Cơ chế suspend/resume compile-time transform. Dùng cho async/generator, tối ưu hon callback spaghetti.

### Q11. `std::span` dùng khi nào?
A: Truyen view của contiguous memory (pointer + size) an toàn hon cấp đổi tham số.

## 4) Template nâng cao

### Q12. Fold expression là gì?
A: Rut gon parameter pack, ví dụ `(args + ...)`.

### Q13. CRTP dùng khi nào?
A: Static polymorphism, tránh virtual dispatch runtime.

### Q14. Type traits để làm gì?
A: Kiểm tra/ra quyết định kiểu o compile-time (`is_trivially_copyable`, `is_same`, ...).

## 5) Build và package ecosystem

### Q15. Vì sao senior cần biết CMake target-based?
A: Vì truyen include/define/link options theo target rõ rang, tránh global state kho debug.

### Q16. `FetchContent`, `find_package`, `add_subdirectory` trade-off?
A:
- `find_package`: tốt cho dependency được cai sẵn
- `FetchContent`: reproducible hon, nhưng tăng thời gian configure
- `add_subdirectory`: tiếp cần source trực tiếp

### Q17. Có nên header-only mọi thu?
A: Không. Build chậm, code bloat, leakage implementation. Dùng khi thu vien nhỏ/template-heavy.

## 6) Các điểm hay hỏi để phân cấp senior

### Q18. ABI compatibility là gì?
A: Tương thích binary giữa version/library/compiler settings. Phá ABI có thể crash đủ compile pass.

### Q19. Inline namespace cho versioning?
A: Giúp version symbol trong C++ library mà van giữ API để dùng.

### Q20. Khi nào dùng module (C++20 modules)?
A: Đủ an lớn cần giảm compile time và ẩn implementation; he sinh thai toolchain còn đang trường thành.
