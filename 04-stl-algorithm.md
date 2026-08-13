# 04 - STL, Algorithm, Complexity

## 1) Container selection

### Q1. `vector` vs `list`?
A: `vector` thuong nhanh hon thuc te nho cache locality. `list` chi co loi khi can splice/insert erase o giua voi iterator da co.

### Q2. `map` vs `unordered_map`?
A:
- `map`: O(log n), co thu tu, iter stable hon theo key order
- `unordered_map`: trung binh O(1), khong co thu tu, phu thuoc hash/rehash

### Q3. `deque` dung khi nao?
A: Khi can push/pop o ca dau va cuoi nhieu, va random access van can.

## 2) Iterator invalidation

### Q4. `vector::push_back` co invalidation khong?
A: Co the co neu reallocate; tat ca iterator/reference/pointer vao phan tu co the invalid.

### Q5. `list` iterator co on dinh hon khong?
A: Thuong on dinh khi insert/erase node khac, nhung iterator toi node bi erase se invalid.

## 3) Algorithm

### Q6. Vi sao uu tien algorithm STL hon loop tay?
A: Code ro y do, it bug, toi uu tot, de compose.

### Q7. `remove` trong erase-remove idiom lam gi?
A: `remove` chi partition va tra ve iterator moi, khong xoa size container. Can `erase` tiep.

### Q8. `stable_sort` vs `sort`?
A: `stable_sort` giu thu tu phan tu bang nhau, doi lai ton bo nho va co the cham hon.

### Q9. Big-O co du de du doan toc do khong?
A: Khong du. Can tinh den constant factor, cache miss, branch misprediction, allocator cost.

## 4) Allocator va memory

### Q10. Polymorphic allocator (`pmr`) loi ich?
A: Tach chinh sach cap phat khoi cau truc du lieu, toi uu theo workload (arena/monotonic).

### Q11. Small string optimization (SSO) la gi?
A: `std::string` luu chuoi ngan trong object khong cap phat heap.

## 5) Cac cau hoi danh gia senior

### Q12. Tai sao `vector<bool>` gay tranh cai?
A: Specialization bit-packed, khong true reference/pointer nhu vector thuong, han che behavior.

### Q13. Khi nao reserve cho `vector`?
A: Khi uoc luong duoc so phan tu de giam reallocation.

### Q14. Co nen micro-opt algorithm som?
A: Khong. Do profile truoc, optimize diem nong sau.

### Q15. Dung `emplace_back` luon co tot hon `push_back`?
A: Khong luon. `emplace_back` huu ich khi tao truc tiep object; voi object da co san, khac biet co the khong dang ke.

## 6) Practical snippets (de tu luyen)

```cpp
std::vector<int> v;
v.reserve(1000); // giam kha nang reallocation
for (int i = 0; i < 1000; ++i) v.push_back(i);

v.erase(std::remove_if(v.begin(), v.end(),
                       [](int x){ return x % 2 == 0; }),
        v.end());
```
