import pytest
import io
from fastapi.testclient import TestClient
from PIL import Image
import numpy as np
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    """Test du endpoint de santé"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"ok": True}

def test_annotations_crud():
    """Test CRUD des annotations"""
    # Test GET annotations (vide au début)
    response = client.get("/annotations")
    assert response.status_code == 200
    assert response.json() == []
    
    # Test POST annotation (point)
    point_data = {"type": "point", "x": 0.5, "y": 0.5}
    response = client.post("/annotations", json=point_data)
    assert response.status_code == 200
    assert "id" in response.json()
    
    # Test POST annotation (rectangle)
    rect_data = {"type": "rect", "x": 0.1, "y": 0.1, "w": 0.2, "h": 0.2}
    response = client.post("/annotations", json=rect_data)
    assert response.status_code == 200
    
    # Test GET annotations (avec données)
    response = client.get("/annotations")
    assert response.status_code == 200
    assert len(response.json()) == 2
    
    # Test DELETE annotations
    response = client.delete("/annotations")
    assert response.status_code == 200
    assert response.json() == {"deleted": True}

def test_detect_endpoint():
    """Test du endpoint de détection"""
    response = client.get("/detect?level=0")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    
    # Vérifie que c'est bien une image PNG
    img = Image.open(io.BytesIO(response.content))
    assert img.format == "PNG"

def test_detect_different_levels():
    """Test de détection avec différents niveaux"""
    for level in [0, 1, 2, 3]:
        response = client.get(f"/detect?level={level}")
        assert response.status_code == 200
        assert response.headers["content-type"] == "image/png"

def test_list_images():
    """Test de la liste des images"""
    response = client.get("/images")
    assert response.status_code == 200
    data = response.json()
    assert "images" in data
    assert isinstance(data["images"], list)

def test_upload_image():
    """Test d'upload d'image"""
    # Crée une image de test
    test_image = Image.new('RGB', (100, 100), color='red')
    img_buffer = io.BytesIO()
    test_image.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    
    # Test upload
    files = {"file": ("test.png", img_buffer, "image/png")}
    response = client.post("/upload", files=files)
    assert response.status_code == 200
    data = response.json()
    assert "file_id" in data
    assert "filename" in data
    assert "path" in data

def test_upload_invalid_file():
    """Test d'upload de fichier invalide"""
    # Crée un fichier texte
    text_content = "Ceci n'est pas une image"
    files = {"file": ("test.txt", io.BytesIO(text_content.encode()), "text/plain")}
    response = client.post("/upload", files=files)
    assert response.status_code == 400
