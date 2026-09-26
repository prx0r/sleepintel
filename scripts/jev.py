"""Jev-native decision client: typed questions, three-band policy, audit log.
Key: OPENROUTER_API_KEY in .env (never in repo). Model pinned (thresholds
couple to versions — jev-latest moves under you).
Policy: auto / confirm / human per action thresholds in jev/decisions.json.
Noul: threshold distance from 0.5 with separate yes/no cutoffs (no confidence
field exists — never invent one). Choice: needs 'other' escape hatch.
Score: threshold the expectation, never do arithmetic on levels."""
import json
import os
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL = "typesafe/jev-1.13"
ENDPOINT = "https://openrouter.ai/api/alpha/decisions"


def _key():
    for p in (os.path.join(ROOT, ".env"), "/root/.openrouter_key"):
        if os.path.exists(p):
            for line in open(p):
                if line.strip().startswith("OPENROUTER_API_KEY="):
                    return line.strip().split("=", 1)[1].strip("'\"")
    raise RuntimeError("OPENROUTER_API_KEY not found (.env)")


def decide(state, questions, model=MODEL):
    body = json.dumps({"model": model, "state": state,
                       "questions": questions}).encode()
    req = urllib.request.Request(
        ENDPOINT, data=body,
        headers={"Authorization": f"Bearer {_key()}",
                 "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        out = json.load(r)
    out["_pinned_model"] = out.get("model", model)
    return out


def band_noul(p, yes=0.8, no=0.2):
    if p >= yes:
        return "auto"
    if p <= no:
        return "auto-negative"
    return "human"


def band_confidence(conf, auto=0.8, assist=0.5):
    if conf >= auto:
        return "auto"
    if conf >= assist:
        return "confirm"
    return "human"


def record(decision_id, state, questions, answers, action):
    os.makedirs(os.path.join(ROOT, "data", "decisions"), exist_ok=True)
    rec = {"id": decision_id, "state": state, "questions": questions,
           "answers": answers, "action": action}
    path = os.path.join(ROOT, "data", "decisions", decision_id + ".json")
    json.dump(rec, open(path, "w"), indent=1)
    return path
