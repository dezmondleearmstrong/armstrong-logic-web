import streamlit as st
from google import genai
import yagmail
import pandas as pd

# --- 1. TITAN CORE CONFIG ---
st.set_page_config(
    page_title="ArmstrongLogic | Neural Node",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Futuristic Obsidian UI Styling
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #e0e0e0; }
    [data-testid="stMetricValue"] { color: #00c6ff !important; font-family: 'Courier New', monospace; }
    .stButton > button {
        background: linear-gradient(135deg, #007bff 0%, #00c6ff 100%);
        color: white; border: none; border-radius: 8px;
        transition: 0.3s; font-weight: bold; letter-spacing: 1px;
    }
    .stButton > button:hover { transform: scale(1.05); box-shadow: 0 0 20px rgba(0, 123, 255, 0.4); }
    hr { border-color: #333 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ENGINE AUTHENTICATION ---
if "gemini_key" in st.secrets:
    client = genai.Client(api_key=st.secrets["gemini_key"])
    MY_EMAIL = st.secrets["my_email"]
    GMAIL_PASS = st.secrets["gmail_pass"]
    ADMIN_PASS = st.secrets.get("admin_password", "Titan97"O
X)
else:
    st.error("SYSTEM OFFLINE: Secrets Vault Not Found.")
    st.stop()

# --- 3. SESSION & REDIRECT LOGIC ---
if 'is_member' not in st.session_state: st.session_state.is_member = False
if 'leak_scans' not in st.session_state: st.session_state.leak_scans = 0

# Handle Payment Success Redirects
query_params = st.query_params
if query_params.get("status") == "success" or query_params.get("tier") == "sovereign":
    st.balloons()
    st.success("💎 AUTHORIZATION GRANTED: Welcome to the ArmstrongLogic Ecosystem.")
    st.info("Use your Neural Signature in the sidebar to unlock full forensic capabilities.")

# --- 4. BRANDED SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='color: #007bff;'>ArmstrongLogic</h1>", unsafe_allow_html=True)
    st.caption("Forensic Neural Mirror | v2.5.0-Quantum")
    st.divider()
    
    if st.session_state.is_member:
        st.success("✅ OPERATOR AUTHENTICATED")
        if st.button("TERMINATE SESSION"):
            st.session_state.is_member = False
            st.rerun()
    else:
        st.markdown("### Neural Signature")
        access_key = st.text_input("Enter Key", type="password")
        if access_key == ADMIN_PASS:
            st.session_state.is_member = True
            st.rerun()
    st.divider()
    st.info("Node Status: Optimal\nRegion: IL-72 | Ottawa")

# --- 5. THE DUAL-MODE ENGINE ---

if st.session_state.is_member:
    # --- MODE A: FORENSIC AUDIT ZONE (PAID) ---
    st.markdown("## 📊 Forensic Audit Zone")
    st.write("Ingest POS data to mirror hidden profit leaks in Labor, Food Waste, and Theft.")
    
    uploaded_file = st.file_uploader("Ingest POS .csv Data", type=['csv'])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        if st.button("EXECUTE NEURAL SCAN"):
            with st.spinner(“ARMSTRONGLOGIC decoding profit vectors..."):
                data_summary = df.describe().to_string()
                try:
                    prompt = (
                        f"Analyze this POS data summary: {data_summary}. "
                        "Identify specific leaks in: 1. Theft/Voids, 2. Labor Over-scheduling, 3. Food Waste. "
                        "Provide a 3-step surgical action plan to recover these profits. "
                        "Style: Direct, brilliant, and authoritative."
                    )
                    response = client.models.generate_content(model="gemini-2.5-pro", contents=prompt)
                    st.markdown("### 🧬 Forensic Insight")
                    st.info(response.text)
                    st.balloons()
                except Exception as e:
                    st.error(f"Neural Error: {e}")
else:
    # --- MODE B: GUEST CALCULATOR & PAYWALL ---
    LIMIT = 3
    if st.session_state.leak_scans < LIMIT:
        st.markdown("## 🛡️ Armstrong Logic | Leak Calculator")
        st.write(f"Node Cycles Remaining: {LIMIT - st.session_state.leak_scans}")
        
        col1, col2 = st.columns(2)
        with col1:
            res_name = st.text_input("Restaurant Name", placeholder="Your Restaurant")
            target_email = st.text_input("Email Destination")
        with col2:
            monthly_sales = st.number_input("Monthly Revenue ($)", min_value=0, step=1000)

        if st.button("ACTIVATE CALCULATION") and monthly_sales > 0 and target_email:
            with st.spinner("ARMSTRONGLOGIC Engine Analyzing..."):
                try:
                    leak_val = monthly_sales * 0.05
                    # TRI-VECTOR PROMPT
                    prompt = (          
                        f"Restaurant {res_name} does ${monthly_sales:,} sales. "
                        f"Explain how they are likely losing 5% (${leak_val:,.0f}) to a combination of: "
                        "1. Theft/Voids, 2. Labor Bloat, and 3. Food Waste. "   
                        "Keep it to 3 concise, punchy sentences. Mention ArmstrongLogic."
                    )
                    
                    response = client.models.generate_content(model="gemini-2.5-pro", contents=prompt)
                    
                    st.session_state.leak_scans += 1
                    
                    # Automated Dispatch
                    yag = yagmail.SMTP(MY_EMAIL, GMAIL_PASS)
                    yag.send(
                        to=[target_email, MY_EMAIL],
