import customtkinter as ctk
from core.music_manager import MusicManager
from core.bible_manager import BibleManager
from services.letras_scraper import LetrasScraper
from core.config_manager import ConfigManager
from gui.dialogs import SettingsDialog
from .controllers.presentation_controller import PresentationController
from .controllers.music_controller import MusicController
from .controllers.bible_controller import BibleController

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Projetor IA")
        self.geometry("950x700")

        self.config_manager = ConfigManager()
        self.music_manager = MusicManager()
        self.bible_manager = BibleManager()
        self.letras_scraper = LetrasScraper()

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(1, weight=1)

        self._create_top_bar()
        self._create_preview_pane()
        self._create_main_tabs()

        self._init_controllers()

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Escape>", lambda e: self.presentation_controller.close_projection_window())
        self.bind("<Right>", lambda e: self.presentation_controller.next_slide())
        self.bind("<Left>", lambda e: self.presentation_controller.prev_slide())
        
        self.is_dark_mode = ctk.get_appearance_mode() == "Dark"
        self.update_theme_button_text()

    def _create_top_bar(self):
        """Cria a barra superior com controles globais de projeção e IA."""
        top_frame = ctk.CTkFrame(self)
        top_frame.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="ew")
        
        self.btn_projection_control = ctk.CTkButton(top_frame, text="Abrir Projeção")
        self.btn_projection_control.pack(side="left", padx=5)
        
        self.btn_clear_projection = ctk.CTkButton(top_frame, text="Limpar Tela")
        self.btn_clear_projection.pack(side="left", padx=5)

        self.theme_button = ctk.CTkButton(top_frame, text="Tema", command=self.toggle_theme)
        self.theme_button.pack(side="right", padx=5)

        self.btn_settings = ctk.CTkButton(top_frame, text="⚙️", width=40, command=self.show_settings_dialog)
        self.btn_settings.pack(side="right", padx=5)
        
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
        controls_frame.grid_columnconfigure((0, 3), weight=1)
        
        self.btn_prev_slide = ctk.CTkButton(controls_frame, text="< Anterior", state="disabled")
        self.btn_prev_slide.grid(row=0, column=0, pady=5, padx=2, sticky="ew")
        
        
        self.slide_indicator_label = ctk.CTkLabel(controls_frame, text="- / -")
        self.slide_indicator_label.grid(row=0, column=1, columnspan=2, pady=5, padx=10)
        
        self.btn_next_slide = ctk.CTkButton(controls_frame, text="Próximo >", state="disabled")
        self.btn_next_slide.grid(row=0, column=3, pady=5, padx=2, sticky="ew")

    def _create_main_tabs(self):
        """Cria o contêiner de abas e chama os métodos para construir a UI de cada aba."""
        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.grid(row=1, column=0, pady=(0,10), padx=10, sticky="nsew")
        
        self.tab_music = self.tab_view.add("Músicas")
        self.tab_bible = self.tab_view.add("Bíblia")
        
        self._setup_music_tab_ui(self.tab_music)
        self._setup_bible_tab_ui(self.tab_bible)
        
    def _setup_music_tab_ui(self, tab):
        """Cria os widgets para a aba de Músicas."""
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1)

        actions_frame = ctk.CTkFrame(tab)
        actions_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        actions_frame.grid_columnconfigure(0, weight=1)

        self.music_search_entry = ctk.CTkEntry(actions_frame, placeholder_text="Buscar música...")
        self.music_search_entry.grid(row=0, column=0, padx=(0,5), pady=5, sticky="ew")

        self.btn_import_music = ctk.CTkButton(actions_frame, text="Importar (URL)")
        self.btn_import_music.grid(row=0, column=1, padx=5)

        self.btn_add_manual_music = ctk.CTkButton(actions_frame, text="Adicionar Nova")
        self.btn_add_manual_music.grid(row=0, column=2, padx=5)

        self.btn_edit_song = ctk.CTkButton(actions_frame, text="Editar", state="disabled")
        self.btn_edit_song.grid(row=0, column=3, padx=5)
        
        self.btn_delete_song = ctk.CTkButton(actions_frame, text="Excluir", state="disabled", fg_color="#D32F2F", hover_color="#B71C1C")
        self.btn_delete_song.grid(row=0, column=4, padx=5)

        self.music_scroll_frame = ctk.CTkScrollableFrame(tab, label_text=None)
        self.music_scroll_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=(0, 5))

    def _setup_bible_tab_ui(self, tab):
        """Cria os widgets para a aba da Bíblia."""
        tab.grid_columnconfigure(0, weight=1)
        options_frame = ctk.CTkFrame(tab)
        options_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        options_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(options_frame, text="Versão:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.bible_version_var = ctk.StringVar(value="Carregando...")
        self.bible_version_optionmenu = ctk.CTkOptionMenu(options_frame, variable=self.bible_version_var, values=["..."])
        self.bible_version_optionmenu.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(options_frame, text="Livro:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.bible_book_var = ctk.StringVar(value="Aguardando...")
        self.bible_book_optionmenu = ctk.CTkOptionMenu(options_frame, variable=self.bible_book_var, values=["..."])
        self.bible_book_optionmenu.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(options_frame, text="Capítulo:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.bible_chapter_var = ctk.StringVar(value="Aguardando...")
        self.bible_chapter_optionmenu = ctk.CTkOptionMenu(options_frame, variable=self.bible_chapter_var, values=["..."])
        self.bible_chapter_optionmenu.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        self.btn_load_verses = ctk.CTkButton(tab, text="Carregar Versículos")
        self.btn_load_verses.grid(row=1, column=0, padx=5, pady=10, sticky="ew")

    def _init_controllers(self):
        """Agrupa os widgets e instancia os controladores, conectando-os."""
        presentation_ui = {
            "preview_label": self.slide_preview_label,
            "indicator_label": self.slide_indicator_label,
            "btn_prev": self.btn_prev_slide,
            "btn_next": self.btn_next_slide,
            "btn_projection": self.btn_projection_control,
            "btn_clear": self.btn_clear_projection
        }
        self.presentation_controller = PresentationController(self, presentation_ui, self.config_manager)

        music_ui = {
            "scroll_frame": self.music_scroll_frame,
            "search_entry": self.music_search_entry,
            "btn_add": self.btn_add_manual_music,
            "btn_edit": self.btn_edit_song,
            "btn_delete": self.btn_delete_song,
            "btn_import": self.btn_import_music,
        }
        self.music_controller = MusicController(
            self, music_ui, self.music_manager, self.letras_scraper,
            self.presentation_controller.load_content
        )

        bible_ui = {
            "version_menu": self.bible_version_optionmenu, "version_var": self.bible_version_var,
            "book_menu": self.bible_book_optionmenu, "book_var": self.bible_book_var,
            "chapter_menu": self.bible_chapter_optionmenu, "chapter_var": self.bible_chapter_var,
            "btn_load": self.btn_load_verses
        }
        self.bible_controller = BibleController(
            self, bible_ui, self.bible_manager,
            self.presentation_controller.load_content
        )

    def show_settings_dialog(self):
        """Abre o diálogo de configurações e, ao fechar, notifica o controlador para aplicar as mudanças."""
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
        text = "Mudar p/ Claro" if self.is_dark_mode else "Mudar p/ Escuro"
        self.theme_button.configure(text=text)

    def on_closing(self):
        """Lida com o fechamento da janela principal."""
        self.presentation_controller.on_closing()
        self.destroy()