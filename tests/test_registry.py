"""Registry tests. No network."""
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_validate_script_passes():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    r = subprocess.run([sys.executable, os.path.join(root, "scripts", "validate.py")],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "56 channels" in r.stdout


def test_every_engine_has_channels():
    import yaml
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data = yaml.safe_load(open(os.path.join(root, "registry", "channels.yaml")))["channels"]
    covered = {e for c in data for e in c["engines"]}
    assert covered == {"E1", "E2", "E3", "E4", "E5", "E6"}
