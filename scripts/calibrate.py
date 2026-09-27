"""Calibration: labeled sets -> accuracy-by-confidence -> tuned thresholds.
Usage: python3 scripts/calibrate.py <decision>
Reads data/calibration_<decision>.jsonl [{state, questions, correct}].
Reports accuracy overall + per band, Brier-ish calibration, suggested cuts.
No labels yet = no calibration. Labels are the asset.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import jev  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def run(name):
    rows = [json.loads(l) for l in open(os.path.join(ROOT, "data", f"calibration_{name}.jsonl"))]
    hits, bands, costs = 0, {"high": [0, 0], "mid": [0, 0], "low": [0, 0]}, 0.0
    for r in rows:
        out = jev.decide(r["state"], r["questions"])
        ans = out["answers"][r["key"]]
        costs += out["usage"]["cost"]
        pred = ans.get("choice", ans.get("noul", ans.get("score")))
        conf = ans.get("confidence", abs(ans.get("noul", 0.5) - 0.5) * 2)
        ok = (pred == r["correct"]) if not isinstance(r["correct"], list) else (pred in r["correct"])
        hits += ok
        band = "high" if conf >= 0.8 else ("mid" if conf >= 0.5 else "low")
        bands[band][0] += ok
        bands[band][1] += 1
    n = len(rows)
    print(f"n={n} acc={hits / n:.2f} cost=${costs:.6f}")
    for b, (h, t) in bands.items():
        print(f"  {b}: {h}/{t} = {h / t:.2f}" if t else f"  {b}: no data")


if __name__ == "__main__":
    run(sys.argv[1])
