"""Hypothesis contract tests. No network."""
import glob
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load():
    schema = json.load(open(os.path.join(ROOT, "schemas", "hypothesis.v1.schema.json")))
    files = glob.glob(os.path.join(ROOT, "hypotheses", "*.json"))
    return schema, files


def test_fifteen_hypotheses():
    _, files = load()
    assert len(files) == 15


def test_all_match_schema():
    schema, files = load()
    pat = schema["properties"]["hypothesis_id"]["pattern"]
    statuses = set(schema["properties"]["status"]["enum"])
    for fp in files:
        h = json.load(open(fp))
        assert h["schema_version"] == "sleepintel-hypothesis.v1", fp
        for k in schema["required"]:
            assert k in h, (fp, k)
        assert re.match(pat, h["hypothesis_id"]), fp
        assert h["status"] in statuses, fp
        assert len(h["statement"]) >= 20 and len(h["mechanism"]) >= 20, fp
        assert len(h["predictions"]) >= 1, fp


def test_campaigns_link_parents():
    _, files = load()
    for fp in files:
        h = json.load(open(fp))
        if h["hypothesis_id"].startswith("H-C-"):
            assert h["parent_hypothesis_ids"], fp
