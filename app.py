import streamlit as st
from datetime import datetime

from modules.roleplay import generate_reply
from modules.prompts import scenario_prompt
from modules.feedback import evaluate_session

# --- Page Configuration ---
st.set_page_config(
    page_title="RoleplayAI Studio | Executive Simulator",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Elite SaaS Dark Theme & Micro-Interactions CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    * {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Background & Layout */
    .stApp {
        background: radial-gradient(circle at 15% 15%, #181c2b 0%, #0d1017 65%);
        color: #e2e8f0;
    }

    /* Sidebar Container */
    [data-testid="stSidebar"] {
        background: #0f131d !important;
        border-right: 1px solid rgba(255, 255, 255, 0.06);
    }
    
    [data-testid="stSidebar"] .block-container {
        padding-top: 2rem;
    }

    /* Gradient Brand Header */
    .brand-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 30%, #38bdf8 70%, #818cf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.03em;
        margin-bottom: 4px;
    }

    .brand-subtitle {
        color: #94a3b8;
        font-size: 0.92rem;
        margin-bottom: 1.2rem;
    }

    /* Metric & Tag Pills */
    .pill-container {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-bottom: 1.5rem;
    }

    .info-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 5px 12px;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 999px;
        font-size: 0.78rem;
        color: #cbd5e1;
        font-weight: 500;
    }

    .metric-badge {
        background: rgba(14, 165, 233, 0.08);
        border: 1px solid rgba(14, 165, 233, 0.25);
        border-radius: 12px;
        padding: 10px 16px;
        text-align: right;
    }

    .metric-num {
        font-size: 1.5rem;
        font-weight: 800;
        color: #38bdf8;
        line-height: 1;
    }

    .metric-label {
        font-size: 0.72rem;
        text-transform: uppercase;
        color: #64748b;
        letter-spacing: 0.6px;
        margin-top: 4px;
    }

    /* Status Dot Animation */
    .status-wrapper {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 6px 14px;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.4px;
        margin-bottom: 1rem;
    }

    .status-active {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        color: #34d399;
    }

    .status-idle {
        background: rgba(148, 163, 184, 0.08);
        border: 1px solid rgba(148, 163, 184, 0.18);
        color: #94a3b8;
    }

    .pulsing-dot {
        width: 8px;
        height: 8px;
        background: #10b981;
        border-radius: 50%;
        box-shadow: 0 0 10px #10b981;
        animation: pulse 1.8s infinite;
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.4; transform: scale(0.85); }
    }

    /* Custom Chat Message Cards */
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.025) !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-radius: 14px !important;
        padding: 18px 22px !important;
        margin-bottom: 14px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.18);
        backdrop-filter: blur(10px);
        transition: border-color 0.2s ease;
    }

    [data-testid="stChatMessage"]:hover {
        border-color: rgba(56, 189, 248, 0.25) !important;
    }

    /* Distinct styling for user message */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        background: rgba(56, 189, 248, 0.04) !important;
        border-left: 3px solid #38bdf8 !important;
    }

    /* Distinct styling for assistant message */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
        background: rgba(129, 140, 248, 0.04) !important;
        border-left: 3px solid #818cf8 !important;
    }

    /* Buttons Styling */
    button[kind="primary"] {
        background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%) !important;
        border: none !important;
        color: white !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35) !important;
        transition: all 0.2s ease !important;
    }

    button[kind="primary"]:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.45) !important;
    }

    button[kind="secondary"] {
        background: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #cbd5e1 !important;
        font-weight: 500 !important;
        border-radius: 8px !important;
        transition: all 0.2s ease !important;
    }

    button[kind="secondary"]:hover {
        background: rgba(255, 255, 255, 0.08) !important;
        border-color: rgba(255, 255, 255, 0.2) !important;
    }

    /* Input Field Polish */
    [data-testid="stChatInput"] {
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        background: rgba(15, 19, 29, 0.8) !important;
    }

    /* Selectboxes and text inputs */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {
        background-color: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.09) !important;
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "started" not in st.session_state:
    st.session_state.started = False
if "feedback_report" not in st.session_state:
    st.session_state.feedback_report = None

