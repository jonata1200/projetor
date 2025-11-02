import customtkinter as ctk
from tkinter import messagebox

class BibleController:
    """
    Controlador responsável por toda a lógica da aba da Bíblia.
    - Gerencia a seleção de versão, livro e capítulo.
    - Interage com o BibleManager para buscar dados.
    - Popula os widgets da UI com os dados corretos.
    - Notifica o PresentationController quando versículos são carregados.
    """
    def __init__(self, master, view_widgets, bible_manager, on_content_selected_callback):
        self.master = master
        self.view = view_widgets
        self.manager = bible_manager
        self.on_content_selected = on_content_selected_callback
        
        self.versions_data = []
        self.books_data = []

        self._setup_callbacks()
        self.populate_versions()

    def _setup_callbacks(self):
        """Conecta os widgets da UI aos métodos deste controlador."""
        self.view["version_menu"].configure(command=self.on_version_selected)
        self.view["book_menu"].configure(command=self.on_book_selected)
        self.view["btn_load"].configure(command=self.load_verses)

    def populate_versions(self):
        """Busca as versões da Bíblia e preenche o menu de versões."""
        self.versions_data = self.manager.load_versions()
        version_menu = self.view["version_menu"]
        version_var = self.view["version_var"]

        if self.versions_data:
            version_names = [v['name'] for v in self.versions_data]
            version_menu.configure(values=version_names)
            if version_names:
                version_var.set(version_names[0])
                self.on_version_selected(version_names[0])
        else:
            version_menu.configure(values=["Erro ao carregar"])
            version_var.set("Erro ao carregar")
            self.view["book_menu"].configure(values=["-"])
            self.view["book_var"].set("-")
            self.view["chapter_menu"].configure(values=["-"])
            self.view["chapter_var"].set("-")

    def on_version_selected(self, selected_version_name):
        """Chamado quando uma nova versão é selecionada. Carrega os livros correspondentes."""
        version_data = next((v for v in self.versions_data if v['name'] == selected_version_name), None)
        if version_data:
            self.manager.current_version = version_data['version']
            self.populate_books()

    def populate_books(self):
        """Busca os livros da Bíblia e preenche o menu de livros."""
        self.books_data = self.manager.load_books()
        book_menu = self.view["book_menu"]
        book_var = self.view["book_var"]

        if self.books_data:
            book_names = [book['name'] for book in self.books_data]
            book_menu.configure(values=book_names)
            if book_names:
                book_var.set(book_names[0])
                self.on_book_selected(book_names[0])
        else:
            book_menu.configure(values=["Erro ao carregar"])
            book_var.set("Erro ao carregar")
            self.view["chapter_menu"].configure(values=["-"])
            self.view["chapter_var"].set("-")

    def on_book_selected(self, selected_book_name):
        """Chamado quando um novo livro é selecionado. Popula os capítulos."""
        chapter_menu = self.view["chapter_menu"]
        chapter_var = self.view["chapter_var"]

        book_data = next((book for book in self.books_data if book['name'] == selected_book_name), None)
        if book_data:
            num_chapters = book_data.get('chapters', 0)
            chapter_values = [str(i) for i in range(1, num_chapters + 1)]
            if chapter_values:
                chapter_menu.configure(values=chapter_values)
                chapter_var.set(chapter_values[0])
            else:
                chapter_menu.configure(values=["N/A"])
                chapter_var.set("N/A")
        else:
            chapter_menu.configure(values=["Erro"])
            chapter_var.set("Erro")
    
    def load_verses(self):
        """
        Pega a seleção atual, busca os versículos através do manager e
        notifica o PresentationController para exibi-los.
        """
        version_name = self.view["version_var"].get()
        book_name = self.view["book_var"].get()
        chapter_str = self.view["chapter_var"].get()

        if not all([version_name, book_name, chapter_str]) or not chapter_str.isdigit():
            messagebox.showwarning("Seleção Inválida", "Por favor, selecione uma versão, livro e capítulo válidos.", parent=self.master)
            return

        version_data = next((v for v in self.versions_data if v['name'] == version_name), None)
        book_data = next((b for b in self.books_data if b['name'] == book_name), None)
        
        if not version_data or not book_data:
            messagebox.showerror("Erro de Dados", "Não foi possível encontrar os dados para a versão ou livro selecionado.", parent=self.master)
            return

        version_abbrev = version_data['version']
        book_abbrev_obj = book_data['abbrev']
        book_abbrev = book_abbrev_obj.get('pt', '') if isinstance(book_abbrev_obj, dict) else book_abbrev_obj
        chapter_num = int(chapter_str)

        slides = self.manager.get_verses_as_slides(version_abbrev, book_abbrev, chapter_num)
        
        if not slides:
            slides = [f"Nenhum versículo encontrado para\n{book_name} {chapter_num} ({version_name})"]

        self.on_content_selected("bible", slides)