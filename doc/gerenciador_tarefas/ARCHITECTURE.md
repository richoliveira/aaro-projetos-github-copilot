# Arquitetura Técnica - Gerenciador de Tarefas

## Índice
1. [Visão Geral da Arquitetura](#visão-geral-da-arquitetura)
2. [Arquitetura em Camadas](#arquitetura-em-camadas)
3. [Componentes Principais](#componentes-principais)
4. [Fluxo de Dados](#fluxo-de-dados)
5. [Padrões de Design](#padrões-de-design)
6. [Dependências e Imports](#dependências-e-imports)
7. [Organização de Pacotes](#organização-de-pacotes)
8. [Decisões Arquiteturais](#decisões-arquiteturais)
9. [Escalabilidade e Limitações](#escalabilidade-e-limitações)
10. [Diagrama de Componentes](#diagrama-de-componentes)

---

## Visão Geral da Arquitetura

O Gerenciador de Tarefas segue uma **arquitetura em camadas** com separação clara entre apresentação (UI) e lógica de negócio (Core).

### Princípios Arquiteturais

```
┌────────────────────────────────────────────────┐
│     Princípios Arquiteturais                   │
├────────────────────────────────────────────────┤
│ ✓ Separation of Concerns (SoC)                 │
│   └─ UI separada da lógica de negócio          │
│                                                 │
│ ✓ Single Responsibility Principle (SRP)        │
│   └─ Cada classe tem uma única responsabilidade│
│                                                 │
│ ✓ Dependency Injection (DI)                    │
│   └─ Componentes não criam suas dependências   │
│                                                 │
│ ✓ Interface Segregation                        │
│   └─ API pública clara e minimizada            │
│                                                 │
│ ✓ High Cohesion, Low Coupling                  │
│   └─ Componentes altamente coesos              │
│   └─ Baixa dependência entre módulos           │
└────────────────────────────────────────────────┘
```

---

## Arquitetura em Camadas

### Camada 1: Presentation Layer (UI)

**Arquivo**: `app.py`

**Responsabilidades**:
- Renderizar componentes visuais Streamlit
- Capturar entrada do usuário
- Chamar métodos da camada de negócio
- Exibir feedback e mensagens
- Gerenciar o ciclo de vida da sessão (cache)

**Componentes**:
```python
def main() -> None:
    """Função principal da interface."""
    # Configuração da página
    # Renderização de formulário
    # Renderização de lista
    # Tratamento de cliques/submissões

def renderizar_tarefa(tarefa: dict, indice: int) -> None:
    """Renderiza uma tarefa individual."""
    # Layout com colunas
    # Exibição do título
    # Checkbox interativo

def inicializar_gestor() -> GerenciadorTarefas:
    """Factory com cache para o gerenciador."""
    # Criação/reutilização do gerenciador
```

**Dependências**:
- `streamlit` (framework)
- `GerenciadorTarefas` (camada de negócio)

---

### Camada 2: Business Logic Layer (Core)

**Arquivo**: `gerenciador.py`

**Responsabilidades**:
- Implementar operações CRUD
- Validar dados de entrada
- Manter estado em memória
- Executar regras de negócio
- Lançar exceções apropriadas

**Componentes**:
```python
class GerenciadorTarefas:
    """Gerencia a lógica de tarefas."""
    
    def __init__(self) -> None:
        """Inicializa o gerenciador."""
        # Estado interno
    
    def adicionar_tarefa(self, titulo: str) -> Dict[str, object]:
        """Cria e armazena nova tarefa."""
        # Validação
        # Criação
        # Armazenamento
    
    def listar_tarefas(self) -> List[Dict[str, object]]:
        """Retorna todas as tarefas."""
        # Cópia segura da lista
    
    def marcar_como_concluida(self, indice: int) -> Dict[str, object]:
        """Marca tarefa como concluída."""
        # Validação de índice
        # Atualização de status
    
    def limpar_tarefas(self) -> None:
        """Remove todas as tarefas."""
        # Limpeza de memória
```

**Dependências**:
- `typing` (type hints)
- Python stdlib

**Independência**: Esta camada NÃO depende de Streamlit ou UI

---

### Camada 3: Data/State Layer

**Responsabilidades**:
- Armazenar dados em memória
- Fornecer acesso aos dados
- Manter integridade estrutural

**Implementação**:
```python
self._tarefas: List[Dict[str, object]] = []
```

**Características**:
- Armazenamento em memória (não persistente)
- Lista ordenada (preserva ordem de inserção)
- Sem relacionamentos externos

---

## Componentes Principais

### Componente 1: GerenciadorTarefas (Core)

```
┌────────────────────────────────────────┐
│      GerenciadorTarefas                │
├────────────────────────────────────────┤
│ Atributos:                             │
│  - _tarefas: List[Dict[str, object]]   │
│                                        │
│ Métodos Públicos:                      │
│  + adicionar_tarefa(titulo) → Tarefa   │
│  + listar_tarefas() → List[Tarefa]     │
│  + marcar_como_concluida(indice)       │
│  + limpar_tarefas() → None             │
│                                        │
│ Métodos Privados:                      │
│  - (nenhum em versão atual)            │
└────────────────────────────────────────┘
```

**Responsabilidade**: Gerenciar todo o estado e lógica de tarefas

---

### Componente 2: Interface Streamlit (UI)

```
┌────────────────────────────────────────┐
│      Interface Streamlit               │
├────────────────────────────────────────┤
│ Funções:                               │
│  - main()                              │
│  - inicializar_gestor()                │
│  - renderizar_tarefa()                 │
│                                        │
│ Entrada:                               │
│  - Text input: nova_tarefa             │
│  - Checkboxes: marcar concluída        │
│                                        │
│ Saída:                                 │
│  - Renderização visual                 │
│  - Mensagens de feedback               │
│  - Chamadas ao core                    │
└────────────────────────────────────────┘
```

**Responsabilidade**: Apresentação e interação do usuário

---

### Componente 3: Cache Resource (Factory)

```
┌────────────────────────────────────────┐
│   @st.cache_resource                   │
│   inicializar_gestor()                 │
├────────────────────────────────────────┤
│ Função:                                │
│  - Criar ou recuperar gerenciador      │
│  - Gerenciar ciclo de vida             │
│  - Garantir singleton na sessão        │
└────────────────────────────────────────┘
```

**Responsabilidade**: Lifecycle management e singleton pattern

---

## Fluxo de Dados

### Fluxo 1: Criar Tarefa

```
Usuário Input
│
├─ novo_tarefa_texto
│
▼
Text Input Widget
│
├─ novo_tarefa: str
│
▼
Form Submit
│
├─ submit: bool
│
▼
Validação UI
│ (check .strip() não vazio)
│
├─ nova_tarefa: str (validada)
│
▼
GerenciadorTarefas.adicionar_tarefa()
│
├─ Validação Core
├─ Criação de Tarefa
├─ Armazenamento
│
▼
Feedback (success/error)
│
▼
st.rerun() - Recarregar UI
│
▼
Renderizar Nova Tarefa
│
▼
Usuário Vê Tarefa Adicionada
```

### Fluxo 2: Marcar Concluída

```
Usuário Clica Checkbox
│
▼
Streamlit Detects Change
│
├─ tarefa_concluida: bool
├─ indice: int
│
▼
renderizar_tarefa() Logic
│ (if tarefa_concluida and not tarefa["concluida"])
│
▼
GerenciadorTarefas.marcar_como_concluida(indice)
│
├─ Validação de Índice
├─ Atualização de Status
│
▼
st.rerun() - Recarregar UI
│
▼
Renderizar com Strikethrough
│
▼
Usuário Vê Tarefa Concluída
```

### Fluxo 3: Listar Tarefas

```
main() Executa
│
▼
inicializar_gestor()
│ (@st.cache_resource)
│
├─ Primeira vez: Cria novo
├─ Outras vezes: Reutiliza
│
▼
GerenciadorTarefas.listar_tarefas()
│
├─ Cria cópia da lista
│
▼
tarefas: List[Dict]
│
▼
for indice, tarefa in enumerate(tarefas):
│   renderizar_tarefa(tarefa, indice)
│
▼
Renderizar Cada Tarefa
│ (título + checkbox)
│
▼
Usuário Vê Lista Completa
```

---

## Padrões de Design

### Padrão 1: Model-View (MV)

```
┌──────────────────────────────┐
│      Model (Business Layer)  │
│  - GerenciadorTarefas        │
│  - Estado em memória         │
│  - Lógica de negócio         │
└────────────┬─────────────────┘
             │
             │ (comunica via métodos)
             │
             ▼
┌──────────────────────────────┐
│      View (UI Layer)         │
│  - app.py                    │
│  - Streamlit components      │
│  - Renderização              │
└──────────────────────────────┘
```

**Benefício**: Separação clara entre apresentação e lógica

---

### Padrão 2: Singleton with Lazy Initialization

```python
@st.cache_resource  # Singleton Pattern
def inicializar_gestor() -> GerenciadorTarefas:
    return GerenciadorTarefas()  # Lazy Initialization
```

**Implementação**:
- Primeira chamada: Cria instância
- Chamadas subsequentes: Retorna a mesma

**Benefício**: Uma única instância por sessão Streamlit

---

### Padrão 3: Factory Method

```python
@st.cache_resource
def inicializar_gestor() -> GerenciadorTarefas:
    """Factory para criar gerenciador."""
    return GerenciadorTarefas()
```

**Benefício**: Encapsula criação do objeto, facilita testes

---

### Padrão 4: Command Pattern (Implicit)

```
Ação do Usuário → Método do Gerenciador → Alteração de Estado

adicionar_tarefa()  → operação atômica
marcar_como_concluida()  → operação atômica
limpar_tarefas()  → operação atômica
```

**Benefício**: Cada operação é discreta e testável

---

### Padrão 5: Defensive Copying

```python
def listar_tarefas(self) -> List[Dict[str, object]]:
    return self._tarefas.copy()  # Retorna cópia
```

**Benefício**: Protege estado interno de modificações externas

---

## Dependências e Imports

### Dependências Externas

#### Framework Principal
```
streamlit >= 1.0.0
```

**Uso**:
- `st.set_page_config()` - Configuração da página
- `st.title()` - Exibição de títulos
- `st.form()` - Formulários
- `st.text_input()` - Entrada de texto
- `st.checkbox()` - Checkboxes
- `st.rerun()` - Re-renderização
- `@st.cache_resource` - Cache
- `st.success()`, `st.warning()`, `st.info()` - Mensagens
- `st.columns()` - Layout em colunas
- `st.container()` - Agrupamento
- `st.markdown()` - Markdown/HTML
- `st.subheader()` - Subtítulos

### Dependências Internas

#### Módulo: `__init__.py`

```python
from .gerenciador import GerenciadorTarefas

__all__ = ["GerenciadorTarefas"]
```

**Propósito**: Expor API pública do pacote

#### Módulo: `gerenciador.py`

```python
from __future__ import annotations  # PEP 563 - Postponed annotation evaluation
from typing import Dict, List
```

**Imports**:
- `annotations` - Type hints sem avaliar imediatamente
- `Dict`, `List` - Type hints de coleções

#### Módulo: `app.py`

```python
from __future__ import annotations
import streamlit as st

try:
    from .gerenciador import GerenciadorTarefas
except ImportError:  # pragma: no cover
    from gerenciador import GerenciadorTarefas
```

**Imports**:
- `streamlit as st` - Framework principal
- `GerenciadorTarefas` - Lógica de negócio
- Import condicional para compatibilidade

---

## Organização de Pacotes

### Estrutura de Diretórios

```
app/
├── __init__.py
│   └── (pacote vazio ou com __all__)
│
└── src/
    ├── __init__.py
    │   └── (pacote vazio ou com __all__)
    │
    ├── crud_cadastro/
    │   ├── __init__.py
    │   ├── pessoa.py
    │   ├── cadastro_pessoas.py
    │   └── console_app.py
    │
    └── gerenciador_tarefas/
        ├── __init__.py
        │   └── Exporta: GerenciadorTarefas
        │
        ├── gerenciador.py
        │   └── Classe: GerenciadorTarefas
        │
        └── app.py
            └── Interface Streamlit
```

### Importação

**Uso no Projeto**:
```python
from app.src.gerenciador_tarefas import GerenciadorTarefas
```

**Execução da Aplicação**:
```bash
streamlit run app/src/gerenciador_tarefas/app.py
```

---

## Decisões Arquiteturais

### Decisão 1: Separação UI e Core

**Decisão**: Manter `app.py` e `gerenciador.py` em arquivos separados

**Razão**:
- ✅ Testabilidade: Core pode ser testado sem Streamlit
- ✅ Reutilização: Core pode ser usado em outros contextos
- ✅ Manutenção: Mudanças na UI não afetam lógica
- ✅ Didática: Demonstra padrão MV

**Alternativa Rejeitada**: Tudo em um arquivo
- ❌ Menor reusabilidade
- ❌ Difícil de testar
- ❌ Acoplamento alto

---

### Decisão 2: Estado em Memória

**Decisão**: Armazenar dados em memória, não em banco de dados

**Razão**:
- ✅ Simplicidade: Sem necessidade de configurar BD
- ✅ Didática: Foco em padrões, não infraestrutura
- ✅ Performance: Acesso O(1) a dados
- ✅ Prototipagem: Rápido de desenvolver

**Trade-offs**:
- ❌ Dados perdidos ao desligar aplicação
- ❌ Não escalável para muitos usuários
- ❌ Sem persistência entre sessões

---

### Decisão 3: Estrutura de Dados em Dicts

**Decisão**: Usar `Dict[str, object]` em vez de classe `Tarefa`

**Razão**:
- ✅ Simplicidade: Sem necessidade de classes
- ✅ Flexibilidade: Fácil adicionar campos
- ✅ Didática: Conceitos básicos de Python
- ✅ Compatibilidade: Funciona com JSON

**Trade-offs**:
- ❌ Sem type safety em tempo de desenvolvimento
- ❌ Menos inteligência do IDE
- ❌ Sem validação de campo

---

### Decisão 4: Cache Resource para Singleton

**Decisão**: Usar `@st.cache_resource` em vez de variável global

**Razão**:
- ✅ Integração com Streamlit: Respeita ciclo de vida
- ✅ Segurança: Gerenciado pelo framework
- ✅ Clareza: Intenção explícita no código
- ✅ Testabilidade: Pode ser mockado

**Alternativa Rejeitada**: Variável global
- ❌ Menos claro
- ❌ Difícil de testar
- ❌ Contra padrões do Streamlit

---

### Decisão 5: Sem Banco de Dados

**Decisão**: Não incluir camada de persistência

**Razão**:
- ✅ Simplicidade: Foco em padrões de código
- ✅ Didática: Não distrai com setup de BD
- ✅ Portabilidade: Sem dependências externas
- ✅ Velocidade: Prototipagem rápida

**Quando Adicionar**:
- Quando dados precisam persistir entre sessões
- Quando há múltiplos usuários simultâneos
- Quando volume de dados cresce

---

## Escalabilidade e Limitações

### Limitações Atuais

```
┌────────────────────────────────────────────┐
│         Limitações Técnicas                │
├────────────────────────────────────────────┤
│ • Dados: Armazenamento em memória         │
│   └─ Limitado por RAM disponível          │
│   └─ Perdido ao desligar aplicação        │
│                                            │
│ • Usuários: Uma instância por sessão      │
│   └─ Sem compartilhamento entre usuários  │
│   └─ Sem sincronização entre abas         │
│                                            │
│ • Performance: Sem índices ou otimizações │
│   └─ OK para poucos dados                 │
│   └─ Lento com 100.000+ tarefas           │
│                                            │
│ • Funcionalidades: Modelo binário simples │
│   └─ Sem prioridades                      │
│   └─ Sem datas                            │
│   └─ Sem categorias                       │
│   └─ Sem undo/redo                        │
└────────────────────────────────────────────┘
```

### Caminhos de Escalação

#### 1. Adicionar Persistência
```python
# Camada adicional: Database Layer
class TarefaRepository:
    def salvar(self, tarefa: Tarefa) -> None
    def carregar(self, id: int) -> Tarefa
    def listar_todas(self) -> List[Tarefa]
```

#### 2. Adicionar Autenticação
```python
# Camada adicional: Authentication Layer
class UsuarioService:
    def login(self, usuario: str, senha: str) -> User
    def obter_tarefas_usuario(self, usuario_id: int)
```

#### 3. Adicionar Concorrência
```python
# Padrão: Message Queue ou WebSocket
# Redis, RabbitMQ, etc.
```

#### 4. Adicionar Features
```python
# Novos atributos de Tarefa:
{
    "titulo": str,
    "concluida": bool,
    "prioridade": int,          # Novo
    "data_vencimento": datetime, # Novo
    "categoria": str,            # Novo
    "criada_em": datetime,       # Novo
}
```

---

## Diagrama de Componentes

### Diagrama UML Simplificado

```
┌──────────────────────────────────────────────────────┐
│              App.py (UI/Presentation)                │
│                                                      │
│  - main()                                            │
│  - renderizar_tarefa()                               │
│  - inicializar_gestor() [@cache_resource]            │
└────────────────────┬─────────────────────────────────┘
                     │
                     │ imports
                     │
                     ▼
┌──────────────────────────────────────────────────────┐
│   Gerenciador.py (Business Logic)                    │
│                                                      │
│  class GerenciadorTarefas:                           │
│    - __init__()                                      │
│    - adicionar_tarefa(titulo)                        │
│    - listar_tarefas()                                │
│    - marcar_como_concluida(indice)                   │
│    - limpar_tarefas()                                │
│                                                      │
│  Internal State:                                     │
│    - _tarefas: List[Dict[str, object]]               │
└──────────────────────────────────────────────────────┘
                     │
                     │ contém
                     │
                     ▼
┌──────────────────────────────────────────────────────┐
│   Tarefa (Data Structure)                            │
│                                                      │
│   {                                                  │
│     "titulo": str,                                   │
│     "concluida": bool                                │
│   }                                                  │
└──────────────────────────────────────────────────────┘


   External Dependencies:
   
   ┌──────────────────────────────────────────┐
   │           Streamlit                      │
   │  (Framework de UI)                       │
   └──────────────────────────────────────────┘
           ▲
           │ uses
           │
      app.py
```

### Diagrama de Fluxo Arquitetural

```
User Interaction (Browser)
        │
        ▼
┌───────────────────┐
│  Streamlit UI     │  (Presentation Layer)
│  - Components     │
│  - Input Capture  │
└────────┬──────────┘
         │ calls
         ▼
┌───────────────────────────────┐
│  GerenciadorTarefas           │ (Business Logic Layer)
│  - Validação                  │
│  - Operações CRUD             │
│  - Regras de Negócio          │
└────────┬──────────────────────┘
         │ manages
         ▼
┌───────────────────┐
│  _tarefas: List   │ (Data Layer)
│  [{"titulo":"...",│
│    "concluida":..}]
└───────────────────┘
        │
        │ persists (em memória)
        │
        ▼
   Session Memory
 (Cache Resource)
```

---

## Resumo Arquitetural

| Aspecto | Implementação |
|---|---|
| **Padrão** | Model-View com camadas |
| **Princípios** | SoC, SRP, DI, Interface Segregation |
| **Separação** | UI (`app.py`) vs Core (`gerenciador.py`) |
| **Estado** | Memória, uma instância por sessão |
| **Cache** | `@st.cache_resource` para singleton |
| **Persistência** | Nenhuma (em memória) |
| **Escalabilidade** | Limitada (prototipagem/demo) |
| **Testabilidade** | Alta (core independente) |
| **Manutenibilidade** | Alta (código simples e separado) |

---

**Última Atualização**: 2026-09-01  
**Versão**: 1.0  
**Autor**: Documentação Técnica
