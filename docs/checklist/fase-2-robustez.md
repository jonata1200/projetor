# Checklist - Fase 2: Robustez 🔴

**Objetivo**: Implementar validação de entrada e padrão Fail Fast.

**Prioridade**: 🔴 ALTA  
**Estimativa**: 3-4 horas  
**Dependências**: Fase 1 (para usar exceções customizadas)

---

## ✅ Tarefa 2.1: Criar Módulo de Validação

### Criar `core/validators.py`
- [x] Criar arquivo `core/validators.py`
- [x] Adicionar imports necessários (`re`, `urllib.parse` para URLs)
- [x] Importar `ValidationError` de `core.exceptions`

### Implementar `validate_string()`
- [x] Criar função `validate_string(value, field_name, min_length=1, max_length=None)`
- [x] Validar que `value` é string
- [x] Validar que não é `None`
- [x] Validar `min_length`
- [x] Validar `max_length` (se fornecido)
- [x] Levantar `ValidationError` com mensagem clara se inválido
- [x] Adicionar docstring com exemplos
- [x] Retornar valor validado (stripado)

### Implementar `validate_url()`
- [x] Criar função `validate_url(url, allowed_domains=None)`
- [x] Validar formato básico de URL
- [x] Validar domínios permitidos (se fornecido)
- [x] Validar esquema (http/https)
- [x] Levantar `ValidationError` com mensagem clara se inválido
- [x] Adicionar docstring com exemplos
- [x] Retornar URL validada

### Implementar `validate_int()`
- [x] Criar função `validate_int(value, field_name, min_value=None, max_value=None)`
- [x] Validar que `value` pode ser convertido para int
- [x] Validar `min_value` (se fornecido)
- [x] Validar `max_value` (se fornecido)
- [x] Levantar `ValidationError` com mensagem clara se inválido
- [x] Adicionar docstring com exemplos
- [x] Retornar valor como int

### Implementar `validate_color()`
- [x] Criar função `validate_color(color_value)`
- [x] Validar formato hex (#RRGGBB)
- [x] Validar nomes de cores comuns (white, black, etc.)
- [x] Levantar `ValidationError` com mensagem clara se inválido
- [x] Adicionar docstring com exemplos
- [x] Retornar cor validada

### Implementar `validate_font_size()`
- [x] Criar função `validate_font_size(size)`
- [x] Validar que é um número positivo
- [x] Validar range razoável (ex: 8-200)
- [x] Levantar `ValidationError` com mensagem clara se inválido
- [x] Adicionar docstring com exemplos
- [x] Retornar tamanho como int

### Adicionar Validação em `core/music_manager.py`
- [x] Adicionar import: `from core.validators import validate_string`
- [x] Adicionar import: `from core.exceptions import ValidationError`
- [x] Modificar `add_music()`:
  - [x] Validar `title` no início (Fail Fast)
  - [x] Validar `artist` no início
  - [x] Validar `lyrics_full` no início
  - [x] Levantar `ValidationError` se alguma validação falhar
- [x] Modificar `edit_music()`:
  - [x] Adicionar mesmas validações no início
  - [x] Levantar `ValidationError` se alguma validação falhar

### Adicionar Validação em `core/config_manager.py`
- [x] Adicionar imports necessários dos validators
- [x] Modificar `set_setting()`:
  - [x] Identificar tipo de setting (font_size, color, etc.)
  - [x] Validar valor conforme tipo
  - [x] Levantar `ValidationError` se inválido
  - [x] Fail Fast antes de processar

### Adicionar Validação em `core/services/letras_scraper.py`
- [x] Adicionar import: `from core.validators import validate_url`
- [x] Modificar `fetch_lyrics_from_url()`:
  - [x] Validar URL no início da função
  - [x] Validar domínio permitido (letras.mus.br)
  - [x] Levantar `ValidationError` se URL inválida

### Criar/Atualizar `ValidationError` em `core/exceptions.py`
- [x] Verificar que `ValidationError` já existe (criado na Fase 1)
- [x] Se não existe, criar: `class ValidationError(ProjectorError)`
- [x] Adicionar docstring explicando uso

---

## ✅ Tarefa 2.2: Implementar Validação de Entrada no Frontend

### Modificar `gui/dialogs.py` - AddEditSongDialog
- [x] Adicionar import: `from core.validators import validate_string`
- [x] Adicionar import: `from core.exceptions import ValidationError`
- [x] Modificar `on_save()`:
  - [x] Validar campos antes de processar
  - [x] Capturar `ValidationError`
  - [x] Mostrar mensagem de erro ao usuário
  - [x] Prevenir salvamento se inválido
  - [x] Destacar campos inválidos visualmente (opcional)

### Modificar `gui/controllers/music_controller.py`
- [x] Adicionar import: `from core.exceptions import ValidationError`
- [x] Modificar `show_add_dialog()`:
  - [x] Adicionar `try/except ValidationError`
  - [x] Mostrar mensagem de erro ao usuário
  - [x] Logar erro apropriadamente
- [x] Modificar `show_edit_dialog()`:
  - [x] Adicionar `try/except ValidationError`
  - [x] Mostrar mensagem de erro ao usuário
  - [x] Logar erro apropriadamente

### Modificar `gui/controllers/music_controller.py` - Importação
- [x] Modificar `show_import_dialog()`:
  - [x] Validar URL antes de enviar para scraper
  - [x] Adicionar `try/except ValidationError`
  - [x] Mostrar mensagem de erro se URL inválida
- [x] Modificar `_on_import_finished()`:
  - [x] Validar dados retornados do scraper
  - [x] Adicionar tratamento de `ValidationError`

### Modificar `gui/controllers/bible_controller.py`
- [x] Adicionar import: `from core.exceptions import ValidationError`
- [x] Adicionar validação de seleções:
  - [x] Validar que versão foi selecionada
  - [x] Validar que livro foi selecionado
  - [x] Validar que capítulo foi selecionado
  - [x] Mostrar mensagem se validação falhar

### Adicionar Feedback Visual (Opcional mas Recomendado)
- [x] Revisar dialogs para destacar campos inválidos
- [x] Adicionar mensagens de erro próximas aos campos
- [x] Melhorar UX mostrando o que está errado

---

## ✅ Checklist de Critérios de Aceitação - Tarefa 2.1

- [x] Todas as entradas são validadas no início das funções
- [x] Validações falham rápido (antes de processamento)
- [x] Mensagens de erro de validação são claras
- [x] Validações incluem tipos e valores
- [x] Módulo `validators.py` está completo e documentado
- [x] Validações são consistentes em todo o código

---

## ✅ Checklist de Critérios de Aceitação - Tarefa 2.2

- [x] Validação acontece antes de processar
- [x] Usuário recebe feedback imediato
- [x] Formulários não são submetidos se inválidos
- [x] Mensagens de erro são claras e orientam o usuário
- [x] Erros de validação são logados

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

**Status**: ✅ Concluída  
**Última atualização**: 2024  
**Progresso**: [x] / [x] tarefas concluídas

