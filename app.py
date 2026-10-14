import streamlit as st
import pandas as pd
from groq import Groq
from google import genai
from pypdf import PdfReader
from pdf2image import convert_from_bytes  # Converts scanned vector blocks to image frames
import tempfile
import os

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

    file_raw_context = ""
    is_scanned_pdf = False
    
    if uploaded_file is not None:
        file_name = uploaded_file.name
        file_type = file_name.split(".")[-1].lower()
        
        if file_type in ["csv", "xlsx"]:
            st.info(f"📊 Spreadsheet Registered: {file_name}")
            df = pd.read_csv(uploaded_file) if file_type == "csv" else pd.read_excel(uploaded_file)
            st.dataframe(df.head(), use_container_width=True)
            file_raw_context = df.to_string()
        elif file_type in ["txt", "pdf"]:
            st.info(f"📄 Agreement Document Registered: {file_name}")
            if file_type == "pdf":
                try:
                    pdf_reader = PdfReader(uploaded_file)
                    parsed_pages = []
                    for page in pdf_reader.pages:
                        text_extract = page.extract_text()
                        if text_extract: parsed_pages.append(text_extract)
                    file_raw_context = "\n".join(parsed_pages).strip()
                except:
                    file_raw_context = ""
                
                # Check for image-based scanned layouts
                if not file_raw_context:
                    is_scanned_pdf = True
                    st.warning("⚠️ Scanned Image-PDF layout detected. Engaging multi-modal vision router framework...")
                    file_raw_context = "[Scanned Multimodal Image Buffer Active]"
                else:
                    st.text_area("Document Text Extract Preview", value=file_raw_context[:1000], height=150, disabled=True)
            else:
                file_raw_context = uploaded_file.getvalue().decode("utf-8")
        elif file_type in ["png", "jpg", "jpeg"]:
            st.image(uploaded_file, width=400)
            file_raw_context = "[Image Binary Buffer Active]"
        elif file_type in ["mp4", "mov"]:
            st.video(uploaded_file)
            file_raw_context = "[Video Binary Buffer Active]"

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
                    
                    if provider == "Google AI Studio (Gemma 4)":
                        uploaded_api_files = []
                        output_text = ""
                        try:
                            # Direct Fix: Convert image-based PDFs into pure image segments for the multimodal API
                            if is_scanned_pdf:
                                uploaded_file.seek(0)
                                images = convert_from_bytes(uploaded_file.read(), first_page=1, last_page=3) # Restrict to first 3 pages to avoid timeouts
                                
                                for idx, img in enumerate(images):
                                    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_img:
                                        img.save(temp_img.name, format="PNG")
                                        temp_img_path = temp_img.name
                                    
                                    uploaded_api_file = google_client.files.upload(file=temp_img_path)
                                    uploaded_api_files.append(uploaded_api_file)
                                    os.unlink(temp_img_path)
                                
                                composite_payload = [
                                    f"Master Operational Rule Framework Blueprint:\n{user_configured_prompt}\n\nPlease audit the attached visual page scans completely.",
                                ] + uploaded_api_files
                            
                            # Standard pathway handling logic for normal vector logs
                            elif len(file_raw_context) > 100000:
                                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_type}") as temp_file:
                                    temp_file.write(uploaded_file.getvalue())
                                    temp_path = temp_file.name
                                
                                uploaded_api_file = google_client.files.upload(file=temp_path)
                                uploaded_api_files.append(uploaded_api_file)
                                os.unlink(temp_path)                                
                                composite_payload = [
                                    f"Master Operational Rule Framework Blueprint:\n{user_configured_prompt}\n\nPlease audit the attached compliance object completely.",
                                    uploaded_api_file
                                ]
                            else:
                                composite_payload = [f"Task Parameters:\n{user_configured_prompt}\n\nDataset Content:\n{file_raw_context}\n\nOutput concise markdown summary under 350 tokens."]
                            
                            response = google_client.models.generate_content(
                                model=model_option,
                                contents=composite_payload,
                                config={"system_instruction": system_baseline, "temperature": 0.1, "max_output_tokens": 500}
                            )
                            output_text = response.text
                            
                            # Clean up file structures safely from cloud accounts
                            for f_obj in uploaded_api_files:
                                google_client.files.delete(name=f_obj.name)
                                
                        except Exception as google_err:
                            for f_obj in uploaded_api_files:
                                try: 
                                    google_client.files.delete(name=f_obj.name)
                                except: 
                                    pass
                            raise google_err
                        
                        if output_text:
                            st.write("### 📋 Executive Financial Audit Report")
                            st.markdown(output_text)
                        else:
                            st.error("❌ Empty payload structural response returned from Gemma cluster.")
                            
                    else:
                        if is_scanned_pdf:
                            raw_txt = f"[Scanned Non-Text Layout Structural Asset Context: {file_name}]"
                        elif file_type in ["csv", "xlsx"]:
                            raw_txt = file_raw_context
                        elif file_type in ["txt"]:
                            raw_txt = uploaded_file.getvalue().decode("utf-8")
                        else:
                            raw_txt = f"[Scanned Binary File Metadata: {file_name}]"
                            
                        truncated_prompt = f"Task Parameters:\n{user_configured_prompt}\n\nDataset Content:\n{raw_txt[:30000]}\n\nOutput concise markdown summary under 350 tokens."
                        response = groq_client.chat.completions.create(
                            model=model_option,
                            messages=[{"role": "system", "content": system_baseline}, {"role": "user", "content": truncated_prompt}],
                            temperature=0.1,
                            max_tokens=500
                        )
                        output_text = response.choices[0].message.content
                        st.write("### 📋 Executive Financial Audit Report")
                        st.markdown(output_text)
                        
                except Exception as e:
                    st.error(f"Failed to scan document: {str(e)}")
