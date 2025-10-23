
<p align="center">
  <img src="https://img.shields.io/badge/LexGuard-Compliance_as_Code-blue?style=for-the-badge" alt="LexGuard Badge"/>
</p>

# LexGuard — *"Language Governed by Law"*

> **LexGuard** derives its name from two core principles:
>
> - **Lex** — from the Latin *lex*, meaning “law,” “policy,” or “rule,” symbolizing **compliance, regulation, and deterministic behavior**.  
> - **Guard** — representing **protection, enforcement, and auditability**, ensuring that AI systems operate **within approved and transparent boundaries**.
>
> Together, **LexGuard** embodies the idea of *“a system that guards language by law.”*  
> It’s designed for teams that seek to merge **policy-driven predictability** with **LLM adaptability** — achieving both **control and creativity** in compliant conversational AI.

---

### 🧠 *A policy-first framework for building compliant, auditable, and adaptive AI chat agents.*

**Goal:** Merge **predictability** (rule-based reliability) with **flexibility** (LLM adaptability) in long, multi-stage conversations — with **compliance guarantees**.

LexGuard is a small, production-minded prototype that demonstrates:
- A **policy DSL (YAML)** to declaratively encode *what an agent may/shall/must not do*
- An **interaction graph** (states + transitions) to constrain control flow
- **Guidelines** (principles) that are contextually activated to let an LLM stay natural *within* the policy envelope
- **Guards** (PII, profanity, topic, channel) that **block/redact/self-heal** violations before responses are released
- **Auditable transcripts** (JSONL) with *who, why, and which rule* influenced each turn
- A **test harness** for scenario-based regression on compliance + behavior
- A minimal **CLI** demo and optional **FastAPI** endpoint

> ✳️ **Inspiration**: Parlant's ideas around *Journeys* and *Guidelines* for agent behavior modeling and tool use informed this design. This repo shows how to attain a similar blend of **control + adaptability** with lightweight components and a transparent policy layer.

## Why this approach?
Traditional flows are brittle; pure LLM autonomy is risky. LexGuard composes:
- **Determinism** via a typed **state graph** + **policy DSL**
- **Adaptability** by letting the LLM *select among allowed* next steps and draft text, *but never outside policy*
- **Compliance** through pre- and post-LLM **guards**, automatic **redaction**, and **human-in-the-loop** gates

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

# Run the CLI demo (HR onboarding example)
python examples/hr_onboarding/run_cli.py

# Optional: run a REST API
uvicorn examples.service.api:app --reload
```

> By default, a **MockLLM** is used so you can run without credentials. To try a real model, set `OPENAI_API_KEY` and run with `--model openai:gpt-4o-mini` (or edit `examples/hr_onboarding/run_cli.py`).

## Repo map

```
lexguard/
  README.md
  LICENSE
  requirements.txt
  pyproject.toml
  .env

  src/lexguard/
    __init__.py
    dsl.py            # YAML policy schema + loader
    graph.py          # State graph + validation
    policy.py         # Policy model (rules, intents, approvals)
    guards.py         # PII / profanity / topic / channel guards
    audit.py          # JSONL audit + trace
    memory.py         # Short/long-term memory
    llm.py            # LLM adapters (Mock + OpenAI stub)
    agent.py          # Orchestrator: one-turn loop with self-healing
    tools.py          # Tool interface + a stubbed HR DB tool
    runtime.py        # High-level runner helpers

  examples/
    hr_onboarding/
      policy.yaml
      prompts/
        system.md
        escalation.md
      run_cli.py
      sample_transcript.jsonl
      tests/
        test_pii_guard.py
        test_flow.py

    service/
      api.py          # Minimal FastAPI app exposing /chat
      docker-compose.yml (optional)

  docs/
    Design.md

```

## Highlights
- **Policy-first**: Declare norms in YAML; code enforces them.
- **Flexible text**: The LLM writes language; rules **shape** it and **veto** when needed.
- **Deterministic control**: Only **allowed transitions** are ever taken.
- **Explainability**: Each output cites which **rules**, **guards**, and **tools** applied.
- **Testability**: Run scenario tests that assert both **answers** and **compliance**.

## How it relates to Parlant
- Similarities: **Guidelines/Principles**, **Journeys (state)**, **tight tool integration**, and **alignment modeling**
- Differences: a very **lightweight, open** DSL; small **standard-library-first** runtime; and transparent guards/audits you can tailor. See `docs/Design.md` for a side-by-side and rationale.

## Demo Scenario (HR / EOR Onboarding)
A multi-stage flow with sensitive data:
1) **Greeting & Eligibility Check** → country, employment type, role  
2) **Collect PII in Secure Channel** → only after consent & channel is `secure_upload`  
3) **Contract Draft** → generate summary (never raw PII)  
4) **Approval Gate** → manager/legal confirmation required  
5) **Finalize & Next Steps** → hand-off links + checklist

Guards enforce **no PII in open chat**, **no legal promises**, and **de-escalation** to a human if uncertainty grows.

---

**Status:** Prototype for interview submission — field-ready patterns, not a full product.  
**Authored:** 2025-10-20

