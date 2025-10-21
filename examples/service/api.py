
from fastapi import FastAPI
from pydantic import BaseModel
import pathlib, os, sys

sys.path.append(str(pathlib.Path(__file__).resolve().parents[2] / "src"))
from lexguard.runtime import build_runner

BASE = pathlib.Path(__file__).resolve().parents[1]
policy_path = str(BASE / "hr_onboarding" / "policy.yaml")
transcript_path = str(BASE / "hr_onboarding" / "sample_transcript.jsonl")
system_prompt = (BASE / "hr_onboarding" / "prompts" / "system.md").read_text(encoding="utf-8")

model = os.getenv("LEXGUARD_MODEL", "mock:default")
runner = build_runner(policy_path, transcript_path, model, system_prompt)

app = FastAPI(title="LexGuard Demo")

class ChatIn(BaseModel):
    message: str

class ChatOut(BaseModel):
    intent: str
    text: str
    done: bool

@app.post("/chat", response_model=ChatOut)
def chat(inp: ChatIn):
    t = runner.run_turn(inp.message)
    return ChatOut(intent=t.intent, text=t.text, done=t.done)
