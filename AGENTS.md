# AGENTS.md — sleepintel (read first, every session)

Controller repo: decides what gets rendered, tracks what happened, grows
the network. Renders nothing. SYSTEM ONLY — no content work here, ever
(see DEV_PLAN.md Forbidden list).

## Start here, in order

SYSTEM.md (map of the map) → THESIS.md → DEV_PLAN.md (current phase) →
registry/channels.yaml → ORGANISM_LINKS.md → jev/decisions.json.

## Daily loop

`scripts/score.py` → `scripts/queue.py` → `scripts/actuate.py --dry-run`
→ `scripts/rerank.py` → read `data/decisions/` → act on receipts.
Validate: `python3 scripts/validate.py`. Tests: `pytest tests/ -q`.

## Laws

Contracts versioned, never silently adapted. Thresholds from data, never
vibes. Low confidence routes human. Secrets in `.env` only (gitignored).
Push only when asked. Kill fast, keep the note.
