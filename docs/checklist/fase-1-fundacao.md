# Checklist - Fase 1: Fundação 🔴

**Objetivo**: Implementar sistema de logging estruturado e classes de erro personalizadas.

**Prioridade**: 🔴 ALTA  
**Estimativa**: 4-6 horas  
**Dependências**: Nenhuma

---

## ✅ Tarefa 1.1: Criar Sistema de Logging Estruturado

### Preparação
- [x] Criar diretório `core/` se não existir
- [x] Verificar estrutura de pastas do projeto

### Criar `core/logging_config.py`
- [x] Criar arquivo `core/logging_config.py`
- [x] Importar bibliotecas necessárias (`logging`, `sys`, `Path`)
- [x] Criar função `setup_logging()`
- [x] Configurar criação automática do diretório `logs/`
- [x] Configurar formato de log estruturado com:
  - [x] Timestamp
  - [x] Nome do módulo
  - [x] Nível de log
  - [x] Mensagem
  - [x] Nome do arquivo e linha
- [x] Configurar handlers:
  - [x] FileHandler para `logs/projetor.log` com encoding UTF-8
  - [x] StreamHandler para console
- [x] Configurar níveis de log por ambiente (DEBUG para dev, INFO para prod)
- [x] Retornar logger configurado
- [x] Adicionar docstring explicando a função

### Modificar `main.py`
- [x] Adicionar import: `from core.logging_config import setup_logging`
- [x] Chamar `setup_logging()` no início do script
- [x] Verificar que logs são gerados ao iniciar aplicação

### Substituir `print()` em `core/services/bible_api_client.py`
- [x] Localizar todos os `print()` no arquivo
- [x] Adicionar `import logging` e `logger = logging.getLogger(__name__)` no topo
- [x] Substituir `print("AVISO: ...")` por `logger.warning(...)`
- [x] Substituir `print("Erro na API da Bíblia: ...")` por `logger.error(..., exc_info=True)`
- [x] Adicionar contexto (endpoint, parâmetros) aos logs de erro
- [x] Verificar que stack traces são incluídos

### Substituir `print()` em `core/services/letras_scraper.py`
- [x] Localizar todos os `print()` no arquivo
- [x] Adicionar `import logging` e `logger = logging.getLogger(__name__)` no topo
- [x] Substituir `print("AVISO: ...")` por `logger.warning(...)`
- [x] Substituir `print("ERRO: ...")` por `logger.error(..., exc_info=True)`
- [x] Adicionar contexto (URL) aos logs
- [x] Verificar que stack traces são incluídos

### Substituir `print()` em `core/music_manager.py`
- [x] Localizar todos os `print()` no arquivo
- [x] Adicionar `import logging` e `logger = logging.getLogger(__name__)` no topo
- [x] Substituir `print("Erro ao carregar...")` por `logger.error(..., exc_info=True)`
- [x] Substituir `print("Erro ao salvar...")` por `logger.error(..., exc_info=True)`
- [x] Adicionar contexto (caminho do arquivo) aos logs
- [x] Verificar que stack traces são incluídos

### Substituir `print()` em `core/config_manager.py`
- [x] Localizar todos os `print()` no arquivo
- [x] Adicionar `import logging` e `logger = logging.getLogger(__name__)` no topo
- [x] Substituir `print("Erro ao salvar...")` por `logger.error(..., exc_info=True)`
- [x] Adicionar contexto (seção, chave) aos logs
- [x] Verificar que stack traces são incluídos

### Substituir `print()` em `core/bible_manager.py`
- [x] Localizar todos os `print()` no arquivo
- [x] Adicionar `import logging` e `logger = logging.getLogger(__name__)` no topo
- [x] Substituir `print("INFO: ...")` por `logger.info(...)`
- [x] Substituir `print("AVISO: ...")` por `logger.warning(...)`
- [x] Substituir `print("ERRO: ...")` por `logger.error(..., exc_info=True)`
- [x] Adicionar contexto aos logs quando relevante
- [x] Verificar que stack traces são incluídos em erros

### Substituir `print()` em `gui/dialogs.py`
- [x] Localizar todos os `print()` no arquivo
- [x] Adicionar `import logging` e `logger = logging.getLogger(__name__)` no topo
- [x] Substituir `print("Erro ao centralizar...")` por `logger.error(..., exc_info=True)`
- [x] Verificar que stack traces são incluídos

### Validação Final do Logging
- [x] Executar aplicação e verificar que `logs/projetor.log` é criado
- [x] Verificar que logs aparecem no console
- [x] Verificar formato estruturado dos logs
- [x] Testar cenários de erro e verificar stack traces
- [x] Verificar que não há mais `print()` no código (usar grep: `grep -r "print(" --include="*.py"`)

---

## ✅ Tarefa 1.2: Criar Classes de Erro Personalizadas

### Criar `core/exceptions.py`
- [x] Criar arquivo `core/exceptions.py`
- [x] Criar classe base `ProjectorError(Exception)`
  - [x] Adicionar docstring explicando propósito
- [x] Criar `ConfigError(ProjectorError)`
  - [x] Adicionar docstring
- [x] Criar `ConfigSaveError(ConfigError)`
  - [x] Adicionar docstring
- [x] Criar `MusicDatabaseError(ProjectorError)`
  - [x] Adicionar docstring
- [x] Criar `BibleAPIError(ProjectorError)`
  - [x] Adicionar docstring
