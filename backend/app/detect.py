from __future__ import annotations
import numpy as np
from PIL import Image
from skimage.filters import laplace, gaussian
from skimage.exposure import rescale_intensity

def to_gray(arr: np.ndarray) -> np.ndarray:
    """Convertit RGB/RGBA → L (float32 0..1)."""
    if arr.ndim == 3:
        arr = arr[..., :3]
        arr = 0.2126*arr[...,0] + 0.7152*arr[...,1] + 0.0722*arr[...,2]
    arr = arr.astype(np.float32)
    arr = (arr - arr.min()) / (np.ptp(arr) + 1e-8)
    return arr

def detect_loglike(gray_01: np.ndarray, sigma_low=1.2, sigma_high=2.5) -> np.ndarray:
    """Anomalies par Difference of Gaussians + Laplacien (rapide, robuste)."""
    g1 = gaussian(gray_01, sigma=sigma_low, preserve_range=True)
    g2 = gaussian(gray_01, sigma=sigma_high, preserve_range=True)
    dog = np.abs(g1 - g2)
    lap = np.abs(laplace(gray_01, ksize=3))
    score = 0.6*dog + 0.4*lap
    score = rescale_intensity(score, out_range=(0, 1)).astype(np.float32)
    return score

def colorize_heatmap(score_01: np.ndarray, alpha: int = 160) -> Image.Image:
    """Map simple: bleu→rouge (BGRA)."""
    s = (score_01*255).astype(np.uint8)
    rgba = np.zeros((s.shape[0], s.shape[1], 4), dtype=np.uint8)
    rgba[...,0] = s            # R
    rgba[...,1] = 0            # G
    rgba[...,2] = 255 - s      # B
    rgba[...,3] = alpha        # A
    return Image.fromarray(rgba, mode='RGBA')

def run_detector_on_image_path(src_path: str, level_scale: float = 1.0) -> tuple[Image.Image, dict]:
    """Charge image, redimensionne selon level_scale, calcule heatmap RGBA et stats."""
    im = Image.open(src_path).convert("RGB")
    if level_scale != 1.0:
        w, h = im.size
        im = im.resize((max(8, int(w/level_scale)), max(8, int(h/level_scale))))
    arr = np.asarray(im)
    gray = to_gray(arr)
    score = detect_loglike(gray)
    heat = colorize_heatmap(score, alpha=160)
    stats = {
        "min": float(score.min()),
        "max": float(score.max()),
        "mean": float(score.mean()),
        "std": float(score.std()),
        "width": heat.size[0],
        "height": heat.size[1],
        "scale": level_scale
    }
    return heat, stats
