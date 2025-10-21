
Subject: Home task — Compliant AI Agent Prototype (LexGuard)

Hi Maciej,

As agreed, please find my submission for the compliant AI chat agent framework.

**Deliverables**
- GitHub repo: *(push the attached folder as a repo named `lexguard`)*
- Prototype: Python package + CLI + minimal FastAPI API
- Design: `docs/Design.md`
- Slides: `docs/Slides.md`
- Short video: script in `docs/VideoScript.md` (I can record a Loom; see script)
- Time spent: see `docs/TimeSpent.md`

**Demo instructions**
```bash
pip install -r requirements.txt
python examples/hr_onboarding/run_cli.py
# Optional: uvicorn examples.service.api:app --reload
```
By default, the demo uses a mock LLM and runs offline. To try a live model, set `OPENAI_API_KEY` and `LEXGUARD_MODEL=openai:gpt-4o-mini`.

**Notes**
- The design is inspired by Parlant's approaches (Journeys/Guidelines), adapted into a compact policy DSL with explicit guards and audit.
- The example scenario focuses on HR/EOR-style onboarding: sensitive data routing, contract summaries, approval gating.

Best regards,
Anh
