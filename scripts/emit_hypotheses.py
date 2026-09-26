"""Emit sleepintel hypothesis JSONs (laws + campaigns). Run once, commit output."""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HDIR = os.path.join(ROOT, "hypotheses")
os.makedirs(HDIR, exist_ok=True)

SCHEMA = "sleepintel-hypothesis.v1"


def H(hid, statement, mechanism, predictions, parents=None, channels=None,
      engines=None, status="active"):
    return {
        "schema_version": SCHEMA,
        "hypothesis_id": hid,
        "version": 1,
        "statement": statement,
        "mechanism": mechanism,
        "status": status,
        "parent_hypothesis_ids": parents or [],
        "channel_ids": channels or [],
        "engine_ids": engines or [],
        "predictions": predictions,
        "created_at": "2026-09-26",
    }


def P(pid, claim, metric, threshold, window_days=30):
    return {"id": pid, "claim": claim, "metric": metric,
            "threshold": threshold, "window_days": window_days}


LAWS = [
    H("H-PLACE", "Nobody clicks 'for sleep'; they click where they want to feel like they are. Sleep is how they consume; place is why they click.",
      "Curiosity selects the video; habitation (a room, century, world, proof) removes the need to keep watching, which is what sleep requires.",
      [P("H-PLACE-P1", "place-framed titles beat topic-framed twins on CTR", "ctr_vs_sibling_median", ">1.0x", 30)],
      channels=list(range(1, 57))),
    H("H-ENGINES", "Six engines serve fifty-six channels; a channel is corpus + accent + flavor on a shared engine. No engine is built for one channel.",
      "Production cost amortizes across expressions; new channels cost a brief + a pilot, not a pipeline.",
      [P("H-ENGINES-P1", "pilot cost stays under 2h operator time on built engines", "operator_minutes_per_pilot", "<=120", 30)]),
    H("H-HOST", "Hosted sleep (one voice, one goodnight, irregular soft check-ins) retains better than abandoned sleep.",
      "Recognition + ritual + unpredictable gentle re-anchors give permission to let go; metronomic patterns train anticipation (wakefulness).",
      [P("H-HOST-P1", "hosted episodes hold past 25% more often than unhosted twins", "avd25_rate_vs_control", ">1.0x", 30)],
      engines=["E1"]),
    H("H-HARD", "Difficulty is a lullaby: dense papers/theory sleep people because tracking-load near zero, not because content is simple.",
      "Interesting enough to choose (curiosity), forgiving enough to drift from (no plot to lose).",
      [P("H-HARD-P1", "hard-paper episodes match network retention medians or better", "avd_vs_network_median", ">=1.0x", 30)],
      engines=["E5"]),
    H("H-DATA", "Every pilot emits tracked IDs; verdicts follow metric rules; the queue re-ranks itself. The network is an organism.",
      "Sense (metrics) → decide (promote/iterate/kill/split) → grow (pilots). Dead ends retained as data.",
      [P("H-DATA-P1", "every shipped pilot has a recorded verdict within 45 days", "verdict_coverage", "=100%", 45)]),
]

CAMPAIGNS = [
    H("H-C-SAIVA", "Saiva Slumber wins: zero-competition Tantraloka readings for an audience that cannot be served elsewhere.",
      "Open field + unfilmable-by-others texts + recognition-without-effort philosophy (pratyabhijna).",
      [P("H-C-SAIVA-P1", "pilot CTR beats channel median", "ctr_vs_median", ">1.0x", 14)], ["H-PLACE"], [16], ["E2"], "probation"),
    H("H-C-CORBIN", "Corbin Sleep wins: the imaginal realm is literally sleep-shaped and unfilmed.",
      "13M bench + subject (in-between worlds) that maps 1:1 onto hypnagogia.",
      [P("H-C-CORBIN-P1", "avg view duration clears 25% of runtime", "avd_share", ">=0.25", 30)], ["H-PLACE"], [15], ["E2"], "probation"),
    H("H-C-DAIMON", "Daimon Dreams wins: empty YouTube field + universal guardian fascination + dream-incubation suggestion.",
      "Everyone wants a guide; 'meet your daimon tonight' is suggestion, story, and series in one line.",
      [P("H-C-DAIMON-P1", "searchCTR from 'daimon' queries above network median", "search_ctr", ">median", 30)], ["H-PLACE"], [3], ["E2", "E3"], "probation"),
    H("H-C-ALBUM", "Composer Evenings wins: ritual (same intro, same goodnight) + owned recordings + wedge branding.",
      "Evening grammar turns music into appointment viewing; owned piano removes rights risk entirely.",
      [P("H-C-ALBUM-P1", "return-viewer rate above network median by episode 4", "return_rate", ">median", 60)], ["H-HOST"], [34], ["E1"], "probation"),
    H("H-C-COVERS", "Sleepy Covers wins: most clickable premise (songs you love, asleep) with novelty front-loaded and piano back-filling paid hours.",
      "Talking-head intro is the only novel cost; rendition plays for hours; claims-not-strikes math holds.",
      [P("H-C-COVERS-P1", "CTR top-quartile of network on pilot", "ctr_quartile", "<=Q1", 30)], ["H-PLACE", "H-HOST"], [37], ["E1"], "draft"),
    H("H-C-FAIRY", "Fairy Tales wins: nostalgia + specific tradition beats generic bedtime (683K vs 1.3K precedent).",
      "Known stories bypass the attention gate; foreign seasons compound the library.",
      [P("H-C-FAIRY-P1", "known-tale pilots beat original-tale pilots on CTR", "ctr_known_vs_original", ">1.0x", 30)], ["H-PLACE"], [41, 42], ["E2"], "draft"),
    H("H-C-HARD", "Hard Sleep wins: dual audience (sleepers + intimidated learners), corpus graded and held.",
      "Bub precedent (1.98M calculus); papers are free scripts; whiteboard hand is the host.",
      [P("H-C-HARD-P1", "comments show study-use alongside sleep-use", "study_comment_share", ">10%", 60)], ["H-HARD"], [27, 6], ["E5"], "draft"),
    H("H-C-SINGULARITY", "Quiet Singularity wins: topic of the decade + black-screen-viable cheapest pipeline.",
      "AI Explained demand without sleep form; no visuals needed (content IS narration).",
      [P("H-C-SINGULARITY-P1", "pilot CTR above network median on topic strength alone", "ctr_vs_median", ">1.0x", 14)], ["H-HARD"], [38], ["E5"], "draft"),
    H("H-C-RAIN", "Rain in Weird Places wins: one bed, N skins; sleep + study + work audiences in one.",
      "Cheapest engine per episode; autocomplete-confirmed demand; leave-it-on format.",
      [P("H-C-RAIN-P1", "non-sleep watch share (study/work comments) above 15%", "daytime_share", ">15%", 60)], ["H-PLACE"], [], ["E4"], "draft"),
    H("H-C-HERE", "Fall Asleep Here wins: era+place+journey beats franchise 20x with zero rights thread.",
      "'Sleep in a ___' grammar owned; the room is written, therefore ours.",
      [P("H-C-HERE-P1", "scenario pilots beat franchise-lore pilots on views/day", "views_per_day_ratio", ">5x", 30)], ["H-PLACE"], [], ["E5"], "draft"),
]

for h in LAWS + CAMPAIGNS:
    lat = h["hypothesis_id"]
    with open(os.path.join(HDIR, lat + ".json"), "w") as f:
        json.dump(h, f, indent=1)
print(f"wrote {len(LAWS) + len(CAMPAIGNS)} hypotheses")
