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
    </style>
    """, unsafe_allow_html=True)

# --- 2. ENGINE AUTHENTICATION ---
if "gemini_key" in st.secrets:
    client = genai.Client(api_key=st.secrets["gemini_key"])
    MY_EMAIL = st.secrets["my_email"]
    GMAIL_PASS = st.secrets["gmail_pass"]
    ADMIN_PASS = st.secrets.get("admin_password", "Titan97")
else:
    st.error("SYSTEM OFFLINE: Secrets Vault Not Found.")
    st.stop()

# --- 3. SESSION LOGIC ---
if 'is_member' not in st.session_state: st.session_state.is_member = False
if 'leak_scans' not in st.session_state: st.session_state.leak_scans = 0

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

# --- 5. THE DUAL-MODE ENGINE ---

if st.session_state.is_member:
    st.markdown("## 📊 Forensic Audit Zone")
    uploaded_file = st.file_uploader("Ingest POS .csv Data", type=['csv'])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        if st.button("EXECUTE NEURAL SCAN"):
            with st.spinner("Gemini 2.5 Pro decoding profit vectors..."):
                data_summary = df.describe().to_string()
                try:
                    response = client.models.generate_content(
                        model="gemini-2.5-pro", 
                        contents=f"Forensic Audit: Analyze {data_summary}. Identify leaks in theft, labor, and waste. ArmstrongLogic style."
                    )
                    st.info(response.text)
                    st.balloons()
                except Exception as e:
                    st.error(f"Neural Error: {e}")
else:
    LIMIT = 3
    if st.session_state.leak_scans < LIMIT:
        st.markdown(f"## 🛡️ Armstrong Logic | Leak Calculator")
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
                    prompt = (          
                        f"Restaurant {res_name} does ${monthly_sales:,} sales. "
                        f"Explain how they are likely losing 5% (${leak_val:,.0f}) to a combination of: "
                        "1. Theft/Voids, 2. Labor Bloat, and 3. Food Waste. "   
                        "Keep it to 3 concise, punchy sentences. Mention ArmstrongLogic."
                    )
                    
                    # --- THIS LINE MUST BE INDENTED EXACTLY LIKE THIS ---
                    response = client.models.generate_content(
                        model="gemini-2.5-pro", 
                        contents=prompt
                    )
                    
                    st.session_state.leak_scans += 1
                    yag = yagmail.SMTP(MY_EMAIL, GMAIL_PASS)
                    yag.send(to=[target_email, MY_EMAIL], subject=f"ArmstrongLogic Report: {res_name}", contents=response.text)
                    
                    st.metric("Detected Monthly Leak", f"${(monthly_sales * 0.05):,.2f}")
                    st.markdown(f"**Forensic Insight:** {response.text}")
                except Exception as e:
                    st.error(f"Execution Error: {e}")
    else:
        st.warning("⚠️ TRIAL LIMIT REACHED")
        st.markdown("""<a href='https://buy.stripe.com/your_trial_link' style='text-decoration:none;'>
        <div style='background:#007bff; color:white; padding:20px; border-radius:10px; text-align:center; font-weight:bold;'>
        START 7-DAY TRIAL ($99/mo)</div></a>""", unsafe_allow_html=True)
