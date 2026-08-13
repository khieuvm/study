# Exercise 07 - Profile and Optimize

## De bai
Mot service C++ bi tang p99 tu 80ms len 300ms sau release moi.

## Yeu cau
1. Lap plan triage trong 30 phut dau.
2. Liet ke thu tu uu tien: rollback, profile, metric nao xem truoc.
3. De xuat 3 gia thuyet bottleneck va cach kiem chung.
4. Viet mau postmortem outline.

## Dap an goi y
- Kiem tra deployment diff truoc.
- Xem p99 theo endpoint + dependency latency + CPU saturation.
- Dung flamegraph/perf de xac dinh hotspot.

## Rubric
- Incident handling thuc te (0-4)
- Hypothesis-driven debugging (0-3)
- Prevention action quality (0-3)
