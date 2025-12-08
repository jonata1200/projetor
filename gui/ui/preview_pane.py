"""
Componente de painel de pré-visualização reutilizável.

Este módulo fornece a classe PreviewPane que encapsula a criação e gerenciamento
do painel de pré-visualização da aplicação.
"""

import customtkinter as ctk
from gui.ui.builders import create_preview_pane


class PreviewPane(ctk.CTkFrame):
    """
    Painel de pré-visualização com abas para visualização de slides.
    
    Esta classe encapsula a criação e gerenciamento do painel de pré-visualização,
    incluindo visualização única, grade de todos os slides e controles de navegação.
    """
    
    def __init__(self, master, on_resize_callback):
        """
        Inicializa o painel de pré-visualização.
        
        Args:
            master: Widget pai onde o painel será criado
            on_resize_callback: Função chamada quando o painel é redimensionado
        """
        super().__init__(master)
        
        widgets = create_preview_pane(master, on_resize_callback)
        
        # Armazena referências aos widgets
        self.outer_frame = widgets['outer_frame']
        self.preview_tab_view = widgets['preview_tab_view']
        self.preview_frame = widgets['preview_frame']
        self.slide_preview_label = widgets['slide_preview_label']
        self.animation_text_indicator = widgets['animation_text_indicator']
        self.animation_color_indicator = widgets['animation_color_indicator']
        self.all_slides_grid_frame = widgets['all_slides_grid_frame']
        self.btn_prev_slide = widgets['btn_prev_slide']
        self.btn_next_slide = widgets['btn_next_slide']
        self.slide_indicator_label = widgets['slide_indicator_label']
        self.btn_clear_preview = widgets['btn_clear_preview']
        self.slide_miniatures = widgets['slide_miniatures']
    
    def get_widgets(self):
        """
        Retorna um dicionário com todos os widgets criados.
        
        Returns:
            dict: Dicionário com widgets do painel de pré-visualização
        """
        return {
            'outer_frame': self.outer_frame,
            'preview_tab_view': self.preview_tab_view,
            'preview_frame': self.preview_frame,
            'slide_preview_label': self.slide_preview_label,
            'animation_text_indicator': self.animation_text_indicator,
            'animation_color_indicator': self.animation_color_indicator,
            'all_slides_grid_frame': self.all_slides_grid_frame,
            'btn_prev_slide': self.btn_prev_slide,
            'btn_next_slide': self.btn_next_slide,
            'slide_indicator_label': self.slide_indicator_label,
            'btn_clear_preview': self.btn_clear_preview,
            'slide_miniatures': self.slide_miniatures
        }

