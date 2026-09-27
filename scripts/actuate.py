"""Actuator: queue -> Jev gate -> brief. The non-theatre joint.
Reads ideas/next.json order, gates the top idea (promote Choice auto>=0.75),
on pass writes data/queue/<id>.brief.json (channel, template, variant, title
seed, sources) for the render side (sleepvids-compatible shape).
Fail-closed: no pass, no brief, queue untouched. Logs to data/decisions/.
Usage: python3 scripts/actuate.py [--dry-run]"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import jev  # noqa: E402
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    dry = "--dry-run" in sys.argv
    ideas = json.load(open(os.path.join(ROOT, "ideas", "next.json")))
    top = ideas[0]
    reg = yaml.safe_load(open(os.path.join(ROOT, "registry", "channels.yaml")))["channels"]
    ch = next(c for c in reg if c["id"] == top["channel_id"])
    out = jev.decide(
        {"idea": top, "channel": {"name": ch["name"], "pitch": ch.get("pitch", ""),
                                  "readiness": ch["readiness"], "engines": ch["engines"]}},
        {"go": {"type": "choice",
                "instructions": "Promote this pilot to render, iterate it, or kill it?",
                "criteria": {"promote": "corpus verified, EV above queue median",
                             "iterate": "one named variable would fix it",
                             "kill": "no corpus or failed twice",
                             "other": "none fit — human decides"}}})
    ans = out["answers"]["go"]
    jev.record("actuate-" + str(top["channel_id"]), {"idea": top},
               {"go": "choice"}, out["answers"], ans["choice"])
    print(f"gate: {ans['choice']} conf={ans.get('confidence', 0):.2f} cost={out['usage']['cost']}")
    if ans["choice"] != "promote" or ans.get("confidence", 0) < 0.75:
        print("HELD: no brief written (fail-closed)")
        return
    slug = ch["name"].lower().replace(" ", "_")
    mechs = [t.split("-", 1)[1] for t in ch.get("tags", []) if t.startswith("mech-")]
    topic = ch["name"].replace(" Sleep", "").replace("Sleepy ", "")
    brief = {"video_id": f"video:{slug}:001", "channel": f"channel:{slug}",
             "title": f"{ch.get('pitch', ch['name'])}",
             "voice": (ch.get("style") or {}).get("voice") or "voice:lecturer",
             "pace": -0.3, "mechanism": [f"mechanism:{m}" for m in mechs],
             "shelf": f"shelf:{ch['shelf'].lower()}", "engine": ch.get("sub", ""),
             "status": "briefed",
             "seo": {"primary_keyword": f"{topic} sleep",
                     "tags": [topic, "sleep", "deep sleep", "fall asleep", "explained slowly"],
                     "hashtags": ["#sleep", f"#{topic.replace(' ', '')}", "#deepsleep"]},
             "sources": [], "script": None,
             "gated_by": out.get("_pinned_model")}
    if dry:
        print("dry-run, brief would be:", json.dumps(brief)[:200])
        return
    os.makedirs(os.path.join(ROOT, "data", "queue"), exist_ok=True)
    json.dump(brief, open(os.path.join(ROOT, "data", "queue", f"{ch['id']:03d}.brief.json"), "w"), indent=1)
    print("brief written")


if __name__ == "__main__":
    main()
