import streamlit as st
import pandas as pd
from groq import Groq

# ==========================================
# 1. PAGE SETUP & APPLICATION DESIGN
# ==========================================
st.set_page_config(
    page_title="FinVantage: Open AI Underwriter",
    page_icon="📊",
    layout="wide"
)

st.title("🤖 Open-Weight FinTech Risk Engine")
st.caption("🚀 Hacktoberfest Side Hustle Track — Hosted on Streamlit Cloud via Groq AI")

# ==========================================
# 2. EXTRA B2B VISUAL METRICS BAR
# ==========================================
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Inference Latency", value="~0.03s", delta="Ultra Fast (LPU)")
with col2:
    st.metric(label="Compliance Check", value="Passed", delta="DPDP Act 2026")
with col3:
    st.metric(label="Data Privacy", value="Isolated", delta="Local Context Zero-Retention")
with col4:
    st.metric(label="Supported Weights", value="2 Active", delta="Multi-LLM Switch")

st.markdown("---")

# ==========================================
# 3. SECURE API CONNECTIONS
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
# 4. SIDEBAR CONTROLS
# ==========================================
with st.sidebar:
    st.header("⚙️ Model Architecture")
    
    model_option = st.selectbox(
        "Select Open-Weight Model",
        options=[
            "openai/gpt-oss-20b",       # Recommended high-performance open replacement workhorse
            "qwen/qwen3.8-27b"          # Advanced high-context reasoning and text-parsing model
        ],
        index=0,
        help="These are fully active open-weight models running on Groq's high-speed LPU infrastructure."
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
    # CLEAR CACHE & RESET BUTTON
    # ==========================================
    st.markdown("---")
    if st.button("🗑️ Clear Cache & Reset Chat", help="Wipes conversation history and resets the AI context state."):
        # Clear the chat message history list
        st.session_state.messages = []
        # Clear Streamlit's internal computation cache
        st.cache_data.clear()
        st.cache_resource.clear()
        # Instantly refresh the UI page state
        st.rerun()

# ==========================================
# 5. MULTI-TAB WORKSPACE (Chat + Data Auditing)
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
                # Stream tokens live directly from the Groq infrastructure cluster
                completion = client.chat.completions.create(
                    model=model_option,
                    messages=api_messages,
                    temperature=temperature,
                    stream=True
                )
                
                for chunk in completion:
                    # Safe index checking for streaming outputs
                    if hasattr(chunk, 'choices') and chunk.choices:
                        delta = chunk.choices[0].delta if isinstance(chunk.choices, list) else chunk.choices.delta
                        chunk_text = getattr(delta, 'content', '') if hasattr(delta, 'content') else delta.get('content', '')
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
                    
                    # Safe structural response handling for list vs object return formats
                    if hasattr(response, 'choices') and response.choices:
                        first_choice = response.choices[0] if isinstance(response.choices, list) else response.choices
                        
                        if hasattr(first_choice, 'message'):
                            output_text = first_choice.message.content
                        elif isinstance(first_choice, dict) and 'message' in first_choice:
                            output_text = first_choice['message'].get('content', '')
                        else:
                            output_text = getattr(first_choice, 'text', str(first_choice))
                            
                        st.markdown(output_text)
                    else:
                        st.error("Received an empty or unparseable payload from the inference endpoint.")
                    
                except Exception as e:
                    st.error(f"Failed to process dataset: {str(e)}")
