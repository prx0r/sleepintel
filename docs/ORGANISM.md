# ORGANISM — the YouTube feedback loop (v1)

Pilots out, metrics in, verdicts applied, queue re-ranked. Weekly cadence.
Secrets: YT_API_KEY env only, never in repo. Quota: cache everything.

## Sense (collect)

Per video (tracked IDs emitted at pilot): views, watch-time minutes,
average view duration, CTR (impressions→views), subs gained, likes,
top comments (文本, newest 20). Endpoints: videos.list (statistics,
contentDetails), search.list sparingly (quota), commentThreads.list.
Store raw JSON under data/yt/<date>/ — immutable, never edited.

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
