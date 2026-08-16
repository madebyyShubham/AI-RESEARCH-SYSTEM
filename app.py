import streamlit as st
import re

from Pipeline import run_research_pipeline


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Nexus Research",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --bg: #0b0e14;
        --surface: #12151f;
        --surface-2: #171b28;
        --border: #232838;
        --text: #e6e8ef;
        --text-dim: #8b91a7;
        --accent: #7c5cff;
        --accent-2: #22d3ee;
        --accent-soft: rgba(124, 92, 255, 0.12);
        --success: #34d399;
    }

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .stApp {
        background:
            radial-gradient(1200px 600px at 15% -10%, rgba(124,92,255,0.16), transparent 60%),
            radial-gradient(1000px 500px at 100% 0%, rgba(34,211,238,0.10), transparent 55%),
            var(--bg);
    }

    .block-container { padding-top: 2rem; max-width: 1100px; }

    h1, h2, h3, h4 { color: var(--text) !important; letter-spacing: -0.01em; }
    p, span, label, div { color: var(--text); }
    .stCaption, [data-testid="stCaptionContainer"] { color: var(--text-dim) !important; }

    /* ---------- Hero ---------- */

    .hero {
        padding: 2.75rem 2.5rem;
        border-radius: 22px;
        margin-bottom: 1.75rem;
        background: linear-gradient(135deg, #171b2b 0%, #1c1440 55%, #10233a 100%);
        border: 1px solid var(--border);
        position: relative;
        overflow: hidden;
    }

    .hero::after {
        content: "";
        position: absolute;
        top: -60px; right: -60px;
        width: 220px; height: 220px;
        background: radial-gradient(circle, rgba(124,92,255,0.35), transparent 70%);
        border-radius: 50%;
    }

    .hero-badge {
        display: inline-block;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--accent-2);
        background: rgba(34, 211, 238, 0.10);
        border: 1px solid rgba(34, 211, 238, 0.25);
        padding: 0.3rem 0.7rem;
        border-radius: 999px;
        margin-bottom: 1rem;
    }

    .hero h1 {
        font-size: 2.6rem;
        font-weight: 800;
        margin: 0 0 0.6rem 0;
        background: linear-gradient(90deg, #ffffff, #c9c3ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero p {
        font-size: 1.02rem;
        color: var(--text-dim);
        max-width: 640px;
        margin: 0;
    }

    /* ---------- Section labels ---------- */

    .section-label {
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: var(--text-dim);
        margin: 1.6rem 0 0.6rem 0;
    }

    /* ---------- Inputs ---------- */

    .stTextInput input {
        background-color: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        color: var(--text) !important;
        padding: 0.85rem 1rem !important;
        font-size: 1rem !important;
    }

    .stTextInput input:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px var(--accent-soft) !important;
    }

    /* ---------- Buttons ---------- */

    .stButton > button {
        border-radius: 11px;
        font-weight: 600;
        min-height: 46px;
        border: 1px solid var(--border);
        transition: all 0.15s ease;
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(90deg, var(--accent), #9b6bff);
        border: none;
        color: white;
        box-shadow: 0 6px 20px rgba(124, 92, 255, 0.35);
    }

    .stButton > button[kind="primary"]:hover {
        filter: brightness(1.08);
        transform: translateY(-1px);
    }

    .stButton > button:not([kind="primary"]) {
        background-color: var(--surface);
        color: var(--text-dim);
    }

    .stButton > button:not([kind="primary"]):hover {
        border-color: var(--accent);
        color: var(--text);
    }

    section[data-testid="stSidebar"] .stButton > button {
        text-align: left;
        justify-content: flex-start;
        font-weight: 500;
        font-size: 0.85rem;
        background-color: var(--surface);
        min-height: 38px;
        white-space: normal;
        line-height: 1.3;
    }

    /* ---------- Cards ---------- */

    .empty-state {
        padding: 3rem 2rem;
        border-radius: 18px;
        background-color: var(--surface);
        border: 1px dashed var(--border);
        text-align: center;
    }

    .empty-state .icon { font-size: 2.2rem; margin-bottom: 0.75rem; }
    .empty-state h4 { margin-bottom: 0.4rem; font-size: 1.15rem; }
    .empty-state p { color: var(--text-dim); max-width: 420px; margin: 0 auto; }

    /* ---------- Pipeline step chips (sidebar) ---------- */

    .step-chip {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        padding: 0.55rem 0.7rem;
        border-radius: 10px;
        background: var(--surface-2);
        border: 1px solid var(--border);
        margin-bottom: 0.5rem;
        font-size: 0.85rem;
    }

    .step-chip .num {
        width: 20px; height: 20px;
        border-radius: 6px;
        background: var(--accent-soft);
        color: var(--accent-2);
        font-size: 0.72rem;
        font-weight: 700;
        display: flex; align-items: center; justify-content: center;
        flex-shrink: 0;
    }

    /* ---------- Metric cards ---------- */

    [data-testid="stMetric"] {
        background-color: var(--surface);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 1rem 1.1rem;
    }

    [data-testid="stMetricLabel"] { color: var(--text-dim) !important; }
    [data-testid="stMetricValue"] { color: var(--success) !important; font-size: 1.1rem !important; }

    /* ---------- Tabs ---------- */

    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background-color: var(--surface);
        padding: 5px;
        border-radius: 12px;
        border: 1px solid var(--border);
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.5rem 1rem;
        color: var(--text-dim);
        font-weight: 600;
        font-size: 0.88rem;
    }

    .stTabs [aria-selected="true"] {
        background-color: var(--accent-soft) !important;
        color: var(--accent-2) !important;
    }

    .stTabs [data-baseweb="tab-panel"] { padding-top: 1.2rem; }

    /* ---------- Report / content text ---------- */

    .content-block {
        background-color: var(--surface);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 1.5rem 1.7rem;
        line-height: 1.65;
    }

    /* ---------- Sidebar container ---------- */

    section[data-testid="stSidebar"] {
        background-color: var(--surface);
        border-right: 1px solid var(--border);
    }

    table { border-color: var(--border) !important; }

    .footer {
        text-align: center;
        color: var(--text-dim);
        padding: 2.5rem 0 1rem 0;
        font-size: 0.8rem;
        letter-spacing: 0.02em;
    }

    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "research_state" not in st.session_state:
    st.session_state.research_state = None

