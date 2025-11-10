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
        self.all_slides_window = None

        self._setup_callbacks()

    def _setup_callbacks(self):
        self.ui["btn_prev"].configure(command=self.prev_slide)
        self.ui["btn_next"].configure(command=self.next_slide)
        self.ui["btn_projection"].configure(command=self.handle_projection_button)
        self.ui["btn_clear"].configure(command=self.clear_projection_content)

    def show_all_slides_view(self):
        """Abre a janela com a visualização de todos os slides."""
        if not self.slides:
            return
        
        # Se a janela já estiver aberta, traga-a para a frente
        if self.all_slides_window and self.all_slides_window.winfo_exists():
            self.all_slides_window.lift()
            # Atualiza a seleção caso tenha mudado
            self.all_slides_window.update_current_selection_highlight(self.current_index)
            return

    def load_content(self, content_type, slides, content_id=None, start_index=0):
        self.content_type = content_type
        self.slides = slides if slides else []
        self.content_id = content_id
        
        if self.slides:
            self.current_index = start_index if 0 <= start_index < len(self.slides) else 0
            self.update_slide_view()
            # Constrói a grade de miniaturas
            self.master.build_all_slides_grid(self.slides, self.current_index)
        else:
            self.current_index = -1
            self.clear_slide_view()
            self.master.build_all_slides_grid([], -1) # Limpa a grade também
        
        self.update_controls_state()

    def next_slide(self):
        if self.slides and self.current_index < len(self.slides) - 1:
            old_index = self.current_index
            self.current_index += 1
            self.update_slide_view()
            self.master.update_miniature_highlight(old_index, self.current_index)

    def prev_slide(self):
        if self.slides and self.current_index > 0:
            old_index = self.current_index
            self.current_index -= 1
            self.update_slide_view()
            self.master.update_miniature_highlight(old_index, self.current_index)

    def go_to_slide(self, index):
        if self.slides and 0 <= index < len(self.slides):
            old_index = self.current_index
            self.current_index = index
            self.update_slide_view()
            self.master.update_miniature_highlight(old_index, self.current_index)

    def update_slide_view(self): # Removido o argumento 'force_projection_update'
        if 0 <= self.current_index < len(self.slides):
            slide_text = self.slides[self.current_index]
            self.ui["preview_label"].configure(text=slide_text)
            self.ui["indicator_label"].configure(text=f"{self.current_index + 1} / {len(self.slides)}")
            
            if self.projection_window and self.projection_window.winfo_exists():
                # --- LÓGICA PRINCIPAL DA MUDANÇA ---
                # 1. Determina qual seção de configuração usar
                content_map = {"music": "Projection_Music", "bible": "Projection_Bible", "text": "Projection_Text"}
                section_name = content_map.get(self.content_type, "Projection_Music") # Padrão para Música

                # 2. Monta o dicionário de estilo
                style_config = {
                    'font_size': self.config_manager.get_int_setting(section_name, 'font_size', 60),
                    'font_color': self.config_manager.get_setting(section_name, 'font_color', 'white'),
                    'bg_color': self.config_manager.get_setting(section_name, 'bg_color', 'black'),
                    'animation_type': self.config_manager.get_setting(section_name, 'animation_type', 'Nenhuma'),
                    'animation_color': self.config_manager.get_setting(section_name, 'animation_color', 'white')
                }

                # 3. Aplica o estilo e depois o conteúdo
                self.projection_window.apply_style(style_config)
                self.projection_window.update_content(slide_text)
        else:
            self.clear_slide_view()
    
    def clear_slide_view(self):
        self.ui["preview_label"].configure(text="")
        self.ui["indicator_label"].configure(text="- / -")
        if self.projection_window and self.projection_window.winfo_exists():
            self.projection_window.clear_content()

    def update_controls_state(self):
        has_slides = bool(self.slides)
        self.ui["btn_prev"].configure(state="normal" if has_slides else "disabled")
        self.ui["btn_next"].configure(state="normal" if has_slides else "disabled")
        self.ui["btn_show_all"].configure(state="normal" if has_slides else "disabled")

    def handle_projection_button(self):
        """
        Manipula o clique no botão de projeção, alternando entre abrir e fechar.
        """
        is_window_open = self.projection_window and self.projection_window.winfo_exists()

        if is_window_open:
            self.close_projection_window()
        else:
            self.open_projection_window()

    def update_ui_after_projection_opens(self):
        """Chamado após um delay para garantir que a janela exista antes de atualizar a UI."""
        if self.projection_window and self.projection_window.winfo_exists():
            self.update_projection_buttons_state()
            self.update_slide_view()

    def _finalize_projection_setup(self):
        """
        CALLBACK chamado pela ProjectionWindow quando ela está 100% inicializada.
        Este método agora tem a garantia de que a janela existe e está pronta.
        """
        if self.projection_window and self.projection_window.winfo_exists():
            self.update_projection_buttons_state()
            self.update_slide_view()
    
    def open_projection_window(self):
        """Cria e configura a janela de projeção."""
        if self.projection_window and self.projection_window.winfo_exists():
            self.projection_window.lift()
            return

        try:
            monitors = get_monitors()
            target_monitor = None
            if len(monitors) > 1:
                target_monitor = next((m for m in monitors if not m.is_primary), None)
            if not target_monitor and monitors:
                target_monitor = monitors[0]
        except Exception:
            monitors, target_monitor = [], None

        if target_monitor:
            geom = {"x": target_monitor.x, "y": target_monitor.y, "width": target_monitor.width, "height": target_monitor.height}
            
            self.projection_window = ProjectionWindow(
                master=self.master, 
                controller=self,
                target_monitor_geometry=geom,
                config_manager=self.config_manager,
                on_ready_callback=self._finalize_projection_setup
            )
            
            self.update_projection_buttons_state()
        else:
            messagebox.showerror("Erro", "Nenhum monitor foi detectado.", parent=self.master)

    def close_projection_window(self):
        """
        Fecha a janela de projeção, limpa a referência e atualiza o botão.
        """
        # Primeiro, verifica se a janela existe e a destrói
        if self.projection_window and self.projection_window.winfo_exists():
            self.projection_window.destroy()
        
        # --- A PARTE QUE FALTAVA ---
        # Depois de destruir, limpa a referência e atualiza o estado do botão
        self.projection_window = None
        self.update_projection_buttons_state()

    def on_projection_window_closed(self):
        """
        Callback executado pela ProjectionWindow quando ela é fechada.
        Atualiza o estado interno e o texto do botão de projeção.
        """
        self.projection_window = None
        self.update_projection_buttons_state()

    def update_projection_buttons_state(self):
        """Atualiza o texto do botão de projeção com base no estado atual."""
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
        
    def on_closing(self):
        self.close_projection_window()