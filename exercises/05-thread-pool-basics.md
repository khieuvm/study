# Exercise 05 - Thread Pool Basics

## De bai
Xay dung thread pool toi thieu:
- N workers
- Queue task
- Shutdown an toan

## Yeu cau
1. Dung `std::mutex` + `std::condition_variable`.
2. Khong deadlock, khong data race.
3. Co co che stop.
4. Viet 3 test: throughput, shutdown khi queue con task, stress race.

## Dap an goi y
- Worker loop: wait predicate `stop || !queue.empty()`.
- Khi stop va queue rong thi thoat.
- Destructor set stop, notify_all, join.

## Rubric
- Correctness concurrent (0-5)
- Shutdown semantics (0-3)
- Test quality (0-2)
