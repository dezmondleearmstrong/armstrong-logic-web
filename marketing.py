import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google import genai

# --- SOVEREIGN BRANDING ---
st.set_page_config(page_title="Armstrong Logic | Profit Watchdog", page_icon="🔱", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #050505; color: #00f2ff; font-family: 'Courier New', monospace; }
    .stNumberInput>div>div>input, .stTextInput>div>div>input { background-color: #111; color: #00f2ff; border: 1px solid #00f2ff; }
    .stButton>button { background-color: #00f2ff; color: black; border-radius: 0px; width: 100%; font-weight: bold; border: none; }
    .metric-box { padding: 20px; border: 1px solid #00f2ff; background: #0a0a0a; text-align: center; margin-bottom: 10px; }
    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }
    .loading-text { color: #00f2ff; font-weight: bold; text-align: center; animation: pulse 1.5s infinite; letter-spacing: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- EMAIL SENTINEL FUNCTION ---
def send_recovery_email(target_email, restaurant_name, est_leakage, prophet_insight):
    try:
        msg = MIMEMultipart()
        msg['From'] = st.secrets["my_email"]
        msg['To'] = target_email
        msg['Subject'] = f"🔱 CAPITAL RECOVERY REPORT: {restaurant_name.upper()}"

        body = f"""
        ARMSTRONG LOGIC | SOVEREIGN AUDIT
        ---------------------------------
        RESTAURANT: {restaurant_name}
        IDENTIFIED MONTHLY LEAKAGE: ${est_leakage:,.2f}
        
        PROPHET DIAGNOSTIC:
        {prophet_insight}
        
        This report was generated via the Armstrong Logic Watchdog Node. 
        To finalize your capital reclamation, reply to this email to schedule a node-level audit.
        
        SYSTEM STATUS: OPTIMAL
        """
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(st.secrets["my_email"], st.secrets["gmail_pass"])
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Email Error: {e}") # Log to console for debugging
        return False

# --- UI INTERFACE ---
st.title("🔱 ARMSTRONG LOGIC")
st.subheader("PROFIT WATCHDOG: INSTANT RECOVERY CALCULATOR")

col_in1, col_in2 = st.columns(2)
with col_in1:
    res_name = st.text_input("Restaurant Name")
    res_email = st.text_input("Decision Maker Email")
with col_in2:
    m_sales = st.number_input("Monthly Sales ($)", min_value=0, value=50000)
    m_labor = st.number_input("Monthly Labor ($)", min_value=0, value=15000)

if st.button("EXECUTE WATCHDOG ANALYSIS"):
    if not res_name or not res_email:
        st.warning("Cipher required: Please enter Restaurant Name and Email.")
    else:
        # Diagnostic Logic
        leak = (m_sales * 0.06) + (m_labor * 0.12) # Aggressive estimation
        
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.markdown(f"<div class='metric-box'><h3>MONTHLY LEAK</h3><h1 style='color: #ff4b4b;'>${leak:,.2f}</h1></div>", unsafe_allow_html=True)
        with col_res2:
            st.markdown(f"<div class='metric-box'><h3>ANNUAL RECOVERY</h3><h1 style='color: #00f2ff;'>${leak*12:,.2f}</h1></div>", unsafe_allow_html=True)

        placeholder = st.empty()
        placeholder.markdown("<p class='loading-text'>ARMSTRONGLOGIC ANALYZING...</p>", unsafe_allow_html=True)
        
        # Prophet Insight
        client = genai.Client(api_key=st.secrets["gemini_key"])
        response = client.models.generate_content(
            model="gemini-3.1-pro-preview",
            contents=f"Explain in 2 authoritative sentences why losing ${leak:,.2f} a month at {res_name} is a systemic failure of POS oversight and how Armstrong Logic stops it."
        )
        insight = response.text
        placeholder.empty()
        
        st.write(f"### 🔱 PROPHET INSIGHT: {res_name.upper()}")
        st.write(insight)

        # Fire Sentinel Email
        if send_recovery_email(res_email, res_name, leak, insight):
            st.success(f"🔱 Full recovery audit transmitted to {res_email}.")
        else:
            st.error("Sentinel Error: Handshake with email server failed.")

st.divider()
st.caption("SYSTEM STATUS: OPTIMAL // ARCHITECTURE: SOVEREIGN")
