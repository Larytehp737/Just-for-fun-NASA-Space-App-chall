from __future__ import annotations
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Literal
import io, numpy as np
from PIL import Image, ImageFilter
from .store import load_annotations, save_annotation, clear_annotations

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.mount('/static', StaticFiles(directory='tiles'), name='static')

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
def health(): return {"ok": True}

@app.get('/annotations')
def get_annotations(): return load_annotations()

@app.post('/annotations')
def post_annotation(item: Point | Rect): return save_annotation(item.model_dump())

@app.delete('/annotations')
def delete_annotations(): clear_annotations(); return {"deleted": True}

@app.get('/detect')
def detect(level: int = 0):
    path = 'backend/data/samples/sample.png'
    try:
        im = Image.open(path).convert('L')
    except Exception:
        im = Image.new('L', (512,512), 64)
    scale = max(1, min(8, level))
    w, h = im.size
    im2 = im.resize((max(32,w//scale), max(32,h//scale)))
    lap = im2.filter(ImageFilter.FIND_EDGES)
    arr = np.array(lap, dtype=np.float32)
    arr = (arr - arr.min()) / (arr.ptp()+1e-6)
    arr = (arr*255).astype(np.uint8)
    rgba = np.zeros((arr.shape[0], arr.shape[1], 4), dtype=np.uint8)
    rgba[...,0] = arr
    rgba[...,1] = 0
    rgba[...,2] = 255 - arr
    rgba[...,3] = 128
    out = Image.fromarray(rgba, mode='RGBA')
    buf = io.BytesIO(); out.save(buf, format='PNG')
    return Response(buf.getvalue(), media_type='image/png')
