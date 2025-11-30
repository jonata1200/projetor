# Checklist - Fase 1: Fundação 🔴

**Objetivo**: Implementar sistema de logging estruturado e classes de erro personalizadas.

**Prioridade**: 🔴 ALTA  
**Estimativa**: 4-6 horas  
**Dependências**: Nenhuma

---

## ✅ Tarefa 1.1: Criar Sistema de Logging Estruturado

### Preparação
- [ ] Criar diretório `core/` se não existir
- [ ] Verificar estrutura de pastas do projeto

### Criar `core/logging_config.py`
- [ ] Criar arquivo `core/logging_config.py`
- [ ] Importar bibliotecas necessárias (`logging`, `sys`, `Path`)
- [ ] Criar função `setup_logging()`
- [ ] Configurar criação automática do diretório `logs/`
- [ ] Configurar formato de log estruturado com:
  - [ ] Timestamp
  - [ ] Nome do módulo
  - [ ] Nível de log
  - [ ] Mensagem
  - [ ] Nome do arquivo e linha
- [ ] Configurar handlers:
  - [ ] FileHandler para `logs/projetor.log` com encoding UTF-8
  - [ ] StreamHandler para console
- [ ] Configurar níveis de log por ambiente (DEBUG para dev, INFO para prod)
- [ ] Retornar logger configurado
- [ ] Adicionar docstring explicando a função

### Modificar `main.py`
- [ ] Adicionar import: `from core.logging_config import setup_logging`
- [ ] Chamar `setup_logging()` no início do script
- [ ] Verificar que logs são gerados ao iniciar aplicação

### Substituir `print()` em `core/services/bible_api_client.py`
- [ ] Localizar todos os `print()` no arquivo
- [ ] Adicionar `import logging` e `logger = logging.getLogger(__name__)` no topo
- [ ] Substituir `print("AVISO: ...")` por `logger.warning(...)`
- [ ] Substituir `print("Erro na API da Bíblia: ...")` por `logger.error(..., exc_info=True)`
- [ ] Adicionar contexto (endpoint, parâmetros) aos logs de erro
- [ ] Verificar que stack traces são incluídos

### Substituir `print()` em `core/services/letras_scraper.py`
- [ ] Localizar todos os `print()` no arquivo
- [ ] Adicionar `import logging` e `logger = logging.getLogger(__name__)` no topo
- [ ] Substituir `print("AVISO: ...")` por `logger.warning(...)`
- [ ] Substituir `print("ERRO: ...")` por `logger.error(..., exc_info=True)`
- [ ] Adicionar contexto (URL) aos logs
- [ ] Verificar que stack traces são incluídos

### Substituir `print()` em `core/music_manager.py`
- [ ] Localizar todos os `print()` no arquivo
- [ ] Adicionar `import logging` e `logger = logging.getLogger(__name__)` no topo
- [ ] Substituir `print("Erro ao carregar...")` por `logger.error(..., exc_info=True)`
- [ ] Substituir `print("Erro ao salvar...")` por `logger.error(..., exc_info=True)`
- [ ] Adicionar contexto (caminho do arquivo) aos logs
- [ ] Verificar que stack traces são incluídos

### Substituir `print()` em `core/config_manager.py`
- [ ] Localizar todos os `print()` no arquivo
- [ ] Adicionar `import logging` e `logger = logging.getLogger(__name__)` no topo
- [ ] Substituir `print("Erro ao salvar...")` por `logger.error(..., exc_info=True)`
- [ ] Adicionar contexto (seção, chave) aos logs
- [ ] Verificar que stack traces são incluídos

### Substituir `print()` em `core/bible_manager.py`
- [ ] Localizar todos os `print()` no arquivo
- [ ] Adicionar `import logging` e `logger = logging.getLogger(__name__)` no topo
- [ ] Substituir `print("INFO: ...")` por `logger.info(...)`
- [ ] Substituir `print("AVISO: ...")` por `logger.warning(...)`
- [ ] Substituir `print("ERRO: ...")` por `logger.error(..., exc_info=True)`
- [ ] Adicionar contexto aos logs quando relevante
- [ ] Verificar que stack traces são incluídos em erros

### Substituir `print()` em `gui/dialogs.py`
- [ ] Localizar todos os `print()` no arquivo
- [ ] Adicionar `import logging` e `logger = logging.getLogger(__name__)` no topo
- [ ] Substituir `print("Erro ao centralizar...")` por `logger.error(..., exc_info=True)`
- [ ] Verificar que stack traces são incluídos

### Validação Final do Logging
- [ ] Executar aplicação e verificar que `logs/projetor.log` é criado
- [ ] Verificar que logs aparecem no console
- [ ] Verificar formato estruturado dos logs
- [ ] Testar cenários de erro e verificar stack traces
- [ ] Verificar que não há mais `print()` no código (usar grep: `grep -r "print(" --include="*.py"`)

---

## ✅ Tarefa 1.2: Criar Classes de Erro Personalizadas

