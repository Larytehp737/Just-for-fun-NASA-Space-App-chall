# 🚀 Guide de Démarrage Rapide - NASA Space App Challenge

## 🎯 Démarrage en 3 Étapes

### Option 1: Script Automatique (Recommandé)
```bash
python3 quick_start.py
```

### Option 2: Script Bash
```bash
./start_manual.sh
```

### Option 3: Démarrage Manuel

#### 1. Installation des Dépendances
```bash
# Dépendances Python
pip3 install fastapi uvicorn pillow numpy scikit-image requests --break-system-packages

# Dépendances Node.js
cd embiggen-your-eyes
npm install
cd ..
```

#### 2. Démarrage des Serveurs

**Terminal 1 - Backend:**
```bash
cd backend
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd embiggen-your-eyes
npm run dev
```

## 🌐 Accès à l'Application

Une fois les serveurs démarrés :

- **🌐 Frontend** : http://localhost:5173
- **🐍 Backend API** : http://localhost:8000
- **📚 Documentation API** : http://localhost:8000/docs

## 🧪 Test Rapide

1. **Ouvrez** http://localhost:5173
2. **Uploadez** une image
3. **Testez** le zoom avec la molette
4. **Ajoutez** des annotations en cliquant
5. **Consultez** l'API sur http://localhost:8000/docs

## 🐛 Résolution de Problèmes

### Erreur "externally-managed-environment"
```bash
# Utilisez --break-system-packages
pip3 install fastapi uvicorn pillow numpy scikit-image requests --break-system-packages
```

### Port déjà utilisé
```bash
# Trouvez le processus
lsof -i :8000  # Backend
lsof -i :5173  # Frontend

# Tuez le processus
kill -9 <PID>
```

### Dépendances manquantes
```bash
# Ubuntu/Debian
sudo apt install python3-pip nodejs npm

# macOS
brew install python node npm
```

## 🎉 Fonctionnalités Disponibles

- ✅ **Interface moderne** avec React + TypeScript
- ✅ **Upload d'images** par drag & drop
- ✅ **Zoom fluide** avec OpenSeadragon
- ✅ **Détection d'anomalies** automatique
- ✅ **Système d'annotations** interactif
- ✅ **API REST** complète et documentée
- ✅ **Mode sombre/clair** toggle

## 📞 Support

Si vous rencontrez des problèmes :
1. Vérifiez que Python 3.8+ et Node.js sont installés
2. Utilisez le script `quick_start.py` pour un démarrage automatique
3. Consultez les logs dans les terminaux des serveurs

---

**🌟 Votre application NASA Space App Challenge est prête !**
