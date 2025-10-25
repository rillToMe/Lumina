from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple
from .scene import Node
from .render import get_renderer
from .assets import get_assets

@dataclass
class Frame:
    uv: Tuple[float,float,float,float]

class Sprite(Node):
    def __init__(self, image_path: str, x=0, y=0, w=None, h=None, color=(1,1,1,1)):
        super().__init__(x,y)
        self.image_path=image_path
        self.w,self.h = w,h
        self.color=color
        self._tex=None
        self._size=None
        self.frames=[Frame((0,0,1,1))]
        self.frame=0

    def _ensure(self):
        if self._tex is None:
            app = self.get_app()
            t = get_assets(app).texture(self.image_path)
            self._tex, self._size = t.tex, t.size
            if self.w is None or self.h is None:
                self.w,self.h = self._size

    def draw(self, W,H):
        self._ensure()
        app = self.get_app()
        r = get_renderer(app)
        cam = self.get_camera()
        if cam: r.set_camera(cam.pos, cam.zoom)
        else:   r.set_camera((0,0), 1.0)
        x,y = self.global_pos()
        r.draw_quad(x,y,self.w,self.h, color=self.color, tex=self._tex, uv=self.frames[self.frame].uv, res=(W,H))

class SpriteSheet(Sprite):
    def __init__(self, image_path, frame_w, frame_h, columns=None, rows=None, x=0, y=0, fps=8, color=(1,1,1,1)):
        super().__init__(image_path, x,y, frame_w, frame_h, color)
        self.frame_w=frame_w; self.frame_h=frame_h
        self.columns=columns; self.rows=rows
        self.time=0; self.fps=fps

    def _ensure(self):
        super()._ensure()
        if len(self.frames)==1:
            W,H = self._size
            cols = self.columns or (W//self.frame_w)
            rows = self.rows or (H//self.frame_h)
            fs=[]
            for j in range(rows):
                for i in range(cols):
                    u0 = (i*self.frame_w)/W
                    v0 = (j*self.frame_h)/H
                    u1 = ((i+1)*self.frame_w)/W
                    v1 = ((j+1)*self.frame_h)/H
                    fs.append(Frame((u0,v0,u1,v1)))
            self.frames = fs

    def update(self, dt: float):
        super().update(dt)
        self.time += dt
        if self.fps>0 and self.frames:
            self.frame = int(self.time*self.fps) % len(self.frames)
