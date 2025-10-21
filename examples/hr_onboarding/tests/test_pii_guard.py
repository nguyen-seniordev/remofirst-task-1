
import re, pathlib, sys
sys.path.append(str(pathlib.Path(__file__).resolve().parents[3] / "src"))

from lexguard.guards import run_guard

def test_email_redaction():
    t = "Contact me at a@b.com and 123-45-6789"
    res = run_guard(t, {"id":"pii","kind":"pii","mode":"redact"})
    assert res.ok
    assert "[REDACTED EMAIL]" in res.transformed
    assert "[REDACTED SSN]" in res.transformed
