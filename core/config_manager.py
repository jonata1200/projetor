import configparser
import os

CONFIG_FILE = 'config.ini'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, CONFIG_FILE)

class ConfigManager:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.load_config()

    def load_config(self):
        """Carrega as configurações do arquivo. Cria o arquivo com padrões se não existir."""
        if not os.path.exists(CONFIG_PATH):
            self._create_default_config()
        self.config.read(CONFIG_PATH)

    def _create_default_config(self):
        """Cria um arquivo de configuração com valores padrão."""
        # --- INÍCIO DA ADIÇÃO ---
        self.config['Projection'] = {
            'font_size': '60',
            'font_color': 'white',
            'bg_color': 'black',
            'animation_type': 'Neve',
            'animation_color': 'white'
        }
        # --- FIM DA ADIÇÃO ---

        self.config['Display'] = {
            'projection_monitor_index': ''
        }

    def get_setting(self, section, key, fallback=None):
        """Obtém uma configuração. Retorna fallback se não encontrada."""
        try:
            return self.config.get(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return fallback

    def get_int_setting(self, section, key, fallback=None):
        try:
            return self.config.getint(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
            return fallback

    def set_setting(self, section, key, value):
        """Define uma configuração e salva no arquivo."""
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, str(value))
        self._save_config_file()

    def _save_config_file(self):
        """Salva o objeto de configuração atual no arquivo."""
        try:
            with open(CONFIG_PATH, 'w') as configfile:
                self.config.write(configfile)
        except IOError as e:
            print(f"Erro ao salvar arquivo de configuração: {e}")

if __name__ == '__main__':
    cm = ConfigManager()
    cm.set_setting('Audio', 'input_device_index', '2')
    cm.set_setting('Audio', 'energy_threshold', '3500')
    idx = cm.get_setting('Audio', 'input_device_index')
    energy = cm.get_int_setting('Audio', 'energy_threshold')