from __future__ import annotations
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Literal
import io
import numpy as np
from PIL import Image, ImageFilter
from pathlib import Path
from .store import load_annotations, save_annotation, clear_annotations

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class CacheStaticFiles(StaticFiles):
    async def get_response(self, path, scope):
        response = await super().get_response(path, scope)
        response.headers["Cache-Control"] = "public, max-age=86400"
        return response

# Monter les tuiles Deep Zoom
app.mount('/tiles', CacheStaticFiles(directory='backend/data/tiles'), name='tiles')

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

@app.get('/api/images')
def list_images():
    tiles_dir = Path('backend/data/tiles')
    if not tiles_dir.exists():
        return {"images": []}
    images = [p.name for p in tiles_dir.iterdir() if p.is_dir()]
    return {"images": images}

@app.get('/detect')
def detect(image_id: str = "sample", level: int = 0):
    heatmap_path = Path(f'backend/data/heatmaps/{image_id}/{level}.png')
    if heatmap_path.exists():
        return FileResponse(heatmap_path, media_type='image/png')

    path = f'backend/data/samples/{image_id}.png'
    try:
        im = Image.open(path).convert('L')
    except Exception:
        im = Image.new('L', (512,512), 64)

    scale = max(1, min(8, level))
    w, h = im.size
    im2 = im.resize((max(32, w // scale), max(32, h // scale)))
    lap = im2.filter(ImageFilter.FIND_EDGES)
    arr = np.array(lap, dtype=np.float32)
    arr = (arr - arr.min()) / (arr.ptp() + 1e-6)
    arr = (arr * 255).astype(np.uint8)
    rgba = np.zeros((arr.shape[0], arr.shape[1], 4), dtype=np.uint8)
    rgba[..., 0] = arr
    rgba[..., 1] = 0
    rgba[..., 2] = 255 - arr
    rgba[..., 3] = 128
    out = Image.fromarray(rgba, mode='RGBA')
    buf = io.BytesIO()
    out.save(buf, format='PNG')
    return Response(buf.getvalue(), media_type='image/png')
