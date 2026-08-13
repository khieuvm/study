# Bilingual Q&A Template (VI/EN)

Su dung template nay de chuyen cac file hoc tap sang dang song ngu phuc vu phong van tieng Anh.

---

## Quy uoc chung

- Moi muc dung format: `### Q<n>. <question>`
- Moi cau tra loi bat dau bang `**A:**`
- Trong phan tra loi, uu tien trinh bay:
  - `EN: ...`
  - `VI: ...`
- Neu co code, giu code bang English comment ngan gon.
- Neu co trade-off, nen theo khung: performance, safety, complexity, portability.

---

## Skeleton

```md
### Q<n>. <question in Vietnamese or neutral style>

**A:**
- EN: <short direct answer in interview style>
- VI: <short equivalent Vietnamese answer>

```cpp
// minimal example
```

Follow-up (EN): <one likely interviewer follow-up>
```

---

## Mau day du

### Q1. Su khac nhau giua stack va heap?

**A:**
- EN: Stack is automatically managed memory with very fast allocation, while heap is dynamically managed memory with flexible lifetime but higher overhead.
- VI: Stack la vung nho duoc quan ly tu dong, cap phat nhanh; heap la vung nho cap phat dong, linh hoat vong doi nhung chi phi cao hon.

```cpp
int x = 42;                // stack
int* p = new int(42);      // heap
delete p;
```

Follow-up (EN): When would you prefer arena allocation over regular heap allocation?

---

## Checklist truoc khi commit

- Kiem tra moi Q co `**A:**`
- Kiem tra co ca `EN` va `VI`
- Kiem tra code block compile logic (neu la code C/C++)
- Kiem tra thuat ngu ky thuat su dung nhat quan
