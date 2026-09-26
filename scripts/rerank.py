"""Jev rerank of the idea queue: one Choice over candidate pilots.
Hard gates first (readiness, rights) run in code; Jev judges the rest.
Fail conduit: error -> human queue order unchanged."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import jev  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOCKED = {"sourcing", "gap", "intake", "personal", "verify"}


def rerank(candidates, n=5):
    """candidates: [{id, name, pitch, readiness}]. Returns ordered ids."""
    eligible = [c for c in candidates if c.get("readiness") not in BLOCKED]
    if not eligible:
        return []
    state = {"pilots": [
        {"id": c["id"], "name": c["name"], "pitch": c.get("pitch", "")}
        for c in eligible[:20]]}
    criteria = {str(c["id"]): f"{c['name']}: {c.get('pitch', '')}"
                for c in eligible[:20]}
    criteria["other"] = "none fit — keep queue order"
    try:
        out = jev.decide(state, {"pick": {
            "type": "choice",
            "instructions": "Which pilot should render next for maximal sleep RPM?",
            "criteria": criteria}})
    except Exception:
        return [c["id"] for c in eligible[:n]]  # fail: queue order stands
    ans = out["answers"]["pick"]
    jev.record("rerank-" + "-".join(str(c["id"]) for c in eligible[:5]),
               state, {"pick": "choice over pilots"}, out["answers"],
               ans["choice"])
    print(f"# jev pick={ans['choice']} conf={ans.get('confidence', 0):.2f} "
          f"model={out.get('_pinned_model')}", file=sys.stderr)
    if ans["choice"] == "other" or ans.get("confidence", 0) < 0.5:
        return [c["id"] for c in eligible[:n]]
    first = int(ans["choice"])
    rest = [c["id"] for c in eligible[:20] if c["id"] != first]
    return [first] + rest[:n - 1]


if __name__ == "__main__":
    import yaml
    data = yaml.safe_load(open(os.path.join(ROOT, "registry", "channels.yaml")))["channels"]
    cands = [{"id": c["id"], "name": c["name"], "pitch": c.get("pitch", ""),
              "readiness": c["readiness"]} for c in data
             if c["readiness"] in ("ready", "ready-ish", "compile", "produced")]
    print(rerank(cands, int(sys.argv[1]) if len(sys.argv) > 1 else 5))
