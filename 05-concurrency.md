# 05 - Concurrency và Memory Model (Senior)

## 1) Threading cần ban nhưng để hỏi sau

### Q1. Data race là gì?
A: Hai thread truy cập cũng memory location, ít nhất 1 ghi, không đóng bỏ dùng. Data race => UB.

### Q2. Race condition và data race có gìống nhau?
A: Không. Race condition là logic phụ thuộc thứ tự xảy ra; data race là vì pham memory model.

### Q3. `std::thread` và `std::jthread`?
A: `jthread` (C++20) có auto-join và stop token ho tro huy cooperative.

## 2) Atomics

### Q4. `std::atomic<int>` đảm bảo gì?
A: Atomicity cho operation trên biến do. không tự động đảm bảo toan bỏ protocol logic.

### Q5. Memory order có các muc nào?
A: `relaxed`, `consume` (it dùng), `acquire`, `release`, `acq_rel`, `seq_cst`.

### Q6. Acquire/Release hiểu đơn giản?
A: Store-release cổng bỏ dữ liệu trước do; load-acquire nhìn thấy dữ liệu do nếu đóng bỏ thành cổng.

### Q7. Khi nào dùng `relaxed`?
A: Khi chỉ cần atomicity của biến dem/độc lập, không cần ordering với dữ liệu khác.

## 3) Mutex và deadlock

### Q8. Deadlock 4 điều kiện Coffman?
A: Mutual exclusion, hold-and-wait, nó preemption, circular wait.

### Q9. Cách tránh deadlock trong code C++?
A: Quy uoc thứ tự lock, lock hierarchy, `std::scoped_lock` lock nhiều mutex cũng luc.

### Q10. `condition_variable` có cần loop khi wait?
A: Có. Vì có spurious wakeup. Luôn `wait(lock, predicate)` hoặc while-check predicate.

## 4) Lock-free cần ban

### Q11. Lock-free có nghĩa là nhanh hơn lock?
A: Không luôn. Có thể nhanh hơn o tránh chap cao, nhưng phức tạp, kho dùng, có van để ABA.

### Q12. ABA problem là gì?
A: Giá trị A đổi thành B rồi ve A, compare-exchange thay van A nên nghi không đổi, dan đến lỗi logic.

## 5) Practical senior questions

### Q13. Cách debug bug concurrency hiếm gap?
A:
1. Bắt TSAN.
2. Log có timestamp/thread id.
3. Làm test stress + deterministic scheduler (nếu có).
4. Giảm chia sẻ mutable state.

### Q14. False sharing là gì?
A: Nhiều thread ghi vào biến khác nhau nhưng cũng cache line, gây ping-pong cache coherency.

### Q15. Cách giảm false sharing?
A: Canh le/padding dữ liệu nong theo cache line, tách writer data structures.

### Q16. Thread pool tại sao huu ich?
A: Giảm chi phí tạo/huy thread, gioi hanh muc concurrency, cai thien latency ổn định.

## 6) Muc senior leadership

### Q17. Khi nào ưu tiên đơn giản hon lock-free?
A: Mặc định. Lock-free chỉ dùng khi profile xác nhận lock là bottleneck nghiêm trọng.

### Q18. Cách review code concurrent của team?
A: Kiểm tra ownership state, lock ordering, invariant được báo ve boi lock nào, exception path.
