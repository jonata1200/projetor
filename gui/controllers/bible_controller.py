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
        self.current_chapter_verses = []

        self._setup_callbacks()
        threading.Thread(target=self.populate_versions, daemon=True).start()

    def _setup_callbacks(self):
        self.view["version_menu"].configure(command=self.on_version_selected)
        self.view["book_menu"].configure(command=self.on_book_selected)
        self.view["chapter_menu"].configure(command=self.on_chapter_selected)
        self.view["btn_load"].configure(command=self.load_selected_content)
        self.view["btn_add_to_playlist"].configure(command=self.add_selected_content_to_playlist)

    def populate_versions(self):
        versions = self.manager.load_versions()
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

    def on_version_selected(self, selected_version_name):
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
                self.on_chapter_selected(chapter_values[0])
    
    def on_chapter_selected(self, chapter_num):
        self.view["verse_menu"].configure(state="disabled")
        self.view["verse_var"].set("Carregando...")
        version_abbrev = self._get_selected_abbrev('version')
        book_abbrev = self._get_selected_abbrev('book')
        if not all([version_abbrev, book_abbrev, chapter_num]): return
        args = (version_abbrev, book_abbrev, int(chapter_num))
        threading.Thread(target=self._threaded_fetch_verses_for_menu, args=args, daemon=True).start()

    def _threaded_fetch_verses_for_menu(self, version_abbrev, book_abbrev, chapter_num):
        self.current_chapter_verses = self.manager.api_client.get_chapter_verses(version_abbrev, book_abbrev, chapter_num)
        self.master.after(0, self._populate_verse_menu)

    def _populate_verse_menu(self):
        """Atualiza a UI, removendo a opção 'Todos os Versículos'."""
        verse_menu = self.view["verse_menu"]
        verse_var = self.view["verse_var"]
        
        if self.current_chapter_verses:
            # --- MUDANÇA AQUI ---
            # A lista agora contém apenas os números dos versículos.
            verse_numbers = [str(v['number']) for v in self.current_chapter_verses]
            verse_menu.configure(values=verse_numbers, state="normal")
            verse_var.set("1") # Continua definindo o versículo 1 como padrão.
        else:
            verse_menu.configure(values=["Nenhum"], state="disabled")
            verse_var.set("Nenhum")

    # --- MÉTODO _get_selected_content TOTALMENTE REESCRITO ---
    def _get_selected_content(self):
        """
        Sempre monta a lista de slides para o CAPÍTULO INTEIRO.
        Retorna os slides, o título do capítulo, e o ÍNDICE INICIAL do versículo selecionado.
        """
        book_name = self.view["book_var"].get()
        chapter_num = self.view["chapter_var"].get()
        selected_verse_str = self.view["verse_var"].get()
        
        slides = []
        start_index = 0
        title = f"{book_name} {chapter_num}"

        if not self.current_chapter_verses:
            return None, None, 0

        # Monta a lista de slides para o capítulo inteiro
        for verse in self.current_chapter_verses:
            slides.append(f"{book_name} {chapter_num}:{verse['number']}\n{verse['text']}")

        # Encontra o índice inicial do versículo selecionado
        if selected_verse_str.isdigit():
            try:
                # O índice é o número do versículo - 1 (pois listas começam em 0)
                verse_num = int(selected_verse_str)
                start_index = verse_num - 1
            except ValueError:
                start_index = 0
        
        # Garante que o índice seja válido
        if not (0 <= start_index < len(slides)):
            start_index = 0
            
        return slides, title, start_index

    # --- Métodos de Ação Atualizados ---
    def load_selected_content(self):
        """Carrega o capítulo inteiro, iniciando no versículo selecionado."""
        slides, _, start_index = self._get_selected_content()
        if slides:
            # Passa o novo parâmetro 'start_index' para o PresentationController
            self.on_content_selected("bible", slides, start_index=start_index)

    def add_selected_content_to_playlist(self):
        """Adiciona o capítulo inteiro à Ordem de Culto."""
        # A playlist sempre recebe o capítulo inteiro. O start_index não é necessário aqui.
        slides, title, _ = self._get_selected_content()
        if slides and title:
            self.playlist_controller.add_bible_item(slides, title)

    # --- Método Auxiliar ---
    def _get_selected_abbrev(self, item_type):
        """Pega a abreviação da versão ou livro selecionado."""
        if item_type == 'version':
            name = self.view["version_var"].get()
            data_list = self.versions_data
            key = 'version'
            data = next((v for v in data_list if v['name'] == name), None)
            return data[key] if data else None
        elif item_type == 'book':
            name = self.view["book_var"].get()
            data_list = self.books_data
            key = 'abbrev'
            data = next((b for b in data_list if b['name'] == name), None)
            if data:
                abbrev_obj = data[key]
                return abbrev_obj.get('pt', '') if isinstance(abbrev_obj, dict) else abbrev_obj
        return None