### Criar `core/exceptions.py`
- [ ] Criar arquivo `core/exceptions.py`
- [ ] Criar classe base `ProjectorError(Exception)`
  - [ ] Adicionar docstring explicando propósito
- [ ] Criar `ConfigError(ProjectorError)`
  - [ ] Adicionar docstring
- [ ] Criar `ConfigSaveError(ConfigError)`
  - [ ] Adicionar docstring
- [ ] Criar `MusicDatabaseError(ProjectorError)`
  - [ ] Adicionar docstring
- [ ] Criar `BibleAPIError(ProjectorError)`
  - [ ] Adicionar docstring
- [ ] Criar `ScraperError(ProjectorError)`
  - [ ] Adicionar docstring
- [ ] Criar `ValidationError(ProjectorError)`
  - [ ] Adicionar docstring (será usado na Fase 2)

### Refatorar `core/config_manager.py`
- [ ] Adicionar import: `from core.exceptions import ConfigSaveError`
- [ ] Modificar `_save_config_file()` para levantar `ConfigSaveError` ao invés de retornar `False`
- [ ] Atualizar tratamento de erro onde `_save_config_file()` é chamado
- [ ] Logar erro antes de levantar exceção
- [ ] Verificar que mensagem de erro é informativa

### Refatorar `core/music_manager.py`
- [ ] Adicionar import: `from core.exceptions import MusicDatabaseError`
- [ ] Modificar `save_music_db()` para levantar `MusicDatabaseError` ao invés de retornar `False`
- [ ] Atualizar tratamento de erro em `add_music()` e `edit_music()`
- [ ] Logar erro antes de levantar exceção
- [ ] Verificar que mensagem de erro é informativa

### Refatorar `core/bible_manager.py`
- [ ] Adicionar import: `from core.exceptions import MusicDatabaseError` (ou criar `BibleCacheError`)
- [ ] Modificar `_save_books_to_cache()` para levantar exceção ao invés de apenas logar
- [ ] Atualizar tratamento de erro onde necessário
- [ ] Logar erro antes de levantar exceção

### Refatorar `core/services/bible_api_client.py`
- [ ] Adicionar import: `from core.exceptions import BibleAPIError`
- [ ] Modificar `_make_request()` para levantar `BibleAPIError` ao invés de retornar `None`
- [ ] Adicionar contexto ao erro (endpoint, status code)
- [ ] Atualizar métodos que usam `_make_request()` para tratar exceções
- [ ] Logar erro antes de levantar exceção
- [ ] Verificar que mensagens são informativas

### Refatorar `core/services/letras_scraper.py`
- [ ] Adicionar import: `from core.exceptions import ScraperError`
- [ ] Modificar `fetch_lyrics_from_url()` para levantar `ScraperError` ao invés de retornar `None`
- [ ] Criar diferentes tipos de erro se necessário (ex: `ScraperNetworkError`, `ScraperParseError`)
- [ ] Adicionar contexto ao erro (URL)
- [ ] Atualizar tratamento de erro nos controllers que usam o scraper
- [ ] Logar erro antes de levantar exceção

### Atualizar Controllers para Tratar Exceções
- [ ] Revisar `gui/controllers/music_controller.py`
  - [ ] Adicionar `try/except` para capturar exceções dos managers
  - [ ] Logar erros apropriadamente
  - [ ] Mostrar mensagens de erro ao usuário
- [ ] Revisar `gui/controllers/bible_controller.py`
  - [ ] Adicionar `try/except` para capturar exceções
  - [ ] Logar erros apropriadamente
  - [ ] Mostrar mensagens de erro ao usuário
- [ ] Verificar outros controllers se necessário

### Validação Final das Exceções
- [ ] Verificar que hierarquia de exceções está correta
- [ ] Testar cenários de erro e verificar que exceções são levantadas
- [ ] Verificar que erros são logados com contexto
- [ ] Verificar que usuário recebe mensagens claras
- [ ] Executar aplicação e testar funcionalidades que podem gerar erros

---

## ✅ Checklist de Critérios de Aceitação - Tarefa 1.1

- [ ] Todos os `print()` substituídos por logging
- [ ] Logs escritos em arquivo `logs/projetor.log`
- [ ] Logs também aparecem no console durante desenvolvimento
- [ ] Erros incluem stack trace completo
- [ ] Logs têm formato estruturado consistente
- [ ] Diretório `logs/` é criado automaticamente
- [ ] Logs incluem contexto relevante (IDs, URLs, etc.)

---

## ✅ Checklist de Critérios de Aceitação - Tarefa 1.2

- [ ] Hierarquia de exceções criada e documentada
- [ ] Métodos que retornavam `None` agora levantam exceções
- [ ] Todos os erros são capturados e tratados adequadamente
- [ ] Mensagens de erro são informativas para o usuário
- [ ] Erros são logados com contexto completo
- [ ] Controllers tratam exceções apropriadamente

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

**Status**: 🔄 Em Progresso  
**Última atualização**: [Data]  
**Progresso**: [ ] / [ ] tarefas concluídas

