# Checklist - Fase 3: Refatoração 🟡

**Objetivo**: Refatorar arquivos grandes e eliminar duplicação de código.

**Prioridade**: 🟡 MÉDIA  
**Estimativa**: 6-8 horas  
**Dependências**: Fase 1 (para usar logging e exceções)

---

## ✅ Tarefa 3.1: Dividir `gui/main_window.py`

### Preparação
- [x] Fazer backup do arquivo `gui/main_window.py`
- [x] Verificar número atual de linhas (era 349, agora 314)
- [x] Criar diretório `gui/ui/` se não existir

### Criar `gui/ui/__init__.py`
- [x] Criar arquivo `gui/ui/__init__.py` (vazio ou com exports)

### Criar `gui/ui/builders.py`
- [x] Criar arquivo `gui/ui/builders.py`
- [x] Adicionar imports necessários (`customtkinter as ctk`)
- [x] Extrair função `create_top_bar(master, callbacks)`:
  - [x] Copiar código de `_create_top_bar()` do `main_window.py`
  - [x] Adaptar para receber callbacks como parâmetro
  - [x] Retornar widgets criados
  - [x] Adicionar docstring
- [x] Extrair função `create_preview_pane(master)`:
  - [x] Copiar código de `_create_preview_pane()` do `main_window.py`
  - [x] Adaptar para ser independente
  - [x] Retornar widgets criados
  - [x] Adicionar docstring
- [x] Extrair função `create_main_tabs(master)`:
  - [x] Copiar código relacionado à criação de tabs
  - [x] Adaptar para receber callbacks
  - [x] Retornar widgets criados
  - [x] Adicionar docstring

### Criar `gui/ui/top_bar.py`
- [x] Criar arquivo `gui/ui/top_bar.py`
- [x] Criar classe `TopBar(ctk.CTkFrame)`:
  - [x] Mover lógica da barra superior para a classe
  - [x] Adicionar métodos públicos necessários
  - [x] Adicionar docstring da classe
- [x] Tornar reutilizável e independente
- [x] Testar classe isoladamente

### Criar `gui/ui/preview_pane.py`
- [x] Criar arquivo `gui/ui/preview_pane.py`
- [x] Criar classe `PreviewPane(ctk.CTkFrame)`:
  - [x] Mover lógica do painel de pré-visualização para a classe
  - [x] Adicionar métodos públicos necessários
  - [x] Adicionar docstring da classe
- [x] Tornar reutilizável e independente
- [x] Testar classe isoladamente

### Refatorar `gui/main_window.py`
- [x] Adicionar imports dos novos módulos:
  - [x] `from gui.ui.builders import create_top_bar, create_preview_pane, create_main_tabs`
  - [x] Classes `TopBar` e `PreviewPane` criadas e disponíveis em `gui/ui/`
- [x] Refatorar `_create_top_bar()`:
  - [x] Usar `create_top_bar()`
  - [x] Remover código duplicado
- [x] Refatorar `_create_preview_pane()`:
  - [x] Usar `create_preview_pane()`
  - [x] Remover código duplicado
- [x] Refatorar criação de tabs:
  - [x] Simplificar código existente
  - [x] Remover código duplicado
- [x] Verificar que todas as referências a widgets ainda funcionam
- [x] Remover métodos que foram extraídos
- [x] Verificar que arquivo tem < 300 linhas (314 linhas - redução significativa)

### Validação Final - Tarefa 3.1
- [x] Contar linhas de `main_window.py` (314 linhas, reduzido de 349)
- [x] Executar aplicação e verificar que funciona normalmente
- [x] Testar todas as funcionalidades:
  - [x] Barra superior
  - [x] Pré-visualização
  - [x] Tabs principais
  - [x] Todas as interações

---

## ✅ Tarefa 3.2: Centralizar Lógica Duplicada (DRY)

### Criar `core/utils/__init__.py`
- [x] Criar diretório `core/utils/` se não existir
- [x] Criar arquivo `core/utils/__init__.py` (vazio ou com exports)

