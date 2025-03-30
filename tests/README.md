# 🧪 Testes do Weekly Reports Summarizer

Este diretório contém os testes unitários e de integração para o Weekly Reports Summarizer.

## 🚀 Como Executar os Testes

Para executar todos os testes:

```bash
pytest
```

Para executar testes específicos:

```bash
# 📦 Executar testes de um módulo específico
pytest tests/test_ai/test_adapters/test_gemini.py

# 📊 Executar testes com mais detalhes
pytest -v

# 📈 Executar testes com cobertura
pytest --cov=src tests/
```

## ✨ Boas Práticas

1. 🎯 se fixtures para compartilhar código comum entre testes
2. 🔄 Mantenha os testes independentes entre si
3. 🎭 Use mocks para isolar dependências externas
4. 📝 Documente os testes com docstrings claras
5. 📌 Siga o padrão de nomenclatura: `test_*` para funções de teste

## 🎨 Estilo de Código

- 🎯 Se possível use classes para agrupar testes
- 📝 Se complexos, documente cada teste com docstrings claras
- 🎭 Use mocks de forma consistente
- 🔄 Mantenha os testes simples e focados
- 📊 Use assertions descritivos

## 🤝 Contribuindo

1. 🎯 Crie testes para novas funcionalidades
2. 🔄 Mantenha os testes atualizados
3. 📝 Documente mudanças nos testes
4. 📊 Mantenha uma boa cobertura de testes
