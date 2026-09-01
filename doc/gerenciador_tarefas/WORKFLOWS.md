# Fluxos de Negócio - Gerenciador de Tarefas

## Índice
1. [Visão Geral dos Workflows](#visão-geral-dos-workflows)
2. [Workflow: Criar Tarefa](#workflow-criar-tarefa)
3. [Workflow: Listar Tarefas](#workflow-listar-tarefas)
4. [Workflow: Marcar como Concluída](#workflow-marcar-como-concluída)
5. [Workflow: Limpar Tarefas](#workflow-limpar-tarefas)
6. [Fluxo Principal da Aplicação](#fluxo-principal-da-aplicação)
7. [Cenários e Casos de Uso](#cenários-e-casos-de-uso)
8. [Tratamento de Erros](#tratamento-de-erros)

---

## Visão Geral dos Workflows

O Gerenciador de Tarefas implementa um conjunto de workflows que cobrem todas as operações CRUD (Create, Read, Update, Delete) e operações auxiliares.

### Workflows Principais

```
┌─────────────────────────────────────────────────┐
│        Operações CRUD do Sistema                │
├─────────────────────────────────────────────────┤
│ 1. CREATE  → Criar Tarefa                       │
│ 2. READ    → Listar Tarefas                     │
│ 3. UPDATE  → Marcar como Concluída              │
│ 4. DELETE  → Limpar Tarefas                     │
│ 5. ADMIN   → Inicializar Sistema                │
└─────────────────────────────────────────────────┘
```

### Diagrama de Fluxo de Alto Nível

```
┌──────────────────────────────────────────────┐
│    Usuário Inicia Aplicação Streamlit        │
└────────────┬─────────────────────────────────┘
             │
             ▼
    ┌────────────────────────┐
    │ Inicializar Gerenciador │ (@st.cache_resource)
    └────────────┬───────────┘
                 │
                 ▼
    ┌────────────────────────────────────┐
    │    Interface Renderizada            │
    │ • Formulário de Entrada             │
    │ • Lista de Tarefas                  │
    └────────────┬───────────────────────┘
                 │
          ┌──────┴──────────┬──────────────────┬─────────────┐
          │                 │                  │             │
          ▼                 ▼                  ▼             ▼
    ┌──────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────┐
    │  Criar   │  │ Listar (READ)│  │   Marcar     │  │ Limpar   │
    │ Tarefa   │  │              │  │ Concluída    │  │ Tarefas  │
    └────┬─────┘  └──────────────┘  └─────┬────────┘  └──────────┘
         │                                 │
         └──────────────┬──────────────────┘
                        │
                        ▼
              ┌──────────────────┐
              │  Persistir Estado │
              │   em Memória      │
              └──────────────────┘
                        │
                        ▼
              ┌──────────────────┐
              │   Rerender UI     │
              │  (st.rerun)       │
              └──────────────────┘
```

---

## Workflow: Criar Tarefa

### Operação: `adicionar_tarefa(titulo: str) -> Dict[str, object]`

### Descrição
Este workflow cria uma nova tarefa e a adiciona à lista do gerenciador.

### Pré-condições
- A aplicação está rodando
- A sessão do Streamlit está ativa
- O gerenciador foi inicializado

### Passos

```
1. Usuário insere título na caixa de texto
2. Usuário clica no botão "Adicionar tarefa"
3. Sistema valida se o título não está vazio
4. Sistema cria novo dicionário de tarefa
5. Sistema adiciona tarefa à lista interna
6. Sistema retorna a tarefa criada
7. Sistema exibe mensagem de sucesso
8. Interface é recarregada (st.rerun)
9. Novo estado é renderizado
```

### Fluxo Detalhado

```python
# Fluxo no app.py (UI Layer)
with st.form(key="form_nova_tarefa"):
    nova_tarefa = st.text_input("Nova tarefa", placeholder="...")
    submit = st.form_submit_button("Adicionar tarefa")
    
    if submit:
        ┌─────────────────────────────────────┐
        │ 1. Validação UI (Camada Apresentação)│
        └─────────────────────────────────────┘
            if nova_tarefa.strip():
                ┌─────────────────────────────────────┐
                │ 2. Chamada ao Gerenciador           │
                └─────────────────────────────────────┘
                    gestor.adicionar_tarefa(nova_tarefa)
                    
                        ┌────────────────────────────────────┐
                        │ 3. Validação Negócio (Core Logic)  │
                        └────────────────────────────────────┘
                            titulo_limpo = titulo.strip()
                            if not titulo_limpo:
                                raise ValueError(...)
                        
                        ┌────────────────────────────────────┐
                        │ 4. Criação da Tarefa               │
                        └────────────────────────────────────┘
                            tarefa = {
                                "titulo": titulo_limpo,
                                "concluida": False
                            }
                        
                        ┌────────────────────────────────────┐
                        │ 5. Persistência em Memória         │
                        └────────────────────────────────────┘
                            self._tarefas.append(tarefa)
                        
                        ┌────────────────────────────────────┐
                        │ 6. Retorno da Tarefa Criada        │
                        └────────────────────────────────────┘
                            return tarefa

                ┌─────────────────────────────────────┐
                │ 7. Feedback ao Usuário              │
                └─────────────────────────────────────┘
                    st.success("Tarefa adicionada com sucesso!")
                
                ┌─────────────────────────────────────┐
                │ 8. Recarregar Interface             │
                └─────────────────────────────────────┘
                    st.rerun()
```

### Entrada (Input)

| Campo | Tipo | Obrigatório | Exemplo |
|---|---|---|---|
| `titulo` | `str` | Sim | "Estudar Python" |

### Saída (Output)

```python
{
    "titulo": "Estudar Python",
    "concluida": False
}
```

### Exceções Possíveis

| Exceção | Condição | Mensagem |
|---|---|---|
| `ValueError` | Título vazio ou apenas espaços | "O título da tarefa não pode estar vazio." |

### Pós-condições
- A tarefa foi adicionada à lista interna do gerenciador
- A contagem de tarefas aumentou em 1
- A interface foi recarregada e o usuário vê a nova tarefa
- O campo de entrada foi limpo

### Exemplo de Execução

```python
gestor = GerenciadorTarefas()  # Estado: []

tarefa = gestor.adicionar_tarefa("Fazer exercício")
# Estado: [{"titulo": "Fazer exercício", "concluida": False}]
# Retorno: {"titulo": "Fazer exercício", "concluida": False}
```

---

## Workflow: Listar Tarefas

### Operação: `listar_tarefas() -> List[Dict[str, object]]`

### Descrição
Este workflow retorna uma cópia da lista completa de tarefas cadastradas.

### Pré-condições
- O gerenciador foi inicializado
- A sessão está ativa

### Passos

```
1. Usuário carrega a página ou interface é recarregada
2. Sistema chama listar_tarefas()
3. Sistema cria uma cópia da lista interna
4. Sistema retorna a cópia
5. Interface itera sobre cada tarefa
6. Para cada tarefa, renderiza um componente visual
7. Exibe status (concluída ou não) visualmente
```

### Fluxo Detalhado

```
┌─────────────────────────┐
│ Renderizar Interface    │
│ (main() function)       │
└────────────┬────────────┘
             │
             ▼
    ┌────────────────────────────┐
    │ tarefas = gestor.           │
    │ listar_tarefas()           │
    └────────────┬───────────────┘
                 │
         ┌───────▼────────┐
         │ Retorna cópia  │
         │ da lista       │
         └───────┬────────┘
                 │
                 ▼
    ┌────────────────────────────────┐
    │ if not tarefas:                │
    │   st.info("Nenhuma tarefa...")│
    │   return                       │
    │ else:                          │
    │   renderizar cada tarefa       │
    └────────────────────────────────┘
                 │
      ┌──────────┴──────────┐
      │                     │
      ▼                     ▼
   Tarefa 1            Tarefa 2
   (renderizar)        (renderizar)
   ...                 ...
```

### Entrada (Input)

Nenhuma (sem parâmetros)

### Saída (Output)

```python
[
    {"titulo": "Tarefa 1", "concluida": False},
    {"titulo": "Tarefa 2", "concluida": True},
    {"titulo": "Tarefa 3", "concluida": False}
]
```

### Pós-condições
- Uma cópia da lista é retornada (não a lista original)
- O estado interno não é modificado
- A lista é renderizada na interface

### Exemplo

```python
gestor = GerenciadorTarefas()
gestor.adicionar_tarefa("Tarefa 1")
gestor.adicionar_tarefa("Tarefa 2")

tarefas = gestor.listar_tarefas()
# Retorna: [
#     {"titulo": "Tarefa 1", "concluida": False},
#     {"titulo": "Tarefa 2", "concluida": False}
# ]

# Modificar a cópia não afeta o gerenciador
tarefas[0]["titulo"] = "Modificada"
print(gestor.listar_tarefas()[0]["titulo"])  # "Tarefa 1" (inalterada)
```

---

## Workflow: Marcar como Concluída

### Operação: `marcar_como_concluida(indice: int) -> Dict[str, object]`

### Descrição
Este workflow marca uma tarefa específica como concluída e retorna a tarefa atualizada.

### Pré-condições
- A tarefa existe na lista (índice válido)
- A tarefa ainda não foi concluída (opcional - permite re-marcar)
- O gerenciador foi inicializado

### Passos

```
1. Usuário clica no checkbox "OK" ao lado de uma tarefa
2. Sistema obtém o índice da tarefa
3. Sistema valida se o índice é válido
4. Sistema marca a tarefa como concluída
5. Sistema retorna a tarefa atualizada
6. Interface exibe feedback visual
7. Interface é recarregada (st.rerun)
8. Usuário vê a tarefa com strikethrough
```

### Fluxo Detalhado (UI e Core)

```python
# UI Layer (app.py)
def renderizar_tarefa(tarefa: dict, indice: int) -> None:
    col_titulo, col_checkbox = st.columns([4, 1])
    
    with col_checkbox:
        tarefa_concluida = st.checkbox(
            "OK",
            key=f"check_{indice}",
            value=tarefa["concluida"],
            on_change=lambda: None
        )
        
        if tarefa_concluida and not tarefa["concluida"]:
            ┌──────────────────────────────┐
            │ 1. Usuário marcou checkbox   │
            └──────────────┬───────────────┘
                           │
                           ▼
            ┌──────────────────────────────┐
            │ 2. Chamar gerenciador        │
            └──────────────┬───────────────┘
                gestor.marcar_como_concluida(indice)
                           │
            ┌──────────────▼───────────────┐
            │ 3. Business Logic (Core)     │
            └──────────────┬───────────────┘
                if indice < 0 or indice >= len(self._tarefas):
                    raise IndexError(...)
                           │
                           ▼
            ┌──────────────────────────────┐
            │ 4. Atualizar Status          │
            └──────────────┬───────────────┘
                tarefa = self._tarefas[indice]
                tarefa["concluida"] = True
                           │
                           ▼
            ┌──────────────────────────────┐
            │ 5. Retornar Tarefa Atualizada│
            └──────────────┬───────────────┘
                return tarefa
                           │
                           ▼
            ┌──────────────────────────────┐
            │ 6. Recarregar Interface      │
            └──────────────┬───────────────┘
                st.rerun()
                           │
                           ▼
            ┌──────────────────────────────┐
            │ 7. Renderizar com Strikethrough
            │    <s>Tarefa 1</s>           │
            └──────────────────────────────┘
```

### Entrada (Input)

| Parâmetro | Tipo | Descrição |
|---|---|---|
| `indice` | `int` | Posição da tarefa na lista (0-based) |

### Saída (Output)

```python
{
    "titulo": "Tarefa Concluída",
    "concluida": True
}
```

### Exceções Possíveis

| Exceção | Condição | Mensagem |
|---|---|---|
| `IndexError` | Índice < 0 ou índice >= len(lista) | "Índice da tarefa inválido." |

### Validações

```python
# Validação de índice
if indice < 0 or indice >= len(self._tarefas):
    raise IndexError("Índice da tarefa inválido.")
```

### Pós-condições
- A tarefa no índice especificado agora tem `concluida = True`
- Não é possível "desmarcar" uma tarefa (sem operação inversa)
- A interface mostra a tarefa com strikethrough

### Exemplo

```python
gestor = GerenciadorTarefas()
gestor.adicionar_tarefa("Tarefa Importante")  # índice 0

# Antes
print(gestor.listar_tarefas()[0])
# {"titulo": "Tarefa Importante", "concluida": False}

# Marcar como concluída
gestor.marcar_como_concluida(0)

# Depois
print(gestor.listar_tarefas()[0])
# {"titulo": "Tarefa Importante", "concluida": True}
```

---

## Workflow: Limpar Tarefas

### Operação: `limpar_tarefas() -> None`

### Descrição
Este workflow remove todas as tarefas da memória, limpando o estado do gerenciador.

### Pré-condições
- O gerenciador foi inicializado
- Existem tarefas na lista (ou lista está vazia)

### Passos

```
1. Usuário solicita limpeza (via código ou API)
2. Sistema chama limpar_tarefas()
3. Sistema remove todas as tarefas
4. Memória é liberada
5. Estado interno fica vazio
```

### Fluxo

```
┌──────────────────────────┐
│ gestor.limpar_tarefas()  │
└────────────┬─────────────┘
             │
             ▼
    ┌────────────────────┐
    │ self._tarefas.     │
    │ clear()            │
    └────────────┬───────┘
                 │
                 ▼
    ┌────────────────────┐
    │ Estado: []         │
    │ (vazio)            │
    └────────────────────┘
```

### Entrada (Input)

Nenhuma (sem parâmetros)

### Saída (Output)

Nenhuma (retorna `None`)

### Pós-condições
- A lista interna fica vazia
- `len(listar_tarefas()) == 0`
- Todas as tarefas foram descartadas

### Exemplo

```python
gestor = GerenciadorTarefas()
gestor.adicionar_tarefa("Tarefa 1")
gestor.adicionar_tarefa("Tarefa 2")

print(len(gestor.listar_tarefas()))  # 2

gestor.limpar_tarefas()

print(len(gestor.listar_tarefas()))  # 0
```

### Uso Típico
- Limpeza de estado entre testes
- Reset da aplicação
- Liberação de memória (raramente necessário em sessão curta)

---

## Fluxo Principal da Aplicação

### Sequência Completa: Usuário Inicia até Interação

```
Tempo │ Ator/Sistema        │ Ação
─────┼──────────────────────┼────────────────────────────────
 0:00 │ Usuário             │ Abre navegador e acessa localhost:8501
     │                     │
 0:05 │ Streamlit           │ Detecta app.py como entry point
     │ (Main Thread)       │
     │                     │
 0:10 │ @st.cache_resource │ Verifica se gestor já foi criado
     │ (inicializar_gestor)│ (primeira vez = criar)
     │                     │
 0:15 │ GerenciadorTarefas  │ __init__() chamado
     │ (__init__)          │ self._tarefas = []
     │                     │
 0:20 │ app.main()          │ Renderizar interface
     │                     │
 0:25 │ st.set_page_config()│ Configurar página
     │                     │
 0:30 │ st.title()          │ Exibir "Gerenciador de Tarefas"
     │                     │
 0:35 │ st.form()           │ Exibir formulário
     │ st.text_input()     │ Campo de entrada
     │ st.form_submit..()  │ Botão "Adicionar tarefa"
     │                     │
 0:40 │ renderizar_tarefa() │ Iterar sobre tarefas (lista vazia)
     │ if not tarefas      │ Exibir st.info("Nenhuma tarefa...")
     │                     │
 0:50 │ Usuário             │ Digita "Estudar" no campo
 1:00 │ Usuário             │ Clica em "Adicionar tarefa"
     │                     │
 1:05 │ app.py (if submit)  │ Valida: nova_tarefa.strip()
     │                     │ Resultado: "Estudar" (válido)
     │                     │
 1:10 │ gestor.             │ Valida novamente no core
     │ adicionar_tarefa()  │ Cria tarefa
     │                     │ Adiciona à lista
     │                     │
 1:15 │ st.success()        │ Exibe mensagem de sucesso
     │                     │
 1:20 │ st.rerun()          │ Recarrega a página
     │                     │
 1:25 │ app.main()          │ Re-executa toda a função main()
     │ (novo script run)   │
     │                     │
 1:30 │ @st.cache_resource │ Retorna instância em cache
     │                     │ (reutiliza o gerenciador)
     │                     │
 1:35 │ renderizar_tarefa() │ Agora há 1 tarefa na lista
     │ for indice, tarefa  │ Renderiza com checkbox
     │ in enumerate()      │
     │                     │
 1:40 │ Usuário             │ Vê a tarefa adicionada
     │                     │
 1:45 │ Usuário             │ Clica no checkbox "OK"
     │                     │
 1:50 │ app.py              │ on_change callback dispara
     │ (checkbox change)   │ marcar_como_concluida(0)
     │                     │
 1:55 │ st.rerun()          │ Recarrega a página
     │                     │
 2:00 │ Usuário             │ Vê a tarefa com strikethrough
```

---

## Cenários e Casos de Uso

### Caso de Uso 1: Fluxo Básico (Happy Path)

**Ator**: Usuário
**Pré-condições**: Aplicação está rodando
**Passos**:
1. Usuário vê lista vazia
2. Usuário digita "Fazer compras"
3. Usuário clica em "Adicionar tarefa"
4. Tarefa aparece na lista
5. Usuário clica no checkbox
6. Tarefa é marcada como concluída
7. Tarefa aparece com strikethrough

**Pós-condições**: Tarefa está na lista como concluída

---

### Caso de Uso 2: Adicionar Múltiplas Tarefas

**Ator**: Usuário
**Pré-condições**: Aplicação está rodando

| Passo | Ação do Usuário | Sistema | Resultado |
|---|---|---|---|
| 1 | Digita "Tarefa 1" | Valida | Adiciona com sucesso |
| 2 | Digita "Tarefa 2" | Valida | Adiciona com sucesso |
| 3 | Digita "Tarefa 3" | Valida | Adiciona com sucesso |
| - | - | Renderiza | Lista mostra 3 tarefas |

---

### Caso de Uso 3: Validação de Entrada Inválida

**Ator**: Usuário
**Pré-condições**: Aplicação está rodando

| Passo | Entrada | Validação UI | Sistema | Resultado |
|---|---|---|---|---|
| 1 | "" (vazio) | Falha | Não chama core | Warning: "Digite um nome..." |
| 2 | "   " (só espaços) | Falha | Não chama core | Warning: "Digite um nome..." |

---

### Caso de Uso 4: Tentar Marcar Tarefa com Índice Inválido

**Ator**: Sistema (via teste ou manupilação direta)
**Pré-condições**: Lista com 2 tarefas

```python
try:
    gestor.marcar_como_concluida(10)  # Índice inválido
except IndexError as e:
    print(f"Erro capturado: {e}")
```

**Resultado**: Exceção `IndexError` é lançada

---

## Tratamento de Erros

### Hierarquia de Exceções

```
Exception
│
├── ValueError
│   └── Título vazio ou inválido
│       └── "O título da tarefa não pode estar vazio."
│
└── IndexError
    └── Índice fora do intervalo
        └── "Índice da tarefa inválido."
```

### Tratamento no Core (gerenciador.py)

```python
def adicionar_tarefa(self, titulo: str) -> Dict[str, object]:
    """Lança ValueError se título for inválido."""
    titulo_limpo = titulo.strip()
    if not titulo_limpo:
        raise ValueError("O título da tarefa não pode estar vazio.")
    # ...

def marcar_como_concluida(self, indice: int) -> Dict[str, object]:
    """Lança IndexError se índice for inválido."""
    if indice < 0 or indice >= len(self._tarefas):
        raise IndexError("Índice da tarefa inválido.")
    # ...
```

### Tratamento na UI (app.py)

```python
with st.form(key="form_nova_tarefa"):
    nova_tarefa = st.text_input("Nova tarefa", placeholder="...")
    submit = st.form_submit_button("Adicionar tarefa")

    if submit:
        if nova_tarefa.strip():
            try:
                gestor.adicionar_tarefa(nova_tarefa)
                st.success("Tarefa adicionada com sucesso!")
                st.rerun()
            except ValueError as e:
                st.error(str(e))
        else:
            st.warning("Digite um nome para a tarefa antes de adicionar.")
```

---

## Resumo de Workflows

| Workflow | Tipo | Entradas | Saídas | Exceções |
|---|---|---|---|---|
| Criar Tarefa | CREATE | titulo: str | Tarefa | ValueError |
| Listar Tarefas | READ | - | List[Tarefa] | - |
| Marcar Concluída | UPDATE | indice: int | Tarefa | IndexError |
| Limpar Tarefas | DELETE | - | None | - |

---

**Última Atualização**: 2026-09-01  
**Versão**: 1.0  
**Autor**: Documentação Técnica
