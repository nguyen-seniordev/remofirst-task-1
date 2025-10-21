
from __future__ import annotations
import re
from dataclasses import dataclass
from typing import Dict, Any, Tuple

PII_PATTERNS = {
    "email": re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
    "phone": re.compile(r"\+?\d[\d\s\-]{7,}\d"),
    "ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
}

@dataclass
class GuardResult:
    ok: bool
    action: str        # "allow", "block", "redact", "warn"
    message: str = ""
    transformed: str = ""  # possibly redacted text
    rule_id: str = ""

def run_guard(text: str, rule: Dict[str, Any]) -> GuardResult:
    kind = rule.get("kind")
    mode = rule.get("mode", "block")
    rid = rule.get("id", kind)

    if kind == "pii":
        redacted = text
        found = False
        for name, pat in PII_PATTERNS.items():
            def repl(m):
                return f"[REDACTED {name.upper()}]"
            if pat.search(text):
                found = True
                redacted = pat.sub(repl, redacted)
        if not found:
            return GuardResult(ok=True, action="allow", rule_id=rid)
        if mode == "redact":
            return GuardResult(ok=True, action="redact", transformed=redacted, rule_id=rid,
                               message="PII redacted")
        return GuardResult(ok=False, action="block", rule_id=rid, message="PII detected")

    if kind == "blocklist":
        terms = [t.lower() for t in rule.get("params", {}).get("terms", [])]
        lowered = text.lower()
        for t in terms:
            if t in lowered:
                if mode == "warn":
                    return GuardResult(ok=True, action="warn", rule_id=rid, message=f"Contains '{t}'")
                return GuardResult(ok=False, action="block", rule_id=rid, message=f"Blocked term '{t}'")
        return GuardResult(ok=True, action="allow", rule_id=rid)

    if kind == "channel":
        # Here we only check text for markers; in a real system, we would inspect context/session
        required = rule.get("params", {}).get("required", "secure_upload")
        if f"[channel:{required}]" in text:
            return GuardResult(ok=True, action="allow", rule_id=rid)
        return GuardResult(ok=False, action="block", rule_id=rid, message=f"Requires channel '{required}'")

    # Default: allow
    return GuardResult(ok=True, action="allow", rule_id=rid)
