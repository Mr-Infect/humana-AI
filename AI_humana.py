import streamlit as st
import uuid
from model.inference import run_inference
from utils.logger import log_terminal_json
from utils.token_counter import get_token_stats
from utils.labeler import extract_topic  # 🆕
# from utils.relevance import is_relevant

st.set_page_config(page_title="Humana AI", layout="wide")

# --- STYLES ---
st.markdown("""
    <style>
    .block-container { padding-top: 1rem; padding-bottom: 0rem; }
    .chat-message { background-color: #202123; border-radius: 10px; padding: 10px; margin-bottom: 10px; }
    .chat-message.user { background-color: #262730; color: #fff; }
    .chat-message.assistant { background-color: #313339; color: #eee; }
    .sidebar-title { font-size: 1.5em; font-weight: bold; padding-bottom: 10px; }
    .history-chat { cursor: pointer; padding: 5px; margin: 4px 0; border-radius: 5px; background-color: #2d2f33; }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE INIT ---
if "chat_id" not in st.session_state:
    st.session_state.chat_id = str(uuid.uuid4())

if "chat_history" not in st.session_state:
    st.session_state.chat_history = {}

if "chat_labels" not in st.session_state:
    st.session_state.chat_labels = {}

# Init current chat
if st.session_state.chat_id not in st.session_state.chat_history:
    st.session_state.chat_history[st.session_state.chat_id] = []

# --- SIDEBAR CHAT HISTORY ---
with st.sidebar:
    st.markdown("<div class='sidebar-title'>💬 Chat Sessions</div>", unsafe_allow_html=True)
    
    for cid in st.session_state.chat_history:
        label = st.session_state.chat_labels.get(cid, f"🗂 Chat {list(st.session_state.chat_history).index(cid)+1}")
        if st.button(label, key=cid):
            st.session_state.chat_id = cid

    st.markdown("---")
    if st.button("➕ New Chat"):
        new_id = str(uuid.uuid4())
        st.session_state.chat_id = new_id
        st.session_state.chat_history[new_id] = []

# --- MAIN HEADING ---
st.title("🧠 Humana AI — Human Rights Chatbot")

# --- DISPLAY CHAT ---
current_chat = st.session_state.chat_history[st.session_state.chat_id]
for msg in current_chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- INPUT BAR ---
user_input = st.chat_input("Ask a human rights question...")

if user_input:
    current_chat.append({"role": "user", "content": user_input})

    # 🧠 Extract topic if this is the first message in chat
    if len(current_chat) == 1:
        topic = extract_topic(user_input)
        st.session_state.chat_labels[st.session_state.chat_id] = f"🗂 {topic.title()}"

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = run_inference(user_input)
            response = result["response"]
            tokens = get_token_stats(result["tokens"])

            st.markdown(response)
            st.caption(f"🧠 Tokens — {tokens} | ⚡ Latency: {result['latency']}s")

            current_chat.append({
                "role": "assistant",
                "content": f"{response}\n\n🧠 Tokens — {tokens} | ⚡ {result['latency']}s"
            })

            log_terminal_json({
                "user_input": user_input,
                "response": response,
                "tokens": tokens,
                "latency": result["latency"]
            })
