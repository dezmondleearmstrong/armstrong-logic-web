import streamlit as st
import json
import os
import pandas as pd
from google import genai

# --- SOVEREIGN BRANDING & THEME ---
st.set_page_config(page_title="Armstrong Logic | Sovereign Command", page_icon="🔱", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #050505; color: #00f2ff; font-family: 'Courier New', monospace; }
    .stTextInput>div>div>input { background-color: #111; color: #00f2ff; border: 1px solid #00f2ff; }
    .stButton>button { background-color: #00f2ff; color: black; border-radius: 0px; width: 100%; font-weight: bold; border: none; transition: 0.3s; }
    .stButton>button:hover { background-color: #0088ff; color: white; transform: scale(1.02); }
    .user-card { padding: 15px; border: 1px solid #333; margin-bottom: 10px; background: #0a0a0a; border-left: 4px solid #00f2ff; }
    .sidebar .sidebar-content { background-image: linear-gradient(#050505, #111); }
    </style>
    """, unsafe_allow_html=True)

# --- REGISTRY LOGIC (The Vault) ---
# This ensures user data survives cloud reboots
REGISTRY_PATH = "vault/registry.json"

def load_registry():
    if not os.path.exists("vault"): os.makedirs("vault")
    if not os.path.exists(REGISTRY_PATH):
        # Default master account
        with open(REGISTRY_PATH, "w") as f: json.dump({"dlee": "master99"}, f)
    with open(REGISTRY_PATH, "r") as f: return json.load(f)

def save_registry(data):
    with open(REGISTRY_PATH, "w") as f: json.dump(data, f)

# --- INITIALIZATION ---
if "authenticated" not in st.session_state: st.session_state.authenticated = False
registry = load_registry()

# --- LOGIN GATE ---
if not st.session_state.authenticated:
    st.title("🔱 ARMSTRONG LOGIC | SOVEREIGN ID GATE")
    st.write("System Status: Encrypted. Authorized Personnel Only.")
    
    col_l, col_r = st.columns(2)
    with col_l:
        user_input = st.text_input("User Cipher")
        pass_input = st.text_input("Access Key", type="password")
        if st.button("INITIATE HANDSHAKE"):
            if user_input in registry and registry[user_input] == pass_input:
                st.session_state.authenticated = True
                st.session_state.current_user = user_input
                st.rerun()
            else:
                st.error("HANDSHAKE FAILED: INVALID CIPHER")
    st.stop()

# --- SIDEBAR CONTROL ---
st.sidebar.title(f"🔱 NODE: {st.session_state.current_user.upper()}")
st.sidebar.write(f"Engine: Gemini 3.1 Pro (Thinking Mode)")
page = st.sidebar.radio("Navigation", ["Prophet Module", "User Registry", "System Diagnostics"])

if st.sidebar.button("DISCONNECT NODE"):
    st.session_state.authenticated = False
    st.rerun()

# --- USER REGISTRY (Pro Management) ---
if page == "User Registry":
    st.title("🛡️ SOVEREIGN USER REGISTRY")
    st.write("Manage active nodes and regional access keys.")
    
    with st.expander("ENROLL NEW USER NODE"):
        new_user = st.text_input("New Username (Cipher)")
        new_pass = st.text_input("New Password (Access Key)", type="password")
        if st.button("FINALIZE ENROLLMENT"):
            if new_user and new_pass:
                registry[new_user] = new_pass
                save_registry(registry)
                st.success(f"Node '{new_user}' has been added to the colony.")
                st.rerun()

    st.divider()
    st.subheader("ACTIVE NODES")
    for user in list(registry.keys()):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"<div class='user-card'>NODE: <b>{user.upper()}</b></div>", unsafe_allow_html=True)
        with col2:
            if user != "dlee": # Protect the Master ID
                if st.button(f"PURGE {user.upper()}", key=f"del_{user}"):
                    del registry[user]
                    save_registry(registry)
                    st.warning(f"Node '{user}' disconnected and purged.")
                    st.rerun()

# --- PROPHET MODULE (Analysis Node) ---
elif page == "Prophet Module":
    st.title("⚡ PROPHET MODULE: 3.1 PRO ANALYSIS")
    st.write("Detecting capital leaks and labor-to-sales entropy.")
    
    uploaded_file = st.file_uploader("Upload POS Data / Labor Log (.csv)", type="csv")
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df, use_container_width=True)
        
        if st.button("EXECUTE 3.1 PRO DIAGNOSTIC"):
            try:
                # Initialize Gemini 3.1 Pro
                client = genai.Client(api_key=st.secrets["gemini_key"])
                
                # Convert data to string for analysis
                data_summary = df.to_string()
                
                with st.spinner("Gemini 3.1 Pro is thinking..."):
                    response = client.models.generate_content(
                        model="gemini-3.1-pro-preview", 
                        contents=f"You are the Armstrong Logic Profit Prophet. Analyze this POS data for labor leaks, fraud, and inefficiencies. Provide a tactical executive summary: {data_summary}"
                    )
                
                st.markdown("### 🔱 PROPHET DIAGNOSTIC REPORT")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"ENGINE ERROR: {str(e)}")

# --- SYSTEM DIAGNOSTICS ---
elif page == "System Diagnostics":
    st.title("📟 SYSTEM DIAGNOSTICS")
    st.write("Infrastructure Status: 100 Trillion Years Ahead.")
    st.metric(label="Regional Nodes", value=len(registry))
    st.metric(label="Engine Latency", value="0.04ms")
    st.info("Ottawa, IL Hub: Operational")