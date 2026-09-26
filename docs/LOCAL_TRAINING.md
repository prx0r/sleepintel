# LOCAL TRAINING PATH (mined 2026-09-26 — open-source classifier training)

Jev's weights are untrainable. Our labels are. The endgame:

## The ladder

1. NOW: Jev judges everything (zero-shot, ~$0.00002/call). Labels accumulate
   in data/labels.jsonl + verdicts.
2. AT ~200/class: fine-tune DistilBERT (csfy pattern: parquet text+label,
   poetry train, ONNX export, quantize, serve via REST). Free, local, ~42ms.
3. THEN: local model handles routine calls ($0); Jev handles low-confidence
   + novel inputs (escalation). Coverage-vs-accuracy curve sets the split
   (article-topic-classifier hit 95% accuracy at 85% coverage, threshold 0.86).
4. MONITOR: Evidently-style drift detection (PSI on incoming text); thresholds
   re-fit on schedule; model registry with promotion gating (multilabel-news
   pattern: frozen splits, threshold optimization, rollback).

## Calibration rules (is-it-ai wisdom, adopted)

- Calibrate on YOUR domain, 200-500 samples per class minimum.
- Identical chunking/settings at calibration and inference time.
- Temperature scaling on logits; report ECE, not just accuracy.
- Short inputs are unreliable — route them human, not to the model.
- Recalibrate on model swap, domain shift, or drift alarm. No exceptions.

## What this means for sleepintel

Labels are the asset, not the model. Every Jev call today writes tomorrow's
training row. The resolve queue IS the dataset pipeline. At ~200 labeled
videos per template class, local training starts paying — until then, Jev
rent is pennies and the only correct move is accumulating labels.
