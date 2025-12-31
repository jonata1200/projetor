import random
import math

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
        self.current_width = 0
        self.current_height = 0
        self._cached_rgb = (255, 255, 255)  # Cache para cores RGB (inicializado com branco)
        self._cached_color_string = None

    def start(self):
        if not self.is_running:
            self.is_running = True
            self.update_frame()

    def stop(self):
        self.is_running = False
        if self._after_id: self.canvas.after_cancel(self._after_id)

    def on_resize(self, width, height):
        # Só recria partículas se as dimensões realmente mudaram significativamente
        if abs(self.current_width - width) > 10 or abs(self.current_height - height) > 10:
            self.current_width = width
            self.current_height = height
            self._recreate_particles(width, height)
        else:
            # Atualiza apenas as dimensões das partículas existentes
            self._update_particles_dimensions(width, height)
    
    def _recreate_particles(self, width, height):
        """Método para recriar partículas - implementado pelas subclasses"""
        raise NotImplementedError
    
    def _update_particles_dimensions(self, width, height):
        """Atualiza dimensões das partículas existentes sem recriá-las - opcional nas subclasses"""
        # Por padrão, atualiza w e h de todas as partículas
        for particle in self.particles:
            if hasattr(particle, 'w'):
                particle.w = width
            if hasattr(particle, 'h'):
                particle.h = height
            # Para SpiralParticle, atualiza também max_dimension e max_radius
            if hasattr(particle, 'max_dimension'):
                particle.max_dimension = max(width, height)
                particle.max_radius = particle.max_dimension * 0.7

    def _get_rgb_color(self, color_string):
        """Obtém RGB da cor, usando cache para evitar winfo_rgb repetido."""
        if color_string != self._cached_color_string:
            try:
                rgb_16bit = self.canvas.winfo_rgb(color_string)
                self._cached_rgb = (rgb_16bit[0] // 256, rgb_16bit[1] // 256, rgb_16bit[2] // 256)
                self._cached_color_string = color_string
            except Exception:
                self._cached_rgb = (255, 255, 255)
                self._cached_color_string = color_string
        return self._cached_rgb

    def update_frame(self):
        raise NotImplementedError

# =============================================================================
# Animação 1: Neve
# =============================================================================
class SnowFlake:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.x, self.y = random.randint(0, self.w), random.randint(-self.h, 0)
        # --- ALTERAÇÃO 1 AQUI ---
        # Antes: self.size = random.randint(2, 5)
        self.size = random.randint(4, 9) # Flocos de neve visivelmente maiores
        self.speed = random.uniform(0.5, 2.0)
        self.drift = random.uniform(-0.3, 0.3)
    def move(self):
        self.y += self.speed; self.x += self.drift
        if self.y > self.h or self.x < 0 or self.x > self.w: self.y, self.x = random.randint(-50, -10), random.randint(0, self.w)

class SnowAnimation(BaseAnimation):
    NUM_PARTICLES, DELAY = 100, 35  # Reduzido partículas e aumentado delay para melhor performance
    def _recreate_particles(self, width, height): self.particles = [SnowFlake(width, height) for _ in range(self.NUM_PARTICLES)]
    def update_frame(self):
        if not self.is_running: return
        self.canvas.delete("anim_particle")
        color_string = getattr(self, 'particle_color', 'white')
        r, g, b = self._get_rgb_color(color_string)
        
        for p in self.particles:
            p.move()
            # Opacidade 100% (não usa alpha, usa a cor diretamente)
            val_r, val_g, val_b = r, g, b
            color = f'#{val_r:02x}{val_g:02x}{val_b:02x}'
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
        # --- ALTERAÇÃO 2 AQUI ---
        # Antes: self.size = random.randint(2, 4)
        self.size = random.randint(3, 7) # Partículas maiores
        self.speed = random.uniform(0.3, 1.2)
        self.drift = random.uniform(-0.2, 0.2)
        self.alpha = random.uniform(0.1, 0.8)
    def move(self):
        self.y -= self.speed; self.x += self.drift
        if self.y < -self.size or self.x < 0 or self.x > self.w: self.y, self.x = self.h + self.size, random.randint(0, self.w)

class FloatingParticlesAnimation(BaseAnimation):
    NUM_PARTICLES, DELAY = 100, 30
    def _recreate_particles(self, width, height): self.particles = [FloatingParticle(width, height) for _ in range(self.NUM_PARTICLES)]
    def update_frame(self):
        if not self.is_running: return
        self.canvas.delete("anim_particle")
        
        color_string = getattr(self, 'particle_color', 'white')
        try:
            rgb_16bit = self.canvas.winfo_rgb(color_string)
            r, g, b = rgb_16bit[0] // 256, rgb_16bit[1] // 256, rgb_16bit[2] // 256
        except Exception:
            r, g, b = 255, 255, 255

        for p in self.particles:
            p.move()
            val_r, val_g, val_b = int(p.alpha * r), int(p.alpha * g), int(p.alpha * b)
            color = f'#{val_r:02x}{val_g:02x}{val_b:02x}'
            x1, y1, x2, y2 = p.x - p.size, p.y - p.size, p.x + p.size, p.y + p.size
            self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline="", tags="anim_particle")
        self.canvas.tag_lower("anim_particle")
        if self.label_window_id: self.canvas.tag_raise(self.label_window_id)
        self._after_id = self.canvas.after(self.DELAY, self.update_frame)

