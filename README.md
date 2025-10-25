# 🌌 Lumina - Modern Game Framework for Python

> A modern, lightweight, **pygame successor** built with ❤️ in Python.  
> Designed for performance, modularity, and beauty - powered by **ModernGL + GLFW + CSS-like UI styling**.

---

## ✨ Features

- 🖥️ **Modern Rendering** - GPU accelerated via [ModernGL](https://moderngl.readthedocs.io/).  
- 🪟 **Cross-Platform Windowing** - Uses [GLFW](https://www.glfw.org/) backend (no pygame dependency).  
- 🧱 **Scene Graph Architecture** - simple `Node` tree for sprites, UI, tiles, and effects.  
- 🎨 **CSS-Themed UI System** - buttons, layout rows, and style sheets powered by [`tinycss2`](https://github.com/Kozea/tinycss2).  
- 🧩 **Sprite & Tilemap Renderer** - batching, texture caching, sprite sheets, and tile-based maps.  
- 💫 **Particle System** - configurable emitters with color, speed, and lifetime.  
- 🔊 **Audio Support** - playback via `sounddevice` + `soundfile`.  
- 🔧 **Event System** - simple event bus for game-wide events.  
- 🧠 **Human-Readable API** - clean design; everything is Pythonic.  

---

## 🧩 Project Structure

```
Lumina/
├─ lumina/
│  ├─ app.py          # Main loop + window creation
│  ├─ scene.py        # Node graph & scene manager
│  ├─ render.py       # GPU renderer / shader batching
│  ├─ input.py        # Keyboard & mouse callbacks
│  ├─ ui.py           # UI system + CSS support
│  ├─ assets.py       # Texture / font cache
│  ├─ sprite.py       # Sprites & animation
│  ├─ tilemap.py      # TileSet / TileMap renderer
│  ├─ particles.py    # Particle system
│  └─ ...
├─ examples/
│  ├─ demo.py         # Example scene using all features
│  └─ assets/         # Images / textures / style.css
└─ README.md
```

---

## 🚀 Getting Started

### 1️⃣ Clone the repository
```bash
git clone https://github.com/rillToMe/Lumina.git
cd Lumina
```

### 2️⃣ Create a virtual environment
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install moderngl glfw Pillow tinycss2 numpy sounddevice soundfile
```

### 4️⃣ Run the demo
```bash
python -m examples.demo
```

---

## 📸 Screenshot

![Lumina Demo](examples/assets/screenshot.png)

> The `demo.py` scene showcases sprites, tilemaps, particles, and CSS-styled UI.

---

## ⚙️ Roadmap

| Version | Highlights |
|----------|-------------|
| **v0.3** | Core renderer, sprite/tilemap/UI system, particle engine |
| **v0.4** | Full CSS layout, flexbox-like UI, hover animations, font smoothing |
| **v0.5** | Scene transitions, shaders (bloom, vignette), hot reload, Tiled map support |
| **v1.0** | Stable release - Lumina Editor & plugin ecosystem |

---

## 💡 Example Usage

```python
from lumina import App, Scene, Sprite, Button, TileMap, TileSet

app = App(1280, 720, "Lumina Game")
scene = Scene()

player = Sprite("assets/player.png", 100, 200)
scene.add(player)

button = Button(20, 20, "Click Me")
button.on_click = lambda b: print("Hello, Lumina!")
scene.add(button)

app.set_scene(scene)
app.run()
```

---

## 🧑‍💻 Author
**rillToMe**  
🔗 [github.com/rillToMe](https://github.com/rillToMe)

---

## 🪄 License
MIT License © 2025 - Feel free to fork, hack, and create your world with **Lumina** 💜

---

> _“Code the light, build the world - Lumina.”_
