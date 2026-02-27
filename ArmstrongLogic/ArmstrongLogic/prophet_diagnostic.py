import streamlit as st
from google import genai
import time

# [ArmstrongLogic Online] - LEVEL-OMEGA Deployment Build
st.set_page_config(page_title="🛡️ArmstrongLogic Prophet", layout="wide")

# 1. Initialize the New 2026 SDK
# Make sure to set GOOGLE_API_KEY in your Streamlit Secrets
client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

def execute_prophet_audit(sales, waste, labor):
    """Refined Audit logic using Gemini 3.1 Pro reasoning."""
    prompt = f"""
    [ArmstrongLogic Audit Protocol]
    Analyze these restaurant metrics:
    - Sales: ${sales}
    - Food Waste: ${waste}
    - Labor Hours: {labor}
    
    Calculate entropy and capital leakage. 
    Explain WHY and HOW MUCH is being lost. 
    Provide a Level-Omega Actionable Playbook.
    """
    
    # Using Gemini 3.1 Pro for the heavy lifting
    response = client.models.generate_content(
        model='gemini-3.1-pro-preview',
        contents=prompt
    )
    return response.text

# 3. Prophet Diagnostic UI
st.title("🛡️ArmstrongLogic Prophet Diagnostic v3.2")
st.write("Analyzing regional POS entropy and capital leakage.")

with st.container():
    col1, col2, col3 = st.columns(3)
    sales_input = col1.number_input("Total Sales ($)", min_value=0.0)
    waste_input = col2.number_input("Food Waste ($)", min_value=0.0)
    labor_input = col3.number_input("Labor Hours", min_value=0.0)

if st.button("EXECUTE PROPHET DIAGNOSTIC"):
    with st.status("🛡️ArmstrongLogic Analyzing....", expanded=True) as status:
        st.write("Initiating LEVEL-OMEGA Handshake...")
        try:
            result = execute_prophet_audit(sales_input, waste_input, labor_input)
            status.update(label="Audit Complete!", state="complete", expanded=False)
            
            st.divider()
            st.subheader("🛡️ArmstrongLogic Audit Result")
            st.markdown(result)
            st.success("STATUS: OPTIMIZED. Performance: LEVEL-OMEGA")
        except Exception as e:
            st.error(f"CRITICAL FAULT: {str(e)}")
            status.update(label="Handshake Failed.", state="error")
