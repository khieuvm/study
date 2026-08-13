# 04 - STL, Algorithm, Complexity

## 1) Container selection

### Q1. `vector` vs `list`?
A: `vector` thường nhanh hơn thực tế nhỏ cache locality. `list` chỉ có lỗi khi cần splice/insert erase o giữa với iterator đã có.

### Q2. `map` vs `unordered_map`?
A:
- `map`: O(log n), có thứ tự, iter stable hon theo key order
- `unordered_map`: trung bình O(1), không có thứ tự, phụ thuộc hash/rehash

### Q3. `deque` dùng khi nào?
A: Khi cần push/pop o ca đầu và cũối nhiều, và random access van cần.

## 2) Iterator invalidation

### Q4. `vector::push_back` có invalidation không?
A: Có thể có nếu reallocate; tất cả iterator/reference/pointer vào phần tử có thể invalid.

### Q5. `list` iterator có ổn định hon không?
A: Thường ổn định khi insert/erase node khác, nhưng iterator tới node bi erase sẽ invalid.

## 3) Algorithm

### Q6. Vì sao ưu tiên algorithm STL hon loop tay?
A: Code rõ y do, it bug, tối ưu tốt, để compose.

### Q7. `remove` trong erase-remove idiom làm gì?
A: `remove` chi partition và trả về iterator mọi, không xóa size container. Cần `erase` tiếp.

### Q8. `stable_sort` vs `sort`?
A: `stable_sort` giữ thứ tự phần tử bảng nhau, đổi lai ton bộ nhớ và có thể chậm hon.

### Q9. Big-O có đủ để dự đoán toc do không?
A: Không đủ. Cần tinh đến constant factor, cache miss, branch misprediction, allocator cost.

## 4) Allocator và memory

### Q10. Polymorphic allocator (`pmr`) lỗi ich?
A: Tách chính sach cấp phát khoi cấu trúc dữ liệu, tối ưu theo workload (arena/monotonic).

### Q11. Small string optimization (SSO) là gì?
A: `std::string` lưu chuoi ngan trong object không cấp phát heap.

## 5) Các câu hỏi danh gia senior

### Q12. Tại sao `vector<bool>` gây tránh cai?
A: Specialization bit-packed, không true reference/pointer như vector thường, han che behavior.

### Q13. Khi nào reserve cho `vector`?
A: Khi uoc luồng được số phần tử để giảm reallocation.

### Q14. Có nên micro-opt algorithm sớm?
A: Không. Do profile trước, optimize điểm nong sau.

### Q15. Dùng `emplace_back` luôn có tốt hơn `push_back`?
A: Không luôn. `emplace_back` huu ich khi tạo trực tiếp object; với object đã có sẵn, khác biết có thể không đang kế.

## 6) Practical snippets (để từ luyen)

```cpp
std::vector<int> v;
v.reserve(1000); // giam kha nang reallocation
for (int i = 0; i < 1000; ++i) v.push_back(i);

v.erase(std::remove_if(v.begin(), v.end(),
                       [](int x){ return x % 2 == 0; }),
        v.end());
```