# =============================================================================
# Animação 3: Estrelas Piscando
# =============================================================================
class StarParticle:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.reset()

    def reset(self):
        self.x = random.randint(0, self.w)
        self.y = random.randint(0, self.h)
        # --- ALTERAÇÃO 3 AQUI ---
        # Antes: self.size = random.uniform(1, 3)
        self.size = random.uniform(3, 7) # Estrelas mais visíveis
        self.max_brightness = random.uniform(0.4, 1.0)
        self.current_brightness = 0.0
        self.state = "brightening"
        self.speed = random.uniform(0.01, 0.04)

    def update(self):
        if self.state == "brightening":
            self.current_brightness += self.speed
            if self.current_brightness >= self.max_brightness:
                self.current_brightness = self.max_brightness
                self.state = "dimming"
        elif self.state == "dimming":
            self.current_brightness -= self.speed
            if self.current_brightness <= 0:
                self.reset()

class BlinkingStarsAnimation(BaseAnimation):
    NUM_PARTICLES, DELAY = 100, 30

    def _recreate_particles(self, width, height):
        self.particles = [StarParticle(width, height) for _ in range(self.NUM_PARTICLES)]
    
    def update_frame(self):
        if not self.is_running: return
        
        self.canvas.delete("anim_particle")
        
        color_string = getattr(self, 'particle_color', 'white')
        try:
            rgb_16bit = self.canvas.winfo_rgb(color_string)
            r, g, b = rgb_16bit[0] // 256, rgb_16bit[1] // 256, rgb_16bit[2] // 256
        except Exception:
            r, g, b = 255, 255, 255

        for p in self.particles:
            p.update()
            
            if p.current_brightness > 0:
                alpha = p.current_brightness
                val_r, val_g, val_b = int(alpha * r), int(alpha * g), int(alpha * b)
                color = f'#{val_r:02x}{val_g:02x}{val_b:02x}'
                
                x1, y1, x2, y2 = p.x - p.size, p.y - p.size, p.x + p.size, p.y + p.size
                self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline="", tags="anim_particle")
        
        self.canvas.tag_lower("anim_particle")
        if self.label_window_id: self.canvas.tag_raise(self.label_window_id)
        self._after_id = self.canvas.after(self.DELAY, self.update_frame)

# =============================================================================
# Animação 4: Chamas/Fogo
# =============================================================================
class FlameParticle:
    def __init__(self, w, h):
        self.w, self.h = w, h
        # Modificado para ocupar toda a largura da tela
        self.x = random.randint(0, self.w)
        self.y = self.h
        self.size = random.uniform(3, 8)
        self.speed = random.uniform(1.5, 4.0)
        self.life = 1.0
        self.decay = random.uniform(0.005, 0.015)
        self.drift = random.uniform(-0.5, 0.5)

    def update(self):
        self.y -= self.speed
        self.x += self.drift
        self.life -= self.decay
        self.size *= 0.99
        
        if self.life <= 0 or self.y < 0 or self.size < 1:
            # Modificado para ocupar toda a largura da tela
            self.x = random.randint(0, self.w)
            self.y = self.h
            self.life = 1.0
            self.size = random.uniform(3, 8)
            self.speed = random.uniform(1.5, 4.0)
            self.drift = random.uniform(-0.5, 0.5)

