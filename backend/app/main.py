from __future__ import annotations
from fastapi import FastAPI, Response, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Literal
import io, numpy as np, os, uuid
from PIL import Image, ImageFilter
from pathlib import Path
from .store import load_annotations, save_annotation, clear_annotations
from .detect import run_detector_on_image_path
from .pyramides import generate_deepzoom

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Monte le dossier des tuiles avec un chemin absolu et le crée au besoin
REPO_ROOT = Path(__file__).resolve().parents[2]
TILES_DIR = REPO_ROOT / 'tiles'
TILES_DIR.mkdir(parents=True, exist_ok=True)
app.mount('/static', StaticFiles(directory=str(TILES_DIR)), name='static')

class Point(BaseModel):
    type: Literal['point']
    x: float
    y: float

class Rect(BaseModel):
    type: Literal['rect']
    x: float
    y: float
    w: float
    h: float

@app.get('/health')
def health():
    return {"ok": True}

@app.get('/annotations')
def get_annotations():
    return load_annotations()

@app.post('/annotations')
def post_annotation(item: Point | Rect):
    return save_annotation(item.model_dump())

@app.delete('/annotations')
def delete_annotations():
    clear_annotations()
    return {"deleted": True}

@app.get('/detect')
def detect(level: int = 0):
    """Détection d'anomalies avec les algorithmes avancés de Py#3"""
    sample_path = REPO_ROOT / 'backend' / 'data' / 'samples' / 'sydneyflooding_oli.jpg'
    src = str(sample_path)
    if not sample_path.exists():
        # crée une image synthétique si l'échantillon n'existe pas
        im = Image.new('L', (512, 512), 64)
        arr = np.array(im, dtype=np.float32)
        arr[128:384, 128:384] = 192
        im = Image.fromarray(arr.astype(np.uint8), mode='L')
        buf = io.BytesIO()
        im.save(buf, format='PNG')
        # passe l'image synthétique dans le pipeline simple
        scale = max(1, min(8, level))
        im2 = im.resize((max(32, im.size[0]//scale), max(32, im.size[1]//scale)))
        lap = im2.filter(ImageFilter.FIND_EDGES)
        arr = np.array(lap, dtype=np.float32)
        arr = (arr - arr.min()) / (np.ptp(arr)+1e-6)
        arr = (arr*255).astype(np.uint8)
        rgba = np.zeros((arr.shape[0], arr.shape[1], 4), dtype=np.uint8)
        rgba[...,0] = arr
        rgba[...,1] = 0
        rgba[...,2] = 255 - arr
        rgba[...,3] = 128
        out = Image.fromarray(rgba, mode='RGBA')
        out_buf = io.BytesIO()
        out.save(out_buf, format='PNG')
        return Response(out_buf.getvalue(), media_type='image/png')
    # chemin valide → utilise l'algo avancé
    try:
        heatmap, _ = run_detector_on_image_path(src, level_scale=2**level)
        buf = io.BytesIO()
        heatmap.save(buf, format='PNG')
        return Response(buf.getvalue(), media_type='image/png')
    except Exception:
        # Fallback vers l'ancien algorithme sur le fichier réel
        im = Image.open(src).convert('L')
        scale = max(1, min(8, level))
        w, h = im.size
        im2 = im.resize((max(32,w//scale), max(32,h//scale)))
        lap = im2.filter(ImageFilter.FIND_EDGES)
        arr = np.array(lap, dtype=np.float32)
        arr = (arr - arr.min()) / (np.ptp(arr)+1e-6)
        arr = (arr*255).astype(np.uint8)
        rgba = np.zeros((arr.shape[0], arr.shape[1], 4), dtype=np.uint8)
        rgba[...,0] = arr
        rgba[...,1] = 0
        rgba[...,2] = 255 - arr
        rgba[...,3] = 128
        out = Image.fromarray(rgba, mode='RGBA')
        buf = io.BytesIO()
        out.save(buf, format='PNG')
        return Response(buf.getvalue(), media_type='image/png')

@app.post('/upload')
async def upload_image(file: UploadFile = File(...)):
    """Upload d'une image pour traitement"""
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Le fichier doit être une image")
    
    # Sauvegarde temporaire
    upload_dir = Path("backend/data/uploads")
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    file_id = str(uuid.uuid4())
    file_path = upload_dir / f"{file_id}_{file.filename}"
    
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    return {
        "file_id": file_id,
        "filename": file.filename,
        "path": str(file_path),
        "size": len(content)
    }

@app.post('/generate-tiles')
async def generate_tiles(request: dict):
    """Génération de tuiles DZI pour une image"""
    image_path = request.get("image_path")
    if not image_path or not Path(image_path).exists():
        raise HTTPException(status_code=400, detail="Chemin d'image invalide")
    
    try:
        # Génère les tuiles DZI dans le répertoire monté par /static
        stem = Path(image_path).stem
        output_base = TILES_DIR / stem
        generate_deepzoom(image_path, str(output_base), tile_size=256, suffix=".jpg")
        # Retourne des chemins relatifs à /static pour simplifier le front
        return {
            "success": True,
            "dzi_path": f"{stem}.dzi",
            "tiles_path": f"{stem}_files/"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la génération: {str(e)}")

@app.get('/images')
def list_images():
    """Liste des images disponibles"""
    samples_dir = Path("backend/data/samples")
    uploads_dir = Path("backend/data/uploads")
    
    images = []
    
    # Images d'exemple
    if samples_dir.exists():
        for img_path in samples_dir.glob("*"):
            if img_path.is_file() and img_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.tiff']:
                images.append({
                    "id": img_path.stem,
                    "name": img_path.name,
                    "path": str(img_path),
                    "type": "sample"
                })
    
    # Images uploadées
    if uploads_dir.exists():
        for img_path in uploads_dir.glob("*"):
            if img_path.is_file() and img_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.tiff']:
                images.append({
                    "id": img_path.stem,
                    "name": img_path.name,
                    "path": str(img_path),
                    "type": "uploaded"
                })
    
    return {"images": images}

@app.post('/detect-on-path')
async def detect_on_path(request: dict, level: int = 0):
    """Lance la détection d'anomalies sur un chemin fourni et renvoie une image PNG."""
    image_path = request.get("image_path")
    if not image_path or not Path(image_path).exists():
        raise HTTPException(status_code=400, detail="Chemin d'image invalide")
    try:
        heatmap, _ = run_detector_on_image_path(str(image_path), level_scale=2**level)
        buf = io.BytesIO()
        heatmap.save(buf, format='PNG')
        return Response(buf.getvalue(), media_type='image/png')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur détection: {str(e)}")