if "last_topic" not in st.session_state:
    st.session_state.last_topic = ""

if "selected_topic" not in st.session_state:
    st.session_state.selected_topic = ""


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("### 🧠 Nexus Research")
    st.caption("Multi-agent AI research pipeline")

    st.markdown('<div class="section-label">Pipeline</div>', unsafe_allow_html=True)

    steps = [
        ("1", "🔎", "Search Agent — scans the web"),
        ("2", "📖", "Reader Agent — reads the best source"),
        ("3", "✍️", "Writer — drafts the report"),
        ("4", "🧐", "Critic — reviews the output"),
    ]

    for num, icon, label in steps:
        st.markdown(
            f'<div class="step-chip"><div class="num">{num}</div><div>{icon} {label}</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="section-label">Example Topics</div>', unsafe_allow_html=True)

    example_topics = [
        "Impact of Generative AI on software development",
        "Future of AI agents",
        "AI in healthcare",
        "Latest developments in quantum computing",
        "Cybersecurity and AI",
    ]

    for example in example_topics:
        if st.button(example, key=f"example_{example}", use_container_width=True):
            st.session_state.selected_topic = example
            st.rerun()

    st.divider()
    st.caption("Built with LangChain · LangGraph · OpenAI · Tavily")


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-badge">Multi-Agent Pipeline</div>
        <h1>Research anything, in minutes</h1>
        <p>
        Give it a topic. Nexus Research searches the web, reads the most
        relevant source, drafts a structured report, and has an AI critic
        review it — all in one pass.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# TOPIC INPUT
# ============================================================

st.markdown('<div class="section-label">Research Topic</div>', unsafe_allow_html=True)

