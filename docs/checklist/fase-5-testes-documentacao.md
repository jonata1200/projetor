# Checklist - Fase 5: Testes e Documentação 🟢

**Objetivo**: Criar testes unitários e documentação completa.

**Prioridade**: 🟢 BAIXA  
**Estimativa**: 8-10 horas  
**Dependências**: Todas as fases anteriores

---

## ✅ Tarefa 5.1: Setup de Testes

### Criar Estrutura de Testes
- [ ] Criar diretório `tests/` na raiz do projeto
- [ ] Criar arquivo `tests/__init__.py` (pode ser vazio)
- [ ] Criar subdiretórios:
  - [ ] `tests/core/`
  - [ ] `tests/core/services/`
  - [ ] `tests/gui/` (se necessário no futuro)

### Criar `requirements-dev.txt`
- [ ] Criar arquivo `requirements-dev.txt`
- [ ] Adicionar dependências de teste:
  - [ ] `pytest>=7.0.0`
  - [ ] `pytest-cov>=4.0.0` (cobertura)
  - [ ] `pytest-mock>=3.10.0` (mocks)
  - [ ] `pytest-asyncio>=0.21.0` (se houver código async)
- [ ] Incluir todas as dependências de `requirements.txt` também
- [ ] Documentar como instalar: `pip install -r requirements-dev.txt`

### Criar `pytest.ini`
- [ ] Criar arquivo `pytest.ini` na raiz
- [ ] Configurar opções:
  - [ ] `testpaths = tests`
  - [ ] `python_files = test_*.py`
  - [ ] `python_classes = Test*`
  - [ ] `python_functions = test_*`
  - [ ] `addopts = --verbose --cov=core --cov-report=html --cov-report=term`
- [ ] Configurar cobertura mínima (meta: 80%)

### Criar `tests/conftest.py`
- [ ] Criar arquivo `tests/conftest.py`
- [ ] Adicionar imports necessários
- [ ] Criar fixture `sample_music_data`:
  - [ ] Retornar dict com dados de música de exemplo
  - [ ] Incluir todos os campos necessários
- [ ] Criar fixture `sample_bible_data`:
  - [ ] Retornar dict com dados de livro bíblico de exemplo
- [ ] Criar fixture `mock_config_manager`:
  - [ ] Mock do ConfigManager
  - [ ] Retornar valores padrão
- [ ] Criar fixture `mock_api_client`:
  - [ ] Mock do BibleAPIClient
  - [ ] Retornar dados de exemplo
- [ ] Criar fixture `temp_music_db`:
  - [ ] Criar arquivo temporário para testes
  - [ ] Limpar após teste
- [ ] Criar fixture `temp_config_file`:
  - [ ] Criar arquivo de config temporário
  - [ ] Limpar após teste

### Testar Setup
- [ ] Instalar dependências: `pip install -r requirements-dev.txt`
- [ ] Executar `pytest --version` → deve funcionar
- [ ] Executar `pytest` → deve passar (mesmo sem testes ainda)
- [ ] Verificar que estrutura de diretórios está correta

---

## ✅ Tarefa 5.2: Criar Testes para Managers

### Criar `tests/core/__init__.py`
- [ ] Criar arquivo `tests/core/__init__.py`

### Criar `tests/core/test_music_manager.py`
- [ ] Criar arquivo `tests/core/test_music_manager.py`
- [ ] Adicionar imports necessários:
  - [ ] `import pytest`
  - [ ] `from core.music_manager import MusicManager`
  - [ ] `from core.exceptions import MusicDatabaseError, ValidationError`
  - [ ] Fixtures do conftest
- [ ] Implementar `test_add_music()`:
  - [ ] Testar adicionar música válida
  - [ ] Verificar que retorna música criada
  - [ ] Verificar que ID é gerado
  - [ ] Verificar que slides são gerados
- [ ] Implementar `test_add_music_invalid()`:
  - [ ] Testar título vazio → deve levantar ValidationError
  - [ ] Testar artista vazio → deve levantar ValidationError
  - [ ] Testar letra vazia → deve levantar ValidationError
- [ ] Implementar `test_get_music_by_id()`:
  - [ ] Testar busca de música existente
  - [ ] Testar busca de música inexistente → deve retornar None
- [ ] Implementar `test_is_duplicate()`:
  - [ ] Testar duplicata (mesmo título e artista)
  - [ ] Testar não duplicata (título ou artista diferente)
  - [ ] Testar case insensitive
