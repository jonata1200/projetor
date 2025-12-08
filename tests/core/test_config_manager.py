"""
Testes para o ConfigManager.

Este módulo contém testes unitários para todas as funcionalidades do ConfigManager.
"""

import pytest
from unittest.mock import patch
from pathlib import Path
import configparser
import tempfile

from core.config_manager import ConfigManager
from core.exceptions import ConfigSaveError


class TestConfigManager:
    """Testes para a classe ConfigManager."""
    
    def test_load_config_existing(self, tmp_path):
        """Testa carregar configuração existente."""
        config_file = tmp_path / "config.ini"
        config_content = """[Projection_Music]
font_size = 70
font_color = white
"""
        config_file.write_text(config_content, encoding='utf-8')
        
        with patch('core.config_manager.CONFIG_PATH', str(config_file)):
            manager = ConfigManager()
            
            value = manager.get_setting("Projection_Music", "font_size")
            assert value == "70"
    
    def test_load_config_create_default(self, tmp_path):
        """Testa criar configuração padrão se não existe."""
        config_file = tmp_path / "config.ini"
        # Arquivo não existe
        
        with patch('core.config_manager.CONFIG_PATH', str(config_file)):
            manager = ConfigManager()
            
            # Verificar que arquivo foi criado
            assert config_file.exists()
            
            # Verificar seções padrão
            assert manager.config.has_section("Projection_Music")
            assert manager.config.has_section("Projection_Bible")
            assert manager.config.has_section("Projection_Text")
    
    def test_set_and_get_setting(self, tmp_path):
        """Testa definir e obter configuração."""
        config_file = tmp_path / "config.ini"
        config_file.write_text("", encoding='utf-8')
        
        with patch('core.config_manager.CONFIG_PATH', str(config_file)):
            manager = ConfigManager()
            
            # Definir setting
            result = manager.set_setting("Projection_Music", "font_size", "80")
            assert result is True
            
            # Obter setting
            value = manager.get_setting("Projection_Music", "font_size")
            assert value == "80"
    
    def test_get_setting_with_fallback(self, tmp_path):
        """Testa obter setting inexistente com fallback."""
        config_file = tmp_path / "config.ini"
        config_file.write_text("", encoding='utf-8')
        
        with patch('core.config_manager.CONFIG_PATH', str(config_file)):
            manager = ConfigManager()
            
            value = manager.get_setting("Projection_Music", "nonexistent", fallback="default")
            assert value == "default"
    
    def test_get_int_setting(self, tmp_path):
        """Testa obter setting como inteiro."""
        config_file = tmp_path / "config.ini"
        config_content = """[Projection_Music]
font_size = 70
"""
        config_file.write_text(config_content, encoding='utf-8')
        
        with patch('core.config_manager.CONFIG_PATH', str(config_file)):
            manager = ConfigManager()
            
            value = manager.get_int_setting("Projection_Music", "font_size")
            assert value == 70
    
    def test_get_int_setting_fallback(self, tmp_path):
        """Testa obter setting inteiro inexistente com fallback."""
        config_file = tmp_path / "config.ini"
        config_file.write_text("", encoding='utf-8')
        
        with patch('core.config_manager.CONFIG_PATH', str(config_file)):
            manager = ConfigManager()
            
            value = manager.get_int_setting("Projection_Music", "nonexistent", fallback=60)
            assert value == 60

