import math 
import numpy as np
try:
    import cv2
    import cv2.aruco as aruco
    HAS_OPENCV = True
    expecpt ImportEror:
    HAS_OPEN = False

DEFAULT_CAM_MATRIX = np.array([  
    [525.0,   0.0, 320.0],        # Default Int-Ball2 navigation camera parameters
    [  0.0, 525.0, 240.0],
    [  0.0,   0.0,   1.0]
], dtype=np.float64)

DEFAULT_DIST_COEFFS = np.zeros((5, 1), dtype=np.float64)
DEFAULT_MARKER_SIZE = 0.05  # 5 cm

class ARMarkerDetector:
    def __init__(self, marker_size=DEFAULT_MARKER_SIZE, dictionary_type=None):
        self.marker_size = marker_size
        self.camera_matrix = DEFAULT_CAM_MATRIX
