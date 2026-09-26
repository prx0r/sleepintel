# CALIBRATION — bullshit audit + proper path (v1, 2026-09-26)

## What's bullshit today (named)

1. EV is ordinal, not cardinal. 1.18 vs 1.026 means rank, not "18% better".
2. Bands ($12 music etc.) are placeholders, never measured.
3. Demand multipliers are judgment with no fitted weights.
4. P(success) > 1.0 is not a probability. It's priority wearing a costume.
5. Zero resolved hypotheses. Uncalibrated by definition — nothing has come true yet.

## The proper path (from literature)

- Brier scoring on every resolved prediction (Tetlock). Decompose into
  calibration (humility) + resolution (discrimination). Track both; elite
  judges win on resolution, not calibration.
- Reference-class priors first (Kahneman/Flyvbjerg): shelf medians ARE the
  reference class. Priors come from base rates, never vibes.
- Two-stage bandit (Reddit pCTR paper): stage 1 = context-free TS weighted
  by historical priors (this is score.py today); stage 2 = contextual as
  data accumulates. Cold start is a solved problem — run the solution.
- Jev as pseudo-observations with calibration-gated decay: Jev predictions
  enter as weighted pseudo-data; weight decays as real data arrives
  (exp(-eta * EMA_error)). Formalizes Jev's pre-data role. Caution from
  the literature: aggressive gating silences useful signal — tune eta
  per domain, prefer simple constant decay first.
- Isotonic regression for raw-score→probability mapping (LinkedIn BanditLP)
  once outcomes exist. Never before.
- Small elite judges beat large noisy crowds (Wharton: ~0.05 Brier edge).
  Owner verdicts + 2-3 trusted judges > comment sentiment mining.
- Training works (CHAMP: 6-12% Brier gain). Whoever judges gets the
  calibration training: base rates, comparison classes, updating.
- Prompt framing dominates tuning (mind_click: 19% regret cut from wording
  alone). Our Jev question wording matters more than our thresholds.

## Standing orders

No EV decimals quoted as percentages. No band cited without "placeholder".
First 10 resolved pilots get Brier-scored publicly in-repo. Weights fit,
never set, after that.
