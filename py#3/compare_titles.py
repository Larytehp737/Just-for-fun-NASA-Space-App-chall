from fastapi import FastAPI
from fastapi.responses import FileResponse
import os

app = FastAPI()

# Path to two sets of tiles
TILES_DIR_1 = "tiles_set_1"
TILES_DIR_2 = "tiles_set_2"

@app.get("/tile/compare/{tile_name_1}/{tile_name_2}")
def compare_tiles(tile_name_1: str, tile_name_2: str):
    """
    Compare two tiles from different sets and return both tiles for A/B comparison.
    """
    tile_path_1 = os.path.join(TILES_DIR_1, tile_name_1)
    tile_path_2 = os.path.join(TILES_DIR_2, tile_name_2)
    
    if os.path.exists(tile_path_1) and os.path.exists(tile_path_2):
        return {"tile_1": FileResponse(tile_path_1), "tile_2": FileResponse(tile_path_2)}
    else:
        return {"error": "One or both tiles not found"}
