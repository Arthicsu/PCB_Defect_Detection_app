from pathlib import Path
import json, zipfile, os

LOG_FILE = Path("src/logs/detections.json")

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

def build_zip(zip_path: Path, images_dir: Path, log_path: Path):
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        if log_path.exists():
            zipf.write(log_path, arcname="detections_logs.json")

        for img in images_dir.glob("pred_*"):
            zipf.write(img, arcname=f"uploads/{img.name}")
        zipf.close()

def iterfile(path: Path):
    with open(path, "rb") as p:
        while chunk := p.read(1024*1024):
            yield chunk

def remove_file(path: Path):
    try:
        if path.exists():
            path.unlink()
    except Exception as e:
        print(f"Ошибка удаления {path}: {e}")