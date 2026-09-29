"""
code/movement.py
Function សម្រាប់បញ្ជាការធ្វើដំណើររបស់ Robot (Robot Movement Functions)
"""

def move_forward(speed: float = 1.0, duration: float = 1.0):
    """បញ្ជា Robot ឱ្យទៅមុខ"""
    print(f"[Movement] Moving forward at speed {speed} for {duration}s")

def move_backward(speed: float = 1.0, duration: float = 1.0):
    """បញ្ជា Robot ឱ្យថយក្រោយ"""
    print(f"[Movement] Moving backward at speed {speed} for {duration}s")

def turn_left(angle_degrees: float = 90.0):
    """បញ្ជា Robot ឱ្យបត់ឆ្វេង"""
    print(f"[Movement] Turning left by {angle_degrees} degrees")

def turn_right(angle_degrees: float = 90.0):
    """បញ្ជា Robot ឱ្យបត់ស្តាំ"""
    print(f"[Movement] Turning right by {angle_degrees} degrees")

def stop_robot():
    """បញ្ឈប់ Robot ភ្លាមៗ"""
    print("[Movement] Robot stopped")
