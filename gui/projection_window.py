import customtkinter as ctk
import tkinter as tk
from .animations import (
    AuroraAnimation, FireAnimation, RainAnimation, SpiralAnimation,
    BlinkingStarsAnimation, SnowAnimation, FloatingParticlesAnimation,
    PulsingParticlesAnimation, PetalsAnimation, LightPoolsAnimation
)

# Cores padrão para cada animação
ANIMATION_DEFAULT_COLORS = {
    "Aurora": "#7B68EE",              # Roxo suave
    "Chamas": "#FF6B35",              # Laranja/vermelho
    "Chuva": "#87CEEB",               # Azul claro
    "Espiral": "#FFD700",             # Dourado
    "Estrelas Piscando": "#FFFAF0",   # Branco creme
    "Neve": "#FFFFFF",                # Branco puro
    "Partículas Flutuantes": "#FF69B4", # Rosa vibrante
    "Partículas Pulsantes": "#32CD32",  # Verde lime
    "Pétalas": "#FFB6C1",             # Rosa claro
    "Poças de Luz": "#4169E1"         # Azul royal
}

# Função auxiliar para obter a cor padrão de uma animação
def get_animation_default_color(animation_type: str) -> str:
    """Retorna a cor padrão para um tipo de animação."""
    return ANIMATION_DEFAULT_COLORS.get(animation_type, '#FFFFFF')

