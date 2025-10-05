#!/usr/bin/env python3
"""
Script de démarrage rapide pour le projet NASA Space App Challenge
"Embiggen your eyes"

Ce script évite les problèmes d'environnement virtuel et démarre directement les serveurs.
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
    """Vérifie que les dépendances de base sont installées"""
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

def start_backend_server():
    """Démarre le serveur backend avec les dépendances système"""
    print("🚀 Démarrage du serveur backend...")
    
    backend_dir = Path("backend")
    
    # Installe les dépendances Python avec --break-system-packages
    print("📦 Installation des dépendances Python...")
    result = run_command("pip install fastapi uvicorn pillow numpy scikit-image requests --break-system-packages", check=False)
    if result.returncode != 0:
        print("⚠️  Installation des dépendances échouée, tentative de démarrage direct...")
    
    # Démarre le serveur en arrière-plan
    process = subprocess.Popen(
        ["python3", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"],
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
    
    return True

def main():
    """Fonction principale de démarrage rapide"""
    print("🚀 DÉMARRAGE RAPIDE NASA SPACE APP CHALLENGE")
    print("🎯 Projet: Embiggen Your Eyes")
    print("=" * 60)
    
    try:
        # Vérification des dépendances
        if not check_dependencies():
            print("❌ Dépendances manquantes")
            sys.exit(1)
        
        # Installation frontend
        if not install_frontend_dependencies():
            print("❌ Échec installation frontend")
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
            
            # Démarrage frontend
            frontend_process = start_frontend_server()
            if not frontend_process:
                print("❌ Impossible de démarrer le frontend")
                sys.exit(1)
            
            print("\n" + "=" * 60)
            print("🎉 APPLICATION DÉMARRÉE AVEC SUCCÈS !")
            print("🌐 Frontend: http://localhost:5173")
            print("🐍 Backend: http://localhost:8000")
            print("📚 API Docs: http://localhost:8000/docs")
            print("=" * 60)
            
            print("\n📋 Fonctionnalités disponibles:")
            print("   ✅ Interface utilisateur moderne")
            print("   ✅ Upload et visualisation d'images")
            print("   ✅ Zoom fluide avec OpenSeadragon")
            print("   ✅ Détection d'anomalies")
            print("   ✅ Système d'annotations")
            print("   ✅ API REST complète")
            
            print("\n🚀 Pour tester l'application:")
            print("   1. Ouvrez http://localhost:5173 dans votre navigateur")
            print("   2. Uploadez une image")
            print("   3. Testez le zoom et les annotations")
            print("   4. Consultez l'API sur http://localhost:8000/docs")
            
            # Garde les serveurs en vie
            print("\nAppuyez sur Ctrl+C pour arrêter les serveurs...")
            while True:
                time.sleep(1)
                
        finally:
            if 'frontend_process' in locals():
                frontend_process.terminate()
            
    except KeyboardInterrupt:
        print("\n🛑 Arrêt des serveurs...")
    except Exception as e:
        print(f"\n❌ Erreur lors du démarrage: {e}")
    finally:
        if 'backend_process' in locals():
            backend_process.terminate()

if __name__ == "__main__":
    main()
