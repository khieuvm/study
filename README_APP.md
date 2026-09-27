# He thong hoc tap - Interview Prep App

Streamlit app chi-doc de on Q&A tu cac file markdown trong repo.

## Cai dat & chay

```bash
pip install -r requirements.txt
streamlit run app.py
```

Browser mo o `http://localhost:8501`.

## Tinh nang

- Chon **Nhom noi dung**: `C/C++ Core (01-18)` hoac `Python & Debugging` (4 part).
- Chon chu de trong nhom, xem so cau hoi cua file.
- Loc cau hoi theo tu khoa.
- Xem/an dap an tung cau, hoac mo san toan bo.

## Cau truc

```
Study/
|- app.py                      # Streamlit app (read-only)
|- requirements.txt
|- 01-c-core.md ... 18-*.md    # Chu de C/C++ core
|- 19-python-debugging/        # Python & debugging (part 1-4)
|- exercises/                  # Bai tap tu luyen
|- CLAUDE.md                   # Huong dan project
```

## Them chu de moi

- File `.md` dat o thu muc goc phai bat dau bang so (vd `20-...md`), hoac dat trong `19-python-debugging/`.
- Format bat buoc de parser nhan dien:

```markdown
### Q1. Cau hoi o day?

**A:**

Noi dung dap an.

---
```

- Dung `---` de ngan cach giua cac cau; khong dung `---` ben trong phan dap an.
