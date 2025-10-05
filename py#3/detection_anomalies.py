import numpy as np
from skimage import filters, io

def load_image(image_path):
    """
    Load an image from the given path.
    """
    return io.imread(image_path)

def apply_log_filter(image):
    """
    Apply Laplacian of Gaussian filter to detect edges/anomalies.
    """
    return filters.laplace(image)

def extract_subsample(image, size=(256, 256)):
    """
    Extract a small sample from the image to work with.
    """
    return image[:size[0], :size[1]]

def detect_anomalies(image_path):
    """
    Main function to load the image, apply the LoG filter, and detect anomalies.
    """
    image = load_image(image_path)
    image_subsample = extract_subsample(image)
    anomalies = apply_log_filter(image_subsample)
    return anomalies
