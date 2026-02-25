import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google import genai
from datetime import datetime

# --- SOVEREIGN BRANDING & CORE DESIGN ---
st.set_page_config(page_title="ArmstrongLogic | Calculator", page_icon="🛡️", layout="wide")

# Persistent State
if "usage_count" not in st.session_state: st.session_state.usage_count = 0
if "last_report" not in st.session_state: st.session_state.last_report = None

# CSS Fix: Visibility and Brutalist Spacing
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap');
    .stApp { background-color: #050505; font-family: 'Inter', sans-serif; }

    /* Force Label Visibility */
    div[data-testid="stWidgetLabel"] p {
        color: #ffffff !important;
        font-size: 0.85rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.15em !important;
    }

    .stNumberInput input, .stTextInput input {
        background-color: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        padding: 15px !important;
    }

    .main-surface {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(50px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 40px;
        padding: 40px;
        box-shadow: 0 40px 120px rgba(0,0,0,0.6);
    }

    .stButton>button {
        background: #ffffff !important;
        color: #000 !important;
        border-radius: 50px !important;
        font-weight: 800 !important;
        padding: 20px !important;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- THE SOVEREIGN EMAIL ENGINE ---
def send_sovereign_report(client_email, biz_name, leak, annual, prophet_text):
    try:
        my_email = st.secrets["my_email"]
        password = st.secrets["gmail_pass"]
        report_body = f"🛡️ ARMSTRONGLOGIC AUDIT\nENTITY: {biz_name.upper()}\n\nRECOVERY DATA:\nMonthly Leakage: ${leak:,.2f}\nAnnual Reclamation: ${annual:,.2f}\n\nCOMMANDER'S INSIGHT:\n{prophet_text}"
        
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(my_email, password)
            for recipient in [client_email, my_email]:
                msg = MIMEMultipart()
                msg['From'] = f"ArmstrongLogic <{my_email}>"
                msg['To'] = recipient
                msg['Subject'] = f"🛡️ SOVEREIGN RECOVERY: {biz_name.upper()}"
                msg.attach(MIMEText(report_body, 'plain'))
                server.send_message(msg)
        return True
    except: return False

# --- UI INTERFACE ---
st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <p style="color: rgba(255,255,255,0.3); letter-spacing: 0.5em; text-transform: uppercase; font-size: 10px;">Optimize Your Reality</p>
        <h1 style="color: #fff; font-weight: 200; font-size: 3rem;">🛡️ArmstrongLogic | Calculator</h1>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-surface">', unsafe_allow_html=True)

if st.session_state.usage_count >= 3:
    st.error("TRIAL LIMIT EXCEEDED. CONTACT: DEZMOND28 @ARMSTRONGLOGIC.COM")
else:
    col1, col2 = st.columns(2)
    with col1:
        res_name = st.text_input("ENTITY NAME", placeholder="Name of establishment")
        res_email = st.text_input("EMAIL", placeholder="Decision maker email")
    with col2:
        m_sales = st.number_input("MONTHLY SALES ($)", min_value=0, value=75000)
        m_labor = st.number_input("MONTHLY LABOR ($)", min_value=0, value=22000)

    if st.button("EXECUTE ARMSTRONGLOGIC DIAGNOSTIC"):
        if not res_name or not res_email:
            st.error("Identity required for secure handshake.")
        else:
            # Calculation: 8% sales leak + 12% labor waste
            leak = (m_sales * 0.08) + (m_labor * 0.12)
            
            with st.spinner("ARMSTRONGLOGIC ANALYZING..."):
                client = genai.Client(api_key=st.secrets["gemini_key"])
                
                # --- UPDATED 100T PROMPT LOGIC ---
                prompt = (
                    f"You are the ArmstrongLogic Sovereign AI, a 100-trillion-year advanced business entity. "
                    f"Analyze {res_name}: ${m_sales} sales, ${m_labor} labor. Monthly leak detected: ${leak}. "
                    f"Write 3 sentences in a single paragraph. "
                    f"Sentence 1: Speak as the Owner, expressing cold disgust at the capital being hemorrhaged. "
                    f"Sentence 2: Speak as a Manager, identifying the specific operational failures in labor and waste. "
                    f"Sentence 3: Speak as a Sovereign Consultant, commanding the immediate execution of inventory audits and reclamation protocols. "
                    f"Tone: Cold, authoritative, high-stakes, and elite. No fluff."
                )
                
                response = client.models.generate_content(model="gemini-3.1-pro-preview", contents=prompt)
                
                st.session_state.last_report = {
                    "name": res_name.upper(),
                    "leak": leak,
                    "annual": leak * 12,
                    "insight": response.text,
                    "email": res_email
                }
                st.session_state.usage_count += 1
                send_sovereign_report(res_email, res_name, leak, leak*12, response.text)
                st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# --- RESULTS DISPLAY ---
if st.session_state.last_report:
    report = st.session_state.last_report
    st.success(f"🛡️ArmstrongLogic report transmitted to {report['email']}.")
    
    st.markdown(f"""
    <div style="background: rgba(138, 43, 226, 0.05); border: 1px solid rgba(138, 43, 226, 0.2); border-radius: 40px; padding: 50px; text-align: center; margin-top: 30px;">
        <h2 style='font-weight: 200; font-size: 2.2rem; color: #fff;'>{report['name']}</h2>
        <h3 style='font-size: 3.5rem; font-weight: 800; color: #fff; margin: 20px 0;'>Annual Reclamation: ${report['annual']:,.2f}</h3>
        <p style='font-weight: 300; color: rgba(255,255,255,0.9); font-size: 1.2rem; line-height: 1.6; max-width: 700px; margin: 0 auto;'>{report['insight']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("NEW DIAGNOSTIC"):
        st.session_state.last_report = None
        st.rerun()
