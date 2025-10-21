
from __future__ import annotations
from typing import Dict, Any

# Minimal stub to illustrate tool contracts
def hrdb_lookup(employee_email: str) -> Dict[str, Any]:
    # In real life, validate scopes and perform secure data access.
    if employee_email.endswith("@example.com"):
        return {"exists": True, "department": "Engineering", "manager": "Dana", "country": "PL"}
    return {"exists": False}
