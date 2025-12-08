"""
Testes para o LetrasScraper.

Este módulo contém testes unitários para o scraper de letras de música.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import requests
from bs4 import BeautifulSoup

from core.services.letras_scraper import LetrasScraper
from core.exceptions import ScraperError, ScraperNetworkError, ScraperParseError, ValidationError


class TestLetrasScraper:
    """Testes para a classe LetrasScraper."""
    
    @patch('core.services.letras_scraper.requests.get')
    def test_fetch_lyrics_success(self, mock_get):
        """Testa buscar letra com sucesso."""
        # Mock de HTML válido
        html_content = """
        <html>
            <body>
                <div class="title-content">
                    <h1 class="textStyle-primary">Música Teste</h1>
                    <h2 class="textStyle-secondary"><a>Artista Teste</a></h2>
                </div>
                <div class="lyric-original">
                    <p>Primeira estrofe</p>
                    <p>Segunda estrofe</p>
                </div>
            </body>
        </html>
        """
        
        mock_response = Mock()
        mock_response.text = html_content
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        scraper = LetrasScraper()
        result = scraper.fetch_lyrics_from_url("https://www.letras.mus.br/artista/musica")
        
        assert result is not None
        assert result['title'] == "Música Teste"
        assert result['artist'] == "Artista Teste"
        assert 'lyrics_full' in result
        assert len(result['lyrics_full']) > 0
    
    @patch('core.services.letras_scraper.requests.get')
    def test_fetch_lyrics_network_error(self, mock_get):
        """Testa erro de rede ao buscar letra."""
        # Mock de erro de rede
        mock_get.side_effect = requests.exceptions.RequestException("Network error")
        
        scraper = LetrasScraper()
        
        with pytest.raises(ScraperNetworkError):
            scraper.fetch_lyrics_from_url("https://www.letras.mus.br/artista/musica")
    
    def test_fetch_lyrics_invalid_url(self):
        """Testa URL inválida."""
        scraper = LetrasScraper()
        
        with pytest.raises(ValidationError):
            scraper.fetch_lyrics_from_url("invalid-url")
    
    @patch('core.services.letras_scraper.requests.get')
    def test_fetch_lyrics_parse_error(self, mock_get):
        """Testa erro ao fazer parse do HTML."""
        # Mock de HTML sem elementos esperados
        html_content = "<html><body><p>Conteúdo sem estrutura esperada</p></body></html>"
        
        mock_response = Mock()
        mock_response.text = html_content
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        scraper = LetrasScraper()
        
        with pytest.raises(ScraperParseError):
            scraper.fetch_lyrics_from_url("https://www.letras.mus.br/artista/musica")