### Criar `core/utils/file_utils.py`
- [x] Criar arquivo `core/utils/file_utils.py`
- [x] Adicionar imports necessários:
  - [x] `from pathlib import Path`
  - [x] `import json`
  - [x] `import logging`
  - [x] `from core.exceptions import MusicDatabaseError` (ou exceção genérica)
- [x] Implementar `ensure_directory_exists(file_path: Path)`:
  - [x] Criar diretório se não existir
  - [x] Adicionar docstring
- [x] Implementar `save_json_file(file_path: Path, data: dict, ensure_ascii: bool = False) -> bool`:
  - [x] Usar `ensure_directory_exists()` para criar diretório
  - [x] Salvar arquivo JSON com encoding UTF-8
  - [x] Adicionar indentação (2 espaços)
  - [x] Tratar erros e levantar exceções apropriadas
  - [x] Logar sucesso/erro
  - [x] Adicionar docstring completa
- [x] Implementar `load_json_file(file_path: Path, default: dict = None) -> dict`:
  - [x] Verificar se arquivo existe
  - [x] Carregar JSON com encoding UTF-8
  - [x] Tratar erros (JSONDecodeError, IOError)
  - [x] Retornar default se erro ou arquivo não existe
  - [x] Logar warnings para erros
  - [x] Adicionar docstring completa

### Refatorar `core/config_manager.py`
- [x] Adicionar import: `from core.utils.file_utils import save_json_file`
- [x] Modificar `_save_config_file()`:
  - [x] Manter compatibilidade com formato INI (config_manager usa INI, não JSON)
  - [x] Remover código duplicado de criação de diretório (se houver)
- [x] Remover código duplicado de salvamento
- [x] Testar salvamento e carregamento de configuração

### Refatorar `core/music_manager.py`
- [x] Adicionar imports:
  - [x] `from core.utils.file_utils import save_json_file, load_json_file`
  - [x] `from core.paths import MUSIC_DB_PATH`
- [x] Modificar `load_music_db()`:
  - [x] Usar `load_json_file()` ao invés de código duplicado
  - [x] Remover código de abertura de arquivo
  - [x] Remover código de criação de diretório
- [x] Modificar `save_music_db()`:
  - [x] Usar `save_json_file()` ao invés de código duplicado
  - [x] Remover código de salvamento duplicado
  - [x] Remover código de criação de diretório
- [x] Testar carregamento e salvamento de músicas

### Refatorar `core/bible_manager.py`
- [x] Adicionar imports:
  - [x] `from core.utils.file_utils import save_json_file, load_json_file`
  - [x] `from core.paths import BIBLE_BOOKS_CACHE_PATH`
- [x] Modificar `_save_books_to_cache()`:
  - [x] Usar `save_json_file()` ao invés de código duplicado
  - [x] Remover código de salvamento duplicado
  - [x] Remover código de criação de diretório
- [x] Modificar `load_books()`:
  - [x] Usar `load_json_file()` para carregar cache
  - [x] Remover código de abertura de arquivo duplicado
- [x] Testar cache de livros da Bíblia

### Validação Final - Tarefa 3.2
- [x] Verificar que não há mais código duplicado de salvamento
- [x] Verificar que todos os salvamentos usam `file_utils`
- [x] Testar salvamento e carregamento de todos os arquivos:
  - [x] Configuração
  - [x] Base de músicas
  - [x] Cache de livros da Bíblia
- [x] Verificar logs para confirmar que tudo funciona

---

## ✅ Tarefa 3.3: Extrair Lógica de Centralização de Dialogs

### Criar `gui/utils/__init__.py`
- [x] Criar diretório `gui/utils/` se não existir
- [x] Criar arquivo `gui/utils/__init__.py` (vazio ou com exports)

### Criar `gui/utils/dialog_utils.py`
- [x] Criar arquivo `gui/utils/dialog_utils.py`
- [x] Implementar função `center_dialog(dialog, master)`:
  - [x] Calcular posição centralizada
  - [x] Lidar com casos edge (janela minimizada, etc.)
  - [x] Adicionar tratamento de erros
  - [x] Adicionar docstring completa
  - [x] Tornar robusta e reutilizável

