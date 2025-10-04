import numpy as np
import matplotlib.pyplot as plt
from detection_anomalies import detect_anomalies

def apply_threshold(anomalies, threshold=0.1):
    """
    Apply a threshold to the anomalies to create a binary map.
    """
    return anomalies > threshold

def generate_heatmap(anomalies, threshold=0.1):
    """
    Generate a heatmap based on the anomalies detected in the image.
    """
    thresholded_anomalies = apply_threshold(anomalies, threshold)
    plt.imshow(thresholded_anomalies, cmap='hot', interpolation='nearest')
    plt.colorbar()
    plt.show()

def save_heatmap(image_path, threshold=0.1):
    """
    Save the generated heatmap to a file.
    """
    anomalies = detect_anomalies(image_path)
    generate_heatmap(anomalies, threshold)
