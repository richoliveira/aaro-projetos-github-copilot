# CRUD Cadastro - Visão Geral

## Índice
- [1. Visão Geral do Módulo](#1-visão-geral-do-módulo)
- [2. Objetivos de Negócio](#2-objetivos-de-negócio)
- [3. Stakeholders e Usuários Finais](#3-stakeholders-e-usuários-finais)
- [4. Escopo Funcional](#4-escopo-funcional)
- [5. Resumo do Fluxo de Operação](#5-resumo-do-fluxo-de-operação)

## 1. Visão Geral do Módulo

O módulo `app/src/crud_cadastro` implementa um sistema simples de cadastro de pessoas em memória, com foco em demonstrar boas práticas de programação em Python utilizando Programação Orientada a Objetos (POO). A solução oferece operações de criação, leitura, atualização e remoção (CRUD) de registros de pessoas, mantendo os dados em memória durante a execução da aplicação.

A arquitetura foi pensada para ser didática, clara e facilmente extensível, com separação entre:

- entidade de negócio (`Pessoa`)
- camada de persistência lógica em memória (`CadastroPessoas`)
- interface de interação via console (`ConsoleApp`)

A aplicação atende principalmente a cenários de demonstração, prototipagem e uso interno em ambientes controlados sem dependence de banco de dados.

## 2. Objetivos de Negócio

Os objetivos principais do módulo são:

- permitir o cadastro de pessoas com nome e idade
- manter uma lista de registros em memória
- oferecer operação de consulta por nome
- permitir alteração de dados cadastrais
- remover registros existentes
- fornecer uma interface em console simples e funcional

## 3. Stakeholders e Usuários Finais

### Stakeholders
- Desenvolvedor responsável pela manutenção da solução
- Instrutor/arquitetos em aula prática
- Equipe interna que valida regras de negócio

### Usuários finais
- Usuários do sistema em console
- Operadores de cadastro
- Desenvolvedores e analistas em ambiente acadêmico ou prototipagem

## 4. Escopo Funcional

O módulo cobre as seguintes funções:

- cadastro de pessoa com validação de dados
- listagem de todos os registros
- busca por nome
- atualização de nome e idade
- remoção de pessoa
- menu interativo em terminal

## 5. Resumo do Fluxo de Operação

O fluxo principal é o seguinte:

1. O usuário inicia a aplicação console.
2. O sistema apresenta um menu com opções de CRUD.
3. O usuário escolhe uma operação.
4. O sistema valida entradas e regras de negócio.
5. O serviço em memória atualiza a lista de registros.
6. O resultado é retornado em mensagem textual no console.

```text
Usuário -> ConsoleApp -> CadastroPessoas -> Pessoa
     \--> validação de dados e mensagens de erro
```

---

Próximo arquivo: [ENTITIES.md](ENTITIES.md)
