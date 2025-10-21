
from __future__ import annotations
import os
from .dsl import load_policy
from .llm import make_llm
from .audit import Auditor
from .agent import AgentRunner

def build_runner(policy_path: str, transcript_path: str, model: str, system_prompt: str) -> AgentRunner:
    policy = load_policy(policy_path)
    llm = make_llm(model)
    auditor = Auditor(transcript_path)
    runner = AgentRunner(policy=policy, llm=llm, auditor=auditor, system_prompt=system_prompt)
    return runner