class ProjectionWindow(ctk.CTkToplevel):
    FADE_STEPS = 5  # Fade rápido mas suave
    FADE_DELAY = 8  # Delay curto para transição rápida

    def __init__(self, master, controller, target_monitor_geometry, config_manager, on_ready_callback=None):
        super().__init__(master)
        self.master = master
        self.controller = controller
        self.config_manager = config_manager
        self.on_ready_callback = on_ready_callback
        self.title("Projetor")
        
        self.is_fading, self._after_id_fade = False, None
        
        self.font_color = 'white'
        self.bg_color = 'black'
        self.text_bg_enabled = True
        self.text_bg_opacity = 0.75

        self.overrideredirect(True)
        self.geometry(f"{target_monitor_geometry['width']}x{target_monitor_geometry['height']}+{target_monitor_geometry['x']}+{target_monitor_geometry['y']}")
        
        # --- ALTERAÇÃO PRINCIPAL AQUI ---
        # Esta linha instrui o sistema operacional a manter esta janela sempre na frente.
        self.attributes("-topmost", True)
        
        self.main_canvas = tk.Canvas(self, bg=self.bg_color, highlightthickness=0)
        self.main_canvas.pack(fill="both", expand=True)
        
        # Usa canvas.create_text para transparência verdadeira (sem preenchimento preto)
        # O texto é desenhado diretamente no canvas, sem widget intermediário
        # Retângulo semi-transparente atrás do texto para melhor legibilidade (sem contorno)
        self.text_bg_id = self.main_canvas.create_rectangle(
            0, 0, 0, 0,
            fill="black",
            outline="",
            stipple="gray75",  # 75% opaco / 25% transparente
            tags="projection_text_bg"
        )
        
        # Texto principal (sem contorno)
        self.text_id = self.main_canvas.create_text(
            0, 0,
            text="",
            fill=self.font_color,
            font=("Arial", 60, "bold"),
            anchor="center",
            justify="center",
            tags="projection_text"
        )
        # Mantém label_window_id como None para compatibilidade com animações
        self.label_window_id = None
        
        self.animation = None
        
        self.bind("<Right>", lambda e: self.controller.next_slide())
        self.bind("<Left>", lambda e: self.controller.prev_slide())
        self.bind("<c>", lambda e: self.controller.clear_projection_content())
        self.bind("<Escape>", self.close_window)
        self.main_canvas.bind("<Double-Button-1>", self.close_window)
        # Permite fechar clicando no texto também
        self.main_canvas.tag_bind("projection_text", "<Double-Button-1>", self.close_window)
        self.protocol("WM_DELETE_WINDOW", self.close_window)
        self.bind("<Configure>", self._on_resize)
        
        self.after(50, self._initialize_layout)
        self.lift()
        self.focus_force()

    # ... (O restante do arquivo permanece exatamente o mesmo, não precisa ser alterado) ...

    def apply_style(self, style_config):
        animation_map = {
            "Aurora": AuroraAnimation,
            "Chamas": FireAnimation,
            "Chuva": RainAnimation,
            "Espiral": SpiralAnimation,
            "Estrelas Piscando": BlinkingStarsAnimation,
            "Neve": SnowAnimation,
            "Partículas Flutuantes": FloatingParticlesAnimation,
            "Partículas Pulsantes": PulsingParticlesAnimation,
            "Pétalas": PetalsAnimation,
            "Poças de Luz": LightPoolsAnimation
        }
        new_anim_name = style_config.get('animation_type', 'Nenhuma')
        new_anim_class = animation_map.get(new_anim_name)
        current_anim_class = self.animation.__class__ if self.animation else None

        if new_anim_class is not current_anim_class:
            if self.animation: self.animation.stop()

            if new_anim_class:
                # Passa o text_id em vez de label_window_id para as animações
                self.animation = new_anim_class(self.main_canvas, self.text_id)
                if self.main_canvas.winfo_width() > 1:
                    self.animation.on_resize(self.main_canvas.winfo_width(), self.main_canvas.winfo_height())
                
                if self.winfo_exists() and self.winfo_width() > 1:
                    self.start_animation()
            else:
                self.animation = None
        
        if self.animation:
            # Usa a cor padrão da animação
            self.animation.particle_color = ANIMATION_DEFAULT_COLORS.get(new_anim_name, '#FFFFFF')

        self.bg_color = style_config.get('bg_color')
        self.font_color = style_config.get('font_color')
        # Configuração do fundo semi-transparente
        self.text_bg_enabled = str(style_config.get('text_bg_enabled', 'true')).lower() in ('1','true','yes','on')
        try:
            self.text_bg_opacity = float(style_config.get('text_bg_opacity', 0.75))
        except (TypeError, ValueError):
            self.text_bg_opacity = 0.75
        self.text_bg_opacity = min(1.0, max(0.0, self.text_bg_opacity))
        self.main_canvas.configure(bg=self.bg_color)
        font_size = int(style_config.get('font_size'))
        # Atualiza o texto do canvas diretamente
        font_tuple = ("Arial", font_size, "bold")
        self.main_canvas.itemconfig(
            self.text_id,
            fill=self.font_color,
            font=font_tuple
        )
        # Atualiza o fundo do texto
        self._update_text_background()
        # Garante que fundo e texto fiquem acima das animações
        self.main_canvas.tag_raise("projection_text_bg")
        self.main_canvas.tag_raise("projection_text")

    def _initialize_layout(self):
        if self.winfo_width() <= 1: self.after(50, self._initialize_layout); return
        self._on_resize()
        
        self.start_animation() 
        
        if self.on_ready_callback: self.on_ready_callback()
        
    def close_window(self, event=None):
        self.stop_animation() 
        if self.controller: self.controller.on_projection_window_closed()
        if self.winfo_exists(): self.destroy()

    def start_animation(self):
        """Inicia a animação de fundo, se houver uma."""
        if self.animation and not self.animation.is_running:
            self.animation.start()

    def stop_animation(self):
        """Para a animação de fundo, se houver uma."""
        if self.animation and self.animation.is_running:
            self.animation.stop()

    def update_content(self, text):
        # Fade rápido para transição suave
        if self.is_fading and self._after_id_fade: 
            self.after_cancel(self._after_id_fade)
        self._fade_out(lambda: self._update_text_and_fade_in(text))

    def _update_text_and_fade_in(self, text):
        # Atualiza o texto diretamente no canvas
        self.main_canvas.itemconfig(self.text_id, text=text)
        # Atualiza o fundo do texto baseado no tamanho do texto
        self._update_text_background()
        self._fade_in()
    
    def _apply_text_background_style(self):
        """Aplica estado e opacidade do fundo atrás do texto."""
        if not self.text_bg_enabled or self.text_bg_opacity <= 0.01:
            self.main_canvas.itemconfig(self.text_bg_id, state="hidden")
            return
        # Mapeia opacidade para padrões de stipple
        if self.text_bg_opacity >= 0.85:
            stipple = "gray75"
        elif self.text_bg_opacity >= 0.6:
            stipple = "gray50"
        elif self.text_bg_opacity >= 0.35:
            stipple = "gray25"
        else:
            stipple = "gray12"
        self.main_canvas.itemconfig(self.text_bg_id, stipple=stipple, state="normal")

    def _update_text_background(self):
        """Atualiza o retângulo de fundo do texto baseado na bounding box do texto."""
        if not self.text_bg_enabled or self.text_bg_opacity <= 0.01:
            self.main_canvas.itemconfig(self.text_bg_id, state="hidden")
            return
        try:
            # Obtém a bounding box do texto
            bbox = self.main_canvas.bbox(self.text_id)
            if bbox:
                # Adiciona padding ao redor do texto
                padding = 20
                x1 = bbox[0] - padding
                y1 = bbox[1] - padding
                x2 = bbox[2] + padding
                y2 = bbox[3] + padding
                self.main_canvas.coords(self.text_bg_id, x1, y1, x2, y2)
                self._apply_text_background_style()
            else:
                # Mesmo sem bbox, aplica estado (útil para limpar/ocultar)
                self._apply_text_background_style()
        except:
            pass  # Se não conseguir obter bbox, ignora
    
    def _fade_out(self, on_finish_callback=None):
        self.is_fading = True
        self._animate_text_color(start_color=self.font_color, end_color=self.bg_color, on_finish=on_finish_callback)

    def _fade_in(self):
        self.is_fading = True
        self._animate_text_color(start_color=self.bg_color, end_color=self.font_color, on_finish=lambda: setattr(self, 'is_fading', False))
    
    def _animate_text_color(self, start_color, end_color, on_finish=None, step=0):
        if step > self.FADE_STEPS:
            if on_finish:
                on_finish()
            return

        try:
            start_r, start_g, start_b = [c // 256 for c in self.winfo_rgb(start_color)]
            end_r, end_g, end_b = [c // 256 for c in self.winfo_rgb(end_color)]
        except tk.TclError:
            start_r, start_g, start_b = (255, 255, 255); end_r, end_g, end_b = (0, 0, 0)
            
        progress = step / self.FADE_STEPS
        new_r = int(start_r + (end_r - start_r) * progress)
        new_g = int(start_g + (end_g - start_g) * progress)
        new_b = int(start_b + (end_b - start_b) * progress)
        
        new_color = f"#{new_r:02x}{new_g:02x}{new_b:02x}"
        
        # Atualiza o texto principal durante o fade
        self.main_canvas.itemconfig(self.text_id, fill=new_color)
        
        self._after_id_fade = self.after(
            self.FADE_DELAY, 
            lambda: self._animate_text_color(start_color, end_color, on_finish, step + 1)
        )


    def _on_resize(self, event=None):
        if not self.winfo_exists() or self.winfo_width() <= 1: return
        width, height = self.main_canvas.winfo_width(), self.main_canvas.winfo_height()
        # Reposiciona o texto no centro e ajusta wraplength
        center_x, center_y = width / 2, height / 2
        self.main_canvas.coords(self.text_id, center_x, center_y)
        self.main_canvas.itemconfig(self.text_id, width=int(width * 0.9))
        # Atualiza o fundo do texto
        self._update_text_background()
        # Garante que o fundo fique atrás do texto principal, mas ambos acima das animações
        self.main_canvas.tag_lower("projection_text_bg", "projection_text")
        self.main_canvas.tag_raise("projection_text_bg")
        self.main_canvas.tag_raise("projection_text")
        if self.animation:
            self.animation.on_resize(width, height)
    
    def clear_content(self):
        self.update_content("")