# Plano de Ação - Melhorias do Projeto

## Visão Geral

Este documento apresenta um plano dividido em **5 fases** para alinhar o projeto com as diretrizes do prompt de IA (`docs/prompt-ia.md`). Cada fase pode ser executada de forma independente e inclui tarefas específicas, critérios de aceitação e estimativas de tempo.

---

## Estrutura das Fases

- **Fase 1**: Fundação - Logging e Tratamento de Erros (Crítico)
- **Fase 2**: Robustez - Validação e Fail Fast (Crítico)
- **Fase 3**: Refatoração - Modularização e DRY (Alta Prioridade)
- **Fase 4**: Qualidade - Performance e Tipagem (Média Prioridade)
- **Fase 5**: Testes e Documentação (Baixa Prioridade)

---

# FASE 1: Fundação - Logging e Tratamento de Erros 🔴

**Objetivo**: Implementar sistema de logging estruturado e classes de erro personalizadas.

**Prioridade**: 🔴 ALTA  
**Estimativa**: 4-6 horas  
**Dependências**: Nenhuma

## Tarefas

### 1.1. Criar Sistema de Logging Estruturado

**Arquivos a criar**:
- `core/logging_config.py`

**Arquivos a modificar**:
- `main.py` (adicionar setup de logging)
- `core/services/bible_api_client.py` (substituir `print()`)
- `core/services/letras_scraper.py` (substituir `print()`)
- `core/music_manager.py` (substituir `print()`)
- `core/config_manager.py` (substituir `print()`)
- `core/bible_manager.py` (substituir `print()`)
- `gui/dialogs.py` (substituir `print()`)

**Tarefas específicas**:
1. Criar `core/logging_config.py` com função `setup_logging()`
   - Configurar logging para arquivo e console
   - Formato estruturado com timestamp, nível, módulo, linha
   - Criar diretório `logs/` automaticamente
   - Configurar níveis de log por ambiente
   
2. Adicionar setup de logging em `main.py`
   ```python
   from core.logging_config import setup_logging
   logger = setup_logging()
   ```

3. Substituir todos os `print()` por logging apropriado:
   - `print("INFO: ...")` → `logger.info(...)`
   - `print("ERRO: ...")` → `logger.error(..., exc_info=True)`
   - `print("AVISO: ...")` → `logger.warning(...)`

4. Adicionar contexto nos logs:
   - IDs de músicas, versículos, etc.
   - Stack traces para erros

**Critérios de Aceitação**:
- [ ] Todos os `print()` substituídos por logging
- [ ] Logs escritos em arquivo `logs/projetor.log`
- [ ] Logs também aparecem no console durante desenvolvimento
- [ ] Erros incluem stack trace completo
- [ ] Logs têm formato estruturado consistente

**Arquivos afetados**: 7 arquivos

---

### 1.2. Criar Classes de Erro Personalizadas

**Arquivos a criar**:
- `core/exceptions.py`

**Arquivos a modificar**:
- `core/config_manager.py`
- `core/music_manager.py`
- `core/bible_manager.py`
- `core/services/bible_api_client.py`
- `core/services/letras_scraper.py`

**Tarefas específicas**:
1. Criar hierarquia de exceções em `core/exceptions.py`:
   ```python
   class ProjectorError(Exception)
   class ConfigError(ProjectorError)
   class MusicDatabaseError(ProjectorError)
   class BibleAPIError(ProjectorError)
   class ScraperError(ProjectorError)
   class ValidationError(ProjectorError)
   ```

2. Refatorar métodos que retornam `None` para levantar exceções:
   - `ConfigManager._save_config_file()` → levanta `ConfigSaveError`
   - `MusicManager.save_music_db()` → levanta `MusicDatabaseError`
   - `BibleAPIClient._make_request()` → levanta `BibleAPIError`
   - `LetrasScraper.fetch_lyrics_from_url()` → levanta `ScraperError`

3. Atualizar tratamento de erros nos controllers:
   - Adicionar `try/except` específicos
   - Logar erros apropriadamente
   - Mostrar mensagens de erro ao usuário

**Critérios de Aceitação**:
- [ ] Hierarquia de exceções criada e documentada
- [ ] Métodos que retornavam `None` agora levantam exceções
- [ ] Todos os erros são capturados e tratados adequadamente
- [ ] Mensagens de erro são informativas para o usuário
- [ ] Erros são logados com contexto completo

