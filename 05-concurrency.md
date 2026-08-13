# 05 - Concurrency va Memory Model (Senior)

## 1) Threading can ban nhung de hoi sau

### Q1. Data race la gi?
A: Hai thread truy cap cung memory location, it nhat 1 ghi, khong dong bo dung. Data race => UB.

### Q2. Race condition va data race co giong nhau?
A: Khong. Race condition la logic phu thuoc thu tu xay ra; data race la vi pham memory model.

### Q3. `std::thread` va `std::jthread`?
A: `jthread` (C++20) co auto-join va stop token ho tro huy cooperative.

## 2) Atomics

### Q4. `std::atomic<int>` dam bao gi?
A: Atomicity cho operation tren bien do. Khong tu dong dam bao toan bo protocol logic.

### Q5. Memory order co cac muc nao?
A: `relaxed`, `consume` (it dung), `acquire`, `release`, `acq_rel`, `seq_cst`.

### Q6. Acquire/Release hieu don gian?
A: Store-release cong bo du lieu truoc do; load-acquire nhin thay du lieu do neu dong bo thanh cong.

### Q7. Khi nao dung `relaxed`?
A: Khi chi can atomicity cua bien dem/doc lap, khong can ordering voi du lieu khac.

## 3) Mutex va deadlock

### Q8. Deadlock 4 dieu kien Coffman?
A: Mutual exclusion, hold-and-wait, no preemption, circular wait.

### Q9. Cach tranh deadlock trong code C++?
A: Quy uoc thu tu lock, lock hierarchy, `std::scoped_lock` lock nhieu mutex cung luc.

### Q10. `condition_variable` co can loop khi wait?
A: Co. Vi co spurious wakeup. Luon `wait(lock, predicate)` hoac while-check predicate.

## 4) Lock-free can ban

### Q11. Lock-free co nghia la nhanh hon lock?
A: Khong luon. Co the nhanh hon o tranh chap cao, nhung phuc tap, kho dung, co van de ABA.

### Q12. ABA problem la gi?
A: Gia tri A doi thanh B roi ve A, compare-exchange thay van A nen nghi khong doi, dan den loi logic.

## 5) Practical senior questions

### Q13. Cach debug bug concurrency hiem gap?
A:
1. Bat TSAN.
2. Log co timestamp/thread id.
3. Lam test stress + deterministic scheduler (neu co).
4. Giam chia se mutable state.

### Q14. False sharing la gi?
A: Nhieu thread ghi vao bien khac nhau nhung cung cache line, gay ping-pong cache coherency.

### Q15. Cach giam false sharing?
A: Canh le/padding du lieu nong theo cache line, tach writer data structures.

### Q16. Thread pool tai sao huu ich?
A: Giam chi phi tao/huy thread, gioi hanh muc concurrency, cai thien latency on dinh.

## 6) Muc senior leadership

### Q17. Khi nao uu tien don gian hon lock-free?
A: Mac dinh. Lock-free chi dung khi profile xac nhan lock la bottleneck nghiem trong.

### Q18. Cach review code concurrent cua team?
A: Kiem tra ownership state, lock ordering, invariant duoc bao ve boi lock nao, exception path.
