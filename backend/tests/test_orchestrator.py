import pytest
import json
import tempfile
import os
from pathlib import Path
from PIL import Image
from app.orchestrator import Job, load_manifest, estimate_level_scale, run_job

def test_estimate_level_scale():
    """Test du calcul d'échelle de niveau"""
    # Test avec ref_level
    scale = estimate_level_scale(2, 4)
    assert scale == 4.0  # 2**(4-2) = 4
    
    scale = estimate_level_scale(0, 3)
    assert scale == 8.0  # 2**(3-0) = 8
    
    # Test sans ref_level
    scale = estimate_level_scale(0, None)
    assert scale == 1.0  # 2**0 = 1
    
    scale = estimate_level_scale(2, None)
    assert scale == 4.0  # 2**2 = 4

def test_load_manifest_json():
    """Test de chargement d'un manifest JSON"""
    manifest_data = {
        "base_level": 8,
        "images": [
            {
                "id": "test1",
                "source": "test1.png",
                "levels": [2, 4, 6]
            },
            {
                "id": "test2", 
                "source": "test2.png",
                "levels": [1, 3, 5]
            }
        ]
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(manifest_data, f)
        manifest_path = f.name
    
    try:
        loaded_manifest = load_manifest(Path(manifest_path))
        assert loaded_manifest == manifest_data
    finally:
        os.unlink(manifest_path)

def test_job_creation():
    """Test de création d'un Job"""
    job = Job(
        image_id="test_image",
        source=Path("test.png"),
        levels=[0, 1, 2],
        base_scale=8.0,
        save_png=True
    )
    
    assert job.image_id == "test_image"
    assert job.source == Path("test.png")
    assert job.levels == [0, 1, 2]
    assert job.base_scale == 8.0
    assert job.save_png == True

def test_run_job():
    """Test d'exécution d'un job complet"""
    # Crée une image de test
    test_image = Image.new('RGB', (100, 100), color='white')
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Sauvegarde l'image de test
        input_path = os.path.join(tmpdir, 'test_image.png')
        test_image.save(input_path)
        
        # Crée un job
        job = Job(
            image_id="test_job",
            source=Path(input_path),
            levels=[0, 1],
            base_scale=None,
            save_png=True
        )
        
        # Exécute le job
        output_dir = Path(tmpdir) / "output"
        results = run_job(job, output_dir, retries=1)
        
        # Vérifie les résultats
        assert results["image_id"] == "test_job"
        assert results["source"] == input_path
        assert len(results["levels"]) == 2
        
        # Vérifie que les fichiers ont été créés
        assert (output_dir / "test_job_L0.png").exists()
        assert (output_dir / "test_job_L1.png").exists()
        assert (output_dir / "test_job_L0.json").exists()
        assert (output_dir / "test_job_L1.json").exists()
        assert (output_dir / "test_job_summary.json").exists()
        
        # Vérifie le contenu des fichiers JSON
        with open(output_dir / "test_job_L0.json", 'r') as f:
            level_data = json.load(f)
            assert level_data["image_id"] == "test_job"
            assert level_data["level"] == 0
            assert "stats" in level_data

def test_run_job_with_errors():
    """Test d'exécution avec des erreurs"""
    # Crée un job avec un fichier inexistant
    job = Job(
        image_id="error_job",
        source=Path("nonexistent.png"),
        levels=[0],
        base_scale=None,
        save_png=False
    )
    
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir) / "output"
        results = run_job(job, output_dir, retries=1)
        
        # Vérifie que l'erreur a été gérée
        assert results["image_id"] == "error_job"
        assert len(results["levels"]) == 1
        assert "error" in results["levels"][0]

def test_run_job_different_levels():
    """Test avec différents niveaux de résolution"""
    test_image = Image.new('RGB', (200, 200), color='red')
    
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, 'test.png')
        test_image.save(input_path)
        
        job = Job(
            image_id="multi_level",
            source=Path(input_path),
            levels=[0, 1, 2, 3],
            base_scale=None,
            save_png=True
        )
        
        output_dir = Path(tmpdir) / "output"
        results = run_job(job, output_dir)
        
        # Vérifie que tous les niveaux ont été traités
        assert len(results["levels"]) == 4
        
        for i, level_result in enumerate(results["levels"]):
            assert level_result["level"] == i
            assert "stats" in level_result
            assert "elapsed_ms" in level_result
            
            # Vérifie que les dimensions diminuent avec le niveau
            if i > 0:
                prev_height = results["levels"][i-1]["stats"]["height"]
                curr_height = level_result["stats"]["height"]
                assert curr_height <= prev_height
