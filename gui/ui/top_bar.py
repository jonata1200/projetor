"""
Componente de barra superior reutilizável.

Este módulo fornece a classe TopBar que encapsula a criação e gerenciamento
da barra superior da aplicação.
"""

import customtkinter as ctk
from gui.ui.builders import create_top_bar


class TopBar(ctk.CTkFrame):
    """
    Barra superior com controles globais da aplicação.
    
    Esta classe encapsula a criação e gerenciamento da barra superior,
    incluindo botões de projeção, tema, configurações e atalhos.
    """
    
    def __init__(self, master, callbacks):
        """
        Inicializa a barra superior.
        
        Args:
            master: Widget pai onde a barra será criada
            callbacks: Dicionário com callbacks:
                - toggle_theme: Função para alternar tema
                - show_settings: Função para mostrar configurações
                - show_shortcuts: Função para mostrar atalhos
        """
        super().__init__(master)
        
        widgets = create_top_bar(master, callbacks)
        
        # Armazena referências aos widgets
        self.frame = widgets['frame']
        self.btn_projection = widgets['btn_projection']
        self.theme_button = widgets['theme_button']
        self.btn_settings = widgets['btn_settings']
        self.btn_shortcuts = widgets['btn_shortcuts']
    
    def get_widgets(self):
        """
        Retorna um dicionário com todos os widgets criados.
        
        Returns:
            dict: Dicionário com widgets da barra superior
        """
        return {
            'frame': self.frame,
            'btn_projection': self.btn_projection,
            'theme_button': self.theme_button,
            'btn_settings': self.btn_settings,
            'btn_shortcuts': self.btn_shortcuts
        }

