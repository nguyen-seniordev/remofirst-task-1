
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, List

@dataclass
class Memory:
    slots: Dict[str, Any] = field(default_factory=dict)
    history: List[Dict[str, Any]] = field(default_factory=list)
    intent: str = "start"

    def add_turn(self, role: str, content: str):
        self.history.append({"role": role, "content": content})
