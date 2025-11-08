from tkinter import messagebox
from screeninfo import get_monitors
from gui.projection_window import ProjectionWindow
from gui.views import AllSlidesViewWindow

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
        self.ui["btn_show_all"].configure(command=self.show_all_slides_view)

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
            
        self.all_slides_window = AllSlidesViewWindow(
            master=self.master,
            slides_list=self.slides,
            current_slide_index=self.current_index,
            callback_goto_slide=self.go_to_slide
        )

    def load_content(self, content_type, slides, content_id=None):
        """Ponto de entrada central para carregar novo conteúdo (música ou bíblia)."""
        self.content_type = content_type
        self.slides = slides if slides else []
        self.content_id = content_id

        if self.slides:
            self.current_index = 0
            self.update_slide_view()
        else:
            self.current_index = -1
            self.clear_slide_view()
        
        self.update_controls_state()

    def update_slide_view(self, force_projection_update=False):
        if 0 <= self.current_index < len(self.slides):
            slide_text = self.slides[self.current_index]
            self.ui["preview_label"].configure(text=slide_text)
            self.ui["indicator_label"].configure(text=f"{self.current_index + 1} / {len(self.slides)}")
            
            if self.projection_window and self.projection_window.winfo_exists():
                self.projection_window.update_content(slide_text)
        else:
            self.clear_slide_view()
    
    def clear_slide_view(self):
        self.ui["preview_label"].configure(text="")
        self.ui["indicator_label"].configure(text="- / -")
        if self.projection_window and self.projection_window.winfo_exists():
            self.projection_window.clear_content()

    def next_slide(self):
        if self.slides and self.current_index < len(self.slides) - 1:
            self.current_index += 1
            self.update_slide_view()

    def prev_slide(self):
        if self.slides and self.current_index > 0:
            self.current_index -= 1
            self.update_slide_view()

    def go_to_slide(self, index):
        if self.slides and 0 <= index < len(self.slides):
            self.current_index = index
            self.update_slide_view()

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
                on_ready_callback=self._finalize_projection_setup  # <--- LINHA ADICIONADA DE VOLTA
            )
            
            self.update_projection_buttons_state()
        else:
            messagebox.showerror("Erro", "Nenhum monitor foi detectado.", parent=self.master)

    def close_projection_window(self):
        if self.projection_window and self.projection_window.winfo_exists():
            self.projection_window.destroy()

    def on_projection_window_closed(self):
        """Este método agora é chamado diretamente pela ProjectionWindow antes de fechar."""
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