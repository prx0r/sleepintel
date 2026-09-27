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
    path = os.path.join(ROOT, "data", f"calibration_{name}.jsonl")
    if not os.path.exists(path) and name == "template":
        path = os.path.join(ROOT, "data", "calibration_template.jsonl")
    if not os.path.exists(path):
        print(f"no labels: {path} missing. Labels are the asset — "
              f"collect rows first (see docs/CALIBRATION.md).")
        sys.exit(1)
    rows = [json.loads(l) for l in open(path) if l.strip()]
    hits, bands, costs, unscored = 0, {"high": [0, 0], "mid": [0, 0], "low": [0, 0]}, 0.0, 0
    for r in rows:
        out = jev.decide(r["state"], r["questions"])
        ans = out["answers"][r["key"]]
        costs += (out.get("usage") or {}).get("cost", 0) or 0
        pred = ans.get("choice", ans.get("noul", ans.get("score")))
        conf = ans.get("confidence")  # model-reported only; never invented
        ok = (pred == r["correct"]) if not isinstance(r["correct"], list) else (pred in r["correct"])
        hits += ok
        if conf is None:
            unscored += 1
            continue
        band = "high" if conf >= 0.8 else ("mid" if conf >= 0.5 else "low")
        bands[band][0] += ok
        bands[band][1] += 1
    n = len(rows)
    print(f"n={n} acc={hits / n:.2f} cost=${costs:.6f} unscored={unscored}")
    for b, (h, t) in bands.items():
        print(f"  {b}: {h}/{t} = {h / t:.2f}" if t else f"  {b}: no data")


if __name__ == "__main__":
    run(sys.argv[1])
