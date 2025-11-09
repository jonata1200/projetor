import random

# =============================================================================
# Classe Base para Animações
# =============================================================================

class BaseAnimation:
    def __init__(self, canvas, label_window_id):
        self.canvas = canvas
        self.label_window_id = label_window_id
        self.is_running = False
        self._after_id = None
        self.particles = []

    def start(self):
        if not self.is_running:
            self.is_running = True
            self.update_frame()

    def stop(self):
        self.is_running = False
        if self._after_id: self.canvas.after_cancel(self._after_id)

    def on_resize(self, width, height):
        raise NotImplementedError

    def update_frame(self):
        raise NotImplementedError

# =============================================================================
# Animação 1: Neve
# =============================================================================

class SnowFlake:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.x, self.y = random.randint(0, self.w), random.randint(-self.h, 0)
        self.size = random.randint(2, 5)
        self.speed = random.uniform(0.5, 2.0)
        self.drift = random.uniform(-0.3, 0.3)
    def move(self):
        self.y += self.speed; self.x += self.drift
        if self.y > self.h or self.x < 0 or self.x > self.w: self.y, self.x = random.randint(-50, -10), random.randint(0, self.w)

class SnowAnimation(BaseAnimation):
    NUM_PARTICLES, DELAY = 150, 30
    def on_resize(self, width, height): self.particles = [SnowFlake(width, height) for _ in range(self.NUM_PARTICLES)]
    def update_frame(self):
        if not self.is_running: return
        self.canvas.delete("anim_particle")
        # A cor será passada pelo __init__ da ProjectionWindow
        color = getattr(self, 'particle_color', 'white')
        for p in self.particles:
            p.move()
            x1, y1, x2, y2 = p.x - p.size, p.y - p.size, p.x + p.size, p.y + p.size
            self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline="", tags="anim_particle")
        self.canvas.tag_lower("anim_particle")
        if self.label_window_id: self.canvas.tag_raise(self.label_window_id)
        self._after_id = self.canvas.after(self.DELAY, self.update_frame)

# =============================================================================
# Animação 2: Partículas Flutuantes
# =============================================================================

class FloatingParticle:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.x, self.y = random.randint(0, self.w), random.randint(0, self.h)
        self.size = random.randint(2, 4)
        self.speed = random.uniform(0.3, 1.2)
        self.drift = random.uniform(-0.2, 0.2)
        self.alpha = random.uniform(0.1, 0.8)
    def move(self):
        self.y -= self.speed; self.x += self.drift
        if self.y < -self.size or self.x < 0 or self.x > self.w: self.y, self.x = self.h + self.size, random.randint(0, self.w)

class FloatingParticlesAnimation(BaseAnimation):
    NUM_PARTICLES, DELAY = 100, 30
    def on_resize(self, width, height): self.particles = [FloatingParticle(width, height) for _ in range(self.NUM_PARTICLES)]
    def update_frame(self):
        if not self.is_running: return
        self.canvas.delete("anim_particle")
        base_color_hex = getattr(self, 'particle_color', '#FFFFFF')
        try: # Converte a cor base de hex para RGB
            r, g, b = int(base_color_hex[1:3], 16), int(base_color_hex[3:5], 16), int(base_color_hex[5:7], 16)
        except (ValueError, IndexError):
            r, g, b = 255, 255, 255 # Fallback para branco
        for p in self.particles:
            p.move()
            # Aplica o alpha da partícula à cor base
            val_r, val_g, val_b = int(p.alpha * r), int(p.alpha * g), int(p.alpha * b)
            color = f'#{val_r:02x}{val_g:02x}{val_b:02x}'
            x1, y1, x2, y2 = p.x - p.size, p.y - p.size, p.x + p.size, p.y + p.size
            self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline="", tags="anim_particle")
        self.canvas.tag_lower("anim_particle")
        if self.label_window_id: self.canvas.tag_raise(self.label_window_id)
        self._after_id = self.canvas.after(self.DELAY, self.update_frame)