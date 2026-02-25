import streamlit as st
import json
import os
import pandas as pd
from google import genai
from fpdf import FPDF
from datetime import datetime

# --- SOVEREIGN BRANDING & THEME ---
st.set_page_config(page_title="Armstrong Logic | Sovereign Command", page_icon="🔱", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #050505; color: #00f2ff; font-family: 'Courier New', monospace; }
    .stTextInput>div>div>input { background-color: #111; color: #00f2ff; border: 1px solid #00f2ff; }
    .stButton>button { background-color: #00f2ff; color: black; border-radius: 0px; width: 100%; font-weight: bold; border: none; transition: 0.3s; }
    .stButton>button:hover { background-color: #0088ff; color: white; transform: scale(1.02); }
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
        self.set_font('Arial', 'B', 18)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, 'ARMSTRONG LOGIC | SOVEREIGN AUDIT', 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 10, f'REGIONAL HUB: OTTAWA, IL | DATE: {datetime.now().strftime("%Y-%m-%d")}', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        user = st.session_state.current_user.upper() if "current_user" in st.session_state else "UNKNOWN"
        self.cell(0, 10, f'Sovereign Identification: {user} | Page {self.page_no()}', 0, 0, 'C')

def generate_pdf(report_text):
    pdf = SentinelReport()
    pdf.add_page()
    
    # --- Tactical Reclamation Table ---
    pdf.set_font("Arial", 'B', 12)
    pdf.set_fill_color(0, 242, 255) # Cyan Header
    pdf.cell(0, 10, "CAPITAL RECLAMATION SUMMARY", 1, 1, 'C', 1)
    
    pdf.set_font("Arial", 'B', 10)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(100, 10, "Leakage Vector", 1, 0, 'L', 1)
    pdf.cell(90, 10, "Potential Recovery", 1, 1, 'R', 1)
    
    pdf.set_font("Arial", '', 10)
    # Pulling specific numbers for the B.A.S.H. / Ottawa demo
    pdf.cell(100, 10, "Employee Void Fraud (Emp_04)", 1, 0, 'L')
    pdf.cell(90, 10, "$90.00 (Identified)", 1, 1, 'R')
    pdf.cell(100, 10, "Alcohol Inventory Variance (Emp_09)", 1, 0, 'L')
    pdf.cell(90, 10, "Audit Required", 1, 1, 'R')
    pdf.ln(10)
    
    # --- Narrative Summary ---
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "EXECUTIVE DIAGNOSTIC NARRATIVE", 0, 1, 'L')
    pdf.set_font("Arial", size=10)
    
    # THE FIX: Convert to string, remove MD bolding, and avoid .encode() on bytearrays
    clean_text = str(report_text).replace('**', '').replace('$', '\$')
    pdf.multi_cell(0, 7, clean_text)
    
    # Return raw bytes directly
    return pdf.output() 

# --- REGISTRY LOGIC (The Vault) ---
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

# --- LOGIN GATE ---
if not st.session_state.authenticated:
    st.title("🔱 ARMSTRONG LOGIC | SOVEREIGN ID GATE")
    st.write("SYSTEM STATUS: ENCRYPTED // REGIONAL HUB: OTTAWA")
    
    col_l, col_r = st.columns(2)
    with col_l:
        user_input = st.text_input("User Cipher")
        pass_input = st.text_input("Access Key", type="password")
        if st.button("INITIATE HANDSHAKE"):
            if user_input in registry and registry[user_input] == pass_input:
                st.session_state.authenticated = True
                st.session_state.current_user = user_input
                st.rerun()
            else:
                st.error("HANDSHAKE FAILED: INVALID CIPHER")
    st.stop()

# --- SIDEBAR CONTROL ---
st.sidebar.title(f"🔱 NODE: {st.session_state.current_user.upper()}")
st.sidebar.write(f"System: Armstrong Logic v3.1")
page = st.sidebar.radio("Navigation", ["Prophet Module", "User Registry", "Network Health"])

if st.sidebar.button("DISCONNECT NODE"):
    st.session_state.authenticated = False
    st.rerun()

# --- USER REGISTRY ---
if page == "User Registry":
    st.title("🛡️ SOVEREIGN USER REGISTRY")
    with st.expander("ENROLL NEW USER NODE"):
        new_user = st.text_input("New Username (Cipher)")
        new_pass = st.text_input("New Password (Access Key)", type="password")
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
                
                # 🔱 Prompt Engineering: Human Business Logic
                prompt = f"""
                You are the Armstrong Logic Profit Prophet. 
                Analyze this POS data for an owner who needs clear, professional, and firm advice.
                1. Use an authoritative but professional tone (The "Sovereign" voice).
                2. Explain the FRAUD in plain English (e.g., 'Employee theft via voids').
                3. Provide the 'Human Logic' behind the math so the owner knows exactly what to do next.
                4. Keep it concise. Focus on the $90 loss and the void pattern.

                Data: {df.to_string()}
                """
                
                response = client.models.generate_content(
                    model="gemini-3.1-pro-preview", 
                    contents=prompt
                )
                
                loading_placeholder.empty()
                st.session_state.last_report = response.text
                st.markdown("### 🔱 ARMSTRONG LOGIC EXECUTIVE REPORT")
                st.write(st.session_state.last_report)
                
                # Manifest the PDF artifact
                pdf_bytes = generate_pdf(st.session_state.last_report)
                
                # Ensure 'data' is the raw bytes from the pdf_bytes
                st.download_button(
                    label="🔱 DOWNLOAD OFFICIAL SENTINEL REPORT",
                    data=bytes(pdf_bytes), # Final fix for the 'bytearray' error
                    file_name=f"Armstrong_Logic_Audit.pdf",
                    mime="application/pdf"
                )
                
            except Exception as e:
                st.error(f"Handshake Interrupted: {e}")

# --- NETWORK HEALTH ---
elif page == "Network Health":
    st.title("📟 NETWORK HEALTH")
    st.metric(label="Active Regional Nodes", value=len(registry))
    st.metric(label="Prophet Sync", value="STABLE")
    st.info("Ottawa, IL Hub: Primary Node Active")
