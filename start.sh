#!/bin/bash
set -e

echo "==> Installation et lancement backend"

cd backend

# Créer l'environnement virtuel Python
if [ ! -d "venv" ]; then
  python3 -m venv venv
fi

source venv/bin/activate

# Installer dépendances Python
pip install --upgrade pip
pip install fastapi uvicorn pydantic numpy pillow scikit-image requests

# Créer dossiers nécessaires
mkdir -p data/tiles
mkdir -p data/heatmaps

# Lancer le backend (en arrière-plan)
nohup uvicorn app.main:app --reload > backend.log 2>&1 &

echo "Backend lancé (log dans backend.log)"

echo "==> Installation et lancement frontend"

cd ../frontend

npm install

npm run dev
