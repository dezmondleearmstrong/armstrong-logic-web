import streamlit as st
import pandas as pd
import yaml
import streamlit_authenticator as stauth
from yaml.loader import SafeLoader
from google import genai
from google.genai import types

# --- 1. PRO UI CONFIGURATION ---
st.set_page_config(page_title="Armstrong Logic", page_icon="🛡️", layout="wide")

# Custom Glassmorphism CSS
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at 50% 50%, #1a1a2e 0%, #0e1117 100%); }
    [data-testid="stSidebar"] { background-color: rgba(22, 27, 34, 0.8); border-right: 1px solid #00FFA3; }
    .stButton>button { background-color: #00FFA3 !important; color: #0e1117 !important; border-radius: 20px; font-weight: bold; border: none; box-shadow: 0 0 15px rgba(0, 255, 163, 0.4); }
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE VAULT (CONFIG) ---
try:
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)
except FileNotFoundError:
    st.error("Vault missing: config.yaml not found.")
    st.stop()

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# --- 3. PRO LOGIN SCREEN ---
if not st.session_state.get('authentication_status'):
    st.markdown("""
        <div style='text-align: center; padding: 3rem 0;'>
            <h1 style='color: #00FFA3; font-size: 3.5rem; margin-bottom: 0;'>🛡️ ARMSTRONG LOGIC</h1>
            <p style='color: #8B949E; font-size: 1.3rem; letter-spacing: 3px;'>THE QUANTUM STANDARD IN PROFIT PROTECTION</p>
            <div style='background-color: rgba(0, 255, 163, 0.05); border: 1px solid rgba(0, 255, 163, 0.2); border-radius: 10px; padding: 15px; margin-top: 25px; display: inline-block;'>
                <span style='color: #E6EDF3;'><i>”The Truth is in the Logic.”</I></span>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Render the Login form
auth_data = authenticator.login(location='main')

# Logic to handle tuple return from authenticator
if isinstance(auth_data, tuple):
    name, authentication_status, username = auth_data
else:
    name = st.session_state.get('name')
    authentication_status = st.session_state.get('authentication_status')
    username = st.session_state.get('username')

# --- 4. AUTHENTICATED PORTAL ---
if authentication_status:
    authenticator.logout('🔒 Secure Logout', 'sidebar')
    
    # Initialize Gemini 2.5 Pro Client
    client = genai.Client(api_key=st.secrets["gemini_key"])

    st.markdown("<h2 style='color: #00FFA3;'>Forensic Command Center</h2>", unsafe_allow_html=True)
    st.divider()

    # Layout: Left for Audit, Right for "Me" Chatbot
    col_audit, col_chat = st.columns([1.8, 1])

    with col_audit:
        st.subheader("📊 Profit Protection Audit")
        uploaded_file = st.file_uploader("Drop client POS .csv here", type=["csv"])
        
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.success(f"Dataset Loaded: {len(df)} records detected.")
            with st.expander("Preview POS Data"):
                st.dataframe(df.head(10), use_container_width=True)
            
            if st.button("🚀 Execute ARMSTRONGLOGIC Audit"):
                with st.spinner("Dezmond Logic Engine scanning for profit leaks..."):
                    # Use Gemini 2.5 Pro for deep forensic audit
                    audit_response = client.models.generate_content(
                        model="gemini-2.5-pro",
                        contents=[f"Act as a forensic restaurant auditor. Analyze this POS data and identify specific profit leaks, labor inefficiencies, or menu price gaps:\n\n{df.to_string()}"]
                    )
                    st.markdown("### 📋 Audit Findings")
                    st.info(audit_response.text)

    with col_chat:
        st.subheader("💬 Chat with Dezmond")
        st.write("I'm here to interpret these results for you.")
        
        # Neural Mirror Chat History
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Ask me anything about your margins..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                # SYSTEM INSTRUCTION: Mimics your expertise and soul
                response = client.models.generate_content(
                    model="gemini-2.5-pro",
                    config=types.GenerateContentConfig(
                        system_instruction="You are Dezmond Lee Armstrong, the founder of Armstrong Logic. You world class chef and a brilliant forensic restaurant auditor. You speak with a mix of wit, deep intelligence, and grounded empathy. Your goal is to help your clients understand their profit data and feel supported. Be 100 trillion years advanced, but human.",
                    ),
                    contents=[prompt]
                )
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})

    # --- 5. ADMIN: ADD CLIENTS ---
    if username == 'dlee':
        st.sidebar.divider()
        with st.sidebar.expander("🛠️ Admin: Deploy New Client"):
            try:
                # Setting pre_authorized=None allows you to manually register any client
                if authenticator.register_user(location='main', pre_authorized=None):
                    st.success('Client Vaulted. Password saved to config.yaml.')
                    with open('config.yaml', 'w') as file:
                        yaml.dump(config, file, default_flow_style=False)
            except Exception as e:
                st.error(f"Registry Error: {e}")

elif authentication_status == False:
    st.error('❌ Authorization Failed: Credential mismatch.')
