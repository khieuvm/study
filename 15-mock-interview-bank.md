# 09 - Mock Interview Bank (Senior C/C++)

Hướng dan: Mọi lan mock chon 12-15 câu, cần bảng các nhom. Mọi câu trả lỗi 2-5 phut.

## A. Nên tăng C/C++ (10 câu)

1. UB là gì? Cho 3 ví dụ và tại sao compiler có thể tối ưu "ky là".
- Dap an ky vong: định nghĩa UB + examples (OOB, signed overflow, data race) + optimizer assumptions.

2. So sánh stack, heap, static storage duration, thread local.
- Dap an ky vong: life-time, scope, cost, use case.

3. Rule of 0/3/5 và khi nào cần custom special members.
- Dap an ky vong: nếu quản lý resource thủ công thì cần 5; ưu tiên rule of 0.

4. Tại sao destructor base class cần virtual trong polymorphism?
- Dap an ky vong: delete qua base pointer để gọi dùng dtor derived.

5. `const` correctness ảnh hưởng API quality ra sao?
- Dap an ky vong: rõ contract, cho phép optimize, giảm bug mutability.

6. `std::move` không move that su là sao?
- Dap an ky vong: cast sang rvalue ref; move xảy ra nếu move ctor/assign được gọi.

7. Exception safety levels là gì?
- Dap an ky vong: basic/strong/no-throw + ví dụ.

8. Header guard và ODR violation thường xảy ra khi nào?
- Dap an ky vong: multiple definitions, inline/static specifics.

9. `string_view` lỗi ich và bay life-time.
- Dap an ky vong: non-owning view; dangling nếu nguon hết đổi sóng.

10. `shared_ptr` cycle và cách phá.
- Dap an ky vong: dùng weak_ptr.

## B. STL + Algorithm (10 câu)

11. Khi nào chon `vector` thay vì `list` đủ logic insert giữa?
- Dap an ky vong: locality + benchmark thực tế thường vector nhanh hơn.

12. `map` vs `unordered_map` trong hệ thống latency-sensitive?
- Dap an ky vong: average vs worst-case, order, memory overhead, hash quality.

13. Iterator invalidation trong `vector`, `deque`, `list`.
- Dap an ky vong: nhỏ các rule cơ bản và reallocation.

14. Erase-remove idiom giải thích từng bước.
- Dap an ky vong: `remove_if` partition, `erase` cat dưới.

15. Tại sao algorithm STL để an toàn hon loop tay?
- Dap an ky vong: express intent, less bug, optimized.

16. Có nên dùng `emplace_back` mặc định?
- Dap an ky vong: không luôn; phụ thuộc context construction.

17. `reserve` có tac dùng gì và khi nào vo nghĩa?
- Dap an ky vong: giảm realloc; vo nghĩa nếu không biết size/size nhỏ.

18. Big-O và "hidden constants".
- Dap an ky vong: branch/cache/alloc/coherency.

19. `stable_sort` khi nào cần?
- Dap an ky vong: giữ thứ tự bảng nhau.

20. `vector<bool>` có gì khác thường?
- Dap an ky vong: bit proxy specialization.

## C. Concurrency (12 câu)

21. Data race vs race condition.
- Dap an ky vong: data race => UB; race condition là logic.

22. Acquire-release bảng ví dụ producer/consumer.
- Dap an ky vong: store-release + load-acquire nhìn thấy dữ liệu.

23. Tinh hướng dùng `memory_order_relaxed`.
- Dap an ky vong: counters/statistics độc lập.

24. Spurious wakeup và wait predicate.
- Dap an ky vong: luôn wait trong loop/predicate.

25. Deadlock prevention strategies.
- Dap an ky vong: lock ordering, scoped_lock, timeout.

26. False sharing là gì?
- Dap an ky vong: cũng cache line, writer conflict.

27. Thread pool design cần gì?
- Dap an ky vong: queue, worker lifecycle, backpressure, shutdown.

28. Lock-free có phải luôn nhanh?
- Dap an ky vong: không; complexity cao, benchmark-driven.

29. ABA problem.
- Dap an ky vong: A->B->A làm CAS bi lua.

