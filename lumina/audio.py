class Sound:
    def __init__(self, path: str):
        self.path = path
        self._ok=False
        try:
            import sounddevice as sd, soundfile as sf
            self.sd=sd; self.sf=sf; self._ok=True
        except Exception:
            self.sd=None; self.sf=None
    def play(self):
        if not self._ok:
            print("[Lumina] audio off (install sounddevice & soundfile)"); return
        data, sr = self.sf.read(self.path, dtype='float32')
        self.sd.play(data, sr, blocking=False)