- [ ] Implementar `test_edit_music()`:
  - [ ] Testar editar música existente
  - [ ] Verificar que alterações são salvas
  - [ ] Testar editar música inexistente → deve retornar False
- [ ] Implementar `test_delete_music()`:
  - [ ] Testar deletar música existente
  - [ ] Verificar que música é removida
  - [ ] Testar deletar música inexistente → deve retornar False
- [ ] Implementar `test_save_and_load_database()`:
  - [ ] Adicionar músicas
  - [ ] Salvar
  - [ ] Criar novo manager e carregar
  - [ ] Verificar que músicas foram carregadas
- [ ] Executar testes: `pytest tests/core/test_music_manager.py -v`

### Criar `tests/core/test_bible_manager.py`
- [ ] Criar arquivo `tests/core/test_bible_manager.py`
- [ ] Adicionar imports necessários
- [ ] Implementar `test_load_books()`:
  - [ ] Testar carregar livros (com mock da API)
  - [ ] Verificar que livros são carregados
- [ ] Implementar `test_cache_functionality()`:
  - [ ] Testar que cache é criado
  - [ ] Testar que cache é usado na próxima carga
  - [ ] Testar que cache corrompido é ignorado
- [ ] Implementar `test_get_book_by_abbrev()`:
  - [ ] Testar busca por abreviação existente
  - [ ] Testar busca por abreviação inexistente
  - [ ] Testar diferentes formatos de abreviação
- [ ] Executar testes: `pytest tests/core/test_bible_manager.py -v`

### Criar `tests/core/test_config_manager.py`
- [ ] Criar arquivo `tests/core/test_config_manager.py`
- [ ] Adicionar imports necessários
- [ ] Implementar `test_load_config()`:
  - [ ] Testar carregar config existente
  - [ ] Testar criar config padrão se não existe
- [ ] Implementar `test_set_and_get_setting()`:
  - [ ] Testar definir e obter setting
  - [ ] Testar obter setting inexistente → deve retornar fallback
- [ ] Implementar `test_default_config_creation()`:
  - [ ] Testar que config padrão é criado
  - [ ] Verificar que todas as seções existem
- [ ] Executar testes: `pytest tests/core/test_config_manager.py -v`

### Validação Final - Tarefa 5.2
- [ ] Executar todos os testes de managers: `pytest tests/core/ -v`
- [ ] Verificar cobertura: `pytest --cov=core tests/core/`
- [ ] Meta: > 80% de cobertura nos managers
- [ ] Corrigir testes que falharem

---

## ✅ Tarefa 5.3: Criar Testes para Serviços

### Criar `tests/core/services/__init__.py`
- [ ] Criar arquivo `tests/core/services/__init__.py`

### Criar `tests/core/services/test_bible_api_client.py`
- [ ] Criar arquivo `tests/core/services/test_bible_api_client.py`
- [ ] Adicionar imports:
  - [ ] `import pytest`
  - [ ] `from unittest.mock import Mock, patch`
  - [ ] `from core.services.bible_api_client import BibleAPIClient`
  - [ ] `from core.exceptions import BibleAPIError`
- [ ] Implementar `test_get_versions()`:
  - [ ] Testar que retorna lista de versões
  - [ ] Verificar formato dos dados
- [ ] Implementar `test_get_books_success()`:
  - [ ] Mock de requisição bem-sucedida
  - [ ] Verificar que retorna lista de livros
- [ ] Implementar `test_make_request_network_error()`:
  - [ ] Mock de erro de rede
  - [ ] Verificar que levanta BibleAPIError
- [ ] Implementar `test_make_request_json_error()`:
  - [ ] Mock de resposta inválida (não JSON)
  - [ ] Verificar que levanta BibleAPIError
- [ ] Implementar `test_get_chapter_verses()`:
  - [ ] Mock de requisição bem-sucedida
  - [ ] Verificar que retorna versículos
- [ ] Executar testes: `pytest tests/core/services/test_bible_api_client.py -v`

### Criar `tests/core/services/test_letras_scraper.py`
- [ ] Criar arquivo `tests/core/services/test_letras_scraper.py`
- [ ] Adicionar imports necessários
- [ ] Implementar `test_fetch_lyrics_success()`:
  - [ ] Mock de HTML válido
  - [ ] Mock de requisição bem-sucedida
  - [ ] Verificar que retorna título, artista e letra
- [ ] Implementar `test_fetch_lyrics_network_error()`:
  - [ ] Mock de erro de rede
  - [ ] Verificar que levanta ScraperError
- [ ] Implementar `test_fetch_lyrics_invalid_url()`:
  - [ ] Testar URL inválida
  - [ ] Verificar que levanta ValidationError ou ScraperError
