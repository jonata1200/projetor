# Checklist - Fase 3: Refatoração 🟡

**Objetivo**: Refatorar arquivos grandes e eliminar duplicação de código.

**Prioridade**: 🟡 MÉDIA  
**Estimativa**: 6-8 horas  
**Dependências**: Fase 1 (para usar logging e exceções)

---

## ✅ Tarefa 3.1: Dividir `gui/main_window.py`

### Preparação
- [ ] Fazer backup do arquivo `gui/main_window.py`
- [ ] Verificar número atual de linhas (deve ser ~414)
- [ ] Criar diretório `gui/ui/` se não existir

### Criar `gui/ui/__init__.py`
- [ ] Criar arquivo `gui/ui/__init__.py` (vazio ou com exports)

### Criar `gui/ui/builders.py`
- [ ] Criar arquivo `gui/ui/builders.py`
- [ ] Adicionar imports necessários (`customtkinter as ctk`)
- [ ] Extrair função `create_top_bar(master, callbacks)`:
  - [ ] Copiar código de `_create_top_bar()` do `main_window.py`
  - [ ] Adaptar para receber callbacks como parâmetro
  - [ ] Retornar widgets criados
  - [ ] Adicionar docstring
- [ ] Extrair função `create_preview_pane(master)`:
  - [ ] Copiar código de `_create_preview_pane()` do `main_window.py`
  - [ ] Adaptar para ser independente
  - [ ] Retornar widgets criados
  - [ ] Adicionar docstring
- [ ] Extrair função `create_main_tabs(master)`:
  - [ ] Copiar código relacionado à criação de tabs
  - [ ] Adaptar para receber callbacks
  - [ ] Retornar widgets criados
  - [ ] Adicionar docstring

### Criar `gui/ui/top_bar.py`
- [ ] Criar arquivo `gui/ui/top_bar.py`
- [ ] Criar classe `TopBar(ctk.CTkFrame)`:
  - [ ] Mover lógica da barra superior para a classe
  - [ ] Adicionar métodos públicos necessários
  - [ ] Adicionar docstring da classe
- [ ] Tornar reutilizável e independente
- [ ] Testar classe isoladamente

### Criar `gui/ui/preview_pane.py`
- [ ] Criar arquivo `gui/ui/preview_pane.py`
- [ ] Criar classe `PreviewPane(ctk.CTkFrame)`:
  - [ ] Mover lógica do painel de pré-visualização para a classe
  - [ ] Adicionar métodos públicos necessários
  - [ ] Adicionar docstring da classe
- [ ] Tornar reutilizável e independente
- [ ] Testar classe isoladamente

### Refatorar `gui/main_window.py`
- [ ] Adicionar imports dos novos módulos:
  - [ ] `from gui.ui.builders import create_top_bar, create_preview_pane, create_main_tabs`
  - [ ] `from gui.ui.top_bar import TopBar`
  - [ ] `from gui.ui.preview_pane import PreviewPane`
- [ ] Refatorar `_create_top_bar()`:
  - [ ] Usar `create_top_bar()` ou instanciar `TopBar`
  - [ ] Remover código duplicado
- [ ] Refatorar `_create_preview_pane()`:
  - [ ] Usar `create_preview_pane()` ou instanciar `PreviewPane`
  - [ ] Remover código duplicado
- [ ] Refatorar criação de tabs:
  - [ ] Usar função extraída ou simplificar
  - [ ] Remover código duplicado
- [ ] Verificar que todas as referências a widgets ainda funcionam
- [ ] Remover métodos que foram extraídos
- [ ] Verificar que arquivo tem < 300 linhas

### Validação Final - Tarefa 3.1
- [ ] Contar linhas de `main_window.py` (deve ser < 300)
- [ ] Executar aplicação e verificar que funciona normalmente
- [ ] Testar todas as funcionalidades:
  - [ ] Barra superior
  - [ ] Pré-visualização
  - [ ] Tabs principais
  - [ ] Todas as interações

---

