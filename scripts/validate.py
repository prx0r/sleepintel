"""Validate sleepintel registries. No network. Run: python3 scripts/validate.py"""
import os
import sys

try:
    import yaml
except ImportError:
    print("pyyaml needed (pip install pyyaml)")
    sys.exit(2)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINES = {"E1", "E2", "E3", "E4", "E5", "E6"}
READINESS = {"ready", "ready-ish", "intake", "intake-free", "sourcing",
             "compile", "gap", "originals", "produced", "personal",
             "freshness", "verify", "mixed"}


def main():
    with open(os.path.join(ROOT, "registry", "channels.yaml")) as f:
        data = yaml.safe_load(f)["channels"]
    assert len(data) == 56, f"expected 56 channels, got {len(data)}"
    ids = [c["id"] for c in data]
    assert sorted(ids) == list(range(1, 57)), "ids must be 1..56 unique"
    for c in data:
        assert c["engines"], f"channel {c['id']} has no engine"
        assert set(c["engines"]) <= ENGINES, f"channel {c['id']} bad engine"
        assert c["readiness"] in READINESS, f"channel {c['id']} bad readiness"
        assert c["name"] and c["pitch"], f"channel {c['id']} missing name/pitch"
    print(f"registry OK: {len(data)} channels, engines+readiness valid")


if __name__ == "__main__":
    main()