- [x] Criar `ScraperError(ProjectorError)`
  - [x] Adicionar docstring
- [x] Criar `ValidationError(ProjectorError)`
  - [x] Adicionar docstring (será usado na Fase 2)

### Refatorar `core/config_manager.py`
- [x] Adicionar import: `from core.exceptions import ConfigSaveError`
- [x] Modificar `_save_config_file()` para levantar `ConfigSaveError` ao invés de retornar `False`
- [x] Atualizar tratamento de erro onde `_save_config_file()` é chamado
- [x] Logar erro antes de levantar exceção
- [x] Verificar que mensagem de erro é informativa

### Refatorar `core/music_manager.py`
- [x] Adicionar import: `from core.exceptions import MusicDatabaseError`
- [x] Modificar `save_music_db()` para levantar `MusicDatabaseError` ao invés de retornar `False`
- [x] Atualizar tratamento de erro em `add_music()` e `edit_music()`
- [x] Logar erro antes de levantar exceção
- [x] Verificar que mensagem de erro é informativa

### Refatorar `core/bible_manager.py`
- [x] Adicionar import: `from core.exceptions import MusicDatabaseError` (ou criar `BibleCacheError`)
- [x] Modificar `_save_books_to_cache()` para levantar exceção ao invés de apenas logar
- [x] Atualizar tratamento de erro onde necessário
- [x] Logar erro antes de levantar exceção

### Refatorar `core/services/bible_api_client.py`
- [x] Adicionar import: `from core.exceptions import BibleAPIError`
- [x] Modificar `_make_request()` para levantar `BibleAPIError` ao invés de retornar `None`
- [x] Adicionar contexto ao erro (endpoint, status code)
- [x] Atualizar métodos que usam `_make_request()` para tratar exceções
- [x] Logar erro antes de levantar exceção
- [x] Verificar que mensagens são informativas

### Refatorar `core/services/letras_scraper.py`
- [x] Adicionar import: `from core.exceptions import ScraperError`
- [x] Modificar `fetch_lyrics_from_url()` para levantar `ScraperError` ao invés de retornar `None`
- [x] Criar diferentes tipos de erro se necessário (ex: `ScraperNetworkError`, `ScraperParseError`)
- [x] Adicionar contexto ao erro (URL)
- [x] Atualizar tratamento de erro nos controllers que usam o scraper
- [x] Logar erro antes de levantar exceção

### Atualizar Controllers para Tratar Exceções
- [x] Revisar `gui/controllers/music_controller.py`
  - [x] Adicionar `try/except` para capturar exceções dos managers
  - [x] Logar erros apropriadamente
  - [x] Mostrar mensagens de erro ao usuário
- [x] Revisar `gui/controllers/bible_controller.py`
  - [x] Adicionar `try/except` para capturar exceções
  - [x] Logar erros apropriadamente
  - [x] Mostrar mensagens de erro ao usuário
- [x] Verificar outros controllers se necessário

### Validação Final das Exceções
- [x] Verificar que hierarquia de exceções está correta
- [x] Testar cenários de erro e verificar que exceções são levantadas
- [x] Verificar que erros são logados com contexto
- [x] Verificar que usuário recebe mensagens claras
- [x] Executar aplicação e testar funcionalidades que podem gerar erros

---

## ✅ Checklist de Critérios de Aceitação - Tarefa 1.1

- [x] Todos os `print()` substituídos por logging
- [x] Logs escritos em arquivo `logs/projetor.log`
- [x] Logs também aparecem no console durante desenvolvimento
- [x] Erros incluem stack trace completo
- [x] Logs têm formato estruturado consistente
- [x] Diretório `logs/` é criado automaticamente
- [x] Logs incluem contexto relevante (IDs, URLs, etc.)

---

## ✅ Checklist de Critérios de Aceitação - Tarefa 1.2

- [x] Hierarquia de exceções criada e documentada
- [x] Métodos que retornavam `None` agora levantam exceções
- [x] Todos os erros são capturados e tratados adequadamente
- [x] Mensagens de erro são informativas para o usuário
- [x] Erros são logados com contexto completo
- [x] Controllers tratam exceções apropriadamente

---

## ✅ Testes Manuais

- [ ] Executar aplicação e verificar que inicia normalmente
- [ ] Verificar criação do arquivo `logs/projetor.log`
- [ ] Testar funcionalidades principais:
  - [ ] Carregar músicas
  - [ ] Adicionar música
  - [ ] Carregar versículos da Bíblia
  - [ ] Importar música por URL
- [ ] Testar cenários de erro:
  - [ ] Erro ao salvar configuração
  - [ ] Erro ao salvar música
  - [ ] Erro de rede na API
  - [ ] URL inválida no scraper
- [ ] Verificar que logs são gerados para cada ação
- [ ] Verificar que erros aparecem nos logs com stack trace
- [ ] Verificar que mensagens de erro aparecem para o usuário

---

## 📝 Notas de Implementação

### Dicas
- Fazer commits incrementais: um arquivo por commit
- Testar após cada mudança
- Revisar formato dos logs antes de finalizar

### Problemas Conhecidos
- Nenhum até o momento

### Próximos Passos Após Esta Fase
- Fase 2: Implementar validação e Fail Fast

---

**Status**: ✅ Concluída  
**Última atualização**: 2024  
**Progresso**: [x] / [x] tarefas concluídas

