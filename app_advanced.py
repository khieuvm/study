import streamlit as st
import re
import json
import requests
from pathlib import Path
from datetime import datetime

st.set_page_config(page_title="C/C++ Interview Prep", layout="wide", initial_sidebar_state="expanded")

APP_DIR = Path(__file__).parent
PROGRESS_FILE = APP_DIR / ".progress.json"
EXCLUDE_FILES = {"CLAUDE.md", "README.md", "README_APP.md", "QUICK_START.md"}
OLLAMA_URL = "http://localhost:11434"
DEFAULT_MODEL = "qwen2.5:14b"


# --- Utility functions ---

@st.cache_data
def parse_qa(text):
    """Parse markdown content into Q&A format."""
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


def load_progress():
    if PROGRESS_FILE.exists():
        try:
            data = json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
            data.setdefault("done", {})
            data.setdefault("chats", {})
            data.setdefault("notes", {})
            return data
        except (json.JSONDecodeError, IOError):
            pass
    return {"scores": {}, "answers": {}, "submitted": {}, "done": {}, "chats": {}, "notes": {}, "last_updated": None}


def save_progress(progress):
    progress["last_updated"] = datetime.now().isoformat()
    PROGRESS_FILE.write_text(json.dumps(progress, ensure_ascii=False, indent=2), encoding="utf-8")


def call_ollama(prompt, model=DEFAULT_MODEL, timeout=30):
    """Generic Ollama call."""
    try:
        resp = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=timeout
        )
        if resp.status_code == 200:
            return resp.json().get("response", "")
    except Exception:
        pass
    return None


def call_ollama_grader(question, reference_answer, user_answer):
    """Grade an answer, return {score, feedback}."""
    prompt = f"""You are an expert C/C++ interviewer evaluating a candidate's answer.

Question: {question}

Reference Answer: {reference_answer}

Student's Answer: {user_answer}

Evaluate based on: correctness, completeness, code examples, clarity.
Respond ONLY with valid JSON:
{{"score": <0-10>, "feedback": "<brief feedback in Vietnamese>"}}"""

    raw = call_ollama(prompt, timeout=60)
    if raw:
        try:
            m = re.search(r'\{.*?\}', raw, re.DOTALL)
            if m:
                parsed = json.loads(m.group())
                parsed["score"] = max(0, min(10, int(parsed.get("score", 0))))
                return parsed
        except (json.JSONDecodeError, ValueError):
            pass
    return {"score": 0, "feedback": "Khong the cham diem"}


def call_ollama_followup(question, reference_answer, chat_history, user_msg):
    """Follow-up conversation as interviewer."""
    history_text = ""
    for msg in chat_history[-6:]:
        role = "Candidate" if msg["role"] == "user" else "Interviewer"
        history_text += f"{role}: {msg['content']}\n"

    prompt = f"""You are a senior C/C++ interviewer conducting a technical interview.
The original question was: {question}
Reference answer: {reference_answer}

Conversation so far:
{history_text}
Candidate: {user_msg}

As the interviewer, ask a follow-up question OR give feedback on their answer.
Keep it concise (2-4 sentences). Respond in Vietnamese.
If the candidate answered well, go deeper or ask about edge cases.
If they answered poorly, give a hint and ask again."""

    return call_ollama(prompt, timeout=30) or "Ollama khong phan hoi. Kiem tra lai connection."


@st.cache_data(ttl=30)
def check_ollama():
    try:
        resp = requests.get(f"{OLLAMA_URL}/api/tags", timeout=2)
        if resp.status_code == 200:
            models = [m["name"] for m in resp.json().get("models", [])]
            return models if models else []
    except Exception:
        pass
    return []


# --- Load progress ---

if "progress" not in st.session_state:
    st.session_state.progress = load_progress()

progress = st.session_state.progress


# --- UI Header ---

st.title("C/C++ Senior Interview Prep")
st.markdown("---")

md_files = sorted([
    f for f in APP_DIR.glob("*.md")
    if f.name not in EXCLUDE_FILES and f.name[0].isdigit()
])

if not md_files:
    st.error("Khong tim thay file markdown")
    st.stop()

