"""
code/main.py
Code ចម្បងសម្រាប់ដំណើរការ Robot (Main Program Entry Point)
"""

import time
from movement import move_forward, stop_robot, turn_left, turn_right
from marker_reader import init_camera, read_ar_marker
from route_planner import RoutePlanner

def main():
    print("=== [ibo-RPC-Team] Starting Robot Control System ===")
    
    # 1. Initialize sensors / Camera
    init_camera()
    
    # 2. Setup Route Planner
    planner = RoutePlanner()
    planner.add_checkpoint(1, 1.0, 0.0, "Checkpoint 1")
    planner.add_checkpoint(2, 2.0, 1.0, "Checkpoint 2")
    
    # 3. Main Control Loop
    try:
        print("[Main] Beginning mission execution...")
        move_forward(speed=1.0, duration=2.0)
        
        # Read Marker
        marker = read_ar_marker()
        if marker:
            print(f"[Main] Detected Marker: {marker}")
            action = planner.plan_path_to_marker(marker)
            print(f"[Main] Planned Action: {action}")
            
        turn_left(90)
        move_forward(speed=0.5, duration=1.0)
        stop_robot()
        print("=== Mission Completed Successfully ===")
        
    except KeyboardInterrupt:
        print("\n[Main] Program stopped by user.")
        stop_robot()
    except Exception as e:
        print(f"\n[Main] Error encountered: {e}")
        stop_robot()

if __name__ == "__main__":
    main()
