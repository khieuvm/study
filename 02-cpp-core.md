# 02 - C++ Core (Senior must-know)

## 1) OOP, object model

### Q1. Class và struct khác nhau gì?
A: Mặc định truy cập: `class` là `private`, `struct` là `public`. Còn lại gìống nhau.

### Q2. Virtual function table là gì?
A: Cơ chế runtime dispatch thông qua vtable/vptr (implementation detail), cho phép đa hình đóng.

### Q3. Khi nào destructor cần virtual?
A: Khi class được dùng polymorphic và có thể delete qua base pointer.

### Q4. Rule of 3/5/0?
A:
- Rule of 3: nếu cần custom dtor/copy ctor/copy assign thì cần ca 3.
- Rule of 5: thêm move ctor/move assign.
- Rule of 0: ưu tiên thiết kế không cần viết special members.

## 2) Value category + move semantics

### Q5. lvalue, xvalue, prvalue?
A: 
- lvalue: có danh tinh
- xvalue: sap hết đổi sóng, có thể move
- prvalue: temporary thường không có danh tinh

### Q6. `std::move` có move that su không?
A: Không. No chi ep kiểu thành rvalue reference; move thực sự xảy ra nếu type có move operation.

### Q7. Khi nào Không nên move?
A: Khi van cần sử dụng object với invariant gìả định cũ, hoặc object nhỏ trivially copyable và copy rẻ.

### Q8. `noexcept` liên quan gì đến move?
A: Container (như `vector`) ưu tiên move khi move ctor `noexcept`; nếu không có thể fallback copy để đảm bảo strong exception guarantee.

## 3) Smart pointer + ownership

### Q9. `unique_ptr` vs `shared_ptr`?
A: `unique_ptr` ownership đọc quyền, nhe. `shared_ptr` đệm tham chiếu, ton chi phí atomics/control block.

### Q10. `weak_ptr` dùng để làm gì?
A: Phá vong tham chiếu khi dùng `shared_ptr`, truy cập an toàn qua `lock()`.

### Q11. Tại sao không nên truyen `shared_ptr` boi value mọi nơi?
A: Tăng/giảm refcount thường xuyen, tiếp tay ownership mo ho. Nên truyen `T&`, `T*`, hoặc `const shared_ptr<T>&` tuy y do.

### Q12. RAII là gì?
A: Resource Acquisition Is Initialization. Gần resource vào object life-time để tự động release trong destructor.

## 4) Exception safety

### Q13. 3 muc exception guarantee?
A: Basic, strong, no-throw.

### Q14. Nếu constructor nem exception thì sao?
A: Object chưa được tạo hoan chính; destructor của object do không chạy, nhưng member đã tạo thành cổng sẽ được huy.

### Q15. Có nên nem exception trong destructor?
A: Không nên. Destructor nên `noexcept`; throw trong stack unwinding có thể `std::terminate`.

## 5) Templates cần ban cho senior

### Q16. Template instantiation time và code bloat?
A: Instantiate tại compile-time, có thể làm tăng binary size. Giảm bảng type erasure, explicit instantiation, giảm duplicate.

### Q17. SFINAE là gì?
A: Substitution Failure Is Not An Error: thay thế template fail thì bỏ qua overload thay vì lỗi.

### Q18. `constexpr` và `consteval`?
A: `constexpr` có thể tinh compile-time nếu đủ điều kiện. `consteval` bắt buộc compile-time.

## 6) API design (senior)

### Q19. Khi nào dùng pass-by-value + move?
A: Khi hàm cần bản sao nội bộ và đối tượng có move rẻ; caller có thể move vào hàm.

### Q20. Cách thiết kế API it UB?
A: Rõ precondition, dùng type mạnh (`span`, `string_view` cần than life-time), han che raw pointer ownership.

## 7) Các câu hỏi "xoay"

### Q21. `new`/`delete` khi nào nên tránh?
A: Gần như luôn ưu tiên smart pointer/container. Raw `new/delete` chỉ dùng o low-level allocator/framework.

### Q22. `dynamic_cast` có xấu không?
A: Không xấu nếu dùng dùng muc. Nhiều `dynamic_cast` có thể là dấu hiệu model dữ liệu/OOP chưa tối ưu.

### Q23. Có nên inline mọi thu?
A: Không. Compiler từ quyết định inline tối ưu. `inline` chu yếu cho ODR/linkage với function trong header.

### Q24. PIMPL trade-off?
A: Giảm rebuild, ẩn implementation, ổn định ABI; đổi lại tăng indirection + cấp phát đóng.
