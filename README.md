# 🤖 FinVantage-AI: Open-Weight Multi-Modal FinTech Risk Engine & Underwriting Workbench

An enterprise-grade B2B credit risk underwriting assistant and multi-format document risk scanner built using open-weight models for the **Hacktoberfest Open-Source AI Challenge (Week 2: Side Hustle)**.

🚀 **Live Interactive Web App Dashboard:** *[PASTE YOUR STREAMLIT APP URL HERE]*  
💻 **Target Open AI Inference Cluster:** Groq Cloud LPU Infrastructure [1]

---

## 💼 The Side Hustle Concept
Manual credit risk underwriting and portfolio tracking for MSMEs in emerging markets are fundamentally bottlenecked by compliance overheads, structural audit density, and fragmented media formats (documents, scans, ledger logs). **FinVantage-AI** transforms this reactive utility process into an automated, proactive **Virtual AI CFO and Multi-Format Underwriting Assistant** tailored directly for Fintechs, Neo-banks, and NBFCs.

By designing the core processing layers entirely around public open-weight architectures rather than closed corporate APIs, enterprise financial clients retain the transparent blueprints necessary to scale background log parsing algorithms seamlessly without risking vendor lock-in or sudden operational cost swings.

---

## 🛠️ The Open-Source Tech Stack
- **Frontend Matrix:** Streamlit Cloud (Engineered for clean, data-dense layouts) [1]
- **Open AI Inference Infrastructure:** Groq Cloud LPU Cluster (Extremely low latency token processing) [1]
- **Target Open Weights Active Portfolio:** [1]
  - `openai/gpt-oss-20b`: Highly optimized open workhorse used for high-velocity structural text generation.
  - `qwen/qwen3.8-27b`: State-of-the-art open-source text generation and deep reasoning model used for multi-tier audit log parsing.
- **Data Engineering Layer:** Pandas Matrix Tables for raw dataset transformations.

---

## 📈 Core Architecture Features

### 💬 1. Underwriting Chat Assistant (Tab 1)
- **High-Density Parsing:** Converts unstructured bank text dumps, account alerts, and chaotic raw audit logs into structured risk assessments instantly.
- **Context Preservation:** Built-in multi-turn session tracking equipped with high-density hyperparameter dials for custom underwriting adjustments.

### 📁 2. Multi-Format Risk Scanner (Tab 2)
Your workflow automatically adapts to the format of the incoming asset layer:
- **Ledger Spreadsheets (`.csv`, `.xlsx`):** Ingests raw data using Pandas, instantly rendering custom **Operational Risk Charts** for KYC distribution and portfolio concentration right above the AI executive audit generation.
- **Text Documents & PDFs (`.txt`, `.pdf`):** Scans document extract character arrays line-by-line to isolate hidden operational liabilities or contract mismatch patterns.
- **Compliance Scans (`.png`, `.jpg`, `.jpeg`):** Embeds client verification images directly into the audit view layout and prompts compliance parameters mapped to national frameworks.
- **Walkthrough Logs (`.mp4`, `.mov`):** Renders digital transactions or verification records inside an interactive media frame to completely protect corporate teams against account repudiation.

### 🗑️ 3. Isolated State Management
- Includes a hardware-level **"Clear Cache & Reset Chat"** escape block that immediately wipes conversational vectors and computation memory streams, guaranteeing zero data retention.

---

## 🔓 Why Open Innovation Matters (The Compliance Argument)
In modern financial markets, data protection laws (such as India's **DPDP Act 2026**) strictly prohibit uploading highly sensitive consumer bank records, corporate ledgers, or customer data to proprietary, opaque cloud endpoints. 

FinVantage-AI establishes a strict **Privacy-First Data Architecture**:
1. **Local Readiness:** The orchestration logic relies purely on open-weight specifications. This means an enterprise can swap the cloud API client out for a local `Ollama` background daemon instance running entirely on internal secure servers.
2. **Regulatory Compliance:** Zero persistent storage on the frontend container aligns fully with isolated local zero-retention mandates.

---

## 🚀 How to Run Locally

1. Clone the repository to your machine:
   ```bash
   git clone https://github.com
   cd your-repo-name
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your environment secrets in a local `.env` file or export your key directly:
   ```bash
   export GROQ_API_KEY="your_gsk_api_key_here"
   ```

4. Launch the dashboard:
   ```bash
   streamlit run app.py
   ```
