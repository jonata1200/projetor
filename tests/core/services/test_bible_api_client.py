"""
Testes para o BibleAPIClient.

Este módulo contém testes unitários para o cliente da API da Bíblia.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import requests
import json

from core.services.bible_api_client import BibleAPIClient
from core.exceptions import BibleAPIError


class TestBibleAPIClient:
    """Testes para a classe BibleAPIClient."""
    
    def test_get_versions(self):
        """Testa obter lista de versões."""
        client = BibleAPIClient()
        
        versions = client.get_versions()
        
        assert isinstance(versions, list)
        assert len(versions) > 0
        assert "version" in versions[0]
        assert "name" in versions[0]
    
    @patch('core.services.bible_api_client.requests.get')
    def test_get_books_success(self, mock_get):
        """Testa obter livros com sucesso."""
        # Mock de resposta bem-sucedida
        mock_response = Mock()
        mock_response.json.return_value = [
            {
                "abbrev": {"pt": "gn", "en": "gen"},
                "name": "Gênesis",
                "chapters": 50,
                "testament": "VT"
            }
        ]
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        client = BibleAPIClient()
        books = client.get_books()
        
        assert isinstance(books, list)
        assert len(books) > 0
        assert "name" in books[0]
        mock_get.assert_called_once()
    
    @patch('core.services.bible_api_client.requests.get')
    def test_make_request_network_error(self, mock_get):
        """Testa erro de rede na requisição."""
        # Mock de erro de rede
        mock_get.side_effect = requests.exceptions.RequestException("Network error")
        
        client = BibleAPIClient()
        
        with pytest.raises(BibleAPIError):
            client._make_request("/books")
    
    @patch('core.services.bible_api_client.requests.get')
    def test_make_request_json_error(self, mock_get):
        """Testa erro de JSON inválido na resposta."""
        # Mock de resposta inválida
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
        mock_get.return_value = mock_response
        
        client = BibleAPIClient()
        
        with pytest.raises(BibleAPIError):
            client._make_request("/books")
    
    @patch('core.services.bible_api_client.requests.get')
    def test_get_chapter_verses(self, mock_get):
        """Testa obter versículos de um capítulo."""
        # Mock de resposta bem-sucedida
        mock_response = Mock()
        mock_response.json.return_value = {
            "verses": [
                {"number": 1, "text": "No princípio criou Deus..."},
                {"number": 2, "text": "E a terra era sem forma..."}
            ]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        client = BibleAPIClient()
        verses = client.get_chapter_verses("nvi", "gn", 1)
        
        assert isinstance(verses, list)
        assert len(verses) == 2
        assert verses[0]["number"] == 1

