# BEST JEV GITHUBS (ranked for sleepintel, 2026-09-26)

## Install now

1. **jkudish/jev-mcp** — 11 tools (verify/screen/noul/find/rerank/classify/
   decide/compare/extract/review/gate) as MCP + agent skill teaching when to
   use each. Multi-provider (Typesafe/OpenRouter/Cloudflare!). Node 24 here
   satisfies Node 22+. Action: register as MCP server, use decide/rerank/
   classify instead of our hand-rolled calls where they fit.

## Adopt patterns (no install)

2. **jev-table** — questions-as-data packs, dry-run cost preview, resume
   cache, corrections.csv → cases.jsonl training rows, review queue.
   Our classify.py wants the corrections loop next.
3. **Spring/NPipeline/Rust clients** — retries with backoff+jitter,
   AdaptiveLimiter, injectable fake transports for tests, fail-closed.
   Our scripts/jev.py wants a fake transport + limiter.
4. **pi-jev gate CLI** — exit-code gates for CI (0 pass / 1 reject / 2 error).
   Gate registry edits + hypothesis files in CI.
5. **jev-hermes compaction** — Jev judges keep/truncate/drop per unit.
   Future: decision-log compaction when data/decisions grows.
6. **Canny evidence ledger** — challenges unsupported "done" claims.
   Matches our receipts philosophy; watch for patterns.

## Watch

- awesome-jev index (tracking new tooling), jev-review-action (PR gates —
  needs repo Actions + key secret, owner call), OpenJev (open-model
  research baseline, not production).
