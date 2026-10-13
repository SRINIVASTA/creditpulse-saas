import streamlit as st
import pandas as pd
from groq import Groq

# ==========================================
# 1. EXPANDED PAGE SETUP & DESIGN
# ==========================================
st.set_page_config(
    page_title="FinVantage: Open AI Underwriter",
    page_icon="📊",
    layout="wide"
)

st.title("🤖 Open-Weight FinTech Risk Engine")
st.caption("🚀 Hacktoberfest Side Hustle Track — Hosted on Streamlit Cloud via Groq AI")

# ==========================================
# 2. SECURE API CONNECTIONS
# ==========================================
if "GROQ_API_KEY" in st.secrets:
    groq_api_key = st.secrets["GROQ_API_KEY"]
else:
    groq_api_key = st.sidebar.text_input("Enter Groq API Key:", type="password")

if not groq_api_key:
    st.warning("⚠️ Please configure your GROQ_API_KEY in the Streamlit Secrets panel to activate the AI engine.")
    st.stop()

# Initialize the Groq open-weight inference client
client = Groq(api_key=groq_api_key)

# ==========================================
# 3. SIDEBAR CONTROLS
# ==========================================
with st.sidebar:
    st.header("⚙️ Model Architecture")
    
    model_option = st.selectbox(
        "Select Open-Weight Model",
        options=[
            "gemma2-9b-it",             # The classic Hacktoberfest event-featured ecosystem model
            "llama-3.1-8b-instant",     # Lightweight, ultra-fast structural parsing model
            "llama-3.3-70b-versatile",  # Powerful high-tier business reasoning model
            "mixtral-8x7b-32768"        # Excellent high-context mixture-of-experts model
        ],
        index=0,
        help="These are fully open-weight models running on high-speed cloud infrastructure."
    )
    
    st.markdown("---")
    temperature = st.slider("Temperature Tuning", min_value=0.0, max_value=1.0, value=0.1, step=0.1)
    
    system_prompt = st.text_area(
        "System Instructions",
        value=(
            "You are an expert financial risk analyst. "
            "Analyze business data, ledger entries, or banking texts carefully. "
            "Provide highly structured, conservative, and bulleted risk audit observations."
        )
    )

# ==========================================
# 4. MULTI-TAB WORKSPACE (Chat + Data Auditing)
# ==========================================
tab1, tab2 = st.tabs(["💬 Underwriting Chat Assistant", "📈 CSV Ledger Auditor"])

# --- TAB 1: CONVERSATIONAL ASSISTANT ---
with tab1:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if user_prompt := st.chat_input("Paste financial text or compliance queries here..."):
        with st.chat_message("user"):
            st.markdown(user_prompt)
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        
        api_messages = [{"role": "system", "content": system_prompt}] + [
            {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
        ]
        
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_response = ""
            
            try:
                completion = client.chat.completions.create(
                    model=model_option,
                    messages=api_messages,
                    temperature=temperature,
                    stream=True
                )
                
                for chunk in completion:
                    chunk_text = chunk.choices.delta.content
                    if chunk_text:
                        full_response += chunk_text
                        placeholder.markdown(full_response + "▌")
                
                placeholder.markdown(full_response)
                
            except Exception as e:
                st.error(f"Inference Error: {str(e)}")
                
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- TAB 2: B2B CSV DATA AUDITOR ---
with tab2:
    st.subheader("📁 Batch Transaction Risk Scanner")
    st.write("Upload a CSV file containing transaction data or account statements to scan for trends and anomalies.")
    
    uploaded_file = st.file_uploader("Choose a financial CSV file", type=["csv"])
    
    if uploaded_file is not None:
        # Read data spreadsheet using pandas
        df = pd.read_csv(uploaded_file)
        
        st.write("### Data Preview (First 5 Rows)")
        st.dataframe(df.head(), use_container_width=True)
        
        # Convert data summary to text so the open-weight model can read it
        data_summary = df.describe(include='all').to_string()
        
        if st.button("🚀 Analyze Uploaded Ledger Data"):
            with st.spinner("Analyzing spreadsheet rows using cloud-hosted open weights..."):
                
                analysis_prompt = f"Analyze the following financial dataset summary table and flag anomalies, suspicious spending patterns, or balance risks:\n\n{data_summary}"
                
                try:
                    response = client.chat.completions.create(
                        model=model_option,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": analysis_prompt}
                        ],
                        temperature=0.1
                    )
                    
                    st.write("### 📋 Executive Financial Audit Report")
                    st.markdown(response.choices[0].message.content)
                    
                except Exception as e:
                    st.error(f"Failed to process dataset: {str(e)}")
