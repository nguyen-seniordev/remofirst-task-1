
import pathlib, sys, os
sys.path.append(str(pathlib.Path(__file__).resolve().parents[3] / "src"))

from lexguard.runtime import build_runner

def test_allowed_transitions(tmp_path):
    policy_path = str(pathlib.Path(__file__).resolve().parents[1] / "policy.yaml")
    tp = tmp_path / "t.jsonl"
    runner = build_runner(policy_path, str(tp), "mock:default", "system")
    t1 = runner.run_turn("Hi")
    assert t1.intent in {"eligibility", "out_of_scope"}
    # Ensure agent never jumps to an undefined state
    assert "not_a_state" not in t1.allowed_next
