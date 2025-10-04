# Prétraitement & Génération de Tuiles (Py#2)

## 📌 Objectif

Ce module prépare les images (PNG, JPG, TIFF) en **pyramides de tuiles DeepZoom (DZI)**.
Il permet :

* un **zoom fluide jusqu’au pixel** dans OpenSeadragon,
* une intégration facile avec le backend (FastAPI, Py#1),
* une base pour les algorithmes de détection (Py#3).

---

## ⚙️ Prérequis

Installer les dépendances dans l’environnement virtuel :

```bash
pip install pyvips pillow
```

(Sous Debian/Ubuntu, il faut aussi : `sudo apt install libvips libvips-tools`)

---

## 🚀 Génération de tuiles

Exemple minimal en Python:

```python
import pyvips

# Charger une image (png, jpg, tif, etc.)
image = pyvips.Image.new_from_file("image.png", access="sequential")

# Générer la pyramide DeepZoom
image.dzsave(
    "slide",                   # sort -> slide.dzi + slide_files/
    tile_size=32,             # taille standard des tuiles (256) mais j'utilise 32 pour un zoom plus fluide
    overlap=0,                 # pas de recouvrement
    suffix=".jpg[Q=90]"        # format JPG qualité 90
)
```

Options :

* `tile_size=256` → valeur standard (bonne perf)
* `tile_size=32` → zoom plus fluide mais plus de fichiers
* `suffix=".png"` → si besoin sans compression

---

## 📂 Structure de sortie

Après génération, on obtient :

```
slide.dzi              # fichier XML (descripteur)
slide_files/           # dossier des tuiles
  ├── 0/               # niveau min
  ├── 1/
  ├── ...
  └── N/               # niveau max (pleine résolution)
```

---

## 🖥️ Test rapide avec OpenSeadragon

1. Créer un fichier `test.html` :

```html
<!DOCTYPE html>
<html>
<head>
    <title>Test OpenSeadragon</title>
    <script src="https://openseadragon.github.io/openseadragon/openseadragon.min.js"></script>
</head>
<body>
    <div id="viewer" style="width: 100%; height: 90vh;"></div>
    <script>
        var viewer = OpenSeadragon({
            id: "viewer",
            prefixUrl: "https://openseadragon.github.io/openseadragon/images/",
            tileSources: "slide.dzi",
            maxZoomPixelRatio: 1,
            visibilityRatio: 1
        });
    </script>
</body>
</html>
```

2. Lancer un serveur local :

```bash
python3 -m http.server 8000
```

3. Ouvrir dans le navigateur :
   👉 [http://localhost:8000/test.html](http://localhost:8000/test.html)

---