# --- Sidebar ---
with st.sidebar:
    st.markdown("### ⚙️ Simulation Control")
    
    # Active Session Indicator
    if st.session_state.started:
        st.markdown(
            '<div class="status-wrapper status-active"><span class="pulsing-dot"></span>Session Active</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div class="status-wrapper status-idle"><span>○</span> Simulator Idle</div>',
            unsafe_allow_html=True
        )

    scenario = st.selectbox(
        "Simulation Track",
        [
            "HR Interview",
            "Technical Interview",
            "Customer Support",
            "English Conversation"
        ],
        disabled=st.session_state.started,
        help="Select your simulation focus area."
    )

    c1, c2 = st.columns(2)
    with c1:
        difficulty = st.selectbox(
            "Difficulty",
            ["Beginner", "Intermediate", "Advanced"],
            disabled=st.session_state.started
        )
    with c2:
        personality = st.selectbox(
            "AI Persona",
            ["Friendly", "Professional", "Challenging"],
            disabled=st.session_state.started
        )

    with st.expander("🛠 Engine Settings", expanded=False):
        model = st.text_input(
            "Ollama Model",
            value="llama3.2",
            disabled=st.session_state.started,
            help="Ensure Ollama is running locally."
        )

    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)

    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        start_btn = st.button("🚀 Start", use_container_width=True, type="primary", disabled=st.session_state.started)
    with btn_col2:
        reset_btn = st.button("↺ Reset", use_container_width=True, type="secondary")

    if start_btn:
        st.session_state.messages = []
        st.session_state.feedback_report = None
        st.session_state.started = True

        opening_prompt = scenario_prompt(scenario, difficulty, personality, opening=True)

        with st.spinner("Initializing scenario environment..."):
            opening_msg = generate_reply([], opening_prompt, model)
            st.session_state.messages.append({"role": "assistant", "content": opening_msg})
        st.rerun()

    if reset_btn:
        st.session_state.messages = []
        st.session_state.started = False
        st.session_state.feedback_report = None
        st.rerun()

# --- Main Workspace ---
header_left, header_right = st.columns([0.75, 0.25])

user_turns = sum(1 for m in st.session_state.messages if m["role"] == "user")

with header_left:
    st.markdown('<div class="brand-title">🎭 AI Roleplay Studio</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-subtitle">High-fidelity conversational sparring powered by local LLMs</div>', unsafe_allow_html=True)
    
    # Context summary badges
    st.markdown(f"""
    <div class="pill-container">
        <span class="info-pill">🎯 {scenario}</span>
        <span class="info-pill">⚡ {difficulty}</span>
        <span class="info-pill">🧠 {personality}</span>
        <span class="info-pill">🤖 {model}</span>
    </div>
    """, unsafe_allow_html=True)

with header_right:
    st.markdown(f"""
    <div class="metric-badge">
        <div class="metric-num">{user_turns}</div>
        <div class="metric-label">Rounds Completed</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr style='border: none; border-top: 1px solid rgba(255,255,255,0.06); margin: 0.5rem 0 1.5rem 0;'>", unsafe_allow_html=True)

# Empty State
if not st.session_state.started and not st.session_state.messages:
    st.markdown("""
    <div style="text-align: center; padding: 3.5rem 1rem; border: 1px dashed rgba(255,255,255,0.12); border-radius: 16px; background: rgba(255,255,255,0.01);">
        <div style="font-size: 2.2rem; margin-bottom: 0.5rem;">🎙️</div>
        <h3 style="color: #cbd5e1; margin-bottom: 0.4rem;">Simulation Room Idle</h3>
        <p style="color: #64748b; font-size: 0.88rem; max-width: 420px; margin: 0 auto 1.2rem auto;">
            Configure your scenario, difficulty, and persona on the sidebar, then click <b>Start</b> to begin.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Conversation Stream
for message in st.session_state.messages:
    avatar_icon = "🤖" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar_icon):
        st.markdown(message["content"])

# User Chat Input
if st.session_state.started:
    user_input = st.chat_input("Compose your response...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)

        prompt = scenario_prompt(scenario, difficulty, personality)
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Analyzing context & formulating response..."):
                response = generate_reply(st.session_state.messages, prompt, model)
                st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})

# --- Feedback & Diagnostics Section ---
if len(st.session_state.messages) >= 2:
    st.markdown("<hr style='border: none; border-top: 1px solid rgba(255,255,255,0.06); margin: 2.5rem 0 1.5rem 0;'>", unsafe_allow_html=True)
    
    col_fb_info, col_fb_act = st.columns([0.72, 0.28])
    with col_fb_info:
        st.markdown("### 📊 Performance Analytics & Feedback")
        st.caption("Receive a detailed breakdown evaluating clarity, delivery, and domain readiness.")
    with col_fb_act:
        eval_btn = st.button("Generate Diagnostic Report", type="secondary", use_container_width=True)

    if eval_btn:
        with st.spinner("Synthesizing interaction analysis..."):
            report = evaluate_session(st.session_state.messages, scenario, difficulty, model)
            st.session_state.feedback_report = report

    if st.session_state.feedback_report:
        with st.container():
            st.markdown("""
            <div style="background: rgba(16, 185, 129, 0.05); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: 12px; padding: 1.2rem; margin-top: 1rem;">
            """, unsafe_allow_html=True)
            st.markdown(st.session_state.feedback_report)
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.download_button(
                label="📥 Export Report (.md)",
                data=st.session_state.feedback_report,
                file_name=f"roleplay_assessment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown",
                type="secondary"
            )
