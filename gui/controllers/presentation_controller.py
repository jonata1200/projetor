from tkinter import messagebox
from screeninfo import get_monitors
from gui.projection_window import ProjectionWindow

class PresentationController:
    def __init__(self, master, ui_elements, config_manager):
        self.master = master
        self.ui = ui_elements
        self.config_manager = config_manager
        self.projection_window = None

        self.slides = []
        self.current_index = -1
        self.content_type = None
        self.content_id = None

        self._setup_callbacks()

    def _setup_callbacks(self):
        self.ui["btn_prev"].configure(command=self.prev_slide)
        self.ui["btn_next"].configure(command=self.next_slide)
        self.ui["btn_projection"].configure(command=self.handle_projection_button)
        self.ui["btn_clear"].configure(command=self.clear_projection_content)

    def load_content(self, content_type, slides, content_id=None, start_index=0):
        """
        Carrega novo conteúdo e aplica o estilo correspondente.
        """
        # Verifica se o TIPO de conteúdo mudou para decidir se um novo estilo deve ser aplicado.
        apply_new_style = (self.content_type != content_type)
        self.content_type = content_type
        
        self.slides = slides if slides else []
        self.content_id = content_id
        
        if self.slides:
            self.current_index = start_index if 0 <= start_index < len(self.slides) else 0
            
            # Se a janela de projeção estiver aberta e o tipo de conteúdo mudou, aplica o novo estilo.
            if self.projection_window and self.projection_window.winfo_exists() and apply_new_style:
                self._apply_style_for_current_content()
            
            self.update_slide_view()
            # Atualiza a grade de miniaturas na janela principal
            if hasattr(self.master, 'build_all_slides_grid'):
                self.master.build_all_slides_grid(self.slides, self.current_index)
        else:
            self.current_index = -1
            self.clear_slide_view()
            if hasattr(self.master, 'build_all_slides_grid'):
                self.master.build_all_slides_grid([], -1)
        
        self.update_controls_state()

    def _apply_style_for_current_content(self):
        """Método auxiliar para pegar a configuração e aplicá-la na janela de projeção."""
        if not self.projection_window or not self.projection_window.winfo_exists():
            return
            
        content_map = {"music": "Projection_Music", "bible": "Projection_Bible", "text": "Projection_Text"}
        # Se o tipo de conteúdo não for conhecido, usa o de música como padrão.
        section_name = content_map.get(self.content_type, "Projection_Music")

        style_config = {
            'font_size': self.config_manager.get_int_setting(section_name, 'font_size', 60),
            'font_color': self.config_manager.get_setting(section_name, 'font_color', 'white'),
            'bg_color': self.config_manager.get_setting(section_name, 'bg_color', 'black'),
            'animation_type': self.config_manager.get_setting(section_name, 'animation_type', 'Nenhuma'),
            'animation_color': self.config_manager.get_setting(section_name, 'animation_color', 'white')
        }
        self.projection_window.apply_style(style_config)

    def update_slide_view(self):
        if 0 <= self.current_index < len(self.slides):
            slide_text = self.slides[self.current_index]
            self.ui["preview_label"].configure(text=slide_text)
            self.ui["indicator_label"].configure(text=f"{self.current_index + 1} / {len(self.slides)}")
            
            if self.projection_window and self.projection_window.winfo_exists():
                self.projection_window.update_content(slide_text)
        else:
            self.clear_slide_view()

    def next_slide(self):
        if self.slides and self.current_index < len(self.slides) - 1:
            old_index = self.current_index
            self.current_index += 1
            self.update_slide_view()
            if hasattr(self.master, 'update_miniature_highlight'):
                self.master.update_miniature_highlight(old_index, self.current_index)

    def prev_slide(self):
        if self.slides and self.current_index > 0:
            old_index = self.current_index
            self.current_index -= 1
            self.update_slide_view()
            if hasattr(self.master, 'update_miniature_highlight'):
                self.master.update_miniature_highlight(old_index, self.current_index)

    def go_to_slide(self, index):
        if self.slides and 0 <= index < len(self.slides):
            old_index = self.current_index
            self.current_index = index
            self.update_slide_view()
            if hasattr(self.master, 'update_miniature_highlight'):
                self.master.update_miniature_highlight(old_index, self.current_index)
    
    def clear_slide_view(self):
        self.ui["preview_label"].configure(text="")
        self.ui["indicator_label"].configure(text="- / -")
        if self.projection_window and self.projection_window.winfo_exists():
            self.projection_window.clear_content()

    def update_controls_state(self):
        has_slides = bool(self.slides)
        self.ui["btn_prev"].configure(state="normal" if has_slides else "disabled")
        self.ui["btn_next"].configure(state="normal" if has_slides else "disabled")

    def handle_projection_button(self):
        is_window_open = self.projection_window and self.projection_window.winfo_exists()
        if is_window_open:
            self.close_projection_window()
        else:
            self.open_projection_window()
    
    def open_projection_window(self):
        if self.projection_window and self.projection_window.winfo_exists():
            self.projection_window.lift()
            return

        try:
            monitors = get_monitors()
            target_monitor = monitors[1] if len(monitors) > 1 else monitors[0]
        except IndexError:
            messagebox.showerror("Erro", "Nenhum monitor detectado.", parent=self.master)
            return

        geom = {"x": target_monitor.x, "y": target_monitor.y, "width": target_monitor.width, "height": target_monitor.height}
        
        self.projection_window = ProjectionWindow(
            master=self.master, 
            controller=self,
            target_monitor_geometry=geom,
            config_manager=self.config_manager,
            on_ready_callback=self._on_projection_window_ready
        )

    def _on_projection_window_ready(self):
        """
        Callback chamado pela ProjectionWindow quando ela está 100% inicializada.
        Aqui, aplicamos o estilo do conteúdo atual ou um estilo padrão.
        """
        self.update_projection_buttons_state()
        
        # --- SOLUÇÃO PARA A "TELA PRETA" ---
        self._apply_style_for_current_content()
        # Após aplicar o estilo, atualiza o conteúdo do slide atual, se houver
        self.update_slide_view() 
    
    def close_projection_window(self):
        if self.projection_window and self.projection_window.winfo_exists():
            self.projection_window.destroy()
        
        # --- SOLUÇÃO PARA O BOTÃO "TRAVADO" ---
        # Limpa a referência e atualiza o estado do botão
        self.on_projection_window_closed()

    def on_projection_window_closed(self):
        """
        Callback para ser chamado pela ProjectionWindow ou pelo método close.
        Garante que o estado seja limpo e a UI atualizada.
        """
        self.projection_window = None
        self.update_projection_buttons_state()

    def update_projection_buttons_state(self):
        is_open = self.projection_window and self.projection_window.winfo_exists()
        text = "Fechar Projeção" if is_open else "Abrir Projeção"
        self.ui["btn_projection"].configure(text=text)

    def clear_projection_content(self):
        self.slides = []
        self.current_index = -1
        self.content_type = None
        self.content_id = None
        self.clear_slide_view() 
        self.update_controls_state() 
        if self.projection_window and self.projection_window.winfo_exists():
            self.projection_window.clear_content()
        if hasattr(self.master, 'build_all_slides_grid'):
            self.master.build_all_slides_grid([], -1)
        
    def on_closing(self):
        self.close_projection_window()