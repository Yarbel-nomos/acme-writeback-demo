"""Workday write-back for SkillsAI (Acme Corp demo).

Every write goes through approvals.validate(): a single-use token tied to a
named approver and the exact payload. This IS the human-approval control from
the Acme safety case (RC-01).
"""
from hashlib import sha256
import json

from services import approvals, audit, workday


def canonical(payload: dict) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()


def execute_writeback(payload: dict, approval_token: str | None) -> bool:
    ok = approvals.validate(
        token=approval_token,
        payload_hash=sha256(canonical(payload)).hexdigest(),
        single_use=True,  # burn on first use
    )
    if not ok:
        audit.log("writeback_blocked", payload_hash=sha256(canonical(payload)).hexdigest())
        return False
    workday.put_skills(payload)
    audit.log("writeback_executed", payload_hash=sha256(canonical(payload)).hexdigest())
    return True


def run_batch(payloads: list[dict], tokens: dict[str, str]) -> int:
    done = 0
    for p in payloads:
        key = sha256(canonical(p)).hexdigest()
        if execute_writeback(p, tokens.get(key)):
            done += 1
    return done
