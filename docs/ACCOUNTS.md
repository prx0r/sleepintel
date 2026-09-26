# ACCOUNTS — risk separation (adopted 2026-09-26)

One flagged channel can endanger every linked channel (TeamYouTube +
creator reports). Separate by content risk, not channel count. Each
account: own Google login, own AdSense, own GCP quota pool.

## Account A — safe (PD readings, human-curated)

Shelves: SPIRITUAL (18) + ESOTERIC (13) + STORY (11) = 42 channels.
Engines: E2, E3, E5-reading. Starts Week 1. Lowest risk: pre-1930 texts,
paraphrase-first channeled, lore-framed everything.

## Account B — medium (AI involvement)

Shelves: MIND (6) + MUSIC (3) = 9 channels.
Engines: E1 (house renders, Suno/ACE covers), E5. Starts Week 3.
Isolated from A: a music-rights dispute never touches the readings.

## Account C — highest risk (ambience, daily)

Shelves: PLACE (4) + FRESH (1) = 5 channels.
Engines: E4, E6. Starts Week 3. Ambience originality + daily-scan
velocity contained here, away from everything else.

## Quota pools (multi-project, cached, deduped)

- A: 5 GCP projects ≈ 50K units/day. B: 3 ≈ 30K. C: 2 ≈ 20K.
- search.list is discovery-only (100/day bucket); tracking runs on
  videos.list + commentThreads (1 unit) + Analytics retention (owned).
- Cache all search in SQLite; only NEW queries hit the API.

## AdSense note (boring, essential)

Separate AdSense per account; may need distinct tax IDs/payment methods.
Set up correctly from the start — retrofitting after a flag is too late.
