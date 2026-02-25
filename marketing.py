import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google import genai
from datetime import datetime

# --- SOVEREIGN BRANDING & CORE DESIGN ---
st.set_page_config(page_title="ArmstrongLogic | Calculator", page_icon="🛡️", layout="wide")

# Persistent State Logic
if "usage_count" not in st.session_state: st.session_state.usage_count = 0
if "last_report" not in st.session_state: st.session_state.last_report = None

# Custom CSS: Radical Minimalism (The Industrial "Sense" Aesthetic)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght @0,14..32,100..900;1,14..32,100..900&display=swap');

    .stApp { background-color: #050505; font-family: 'Inter', sans-serif; }

    /* Glassmorphism Surface */
    .main-surface {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(50px) saturate(180%);
        -webkit-backdrop-filter: blur(50px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 40px;
        padding: 60px;
        box-shadow: 0 40px 120px rgba(0,0,0,0.6);
        color: #ffffff;
        margin-bottom: 40px;
    }

    /* Minimalist Inputs */
    .stNumberInput input, .stTextInput input {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: #fff !important;
        padding: 12px !important;
    }

    /* Sovereign Button */
    .stButton>button {
        background: #ffffff !important;
        color: #000000 !important;
        border-radius: 50px !important;
        border: none !important;
        padding: 15px 40px !important;
        font-weight: 600 !important;
        letter-spacing: -0.02em !important;
        transition: 0.5s cubic-bezier(0.2, 0, 0.2, 1) !important;
        height: auto !important;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 40px rgba(255,255,255,0.2);
    }

    .sovereign-header { text-align: center; margin-bottom: 50px; }
    .sovereign-header h1 { font-weight: 200; letter-spacing: -0.05em; font-size: 3.5rem; color: #ffffff; }
    .sovereign-header p { color: rgba(255, 255, 255, 0.2); letter-spacing: 0.4em; text-transform: uppercase; font-size: 10px; font-weight: 800; }

    .report-box {
        background: rgba(138, 43, 226, 0.04);
        border: 1px solid rgba(138, 43, 226, 0.15);
        border-radius: 40px;
        padding: 50px;
        margin-top: 40px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DUAL-SENTINEL EMAIL ---
def send_dual_reports(client_email, biz_name, leak_amt, annual_amt, prophet_text):
    try:
        my_email = st.secrets["my_email"]
        password = st.secrets["gmail_pass"]
        report_body = f"🛡️ ARMSTRONGLOGIC AUDIT\nENTITY: {biz_name.upper()}\nMONTHLY LEAKAGE: ${leak_amt:,.2f}\nANNUAL RECLAMATION: ${annual_amt:,.2f}\n\nPROPHET INSIGHT:\n{prophet_text}"
        
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(my_email, password)
            for recipient in [client_email, my_email]:
                msg = MIMEMultipart()
                msg['From'] = f"ArmstrongLogic <{my_email}>"
                msg['To'] = recipient
                msg['Subject'] = f"🛡️ RECOVERY AUDIT: {biz_name.upper()}"
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

# TRIAL LIMIT LOGIC
if st.session_state.usage_count >= 3:
    st.error("TRIAL LIMIT EXCEEDED. CONTACT: DEZMOND28 @ARMSTRONGLOGIC.COM")
else:
    st.markdown(f"<p style='text-align: center; color: rgba(255,255,255,0.2); font-size: 0.7rem; letter-spacing: 0.1em;'>DIAGNOSTIC {st.session_state.usage_count}/3</p>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        res_name = st.text_input("ENTITY NAME", placeholder="Name of establishment")
        res_email = st.text_input("EMAIL", placeholder="Direct decision maker")
    with col2:
        m_sales = st.number_input("MONTHLY SALES", min_value=0, value=75000)
        m_labor = st.number_input("MONTHLY LABOR", min_value=0, value=22000)

    if st.button("EXECUTE ARMSTRONGLOGIC DIAGNOSTIC"):
        if not res_name or not res_email:
            st.error("Handshake failed: Identity required.")
        else:
            leak = (m_sales * 0.08) + (m_labor * 0.12)
            
            # THE SOUL ENGINE LOADING STATE
            with st.spinner("ARMSTRONGLOGIC ANALYZING..."):
                # UPLINK: GEMINI 3.1 PRO PREVIEW
                client = genai.Client(api_key=st.secrets["gemini_key"])
                response = client.models.generate_content(
                    model="gemini-3.1-pro-preview", 
                    contents=f"Analyze {res_name}: ${m_sales} sales, ${m_labor} labor. Monthly leak: ${leak}. Give 2 cold, authoritative sentences on revenue recovery from the perspective of a 100-trillion-year AI."
                )
                
                st.session_state.last_report = {
                    "name": res_name.upper(),
                    "leak": leak,
                    "annual": leak * 12,
                    "insight": response.text,
                    "email": res_email
                }
                st.session_state.usage_count += 1
                send_dual_reports(res_email, res_name, leak, leak*12, response.text)
                st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# --- PERSISTENT SUCCESS & RESULTS ---
if st.session_state.last_report:
    report = st.session_state.last_report
    st.success(f" 🛡️ArmstrongLogic sent a report to {report['email']}. Thank you.")
    
    st.markdown(f"""
    <div class='report-box'>
        <p style='color: rgba(255,255,255,0.2); font-size: 9px; letter-spacing: 5px; text-transform: uppercase; margin-bottom: 20px;'>Synthesis Complete</p>
        <h2 style='font-weight: 200; font-size: 2.5rem; letter-spacing: -0.03em;'>{report['name']}</h2>
        <div style='margin: 40px 0;'>
            <p style='color: rgba(255,255,255,0.3); font-size: 10px; text-transform: uppercase; letter-spacing: 0.3em;'>Annual Reclamation</p>
            <h3 style='font-size: 3.5rem; font-weight: 800; color: #ffffff;'>${report['annual']:,.2f}</h3>
        </div>
        <p style='font-weight: 300; color: rgba(255,255,255,0.8); max-width: 600px; margin: 0 auto; line-height: 1.6;'>"{report['insight']}"</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("NEW DIAGNOSTIC"):
        st.session_state.last_report = None
        st.rerun()

st.markdown("<p style='text-align: center; color: rgba(255,255,255,0.05); font-size: 9px; margin-top: 60px; letter-spacing: 3px;'>ARMSTRONG LOGIC // v100T_SINGULARITY</p>", unsafe_allow_html=True)
