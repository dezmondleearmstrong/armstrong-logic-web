import streamlit as st
import pandas as pd
from google import genai
import time
import yagmail

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Armstrong Logic | Professional Auditor", layout="wide")

# --- 2. SECURE INITIALIZATION ---
if "gemini_key" in st.secrets:
    client = genai.Client(api_key=st.secrets["gemini_key"])
    MY_EMAIL = st.secrets["my_email"]
    GMAIL_PASS = st.secrets["gmail_pass"]
else:
    st.error("🔑 Secrets missing. Please check your .streamlit/secrets.toml")
    st.stop()

# --- 3. LOGIN GATEKEEPER ---
CLIENT_PASSWORDS = {"armstrong": "logic99"}

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("🛡️ Armstrong Logic | Internal Portal")
    user = st.text_input("Username").lower()
    pw = st.text_input("Password", type="password")
    if st.button("Login"):
        if user in CLIENT_PASSWORDS and CLIENT_PASSWORDS[user] == pw:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Invalid Login")
    st.stop()

# --- 4. DATA AUDIT INTERFACE ---
st.title("📊 Deep-Dive Profit Audit")
st.write("Upload a restaurant's CSV export (Sales, COGS, or Labor) for Gemini Pro analysis.")

uploaded_file = st.file_uploader("Upload Restaurant CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df.head(10)) # Show preview
    
    analysis_goal = st.selectbox("Focus Area", ["Overall Profit Leak", "Inventory Inefficiencies", "Labor Overages"])

    if st.button("🚀 Run Gemini Pro Forensic Audit"):
        with st.spinner("Gemini Pro is crunching the data (this may take 20-30 seconds)..."):
            
            # Convert CSV to string for the AI
            csv_data = df.to_string(index=False)
            
            prompt = f"""
            Act as a high-level restaurant consultant. Analyze this data: {csv_data}
            Focus on {analysis_goal}. 
            Identify specific patterns of loss and provide a recovery plan.
            """

            # --- 5. RETRY LOGIC FOR GEMINI PRO ---
            success = False
            for attempt in range(3):
                try:
                    response = client.models.generate_content(
                        model="gemini-1.5-pro", 
                        contents=prompt
                    )
                    audit_result = response.text
                    st.success("Analysis Complete!")
                    st.markdown(audit_result)
                    
                    # Store result for email
                    st.session_state['last_audit'] = audit_result
                    success = True
                    break
                except Exception as e:
                    if "429" in str(e):
                        st.warning(f"Pro limits reached. Retrying in {15*(attempt+1)}s...")
                        time.sleep(15 * (attempt + 1))
                    else:
                        st.error(f"Error: {e}")
                        break
            
            if success:
                # Option to email this deep audit to the client
                target_client = st.text_input("Email this audit to client?")
                if st.button("📧 Send Audit Report") and target_client:
                    yag = yagmail.SMTP(MY_EMAIL, GMAIL_PASS)
                    yag.send(to=target_client, subject="Deep-Dive Profit Audit", contents=st.session_state['last_audit'])
                    st.success("Sent!")

# Sidebar Navigation Note
st.sidebar.success("Logged in: Armstrong")
if st.sidebar.button("Logout"):
    st.session_state["authenticated"] = False
    st.rerun()