- [ ] Implementar `test_fetch_lyrics_parse_error()`:
  - [ ] Mock de HTML sem elementos esperados
  - [ ] Verificar comportamento (retorna None ou levanta erro)
- [ ] Executar testes: `pytest tests/core/services/test_letras_scraper.py -v`

### Validação Final - Tarefa 5.3
- [ ] Executar todos os testes de serviços: `pytest tests/core/services/ -v`
- [ ] Verificar que não fazem requisições reais (apenas mocks)
- [ ] Verificar cobertura dos serviços

---

## ✅ Tarefa 5.4: Criar Documentação

### Criar `README.md` na Raiz
- [ ] Criar arquivo `README.md`
- [ ] Adicionar cabeçalho com nome do projeto
- [ ] Adicionar descrição do projeto:
  - [ ] O que faz
  - [ ] Para que serve
  - [ ] Principais funcionalidades
- [ ] Adicionar seção "Screenshots" (se tiver imagens)
- [ ] Adicionar seção "Instalação":
  - [ ] Requisitos
  - [ ] Passo a passo
  - [ ] Link para `docs/instalacao.md` para detalhes
- [ ] Adicionar seção "Como Usar":
  - [ ] Guia rápido
  - [ ] Principais funcionalidades
- [ ] Adicionar seção "Desenvolvimento":
  - [ ] Como rodar testes
  - [ ] Como contribuir
- [ ] Adicionar seção "Licença" (se aplicável)
- [ ] Adicionar badges (opcional): Python version, license, etc.

### Criar `docs/arquitetura.md`
- [ ] Criar arquivo `docs/arquitetura.md`
- [ ] Adicionar diagrama de arquitetura (texto ou imagem)
- [ ] Descrever componentes principais:
  - [ ] Core (managers, serviços)
  - [ ] GUI (controllers, windows)
  - [ ] Data (armazenamento)
- [ ] Descrever fluxo de dados:
  - [ ] Como dados fluem entre componentes
  - [ ] Responsabilidades de cada camada
- [ ] Documentar padrões usados (MVC, etc.)

### Criar `docs/api.md`
- [ ] Criar arquivo `docs/api.md`
- [ ] Documentar `MusicManager`:
  - [ ] Descrição
  - [ ] Métodos públicos
  - [ ] Parâmetros e retornos
  - [ ] Exemplos de uso
- [ ] Documentar `BibleManager`:
  - [ ] Mesmo formato
- [ ] Documentar `ConfigManager`:
  - [ ] Mesmo formato
- [ ] Documentar Controllers principais:
  - [ ] Principais métodos
  - [ ] Como usar
- [ ] Adicionar exemplos de código

### Criar `docs/instalacao.md`
- [ ] Criar arquivo `docs/instalacao.md`
- [ ] Seção "Requisitos":
  - [ ] Python 3.x
  - [ ] Bibliotecas necessárias
  - [ ] Sistema operacional
- [ ] Seção "Instalação Passo a Passo":
  - [ ] Clonar repositório
  - [ ] Criar ambiente virtual
  - [ ] Instalar dependências
  - [ ] Configurar variáveis de ambiente
- [ ] Seção "Troubleshooting":
  - [ ] Problemas comuns
  - [ ] Soluções

### Verificar/Criar `.gitignore`
- [ ] Verificar se `.gitignore` existe
- [ ] Se não existe, criar:
  - [ ] `__pycache__/`
  - [ ] `*.pyc`
  - [ ] `.env`
  - [ ] `logs/`
  - [ ] `*.log`
  - [ ] `.pytest_cache/`
  - [ ] `htmlcov/`
  - [ ] `.coverage`
  - [ ] Arquivos temporários

### Validação Final - Tarefa 5.4
- [ ] Revisar README.md para completude
- [ ] Verificar links e referências
- [ ] Testar instruções de instalação seguindo a documentação

---

## ✅ Tarefa 5.5: Melhorar Docstrings

### Escolher Formato de Docstring
- [ ] Decidir formato (Google Style ou NumPy Style)
- [ ] Recomendado: Google Style (mais legível)

### Adicionar Docstrings em Classes
- [ ] `core/music_manager.py` - classe MusicManager
- [ ] `core/bible_manager.py` - classe BibleManager
- [ ] `core/config_manager.py` - classe ConfigManager
- [ ] `core/services/bible_api_client.py` - classe BibleAPIClient
- [ ] `core/services/letras_scraper.py` - classe LetrasScraper
- [ ] Todos os controllers
- [ ] Todas as outras classes

