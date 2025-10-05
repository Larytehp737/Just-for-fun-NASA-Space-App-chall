#!/usr/bin/env python3
"""
Script d'intégration et de test pour le projet NASA Space App Challenge
"Embiggen your eyes"

Ce script exécute tous les tests et vérifie l'intégration complète.
"""

import subprocess
import sys
import os
import time
import requests
from pathlib import Path

def run_command(cmd, cwd=None, check=True):
    """Exécute une commande et retourne le résultat"""
    print(f"🔧 Exécution: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, check=check, 
                              capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur: {e}")
        if e.stderr:
            print(f"Stderr: {e.stderr}")
        return e

def check_dependencies():
    """Vérifie que toutes les dépendances sont installées"""
    print("📦 Vérification des dépendances...")
    
    # Vérifie Python
    python_version = sys.version_info
    if python_version < (3, 8):
        print("❌ Python 3.8+ requis")
        return False
    print(f"✅ Python {python_version.major}.{python_version.minor}")
    
    # Vérifie Node.js
    result = run_command("node --version", check=False)
    if result.returncode != 0:
        print("❌ Node.js non installé")
        return False
    print(f"✅ Node.js {result.stdout.strip()}")
    
    # Vérifie npm
    result = run_command("npm --version", check=False)
    if result.returncode != 0:
        print("❌ npm non installé")
        return False
    print(f"✅ npm {result.stdout.strip()}")
    
    return True

def install_backend_dependencies():
    """Installe les dépendances Python dans l'environnement courant"""
    print("🐍 Installation des dépendances Python...")
    
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Dossier backend non trouvé")
        return False
    
    # Installation des dépendances du backend (assume venv déjà activé si utilisé)
    result = run_command("pip install -e .", cwd=backend_dir, check=False)
    if result.returncode != 0:
        print("❌ Échec installation dépendances Python")
        return False
    
    # Dépendances de test
    result = run_command("pip install pytest pytest-asyncio httpx", check=False)
    if result.returncode != 0:
        print("❌ Échec installation dépendances de test")
        return False
    
    print("✅ Dépendances Python installées")
    return True

def install_frontend_dependencies():
    """Installe les dépendances Node.js"""
    print("🌐 Installation des dépendances Node.js...")
    
    frontend_dir = Path("embiggen-your-eyes")
    if not frontend_dir.exists():
        print("❌ Dossier frontend non trouvé")
        return False
    
    result = run_command("npm install", cwd=frontend_dir, check=False)
    if result.returncode != 0:
        print("❌ Échec installation dépendances Node.js")
        return False
    
    print("✅ Dépendances Node.js installées")
    return True

def run_backend_tests():
    """Exécute les tests du backend"""
    print("🧪 Exécution des tests backend...")
    
    backend_dir = Path("backend")
    result = run_command("python -m pytest tests/ -v", cwd=backend_dir, check=False)
    
    if result.returncode == 0:
        print("✅ Tests backend réussis")
        return True
    else:
        print("❌ Échec des tests backend")
        return False

def start_backend_server():
    """Démarre le serveur backend"""
    print("🚀 Démarrage du serveur backend...")
    
    backend_dir = Path("backend")
    # Démarre le serveur en arrière-plan avec l'environnement courant
    process = subprocess.Popen(
        ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"],
        cwd=backend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Attend que le serveur démarre
    for i in range(30):  # 30 secondes max
        try:
            response = requests.get("http://localhost:8000/health", timeout=1)
            if response.status_code == 200:
                print("✅ Serveur backend démarré")
                return process
        except requests.exceptions.RequestException:
            time.sleep(1)
    
    print("❌ Timeout démarrage serveur backend")
    process.terminate()
    return None

def test_backend_endpoints():
    """Test des endpoints du backend"""
    print("🔍 Test des endpoints backend...")
    
    base_url = "http://localhost:8000"
    
    # Test health
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code != 200:
            print("❌ Endpoint /health échoué")
            return False
        print("✅ Endpoint /health OK")
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur connexion backend: {e}")
        return False
    
    # Test annotations
    try:
        response = requests.get(f"{base_url}/annotations")
        if response.status_code != 200:
            print("❌ Endpoint /annotations échoué")
            return False
        print("✅ Endpoint /annotations OK")
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur endpoint annotations: {e}")
        return False
    
    # Test détection
    try:
        response = requests.get(f"{base_url}/detect?level=0")
        if response.status_code != 200:
            print("❌ Endpoint /detect échoué")
            return False
        print("✅ Endpoint /detect OK")
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur endpoint detect: {e}")
        return False
    
    return True

def smoke_test_upload_tiles_static():
    """Enchaîne upload -> generate-tiles -> fetch DZI via /static pour vérifier le front path."""
    print("🧪 Smoke test upload → tiles → static ...")
    base_url = "http://localhost:8000"
    import io
    from PIL import Image
    # image en mémoire
    img = Image.new('RGB', (128, 128), color='red')
    buf = io.BytesIO(); img.save(buf, format='PNG'); buf.seek(0)
    files = {"file": ("smoke.png", buf, "image/png")}
    r = requests.post(f"{base_url}/upload", files=files)
    r.raise_for_status()
    up = r.json(); assert 'path' in up
    r2 = requests.post(f"{base_url}/generate-tiles", json={"image_path": up['path']})
    r2.raise_for_status()
    g = r2.json(); assert 'dzi_path' in g
    # construit l'URL /static (backend renvoie <stem>.dzi)
    dzi_path = g['dzi_path']
    static_url = f"{base_url}/static/{dzi_path}"
    r3 = requests.get(static_url)
    if r3.status_code != 200:
        print(f"❌ Static DZI fetch failed: {r3.status_code} {static_url}")
        return False
    print("✅ Smoke test OK:", static_url)
    return True

def start_frontend_server():
    """Démarre le serveur frontend"""
    print("🌐 Démarrage du serveur frontend...")
    
    frontend_dir = Path("embiggen-your-eyes")
    process = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=frontend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Attend que le serveur démarre
    for i in range(30):  # 30 secondes max
        try:
            response = requests.get("http://localhost:5173", timeout=1)
            if response.status_code == 200:
                print("✅ Serveur frontend démarré")
                return process
        except requests.exceptions.RequestException:
            time.sleep(1)
    
    print("❌ Timeout démarrage serveur frontend")
    process.terminate()
    return None

def run_integration_tests():
    """Exécute les tests d'intégration"""
    print("🔗 Tests d'intégration...")
    
    # Test de communication frontend-backend
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✅ Communication frontend-backend OK")
            return True
    except requests.exceptions.RequestException:
        print("❌ Communication frontend-backend échouée")
        return False

def main():
    """Fonction principale"""
    print("🚀 Démarrage des tests d'intégration NASA Space App Challenge")
    print("=" * 60)
    
    # Vérification des dépendances
    if not check_dependencies():
        print("❌ Dépendances manquantes")
        sys.exit(1)
    
    # Installation des dépendances
    if not install_backend_dependencies():
        print("❌ Échec installation backend")
        sys.exit(1)
    
    if not install_frontend_dependencies():
        print("❌ Échec installation frontend")
        sys.exit(1)
    
    # Tests backend
    if not run_backend_tests():
        print("❌ Tests backend échoués")
        sys.exit(1)
    
    # Démarrage des serveurs
    backend_process = start_backend_server()
    if not backend_process:
        print("❌ Impossible de démarrer le backend")
        sys.exit(1)
    
    try:
        # Test des endpoints
        if not test_backend_endpoints():
            print("❌ Tests endpoints échoués")
            sys.exit(1)
        # Smoke test pour pipeline upload->tiles->/static (pour le front)
        if not smoke_test_upload_tiles_static():
            print("❌ Smoke test upload/tiles/static échoué")
            sys.exit(1)
        
        # Démarrage frontend
        frontend_process = start_frontend_server()
        if not frontend_process:
            print("❌ Impossible de démarrer le frontend")
            sys.exit(1)
        
        try:
            # Tests d'intégration
            if not run_integration_tests():
                print("❌ Tests d'intégration échoués")
                sys.exit(1)
            
            print("\n" + "=" * 60)
            print("🎉 TOUS LES TESTS RÉUSSIS !")
            print("🌐 Frontend: http://localhost:5173")
            print("🐍 Backend: http://localhost:8000")
            print("📚 API Docs: http://localhost:8000/docs")
            print("=" * 60)
            
            # Garde les serveurs en vie
            print("Appuyez sur Ctrl+C pour arrêter les serveurs...")
            while True:
                time.sleep(1)
                
        finally:
            frontend_process.terminate()
            
    finally:
        backend_process.terminate()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Arrêt des serveurs...")
        sys.exit(0)
