"""
app.py — DSA Mentor AI ✦ Premium Streamlit UI
================================================
A beautiful, dark-themed RAG chatbot for Data Structures & Algorithms.
"""

import streamlit as st
import os
import random
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# ╔══════════════════════════════════════════════════════════════════╗
# ║  1. PAGE CONFIG                                                 ║
# ╚══════════════════════════════════════════════════════════════════╝
st.set_page_config(
    page_title="DSA Mentor AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ╔══════════════════════════════════════════════════════════════════╗
# ║  2. CUSTOM CSS — Dark Theme + Glassmorphism + Animations        ║
# ╚══════════════════════════════════════════════════════════════════╝
def apply_custom_css():
    """Inject all custom styles into the Streamlit app."""
    st.markdown("""
    <style>
    /* ── Google Fonts ─────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* ── Root Variables ───────────────────────────────────── */
    :root {
        --bg-primary:    #0a0e17;
        --bg-secondary:  #111827;
        --bg-card:       #1a1f2e;
        --bg-glass:      rgba(17, 24, 39, 0.7);
        --border-color:  rgba(59, 130, 246, 0.15);
        --accent-blue:   #3B82F6;
        --accent-cyan:   #06B6D4;
        --accent-green:  #22C55E;
        --accent-purple: #8B5CF6;
        --accent-orange: #F59E0B;
        --accent-pink:   #EC4899;
        --text-primary:  #E2E8F0;
        --text-secondary:#94A3B8;
        --text-muted:    #64748B;
        --glow-blue:     0 0 20px rgba(59, 130, 246, 0.3);
    }

    /* ── Global Reset ─────────────────────────────────────── */
    .stApp {
        background: var(--bg-primary) !important;
        font-family: 'Inter', sans-serif !important;
        color: var(--text-primary) !important;
    }

    /* ── Sidebar ──────────────────────────────────────────── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1321 0%, #111827 100%) !important;
        border-right: 1px solid var(--border-color) !important;
    }
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown li,
    section[data-testid="stSidebar"] label {
        color: var(--text-secondary) !important;
        font-family: 'Inter', sans-serif !important;
    }
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stRadio label {
        color: var(--text-secondary) !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* ── Headings ─────────────────────────────────────────── */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif !important;
        color: var(--text-primary) !important;
    }

    /* ── Chat Messages ────────────────────────────────────── */
    .stChatMessage {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 16px !important;
        padding: 1.2rem !important;
        margin-bottom: 1rem !important;
        backdrop-filter: blur(12px) !important;
        animation: fadeSlideIn 0.4s ease-out !important;
    }
    @keyframes fadeSlideIn {
        from { opacity: 0; transform: translateY(12px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    .stChatMessage p, .stChatMessage li, .stChatMessage span {
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif !important;
        line-height: 1.7 !important;
    }
    .stChatMessage strong {
        color: var(--accent-cyan) !important;
    }

    /* ── Code Blocks ──────────────────────────────────────── */
    .stChatMessage pre, .stChatMessage code,
    pre, code, .stCode {
        font-family: 'JetBrains Mono', 'Fira Code', monospace !important;
    }
    .stChatMessage pre {
        background: #0d1117 !important;
        border: 1px solid rgba(59, 130, 246, 0.2) !important;
        border-radius: 12px !important;
        padding: 1rem !important;
    }

    /* ── Chat Input ───────────────────────────────────────── */
    .stChatInput {
        border-color: var(--border-color) !important;
    }
    .stChatInput > div {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 14px !important;
    }
    .stChatInput textarea {
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif !important;
        caret-color: var(--accent-blue) !important;
    }

    /* ── Custom Buttons (Quick Prompts) ───────────────────── */
    div.stButton > button {
        background: linear-gradient(135deg, rgba(59,130,246,0.1), rgba(6,182,212,0.1)) !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        border-radius: 10px !important;
        color: var(--accent-cyan) !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.82rem !important;
        font-weight: 500 !important;
        padding: 0.45rem 1rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: pointer !important;
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, rgba(59,130,246,0.25), rgba(6,182,212,0.25)) !important;
        border-color: var(--accent-blue) !important;
        box-shadow: var(--glow-blue) !important;
        transform: translateY(-1px) !important;
    }

    /* ── Expander (Source Docs) ────────────────────────────── */
    .streamlit-expanderHeader {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 10px !important;
        color: var(--text-secondary) !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.82rem !important;
    }
    .streamlit-expanderContent {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 0 0 10px 10px !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.78rem !important;
        color: var(--text-muted) !important;
    }

    /* ── Selectbox & Radio ────────────────────────────────── */
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
    }

    /* ── Divider ──────────────────────────────────────────── */
    hr {
        border-color: var(--border-color) !important;
    }

    /* ── Scrollbar ─────────────────────────────────────────── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg-primary); }
    ::-webkit-scrollbar-thumb { background: var(--border-color); border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--accent-blue); }

    /* ── Badges / Chips ───────────────────────────────────── */
    .complexity-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px;
        border-radius: 20px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        font-weight: 600;
        margin: 2px 4px;
    }
    .badge-time {
        background: rgba(59, 130, 246, 0.15);
        color: #60A5FA;
        border: 1px solid rgba(59, 130, 246, 0.3);
    }
    .badge-space {
        background: rgba(34, 197, 94, 0.15);
        color: #4ADE80;
        border: 1px solid rgba(34, 197, 94, 0.3);
    }
    .badge-difficulty-easy {
        background: rgba(34, 197, 94, 0.15);
        color: #4ADE80;
        border: 1px solid rgba(34, 197, 94, 0.3);
    }
    .badge-difficulty-medium {
        background: rgba(245, 158, 11, 0.15);
        color: #FBBF24;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }
    .badge-difficulty-hard {
        background: rgba(239, 68, 68, 0.15);
        color: #F87171;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }

    /* ── Logo / App Title ─────────────────────────────────── */
    .app-logo {
        text-align: center;
        padding: 1.5rem 0 1rem 0;
    }
    .app-logo .logo-icon {
        font-size: 3rem;
        display: block;
        margin-bottom: 0.3rem;
        animation: pulse 2s ease-in-out infinite;
    }
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50%      { transform: scale(1.08); }
    }
    .app-logo .logo-title {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 1.4rem;
        background: linear-gradient(135deg, #3B82F6, #06B6D4, #22C55E);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .app-logo .logo-sub {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        color: var(--text-muted);
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    /* ── Problem of the Day Card ──────────────────────────── */
    .potd-card {
        background: linear-gradient(135deg, rgba(139,92,246,0.12), rgba(59,130,246,0.10));
        border: 1px solid rgba(139, 92, 246, 0.25);
        border-radius: 14px;
        padding: 1rem 1.1rem;
        margin-top: 0.5rem;
    }
    .potd-card .potd-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: var(--accent-purple);
        margin-bottom: 0.5rem;
    }
    .potd-card .potd-title {
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.3rem;
    }
    .potd-card .potd-category {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: var(--text-muted);
    }

    /* ── Welcome Hero ─────────────────────────────────────── */
    .welcome-hero {
        text-align: center;
        padding: 4rem 2rem 2rem 2rem;
        animation: fadeSlideIn 0.6s ease-out;
    }
    .welcome-hero .hero-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
        display: block;
    }
    .welcome-hero .hero-title {
        font-family: 'Inter', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #3B82F6, #06B6D4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }
    .welcome-hero .hero-sub {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        color: var(--text-muted);
        max-width: 500px;
        margin: 0 auto;
        line-height: 1.6;
    }

    /* ── Source chip ───────────────────────────────────────── */
    .source-chip {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 12px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        font-weight: 500;
        background: rgba(6, 182, 212, 0.1);
        color: #22D3EE;
        border: 1px solid rgba(6, 182, 212, 0.25);
        margin-right: 6px;
    }

    /* ── Hide Streamlit branding (keep header visible for sidebar toggle) */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }

    /* ── Remove white borders / backgrounds from header & bottom bar ── */
    header[data-testid="stHeader"],
    div[data-testid="stBottom"],
    .stBottom,
    [data-testid="stBottomBlockContainer"] {
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
    }
    header[data-testid="stHeader"]::before,
    header[data-testid="stHeader"]::after,
    div[data-testid="stBottom"]::before,
    div[data-testid="stBottom"]::after,
    .stBottom::before,
    .stBottom::after {
        background: none !important;
        background-image: none !important;
        display: none !important;
    }
    /* Remove any remaining light backgrounds on main containers */
    .stMainBlockContainer, .block-container,
    [data-testid="stAppViewBlockContainer"] {
        background: transparent !important;
    }
    div[data-testid="stDecoration"] {
        display: none !important;
    }

    /* ── File uploader style ──────────────────────────────── */
    .stFileUploader {
        background: transparent !important;
    }
    .stFileUploader > div {
        background: var(--bg-card) !important;
        border: 1px dashed var(--border-color) !important;
        border-radius: 12px !important;
    }

    /* ── Spinner ──────────────────────────────────────────── */
    .stSpinner > div {
        border-top-color: var(--accent-blue) !important;
    }
    </style>
    """, unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════════╗
# ║  3. SESSION STATE MANAGEMENT                                    ║
# ╚══════════════════════════════════════════════════════════════════╝
def init_session_state():
    """Initialise all session-state keys used across the app."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "rag_ready" not in st.session_state:
        st.session_state.rag_ready = False
    if "potd" not in st.session_state:
        st.session_state.potd = _random_problem()


# ╔══════════════════════════════════════════════════════════════════╗
# ║  4. PROBLEM-OF-THE-DAY DATA                                    ║
# ╚══════════════════════════════════════════════════════════════════╝
PROBLEMS_POOL = [
    {"title": "Two Sum", "category": "Arrays • Hash Map", "difficulty": "Easy"},
    {"title": "Reverse Linked List", "category": "Linked Lists", "difficulty": "Easy"},
    {"title": "Valid Parentheses", "category": "Stacks", "difficulty": "Easy"},
    {"title": "Binary Search", "category": "Searching", "difficulty": "Easy"},
    {"title": "Maximum Subarray", "category": "Arrays • DP", "difficulty": "Medium"},
    {"title": "Merge Intervals", "category": "Arrays • Sorting", "difficulty": "Medium"},
    {"title": "LRU Cache", "category": "Hash Map • Linked Lists", "difficulty": "Medium"},
    {"title": "Number of Islands", "category": "Graphs • BFS/DFS", "difficulty": "Medium"},
    {"title": "Course Schedule", "category": "Graphs • Topological Sort", "difficulty": "Medium"},
    {"title": "Coin Change", "category": "Dynamic Programming", "difficulty": "Medium"},
    {"title": "Longest Increasing Subsequence", "category": "Dynamic Programming", "difficulty": "Medium"},
    {"title": "Kth Largest Element", "category": "Heaps", "difficulty": "Medium"},
    {"title": "Word Ladder", "category": "Graphs • BFS", "difficulty": "Hard"},
    {"title": "Serialize and Deserialize BST", "category": "Trees", "difficulty": "Hard"},
    {"title": "Trapping Rain Water", "category": "Arrays • Two Pointers", "difficulty": "Hard"},
    {"title": "N-Queens", "category": "Backtracking", "difficulty": "Hard"},
    {"title": "Sliding Window Maximum", "category": "Queues • Deque", "difficulty": "Hard"},
    {"title": "Merge K Sorted Lists", "category": "Heaps • Linked Lists", "difficulty": "Hard"},
]


def _random_problem():
    """Pick a random DSA problem for the sidebar widget."""
    return random.choice(PROBLEMS_POOL)


# ╔══════════════════════════════════════════════════════════════════╗
# ║  5. RAG PIPELINE CALL                                          ║
# ╚══════════════════════════════════════════════════════════════════╝
def call_rag_pipeline(query: str, topic_filter: str):
    """
    Call the RAG backend and return the response dict.
    Falls back to a simple chain if get_rag_response is unavailable.
    """
    from rag_chain import get_rag_response
    return get_rag_response(query, topic_filter)


# ╔══════════════════════════════════════════════════════════════════╗
# ║  6. HELPER: Extract complexity from answer text                 ║
# ╚══════════════════════════════════════════════════════════════════╝
def extract_complexity_badges(answer: str) -> str:
    """
    Scan the answer for Time/Space complexity mentions and
    return styled HTML badge chips.
    """
    import re

    badges = ""
    # Look for patterns like "Time: O(...)" or "Time Complexity: O(...)"
    time_match = re.search(r"[Tt]ime(?:\s*[Cc]omplexity)?[:\s]*O\([^)]+\)", answer)
    space_match = re.search(r"[Ss]pace(?:\s*[Cc]omplexity)?[:\s]*O\([^)]+\)", answer)

    if time_match:
        tc = re.search(r"O\([^)]+\)", time_match.group()).group()
        badges += f'<span class="complexity-badge badge-time">⏱ Time: {tc}</span>'
    if space_match:
        sc = re.search(r"O\([^)]+\)", space_match.group()).group()
        badges += f'<span class="complexity-badge badge-space">💾 Space: {sc}</span>'

    return badges


# ╔══════════════════════════════════════════════════════════════════╗
# ║  7. SIDEBAR RENDERING                                          ║
# ╚══════════════════════════════════════════════════════════════════╝
def render_sidebar():
    """Render the full sidebar: logo, filters, upload, and POTD widget."""
    with st.sidebar:

        # ── App Logo ─────────────────────────────────────────
        st.markdown("""
        <div class="app-logo">
            <span class="logo-icon">🧠</span>
            <div class="logo-title">DSA Mentor AI</div>
            <div class="logo-sub">Your Algorithm Companion</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # ── Topic Filter ─────────────────────────────────────
        st.markdown("##### 🏷️ Topic Filter")
        topic = st.selectbox(
            "Focus area",
            [
                "All Topics",
                "Arrays",
                "Linked Lists",
                "Stacks",
                "Queues",
                "Trees",
                "Graphs",
                "Hash Tables",
                "Heaps",
                "Sorting",
                "Searching",
                "Dynamic Programming",
                "Greedy Algorithms",
                "Backtracking",
            ],
            label_visibility="collapsed",
        )

        # ── Difficulty Selector ──────────────────────────────
        st.markdown("##### 🎯 Difficulty")
        difficulty = st.radio(
            "Difficulty",
            ["All", "Easy", "Medium", "Hard"],
            horizontal=True,
            label_visibility="collapsed",
        )

        st.markdown("---")

        # ── Clear Chat ───────────────────────────────────────
        if st.button("🗑️  Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

        st.markdown("---")

        # ── Upload PDF / Notes ───────────────────────────────
        st.markdown("##### 📄 Upload Notes")
        uploaded_file = st.file_uploader(
            "Upload PDF or TXT for RAG ingestion",
            type=["pdf", "txt", "json"],
            label_visibility="collapsed",
        )
        if uploaded_file:
            st.success(f"📎 **{uploaded_file.name}** uploaded!")
            # Save to data folder for future ingestion
            save_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "data", uploaded_file.name
            )
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.caption("Run `python ingest.py` to index this file.")

        st.markdown("---")

        # ── Problem of the Day ───────────────────────────────
        potd = st.session_state.potd
        diff_class = f"badge-difficulty-{potd['difficulty'].lower()}"
        st.markdown(f"""
        <div class="potd-card">
            <div class="potd-label">⚡ Problem of the Day</div>
            <div class="potd-title">{potd['title']}</div>
            <div class="potd-category">{potd['category']}</div>
            <div style="margin-top:8px;">
                <span class="complexity-badge {diff_class}">{potd['difficulty']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Ask about POTD button
        if st.button(f"💡 Solve: {potd['title']}", use_container_width=True):
            st.session_state.messages.append(
                {"role": "user", "content": f"Explain and solve the '{potd['title']}' problem with Python code, time and space complexity."}
            )
            st.rerun()

        st.markdown("---")
        st.caption("Built with ❤️ using LangChain + Gemini + ChromaDB")

    return topic, difficulty


# ╔══════════════════════════════════════════════════════════════════╗
# ║  8. QUICK PROMPT SUGGESTIONS                                   ║
# ╚══════════════════════════════════════════════════════════════════╝
def render_quick_prompts():
    """Render quick prompt suggestion buttons above the chat input."""
    suggestions = [
        "Explain Binary Search",
        "Solve a DP problem",
        "Time complexity of QuickSort",
        "Visualize BFS",
        "What is a Trie?",
        "Compare DFS vs BFS",
    ]

    cols = st.columns(len(suggestions))
    for i, suggestion in enumerate(suggestions):
        with cols[i]:
            if st.button(suggestion, key=f"quick_{i}", use_container_width=True):
                st.session_state.messages.append(
                    {"role": "user", "content": suggestion}
                )
                st.rerun()


# ╔══════════════════════════════════════════════════════════════════╗
# ║  9. CHAT INTERFACE RENDERING                                   ║
# ╚══════════════════════════════════════════════════════════════════╝
def render_chat_history():
    """Display all past chat messages with avatars, sources, and badges."""
    for i, msg in enumerate(st.session_state.messages):
        avatar = "🧑‍💻" if msg["role"] == "user" else "🧠"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

            # Show complexity badges for assistant messages
            if msg["role"] == "assistant":
                badges_html = extract_complexity_badges(msg["content"])
                if badges_html:
                    st.markdown(badges_html, unsafe_allow_html=True)

                # Show source documents in an expander
                if "sources" in msg and msg["sources"]:
                    with st.expander(f"📚 Source Documents ({len(msg['sources'])} retrieved)", expanded=False):
                        for j, src in enumerate(msg["sources"]):
                            st.markdown(
                                f'<span class="source-chip">{src["source"]}</span>',
                                unsafe_allow_html=True,
                            )
                            st.caption(src["content"])
                            if j < len(msg["sources"]) - 1:
                                st.markdown("---")


def render_welcome():
    """Show the welcome hero when chat is empty."""
    st.markdown("""
    <div class="welcome-hero">
        <span class="hero-icon">🧠</span>
        <div class="hero-title">Welcome to DSA Mentor AI</div>
        <div class="hero-sub">
            Your intelligent companion for mastering Data Structures & Algorithms.
            Ask me anything — from basic concepts to hard interview problems!
        </div>
    </div>
    """, unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════════╗
# ║  10. MAIN APPLICATION                                          ║
# ╚══════════════════════════════════════════════════════════════════╝
def main():
    """Entry point — wire everything together."""

    # Apply custom CSS
    apply_custom_css()

    # Initialise session state
    init_session_state()

    # Render sidebar and get filter selections
    topic_filter, difficulty = render_sidebar()

    # ── Main Chat Area ───────────────────────────────────────
    if not st.session_state.messages:
        render_welcome()

    # Quick prompt suggestions (shown only when chat is empty or always)
    render_quick_prompts()

    # Display chat history
    render_chat_history()

    # ── Chat Input ───────────────────────────────────────────
    if prompt := st.chat_input("Ask me anything about DSA..."):
        # Append difficulty hint if selected
        full_query = prompt
        if difficulty != "All":
            full_query = f"[{difficulty} difficulty] {prompt}"

        # Show user message immediately
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(prompt)

        # Generate assistant response
        with st.chat_message("assistant", avatar="🧠"):
            with st.spinner("🔍 Searching knowledge base & thinking..."):
                try:
                    result = call_rag_pipeline(full_query, topic_filter)
                    answer = result["answer"]
                    sources = result.get("sources", [])
                except Exception as e:
                    answer = (
                        f"⚠️ Sorry, an error occurred: `{e}`\n\n"
                        "Please make sure you've run `python ingest.py` and your "
                        "`.env` file contains a valid `GEMINI_API_KEY`."
                    )
                    sources = []

            # Render the answer
            st.markdown(answer)

            # Complexity badges
            badges_html = extract_complexity_badges(answer)
            if badges_html:
                st.markdown(badges_html, unsafe_allow_html=True)

            # Source documents expander
            if sources:
                with st.expander(f"📚 Source Documents ({len(sources)} retrieved)", expanded=False):
                    for j, src in enumerate(sources):
                        st.markdown(
                            f'<span class="source-chip">{src["source"]}</span>',
                            unsafe_allow_html=True,
                        )
                        st.caption(src["content"])
                        if j < len(sources) - 1:
                            st.markdown("---")

        # Save to history with sources
        st.session_state.messages.append(
            {"role": "assistant", "content": answer, "sources": sources}
        )


# ── Run ──────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
