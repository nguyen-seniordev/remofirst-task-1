
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any, List

from .dsl import Policy, Intent
from .graph import Graph
from .guards import run_guard, GuardResult
from .memory import Memory
from .audit import Auditor
from .llm import BaseLLM

@dataclass
class TurnResult:
    intent: str
    text: str
    guard_events: List[GuardResult]
    allowed_next: List[str]
    done: bool = False

class AgentRunner:
    def __init__(self, policy: Policy, llm: BaseLLM, auditor: Auditor, system_prompt: str):
        self.policy = policy
        self.graph = Graph.from_policy(policy)
        self.llm = llm
        self.auditor = auditor
        self.system_prompt = system_prompt
        self.mem = Memory(intent=policy.default_intent)

    def _allowed_next(self, intent_id: str) -> List[str]:
        it = self.policy.intents.get(intent_id)
        return list(it.allowed_next) if it else []

    def run_turn(self, user_text: str) -> TurnResult:
        self.mem.add_turn("user", user_text)

        # 1) Choose next intent within policy envelope
        allowed = self._allowed_next(self.mem.intent)
        next_intent = self.llm.choose_next_intent(allowed, {"intent": self.mem.intent, "fallback_intent": "goodbye"})
        if next_intent not in allowed and allowed:
            # self-heal: clamp to allowed[0]
            next_intent = allowed[0]

        # 2) Draft reply
        text = self.llm.draft_reply(self.system_prompt, self.mem.history, {"intent": next_intent})

        # 3) Apply guards (pre-release)
        guard_events: List[GuardResult] = []
        transformed = text
        for g in self.policy.guards:
            res = run_guard(transformed, {"id": g.id, "kind": g.kind, "mode": g.mode, "params": g.params})
            guard_events.append(res)
            if not res.ok and res.action == "block":
                transformed = "I'm not able to share that here. I've routed this to a secure channel."
                break
            if res.ok and res.action == "redact" and res.transformed:
                transformed = res.transformed

        # 4) Persist
        self.mem.add_turn("assistant", transformed)
        self.mem.intent = next_intent

        done = next_intent in self.policy.end_intents
        self.auditor.log({
            "kind": "turn",
            "intent": next_intent,
            "allowed_next": allowed,
            "user_text": user_text,
            "assistant_text": transformed,
            "guard_events": [ge.__dict__ for ge in guard_events],
            "done": done,
        })

        return TurnResult(
            intent=next_intent,
            text=transformed,
            guard_events=guard_events,
            allowed_next=self._allowed_next(next_intent),
            done=done,
        )
