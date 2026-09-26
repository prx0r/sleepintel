# ORGANISM — the YouTube feedback loop (v1)

Pilots out, metrics in, verdicts applied, queue re-ranked. Weekly cadence.
Secrets: YT_API_KEY env only, never in repo. Quota: cache everything.

## Sense (collect — contract: YOUTUBE_API.md)

Per video (tracked IDs emitted at pilot): views, watch-time minutes,
average view duration, CTR (impressions→views), subs gained, likes,
top comments (文本, newest 20). Endpoints: videos.list statistics,
commentThreads.list, Analytics audienceRetention (owned channels only —
Data API has no retention; competitor retention is inferred, never
claimed). Store raw JSON under data/yt/<date>/ — immutable, never edited.

## Decide (rules, no vibes)

- PROMOTE (→ CAMPAIGNS queue): CTR ≥ channel median AND avd ≥ 25% of
  runtime within 14 days. Either pillar of the formula working.
- ITERATE (one variable): clicks without retention = packaging fail
  (retitle/rethumb, same video). Retention without clicks = topic fail
  (same packaging, new topic).
- KILL: below both medians at 30 days. Retained in registry as dead —
  dead ends are data.
- SPLIT: a series inside a channel beats its siblings 3× → own channel
  (folklore-season rule).

## Grow (act)

Queue re-ranked by (readiness × verdict momentum × moat). Pilots emit
with video IDs that encode channel + variant (ct=<id>&v=<hook>) so returns
join without manual mapping. Monthly: prune bottom-quartile pilots from
production rotation; never delete records.

## Measurement ontology (never collapse)

EXPOSED (impression) → OPENED (click) → HELD (retained past 25%) →
STAYED (past 50%) → RETURNED (next video same channel) → JOINED (sub).
Clicking ≠ watching. Watching ≠ returning. Separate stages, separate rules.

## Return rate is per video (adopted 2026-09-26)

RETURNED is measured per video, not per channel: a visualization people
return to nightly is worth 10× a story heard once. Track
`return_viewers_7d` per video ID. Kill rule exception: a low-CTR video
with high per-video return is a library asset, not a failure — it compounds.

## Open tension: hosted vs ambient (data decides)

Hosted (voice, personality) should win RPM (narrated > ambient); ambient
should win watch time (leave-it-on). Both are hypotheses (H-HOST,
H-AMBIENT), not positions. The resolver, not the author, calls it.
