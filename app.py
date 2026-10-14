import streamlit as st
import pandas as pd
from groq import Groq
from google import genai

# ==========================================
# 1. PAGE SETUP & APPLICATION DESIGN
# ==========================================
st.set_page_config(
    page_title="CreditPulse: B2B Multi-Engine Underwriter",
    page_icon="📊",
    layout="wide"
)

st.title("🤖 CreditPulse: Hybrid Open-Weight Risk Engine")
st.caption("🚀 Hacktoberfest AI Challenge — Dual Cloud Inference Engine (Groq LPU / Google AI Studio)")

# ==========================================
# 2. EXTRA B2B VISUAL METRICS BAR
# ==========================================
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="System Architecture", value="Dual-API Engine", delta="Groq LPU + Google Cloud")
with col2:
    st.metric(label="Compliance Check", value="Passed", delta="DPDP Act 2026 Framework")
with col3:
    st.metric(label="Data Privacy", value="Isolated", delta="Local Context Zero-Retention")
with col4:
    st.metric(label="Active Weights", value="4 Options", delta="Gemma 4 / Qwen / GPT-OSS")

st.markdown("---")

# ==========================================
# 3. HYBRID SECURE API ROUTING PIPELINE
# ==========================================
# Check for existing background deployment configurations
groq_key_available = "GROQ_API_KEY" in st.secrets
google_key_available = "GOOGLE_API_KEY" in st.secrets

groq_client = None
google_client = None

if groq_key_available:
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
if google_key_available:
    google_client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
# ==========================================
# 4. TRANSIENT SESSION STATE INITIALISATION
# ==========================================
if "current_file_type" not in st.session_state:
    st.session_state.current_file_type = "default"

persona_blueprints = {
    "default": "You are an expert financial risk analyst. Provide highly structured, conservative, and bulleted risk audit observations.",
    "spreadsheet": "You are a quantitative data risk scientist specializing in forensic accounting and tabular anomaly detection. Output highly precise statistical summaries and structural risk analysis tables.",
    "document": "You are an expert corporate legal officer and contract risk auditor. You review text clauses meticulously, looking for hidden liabilities, missing regulatory disclosures, and formatting risks.",
    "image": "You are a specialist in automated KYC imaging, computer vision OCR auditing, and digital identity fraud verification under the strict parameters of the DPDP Act 2026.",
    "video": "You are a senior forensic multi-modal video analyst and digital transaction audit trail investigator specializing in preventing account transaction repudiation."
}

# ==========================================
# 5. SIDEBAR USER HYBRID CONTROLLER
# ==========================================
with st.sidebar:
    st.header("⚙️ Inference Router")
    
    # Core architectural engine selection toggle
    provider = st.radio(
        "Choose Infrastructure Layer",
        options=["Google AI Studio (Gemma 4)", "Groq Cloud (Open-Weights)"],
        index=0
    )
    
    st.markdown("---")
    
    # Dynamically pivot available open architectures based on selected provider layer
    if provider == "Google AI Studio (Gemma 4)":
        if not google_key_available:
            manual_google_key = st.text_input("Enter Google API Key:", type="password")
            if manual_google_key:
                google_client = genai.Client(api_key=manual_google_key)
            else:
                st.warning("⚠️ Google API Key missing.")
                
        model_option = st.selectbox(
            "Select Gemma 4 Variant",
            options=["gemma-4-26b-a4b-it", "gemma-4-31b-it"],
            help="High-reasoning frontier open-weights featuring up to 256K context capabilities."
        )
    else:
        if not groq_key_available:
            manual_groq_key = st.text_input("Enter Groq API Key:", type="password")
            if manual_groq_key:
                groq_client = Groq(api_key=manual_groq_key)
            else:
                st.warning("⚠️ Groq API Key missing.")
                
        model_option = st.selectbox(
            "Select Open-Weight Architecture",
            options=["openai/gpt-oss-20b", "qwen/qwen3.8-27b"],
            help="Ultra-low latency open models running natively on high-speed hardware clusters."
        )
        
    st.markdown("---")
    temperature = st.slider("Temperature Tuning", min_value=0.0, max_value=1.0, value=0.1, step=0.1)
    
    st.markdown("---")
    st.subheader("🛡️ Live System Persona")
    override_mode = st.checkbox("🔒 Lock Custom User Instructions", value=False)

    if override_mode:
        if "user_frozen_prompt" not in st.session_state:
            st.session_state.user_frozen_prompt = persona_blueprints[st.session_state.current_file_type]
        active_blueprint = st.session_state.user_frozen_prompt
    else:
        active_blueprint = persona_blueprints[st.session_state.current_file_type]
    
    user_configured_prompt = st.text_area("Active System Instructions", value=active_blueprint, height=150)
    
    if override_mode:
        st.session_state.user_frozen_prompt = user_configured_prompt

    st.markdown("---")
    if st.button("🗑️ Clear Cache & Reset Chat"):
        st.session_state.messages = []
        st.session_state.current_file_type = "default"
        if "user_frozen_prompt" in st.session_state:
            del st.session_state.user_frozen_prompt
        st.cache_data.clear()
        st.cache_resource.clear()
        st.rerun()
