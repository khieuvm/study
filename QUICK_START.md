# ⚡ Quick Start (5 phút)

## Bước 1: Cài dependencies (1 phút)

```bash
cd Study
pip install -r requirements.txt
```

## Bước 2: Chạy Streamlit (ngay lập tức)

**Chỉ muốn đọc đáp án?**
```bash
streamlit run app.py
```

**Muốn trả lời + được Ollama chấm?** (Bỏ qua bước 3, 4 nếu không cần)
```bash
streamlit run app_advanced.py
```

→ Browser mở tự động `http://localhost:8501`

---

## Bước 3: Cài Ollama (nếu muốn tính năng chấm điểm)

### Windows / macOS / Linux
Tải từ: https://ollama.ai/download

Sau khi cài xong:

```bash
# Terminal/PowerShell mới, chạy:
ollama serve
```

---

## Bước 4: Download model (1 lần duy nhất)

**Terminal khác** (giữ Terminal Ollama chạy):

```bash
# Option 1: Mistral (tốt nhất, ~7GB)
ollama pull mistral

# Option 2: Neural Chat (nhanh hơn, ~4GB)
ollama pull neural-chat

# Option 3: Phi (siêu nhanh, ~3GB)
ollama pull phi
```

---

## Xong! 🎉

Mở Streamlit → Chọn "✍️ Trả lời" → Nhập đáp án → Bấm "Nộp" → Ollama chấm điểm

---

## Nếu gặp lỗi

### ❌ "Ollama chưa chạy"
→ Mở terminal mới, chạy `ollama serve`

### ❌ "Không có model nào"
→ Chạy `ollama pull mistral` (cần ~5-10 phút)

### ❌ "Streamlit không mở browser"
→ Truy cập tay: http://localhost:8501

### ❌ "Chấm điểm quá chậm"
→ Dùng model nhẹ: `phi` hoặc `neural-chat`

---

## Các file bạn cần biết

| File | Mục đích |
|------|---------|
| `app.py` | Đơn giản: chỉ show/hide đáp án |
| `app_advanced.py` | Đầy đủ: trả lời + Ollama chấm |
| `01-10-*.md` | 10 chủ đề Q&A (mở bằng text editor) |
| `CLAUDE.md` | Hướng dẫn project |

---

## Tip nhanh

- 📖 Chế độ **Đọc**: ôn nhanh Q&A
- ✍️ Chế độ **Trả lời**: luyện tập thực tế

Chúc bạn ôn tập vui vẻ! 🚀
