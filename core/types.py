"""
Definições de tipos customizados para o projeto.

Este módulo centraliza os tipos de dados usados em todo o projeto,
facilitando a manutenção e melhorando a legibilidade do código.
"""

from typing import Dict, Any, List, Tuple

# Tipo para dados de música
MusicData = Dict[str, Any]
"""
Dicionário contendo dados de uma música.
Estrutura esperada:
{
    'id': str,
    'title': str,
    'artist': str,
    'lyrics_full': str,
    'slides': List[str]
}
"""

# Tipo para dados de livro da Bíblia
BibleBook = Dict[str, Any]
"""
Dicionário contendo dados de um livro da Bíblia.
Estrutura esperada:
{
    'name': str,
    'abbrev': str | Dict[str, str],
    'chapters': int,
    ...
}
"""

# Tipo para slide (string de texto)
Slide = str
"""
String representando um slide de apresentação.
"""

# Tipo para versão da Bíblia
BibleVersion = Dict[str, Any]
"""
Dicionário contendo dados de uma versão da Bíblia.
Estrutura esperada:
{
    'name': str,
    'abbrev': str,
    ...
}
"""

# Tipo para item da playlist
PlaylistItem = Dict[str, Any]
"""
Dicionário contendo dados de um item da playlist.
Estrutura esperada:
{
    'type': str,  # 'music', 'bible', 'text'
    'id': str,
    'title': str,
    'data': Any,
    ...
}
"""

