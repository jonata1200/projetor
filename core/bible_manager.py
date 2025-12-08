import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
# --- IMPORTAÇÕES MODIFICADAS ---
from .services.bible_api_client import BibleAPIClient
from core.paths import BIBLE_BOOKS_CACHE_PATH
from core.exceptions import MusicDatabaseError
from core.utils.file_utils import save_json_file, load_json_file

logger = logging.getLogger(__name__)

class BibleManager:
    """
    Gerenciador de acesso à Bíblia.
    
    Responsável por carregar livros bíblicos, buscar versículos e gerenciar
    cache local. Utiliza índice O(1) para busca por abreviação.
    
    Attributes:
        api_client: Cliente para API da Bíblia Digital
        versions: Lista de versões bíblicas disponíveis
        books: Lista de livros bíblicos carregados
        current_version: Versão bíblica atual selecionada
        _books_by_abbrev: Índice mapeando abreviação → livro (busca O(1))
    """
    def __init__(self) -> None:
        """
        Inicializa o BibleManager com cliente de API e estruturas vazias.
        """
        self.api_client = BibleAPIClient()
        self.versions: List[Dict] = []
        self.books: List[Dict] = []
        self.current_version: Optional[str] = None
        # Índice para busca O(1) por abreviação
        self._books_by_abbrev: Dict[str, Dict] = {}  # abreviação → livro

    def _save_books_to_cache(self, books_data: List[Dict]) -> None:
        """Salva a lista de livros em um arquivo JSON local."""
        save_json_file(Path(BIBLE_BOOKS_CACHE_PATH), books_data, ensure_ascii=False)
        logger.info("Lista de livros salva no cache local.")

    def _rebuild_abbrev_index(self) -> None:
        """
        Reconstrói o índice de busca O(1) por abreviação.
        
        Constrói _books_by_abbrev mapeando abreviação → livro.
        Lida com diferentes formatos de abreviação (dict ou str).
        """
        self._books_by_abbrev.clear()
        
        for book in self.books:
            abbrev = book.get('abbrev')
            if not abbrev:
                continue
            
            # Lidar com diferentes formatos de abreviação
            if isinstance(abbrev, dict):
                # Se for dict, indexar por 'pt' e 'en'
                pt_abbrev = abbrev.get('pt')
                en_abbrev = abbrev.get('en')
                if pt_abbrev:
                    self._books_by_abbrev[pt_abbrev] = book
                if en_abbrev:
                    self._books_by_abbrev[en_abbrev] = book
            elif isinstance(abbrev, str):
                # Se for string, indexar diretamente
                self._books_by_abbrev[abbrev] = book

    def load_versions(self) -> List[Dict]:
        self.versions = self.api_client.get_versions()
        return self.versions

    def load_books(self) -> List[Dict]:
        """
        Carrega os livros da Bíblia, priorizando o cache local.
        Se o cache não existir, busca na API e cria o cache.
        Reconstrói o índice de abreviações após carregar.
        """
        # Se os livros já estão na memória, não faz nada.
        if self.books:
            return self.books

        # Tenta carregar do arquivo de cache primeiro.
        cached_books = load_json_file(Path(BIBLE_BOOKS_CACHE_PATH), default=None)
        if cached_books is not None and cached_books:
            self.books = cached_books
            logger.info("Lista de livros carregada do cache.")
            # Reconstruir índice após carregar
            self._rebuild_abbrev_index()
            return self.books
        
        # Se o cache não existe ou falhou, busca na API.
        logger.info("Cache não encontrado. Buscando lista de livros da API.")
        try:
            self.books = self.api_client.get_books()
            # Se a busca na API foi bem-sucedida, salva no cache para a próxima vez.
            if self.books:
                self._save_books_to_cache(self.books)
                # Reconstruir índice após carregar
                self._rebuild_abbrev_index()
        except Exception as e:
            logger.error("Erro ao buscar livros da API", exc_info=True)
            # Se falhar, retorna lista vazia ao invés de levantar exceção
            # para não quebrar a aplicação se a API estiver indisponível
            self.books = []
        
        return self.books
    
    def get_book_by_abbrev(self, abbrev: str) -> Optional[Dict]:
        """
        Busca um livro da Bíblia por abreviação usando índice O(1).
        
        Args:
            abbrev: Abreviação do livro (pode ser pt ou en)
        
        Returns:
            Dict com dados do livro ou None se não encontrado
        """
        if not self.books:
            self.load_books()
        
        # Se índice não foi construído, reconstruir
        if not self._books_by_abbrev:
            self._rebuild_abbrev_index()
        
        # Busca O(1) no índice
        return self._books_by_abbrev.get(abbrev)