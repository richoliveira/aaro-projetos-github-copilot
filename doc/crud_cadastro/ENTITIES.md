# CRUD Cadastro - Entidades de Negócio

## Índice
- [1. Entidade Pessoa](#1-entidade-pessoa)
- [2. Entidade CadastroPessoas](#2-entidade-cadastropessoas)
- [3. Validações e Regras de Negócio](#3-validações-e-regras-de-negócio)
- [4. Relacionamentos](#4-relacionamentos)

## 1. Entidade Pessoa

A classe `Pessoa` representa um cadastro de pessoa dentro do sistema.

### Estrutura

```python
@dataclass
class Pessoa:
    nome: str
    idade: int
```

### Atributos

| Atributo | Tipo | Descrição | Regras |
|---|---|---|---|
| nome | str | Nome completo da pessoa | Não pode ser vazio ou somente espaços |
| idade | int | Idade em anos | Não pode ser negativa |

### Métodos

- `__post_init__()`
  - valida nome e idade após instanciar a classe
- `__str__()`
  - retorna uma representação amigável no formato `Nome - idade anos`

### Validações

- Nome obrigatório
- Nome não pode conter espaço em branco
- Idade não pode ser menor que zero

## 2. Entidade CadastroPessoas

A classe `CadastroPessoas` atua como repositório em memória do sistema.

### Responsabilidades

- armazenar todas as pessoas cadastradas
- adicionar novo registro
- listar registros
- buscar por nome
- atualizar dados
- remover registros

### Estrutura Interna

```python
self._pessoas: List[Pessoa] = []
```

### Operações Públicas

| Método | Finalidade |
|---|---|
| `adicionar` | adiciona pessoa ao registro |
| `listar` | retorna cópia da lista |
| `buscar_por_nome` | busca pessoa por nome |
| `atualizar` | atualiza nome e idade |
| `remover` | remove pessoa do cadastro |
| `__len__` | retorna quantidade de pessoas |

## 3. Validações e Regras de Negócio

### Regras principais

- não podem existir pessoas com nomes repetidos, considerando comparação case-insensitive
- nome na atualização não pode ser vazio
- idade na atualização não pode ser negativa
- a remoção e atualização exigem que a pessoa exista

### Exemplo de regra de unicidade

```python
if any(p.nome.lower() == pessoa.nome.lower() for p in self._pessoas):
    raise ValueError(f"A pessoa '{pessoa.nome}' já está cadastrada.")
```

## 4. Relacionamentos

A implementação atual trabalha com um modelo simples e direto:

- uma `Pessoa` pertence ao cadastro
- o `CadastroPessoas` mantém uma coleção de `Pessoa`
- não há relacionamento com banco de dados nem tabelas adicionais

```text
CadastroPessoas
    └── lista de Pessoa
```

---

Próximo arquivo: [WORKFLOWS.md](WORKFLOWS.md)
