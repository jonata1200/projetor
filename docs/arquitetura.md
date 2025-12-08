# 🏗️ Arquitetura do Sistema

Documentação da arquitetura e design do Projetor.

## 📐 Visão Geral

O Projetor segue uma arquitetura em camadas com padrão MVC (Model-View-Controller):

```
┌─────────────────────────────────────────┐
│           GUI (Interface)               │
│  ┌──────────┐  ┌──────────┐            │
│  │ Windows  │  │ Dialogs  │            │
│  └──────────┘  └──────────┘            │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│        Controllers (Lógica)             │
│  ┌──────────┐  ┌──────────┐            │
│  │ Music    │  │ Bible    │            │
│  │ Controller│  │Controller│            │
│  └──────────┘  └──────────┘            │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│      Core (Regras de Negócio)           │
│  ┌──────────┐  ┌──────────┐            │
│  │ Managers │  │ Services  │            │
│  └──────────┘  └──────────┘            │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│         Data (Armazenamento)            │
│  ┌──────────┐  ┌──────────┐            │
│  │ JSON     │  │ Cache     │            │
│  │ Files    │  │ Files     │            │
│  └──────────┘  └──────────┘            │
└─────────────────────────────────────────┘
```

## 🧩 Componentes Principais

### 1. Core (Lógica de Negócio)

#### Managers
Gerenciam os dados principais da aplicação:

- **MusicManager** (`core/music_manager.py`)
  - Gerencia banco de dados de músicas
  - CRUD completo (Create, Read, Update, Delete)
  - Índices O(1) para busca rápida
  - Geração automática de slides

- **BibleManager** (`core/bible_manager.py`)
  - Gerencia acesso à Bíblia
  - Cache local de livros
  - Busca por abreviação (O(1))
  - Integração com API externa

- **ConfigManager** (`core/config_manager.py`)
  - Gerencia configurações da aplicação
  - Persistência em arquivo INI
  - Validação de valores

#### Services
Serviços externos e utilitários:

- **BibleAPIClient** (`core/services/bible_api_client.py`)
  - Cliente para API da Bíblia Digital
  - Requisições HTTP
  - Tratamento de erros

- **LetrasScraper** (`core/services/letras_scraper.py`)
  - Scraping de letras do Letras.mus.br
  - Parsing de HTML
  - Extração de título, artista e letra

#### Utils
Utilitários compartilhados:

- **file_utils** (`core/utils/file_utils.py`)
  - Funções para salvar/carregar JSON
  - Criação de diretórios
  - Tratamento de erros

- **validators** (`core/validators.py`)
  - Validação de dados
  - Fail Fast pattern

- **exceptions** (`core/exceptions.py`)
  - Exceções customizadas
  - Hierarquia de erros

### 2. GUI (Interface Gráfica)

#### Controllers
Controlam a lógica da interface:

- **MusicController** (`gui/controllers/music_controller.py`)
  - Gerencia aba de músicas
  - Busca e filtragem
  - Diálogos de adição/edição

- **BibleController** (`gui/controllers/bible_controller.py`)
  - Gerencia aba da Bíblia
  - Seleção de versão, livro, capítulo
  - Carregamento de versículos

- **PlaylistController** (`gui/controllers/playlist_controller.py`)
  - Gerencia ordem de culto
  - Adição/remoção de itens
  - Reordenação

- **PresentationController** (`gui/controllers/presentation_controller.py`)
  - Controla janela de projeção
  - Navegação entre slides
  - Ajuste de fonte

- **TextController** (`gui/controllers/text_controller.py`)
  - Gerencia aba de texto livre
  - Criação de avisos

#### Windows
Janelas principais:

- **MainWindow** (`gui/main_window.py`)
  - Janela principal
  - Abas e controles
  - Integração de controllers

- **ProjectionWindow** (`gui/projection_window.py`)
  - Janela de projeção
  - Exibição de slides
  - Animações

#### UI Components
Componentes reutilizáveis:

- **builders** (`gui/ui/builders.py`)
  - Funções para criar componentes UI
  - Top bar, preview pane, tabs

- **dialog_utils** (`gui/utils/dialog_utils.py`)
  - Utilitários para diálogos
  - Centralização de janelas

## 🔄 Fluxo de Dados

### Adicionar Música

```
User → MusicController → MusicManager → file_utils → JSON File
                                    ↓
                              Índices O(1)
```

### Buscar Versículo

```
User → BibleController → BibleManager → BibleAPIClient → API Externa
                                    ↓
                              Cache Local
```

### Projetar Slide

```
User → PlaylistController → PresentationController → ProjectionWindow
                                              ↓
                                    Slide atualizado
```

## 📦 Padrões Utilizados

### MVC (Model-View-Controller)
- **Model**: Managers (dados)
- **View**: Windows e UI Components
- **Controller**: Controllers (lógica)

### Singleton (implícito)
- Managers são instanciados uma vez
- ConfigManager mantém estado global

### Repository Pattern
- Managers atuam como repositórios
- Abstração de acesso a dados

### Strategy Pattern
- Diferentes tipos de animação
- Diferentes tipos de conteúdo (música, bíblia, texto)

## 🔐 Segurança e Validação

### Fail Fast
- Validação no início
- Erros levantados imediatamente

### Validação de Entrada
- Validators para strings, URLs, cores, etc.
- Exceções específicas (ValidationError)

### Tratamento de Erros
- Hierarquia de exceções
- Logging de erros
- Mensagens amigáveis ao usuário

## ⚡ Performance

### Índices O(1)
- MusicManager: busca por ID e duplicata
- BibleManager: busca por abreviação

### Cache
- Cache de livros da Bíblia
- Reduz requisições à API

### Lazy Loading
- Livros carregados sob demanda
- Cache usado quando disponível

## 📁 Estrutura de Arquivos

```
projetor/
├── core/                    # Lógica de negócio
│   ├── managers/            # Gerenciadores
│   ├── services/            # Serviços externos
│   ├── utils/               # Utilitários
│   └── exceptions.py        # Exceções
├── gui/                     # Interface
│   ├── controllers/         # Controladores
│   ├── ui/                  # Componentes UI
│   └── utils/               # Utilitários GUI
├── tests/                    # Testes
├── data/                     # Dados
└── docs/                     # Documentação
```

## 🔮 Melhorias Futuras

- [ ] Banco de dados SQLite (ao invés de JSON)
- [ ] Suporte a múltiplos idiomas
- [ ] Exportação de ordem de culto
- [ ] Histórico de projeções
- [ ] Temas personalizados
- [ ] Plugins/extensões

---

**Última atualização**: 2024

