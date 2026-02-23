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

# Futuristic Obsidian UI Styling - TYPO FIXED
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #050505;
        color: #e0e0e0;
    }
    /* Metric Glow */
    [data-testid="stMetricValue"] {
        color: #00c6ff !important;
        font-family: 'Courier New', monospace;
        text-shadow: 0 0 10px rgba(0, 198, 255, 0.5);
    }
    /* Button Aesthetics */
    .stButton > button {
        background: linear-gradient(135deg, #007bff 0%, #00c6ff 100%);
        color: white;
        border: none;
        padding: 12px 30px;
        border-radius: 8px;
        font-weight: bold;
        transition: 0.3s;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 20px rgba(0, 123, 255, 0.4);
    }
    /* Input Overrides */
    .stTextInput input, .stNumberInput input {
        background-color: #111 !important;
        color: #00c6ff !important;
        border: 1px solid #333 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ENGINE AUTHENTICATION ---
if "gemini_key" in st.secrets:
    client = genai.Client(api_key=st.secrets["gemini_key"])
    MY_EMAIL = st.secrets["my_email"]
    GMAIL_PASS = st.secrets["gmail_pass"]
    ADMIN_PASS = st.secrets.get("admin_password")
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
        st.info("Node: IL-72")
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
    st.progress(100, text="System Integrity: Optimal")
    st.caption("© 2026 ArmstrongLogic")

# --- 5. THE DUAL-MODE ENGINE ---

# MODE A: UNLIMITED MEMBER ACCESS (GEMINI 2.5 PRO)
if st.session_state.is_member:
    st.markdown("## 📊 Forensic Audit Zone")
    st.write("Deep-scanning POS structures for hidden waste.")
    
    uploaded_file = st.file_uploader("Ingest POS .csv Data", type=['csv'])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df.head(10), use_container_width=True)
        
        if st.button("EXECUTE NEURAL SCAN"):
            with st.spinner(“ARMSTRONGLOGIC decoding profit vectors..."):
                data_summary = df.describe().to_string()
                try:
                    response = client.models.generate_content(
                        model="gemini-2.5-pro", 
                        contents=f"Perform a forensic audit on this data: {data_summary}. Identify 3 profit leaks. Be direct, witty, and brilliant. ArmstrongLogic style."
                    )
                    st.markdown("---")
                    st.info(response.text)
                    st.balloons()
                except Exception as e:
                    st.error(f"Neural Error: {e}")

# MODE B: GUEST CALCULATOR (3-STRIKE LIMIT)
else:
    LIMIT = 3
    if st.session_state.leak_scans < LIMIT:
        st.markdown(f"## 🧪 Profit Leak Calculator")
        st.write(f"Node Cycles Remaining: {LIMIT - st.session_state.leak_scans}")
        
        col1, col2 = st.columns(2)
        with col1:
            res_name = st.text_input("Restaurant Name", placeholder="Mama's Pizza")
            target_email = st.text_input("Email Destination")
        with col2:
            monthly_sales = st.number_input("Monthly Revenue ($)", min_value=0, step=1000)

        if st.button("ACTIVATE CALCULATION") and monthly_sales > 0 and target_email:
            with st.spinner("2.5 Pro Engine Analyzing..."):
                try:
                    prompt = f"Restaurant {res_name} does ${monthly_sales} sales. Explain 5% loss to theft/voids in 2 sentences. Mention ArmstrongLogic."
                    response = client.models.generate_content(model="gemini-2.5-pro", contents=prompt)
                    
                    st.session_state.leak_scans += 1
                    
                    # Email Logic
                    yag = yagmail.SMTP(MY_EMAIL, GMAIL_PASS)
                    yag.send(to=[target_email, MY_EMAIL], 
                             subject=f"ArmstrongLogic Report: {res_name}", 
                             contents=f"Analysis:\n\n{response.text}")
                    
                    # UI Result
                    leak_val = monthly_sales * 0.05
                    st.metric("Estimated Monthly Leak", f"${leak_val:,.2f}", delta="Action Required", delta_color="inverse")
                    st.markdown(f"**Forensic Insight:** {response.text}")
                    st.success(f"Report dispatched to {target_email}.")
                except Exception as e:
                    st.error(f"Execution Error: {e}")
    else:
        # THE PAYWALL
        st.markdown(f"""
        <div style="background: rgba(0, 123, 255, 0.1); padding: 40px; border-radius: 20px; border: 1px solid #007bff; text-align: center;">
            <h1 style="color: #007bff;">LIMIT REACHED</h1>
            <p style="font-size: 1.1rem;">Trial node exhausted. Unlock the full Forensic Suite.</p>
            <br>
            <a href="https://buy.stripe.com/your_trial_link" target="_blank" style="
                background: linear-gradient(135deg, #007bff 0%, #00c6ff 100%);
                color: white; padding: 20px 40px; text-decoration: none; 
                font-weight: bold; border-radius: 12px; font-size: 1.1rem;
                box-shadow: 0 0 20px rgba(0,123,255,0.4);
            ">Activate Full Neural Mirror ($99/mo)</a>
        </div>
        """, unsafe_allow_html=True)
