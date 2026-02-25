import streamlit as st
import json
import os
import pandas as pd
from google import genai
from fpdf import FPDF
from datetime import datetime

# --- SOVEREIGN BRANDING & SHIELD THEME ---
st.set_page_config(page_title="Armstrong Logic | Command", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    /* Full Black-Out Aesthetic */
    .main { background-color: #000000; color: #00f2ff; font-family: 'Courier New', monospace; }
    
    /* Precision Input Styling */
    .stTextInput>div>div>input { 
        background-color: #0a0a0a; color: #00f2ff; border: 1px solid #00f2ff; border-radius: 0px; 
    }
    
    /* Pro Button Handshake */
    .stButton>button { 
        background-color: #00f2ff; color: #000; border-radius: 0px; width: 100%; 
        font-weight: bold; border: none; height: 3em; transition: 0.5s;
    }
    .stButton>button:hover { 
        background-color: #ffffff; color: #000; box-shadow: 0px 0px 25px #00f2ff; 
    }
    
    /* Futuristic Header */
    .sovereign-header {
        font-size: 2.2rem; font-weight: 900; color: #00f2ff; text-transform: uppercase;
        letter-spacing: 8px; text-shadow: 0px 0px 15px #00f2ff; text-align: center;
        border-bottom: 2px solid #00f2ff; margin-bottom: 40px; padding-bottom: 10px;
    }

    /* Additional UI Styles */
    .user-card { padding: 15px; border: 1px solid #333; margin-bottom: 10px; background: #0a0a0a; border-left: 4px solid #00f2ff; }
    
    @keyframes pulse { 
        0% { opacity: 1; } 
        50% { opacity: 0.3; } 
        100% { opacity: 1; } 
    }
    .loading-text { 
        color: #00f2ff; 
        font-weight: bold; 
        text-align: center; 
        animation: pulse 1.5s infinite; 
        letter-spacing: 5px; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- PDF GENERATION ENGINE (The Sentinel Report) ---
class SentinelReport(FPDF):
    def header(self):
        self.set_fill_color(0, 242, 255) # Cyan
        self.rect(0, 0, 210, 30, 'F')
        self.set_font('Helvetica', 'B', 18)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, 'ARMSTRONG LOGIC | SOVEREIGN AUDIT', 0, 1, 'C')
        self.set_font('Helvetica', 'I', 10)
        self.cell(0, 10, f'REGIONAL HUB: OTTAWA, IL | DATE: {datetime.now().strftime("%Y-%m-%d")}', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        user = st.session_state.current_user.upper() if "current_user" in st.session_state else "UNKNOWN"
        self.cell(0, 10, f'Sovereign Identification: {user} | Page {self.page_no()}', 0, 0, 'C')

def generate_pdf(report_text):
    pdf = SentinelReport()
    pdf.add_page()
    pdf.set_font("Helvetica", size=11)
    pdf.set_text_color(0, 0, 0)
    
    # --- Capital Reclamation Table ---
    pdf.set_font("Helvetica", 'B', 12)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(0, 10, "LEAKAGE RECLAMATION SUMMARY", 1, 1, 'C', 1)
    pdf.set_font("Helvetica", '', 10)
    pdf.cell(100, 10, "Target Leak Type", 1, 0, 'L')
    pdf.cell(90, 10, "Estimated Hourly Savings", 1, 1, 'R')
    
    # Hardcoded logic based on specific audit
    pdf.cell(100, 10, "Phantom Labor / Time Theft", 1, 0, 'L')
    pdf.cell(90, 10, "$120.00 / hr", 1, 1, 'R')
    pdf.cell(100, 10, "Static Schedule Inefficiency", 1, 0, 'L')
    pdf.cell(90, 10, "Variable ($40 - $120 / hr)", 1, 1, 'R')
    pdf.ln(10)
    
    # --- Audit Narrative ---
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 10, "PROPHET DIAGNOSTIC NARRATIVE", 0, 1, 'L')
    pdf.set_font("Helvetica", size=10)
    
    # Strip markdown bold for PDF and encode safely
    clean_text = str(report_text).replace('**', '')
    safe_text = clean_text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 7, safe_text)
    
    return pdf.output(dest='S').encode('latin-1') # Return bytes

# --- VAULT LOGIC ---
REGISTRY_PATH = "vault/registry.json"

def load_registry():
    if not os.path.exists("vault"): os.makedirs("vault")
    if not os.path.exists(REGISTRY_PATH):
        with open(REGISTRY_PATH, "w") as f: json.dump({"dlee": "master99"}, f)
    with open(REGISTRY_PATH, "r") as f: return json.load(f)

def save_registry(data):
    with open(REGISTRY_PATH, "w") as f: json.dump(data, f)

if "authenticated" not in st.session_state: st.session_state.authenticated = False
registry = load_registry()

# --- PROFESSIONAL LOGIN GATE ---
if not st.session_state.authenticated:
    st.markdown("<h1 class='sovereign-header'>🛡️ ARMSTRONG LOGIC</h1>", unsafe_allow_html=True)
    
    col_l, col_r = st.columns([1, 1])
    with col_l:
        st.write("### SYSTEM ACCESS")
        user_input = st.text_input("Username")
        pass_input = st.text_input("Password", type="password")
        
        if st.button("LOG IN"):
            if user_input in registry and registry[user_input] == pass_input:
                st.session_state.authenticated = True
                st.session_state.current_user = user_input
                st.rerun()
            else:
                st.error("Access Denied: Invalid Credentials.")
    st.stop()

# --- INTERNAL COMMAND CENTER ---
st.sidebar.title(f"🛡️ NODE: {st.session_state.current_user.upper()}")
st.sidebar.write(f"System: Armstrong Logic v3.1")
page = st.sidebar.radio("Navigation", ["Prophet Module", "User Registry", "Network Health"])

if st.sidebar.button("DISCONNECT NODE"):
    st.session_state.authenticated = False
    st.rerun()

# --- USER REGISTRY ---
if page == "User Registry":
    st.title("🛡️ SOVEREIGN USER REGISTRY")
    with st.expander("ENROLL NEW USER NODE"):
        new_user = st.text_input("New Username")
        new_pass = st.text_input("New Password", type="password")
        if st.button("FINALIZE ENROLLMENT"):
            if new_user and new_pass:
                registry[new_user] = new_pass
                save_registry(registry)
                st.success(f"Node '{new_user}' activated.")
                st.rerun()

    st.divider()
    for user in list(registry.keys()):
        col1, col2 = st.columns([4, 1])
        with col1: st.markdown(f"<div class='user-card'>NODE: <b>{user.upper()}</b></div>", unsafe_allow_html=True)
        with col2:
            if user != "dlee" and st.button(f"PURGE {user.upper()}", key=f"del_{user}"):
                del registry[user]
                save_registry(registry)
                st.rerun()

# --- PROPHET MODULE (With Updated PDF Logic) ---
elif page == "Prophet Module":
    st.title("⚡ ARMSTRONG LOGIC: PROPHET DIAGNOSTIC")
    st.write("Analyzing regional POS entropy and capital leakage.")
    
    uploaded_file = st.file_uploader("Upload Node Data (.csv)", type="csv")
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df, use_container_width=True)
        
        if st.button("EXECUTE PROPHET DIAGNOSTIC"):
            try:
                client = genai.Client(api_key=st.secrets["gemini_key"])
                
                loading_placeholder = st.empty()
                loading_placeholder.markdown("<p class='loading-text'>ARMSTRONGLOGIC ANALYZING...</p>", unsafe_allow_html=True)
                
                data_summary = df.to_string()
                response = client.models.generate_content(
                    model="gemini-3.1-pro-preview", 
                    contents=f"You are the Armstrong Logic Profit Prophet. Focus solely on analyzing this POS data to uncover labor leaks, fraud, or inefficiencies. Provide a highly tactical, concise executive summary with direct actionable steps. Keep the tone authoritative, metallic, and absolute (100 trillion years ahead). Data: {data_summary}"
                )
                
                loading_placeholder.empty()
                st.session_state.last_report = response.text
                st.markdown("### 🛡️ ARMSTRONG LOGIC EXECUTIVE REPORT")
                st.write(st.session_state.last_report)
                
                # Manifest the PDF artifact using the new function
                pdf_output = generate_pdf(st.session_state.last_report)
                
                # Use bytes() to ensure Streamlit accepts it cleanly
                st.download_button(
                    label="🛡️ DOWNLOAD OFFICIAL SENTINEL REPORT",
                    data=bytes(pdf_output),
                    file_name=f"Armstrong_Logic_Audit_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf"
                )
                
            except Exception as e:
                st.error(f"SYSTEM ERROR: {e}")

# --- NETWORK HEALTH ---
elif page == "Network Health":
    st.title("📟 NETWORK HEALTH")
    st.metric(label="Active Regional Nodes", value=len(registry))
    st.metric(label="Prophet Sync", value="STABLE")
    st.info("Ottawa, IL Hub: Primary Node Active")
