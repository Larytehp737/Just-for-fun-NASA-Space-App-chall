from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Modèle pour les options d'affichage
class LayerOptions(BaseModel):
    show_heatmap: bool
    opacity: float

# Variable pour stocker les options de l'utilisateur
current_layer_options = {
    "show_heatmap": True,
    "opacity": 0.5
}

@app.post("/layer/options/")
def update_layer_options(options: LayerOptions):
    """
    Update the layer options for heatmap visibility and opacity.
    """
    global current_layer_options
    current_layer_options["show_heatmap"] = options.show_heatmap
    current_layer_options["opacity"] = options.opacity
    return {"message": "Layer options updated successfully"}

@app.get("/layer/options/")
def get_layer_options():
    """
    Get the current layer options.
    """
    return current_layer_options
