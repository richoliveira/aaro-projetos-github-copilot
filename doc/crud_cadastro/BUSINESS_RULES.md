# CRUD Cadastro - Regras de Negócio

## Índice
- [1. Validações Obrigatórias](#1-validações-obrigatórias)
- [2. Restrições de Dados](#2-restrições-de-dados)
- [3. Política de Integridade](#3-política-de-integridade)
- [4. Tratamento de Erros](#4-tratamento-de-erros)

## 1. Validações Obrigatórias

### Pessoa

- nome deve ser informado
- nome não pode conter apenas espaços
- idade deve existir e ser numérica
- idade não pode ser negativa

### Cadastro

- não deve haver nomes duplicados
- busca por nome deve considerar comparação case-insensitive
- atualização exige que o registro exista
- remoção exige que o registro exista

## 2. Restrições de Dados

| Campo | Restrição |
|---|---|
| nome | obrigatório, não vazio |
| idade | inteiro, maior ou igual a zero |
| busca por nome | comparação sem distinção de caixa |
| duplicidade | nome repetido em qualquer capitalização não é permitido |

## 3. Política de Integridade

A solução preserva a integridade dos dados por meio de validações antes da persistência lógica e antes da alteração do estado do cadastro. Toda operação que viola as regras resulta em `ValueError`, mantendo o sistema em um estado consistente.

## 4. Tratamento de Erros

Exemplos de mensagens de erro:

- `O nome da pessoa não pode estar vazio.`
- `A idade não pode ser negativa.`
- `A pessoa 'Maria' já está cadastrada.`
- `Pessoa 'Maria' não encontrada.`

Essas mensagens orientam o usuário final e evitam que operações inválidas modifiquem o estado do sistema.

---

Próximo arquivo: [SECURITY.md](SECURITY.md)
