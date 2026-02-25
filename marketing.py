import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google import genai
from datetime import datetime

# --- BRANDING & PERSISTENCE ---
st.set_page_config(page_title="ArmstrongLogic | Calculator", page_icon="🛡️", layout="wide")

if "usage_count" not in st.session_state: st.session_state.usage_count = 0
if "last_report" not in st.session_state: st.session_state.last_report = None

st.markdown("""
    <style>
    .main { background-color: #000000; color: #00f2ff; font-family: 'Courier New', monospace; }
    
    /* Flex-Column Sovereign Stack */
    .sovereign-stack {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        border-bottom: 2px solid #00f2ff;
        margin-bottom: 30px;
        padding-bottom: 20px;
    }
    .stack-shield {
        font-size: 5vw;
        margin-bottom: -1vw; /* pull text closer */
        text-shadow: 0px 0px 15px #00f2ff;
    }
    .stack-word {
        font-weight: 900;
        color: #00f2ff;
        text-transform: uppercase;
        text-shadow: 0px 0px 15px #00f2ff;
        line-height: 0.85; /* Tight vertical stacking */
        margin: 0;
        padding: 0;
    }
    .word-armstrong { font-size: 8vw; letter-spacing: 0.8vw; margin-left: 0.8vw; }
    .word-logic { font-size: 8vw; letter-spacing: 2.2vw; margin-left: 2.2vw; }
    .word-calculator { font-size: 3.5vw; letter-spacing: 1.5vw; margin-left: 1.5vw; margin-top: 10px; color: #ffffff; text-shadow: 0px 0px 10px #ffffff; }

    .stNumberInput>div>div>input, .stTextInput>div>div>input { background-color: #0a0a0a; color: #00f2ff; border: 1px solid #00f2ff; border-radius: 0px; }
    .stButton>button { background-color: #00f2ff; color: #000; border-radius: 0px; width: 100%; font-weight: bold; border: none; height: 3.5em; transition: 0.5s; }
    .stButton>button:hover { background-color: #ffffff; box-shadow: 0px 0px 30px #00f2ff; }
    .report-box { padding: 40px; border: 1px solid #00f2ff; background: #050505; box-shadow: inset 0px 0px 20px #00f2ff; margin-top: 25px; }
    
    /* Corrected pulse keyframes for web */
    @keyframes pulse { 
        0% { opacity: 1; } 
        50% { opacity: 0.1; } 
        100% { opacity: 1; } 
    }
    .loading-text { color: #00f2ff; font-weight: bold; text-align: center; animation: pulse 0.8s infinite; letter-spacing: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- DUAL-SENTINEL EMAIL ---
def send_dual_reports(client_email, biz_name, leak_amt, annual_amt, prophet_text):
    try:
        my_email = st.secrets["my_email"]
        password = st.secrets["gmail_pass"]
        report_body = f"🛡️ ARMSTRONGLOGIC SOVEREIGN AUDIT\nENTITY: {biz_name.upper()}\nMONTHLY LEAKAGE: ${leak_amt:,.2f}\nANNUAL RECLAMATION: ${annual_amt:,.2f}\n\nPROPHET INSIGHT:\n{prophet_text}"
        
        # Combined sending logic to reduce server handshakes
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(my_email, password)
            for recipient in [client_email, my_email]:
                msg = MIMEMultipart()
                msg['From'] = my_email
                msg['To'] = recipient
                msg['Subject'] = f"🛡️ RECOVERY AUDIT: {biz_name.upper()}"
                msg.attach(MIMEText(report_body, 'plain'))
                server.send_message(msg)
        return True
    except Exception as e:
        print(f"SMTP Error: {e}")
        return False

# --- UI INTERFACE ---
st.markdown("""
<div class='sovereign-stack'>
    <div class='stack-shield'>🛡️</div>
    <div class='stack-word word-armstrong'>ARMSTRONG</div>
    <div class='stack-word word-logic'>LOGIC</div>
    <div class='stack-word word-calculator'>CALCULATOR</div>
</div>
""", unsafe_allow_html=True)

if st.session_state.usage_count >= 3:
    st.error("TRIAL LIMIT EXCEEDED. CONTACT: DEZMOND28 @ARMSTRONGLOGIC.COM")
else:
    st.write(f"<p style='text-align: center; color: #00f2ff;'>DIAGNOSTIC LIMIT: {st.session_state.usage_count}/3</p>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        res_name = st.text_input("RESTAURANT NAME")
        res_email = st.text_input("DECISION MAKER EMAIL")
    with col2:
        m_sales = st.number_input("MONTHLY SALES ($)", min_value=0, value=75000)
        m_labor = st.number_input("MONTHLY LABOR ($)", min_value=0, value=22000)

    if st.button("EXECUTE SHIELD DIAGNOSTIC"):
        if not res_name or not res_email:
            st.error("HANDSHAKE FAILED: Identity required.")
        else:
            leak = (m_sales * 0.08) + (m_labor * 0.12)
            
            placeholder = st.empty()
            placeholder.markdown("<p class='loading-text'>ARMSTRONGLOGIC ANALYZING...</p>", unsafe_allow_html=True)
            
            # Gemini Call
            client = genai.Client(api_key=st.secrets["gemini_key"])
            response = client.models.generate_content(
                model="gemini-3.1-pro-preview",
                contents=f"Analyze {res_name}: ${m_sales} sales, ${m_labor} labor. Monthly leak: ${leak}. Provide 2 authoritative sentences on recovery."
            )
            
            # STORE DATA BEFORE EMAIL
            st.session_state.last_report = {
                "name": res_name.upper(),
                "leak": leak,
                "annual": leak * 12,
                "insight": response.text,
                "email": res_email
            }
            st.session_state.usage_count += 1
            
            # TRIGGER EMAIL (With speed optimization)
            send_dual_reports(res_email, res_name, leak, leak*12, response.text)
            
            placeholder.empty()
            st.rerun()

# --- 🔱 PERSISTENT DISPLAY & SUCCESS MESSAGE ---
if st.session_state.last_report:
    report = st.session_state.last_report
    st.success(f"🛡️ ArmstrongLogic sent a report to {report['email']}. Thank you.")
    
    st.markdown(f"""
    <div class='report-box'>
        <h2 style='color: #00f2ff; text-align: center;'>🛡️ OFFICIAL RECOVERY REPORT</h2>
        <p><b>ENTITY:</b> {report['name']}</p>
        <p style='color: #ff4b4b; font-size: 1.8rem;'><b>MONTHLY LEAKAGE:</b> ${report['leak']:,.2f}</p>
        <p style='color: #00f2ff; font-size: 1.8rem;'><b>ANNUAL RECLAMATION:</b> ${report['annual']:,.2f}</p>
        <p><b>PROPHET INSIGHT:</b><br>{report['insight']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("NEW DIAGNOSTIC"):
        st.session_state.last_report = None
        st.rerun()

st.divider()
st.caption("SYSTEM STATUS: SECURED // ARCHITECTURE: Dezmond Armstrong")
