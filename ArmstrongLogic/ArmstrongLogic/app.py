import os
import streamlit as st
import pandas as pd
from google import genai
import io

# --- 1. SOVEREIGN UI CONFIGURATION ---
st.set_page_config(page_title="Armstrong Logic | Prophet", layout="wide")

#  
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #1a2a3a 0%, #0a0f14 100%); color: #f0f0f0; }
    [data-testid="stSidebar"] { background-color: rgba(10, 15, 20, 0.9); border-right: 1px solid rgba(0, 229, 255, 0.1); }
    .crystalline-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(25px);
        border: 1px solid rgba(0, 229, 255, 0.2);
        border-radius: 15px;
        padding: 30px;
        margin-bottom: 20px;
    }
    .stButton>button {
        background: #ffffff; color: #000000; border-radius: 20px; border: none; font-weight: bold; width: 100%;
    }
    input { background-color: rgba(0, 0, 0, 0.2) !important; color: white !important; border: 1px solid #333 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. API & AUTH INITIALIZATION ---
api_key = st.secrets.get("gemini_key")
client = genai.Client(api_key=api_key) if api_key else None

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# --- 3. THE GATEKEEPER (Login Node) ---
if not st.session_state["authenticated"]:
    cols = st.columns([1, 1.5, 1])
    with cols[1]:
        st.markdown('<div class="crystalline-card">', unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; color: #00e5ff;'>ARMSTRONGLOGIC</h1>", unsafe_allow_html=True)
        st.write("### AI-Powered Profit Protection")
        
        user_input = st.text_input("Node ID").lower()
        pass_input = st.text_input("Security Key", type="password")
        
        if st.button("Initialize Uplink"):
            if user_input == "armstrong" and pass_input == "logic99":
                st.session_state["authenticated"] = True
                st.session_state["user"] = "Dezmond"
                st.rerun()
            else:
                st.error("Access Denied: Invalid Credentials")
        st.markdown('</div>', unsafe_allow_html=True)

# --- 4. THE PROPHET DASHBOARD ---
else:
    # Sidebar Logout
    if st.sidebar.button("Terminate Session"):
        st.session_state["authenticated"] = False
        st.rerun()
    
    st.sidebar.markdown("---")
    st.sidebar.write(f"Architect: {st.session_state['user']}")
    st.sidebar.write("System: Prophet v4.0")

    st.title("🛡️Armstronglogic  Dashboard")
    
    if not client:
        st.error("🔑 API Key Missing: Configure 'gemini_key' in Secrets.")

    # CSV AUDIT SECTION
    st.markdown('<div class="crystalline-card">', unsafe_allow_html=True)
    st.write("### 📂 Upload Audit Data")
    uploaded_file = st.file_uploader("Drop restaurant CSV file", type="csv")
    st.markdown('</div>', unsafe_allow_html=True)

    if uploaded_file:
        # Load data once to prevent multiple reads
        df = pd.read_csv(uploaded_file)
        st.dataframe(df.head(10), use_container_width=True)

        if st.button("🚀 Run 🛡️armstronglogic Audit"):
            if client:
                with st.spinner("🛡️Armstronglogic analyzing..."):
                    data_summary = df.head(50).to_string()
                    prompt = f"You are 'Profit Watchdog AI'. Analyze this data and identify 3 areas of profit loss and 3 action steps: {data_summary}"
                    
                    try:
                        response = client.models.generate_content(
                            model="gemini-3-flash-preview", 
                            contents=prompt
                        )
                        st.markdown('<div class="crystalline-card">', unsafe_allow_html=True)
                        st.markdown("### 🤖 AI Auditor Breakdown")
                        st.write(response.text)
                        st.markdown('</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"AI Logic Fault: {e}")
            else:
                st.warning("AI Node Offline: Missing API Key.")

# --- 5. GLOBAL FOOTER ---
st.markdown("---")
st.caption("ANAB ACCREDITED • CERTIFIED FOOD PROTECTION MANAGER  • ISO 42001 COMPLIANT")
