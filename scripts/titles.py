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


# Provisional floor: no calibration data yet. Move to decisions when measured.
TITLE_FLOOR = 0.5


def main():
    base = sys.argv[1]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    vs = variants(base, n)
    try:
        out = jev.decide(
            {"base": base, "variants": vs},
            {"pick": {"type": "choice",
                      "instructions": "Which title earns the click for sleep content?",
                      "criteria": {f"v{i}": v for i, v in enumerate(vs)} | {"other": "none fit"}}})
    except Exception as e:
        print(f"GATE ERROR ({type(e).__name__}): human picks (fail-open to human)")
        return
    a = out["answers"]["pick"]
    conf = a.get("confidence", 0)
    action = a["choice"] if conf >= TITLE_FLOOR else "human-picks"
    jev.record("title-" + str(abs(hash(base)) % 99999), {"base": base},
               {"pick": "choice"}, out["answers"], action,
               extra={"model": out.get("_pinned_model"),
                      "band": jev.band_confidence(conf),
                      "threshold_applied": {"floor": TITLE_FLOOR},
                      "cost": (out.get("usage") or {}).get("cost")})
    for i, v in enumerate(vs):
        mark = " <-- PICK" if action == f"v{i}" else ""
        print(f"[v{i}] {v}{mark}")
    print(f"conf={conf:.2f} action={action} cost={(out.get('usage') or {}).get('cost')}")


if __name__ == "__main__":
    main()
