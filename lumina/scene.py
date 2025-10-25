# lumina/scene.py
from __future__ import annotations
from typing import List, Optional

class Node:
    def __init__(self, x=0, y=0):
        self.x,self.y = x,y
        self.children: List[Node] = []
        self.parent: Optional[Node] = None
        self.visible = True

    def add(self,*nodes):
        for n in nodes:
            n.parent=self
            self.children.append(n)
        return self

    def global_pos(self):
        if self.parent:
            px,py = self.parent.global_pos()
            return self.x+px, self.y+py
        return self.x, self.y

    def get_scene(self) -> Optional["Scene"]:
        n = self
        while n is not None:
            if isinstance(n, Scene):
                return n
            n = n.parent
        return None

    def get_app(self):
        sc = self.get_scene()
        return getattr(sc, "app", None)

    def get_camera(self):
        sc = self.get_scene()
        return getattr(sc, "camera", None)

    def update(self, dt: float):
        for c in self.children: 
            c.update(dt)

    def draw(self, w:int, h:int):
        for c in self.children: 
            c.draw(w,h)

class Scene(Node):
    def __init__(self):
        super().__init__()
        self.app=None
        self.camera=None

    def set_camera(self, camera):
        self.camera = camera
