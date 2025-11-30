# Roadmap Visual - Melhorias do Projeto

## Timeline das Fases

```
┌─────────────────────────────────────────────────────────────────────┐
│                        FASE 1: FUNDAÇÃO                             │
│  Logging + Tratamento de Erros                                      │
│  ⏱️ 4-6h | 🔴 ALTA | Dependências: Nenhuma                         │
│                                                                      │
│  📦 Criar:                                                          │
│     • core/logging_config.py                                        │
│     • core/exceptions.py                                            │
│                                                                      │
│  🔧 Modificar:                                                      │
│     • main.py                                                       │
│     • 6 arquivos (substituir print() por logging)                   │
│                                                                      │
│  ✅ Resultado: Base sólida para debugging                           │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                    FASE 2: ROBUSTEZ                                 │
│  Validação + Fail Fast                                              │
│  ⏱️ 3-4h | 🔴 ALTA | Dependências: Fase 1                          │
│                                                                      │
│  📦 Criar:                                                          │
│     • core/validators.py                                            │
│                                                                      │
│  🔧 Modificar:                                                      │
│     • core/music_manager.py                                         │
│     • core/config_manager.py                                        │
│     • gui/controllers/*.py                                          │
│                                                                      │
│  ✅ Resultado: Validação robusta, menos bugs                        │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│              FASE 3: REFATORAÇÃO (Pode ser paralela)                │
│  Modularização + DRY                                                │
│  ⏱️ 6-8h | 🟡 MÉDIA | Dependências: Fase 1                         │
│                                                                      │
│  📦 Criar:                                                          │
│     • gui/ui/builders.py                                            │
│     • gui/ui/top_bar.py                                             │
│     • gui/ui/preview_pane.py                                        │
│     • core/utils/file_utils.py                                      │
│     • gui/utils/dialog_utils.py                                     │
│                                                                      │
│  🔧 Modificar:                                                      │
│     • gui/main_window.py (dividir - objetivo: < 300 linhas)        │
│     • core/config_manager.py                                        │
│     • core/music_manager.py                                         │
│     • core/bible_manager.py                                         │
│     • gui/dialogs.py                                                │
│                                                                      │
│  ✅ Resultado: Código modular e sem duplicação                      │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│              FASE 4: QUALIDADE (Pode ser paralela)                  │
│  Performance + Tipagem                                              │
│  ⏱️ 5-7h | 🟡 MÉDIA | Dependências: Fase 1                         │
│                                                                      │
│  📦 Criar:                                                          │
│     • core/types.py                                                 │
│     • mypy.ini                                                      │
│                                                                      │
│  🔧 Modificar:                                                      │
│     • core/music_manager.py (índices O(1))                          │
│     • core/bible_manager.py (índices O(1))                          │
│     • Todos os 16 arquivos (type hints)                             │
│                                                                      │
│  ✅ Resultado: Performance otimizada + Type safety                  │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│               FASE 5: TESTES E DOCUMENTAÇÃO                         │
│  Testes Unitários + Docs                                            │
│  ⏱️ 8-10h | 🟢 BAIXA | Dependências: Todas as fases                │
│                                                                      │
│  📦 Criar:                                                          │
│     • tests/__init__.py                                             │
│     • tests/conftest.py                                             │
│     • tests/core/test_*.py (3 arquivos)                             │
│     • tests/core/services/test_*.py (2 arquivos)                    │
│     • README.md                                                     │
│     • docs/arquitetura.md                                           │
│     • docs/api.md                                                   │
│     • docs/instalacao.md                                            │
│     • requirements-dev.txt                                          │
│                                                                      │
│  🔧 Modificar:                                                      │
│     • Todos os arquivos (docstrings)                                │
│                                                                      │
│  ✅ Resultado: Projeto profissional e testado                       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Priorização Visual

```
CRÍTICO (Faça Primeiro)          IMPORTANTE (Faça Depois)          DESEJÁVEL (Faça Por Último)
═══════════════════════          ═══════════════════════          ════════════════════════════

┌─────────────────────┐          ┌─────────────────────┐          ┌─────────────────────┐
│   FASE 1            │          │   FASE 3            │          │   FASE 5            │
│   Fundação          │          │   Refatoração       │          │   Testes + Docs     │
│   4-6h              │          │   6-8h              │          │   8-10h             │
│                     │          │                     │          │                     │
│   • Logging         │          │   • Dividir arquivos│          │   • Testes unitários│
│   • Exceções        │          │   • Eliminar DRY    │          │   • Documentação    │
└─────────────────────┘          └─────────────────────┘          └─────────────────────┘

┌─────────────────────┐          ┌─────────────────────┐
│   FASE 2            │          │   FASE 4            │
│   Robustez          │          │   Qualidade         │
│   3-4h              │          │   5-7h              │
│                     │          │                     │
│   • Validação       │          │   • Performance     │
│   • Fail Fast       │          │   • Type hints      │
└─────────────────────┘          └─────────────────────┘
```

---

## Estatísticas do Plano

| Métrica | Valor |
|---------|-------|
| **Total de Fases** | 5 |
| **Total de Horas Estimadas** | 26-35h |
| **Arquivos a Criar** | ~20 |
| **Arquivos a Modificar** | ~30 |
| **Tempo Crítico (Fases 1-2)** | 7-10h |
| **Tempo Médio (Fases 3-4)** | 11-15h |
| **Tempo Baixa Prioridade (Fase 5)** | 8-10h |

---

## Dependências entre Fases

```
Fase 1 (Fundação)
    ├─→ Fase 2 (Robustez)
    ├─→ Fase 3 (Refatoração)
    └─→ Fase 4 (Qualidade)
            │
            └─→ Fase 5 (Testes + Docs)
```

**Nota**: Fases 3 e 4 podem ser executadas em paralelo após a Fase 1.

---

## Próximos Passos Imediatos

### Para Começar Hoje:

1. ✅ **Revisar este roadmap**
2. ✅ **Escolher fase para começar** (recomendado: Fase 1)
3. ✅ **Ler tarefas detalhadas em `docs/plano-de-acao.md`**
4. ✅ **Configurar ambiente de desenvolvimento**
5. ✅ **Criar branch para Fase 1**: `git checkout -b fase-1-fundacao`

### Checklist Inicial:

- [ ] Repositório clonado e atualizado
- [ ] Ambiente virtual configurado
- [ ] Dependências instaladas
- [ ] Aplicação funciona localmente
- [ ] Branch criada para trabalho

---

## Métricas de Sucesso

### Ao Final de Cada Fase:

**Fase 1**:
- [ ] 0 usos de `print()` no código
- [ ] Sistema de logging funcionando
- [ ] Classes de erro criadas e usadas

**Fase 2**:
- [ ] Todas as entradas validadas
- [ ] Fail Fast implementado
- [ ] Mensagens de erro claras

**Fase 3**:
- [ ] `main_window.py` < 300 linhas
- [ ] Sem código duplicado
- [ ] Componentes reutilizáveis criados

**Fase 4**:
- [ ] Buscas O(1) implementadas
- [ ] Type hints em > 90% do código
- [ ] mypy passando

**Fase 5**:
- [ ] Cobertura de testes > 80%
- [ ] Documentação completa
- [ ] README.md atualizado

---

**Criado em**: 2024  
**Baseado em**: `docs/analise-prompt-ia.md`  
**Detalhes completos**: `docs/plano-de-acao.md`

