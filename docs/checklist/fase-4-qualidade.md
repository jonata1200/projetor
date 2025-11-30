# Checklist - Fase 4: Qualidade 🟡

**Objetivo**: Otimizar performance e adicionar type hints.

**Prioridade**: 🟡 MÉDIA  
**Estimativa**: 5-7 horas  
**Dependências**: Fase 1 (para usar logging)

---

## ✅ Tarefa 4.1: Otimizar Performance com Índices

### Preparação
- [ ] Revisar código atual de `core/music_manager.py`
- [ ] Identificar métodos que fazem busca linear (O(n))

### Adicionar Índices em `MusicManager`
- [ ] Adicionar atributos de índice no `__init__()`:
  - [ ] `self._music_index: Dict[str, dict] = {}`
  - [ ] `self._title_artist_index: Dict[Tuple[str, str], str] = {}`
- [ ] Criar método `_rebuild_indexes()`:
  - [ ] Limpar índices existentes
  - [ ] Construir `_music_index` (ID → música)
  - [ ] Construir `_title_artist_index` ((title, artist) → ID)
  - [ ] Adicionar docstring
  - [ ] Logar se houver problemas

### Modificar `load_music_db()` para Reconstruir Índices
- [ ] Chamar `_rebuild_indexes()` após carregar dados
- [ ] Verificar que índices são construídos corretamente

### Refatorar `get_music_by_id()`
- [ ] Modificar para usar `_music_index.get(music_id)` (O(1))
- [ ] Remover loop linear
- [ ] Adicionar log se música não encontrada (opcional)
- [ ] Manter compatibilidade (retornar `None` se não encontrado)

### Refatorar `is_duplicate()`
- [ ] Modificar para usar `_title_artist_index` (O(1))
- [ ] Criar chave: `(title.lower().strip(), artist.lower().strip())`
- [ ] Verificar se chave existe no índice
- [ ] Remover loop linear
- [ ] Adicionar docstring atualizada

### Atualizar Métodos que Modificam Dados
- [ ] Modificar `add_music()`:
  - [ ] Chamar `_rebuild_indexes()` após adicionar
  - [ ] OU atualizar índices incrementalmente (mais eficiente)
- [ ] Modificar `edit_music()`:
  - [ ] Atualizar índices após editar
  - [ ] OU chamar `_rebuild_indexes()`
- [ ] Modificar `delete_music()`:
  - [ ] Atualizar índices após deletar
  - [ ] OU chamar `_rebuild_indexes()`

### Otimização Incremental (Opcional mas Recomendado)
- [ ] Implementar atualização incremental dos índices:
  - [ ] Adicionar música ao índice ao adicionar
  - [ ] Atualizar índice ao editar
  - [ ] Remover do índice ao deletar
- [ ] Isso evita reconstruir índices toda vez

### Validação Final - Tarefa 4.1
- [ ] Testar busca por ID com base grande (criar dados de teste se necessário)
- [ ] Testar verificação de duplicata
- [ ] Verificar que índices são mantidos consistentes
- [ ] Verificar que performance melhorou (teste com muitas músicas)

---

## ✅ Tarefa 4.2: Adicionar Type Hints

### Criar `core/types.py`
- [ ] Criar arquivo `core/types.py`
- [ ] Adicionar imports: `from typing import Dict, Any`
- [ ] Definir tipos customizados:
  - [ ] `MusicData = Dict[str, Any]`
  - [ ] `BibleBook = Dict[str, Any]`
  - [ ] `Slide = str`
  - [ ] Outros tipos relevantes
- [ ] Adicionar docstrings explicando cada tipo

### Adicionar Type Hints em `core/music_manager.py`
- [ ] Adicionar imports: `from typing import Optional, List, Dict`
- [ ] Adicionar type hints em `__init__()`:
  - [ ] `-> None`
- [ ] Adicionar type hints em `load_music_db()`:
  - [ ] `-> List[MusicData]`
- [ ] Adicionar type hints em `save_music_db()`:
  - [ ] `-> bool`
- [ ] Adicionar type hints em `get_music_by_id()`:
  - [ ] `(music_id: str) -> Optional[MusicData]`
- [ ] Adicionar type hints em `is_duplicate()`:
  - [ ] `(title: str, artist: str) -> bool`
- [ ] Adicionar type hints em todos os outros métodos

### Adicionar Type Hints em `core/bible_manager.py`
- [ ] Adicionar imports necessários do `typing`
- [ ] Adicionar type hints em todos os métodos públicos
- [ ] Usar tipos customizados de `core.types` quando apropriado

### Adicionar Type Hints em `core/config_manager.py`
- [ ] Adicionar imports necessários do `typing`
- [ ] Adicionar type hints em todos os métodos
- [ ] Especificar tipos de retorno (`Optional[str]`, etc.)

