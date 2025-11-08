import customtkinter as ctk
from core.music_manager import MusicManager
from core.bible_manager import BibleManager
from services.letras_scraper import LetrasScraper
from core.config_manager import ConfigManager
from .controllers.presentation_controller import PresentationController
from .controllers.music_controller import MusicController
from .controllers.bible_controller import BibleController
from .controllers.playlist_controller import PlaylistController
from .controllers.text_controller import TextController
from gui.dialogs import SettingsDialog, ShortcutsHelpDialog

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
        top_frame = ctk.CTkFrame(self)
        top_frame.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="ew")
        
        self.btn_projection_control = ctk.CTkButton(top_frame, text="Abrir Projeção")
        self.btn_projection_control.pack(side="left", padx=5)

        self.theme_button = ctk.CTkButton(top_frame, text="Tema", command=self.toggle_theme)
        self.theme_button.pack(side="right", padx=5)

        self.btn_settings = ctk.CTkButton(top_frame, text="⚙️", width=40, command=self.show_settings_dialog)
        self.btn_settings.pack(side="right", padx=5)
        
        # --- INÍCIO DA ADIÇÃO DO BOTÃO DE AJUDA ---
        self.btn_shortcuts = ctk.CTkButton(top_frame, text="?", width=40, command=self.show_shortcuts_dialog)
        self.btn_shortcuts.pack(side="right", padx=(0, 5))
        # --- FIM DA ADIÇÃO ---
        
    def show_shortcuts_dialog(self):
        """Abre a janela de diálogo com a ajuda dos atalhos."""
        dialog = ShortcutsHelpDialog(master=self)
        dialog.wait_window()

    def _create_preview_pane(self):
        """Cria o painel direito para pré-visualização e controle de slides."""
        outer_frame = ctk.CTkFrame(self)
        outer_frame.grid(row=1, column=1, pady=(0,10), padx=(0,10), sticky="nsew")
        outer_frame.grid_rowconfigure(1, weight=1)
        outer_frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(outer_frame, text="Pré-visualização do Slide Atual", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, pady=5, padx=5, sticky="nw")
        
        preview_frame = ctk.CTkFrame(outer_frame, fg_color=("gray90", "gray20"))
        preview_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=(0,5))
        preview_frame.grid_propagate(False)
        preview_frame.grid_rowconfigure(0, weight=1)
        preview_frame.grid_columnconfigure(0, weight=1)
        
        self.slide_preview_label = ctk.CTkLabel(preview_frame, text="", font=ctk.CTkFont(size=30, weight="bold"), justify=ctk.CENTER)
        self.slide_preview_label.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        
        def _on_resize(event):
            self.slide_preview_label.configure(wraplength=event.width * 0.95)
        preview_frame.bind("<Configure>", _on_resize)
        
        controls_frame = ctk.CTkFrame(outer_frame)
        controls_frame.grid(row=2, column=0, pady=(5,0), padx=5, sticky="ew")
        controls_frame.grid_columnconfigure(1, weight=1)

        self.btn_prev_slide = ctk.CTkButton(controls_frame, text="< Anterior", state="disabled")
        self.btn_prev_slide.grid(row=0, column=0, pady=5, padx=5, sticky="w")
        
        middle_sub_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        middle_sub_frame.grid(row=0, column=1, pady=5, padx=5) # sticky="ew" removido para centralizar

        # Adicione os widgets DENTRO do sub-frame central
        self.btn_show_all_slides = ctk.CTkButton(middle_sub_frame, text="Ver Todos", state="disabled", width=100)
        self.btn_show_all_slides.pack(side="left", padx=10)
        
        self.slide_indicator_label = ctk.CTkLabel(middle_sub_frame, text="- / -")
        self.slide_indicator_label.pack(side="left", padx=10)
        
        # --- BOTÃO NOVO ADICIONADO AQUI ---
        self.btn_clear_preview = ctk.CTkButton(middle_sub_frame, text="Limpar", width=80, fg_color=("gray70", "gray30"))
        self.btn_clear_preview.pack(side="left", padx=10)
        
        self.btn_next_slide = ctk.CTkButton(controls_frame, text="Próximo >", state="disabled")
        self.btn_next_slide.grid(row=0, column=2, pady=5, padx=5, sticky="e")

    def _create_main_tabs(self):
        """Cria o contêiner de abas e chama os métodos para construir a UI de cada aba."""
        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.grid(row=1, column=0, pady=(0,10), padx=10, sticky="nsew")
        
        self.tab_playlist = self.tab_view.add("Ordem de Culto")
        self.tab_music = self.tab_view.add("Músicas")
        self.tab_bible = self.tab_view.add("Bíblia")
        self.tab_text = self.tab_view.add("Avisos / Texto")

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
        """Cria os widgets para a aba da Bíblia (layout simplificado)."""
        tab.grid_columnconfigure(0, weight=1)
        # A linha 0 (options_frame) vai ocupar todo o espaço
        tab.grid_rowconfigure(0, weight=1) 
        
        options_frame = ctk.CTkFrame(tab)
        options_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        options_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(options_frame, text="Navegar por Referência", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=2, pady=(5,10))

        ctk.CTkLabel(options_frame, text="Versão:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.bible_version_var = ctk.StringVar(value="Carregando...")
        self.bible_version_optionmenu = ctk.CTkOptionMenu(options_frame, variable=self.bible_version_var, values=["..."])
        self.bible_version_optionmenu.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(options_frame, text="Livro:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.bible_book_var = ctk.StringVar(value="Aguardando...")
        self.bible_book_optionmenu = ctk.CTkOptionMenu(options_frame, variable=self.bible_book_var, values=["..."])
        self.bible_book_optionmenu.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(options_frame, text="Capítulo:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.bible_chapter_var = ctk.StringVar(value="Aguardando...")
        self.bible_chapter_optionmenu = ctk.CTkOptionMenu(options_frame, variable=self.bible_chapter_var, values=["..."])
        self.bible_chapter_optionmenu.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        
        bottom_frame = ctk.CTkFrame(options_frame)
        bottom_frame.grid(row=4, column=0, columnspan=2, padx=0, pady=10, sticky="ew")
        bottom_frame.grid_columnconfigure((0, 1), weight=1)

        self.btn_load_verses = ctk.CTkButton(bottom_frame, text="Carregar e Visualizar")
        self.btn_load_verses.grid(row=0, column=0, padx=(0,5), sticky="ew")

        self.btn_add_to_playlist_bible = ctk.CTkButton(bottom_frame, text="Adicionar à Ordem", fg_color="sea green", hover_color="dark sea green")
        self.btn_add_to_playlist_bible.grid(row=0, column=1, padx=(5,0), sticky="ew")

    def _init_controllers(self):
        """Agrupa os widgets e instancia os controladores, conectando-os."""
        presentation_ui = {
            "preview_label": self.slide_preview_label,
            "indicator_label": self.slide_indicator_label,
            "btn_prev": self.btn_prev_slide,
            "btn_next": self.btn_next_slide,
            "btn_projection": self.btn_projection_control,
            "btn_clear": self.btn_clear_preview, # <-- ALTERE DE self.btn_clear_projection PARA self.btn_clear_preview
            "btn_show_all": self.btn_show_all_slides
        }
        self.presentation_controller = PresentationController(self, presentation_ui, self.config_manager)

        # O controlador da Playlist é criado primeiro, pois os outros dependem dele.
        playlist_ui = {
            "scroll_frame": self.playlist_scroll_frame,
            "btn_remove": self.btn_playlist_remove,
            "btn_up": self.btn_playlist_up,
            "btn_down": self.btn_playlist_down,
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
            # Navegação
            "version_menu": self.bible_version_optionmenu, "version_var": self.bible_version_var,
            "book_menu": self.bible_book_optionmenu, "book_var": self.bible_book_var,
            "chapter_menu": self.bible_chapter_optionmenu, "chapter_var": self.bible_chapter_var,
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
        dialog.wait_window()

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