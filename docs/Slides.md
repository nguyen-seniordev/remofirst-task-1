
# LexGuard — Compliant AI Chat Agents (Interview Deck)

## Problem
- LLMs are powerful but unpredictable
- Flows are predictable but brittle
- We need **both** for multi-stage conversations with compliance

## Idea
- Put the LLM inside a **policy envelope**
- Deterministic **graph** controls *where* it can go
- **Guidelines** shape *how* it speaks
- **Guards** enforce safety/compliance

## Architecture (Mermaid)
```mermaid
flowchart LR
  U[User] -->|text| O(Orchestrator)
  subgraph Policy Envelope
    G[Graph: Allowed Transitions]
    GL[Guidelines: Contextual Principles]
    GD[Guards: PII / Blocklist / Channel]
  end
  O -->|choose among allowed| LLM[LLM]
  LLM -->|draft| O
  O -->|apply guards| GD
  GD -->|allow/redact/block| O
  O -->|reply + audit| U
  O -->|JSONL| A[(Audit Log)]
```

## Demo
- HR / EOR onboarding assistant
- PII only through **secure_upload**
- Contract summary without raw PII
- Approval gate before finalization

## Why It Works
- **Predictability**: Graph + DSL
- **Flexibility**: LLM drafts & selects within bounds
- **Compliance**: Guards + Audit + Approvals
- **Maintainability**: Tests and explicit policy

## Roadmap
- Stronger guards (DLP, classification)
- Tool authz scopes per intent
- Confidence scoring / auto-escalation
- Synthetic scenario generation for tests