### Adicionar Type Hints em Controllers
- [ ] Adicionar type hints em `gui/controllers/music_controller.py`
- [ ] Adicionar type hints em `gui/controllers/bible_controller.py`
- [ ] Adicionar type hints em `gui/controllers/text_controller.py`
- [ ] Adicionar type hints em `gui/controllers/presentation_controller.py`
- [ ] Adicionar type hints em `gui/controllers/playlist_controller.py`

### Adicionar Type Hints em Managers e Serviços Restantes
- [ ] Adicionar type hints em `core/services/bible_api_client.py`
- [ ] Adicionar type hints em `core/services/letras_scraper.py`
- [ ] Adicionar type hints em outros arquivos conforme necessário

### Configurar `mypy`
- [ ] Criar arquivo `mypy.ini` na raiz do projeto
- [ ] Configurar opções básicas:
  - [ ] `python_version = 3.x`
  - [ ] `warn_return_any = True`
  - [ ] `warn_unused_configs = True`
  - [ ] `ignore_missing_imports = True` (para customtkinter se necessário)
- [ ] Executar `mypy .` para verificar
- [ ] Corrigir erros reportados
- [ ] Adicionar comentários `# type: ignore` apenas se necessário

### Validação Final - Tarefa 4.2
- [ ] Verificar que > 90% do código tem type hints
- [ ] Executar `mypy` e corrigir erros críticos
- [ ] Verificar que autocomplete funciona melhor no IDE
- [ ] Documentar tipos complexos

---

## ✅ Tarefa 4.3: Otimizar Buscas em `BibleManager`

### Adicionar Índice em `BibleManager`
- [ ] Adicionar atributo no `__init__()`:
  - [ ] `self._books_by_abbrev: Dict[str, dict] = {}`
- [ ] Criar método `_rebuild_abbrev_index()`:
  - [ ] Construir índice mapeando abreviação → livro
  - [ ] Lidar com diferentes formatos de abreviação (dict ou str)
  - [ ] Adicionar docstring

### Modificar `load_books()` para Construir Índice
- [ ] Chamar `_rebuild_abbrev_index()` após carregar livros
- [ ] Verificar que índice é construído corretamente

### Refatorar `get_book_by_abbrev()`
- [ ] Modificar para usar `_books_by_abbrev` (O(1))
- [ ] Remover loop linear
- [ ] Manter lógica de compatibilidade com diferentes formatos
- [ ] Adicionar type hints

### Validação Final - Tarefa 4.3
- [ ] Testar busca de livro por abreviação
- [ ] Verificar que é O(1) agora
- [ ] Verificar que funciona com diferentes formatos de abreviação

---

## ✅ Checklist de Critérios de Aceitação - Tarefa 4.1

- [ ] Busca por ID é O(1)
- [ ] Verificação de duplicata é O(1)
- [ ] Índices são mantidos consistentes
- [ ] Performance melhorada para bases grandes
- [ ] Código mais eficiente e escalável

---

## ✅ Checklist de Critérios de Aceitação - Tarefa 4.2

- [ ] Todas as funções públicas têm type hints
- [ ] Type hints cobrem > 90% do código
- [ ] `mypy` não reporta erros (ou mínimos)
- [ ] Autocomplete funciona melhor no IDE
- [ ] Tipos customizados definidos em `core/types.py`

---

## ✅ Checklist de Critérios de Aceitação - Tarefa 4.3

- [ ] Busca de livro é O(1)
- [ ] Índice é construído no carregamento
- [ ] Funcionalidade mantida
- [ ] Performance melhorada

---

## ✅ Testes Manuais

### Testar Performance
- [ ] Criar base de dados grande (100+ músicas) para teste
- [ ] Testar busca por ID → deve ser instantânea
- [ ] Testar verificação de duplicata → deve ser rápida
- [ ] Comparar performance antes/depois (opcional)

### Testar Type Hints
- [ ] Verificar autocomplete no IDE funciona melhor
- [ ] Executar `mypy` e revisar erros
- [ ] Verificar que código ainda funciona normalmente

### Testar Busca de Livros
- [ ] Carregar livros da Bíblia
- [ ] Buscar livro por abreviação → deve ser rápida
- [ ] Verificar que funciona com diferentes formatos

---

## 📝 Notas de Implementação

### Dicas
- Adicionar type hints gradualmente, arquivo por arquivo
- Testar após cada mudança
- Usar `mypy --strict` apenas em arquivos novos primeiro

### Tipos Úteis
- `Optional[T]` - para valores que podem ser None
- `List[T]` - para listas
- `Dict[K, V]` - para dicionários
- `Tuple[T, ...]` - para tuplas
- `Union[T, U]` - para valores que podem ser de tipos diferentes

### Próximos Passos Após Esta Fase
- Fase 5: Criar testes e documentação completa

---

**Status**: 🔄 Em Progresso  
**Última atualização**: [Data]  
**Progresso**: [ ] / [ ] tarefas concluídas

