# 🎤 Projetor - Sistema de Projeção para Cultos

Sistema completo para gerenciar e projetar músicas, versículos bíblicos e textos durante cultos e apresentações.

## 📋 Descrição

O **Projetor** é uma aplicação desktop desenvolvida em Python que permite:

- 🎵 **Gerenciar músicas**: Adicionar, editar e organizar músicas com letras completas
- 📖 **Acessar a Bíblia**: Buscar e projetar versículos de diferentes versões
- 📝 **Criar textos livres**: Adicionar avisos e textos personalizados
- 🎬 **Projetar conteúdo**: Exibir slides em tela secundária com animações
- 📋 **Ordem de culto**: Organizar a sequência de apresentação

## ✨ Principais Funcionalidades

- **Gerenciamento de Músicas**
  - Importar letras de músicas via URL (Letras.mus.br)
  - Adicionar músicas manualmente
  - Busca rápida e filtragem
  - Geração automática de slides a partir das letras

- **Acesso à Bíblia**
  - Múltiplas versões (NVI, ACF)
  - Busca por livro, capítulo e versículo
  - Cache local para acesso offline
  - Projeção de versículos formatados

- **Sistema de Projeção**
  - Pré-visualização antes de projetar
  - Suporte a múltiplos monitores
  - Animações personalizáveis (Neve, Partículas, etc.)
  - Controles de navegação entre slides

- **Personalização**
  - Temas claro/escuro
  - Configurações de fonte, cor e animação por tipo de conteúdo
  - Atalhos de teclado configuráveis

## 🚀 Instalação

### Requisitos

- Python 3.10 ou superior
- Windows 10/11 (testado)
- Conexão com internet (para importar músicas e acessar API da Bíblia)

### Passo a Passo

1. **Clone o repositório**
   ```bash
   git clone https://github.com/seu-usuario/projetor.git
   cd projetor
   ```

2. **Crie um ambiente virtual** (recomendado)
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure variáveis de ambiente** (opcional)
   Crie um arquivo `.env` na raiz do projeto:
   ```
   BIBLE_API_TOKEN=seu_token_aqui
   ```

5. **Execute a aplicação**
   ```bash
   python main.py
   ```

Para instruções detalhadas, consulte [docs/instalacao.md](docs/instalacao.md).

## 📖 Como Usar

### Guia Rápido

1. **Adicionar Música**
   - Vá para a aba "Músicas"
   - Clique em "Adicionar Nova" ou "Importar (URL)"
   - Preencha os dados e salve

2. **Buscar Versículo**
   - Vá para a aba "Bíblia"
   - Selecione versão, livro, capítulo e versículo
   - Clique em "Carregar e Visualizar"

3. **Criar Ordem de Culto**
   - Adicione itens (músicas, versículos, textos) à ordem
   - Use os botões "Subir" e "Descer" para reorganizar
   - Clique em "Abrir Projeção" para exibir

4. **Projetar**
   - Clique em "Abrir Projeção"
   - Use as setas ou botões para navegar entre slides
   - Ajuste o tamanho da fonte conforme necessário

## 🛠️ Desenvolvimento

### Executar Testes

```bash
# Instalar dependências de desenvolvimento
pip install -r requirements-dev.txt

# Executar todos os testes
pytest

# Executar com cobertura
pytest --cov=core --cov-report=html

# Executar testes específicos
pytest tests/core/test_music_manager.py -v
```

### Estrutura do Projeto

```
projetor/
├── core/              # Lógica de negócio
│   ├── managers/      # Gerenciadores (música, bíblia, config)
│   ├── services/      # Serviços externos (API, scraper)
│   ├── utils/         # Utilitários
│   └── exceptions.py  # Exceções customizadas
├── gui/               # Interface gráfica
│   ├── controllers/   # Controladores (MVC)
│   ├── dialogs.py     # Diálogos
│   └── ui/            # Componentes de UI
├── tests/             # Testes unitários
├── docs/              # Documentação
└── data/              # Dados (músicas, cache)
```

Para mais detalhes sobre a arquitetura, consulte [docs/arquitetura.md](docs/arquitetura.md).

### Contribuir

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📚 Documentação

- [Guia de Instalação](docs/instalacao.md) - Instalação detalhada
- [Arquitetura](docs/arquitetura.md) - Estrutura e design do sistema
- [API](docs/api.md) - Documentação da API interna
- [Plano de Ação](docs/plano-de-acao.md) - Roadmap de desenvolvimento

## 🐛 Troubleshooting

### Problemas Comuns

**Aplicação não inicia**
- Verifique se todas as dependências estão instaladas
- Verifique se o Python está na versão 3.10+

**Erro ao importar música**
- Verifique sua conexão com internet
- Confirme que a URL é do Letras.mus.br

**Projeção não aparece**
- Verifique se há múltiplos monitores conectados
- Configure o índice do monitor de projeção nas configurações

Para mais soluções, consulte [docs/instalacao.md](docs/instalacao.md#troubleshooting).

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👥 Autores

- Desenvolvido com ❤️ para facilitar a projeção em cultos

## 🙏 Agradecimentos

- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Interface moderna
- [API Bíblia Digital](https://www.abibliadigital.com.br/) - Versículos bíblicos
- [Letras.mus.br](https://www.letras.mus.br/) - Letras de músicas

---

**Versão**: 1.0  
**Última atualização**: 2024

