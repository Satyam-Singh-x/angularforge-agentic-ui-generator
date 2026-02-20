import streamlit as st
from core.agent_loop import run_agent
import difflib

# ===================== PAGE CONFIG =====================
st.set_page_config(
    page_title="AngularForge",
    page_icon="⚙️",
    layout="wide"
)

# ===================== CUSTOM THEME =====================
st.markdown(
    """
    <style>
    /* Global font */
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }

    /* Main background */
    .stApp {
        background-color: #C9D8CF;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0E1A2B !important;
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Titles */
    h1 {
        color: #0F3D2E;
        font-weight: 700;
        text-align: center;
        font-size: 48px;
    }

    h2, h3 {
        color: #0F3D2E;
        font-weight: 600;
    }

    /* Buttons */
    .stButton>button {
        background-color: #1E5B47;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.6rem 1rem;
    }

    .stButton>button:hover {
        background-color: #164A3A;
    }

    /* Tabs */
    button[role="tab"] {
        font-weight: 600;
        color: #0F3D2E !important;
    }

    button[aria-selected="true"] {
        border-bottom: 3px solid #1E5B47 !important;
    }

    /* Code block */
    code {
        background-color: #F4F7F6;
        color: #0F3D2E;
    }

    </style>
    """,
    unsafe_allow_html=True
)
# ===================== HEADER =====================
st.markdown("""
<h1>⚙️ AngularForge</h1>
<p style='text-align:center; font-size:20px; color:#1E5B47;'>
Guided Component Architect – Agentic Angular UI Generator ✨
</p>
""", unsafe_allow_html=True)

# ===================== SIDEBAR =====================
with st.sidebar:
    st.header("🔧 AngularForge")

    st.markdown("""
Generate production-ready Angular components
using a controlled AI agentic workflow.
""")

    user_prompt = st.text_area(
        "Describe the UI Component",
        placeholder="Example: Create a login card with glassmorphism"
    )

    max_retries = st.slider("Max Correction Attempts", 1, 3, 2)

    generate_button = st.button("🚀 Generate Component")

# ===================== RUN AGENT =====================
if generate_button and user_prompt:
    with st.spinner("Running Agentic Workflow..."):
        result = run_agent(user_prompt,max_retries)

    st.session_state["result"] = result
    st.session_state["original_prompt"] = user_prompt

# ===================== MAIN TABS =====================
tabs = st.tabs([
    "🧩 Generated Component",
    "📜 Execution Logs",
    "✅ Validation Report",
    "👤 About"
])

# ===================== TAB 1: GENERATED CODE =====================
with tabs[0]:
    if "result" in st.session_state:
        final_code = st.session_state["result"]["current_code"]

        st.subheader("Final Angular Component")
        st.code(final_code, language="typescript")

        st.markdown("### ✏ Minor Adjustments")

        modification_prompt = st.text_area(
            "Refine this component",
            placeholder="Example: Make the button larger and centered"
        )

        if st.button("Apply Modification"):
            previous_code = st.session_state["result"]["current_code"]
            original_prompt = st.session_state.get("original_prompt", "")

            combined_prompt = f"""
Original User Request:
{original_prompt}

Existing Angular Component:
{previous_code}

Refinement Instructions:
{modification_prompt}

Modify the existing component according to the refinement instructions.
Preserve valid Angular structure.
Strictly follow the predefined design system.
Do not redesign from scratch unless absolutely necessary.
"""

            with st.spinner("Re-running with refinement..."):
                new_result = run_agent(combined_prompt)

            st.session_state["result"] = new_result
            st.rerun()

        st.download_button(
            label="📥 Download Component",
            data=final_code,
            file_name="generated_component.ts",
            mime="text/plain"
        )

# ===================== TAB 2: EXECUTION LOGS =====================
with tabs[1]:
    if "result" in st.session_state:
        logs = st.session_state["result"]["attempt_logs"]

        for i, attempt in enumerate(logs, start=1):
            st.markdown(f"### Attempt {i}")

            st.code(attempt["code"], language="typescript")
            st.json(attempt["validation"])

# ===================== TAB 3: VALIDATION SUMMARY =====================
with tabs[2]:
    if "result" in st.session_state:
        final_validation = st.session_state["result"]["approved"]

        if final_validation:
            st.success("Component Approved by Validator ✅")
        else:
            st.error("Component Rejected After Maximum Retries ❌")

# ===================== TAB 4: ABOUT =====================
with tabs[3]:
    st.markdown("""
### 👨‍💻 Built By

**Satyam Singh**  
AI & GenAI Engineer  

🔗 LinkedIn: https://www.linkedin.com/in/satyam-singh-61152a334/

---

### 🚀 What This Project Demonstrates

- LangGraph-based agentic orchestration
- Hybrid validation (LLM + rule-based)
- Strict design system enforcement
- Structured outputs using Pydantic
- Controlled self-correction workflow

AngularForge is built as a production-style AI system — not a simple chatbot.
""")
