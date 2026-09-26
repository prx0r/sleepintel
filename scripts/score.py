"""Pre-launch EV scoring from the registry. Deterministic. Run: python3 scripts/score.py"""
import os
import sys

try:
    import yaml
except ImportError:
    print("pyyaml needed")
    sys.exit(2)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
READINESS = {"ready": 1.0, "ready-ish": 0.85, "intake-free": 0.9,
             "produced": 0.7, "compile": 0.6, "freshness": 0.6,
             "mixed": 0.6, "originals": 0.5, "sourcing": 0.5,
             "verify": 0.5, "gap": 0.4, "personal": 0.3}
BAND = {"MUSIC": 1.3, "PLACE": 1.15, "MIND": 1.0, "STORY": 0.95,
        "SPIRITUAL": 0.9, "ESOTERIC": 0.85, "FRESH": 0.8}
MOAT = {"mech-completionist": 0.20, "mech-collection": 0.15,
        "mech-hosted": 0.15, "mech-place": 0.10, "mech-ritual": 0.05}
# demand: curated evidence multipliers (competitor proof, empty field, bench
# depth). Default 1.0. Document the evidence in the channel row to earn >1.
DEMAND = {3: 1.2, 15: 1.1, 16: 1.15, 27: 1.25, 34: 1.1, 37: 1.25, 38: 1.2,
          41: 1.2, 11: 1.2, 75: 1.15, 80: 1.1, 212: 1.15, 123: 1.15,
          124: 1.15, 8: 1.05, 45: 1.1, 26: 1.05, 49: 1.1, 29: 1.2}
ECON = {"E1": 0.6, "E2": 0.9, "E3": 0.7, "E4": 1.0, "E5": 0.9, "E6": 0.8}


def score(c):
    r = READINESS.get(c["readiness"], 0.5)
    b = BAND.get(c["shelf"], 1.0)
    m = 1.0
    for t in c.get("tags", []):
        m *= 1.0 + MOAT.get(t, 0)
    m = min(1.6, round(m, 3))
    e = max(ECON.get(x, 0.8) for x in c["engines"])
    d = DEMAND.get(c["id"], 1.0)
    return round(r * b * m * e * d, 3)


def main(top=20):
    data = yaml.safe_load(open(os.path.join(ROOT, "registry", "channels.yaml")))["channels"]
    ranked = sorted(((score(c), c["id"], c["name"]) for c in data), reverse=True)
    print(f"{'EV':>6}  id   channel")
    for s, i, n in ranked[:top]:
        print(f"{s:>6}  {i:<4} {n}")


if __name__ == "__main__":
    main(*(int(a) for a in sys.argv[1:2]))