**Arquivos afetados**: 6 arquivos

---

## Resultado Esperado da Fase 1

- ✅ Sistema de logging funcionando
- ✅ Todos os erros tipados e tratados
- ✅ Logs estruturados com contexto
- ✅ Base sólida para debugging e monitoramento

---

# FASE 2: Robustez - Validação e Fail Fast 🔴

**Objetivo**: Implementar validação de entrada e padrão Fail Fast.

**Prioridade**: 🔴 ALTA  
**Estimativa**: 3-4 horas  
**Dependências**: Fase 1 (para usar exceções customizadas)

## Tarefas

### 2.1. Criar Módulo de Validação

**Arquivos a criar**:
- `core/validators.py`

**Arquivos a modificar**:
- `core/music_manager.py`
- `core/config_manager.py`
- `gui/controllers/music_controller.py`
- `core/services/letras_scraper.py`

**Tarefas específicas**:
1. Criar funções de validação em `core/validators.py`:
   - `validate_string(value, field_name, min_length=1, max_length=None)`
   - `validate_url(url, allowed_domains=None)`
   - `validate_int(value, field_name, min_value=None, max_value=None)`
   - `validate_color(color_value)`
   - `validate_font_size(size)`

2. Adicionar validação Fail Fast em:
   - `MusicManager.add_music()` - validar title, artist, lyrics_full
   - `MusicManager.edit_music()` - validar todos os campos
   - `ConfigManager.set_setting()` - validar tipo e valor
   - `LetrasScraper.fetch_lyrics_from_url()` - validar URL

3. Criar exceção `ValidationError` para erros de validação

**Critérios de Aceitação**:
- [ ] Todas as entradas são validadas no início das funções
- [ ] Validações falham rápido (antes de processamento)
- [ ] Mensagens de erro de validação são claras
- [ ] Validações incluem tipos e valores

**Arquivos afetados**: 5 arquivos

---

### 2.2. Implementar Validação de Entrada no Frontend

**Arquivos a modificar**:
- `gui/dialogs.py` (AddEditSongDialog)
- `gui/controllers/music_controller.py`
- `gui/controllers/bible_controller.py`

**Tarefas específicas**:
1. Validar entrada antes de enviar para managers:
   - Validar campos vazios
   - Validar formatos de URL
   - Validar tipos de dados

2. Mostrar feedback visual para erros de validação
3. Prevenir submissão de formulários inválidos

**Critérios de Aceitação**:
- [ ] Validação acontece antes de processar
- [ ] Usuário recebe feedback imediato
- [ ] Formulários não são submetidos se inválidos

**Arquivos afetados**: 3 arquivos

---

## Resultado Esperado da Fase 2

- ✅ Validação robusta de todas as entradas
- ✅ Fail Fast implementado
- ✅ Mensagens de erro claras
- ✅ Menos bugs causados por dados inválidos

---

# FASE 3: Refatoração - Modularização e DRY 🟡

**Objetivo**: Refatorar arquivos grandes e eliminar duplicação de código.

**Prioridade**: 🟡 MÉDIA  
**Estimativa**: 6-8 horas  
**Dependências**: Fase 1 (para usar logging e exceções)

## Tarefas

### 3.1. Dividir `gui/main_window.py`

**Arquivos a criar**:
- `gui/ui/builders.py` (métodos de criação de UI)
- `gui/ui/top_bar.py` (componente de barra superior)
- `gui/ui/preview_pane.py` (componente de pré-visualização)

**Arquivos a modificar**:
- `gui/main_window.py` (refatorar para usar componentes)

**Tarefas específicas**:
1. Extrair métodos de criação de UI para `gui/ui/builders.py`:
   - `create_top_bar(master, callbacks)`
   - `create_preview_pane(master)`
   - `create_main_tabs(master)`
   
2. Criar classes de componentes:
   - `TopBar` em `gui/ui/top_bar.py`
   - `PreviewPane` em `gui/ui/preview_pane.py`

3. Refatorar `main_window.py` para usar componentes:
   - Reduzir para < 300 linhas
   - Manter apenas lógica de coordenação

