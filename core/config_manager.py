import configparser
import os
# --- IMPORTAÇÃO MODIFICADA ---
from core.paths import CONFIG_PATH

class ConfigManager:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.load_config()

    def load_config(self):
        """Carrega as configurações do arquivo. Cria o arquivo com padrões se não existir."""
        if not os.path.exists(CONFIG_PATH):
            self._create_default_config()
            # Precisamos salvar o arquivo recém-criado antes de lê-lo
            self._save_config_file()
        
        # O argumento encoding é importante para consistência
        self.config.read(CONFIG_PATH, encoding='utf-8')

    def _create_default_config(self):
        """Cria um arquivo de config com seções de estilo separadas."""
        self.config['Projection_Music'] = {
            'font_size': '70',
            'font_color': 'white',
            'bg_color': 'black',
            'animation_type': 'Neve',
            'animation_color': '#DDDDDD'
        }
        self.config['Projection_Bible'] = {
            'font_size': '60',
            'font_color': '#FFFFE0', # Um branco amarelado
            'bg_color': '#000033', # Um azul bem escuro
            'animation_type': 'Nenhuma',
            'animation_color': 'white'
        }
        self.config['Projection_Text'] = {
            'font_size': '65',
            'font_color': 'white',
            'bg_color': 'black',
            'animation_type': 'Partículas Flutuantes',
            'animation_color': '#AAAAAA'
        }
        self.config['Display'] = {
            'projection_monitor_index': ''
        }
        # Salva o arquivo após criar a configuração padrão
        self._save_config_file()

    def get_setting(self, section, key, fallback=None):
        """Obtém uma configuração. Retorna fallback se não encontrada."""
        # Adicionado encoding='utf-8' para consistência
        self.config.read(CONFIG_PATH, encoding='utf-8')
        return self.config.get(section, key, fallback=fallback)

    def get_int_setting(self, section, key, fallback=None):
        # Adicionado encoding='utf-8' para consistência
        self.config.read(CONFIG_PATH, encoding='utf-8')
        try:
            return self.config.getint(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
            return fallback

    def set_setting(self, section, key, value):
        """Define uma configuração e salva no arquivo."""
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, str(value))
        return self._save_config_file() # Adiciona o 'return' aqui

    def _save_config_file(self):
        """Salva o objeto de configuração atual no arquivo."""
        try:
            with open(CONFIG_PATH, 'w', encoding='utf-8') as configfile:
                self.config.write(configfile)
            return True # Retorna True em caso de sucesso
        except IOError as e:
            print(f"Erro ao salvar arquivo de configuração: {e}")
            return False # Retorna False em caso de erro