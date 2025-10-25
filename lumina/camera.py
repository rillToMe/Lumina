from __future__ import annotations
class Camera:
    def __init__(self, x=0, y=0, zoom=1.0):
        self.x=float(x); self.y=float(y); self.zoom=float(zoom)
    @property
    def pos(self): return (self.x, self.y)
    def move(self, dx, dy): self.x += dx; self.y += dy; return self
    def set(self, x, y): self.x=x; self.y=y; return self
    def set_zoom(self, z): self.zoom = max(0.1, float(z)); return self
