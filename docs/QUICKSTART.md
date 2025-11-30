# 🚀 Guia Rápido - Início das Melhorias

## Como Começar

Este guia te ajuda a começar imediatamente com as melhorias do projeto.

---

## 📋 Pré-requisitos

Antes de começar, certifique-se de que:

- [ ] O projeto está funcionando localmente
- [ ] Você entendeu a estrutura atual do código
- [ ] Leu a análise completa em `docs/analise-prompt-ia.md`

---

## 🎯 Por Onde Começar?

### Recomendação: **FASE 1 - Fundação**

A Fase 1 cria a base para todas as outras melhorias. É a mais importante e pode ser feita independentemente.

---

## ⚡ Início Rápido - Fase 1

### Passo 1: Criar Branch
```bash
git checkout -b fase-1-fundacao
```

### Passo 2: Criar Sistema de Logging

1. **Criar arquivo `core/logging_config.py`**:
```python
import logging
import sys
from pathlib import Path

def setup_logging():
    log_dir = Path(__file__).parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)d]',
        handlers=[
            logging.FileHandler(log_dir / "projetor.log", encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)
```

2. **Adicionar em `main.py`** (no início):
```python
from core.logging_config import setup_logging
logger = setup_logging()
```

### Passo 3: Criar Classes de Erro

1. **Criar arquivo `core/exceptions.py`**:
```python
class ProjectorError(Exception):
    """Base exception para erros do projeto"""
    pass

class ConfigError(ProjectorError):
    """Erro relacionado a configuração"""
    pass

class ConfigSaveError(ConfigError):
    """Erro ao salvar configuração"""
    pass

class MusicDatabaseError(ProjectorError):
    """Erro na base de dados de músicas"""
    pass

class BibleAPIError(ProjectorError):
    """Erro em requisição à API da Bíblia"""
    pass

class ScraperError(ProjectorError):
    """Erro no scraper de letras"""
    pass

class ValidationError(ProjectorError):
    """Erro de validação de dados"""
    pass
```

### Passo 4: Substituir Primeiro `print()`

**Arquivo**: `core/config_manager.py`

**Encontrar**:
```python
print(f"Erro ao salvar arquivo de configuração: {e}")
```

**Substituir por**:
```python
import logging
logger = logging.getLogger(__name__)
# ...
logger.error(f"Erro ao salvar arquivo de configuração: {e}", exc_info=True)
```

### Passo 5: Testar

1. Execute a aplicação
2. Verifique se o arquivo `logs/projetor.log` foi criado
3. Verifique se os logs aparecem no console

---

## 📚 Documentação Completa

Para detalhes completos de cada fase:

- **Plano Detalhado**: `docs/plano-de-acao.md`
- **Roadmap Visual**: `docs/roadmap-visual.md`
- **Análise Completa**: `docs/analise-prompt-ia.md`

---

## 🎯 Próximos Passos Após Fase 1

1. ✅ Completar substituição de todos os `print()`
2. ✅ Implementar uso de exceções personalizadas
3. ✅ Fazer commit: `git commit -m "Fase 1: Sistema de logging e exceções"`
4. ✅ Ir para Fase 2: Validação e Fail Fast

---

## ⚠️ Dicas Importantes

1. **Faça commits frequentes**: Uma mudança pequena por commit
2. **Teste após cada mudança**: Não acumule mudanças sem testar
3. **Leia o plano completo**: Cada fase tem detalhes importantes
4. **Peça ajuda se necessário**: Revise a documentação ou pergunte

---

## 📞 Recursos

- **Lista de Tarefas**: Ver `docs/plano-de-acao.md` seção "Checklist de Progresso"
- **Problemas comuns**: Ver seção "Notas Importantes" no plano
- **Cronograma**: Ver seção "Cronograma Sugerido" no plano

---

**Boa sorte! 🚀**