**Critérios de Aceitação**:
- [ ] `main_window.py` tem < 300 linhas
- [ ] Componentes são reutilizáveis
- [ ] Funcionalidade existente mantida
- [ ] Código mais fácil de testar

**Arquivos afetados**: 4 arquivos (1 refatorado, 3 novos)

---

### 3.2. Centralizar Lógica Duplicada (DRY)

**Arquivos a criar**:
- `core/utils/file_utils.py`

**Arquivos a modificar**:
- `core/config_manager.py`
- `core/music_manager.py`
- `core/bible_manager.py`

**Tarefas específicas**:
1. Criar utilitários de arquivo em `core/utils/file_utils.py`:
   - `save_json_file(file_path, data, ensure_ascii=False)`
   - `load_json_file(file_path, default=None)`
   - `ensure_directory_exists(file_path)`

2. Refatorar para usar utilitários:
   - `ConfigManager._save_config_file()` → usar `save_json_file()`
   - `MusicManager.save_music_db()` → usar `save_json_file()`
   - `BibleManager._save_books_to_cache()` → usar `save_json_file()`

3. Centralizar lógica de criação de diretórios

**Critérios de Aceitação**:
- [ ] Lógica de salvamento centralizada
- [ ] Sem duplicação de código
- [ ] Tratamento de erros consistente
- [ ] Todos os salvamentos usam os mesmos utilitários

**Arquivos afetados**: 4 arquivos (1 novo, 3 modificados)

---

### 3.3. Extrair Lógica de Centralização de Dialogs

**Arquivos a criar**:
- `gui/utils/dialog_utils.py`

**Arquivos a modificar**:
- `gui/dialogs.py`

**Tarefas específicas**:
1. Criar função utilitária `center_dialog(dialog, master)` em `gui/utils/dialog_utils.py`

2. Refatorar todos os dialogs para usar a função utilitária:
   - Remover métodos `_center_window()` duplicados
   - Usar função centralizada

**Critérios de Aceitação**:
- [ ] Lógica de centralização não está duplicada
- [ ] Todos os dialogs usam a mesma função
- [ ] Funcionalidade mantida

**Arquivos afetados**: 2 arquivos (1 novo, 1 modificado)

---

## Resultado Esperado da Fase 3

- ✅ Arquivos grandes divididos e organizados
- ✅ Código duplicado eliminado
- ✅ Componentes reutilizáveis criados
- ✅ Manutenibilidade melhorada

---

# FASE 4: Qualidade - Performance e Tipagem 🟡

**Objetivo**: Otimizar performance e adicionar type hints.

**Prioridade**: 🟡 MÉDIA  
**Estimativa**: 5-7 horas  
**Dependências**: Fase 1 (para usar logging)

## Tarefas

### 4.1. Otimizar Performance com Índices

**Arquivos a modificar**:
- `core/music_manager.py`

**Tarefas específicas**:
1. Adicionar índices para buscas O(1):
   - `_music_index: Dict[str, dict]` - mapeia ID → música
   - `_title_artist_index: Dict[Tuple[str, str], str]` - mapeia (title, artist) → ID

2. Criar método `_rebuild_indexes()`:
   - Reconstrói índices após mudanças
   - Chamado após carregar, adicionar, editar, deletar

3. Refatorar métodos de busca:
   - `get_music_by_id()` → usar `_music_index` (O(1))
   - `is_duplicate()` → usar `_title_artist_index` (O(1))

**Critérios de Aceitação**:
- [ ] Busca por ID é O(1)
- [ ] Verificação de duplicata é O(1)
- [ ] Índices são mantidos consistentes
- [ ] Performance melhorada para bases grandes

**Arquivos afetados**: 1 arquivo

---

### 4.2. Adicionar Type Hints

**Arquivos a modificar**:
- Todos os arquivos Python do projeto

**Tarefas específicas**:
1. Adicionar type hints em todas as funções públicas:
   - Parâmetros com tipos
   - Tipo de retorno
   - Usar `Optional`, `List`, `Dict`, `Tuple` do `typing`

2. Criar arquivo `core/types.py` para tipos customizados:
   - `MusicData = Dict[str, Any]`
   - `BibleBook = Dict[str, Any]`
   - `Slide = str`

