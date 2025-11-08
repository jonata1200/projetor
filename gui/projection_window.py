import customtkinter as ctk
import tkinter as tk
# Importa nossas novas classes de animação
from .animations import SnowAnimation, FloatingParticlesAnimation, SparklingStarsAnimation, ConnectingLinesAnimation

class ProjectionWindow(ctk.CTkToplevel):
    FADE_STEPS = 10
    FADE_DELAY = 15

    def __init__(self, master, controller, target_monitor_geometry, config_manager, on_ready_callback=None):
        super().__init__(master)
        # ... (código de setup inicial)
        self.master = master
        self.controller = controller
        self.config_manager = config_manager
        self.on_ready_callback = on_ready_callback
        self.title("Projetor")

        # --- Carregando configurações ---
        try:
            font_size = self.config_manager.get_int_setting('Projection', 'font_size', 60)
            font_color = self.config_manager.get_setting('Projection', 'font_color', 'white')
            bg_color = self.config_manager.get_setting('Projection', 'bg_color', 'black')
            animation_type = self.config_manager.get_setting('Projection', 'animation_type', 'Neve')
            print(f"--- PASSO 1: Animação lida da configuração: '{animation_type}' ---") # <-- ADICIONE AQUI
        except Exception:
            font_size, font_color, bg_color, animation_type = 60, 'white', 'black', 'Neve'

        self.is_fading, self._after_id_fade = False, None
        
        self.overrideredirect(True)
        self.geometry(f"{target_monitor_geometry['width']}x{target_monitor_geometry['height']}+{target_monitor_geometry['x']}+{target_monitor_geometry['y']}")
        
        self.main_canvas = tk.Canvas(self, bg=bg_color, highlightthickness=0)
        self.main_canvas.pack(fill="both", expand=True)
        
        self.projection_label = ctk.CTkLabel(self.main_canvas, text="", font=ctk.CTkFont(size=font_size, weight="bold"), text_color=font_color, fg_color=bg_color, justify=ctk.CENTER)
        
        # --- MUDANÇA CRÍTICA ---
        # Cria a janela do label ANTES de criar a animação.
        # Nós ainda não sabemos a posição correta, então usamos (0,0) como placeholder.
        self.label_window_id = self.main_canvas.create_window(0, 0, window=self.projection_label, anchor="center")
        
        self.animation = None
        animation_map = {
            "Neve": SnowAnimation, "Partículas Flutuantes": FloatingParticlesAnimation,
            "Estrelas Cintilantes": SparklingStarsAnimation, "Linhas de Conexão": ConnectingLinesAnimation
        }
        if animation_type in animation_map:
            animation_class = animation_map[animation_type]
            # Agora passamos o ID do label para a classe de animação.
            self.animation = animation_class(self.main_canvas, self.label_window_id)
        
        print(f"--- PASSO 2: Objeto de animação criado: {self.animation} ---")

        # --- Vinculando atalhos e eventos ---
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

    def _initialize_layout(self):
        if self.winfo_width() <= 1: self.after(50, self._initialize_layout); return
        self._on_resize()
        self.start_animation() # Inicia a animação escolhida
        if self.on_ready_callback: self.on_ready_callback()
        
    def close_window(self, event=None):
        self.stop_animation()
        if self.controller: self.controller.on_projection_window_closed()
        if self.winfo_exists(): self.destroy()

    # --- NOVOS MÉTODOS GENÉRICOS DE ANIMAÇÃO ---
    def start_animation(self):
        if self.animation:
            self.animation.start()

    def stop_animation(self):
        if self.animation:
            self.animation.stop()

    # --- O RESTO DO CÓDIGO PERMANECE O MESMO ---
    # (update_content, _fade_out, _fade_in, _on_resize, etc.)
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
        if self.label_window_id is None:
            # Adiciona a tag="text_window" ao criar a janela do label
            self.label_window_id = self.main_canvas.create_window(
                width / 2, height / 2, window=self.projection_label, anchor="center", tags="text_window"
            )
        else:
            self.main_canvas.coords(self.label_window_id, width / 2, height / 2)
    
    def clear_content(self): self.update_content("")