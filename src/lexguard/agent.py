from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any, List, Optional, Callable
import os

from .dsl import Policy
from .graph import Graph
from .guards import run_guard, GuardResult
from .memory import Memory
from .audit import Auditor
from .llm import BaseLLM

# Pretty printing (falls back to print if rich isn't available)
try:
    from rich import print as rprint  # type: ignore
except Exception:  # pragma: no cover
    rprint = print


@dataclass
class TurnResult:
    """Structured result of a single turn."""
    intent: str
    text: str
    guard_events: List[GuardResult]
    allowed_next: List[str]
    done: bool = False


class AgentRunner:
    """
    Orchestrates one conversational turn:
      1) Determine allowed next intents from policy graph
      2) Ask the LLM to choose among allowed (bounded autonomy)
      3) Ask the LLM to draft a reply
      4) Run guards (block/redact/warn) before release
      5) Persist audit + memory and return TurnResult

    Debugging:
      - Toggle verbose checkpoints with env var: LEXGUARD_DEBUG=1
      - Checkpoints: STEP A..F show state, choices, drafts, guards, and final output
    """

    def __init__(
        self,
        policy: Policy,
        llm: BaseLLM,
        auditor: Auditor,
        system_prompt: str,
        step_callback: Optional[Callable[[Dict[str, Any]], None]] = None,
    ):
        self.policy = policy
        self.graph = Graph.from_policy(policy)
        self.llm = llm
        self.auditor = auditor
        self.system_prompt = system_prompt
        self.mem = Memory(intent=policy.default_intent)

        # Debug switch via env var
        self._debug = os.getenv("LEXGUARD_DEBUG", "0").lower() in {"1", "true", "yes"}
        # Optional programmatic hook to observe middle results
        self._step_cb = step_callback

    # ------------- internal helpers -------------

    def _d(self, *args, **kwargs) -> None:
        """Conditional debug print."""
        if self._debug:
            rprint(*args, **kwargs)

    def _allowed_next(self, intent_id: str) -> List[str]:
        """Return allowed next intents for a given current intent."""
        it = self.policy.intents.get(intent_id)
        return list(it.allowed_next) if it else []

    # ------------- main turn loop -------------

    def run_turn(self, user_text: str) -> TurnResult:
        """Process a single user message and return the agent's response."""
        # Record user input in memory
        self.mem.add_turn("user", user_text)

        # STEP A: Determine allowed next intents from current state
        allowed = self._allowed_next(self.mem.intent)
        self._d(f"[bold cyan]STEP A[/] current_intent=[bold]{self.mem.intent}[/], allowed_next={allowed}")

        # Ask the LLM to choose among allowed (bounded autonomy)
        next_intent = self.llm.choose_next_intent(
            allowed,
            {"intent": self.mem.intent, "fallback_intent": "goodbye"},
        )
        if self._step_cb:
            self._step_cb({
                "stage": "choose_intent",
                "current": self.mem.intent,
                "allowed": allowed,
                "chosen": next_intent,
            })
        self._d(f"[bold cyan]STEP B[/] chosen_next_intent(by LLM)=[bold]{next_intent}[/]")

        # Self-heal if the model proposes something illegal
        if next_intent not in allowed and allowed:
            next_intent = allowed[0]
            self._d(f"[yellow]self-heal[/] clamped to allowed: {next_intent}")

        # STEP C: Ask the LLM to draft a reply (pre-guards)
        draft_text = self.llm.draft_reply(self.system_prompt, self.mem.history, {"intent": next_intent})
        if self._step_cb:
            self._step_cb({
                "stage": "draft",
                "intent": next_intent,
                "draft": draft_text,
            })
        self._d(f"[bold cyan]STEP C[/] draft_before_guards:\n[white]{draft_text}[/]")

        # STEP D: Apply guards (block/redact/warn) in order
        guard_events: List[GuardResult] = []
        transformed = draft_text
        for g in self.policy.guards:
            res = run_guard(
                transformed,
                {"id": g.id, "kind": g.kind, "mode": g.mode, "params": g.params},
            )
            guard_events.append(res)
            if self._step_cb:
                self._step_cb({"stage": "guard", "guard": g.id, "result": res.__dict__})

            self._d(
                f"[bold cyan]STEP D[/] guard={g.id} kind={g.kind} mode={g.mode} "
                f"-> ok={res.ok} action={res.action} msg='{res.message}'"
            )

            if not res.ok and res.action == "block":
                transformed = "I'm not able to share that here. I've routed this to a secure channel."
                self._d("[red]BLOCK[/] response replaced due to guard failure.")
                break
            if res.ok and res.action == "redact" and res.transformed:
                transformed = res.transformed
                self._d("[green]REDACT[/] applied.")

        # STEP E: Persist assistant reply + update state
        self.mem.add_turn("assistant", transformed)
        self.mem.intent = next_intent
        self._d(f"[bold cyan]STEP E[/] final_text_after_guards:\n[white]{transformed}[/]")

        # STEP F: Compute termination and log audit
        done = next_intent in self.policy.end_intents
        next_allowed = self._allowed_next(next_intent)
        self._d(f"[bold cyan]STEP F[/] next_intent={next_intent}, done={done}, next_allowed={next_allowed}")

        if self._step_cb:
            self._step_cb({"stage": "final", "intent": next_intent, "text": transformed, "done": done})

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
            intent=self.mem.intent,
            text=transformed,
            guard_events=guard_events,
            allowed_next=next_allowed,
            done=done,
        )
