from __future__ import annotations
import random, math
from dataclasses import dataclass
from typing import List
from .render import get_renderer

@dataclass
class P:
    x:float; y:float; vx:float; vy:float; life:float; r:float; g:float; b:float; a:float; size:float

class ParticleSystem:
    def __init__(self, x=0, y=0, rate=60, life=(0.5,1.5), speed=(50,150), spread=math.pi, color=(1,1,1,1), size=(2,6)):
        self.x=x; self.y=y
        self.rate=rate
        self.life_range=life
        self.speed_range=speed
        self.spread=spread
        self.color=color
        self.size_range=size
        self.particles: List[P] = []
        self._acc=0.0
        self.parent=None  

    def emit(self, n=1):
        for _ in range(n):
            ang = (random.random()-0.5)*self.spread
            spd = random.uniform(*self.speed_range)
            vx = math.cos(ang)*spd; vy = math.sin(ang)*spd
            life = random.uniform(*self.life_range)
            size = random.uniform(*self.size_range)
            r,g,b,a = self.color
            self.particles.append(P(self.x,self.y,vx,vy,life,r,g,b,a,size))

    def update(self, dt: float):
        self._acc += dt*self.rate
        while self._acc>=1.0: self.emit(1); self._acc-=1.0
        alive=[]
        for p in self.particles:
            p.life -= dt
            if p.life<=0: continue
            p.x += p.vx*dt; p.y += p.vy*dt
            p.a = max(0.0, p.a - dt*1.0)
            alive.append(p)
        self.particles = alive

    def draw(self, W,H):
        node = getattr(self, "parent", None)
        app = node.get_app() if node else None
        r = get_renderer(app)
        cam = node.get_camera() if node else None
        if cam: r.set_camera(cam.pos, cam.zoom)
        else:   r.set_camera((0,0),1.0)
        for p in self.particles:
            r.draw_quad(p.x, p.y, p.size, p.size, color=(p.r,p.g,p.b,p.a), res=(W,H))
