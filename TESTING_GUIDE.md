# 🧪 Guide de Test - NASA Space App Challenge "Embiggen Your Eyes"

## 📋 Vue d'ensemble

Ce guide vous explique comment tester l'application complète développée pour le hackathon NASA Space Apps Challenge. L'application permet de visualiser et analyser des images spatiales haute résolution avec détection d'anomalies.

## 🏗️ Architecture

```
Frontend (React + OpenSeadragon) ←→ Backend (FastAPI) ←→ Algorithmes (Py#3)
                ↓                           ↓                    ↓
        Interface utilisateur        API REST + Storage    Détection d'anomalies
                ↓                           ↓                    ↓
        Visualisation DZI            Gestion annotations   Heatmaps + LoG/DoG
```

## 🚀 Démarrage Rapide

### Option 1: Script Automatique (Recommandé)
```bash
# Clone le repository
git clone <votre-repo>
cd Just-for-fun-NASA-Space-App-chall

# Exécute tous les tests et démarre les serveurs
python run_tests.py
```

### Option 2: Démarrage Manuel

#### 1. Backend (Python/FastAPI)
```bash
cd backend
pip install -e .
pip install pytest pytest-asyncio httpx
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

#### 2. Frontend (React/TypeScript)
```bash
cd embiggen-your-eyes
npm install
npm run dev
```

## 🧪 Tests Disponibles

### 1. Tests Backend
```bash
cd backend
python -m pytest tests/ -v
```

**Tests inclus :**
- ✅ Tests des endpoints API (`test_main.py`)
- ✅ Tests des algorithmes de détection (`test_detect.py`)
- ✅ Tests de génération de tuiles (`test_pyramides.py`)
- ✅ Tests de l'orchestrateur (`test_orchestrator.py`)

### 2. Tests Frontend
```bash
cd embiggen-your-eyes
npm run lint
npm run build
```

### 3. Tests d'Intégration
Le script `run_tests.py` exécute automatiquement :
- ✅ Vérification des dépendances
- ✅ Installation des packages
- ✅ Tests unitaires backend
- ✅ Démarrage des serveurs
- ✅ Tests des endpoints
- ✅ Tests de communication frontend-backend

## 🔍 Tests Manuels

### 1. Interface Web
1. Ouvrez http://localhost:5173
2. Testez l'upload d'image
3. Vérifiez la visualisation OpenSeadragon
4. Testez les annotations
5. Vérifiez le mode sombre/clair

### 2. API Backend
1. Ouvrez http://localhost:8000/docs (Swagger UI)
2. Testez les endpoints :
   - `GET /health` - Vérification santé
   - `GET /annotations` - Liste annotations
   - `POST /annotations` - Ajout annotation
   - `GET /detect?level=0` - Détection anomalies
   - `GET /images` - Liste images disponibles

### 3. Algorithmes de Détection
```bash
cd backend
python -c "
from app.detect import run_detector_on_image_path
heatmap, stats = run_detector_on_image_path('data/samples/sample.png')
print('Stats:', stats)
heatmap.save('test_heatmap.png')
"
```

### 4. Génération de Tuiles
```bash
cd backend
python -c "
from app.pyramides import generate_deepzoom
generate_deepzoom('data/samples/sample.png', 'output/test_tiles')
"
```

## 📊 Métriques de Performance

### Backend
- **Temps de réponse API** : < 500ms
- **Détection d'anomalies** : < 2s pour image 1MP
- **Génération tuiles** : < 30s pour image 10MP

### Frontend
- **Temps de chargement** : < 3s
- **Zoom fluide** : 60fps
- **Mémoire utilisée** : < 100MB

## 🐛 Dépannage

### Problèmes Courants

#### 1. Erreur "Module not found"
```bash
# Réinstalle les dépendances
cd backend && pip install -e .
cd ../embiggen-your-eyes && npm install
```

#### 2. Port déjà utilisé
```bash
# Trouve le processus utilisant le port
lsof -i :8000  # Backend
lsof -i :5173  # Frontend

# Tue le processus
kill -9 <PID>
```

#### 3. Erreur OpenSeadragon
```bash
# Vérifie l'installation
cd embiggen-your-eyes
npm list openseadragon
```

#### 4. Erreur pyvips
```bash
# Ubuntu/Debian
sudo apt install libvips libvips-tools

# macOS
brew install vips

# Windows
# Télécharge depuis https://libvips.github.io/libvips/install.html
```

### Logs de Debug

#### Backend
```bash
# Active les logs détaillés
cd backend
python -m uvicorn app.main:app --log-level debug
```

#### Frontend
```bash
# Active le mode debug
cd embiggen-your-eyes
npm run dev -- --debug
```

## 📈 Tests de Charge

### Test API avec Artillery
```bash
# Installe Artillery
npm install -g artillery

# Crée un test de charge
cat > load_test.yml << EOF
config:
  target: 'http://localhost:8000'
  phases:
    - duration: 60
      arrivalRate: 10
scenarios:
  - name: "Test détection"
    requests:
      - get:
          url: "/detect?level=0"
EOF

# Exécute le test
artillery run load_test.yml
```

## 🔧 Configuration Avancée

### Variables d'Environnement
```bash
# Backend
export FASTAPI_ENV=development
export LOG_LEVEL=debug

# Frontend
export REACT_APP_API_URL=http://localhost:8000
export REACT_APP_DEBUG=true
```

### Configuration des Tests
```bash
# Tests avec couverture
cd backend
pip install pytest-cov
python -m pytest tests/ --cov=app --cov-report=html

# Tests en parallèle
pip install pytest-xdist
python -m pytest tests/ -n auto
```

## 📝 Rapport de Tests

Après exécution des tests, vous devriez voir :

```
✅ Dépendances vérifiées
✅ Backend installé et testé
✅ Frontend installé et testé
✅ Serveurs démarrés
✅ Endpoints fonctionnels
✅ Communication frontend-backend OK
✅ Tests d'intégration réussis

🌐 Frontend: http://localhost:5173
🐍 Backend: http://localhost:8000
📚 API Docs: http://localhost:8000/docs
```

## 🎯 Critères de Succès

- [ ] Tous les tests unitaires passent
- [ ] Interface web responsive et fonctionnelle
- [ ] API REST complète et documentée
- [ ] Algorithmes de détection performants
- [ ] Génération de tuiles DZI fonctionnelle
- [ ] Intégration frontend-backend fluide
- [ ] Gestion d'erreurs robuste
- [ ] Performance acceptable (< 3s chargement)

## 🚀 Déploiement

### Production
```bash
# Build frontend
cd embiggen-your-eyes
npm run build

# Serveur production
cd backend
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Docker
```bash
# Build et run avec Docker
docker-compose up --build
```

---

**🎉 Félicitations ! Votre application NASA Space App Challenge est prête !**