topic = st.text_input(
    "Research Topic",
    value=st.session_state.selected_topic,
    placeholder="e.g. Impact of Generative AI on software development",
    label_visibility="collapsed",
    key="topic_input",
)

col1, col2, col3 = st.columns([1, 1, 3])

with col1:
    research_button = st.button("🚀 Start Research", type="primary", use_container_width=True)

with col2:
    clear_button = st.button("Clear", use_container_width=True)


if clear_button:
    st.session_state.research_state = None
    st.session_state.last_topic = ""
    st.session_state.selected_topic = ""
    st.rerun()


# ============================================================
# RUN RESEARCH
# ============================================================

if research_button:

    if not topic.strip():
        st.warning("⚠️ Please enter a research topic first.")

    else:
        st.session_state.last_topic = topic
        st.session_state.selected_topic = topic

        status = st.status("Running the research pipeline...", expanded=True)

        try:
            with status:
                st.write("🔎 Search Agent is researching the web...")
                st.write("📖 Reader Agent will analyze the best source...")
                st.write("✍️ Writer will generate the research report...")
                st.write("🧐 Critic will review the report...")
                st.caption(
                    "This backend runs synchronously, so stages complete "
                    "together rather than streaming live — that would need "
                    "callbacks added to Pipeline.py."
                )

                result = run_research_pipeline(topic)

            status.update(label="Research completed", state="complete", expanded=False)
            st.session_state.research_state = result

        except Exception as e:
            status.update(label="Something went wrong", state="error", expanded=True)
            with st.expander("Technical error details"):
                st.exception(e)


# ============================================================
# DISPLAY RESULTS
# ============================================================

result = st.session_state.research_state

if result:

    st.markdown('<div class="section-label">Results</div>', unsafe_allow_html=True)
    st.markdown(f"#### {st.session_state.last_topic}")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Search Agent", "Done")
    with col2:
        st.metric("Reader Agent", "Done")
    with col3:
        st.metric("Writer", "Done")
    with col4:
        st.metric("Critic", "Done")

    st.write("")

    search_result = result.get("search_result", "No search results available.")
    scraped_content = result.get(
        "scraped_content", result.get("Scrapped_content", "No scraped content available.")
    )
    report = result.get("report", "No report generated.")
    feedback = result.get("feedback", "No critic feedback available.")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["🔎 Search Results", "📖 Source Content", "📄 Final Report", "🧐 Critic Review"]
    )

    with tab1:
        st.markdown(f'<div class="content-block">{search_result}</div>', unsafe_allow_html=True)

        urls = list(dict.fromkeys(re.findall(r'https?://[^\s\)\]>"\']+', search_result)))
        if urls:
            st.markdown('<div class="section-label">Sources</div>', unsafe_allow_html=True)
            for i, url in enumerate(urls, start=1):
                st.markdown(f"{i}. [{url}]({url})")

    with tab2:
        if scraped_content:
            if len(scraped_content) > 4000:
                with st.expander("View full scraped content"):
                    st.markdown(scraped_content)
            else:
                st.markdown(f'<div class="content-block">{scraped_content}</div>', unsafe_allow_html=True)
        else:
            st.info("No scraped content was returned.")

    with tab3:
        st.markdown(f'<div class="content-block">{report}</div>', unsafe_allow_html=True)
        st.write("")

        safe_filename = (st.session_state.last_topic.replace(" ", "_").replace("/", "_") or "research")
        st.download_button(
            "⬇️ Download Report",
            data=report,
            file_name=f"{safe_filename}_research_report.txt",
            mime="text/plain",
        )

    with tab4:
        st.markdown(f'<div class="content-block">{feedback}</div>', unsafe_allow_html=True)

else:
    st.markdown(
        """
        <div class="empty-state">
            <div class="icon">🧠</div>
            <h4>No research yet</h4>
            <p>Enter a topic above and click <b>Start Research</b> — the agents will search, read, write and review automatically.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('<div class="footer">Nexus Research · Multi-Agent Research Pipeline</div>', unsafe_allow_html=True)