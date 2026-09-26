"""Fisher: per-channel demand-validation search packs. No new infra.
Reads ideas/next.json, emits queries + what-to-look-for per channel.
Agent runs the searches (websearch tool), files findings to research.
Usage: python3 scripts/fisher.py [topN]"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def pack(channel_id, channel, slot):
    q = channel.lower().replace("sleepy ", "").replace("sleep ", "").strip()
    return {
        "channel_id": channel_id,
        "channel": channel,
        "queries": [f"{q} sleep", f"{q} bedtime", f"{q} relax night"],
        "look_for": ["demand proof (views/subs)", "format gaps",
                     "title grammars to steal", "sourcing leads"],
        "file_to": "docs/SLEEP_RESEARCH_FISHER.md",
    }


def main(n=5):
    ideas = json.load(open(os.path.join(ROOT, "ideas", "next.json")))
    packs = [pack(i["channel_id"], i["channel"], i["slot"]) for i in ideas[:n]]
    print(json.dumps(packs, indent=1))


if __name__ == "__main__":
    main(*(int(a) for a in sys.argv[1:2]))
