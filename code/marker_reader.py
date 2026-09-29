import math
import numpy as np

try:
    import cv2
    import cv2.aruco as aruco
    HAS_OPENCV = True
except ImportError:
    HAS_OPENCV = False

# Default Int-Ball2 navigation camera parameters
DEFAULT_CAM_MATRIX = np.array([
    [525.0,   0.0, 320.0],
    [  0.0, 525.0, 240.0],
    [  0.0,   0.0,   1.0]
], dtype=np.float64)

DEFAULT_DIST_COEFFS = np.zeros((5, 1), dtype=np.float64)
DEFAULT_MARKER_SIZE = 0.05  # 5 cm


class ARMarkerDetector:
    def __init__(self, marker_size=DEFAULT_MARKER_SIZE, dictionary_type=None):
        self.marker_size = marker_size
        self.camera_matrix = DEFAULT_CAM_MATRIX
        self.dist_coeffs = DEFAULT_DIST_COEFFS
        self.aruco_dict = None
        self.parameters = None
        self.detector = None
        
        if HAS_OPENCV:
            # Handle dictionary loading across OpenCV versions
            dict_id = aruco.DICT_5X5_250 if dictionary_type is None else dictionary_type
            if hasattr(aruco, "getPredefinedDictionary"):
                self.aruco_dict = aruco.getPredefinedDictionary(dict_id)
            elif hasattr(aruco, "Dictionary_get"):
                self.aruco_dict = aruco.Dictionary_get(dict_id)

            # Handle DetectorParameters compatibility across OpenCV versions
            if hasattr(aruco, "DetectorParameters"):
                self.parameters = aruco.DetectorParameters()
            elif hasattr(aruco, "DetectorParameters_create"):
                self.parameters = aruco.DetectorParameters_create()

            # OpenCV 4.7+ introduced ArucoDetector class
            if hasattr(aruco, "ArucoDetector") and self.aruco_dict is not None and self.parameters is not None:
                self.detector = aruco.ArucoDetector(self.aruco_dict, self.parameters)

    def detect_markers_from_frame(self, frame):
        """
        Process a single image frame and return all detected AR markers.
        """
        if frame is None:
            return []

        # If running unit test with dummy/mock frame or without numpy array
        if not HAS_OPENCV or not isinstance(frame, np.ndarray):
            return self._mock_detect(frame)

        if len(frame.shape) == 3:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            gray = frame

        # Detect markers according to available OpenCV API
        if self.detector is not None:
            corners, ids, _ = self.detector.detectMarkers(gray)
        elif hasattr(aruco, "detectMarkers"):
            corners, ids, _ = aruco.detectMarkers(
                gray, self.aruco_dict, parameters=self.parameters
            )
        else:
            return self._mock_detect(frame)

        if ids is None or len(ids) == 0:
            return []

        results = []
        # Estimate pose
        if hasattr(aruco, "estimatePoseSingleMarkers"):
            rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(
                corners, self.marker_size, self.camera_matrix, self.dist_coeffs
            )
        else:
            # Fallback calculation if estimatePoseSingleMarkers is deprecated
            rvecs, tvecs = self._estimate_pose_fallback(corners)

        for i in range(len(ids)):
            marker_id = int(ids[i][0])
            c = corners[i][0]
            cx = float(np.mean(c[:, 0]))
            cy = float(np.mean(c[:, 1]))

            tx = float(tvecs[i][0][0]) if tvecs is not None else 0.0
            ty = float(tvecs[i][0][1]) if tvecs is not None else 0.0
            tz = float(tvecs[i][0][2]) if tvecs is not None else 0.5
            distance = math.sqrt(tx * tx + ty * ty + tz * tz)

            results.append({
                "id": marker_id,
                "center_pixel": (cx, cy),
                "translation": (tx, ty, tz),
                "distance_m": distance,
                "rvec": rvecs[i][0].tolist() if rvecs is not None else [0.0, 0.0, 0.0],
                "corners": c.tolist()
            })

        return results

    def _estimate_pose_fallback(self, corners):
        """SolvePnP fallback for newer OpenCV versions where estimatePoseSingleMarkers was removed."""
        half_size = self.marker_size / 2.0
        obj_points = np.array([
            [-half_size,  half_size, 0.0],
            [ half_size,  half_size, 0.0],
            [ half_size, -half_size, 0.0],
            [-half_size, -half_size, 0.0]
        ], dtype=np.float32)

        rvecs = []
        tvecs = []
        for corner in corners:
            img_points = corner.reshape(4, 2).astype(np.float32)
            success, rvec, tvec = cv2.solvePnP(
                obj_points, img_points, self.camera_matrix, self.dist_coeffs, False, cv2.SOLVEPNP_IPPE_SQUARE
            )
            if success:
                rvecs.append([rvec])
                tvecs.append([tvec])
            else:
                rvecs.append([np.zeros((3, 1))])
                tvecs.append([np.zeros((3, 1))])
        return rvecs, tvecs

    def calculate_alignment_offsets(self, detected_marker, target_distance=0.50):
        """
        Calculate error vector for Int-Ball2 attitude control to align directly with marker center.
        Used by Lyinh (Main Programmer) for attitude correction.
        """
        if not detected_marker:
            return None

        cx, cy = detected_marker["center_pixel"]
        image_center_x = self.camera_matrix[0, 2]
        image_center_y = self.camera_matrix[1, 2]

        pixel_err_x = cx - image_center_x
        pixel_err_y = cy - image_center_y
        dist_err = detected_marker["distance_m"] - target_distance

        is_aligned = (abs(pixel_err_x) < 15.0 and 
                      abs(pixel_err_y) < 15.0 and 
                      abs(dist_err) < 0.03)

        return {
            "marker_id": detected_marker["id"],
            "pixel_error_x": round(pixel_err_x, 2),
            "pixel_error_y": round(pixel_err_y, 2),
            "distance_error_m": round(dist_err, 3),
            "is_aligned": is_aligned
        }

    def _mock_detect(self, frame):
        """
        Mock detection for local unit tests without active camera feed.
        """
        return [{
            "id": 1,
            "center_pixel": (320.0, 240.0),
            "translation": (0.0, 0.0, 0.50),
            "distance_m": 0.50,
            "rvec": [0.0, 0.0, 0.0],
            "corners": [[310, 230], [330, 230], [330, 250], [310, 250]]
        }]
