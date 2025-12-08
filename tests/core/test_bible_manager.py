"""
Testes para o BibleManager.

Este módulo contém testes unitários para todas as funcionalidades do BibleManager.
"""

import pytest
from unittest.mock import patch, Mock
from pathlib import Path
import json
import tempfile

from core.bible_manager import BibleManager
from core.exceptions import BibleAPIError


class TestBibleManager:
    """Testes para a classe BibleManager."""
    
    def test_load_books_from_cache(self, sample_bible_data, tmp_path):
        """Testa carregar livros do cache."""
        cache_file = tmp_path / "bible_books_cache.json"
        cache_file.write_text(json.dumps([sample_bible_data]))
        
        with patch('core.bible_manager.BIBLE_BOOKS_CACHE_PATH', str(cache_file)):
            manager = BibleManager()
            manager.api_client = Mock()  # Mock do API client
            
            books = manager.load_books()
            
            assert len(books) == 1
            assert books[0]['name'] == "Gênesis"
            # Verificar que não chamou a API
            manager.api_client.get_books.assert_not_called()
    
    def test_load_books_from_api(self, sample_bible_data, tmp_path):
        """Testa carregar livros da API quando cache não existe."""
        cache_file = tmp_path / "bible_books_cache.json"
        # Cache não existe
        
        with patch('core.bible_manager.BIBLE_BOOKS_CACHE_PATH', str(cache_file)):
            manager = BibleManager()
            manager.api_client.get_books = Mock(return_value=[sample_bible_data])
            
            books = manager.load_books()
            
            assert len(books) == 1
            assert books[0]['name'] == "Gênesis"
            # Verificar que chamou a API
            manager.api_client.get_books.assert_called_once()
            # Verificar que cache foi criado
            assert cache_file.exists()
    
    def test_get_book_by_abbrev_pt(self, sample_bible_data, tmp_path):
        """Testa buscar livro por abreviação em português."""
        cache_file = tmp_path / "bible_books_cache.json"
        cache_file.write_text(json.dumps([sample_bible_data]))
        
        with patch('core.bible_manager.BIBLE_BOOKS_CACHE_PATH', str(cache_file)):
            manager = BibleManager()
            manager.load_books()
            
            book = manager.get_book_by_abbrev("gn")
            
            assert book is not None
            assert book['name'] == "Gênesis"
    
    def test_get_book_by_abbrev_en(self, sample_bible_data, tmp_path):
        """Testa buscar livro por abreviação em inglês."""
        cache_file = tmp_path / "bible_books_cache.json"
        cache_file.write_text(json.dumps([sample_bible_data]))
        
        with patch('core.bible_manager.BIBLE_BOOKS_CACHE_PATH', str(cache_file)):
            manager = BibleManager()
            manager.load_books()
            
            book = manager.get_book_by_abbrev("gen")
            
            assert book is not None
            assert book['name'] == "Gênesis"
    
    def test_get_book_by_abbrev_nonexistent(self, sample_bible_data, tmp_path):
        """Testa buscar livro por abreviação inexistente."""
        cache_file = tmp_path / "bible_books_cache.json"
        cache_file.write_text(json.dumps([sample_bible_data]))
        
        with patch('core.bible_manager.BIBLE_BOOKS_CACHE_PATH', str(cache_file)):
            manager = BibleManager()
            manager.load_books()
            
            book = manager.get_book_by_abbrev("xxx")
            
            assert book is None
    
    def test_load_versions(self, tmp_path):
        """Testa carregar versões."""
        with patch('core.bible_manager.BIBLE_BOOKS_CACHE_PATH', str(tmp_path / "cache.json")):
            manager = BibleManager()
            manager.api_client.get_versions = Mock(return_value=[
                {"version": "nvi", "name": "Nova Versão Internacional"}
            ])
            
            versions = manager.load_versions()
            
            assert len(versions) == 1
            assert versions[0]['version'] == "nvi"

