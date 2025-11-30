# Checklist - Fase 2: Robustez 🔴

**Objetivo**: Implementar validação de entrada e padrão Fail Fast.

**Prioridade**: 🔴 ALTA  
**Estimativa**: 3-4 horas  
**Dependências**: Fase 1 (para usar exceções customizadas)

---

## ✅ Tarefa 2.1: Criar Módulo de Validação

### Criar `core/validators.py`
- [ ] Criar arquivo `core/validators.py`
- [ ] Adicionar imports necessários (`re`, `urllib.parse` para URLs)
- [ ] Importar `ValidationError` de `core.exceptions`

### Implementar `validate_string()`
- [ ] Criar função `validate_string(value, field_name, min_length=1, max_length=None)`
- [ ] Validar que `value` é string
- [ ] Validar que não é `None`
- [ ] Validar `min_length`
- [ ] Validar `max_length` (se fornecido)
- [ ] Levantar `ValidationError` com mensagem clara se inválido
- [ ] Adicionar docstring com exemplos
- [ ] Retornar valor validado (stripado)

### Implementar `validate_url()`
- [ ] Criar função `validate_url(url, allowed_domains=None)`
- [ ] Validar formato básico de URL
- [ ] Validar domínios permitidos (se fornecido)
- [ ] Validar esquema (http/https)
- [ ] Levantar `ValidationError` com mensagem clara se inválido
- [ ] Adicionar docstring com exemplos
- [ ] Retornar URL validada

### Implementar `validate_int()`
- [ ] Criar função `validate_int(value, field_name, min_value=None, max_value=None)`
- [ ] Validar que `value` pode ser convertido para int
- [ ] Validar `min_value` (se fornecido)
- [ ] Validar `max_value` (se fornecido)
- [ ] Levantar `ValidationError` com mensagem clara se inválido
- [ ] Adicionar docstring com exemplos
- [ ] Retornar valor como int

