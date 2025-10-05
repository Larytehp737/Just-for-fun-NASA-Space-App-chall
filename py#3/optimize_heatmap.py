import numba
import numpy as np

@numba.jit(nopython=True)
def optimize_heatmap(heatmap):
    """
    Optimise la génération de la heatmap en utilisant Numba pour une exécution rapide.
    """
    return np.log(heatmap + 1)  # Exemple d'opération pour améliorer la chaleur de la heatmap
