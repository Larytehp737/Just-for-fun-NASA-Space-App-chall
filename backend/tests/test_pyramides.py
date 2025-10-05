import pytest
import os
import tempfile
from pathlib import Path
from PIL import Image
from app.pyramides import generate_deepzoom

def test_generate_deepzoom():
    """Test de génération de tuiles DZI"""
    # Crée une image de test
    test_image = Image.new('RGB', (256, 256), color='white')
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Sauvegarde l'image de test
        input_path = os.path.join(tmpdir, 'test_image.png')
        test_image.save(input_path)
        
        # Génère les tuiles DZI
        output_basename = os.path.join(tmpdir, 'test_output')
        generate_deepzoom(input_path, output_basename, tile_size=64, suffix=".jpg")
        
        # Vérifie que les fichiers ont été créés
        dzi_file = f"{output_basename}.dzi"
        tiles_dir = f"{output_basename}_files"
        
        assert os.path.exists(dzi_file), "Fichier DZI non créé"
        assert os.path.exists(tiles_dir), "Dossier de tuiles non créé"
        assert os.path.isdir(tiles_dir), "Le dossier de tuiles n'est pas un répertoire"
        
        # Vérifie le contenu du fichier DZI
        with open(dzi_file, 'r') as f:
            dzi_content = f.read()
            assert 'Image' in dzi_content
            assert 'TileSize' in dzi_content
            assert 'Overlap' in dzi_content

def test_generate_deepzoom_different_formats():
    """Test avec différents formats de sortie"""
    test_image = Image.new('RGB', (128, 128), color='blue')
    
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, 'test.png')
        test_image.save(input_path)
        
        # Test avec PNG
        output_png = os.path.join(tmpdir, 'test_png')
        generate_deepzoom(input_path, output_png, suffix=".png")
        
        assert os.path.exists(f"{output_png}.dzi")
        assert os.path.exists(f"{output_png}_files")
        
        # Test avec JPG
        output_jpg = os.path.join(tmpdir, 'test_jpg')
        generate_deepzoom(input_path, output_jpg, suffix=".jpg[Q=90]")
        
        assert os.path.exists(f"{output_jpg}.dzi")
        assert os.path.exists(f"{output_jpg}_files")

def test_generate_deepzoom_different_tile_sizes():
    """Test avec différentes tailles de tuiles"""
    test_image = Image.new('RGB', (512, 512), color='green')
    
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, 'test.png')
        test_image.save(input_path)
        
        tile_sizes = [32, 64, 128, 256]
        
        for tile_size in tile_sizes:
            output_name = os.path.join(tmpdir, f'test_{tile_size}')
            generate_deepzoom(input_path, output_name, tile_size=tile_size)
            
            # Vérifie que les fichiers existent
            assert os.path.exists(f"{output_name}.dzi")
            assert os.path.exists(f"{output_name}_files")
            
            # Vérifie que la taille de tuile est correcte dans le DZI
            with open(f"{output_name}.dzi", 'r') as f:
                content = f.read()
                assert f'TileSize="{tile_size}"' in content

def test_generate_deepzoom_nonexistent_file():
    """Test avec un fichier inexistant"""
    with tempfile.TemporaryDirectory() as tmpdir:
        nonexistent_path = os.path.join(tmpdir, 'nonexistent.png')
        output_name = os.path.join(tmpdir, 'test')
        
        with pytest.raises(Exception):
            generate_deepzoom(nonexistent_path, output_name)

def test_generate_deepzoom_invalid_image():
    """Test avec un fichier qui n'est pas une image"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Crée un fichier texte
        text_file = os.path.join(tmpdir, 'not_an_image.txt')
        with open(text_file, 'w') as f:
            f.write("Ceci n'est pas une image")
        
        output_name = os.path.join(tmpdir, 'test')
        
        with pytest.raises(Exception):
            generate_deepzoom(text_file, output_name)
