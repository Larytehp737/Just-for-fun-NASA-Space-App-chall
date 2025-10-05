from __future__ import annotations
import json, time, os, math, argparse, sys
from pathlib import Path
from typing import Any, Dict, List
from dataclasses import dataclass
from PIL import Image
import traceback

try:
    import psutil
except Exception:
    psutil = None  # mémoire max optionnelle

from .detect import run_detector_on_image_path

DEFAULT_OUT = Path("backend/outputs")

@dataclass
class Job:
    image_id: str
    source: Path
    levels: List[int]
    base_scale: float | None  # si connu (ex: niveau max DZI → 2**n)
    save_png: bool

def load_manifest(p: Path) -> dict:
    with open(p, "r", encoding="utf-8") as f:
        if p.suffix.lower() in (".yml", ".yaml"):
            import yaml  # facultatif si YAML
            return yaml.safe_load(f)
        return json.load(f)

def estimate_level_scale(level: int, ref_level: int | None) -> float:
    """
    Renvoie un facteur 'scale' pour simuler la résolution d’un niveau.
    Si ref_level est fourni, on prend scale = 2**(ref_level - level).
    Par défaut, scale = 2**level (niveau 0 = pleine résolution, 1 = /2, etc.).
    """
    if ref_level is not None:
        return float(2 ** (ref_level - level))
    return float(2 ** level)

def memory_info_mb() -> float | None:
    if psutil is None:
        return None
    proc = psutil.Process(os.getpid())
    return proc.memory_info().rss / (1024*1024)

def run_job(job: Job, outdir: Path, retries: int = 2, backoff: float = 0.7) -> dict:
    outdir.mkdir(parents=True, exist_ok=True)
    results = {"image_id": job.image_id, "source": str(job.source), "levels": []}
    for lv in job.levels:
        attempt, ok = 0, False
        while attempt <= retries and not ok:
            t0 = time.perf_counter()
            mem0 = memory_info_mb()
            err_text = None
            try:
                scale = estimate_level_scale(lv, None if job.base_scale is None else int(job.base_scale))
                heat, stats = run_detector_on_image_path(str(job.source), level_scale=scale)
                # Sauvegardes
                record = {
                    "level": lv,
                    "scale": scale,
                    "stats": stats,
                    "elapsed_ms": None,
                    "mem_mb_before": mem0,
                    "mem_mb_after": None,
                    "error": None,
                    "heatmap_png": None
                }
                if job.save_png:
                    png_path = outdir / f"{job.image_id}_L{lv}.png"
                    heat.save(png_path, "PNG")
                    record["heatmap_png"] = str(png_path)
                # JSON minimal par niveau
                lvl_json = outdir / f"{job.image_id}_L{lv}.json"
                with open(lvl_json, "w", encoding="utf-8") as jf:
                    json.dump({"image_id": job.image_id, "level": lv, "stats": stats}, jf, indent=2, ensure_ascii=False)
                # temps/mémoire
                record["elapsed_ms"] = int((time.perf_counter() - t0)*1000)
                record["mem_mb_after"] = memory_info_mb()
                results["levels"].append(record)
                ok = True
            except Exception as e:
                err_text = "".join(traceback.format_exception(e))
                attempt += 1
                if attempt <= retries:
                    time.sleep(backoff * attempt)  # backoff simple
                if attempt > retries:
                    results["levels"].append({
                        "level": lv,
                        "error": f"Failed after {retries} retries: {str(e)}",
                        "traceback": err_text
                    })
    # journal global
    with open(outdir / f"{job.image_id}_summary.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    return results

def main():
    ap = argparse.ArgumentParser(description="Orchestrateur détection (batch).")
    ap.add_argument("--manifest", type=str, default="backend/manifest.json", help="Chemin manifest JSON/YAML.")
    ap.add_argument("--out", type=str, default=str(DEFAULT_OUT), help="Dossier de sortie.")
    ap.add_argument("--png", action="store_true", help="Sauver heatmap PNG par niveau.")
    ap.add_argument("--retries", type=int, default=2, help="Nombre de retries par niveau.")
    args = ap.parse_args()

    manifest = load_manifest(Path(args.manifest))
    out_root = Path(args.out)
    out_root.mkdir(parents=True, exist_ok=True)

    images: List[Dict[str, Any]] = manifest.get("images", [])
    base_level = manifest.get("base_level")  # optionnel

    all_results = {"jobs": []}
    for it in images:
        job = Job(
            image_id=it["id"],
            source=Path(it["source"]),
            levels=it.get("levels", [0]),
            base_scale=base_level,
            save_png=args.png
        )
        job_dir = out_root / job.image_id
        res = run_job(job, job_dir, retries=args.retries)
        all_results["jobs"].append(res)

    with open(out_root / "batch_summary.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)

    print("✅ Orchestration terminée. Résultats dans:", out_root.resolve())

if __name__ == "__main__":
    main()
