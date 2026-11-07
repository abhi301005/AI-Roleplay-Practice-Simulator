
import streamlit as st

from modules.roleplay import generate_reply
from modules.prompts import scenario_prompt
from modules.feedback import evaluate_session

st.set_page_config(
    page_title="AI Roleplay Simulator",
    page_icon="🎭",
    layout="wide"
)

st.title("🎭 AI Roleplay Practice Simulator")
st.caption("Practice real-world conversations using Generative AI")

with st.sidebar:
    st.header("Session Settings")

    scenario = st.selectbox(
        "Choose Scenario",
        [
            "HR Interview",
            "Technical Interview",
            "Customer Support",
            "English Conversation"
        ]
    )

    difficulty = st.selectbox(
        "Difficulty",
        ["Beginner", "Intermediate", "Advanced"]
    )

    personality = st.selectbox(
        "AI Personality",
        ["Friendly", "Professional", "Challenging"]
    )

    model = st.text_input(
        "Ollama Model",
        "llama3.2"
    )

    st.info("Use Ollama locally. No API key required.")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "started" not in st.session_state:
    st.session_state.started = False

if st.button("Start Roleplay", type="primary"):
    st.session_state.messages = []
    st.session_state.started = True

    opening_prompt = scenario_prompt(
        scenario,
        difficulty,
        personality,
        opening=True
    )

    response = generate_reply(
        [],
        opening_prompt,
        model
    )

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    st.rerun()

if st.button("Reset Conversation"):
    st.session_state.messages = []
    st.session_state.started = False
    st.rerun()

# Display conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat interface
if st.session_state.started:

    user_input = st.chat_input("Type your answer here...")

    if user_input:

        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        prompt = scenario_prompt(
            scenario,
            difficulty,
            personality
        )

        with st.spinner("AI is responding..."):

            response = generate_reply(
                st.session_state.messages,
                prompt,
                model
            )

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

        st.rerun()

st.divider()

st.subheader("📊 Performance Evaluation")

if st.session_state.messages:

    if st.button("Generate Feedback Report"):

        with st.spinner("Analyzing your answers..."):

            report = evaluate_session(
                st.session_state.messages,
                scenario,
                difficulty,
                model
            )

        st.markdown(report)

st.caption(
    "AI-generated educational feedback. "
    "Results are for practice purposes only."
)