col_file, col_mode = st.columns([3, 1])
with col_file:
    selected_file = st.selectbox(
        "Chon chu de:",
        options=[f.stem for f in md_files],
        format_func=lambda x: x.replace("-", " | ", 1)
    )
with col_mode:
    mode = st.radio("Che do:", ["Doc", "Tra loi"], horizontal=True)

# Load & parse
file_path = APP_DIR / f"{selected_file}.md"
content = file_path.read_text(encoding="utf-8")
questions = parse_qa(content)

if not questions:
    st.warning(f"File `{selected_file}.md` khong co Q&A format")
    st.stop()


# --- Stats (placeholder - filled after checkboxes update) ---

stats_placeholder = st.container()
st.markdown("---")


# --- Read Mode ---

if mode == "Doc":
    for idx, qa in enumerate(questions, 1):
        key = f"{selected_file}_q{idx}"

        is_done = st.checkbox(
            f"Q{idx}. {qa['question']}",
            value=progress["done"].get(key, False),
            key=f"chk_{key}",
        )
        if is_done != progress["done"].get(key, False):
            progress["done"][key] = is_done
            save_progress(progress)

        with st.expander("Xem dap an", expanded=False):
            st.markdown(qa["answer"])

        # Note
        saved_note = progress["notes"].get(key, "")
        note = st.text_input(
            "Ghi chu:",
            value=saved_note,
            key=f"note_{key}",
            placeholder="Ghi chu cua ban..."
        )
        if note != saved_note:
            progress["notes"][key] = note
            save_progress(progress)

        if progress["scores"].get(key):
            st.caption(f"Diem: {progress['scores'][key]}/10")

        st.markdown("")


# --- Answer Mode ---

else:
    ollama_models = check_ollama()
    ollama_available = len(ollama_models) > 0
    if ollama_available:
        st.success(f"Ollama: {', '.join(ollama_models[:3])}")
    else:
        st.info("Ollama chua chay. `ollama serve` + `ollama pull qwen2.5:14b`")

    for idx, qa in enumerate(questions, 1):
        key = f"{selected_file}_q{idx}"

        is_done = st.checkbox(
            f"Q{idx}. {qa['question']}",
            value=progress["done"].get(key, False),
            key=f"chk2_{key}",
        )
        if is_done != progress["done"].get(key, False):
            progress["done"][key] = is_done
            save_progress(progress)

        # Reference answer
        with st.expander("Xem goi y"):
            st.markdown(qa["answer"])

        # Note
        saved_note = progress["notes"].get(key, "")
        note = st.text_input(
            "Ghi chu:",
            value=saved_note,
            key=f"note2_{key}",
            placeholder="Ghi chu cua ban..."
        )
        if note != saved_note:
            progress["notes"][key] = note
            save_progress(progress)

        # User answer
        saved_answer = progress["answers"].get(key, "")
        user_answer = st.text_area(
            f"Tra loi cau {idx}:",
            value=saved_answer,
            height=100,
            key=f"ta_{key}"
        )
        if user_answer != saved_answer:
            progress["answers"][key] = user_answer[:10000]
            save_progress(progress)

        # Submit + score
        col_a, col_b = st.columns([3, 1])
        with col_a:
            if st.button(f"Nop cau {idx}", key=f"btn_{key}"):
                if not user_answer.strip():
                    st.error("Nhap dap an truoc")
                elif not ollama_available:
                    progress["submitted"][key] = True
                    progress["scores"][key] = "?"
                    save_progress(progress)
                    st.warning("Luu roi. Chua co Ollama nen chua cham.")
                else:
                    with st.spinner("Dang cham diem..."):
                        result = call_ollama_grader(qa["question"], qa["answer"], user_answer)
                        score = result.get("score", 0)
                        feedback = result.get("feedback", "")
                        progress["scores"][key] = score
                        progress["submitted"][key] = True
                        progress["answers"][key] = user_answer[:10000]
                        save_progress(progress)
                        if score >= 7:
                            st.success(f"{score}/10 - {feedback}")
                        elif score >= 5:
                            st.info(f"{score}/10 - {feedback}")
                        else:
                            st.error(f"{score}/10 - {feedback}")

        with col_b:
            s = progress["scores"].get(key)
            if isinstance(s, (int, float)):
                color = "green" if s >= 7 else "orange" if s >= 5 else "red"
                st.markdown(f":{color}[{s}/10]")

        # --- Follow-up chat ---
        if ollama_available and progress["submitted"].get(key):
            with st.expander(f"Follow-up (cau {idx})", expanded=False):
                chat_key = f"chat_{key}"
                if chat_key not in progress["chats"]:
                    progress["chats"][chat_key] = []

                chat_history = progress["chats"][chat_key]

                # Display chat history
                for msg in chat_history:
                    if msg["role"] == "user":
                        st.chat_message("user").write(msg["content"])
                    else:
                        st.chat_message("assistant").write(msg["content"])

                # Input for follow-up
                followup_msg = st.text_input(
                    "Hoi them / tra loi follow-up:",
                    key=f"followup_{key}",
                    placeholder="VD: Tai sao khong dung mutex thay cho atomic?"
                )

                if st.button("Gui", key=f"send_{key}") and followup_msg.strip():
                    chat_history.append({"role": "user", "content": followup_msg})

                    with st.spinner("Interviewer dang suy nghi..."):
                        reply = call_ollama_followup(
                            qa["question"], qa["answer"],
                            chat_history, followup_msg
                        )
                        chat_history.append({"role": "assistant", "content": reply})
                        progress["chats"][chat_key] = chat_history
                        save_progress(progress)
                        st.rerun()

        st.markdown("---")


