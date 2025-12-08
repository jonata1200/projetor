"""
Hierarquia de exceções personalizadas para o Projetor.

Este módulo define uma hierarquia de exceções que permite tratamento
específico de diferentes tipos de erros na aplicação.
"""


class ProjectorError(Exception):
    """
    Classe base para todas as exceções do Projetor.
    
    Esta classe serve como base para todas as exceções customizadas
    do projeto, permitindo captura genérica quando necessário.
    """
    pass


class ConfigError(ProjectorError):
    """
    Exceção base para erros relacionados a configurações.
    
    Usada para erros gerais de configuração do sistema.
    """
    pass


class ConfigSaveError(ConfigError):
    """
    Exceção levantada quando há falha ao salvar configurações.
    
    Geralmente causada por problemas de permissão de escrita
    ou problemas de I/O no arquivo de configuração.
    """
    pass


class MusicDatabaseError(ProjectorError):
    """
    Exceção levantada quando há erros relacionados ao banco de dados de músicas.
    
    Pode ocorrer durante operações de leitura, escrita ou manipulação
    do arquivo music_db.json.
    """
    pass


class BibleAPIError(ProjectorError):
    """
    Exceção levantada quando há erros na comunicação com a API da Bíblia.
    
    Pode ser causada por problemas de rede, autenticação, ou respostas
    inválidas da API.
    """
    pass


class ScraperError(ProjectorError):
    """
    Exceção base para erros relacionados ao scraper de letras.
    
    Usada para erros gerais durante o processo de scraping.
    """
    pass


class ScraperNetworkError(ScraperError):
    """
    Exceção levantada quando há erros de rede durante o scraping.
    
    Causada por problemas de conexão, timeout ou requisições HTTP falhadas.
    """
    pass


class ScraperParseError(ScraperError):
    """
    Exceção levantada quando há erros ao fazer parsing do HTML.
    
    Causada quando a estrutura HTML da página não corresponde
    aos seletores esperados.
    """
    pass


class ValidationError(ProjectorError):
    """
    Exceção levantada quando há erros de validação de dados.
    
    Será usada na Fase 2 para validação de entrada de dados.
    """
    pass

