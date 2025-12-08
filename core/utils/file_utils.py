"""
Utilitários para operações com arquivos.

Este módulo fornece funções centralizadas para operações comuns de arquivo,
eliminando duplicação de código e garantindo tratamento consistente de erros.
"""

from pathlib import Path
import json
import logging
from core.exceptions import MusicDatabaseError

logger = logging.getLogger(__name__)


def ensure_directory_exists(file_path: Path) -> None:
    """
    Garante que o diretório do arquivo existe, criando-o se necessário.
    
    Args:
        file_path: Caminho do arquivo (o diretório será criado se não existir)
    
    Examples:
        >>> from pathlib import Path
        >>> ensure_directory_exists(Path("data/music_db.json"))
        # Cria o diretório 'data' se não existir
    """
    directory = file_path.parent
    if directory:
        directory.mkdir(parents=True, exist_ok=True)


def save_json_file(file_path: Path, data: dict, ensure_ascii: bool = False) -> None:
    """
    Salva dados em um arquivo JSON com tratamento de erros centralizado.
    
    Cria automaticamente o diretório se não existir e salva o arquivo
    com encoding UTF-8 e indentação de 2 espaços.
    
    Args:
        file_path: Caminho do arquivo JSON a ser criado
        data: Dados a serem salvos (deve ser serializável em JSON)
        ensure_ascii: Se True, caracteres não-ASCII são escapados (padrão: False)
    
    Raises:
        MusicDatabaseError: Se houver erro ao salvar o arquivo
    
    Examples:
        >>> from pathlib import Path
        >>> save_json_file(Path("data/test.json"), {"key": "value"})
        # Salva o arquivo com indentação e encoding UTF-8
    """
    try:
        ensure_directory_exists(file_path)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=ensure_ascii, indent=2)
        
        logger.debug(f"Arquivo JSON salvo com sucesso: {file_path}")
    except IOError as e:
        logger.error(f"Erro ao salvar arquivo JSON - caminho: {file_path}", exc_info=True)
        raise MusicDatabaseError(f"Não foi possível salvar o arquivo: {e}") from e
    except (TypeError, ValueError) as e:
        logger.error(f"Erro ao serializar dados JSON - caminho: {file_path}", exc_info=True)
        raise MusicDatabaseError(f"Erro ao serializar dados para JSON: {e}") from e


def load_json_file(file_path: Path, default: dict = None) -> dict:
    """
    Carrega dados de um arquivo JSON com tratamento de erros centralizado.
    
    Args:
        file_path: Caminho do arquivo JSON a ser carregado
        default: Valor padrão a retornar se o arquivo não existir ou houver erro
                 (padrão: None, que será convertido para {} se necessário)
    
    Returns:
        dict: Dados carregados do arquivo, ou default se houver erro
    
    Examples:
        >>> from pathlib import Path
        >>> data = load_json_file(Path("data/test.json"), default=[])
        # Retorna os dados do arquivo ou [] se não existir
    """
    if default is None:
        default = {}
    
    if not file_path.exists():
        logger.debug(f"Arquivo JSON não encontrado, usando padrão: {file_path}")
        return default
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        logger.debug(f"Arquivo JSON carregado com sucesso: {file_path}")
        return data
    except json.JSONDecodeError as e:
        logger.warning(f"Erro ao decodificar JSON - caminho: {file_path}, erro: {e}")
        return default
    except IOError as e:
        logger.warning(f"Erro ao ler arquivo JSON - caminho: {file_path}, erro: {e}")
        return default