### Adicionar Docstrings em Métodos Públicos
- [ ] Documentar cada método público:
  - [ ] Descrição breve
  - [ ] Args (parâmetros):
    - [ ] Nome do parâmetro
    - [ ] Tipo
    - [ ] Descrição
  - [ ] Returns:
    - [ ] Tipo de retorno
    - [ ] Descrição
  - [ ] Raises (se aplicável):
    - [ ] Tipo de exceção
    - [ ] Quando é levantada
  - [ ] Exemplo (quando relevante)

### Padrão Google Style Exemplo
```python
def add_music(self, title: str, artist: str, lyrics_full: str) -> Optional[MusicData]:
    """Adiciona uma nova música ao banco de dados.
    
    Args:
        title: Título da música (não pode ser vazio).
        artist: Nome do artista (não pode ser vazio).
        lyrics_full: Letra completa da música (não pode ser vazia).
    
    Returns:
        Dicionário com dados da música criada, ou None em caso de erro.
    
    Raises:
        ValidationError: Se algum campo for inválido.
        MusicDatabaseError: Se houver erro ao salvar no arquivo.
    
    Example:
        >>> manager = MusicManager()
        >>> music = manager.add_music("Música", "Artista", "Letra...")
        >>> print(music['id'])
        'uuid-here'
    """
```

### Validação Final - Tarefa 5.5
- [ ] Verificar que todas as classes têm docstrings
- [ ] Verificar que todos os métodos públicos têm docstrings
- [ ] Verificar formato consistente
- [ ] Revisar qualidade das docstrings

---

## ✅ Checklist de Critérios de Aceitação - Tarefa 5.1

- [ ] Pytest configurado e funcionando
- [ ] Fixtures criadas
- [ ] Comando `pytest` executa sem erros
- [ ] Estrutura de testes organizada

---

## ✅ Checklist de Critérios de Aceitação - Tarefa 5.2

- [ ] Todos os métodos públicos testados
- [ ] Casos de sucesso e erro cobertos
- [ ] Cobertura > 80% nos managers
- [ ] Testes são claros e mantíveis

---

## ✅ Checklist de Critérios de Aceitação - Tarefa 5.3

- [ ] Serviços testados com mocks
- [ ] Não fazem requisições reais durante testes
- [ ] Todos os cenários de erro cobertos
- [ ] Testes são isolados e independentes

---

## ✅ Checklist de Critérios de Aceitação - Tarefa 5.4

- [ ] README.md completo e atualizado
- [ ] Documentação de arquitetura criada
- [ ] Documentação de API criada
- [ ] Guia de instalação completo
- [ ] `.gitignore` configurado

---

## ✅ Checklist de Critérios de Aceitação - Tarefa 5.5

- [ ] Todas as classes têm docstrings
- [ ] Todos os métodos públicos têm docstrings
- [ ] Docstrings seguem padrão consistente
- [ ] Docstrings são informativas e claras

---

## ✅ Testes Finais Completos

### Executar Suite de Testes
- [ ] Executar todos os testes: `pytest -v`
- [ ] Verificar cobertura: `pytest --cov=. --cov-report=html`
- [ ] Meta: > 80% de cobertura geral
- [ ] Verificar relatório HTML de cobertura

### Testar Instalação com Documentação
- [ ] Seguir `docs/instalacao.md` do zero
- [ ] Verificar que todas as instruções funcionam
- [ ] Corrigir problemas encontrados

### Revisar Documentação
- [ ] Revisar README.md
- [ ] Revisar docs/arquitetura.md
- [ ] Revisar docs/api.md
- [ ] Verificar que está atualizada e correta

---

## 📝 Notas de Implementação

### Dicas Importantes
- Escrever testes antes de corrigir bugs (TDD opcional)
- Manter testes simples e focados
- Um teste = uma funcionalidade/edge case
- Documentar código complexo

### Estrutura de Testes Recomendada
```
tests/
├── __init__.py
├── conftest.py
├── core/
│   ├── __init__.py
│   ├── test_music_manager.py
│   ├── test_bible_manager.py
│   ├── test_config_manager.py
│   └── services/
│       ├── __init__.py
│       ├── test_bible_api_client.py
│       └── test_letras_scraper.py
```

### Próximos Passos
- Manter cobertura acima de 80%
- Adicionar testes conforme novas features
- Atualizar documentação conforme necessário

---

**Status**: 🔄 Em Progresso  
**Última atualização**: [Data]  
**Progresso**: [ ] / [ ] tarefas concluídas

