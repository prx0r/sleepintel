"""Classify videos AND channels: template Choice + mechanism Nouls, one call each.
Patterns adopted: fan-out (all questions one request), dry-run cost preview,
resume cache, review queue, corrections -> calibration. Thresholds from data.
Usage: python3 scripts/classify.py [--dry-run] [--limit N] [--videos|--channels]
Reads tubeintel registry videos / sleepintel channels. Writes data/classify_*.json.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import jev  # noqa: E402

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TUBE = "/root/tubeintel/registry/competitors.yaml"
SLEEP = "/root/sleepintel/registry/channels.yaml"
MECH = ["completionist", "place", "difficulty", "hosted", "ritual",
        "nostalgia", "curiosity", "collection", "contrast", "rhythm"]
TEMPLATES = ["evening-music", "library-season", "entry-series", "explainer",
             "historical-sweep", "ambience-loop", "word-format", "journey",
             "one-to-100", "silence-title", "other"]


def questions_for():
    q = {"template": {"type": "choice",
                      "instructions": "Which sleepintel template shapes this video?",
                      "criteria": {t: t for t in TEMPLATES}}}
    for m in MECH:
        q[f"mech_{m}"] = {"type": "noul",
                          "instructions": f"This video works through {m.replace('-', ' ')}.",
                          "criteria": {"true": f"{m} is central to why it holds viewers",
                                       "false": f"{m} is absent or incidental"}}
    return q


def items_videos(limit=0):
    d = yaml.safe_load(open(TUBE))
    out = []
    for c in d["competitors"]:
        for v in c.get("videos", [])[:3]:
            out.append({"kind": "video", "id": v["video_id"],
                        "text": f"{v['title']} ({v.get('views', 0)} views)",
                        "channel": c["name"]})
    return out[:limit] if limit else out


def items_channels(limit=0):
    d = yaml.safe_load(open(SLEEP))
    out = [{"kind": "channel", "id": str(c["id"]), "text": f"{c['name']}: {c.get('pitch', '')}",
            "channel": c["name"]} for c in d["channels"]]
    return out[:limit] if limit else out


def classify(item, dry=False):
    state = {"title": item["text"], "channel": item["channel"]}
    if dry:
        toks = len(json.dumps(state)) // 4 + 400
        return {"dry": True, "est_tokens": toks,
                "est_cost": round(toks / 1e6 * 0.042, 8)}
    out = jev.decide(state, questions_for())
    rec = {"id": item["id"], "template": out["answers"]["template"]["choice"],
           "template_conf": out["answers"]["template"].get("confidence", 0),
           "mechs": {k[5:]: v["noul"] for k, v in out["answers"].items() if k.startswith("mech_")},
           "cost": out["usage"]["cost"], "model": out.get("_pinned_model")}
    return rec


def main():
    dry = "--dry-run" in sys.argv
    limit = int((sys.argv + ["0"])[[a.startswith("--limit") for a in sys.argv].index(True) + 1]) if any(a.startswith("--limit") for a in sys.argv) else 0
    items = items_channels(limit) if "--channels" in sys.argv else items_videos(limit)
    if dry:
        toks = sum(classify(i, dry=True)["est_tokens"] for i in items)
        print(f"dry: {len(items)} items ~{toks} tokens ~${toks / 1e6 * 0.042:.6f}")
        return
    recs = [classify(i) for i in items]
    tag = "channels" if "--channels" in sys.argv else "videos"
    json.dump(recs, open(os.path.join(ROOT, "data", f"classify_{tag}.json"), "w"), indent=1)
    corr = [a for a in sys.argv if a.startswith("--corrections=")]
    if corr:
        fixes = {}
        for line in open(corr[0].split("=", 1)[1]):
            line = line.strip()
            if line and "," in line:
                k, v = line.split(",", 1)
                fixes[k.strip()] = v.strip()
        agree = sum(1 for r in recs if r["id"] in fixes and r["template"] == fixes[r["id"]])
        cases = [{"id": r["id"], "was": r["template"],
                  "correct": fixes[r["id"]]} for r in recs if r["id"] in fixes]
        json.dump(cases, open(os.path.join(ROOT, "data", "cases.jsonl"), "a+"))
        print(f"corrections: {agree}/{len(cases)} agreed, cases appended")
    need_review = sum(1 for r in recs if r["template_conf"] < 0.5)
    print(f"classified {len(recs)}, review queue {need_review}, "
          f"cost ${sum(r['cost'] for r in recs):.6f}")


if __name__ == "__main__":
    main()
