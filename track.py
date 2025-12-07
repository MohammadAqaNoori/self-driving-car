# track.py  ← ONE SUPER CLEAR WIDE ROAD
import math
def get_track_points():
    points = []
    cx, cy = 640, 360
    radius = 380
    for i in range(0, 1000, 4):
        angle = math.radians(i * 0.8)
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle * 1.3)
        points.append((int(x), int(y)))
    return points