# -*- coding: utf-8 -*-
"""
code/route_planner.py
Route & Path Planning for Kibo-RPC Int-Ball2.
Compatible with Python 2.7 (ROS Melodic) and Python 3.
"""

import math

class RoutePlanner(object):
    def __init__(self, checkpoints=None):
        self.checkpoints = list(checkpoints) if checkpoints else []
        self.current_index = 0

    def add_checkpoint(self, checkpoint_id, x, y, description=""):
        """Add a new checkpoint to the route."""
        item = {
            "id": int(checkpoint_id),
            "x": float(x),
            "y": float(y),
            "desc": str(description)
        }
        self.checkpoints.append(item)
        print("[RoutePlanner] Added checkpoint %s: (%s, %s)" % (str(checkpoint_id), str(x), str(y)))

    def get_next_checkpoint(self):
        """Retrieve next checkpoint in sequence."""
        if self.current_index < len(self.checkpoints):
            target = self.checkpoints[self.current_index]
            self.current_index += 1
            return target
        return None

    def reset(self):
        """Reset sequence index back to start."""
        self.current_index = 0

    def plan_path_to_marker(self, marker_info=None):
        """Plan trajectory towards detected AR marker."""
        if not marker_info or not isinstance(marker_info, dict):
            print("[RoutePlanner] No marker info provided.")
            return "SEARCH_MARKER"

        marker_id = marker_info.get("marker_id", marker_info.get("id", "UNKNOWN"))
        print("[RoutePlanner] Planning trajectory to Marker ID %s..." % str(marker_id))
        return "FORWARD_AND_ALIGN"

    def compute_distance(self, p1, p2):
        """Compute Euclidean distance between two 2D/3D points."""
        dx = p1.get("x", 0.0) - p2.get("x", 0.0)
        dy = p1.get("y", 0.0) - p2.get("y", 0.0)
        dz = p1.get("z", 0.0) - p2.get("z", 0.0)
        return math.sqrt(dx * dx + dy * dy + dz * dz)

