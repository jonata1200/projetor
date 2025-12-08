"""
Testes para o MusicManager.

Este módulo contém testes unitários para todas as funcionalidades do MusicManager.
"""

import pytest
from unittest.mock import patch, mock_open
from pathlib import Path
import json
import tempfile
import os

from core.music_manager import MusicManager
from core.exceptions import MusicDatabaseError, ValidationError


class TestMusicManager:
    """Testes para a classe MusicManager."""
    
    def test_add_music_success(self, sample_music_data, tmp_path):
        """Testa adicionar uma música válida."""
        # Mock do caminho do arquivo
        db_file = tmp_path / "music_db.json"
        db_file.write_text("[]")
        
        with patch('core.music_manager.MUSIC_DB_PATH', str(db_file)):
            manager = MusicManager()
            
            result = manager.add_music(
                title="Nova Música",
                artist="Novo Artista",
                lyrics_full="Estrofe 1\n\nEstrofe 2"
            )
            
            assert result is not None
            assert result['title'] == "Nova Música"
            assert result['artist'] == "Novo Artista"
            assert 'id' in result
            assert 'slides' in result
            assert len(result['slides']) == 2
    
    def test_add_music_invalid_title(self, tmp_path):
        """Testa adicionar música com título vazio."""
        db_file = tmp_path / "music_db.json"
        db_file.write_text("[]")
        
        with patch('core.music_manager.MUSIC_DB_PATH', str(db_file)):
            manager = MusicManager()
            
            with pytest.raises(ValidationError):
                manager.add_music("", "Artista", "Letra")
    
    def test_add_music_invalid_artist(self, tmp_path):
        """Testa adicionar música com artista vazio."""
        db_file = tmp_path / "music_db.json"
        db_file.write_text("[]")
        
        with patch('core.music_manager.MUSIC_DB_PATH', str(db_file)):
            manager = MusicManager()
            
            with pytest.raises(ValidationError):
                manager.add_music("Título", "", "Letra")
    
    def test_add_music_invalid_lyrics(self, tmp_path):
        """Testa adicionar música com letra vazia."""
        db_file = tmp_path / "music_db.json"
        db_file.write_text("[]")
        
        with patch('core.music_manager.MUSIC_DB_PATH', str(db_file)):
            manager = MusicManager()
            
            with pytest.raises(ValidationError):
                manager.add_music("Título", "Artista", "")
    
    def test_get_music_by_id_existing(self, sample_music_data, tmp_path):
        """Testa buscar música existente por ID."""
        db_file = tmp_path / "music_db.json"
        db_file.write_text(json.dumps([sample_music_data]))
        
        with patch('core.music_manager.MUSIC_DB_PATH', str(db_file)):
            manager = MusicManager()
            
            result = manager.get_music_by_id("test-music-id-123")
            
            assert result is not None
            assert result['title'] == "Música de Teste"
            assert result['id'] == "test-music-id-123"
    
    def test_get_music_by_id_nonexistent(self, tmp_path):
        """Testa buscar música inexistente por ID."""
        db_file = tmp_path / "music_db.json"
        db_file.write_text("[]")
        
        with patch('core.music_manager.MUSIC_DB_PATH', str(db_file)):
            manager = MusicManager()
            
            result = manager.get_music_by_id("nonexistent-id")
            
            assert result is None
    
    def test_is_duplicate_true(self, sample_music_data, tmp_path):
        """Testa verificação de duplicata quando existe."""
        db_file = tmp_path / "music_db.json"
        db_file.write_text(json.dumps([sample_music_data]))
        
        with patch('core.music_manager.MUSIC_DB_PATH', str(db_file)):
            manager = MusicManager()
            
            # Mesmo título e artista (case insensitive)
            assert manager.is_duplicate("Música de Teste", "Artista de Teste") is True
            assert manager.is_duplicate("música de teste", "artista de teste") is True
    
    def test_is_duplicate_false(self, sample_music_data, tmp_path):
        """Testa verificação de duplicata quando não existe."""
        db_file = tmp_path / "music_db.json"
        db_file.write_text(json.dumps([sample_music_data]))
        
        with patch('core.music_manager.MUSIC_DB_PATH', str(db_file)):
            manager = MusicManager()
            
            # Título ou artista diferente
            assert manager.is_duplicate("Outra Música", "Artista de Teste") is False
            assert manager.is_duplicate("Música de Teste", "Outro Artista") is False
    
    def test_edit_music_success(self, sample_music_data, tmp_path):
        """Testa editar música existente."""
        db_file = tmp_path / "music_db.json"
        db_file.write_text(json.dumps([sample_music_data]))
        
        with patch('core.music_manager.MUSIC_DB_PATH', str(db_file)):
            manager = MusicManager()
            
            result = manager.edit_music(
                song_id="test-music-id-123",
                new_title="Título Editado",
                new_artist="Artista Editado",
                new_lyrics_full="Nova letra\n\nSegunda estrofe"
            )
            
            assert result is True
            music = manager.get_music_by_id("test-music-id-123")
            assert music['title'] == "Título Editado"
            assert music['artist'] == "Artista Editado"
    
    def test_edit_music_nonexistent(self, tmp_path):
        """Testa editar música inexistente."""
        db_file = tmp_path / "music_db.json"
        db_file.write_text("[]")
        
        with patch('core.music_manager.MUSIC_DB_PATH', str(db_file)):
            manager = MusicManager()
            
            result = manager.edit_music(
                song_id="nonexistent-id",
                new_title="Título",
                new_artist="Artista",
                new_lyrics_full="Letra"
            )
            
            assert result is False
    
    def test_delete_music_success(self, sample_music_data, tmp_path):
        """Testa deletar música existente."""
        db_file = tmp_path / "music_db.json"
        db_file.write_text(json.dumps([sample_music_data]))
        
        with patch('core.music_manager.MUSIC_DB_PATH', str(db_file)):
            manager = MusicManager()
            
            result = manager.delete_music("test-music-id-123")
            
            assert result is True
            assert manager.get_music_by_id("test-music-id-123") is None
    
    def test_delete_music_nonexistent(self, tmp_path):
        """Testa deletar música inexistente."""
        db_file = tmp_path / "music_db.json"
        db_file.write_text("[]")
        
        with patch('core.music_manager.MUSIC_DB_PATH', str(db_file)):
            manager = MusicManager()
            
            result = manager.delete_music("nonexistent-id")
            
            assert result is False
    
    def test_save_and_load_database(self, tmp_path):
        """Testa salvar e carregar banco de dados."""
        db_file = tmp_path / "music_db.json"
        db_file.write_text("[]")
        
        with patch('core.music_manager.MUSIC_DB_PATH', str(db_file)):
            # Criar primeiro manager e adicionar música
            manager1 = MusicManager()
            manager1.add_music("Música 1", "Artista 1", "Letra 1")
            manager1.add_music("Música 2", "Artista 2", "Letra 2")
            
            # Criar segundo manager e carregar
            manager2 = MusicManager()
            
            assert len(manager2.music_database) == 2
            assert manager2.get_music_by_id(manager1.music_database[0]['id']) is not None
    
    def test_get_all_music_titles_with_artists(self, sample_music_data, tmp_path):
        """Testa obter lista de títulos com artistas."""
        db_file = tmp_path / "music_db.json"
        db_file.write_text(json.dumps([sample_music_data]))
        
        with patch('core.music_manager.MUSIC_DB_PATH', str(db_file)):
            manager = MusicManager()
            
            result = manager.get_all_music_titles_with_artists()
            
            assert len(result) == 1
            assert result[0][0] == "test-music-id-123"
            assert "Música de Teste" in result[0][1]
            assert "Artista de Teste" in result[0][1]
    
    def test_get_lyrics_slides(self, sample_music_data, tmp_path):
        """Testa obter slides de uma música."""
        db_file = tmp_path / "music_db.json"
        db_file.write_text(json.dumps([sample_music_data]))
        
        with patch('core.music_manager.MUSIC_DB_PATH', str(db_file)):
            manager = MusicManager()
            
            slides = manager.get_lyrics_slides("test-music-id-123")
            
            assert len(slides) == 3
            assert "Primeira estrofe" in slides
    
    def test_get_lyrics_slides_nonexistent(self, tmp_path):
        """Testa obter slides de música inexistente."""
        db_file = tmp_path / "music_db.json"
        db_file.write_text("[]")
        
        with patch('core.music_manager.MUSIC_DB_PATH', str(db_file)):
            manager = MusicManager()
            
            slides = manager.get_lyrics_slides("nonexistent-id")
            
            assert slides == []