class FireAnimation(BaseAnimation):
    NUM_PARTICLES, DELAY = 120, 30

    def _recreate_particles(self, width, height):
        self.particles = [FlameParticle(width, height) for _ in range(self.NUM_PARTICLES)]
    
    def update_frame(self):
        if not self.is_running: return
        self.canvas.delete("anim_particle")
        
        color_string = getattr(self, 'particle_color', 'white')
        try:
            rgb_16bit = self.canvas.winfo_rgb(color_string)
            r, g, b = rgb_16bit[0] // 256, rgb_16bit[1] // 256, rgb_16bit[2] // 256
        except Exception:
            r, g, b = 255, 255, 255

        for p in self.particles:
            p.update()
            alpha = p.life * 0.8
            val_r = min(255, int(alpha * r + (1 - alpha) * 255))
            val_g = min(255, int(alpha * g + (1 - alpha) * 200))
            val_b = int(alpha * b)
            color = f'#{val_r:02x}{val_g:02x}{val_b:02x}'
            x1, y1, x2, y2 = p.x - p.size, p.y - p.size, p.x + p.size, p.y + p.size
            self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline="", tags="anim_particle")
        
        self.canvas.tag_lower("anim_particle")
        if self.label_window_id: self.canvas.tag_raise(self.label_window_id)
        self._after_id = self.canvas.after(self.DELAY, self.update_frame)

# =============================================================================
# Animação 6: Chuva
# =============================================================================
class RainDrop:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.x = random.randint(0, self.w)
        self.y = random.randint(-self.h, 0)
        self.length = random.uniform(15, 40)
        # Velocidade reduzida: de 3.0-7.0 para 1.5-3.5
        self.speed = random.uniform(1.5, 3.5)
        # Chuva mais grossa: aumentado de 1-2 para 2-4
        self.width = random.uniform(2, 4)

    def move(self):
        self.y += self.speed
        if self.y > self.h:
            self.y = random.randint(-50, 0)
            self.x = random.randint(0, self.w)

class RainAnimation(BaseAnimation):
    NUM_PARTICLES, DELAY = 120, 25  # Reduzido partículas e aumentado delay para melhor performance

    def _recreate_particles(self, width, height):
        self.particles = [RainDrop(width, height) for _ in range(self.NUM_PARTICLES)]
    
    def update_frame(self):
        if not self.is_running: return
        self.canvas.delete("anim_particle")
        
        color_string = getattr(self, 'particle_color', 'white')
        try:
            rgb_16bit = self.canvas.winfo_rgb(color_string)
            r, g, b = rgb_16bit[0] // 256, rgb_16bit[1] // 256, rgb_16bit[2] // 256
        except Exception:
            r, g, b = 255, 255, 255

        for p in self.particles:
            p.move()
            val_r, val_g, val_b = int(0.7 * r), int(0.7 * g), int(0.7 * b)
            color = f'#{val_r:02x}{val_g:02x}{val_b:02x}'
            x1, y1, x2, y2 = p.x, p.y, p.x + p.width, p.y + p.length
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=int(p.width), tags="anim_particle")
        
        self.canvas.tag_lower("anim_particle")
        if self.label_window_id: self.canvas.tag_raise(self.label_window_id)
        self._after_id = self.canvas.after(self.DELAY, self.update_frame)

# =============================================================================
# Animação 7: Pétalas de Flores
# =============================================================================
class PetalParticle:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.x = random.randint(0, self.w)
        self.y = random.randint(-self.h, 0)
        self.size = random.uniform(4, 10)
        self.speed = random.uniform(0.8, 2.5)
        self.rotation = random.uniform(0, 6.28)
        self.rotation_speed = random.uniform(-3, 3)
        self.drift = random.uniform(-0.5, 0.5)
        self.alpha = random.uniform(0.4, 0.9)

    def move(self):
        self.y += self.speed
        self.x += self.drift + math.sin(self.rotation) * 0.3
        self.rotation += self.rotation_speed * 0.01
        
        if self.y > self.h or self.x < -self.size or self.x > self.w + self.size:
            self.y = random.randint(-50, 0)
            self.x = random.randint(0, self.w)
            self.rotation = random.uniform(0, 6.28)

