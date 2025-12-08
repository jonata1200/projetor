"""
Configuração compartilhada para todos os testes.

Este módulo contém fixtures e configurações comuns usadas em todos os testes.
"""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, MagicMock
from typing import Dict, Any


@pytest.fixture
def sample_music_data() -> Dict[str, Any]:
    """
    Retorna dados de exemplo de uma música para testes.
    
    Returns:
        Dict com dados completos de uma música de exemplo
    """
    return {
        "id": "test-music-id-123",
        "title": "Música de Teste",
        "artist": "Artista de Teste",
        "lyrics_full": "Primeira estrofe\n\nSegunda estrofe\n\nTerceira estrofe",
        "slides": [
            "Primeira estrofe",
            "Segunda estrofe",
            "Terceira estrofe"
        ]
    }


@pytest.fixture
def sample_bible_data() -> Dict[str, Any]:
    """
    Retorna dados de exemplo de um livro bíblico para testes.
    
    Returns:
        Dict com dados completos de um livro bíblico de exemplo
    """
    return {
        "abbrev": {
            "pt": "gn",
            "en": "gen"
        },
        "name": "Gênesis",
        "chapters": 50,
        "testament": "VT"
    }


@pytest.fixture
def mock_config_manager():
    """
    Cria um mock do ConfigManager para testes.
    
    Returns:
        Mock configurado do ConfigManager
    """
    mock = Mock()
    mock.get_setting.return_value = "default_value"
    mock.get_int_setting.return_value = 60
    mock.set_setting.return_value = True
    mock._save_config_file.return_value = True
    
    # Configurações padrão
    mock.get_setting.side_effect = lambda section, key, fallback=None: {
        ("Projection_Music", "font_size"): "70",
        ("Projection_Music", "font_color"): "white",
        ("Projection_Music", "bg_color"): "black",
        ("Projection_Bible", "font_size"): "60",
        ("Projection_Bible", "font_color"): "#FFFFE0",
        ("Projection_Bible", "bg_color"): "#000033",
    }.get((section, key), fallback)
    
    return mock


@pytest.fixture
def mock_api_client():
    """
    Cria um mock do BibleAPIClient para testes.
    
    Returns:
        Mock configurado do BibleAPIClient
    """
    mock = Mock()
    
    # Mock de get_versions
    mock.get_versions.return_value = [
        {"version": "nvi", "name": "Nova Versão Internacional"},
        {"version": "acf", "name": "Almeida Corrigida Fiel"}
    ]
    
    # Mock de get_books
    mock.get_books.return_value = [
        {
            "abbrev": {"pt": "gn", "en": "gen"},
            "name": "Gênesis",
            "chapters": 50,
            "testament": "VT"
        },
        {
            "abbrev": {"pt": "ex", "en": "exo"},
            "name": "Êxodo",
            "chapters": 40,
            "testament": "VT"
        }
    ]
    
    # Mock de get_chapter_verses
    mock.get_chapter_verses.return_value = [
        {"number": 1, "text": "No princípio criou Deus os céus e a terra."},
        {"number": 2, "text": "E a terra era sem forma e vazia..."}
    ]
    
    return mock


@pytest.fixture
def temp_music_db(tmp_path):
    """
    Cria um arquivo temporário para o banco de dados de músicas.
    
    Args:
        tmp_path: Fixture do pytest que cria diretório temporário
    
    Yields:
        Path para o arquivo temporário de música
    """
    db_file = tmp_path / "music_db.json"
    db_file.write_text("[]")  # Inicializa com lista vazia
    
    yield db_file
    
    # Limpeza após teste (pytest faz isso automaticamente, mas é bom documentar)
    if db_file.exists():
        db_file.unlink()


@pytest.fixture
def temp_config_file(tmp_path):
    """
    Cria um arquivo temporário para configuração.
    
    Args:
        tmp_path: Fixture do pytest que cria diretório temporário
    
    Yields:
        Path para o arquivo temporário de configuração
    """
    config_file = tmp_path / "config.ini"
    
    # Cria config padrão
    config_content = """[Projection_Music]
font_size = 70
font_color = white
bg_color = black

[Projection_Bible]
font_size = 60
font_color = #FFFFE0
bg_color = #000033

[Projection_Text]
font_size = 65
font_color = white
bg_color = black
"""
    config_file.write_text(config_content, encoding='utf-8')
    
    yield config_file
    
    # Limpeza após teste
    if config_file.exists():
        config_file.unlink()


@pytest.fixture
def temp_bible_cache(tmp_path):
    """
    Cria um arquivo temporário para o cache de livros da Bíblia.
    
    Args:
        tmp_path: Fixture do pytest que cria diretório temporário
    
    Yields:
        Path para o arquivo temporário de cache
    """
    cache_file = tmp_path / "bible_books_cache.json"
    cache_file.write_text("[]")  # Inicializa com lista vazia
    
    yield cache_file
    
    # Limpeza após teste
    if cache_file.exists():
        cache_file.unlink()

