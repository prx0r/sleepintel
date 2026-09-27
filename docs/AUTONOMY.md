# AUTONOMY — is Jev theatre, and the path out (v1, 2026-09-27)

## The audit (honest)

Today Jev is 80% theatre: it advises, humans act. Every decision ends in a
receipt no actuator reads. Probabilities with no policy teeth are commentary.
The 20% that's real: floors that refused to guess (rerank 0.24 kept queue
order), shapes that validate, costs measured in micro-dollars.

## What autonomy actually requires (in order)

1. OAuth on owned channels (Analytics: averageViewPercentage, revenue*,
   subscribedStatus per video per day — needs yt-analytics.readonly, money
   needs monetary scope + YPP). Without this the loop has no eyes.
2. Scheduled daemon (weekly sense→decide→act; watchdog-respawned).
3. Actuators with teeth: queue reorder (safe, first), render triggers
   (bounded cost), publish flow (human sign-off until thresholds earn auto).
4. Gated auto-actions: low-stakes auto above high confidence, everything
   else human. Fail-closed publish, fail-open verdicts. Thresholds from
   labeled data, never vibes.
5. Calibration loop: Brier-tracked accuracy per decision point; thresholds
   move on measured accuracy; model pinned, re-tuned on upgrade.

## Staged path (no jumps)

Advisory (now) → gated auto on reversible actions (queue order, tag
assignment) → actuators on bounded-cost renders → publish flow with sign-off
→ full loop with human only below floors. Each stage needs its predecessor's
receipts. Skip a stage and the theatre just gets more expensive lighting.
