"""
Configuração de logging estruturado para o Projetor.

Este módulo fornece uma função para configurar o sistema de logging
com handlers para arquivo e console, formatando logs de forma consistente.
"""

import logging
import sys
from pathlib import Path


def setup_logging(log_level=logging.INFO):
    """
    Configura o sistema de logging estruturado para a aplicação.
    
    Cria automaticamente o diretório 'logs/' se não existir e configura:
    - FileHandler para escrever logs em 'logs/projetor.log' com encoding UTF-8
    - StreamHandler para exibir logs no console
    - Formato estruturado com timestamp, módulo, nível, mensagem e localização
    
    Args:
        log_level: Nível de log padrão (logging.DEBUG para dev, logging.INFO para prod)
    
    Returns:
        logging.Logger: Logger configurado para uso na aplicação
    """
    # Cria o diretório de logs se não existir
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Formato estruturado de log
    log_format = (
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s "
        "(%(filename)s:%(lineno)d)"
    )
    
    # Formato de data/hora
    date_format = "%Y-%m-%d %H:%M:%S"
    
    # Configura o logger raiz
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Remove handlers existentes para evitar duplicação
    root_logger.handlers.clear()
    
    # Handler para arquivo
    file_handler = logging.FileHandler(
        logs_dir / "projetor.log",
        encoding="utf-8",
        mode="a"
    )
    file_handler.setLevel(log_level)
    file_formatter = logging.Formatter(log_format, datefmt=date_format)
    file_handler.setFormatter(file_formatter)
    root_logger.addHandler(file_handler)
    
    # Handler para console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_formatter = logging.Formatter(log_format, datefmt=date_format)
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    # Retorna o logger configurado
    logger = logging.getLogger(__name__)
    logger.info("Sistema de logging configurado com sucesso")
    
    return logger

