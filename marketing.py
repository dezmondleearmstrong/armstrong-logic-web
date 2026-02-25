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

# FIXED CSS: Forces label visibility and eliminates container gaps
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
        color: #ffffff !important; /* Force labels to be white */
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
        margin-bottom: -10px !important; /* Pull the box up to the label */
    }

    /* THE FIX: Remove the 'Black Space' Gap */
    div[data-testid="stVerticalBlock"] > div {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
    }

    /* Input Field Styling */
    .stNumberInput input, .stTextInput input {
        background-color: rgba(255, 255, 255, 0.07) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        color: #ffffff !important; /* White text when typing */
        padding: 15px !important;
        font-size: 1.1rem !important;
    }

    /* Main Surface Container */
    .main-surface {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(50px) saturate(180%);
        -webkit-backdrop-filter: blur(50px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 40px;
        padding: 40px;
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
        font-weight: 700 !important;
        width: 100%;
        margin-top: 20px;
        transition: 0.4s ease;
    }
    
    .stButton>button:hover {
        transform: scale(1.01);
        box-shadow: 0 0 50px rgba(255,255,255,0.2);
    }

    .sovereign-header { text-align: center; margin-bottom: 30px; }
    .sovereign-header h1 { font-weight: 200; font-size: 3rem; color: #ffffff; }
    .sovereign-header p { color: rgba(255, 255, 255, 0.4); letter-spacing: 0.4em; text-transform: uppercase; font-size: 10px; }
    
    /* Success Message Fix */
    .stSuccess {
        background-color: rgba(138, 43, 226, 0.1) !important;
        color: #ffffff !important;
        border: 1px solid rgba(138, 43, 226, 0.3) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIC DEPLOYMENT ---
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
        res_name = st.text_input("ENTITY NAME", placeholder="Establishment name")
        res_email = st.text_input("EMAIL", placeholder="Direct email")
    with col2:
        m_sales = st.number_input("MONTHLY SALES ($)", min_value=0, value=75000)
        m_labor = st.number_input("MONTHLY LABOR ($)", min_value=0, value=22000)

    if st.button("EXECUTE ARMSTRONG DIAGNOSTIC"):
        if not res_name or not res_email:
            st.error("Handshake failed: Identity required.")
        else:
            leak = (m_sales * 0.08) + (m_labor * 0.12)
            with st.spinner("ARMSTRONGLOGIC ANALYZING..."):
                client = genai.Client(api_key=st.secrets["gemini_key"])
                response = client.models.generate_content(
                    model="gemini-3.1-pro-preview", 
                    contents=f"Analyze {res_name}: ${m_sales} sales, ${m_labor} labor. Monthly leak: ${leak}. Provide 2 cold, authoritative sentences on revenue recovery."
                )
                
                st.session_state.last_report = {
                    "name": res_name.upper(),
                    "leak": leak,
                    "annual": leak * 12,
                    "insight": response.text,
                    "email": res_email
                }
                st.session_state.usage_count += 1
                st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# --- SUCCESS & REPORT DISPLAY ---
if st.session_state.last_report:
    report = st.session_state.last_report
    st.success(f"🛡️ArmstrongLogic sent a report to {report['email']}.")
    
    st.markdown(f"""
    <div style="background: rgba(138, 43, 226, 0.05); border: 1px solid rgba(138, 43, 226, 0.2); border-radius: 30px; padding: 40px; text-align: center;">
        <h2 style='font-weight: 200; font-size: 2.5rem;'>{report['name']}</h2>
        <h3 style='font-size: 3rem; font-weight: 800; color: #ffffff;'>Annual Reclamation: ${report['annual']:,.2f}</h3>
        <p style='font-weight: 300; color: rgba(255,255,255,0.7);'>"{report['insight']}"</p>
    </div>
    """, unsafe_allow_html=True)
