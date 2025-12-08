import configparser
import os
import logging
from typing import Optional, Any
# --- IMPORTAÇÃO MODIFICADA ---
from core.paths import CONFIG_PATH
from core.exceptions import ConfigSaveError, ValidationError
from core.validators import validate_font_size, validate_color

logger = logging.getLogger(__name__)

class ConfigManager:
    """
    Gerenciador de configurações da aplicação.
    
    Responsável por carregar, salvar e gerenciar todas as configurações
    da aplicação em arquivo INI. Cria configurações padrão se não existirem.
    
    Attributes:
        config: Objeto ConfigParser com todas as configurações
    """
    def __init__(self) -> None:
        """
        Inicializa o ConfigManager e carrega as configurações.
        
        Cria arquivo de configuração padrão se não existir.
        """
        self.config = configparser.ConfigParser()
        self.load_config()

    def load_config(self) -> None:
        """Carrega as configurações do arquivo. Cria o arquivo com padrões se não existir."""
        if not os.path.exists(CONFIG_PATH):
            self._create_default_config()
            # Precisamos salvar o arquivo recém-criado antes de lê-lo
            self._save_config_file()
        
        # O argumento encoding é importante para consistência
        self.config.read(CONFIG_PATH, encoding='utf-8')

    def _create_default_config(self) -> None:
        """Cria um arquivo de config com seções de estilo separadas."""
        # Música não tem mais animação nas configs (animação é por item na playlist)
        self.config['Projection_Music'] = {
            'font_size': '70',
            'font_color': 'white',
            'bg_color': 'black'
        }
        self.config['Projection_Bible'] = {
            'font_size': '60',
            'font_color': '#FFFFE0', # Um branco amarelado
            'bg_color': '#000033' # Um azul bem escuro
        }
        self.config['Projection_Text'] = {
            'font_size': '65',
            'font_color': 'white',
            'bg_color': 'black'
        }
        self.config['Display'] = {
            'projection_monitor_index': ''
        }
        # Salva o arquivo após criar a configuração padrão
        self._save_config_file()

    def get_setting(self, section: str, key: str, fallback: Optional[str] = None) -> Optional[str]:
        """Obtém uma configuração. Retorna fallback se não encontrada."""
        # Adicionado encoding='utf-8' para consistência
        self.config.read(CONFIG_PATH, encoding='utf-8')
        return self.config.get(section, key, fallback=fallback)

    def get_int_setting(self, section: str, key: str, fallback: Optional[int] = None) -> Optional[int]:
        """Obtém uma configuração como inteiro. Retorna fallback se não encontrada."""
        # Adicionado encoding='utf-8' para consistência
        self.config.read(CONFIG_PATH, encoding='utf-8')
        try:
            return self.config.getint(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
            return fallback

    def set_setting(self, section: str, key: str, value: Any) -> bool:
        """Define uma configuração e salva no arquivo."""
        # Fail Fast: Validar valor conforme tipo de setting
        if key == 'font_size':
            value = validate_font_size(value)
        elif key in ('font_color', 'bg_color', 'animation_color'):
            value = validate_color(value)
        # Outros tipos de settings (como animation_type) são strings simples
        # e não precisam de validação específica além do que já é feito
        
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, str(value))
        return self._save_config_file() # Adiciona o 'return' aqui

    def _save_config_file(self) -> bool:
        """Salva o objeto de configuração atual no arquivo."""
        try:
            with open(CONFIG_PATH, 'w', encoding='utf-8') as configfile:
                self.config.write(configfile)
            return True # Retorna True em caso de sucesso
        except IOError as e:
            logger.error(f"Erro ao salvar arquivo de configuração - caminho: {CONFIG_PATH}, seção: {list(self.config.sections())}", exc_info=True)
            raise ConfigSaveError(f"Não foi possível salvar o arquivo de configuração: {e}") from e