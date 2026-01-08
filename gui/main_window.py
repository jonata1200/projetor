import customtkinter as ctk
from core.music_manager import MusicManager
from core.bible_manager import BibleManager
# --- IMPORTAÇÃO MODIFICADA ---
from core.services.letras_scraper import LetrasScraper
from core.config_manager import ConfigManager
from .controllers.presentation_controller import PresentationController
from .controllers.music_controller import MusicController
from .controllers.bible_controller import BibleController
from .controllers.playlist_controller import PlaylistController
from .controllers.text_controller import TextController
from gui.dialogs import SettingsDialog, ShortcutsHelpDialog
from gui.ui.builders import create_top_bar, create_preview_pane, create_main_tabs

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Projetor")
        self.geometry("950x700")

        # Gerenciadores de Lógica
        self.config_manager = ConfigManager()
        self.music_manager = MusicManager()
        self.bible_manager = BibleManager()
        self.letras_scraper = LetrasScraper()

        # Configuração do Layout Principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(1, weight=1)

        # Criação dos Componentes da UI
        self._create_top_bar()
        self._create_preview_pane()
        self._create_main_tabs()

        # Inicialização dos Controladores
        self._init_controllers()

        # Atalhos e Eventos Globais
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Escape>", lambda e: self.presentation_controller.close_projection_window())
        self.bind("<Right>", lambda e: self.presentation_controller.next_slide())
        self.bind("<Left>", lambda e: self.presentation_controller.prev_slide())
        self.bind("<c>", lambda e: self.presentation_controller.clear_projection_content())

        self.is_dark_mode = ctk.get_appearance_mode() == "Dark"
        self.update_theme_button_text()

    def _create_top_bar(self):
        """Cria a barra superior com controles globais de projeção."""
        callbacks = {
            'toggle_theme': self.toggle_theme,
            'show_settings': self.show_settings_dialog,
            'show_shortcuts': self.show_shortcuts_dialog
        }
        widgets = create_top_bar(self, callbacks)
        
        self.btn_projection_control = widgets['btn_projection']
        self.theme_button = widgets['theme_button']
        self.btn_settings = widgets['btn_settings']
        self.btn_shortcuts = widgets['btn_shortcuts']
        
    def show_shortcuts_dialog(self):
        """Abre a janela de diálogo com a ajuda dos atalhos."""
        dialog = ShortcutsHelpDialog(master=self)
        dialog.wait_window()

    def _create_preview_pane(self):
        """Cria o painel direito com abas para pré-visualização e visão geral."""
        widgets = create_preview_pane(self, self._on_preview_resize)
        
        self.preview_tab_view = widgets['preview_tab_view']
        self.preview_frame = widgets['preview_frame']
        self.slide_preview_label = widgets['slide_preview_label']
        self.animation_text_indicator = widgets['animation_text_indicator']
        self.animation_color_indicator = widgets['animation_color_indicator']
        self.all_slides_grid_frame = widgets['all_slides_grid_frame']
        self.slide_miniatures = widgets['slide_miniatures']
        self.btn_prev_slide = widgets['btn_prev_slide']
        self.btn_next_slide = widgets['btn_next_slide']
        self.slide_indicator_label = widgets['slide_indicator_label']
        self.btn_clear_preview = widgets['btn_clear_preview']

    def build_all_slides_grid(self, slides, current_index):
        """Constrói a grade de miniaturas de slides na aba 'Todos os Slides'."""
        for widget in self.all_slides_grid_frame.winfo_children():
            widget.destroy()
        self.slide_miniatures.clear()

        if not slides: return

        num_columns = 3
        for i in range(num_columns):
            self.all_slides_grid_frame.grid_columnconfigure(i, weight=1, uniform="slide_col")

        for index, slide_text in enumerate(slides):
            is_current = (index == current_index)
            border_color = "cyan" if is_current else ("gray70", "gray30")
            
            miniature_frame = ctk.CTkFrame(self.all_slides_grid_frame, border_width=2, border_color=border_color)
            miniature_frame.grid(row=index // num_columns, column=index % num_columns, padx=5, pady=5, sticky="nsew")
            self.slide_miniatures.append(miniature_frame)

            preview_text = " ".join(slide_text.split()[:20]) + ("..." if len(slide_text.split()) > 20 else "")
            text_label = ctk.CTkLabel(miniature_frame, text=preview_text, font=ctk.CTkFont(size=11), wraplength=180, justify="left", anchor="nw")
            text_label.pack(fill="both", expand=True, padx=5, pady=5)

            for widget in [miniature_frame, text_label]:
                widget.bind("<Button-1>", lambda e, idx=index: self.presentation_controller.go_to_slide(idx))

    def update_miniature_highlight(self, old_index, new_index):
        """Atualiza qual miniatura está destacada."""
        if 0 <= old_index < len(self.slide_miniatures):
            self.slide_miniatures[old_index].configure(border_color=("gray70", "gray30"))
        if 0 <= new_index < len(self.slide_miniatures):
            self.slide_miniatures[new_index].configure(border_color="cyan")

    def _create_main_tabs(self):
        """Cria o contêiner de abas e chama os métodos para construir a UI de cada aba."""
        widgets = create_main_tabs(self)
        
        self.tab_view = widgets['tab_view']
        self.tab_playlist = widgets['tab_playlist']
        self.tab_music = widgets['tab_music']
        self.tab_bible = widgets['tab_bible']
        self.tab_text = widgets['tab_text']

        self._setup_playlist_tab_ui(self.tab_playlist)
        self._setup_music_tab_ui(self.tab_music)
        self._setup_bible_tab_ui(self.tab_bible)
        self._setup_text_tab_ui(self.tab_text)

        self.tab_view.set("Ordem de Culto") # Inicia na aba da playlist

    def _setup_text_tab_ui(self, tab):
        """Cria os widgets para a aba de Texto Livre / Avisos."""
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(0, weight=1) # A caixa de texto vai expandir

        # Caixa de texto grande para o usuário digitar
        self.text_input_textbox = ctk.CTkTextbox(tab, font=ctk.CTkFont(size=14), wrap="word")
        self.text_input_textbox.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # Frame para os botões de ação
        buttons_frame = ctk.CTkFrame(tab)
        buttons_frame.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        buttons_frame.grid_columnconfigure(0, weight=1) # Faz o botão de projetar expandir

        self.btn_project_text = ctk.CTkButton(buttons_frame, text="Projetar Texto")
        self.btn_project_text.grid(row=0, column=0, padx=(0,5), sticky="ew")

        self.btn_clear_text = ctk.CTkButton(buttons_frame, text="Limpar Caixa", width=120)
        self.btn_clear_text.grid(row=0, column=1, padx=(5,0), sticky="e")

    def _setup_playlist_tab_ui(self, tab):
        """Cria os widgets para a aba da Ordem de Culto."""
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1)

        actions_frame = ctk.CTkFrame(tab)
        actions_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.btn_playlist_remove = ctk.CTkButton(actions_frame, text="Remover", state="disabled", fg_color="#D32F2F", hover_color="#B71C1C")
        self.btn_playlist_remove.pack(side="left", padx=5, pady=5)

        self.btn_playlist_up = ctk.CTkButton(actions_frame, text="Subir ▲", state="disabled", width=100)
        self.btn_playlist_up.pack(side="left", padx=5, pady=5)

        self.btn_playlist_down = ctk.CTkButton(actions_frame, text="Descer ▼", state="disabled", width=100)
        self.btn_playlist_down.pack(side="left", padx=5, pady=5)
        
        self.btn_playlist_edit_animation = ctk.CTkButton(actions_frame, text="Editar Animação", state="disabled", width=120)
        self.btn_playlist_edit_animation.pack(side="left", padx=5, pady=5)
        
        self.btn_playlist_clear = ctk.CTkButton(actions_frame, text="Limpar Tudo")
        self.btn_playlist_clear.pack(side="right", padx=5, pady=5)

        self.playlist_scroll_frame = ctk.CTkScrollableFrame(tab, label_text="Itens da Ordem de Culto")
        self.playlist_scroll_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=(0, 5))

    def _setup_music_tab_ui(self, tab):
        """Cria os widgets para a aba de Músicas com um layout melhorado."""

        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1) # Apenas a lista de músicas expande

        # --- Frame superior para busca e adição ---
        top_actions_frame = ctk.CTkFrame(tab)
        top_actions_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        top_actions_frame.grid_columnconfigure(0, weight=1) # Campo de busca expande

        self.music_search_entry = ctk.CTkEntry(top_actions_frame, placeholder_text="Buscar música...")
        self.music_search_entry.grid(row=0, column=0, padx=(0,5), pady=5, sticky="ew")

        self.btn_import_music = ctk.CTkButton(top_actions_frame, text="Importar (URL)")
        self.btn_import_music.grid(row=0, column=1, padx=5, pady=5)

        self.btn_add_manual_music = ctk.CTkButton(top_actions_frame, text="Adicionar Nova")
        self.btn_add_manual_music.grid(row=0, column=2, padx=5, pady=5)
        
        # --- Lista de Músicas (no meio) ---
        self.music_scroll_frame = ctk.CTkScrollableFrame(tab, label_text=None)
        self.music_scroll_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=(0, 5))

        # --- Frame inferior para ações contextuais ---
        bottom_actions_frame = ctk.CTkFrame(tab)
        bottom_actions_frame.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        bottom_actions_frame.grid_columnconfigure((0, 4), weight=1) # Colunas vazias para centralizar

        self.btn_add_to_playlist_music = ctk.CTkButton(bottom_actions_frame, text="✔ Adicionar à Ordem", state="disabled", fg_color="sea green", hover_color="dark sea green")
        self.btn_add_to_playlist_music.grid(row=0, column=1, padx=5, pady=5)

        self.btn_edit_song = ctk.CTkButton(bottom_actions_frame, text="✎ Editar", state="disabled")
        self.btn_edit_song.grid(row=0, column=2, padx=5, pady=5)
        
        self.btn_delete_song = ctk.CTkButton(bottom_actions_frame, text="❌ Excluir", state="disabled", fg_color="#D32F2F", hover_color="#B71C1C")
        self.btn_delete_song.grid(row=0, column=3, padx=5, pady=5)

    def _setup_bible_tab_ui(self, tab):
        """Cria os widgets para a aba da Bíblia com seletor de versículo."""
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(0, weight=1) 
        
        options_frame = ctk.CTkFrame(tab)
        options_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        options_frame.grid_columnconfigure(1, weight=1)
        
        # O texto "Navegar por Referência" foi removido.

        # Linha 0: Versão
        ctk.CTkLabel(options_frame, text="Versão:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.bible_version_var = ctk.StringVar(value="Carregando...")
        self.bible_version_optionmenu = ctk.CTkOptionMenu(options_frame, variable=self.bible_version_var, values=["..."])
        self.bible_version_optionmenu.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Linha 1: Livro
        ctk.CTkLabel(options_frame, text="Livro:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.bible_book_var = ctk.StringVar(value="Aguardando...")
        self.bible_book_optionmenu = ctk.CTkOptionMenu(options_frame, variable=self.bible_book_var, values=["..."])
        self.bible_book_optionmenu.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Linha 2: Capítulo
        ctk.CTkLabel(options_frame, text="Capítulo:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.bible_chapter_var = ctk.StringVar(value="Aguardando...")
        self.bible_chapter_optionmenu = ctk.CTkOptionMenu(options_frame, variable=self.bible_chapter_var, values=["..."])
        self.bible_chapter_optionmenu.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # --- INÍCIO DA ADIÇÃO DO SELETOR DE VERSÍCULO ---
        # Linha 3: Versículo
        ctk.CTkLabel(options_frame, text="Versículo:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.bible_verse_var = ctk.StringVar(value="Aguardando...")
        self.bible_verse_optionmenu = ctk.CTkOptionMenu(options_frame, variable=self.bible_verse_var, values=["..."], state="disabled")
        self.bible_verse_optionmenu.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        # --- FIM DA ADIÇÃO ---

        # Linha 4: Botões
        bottom_frame = ctk.CTkFrame(options_frame)
        bottom_frame.grid(row=4, column=0, columnspan=2, padx=0, pady=10, sticky="ew")
        bottom_frame.grid_columnconfigure((0, 1), weight=1)

        self.btn_load_verses = ctk.CTkButton(bottom_frame, text="Carregar e Visualizar")
        self.btn_load_verses.grid(row=0, column=0, padx=(0,5), sticky="ew")

        self.btn_add_to_playlist_bible = ctk.CTkButton(bottom_frame, text="Adicionar à Ordem", fg_color="sea green", hover_color="dark sea green")
        self.btn_add_to_playlist_bible.grid(row=0, column=1, padx=(5,0), sticky="ew")

    # --- ALTERAÇÃO 2: MÉTODO PARA CHAMAR O CONTROLADOR QUANDO A JANELA REDIMENSIONA ---
    def _on_preview_resize(self, event):
        """
        Quando a pré-visualização muda de tamanho, atualiza o wraplength e
        avisa o controlador para recalcular o tamanho da fonte.
        """
        # Calcula o wraplength proporcional à largura da projeção
        if hasattr(self, 'presentation_controller'):
            # Usa a mesma proporção de largura que a projeção (90% da largura)
            # Isso garante que o texto quebre na mesma posição que na projeção
            # Matematicamente: (projection_width * 0.9) * (event.width / projection_width) = event.width * 0.9
            wraplength = int(event.width * 0.9)
            self.slide_preview_label.configure(wraplength=wraplength)
            # Chama o método do controlador para ajustar a fonte com largura e altura
            self.presentation_controller.update_preview_font_size(event.width, event.height)
        else:
            # Fallback se o controlador ainda não foi criado
            self.slide_preview_label.configure(wraplength=int(event.width * 0.9))

    def _init_controllers(self):
        """Agrupa os widgets e instancia os controladores, conectando-os."""
        presentation_ui = {
            "preview_label": self.slide_preview_label,
            "preview_frame": self.preview_frame,
            "animation_indicator": self.animation_color_indicator,
            # --- ALTERAÇÃO 3: PASSA O NOVO LABEL PARA O CONTROLADOR ---
            "animation_text_indicator": self.animation_text_indicator,
            "indicator_label": self.slide_indicator_label,
            "btn_prev": self.btn_prev_slide,
            "btn_next": self.btn_next_slide,
            "btn_projection": self.btn_projection_control,
            "btn_clear": self.btn_clear_preview,
        }
        self.presentation_controller = PresentationController(self, presentation_ui, self.config_manager)

        # O controlador da Playlist é criado primeiro, pois os outros dependem dele.
        playlist_ui = {
            "scroll_frame": self.playlist_scroll_frame,
            "btn_remove": self.btn_playlist_remove,
            "btn_up": self.btn_playlist_up,
            "btn_down": self.btn_playlist_down,
            "btn_edit_animation": self.btn_playlist_edit_animation,
            "btn_clear": self.btn_playlist_clear
        }
        self.playlist_controller = PlaylistController(
            self, playlist_ui, self.presentation_controller
        )

        # O controlador de Música recebe a referência ao controlador da Playlist.
        music_ui = {
            "scroll_frame": self.music_scroll_frame,
            "search_entry": self.music_search_entry,
            "btn_add": self.btn_add_manual_music,
            "btn_edit": self.btn_edit_song,
            "btn_delete": self.btn_delete_song,
            "btn_import": self.btn_import_music,
            "btn_add_to_playlist": self.btn_add_to_playlist_music
        }
        self.music_controller = MusicController(
            self, music_ui, self.music_manager, self.letras_scraper,
            self.presentation_controller.load_content,
            self.playlist_controller
        )

        # O controlador da Bíblia também recebe a referência ao controlador da Playlist.
        bible_ui = {
            "version_menu": self.bible_version_optionmenu, "version_var": self.bible_version_var,
            "book_menu": self.bible_book_optionmenu, "book_var": self.bible_book_var,
            "chapter_menu": self.bible_chapter_optionmenu, "chapter_var": self.bible_chapter_var,
            # --- INÍCIO DA ADIÇÃO ---
            "verse_menu": self.bible_verse_optionmenu, "verse_var": self.bible_verse_var,
            # --- FIM DA ADIÇÃO ---
            "btn_load": self.btn_load_verses,
            "btn_add_to_playlist": self.btn_add_to_playlist_bible,
        }
        self.bible_controller = BibleController(
            self, bible_ui, self.bible_manager,
            self.presentation_controller.load_content,
            self.playlist_controller
        )

        # Instancia o novo controlador de Texto
        text_ui = {
            "textbox": self.text_input_textbox,
            "btn_project": self.btn_project_text,
            "btn_clear": self.btn_clear_text
        }
        self.text_controller = TextController(
            self, text_ui, self.presentation_controller
        )

    def show_settings_dialog(self):
        """Abre o diálogo de configurações."""
        dialog = SettingsDialog(master=self, config_manager=self.config_manager)
        dialog.wait_window() # Esta linha pausa a execução até a janela de diálogo ser fechada

        # --- ALTERAÇÃO 4: AVISAMOS O CONTROLADOR PARA ATUALIZAR OS ESTILOS ---
        # Assim que a janela fecha, mandamos o controlador recarregar os estilos.
        self.presentation_controller.refresh_styles()

    def toggle_theme(self):
        """Alterna entre os temas Claro e Escuro."""
        new_mode = "Light" if self.is_dark_mode else "Dark"
        ctk.set_appearance_mode(new_mode)
        self.is_dark_mode = not self.is_dark_mode
        self.update_theme_button_text()

    def update_theme_button_text(self):
        """Atualiza o texto do botão de tema."""
        text = "Tema Claro" if self.is_dark_mode else "Tema Escuro"
        self.theme_button.configure(text=text)

    def on_closing(self):
        """Lida com o fechamento da janela principal."""
        self.presentation_controller.on_closing()
        self.destroy()