class PetalsAnimation(BaseAnimation):
    NUM_PARTICLES, DELAY = 80, 30

    def _recreate_particles(self, width, height):
        self.particles = [PetalParticle(width, height) for _ in range(self.NUM_PARTICLES)]
    
    def update_frame(self):
        if not self.is_running: return
        self.canvas.delete("anim_particle")
        
        color_string = getattr(self, 'particle_color', 'white')
        try:
            rgb_16bit = self.canvas.winfo_rgb(color_string)
            r, g, b = rgb_16bit[0] // 256, rgb_16bit[1] // 256, rgb_16bit[2] // 256
        except Exception:
            r, g, b = 255, 255, 255

        for p in self.particles:
            p.move()
            val_r, val_g, val_b = int(p.alpha * r), int(p.alpha * g), int(p.alpha * b)
            color = f'#{val_r:02x}{val_g:02x}{val_b:02x}'
            x1, y1, x2, y2 = p.x - p.size, p.y - p.size, p.x + p.size, p.y + p.size
            self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline="", tags="anim_particle")
        
        self.canvas.tag_lower("anim_particle")
        if self.label_window_id: self.canvas.tag_raise(self.label_window_id)
        self._after_id = self.canvas.after(self.DELAY, self.update_frame)

# =============================================================================
# Animação 9: Partículas em Espiral
# =============================================================================
class SpiralParticle:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.center_x = w / 2
        self.center_y = h / 2
        self.angle = random.uniform(0, 6.28)
        # Usa o maior lado da tela para permitir espiral maior
        self.max_dimension = max(w, h)
        self.radius = random.uniform(0, self.max_dimension / 4)
        self.angular_speed = random.uniform(0.005, 0.01)  # Reduzido ainda mais: de 0.01-0.02 para 0.005-0.01
        self.radius_speed = random.uniform(0.1, 0.4)      # Reduzido ainda mais: de 0.2-0.8 para 0.1-0.4
        self.size = random.uniform(2, 5)
        # Aumentado para ocupar mais espaço - usa até 70% da maior dimensão
        self.max_radius = self.max_dimension * 0.7

    def update(self):
        self.angle += self.angular_speed
        self.radius += self.radius_speed
        
        if self.radius > self.max_radius:
            self.radius = 0
            self.angle = random.uniform(0, 6.28)
        
        self.x = self.center_x + math.cos(self.angle) * self.radius
        self.y = self.center_y + math.sin(self.angle) * self.radius

class SpiralAnimation(BaseAnimation):
    NUM_PARTICLES, DELAY = 100, 30

    def _recreate_particles(self, width, height):
        self.particles = [SpiralParticle(width, height) for _ in range(self.NUM_PARTICLES)]
    
    def update_frame(self):
        if not self.is_running: return
        self.canvas.delete("anim_particle")
        
        color_string = getattr(self, 'particle_color', 'white')
        try:
            rgb_16bit = self.canvas.winfo_rgb(color_string)
            r, g, b = rgb_16bit[0] // 256, rgb_16bit[1] // 256, rgb_16bit[2] // 256
        except Exception:
            r, g, b = 255, 255, 255

        for p in self.particles:
            p.update()
            alpha = 0.7
            val_r, val_g, val_b = int(alpha * r), int(alpha * g), int(alpha * b)
            color = f'#{val_r:02x}{val_g:02x}{val_b:02x}'
            x1, y1, x2, y2 = p.x - p.size, p.y - p.size, p.x + p.size, p.y + p.size
            self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline="", tags="anim_particle")
        
        self.canvas.tag_lower("anim_particle")
        if self.label_window_id: self.canvas.tag_raise(self.label_window_id)
        self._after_id = self.canvas.after(self.DELAY, self.update_frame)

