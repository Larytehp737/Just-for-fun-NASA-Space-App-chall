from fastapi import FastAPI
from pydantic import BaseModel
import json
import os

app = FastAPI()

# Dossier où les annotations seront stockées
ANNOTATIONS_FILE = "annotations.json"

# Modèle pour les annotations (point ou rectangle)
class Annotation(BaseModel):
    x: int
    y: int
    width: int = None  # Pour un rectangle
    height: int = None  # Pour un rectangle
    label: str

def save_annotations(annotations):
    """
    Save annotations to a JSON file.
    """
    with open(ANNOTATIONS_FILE, 'w') as f:
        json.dump(annotations, f)

def load_annotations():
    """
    Load annotations from the JSON file.
    """
    if os.path.exists(ANNOTATIONS_FILE):
        with open(ANNOTATIONS_FILE, 'r') as f:
            return json.load(f)
    return []

@app.post("/annotations/")
def add_annotation(annotation: Annotation):
    annotations = load_annotations()
    annotations.append(annotation.dict())
    save_annotations(annotations)
    return {"message": "Annotation added successfully"}

@app.get("/annotations/")
def get_annotations():
    annotations = load_annotations()
    return {"annotations": annotations}
