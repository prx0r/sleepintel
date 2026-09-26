"""Jev policy tests. Pure functions only — no network."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

from jev import band_confidence, band_noul


def test_noul_bands():
    assert band_noul(0.94) == "auto"
    assert band_noul(0.1) == "auto-negative"
    assert band_noul(0.5) == "human"


def test_confidence_bands():
    assert band_confidence(0.9) == "auto"
    assert band_confidence(0.6) == "confirm"
    assert band_confidence(0.3) == "human"


def test_decisions_config_valid():
    import json
    d = json.load(open(os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "jev", "decisions.json")))
    assert d["model"] == "typesafe/jev-1.13"
    prims = {x["primitive"] for x in d["decisions"]}
    assert {"choice", "noul", "score"} <= prims
