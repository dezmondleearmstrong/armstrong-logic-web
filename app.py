import streamlit as st
import pandas as pd
from google import genai
import time
import yagmail

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Armstrong Logic | Sovereign Command", layout="wide")

# --- CUSTOM BRANDING (Metallic & Cyan) ---
st.markdown("""
<style>
    /* Main background: Dark metallic gradient */
    .stApp {
        background: linear-gradient(135deg, #111111 0%, #2a2a2a 100%);
        color: #e0e0e0;
    }
    /* Headers and highlights */
    h1, h2, h3, h4, h5, h6 {
        color: #00FFFF !important;
        font-family: 'Courier New', Courier, monospace;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    p, span, div {
        font-family: 'Courier New', Courier, monospace;
    }
    /* Buttons: Cyan accent */
    .stButton>button {
        background-color: transparent;
        color: #00FFFF;
        border: 1px solid #00FFFF;
        border-radius: 2px;
        transition: all 0.3s ease;
        text-transform: uppercase;
        font-weight: bold;
        letter-spacing: 1px;
    }
    .stButton>button:hover {
        background-color: #00FFFF;
        color: #000000;
        box-shadow: 0 0 15px #00FFFF;
    }
    /* Metric styling */
    [data-testid="stMetricValue"] {
        color: #00FFFF !important;
    }
    [data-testid="stMetricDelta"] {
        color: #00FF99 !important;
    }
    /* Inputs */
    .stTextInput>div>div>input {
        background-color: #1a1a1a;
        color: #00FFFF;
        border: 1px solid #444;
    }
    /* Divider */
    hr {
        border-color: #00FFFF;
        opacity: 0.3;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. SECURE INITIALIZATION ---
if "gemini_key" in st.secrets:
    client = genai.Client(api_key=st.secrets["gemini_key"])
    MY_EMAIL = st.secrets["my_email"]
    GMAIL_PASS = st.secrets["gmail_pass"]
else:
    st.error("🔑 Secrets missing. Please check your .streamlit/secrets.toml")
    st.stop()

# --- 3. LOGIN GATEKEEPER ---
CLIENT_PASSWORDS = {"armstrong": "logic99"}

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.markdown("<h1 style='text-align: center; margin-top: 10vh;'>🔱 ARMSTRONG LOGIC 🔱<br>SOVEREIGN OPERATIONAL COMMAND</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888;'>RESTRICTED ACCESS: 100 TRILLION YEAR DIRECTIVE</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        user = st.text_input("SOVEREIGN ID").lower()
        pw = st.text_input("CIPHER", type="password")
        if st.button("INITIALIZE LINK"):
            if user in CLIENT_PASSWORDS and CLIENT_PASSWORDS[user] == pw:
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("ACCESS DENIED: ENTROPY DETECTED.")
    st.stop()

# --- 4. COMMAND INTERFACE ---
st.title("🔱 ARMSTRONG LOGIC: SOVEREIGN OPERATIONAL COMMAND")
st.markdown("### SYSTEM STATUS: **100 TRILLION YEARS AHEAD. OPTIMAL.**")

# --- 5. OTTAWA NODE DIAGNOSTICS ---
st.markdown("---")
st.header("📍 OTTAWA NODE DIAGNOSTICS")
st.markdown("Real-time telemetry for regional expansion and capital reclamation.")

col_a, col_b, col_c = st.columns(3)
col_a.metric(label="Active Nodes (Ottawa, IL)", value="3", delta="Saturation Reached")
col_b.metric(label="Empire EBITDA Lift", value="$422,415.33", delta="+$35,201.28/mo")
col_c.metric(label="System Entropy", value="0.0%", delta="-33.3% Labor Variance")
st.markdown("---")

# --- 6. DATA AUDIT INTERFACE ---
st.subheader("📡 REGIONAL DATA ASSIMILATION")
st.write("Upload an operational CSV export (Sales, COGS, or Labor) for Sentinel/Prophet processing.")

uploaded_file = st.file_uploader("Upload Node Data", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df.head(10)) # Show preview
    
    analysis_goal = st.selectbox("Focus Area", ["Overall Profit Leak", "Inventory Inefficiencies", "Labor Overages (The 25% Cap)"])

    if st.button("🚀 EXECUTE PROPHET REALLOCATION"):
        with st.spinner("Synthesizing logic... Folding spacetime..."):
            
            # Convert CSV to string for the AI
            csv_data = df.to_string(index=False)
            
            prompt = f"""
            Act as the 'Prophet' module of the Armstrong Logic Empire. Analyze this data: {csv_data}
            Focus on {analysis_goal}. 
            Identify specific patterns of operational entropy, ruthlessly enforce a 25% labor cap, and provide a Deterministic Command Directive (e.g., CUT mid-day overlaps, SURGE evening peaks). Maintain a cold, absolute, high-end '100 trillion years ahead' tone.
            """

            # --- 7. RETRY LOGIC FOR GEMINI PRO ---
            success = False
            for attempt in range(3):
                try:
                    response = client.models.generate_content(
                        model="gemini-1.5-pro", 
                        contents=prompt
                    )
                    audit_result = response.text
                    st.success("SYNTHESIS COMPLETE.")
                    st.markdown(audit_result)
                    
                    # Store result for email
                    st.session_state['last_audit'] = audit_result
                    success = True
                    break
                except Exception as e:
                    if "429" in str(e):
                        st.warning(f"Bandwidth saturated. Re-routing in {15*(attempt+1)}s...")
                        time.sleep(15 * (attempt + 1))
                    else:
                        st.error(f"Error: {e}")
                        break
            
            if success:
                # Option to email this deep audit to the client
                st.markdown("---")
                target_client = st.text_input("Transmit Executive Summary to Sovereign Lead (Email):")
                if st.button("📧 TRANSMIT DIRECTIVE") and target_client:
                    yag = yagmail.SMTP(MY_EMAIL, GMAIL_PASS)
                    yag.send(to=target_client, subject="Armstrong Logic: Sovereign Command Directive", contents=st.session_state['last_audit'])
                    st.success("TRANSMISSION SECURED.")

# Sidebar Navigation Note
st.sidebar.markdown("### 🔱 SOVEREIGN LINK")
st.sidebar.success("LOGGED IN: ARMSTRONG")
if st.sidebar.button("TERMINATE LINK"):
    st.session_state["authenticated"] = False
    st.rerun()
