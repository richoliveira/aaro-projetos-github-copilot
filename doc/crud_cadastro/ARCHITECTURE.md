# CRUD Cadastro - Arquitetura Técnica

## Índice
- [1. Visão de Arquitetura](#1-visão-de-arquitetura)
- [2. Organização de Pacotes](#2-organização-de-pacotes)
- [3. Diagrama de Componentes](#3-diagrama-de-componentes)
- [4. Padrões de Design](#4-padrões-de-design)
- [5. Dependências e Extensibilidade](#5-dependências-e-extensibilidade)

## 1. Visão de Arquitetura

A solução adota uma arquitetura simples em camadas, porém com boa clareza de responsabilidades:

- Modelo: `Pessoa`
- Serviço/Repositório: `CadastroPessoas`
- Interface: `ConsoleApp`

Essa estrutura facilita a manutenção e a evolução do código sem aumentar a complexidade inicial.

## 2. Organização de Pacotes

```text
app/
└── src/
    └── crud_cadastro/
        ├── __init__.py
        ├── pessoa.py
        ├── cadastro_pessoas.py
        └── console_app.py
```

## 3. Diagrama de Componentes

```text
+---------------------+
| ConsoleApp          |
| - exibir_menu       |
| - cadastrar_pessoa  |
| - listar_pessoas    |
| - buscar_pessoa     |
| - atualizar_pessoa  |
| - remover_pessoa    |
+----------+----------+
           |
           v
+---------------------+
| CadastroPessoas     |
| - _pessoas          |
| + adicionar()       |
| + listar()          |
| + buscar_por_nome() |
| + atualizar()       |
| + remover()         |
+----------+----------+
           |
           v
+---------------------+
| Pessoa              |
| - nome              |
| - idade             |
| + __post_init__     |
| + __str__()         |
+---------------------+
```

## 4. Padrões de Design

### Padrão utilizado

- POO (Programação Orientada a Objetos)
- Data class para modelagem da entidade
- Encapsulamento via atributos privados em repositório
- Validação de regras dentro do próprio objeto e da lógica de cadastro

## 5. Dependências e Extensibilidade

### Dependências externas

- Python 3.8+
- nenhuma biblioteca externa para o CRUD base

### Extensibilidade

A solução pode ser estendida para:

- persistência em JSON ou SQLite
- camada de serviço separada
- API REST
- testes automatizados
- interface gráfica

---

Documentação concluída com visão geral, regras, arquitetura e fluxos do módulo de cadastro.
