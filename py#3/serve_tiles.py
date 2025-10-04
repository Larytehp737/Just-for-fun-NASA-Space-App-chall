from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import os

app = FastAPI()

# Dossier où les tuiles sont stockées
TILES_DIR = "tiles"

@app.get("/tile/{tile_name}")
def get_tile(tile_name: str):
    tile_path = os.path.join(TILES_DIR, tile_name)
    if os.path.exists(tile_path):
        return FileResponse(tile_path)
    else:
        raise HTTPException(status_code=404, detail="Tile not found")
