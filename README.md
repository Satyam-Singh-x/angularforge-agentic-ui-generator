# ⚙ AngularForge – Guided Component Architect

AngularForge is an agentic AI system that generates, validates, and self-corrects Angular UI components using a predefined design system.

This project demonstrates structured LLM orchestration using LangGraph, hybrid validation, and controlled generation pipelines.

---

## 🚀 Features

- Agentic workflow powered by LangGraph
  
- Hybrid validation (LLM + rule-based enforcement)
  
- Strict design token compliance
  
- Self-correcting generation loop
  
- Structured output using Pydantic
  
- Prompt injection protection
  
- Streamlit-based product UI
  
- Downloadable Angular component export

---

## 🧠 Architecture Overview

User Prompt  
→ Initial Generation Agent  
→ Hybrid Validator Agent  
→ (If rejected) Correction Agent  
→ Re-validation  
→ Final Output  

All orchestration handled using LangGraph state machine.

---

## 🛠 Tech Stack

- Python 3.10
- LangChain
- LangGraph
- Gemini (ChatGoogleGenerativeAI)
- Pydantic
- Streamlit

---

## 📂 Project Structure


guided-component-architect/

│

├── app.py

├── core/

│ ├── agent_loop.py

│ ├── initial_generator.py

│ ├── correction_generator.py

│ ├── validator.py

│ └── base_llm.py

│

├── design/

│ ├── design-system.json

│ └── design_loader.py

│
├── prompts/

│ ├── system_prompt.txt

│ ├── generator_prompt.txt

│ ├── correction_prompt.txt

│ └── validation_prompt.txt

│
├── requirements.txt

└── README.md


---

## 🔐 Security


- System prompt overrides user input.
  
- Design system tokens strictly enforced.
  
- Hybrid validation prevents hallucinated output.
  
- Prompt injection attempts ignored.

---

## ▶ Run Locally


git clone https://github.com/Satyam-Singh-x/angularforge-agentic-ui-generator/

cd angularforge-agentic-ui-generator

python -m venv .venv

source .venv/bin/activate  # or .venv\Scripts\activate on Windows

pip install -r requirements.txt

streamlit run app.py

👨‍💻 Built By

Satyam Singh

AI & GenAI Engineer

LinkedIn: https://www.linkedin.com/in/satyam-singh-61152a334/
