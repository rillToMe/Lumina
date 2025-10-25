from __future__ import annotations
import glfw

_keys_down = set()
_mouse_down = set()
_mouse_pos = (0, 0)
_scroll_delta = (0.0, 0.0)

def _cb_key(window, key, scancode, action, mods):
    if action == glfw.PRESS:
        _keys_down.add(key)
    elif action == glfw.RELEASE:
        if key in _keys_down:
            _keys_down.remove(key)

def _cb_mouse(window, button, action, mods):
    if action == glfw.PRESS:
        _mouse_down.add(button)
    elif action == glfw.RELEASE:
        if button in _mouse_down:
            _mouse_down.remove(button)

def _cb_cursor(window, x, y):
    global _mouse_pos
    _mouse_pos = (int(x), int(y))

def _cb_scroll(window, dx, dy):
    
    global _scroll_delta
    _scroll_delta = (_scroll_delta[0] + dx, _scroll_delta[1] + dy)

def bind_window(window):
    glfw.set_key_callback(window, _cb_key)
    glfw.set_mouse_button_callback(window, _cb_mouse)
    glfw.set_cursor_pos_callback(window, _cb_cursor)
    glfw.set_scroll_callback(window, _cb_scroll)

def poll_input(window=None, scene=None):
    global _scroll_delta
    _scroll_delta = (0.0, 0.0)

def key_pressed(key): return key in _keys_down
def mouse_pressed(button=glfw.MOUSE_BUTTON_LEFT): return button in _mouse_down
def mouse(): return _mouse_pos
def scroll_delta(): return _scroll_delta
