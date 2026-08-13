# Exercise 06 - Design Rate Limiter

## De bai
Thiet ke rate limiter cho API:
- 100 req/phut/user
- p99 them do tre < 2ms
- Co the scale ngang

## Yeu cau
1. Chon algorithm (token bucket/sliding window) + ly do.
2. De xuat data model in-memory va distributed.
3. Xu ly clock skew, retry, fail-open/fail-closed.
4. Monitoring va alert can co.

## Dap an goi y
- Token bucket de don gian + hieu nang.
- Distributed state co the dung Redis + key theo user.
- Co local cache de giam RTT neu can.

## Rubric
- Dung yeu cau phi chuc nang (0-4)
- Trade-off ro rang (0-3)
- Failure mode handling (0-3)
