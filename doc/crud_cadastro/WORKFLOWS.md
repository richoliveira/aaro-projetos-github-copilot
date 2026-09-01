# CRUD Cadastro - Fluxos de Negócio

## Índice
- [1. Fluxo de Cadastro](#1-fluxo-de-cadastro)
- [2. Fluxo de Listagem](#2-fluxo-de-listagem)
- [3. Fluxo de Busca](#3-fluxo-de-busca)
- [4. Fluxo de Atualização](#4-fluxo-de-atualização)
- [5. Fluxo de Remoção](#5-fluxo-de-remoção)
- [6. Fluxo de Menu Console](#6-fluxo-de-menu-console)

## 1. Fluxo de Cadastro

### Objetivo
Incluir uma nova pessoa no sistema.

### Passos
1. Usuário informa nome e idade.
2. Aplicação instancia `Pessoa`.
3. Sistema valida:
   - nome preenchido
   - idade maior ou igual a zero
4. Sistema verifica duplicidade pelo nome.
5. Se válido, adiciona à lista em memória.
6. Mensagem de sucesso é exibida.

### Tratamento de erro

- nome vazio -> `ValueError`
- idade negativa -> `ValueError`
- nome duplicado -> `ValueError`

## 2. Fluxo de Listagem

### Objetivo
Exibir todas as pessoas cadastradas.

### Passos
1. Usuário seleciona a opção de listagem.
2. Sistema chama `listar()`.
3. O método retorna uma cópia da lista interna.
4. A interface exibe os dados em texto no console.

### Regras
- se a lista estiver vazia, exibe mensagem informativa

## 3. Fluxo de Busca

### Objetivo
Localizar uma pessoa pelo nome.

### Passos
1. Usuário informa o nome para buscar.
2. Sistema chama `buscar_por_nome(nome)`.
3. O método compara o valor em caixa baixa.
4. Se encontrar, retorna o objeto `Pessoa`.
5. Caso contrário, retorna `None`.

### Validação
- busca é sensível a espaços e normalização de maiúsculas/minúsculas

## 4. Fluxo de Atualização

### Objetivo
Modificar nome e idade de uma pessoa existente.

### Passos
1. Usuário informa o nome atual.
2. Sistema localiza a pessoa.
3. Usuário informa novo nome e nova idade.
4. Sistema valida:
   - registro existente
   - novo nome preenchido
   - nova idade não negativa
5. Dados são atualizados na instância.
6. Mensagem de sucesso é exibida.

## 5. Fluxo de Remoção

### Objetivo
Excluir uma pessoa do cadastro.

### Passos
1. Usuário informa o nome da pessoa.
2. Sistema busca o registro.
3. Se existir, remove da lista em memória.
4. Retorna a pessoa removida.
5. Se não existir, dispara `ValueError`.

## 6. Fluxo de Menu Console

### Objetivo
Oferecer interação ao usuário por linha de comando.

### Opções do Menu

| Opção | Função |
|---|---|
| 1 | cadastrar pessoa |
| 2 | listar pessoas |
| 3 | buscar pessoa |
| 4 | atualizar pessoa |
| 5 | remover pessoa |
| 0 | sair |

### Fluxo geral

```text
inicio
  -> exibir_menu()
  -> ler entrada
  -> executar ação
  -> repetir até option 0
```

---

Próximo arquivo: [API.md](API.md)
