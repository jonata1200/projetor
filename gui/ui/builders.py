"""
Funções auxiliares para construção de componentes de UI.

Este módulo fornece funções reutilizáveis para criar componentes da interface,
facilitando a manutenção e reduzindo duplicação de código.
"""

import customtkinter as ctk


def create_top_bar(master, callbacks):
    """
    Cria a barra superior com controles globais.
    
    Args:
        master: Widget pai onde a barra será criada
        callbacks: Dicionário com callbacks:
            - toggle_theme: Função para alternar tema
            - show_settings: Função para mostrar configurações
            - show_shortcuts: Função para mostrar atalhos
    
    Returns:
        dict: Dicionário com widgets criados:
            - frame: Frame da barra superior
            - btn_projection: Botão de controle de projeção
            - theme_button: Botão de tema
            - btn_settings: Botão de configurações
            - btn_shortcuts: Botão de atalhos
    """
    top_frame = ctk.CTkFrame(master)
    top_frame.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="ew")
    
    btn_projection = ctk.CTkButton(top_frame, text="Abrir Projeção")
    btn_projection.pack(side="left", padx=5)
    
    theme_button = ctk.CTkButton(top_frame, text="Tema", command=callbacks.get('toggle_theme'))
    theme_button.pack(side="right", padx=5)
    
    btn_settings = ctk.CTkButton(top_frame, text="⚙️", width=40, command=callbacks.get('show_settings'))
    btn_settings.pack(side="right", padx=5)
    
    btn_shortcuts = ctk.CTkButton(top_frame, text="?", width=40, command=callbacks.get('show_shortcuts'))
    btn_shortcuts.pack(side="right", padx=(0, 5))
    
    return {
        'frame': top_frame,
        'btn_projection': btn_projection,
        'theme_button': theme_button,
        'btn_settings': btn_settings,
        'btn_shortcuts': btn_shortcuts
    }


def create_preview_pane(master, on_resize_callback):
    """
    Cria o painel de pré-visualização com abas.
    
    Args:
        master: Widget pai onde o painel será criado
        on_resize_callback: Função chamada quando o painel é redimensionado
    
    Returns:
        dict: Dicionário com widgets criados:
            - outer_frame: Frame externo
            - preview_tab_view: Tabview de pré-visualização
            - preview_frame: Frame de pré-visualização
            - slide_preview_label: Label do slide
            - animation_text_indicator: Indicador de texto de animação
            - animation_color_indicator: Indicador de cor de animação
            - all_slides_grid_frame: Frame da grade de slides
            - btn_prev_slide: Botão slide anterior
            - btn_next_slide: Botão próximo slide
            - slide_indicator_label: Label do indicador
            - btn_clear_preview: Botão limpar pré-visualização
            - slide_miniatures: Lista de miniaturas (inicialmente vazia)
    """
    outer_frame = ctk.CTkFrame(master)
    outer_frame.grid(row=1, column=1, pady=(0,10), padx=(0,10), sticky="nsew")
    outer_frame.grid_rowconfigure(0, weight=1)
    outer_frame.grid_columnconfigure(0, weight=1)
    
    preview_tab_view = ctk.CTkTabview(outer_frame)
    preview_tab_view.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    
    tab_single = preview_tab_view.add("Pré-visualização")
    tab_all = preview_tab_view.add("Todos os Slides")
    
    tab_single.grid_rowconfigure(0, weight=1)
    tab_single.grid_columnconfigure(0, weight=1)
    
    preview_frame = ctk.CTkFrame(tab_single, fg_color=("gray90", "gray20"))
    preview_frame.grid(row=0, column=0, sticky="nsew")
    preview_frame.grid_propagate(False)
    
    slide_preview_label = ctk.CTkLabel(
        preview_frame, text="", 
        font=ctk.CTkFont(size=30, weight="bold"), 
        justify=ctk.CENTER,
        corner_radius=0  # Remove bordas arredondadas que podem afetar o espaço
    )
    slide_preview_label.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
    
    preview_frame.bind("<Configure>", on_resize_callback)
    
    animation_text_indicator = ctk.CTkLabel(
        preview_frame, text="", 
        font=ctk.CTkFont(size=12), 
        text_color="gray"
    )
    animation_text_indicator.place(relx=0.02, rely=0.03)
    
    animation_color_indicator = ctk.CTkFrame(
        preview_frame, height=5, fg_color="transparent"
    )
    animation_color_indicator.pack(side="bottom", fill="x", padx=5, pady=5)
    
    all_slides_grid_frame = ctk.CTkScrollableFrame(tab_all, label_text=None)
    all_slides_grid_frame.pack(fill="both", expand=True)
    
    controls_frame = ctk.CTkFrame(outer_frame)
    controls_frame.grid(row=1, column=0, pady=(5,0), padx=5, sticky="ew")
    controls_frame.grid_columnconfigure(1, weight=1)
    
    btn_prev_slide = ctk.CTkButton(controls_frame, text="< Anterior", state="disabled")
    btn_prev_slide.grid(row=0, column=0, pady=5, padx=5, sticky="w")
    
    middle_sub_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
    middle_sub_frame.grid(row=0, column=1, pady=5, padx=5)
    
    slide_indicator_label = ctk.CTkLabel(middle_sub_frame, text="- / -")
    slide_indicator_label.pack(side="left", padx=10)
    
    btn_clear_preview = ctk.CTkButton(
        middle_sub_frame, text="Limpar", width=80, 
        fg_color=("gray70", "gray30")
    )
    btn_clear_preview.pack(side="left", padx=10)
    
    btn_next_slide = ctk.CTkButton(controls_frame, text="Próximo >", state="disabled")
    btn_next_slide.grid(row=0, column=2, pady=5, padx=5, sticky="e")
    
    return {
        'outer_frame': outer_frame,
        'preview_tab_view': preview_tab_view,
        'preview_frame': preview_frame,
        'slide_preview_label': slide_preview_label,
        'animation_text_indicator': animation_text_indicator,
        'animation_color_indicator': animation_color_indicator,
        'all_slides_grid_frame': all_slides_grid_frame,
        'btn_prev_slide': btn_prev_slide,
        'btn_next_slide': btn_next_slide,
        'slide_indicator_label': slide_indicator_label,
        'btn_clear_preview': btn_clear_preview,
        'slide_miniatures': []
    }


def create_main_tabs(master):
    """
    Cria o contêiner de abas principais da aplicação.
    
    Args:
        master: Widget pai onde as abas serão criadas
    
    Returns:
        dict: Dicionário com widgets criados:
            - tab_view: Tabview principal
            - tab_playlist: Aba de Ordem de Culto
            - tab_music: Aba de Músicas
            - tab_bible: Aba de Bíblia
            - tab_text: Aba de Avisos / Texto
    """
    tab_view = ctk.CTkTabview(master)
    tab_view.grid(row=1, column=0, pady=(0,10), padx=10, sticky="nsew")
    
    tab_playlist = tab_view.add("Ordem de Culto")
    tab_music = tab_view.add("Músicas")
    tab_bible = tab_view.add("Bíblia")
    tab_text = tab_view.add("Avisos / Texto")
    
    return {
        'tab_view': tab_view,
        'tab_playlist': tab_playlist,
        'tab_music': tab_music,
        'tab_bible': tab_bible,
        'tab_text': tab_text
    }

