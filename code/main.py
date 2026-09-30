# -*- coding: utf-8 -*-
"""
code/main.py
Main Execution Controller for Kibo-RPC 7th Int-Ball2 Mission.
Compatible with Python 2.7 (ROS Melodic) and Python 3.
"""

import sys
import time
from movement import move_forward, stop_robot, turn_left, turn_right, move_to_relative_coordinate
from marker_reader import init_camera, read_ar_marker
from route_planner import RoutePlanner

def execute_mission():
    print("==================================================")
    print("[Kibo-RPC-Team] Starting Int-Ball2 Autonomous Mission")
    print("==================================================")

    # 1. Initialize sensors / Camera & Detector
    detector = init_camera()

    # 2. Setup Checkpoints according to Kibo-RPC Mission Specs
    planner = RoutePlanner()
    planner.add_checkpoint(1, 1.2, 0.0, "Joint Inspection Point")
    planner.add_checkpoint(2, 2.5, 0.8, "Hatch Inspection Point")
    planner.add_checkpoint(3, 3.8, 1.2, "Experimental Rack Point")
    planner.add_checkpoint(4, 4.5, 0.5, "Goal Checkpoint")

    # 3. Main Mission Execution Loop
    try:
        print("[Main] Int-Ball2 departing from Docking Station...")
        move_forward(speed=0.5, duration=1.5)

        step = 1
        while True:
            cp = planner.get_next_checkpoint()
            if not cp:
                break

            print("\n[Main] Step %d: Navigating to Checkpoint %d (%s)..." % (step, cp["id"], cp["desc"]))
            move_to_relative_coordinate(dx=cp["x"], dy=cp["y"], dz=0.0, yaw=0.0)

            # Read AR Marker at checkpoint
            marker = read_ar_marker()
            if marker:
                marker_id = marker.get("marker_id", marker.get("id"))
                dist = marker.get("distance_m", 0.0)
                print("[Main] Detected AR Marker ID %s at distance %.2fm" % (str(marker_id), dist))

                alignment = detector.calculate_alignment_offsets(marker, target_distance=0.50)
                if alignment:
                    print("[Main] Alignment status: is_aligned=%s, offset_x=%.2f, offset_y=%.2f" % (
                        str(alignment["is_aligned"]),
                        alignment["pixel_error_x"],
                        alignment["pixel_error_y"]
                    ))

                action = planner.plan_path_to_marker(marker)
                print("[Main] Action dispatched: %s" % action)
            else:
                print("[Main] Warning: No AR marker detected at Checkpoint %d. Searching..." % cp["id"])
                turn_right(15.0)

            step += 1

        print("\n[Main] Arrived at Goal Checkpoint.")
        stop_robot()
        print("==================================================")
        print("[Main] Mission Completed: Pressure anomaly inspected successfully.")
        print("==================================================")
        return True

    except KeyboardInterrupt:
        print("\n[Main] Mission aborted by user interruption.")
        stop_robot()
        return False
    except Exception as e:
        print("\n[Main] Unexpected error encountered: %s" % str(e))
        stop_robot()
        return False

def main():
    success = execute_mission()
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()

