import json
import os
# --- IMPORTAÇÕES MODIFICADAS ---
from .services.bible_api_client import BibleAPIClient
from core.paths import BIBLE_BOOKS_CACHE_PATH

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