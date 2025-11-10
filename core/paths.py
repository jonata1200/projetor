from pathlib import Path

# SOURCE_ROOT é o caminho para a pasta 'projetor'
SOURCE_ROOT = Path(__file__).resolve().parent.parent

# --- ALTERAÇÃO PRINCIPAL AQUI ---
# Procuramos a pasta 'data' DENTRO da pasta 'projetor' (SOURCE_ROOT)
DATA_DIR = SOURCE_ROOT / "data"

# O arquivo de configuração geralmente fica na raiz do projeto, um nível acima do source
PROJECT_ROOT = SOURCE_ROOT.parent
CONFIG_PATH = PROJECT_ROOT / "config.ini"

# Os caminhos para os arquivos de dados agora serão calculados corretamente
MUSIC_DB_PATH = DATA_DIR / "music_db.json"
BIBLE_BOOKS_CACHE_PATH = DATA_DIR / "bible_books_cache.json"