## ✅ Tarefa 3.2: Centralizar Lógica Duplicada (DRY)

### Criar `core/utils/__init__.py`
- [ ] Criar diretório `core/utils/` se não existir
- [ ] Criar arquivo `core/utils/__init__.py` (vazio ou com exports)

### Criar `core/utils/file_utils.py`
- [ ] Criar arquivo `core/utils/file_utils.py`
- [ ] Adicionar imports necessários:
  - [ ] `from pathlib import Path`
  - [ ] `import json`
  - [ ] `import logging`
  - [ ] `from core.exceptions import MusicDatabaseError` (ou exceção genérica)
- [ ] Implementar `ensure_directory_exists(file_path: Path)`:
  - [ ] Criar diretório se não existir
  - [ ] Adicionar docstring
- [ ] Implementar `save_json_file(file_path: Path, data: dict, ensure_ascii: bool = False) -> bool`:
  - [ ] Usar `ensure_directory_exists()` para criar diretório
  - [ ] Salvar arquivo JSON com encoding UTF-8
  - [ ] Adicionar indentação (2 espaços)
  - [ ] Tratar erros e levantar exceções apropriadas
  - [ ] Logar sucesso/erro
  - [ ] Adicionar docstring completa
- [ ] Implementar `load_json_file(file_path: Path, default: dict = None) -> dict`:
  - [ ] Verificar se arquivo existe
  - [ ] Carregar JSON com encoding UTF-8
  - [ ] Tratar erros (JSONDecodeError, IOError)
  - [ ] Retornar default se erro ou arquivo não existe
  - [ ] Logar warnings para erros
  - [ ] Adicionar docstring completa

### Refatorar `core/config_manager.py`
- [ ] Adicionar import: `from core.utils.file_utils import save_json_file`
- [ ] Modificar `_save_config_file()`:
  - [ ] Adaptar para usar `save_json_file()` ou substituir completamente
  - [ ] Manter compatibilidade com formato INI (se necessário)
  - [ ] OU criar função específica para INI se diferente de JSON
- [ ] Remover código duplicado de criação de diretório
- [ ] Remover código duplicado de salvamento
- [ ] Testar salvamento e carregamento de configuração

### Refatorar `core/music_manager.py`
- [ ] Adicionar imports:
  - [ ] `from core.utils.file_utils import save_json_file, load_json_file`
  - [ ] `from core.paths import MUSIC_DB_PATH`
- [ ] Modificar `load_music_db()`:
  - [ ] Usar `load_json_file()` ao invés de código duplicado
  - [ ] Remover código de abertura de arquivo
  - [ ] Remover código de criação de diretório
- [ ] Modificar `save_music_db()`:
  - [ ] Usar `save_json_file()` ao invés de código duplicado
  - [ ] Remover código de salvamento duplicado
  - [ ] Remover código de criação de diretório
- [ ] Testar carregamento e salvamento de músicas

### Refatorar `core/bible_manager.py`
- [ ] Adicionar imports:
  - [ ] `from core.utils.file_utils import save_json_file, load_json_file`
  - [ ] `from core.paths import BIBLE_BOOKS_CACHE_PATH`
- [ ] Modificar `_save_books_to_cache()`:
  - [ ] Usar `save_json_file()` ao invés de código duplicado
  - [ ] Remover código de salvamento duplicado
  - [ ] Remover código de criação de diretório
- [ ] Modificar `load_books()`:
  - [ ] Usar `load_json_file()` para carregar cache
  - [ ] Remover código de abertura de arquivo duplicado
- [ ] Testar cache de livros da Bíblia

### Validação Final - Tarefa 3.2
- [ ] Verificar que não há mais código duplicado de salvamento
- [ ] Verificar que todos os salvamentos usam `file_utils`
- [ ] Testar salvamento e carregamento de todos os arquivos:
  - [ ] Configuração
  - [ ] Base de músicas
  - [ ] Cache de livros da Bíblia
- [ ] Verificar logs para confirmar que tudo funciona

---

