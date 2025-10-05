import numpy as np
import matplotlib.pyplot as plt
from detection_anomalies import detect_anomalies
from serve_tiles import get_tile

def apply_annotations_to_heatmap(heatmap, annotations):
    """
    Apply annotations on the heatmap. Annotations will be drawn as circles or rectangles.
    """
    for annotation in annotations:
        if annotation["width"] and annotation["height"]:  # Rectangle
            heatmap[annotation["y"]:annotation["y"]+annotation["height"], annotation["x"]:annotation["x"]+annotation["width"]] = 1
        else:  # Point
            heatmap[annotation["y"], annotation["x"]] = 1
    return heatmap

def generate_heatmap_with_annotations(image_path, annotations, threshold=0.1):
    """
    Generate a heatmap including both detected anomalies and annotations.
    """
    anomalies = detect_anomalies(image_path)
    heatmap = anomalies > threshold
    annotated_heatmap = apply_annotations_to_heatmap(heatmap, annotations)
    
    plt.imshow(annotated_heatmap, cmap='hot', interpolation='nearest')
    plt.colorbar()
    plt.show()
