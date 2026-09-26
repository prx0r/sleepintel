"""Template + plugin contract tests. No network."""
import glob
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_nine_templates():
    files = glob.glob(os.path.join(ROOT, "templates", "*.json"))
    assert len(files) == 9


def test_templates_match_schema():
    for fp in glob.glob(os.path.join(ROOT, "templates", "*.json")):
        t = json.load(open(fp))
        assert t["schema_version"] == "sleepintel-template.v1", fp
        for k in ("template_id", "name", "structure", "engines", "created_at"):
            assert k in t, (fp, k)


def test_jev_decisions_present():
    d = json.load(open(os.path.join(ROOT, "jev", "decisions.json")))
    prims = {x["primitive"] for x in d["decisions"]}
    assert {"choice", "noul", "score"} <= prims