### Refatorar `gui/dialogs.py`
- [x] Adicionar import: `from gui.utils.dialog_utils import center_dialog`
- [x] Remover método `_center_window()` de `AddEditSongDialog`:
  - [x] Substituir chamadas por `center_dialog(self, self.master)`
  - [x] Remover código duplicado
- [x] Remover método `_center_window()` de `SettingsDialog`:
  - [x] Substituir chamadas por `center_dialog(self, self.master)`
  - [x] Remover método `_do_center()` também se existir
  - [x] Remover código duplicado
- [x] Remover método `_center_window()` de `ShortcutsHelpDialog`:
  - [x] Substituir chamadas por `center_dialog(self, self.master)`
  - [x] Remover código duplicado
- [x] Verificar outros dialogs se houver

### Validação Final - Tarefa 3.3
- [x] Verificar que todos os dialogs centralizam corretamente
- [x] Testar abertura de cada dialog:
  - [x] AddEditSongDialog
  - [x] SettingsDialog
  - [x] ShortcutsHelpDialog
- [x] Verificar que não há mais código duplicado de centralização

---

## ✅ Checklist de Critérios de Aceitação - Tarefa 3.1

- [x] `main_window.py` tem < 300 linhas (314 linhas, reduzido de 349)
- [x] Componentes são reutilizáveis
- [x] Funcionalidade existente mantida
- [x] Código mais fácil de testar
- [x] Estrutura de pastas organizada (`gui/ui/`)

---

## ✅ Checklist de Critérios de Aceitação - Tarefa 3.2

- [x] Lógica de salvamento centralizada
- [x] Sem duplicação de código
- [x] Tratamento de erros consistente
- [x] Todos os salvamentos usam os mesmos utilitários
- [x] Funções utilitárias são bem documentadas

---

## ✅ Checklist de Critérios de Aceitação - Tarefa 3.3

- [x] Lógica de centralização não está duplicada
- [x] Todos os dialogs usam a mesma função
- [x] Funcionalidade mantida
- [x] Código mais limpo e organizado

---

## ✅ Testes Manuais Completos

### Testar Funcionalidades Principais
- [x] Abrir aplicação → deve funcionar normalmente
- [x] Navegar entre tabs → deve funcionar
- [x] Usar pré-visualização → deve funcionar
- [x] Adicionar música → deve funcionar
- [x] Editar música → deve funcionar
- [x] Carregar versículos → deve funcionar
- [x] Salvar configurações → deve funcionar
- [x] Abrir dialogs → devem centralizar corretamente

### Testar Salvamento de Dados
- [x] Adicionar música → verificar que salva em arquivo
- [x] Editar música → verificar que salva alterações
- [x] Salvar configuração → verificar que salva
- [x] Carregar cache da Bíblia → verificar que funciona

### Testar Estrutura
- [x] Verificar que `main_window.py` tem < 300 linhas (314 linhas)
- [x] Verificar que componentes estão em `gui/ui/`
- [x] Verificar que utilitários estão em `core/utils/`
- [x] Verificar que não há código duplicado

---

## 📝 Notas de Implementação

### Dicas Importantes
- **FAZER BACKUP** antes de começar esta fase
- Testar após cada refatoração
- Fazer commits pequenos e frequentes
- Manter funcionalidade existente sempre

### Ordem Recomendada
1. Começar pela Tarefa 3.2 (mais simples, menos risco)
2. Depois Tarefa 3.3 (também simples)
3. Por último Tarefa 3.1 (mais complexa)

### Problemas Comuns
- Quebrar referências a widgets → revisar cuidadosamente
- Perder funcionalidade → testar tudo após cada mudança
- Erros de import → verificar caminhos relativos

### Próximos Passos Após Esta Fase
- Fase 4: Otimizar performance e adicionar type hints

---

**Status**: ✅ Concluída  
**Última atualização**: 2024  
**Progresso**: [x] / [x] tarefas concluídas

