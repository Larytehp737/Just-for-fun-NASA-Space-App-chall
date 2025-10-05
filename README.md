# 🚀 NASA Space App Challenge - "Embiggen Your Eyes"

> **Transformez l'exploration spatiale en une expérience collaborative et intelligente**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![React](https://img.shields.io/badge/React-18.2.0-blue.svg)](https://reactjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com)
[![OpenSeadragon](https://img.shields.io/badge/OpenSeadragon-4.1.0-orange.svg)](https://openseadragon.github.io)

## 🎯 Vision du Projet

Notre application révolutionne l'exploration des images spatiales NASA en permettant aux utilisateurs de **zoomer jusqu'au pixel**, **détecter des anomalies** et **collaborer en temps réel** sur des découvertes scientifiques.

### 🌟 Fonctionnalités Principales

- 🔍 **Zoom fluide** sur des images de milliards de pixels avec OpenSeadragon
- 🤖 **Détection d'anomalies** avec algorithmes avancés (LoG, DoG, entropie texture)
- 📝 **Annotations collaboratives** en temps réel
- 🎨 **Interface moderne** avec React + TypeScript + Tailwind CSS
- ⚡ **API REST** performante avec FastAPI
- 🧪 **Tests complets** et intégration continue

## 👥 Équipe de Développement

| Rôle | Responsabilités | Technologies |
|------|----------------|--------------|
| **🌐 Dev Web (Lead Front)** | Interface utilisateur, OpenSeadragon, intégration API | React, TypeScript, OpenSeadragon, Tailwind CSS |
| **🐍 Dev Py#1 (Backend Lead)** | API REST, gestion fichiers, endpoints | FastAPI, Python, Pydantic |
| **🔧 Dev Py#2 (Prétraitement)** | Pipeline pyramide de tuiles, conversion images | pyvips, PIL, DeepZoom |
| **🔍 Dev Py#3 (Détection)** | Algorithmes de détection, heatmaps | scikit-image, numpy, OpenCV |
| **⚡ Dev C/Py#4 (Perf & Glue)** | Tests, orchestration, intégration | pytest, Docker, CI/CD |

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   Algorithmes   │
│   React + TS    │◄──►│   FastAPI       │◄──►│   Détection     │
│   OpenSeadragon │    │   REST API      │    │   LoG/DoG/ML    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Interface     │    │   Gestion       │    │   Heatmaps      │
│   Utilisateur   │    │   Annotations   │    │   & Analytics   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
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

#### Backend (Python/FastAPI)
```bash
cd backend
pip install -e .
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

#### Frontend (React/TypeScript)
```bash
cd embiggen-your-eyes
npm install
npm run dev
```

## 🧪 Tests et Démonstration

### Tests Automatiques
```bash
# Tests backend
cd backend && python -m pytest tests/ -v

# Tests frontend
cd embiggen-your-eyes && npm run lint && npm run build

# Tests d'intégration complets
python run_tests.py
```

### Démonstration Interactive
```bash
# Lance la démonstration de toutes les fonctionnalités
python demo.py
```

## 📊 Fonctionnalités Développées

### ✅ Travail du Dev Web (Lead Front)
- **Interface moderne** avec React 18 + TypeScript
- **Composants UI avancés** : ImageUploader, ImageViewer, Navbar
- **Intégration OpenSeadragon** pour zoom fluide
- **Système d'annotations** avec overlays interactifs
- **API client** avec axios
- **Animations** avec Framer Motion

### ✅ Travail du Dev Py#1 (Backend Lead)
- **API FastAPI** avec CORS configuré
- **Endpoints complets** : annotations, détection, upload
- **Gestion des fichiers** statiques et uploads
- **Système de stockage** JSON pour annotations
- **Documentation automatique** avec Swagger

### ✅ Travail du Dev Py#2 (Prétraitement/Imagerie)
- **Génération de tuiles DZI** avec pyvips
- **Pipeline de conversion** pour différents formats
- **Configuration flexible** (taille tuiles, qualité)
- **Documentation complète** du processus

### ✅ Travail du Dev Py#3 (Détection/Anomalies)
- **Algorithmes avancés** : LoG, DoG, entropie texture
- **Système de heatmap** avec colorisation
- **Orchestrateur batch** pour traitement multiple
- **Gestion des niveaux** de résolution
- **Métriques de performance** (temps, mémoire)

### ✅ Travail du Dev C/Py#4 (Perf & Glue)
- **Tests unitaires complets** (pytest)
- **Tests d'intégration** automatisés
- **Script d'orchestration** complet
- **Documentation** et guides de test
- **Correction des erreurs** et intégration

## 🔧 Corrections et Améliorations Apportées

### 🐛 Erreurs Corrigées
- ✅ **OpenSeadragon manquant** dans les dépendances frontend
- ✅ **Endpoints API** non alignés entre frontend et backend
- ✅ **Algorithmes de détection** non intégrés dans l'API
- ✅ **Gestion d'erreurs** améliorée
- ✅ **Tests manquants** ajoutés

### 🚀 Améliorations Ajoutées
- ✅ **Endpoints API** complets (upload, génération tuiles, liste images)
- ✅ **Tests unitaires** pour tous les modules
- ✅ **Script d'intégration** automatisé
- ✅ **Documentation** complète
- ✅ **Démonstration** interactive

## 🌐 URLs d'Accès

Une fois les serveurs démarrés :

- **🌐 Frontend** : http://localhost:5173
- **🐍 Backend API** : http://localhost:8000
- **📚 Documentation API** : http://localhost:8000/docs
- **🔍 Interface Swagger** : http://localhost:8000/redoc

## 🧪 Comment Tester

### 1. Tests Automatiques
```bash
# Script complet (recommandé)
python run_tests.py

# Tests individuels
cd backend && python -m pytest tests/ -v
cd embiggen-your-eyes && npm test
```

### 2. Tests Manuels
1. **Interface Web** : Ouvrez http://localhost:5173
2. **Upload d'image** : Testez le drag & drop
3. **Zoom fluide** : Utilisez la molette pour zoomer
4. **Annotations** : Cliquez pour ajouter des annotations
5. **API** : Testez les endpoints sur http://localhost:8000/docs

### 3. Démonstration
```bash
python demo.py
```

## 🚀 Approches Innovantes Proposées

### 🤖 Intelligence Artificielle
- **Détection multi-algorithmes** avec fusion intelligente
- **Apprentissage automatique** adaptatif
- **Prédiction d'anomalies** basée sur l'historique

### 🌐 Collaboration Temps Réel
- **Annotations collaboratives** avec WebSocket
- **Système de validation** communautaire
- **Gamification** des contributions

### 🎮 Interface Immersive
- **Mode VR/AR** avec WebXR
- **Navigation gestuelle** et contrôles vocaux
- **Eye tracking** pour navigation par regard

### 📊 Analytics Avancées
- **Dashboard scientifique** avec métriques
- **Analyse temporelle** des changements
- **Intégration données externes** (météo, satellites)

## 📁 Structure du Projet

```
Just-for-fun-NASA-Space-App-chall/
├── 🌐 embiggen-your-eyes/          # Frontend React + TypeScript
│   ├── src/components/             # Composants UI
│   ├── src/api/                    # Client API
│   └── package.json                # Dépendances Node.js
├── 🐍 backend/                     # Backend FastAPI
│   ├── app/                        # Code Python
│   │   ├── main.py                 # API FastAPI
│   │   ├── detect.py               # Algorithmes détection
│   │   ├── pyramides.py            # Génération tuiles
│   │   └── orchestrator.py         # Orchestration batch
│   ├── tests/                      # Tests unitaires
│   └── pyproject.toml              # Dépendances Python
├── 🔬 py#3/                        # Scripts algorithmes avancés
├── 📚 scripts/                     # Scripts utilitaires
├── 🧪 run_tests.py                 # Script d'intégration
├── 🎭 demo.py                      # Démonstration interactive
├── 📖 TESTING_GUIDE.md             # Guide de test complet
└── 🚀 INNOVATIVE_FEATURES.md       # Approches innovantes
```

## 🎯 Critères de Succès

- [x] **Interface utilisateur** moderne et responsive
- [x] **Zoom fluide** sur images haute résolution
- [x] **Détection d'anomalies** performante
- [x] **API REST** complète et documentée
- [x] **Tests complets** et automatisés
- [x] **Intégration** frontend-backend fluide
- [x] **Documentation** complète
- [x] **Démonstration** interactive

## 🏆 Impact et Valeur

### Pour la Communauté Scientifique
- **Démocratisation** de l'analyse spatiale
- **Accélération** des découvertes
- **Collaboration** internationale

### Pour la NASA
- **Engagement public** accru
- **Données crowdsourcées** de qualité
- **Innovation** dans l'analyse d'images

### Pour les Utilisateurs
- **Expérience immersive** unique
- **Apprentissage** interactif
- **Contribution** à la science

## 🔮 Roadmap Future

### Phase 1 (Immédiate) - MVP Amélioré ✅
- [x] Intégration des algorithmes avancés
- [x] Interface utilisateur optimisée
- [x] Tests complets et documentation

### Phase 2 (Court terme) - Intelligence
- [ ] Système de machine learning
- [ ] Collaboration en temps réel
- [ ] Analytics dashboard

### Phase 3 (Moyen terme) - Immersion
- [ ] Mode VR/AR
- [ ] Contrôles gestuels
- [ ] Visualisations 3D

### Phase 4 (Long terme) - Écosystème
- [ ] Intégration APIs externes
- [ ] Outils scientifiques avancés
- [ ] Plateforme communautaire

## 📞 Support et Contribution

- **🐛 Issues** : Signalez les bugs via GitHub Issues
- **💡 Suggestions** : Proposez des améliorations
- **🤝 Contributions** : Pull requests bienvenues
- **📧 Contact** : Équipe NASA Space App Challenge

## 📄 Licence

Ce projet est développé dans le cadre du **NASA Space Apps Challenge 2024** sous licence MIT.

---

**🌟 "L'avenir de l'exploration spatiale est collaboratif, intelligent et accessible à tous."**

*Développé avec ❤️ par une équipe de 5 développeurs passionnés pour le hackathon NASA Space Apps Challenge*
