import customtkinter as ctk
import tkinter as tk
from .animations import SnowAnimation, FloatingParticlesAnimation

class ProjectionWindow(ctk.CTkToplevel):
    FADE_STEPS = 15  # Aumentei os passos para uma transição mais suave
    FADE_DELAY = 10  # Diminuí o delay para uma transição mais rápida

    def __init__(self, master, controller, target_monitor_geometry, config_manager, on_ready_callback=None):
        super().__init__(master)
        self.master = master
        self.controller = controller
        self.config_manager = config_manager
        self.on_ready_callback = on_ready_callback
        self.title("Projetor")
        
        self.is_fading, self._after_id_fade = False, None
        
        # Armazenaremos as cores do estilo atual aqui
        self.font_color = 'white'
        self.bg_color = 'black'

        self.overrideredirect(True)
        self.geometry(f"{target_monitor_geometry['width']}x{target_monitor_geometry['height']}+{target_monitor_geometry['x']}+{target_monitor_geometry['y']}")
        
        self.main_canvas = tk.Canvas(self, bg=self.bg_color, highlightthickness=0)
        self.main_canvas.pack(fill="both", expand=True)
        
        self.projection_label = ctk.CTkLabel(self.main_canvas, text="", font=ctk.CTkFont(size=60, weight="bold"), text_color=self.font_color, fg_color=self.bg_color, justify=ctk.CENTER)
        self.label_window_id = self.main_canvas.create_window(0, 0, window=self.projection_label, anchor="center")
        
        self.animation = None
        
        # Vinculando atalhos e eventos...
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
        print(f"--- DEBUG 2: 'apply_style' foi chamado com a configuração: {style_config.get('animation_type')} ---")
        
        animation_map = {"Neve": SnowAnimation, "Partículas Flutuantes": FloatingParticlesAnimation}
        new_anim_name = style_config.get('animation_type', 'Nenhuma')
        new_anim_class = animation_map.get(new_anim_name)
        current_anim_class = self.animation.__class__ if self.animation else None

        # Compara as classes. Só age se a CLASSE for diferente.
        if new_anim_class is not current_anim_class:
            if self.animation: self.animation.stop()

            if new_anim_class:
                self.animation = new_anim_class(self.main_canvas, self.label_window_id)
                if self.main_canvas.winfo_width() > 1:
                    self.animation.on_resize(self.main_canvas.winfo_width(), self.main_canvas.winfo_height())
                
                # --- CORREÇÃO IMPORTANTE ---
                # O start_animation não deve ser chamado aqui, mas sim pelo _initialize_layout
                # ou quando a janela já está visível e pronta.
                # Apenas iniciamos se a janela já estiver pronta.
                if self.winfo_exists() and self.winfo_width() > 1:
                    self.start_animation()
            else:
                self.animation = None
        
        if self.animation:
            self.animation.particle_color = style_config.get('animation_color')

        self.bg_color = style_config.get('bg_color')
        self.font_color = style_config.get('font_color')
        self.main_canvas.configure(bg=self.bg_color)
        self.projection_label.configure(
            font=ctk.CTkFont(size=int(style_config.get('font_size')), weight="bold"),
            text_color=self.font_color,
            fg_color=self.bg_color
        )

    def _initialize_layout(self):
        if self.winfo_width() <= 1: self.after(50, self._initialize_layout); return
        self._on_resize()
        
        # A chamada a apply_style foi movida para o PresentationController,
        # mas a animação precisa ser iniciada aqui se já foi criada.
        self.start_animation() 
        
        if self.on_ready_callback: self.on_ready_callback()
        
    def close_window(self, event=None):
        # O stop_animation é chamado aqui, então precisamos do método
        self.stop_animation() 
        if self.controller: self.controller.on_projection_window_closed()
        if self.winfo_exists(): self.destroy()

    # --- INÍCIO DOS MÉTODOS FALTANTES ---
    def start_animation(self):
        """Inicia a animação de fundo, se houver uma."""
        if self.animation:
            print(f"--- DEBUG 3: 'start_animation' está iniciando o objeto: {self.animation.__class__.__name__} ---")
            self.animation.start()

    def stop_animation(self):
        """Para a animação de fundo, se houver uma."""
        if self.animation:
            self.animation.stop()
    # --- FIM DOS MÉTODOS FALTANTES ---

    def update_content(self, text):
        if self.is_fading: self.after_cancel(self._after_id_fade)
        self._fade_out(lambda: self._update_text_and_fade_in(text))

    def _update_text_and_fade_in(self, text):
        if self.projection_label.winfo_exists():
            self.projection_label.configure(text=text)
        self._fade_in()
    
    def _fade_out(self, on_finish_callback=None):
        self.is_fading = True
        self._animate_text_color(start_color=self.font_color, end_color=self.bg_color, on_finish=on_finish_callback)

    def _fade_in(self):
        self.is_fading = True
        self._animate_text_color(start_color=self.bg_color, end_color=self.font_color)

    def _animate_text_color(self, start_color, end_color, on_finish=None, step=0):
        """Motor da animação que interpola a cor do texto."""
        if step > self.FADE_STEPS:
            self.is_fading = False
            if on_finish:
                on_finish()
            return

        try:
            # Converte as cores hex/nome para componentes RGB (0-255)
            start_r, start_g, start_b = [c // 256 for c in self.winfo_rgb(start_color)]
            end_r, end_g, end_b = [c // 256 for c in self.winfo_rgb(end_color)]
        except tk.TclError: # Fallback se a cor for inválida
            start_r, start_g, start_b = (255, 255, 255)
            end_r, end_g, end_b = (0, 0, 0)
            
        # Calcula a cor intermediária
        progress = step / self.FADE_STEPS
        new_r = int(start_r + (end_r - start_r) * progress)
        new_g = int(start_g + (end_g - start_g) * progress)
        new_b = int(start_b + (end_b - start_b) * progress)
        
        new_color = f"#{new_r:02x}{new_g:02x}{new_b:02x}"
        
        self.projection_label.configure(text_color=new_color)
        
        self._after_id_fade = self.after(
            self.FADE_DELAY, 
            lambda: self._animate_text_color(start_color, end_color, on_finish, step + 1)
        )

    def _on_resize(self, event=None):
        if not self.winfo_exists() or self.winfo_width() <= 1: return
        width = self.main_canvas.winfo_width(); height = self.main_canvas.winfo_height()
        self.projection_label.configure(wraplength=width * 0.9)
        self.main_canvas.coords(self.label_window_id, width / 2, height / 2)
        if self.animation:
            self.animation.on_resize(width, height)
    
    def clear_content(self): self.update_content("")