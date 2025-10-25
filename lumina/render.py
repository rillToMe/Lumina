from __future__ import annotations
import numpy as np
import moderngl

class Renderer:
    def __init__(self, ctx: moderngl.Context):
        self.ctx = ctx
        self.prog = ctx.program(
            vertex_shader='''
                #version 330
                in vec2 in_pos; in vec2 in_uv; in vec4 in_color;
                uniform vec2 u_res;
                uniform vec2 u_cam;       // camera offset (x,y)
                uniform float u_zoom;     // camera zoom
                out vec2 v_uv; out vec4 v_color;
                void main(){
                    vec2 p = (in_pos - u_cam) * u_zoom;
                    vec2 ndc = (p / u_res) * 2.0 - 1.0;
                    ndc.y = -ndc.y;
                    gl_Position = vec4(ndc,0,1);
                    v_uv = in_uv; v_color = in_color;
                }''',
            fragment_shader='''
                #version 330
                uniform sampler2D u_tex;
                in vec2 v_uv; in vec4 v_color;
                out vec4 f_color;
                void main(){
                    vec4 texc = texture(u_tex, v_uv);
                    f_color = texc * v_color;
                }'''
        )
        self.u_res = self.prog["u_res"]
        self.u_cam = self.prog["u_cam"]
        self.u_zoom = self.prog["u_zoom"]
        self.tex_white = ctx.texture((1,1), 4, bytes([255,255,255,255]))
        self.vbo = ctx.buffer(reserve=4*(2+2+4)*4)
        self.ibo = ctx.buffer(np.array([0,1,2, 0,2,3], dtype="i4").tobytes())
        self.vao = ctx.vertex_array(self.prog, [(self.vbo, "2f 2f 4f", "in_pos","in_uv","in_color")], self.ibo)
        self.current_tex = None

    def set_camera(self, cam_pos=(0,0), zoom=1.0):
        self.u_cam.value = cam_pos
        self.u_zoom.value = zoom

    def draw_quad(self, x,y,w,h, *, color=(1,1,1,1), tex=None, uv=(0,0,1,1), res=(800,600)):
        u0,v0,u1,v1 = uv
        verts = np.array([
            x,y, u0,v0, *color,
            x+w,y, u1,v0, *color,
            x+w,y+h, u1,v1, *color,
            x,y+h, u0,v1, *color,
        ], dtype="f4")
        self.vbo.write(verts.tobytes())
        (tex or self.tex_white).use(location=0)
        self.u_res.value = res
        self.vao.render()

_renderer_cache = {}
def get_renderer(app):
    if id(app) not in _renderer_cache:
        _renderer_cache[id(app)] = Renderer(app.ctx)
    return _renderer_cache[id(app)]
