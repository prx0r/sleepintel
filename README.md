# sleepintel — the sleep-channel controller and organism

Theory + registry + feedback loop for a 244-channel sleep network.
Renders nothing — engines do that. Decides what gets rendered, tracks
what happened, grows the network. When a video posts, it becomes a child
of its channel and live-updates from the API.

Start: `docs/SYSTEM.md` (full map), then `docs/DEV_PLAN.md` (current phase).
Every doc is listed in SYSTEM.md §The pieces. Key runs:
`scripts/score.py` (rank) · `scripts/queue.py` (xRPM) · `scripts/actuate.py`
(gated briefs) · `scripts/rerank.py` · `scripts/classify.py` ·
`scripts/ideas.py` · `scripts/fisher.py`.
Validate: `python3 scripts/validate.py`. Tests: `pytest tests/ -q`.
