#!/bin/bash

echo "🚀 Démarrage manuel NASA Space App Challenge"
echo "============================================="

# Vérification des dépendances
echo "📦 Vérification des dépendances..."

# Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 non installé"
    exit 1
fi
echo "✅ Python3 installé"

# Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js non installé"
    exit 1
fi
echo "✅ Node.js installé"

# npm
if ! command -v npm &> /dev/null; then
    echo "❌ npm non installé"
    exit 1
fi
echo "✅ npm installé"

echo ""
echo "🔧 Installation des dépendances..."

# Installation des dépendances Python
echo "🐍 Installation des dépendances Python..."
pip3 install fastapi uvicorn pillow numpy scikit-image requests --break-system-packages

# Installation des dépendances Node.js
echo "🌐 Installation des dépendances Node.js..."
cd embiggen-your-eyes
npm install
cd ..

echo ""
echo "🚀 Démarrage des serveurs..."

# Démarrage du backend en arrière-plan
echo "🐍 Démarrage du backend (port 8000)..."
cd backend
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

# Attendre que le backend démarre
sleep 3

# Démarrage du frontend en arrière-plan
echo "🌐 Démarrage du frontend (port 5173)..."
cd embiggen-your-eyes
npm run dev &
FRONTEND_PID=$!
cd ..

# Attendre que le frontend démarre
sleep 5

echo ""
echo "🎉 APPLICATION DÉMARRÉE !"
echo "========================="
echo "🌐 Frontend: http://localhost:5173"
echo "🐍 Backend: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter les serveurs..."

# Fonction de nettoyage
cleanup() {
    echo ""
    echo "🛑 Arrêt des serveurs..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}

# Capturer Ctrl+C
trap cleanup SIGINT

# Attendre indéfiniment
while true; do
    sleep 1
done
