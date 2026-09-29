"""
code/route_planner.py
Function សម្រាប់រៀបចំផ្លូវ និង Checkpoint (Route & Path Planning)
"""

from typing import List, Dict, Any

class RoutePlanner:
    def __init__(self, checkpoints: List[Dict[str, Any]] = None):
        self.checkpoints = checkpoints or []
        self.current_index = 0

    def add_checkpoint(self, checkpoint_id: int, x: float, y: float, description: str = ""):
        """បន្ថែម Checkpoint ថ្មីទៅក្នុងផ្លូវ"""
        self.checkpoints.append({
            "id": checkpoint_id,
            "x": x,
            "y": y,
            "desc": description
        })
        print(f"[RoutePlanner] Added checkpoint {checkpoint_id}: ({x}, {y})")

    def get_next_checkpoint(self):
        """ទាញយក Checkpoint បន្ទាប់"""
        if self.current_index < len(self.checkpoints):
            target = self.checkpoints[self.current_index]
            self.current_index += 1
            return target
        return None

    def plan_path_to_marker(self, marker_info: dict):
        """គណនាផ្លូវទៅកាន់ AR Marker ដែលបានស្កេនឃើញ"""
        print(f"[RoutePlanner] Planning trajectory to Marker ID {marker_info.get('marker_id')}...")
        return "FORWARD_AND_ALIGN"
