# -*- coding: utf-8 -*-
"""
code/movement.py
Robot Movement & Attitude Control Functions for Kibo-RPC Int-Ball2.
Compatible with Python 2.7 (ROS Melodic) and Python 3.
"""

def move_forward(speed=1.0, duration=1.0):
    """Move robot forward."""
    print("[Movement] Moving forward at speed %s for %ss" % (str(speed), str(duration)))

def move_backward(speed=1.0, duration=1.0):
    """Move robot backward."""
    print("[Movement] Moving backward at speed %s for %ss" % (str(speed), str(duration)))

def turn_left(angle_degrees=90.0):
    """Turn robot left (yaw counter-clockwise)."""
    print("[Movement] Turning left by %s degrees" % str(angle_degrees))

def turn_right(angle_degrees=90.0):
    """Turn robot right (yaw clockwise)."""
    print("[Movement] Turning right by %s degrees" % str(angle_degrees))

def move_to_relative_coordinate(dx=0.0, dy=0.0, dz=0.0, yaw=0.0):
    """Move robot along 3D relative translation and yaw angle."""
    print("[Movement] Relative move dx=%s, dy=%s, dz=%s, yaw=%s" % (str(dx), str(dy), str(dz), str(yaw)))

def stop_robot():
    """Emergency stop / halt robot motion."""
    print("[Movement] Robot stopped")

