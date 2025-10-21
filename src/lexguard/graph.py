
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List

from .dsl import Policy

@dataclass
class Graph:
    adjacency: Dict[str, List[str]] = field(default_factory=dict)

    @classmethod
    def from_policy(cls, policy: Policy) -> "Graph":
        adj = {intent_id: it.allowed_next for intent_id, it in policy.intents.items()}
        return cls(adjacency=adj)

    def is_allowed(self, current: str, next_intent: str) -> bool:
        if current not in self.adjacency:
            return False
        return next_intent in self.adjacency[current]
