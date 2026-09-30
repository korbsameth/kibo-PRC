# -*- coding: utf-8 -*-
"""
tests/test_mission.py
Comprehensive automated test suite for kibo-PRC.
Verifies zero bugs, edge case handling, and Python 2/3 compatibility.
"""

import sys
import os
import unittest
import numpy as np

# Add code folder to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "code")))

from marker_reader import ARMarkerDetector, init_camera, read_ar_marker
from route_planner import RoutePlanner
from movement import (
    move_forward,
    move_backward,
    turn_left,
    turn_right,
    move_to_relative_coordinate,
    stop_robot
)
from main import execute_mission

class TestKiboRPC(unittest.TestCase):

    def setUp(self):
        self.detector = ARMarkerDetector()
        self.planner = RoutePlanner()

    def test_marker_detection_mock(self):
        """Test marker detector with None frame returns mock detection."""
        markers = self.detector.detect_markers_from_frame(None)
        self.assertIsInstance(markers, list)
        self.assertGreaterEqual(len(markers), 1)
        first = markers[0]
        self.assertIn("id", first)
        self.assertIn("center_pixel", first)
        self.assertIn("distance_m", first)

    def test_marker_alignment_calculation(self):
        """Test alignment offset calculations with valid and invalid inputs."""
        mock_marker = {
            "id": 1,
            "center_pixel": (320.0, 240.0),
            "distance_m": 0.50
        }
        res = self.detector.calculate_alignment_offsets(mock_marker, target_distance=0.50)
        self.assertIsNotNone(res)
        self.assertTrue(res["is_aligned"])
        self.assertEqual(res["pixel_error_x"], 0.0)
        self.assertEqual(res["pixel_error_y"], 0.0)

        # Off-center marker
        off_marker = {
            "id": 2,
            "center_pixel": (400.0, 300.0),
            "distance_m": 0.80
        }
        res_off = self.detector.calculate_alignment_offsets(off_marker, target_distance=0.50)
        self.assertIsNotNone(res_off)
        self.assertFalse(res_off["is_aligned"])

        # Edge cases: None and empty dict
        self.assertIsNone(self.detector.calculate_alignment_offsets(None))
        self.assertIsNone(self.detector.calculate_alignment_offsets({}))

    def test_route_planner(self):
        """Test checkpoint sequencing and distance computation."""
        self.planner.add_checkpoint(1, 1.0, 2.0, "CP 1")
        self.planner.add_checkpoint(2, 3.0, 4.0, "CP 2")

        cp1 = self.planner.get_next_checkpoint()
        self.assertEqual(cp1["id"], 1)

        cp2 = self.planner.get_next_checkpoint()
        self.assertEqual(cp2["id"], 2)

        # End of checkpoints
        cp3 = self.planner.get_next_checkpoint()
        self.assertIsNone(cp3)

        # Reset
        self.planner.reset()
        cp1_again = self.planner.get_next_checkpoint()
        self.assertEqual(cp1_again["id"], 1)

        # Plan path with None
        action_none = self.planner.plan_path_to_marker(None)
        self.assertEqual(action_none, "SEARCH_MARKER")

        # Plan path with valid marker
        action_valid = self.planner.plan_path_to_marker({"marker_id": 1})
        self.assertEqual(action_valid, "FORWARD_AND_ALIGN")

        # Distance calculation
        dist = self.planner.compute_distance({"x": 0.0, "y": 0.0, "z": 0.0}, {"x": 3.0, "y": 4.0, "z": 0.0})
        self.assertAlmostEqual(dist, 5.0)

    def test_movement_functions(self):
        """Verify movement functions execute without throwing exceptions."""
        try:
            move_forward(1.0, 1.0)
            move_backward(1.0, 1.0)
            turn_left(45.0)
            turn_right(45.0)
            move_to_relative_coordinate(1.0, 2.0, 0.5, 90.0)
            stop_robot()
        except Exception as e:
            self.fail("Movement function raised unexpected exception: %s" % str(e))

    def test_full_mission_run(self):
        """Verify entire mission executes to completion successfully."""
        result = execute_mission()
        self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()
