import pytest
import numpy as np
from PIL import Image
from app.detect import to_gray, detect_loglike, colorize_heatmap, run_detector_on_image_path

def test_to_gray_rgb():
    """Test conversion RGB vers niveaux de gris"""
    # Image RGB 3x3
    rgb_array = np.array([
        [[255, 0, 0], [0, 255, 0], [0, 0, 255]],
        [[128, 128, 128], [255, 255, 255], [0, 0, 0]],
        [[100, 150, 200], [50, 100, 150], [200, 100, 50]]
    ], dtype=np.uint8)
    
    gray = to_gray(rgb_array)
    
    assert gray.shape == (3, 3)
    assert gray.dtype == np.float32
    assert 0.0 <= gray.min() <= gray.max() <= 1.0

def test_to_gray_rgba():
    """Test conversion RGBA vers niveaux de gris"""
    # Image RGBA 2x2
    rgba_array = np.array([
        [[255, 0, 0, 255], [0, 255, 0, 128]],
        [[0, 0, 255, 255], [128, 128, 128, 64]]
    ], dtype=np.uint8)
    
    gray = to_gray(rgba_array)
    
    assert gray.shape == (2, 2)
    assert gray.dtype == np.float32

def test_detect_loglike():
    """Test de l'algorithme de détection LoG"""
    # Image de test avec un carré blanc sur fond noir
    test_image = np.zeros((100, 100), dtype=np.float32)
    test_image[30:70, 30:70] = 1.0  # Carré blanc
    
    score = detect_loglike(test_image)
    
    assert score.shape == (100, 100)
    assert score.dtype == np.float32
    assert 0.0 <= score.min() <= score.max() <= 1.0
    
    # Les bords du carré devraient avoir des scores élevés
    edge_scores = score[30, 30:70]  # Bord supérieur
    assert edge_scores.max() > 0.1

def test_colorize_heatmap():
    """Test de colorisation de heatmap"""
    # Score de test
    score = np.array([
        [0.0, 0.5, 1.0],
        [0.2, 0.8, 0.3]
    ], dtype=np.float32)
    
    heatmap = colorize_heatmap(score, alpha=128)
    
    assert isinstance(heatmap, Image.Image)
    assert heatmap.mode == 'RGBA'
    assert heatmap.size == (3, 2)
    
    # Vérifie que les pixels ont les bonnes valeurs
    rgba_array = np.array(heatmap)
    assert rgba_array.shape == (2, 3, 4)  # (height, width, channels)

def test_run_detector_on_image_path():
    """Test du pipeline complet de détection"""
    # Crée une image de test
    test_image = Image.new('RGB', (50, 50), color='white')
    test_image.putpixel((25, 25), (255, 0, 0))  # Pixel rouge au centre
    
    # Sauvegarde temporaire
    import tempfile
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        test_image.save(tmp.name)
        tmp_path = tmp.name
    
    try:
        heatmap, stats = run_detector_on_image_path(tmp_path, level_scale=1.0)
        
        assert isinstance(heatmap, Image.Image)
        assert heatmap.mode == 'RGBA'
        
        assert isinstance(stats, dict)
        assert 'min' in stats
        assert 'max' in stats
        assert 'mean' in stats
        assert 'std' in stats
        assert 'width' in stats
        assert 'height' in stats
        assert 'scale' in stats
        
        assert stats['width'] == 50
        assert stats['height'] == 50
        assert stats['scale'] == 1.0
        
    finally:
        import os
        os.unlink(tmp_path)

def test_run_detector_with_scaling():
    """Test de détection avec redimensionnement"""
    # Crée une image de test plus grande
    test_image = Image.new('RGB', (200, 200), color='white')
    
    import tempfile
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        test_image.save(tmp.name)
        tmp_path = tmp.name
    
    try:
        # Test avec scale = 2.0 (image divisée par 2)
        heatmap, stats = run_detector_on_image_path(tmp_path, level_scale=2.0)
        
        assert stats['width'] == 100  # 200 / 2
        assert stats['height'] == 100
        assert stats['scale'] == 2.0
        
    finally:
        import os
        os.unlink(tmp_path)
