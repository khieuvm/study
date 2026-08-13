# Exercise 04 - Container Trade-off

## De bai
Ban co workload:
- 70% doc tuan tu
- 20% append
- 10% xoa theo dieu kien
- So phan tu trung binh 200k

## Yeu cau
1. Chon container chinh (`vector`, `deque`, `list`, ...), giai thich.
2. Viet pseudo-code xoa theo dieu kien toi uu.
3. De xuat cach benchmark de xac nhan quyet dinh.

## Dap an goi y
- Thuong bat dau voi `vector` + erase-remove.
- `reserve` neu biet truoc kich thuoc.
- Benchmark voi data distribution thuc te.

## Rubric
- Chon container co ly do (0-4)
- Dung complexity + cache locality (0-3)
- Benchmark plan thuyet phuc (0-3)
