from lumina import App, Scene, Camera, Sprite, SpriteSheet, ParticleSystem
from lumina.ui import UIRoot, Button, Row
from lumina.tilemap import TileMap, TileSet

class Demo(Scene):
    def __init__(self):
        super().__init__()
        self.set_camera(Camera(0,0,1.0))

        self.ui = UIRoot('assets/style.css')
        self.add(self.ui)
        bar = Row(20,20, style=self.ui.styles.style('Row.toolbar'))
        btn = Button(0,0, text='Hello Lumina', style=self.ui.styles.style('Button.primary'))
        btn.on_click = lambda b: print('Clicked!')
        bar.add(btn)
        self.add(bar)

        self.hero = Sprite('assets/crate.png', x=120, y=120, w=128, h=128)
        self.add(self.hero)

        self.pfx = ParticleSystem(x=260, y=180, color=(1,0.7,0.2,1), spread=3.14, rate=80)
        self.add(self.pfx)

        ts = TileSet('assets/crate.png', 64, 64)
        grid = [[0 if (i+j)%2==0 else -1 for i in range(10)] for j in range(6)]
        self.map = TileMap(ts, grid, x=400, y=280)
        self.add(self.map)

        self.t=0

    def update(self, dt):
        super().update(dt)
        self.t += dt
        self.hero.x = 120 + 40 * __import__("math").sin(self.t*2.0)
        self.pfx.update(dt)

    def draw(self, w, h):
        from lumina.render import get_renderer
        r = get_renderer(self.app)
        cx = 280 + 100*__import__("math").sin(self.t)
        cy = 220 + 60*__import__("math").cos(self.t*0.7)
        if self.camera: r.set_camera(self.camera.pos, self.camera.zoom)
        r.draw_quad(cx,cy, 240, 160, color=(0.3,0.1,0.6,0.35), res=(w,h))
        super().draw(w,h)

if __name__ == "__main__":
    app = App(1024, 600, "Lumina v0.3")
    app.set_scene(Demo())
    app.run()
