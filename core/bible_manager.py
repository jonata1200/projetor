import json
import os
from services.bible_api_client import BibleAPIClient

# --- NOVAS CONSTANTES ---
# Define o caminho base do projeto para encontrar a pasta 'data'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Define o caminho para o nosso novo arquivo de cache
BIBLE_BOOKS_CACHE_PATH = os.path.join(BASE_DIR, 'data', 'bible_books_cache.json')

class BibleManager:
    def __init__(self):
        self.api_client = BibleAPIClient()
        self.versions = []
        self.books = []
        self.current_version = None

    def _save_books_to_cache(self, books_data):
        """Salva a lista de livros em um arquivo JSON local."""
        try:
            # Garante que o diretório 'data' exista
            os.makedirs(os.path.dirname(BIBLE_BOOKS_CACHE_PATH), exist_ok=True)
            with open(BIBLE_BOOKS_CACHE_PATH, 'w', encoding='utf-8') as f:
                json.dump(books_data, f, ensure_ascii=False, indent=2)
            print("INFO: BibleManager - Lista de livros salva no cache local.")
        except IOError as e:
            print(f"ERRO: BibleManager - Falha ao salvar cache dos livros: {e}")

    def load_versions(self):
        self.versions = self.api_client.get_versions()
        return self.versions

    def load_books(self):
        """
        Carrega os livros da Bíblia, priorizando o cache local.
        Se o cache não existir, busca na API e cria o cache.
        """
        # Se os livros já estão na memória, não faz nada.
        if self.books:
            return self.books

        # Tenta carregar do arquivo de cache primeiro.
        if os.path.exists(BIBLE_BOOKS_CACHE_PATH):
            try:
                with open(BIBLE_BOOKS_CACHE_PATH, 'r', encoding='utf-8') as f:
                    self.books = json.load(f)
                    print("INFO: BibleManager - Lista de livros carregada do cache.")
                    return self.books
            except (json.JSONDecodeError, IOError) as e:
                print(f"AVISO: BibleManager - Cache de livros corrompido ou ilegível ({e}). Buscando da API.")
        
        # Se o cache não existe ou falhou, busca na API.
        print("INFO: BibleManager - Cache não encontrado. Buscando lista de livros da API.")
        self.books = self.api_client.get_books()
        
        # Se a busca na API foi bem-sucedida, salva no cache para a próxima vez.
        if self.books:
            self._save_books_to_cache(self.books)
        
        return self.books
    
    def get_book_by_abbrev(self, abbrev):
        if not self.books: self.load_books()
        for book in self.books:
            current_book_abbrev = book.get('abbrev')
            # Lógica para lidar com diferentes formatos de abreviação
            if isinstance(current_book_abbrev, dict):
                if current_book_abbrev.get('pt') == abbrev or current_book_abbrev.get('en') == abbrev:
                    return book
            elif isinstance(current_book_abbrev, str):
                if current_book_abbrev == abbrev:
                    return book
        return None

    def get_verses_as_slides(self, version_abbrev, book_abbrev, chapter_number):
        """
        Retorna os versículos de um capítulo como uma lista de strings (slides).
        """
        verses_data = self.api_client.get_chapter_verses(version_abbrev, book_abbrev, chapter_number)
        slides = []
        if verses_data:
            book_name = book_abbrev.upper()
            
            # Garante que os livros foram carregados para obter o nome completo
            found_book = self.get_book_by_abbrev(book_abbrev)
            if found_book:
                book_name = found_book.get("name", book_name)

            for verse in verses_data:
                slide_text = f"{book_name} {chapter_number}:{verse['number']}\n{verse['text']}"
                slides.append(slide_text)
        return slides

# O bloco de teste abaixo não precisa ser alterado.
if __name__ == '__main__':
    manager = BibleManager()
    
    versions = manager.load_versions()
    if versions:
        for v in versions:
            print(f"{v['name']} ({v['version']})")
        selected_version = versions[0]['version']
    else:
        print("Nenhuma versão carregada.")
        selected_version = "nvi"

    books = manager.load_books()
    if books:
        for i, book in enumerate(books[:3]):
             current_book_abbrev = book.get('abbrev')
             abbrev_display = current_book_abbrev.get('pt') if isinstance(current_book_abbrev, dict) else current_book_abbrev
             print(f"{book['name']} ({abbrev_display})")
        
        if books:
            selected_book_data = books[0]
            selected_book_abbrev_obj = selected_book_data['abbrev']
            selected_book_abbrev = selected_book_abbrev_obj.get('pt') if isinstance(selected_book_abbrev_obj, dict) else selected_book_abbrev_obj
            chapter_to_load = 1

            print(f"\n--- Slides de {selected_book_data['name']} Cap. {chapter_to_load} ({selected_version}) ---")
            slides = manager.get_verses_as_slides(selected_version, selected_book_abbrev, chapter_to_load)
            if slides:
                for i, slide in enumerate(slides[:2]):
                    print(f"Slide {i+1}:\n{slide}\n")
            else:
                print("Nenhum slide de versículo encontrado.")
    else:
        print("Nenhum livro carregado.")