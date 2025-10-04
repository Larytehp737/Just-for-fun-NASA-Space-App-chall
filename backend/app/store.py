from __future__ import annotations
import json
from pathlib import Path
from typing import List, Dict, Any
import threading

DATA = Path(__file__).resolve().parent.parent / 'data'
ANN = DATA / 'annotations.json'
DATA.mkdir(parents=True, exist_ok=True)
if not ANN.exists():
    ANN.write_text('[]', encoding='utf-8')

file_lock = threading.Lock()

def load_annotations() -> List[Dict[str, Any]]:
    with file_lock:
        if not ANN.exists():
            return []
        return json.loads(ANN.read_text(encoding='utf-8'))

def save_annotation(item: Dict[str, Any]) -> Dict[str, Any]:
    with file_lock:
        items = load_annotations()
        item['id'] = len(items) + 1
        items.append(item)
        ANN.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding='utf-8')
    return item

def clear_annotations() -> None:
    with file_lock:
        ANN.write_text('[]', encoding='utf-8')
