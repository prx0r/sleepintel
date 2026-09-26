"""Queue pilots by P(success) x RPM band. Run: python3 scripts/queue.py [topN].
P(success) = normalized EV x hypothesis support. Play money: none — Jev gates next."""
import json
import os
import sys

try:
    import yaml
except ImportError:
    print("pyyaml needed")
    sys.exit(2)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from score import score  # noqa: E402


def main(top=10):
    data = yaml.safe_load(open(os.path.join(ROOT, "registry", "channels.yaml")))["channels"]
    evs = [(score(c), c) for c in data]
    mx = max(s for s, _ in evs) or 1.0
    hyps = []
    hdir = os.path.join(ROOT, "hypotheses")
    if os.path.isdir(hdir):
        for fp in os.listdir(hdir):
            if fp.endswith(".json"):
                hyps.append(json.load(open(os.path.join(hdir, fp))))
    boost = {}
    for h in hyps:
        w = {"active": 1.15, "probation": 1.05, "draft": 1.0,
             "demoted": 0.85, "retired": 0.0}.get(h.get("status"), 1.0)
        for cid in h.get("channel_ids", []):
            boost[cid] = boost.get(cid, 1.0) * w
    ranked = []
    for s, c in evs:
        p = round((s / mx) * boost.get(c["id"], 1.0), 3)
        rpm = round(p * {"MUSIC": 12, "PLACE": 10, "MIND": 8, "STORY": 8,
                         "SPIRITUAL": 7, "ESOTERIC": 7, "FRESH": 6}.get(c["shelf"], 7), 2)
        ranked.append((rpm, p, c["id"], c["name"]))
    ranked.sort(reverse=True)
    print(f"{'xRPM':>6}  {'P':>5}  id   channel")
    for r, p, i, n in ranked[:top]:
        print(f"{r:>6}  {p:>5}  {i:<4} {n}")


if __name__ == "__main__":
    main(*(int(a) for a in sys.argv[1:2]))
