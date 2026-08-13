# 09 - Mock Interview Bank (Senior C/C++)

Huong dan: Moi lan mock chon 12-15 cau, can bang cac nhom. Moi cau tra loi 2-5 phut.

## A. Nen tang C/C++ (10 cau)

1. UB la gi? Cho 3 vi du va tai sao compiler co the toi uu "ky la".
- Dap an ky vong: dinh nghia UB + examples (OOB, signed overflow, data race) + optimizer assumptions.

2. So sanh stack, heap, static storage duration, thread local.
- Dap an ky vong: life-time, scope, cost, use case.

3. Rule of 0/3/5 va khi nao can custom special members.
- Dap an ky vong: neu quan ly resource thu cong thi can 5; uu tien rule of 0.

4. Tai sao destructor base class can virtual trong polymorphism?
- Dap an ky vong: delete qua base pointer de goi dung dtor derived.

5. `const` correctness anh huong API quality ra sao?
- Dap an ky vong: ro contract, cho phep optimize, giam bug mutability.

6. `std::move` khong move that su la sao?
- Dap an ky vong: cast sang rvalue ref; move xay ra neu move ctor/assign duoc goi.

7. Exception safety levels la gi?
- Dap an ky vong: basic/strong/no-throw + vi du.

8. Header guard va ODR violation thuong xay ra khi nao?
- Dap an ky vong: multiple definitions, inline/static specifics.

9. `string_view` loi ich va bay life-time.
- Dap an ky vong: non-owning view; dangling neu nguon het doi song.

10. `shared_ptr` cycle va cach pha.
- Dap an ky vong: dung weak_ptr.

## B. STL + Algorithm (10 cau)

11. Khi nao chon `vector` thay vi `list` du logic insert giua?
- Dap an ky vong: locality + benchmark thuc te thuong vector nhanh hon.

12. `map` vs `unordered_map` trong he thong latency-sensitive?
- Dap an ky vong: average vs worst-case, order, memory overhead, hash quality.

13. Iterator invalidation trong `vector`, `deque`, `list`.
- Dap an ky vong: nho cac rule co ban va reallocation.

14. Erase-remove idiom giai thich tung buoc.
- Dap an ky vong: `remove_if` partition, `erase` cat duoi.

15. Tai sao algorithm STL de an toan hon loop tay?
- Dap an ky vong: express intent, less bug, optimized.

16. Co nen dung `emplace_back` mac dinh?
- Dap an ky vong: khong luon; phu thuoc context construction.

17. `reserve` co tac dung gi va khi nao vo nghia?
- Dap an ky vong: giam realloc; vo nghia neu khong biet size/size nho.

18. Big-O va "hidden constants".
- Dap an ky vong: branch/cache/alloc/coherency.

19. `stable_sort` khi nao can?
- Dap an ky vong: giu thu tu bang nhau.

20. `vector<bool>` co gi khac thuong?
- Dap an ky vong: bit proxy specialization.

## C. Concurrency (12 cau)

21. Data race vs race condition.
- Dap an ky vong: data race => UB; race condition la logic.

22. Acquire-release bang vi du producer/consumer.
- Dap an ky vong: store-release + load-acquire nhin thay du lieu.

23. Tinh huong dung `memory_order_relaxed`.
- Dap an ky vong: counters/statistics doc lap.

24. Spurious wakeup va wait predicate.
- Dap an ky vong: luon wait trong loop/predicate.

25. Deadlock prevention strategies.
- Dap an ky vong: lock ordering, scoped_lock, timeout.

26. False sharing la gi?
- Dap an ky vong: cung cache line, writer conflict.

27. Thread pool design can gi?
- Dap an ky vong: queue, worker lifecycle, backpressure, shutdown.

28. Lock-free co phai luon nhanh?
- Dap an ky vong: khong; complexity cao, benchmark-driven.

29. ABA problem.
- Dap an ky vong: A->B->A lam CAS bi lua.

30. Khi nao dung `jthread`?
- Dap an ky vong: auto join + cancellation cooperative.

