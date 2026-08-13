# 📚 Hệ thống Học tập C/C++ Interview Prep

Interactive Streamlit app để ôn tập và luyện phỏng vấn C/C++ Senior.

## ✨ Tính năng

### Phiên bản cơ bản (`app.py`)
- 📖 **Chế độ Đọc**: Show/Hide đáp án từng câu
- 📊 Thống kê tiến độ
- 🎯 10 chủ đề từ cơ bản đến nâng cao

### Phiên bản nâng cao (`app_advanced.py`)
- 📖 **Chế độ Đọc**: Xem đáp án tham khảo
- ✍️ **Chế độ Trả lời**: Nhập câu trả lời của bạn
- 🤖 **Chấm điểm tự động**: Dùng Ollama (LLM) chấm
- ⭐ **Feedback tức thì**: Nhận phản hồi từ AI
- 📊 **Thống kê điểm**: Theo dõi tiến độ

## 🚀 Cài đặt & Chạy

### 1. Cài đặt Streamlit

```bash
pip install -r requirements.txt
```

### 2. Cài đặt Ollama (để dùng tính năng chấm điểm)

**Bước 1: Download & cài Ollama**
- Truy cập: https://ollama.ai
- Download cho hệ điều hành của bạn
- Cài đặt bình thường

**Bước 2: Download model (chạy 1 lần)**

```bash
# Terminal/PowerShell mới
ollama pull mistral
# hoặc model khác (gọn/nhanh hơn):
ollama pull neural-chat
```

**Bước 3: Khởi chạy Ollama**

```bash
ollama serve
# Ollama sẽ chạy ở http://localhost:11434
```

### 3. Chạy Streamlit

**Chế độ cơ bản (chỉ đọc):**
```bash
streamlit run app.py
```

**Chế độ nâng cao (đọc + trả lời + chấm điểm Ollama):**
```bash
streamlit run app_advanced.py
```

Streamlit sẽ mở browser tự động ở `http://localhost:8501`

## 📖 Hướng dẫn sử dụng

### Chế độ Đọc 📖
1. Chọn chủ đề ở sidebar
2. Đọc câu hỏi
3. Bấm "👀 Xem đáp án" để xem đáp án
4. Lặp lại với câu tiếp theo

### Chế độ Trả lời (Advanced) ✍️
1. Chọn chế độ "✍️ Trả lời"
2. Bấm "📖 Xem gợi ý đáp án" để tham khảo (không bắt buộc)
3. Nhập câu trả lời của bạn vào text area
4. Bấm "📤 Nộp câu X"
5. Chờ Ollama chấm điểm (~5-10 giây)
6. Xem điểm & feedback

## 📚 Cấu trúc tài liệu

10 file markdown với các chủ đề:

```
01-c-core.md              ← C cơ bản: data types, pointers, UB
02-cpp-oop.md             ← OOP: class, virtual, RAII
03-cpp-memory.md          ← Memory: stack, heap, smart pointers
04-cpp-templates.md       ← Templates: SFINAE, concepts
05-cpp-stl.md             ← STL: containers, algorithms
06-cpp-modern.md          ← C++11/17/20: move, lambda, async
07-concurrency.md         ← Threading: mutex, atomic, lock-free
08-design-patterns.md     ← Design patterns: Singleton, Factory, ...
09-optimization.md        ← Performance: cache, SIMD, profiling
10-systems.md             ← Systems: process, IPC, networking, ELF
```

Mỗi file có **10-20 Q&A** chi tiết với:
- Giải thích rõ ràng
- Code example thực tế
- Best practice
- Flash card ôn nhanh

## 💡 Tips

### Tối ưu hiệu suất Ollama

Nếu model chạy **chậm**, chọn model nhẹ hơn:

```bash
ollama pull neural-chat    # ~4GB, nhanh hơn
ollama pull orca-mini      # ~1.5GB, tốc độ tốt
ollama pull phi            # ~3GB, rất nhanh
```

Rồi dùng trong Streamlit bằng cách sửa `app_advanced.py`:

```python
# Tìm dòng: model="mistral"
# Đổi thành:
model="neural-chat"  # hoặc model khác
```

### Cải thiện điểm

1. **Ôn cơ bản trước** (dùng chế độ Đọc)
2. **Tự trả lời trước** khi xem gợi ý
3. **Đọc feedback chi tiết** từ Ollama
4. **Hỏi lại câu giống** lần tiếp theo

### Lưu tiến độ (future)

Hiện tại tiến độ chỉ lưu trong session. Sắp sẽ thêm:
- Lưu vào database
- Export báo cáo
- So sánh tiến độ qua thời gian

## 🐛 Troubleshooting

### "Ollama chưa chạy"
```bash
# Terminal mới, chạy:
ollama serve
```

### "Ollama chưa có model"
```bash
# Terminal mới, chạy:
ollama pull mistral
```

### Streamlit không mở browser
Truy cập tay: `http://localhost:8501`

### Ollama chạy chậm
- Dùng model nhẹ: `neural-chat`, `phi`
- Giảm độ dài câu trả lời
- Tăng RAM của máy

## 📊 Cấu trúc Code

```
Study/
├── app.py                 # Streamlit app cơ bản
├── app_advanced.py        # Streamlit app nâng cao (+ Ollama)
├── requirements.txt       # Dependencies
├── 01-c-core.md          # 20 Q&A
├── 02-cpp-oop.md         # 16 Q&A
├── ... (01-10)
├── CLAUDE.md             # Project instructions
└── README.md             # File này
```

## 🎓 Mục tiêu

Chuẩn bị cho phỏng vấn **Senior C/C++ Engineer** bằng cách:
1. Nắm vững kiến thức cơ bản
2. Hiểu sâu các advanced concept
3. Luyện trả lời câu hỏi thực tế
4. Nhận feedback từ AI

## 🔄 Roadmap

- [x] Tạo 10 file Q&A chi tiết
- [x] App Streamlit cơ bản (show/hide)
- [x] App nâng cao (trả lời + Ollama)
- [ ] Lưu tiến độ vào database
- [ ] Export báo cáo PDF
- [ ] Thống kê chi tiết (thời gian, điểm, ...)
- [ ] Video giải thích
- [ ] Tạo mock interview

## 📝 License

Personal Study Material - For learning purposes only

---

**Happy Learning! 🚀**

Nếu có câu hỏi, hãy check lại các file `.md` hoặc modify `app_advanced.py` theo ý bạn.
