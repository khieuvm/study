# 02 - C++ Core (Senior must-know)

## 1) OOP, object model

### Q1. Class va struct khac nhau gi?
A: Mac dinh truy cap: `class` la `private`, `struct` la `public`. Con lai giong nhau.

### Q2. Virtual function table la gi?
A: Co che runtime dispatch thong qua vtable/vptr (implementation detail), cho phep da hinh dong.

### Q3. Khi nao destructor can virtual?
A: Khi class duoc dung polymorphic va co the delete qua base pointer.

### Q4. Rule of 3/5/0?
A:
- Rule of 3: neu can custom dtor/copy ctor/copy assign thi can ca 3.
- Rule of 5: them move ctor/move assign.
- Rule of 0: uu tien thiet ke khong can viet special members.

## 2) Value category + move semantics

### Q5. lvalue, xvalue, prvalue?
A: 
- lvalue: co danh tinh
- xvalue: sap het doi song, co the move
- prvalue: temporary thuong khong co danh tinh

### Q6. `std::move` co move that su khong?
A: Khong. No chi ep kieu thanh rvalue reference; move thuc su xay ra neu type co move operation.

### Q7. Khi nao KHONG nen move?
A: Khi van can su dung object voi invariant gia dinh cu, hoac object nho trivially copyable va copy re.

### Q8. `noexcept` lien quan gi den move?
A: Container (nhu `vector`) uu tien move khi move ctor `noexcept`; neu khong co the fallback copy de dam bao strong exception guarantee.

## 3) Smart pointer + ownership

### Q9. `unique_ptr` vs `shared_ptr`?
A: `unique_ptr` ownership doc quyen, nhe. `shared_ptr` dem tham chieu, ton chi phi atomics/control block.

### Q10. `weak_ptr` dung de lam gi?
A: Pha vong tham chieu khi dung `shared_ptr`, truy cap an toan qua `lock()`.

### Q11. Tai sao khong nen truyen `shared_ptr` boi value moi noi?
A: Tang/giảm refcount thuong xuyen, tiep tay ownership mo ho. Nen truyen `T&`, `T*`, hoac `const shared_ptr<T>&` tuy y do.

### Q12. RAII la gi?
A: Resource Acquisition Is Initialization. Gan resource vao object life-time de tu dong release trong destructor.

## 4) Exception safety

### Q13. 3 muc exception guarantee?
A: Basic, strong, no-throw.

### Q14. Neu constructor nem exception thi sao?
A: Object chua duoc tao hoan chinh; destructor cua object do khong chay, nhung member da tao thanh cong se duoc huy.

### Q15. Co nen nem exception trong destructor?
A: Khong nen. Destructor nen `noexcept`; throw trong stack unwinding co the `std::terminate`.

## 5) Templates can ban cho senior

### Q16. Template instantiation time va code bloat?
A: Instantiate tai compile-time, co the lam tang binary size. Giam bang type erasure, explicit instantiation, giam duplicate.

### Q17. SFINAE la gi?
A: Substitution Failure Is Not An Error: thay the template fail thi bo qua overload thay vi loi.

### Q18. `constexpr` va `consteval`?
A: `constexpr` co the tinh compile-time neu du dieu kien. `consteval` bat buoc compile-time.

## 6) API design (senior)

### Q19. Khi nao dung pass-by-value + move?
A: Khi ham can ban sao noi bo va doi tuong co move re; caller co the move vao ham.

### Q20. Cach thiet ke API it UB?
A: Ro precondition, dung type manh (`span`, `string_view` can than life-time), han che raw pointer ownership.

## 7) Cac cau hoi "xoay"

### Q21. `new`/`delete` khi nao nen tranh?
A: Gan nhu luon uu tien smart pointer/container. Raw `new/delete` chi dung o low-level allocator/framework.

### Q22. `dynamic_cast` co xau khong?
A: Khong xau neu dung dung muc. Nhieu `dynamic_cast` co the la dau hieu model du lieu/OOP chua toi uu.

### Q23. Co nen inline moi thu?
A: Khong. Compiler tu quyet dinh inline toi uu. `inline` chu yeu cho ODR/linkage voi function trong header.

### Q24. PIMPL trade-off?
A: Giam rebuild, an implementation, on dinh ABI; doi lai tang indirection + cap phat dong.
