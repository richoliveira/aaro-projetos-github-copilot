# CRUD Cadastro - Segurança e Conformidade

## Índice
- [1. Visão Geral de Segurança](#1-visão-geral-de-segurança)
- [2. Proteções Implementadas](#2-proteções-implementadas)
- [3. Riscos e Controles](#3-riscos-e-controles)
- [4. Boas Práticas](#4-boas-práticas)

## 1. Visão Geral de Segurança

A aplicação de cadastro em memória tem caráter acadêmico e interno. Como não há persistência em banco de dados nem autenticação de usuários, o foco principal da segurança está na integridade dos dados e na validação das entradas.

## 2. Proteções Implementadas

- validação de campos obrigatórios
- rejeição de valores negativos
- bloqueio de duplicidade de nomes
- controle de exceções para evitar estados inconsistentes

## 3. Riscos e Controles

| Risco | Controle |
|---|---|
| entrada vazia | validação no construtor de `Pessoa` |
| idade inválida | validação em `__post_init__` |
| duplicidade | verificação em `adicionar` |
| operação em registro inexistente | `ValueError` em `atualizar` e `remover` |

## 4. Boas Práticas

- sempre validar entrada antes de persistir
- evitar uso de dados sem sanitização
- manter mensagens de erro claras e compatíveis com uso em console
- separar responsabilidades entre entidade e lógica de negócio

> A solução foi construída para demonstração e prototipagem, não sendo um sistema com autenticação, controle de sessão ou armazenamento sensível em produção.

---

Próximo arquivo: [ARCHITECTURE.md](ARCHITECTURE.md)
