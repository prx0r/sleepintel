# SCORING — pre-launch math + autonomous selection (v1, 2026-09-26)

Goal: maximal RPM (blended: realized RPM × watch-hours, per engine-hour).

## Phase 1 — pre-launch score (no metrics yet, runs today)

EV(channel) = readiness × shelf_band × moat × engine_economy, each 0..~1.2.

- readiness: ready 1.0 · ready-ish/intake-free 0.85 · produced 0.7 ·
  compile/freshness/mixed/originals 0.6 · sourcing/verify 0.5 · gap 0.4 ·
  personal 0.3.
- shelf_band (RPM priors): MUSIC 1.2 · PLACE 1.1 · MIND 1.0 · STORY 1.0 ·
  SPIRITUAL 0.9 · ESOTERIC 0.9 · FRESH 0.8.
- moat (tags, additive): completionist +0.20 · collection +0.15 ·
  hosted +0.15 · place +0.10 · ritual +0.05 (cap total 1.5).
- engine_economy (cost per hour): E4 1.0 · E2/E5 0.9 · E6 0.8 · E3 0.7 · E1 0.6.
- demand (curated 1.0–1.25): competitor proof, empty field, bench depth.
  Earns >1 only with cited evidence. Moat compounds multiplicatively (cap 1.6).
- Plateaus are honest: equivalent features = equivalent bets (libraries
  cluster). Order inside a plateau barely matters; the bandit breaks ties
  with data.

`scripts/score.py` computes it from the registry. Deterministic, committed,
re-run on every registry change. Top of queue = next pilot.

## Phase 2 — bandit selection (once pilots return metrics)

UCB1 over pilots: each channel arm pulls realized RPM×hours; selector plays
highest upper-confidence bound weekly. Exploration budgeted at 20% of renders
(new/untried channels), exploitation 80%. Hypotheses resolve on the same
numbers (playing_out / not_playing_out → resources shift).

## Phase 3 — goal discipline

Maximal RPM, not maximal views. A 10K-view $15-RPM video beats a 100K-view
$1-RPM video. Kill rule stays views-agnostic: below-median realized RPM ×
hours at 30 days, with per-video-return exception (library assets compound).
