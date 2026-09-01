# Entidades de Negócio - Gerenciador de Tarefas

## Índice
1. [Visão Geral das Entidades](#visão-geral-das-entidades)
2. [Entidade: Tarefa](#entidade-tarefa)
3. [Ciclo de Vida das Entidades](#ciclo-de-vida-das-entidades)
4. [Mapeamento de Dados](#mapeamento-de-dados)
5. [Relacionamentos](#relacionamentos)
6. [Validações e Constraints](#validações-e-constraints)
7. [Exemplos de Dados](#exemplos-de-dados)

---

## Visão Geral das Entidades

O **Gerenciador de Tarefas** trabalha com uma única entidade de negócio primária:

### Diagrama ER (Entity-Relationship)

```
┌──────────────────────────────────────┐
│            Tarefa                    │
├──────────────────────────────────────┤
│ • id: Integer (implicit)             │
│ • titulo: String (Required)          │
│ • concluida: Boolean (Default: False)│
└──────────────────────────────────────┘
```

### Características Principais
- Entidade simples e direta
- Sem relacionamentos com outras entidades
- Armazenamento em memória
- Ciclo de vida vinculado à sessão do usuário

---

## Entidade: Tarefa

### Definição
Uma **Tarefa** representa uma ação ou atividade que o usuário deseja rastrear. É a unidade fundamental do sistema de gerenciamento.

### Estrutura de Dados

```python
{
    "titulo": str,      # Nome ou descrição da tarefa
    "concluida": bool   # Status de conclusão
}
```

### Campos Detalhados

#### Campo: `titulo`

| Propriedade | Valor |
|---|---|
| **Tipo** | `str` (String) |
| **Obrigatório** | Sim |
| **Padrão** | Nenhum |
| **Comprimento Máximo** | Sem limite técnico |
| **Comprimento Recomendado** | 50-200 caracteres |
| **Formato** | Texto livre |
| **Sensibilidade** | Case-sensitive |
| **Trim/Normalização** | `.strip()` aplicado automaticamente |

**Exemplos Válidos:**
```
"Fazer compras no supermercado"
"Estudar Python para prova"
"Limpar a casa antes das 19h"
"Implementar feature de login"
"Reunião com o cliente às 15h"
```

**Restrições:**
- Não pode estar vazio ou conter apenas espaços em branco
- Espaços em branco no início/fim são removidos automaticamente
- Caracteres especiais são permitidos

#### Campo: `concluida`

| Propriedade | Valor |
|---|---|
| **Tipo** | `bool` (Boolean) |
| **Obrigatório** | Sim |
| **Padrão** | `False` |
| **Valores Permitidos** | `True` ou `False` |
| **Significado** | Indica se a tarefa foi realizada |

**Transições de Estado:**
```
Criação da Tarefa
      │
      ▼
  concluida = False (pendente)
      │
      ├─► Usuário marca como concluída
      │       │
      │       ▼
      │   concluida = True (concluída)
      │
      └─► Permanece pendente (sem ação)
              │
              ▼
          concluida = False (permanente nesta sessão)
```

---

## Ciclo de Vida das Entidades

### Estados Possíveis

```
┌─────────────┐
│   CRIADA    │  Nova tarefa adicionada ao sistema
└──────┬──────┘
       │ (criação bem-sucedida)
       ▼
┌─────────────┐
│  PENDENTE   │  Tarefa aguardando execução
└──────┬──────┘
       │ (usuário marca como concluída)
       ▼
┌─────────────┐
│ CONCLUÍDA   │  Tarefa marcada como realizada
└─────────────┘
       │ (sessão termina)
       ▼
┌─────────────┐
│ DESCARTADA  │  Tarefa removida da memória
└─────────────┘
```

### Transições Permitidas

| Estado Atual | Ação | Estado Próximo | Observações |
|---|---|---|---|
| CRIADA | (Nenhuma) | PENDENTE | Transição automática |
| PENDENTE | Marcar como concluída | CONCLUÍDA | Transição irreversível |
| CONCLUÍDA | (Nenhuma) | CONCLUÍDA | Estado final |
| DESCARTADA | (Nenhuma) | - | Estado terminal (sem retorno) |

### Tempo de Vida
- **Início**: Quando `adicionar_tarefa()` é chamado
- **Fim**: Quando a sessão do Streamlit termina ou `limpar_tarefas()` é invocado
- **Duração**: Limitada à sessão do navegador ativo

---

## Mapeamento de Dados

### Estrutura em Python

```python
from typing import Dict, List

# Tipo de uma Tarefa
Tarefa = Dict[str, object]

# Exemplo de instância
tarefa_exemplo: Tarefa = {
    "titulo": "Estudar Streamlit",
    "concluida": False
}

# Coleção de Tarefas
ListaTarefas = List[Dict[str, object]]

tarefas_exemplo: ListaTarefas = [
    {"titulo": "Tarefa 1", "concluida": False},
    {"titulo": "Tarefa 2", "concluida": True},
    {"titulo": "Tarefa 3", "concluida": False}
]
```

### Serialização JSON

Quando transmitida para a interface ou persistida:

```json
{
  "titulo": "Implementar validação",
  "concluida": false
}
```

### Representação em Memória

```python
class GerenciadorTarefas:
    def __init__(self):
        self._tarefas: List[Dict[str, object]] = []
        # Lista vazia, ready para adicionar tarefas
```

---

## Relacionamentos

### Relacionamentos Diretos

Atualmente, **não existem relacionamentos diretos** entre entidades:

- ❌ Tarefa não tem referência para outra Tarefa
- ❌ Tarefa não tem relação com usuário ou categoria
- ❌ Tarefa não tem dependências de outras tarefas
- ✅ Tarefa é uma entidade independente

### Relacionamentos Implícitos

```
┌──────────────────────────────────┐
│   GerenciadorTarefas             │
│  (1 por sessão do Streamlit)     │
└──────────────────┬───────────────┘
                   │ possui
                   ▼
┌──────────────────────────────────┐
│   List[Tarefa]                   │
│  (0 a N tarefas)                 │
└──────────────────────────────────┘
                   │
              cada elemento
                   │
                   ▼
┌──────────────────────────────────┐
│   Tarefa                         │
│  • titulo: str                   │
│  • concluida: bool               │
└──────────────────────────────────┘
```

### Ciclo de Vida Compartilhado
- Todas as tarefas existem enquanto a sessão Streamlit está ativa
- Quando a sessão encerra, todas as tarefas são perdidas
- Cache do Streamlit mantém a instância do GerenciadorTarefas

---

## Validações e Constraints

### Constraints de Negócio

#### 1. Validação de Título

```python
titulo_limpo = titulo.strip()
if not titulo_limpo:
    raise ValueError("O título da tarefa não pode estar vazio.")
```

| Constraint | Regra | Mensagem de Erro |
|---|---|---|
| **Não vazio** | `len(titulo.strip()) > 0` | "O título da tarefa não pode estar vazio." |
| **Type check** | `isinstance(titulo, str)` | Implícito (Python type hints) |
| **Trim automático** | `.strip()` aplicado antes de validar | - |

#### 2. Validação de Índice (Marcar como Concluída)

```python
if indice < 0 or indice >= len(self._tarefas):
    raise IndexError("Índice da tarefa inválido.")
```

| Constraint | Regra | Mensagem de Erro |
|---|---|---|
| **Índice >= 0** | `indice >= 0` | "Índice da tarefa inválido." |
| **Índice < tamanho** | `indice < len(lista)` | "Índice da tarefa inválido." |

#### 3. Constraints de Estado

| Constraint | Descrição |
|---|---|
| **Imutabilidade de estado final** | Uma tarefa concluída permanece concluída (sem rollback) |
| **Estado inicial** | Toda tarefa inicia com `concluida = False` |
| **Permanência de dados** | Uma tarefa criada permanece na lista até `limpar_tarefas()` |

### Validações de Entrada

#### Validação do Campo Título (UI Level - app.py)

```python
with st.form(key="form_nova_tarefa"):
    nova_tarefa = st.text_input(
        "Nova tarefa",
        placeholder="Digite o nome da tarefa...",
    )
    submit = st.form_submit_button("Adicionar tarefa")

    if submit:
        if nova_tarefa.strip():  # Validação 1: Não vazio
            try:
                gestor.adicionar_tarefa(nova_tarefa)  # Validação 2: No gerenciador
                st.success("Tarefa adicionada com sucesso!")
                st.rerun()
            except ValueError as e:
                st.error(str(e))
        else:
            st.warning("Digite um nome para a tarefa antes de adicionar.")
```

**Camadas de Validação:**
1. **UI Layer**: Verifica se `nova_tarefa.strip()` não está vazio
2. **Business Layer**: Valida novamente no `GerenciadorTarefas`
3. **Feedback**: Exibe mensagens apropriadas ao usuário

---

## Exemplos de Dados

### Exemplo 1: Caso Simples

```python
# Estado inicial
tarefas = []

# Após adicionar uma tarefa
tarefas = [
    {"titulo": "Fazer compras", "concluida": False}
]

# Após marcar como concluída
tarefas = [
    {"titulo": "Fazer compras", "concluida": True}
]
```

### Exemplo 2: Lista Completa

```python
tarefas = [
    {
        "titulo": "Estudar Python",
        "concluida": False
    },
    {
        "titulo": "Fazer exercícios",
        "concluida": True
    },
    {
        "titulo": "Trabalho em grupo",
        "concluida": False
    },
    {
        "titulo": "Reunião com professor",
        "concluida": True
    },
    {
        "titulo": "Projeto final",
        "concluida": False
    }
]
```

### Exemplo 3: Caso de Erro - Título Inválido

```python
# ❌ Tentativa de adicionar tarefa vazia
try:
    gestor.adicionar_tarefa("   ")  # Apenas espaços
except ValueError as e:
    print(f"Erro: {e}")  # Output: Erro: O título da tarefa não pode estar vazio.
```

### Exemplo 4: Caso de Erro - Índice Inválido

```python
tarefas = [
    {"titulo": "Tarefa 1", "concluida": False},
    {"titulo": "Tarefa 2", "concluida": False}
]

# ❌ Tentar marcar tarefa com índice fora do intervalo
try:
    gestor.marcar_como_concluida(5)  # Índice 5 não existe
except IndexError as e:
    print(f"Erro: {e}")  # Output: Erro: Índice da tarefa inválido.
```

### Exemplo 5: Títulos com Caracteres Especiais

```python
# ✅ Todos os exemplos abaixo são válidos
tarefas_validas = [
    {"titulo": "Comprar café @ Starbucks", "concluida": False},
    {"titulo": "Implementar #feature importante", "concluida": False},
    {"titulo": "Reunião 15:30 (sala 201)", "concluida": False},
    {"titulo": "Checar email [IMPORTANTE]", "concluida": False},
    {"titulo": "Pagar conta: R$ 150,00", "concluida": False},
]
```

---

## Tipo de Dados Completo (Python Type Hints)

```python
from typing import TypedDict, List

class Tarefa(TypedDict):
    """Definição formal de uma tarefa usando TypedDict."""
    titulo: str
    concluida: bool

# Tipo para a coleção
ListaTarefas = List[Tarefa]

# Uso em type hints
def adicionar_tarefa(titulo: str) -> Tarefa:
    """Adiciona e retorna uma tarefa."""
    pass

def listar_tarefas() -> ListaTarefas:
    """Retorna lista de tarefas."""
    pass
```

---

## Resumo de Entidades

| Propriedade | Valor |
|---|---|
| **Total de Entidades** | 1 |
| **Nome da Entidade** | Tarefa |
| **Campos Principais** | titulo, concluida |
| **Tipo de Armazenamento** | Memória (List[Dict]) |
| **Relacionamentos** | Nenhum |
| **Constraints Principais** | Título não vazio, Índice válido |
| **Ciclo de Vida** | Sessão do Streamlit |

---

**Última Atualização**: 2026-09-01  
**Versão**: 1.0  
**Autor**: Documentação Técnica
