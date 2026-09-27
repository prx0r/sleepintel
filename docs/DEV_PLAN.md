# CANONICAL DEV PLAN — wire the full system up (v1, 2026-09-27)

Scope lock: SYSTEM ONLY. No renders, no pilots, no content. Content is
sleepvids/powvid's department. We build nerves, not videos.

## Phase 0 — Freeze (done)
Docs, registries, graphs, hypotheses, gates, scoring, queue, actuator,
tubeintel collector, review studio, upload path, vault. All committed.

## Phase 1 — Contracts (current)
Every repo-to-repo handoff as a versioned schema with a validator.
DONE: assembly.v1, hypothesis.v1, template.v1, decisions config, video
children rows. TODO: brief→sleepvids handshake test (dry-run both ends),
quota ledger reconciliation test, review-state machine parity (dash JSON
vs receipts).

## Phase 2 — Calibration data
Resolve queue drains into labeled rows. Jev relabels unclassified.
Thresholds fit on measured accuracy, never vibes. Brier tracked per
decision point. DONE when: 100+ labeled rows, thresholds v1 committed.

## Phase 3 — Autonomy (gated)
Daemon runs sense→decide→act weekly. Actuators: queue reorder (safe),
brief emission (bounded), publish flow (sign-off). Fail-closed everywhere
except verdict routing (fail-open to human). DONE when: one full week runs
unattended with receipts to prove it.

## Phase 4 — Organism learns
Fitness re-ranks hypotheses. Weights shift with commit messages citing
verdicts. Demand multipliers fit, not set. DONE when: first weight change
lands from real returns.

## Forbidden (always)
Content renders. Editing another agent's repo. Committing secrets. Pushing
without asking. Quota spend without ledger entry. Verdicts without rules.
Theatre (receipts no actuator reads).

## Right now
Phase 1 tail: handshake tests + ledger check. Nothing else until green.
