# StageGuard: A Framework for Compliant Conversational AI Agents

## 🚀 Overview
**StageGuard** is a lightweight framework for building **compliant, predictable AI chat agents** — balancing flexibility (LLM adaptability) with control (scenario-based orchestration).  
It draws inspiration from *Parlant Journeys*, but focuses on enterprise compliance and reliability, using structured stages, contextual prompts, and adaptive guardrails.

This prototype was developed as part of an **AI Engineer assignment for RemoFirst** to demonstrate design thinking, R&D approach, and coding proficiency.

---

## 🎯 Core Idea
> “Combine the adaptability of LLMs with the predictability of structured workflows.”

StageGuard introduces the concept of **conversation stages**, each with specific rules and goals.  
The agent transitions through stages while validating outputs for safety, accuracy, and compliance.

---

## 🧩 Framework Architecture

```
User
  ↓
Controller (FastAPI)
  ↓
StageManager → Stage Prompts
  ↓
LLM Engine (OpenAI / Ollama / Local)
  ↓
Guardrail Filter (safety + compliance checks)
  ↓
Response Logger
```

Each **Stage** = mini-context with its own system prompt, input expectations, and compliance filters.

---

## ⚙️ Key Components

| Component | Description |
|------------|--------------|
| **StageManager** | Controls flow of conversation; tracks current stage, transitions, and next steps. |
| **Prompt Templates** | Define structure for each stage (Intro, Info Collection, Policy, Summary). |
| **Guardrails** | Filters out unsafe or non-compliant outputs (keywords, patterns, or policies). |
| **LLM Adapter** | Interface to any language model (OpenAI GPT, LLaMA 3, Mistral, etc.). |
| **Logger** | Stores model outputs for transparency and debugging. |

---

## 💬 Example Conversation Flow

| Stage | Role | Behavior |
|--------|------|----------|
| Intro | HR Assistant | Greets user, explains purpose, asks to proceed. |
| Info Collection | Data Collector | Gathers country + position, avoids personal data. |
| Policy | Compliance Advisor | Explains local rules, without offering legal advice. |
| Summary | Recorder | Confirms understanding, summarizes conversation. |

---

## 🧠 Sample Code Snippet

```python
# stage_manager.py
class StageManager:
    def __init__(self):
        self.current_stage = "intro"

    def next_stage(self):
        transitions = {
            "intro": "collect_info",
            "collect_info": "policy",
            "policy": "summary"
        }
        self.current_stage = transitions.get(self.current_stage, "summary")
```

```python
# guardrails.py
def guardrail_filter(text):
    banned = ["guarantee", "personal ID", "social security", "bank account"]
    if any(b in text.lower() for b in banned):
        return {"safe": False, "text": "[Filtered for compliance.]"}
    return {"safe": True, "text": text}
```

```python
# main.py
from fastapi import FastAPI
from stage_manager import StageManager
from guardrails import guardrail_filter
from openai import OpenAI

app = FastAPI()
manager = StageManager()

@app.post("/chat")
def chat(user_input: str):
    stage = manager.current_stage
    prompt = stage_prompts[stage]
    raw_output = llm(prompt + "\nUser: " + user_input)
    response = guardrail_filter(raw_output)
    manager.next_stage()
    return {"stage": stage, "response": response["text"]}
```

---

## 🔒 Compliance Features

✅ Rule-based filtering for restricted content  
✅ Stage isolation for predictable behavior  
✅ Regeneration logic for unsafe outputs  
✅ Logging of all inputs/outputs for auditability  

---

## 🧰 Tools Used
- **Python 3.11**
- **FastAPI**
- **LangChain** (prompt management)
- **OpenAI / Ollama API**
- **Guardrails.ai** (optional for advanced validation)
- **Redis or JSON Memory** (for conversation context)
- **Gradio / Streamlit** (optional UI)

---

## 🎥 Demo
A short **Loom video (3–5 min)** walkthrough explaining:
- Motivation & design decisions  
- Example conversation flow  
- How StageGuard balances compliance and adaptability  
*(link placeholder — add your video URL here)*

---

## 🕓 Time Spent
Approx. **8–10 hours**, including:
- Design & architecture: 3h  
- Coding prototype: 4h  
- Testing & video: 2h  

---

## 🧭 Future Enhancements
- Replace keyword filters with **embedding-based safety classifier**  
- Integrate **Whisper + TTS** for full speech interface  
- Add **confidence-based response regeneration**  
- Support **parallel sub-agents** for multi-turn workflows  
- Extend to **multi-lingual compliance checks**

---

## 📦 Repository Structure

```
.
├── main.py
├── stage_manager.py
├── guardrails.py
├── prompts.yaml
├── requirements.txt
├── README.md
└── demo/
    ├── example_conversation.json
    └── architecture.png
```

---

## 🧑‍💻 Author
**Anh Nguyen Le**  
AI Engineer | Generative AI / LLM Specialist  
📍 Kraków, Poland  
🔗 [LinkedIn](https://www.linkedin.com/in/anh-nguyen-le-468271382/)
