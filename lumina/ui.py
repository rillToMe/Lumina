# lumina/ui.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Tuple
from tinycss2 import parse_stylesheet_bytes
from .scene import Node
from .render import get_renderer
from .assets import get_assets
from .input import mouse, mouse_pressed

def _parse_color(val: str):
    val = val.strip().lower()
    if val.startswith("#"):
        h=val[1:]
        if len(h)==3: r,g,b=[int(c*2,16) for c in h]; a=255
        elif len(h)==6: r=int(h[0:2],16); g=int(h[2:4],16); b=int(h[4:6],16); a=255
        elif len(h)==8: r=int(h[0:2],16); g=int(h[2:4],16); b=int(h[4:6],16); a=int(h[6:8],16)
        else: r=g=b=255; a=255
        return (r/255,g/255,b/255,a/255)
    NAMED={'primary':'#7c3aed','secondary':'#22d3ee','accent':'#f59e0b','surface':'#1e1e2e','white':'#ffffff','black':'#000000'}
    return _parse_color(NAMED.get(val,'#ffffff'))

@dataclass
class Style:
    background: Tuple[float,float,float,float]=(0.12,0.12,0.18,1)
    color: Tuple[float,float,float,float]=(1,1,1,1)
    padding:int=8
    radius:int=8
    width:Optional[int]=None
    height:Optional[int]=None
    font_size:int=20
    direction:str="row"
    gap:int=8
    align:str="start"
    justify:str="start"

class StyleSheet:
    def __init__(self, css_bytes: bytes=b""):
        self.css_bytes=css_bytes
    def style(self, selector: str)->Style:
        if not self.css_bytes: return Style()
        rules = parse_stylesheet_bytes(self.css_bytes, skip_comments=True, skip_whitespace=True)
        d={'background':'#1e1e2e','color':'#ffffff','padding':'8','radius':'8','width':'','height':'','font_size':'20','direction':'row','gap':'8','align':'start','justify':'start'}
        for rule in rules:
            if getattr(rule,'type','')!='qualified-rule': continue
            pre = ''.join([t.serialize() for t in rule.prelude]).strip()
            if pre != selector: continue
            content = ''.join([t.serialize() for t in rule.content]).split(';')
            for decl in content:
                if ':' not in decl: continue
                k,v = decl.split(':',1); k=k.strip().replace('-','_'); v=v.strip()
                d[k]=v
        def to_int(x):
            s=''.join([c for c in x if c.isdigit()])
            return int(s) if s else None
        return Style(
            background=_parse_color(d['background']),
            color=_parse_color(d['color']),
            padding=int(''.join([c for c in d['padding'] if c.isdigit()]) or '8'),
            radius=int(''.join([c for c in d['radius'] if c.isdigit()]) or '8'),
            width=to_int(d.get('width','')),
            height=to_int(d.get('height','')),
            font_size=int(''.join([c for c in d.get('font_size','20') if c.isdigit()]) or 20),
            direction=d.get('direction','row'),
            gap=int(''.join([c for c in d.get('gap','8') if c.isdigit()]) or 8),
            align=d.get('align','start'),
            justify=d.get('justify','start'),
        )

class UIRoot(Node):
    def __init__(self, css_path:str|None=None):
        super().__init__(0,0); self.styles=StyleSheet()
        if css_path:
            try:
                with open(css_path,'rb') as f: self.styles=StyleSheet(f.read())
            except: pass

class UIElement(Node):
    def __init__(self, x=0,y=0,w=120,h=40, style:Style|None=None):
        super().__init__(x,y); self.w,self.h=w,h; self.style=style or Style(); self.hover=False; self.on_click=None
    def contains(self, px,py):
        gx,gy = self.global_pos()
        return (px>=gx and py>=gy and px<=gx+self.w and py<=gy+self.h)

class Row(UIElement):
    def __init__(self, x=0,y=0, style:Style|None=None):
        super().__init__(x,y, style=style)
    def update(self, dt: float):
        super().update(dt)
        x,y = self.x + self.style.padding, self.y + self.style.padding
        if self.style.direction == "row":
            for ch in self.children:
                ch.x = x; ch.y = y
                x += getattr(ch,'w',0) + self.style.gap
        else:
            for ch in self.children:
                ch.x = x; ch.y = y
                y += getattr(ch,'h',0) + self.style.gap
        if not self.style.width:
            if self.style.direction=="row":
                total = sum(getattr(c,'w',0) for c in self.children) + self.style.gap*max(0,len(self.children)-1)
                self.w = total + self.style.padding*2
            else:
                self.w = max((getattr(c,'w',0) for c in self.children), default=0) + self.style.padding*2
        else:
            self.w = self.style.width
        if not self.style.height:
            if self.style.direction=="row":
                self.h = max((getattr(c,'h',0) for c in self.children), default=0) + self.style.padding*2
            else:
                total = sum(getattr(c,'h',0) for c in self.children) + self.style.gap*max(0,len(self.children)-1)
                self.h = total + self.style.padding*2
        else:
            self.h = self.style.height

    def draw(self,W,H):
        app = self.get_app()
        r = get_renderer(app)
        cam = self.get_camera()
        if cam: r.set_camera(cam.pos, cam.zoom)
        else:   r.set_camera((0,0),1.0)
        r.draw_quad(self.x,self.y,self.w,self.h, color=self.style.background, res=(W,H))
        super().draw(W,H)

class Button(UIElement):
    def __init__(self, x=0,y=0,text="Button", style:Style|None=None):
        super().__init__(x,y, style=style); self.text=text
        self._autosize()
    def _autosize(self):
        w = max(64, int(self.style.font_size*0.56*len(self.text))+self.style.padding*2)
        h = int(self.style.font_size+16)+self.style.padding*2
        if self.style.width: w=self.style.width
        if self.style.height: h=self.style.height
        self.w,self.h=w,h
    def update(self, dt: float):
        super().update(dt)
        mx,my = mouse()
        self.hover = self.contains(mx,my)
        if self.hover and mouse_pressed() and self.on_click: self.on_click(self)
    def draw(self,W,H):
        app = self.get_app()
        r = get_renderer(app)
        cam = self.get_camera()
        if cam: r.set_camera(cam.pos, cam.zoom)
        else:   r.set_camera((0,0),1.0)
        base = self.style.background
        if self.hover:
            base = (min(1,base[0]+0.1), min(1,base[1]+0.1), min(1,base[2]+0.1), base[3])
        r.draw_quad(self.x,self.y,self.w,self.h, color=base, res=(W,H))
        assets = get_assets(app)
        tex = assets.text_texture(self.text, size=self.style.font_size)
        tw,th = tex.size
        tx = self.x + (self.w-tw)//2
        ty = self.y + (self.h-th)//2
        r.draw_quad(tx,ty,tw,th, color=self.style.color, tex=tex.tex, res=(W,H))