31. Cach test code concurrent.
- Dap an ky vong: stress test, TSAN, deterministic seeds.

32. Neu can timeout + cancel task dang cho I/O?
- Dap an ky vong: cancellation token + non-blocking/polling strategy.

## D. System Design C++ (12 cau)

33. Design URL shortener (hoac ID service) voi C++ backend.
- Dap an ky vong: ID generation, storage, cache, scaling.

34. Design in-memory rate limiter.
- Dap an ky vong: token bucket/sliding window + distributed state.

35. Design log ingestion pipeline p99<100ms.
- Dap an ky vong: batching, queue, backpressure, drop policy.

36. Cach giu ABI on dinh cho library C++?
- Dap an ky vong: pimpl, C API boundary, symbol versioning.

37. Reliable retry policy cho external dependency.
- Dap an ky vong: timeout + exponential backoff + jitter + idempotency.

38. Cache invalidation strategy.
- Dap an ky vong: TTL/event-based/versioned key + stampede protection.

39. Message ordering guarantee trong queue.
- Dap an ky vong: partition key, per-partition ordering.

40. Exactly-once semantics thuc te.
- Dap an ky vong: effectively-once via dedup/idempotency.

41. Multi-tenant service constraints.
- Dap an ky vong: isolation quota, noisy neighbor control.

42. Rollout an toan cho thay doi lon.
- Dap an ky vong: canary, feature flag, rollback fast.

43. Observability baseline cho service moi.
- Dap an ky vong: golden signals + trace + alert SLO.

44. Postmortem quality checklist.
- Dap an ky vong: root cause, guardrail, owner, due date.

## E. Debugging + Performance (10 cau)

45. Quy trinh toi uu latency.
- Dap an ky vong: measure -> locate hotspot -> change -> verify.

46. Khi nao su dung ASan/TSan/UBSan?
- Dap an ky vong: map dung cho tung loai loi.

47. LTO va PGO trong production build.
- Dap an ky vong: trade-off build time vs runtime speed.

48. Vi sao benchmark local nhanh nhung production cham?
- Dap an ky vong: data shape, cache, NUMA, I/O, contention.

49. Heap fragmentation xu ly sao?
- Dap an ky vong: pooling, arena, allocation patterns.

50. Cach doc flame graph.
- Dap an ky vong: width = time ratio, tap trung stack rong.

51. p99 tang nhung p50 on dinh nghia la gi?
- Dap an ky vong: tail latency issue, contention, GC/IO bursts.

52. Nhan dien false bottleneck.
- Dap an ky vong: correlation != causation, can controlled experiment.

53. Debug crash hiem gap.
- Dap an ky vong: core dump + symbols + sanitizers + bisect.

54. Khi nao rewrite thay vi optimize?
- Dap an ky vong: debt qua lon, architecture mismatch, roi ro rewrite.

## F. Behavioral + Seniority (10 cau)

55. Lan ban quyet dinh no voi 1 de xuat ky thuat.
56. Lan ban dan dat migration khong downtime.
57. Lan ban mentor junior va ket qua.
58. Lan ban xu ly disagreement voi PM.
59. Lan ban fail va hoc duoc gi.
60. Cach ban uu tien cong viec khi moi thu deu gap.
61. Cach ban danh gia effort/risk truoc khi commitment.
62. Cach ban giu chat luong code trong team nhanh.
63. Cach ban truyen dat trade-off cho stakeholder.
64. Why you for senior role?

Dap an ky vong behavioral:
- STAR ro rang
- Co metric truoc/sau
- Co bai hoc va preventive action
- Co tac dong den team, khong chi ca nhan

## Rubric cham nhanh (0-2 diem moi tieu chi)

- Do dung technical
- Do sau va trade-off
- Clarity va cau truc
- Practicality (kinh nghiem thuc te)
- Senior signal (ownership, risk, leadership)

Tong 10 diem/cau:
- 8-10: senior strong
- 6-7: pass can cai thien
- <=5: can on lai chu de
