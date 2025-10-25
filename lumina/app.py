from __future__ import annotations
import time
import glfw
import moderngl

class App:
    def __init__(self, width=1280, height=720, title="Lumina", vsync=True, clear_color=(0.07,0.07,0.1,1)):
        if not glfw.init():
            raise RuntimeError("GLFW init failed")
        glfw.window_hint(glfw.RESIZABLE, glfw.TRUE)
        self.window = glfw.create_window(width, height, title, None, None)
        if not self.window:
            glfw.terminate(); raise RuntimeError("Window creation failed")
        glfw.make_context_current(self.window)
        glfw.swap_interval(1 if vsync else 0)
        self.ctx = moderngl.create_context()
        self.scene = None
        self._last = time.time()
        self.clear_color = clear_color
        self.size = glfw.get_framebuffer_size(self.window)
        
        from . import input as _inp
        _inp.bind_window(self.window)

    def set_scene(self, scene):
        self.scene = scene
        scene.app = self

    def run(self):
        from .input import poll_input
        while not glfw.window_should_close(self.window):
            now = time.time()
            dt = now - self._last
            self._last = now

            glfw.poll_events()
            self.size = glfw.get_framebuffer_size(self.window)
            self.ctx.viewport = (0,0,self.size[0], self.size[1])
            self.ctx.clear(*self.clear_color)

            poll_input(self.window, self.scene)

            if self.scene:
                self.scene.update(dt)
                self.scene.draw(self.size[0], self.size[1])

            glfw.swap_buffers(self.window)
        glfw.terminate()
