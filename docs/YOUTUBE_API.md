# YOUTUBE API — collection contract (imported 2026-09-26, docs Sept 2026)

Two APIs, different jobs. Data API = public stats (any video). Analytics
API = retention (our channels only, OAuth). The ontology needs both.

## Data API v3 (key only, 10,000 units/day + buckets)

| Call | Cost | Parts we take | Feeds ontology |
|---|---|---|---|
| videos.list (id=…, 50/batch) | 1 | snippet (title, tags, publishedAt), statistics (views, likes, comments), contentDetails (duration) | EXPOSED→OPENED (views), JOINED (subs via channel delta) |
| channels.list (id=…) | 1 | statistics (subs, videoCount) | JOINED |
| commentThreads.list (videoId, 100/page) | 1 | top-level text + likeCount (newest 20) | signal mining (study/sleep mentions) |
| search.list | 100/day bucket, do NOT use for tracking | — | forbidden for collection; discovery only, rare |
| videos.insert | 100/day bucket | — | uploads go through render pipeline, not here |

Daily budget for 56 channels × 10 pilots: one videos.list batch (50 ids)
= 1 unit × ~12 batches = 12 units. Comments: 20 newest per pilot, only
pilots under verdict. Total well under quota. Cache everything; never
re-pull the same day.

## Analytics API (OAuth, our channels only)

Data API has NO retention. Collect per video via reports.query:

| Metric/dimension | What it feeds |
|---|---|
| averageViewDuration + averageViewPercentage | HELD / STAYED |
| audienceWatchRatio + relativeRetentionPerformance (100-pt curve) | WHERE it holds (intro vs body — first-5s law, scored) |
| engagedViews, views | OPENED, depth |
| Traffic source (search / suggested / browse / playlist) | which shelf discovery works |
| Device type (TV share!) | sleep signal — TV at night is the product working |
| subscribedStatus (new vs returning) | RETURNED, per video |
| Playlist adds + playlist retention | series completion (library mechanic, measured) |
| End-screen CTR + card clicks | bridge effectiveness (next-episode pull) |
| estimatedRevenue + Premium minutes | RPM vs actuals (ANALYTICS roadmap) |
| shares, comments, likes | JOINED-adjacent signals |

Variant record (pace, captions, hand, accent, art) joins every metric row
as dimensions — format features resolve against retention directly.
Series position (ep N of M) joins playlist retention — completion measured,
not assumed.

## Rules

- YT_API_KEY + OAuth refresh in env/vault only. Raw JSON → data/yt/<date>/
  immutable. No author PII beyond public comment text + counts.
- search.list is discovery-only (100/day bucket burns fast).
- Scale via multi-project pools (ACCOUNTS.md): 5+3+2 projects ≈ 100K/day.
  Cache search in SQLite; dedupe queries; quota-increase on primary.
- Retention needs owned channels — competitor retention is inferred
  (views/subs ratios), never claimed as measured.