## ✅ Tarefa 3.3: Extrair Lógica de Centralização de Dialogs

### Criar `gui/utils/__init__.py`
- [ ] Criar diretório `gui/utils/` se não existir
- [ ] Criar arquivo `gui/utils/__init__.py` (vazio ou com exports)

### Criar `gui/utils/dialog_utils.py`
- [ ] Criar arquivo `gui/utils/dialog_utils.py`
- [ ] Implementar função `center_dialog(dialog, master)`:
  - [ ] Calcular posição centralizada
  - [ ] Lidar com casos edge (janela minimizada, etc.)
  - [ ] Adicionar tratamento de erros
  - [ ] Adicionar docstring completa
  - [ ] Tornar robusta e reutilizável

### Refatorar `gui/dialogs.py`
- [ ] Adicionar import: `from gui.utils.dialog_utils import center_dialog`
- [ ] Remover método `_center_window()` de `AddEditSongDialog`:
  - [ ] Substituir chamadas por `center_dialog(self, self.master)`
  - [ ] Remover código duplicado
- [ ] Remover método `_center_window()` de `SettingsDialog`:
  - [ ] Substituir chamadas por `center_dialog(self, self.master)`
  - [ ] Remover método `_do_center()` também se existir
  - [ ] Remover código duplicado
- [ ] Remover método `_center_window()` de `ShortcutsHelpDialog`:
  - [ ] Substituir chamadas por `center_dialog(self, self.master)`
  - [ ] Remover código duplicado
- [ ] Verificar outros dialogs se houver

### Validação Final - Tarefa 3.3
- [ ] Verificar que todos os dialogs centralizam corretamente
- [ ] Testar abertura de cada dialog:
  - [ ] AddEditSongDialog
  - [ ] SettingsDialog
  - [ ] ShortcutsHelpDialog
- [ ] Verificar que não há mais código duplicado de centralização

---

## ✅ Checklist de Critérios de Aceitação - Tarefa 3.1

- [ ] `main_window.py` tem < 300 linhas
- [ ] Componentes são reutilizáveis
- [ ] Funcionalidade existente mantida
- [ ] Código mais fácil de testar
- [ ] Estrutura de pastas organizada (`gui/ui/`)

---

## ✅ Checklist de Critérios de Aceitação - Tarefa 3.2

- [ ] Lógica de salvamento centralizada
- [ ] Sem duplicação de código
- [ ] Tratamento de erros consistente
- [ ] Todos os salvamentos usam os mesmos utilitários
- [ ] Funções utilitárias são bem documentadas

---

## ✅ Checklist de Critérios de Aceitação - Tarefa 3.3

- [ ] Lógica de centralização não está duplicada
- [ ] Todos os dialogs usam a mesma função
- [ ] Funcionalidade mantida
- [ ] Código mais limpo e organizado

---

## ✅ Testes Manuais Completos

### Testar Funcionalidades Principais
- [ ] Abrir aplicação → deve funcionar normalmente
- [ ] Navegar entre tabs → deve funcionar
- [ ] Usar pré-visualização → deve funcionar
- [ ] Adicionar música → deve funcionar
- [ ] Editar música → deve funcionar
- [ ] Carregar versículos → deve funcionar
- [ ] Salvar configurações → deve funcionar
- [ ] Abrir dialogs → devem centralizar corretamente

### Testar Salvamento de Dados
- [ ] Adicionar música → verificar que salva em arquivo
- [ ] Editar música → verificar que salva alterações
- [ ] Salvar configuração → verificar que salva
- [ ] Carregar cache da Bíblia → verificar que funciona

### Testar Estrutura
- [ ] Verificar que `main_window.py` tem < 300 linhas
- [ ] Verificar que componentes estão em `gui/ui/`
- [ ] Verificar que utilitários estão em `core/utils/`
- [ ] Verificar que não há código duplicado

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

**Status**: 🔄 Em Progresso  
**Última atualização**: [Data]  
**Progresso**: [ ] / [ ] tarefas concluídas

