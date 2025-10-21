
# Video Script (3–5 minutes)

**Opening (10s)**  
"Hi, I'm walking you through LexGuard — a lightweight framework that merges the predictability of rules with the flexibility of LLMs for compliant, multi-stage conversations."

**Problem (20s)**  
"LLMs are natural but risky. Flow builders are safe but brittle. Customer-grade chat agents need both: deterministic control and adaptive language."

**Key Concept (30s)**  
"LexGuard places the LLM inside a *policy envelope*. A YAML policy defines states, allowed transitions, guidelines, and guards. The LLM drafts text and chooses among allowed next steps — never outside policy."

**Architecture (40s)**  
"At runtime, the orchestrator loads the policy graph, asks the LLM to pick the next intent from allowed ones, drafts a reply using contextual guidelines, then enforces guards like PII redaction or channel requirements. Every turn is logged to JSONL with which rule fired and why."

**Demo (60–90s)**  
"Let's run the HR onboarding example. I type 'I want to onboard a contractor in Poland; my email is a@b.com'. The agent detects we're in eligibility or PII collection. When PII appears, the PII guard redacts the email and routes the user to `[channel:secure_upload]`. We can proceed to a contract summary — which never displays raw PII — and then require a manager approval before finalize."

**Differentiation (30s)**  
"Compared to heavyweight frameworks, this design is intentionally compact and transparent. Inspired by Parlant's *Guidelines* and *Journeys*, LexGuard keeps the pieces explicit and testable so teams can prove compliance."

**Close (15s)**  
"That's LexGuard. You get control, adaptability, and auditability in a few files. The repo includes a CLI, FastAPI endpoint, tests, and docs. Thanks for watching."
