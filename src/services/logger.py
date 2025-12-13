import os
from pathlib import Path
import json

LOG_FILE = Path("src/logs/detections.json")
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)


def append_to_json_file(path: str, new_record: dict):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    data.append(new_record)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
