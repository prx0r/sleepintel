# CONTROLLER — sleepintel as control plane (v1, 2026-09-26)

sleepintel renders nothing. It queues, gates, measures, learns — the
controller around finalbuilds2-style registries and powvid engines.

## The loop (one cycle)

1. SCORE — `scripts/score.py`: every channel gets EV from static features.
2. QUEUE — `scripts/queue.py`: pilots ranked by P(success) × RPM band.
   P(success) = normalized EV × hypothesis support (active parents boost,
   demoted parents drag) × calibration (resolved history where it exists).
3. GATE — Jev verdict Choice per queued pilot (promote/iterate/kill/other).
   Low confidence → human. Receipts in data/decisions/.
4. EMIT — assembly manifest (schemas/assembly.v1) to the engine queue.
5. MEASURE — tubeintel pulls metrics; snapshots join hypotheses.
6. RESOLVE — forecasts playing_out/not → fitness updates → weights shift
   (commit message says which verdict caused it).
7. LEARN — demand multipliers, thresholds, queue order all move. The
   controller generates its own intelligence: every cycle's priors are
   last cycle's posteriors.

## RPM discipline

Rank key is expected RPM per engine-hour (EV × band ÷ effort), not views.
Maximal RPM is the goal; watch-hours are the constraint; kill rule stays
views-agnostic with the library-asset exception.

## Registry parallel (finalbuilds2)

channels.yaml IS the work registry: each row a candidate with parents
(hypotheses), status (readiness lifecycle), predictions (thresholds).
Ideas queue (`ideas/next.json`) is the dispatch list. Videos become
children with tracked IDs. Same shape, sleep content.
