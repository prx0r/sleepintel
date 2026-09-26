"""Emit the idea queue: next slot per channel from its subengine run-mode.
Run: python3 scripts/ideas.py [topN]. Output: ideas/next.json (committed).
Corpus-state (which entry/chapter/word) resolves at brief time; slots are structural."""
import json
import os
import sys

try:
    import yaml
except ImportError:
    print("pyyaml needed")
    sys.exit(2)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLOT = {
    "E1a": "next album evening", "E1b": "next cover rendition",
    "E1c": "next deconstruction", "E1d": "next generated bed",
    "E2a": "next passage reading", "E2c": "next chapter",
    "E3a": "next journey", "E3b": "next embodiment",
    "E4a": "next place loop", "E4b": "next bed recipe",
    "E5a": "next essay", "E5b": "next word", "E5c": "next procedure",
    "E5d": "next entry", "E5e": "next life stage", "E6a": "tonight's brief",
}
READY = {"ready": 3, "ready-ish": 2, "intake-free": 2, "produced": 2,
         "compile": 1, "verify": 1, "mixed": 1, "originals": 1,
         "sourcing": 0, "gap": 0, "freshness": 1, "personal": 0}


def main(n=0):
    data = yaml.safe_load(open(os.path.join(ROOT, "registry", "channels.yaml")))["channels"]
    ideas = [{"channel_id": c["id"], "channel": c["name"], "slot": SLOT.get(c.get("sub"), "next pilot"),
              "engine": c.get("sub"), "readiness_weight": READY.get(c["readiness"], 0)}
             for c in data]
    ideas.sort(key=lambda x: (-x["readiness_weight"], x["channel_id"]))
    if n:
        ideas = ideas[:n]
    os.makedirs(os.path.join(ROOT, "ideas"), exist_ok=True)
    with open(os.path.join(ROOT, "ideas", "next.json"), "w") as f:
        json.dump(ideas, f, indent=1)
    print(f"ideas: {len(ideas)}")


if __name__ == "__main__":
    main(*(int(a) for a in sys.argv[1:2]))
