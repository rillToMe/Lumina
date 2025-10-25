from __future__ import annotations
from PIL import Image, ImageFont, ImageDraw
from dataclasses import dataclass
from typing import Dict, Tuple
import moderngl

@dataclass
class Texture:
    tex: moderngl.Texture
    size: Tuple[int,int]

class AssetLoader:
    def __init__(self, app):
        self.app = app
        self.cache: Dict[str, Texture] = {}
        self.fonts: Dict[tuple, ImageFont.FreeTypeFont] = {}

    def texture(self, path: str) -> Texture:
        if path in self.cache: return self.cache[path]
        img = Image.open(path).convert("RGBA")
        tex = self.app.ctx.texture(img.size, 4, img.tobytes())
        out = Texture(tex, img.size)
        self.cache[path] = out
        return out

    def font(self, name="DejaVuSans.ttf", size=20):
        key=(name,size)
        if key not in self.fonts:
            try: self.fonts[key]=ImageFont.truetype(name,size)
            except: self.fonts[key]=ImageFont.load_default()
        return self.fonts[key]

    def text_texture(self, text:str, size=20, color=(255,255,255,255), font="DejaVuSans.ttf"):
        f = self.font(font, size)
        tmp = Image.new("RGBA", (2,2), (0,0,0,0))
        d = ImageDraw.Draw(tmp)
        w = int(d.textlength(text, font=f))+4
        h = int(size+6)
        img = Image.new("RGBA", (w,h), (0,0,0,0))
        d = ImageDraw.Draw(img)
        d.text((2,0), text, fill=color, font=f)
        tex = self.app.ctx.texture(img.size, 4, img.tobytes())
        return Texture(tex, img.size)

_assets_cache={}
def get_assets(app):
    if id(app) not in _assets_cache:
        _assets_cache[id(app)] = AssetLoader(app)
    return _assets_cache[id(app)]
