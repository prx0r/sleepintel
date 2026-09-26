# FORECASTS + FITNESS (adopted from finalbuilds2, 2026-09-26)

finalbuilds2 runs hypotheses with four records we lack. Adopt all four.

## 1. Forecasts (new: hypotheses/forecasts/)

Prediction + window_start + window_end + predictive_distribution +
resolution_rule_version + evidence_snapshot_hash. Our predictions have
thresholds but no windows or frozen evidence — add both. A forecast is
what gets resolved; a prediction is what it claims.

## 2. Fitness (new: hypotheses/fitness.json)

Per hypothesis: predictive hits, parameter_evidence, complexity_penalty,
information_gain_bits, decision. The complexity penalty matters most:
simpler claims win ties (Occam as arithmetic). Rank the queue by fitness,
not raw EV, once data flows.

## 3. Observations (extend snapshots)

metric, entity_id, value, observed_at, source_id, QUALITY,
provenance_hash. Our snapshots lack quality + provenance — add both fields
before the first real pull, or later data can't weight itself.

## 4. Resolutions (link, don't prose)

resolution_id + forecast_id + rule_version + outcome + scores +
observation_ids. Our RESOLUTIONS.md is prose; machine resolutions join
forecasts to observations by ID. Both live: prose for humans, records
for the resolver.
