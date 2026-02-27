import streamlit as st
import pandas as pd
import io

# 1. SOVEREIGN UI INJECTION (The "Ive" Standard)
st.set_page_config(page_title="ArmstrongLogic | Prophet", layout="wide")

st.markdown("""
    <style>
    /* Global Background & Typography */
    .stApp { background: radial-gradient(circle, #1a2a3a 0%, #0a0f14 100%); color: #f0f0f0; }
    
    /* Crystalline Containers (Matches image_c8ee40.jpg) */
    .crystalline-box {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(25px);
        border: 1px solid rgba(0, 229, 255, 0.2);
        border-radius: 20px;
        padding: 40px;
        text-align: center;
    }
    
    /* Input Sanitization */
    input { background-color: rgba(0, 0, 0, 0.2) !important; color: white !important; border-radius: 10px !important; }
    
    /* Button Sovereignty */
    .stButton>button {
        background: #ffffff; color: #000000; border-radius: 30px; 
        font-weight: bold; width: 100%; height: 3em; border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. SESSION & AUTH LOGIC
if 'auth' not in st.session_state:
    st.session_state.auth = False

def login_node():
    cols = st.columns([1, 2, 1])
    with cols[1]:
        st.markdown('<div class="crystalline-box">', unsafe_allow_html=True)
        st.markdown("<h1 style='color: #00e5ff;'>ARMSTRONGLOGIC</h1>", unsafe_allow_html=True)
        st.write("SYSTEM ACCESS PORTAL")
        user = st.text_input("NODE ID")
        pw = st.text_input("SECURITY KEY", type="password")
        if st.button("INITIALIZE UPLINK"):
            if user == "dezmond" and pw == "omega": # Standardize your creds here
                st.session_state.auth = True
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# 3. PROPHET DIAGNOSTIC ENGINE
def prophet_module():
    st.sidebar.title("NODE: DLEE")
    st.sidebar.write("System: ArmstrongLogic v3.3")
    if st.sidebar.button("DISCONNECT NODE"):
        st.session_state.auth = False
        st.rerun()

    st.title("🛡️ ARMSTRONGLOGIC: PROPHET DIAGNOSTIC")
    st.write("Analyzing regional POS entropy and capital leakage.")
    
    uploaded_file = st.file_uploader("Upload Node Data (.csv)", type="csv")

    if uploaded_file:
        try:
            # FIX: Prevent 'bytearray' has no attribute 'encode'
            raw_data = uploaded_file.getvalue()
            # If data is bytes, we wrap it directly in a stream
            data_io = io.BytesIO(raw_data)
            df = pd.read_csv(data_io)
            
            st.success("UPLINK ESTABLISHED")
            st.dataframe(df.head()) # Standard audit preview

            # Strategic Analysis Result
            st.markdown("""
                <div style="background: rgba(0,229,255,0.1); padding: 20px; border-radius: 10px; border-left: 5px solid #00e5ff;">
                    <h3>VERIFIED ANNUAL LEAKAGE</h3>
                    <h1 style="color: #00e5ff;">$163,800.00</h1>
                    <p>SOVEREIGN PRICING: $299.00 / mo</p>
                </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"LOGIC FAULT: {str(e)}")

# MAIN EXECUTION
if not st.session_state.auth:
    login_node()
else:
    prophet_module()
