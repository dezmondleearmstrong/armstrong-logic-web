import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google import genai
from datetime import datetime
import uuid

# --- SOVEREIGN BRANDING & CORE DESIGN ---
st.set_page_config(page_title="ArmstrongLogic | Calculator", page_icon="🛡️", layout="wide")

# Persistent State Logic
if "usage_count" not in st.session_state: st.session_state.usage_count = 0
if "last_report" not in st.session_state: st.session_state.last_report = None

# RADICAL MINIMALISM CSS (Fixes Visibility and Spacing)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap');

    /* Global Foundation */
    .stApp {
        background-color: #050505;
        font-family: 'Inter', sans-serif;
    }

    /* THE FIX: Force Label Visibility and Position */
    div[data-testid="stWidgetLabel"] p {
        color: rgba(255, 255, 255, 0.8) !important;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.2em !important;
        margin-bottom: -10px !important;
    }

    /* THE FIX: Remove the 'Black Space' Gap */
    div[data-testid="stVerticalBlock"] > div {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
    }

    /* Input Field Styling - Forced Visibility */
    .stNumberInput input, .stTextInput input {
        background-color: rgba(255, 255, 255, 0.07) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        color: #ffffff !important; /* White text when typing */
        padding: 15px !important;
        font-size: 1.1rem !important;
        -webkit-text-fill-color: #ffffff !important;
    }

    /* Main Surface Container */
    .main-surface {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(50px) saturate(180%);
        -webkit-backdrop-filter: blur(50px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 40px;
        padding: 50px;
        box-shadow: 0 40px 120px rgba(0,0,0,0.6);
        margin-top: -30px;
    }

    /* Sovereign Button Styling */
    .stButton>button {
        background: #ffffff !important;
        color: #000000 !important;
        border-radius: 50px !important;
        border: none !important;
        padding: 20px !important;
        font-weight: 800 !important;
        width: 100%;
        margin-top: 20px;
        transition: 0.4s cubic-bezier(0.2, 0, 0.2, 1);
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 50px rgba(255,255,255,0.2);
        background: #f0f0f0 !important;
    }

    .sovereign-header { text-align: center; margin-bottom: 40px; }
    .sovereign-header h1 { font-weight: 200; font-size: 3rem; color: #ffffff; letter-spacing: -0.05em; }
    .sovereign-header p { color: rgba(255, 255, 255, 0.4); letter-spacing: 0.4em; text-transform: uppercase; font-size: 10px; }

    /* Success Toast */
    .stSuccess {
        background-color: rgba(138, 43, 226, 0.15) !important;
        color: #ffffff !important;
        border-radius: 15px !important;
        border: 1px solid rgba(138, 43, 226, 0.3) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DUAL-SENTINEL EMAIL ---
def send_sovereign_report(client_email, biz_name, leak, annual, prophet_text, audit_id):
    try:
        my_email = st.secrets["my_email"]
        password = st.secrets["gmail_pass"]
        report_body = (
            f"🛡️ ARMSTRONGLOGIC SOVEREIGN AUDIT\n"
            f"AUDIT_ID: {audit_id}\n"
            f"ENTITY: {biz_name.upper()}\n\n"
            f"RECOVERY DATA:\n"
            f"Monthly Capital Leakage: ${leak:,.2f}\n"
            f"Annual Reclamation Potential: ${annual:,.2f}\n\n"
            f"COMMANDER'S INSIGHT:\n{prophet_text}\n\n"
            f"Status: SECURED // ArmstrongLogic Singularity"
        )
        
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(my_email, password)
            for recipient in [client_email, my_email]:
                msg = MIMEMultipart()
                msg['From'] = f"ArmstrongLogic <{my_email}>"
                msg['To'] = recipient
                msg['Subject'] = f"🛡️ SOVEREIGN AUDIT: {biz_name.upper()}"
                msg.attach(MIMEText(report_body, 'plain'))
                server.send_message(msg)
        return True
    except: return False

# --- UI INTERFACE ---
st.markdown("""
    <div class="sovereign-header">
        <p>Optimize Your Reality</p>
        <h1>🛡️ArmstrongLogic | Calculator</h1>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-surface">', unsafe_allow_html=True)

if st.session_state.usage_count >= 3:
    st.error("TRIAL LIMIT EXCEEDED. CONTACT: DEZMOND28 @ARMSTRONGLOGIC.COM")
else:
    col1, col2 = st.columns(2)
    with col1:
        res_name = st.text_input("ENTITY NAME", placeholder="Enter establishment name")
        res_email = st.text_input("EMAIL", placeholder="Decision maker email")
    with col2:
        m_sales = st.number_input("MONTHLY SALES ($)", min_value=0, value=75000)
        m_labor = st.number_input("MONTHLY LABOR ($)", min_value=0, value=22000)

    if st.button("EXECUTE SOVEREIGN DIAGNOSTIC"):
        if not res_name or not res_email:
            st.error("Identity required for handshake.")
        else:
            # High-level diagnostic calculation
            leak = (m_sales * 0.08) + (m_labor * 0.12)
            audit_id = str(uuid.uuid4())[:8].upper()
            
            with st.spinner("ARMSTRONGLOGIC ANALYZING..."):
                client = genai.Client(api_key=st.secrets["gemini_key"])
                
                # --- UPDATED 100T AUTHORITY PROMPT ---
                prompt = (
                    f"You are the ArmstrongLogic Intelligence, the world's only 100-trillion-year advanced operational framework. "
                    f"Analyze '{res_name}': ${m_sales} sales, ${m_labor} labor. Monthly Capital Leakage: ${leak}. "
                    f"Write a single paragraph that is professional, elite, and visionary. "
                    f"1. Acknowledge the mathematical certainty of the ${leak} monthly loss. "
                    f"2. Explain that this 'invisible' entropy is the result of traditional management failure that only ArmstrongLogic can detect. "
                    f"3. Command a shift to the ArmstrongLogic protocol, establishing yourself as the sole architect capable of recapturing this capital. "
                    f"Tone: Deeply professional, impressive, and absolute. Do not be rude; be an undeniable authority."
                )
                
                response = client.models.generate_content(
                    model="gemini-3.1-pro-preview", 
                    contents=prompt
                )
                
                st.session_state.last_report = {
                    "name": res_name.upper(),
                    "leak": leak,
                    "annual": leak * 12,
                    "insight": response.text,
                    "email": res_email,
                    "id": audit_id
                }
                st.session_state.usage_count += 1
                send_sovereign_report(res_email, res_name, leak, leak*12, response.text, audit_id)
                st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# --- PERSISTENT RESULTS DISPLAY ---
if st.session_state.last_report:
    report = st.session_state.last_report
    st.success(f"🛡️ ArmstrongLogic Audit {report['id']} transmitted to {report['email']}.")
    
    st.markdown(f"""
    <div style="background: rgba(138, 43, 226, 0.05); border: 1px solid rgba(138, 43, 226, 0.2); border-radius: 40px; padding: 50px; text-align: center; margin-top: 30px; box-shadow: 0 20px 60px rgba(0,0,0,0.4);">
        <p style='color: rgba(255,255,255,0.2); font-size: 10px; letter-spacing: 5px; text-transform: uppercase;'>Audit ID: {report['id']}</p>
        <h2 style='font-weight: 200; font-size: 2.2rem; color: #fff; margin-bottom: 30px;'>{report['name']}</h2>
        
        <div style='margin-bottom: 40px;'>
            <p style='color: rgba(255,255,255,0.4); font-size: 10px; text-transform: uppercase; letter-spacing: 0.3em;'>Annual Reclamation Potential</p>
            <h3 style='font-size: 4rem; font-weight: 900; color: #ffffff; letter-spacing: -0.05em;'>${report['annual']:,.2f}</h3>
        </div>
        
        <p style='font-weight: 300; color: rgba(255,255,255,0.9); font-size: 1.25rem; line-height: 1.6; max-width: 750px; margin: 0 auto; padding: 20px; border-top: 1px solid rgba(255,255,255,0.1);'>
            "{report['insight']}"
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("INITIATE NEW DIAGNOSTIC"):
        st.session_state.last_report = None
        st.rerun()

st.markdown("<p style='text-align: center; color: rgba(255,255,255,0.05); font-size: 9px; margin-top: 60px; letter-spacing: 3px;'>ARMSTRONG LOGIC // v100T_SINGULARITY</p>", unsafe_allow_html=True)