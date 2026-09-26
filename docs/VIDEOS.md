# VIDEOS — produce → ingest → assign → monitor (v1, 2026-09-26)

Pipelines (powvid engines) produce. sleepintel ingests, assigns, watches.
All data global from ingest onward: every stat, verdict, and competitor
note joins the same store the hypotheses resolve against.

## Lifecycle

1. PRODUCE (pipeline side): engine renders → out.mp4 + manifest (inputs,
   hashes, variant). Emits a tracked ID: `ct=<channel_id>&v=<hook>`
   baked into the upload metadata + manifest.
2. INGEST: video record created in registry/videos.yaml (id, channel,
   engine, variant, hashes, upload date, platform IDs when published).
3. ASSIGN: channel binding confirmed (shelf + account derived, never
   hand-set — derived from the channel row so re-shelving propagates).
4. MONITOR: daily metric snapshots → data/yt/<date>/<video>.json
   (Data API publics + Analytics retention on owned).
5. VERDICT: ORGANISM rules fire on the snapshots (promote / iterate with
   one named variable / kill retained-as-data). Hypotheses resolve.

## Video record (schema)

video_id (tracked) · channel_id · engine · variant{pace, captions, hand,
accent, art} · out_sha · duration_s · uploaded_at · platform{yt_id} ·
status (pilot / network / killed) · verdicts[].

## Competitors (same store, flagged)

registry/competitors.yaml: channel URL, shelf guess, subs/views snapshots
(same daily cadence, inferred-only retention). Research on other sleep
channels lives here, not in chat — every claim carries its snapshot date.

## Stats views (questions the store answers weekly)

- Per-video return rate (library assets vs one-shots).
- Variant matrix results (pace × captions × hand × accent, per engine).
- Shelf medians (CTR, AVD share, return) — the prune inputs.
- Engine cost per retained hour (operator minutes + cash ÷ watch hours).
- Competitor velocity (views/day by shelf — where is the field moving).

## Laws

No video without a tracked ID. No metrics without a snapshot file.
No verdict without a rule. Competitor numbers are inferred, never
presented as measured.
