# CRUD Cadastro - Interface e Endpoints

## Índice
- [1. Visão Geral da Interface](#1-visão-geral-da-interface)
- [2. Métodos Públicos de `CadastroPessoas`](#2-métodos-públicos-de-cadastropessoas)
- [3. Métodos Públicos de `ConsoleApp`](#3-métodos-públicos-de-consoleapp)
- [4. Exemplos de Uso](#4-exemplos-de-uso)

## 1. Visão Geral da Interface

Como a aplicação foi implementada em console, a interface é textual e interativa. O usuário navega por um menu em terminal em vez de endpoints HTTP.

## 2. Métodos Públicos de `CadastroPessoas`

| Método | Parâmetros | Retorno | Descrição |
|---|---|---|---|
| `adicionar` | `pessoa: Pessoa` | `None` | adiciona uma pessoa |
| `listar` | nenhum | `List[Pessoa]` | retorna pessoas cadastradas |
| `buscar_por_nome` | `nome: str` | `Optional[Pessoa]` | busca por nome |
| `atualizar` | `nome, novo_nome, nova_idade` | `Pessoa` | atualiza os dados |
| `remover` | `nome: str` | `Pessoa` | remove um registro |
| `__len__` | nenhum | `int` | quantidade atual de registros |

### Observações
- Os métodos lançam `ValueError` quando as regras de negócio forem violadas.
- O armazenamento está em memória, não persistente em arquivo ou banco.

## 3. Métodos Públicos de `ConsoleApp`

| Método | Finalidade |
|---|---|
| `exibir_menu` | mostra o menu principal |
| `cadastrar_pessoa` | coleta dados e chama o cadastro |
| `listar_pessoas` | exibe pessoas cadastradas |
| `buscar_pessoa` | busca por nome |
| `atualizar_pessoa` | atualiza dados de uma pessoa |
| `remover_pessoa` | remove registro |
| `executar` | loop principal do console |

### Exemplo de menu

```text
=== CRUD de Cadastro de Pessoas ===
1. Cadastrar pessoa
2. Listar pessoas
3. Buscar pessoa
4. Atualizar pessoa
5. Remover pessoa
0. Sair
```

## 4. Exemplos de Uso

### Cadastro

```python
cadastro = CadastroPessoas()
pessoa = Pessoa(nome="Ana", idade=25)
cadastro.adicionar(pessoa)
```

### Busca

```python
pessoa = cadastro.buscar_por_nome("Ana")
```

### Atualização

```python
cadastro.atualizar("Ana", "Ana Souza", 26)
```

### Remoção

```python
cadastro.remover("Ana Souza")
```

---

Próximo arquivo: [BUSINESS_RULES.md](BUSINESS_RULES.md)
