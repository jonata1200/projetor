import customtkinter as ctk
import tkinter as tk
from .animations import SnowAnimation, FloatingParticlesAnimation

class ProjectionWindow(ctk.CTkToplevel):
    FADE_STEPS = 10
    FADE_DELAY = 15

    def __init__(self, master, controller, target_monitor_geometry, config_manager, on_ready_callback=None):
        super().__init__(master)
        self.master = master
        self.controller = controller
        self.config_manager = config_manager
        self.on_ready_callback = on_ready_callback
        self.title("Projetor")
        
        self.is_fading, self._after_id_fade = False, None
        
        self.overrideredirect(True)
        self.geometry(f"{target_monitor_geometry['width']}x{target_monitor_geometry['height']}+{target_monitor_geometry['x']}+{target_monitor_geometry['y']}")
        
        # 1. Inicializa com um fundo preto padrão. O estilo real será aplicado depois.
        self.main_canvas = tk.Canvas(self, bg="black", highlightthickness=0)
        self.main_canvas.pack(fill="both", expand=True)
        
        # 2. O Label é criado com um estilo padrão, que será sobrescrito pelo apply_style.
        self.projection_label = ctk.CTkLabel(self.main_canvas, text="", font=ctk.CTkFont(size=60, weight="bold"), text_color="white", fg_color="black", justify=ctk.CENTER)
        self.label_window_id = self.main_canvas.create_window(0, 0, window=self.projection_label, anchor="center")
        
        # 3. A animação começa como nula.
        self.animation = None
        
        # Vinculando atalhos e eventos
        self.bind("<Right>", lambda e: self.controller.next_slide())
        self.bind("<Left>", lambda e: self.controller.prev_slide())
        self.bind("<c>", lambda e: self.controller.clear_projection_content())
        self.bind("<Escape>", self.close_window)
        self.main_canvas.bind("<Double-Button-1>", self.close_window)
        self.projection_label.bind("<Double-Button-1>", self.close_window)
        self.protocol("WM_DELETE_WINDOW", self.close_window)
        self.bind("<Configure>", self._on_resize)
        
        self.after(50, self._initialize_layout)
        self.lift()
        self.focus_force()

    def apply_style(self, style_config):
        """Aplica um novo perfil de estilo à janela de projeção."""
        # --- LÓGICA DE ANIMAÇÃO ---
        # Determina o nome da classe da nova animação
        new_anim_name_raw = style_config.get('animation_type', 'Nenhuma')
        new_anim_class_name = new_anim_name_raw.replace(" ", "") + "Animation"
        
        # Determina o nome da classe da animação atual (se houver)
        current_anim_class_name = self.animation.__class__.__name__ if self.animation else "NenhumaAnimation"

        # Só recria a animação se o TIPO mudou
        if new_anim_class_name != current_anim_class_name:
            if self.animation:
                self.animation.stop()

            animation_map = {"NeveAnimation": SnowAnimation, "PartículasFlutuantesAnimation": FloatingParticlesAnimation}
            
            if new_anim_name_raw in ["Neve", "Partículas Flutuantes"]:
                animation_class = animation_map[new_anim_class_name]
                self.animation = animation_class(self.main_canvas, self.label_window_id)
                self.animation.on_resize(self.main_canvas.winfo_width(), self.main_canvas.winfo_height())
                self.animation.start()
            else:
                self.animation = None
        
        # Atualiza a cor da animação (se ela existir)
        if self.animation:
            self.animation.particle_color = style_config.get('animation_color')

        # --- LÓGICA DE ESTILO VISUAL ---
        bg_color = style_config.get('bg_color')
        self.main_canvas.configure(bg=bg_color)
        self.projection_label.configure(
            font=ctk.CTkFont(size=int(style_config.get('font_size')), weight="bold"),
            text_color=style_config.get('font_color'),
            fg_color=bg_color
        )
        
    def _initialize_layout(self):
        if self.winfo_width() <= 1: self.after(50, self._initialize_layout); return
        self._on_resize()
        # Não inicia mais a animação aqui, pois o apply_style cuidará disso.
        if self.on_ready_callback: self.on_ready_callback()
        
    def close_window(self, event=None):
        if self.animation: self.animation.stop()
        if self.controller: self.controller.on_projection_window_closed()
        if self.winfo_exists(): self.destroy()

    # (O resto dos métodos: update_content, fades, on_resize, etc., permanecem os mesmos)
    def update_content(self, text):
        if self.is_fading: self.after_cancel(self._after_id_fade)
        self._fade_out(lambda: self._update_text_and_fade_in(text))

    def _update_text_and_fade_in(self, text):
        if self.projection_label.winfo_exists(): self.projection_label.configure(text=text)
        self._fade_in()
    
    def _fade_out(self, on_finish_callback=None):
        self.is_fading = True
        self._animate_fade(start=1.0, end=0.0, step=-1.0/self.FADE_STEPS, on_finish=on_finish_callback)

    def _fade_in(self):
        self.is_fading = True
        self._animate_fade(start=0.0, end=1.0, step=1.0/self.FADE_STEPS)

    def _animate_fade(self, start, end, step, on_finish=None):
        current_alpha = self.attributes("-alpha")
        next_alpha = current_alpha + step
        is_finished = (step > 0 and next_alpha >= end) or (step < 0 and next_alpha <= end)
        if is_finished: next_alpha = end
        self.attributes("-alpha", next_alpha)
        if not is_finished:
            self._after_id_fade = self.after(self.FADE_DELAY, lambda: self._animate_fade(start, end, step, on_finish))
        else:
            self.is_fading = False
            if on_finish: on_finish()

    def _on_resize(self, event=None):
        if not self.winfo_exists() or self.winfo_width() <= 1: return
        width = self.main_canvas.winfo_width(); height = self.main_canvas.winfo_height()
        self.projection_label.configure(wraplength=width * 0.9)
        self.main_canvas.coords(self.label_window_id, width / 2, height / 2)
        if self.animation:
            self.animation.on_resize(width, height)
    
    def clear_content(self): self.update_content("")