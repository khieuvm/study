import re
from pathlib import Path

import streamlit as st

APP_DIR = Path(__file__).parent
EXTRA_DIR = APP_DIR / "19-python-debugging"
EXCLUDE_FILES = {"CLAUDE.md", "README.md", "README_APP.md", "QUICK_START.md", "BILINGUAL_QA_TEMPLATE.md"}

GROUP_MAIN = "C/C++ Core (01-18)"
GROUP_EXTRA = "Python & Debugging"
PART_LABELS = {
    "part1-python-core": "Part 1 | Python Core",
    "part2-python-debugging": "Part 2 | Python Debugging",
    "part3-cpp-gdb-debugging": "Part 3 | C/C++ Debugging (gdb)",
    "part4-thuc-chien": "Part 4 | Bài tập thực chiến",
}


@st.cache_data
def parse_qa(text):
    """Tach markdown thanh cac cap Q&A: heading '### Q<n>.' va dap an '**A:**' (hoac 'A:')."""
    questions = []
    for block in re.split(r"^### Q\d+\.", text, flags=re.MULTILINE)[1:]:
        head, _, body = block.strip().partition("\n")
        match = re.search(r"\*\*A:\*\*(.*?)(?=\n---|\n### Q|\Z)", body, re.DOTALL)
        if not match:
            match = re.search(r"^A:(.*?)(?=\n---|\n### Q|\Z)", body, re.DOTALL | re.MULTILINE)
        if match and match.group(1).strip():
            questions.append({"question": head.strip(), "answer": match.group(1).strip()})
    return questions


def list_files(directory, numbered_only):
    if not directory.exists():
        return []
    return sorted(
        f for f in directory.glob("*.md")
        if f.name not in EXCLUDE_FILES and (f.name[0].isdigit() or not numbered_only)
    )


st.set_page_config(page_title="Interview Prep", layout="wide")
st.title("Interview Prep")

main_files = list_files(APP_DIR, numbered_only=True)
extra_files = list_files(EXTRA_DIR, numbered_only=False)

if not main_files and not extra_files:
    st.error("Không tìm thấy file markdown nào")
    st.stop()

groups = [GROUP_MAIN] + ([GROUP_EXTRA] if extra_files else [])
group = st.sidebar.radio("Nhóm nội dung:", groups)
files = extra_files if group == GROUP_EXTRA else main_files

selected = st.sidebar.selectbox(
    "Chọn chủ đề:",
    options=[f.stem for f in files],
    format_func=lambda stem: PART_LABELS.get(stem, stem.replace("-", " | ", 1)),
)

file_path = next(f for f in files if f.stem == selected)
questions = parse_qa(file_path.read_text(encoding="utf-8"))

if not questions:
    st.warning(f"File `{file_path.name}` không có Q&A format")
    st.stop()

keyword = st.sidebar.text_input("Tìm trong câu hỏi:", placeholder="ví dụ: pointer, gdb")
if keyword:
    questions = [q for q in questions if keyword.lower() in q["question"].lower()]

expand_all = st.sidebar.checkbox("Mở sẵn đáp án")

st.caption(f"{file_path.name} — {len(questions)} câu hỏi")
st.markdown("---")

for idx, qa in enumerate(questions, 1):
    st.markdown(f"**Q{idx}. {qa['question']}**")
    with st.expander("Xem đáp án", expanded=expand_all):
        st.markdown(qa["answer"])
    st.markdown("")
