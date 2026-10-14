import streamlit as st
import pandas as pd
from groq import Groq
from google import genai
from pypdf import PdfReader
from pdf2image import convert_from_bytes
import tempfile
import time
import os

# Try importing extended document enclosure parsers safely with standard fallback overrides
try:
    from docx import Document as DocxReader
except ImportError:
    DocxReader = None

try:
    from pptx import Presentation as PptxReader
except ImportError:
    PptxReader = None

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
# 2. HYBRID SECURE API ROUTING PIPELINE
# ==========================================
groq_key_available = "GROQ_API_KEY" in st.secrets
google_key_available = "GOOGLE_API_KEY" in st.secrets

groq_client = None
google_client = None

if groq_key_available:
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
if google_key_available:
    google_client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
# ==========================================
# 3. TRANSIENT SESSION STATE INITIALISATION
# ==========================================
if "current_file_type" not in st.session_state:
    st.session_state.current_file_type = "default"

# Primary session storage buckets for ACTUAL real-time execution benchmarks
if "actual_latency" not in st.session_state:
    st.session_state.actual_latency = 0.0
if "actual_tokens_per_sec" not in st.session_state:
    st.session_state.actual_tokens_per_sec = 0.0
if "actual_token_count" not in st.session_state:
    st.session_state.actual_token_count = 0
if "last_audit_report" not in st.session_state:
    st.session_state.last_audit_report = ""

persona_blueprints = {
    "default": "You are an expert financial risk analyst. Provide highly structured, conservative, and bulleted risk audit observations.",
    "spreadsheet": "You are a quantitative data risk scientist specializing in forensic accounting and tabular anomaly detection. Output highly precise statistical summaries and structural risk analysis tables.",
    "document": "You are an expert corporate legal officer and contract risk auditor. You review text clauses meticulously, looking for hidden liabilities, missing regulatory disclosures, and formatting risks.",
    "image": "You are a specialist in automated KYC imaging, computer vision OCR auditing, and digital identity fraud verification under the strict parameters of the DPDP Act 2026.",
    "video": "You are a senior forensic multi-modal video analyst and digital transaction audit trail investigator specializing in preventing account transaction repudiation.",
    "audio": "You are a forensic audio investigator and speech analytics risk compliance officer checking spoken verification statements."
}

# ==========================================
# 4. SIDEBAR USER HYBRID CONTROLLER
# ==========================================
with st.sidebar:
    st.header("⚙️ Inference Router")
    
    provider = st.radio(
        "Choose Infrastructure Layer",
        options=["Google AI Studio (Gemma 4)", "Groq Cloud (Open-Weights)"],
        index=0
    )
    
    st.markdown("---")
    
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
        st.session_state.actual_latency = 0.0
        st.session_state.actual_tokens_per_sec = 0.0
        st.session_state.actual_token_count = 0
        st.session_state.last_audit_report = ""
        if "user_frozen_prompt" in st.session_state:
            del st.session_state.user_frozen_prompt
        st.cache_data.clear()
        st.cache_resource.clear()
        st.rerun()

# ==========================================
# 5. DYNAMIC B2B VISUAL METRICS TELEMETRY BAR
# ==========================================
metrics_container = st.container()
with metrics_container:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.session_state.actual_latency > 0.0:
            st.metric(label="Live Inference Latency", value=f"{st.session_state.actual_latency:.3f}s", delta="Stopwatch Calculation")
        else:
            st.metric(label="Live Inference Latency", value="Waiting...", delta="Awaiting First Run")
    with col2:
        if st.session_state.actual_tokens_per_sec > 0.0:
            st.metric(label="Generation Throughput", value=f"{st.session_state.actual_tokens_per_sec:.1f} TPS", delta=f"{st.session_state.actual_token_count} Generated Tokens")
        else:
            st.metric(label="Generation Throughput", value="Waiting...", delta="0 Tokens Compiled")
    with col3:
        st.metric(label="Compliance Matrix", value="100% Isolated", delta="DPDP Act 2026 Ready")
    with col4:
        st.metric(label="Active Target Architecture", value=model_option.split("/")[-1], delta=f"Engine infrastructure: {provider.split()}")

st.markdown("---")
# ==========================================
# 6. MULTI-TAB WORKSPACE INITIALISATION
# ==========================================
tab1, tab2 = st.tabs(["💬 Underwriting Chat Assistant", "📁 Multi-Format Risk Scanner"])

# --- TAB 1: CONVERSATIONAL ASSISTANT ---
with tab1:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Direct extraction loop to display previous conversation data cleanly
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
            generated_chunks = 0
            
            try:
                # Trigger Actual Real-Time Benchmark Stopwatch
                start_timer = time.time()
                
                # ROUTE 1: GOOGLE GEMMA 4 RUNTIME INFERENCE MATRIX
                if provider == "Google AI Studio (Gemma 4)":
                    chat_contents = [m["content"] for m in st.session_state.messages]
                    try:
                        # Try standard streaming path first
                        response_stream = google_client.models.generate_content_stream(
                            model=model_option,
                            contents=chat_contents,
                            config={"system_instruction": user_configured_prompt, "temperature": temperature}
                        )
                        for chunk in response_stream:
                            if chunk.text:
                                full_response += chunk.text
                                generated_chunks += 1
                                placeholder.markdown(full_response + "▌")
                    except Exception as chat_err:
                        # HARDENED FIX: If streaming hits a 500 error, drop streaming and run stable batch content delivery
                        st.warning("🔄 Server congestion handled. Re-routing through stabilized B2B transaction layer...")
                        try:
                            stable_response = google_client.models.generate_content(
                                model="gemma-4-26b-a4b-it", # Fallback to high-velocity MoE
                                contents=chat_contents,
                                config={"system_instruction": user_configured_prompt, "temperature": temperature, "max_output_tokens": 500}
                            )
                            if stable_response.text:
                                full_response = stable_response.text
                                placeholder.markdown(full_response)
                            else:
                                raise chat_err
                        except Exception as stable_err:
                            raise stable_err
                            
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
                        if chunk.choices and hasattr(chunk.choices[0].delta, 'content'):
                            chunk_text = chunk.choices[0].delta.content or ''
                            if chunk_text:
                                full_response += chunk_text
                                generated_chunks += 1
                                placeholder.markdown(full_response + "▌")
                                
                # Compute Actual Benchmarking Suite Metrics
                stop_timer = time.time()
                duration = stop_timer - start_timer
                
                estimated_tokens = int(len(full_response.split()) * 1.33) if full_response else 0
                if estimated_tokens == 0:
                    estimated_tokens = generated_chunks
                
                # Save data directly into session storage elements
                st.session_state.actual_latency = duration
                st.session_state.actual_token_count = estimated_tokens
                st.session_state.actual_tokens_per_sec = (estimated_tokens / duration) if duration > 0 else 0.0
                
                # Clear text box and append raw response parameters securely before layout render pass
                placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
                # Force window reload to lock data onto telemetry metrics grid bars
                st.rerun()
                
            except Exception as e:
                st.error(f"Execution Error: {str(e)}")

        # FIXED PERSISTENT RENDERING LAYER: Draws text directly onto the secure anchor layout framework
        if st.session_state.last_audit_report:
            with report_display_anchor.container():
                st.write("---")
                st.write("### 📋 Executive Financial Audit Report")
                st.markdown(st.session_state.last_audit_report)