# --- Fill stats (after checkboxes updated progress) ---

prefix = selected_file + "_q"
file_done = sum(1 for k, v in progress["done"].items() if k.startswith(prefix) and v)
file_scores = {k: v for k, v in progress["scores"].items() if k.startswith(prefix)}
avg_score = (sum(file_scores.values()) / len(file_scores)) if file_scores else 0

with stats_placeholder:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Tong cau", len(questions))
    col2.metric("Done", f"{file_done}/{len(questions)}")
    col3.metric("Diem TB", f"{avg_score:.1f}/10" if file_scores else "-")
    col4.metric("Lan cuoi", progress["last_updated"][:10] if progress["last_updated"] else "-")
    if len(questions) > 0:
        st.progress(file_done / len(questions))


# --- Sidebar ---

st.sidebar.markdown("### Tien do:")
total_done = sum(1 for v in progress["done"].values() if v)
total_questions = sum(
    len(parse_qa((APP_DIR / f"{f.stem}.md").read_text(encoding="utf-8")))
    for f in md_files
)
st.sidebar.progress(total_done / total_questions if total_questions else 0)
st.sidebar.caption(f"{total_done}/{total_questions} cau done")

all_scores = [v for v in progress["scores"].values() if isinstance(v, (int, float))]
if all_scores:
    st.sidebar.metric("Diem TB", f"{sum(all_scores)/len(all_scores):.1f}/10")

st.sidebar.markdown("---")
st.sidebar.markdown("### Tung file:")
for f in md_files:
    stem = f.stem
    p = stem + "_q"
    done_cnt = sum(1 for k, v in progress["done"].items() if k.startswith(p) and v)
    total_cnt = len(parse_qa((APP_DIR / f"{stem}.md").read_text(encoding="utf-8")))
    if total_cnt > 0:
        pct = int(done_cnt / total_cnt * 100)
        bar = "█" * (pct // 10) + "░" * (10 - pct // 10)
        st.sidebar.caption(f"`{bar}` {stem.split('-')[-1]}: {done_cnt}/{total_cnt}")

st.sidebar.markdown("---")
confirm_reset = st.sidebar.checkbox("Xac nhan xoa tien do")
if st.sidebar.button("Xoa tien do (reset)", disabled=not confirm_reset):
    st.session_state.progress = {"scores": {}, "answers": {}, "submitted": {}, "done": {}, "chats": {}, "notes": {}, "last_updated": None}
    save_progress(st.session_state.progress)
    st.rerun()
