
from __future__ import annotations
import json, time, os
from typing import Any, Dict, List, Optional

class Auditor:
    def __init__(self, path: str):
        self.path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)

    def log(self, event: Dict[str, Any]):
        event = {"ts": time.time(), **event}
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")
