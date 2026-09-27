"""Title variants, Jev-scored. Growit pattern, our thresholds.
Usage: python3 scripts/titles.py "base title" [n=3]
Emits n rewrites (rule-based) + Jev Choice pick with confidence.
Low confidence -> human picks. Costs ~$0.00002.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import jev  # noqa: E402


def variants(base, n=3):
    out = [base]
    if n > 1:
        out.append(f"Fall Asleep to {base}")
    if n > 2:
        out.append(f"{base} to Fall Asleep To")
    return out[:n]


def main():
    base = sys.argv[1]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    vs = variants(base, n)
    out = jev.decide(
        {"base": base, "variants": vs},
        {"pick": {"type": "choice",
                  "instructions": "Which title earns the click for sleep content?",
                  "criteria": {f"v{i}": v for i, v in enumerate(vs)} | {"other": "none fit"}}})
    a = out["answers"]["pick"]
    jev.record("title-" + str(abs(hash(base)) % 99999), {"base": base},
               {"pick": "choice"}, out["answers"], a["choice"])
    for i, v in enumerate(vs):
        mark = " <-- PICK" if a["choice"] == f"v{i}" else ""
        print(f"[v{i}] {v}{mark}")
    print(f"conf={a.get('confidence', 0):.2f} cost={out['usage']['cost']}")


if __name__ == "__main__":
    main()
