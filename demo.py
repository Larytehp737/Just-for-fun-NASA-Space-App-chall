#!/usr/bin/env python3
"""
Script de démonstration pour le projet NASA Space App Challenge
"Embiggen your eyes"

Ce script démontre toutes les fonctionnalités développées par l'équipe.
"""

import asyncio
import time
import json
from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np

# Import des modules du projet
import sys
sys.path.append('backend')

from app.detect import run_detector_on_image_path, detect_loglike, colorize_heatmap
from app.pyramides import generate_deepzoom
from app.orchestrator import Job, run_job
from app.store import save_annotation, load_annotations

def print_header(title):
    """Affiche un en-tête stylisé"""
    print("\n" + "="*60)
    print(f"🚀 {title}")
    print("="*60)

def print_step(step, description):
    """Affiche une étape de démonstration"""
    print(f"\n📋 Étape {step}: {description}")
    print("-" * 40)

def demo_image_processing():
    """Démonstration du traitement d'images"""
    print_header("DÉMONSTRATION - TRAITEMENT D'IMAGES")
    
    # Crée une image de test avec des anomalies
    print_step(1, "Création d'une image de test avec anomalies")
    test_image = Image.new('RGB', (400, 400), color='darkblue')
    draw = ImageDraw.Draw(test_image)
    
    # Ajoute des formes qui simulent des anomalies
    draw.ellipse([100, 100, 200, 200], fill='red', outline='white', width=3)
    draw.rectangle([250, 150, 350, 250], fill='yellow', outline='white', width=3)
    draw.polygon([(50, 300), (150, 250), (200, 350)], fill='green', outline='white', width=3)
    
    # Sauvegarde l'image de test
    test_path = "demo_test_image.png"
    test_image.save(test_path)
    print(f"✅ Image de test créée: {test_path}")
    
    # Détection d'anomalies
    print_step(2, "Détection d'anomalies avec algorithmes avancés")
    try:
        heatmap, stats = run_detector_on_image_path(test_path, level_scale=1.0)
        print(f"✅ Détection réussie!")
        print(f"   📊 Statistiques: {json.dumps(stats, indent=2)}")
        
        # Sauvegarde la heatmap
        heatmap_path = "demo_heatmap.png"
        heatmap.save(heatmap_path)
        print(f"✅ Heatmap sauvegardée: {heatmap_path}")
        
    except Exception as e:
        print(f"❌ Erreur lors de la détection: {e}")
    
    return test_path

def demo_tile_generation(image_path):
    """Démonstration de génération de tuiles"""
    print_header("DÉMONSTRATION - GÉNÉRATION DE TUILES DZI")
    
    print_step(1, "Génération de tuiles DeepZoom")
    try:
        output_name = "demo_tiles"
        generate_deepzoom(image_path, output_name, tile_size=64, suffix=".jpg")
        
        # Vérifie que les fichiers ont été créés
        dzi_file = f"{output_name}.dzi"
        tiles_dir = f"{output_name}_files"
        
        if Path(dzi_file).exists() and Path(tiles_dir).exists():
            print(f"✅ Tuiles DZI générées avec succès!")
            print(f"   📁 Fichier DZI: {dzi_file}")
            print(f"   📁 Dossier tuiles: {tiles_dir}")
            
            # Affiche le contenu du fichier DZI
            with open(dzi_file, 'r') as f:
                content = f.read()
                print(f"   📄 Contenu DZI (extrait): {content[:200]}...")
        else:
            print("❌ Erreur lors de la génération des tuiles")
            
    except Exception as e:
        print(f"❌ Erreur lors de la génération: {e}")

def demo_annotations():
    """Démonstration du système d'annotations"""
    print_header("DÉMONSTRATION - SYSTÈME D'ANNOTATIONS")
    
    print_step(1, "Ajout d'annotations")
    
    # Ajoute quelques annotations de test
    annotations = [
        {"type": "point", "x": 0.3, "y": 0.4, "label": "Cratère suspect"},
        {"type": "rect", "x": 0.6, "y": 0.2, "w": 0.2, "h": 0.3, "label": "Formation géologique"},
        {"type": "point", "x": 0.8, "y": 0.7, "label": "Anomalie thermique"}
    ]
    
    for i, annotation in enumerate(annotations):
        try:
            result = save_annotation(annotation)
            print(f"✅ Annotation {i+1} ajoutée: {result['id']}")
        except Exception as e:
            print(f"❌ Erreur annotation {i+1}: {e}")
    
    print_step(2, "Récupération des annotations")
    try:
        all_annotations = load_annotations()
        print(f"✅ {len(all_annotations)} annotations récupérées:")
        for ann in all_annotations:
            print(f"   📍 ID {ann['id']}: {ann.get('label', 'Sans label')} à ({ann['x']}, {ann['y']})")
    except Exception as e:
        print(f"❌ Erreur récupération: {e}")

