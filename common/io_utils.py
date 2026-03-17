import json
from pathlib import Path

def load_json(filepath: Path) -> dict:
    if not filepath.exists():
        return {}
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data: dict, filepath: Path) -> None:
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_markdown(filepath: Path) -> str:
    if not filepath.exists():
        return ""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()
