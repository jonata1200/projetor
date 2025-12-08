from tkinter import messagebox
from screeninfo import get_monitors
from gui.projection_window import ProjectionWindow
import customtkinter as ctk

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
        self.item_animation_data = None  # Animação específica do item (apenas para músicas)

        self.default_preview_bg = self.ui["preview_frame"].cget("fg_color")
        self.default_preview_fg = ctk.ThemeManager.theme["CTkLabel"]["text_color"]

        self._setup_callbacks()
        self._update_preview_style()

    def _setup_callbacks(self):
        self.ui["btn_prev"].configure(command=self.prev_slide)
        self.ui["btn_next"].configure(command=self.next_slide)
        self.ui["btn_projection"].configure(command=self.handle_projection_button)
        self.ui["btn_clear"].configure(command=self.clear_projection_content)

    def load_content(self, content_type, slides, content_id=None, start_index=0, animation_data=None):
        """
        Carrega conteúdo para exibição.
        
        Args:
            content_type: Tipo de conteúdo ('music', 'bible', 'text')
            slides: Lista de slides
            content_id: ID do conteúdo (opcional)
            start_index: Índice inicial do slide (padrão: 0)
            animation_data: Dados de animação do item (apenas para músicas, opcional)
        """
        apply_new_style = (self.content_type != content_type)
        self.content_type = content_type
        
        self.slides = slides if slides else []
        self.content_id = content_id
        # Armazena animação do item se for música
        self.item_animation_data = animation_data if content_type == 'music' else None
        
        if self.slides:
            self.current_index = start_index if 0 <= start_index < len(self.slides) else 0
            
            # Sempre aplica o estilo quando o conteúdo muda (especialmente para animação)
            if self.projection_window and self.projection_window.winfo_exists():
                self._apply_style_to_projection_window()
            
            self.update_slide_view()
            if hasattr(self.master, 'build_all_slides_grid'):
                self.master.build_all_slides_grid(self.slides, self.current_index)
        else:
            self.current_index = -1
            self.clear_slide_view()
            if hasattr(self.master, 'build_all_slides_grid'):
                self.master.build_all_slides_grid([], -1)
        
        self.update_controls_state()
        self._update_preview_style()
    
    def _apply_style_to_projection_window(self):
        if not self.projection_window or not self.projection_window.winfo_exists():
            return
        
        style_config = self._get_style_config_for_current_content()
        self.projection_window.apply_style(style_config)

    def _update_preview_style(self):
        if self.content_type is None:
            self.ui["preview_frame"].configure(fg_color=self.default_preview_bg)
            self.ui["preview_label"].configure(text_color=self.default_preview_fg)
            self.ui["animation_indicator"].configure(fg_color="transparent")
            # Limpa o indicador de texto da animação
            self.ui["animation_text_indicator"].configure(text="")
            return

        style_config = self._get_style_config_for_current_content()

        self.ui["preview_frame"].configure(fg_color=style_config['bg_color'])
        self.ui["preview_label"].configure(text_color=style_config['font_color'])
        
        anim_type = style_config.get('animation_type', 'Nenhuma')
        anim_text_map = {
            "Neve": "❄️ Neve Ativa",
            "Partículas Flutuantes": "✨ Partículas Ativas",
            "Estrelas Piscando": "⭐ Estrelas Ativas"
        }
        # --- ALTERAÇÃO 1: ATUALIZA O INDICADOR DE TEXTO DA ANIMAÇÃO ---
        self.ui["animation_text_indicator"].configure(text=anim_text_map.get(anim_type, ""))
        
        if anim_type != 'Nenhuma':
            self.ui["animation_indicator"].configure(fg_color=style_config['animation_color'])
        else:
            self.ui["animation_indicator"].configure(fg_color="transparent")
        
        # Força o recálculo da fonte com base no tamanho atual
        current_height = self.ui["preview_frame"].winfo_height()
        if current_height > 1: # Garante que o widget já tenha sido desenhado
            self.update_preview_font_size(current_height)

    def _get_style_config_for_current_content(self):
        content_map = {"music": "Projection_Music", "bible": "Projection_Bible", "text": "Projection_Text"}
        section_name = content_map.get(self.content_type, "Projection_Music")

        config = {
            'font_size': self.config_manager.get_int_setting(section_name, 'font_size', 60),
            'font_color': self.config_manager.get_setting(section_name, 'font_color', 'white'),
            'bg_color': self.config_manager.get_setting(section_name, 'bg_color', 'black'),
            'animation_type': 'Nenhuma',  # Padrão: nenhuma animação
            'animation_color': '#DDDDDD'  # Cor padrão (não usada se animation_type for 'Nenhuma')
        }
        
        # Para músicas, usa a animação do item (se houver)
        # A animação agora é configurada apenas na Ordem de Culto
        if self.content_type == 'music':
            if self.item_animation_data:
                config['animation_type'] = self.item_animation_data.get('animation_type', 'Nenhuma')
                config['animation_color'] = self.item_animation_data.get('animation_color', '#DDDDDD')
            else:
                # Item antigo sem animação - usa "Nenhuma" como padrão
                config['animation_type'] = 'Nenhuma'
                config['animation_color'] = '#DDDDDD'
        
        # Para Bíblia e Texto, sempre usa "Nenhuma" (animação removida das configurações)
        
        return config

    def refresh_styles(self):
        self._update_preview_style()
        if self.projection_window and self.projection_window.winfo_exists():
            self._apply_style_to_projection_window()

    # --- ALTERAÇÃO 2: NOVO MÉTODO PARA A FONTE PROPORCIONAL ---
    def update_preview_font_size(self, current_height):
        """
        Calcula e aplica um tamanho de fonte proporcional à altura do painel de pré-visualização.
        """
        if current_height <= 1: return # Evita cálculos se o widget não for visível

        # Fator de proporção: um valor maior resulta em fonte menor.
        # 12 a 15 geralmente funcionam bem.
        PROPORTION_FACTOR = 14
        
        # Calcula o novo tamanho, garantindo um tamanho mínimo de 8.
        new_size = max(8, int(current_height / PROPORTION_FACTOR))
        
        # Aplica a nova fonte ao label de pré-visualização
        self.ui["preview_label"].configure(font=ctk.CTkFont(size=new_size, weight="bold"))

    def update_slide_view(self):
        if 0 <= self.current_index < len(self.slides):
            slide_text = self.slides[self.current_index]
            self.ui["preview_label"].configure(text=slide_text)
            self.ui["indicator_label"].configure(text=f"{self.current_index + 1} / {len(self.slides)}")
            
            if self.projection_window and self.projection_window.winfo_exists():
                self.projection_window.update_content(slide_text)
        else:
            self.clear_slide_view()

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
        self._update_preview_style()

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
        self.update_projection_buttons_state()
        self._apply_style_to_projection_window()
        self.update_slide_view() 
    
    def close_projection_window(self):
        if self.projection_window and self.projection_window.winfo_exists():
            self.projection_window.destroy()
        self.on_projection_window_closed()

    def on_projection_window_closed(self):
        self.projection_window = None
        self.update_projection_buttons_state()

    def update_projection_buttons_state(self):
        is_open = self.projection_window and self.projection_window.winfo_exists()
        text = "Fechar Projeção" if is_open else "Abrir Projeção"
        self.ui["btn_projection"].configure(text=text)
        
    def on_closing(self):
        self.close_projection_window()