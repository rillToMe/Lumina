from collections import defaultdict
class EventBus:
    def __init__(self): self._h=defaultdict(list)
    def on(self, name, fn): self._h[name].append(fn); return fn
    def emit(self, name, *a, **k):
        for fn in list(self._h.get(name,())): fn(*a,**k)

_bus={}
def get_bus(app):
    if id(app) not in _bus: _bus[id(app)] = EventBus()
    return _bus[id(app)]
