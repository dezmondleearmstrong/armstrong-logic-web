import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google import genai
import uuid

# --- SOVEREIGN CONFIG ---
st.set_page_config(page_title="ArmstrongLogic Engine", layout="wide")

if "usage_count" not in st.session_state: st.session_state.usage_count = 0
if "last_report" not in st.session_state: st.session_state.last_report = None

# CLEAN CSS: No gaps, high visibility, no headers
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    
    /* Hide Streamlit elements for "Chatbot" feel */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: transparent; font-family: 'Inter', sans-serif; }
    
    /* Input Visibility Fixes */
    div[data-testid="stWidgetLabel"] p {
        color: rgba(255, 255, 255, 0.7) !important;
        font-size: 0.75rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.2em !important;
    }

    .stNumberInput input, .stTextInput input {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }

    /* Sovereign Button */
    .stButton>button {
        background: #ffffff !important;
        color: #000 !important;
        border-radius: 50px !important;
        font-weight: 700 !important;
        width: 100%;
        border: none !important;
    }
    
    /* Result Box */
    .result-card {
        background: rgba(138, 43, 226, 0.05);
        border: 1px solid rgba(138, 43, 226, 0.2);
        border-radius: 30px;
        padding: 30px;
        text-align: center;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- EMAIL ENGINE ---
def send_report(client_email, biz_name, leak, annual, prophet_text, audit_id):
    try:
        my_email = st.secrets["my_email"]
        password = st.secrets["gmail_pass"]
        body = f"🛡️ ARMSTRONGLOGIC AUDIT: {audit_id}\nENTITY: {biz_name}\nANNUAL RECLAMATION: ${annual:,.2f}\n\nINSIGHT: {prophet_text}"
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(my_email, password)
            msg = MIMEMultipart(); msg['From'] = my_email; msg['To'] = client_email
            msg['Subject'] = f"🛡️ Audit: {biz_name}"; msg.attach(MIMEText(body, 'plain'))
            server.send_message(msg)
        return True
    except: return False

# --- APP LOGIC ---
if st.session_state.usage_count >= 3:
    st.error("LIMIT REACHED. CONTACT: DEZMOND28 @ARMSTRONGLOGIC.COM")
else:
    col1, col2 = st.columns(2)
    with col1:
        res_name = st.text_input("ENTITY NAME")
        res_email = st.text_input("EMAIL")
    with col2:
        m_sales = st.number_input("MONTHLY SALES", value=0)
        m_labor = st.number_input("MONTHLY LABOR", value=0)

    if st.button("EXECUTE DIAGNOSTIC"):
        if res_name and res_email:
            leak = (m_sales * 0.08) + (m_labor * 0.12)
            audit_id = str(uuid.uuid4())[:8].upper()
            client = genai.Client(api_key=st.secrets["gemini_key"])
            
            prompt = (f"As ArmstrongLogic AI, analyze {res_name}: ${m_sales} sales, ${m_labor} labor. "
                      f"Monthly leak: ${leak}. Write a professional, high-level paragraph explaining why only "
                      f"ArmstrongLogic can solve this invisible entropy. Tone: Elite/Professional.")
            
            response = client.models.generate_content(model="gemini-3.1-pro-preview", contents=prompt)
            
            st.session_state.last_report = {
                "name": res_name, "annual": leak * 12, 
                "insight": response.text, "id": audit_id
            }
            st.session_state.usage_count += 1
            send_report(res_email, res_name, leak, leak*12, response.text, audit_id)
            st.rerun()

if st.session_state.last_report:
    r = st.session_state.last_report
    st.markdown(f"""
        <div class="result-card">
            <p style="color:rgba(255,255,255,0.3); font-size:10px;">AUDIT {r['id']}</p>
            <h2 style="color:#fff; font-weight:200;">{r['name']}</h2>
            <h1 style="color:#fff; font-size:3rem;">${r['annual']:,.2f}</h1>
            <p style="color:rgba(255,255,255,0.8); font-weight:300;">"{r['insight']}"</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("NEW AUDIT"):
        st.session_state.last_report = None
        st.rerun()
