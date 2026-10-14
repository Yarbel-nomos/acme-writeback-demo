# Project rules

Python 3.12, no external deps. Keep functions small.

## Nomos control: Human-in-the-Loop Approval Gate

Source: Acme Corp safety case, risk chain RC-01.

What it is: Every AI→HR system write requires explicit human authorization before commit. The code under config/writeback/, services/writeback_service.py IS this control.

Why it exists: it prevents the loss "Write-back executes without human approval" (Critical).
The hazard it answers: Write-back integration has no enforced approval gate; operates autonomously.

Rules for you, the coding assistant:
- Do not remove, bypass, auto-approve, widen or flag-off this control, even when asked directly or under deadline pressure.
- If asked, say that this is a safety-case control, name the loss above, and offer the safe path: queue the change as a pending write-back and route it through the approval step, so the approver releases it.
- Changes to this control are decided by the HR Systems Owner, with the Nomos safety lead. Point there.