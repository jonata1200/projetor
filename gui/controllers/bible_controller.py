import customtkinter as ctk
from tkinter import messagebox
import threading

class BibleController:
    def __init__(self, master, view_widgets, bible_manager, on_content_selected_callback, playlist_controller):
        self.master = master
        self.view = view_widgets
        self.manager = bible_manager
        self.on_content_selected = on_content_selected_callback
        self.playlist_controller = playlist_controller
        
        self.versions_data = []
        self.books_data = []

        self._setup_callbacks()
        # Inicia o carregamento das versões da Bíblia
        threading.Thread(target=self.populate_versions, daemon=True).start()

    def _setup_callbacks(self):
        self.view["version_menu"].configure(command=self.on_version_selected)
        self.view["book_menu"].configure(command=self.on_book_selected)
        self.view["btn_load"].configure(command=self.load_verses)
        self.view["btn_add_to_playlist"].configure(command=self.add_to_playlist)

    def populate_versions(self):
        versions = self.manager.load_versions()
        # Usa 'after' para garantir que a UI seja atualizada na thread principal
        self.master.after(0, self._update_version_menu, versions)

    def _update_version_menu(self, versions):
        self.versions_data = versions
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

    def on_version_selected(self, selected_version_name):
        version_data = next((v for v in self.versions_data if v['name'] == selected_version_name), None)
        if version_data:
            self.manager.current_version = version_data['version']
            self.populate_books()

    def populate_books(self):
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

    def on_book_selected(self, selected_book_name):
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
                chapter_menu.configure(values=["N/A"]); chapter_var.set("N/A")
        else:
            chapter_menu.configure(values=["Erro"]); chapter_var.set("Erro")
    
    def _get_and_process_verses(self, callback):
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
        title = f"{book_name} {chapter_num}"
        args = (version_abbrev, book_abbrev, chapter_num, title, version_name, callback)
        thread = threading.Thread(target=self._threaded_get_verses, args=args, daemon=True)
        thread.start()
        self.view["btn_load"].configure(state="disabled", text="Carregando...")
        self.view["btn_add_to_playlist"].configure(state="disabled")

    def _threaded_get_verses(self, version_abbrev, book_abbrev, chapter_num, title, version_name, callback):
        try:
            slides = self.manager.get_verses_as_slides(version_abbrev, book_abbrev, chapter_num)
            if not slides:
                slides = [f"Nenhum versículo encontrado para\n{title} ({version_name})"]
            self.master.after(0, callback, slides, title)
        except Exception as e:
            error_message = f"Erro ao buscar versículos: {e}"
            self.master.after(0, callback, None, title, error_message)

    def load_verses(self):
        self._get_and_process_verses(self._on_load_verses_finished)

    def _on_load_verses_finished(self, slides, title, error=None):
        self.view["btn_load"].configure(state="normal", text="Carregar e Visualizar")
        self.view["btn_add_to_playlist"].configure(state="normal")
        if error:
            messagebox.showerror("Erro de Rede", error, parent=self.master)
            return
        self.on_content_selected("bible", slides)

    def add_to_playlist(self):
        self._get_and_process_verses(self._on_add_to_playlist_finished)
    
    def _on_add_to_playlist_finished(self, slides, title, error=None):
        self.view["btn_load"].configure(state="normal", text="Carregar e Visualizar")
        self.view["btn_add_to_playlist"].configure(state="normal")
        if error:
            messagebox.showerror("Erro de Rede", error, parent=self.master)
            return
        self.playlist_controller.add_bible_item(slides, title)