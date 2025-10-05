import requests

def test_mvp_flow():
    # Test adding an annotation
    annotation = {"x": 100, "y": 150, "label": "anomaly"}
    response = requests.post("http://localhost:8000/annotations/", json=annotation)
    assert response.status_code == 200
    assert response.json()["message"] == "Annotation added successfully"

    # Test getting annotations
    response = requests.get("http://localhost:8000/annotations/")
    annotations = response.json()["annotations"]
    assert len(annotations) > 0

    # Test if heatmap is generated correctly
    response = requests.get("http://localhost:8000/detect?image=some_image_path")
    assert response.status_code == 200
    assert "heatmap" in response.json()

    print("MVP flow test passed successfully!")

test_mvp_flow()
