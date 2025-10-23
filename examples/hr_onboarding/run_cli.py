
import os, sys, json, pathlib
from dotenv import load_dotenv

load_dotenv()
sys.path.append(str(pathlib.Path(__file__).resolve().parents[2] / "src"))

from lexguard.runtime import build_runner

BASE = pathlib.Path(__file__).resolve().parent
policy_path = str(BASE / "policy.yaml")
transcript_path = str(BASE / "sample_transcript.jsonl")
system_prompt = (BASE / "prompts" / "system.md").read_text(encoding="utf-8")

model = os.getenv("LEXGUARD_MODEL", "mock:default")
runner = build_runner(policy_path, transcript_path, model, system_prompt)

print("LexGuard HR Onboarding Demo. Type 'exit' to quit.\n")

while True:
    user = input("You: ").strip()
    if user.lower() in {"exit", "quit"}:
        break
    turn = runner.run_turn(user)
    print(f"Agent[{turn.intent}]: {turn.text}")
    if turn.guard_events:
        for ge in turn.guard_events:
            if ge.action in ("redact", "warn") and ge.message:
                print(f"  (guard: {ge.rule_id} -> {ge.action}: {ge.message})")
    if turn.done:
        print("Conversation ended.\n")
        break

print(f"\nTranscript saved to: {transcript_path}")
print(f"[debug] Using LLM: {model}")
