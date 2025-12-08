"""
Módulo de validação de entrada para o Projetor.

Este módulo fornece funções de validação que implementam o padrão Fail Fast,
validando dados no início das operações e levantando exceções imediatamente
se os dados forem inválidos.
"""

import re
from urllib.parse import urlparse
from core.exceptions import ValidationError


def validate_string(value, field_name, min_length=1, max_length=None):
    """
    Valida que um valor é uma string válida.
    
    Args:
        value: Valor a ser validado
        field_name: Nome do campo (para mensagens de erro)
        min_length: Comprimento mínimo permitido (padrão: 1)
        max_length: Comprimento máximo permitido (None = sem limite)
    
    Returns:
        str: String validada e stripada
    
    Raises:
        ValidationError: Se o valor não for uma string válida
    
    Examples:
        >>> validate_string("  Hello  ", "nome")
        'Hello'
        >>> validate_string("", "nome")
        ValidationError: O campo 'nome' não pode estar vazio
        >>> validate_string(None, "nome")
        ValidationError: O campo 'nome' não pode ser None
    """
    if value is None:
        raise ValidationError(f"O campo '{field_name}' não pode ser None")
    
    if not isinstance(value, str):
        raise ValidationError(f"O campo '{field_name}' deve ser uma string, recebido: {type(value).__name__}")
    
    value = value.strip()
    
    if len(value) < min_length:
        raise ValidationError(
            f"O campo '{field_name}' deve ter pelo menos {min_length} caractere(s), "
            f"recebido: {len(value)}"
        )
    
    if max_length is not None and len(value) > max_length:
        raise ValidationError(
            f"O campo '{field_name}' deve ter no máximo {max_length} caractere(s), "
            f"recebido: {len(value)}"
        )
    
    return value


def validate_url(url, allowed_domains=None):
    """
    Valida que uma URL é válida e, opcionalmente, pertence a domínios permitidos.
    
    Args:
        url: URL a ser validada
        allowed_domains: Lista de domínios permitidos (ex: ['letras.mus.br'])
    
    Returns:
        str: URL validada
    
    Raises:
        ValidationError: Se a URL for inválida ou não pertencer aos domínios permitidos
    
    Examples:
        >>> validate_url("https://www.letras.mus.br/song")
        'https://www.letras.mus.br/song'
        >>> validate_url("invalid-url")
        ValidationError: URL inválida: formato incorreto
        >>> validate_url("https://example.com", allowed_domains=['letras.mus.br'])
        ValidationError: URL inválida: domínio 'example.com' não é permitido
    """
    if not isinstance(url, str):
        raise ValidationError(f"URL deve ser uma string, recebido: {type(url).__name__}")
    
    url = url.strip()
    
    if not url:
        raise ValidationError("URL não pode estar vazia")
    
    try:
        parsed = urlparse(url)
    except Exception as e:
        raise ValidationError(f"URL inválida: erro ao fazer parse - {e}")
    
    # Validar esquema
    if parsed.scheme not in ('http', 'https'):
        raise ValidationError(f"URL inválida: esquema deve ser 'http' ou 'https', recebido: '{parsed.scheme}'")
    
    # Validar que tem netloc (domínio)
    if not parsed.netloc:
        raise ValidationError("URL inválida: formato incorreto (sem domínio)")
    
    # Validar domínios permitidos
    if allowed_domains:
        domain = parsed.netloc.lower()
        # Remove 'www.' se presente para comparação
        domain_clean = domain.replace('www.', '')
        
        allowed_clean = [d.lower().replace('www.', '') for d in allowed_domains]
        
        if domain_clean not in allowed_clean:
            raise ValidationError(
                f"URL inválida: domínio '{parsed.netloc}' não é permitido. "
                f"Domínios permitidos: {', '.join(allowed_domains)}"
            )
    
    return url


def validate_int(value, field_name, min_value=None, max_value=None):
    """
    Valida que um valor pode ser convertido para int e está dentro de um range.
    
    Args:
        value: Valor a ser validado
        field_name: Nome do campo (para mensagens de erro)
        min_value: Valor mínimo permitido (None = sem limite)
        max_value: Valor máximo permitido (None = sem limite)
    
    Returns:
        int: Valor validado como int
    
    Raises:
        ValidationError: Se o valor não puder ser convertido ou estiver fora do range
    
    Examples:
        >>> validate_int("42", "idade")
        42
        >>> validate_int("abc", "idade")
        ValidationError: O campo 'idade' deve ser um número inteiro
        >>> validate_int("5", "idade", min_value=10)
        ValidationError: O campo 'idade' deve ser no mínimo 10, recebido: 5
    """
    if value is None:
        raise ValidationError(f"O campo '{field_name}' não pode ser None")
    
    try:
        int_value = int(value)
    except (ValueError, TypeError):
        raise ValidationError(f"O campo '{field_name}' deve ser um número inteiro, recebido: {value}")
    
    if min_value is not None and int_value < min_value:
        raise ValidationError(
            f"O campo '{field_name}' deve ser no mínimo {min_value}, recebido: {int_value}"
        )
    
    if max_value is not None and int_value > max_value:
        raise ValidationError(
            f"O campo '{field_name}' deve ser no máximo {max_value}, recebido: {int_value}"
        )
    
    return int_value


def validate_color(color_value):
    """
    Valida que um valor é uma cor válida (hex ou nome comum).
    
    Args:
        color_value: Valor da cor a ser validado
    
    Returns:
        str: Cor validada
    
    Raises:
        ValidationError: Se a cor for inválida
    
    Examples:
        >>> validate_color("#FF0000")
        '#FF0000'
        >>> validate_color("white")
        'white'
        >>> validate_color("invalid")
        ValidationError: Cor inválida: 'invalid'
    """
    if not isinstance(color_value, str):
        raise ValidationError(f"Cor deve ser uma string, recebido: {type(color_value).__name__}")
    
    color_value = color_value.strip()
    
    if not color_value:
        raise ValidationError("Cor não pode estar vazia")
    
    # Nomes de cores comuns aceitos
    common_colors = {
        'white', 'black', 'red', 'green', 'blue', 'yellow', 'cyan', 'magenta',
        'gray', 'grey', 'orange', 'purple', 'pink', 'brown', 'silver', 'gold'
    }
    
    # Validar formato hex (#RRGGBB ou #RGB)
    hex_pattern = re.compile(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
    
    if hex_pattern.match(color_value):
        return color_value
    
    # Validar nome comum
    if color_value.lower() in common_colors:
        return color_value
    
    raise ValidationError(f"Cor inválida: '{color_value}'. Use formato hex (#RRGGBB) ou nome de cor comum")


def validate_font_size(size):
    """
    Valida que um tamanho de fonte é válido (número positivo dentro de range razoável).
    
    Args:
        size: Tamanho da fonte a ser validado
    
    Returns:
        int: Tamanho validado como int
    
    Raises:
        ValidationError: Se o tamanho for inválido
    
    Examples:
        >>> validate_font_size("70")
        70
        >>> validate_font_size("-10")
        ValidationError: Tamanho de fonte deve ser um número positivo, recebido: -10
        >>> validate_font_size("300")
        ValidationError: Tamanho de fonte deve estar entre 8 e 200, recebido: 300
    """
    MIN_FONT_SIZE = 8
    MAX_FONT_SIZE = 200
    
    int_value = validate_int(size, "tamanho de fonte", min_value=MIN_FONT_SIZE, max_value=MAX_FONT_SIZE)
    
    return int_value