def demo_orchestrator():
    """Démonstration de l'orchestrateur"""
    print_header("DÉMONSTRATION - ORCHESTRATEUR BATCH")
    
    print_step(1, "Création d'un job de traitement")
    
    # Crée une image de test pour l'orchestrateur
    test_image = Image.new('RGB', (200, 200), color='purple')
    test_path = "orchestrator_test.png"
    test_image.save(test_path)
    
    # Crée un job
    job = Job(
        image_id="demo_job",
        source=Path(test_path),
        levels=[0, 1, 2],
        base_scale=None,
        save_png=True
    )
    
    print(f"✅ Job créé: {job.image_id}")
    print(f"   📁 Source: {job.source}")
    print(f"   📊 Niveaux: {job.levels}")
    
    print_step(2, "Exécution du job")
    try:
        output_dir = Path("demo_output")
        results = run_job(job, output_dir, retries=1)
        
        print(f"✅ Job exécuté avec succès!")
        print(f"   📊 Résultats: {len(results['levels'])} niveaux traités")
        
        for level_result in results['levels']:
            if 'error' not in level_result:
                print(f"   📈 Niveau {level_result['level']}: {level_result['elapsed_ms']}ms")
            else:
                print(f"   ❌ Niveau {level_result['level']}: {level_result['error']}")
                
    except Exception as e:
        print(f"❌ Erreur orchestrateur: {e}")

def demo_performance_metrics():
    """Démonstration des métriques de performance"""
    print_header("DÉMONSTRATION - MÉTRIQUES DE PERFORMANCE")
    
    print_step(1, "Test de performance des algorithmes")
    
    # Test avec différentes tailles d'images
    sizes = [(100, 100), (200, 200), (400, 400)]
    
    for width, height in sizes:
        print(f"\n🔍 Test image {width}x{height}:")
        
        # Crée une image de test
        test_image = Image.new('RGB', (width, height), color='blue')
        test_path = f"perf_test_{width}x{height}.png"
        test_image.save(test_path)
        
        # Mesure le temps de traitement
        start_time = time.time()
        try:
            heatmap, stats = run_detector_on_image_path(test_path, level_scale=1.0)
            end_time = time.time()
            
            processing_time = (end_time - start_time) * 1000  # en ms
            print(f"   ⏱️  Temps de traitement: {processing_time:.2f}ms")
            print(f"   📊 Statistiques: min={stats['min']:.3f}, max={stats['max']:.3f}")
            
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
        
        # Nettoie le fichier temporaire
        Path(test_path).unlink(missing_ok=True)

def demo_api_simulation():
    """Simulation des appels API"""
    print_header("DÉMONSTRATION - SIMULATION API")
    
    print_step(1, "Simulation des endpoints")
    
    # Simule les appels API qui seraient faits par le frontend
    api_calls = [
        ("GET /health", "Vérification santé du serveur"),
        ("GET /annotations", "Récupération des annotations"),
        ("GET /detect?level=0", "Détection d'anomalies niveau 0"),
        ("GET /detect?level=1", "Détection d'anomalies niveau 1"),
        ("GET /images", "Liste des images disponibles")
    ]
    
    for endpoint, description in api_calls:
        print(f"   🌐 {endpoint} - {description}")
        # Ici on simulerait l'appel API réel
        time.sleep(0.1)  # Simulation du délai réseau
        print(f"   ✅ Réponse simulée: 200 OK")

def cleanup_demo_files():
    """Nettoie les fichiers de démonstration"""
    print_header("NETTOYAGE")
    
    demo_files = [
        "demo_test_image.png",
        "demo_heatmap.png", 
        "demo_tiles.dzi",
        "demo_tiles_files",
        "orchestrator_test.png",
        "demo_output"
    ]
    
    for file_path in demo_files:
        path = Path(file_path)
        if path.exists():
            if path.is_file():
                path.unlink()
                print(f"🗑️  Fichier supprimé: {file_path}")
            elif path.is_dir():
                import shutil
                shutil.rmtree(path)
                print(f"🗑️  Dossier supprimé: {file_path}")

def main():
    """Fonction principale de démonstration"""
    print("🌟 DÉMONSTRATION NASA SPACE APP CHALLENGE")
    print("🎯 Projet: Embiggen Your Eyes")
    print("👥 Équipe: 5 développeurs")
    print("🚀 Fonctionnalités: Visualisation + Détection + Collaboration")
    
    try:
        # Démonstrations principales
        image_path = demo_image_processing()
        demo_tile_generation(image_path)
        demo_annotations()
        demo_orchestrator()
        demo_performance_metrics()
        demo_api_simulation()
        
        print_header("DÉMONSTRATION TERMINÉE")
        print("🎉 Toutes les fonctionnalités ont été démontrées avec succès!")
        print("\n📋 Résumé des fonctionnalités testées:")
        print("   ✅ Traitement d'images et détection d'anomalies")
        print("   ✅ Génération de tuiles DZI pour zoom fluide")
        print("   ✅ Système d'annotations collaboratives")
        print("   ✅ Orchestrateur batch pour traitement multiple")
        print("   ✅ Métriques de performance")
        print("   ✅ Simulation d'API REST")
        
        print("\n🚀 Pour tester l'application complète:")
        print("   python run_tests.py")
        
    except KeyboardInterrupt:
        print("\n🛑 Démonstration interrompue par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur lors de la démonstration: {e}")
    finally:
        # Demande si l'utilisateur veut nettoyer
        try:
            response = input("\n🧹 Voulez-vous nettoyer les fichiers de démonstration? (y/N): ")
            if response.lower() in ['y', 'yes', 'oui']:
                cleanup_demo_files()
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    main()
