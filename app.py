import streamlit as st
import re
from pathlib import Path

st.set_page_config(page_title="C/C++ Interview Prep", layout="wide")

EXCLUDE_FILES = {"CLAUDE.md", "README.md", "README_APP.md", "QUICK_START.md"}


def parse_qa(text):
    """Parse markdown content into Q&A format. Handles both **A:** and A: formats."""
    qa_blocks = re.split(r'^### Q\d+\.', text, flags=re.MULTILINE)[1:]
    questions = []
    for block in qa_blocks:
        lines = block.strip().split('\n', 1)
        if len(lines) < 2:
            continue
        q_text = lines[0].strip()
        a_text = lines[1].strip()
        a_match = re.search(r'\*\*A:\*\*(.*?)(?=\n---|\n### Q|\Z)', a_text, re.DOTALL)
        if not a_match:
            a_match = re.search(r'^A:(.*?)(?=\n---|\n### Q|\Z)', a_text, re.DOTALL | re.MULTILINE)
        if a_match:
            a_content = a_match.group(1).strip()
            if a_content:
                questions.append({"question": q_text, "answer": a_content})
    return questions


st.title("C/C++ Senior Interview Prep")
st.markdown("---")

# File selection
APP_DIR = Path(__file__).parent
md_files = sorted([
    f for f in APP_DIR.glob("*.md")
    if f.name not in EXCLUDE_FILES and f.name[0].isdigit()
])

if not md_files:
    st.error("Khong tim thay file markdown nao")
    st.stop()

selected_file = st.sidebar.selectbox(
    "Chon chu de:",
    options=[f.stem for f in md_files],
    format_func=lambda x: x.replace("-", " | ", 1)
)

# Load & parse
file_path = APP_DIR / f"{selected_file}.md"
content = file_path.read_text(encoding="utf-8")
questions = parse_qa(content)

if not questions:
    st.warning(f"File `{selected_file}.md` khong co Q&A format.")
    st.stop()

# Stats
st.metric("Tong cau hoi", len(questions))
st.markdown("---")

# Display Q&A
for idx, qa in enumerate(questions, 1):
    st.markdown(f"**Q{idx}. {qa['question']}**")
    with st.expander("Xem dap an", expanded=False):
        st.markdown(qa['answer'])
    st.markdown("")
