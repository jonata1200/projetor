import threading
import logging
import time
from tkinter import messagebox
from core.exceptions import BibleAPIError, ValidationError

logger = logging.getLogger(__name__)

class BibleController:
    def __init__(self, master, view_widgets, bible_manager, on_content_selected_callback, playlist_controller):
        self.master = master
        self.view = view_widgets
        self.manager = bible_manager
        self.on_content_selected = on_content_selected_callback
        self.playlist_controller = playlist_controller
        
        self.versions_data = []
        self.books_data = []
        # Armazena os versículos do capítulo atualmente selecionado para evitar chamadas repetidas à API
        self.current_chapter_verses = []

        self._setup_callbacks()
        # Inicia o carregamento das versões da Bíblia em uma thread separada para não travar a UI
        # Usa after() para garantir que a thread seja criada após a janela estar totalmente inicializada
        self.master.after(100, lambda: threading.Thread(target=self.populate_versions, daemon=True).start())

    def _setup_callbacks(self):
        self.view["version_menu"].configure(command=self.on_version_selected)
        self.view["book_menu"].configure(command=self.on_book_selected)
        self.view["chapter_menu"].configure(command=self.on_chapter_selected)
        # O seletor de versículo não precisa de um 'command', pois sua seleção é lida no momento do clique nos botões.
        self.view["btn_load"].configure(command=self.load_selected_content)
        self.view["btn_add_to_playlist"].configure(command=self.add_selected_content_to_playlist)

    def populate_versions(self):
        versions = self.manager.load_versions()
        # Tenta atualizar a UI na thread principal
        # Se o loop principal ainda não estiver rodando, tenta novamente após um delay
        try:
            self.master.after(0, self._update_version_menu, versions)
        except RuntimeError:
            # Se o loop principal ainda não estiver ativo, aguarda um pouco e tenta novamente
            time.sleep(0.1)
            try:
                self.master.after(0, self._update_version_menu, versions)
            except RuntimeError:
                # Se ainda falhar, agenda após um delay maior usando after_idle quando disponível
                logger.warning("Não foi possível agendar atualização de versões imediatamente. Tentando novamente...")
                # Tenta novamente após mais tempo
                threading.Timer(0.5, lambda: self._safe_update_versions(versions)).start()
    
    def _safe_update_versions(self, versions):
        """Método auxiliar para tentar atualizar as versões de forma segura."""
        try:
            if hasattr(self.master, 'winfo_exists') and self.master.winfo_exists():
                self.master.after(0, self._update_version_menu, versions)
        except RuntimeError:
            logger.error("Falha ao atualizar menu de versões da Bíblia após várias tentativas")

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
        # Quando uma versão é selecionada, o próximo passo é popular os livros
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
        # Ação ao selecionar um capítulo: buscar os versículos para popular o menu de versículos
        self.view["verse_menu"].configure(state="disabled")
        self.view["verse_var"].set("Carregando...")
        version_abbrev = self._get_selected_abbrev('version')
        book_abbrev = self._get_selected_abbrev('book')
        if not all([version_abbrev, book_abbrev, chapter_num]): return
        
        args = (version_abbrev, book_abbrev, int(chapter_num))
        threading.Thread(target=self._threaded_fetch_verses_for_menu, args=args, daemon=True).start()

    def _threaded_fetch_verses_for_menu(self, version_abbrev, book_abbrev, chapter_num):
        # Busca os dados em uma thread
        try:
            verses_data = self.manager.api_client.get_chapter_verses(version_abbrev, book_abbrev, chapter_num)
            # Atualiza a UI na thread principal de forma segura
            self._safe_after(0, self._populate_verse_menu, verses_data)
        except BibleAPIError as e:
            logger.error(f"Erro ao buscar versículos - versão: {version_abbrev}, livro: {book_abbrev}, capítulo: {chapter_num}", exc_info=True)
            # Atualiza a UI para mostrar erro
            self._safe_after(0, self._populate_verse_menu, None, str(e))
    
    def _safe_after(self, delay_ms, callback, *args):
        """Executa after() de forma segura, lidando com RuntimeError se o loop principal não estiver ativo."""
        try:
            self.master.after(delay_ms, callback, *args)
        except RuntimeError:
            # Se o loop principal não estiver ativo, aguarda um pouco e tenta novamente
            time.sleep(0.1)
            try:
                self.master.after(delay_ms, callback, *args)
            except RuntimeError:
                logger.warning(f"Não foi possível agendar callback {callback.__name__}. Tentando novamente após delay...")
                threading.Timer(0.5, lambda: self._safe_after(delay_ms, callback, *args)).start()

    def _populate_verse_menu(self, verses_data, error_message=None):
        from tkinter import messagebox
        
        if error_message:
            messagebox.showerror("Erro ao Carregar Versículos",
                                f"Não foi possível carregar os versículos da API.\n\n"
                                f"Detalhes: {error_message}",
                                parent=self.master)
            verses_data = []
        
        self.current_chapter_verses = verses_data or [] # Armazena os versículos carregados
        verse_menu = self.view["verse_menu"]
        verse_var = self.view["verse_var"]
        
        if self.current_chapter_verses:
            verse_numbers = [str(v['number']) for v in self.current_chapter_verses]
            verse_menu.configure(values=verse_numbers, state="normal")
            verse_var.set("1") # Define o versículo 1 como padrão
        else:
            verse_menu.configure(values=["Nenhum"], state="disabled")
            verse_var.set("Nenhum")

    # --- MÉTODO CENTRAL DA MELHORIA ---
    def _get_selected_content(self):
        """
        Monta a lista de slides para o CAPÍTULO INTEIRO.
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

        # 1. Monta a lista de slides para o capítulo inteiro
        for verse in self.current_chapter_verses:
            slides.append(f"{book_name} {chapter_num}:{verse['number']}\n{verse['text']}")

        # 2. Encontra o índice inicial do versículo selecionado
        if selected_verse_str.isdigit():
            try:
                # O índice da lista é o número do versículo - 1
                verse_num = int(selected_verse_str)
                start_index = verse_num - 1
            except ValueError:
                start_index = 0
        
        # 3. Garante que o índice seja válido
        if not (0 <= start_index < len(slides)):
            start_index = 0
            
        return slides, title, start_index

    def load_selected_content(self):
        """
        Carrega o capítulo inteiro na pré-visualização, mas inicia a projeção
        a partir do versículo que o usuário selecionou.
        """
        # Validar seleções antes de processar (Fail Fast)
        version_name = self.view["version_var"].get()
        book_name = self.view["book_var"].get()
        chapter_num = self.view["chapter_var"].get()
        
        if not version_name or version_name == "Nenhum":
            messagebox.showwarning("Seleção Incompleta", "Por favor, selecione uma versão da Bíblia.", parent=self.master)
            return
        
        if not book_name or book_name == "Nenhum":
            messagebox.showwarning("Seleção Incompleta", "Por favor, selecione um livro da Bíblia.", parent=self.master)
            return
        
        if not chapter_num or chapter_num == "Nenhum":
            messagebox.showwarning("Seleção Incompleta", "Por favor, selecione um capítulo.", parent=self.master)
            return
        
        slides, _, start_index = self._get_selected_content()
        if slides:
            # A mágica acontece aqui: passamos o 'start_index' para o PresentationController
            self.on_content_selected("bible", slides, start_index=start_index)
        else:
            messagebox.showwarning("Sem Conteúdo", "Não foi possível carregar os versículos selecionados.", parent=self.master)

    def add_selected_content_to_playlist(self):
        """
        Adiciona o capítulo inteiro à Ordem de Culto, ignorando qual
        versículo individual foi selecionado.
        """
        slides, title, _ = self._get_selected_content() # O start_index é ignorado aqui
        if slides and title:
            self.playlist_controller.add_bible_item(slides, title)

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
                abbrev_obj = data.get(key)
                # Lida com o formato de abreviação que pode ser um dict ou uma string
                return abbrev_obj.get('pt', abbrev_obj) if isinstance(abbrev_obj, dict) else abbrev_obj
        return None