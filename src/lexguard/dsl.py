
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
import yaml

@dataclass
class Guideline:
    id: str
    when: str
    do: str
    weight: int = 1

@dataclass
class GuardRule:
    id: str
    kind: str                # "pii", "blocklist", "channel", "custom"
    mode: str = "block"      # "block", "redact", "warn"
    params: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Intent:
    id: str
    description: str = ""
    required_slots: List[str] = field(default_factory=list)
    allowed_next: List[str] = field(default_factory=list)
    human_approval: Optional[str] = None  # e.g., "legal", "manager"

@dataclass
class Policy:
    id: str
    version: str
    intents: Dict[str, Intent]
    guidelines: List[Guideline] = field(default_factory=list)
    guards: List[GuardRule] = field(default_factory=list)
    default_intent: str = "start"
    end_intents: List[str] = field(default_factory=lambda: ["goodbye"])

def load_policy(path: str) -> Policy:
    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    intents = {}
    for it in raw.get("intents", []):
        intents[it["id"]] = Intent(
            id=it["id"],
            description=it.get("description",""),
            required_slots=it.get("required_slots", []),
            allowed_next=it.get("allowed_next", []),
            human_approval=it.get("human_approval"),
        )

    guidelines = [Guideline(**g) for g in raw.get("guidelines", [])]
    guards = [GuardRule(**g) for g in raw.get("guards", [])]
    return Policy(
        id=raw["id"],
        version=str(raw.get("version","0")),
        intents=intents,
        guidelines=guidelines,
        guards=guards,
        default_intent=raw.get("default_intent", "start"),
        end_intents=raw.get("end_intents", ["goodbye"]),
    )
