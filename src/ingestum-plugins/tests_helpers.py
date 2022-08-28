import json
import os

def get_expected(path, script):
    filepath = os.path.join(path, "output", script + ".json")
    with open(filepath, "r") as f:
        expected = json.loads(f.read())
    return expected