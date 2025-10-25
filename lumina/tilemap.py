from __future__ import annotations
from typing import List
from .scene import Node
from .render import get_renderer
from .assets import get_assets

class TileSet:
    def __init__(self, image_path: str, tile_w: int, tile_h: int):
        self.image_path=image_path; self.tile_w=tile_w; self.tile_h=tile_h
        self._tex=None; self._size=None; self._uv_cache={}

    def _ensure(self, app):
        if self._tex is None:
            t = get_assets(app).texture(self.image_path)
            self._tex, self._size = t.tex, t.size

    def uv_for_index(self, idx: int):
        if idx in self._uv_cache: return self._uv_cache[idx]
        W,H = self._size
        cols = W//self.tile_w
        i = idx % cols; j = idx // cols
        u0 = (i*self.tile_w)/W; v0=(j*self.tile_h)/H
        u1 = ((i+1)*self.tile_w)/W; v1=((j+1)*self.tile_h)/H
        self._uv_cache[idx] = (u0,v0,u1,v1)
        return self._uv_cache[idx]

class TileMap(Node):
    def __init__(self, tileset: TileSet, grid: List[List[int]], x=0, y=0):
        super().__init__(x,y)
        self.tileset=tileset
        self.grid=grid

    def update(self, dt: float):
        pass

    def draw(self, W,H):
        app = self.get_app()
        r = get_renderer(app)
        cam = self.get_camera()
        if cam: r.set_camera(cam.pos, cam.zoom)
        else:   r.set_camera((0,0),1.0)
        self.tileset._ensure(app)
        tw,th = self.tileset.tile_w, self.tileset.tile_h
        tex = self.tileset._tex
        gx,gy = self.global_pos()
        for j,row in enumerate(self.grid):
            for i,idx in enumerate(row):
                if idx<0: continue
                uv = self.tileset.uv_for_index(idx)
                r.draw_quad(gx+i*tw, gy+j*th, tw, th, tex=tex, uv=uv, res=(W,H))
