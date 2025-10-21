
# LexGuard — Design Document

**Objective:** Deliver a framework that blends **predictability** with **flexibility** for multi-stage, compliant LLM conversations.

---

## 1) Mental Model

- **Policy Envelope** — a declarative YAML policy defines *what is allowed*, *what is required*, and *what is forbidden*.  
- **Conversation Graph** — deterministic states + allowed transitions.  
- **Guidelines (Principles)** — contextual nudges that shape *how* the LLM speaks **within** the policy envelope.  
- **Guards** — programmatic checks that block/redact/warn on policy violations pre-release.  
- **Auditability** — every turn is logged with rationale and guard decisions.  
- **Self-Healing** — if the LLM proposes an out-of-policy step, we clamp to the nearest allowed transition and explain.

This yields natural language where the **LLM supplies language + local choices**, and the **policy supplies structure and safety**.

## 2) Policy DSL

```yaml
id: hr_onboarding
version: "1.0"
default_intent: start
end_intents: ["goodbye"]
intents:
  - id: eligibility
    required_slots: ["country", "employment_type"]
    allowed_next: ["collect_pii", "out_of_scope"]
guidelines:
  - id: pii_handling
    when: "intent == 'collect_pii'"
    do: "Ask for [channel:secure_upload]; don't echo PII."
guards:
  - id: redact_pii
    kind: pii
    mode: redact
```

- **Intents** ≈ stages of a journey.  
- **Guidelines** ≈ targeted behavior rules (inspired by Parlant *Guidelines*).  
- **Guards** ≈ enforcement layer (PII, blocklists, channel policies).

## 3) Flow of a Turn
1. Load **allowed next** states for the current intent.  
2. Let the **LLM choose** among allowed next (never outside).  
3. Ask LLM to **draft a reply** guided by active principles.  
4. Run **guards** → block, redact, or warn.  
5. **Persist** transcript + guard events.  
6. If end state, **terminate**; else update current intent.

## 4) Compliance Features
- **PII Guard** (regex prototype → pluggable to enterprise DLP)  
- **Channel Guard** (requires secure channel markers before collecting sensitive data)  
- **Blocklist Guard** (warn/block certain claims or language)  
- **Approval Gates** (human review before finalization)  
- **Audit JSONL** with evidence of checks

## 5) Testing
- **Scenario tests** assert transitions + guard actions.  
- **Redaction tests** ensure sensitive markers are removed.  
- Determinism comes from the **graph** and guards; the LLM remains bounded.

## 6) Relationship to Prior Art
- **Parlant** — aligns behavior with *Journeys* and *Guidelines*, plus deep tool integration (see docs). LexGuard mirrors these ideas with a compact DSL and explicit guard layer.  
- **LangGraph** — stateful orchestration for agents via graphs; LexGuard uses a simplified, built-in graph to keep the dependency surface small.

## 7) Extensibility
- Swap `MockLLM` with OpenAI, Anthropic, etc.  
- Replace regex PII with a real-time **guardrail service**.  
- Add **tool contracts** with typed IO and per-intent authorization.  
- Expand the YAML DSL to cover scoring, routing, and rollback.

---

*This document accompanies the code prototype in this repo.*