30. Khi nào dùng `jthread`?
- Dap an ky vong: auto join + cancellation cooperative.

31. Cách test code concurrent.
- Dap an ky vong: stress test, TSAN, deterministic seeds.

32. Nếu cần timeout + cancel task đang cho I/O?
- Dap an ky vong: cancellation token + non-blocking/polling strategy.

## D. System Design C++ (12 câu)

33. Design URL shortener (hoặc ID service) với C++ backend.
- Dap an ky vong: ID generation, storage, cache, scaling.

34. Design in-memory rate limiter.
- Dap an ky vong: token bucket/sliding window + distributed state.

35. Design log ingestion pipeline p99<100ms.
- Dap an ky vong: batching, queue, backpressure, drop policy.

36. Cách giữ ABI ổn định cho library C++?
- Dap an ky vong: pimpl, C API boundary, symbol versioning.

37. Reliable retry policy cho external dependency.
- Dap an ky vong: timeout + exponential backoff + jitter + idempotency.

38. Cache invalidation strategy.
- Dap an ky vong: TTL/event-based/versioned key + stampede protection.

39. Message ordering guarantee trong queue.
- Dap an ky vong: partition key, per-partition ordering.

40. Exactly-once semantics thực tế.
- Dap an ky vong: effectively-once via dedup/idempotency.

41. Multi-tenant service constraints.
- Dap an ky vong: isolation quota, noisy neighbor control.

42. Rollout an toàn cho thay đổi lớn.
- Dap an ky vong: canary, feature flag, rollback fast.

43. Observability baseline cho service mọi.
- Dap an ky vong: golden signals + trace + alert SLO.

44. Postmortem quality checklist.
- Dap an ky vong: root cause, guardrail, owner, due date.

## E. Debugging + Performance (10 câu)

45. Quy trình tối ưu latency.
- Dap an ky vong: measure -> locate hotspot -> change -> verify.

46. Khi nào sử dụng ASan/TSan/UBSan?
- Dap an ky vong: map dùng cho tung loại lỗi.

47. LTO và PGO trong production build.
- Dap an ky vong: trade-off build time vs runtime speed.

48. Vì sao benchmark local nhanh nhưng production chậm?
- Dap an ky vong: data shape, cache, NUMA, I/O, contention.

49. Heap fragmentation xử lý sao?
- Dap an ky vong: pooling, arena, allocation patterns.

50. Cách đọc flame graph.
- Dap an ky vong: width = time ratio, tap trung stack rong.

51. p99 tăng nhưng p50 on định nghĩa là gì?
- Dap an ky vong: tail latency issue, contention, GC/IO bursts.

52. Nhận dien false bottleneck.
- Dap an ky vong: correlation != causation, cần controlled experiment.

53. Debug crash hiếm gap.
- Dap an ky vong: core dump + symbols + sanitizers + bisect.

54. Khi nào rewrite thay vì optimize?
- Dap an ky vong: debt qua lớn, architecture mismatch, rồi rõ rewrite.

## F. Behavioral + Seniority (10 câu)

55. Lan ban quyết định no với 1 để xuat kỹ thuật.
56. Lan ban dan đặt migration không downtime.
57. Lan ban mentor junior và kết quả.
58. Lan ban xử lý disagreement với PM.
59. Lan ban fail và hoc được gì.
60. Cách ban ưu tiên cổng viec khi mọi thu đều gap.
61. Cách ban danh gia effort/risk trước khi commitment.
62. Cách ban giữ chất lượng code trong team nhanh.
63. Cách ban truyen đặt trade-off cho stakeholder.
64. Why you for senior role?

Dap an ky vong behavioral:
- STAR rõ rang
- Có metric trước/sau
- Có bài hoc và preventive action
- Có tac đóng đến team, không chi ca nhận

## Rubric chậm nhanh (0-2 điểm mọi tieu chi)

- Do dùng technical
- Do sau và trade-off
- Clarity và cấu trúc
- Practicality (kinh nghiệm thực tế)
- Senior signal (ownership, risk, leadership)

Tong 10 điểm/câu:
- 8-10: senior strong
- 6-7: pass cần cai thien
- <=5: cần on lai chu để