3. Configurar `mypy` para validação:
   - Criar `mypy.ini`
   - Adicionar verificação no CI/CD (futuro)

**Critérios de Aceitação**:
- [ ] Todas as funções públicas têm type hints
- [ ] Type hints cobrem > 90% do código
- [ ] `mypy` não reporta erros (ou mínimos)
- [ ] Autocomplete funciona melhor no IDE

**Arquivos afetados**: 16 arquivos

---

### 4.3. Otimizar Buscas em `BibleManager`

**Arquivos a modificar**:
- `core/bible_manager.py`

**Tarefas específicas**:
1. Criar índice para busca de livros por abreviação:
   - `_books_by_abbrev: Dict[str, dict]`
   
2. Refatorar `get_book_by_abbrev()` para usar índice O(1)

**Critérios de Aceitação**:
- [ ] Busca de livro é O(1)
- [ ] Índice é construído no carregamento

**Arquivos afetados**: 1 arquivo

---

## Resultado Esperado da Fase 4

- ✅ Performance otimizada (busca O(1))
- ✅ Type hints em todo o código
- ✅ Melhor suporte do IDE
- ✅ Menos erros de tipo em runtime

---

# FASE 5: Testes e Documentação 🟢

**Objetivo**: Criar testes unitários e documentação completa.

**Prioridade**: 🟢 BAIXA  
**Estimativa**: 8-10 horas  
**Dependências**: Todas as fases anteriores

## Tarefas

### 5.1. Setup de Testes

**Arquivos a criar**:
- `tests/__init__.py`
- `tests/conftest.py` (fixtures do pytest)
- `requirements-dev.txt`

**Tarefas específicas**:
1. Instalar e configurar pytest:
   - Adicionar `pytest`, `pytest-cov`, `pytest-mock` ao `requirements-dev.txt`
   - Criar `pytest.ini` com configurações

2. Criar fixtures em `tests/conftest.py`:
   - `sample_music_data`
   - `sample_bible_data`
   - `mock_config_manager`
   - `mock_api_client`

3. Configurar cobertura de código:
   - Meta: 80% de cobertura
   - Gerar relatório HTML

**Critérios de Aceitação**:
- [ ] Pytest configurado e funcionando
- [ ] Fixtures criadas
- [ ] Comando `pytest` executa sem erros

**Arquivos afetados**: 3 arquivos novos

---

### 5.2. Criar Testes para Managers

**Arquivos a criar**:
- `tests/core/test_music_manager.py`
- `tests/core/test_bible_manager.py`
- `tests/core/test_config_manager.py`

**Tarefas específicas**:
1. Testes para `MusicManager`:
   - `test_add_music()`
   - `test_get_music_by_id()`
   - `test_is_duplicate()`
   - `test_edit_music()`
   - `test_delete_music()`
   - `test_save_and_load_database()`

2. Testes para `BibleManager`:
   - `test_load_books()`
   - `test_cache_functionality()`
   - `test_get_book_by_abbrev()`

3. Testes para `ConfigManager`:
   - `test_load_config()`
   - `test_set_and_get_setting()`
   - `test_default_config_creation()`

**Critérios de Aceitação**:
- [ ] Todos os métodos públicos testados
- [ ] Casos de sucesso e erro cobertos
- [ ] Cobertura > 80% nos managers

**Arquivos afetados**: 3 arquivos novos

---

### 5.3. Criar Testes para Serviços

**Arquivos a criar**:
- `tests/core/services/test_bible_api_client.py`
- `tests/core/services/test_letras_scraper.py`

**Tarefas específicas**:
1. Testes para `BibleAPIClient` (com mocks):
   - Testar requisições bem-sucedidas
   - Testar erros de rede
   - Testar erros de JSON

2. Testes para `LetrasScraper` (com mocks):
   - Testar scraping bem-sucedido
   - Testar erros de rede
   - Testar URLs inválidas

**Critérios de Aceitação**:
- [ ] Serviços testados com mocks
- [ ] Não fazem requisições reais durante testes
- [ ] Todos os cenários de erro cobertos

**Arquivos afetados**: 2 arquivos novos

---

### 5.4. Criar Documentação

**Arquivos a criar**:
- `README.md`
- `docs/arquitetura.md`
- `docs/api.md`
- `docs/instalacao.md`
- `.gitignore` (se não existir)

