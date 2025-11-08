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
        self.populate_versions()

    def _setup_callbacks(self):
        # Callbacks para navegação
        self.view["version_menu"].configure(command=self.on_version_selected)
        self.view["book_menu"].configure(command=self.on_book_selected)
        self.view["btn_load"].configure(command=self.load_verses)
        self.view["btn_add_to_playlist"].configure(command=self.add_to_playlist)
        
        # Callbacks para busca
        self.view["btn_search"].configure(command=self.perform_search)
        self.view["search_entry"].bind("<Return>", lambda event: self.perform_search())

    # --- Métodos de Busca (NOVOS) ---

    def perform_search(self):
        """Inicia a busca por palavra-chave em uma thread."""
        search_term = self.view["search_entry"].get().strip()
        if not search_term:
            messagebox.showwarning("Busca Inválida", "Por favor, digite um termo para buscar.", parent=self.master)
            return

        # --- INÍCIO DA CORREÇÃO: Pegar a versão selecionada ---
        version_name = self.view["version_var"].get()
        version_data = next((v for v in self.versions_data if v['name'] == version_name), None)
        
        if not version_data:
            messagebox.showerror("Erro de Versão", "Nenhuma versão da Bíblia selecionada ou encontrada.", parent=self.master)
            return
        version_abbrev = version_data['version']
        # --- FIM DA CORREÇÃO ---

        # Passa a versão para a thread
        thread = threading.Thread(target=self._threaded_search, args=(version_abbrev, search_term,), daemon=True)
        thread.start()
        
        self.view["btn_search"].configure(state="disabled", text="Buscando...")
        self._clear_search_results()
        loading_label = ctk.CTkLabel(self.view["results_frame"], text="Buscando, por favor aguarde...")
        loading_label.pack(pady=10)

    def _threaded_search(self, version_abbrev, term): # <-- Recebe version_abbrev
        """Executado em background. Busca os versículos e chama o callback."""
        try:
            # Passa a versão para o gerenciador
            results = self.manager.search_verses_as_slides(version_abbrev, term)
            self.master.after(0, self._on_search_finished, results)
        except Exception as e:
            self.master.after(0, self._on_search_finished, None, str(e))

    def _on_search_finished(self, results, error=None):
        """Executado na thread principal. Renderiza os resultados da busca."""
        self.view["btn_search"].configure(state="normal", text="Buscar")
        self._clear_search_results()

        if error:
            messagebox.showerror("Erro na Busca", f"Ocorreu um erro: {error}", parent=self.master)
            return
        
        if not results:
            no_results_label = ctk.CTkLabel(self.view["results_frame"], text="Nenhum resultado encontrado.")
            no_results_label.pack(pady=10)
            return
        
        for verse_text in results:
            # Limita o texto do botão para não ficar muito longo
            btn_text = verse_text.replace("\n", " ").strip()
            if len(btn_text) > 80:
                btn_text = btn_text[:77] + "..."
                
            result_button = ctk.CTkButton(
                self.view["results_frame"],
                text=btn_text,
                anchor="w",
                command=lambda text=verse_text: self._on_search_result_selected(text)
            )
            result_button.pack(fill="x", padx=5, pady=2)
            
    def _on_search_result_selected(self, verse_slide):
        """Carrega um único versículo do resultado da busca na projeção."""
        self.on_content_selected("bible", [verse_slide])

    def _clear_search_results(self):
        """Limpa todos os widgets do frame de resultados."""
        for widget in self.view["results_frame"].winfo_children():
            widget.destroy()

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
    
    def _get_and_process_verses(self, callback):
        """
        Lógica central para buscar versículos e chamar um callback com o resultado.
        Usa threading para não travar a UI.
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
        
        title = f"{book_name} {chapter_num}"
        args = (version_abbrev, book_abbrev, chapter_num, title, version_name, callback)

        thread = threading.Thread(target=self._threaded_get_verses, args=args, daemon=True)
        thread.start()

        self.view["btn_load"].configure(state="disabled", text="Carregando...")
        self.view["btn_add_to_playlist"].configure(state="disabled")

    def _threaded_get_verses(self, version_abbrev, book_abbrev, chapter_num, title, version_name, callback):
        """Busca os versículos em background."""
        try:
            slides = self.manager.get_verses_as_slides(version_abbrev, book_abbrev, chapter_num)
            if not slides:
                slides = [f"Nenhum versículo encontrado para\n{title} ({version_name})"]
            
            self.master.after(0, callback, slides, title)
        except Exception as e:
            error_message = f"Erro ao buscar versículos: {e}"
            self.master.after(0, callback, None, title, error_message)

    def load_verses(self):
        """Ação do botão 'Carregar e Visualizar'."""
        self._get_and_process_verses(self._on_load_verses_finished)

    def _on_load_verses_finished(self, slides, title, error=None):
        self.view["btn_load"].configure(state="normal", text="Carregar e Visualizar")
        self.view["btn_add_to_playlist"].configure(state="normal")
        if error:
            messagebox.showerror("Erro de Rede", error, parent=self.master)
            return
        self.on_content_selected("bible", slides)

    def add_to_playlist(self):
        """Ação do botão 'Adicionar à Ordem'."""
        self._get_and_process_verses(self._on_add_to_playlist_finished)

    def _on_add_to_playlist_finished(self, slides, title, error=None):
        self.view["btn_load"].configure(state="normal", text="Carregar e Visualizar")
        self.view["btn_add_to_playlist"].configure(state="normal")
        if error:
            messagebox.showerror("Erro de Rede", error, parent=self.master)
            return
        self.playlist_controller.add_bible_item(slides, title)

    def _threaded_load_verses(self, version_abbrev, book_abbrev, chapter_num, book_name, version_name):
        """
        Executado em segundo plano. Busca os versículos na API.
        """
        try:
            slides = self.manager.get_verses_as_slides(version_abbrev, book_abbrev, chapter_num)
            
            if not slides:
                # Cria uma mensagem de "não encontrado" para passar para a UI
                slides = [f"Nenhum versículo encontrado para\n{book_name} {chapter_num} ({version_name})"]
            
            # Agenda a atualização da UI na thread principal
            self.master.after(0, self._on_verses_loaded, slides)
        except Exception as e:
            # Se ocorrer um erro de rede, agenda a exibição do erro
            error_message = f"Erro ao buscar versículos: {e}"
            self.master.after(0, self._on_verses_loaded, None, error_message)

    def _on_verses_loaded(self, slides, error=None):
        """
        Executado de volta na thread principal. Atualiza a UI com os resultados.
        """
        # Sempre reabilita o botão
        self.view["btn_load"].configure(state="normal", text="Carregar Versículos")

        if error:
            messagebox.showerror("Erro de Rede", error, parent=self.master)
            return
        
        # Envia o conteúdo para o controlador de apresentação
        self.on_content_selected("bible", slides)