# =============================================================================
# Animação 10: Poças de Luz
# =============================================================================
class LightPool:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.x = random.randint(0, self.w)
        self.y = random.randint(0, self.h)
        # Reduzido para círculos menores: de 80-200 para 30-60
        self.max_size = random.uniform(30, 60)
        self.current_size = 0
        self.alpha = 0.0
        self.growing = True
        self.growth_speed = random.uniform(0.5, 1.5)  # Reduzido também para acompanhar tamanho menor
        self.fade_speed = random.uniform(0.02, 0.05)

    def update(self):
        if self.growing:
            self.current_size += self.growth_speed
            self.alpha += self.fade_speed
            if self.current_size >= self.max_size:
                self.growing = False
        else:
            self.current_size -= self.growth_speed * 0.5
            self.alpha -= self.fade_speed * 0.7
            if self.alpha <= 0 or self.current_size <= 0:
                self.x = random.randint(0, self.w)
                self.y = random.randint(0, self.h)
                self.current_size = 0
                self.alpha = 0.0
                self.growing = True
                # Reduzido para círculos menores: de 80-200 para 30-60
                self.max_size = random.uniform(30, 60)

class LightPoolsAnimation(BaseAnimation):
    NUM_PARTICLES, DELAY = 8, 40

    def _recreate_particles(self, width, height):
        self.particles = [LightPool(width, height) for _ in range(self.NUM_PARTICLES)]
    
    def update_frame(self):
        if not self.is_running: return
        self.canvas.delete("anim_particle")
        
        color_string = getattr(self, 'particle_color', 'white')
        try:
            rgb_16bit = self.canvas.winfo_rgb(color_string)
            r, g, b = rgb_16bit[0] // 256, rgb_16bit[1] // 256, rgb_16bit[2] // 256
        except Exception:
            r, g, b = 255, 255, 255

        for p in self.particles:
            p.update()
            if p.alpha > 0 and p.current_size > 0:
                # Garante que alpha esteja entre 0 e 1
                alpha = max(0.0, min(1.0, p.alpha))
                val_r = max(0, min(255, int(alpha * r)))
                val_g = max(0, min(255, int(alpha * g)))
                val_b = max(0, min(255, int(alpha * b)))
                color = f'#{val_r:02x}{val_g:02x}{val_b:02x}'
                x1, y1, x2, y2 = p.x - p.current_size, p.y - p.current_size, p.x + p.current_size, p.y + p.current_size
                self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline="", tags="anim_particle")
        
        self.canvas.tag_lower("anim_particle")
        if self.label_window_id: self.canvas.tag_raise(self.label_window_id)
        self._after_id = self.canvas.after(self.DELAY, self.update_frame)

# =============================================================================
# Animação 11: Partículas Pulsantes
# =============================================================================
class PulsingParticle:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.x = random.randint(0, self.w)
        self.y = random.randint(0, self.h)
        self.base_size = random.uniform(3, 8)
        self.current_size = self.base_size
        self.pulse_speed = random.uniform(0.05, 0.15)
        self.pulse_phase = random.uniform(0, 6.28)
        self.alpha = random.uniform(0.5, 1.0)

    def update(self):
        self.pulse_phase += self.pulse_speed
        pulse = 0.7 + 0.3 * math.sin(self.pulse_phase)
        self.current_size = self.base_size * pulse

class PulsingParticlesAnimation(BaseAnimation):
    NUM_PARTICLES, DELAY = 80, 30

    def _recreate_particles(self, width, height):
        self.particles = [PulsingParticle(width, height) for _ in range(self.NUM_PARTICLES)]
    
    def update_frame(self):
        if not self.is_running: return
        self.canvas.delete("anim_particle")
        
        color_string = getattr(self, 'particle_color', 'white')
        try:
            rgb_16bit = self.canvas.winfo_rgb(color_string)
            r, g, b = rgb_16bit[0] // 256, rgb_16bit[1] // 256, rgb_16bit[2] // 256
        except Exception:
            r, g, b = 255, 255, 255

        for p in self.particles:
            p.update()
            val_r, val_g, val_b = int(p.alpha * r), int(p.alpha * g), int(p.alpha * b)
            color = f'#{val_r:02x}{val_g:02x}{val_b:02x}'
            x1, y1, x2, y2 = p.x - p.current_size, p.y - p.current_size, p.x + p.current_size, p.y + p.current_size
            self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline="", tags="anim_particle")
        
        self.canvas.tag_lower("anim_particle")
        if self.label_window_id: self.canvas.tag_raise(self.label_window_id)
        self._after_id = self.canvas.after(self.DELAY, self.update_frame)