**Tarefas específicas**:
1. Criar `README.md` completo:
   - Descrição do projeto
   - Screenshots
   - Instruções de instalação
   - Como usar
   - Contribuindo

2. Criar `docs/arquitetura.md`:
   - Diagrama de arquitetura
   - Descrição de componentes
   - Fluxo de dados

3. Criar `docs/api.md`:
   - Documentação dos managers
   - Documentação dos controllers
   - Exemplos de uso

4. Criar `docs/instalacao.md`:
   - Requisitos
   - Passo a passo de instalação
   - Troubleshooting

**Critérios de Aceitação**:
- [ ] README.md completo e atualizado
- [ ] Documentação de arquitetura criada
- [ ] Documentação de API criada
- [ ] Guia de instalação completo

**Arquivos afetados**: 5 arquivos novos

---

### 5.5. Melhorar Docstrings

**Arquivos a modificar**:
- Todos os arquivos Python

**Tarefas específicas**:
1. Adicionar docstrings em todas as classes
2. Adicionar docstrings em todos os métodos públicos
3. Usar formato Google Style ou NumPy Style
4. Incluir:
   - Descrição
   - Parâmetros
   - Retorno
   - Exceções
   - Exemplos (quando relevante)

**Critérios de Aceitação**:
- [ ] Todas as classes têm docstrings
- [ ] Todos os métodos públicos têm docstrings
- [ ] Docstrings seguem padrão consistente

**Arquivos afetados**: 16 arquivos

---

## Resultado Esperado da Fase 5

- ✅ Suite de testes completa
- ✅ Cobertura de código > 80%
- ✅ Documentação completa
- ✅ Projeto profissional e mantível

---

# Cronograma Sugerido

| Fase | Estimativa | Prioridade | Pode começar após |
|------|------------|------------|-------------------|
| Fase 1 | 4-6 horas | 🔴 ALTA | Imediatamente |
| Fase 2 | 3-4 horas | 🔴 ALTA | Fase 1 |
| Fase 3 | 6-8 horas | 🟡 MÉDIA | Fase 1 |
| Fase 4 | 5-7 horas | 🟡 MÉDIA | Fase 1 |
| Fase 5 | 8-10 horas | 🟢 BAIXA | Fases 1-4 |

**Total estimado**: 26-35 horas

---

# Checklist de Progresso

## Fase 1: Fundação
- [ ] 1.1 Sistema de logging criado
- [ ] 1.2 Classes de erro criadas
- [ ] Todos os `print()` substituídos
- [ ] Testes manuais passando

## Fase 2: Robustez
- [ ] 2.1 Módulo de validação criado
- [ ] 2.2 Validação no frontend implementada
- [ ] Fail Fast funcionando
- [ ] Testes manuais passando

## Fase 3: Refatoração
- [ ] 3.1 `main_window.py` dividido
- [ ] 3.2 Lógica duplicada centralizada
- [ ] 3.3 Dialogs refatorados
- [ ] Arquivo principal < 300 linhas
- [ ] Testes manuais passando

## Fase 4: Qualidade
- [ ] 4.1 Índices O(1) implementados
- [ ] 4.2 Type hints adicionados
- [ ] 4.3 Buscas otimizadas
- [ ] mypy configurado
- [ ] Testes manuais passando

## Fase 5: Testes e Documentação
- [ ] 5.1 Setup de testes
- [ ] 5.2 Testes de managers
- [ ] 5.3 Testes de serviços
- [ ] 5.4 Documentação criada
- [ ] 5.5 Docstrings melhoradas
- [ ] Cobertura > 80%

---

# Notas Importantes

1. **Ordem de Execução**: As fases podem ser executadas em paralelo (exceto dependências), mas recomenda-se seguir a ordem para evitar retrabalho.

2. **Testes Contínuos**: Após cada fase, testar manualmente toda a aplicação para garantir que nada quebrou.

3. **Commits Incrementais**: Fazer commits pequenos e frequentes, uma feature por vez.

4. **Code Review**: Se trabalhando em equipe, revisar código antes de merge.

5. **Backup**: Fazer backup antes de iniciar refatorações grandes (Fase 3).

---

**Última atualização**: 2024  
**Baseado em**: `docs/analise-prompt-ia.md`

