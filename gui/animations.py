import random
import math

class BaseAnimation:
    """Classe base para todas as animações de fundo."""
    def __init__(self, canvas):
        self.canvas = canvas
        self.is_running = False
        self._after_id = None

    def start(self):
        if not self.is_running:
            self.is_running = True
            self.update_frame()

    def stop(self):
        self.is_running = False
        if self._after_id:
            self.canvas.after_cancel(self._after_id)

    def update_frame(self):
        """Este método deve ser implementado por cada subclasse de animação."""
        raise NotImplementedError

# --- ANIMAÇÃO 1: Neve (Refatorada) ---
class SnowFlake:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.x = random.randint(0, self.w)
        self.y = random.randint(-self.h, 0)
        self.size = random.randint(2, 5)
        self.speed = random.uniform(0.5, 2.0)
        self.drift = random.uniform(-0.3, 0.3)
    def move(self):
        self.y += self.speed; self.x += self.drift
        if self.y > self.h or self.x < 0 or self.x > self.w:
            self.y = random.randint(-50, -10); self.x = random.randint(0, self.w)

class SnowAnimation(BaseAnimation):
    NUM_PARTICLES = 150
    DELAY = 30
    def __init__(self, canvas):
        super().__init__(canvas)
        self.particles = [SnowFlake(self.canvas.winfo_width(), self.canvas.winfo_height()) for _ in range(self.NUM_PARTICLES)]

    def update_frame(self):
        if not self.is_running: return
        self.canvas.delete("anim_particle")
        for p in self.particles:
            p.move()
            x1, y1, x2, y2 = p.x - p.size, p.y - p.size, p.x + p.size, p.y + p.size
            self.canvas.create_oval(x1, y1, x2, y2, fill="white", outline="", tags="anim_particle")
        self.canvas.tag_lower("anim_particle")
        self._after_id = self.canvas.after(self.DELAY, self.update_frame)

# --- ANIMAÇÃO 2: Partículas Flutuantes ---
class FloatingParticle:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.x = random.randint(0, self.w); self.y = random.randint(0, self.h)
        self.size = random.randint(2, 4)
        self.speed = random.uniform(0.3, 1.2)
        self.drift = random.uniform(-0.2, 0.2)
        self.alpha = random.uniform(0.1, 0.8)
    def move(self):
        self.y -= self.speed; self.x += self.drift
        if self.y < -self.size or self.x < 0 or self.x > self.w:
            self.y = self.h + self.size; self.x = random.randint(0, self.w)

class FloatingParticlesAnimation(BaseAnimation):
    NUM_PARTICLES = 100
    DELAY = 30
    def __init__(self, canvas):
        super().__init__(canvas)
        self.particles = [FloatingParticle(self.canvas.winfo_width(), self.canvas.winfo_height()) for _ in range(self.NUM_PARTICLES)]

    def update_frame(self):
        if not self.is_running: return
        self.canvas.delete("anim_particle")
        for p in self.particles:
            p.move()
            val = int(p.alpha * 255)
            color = f'#{val:02x}{val:02x}{val:02x}' # Finge transparência com tons de cinza
            x1, y1, x2, y2 = p.x - p.size, p.y - p.size, p.x + p.size, p.y + p.size
            self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline="", tags="anim_particle")
        self.canvas.tag_lower("anim_particle")
        self._after_id = self.canvas.after(self.DELAY, self.update_frame)

# --- ANIMAÇÃO 3: Estrelas Cintilantes ---
class Star:
    def __init__(self, w, h):
        self.x, self.y = random.randint(0, w), random.randint(0, h)
        self.size = random.uniform(0.5, 2.5)
        self.alpha = random.uniform(0.1, 1.0)
        self.twinkle_speed = random.uniform(0.01, 0.05)
        self.cycle = random.uniform(0, 2 * math.pi)
    def twinkle(self):
        self.cycle += self.twinkle_speed
        self.alpha = (math.sin(self.cycle) + 1) / 2 # Varia alpha suavemente entre 0 e 1

class SparklingStarsAnimation(BaseAnimation):
    NUM_PARTICLES = 200
    DELAY = 40
    def __init__(self, canvas):
        super().__init__(canvas)
        self.particles = [Star(self.canvas.winfo_width(), self.canvas.winfo_height()) for _ in range(self.NUM_PARTICLES)]

    def update_frame(self):
        if not self.is_running: return
        self.canvas.delete("anim_particle")
        for p in self.particles:
            p.twinkle()
            val = int(p.alpha * 200) + 55 # Garante que a estrela nunca fique totalmente preta
            color = f'#{val:02x}{val:02x}{val:02x}'
            x1, y1, x2, y2 = p.x - p.size, p.y - p.size, p.x + p.size, p.y + p.size
            self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline="", tags="anim_particle")
        self.canvas.tag_lower("anim_particle")
        self._after_id = self.canvas.after(self.DELAY, self.update_frame)

# --- ANIMAÇÃO 4: Linhas de Conexão (Plexus) ---
class Node:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.x, self.y = random.randint(0, w), random.randint(0, h)
        self.vx, self.vy = random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5)
        self.size = 2
    def move(self):
        self.x += self.vx; self.y += self.vy
        if self.x <= 0 or self.x >= self.w: self.vx *= -1
        if self.y <= 0 or self.y >= self.h: self.vy *= -1

class ConnectingLinesAnimation(BaseAnimation):
    NUM_PARTICLES = 70
    DELAY = 25
    CONNECTION_DISTANCE = 120
    def __init__(self, canvas):
        super().__init__(canvas)
        self.particles = [Node(self.canvas.winfo_width(), self.canvas.winfo_height()) for _ in range(self.NUM_PARTICLES)]

    def update_frame(self):
        if not self.is_running: return
        self.canvas.delete("anim_particle")
        for p in self.particles: p.move()
        
        for i in range(len(self.particles)):
            for j in range(i + 1, len(self.particles)):
                p1, p2 = self.particles[i], self.particles[j]
                dist = math.hypot(p1.x - p2.x, p1.y - p2.y)
                if dist < self.CONNECTION_DISTANCE:
                    alpha = 1 - (dist / self.CONNECTION_DISTANCE)
                    val = int(alpha * 128) # Linhas mais sutis
                    color = f'#{val:02x}{val:02x}{val:02x}'
                    self.canvas.create_line(p1.x, p1.y, p2.x, p2.y, fill=color, tags="anim_particle")
        
        self.canvas.tag_lower("anim_particle")
        self._after_id = self.canvas.after(self.DELAY, self.update_frame)