import customtkinter as ctk
import tkinter as tk
import random

class SnowFlake:
    def __init__(self, canvas_width, canvas_height):
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.x = random.randint(0, canvas_width)
        self.y = random.randint(-canvas_height, 0)
        self.size = random.randint(2, 5)
        self.speed = random.uniform(0.5, 2.0)
        self.drift = random.uniform(-0.3, 0.3)

    def move(self):
        self.y += self.speed
        self.x += self.drift
        if self.y > self.canvas_height or self.x < 0 or self.x > self.canvas_width:
            self.y = random.randint(-50, -10)
            self.x = random.randint(0, self.canvas_width)

class ProjectionWindow(ctk.CTkToplevel):
    NUM_SNOWFLAKES = 150
    ANIMATION_DELAY_MS = 30

    def __init__(self, master, controller, target_monitor_geometry, config_manager, on_ready_callback=None):
        super().__init__(master)
        self.master_app = master
        self.controller = controller
        self.config_manager = config_manager # <-- Recebe o config_manager
        self.on_ready_callback = on_ready_callback
        self.title("Projetor IA")

        # --- Lendo as configurações de aparência ---
        try:
            font_size = self.config_manager.get_int_setting('Projection', 'font_size', 60)
            font_color = self.config_manager.get_setting('Projection', 'font_color', 'white')
            bg_color = self.config_manager.get_setting('Projection', 'bg_color', 'black')
        except Exception: # Fallback em caso de erro no arquivo de config
            font_size = 60
            font_color = 'white'
            bg_color = 'black'


        self.overrideredirect(True)
        self.geometry(f"{target_monitor_geometry['width']}x{target_monitor_geometry['height']}+{target_monitor_geometry['x']}+{target_monitor_geometry['y']}")

        # --- Aplicando as configurações de aparência ---
        self.main_canvas = tk.Canvas(self, bg=bg_color, highlightthickness=0)
        self.main_canvas.pack(fill="both", expand=True)

        self.projection_label = ctk.CTkLabel(
            self.main_canvas, text="", 
            font=ctk.CTkFont(size=font_size, weight="bold"),
            text_color=font_color,
            fg_color=bg_color, # Importante para o label não ter uma cor de fundo diferente
            justify=ctk.CENTER
        )
        self.label_window_id = None

        self.snowflakes = []
        self.animation_running = False
        self._after_id_snow = None

        self.bind("<Configure>", self._on_resize)
        self.bind("<Escape>", self.close_window)
        self.main_canvas.bind("<Double-Button-1>", self.close_window)
        self.projection_label.bind("<Double-Button-1>", self.close_window)

        self.protocol("WM_DELETE_WINDOW", self.close_window)

        self.after(50, self._initialize_layout)
        self.lift()
        self.focus_force()

    def close_window(self, event=None):
        """Notifica o controlador e depois destrói a si mesma."""
            
        if self.controller:
            self.controller.on_projection_window_closed()

        self.stop_snow_animation()
        
        if self.winfo_exists():
            self.destroy()

    def _initialize_layout(self):
        if self.winfo_width() <= 1:
            self.after(50, self._initialize_layout)
            return
        
        self._on_resize()
        self._init_snowflakes()
        self.start_snow_animation()

        if self.on_ready_callback:
            self.on_ready_callback()

    def update_content(self, text):
        if self.projection_label.winfo_exists():
            self.projection_label.configure(text=text)

    def _on_resize(self, event=None):
        if not self.winfo_exists() or self.winfo_width() <= 1: return
        
        width = self.main_canvas.winfo_width()
        height = self.main_canvas.winfo_height()

        self.projection_label.configure(wraplength=width * 0.9)

        if self.label_window_id is None:
            self.label_window_id = self.main_canvas.create_window(width / 2, height / 2, window=self.projection_label, anchor="center")
        else:
            self.main_canvas.coords(self.label_window_id, width / 2, height / 2)
        
        for flake in self.snowflakes:
            flake.canvas_width = width
            flake.canvas_height = height

    def is_content_cleared(self):
        """Retorna True se o label de projeção estiver vazio."""
        if self.projection_label.winfo_exists():
            return self.projection_label.cget("text") == ""
        return True

    def clear_content(self):
        self.update_content("")

    def _init_snowflakes(self):
        self.snowflakes.clear()
        if self.main_canvas.winfo_width() > 1:
            for _ in range(self.NUM_SNOWFLAKES):
                self.snowflakes.append(SnowFlake(self.main_canvas.winfo_width(), self.main_canvas.winfo_height()))

    def _draw_snowflakes(self):
        self.main_canvas.delete("snow")
        for flake in self.snowflakes:
            x1, y1 = flake.x - flake.size, flake.y - flake.size
            x2, y2 = flake.x + flake.size, flake.y + flake.size
            self.main_canvas.create_oval(x1, y1, x2, y2, fill="white", outline="", tags="snow")
        
        self.main_canvas.tag_raise(self.label_window_id, "snow")

    def _update_snowflakes(self):
        if not self.animation_running or not self.winfo_exists(): return
        for flake in self.snowflakes: flake.move()
        self._draw_snowflakes()
        self._after_id_snow = self.after(self.ANIMATION_DELAY_MS, self._update_snowflakes)

    def start_snow_animation(self):
        if not self.animation_running and self.snowflakes and self.winfo_exists():
            self.animation_running = True
            self._update_snowflakes()

    def stop_snow_animation(self):
        self.animation_running = False
        if self._after_id_snow:
            self.after_cancel(self._after_id_snow)