### Implementar `validate_color()`
- [ ] Criar função `validate_color(color_value)`
- [ ] Validar formato hex (#RRGGBB)
- [ ] Validar nomes de cores comuns (white, black, etc.)
- [ ] Levantar `ValidationError` com mensagem clara se inválido
- [ ] Adicionar docstring com exemplos
- [ ] Retornar cor validada

### Implementar `validate_font_size()`
- [ ] Criar função `validate_font_size(size)`
- [ ] Validar que é um número positivo
- [ ] Validar range razoável (ex: 8-200)
- [ ] Levantar `ValidationError` com mensagem clara se inválido
- [ ] Adicionar docstring com exemplos
- [ ] Retornar tamanho como int

### Adicionar Validação em `core/music_manager.py`
- [ ] Adicionar import: `from core.validators import validate_string`
- [ ] Adicionar import: `from core.exceptions import ValidationError`
- [ ] Modificar `add_music()`:
  - [ ] Validar `title` no início (Fail Fast)
  - [ ] Validar `artist` no início
  - [ ] Validar `lyrics_full` no início
  - [ ] Levantar `ValidationError` se alguma validação falhar
- [ ] Modificar `edit_music()`:
  - [ ] Adicionar mesmas validações no início
  - [ ] Levantar `ValidationError` se alguma validação falhar

### Adicionar Validação em `core/config_manager.py`
- [ ] Adicionar imports necessários dos validators
- [ ] Modificar `set_setting()`:
  - [ ] Identificar tipo de setting (font_size, color, etc.)
  - [ ] Validar valor conforme tipo
  - [ ] Levantar `ValidationError` se inválido
  - [ ] Fail Fast antes de processar

### Adicionar Validação em `core/services/letras_scraper.py`
- [ ] Adicionar import: `from core.validators import validate_url`
- [ ] Modificar `fetch_lyrics_from_url()`:
  - [ ] Validar URL no início da função
  - [ ] Validar domínio permitido (letras.mus.br)
  - [ ] Levantar `ValidationError` se URL inválida

### Criar/Atualizar `ValidationError` em `core/exceptions.py`
- [ ] Verificar que `ValidationError` já existe (criado na Fase 1)
- [ ] Se não existe, criar: `class ValidationError(ProjectorError)`
- [ ] Adicionar docstring explicando uso

---

## ✅ Tarefa 2.2: Implementar Validação de Entrada no Frontend

### Modificar `gui/dialogs.py` - AddEditSongDialog
- [ ] Adicionar import: `from core.validators import validate_string`
- [ ] Adicionar import: `from core.exceptions import ValidationError`
- [ ] Modificar `on_save()`:
  - [ ] Validar campos antes de processar
  - [ ] Capturar `ValidationError`
  - [ ] Mostrar mensagem de erro ao usuário
  - [ ] Prevenir salvamento se inválido
  - [ ] Destacar campos inválidos visualmente (opcional)

### Modificar `gui/controllers/music_controller.py`
- [ ] Adicionar import: `from core.exceptions import ValidationError`
- [ ] Modificar `show_add_dialog()`:
  - [ ] Adicionar `try/except ValidationError`
  - [ ] Mostrar mensagem de erro ao usuário
  - [ ] Logar erro apropriadamente
- [ ] Modificar `show_edit_dialog()`:
  - [ ] Adicionar `try/except ValidationError`
  - [ ] Mostrar mensagem de erro ao usuário
  - [ ] Logar erro apropriadamente

### Modificar `gui/controllers/music_controller.py` - Importação
- [ ] Modificar `show_import_dialog()`:
  - [ ] Validar URL antes de enviar para scraper
  - [ ] Adicionar `try/except ValidationError`
  - [ ] Mostrar mensagem de erro se URL inválida
- [ ] Modificar `_on_import_finished()`:
  - [ ] Validar dados retornados do scraper
  - [ ] Adicionar tratamento de `ValidationError`

### Modificar `gui/controllers/bible_controller.py`
- [ ] Adicionar import: `from core.exceptions import ValidationError`
- [ ] Adicionar validação de seleções:
  - [ ] Validar que versão foi selecionada
  - [ ] Validar que livro foi selecionado
  - [ ] Validar que capítulo foi selecionado
  - [ ] Mostrar mensagem se validação falhar

### Adicionar Feedback Visual (Opcional mas Recomendado)
- [ ] Revisar dialogs para destacar campos inválidos
- [ ] Adicionar mensagens de erro próximas aos campos
- [ ] Melhorar UX mostrando o que está errado

---

## ✅ Checklist de Critérios de Aceitação - Tarefa 2.1

- [ ] Todas as entradas são validadas no início das funções
- [ ] Validações falham rápido (antes de processamento)
- [ ] Mensagens de erro de validação são claras
- [ ] Validações incluem tipos e valores
- [ ] Módulo `validators.py` está completo e documentado
- [ ] Validações são consistentes em todo o código

---

## ✅ Checklist de Critérios de Aceitação - Tarefa 2.2

- [ ] Validação acontece antes de processar
- [ ] Usuário recebe feedback imediato
- [ ] Formulários não são submetidos se inválidos
- [ ] Mensagens de erro são claras e orientam o usuário
- [ ] Erros de validação são logados

---

## ✅ Testes Manuais

### Testar Validação de Música
- [ ] Tentar adicionar música com título vazio → deve falhar
- [ ] Tentar adicionar música com artista vazio → deve falhar
- [ ] Tentar adicionar música com letra vazia → deve falhar
- [ ] Verificar mensagem de erro clara
- [ ] Verificar que não salva dados inválidos

### Testar Validação de URL
- [ ] Tentar importar música com URL inválida → deve falhar
- [ ] Tentar importar música com URL de domínio diferente → deve falhar
- [ ] Tentar importar música com URL válida → deve funcionar
- [ ] Verificar mensagem de erro clara

### Testar Validação de Configuração
- [ ] Tentar salvar tamanho de fonte inválido (ex: negativo) → deve falhar
- [ ] Tentar salvar tamanho de fonte muito grande → deve falhar (se limite definido)
- [ ] Tentar salvar cor inválida → deve falhar
- [ ] Verificar mensagem de erro clara

### Testar Fail Fast
- [ ] Verificar que validação acontece antes de qualquer processamento
- [ ] Verificar que não há mudanças parciais em dados inválidos
- [ ] Verificar logs para confirmar que falhou rapidamente

---

## 📝 Notas de Implementação

### Dicas
- Testar cada validador isoladamente antes de integrar
- Usar mensagens de erro descritivas
- Considerar criar testes unitários para validadores (Fase 5)

### Validações Importantes
- Strings: não vazias, não None, tamanho mínimo/máximo
- URLs: formato válido, domínio permitido
- Inteiros: tipo correto, range válido
- Cores: formato hex ou nome válido
- Font size: número positivo, range razoável

### Próximos Passos Após Esta Fase
- Fase 3: Refatoração e modularização
- Fase 4: Performance e tipagem

---

**Status**: 🔄 Em Progresso  
**Última atualização**: [Data]  
**Progresso**: [ ] / [ ] tarefas concluídas

