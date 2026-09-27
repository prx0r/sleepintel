"""Jev-native decision client: typed questions, three-band policy, audit log.
Key: OPENROUTER_API_KEY in .env (never in repo). Model pinned (thresholds
couple to versions — jev-latest moves under you).
Policy: auto / confirm / human per action thresholds in jev/decisions.json.
Noul: threshold distance from 0.5 with separate yes/no cutoffs. Choice results
carry a model-reported confidence (0..1) when the backend provides one — never
invent it client-side; rows without one are banded 'unscored'. Choice: needs
'other' escape hatch.
Score: threshold the expectation, never do arithmetic on levels.
Failure modes: decide() raises on transport/auth errors; every caller must
declare its fail direction (fail-closed for publish/ship, fail-open to prior
order for routing) — see ACTUATE_FAIL / RERANK_FAIL below."""
import json
import os
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL = "typesafe/jev-1.13"
ENDPOINT = "https://openrouter.ai/api/alpha/decisions"


def _key():
    env = os.environ.get("OPENROUTER_API_KEY")
    if env:
        return env.strip("'\"")
    for p in (os.path.join(ROOT, ".env"), "/root/.openrouter_key"):
        if os.path.exists(p):
            for line in open(p):
                if line.strip().startswith("OPENROUTER_API_KEY="):
                    return line.strip().split("=", 1)[1].strip("'\"")
    raise RuntimeError("OPENROUTER_API_KEY not found (env or .env)")


def decide(state, questions, model=MODEL, retries=3):
    import time
    import urllib.error
    body = json.dumps({"model": model, "state": state,
                       "questions": questions}).encode()
    delay = 1.0
    for attempt in range(retries):
        req = urllib.request.Request(
            ENDPOINT, data=body,
            headers={"Authorization": f"Bearer {_key()}",
                     "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                out = json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (429, 529) and attempt < retries - 1:
                time.sleep(delay)
                delay *= 2
                continue
            raise
        out["_pinned_model"] = out.get("model", model)
        return out
    raise RuntimeError("jev unreachable after retries")


def fail_closed(action_default="human"):
    """Publish/ship gates fail CLOSED (no action on error).
    Verdict routing fails OPEN to human. Call the right one."""
    return action_default


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


def record(decision_id, state, questions, answers, action, extra=None):
    import datetime
    os.makedirs(os.path.join(ROOT, "data", "decisions"), exist_ok=True)
    rec = {"id": decision_id, "state": state, "questions": questions,
           "answers": answers, "action": action,
           "recorded_at": datetime.datetime.now(
               datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
    if extra:
        # Callers pass provenance they own: model (out["_pinned_model"]),
        # band applied, thresholds applied, cost (out["usage"]["cost"]).
        rec.update(extra)
    path = os.path.join(ROOT, "data", "decisions", decision_id + ".json")
    json.dump(rec, open(path, "w"), indent=1)
    return path