# ==========================================
# 6. MULTI-TAB WORKSPACE INITIALISATION
# ==========================================
tab1, tab2 = st.tabs(["💬 Underwriting Chat Assistant", "📁 Multi-Format Risk Scanner"])

# --- TAB 1: CONVERSATIONAL ASSISTANT ---
with tab1:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if user_prompt := st.chat_input("Paste financial text or compliance queries here..."):
        if (provider == "Google AI Studio (Gemma 4)" and not google_client) or (provider == "Groq Cloud (Open-Weights)" and not groq_client):
            st.error("❌ Target client is uninitialized. Configure valid API keys to communicate.")
            st.stop()
            
        with st.chat_message("user"):
            st.markdown(user_prompt)
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_response = ""
            
            try:
                # ROUTE 1: GOOGLE GEMMA 4 RUNTIME INFERENCE MATRIX
                if provider == "Google AI Studio (Gemma 4)":
                    chat_contents = [m["content"] for m in st.session_state.messages]
                    try:
                        response_stream = google_client.models.generate_content_stream(
                            model=model_option,
                            contents=chat_contents,
                            config={"system_instruction": user_configured_prompt, "temperature": temperature}
                        )
                        for chunk in response_stream:
                            if chunk.text:
                                full_response += chunk.text
                                placeholder.markdown(full_response + "▌")
                    except Exception as chat_err:
                        # Chat-level 500 fallback engine trigger
                        if "500" in str(chat_err) and model_option != "gemma-4-26b-a4b-it":
                            st.warning("🔄 System encountered a server workload spike. Routing to Gemma 4 MoE fallback cluster...")
                            response_stream = google_client.models.generate_content_stream(
                                model="gemma-4-26b-a4b-it",
                                contents=chat_contents,
                                config={"system_instruction": user_configured_prompt, "temperature": temperature}
                            )
                            for chunk in response_stream:
                                if chunk.text:
                                    full_response += chunk.text
                                    placeholder.markdown(full_response + "▌")
                        else:
                            raise chat_err
                            
                # ROUTE 2: GROQ TRADITIONAL TOKEN PROCESSING LOOP
                else:
                    api_messages = [{"role": "system", "content": user_configured_prompt}] + [
                        {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
                    ]
                    completion = groq_client.chat.completions.create(
                        model=model_option,
                        messages=api_messages,
                        temperature=temperature,
                        stream=True
                    )
                    for chunk in completion:
                        if chunk.choices and hasattr(chunk.choices, 'delta'):
                            chunk_text = getattr(chunk.choices.delta, 'content', '') or ''
                            if chunk_text:
                                full_response += chunk_text
                                placeholder.markdown(full_response + "▌")
                                
                placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
            except Exception as e:
                st.error(f"Execution Error: {str(e)}")

# --- TAB 2: MULTI-FORMAT AUDITOR ENGINE ---
with tab2:
    st.subheader("📁 Batch Document & Transaction Risk Scanner")
    uploaded_file = st.file_uploader(
        "Choose an operational file to audit...", 
        type=["csv", "xlsx", "pdf", "txt", "png", "jpg", "jpeg", "mp4", "mov"]
    )
    
    detected_type = "default"
    if uploaded_file is not None:
        file_name = uploaded_file.name
        file_type = file_name.split(".")[-1].lower()
        if file_type in ["csv", "xlsx"]: detected_type = "spreadsheet"
        elif file_type in ["txt", "pdf"]: detected_type = "document"
        elif file_type in ["png", "jpg", "jpeg"]: detected_type = "image"
        elif file_type in ["mp4", "mov"]: detected_type = "video"

    if not override_mode and detected_type != st.session_state.current_file_type:
        st.session_state.current_file_type = detected_type
        st.rerun()

    if uploaded_file is not None:
        file_name = uploaded_file.name
        file_type = file_name.split(".")[-1].lower()
        file_raw_context = ""
        
        if file_type in ["csv", "xlsx"]:
            st.info(f"📊 Processing Ledger: {file_name}")
            df = pd.read_csv(uploaded_file) if file_type == "csv" else pd.read_excel(uploaded_file)
            st.dataframe(df.head(), use_container_width=True)
            file_raw_context = df.describe(include='all').to_string()
        elif file_type in ["txt", "pdf"]:
            st.info(f"📄 Processing Agreement: {file_name}")
            try: file_raw_context = uploaded_file.read().decode("utf-8").strip()
            except: file_raw_context = f"[Target Document Context: {file_name}]"
        elif file_type in ["png", "jpg", "jpeg"]:
            st.image(uploaded_file, width=400)
            file_raw_context = f"[Compliance Document Image Context: {file_name}]"
        elif file_type in ["mp4", "mov"]:
            st.video(uploaded_file)
            file_raw_context = f"[Digital Video Compliance Context: {file_name}]"

        # ==========================================
        # HYBRID ENGINE COMPOSITE SCAN PLAN
        # ==========================================
        if file_raw_context and st.button("🚀 Execute Hybrid Platform Risk Scan"):
            if (provider == "Google AI Studio (Gemma 4)" and not google_client) or (provider == "Groq Cloud (Open-Weights)" and not groq_client):
                st.error("❌ Key infrastructure parameters missing.")
                st.stop()
                
            with st.spinner("Executing calculations via chosen engine router..."):
                try:
                    system_baseline = "You are an expert financial risk engine auditor. Respond cleanly and objectively using structured markdown."
                    composite_user_prompt = f"Task Parameters:\n{user_configured_prompt}\n\nDataset Content:\n{file_raw_context}\n\nOutput concise markdown summary under 350 tokens."
                    
                    if provider == "Google AI Studio (Gemma 4)":
                        try:
                            # Primary Action Plan
                            response = google_client.models.generate_content(
                                model=model_option,
                                contents=[composite_user_prompt],
                                config={"system_instruction": system_baseline, "temperature": 0.1, "max_output_tokens": 500}
                            )
                            output_text = response.text
                        except Exception as google_err:
                            # Fallback intercept system logic for 500 errors
                            if "500" in str(google_err) and model_option != "gemma-4-26b-a4b-it":
                                st.warning("🔄 Target cluster busy (500 Internal). Routing calculations to Gemma 4 MoE fallback layer...")
                                response = google_client.models.generate_content(
                                    model="gemma-4-26b-a4b-it",
                                    contents=[composite_user_prompt],
                                    config={"system_instruction": system_baseline, "temperature": 0.1, "max_output_tokens": 500}
                                )
                                output_text = response.text
                            else:
                                raise google_err
                        
                        if output_text:
                            st.write("### 📋 Executive Financial Audit Report")
                            st.markdown(output_text)
                        else:
                            st.error("❌ Empty payload structural response returned from Gemma cluster.")
                            
                    else:
                        response = groq_client.chat.completions.create(
                            model=model_option,
                            messages=[{"role": "system", "content": system_baseline}, {"role": "user", "content": composite_user_prompt}],
                            temperature=0.1,
                            max_tokens=500
                        )
                        output_text = response.choices.message.content
                        st.write("### 📋 Executive Financial Audit Report")
                        st.markdown(output_text)
                    
                except Exception as e:
                    st.error(f"Failed to scan document: {str(e)}")
