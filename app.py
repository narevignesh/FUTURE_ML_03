import streamlit as st
import google.generativeai as genai

# --- CONFIGURE GEMINI ---
genai.configure(api_key="YOUR_API_KEY_HERE")  
model = genai.GenerativeModel("gemini-1.5-flash")

# --- STREAMLIT CONFIG ---
st.set_page_config(page_title="💬 AI ChatBot", layout="wide")

# --- SESSION STATE INIT ---
if "all_chats" not in st.session_state:
    st.session_state.all_chats = [[]]
if "current_chat_index" not in st.session_state:
    st.session_state.current_chat_index = 0

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("""
        <style>
        .sidebar {
            background-color: #1E1E1E;
            padding: 10px;
            height: 100vh;
        }
        .sidebar-title {
            font-size: 18px;
            font-family: 'Segoe UI', sans-serif;
            font-weight: 600;
            color: #ffffff;
            padding: 12px 14px;
            background: linear-gradient(90deg, #3B82F6 0%, #1D4ED8 100%);
            border-radius: 8px;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .sidebar-chat-container {
            max-height: calc(100vh - 180px);
            overflow-y: auto;
            padding-right: 4px;
        }
        .sidebar-chat-container::-webkit-scrollbar {
            width: 5px;
        }
        .sidebar-chat-container::-webkit-scrollbar-track {
            background: #2C2C2E;
            border-radius: 10px;
        }
        .sidebar-chat-container::-webkit-scrollbar-thumb {
            background: #3B82F6;
            border-radius: 10px;
        }
        .sidebar-chat-btn {
            background-color: #2C2C2E;
            color: #E5E5E5;
            border: none;
            padding: 10px 14px;
            text-align: left;
            width: 100%;
            font-size: 14px;
            font-family: 'Segoe UI', sans-serif;
            border-radius: 6px;
            margin-bottom: 8px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: all 0.2s ease;
        }
        .sidebar-chat-btn:hover {
            background-color: #3C3C3E;
            transform: translateX(2px);
        }
        .sidebar-chat-btn.active {
            background-color: #3B82F6;
            color: white;
        }
        .delete-chat-btn {
            background: transparent;
            border: none;
            color: #ff6b6b;
            cursor: pointer;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 14px;
            transition: all 0.2s ease;
        }
        .delete-chat-btn:hover {
            background: rgba(255, 75, 75, 0.2);
            transform: scale(1.1);
        }
        .new-chat-btn {
            margin-top: 16px;
            font-weight: bold;
            background: linear-gradient(90deg, #3B82F6 0%, #1D4ED8 100%);
            color: white;
            border: none;
            padding: 12px;
            width: 100%;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            transition: all 0.2s ease;
        }
        .new-chat-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        }
        .sidebar-divider {
            border-top: 1px solid #3C3C3E;
            margin: 16px 0;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-title">💬 Chat History</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-chat-container">', unsafe_allow_html=True)
    for i, chat in enumerate(st.session_state.all_chats):
        col1, col2 = st.columns([8, 1])
        with col1:
            title = chat[0][1][:26] + "..." if chat else "New chat"
            is_active = "active" if i == st.session_state.current_chat_index else ""
            if st.button(f"{title}", key=f"title_{i}", use_container_width=True, 
                        help="Click to load chat"):
                st.session_state.current_chat_index = i
        with col2:
            if st.button("🗑️", key=f"delete_{i}", help="Delete this chat"):
                if len(st.session_state.all_chats) > 1:
                    st.session_state.all_chats.pop(i)
                    if st.session_state.current_chat_index >= i:
                        st.session_state.current_chat_index = max(0, st.session_state.current_chat_index - 1)
                    st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    
    if st.button("➕ New chat", key="new_chat", use_container_width=True):
        st.session_state.all_chats.append([])
        st.session_state.current_chat_index = len(st.session_state.all_chats) - 1
        st.rerun()

# --- MAIN STYLING ---
st.markdown("""
    <style>
    html, body {
        background-color: #f9fafb;
        font-family: 'Segoe UI', sans-serif;
    }
    .main-content {
        padding-bottom: 100px;
    }
    .chat-container {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        max-height: calc(100vh - 300px);
        overflow-y: auto;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .user-msg, .bot-msg {
        padding: 10px 16px;
        border-radius: 16px;
        margin: 8px 0;
        font-size: 15px;
        max-width: 75%;
        line-height: 1.5;
        font-family: 'Segoe UI', sans-serif;
    }
    .user-msg {
        background-color: #DCFCE7;
        color: #065F46;
        align-self: flex-end;
        margin-left: auto;
    }
    .bot-msg {
        background-color: #E0F2FE;
        color: #0C4A6E;
        align-self: flex-start;
        margin-right: auto;
    }
    .msg-block {
        display: flex;
        align-items: flex-start;
        margin-bottom: 10px;
    }
    .user-block {
        justify-content: flex-end;
        flex-direction: row-reverse;
    }
    .title-style {
        font-size: 26px;
        font-weight: 700;
        color: #1D4ED8;
        margin-bottom: 0.3em;
        font-family: 'Segoe UI', sans-serif;
    }
    .subtitle-style {
        color: #64748B;
        font-size: 15px;
        margin-bottom: 1.2em;
        font-family: 'Segoe UI', sans-serif;
    }
    .chat-input-container {
        position: fixed;
        bottom: 0;
        left: 20%;
        right: 0;
        background: white;
        padding: 15px;
        border-radius: 10px 10px 0 0;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
        z-index: 100;
    }
    .stTextInput>div>div>input {
        padding-right: 40px !important;
    }
    .send-button {
        position: absolute;
        right: 10px;
        top: 50%;
        transform: translateY(-50%);
        background: none;
        border: none;
        cursor: pointer;
        color: #1D4ED8;
        font-size: 20px;
    }
    .stButton>button {
        background-color: #1D4ED8;
        color: white;
        padding: 10px 20px;
        border-radius: 8px;
        font-weight: bold;
        margin-top: 10px;
        font-family: 'Segoe UI', sans-serif;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #2563EB;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<div class="title-style">🤖 AI Support Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-style">Ask anything about our services. Gemini AI is ready to help you instantly.</div>', unsafe_allow_html=True)

# --- CHAT DISPLAY ---
st.markdown('<div class="main-content">', unsafe_allow_html=True)
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

current_chat = st.session_state.all_chats[st.session_state.current_chat_index]
for sender, msg in current_chat:
    if sender == "user":
        st.markdown(f"""
        <div class="msg-block user-block">
            <div class="user-msg">🧑 {msg}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="msg-block">
            <div class="bot-msg">🤖 {msg}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- USER INPUT FORM (FIXED AT BOTTOM) ---
with st.form("chat_form", clear_on_submit=True):
    st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)
    col1, col2 = st.columns([10, 1])
    with col1:
        user_input = st.text_input("You:", placeholder="Type your question...", label_visibility="collapsed")
    with col2:
        submitted = st.form_submit_button("➤", help="Send message")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if submitted and user_input:
        current_chat.append(("user", user_input))
        try:
            response = model.generate_content(user_input)
            bot_reply = response.text.strip()
        except Exception as e:
            bot_reply = "⚠️ Sorry, an error occurred while processing your request."
        current_chat.append(("bot", bot_reply))
        st.rerun()
